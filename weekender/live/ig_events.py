"""Scan local business Instagram accounts for upcoming event posts (owner 10/13/2026: "comb social media" for events).
Reads ig_accounts.json + IG_HANDLES (comma list, e.g. members' handles) + posts that tag @threevillagelocal.
Keeps posts from the last IG_DAYS days whose caption matches IG_WORDS (regex); saves igpull/events.json + each post's image.
Read-only. Token comes from the IG_TOKEN env var and is never printed."""
import json, os, re, time, urllib.request, urllib.parse, urllib.error
from datetime import datetime, timezone, timedelta

TOKEN = os.environ.get("IG_TOKEN", "").strip()
ME, V = "17841472800565482", "v21.0"
DAYS = int(os.environ.get("IG_DAYS", "40"))
WORDS = re.compile(os.environ.get("IG_WORDS") or r"hallo|spook|haunt|trick.or.treat|trunk.or.treat|costume|pumpkin|ghost|witch|zombie|monster|boo\b|creep|fright|scare|dia de|day of the dead|hocus|horror|candy", re.I)
OUT = "igpull"
os.makedirs(OUT, exist_ok=True)


def get(path, params):
    url = "https://graph.facebook.com/%s/%s?%s" % (V, path, urllib.parse.urlencode(dict(params, access_token=TOKEN)))
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        try:
            return {"ERROR": json.load(e).get("error", {}).get("message", "")[:160]}
        except Exception:
            return {"ERROR": str(e)}


def keep(m, who, since):
    cap = m.get("caption") or ""
    ts = m.get("timestamp", "")
    if not ts or datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S%z") < since or not WORDS.search(cap):
        return None
    img = m.get("media_url") if m.get("media_type") != "VIDEO" else m.get("thumbnail_url")
    if m.get("media_type") == "CAROUSEL_ALBUM" and not img:
        kids = (m.get("children") or {}).get("data") or []
        img = kids[0].get("media_url") if kids else None
    fn = ""
    if img:
        fn = "%s_%s.jpg" % (re.sub(r"\W", "", who), m["id"])
        try:
            urllib.request.urlretrieve(img, os.path.join(OUT, fn))
        except Exception:
            fn = ""
    return {"handle": who, "time": ts, "link": m.get("permalink"), "caption": cap, "image": fn, "type": m.get("media_type")}


def main():
    since = datetime.now(timezone.utc) - timedelta(days=DAYS)
    accts = json.load(open(os.path.join(os.path.dirname(__file__), "ig_accounts.json"), encoding="utf-8"))
    handles = ([] if os.environ.get("IG_ONLY") else [a["ig"] for a in accts]) + [h.strip().lstrip("@") for h in os.environ.get("IG_HANDLES", "").split(",") if h.strip()]
    seen, hits, errs = set(), [], []
    fields = "caption,timestamp,permalink,media_type,media_url,thumbnail_url,children{media_url}"
    for h in handles:
        if h.lower() in seen:
            continue
        seen.add(h.lower())
        d = get(ME, {"fields": "business_discovery.username(%s){media.limit(30){%s}}" % (h, fields)})
        if "ERROR" in d:
            errs.append((h, d["ERROR"])); continue
        for m in ((d.get("business_discovery") or {}).get("media") or {}).get("data", []):
            k = keep(m, h, since)
            if k:
                hits.append(k)
        time.sleep(0.4)
    # posts that tag @threevillagelocal (businesses tagging us)
    t = get(ME + "/tags", {"fields": "username," + fields, "limit": 50})
    for m in t.get("data", []):
        k = keep(m, m.get("username", "tagged"), since)
        if k:
            k["tagged_us"] = True
            hits.append(k)
    hits.sort(key=lambda x: x["time"], reverse=True)
    json.dump({"scanned": len(seen), "errors": errs, "hits": hits}, open(os.path.join(OUT, "events.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("scanned %d accounts, %d matching posts, %d errors" % (len(seen), len(hits), len(errs)))


if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("IG_TOKEN missing")
    main()
