"""Manual helper: download recent public photos from business Instagram accounts (Business Discovery) for article artwork.
Usage (workflow ig-test.yml, script=ig_photos.py, handles in IG_HANDLES env or default list). Output: igpull/ (uploaded as a
workflow artifact, never committed). Credit the account when a photo is used."""
import json, os, sys, urllib.request, urllib.parse, urllib.error
ME, V = "17841472800565482", "v21.0"
T = os.environ.get("IG_TOKEN", "").strip()
H = [h.strip() for h in (os.environ.get("IG_HANDLES") or "").split(",") if h.strip()]
OUT = "igpull"; os.makedirs(OUT, exist_ok=True)
idx = []
for h in H:
    q = "business_discovery.username(%s){username,name,media.limit(20){id,timestamp,media_type,media_url,permalink,caption,children{media_type,media_url}}}" % h
    try:
        d = json.load(urllib.request.urlopen("https://graph.facebook.com/%s/%s?%s" % (V, ME, urllib.parse.urlencode({"fields": q, "access_token": T})), timeout=40))
    except urllib.error.HTTPError as e:
        print("NO", h, json.load(e).get("error", {}).get("message", "")[:90]); continue
    bd = d.get("business_discovery", {}); n = 0
    for m in bd.get("media", {}).get("data", []):
        url = m.get("media_url") if m.get("media_type") == "IMAGE" else None
        if m.get("media_type") == "CAROUSEL_ALBUM":
            kids = [c for c in m.get("children", {}).get("data", []) if c.get("media_type") == "IMAGE"]
            url = kids[0]["media_url"] if kids else None
        if not url: continue
        fn = "%s/%s_%s.jpg" % (OUT, h, m["id"])
        try: open(fn, "wb").write(urllib.request.urlopen(url, timeout=40).read()); n += 1
        except Exception as ex: print("dl fail", h, ex); continue
        idx.append({"handle": h, "file": fn, "date": m.get("timestamp", "")[:10], "link": m.get("permalink"), "caption": (m.get("caption") or "")[:300]})
    print("OK", h, bd.get("name"), n, "photos")
json.dump(idx, open(OUT + "/index.json", "w"), indent=1)
