"""One-off connectivity test for Instagram Business Discovery (reads public posts of other business accounts).
Token comes from the IG_TOKEN env var (GitHub secret) and is never printed."""
import json, os, sys, time, urllib.request, urllib.parse, urllib.error
from datetime import datetime, timezone
TOKEN = os.environ.get("IG_TOKEN", "").strip()
ME = "17841472800565482"  # Three Village Local IG business account
V = "v21.0"
if not TOKEN:
    sys.exit("IG_TOKEN missing")

def get(path, params):
    params = dict(params, access_token=TOKEN)
    url = "https://graph.facebook.com/%s/%s?%s" % (V, path, urllib.parse.urlencode(params))
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.load(r), None
    except urllib.error.HTTPError as e:
        try: err = json.load(e).get("error", {})
        except Exception: err = {"message": str(e)}
        return None, "%s (code %s/%s)" % (err.get("message", "?")[:160], err.get("code"), err.get("error_subcode"))

me, err = get(ME, {"fields": "username,name,followers_count,media_count"})
print("SELF:", me if me else "ERROR " + err)
if not me:
    sys.exit(1)

accts = json.load(open(os.path.join(os.path.dirname(__file__), "ig_accounts.json"), encoding="utf-8"))
now = datetime.now(timezone.utc)
ok = fail = 0
rows = []
for a in accts:
    h = a["ig"]
    fields = "business_discovery.username(%s){username,name,followers_count,media_count,media.limit(1){timestamp}}" % h
    d, err = get(ME, {"fields": fields})
    if d:
        bd = d["business_discovery"]
        m = (bd.get("media") or {}).get("data") or []
        last = m[0]["timestamp"] if m else None
        age = (now - datetime.strptime(last, "%Y-%m-%dT%H:%M:%S%z")).days if last else None
        rows.append((a["name"], h, "OK", bd.get("media_count"), age))
        ok += 1
    else:
        rows.append((a["name"], h, "FAIL " + err, None, None))
        fail += 1
    time.sleep(0.4)

print("\nRESULT: %d readable, %d not readable (of %d)\n" % (ok, fail, len(accts)))
for r in rows:
    print("%-38s @%-32s %s  posts=%s  last_post_days_ago=%s" % r)

print("\nSAMPLE LATEST POSTS:")
for h in ["countrycornerlongisland", "madiranthewinebar_eastsetauket", "tommysplaceportjeff_", "ixchelmexicancuisine", "djsclamshackstonybrook"]:
    fields = "business_discovery.username(%s){media.limit(3){timestamp,media_type,permalink,caption}}" % h
    d, err = get(ME, {"fields": fields})
    print("\n@" + h)
    if not d:
        print("  ERROR", err); continue
    for p in d["business_discovery"].get("media", {}).get("data", []):
        cap = (p.get("caption") or "").replace("\n", " ")[:220]
        print("  %s %s %s\n    %s" % (p["timestamp"][:16], p["media_type"], p["permalink"], cap))
