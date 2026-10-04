"""Read-only check: can the IG token publish to the Three Village Local account? Posts NOTHING. Token never printed."""
import json, os, urllib.request, urllib.parse, urllib.error
T = os.environ.get("IG_TOKEN", "").strip()
ME, V = "17841472800565482", "v21.0"
def get(path, params):
    url = "https://graph.facebook.com/%s/%s?%s" % (V, path, urllib.parse.urlencode(dict(params, access_token=T)))
    try:
        with urllib.request.urlopen(url, timeout=30) as r: return json.load(r)
    except urllib.error.HTTPError as e:
        try: return {"ERROR": json.load(e).get("error", {}).get("message", "")[:200]}
        except Exception: return {"ERROR": str(e)}
print("publishing limit:", get(ME + "/content_publishing_limit", {"fields": "config,quota_usage"}))
print("permissions:", [p["permission"] for p in get("me/permissions", {}).get("data", []) if p.get("status") == "granted"])
