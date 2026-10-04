"""Read-only: list the Three Village Local account's latest posts (type, time, link, caption start). Token never printed."""
import json, os, urllib.request, urllib.parse, urllib.error
T = os.environ.get("IG_TOKEN", "").strip(); ME, V = "17841472800565482", "v21.0"
def get(path, params):
    url = "https://graph.facebook.com/%s/%s?%s" % (V, path, urllib.parse.urlencode(dict(params, access_token=T)))
    try:
        with urllib.request.urlopen(url, timeout=30) as r: return json.load(r)
    except urllib.error.HTTPError as e:
        return {"ERROR": json.load(e).get("error", {}).get("message", "")[:200]}
d = get(ME + "/media", {"fields": "media_type,media_product_type,timestamp,permalink,caption,like_count,comments_count", "limit": 5})
for m in d.get("data", []):
    print(m.get("timestamp"), m.get("media_product_type"), m.get("media_type"), m.get("permalink"), "likes", m.get("like_count"), "|", (m.get("caption") or "")[:120].replace("\n", " "))
    t = get(m["id"] + "/tags", {"fields": "username"})
print(d.get("ERROR", ""))
s = get(ME + "/stories", {"fields": "media_type,timestamp,permalink"})
print("STORIES:", s)
