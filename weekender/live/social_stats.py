"""Prints 3VL's own Facebook Page + Instagram follower counts (for the Business Insider). Token from IG_TOKEN, never printed."""
import json, os, urllib.request, urllib.parse, urllib.error
T = os.environ["IG_TOKEN"].strip()
def get(path, fields, tok=T):
    u = "https://graph.facebook.com/v21.0/%s?%s" % (path, urllib.parse.urlencode({"fields": fields, "access_token": tok}))
    try:
        with urllib.request.urlopen(u, timeout=30) as r: return json.load(r)
    except urllib.error.HTTPError as e: return {"error": json.load(e).get("error", {}).get("message")}
print("IG:", get("17841472800565482", "username,followers_count,media_count"))
page = get("106710385522764", "name,fan_count,followers_count,access_token")
ptok = page.pop("access_token", None)
print("FB page:", page)
if ptok and "followers_count" not in page:
    print("FB page (page token):", get("106710385522764", "name,fan_count,followers_count", ptok))
