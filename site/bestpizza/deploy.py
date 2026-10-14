"""Best Pizza 2026 poll page /bestpizza (owner 10/14/2026). Form = best_pizza (form_id 342, website_contacts).
    python site/bestpizza/deploy.py"""
import json, os, sys, urllib.parse, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "share-img"))
from bdkey import key
H = {"X-Api-Key": key(), "User-Agent": "Mozilla/5.0 3VL", "Content-Type": "application/x-www-form-urlencoded"}
API = "https://www.threevillagelocal.com/api/v2/"
SLUG = "bestpizza"
DESC = "Vote for the best pizza in Three Village: Setauket, Stony Brook and Port Jefferson. Pick your favorite, one vote per person."

def call(method, path, data=None):
    body = urllib.parse.urlencode(data).encode() if data is not None else None
    return json.loads(urllib.request.urlopen(urllib.request.Request(API + path, data=body, headers=H, method=method), timeout=60).read())

def rd(f):
    s = open(os.path.join(HERE, f), encoding="utf-8").read()
    assert "\\" not in s, f + " has a backslash (BD strips them)"
    return s

page = {"content": rd("content.html"), "content_css": rd("page.css"), "enable_hero_section": "0",
        "title": "Vote: Best Pizza in Three Village 2026 | Three Village Local", "meta_desc": DESC,
        "facebook_title": "Who makes the best pizza in Three Village? Vote now", "facebook_desc": DESC}
SHARE_SRC = "https://threevillagelocal-cloud.github.io/3vl-share/site/bestpizza/share-v2.jpg"
red = call("GET", "redirect_301/get?property=old_filename&property_value=share/bestpizza-v2.jpg").get("message")
if not (isinstance(red, list) and red):
    print("redirect", call("POST", "redirect_301/create", {"old_filename": "share/bestpizza-v2.jpg", "new_filename": SHARE_SRC}).get("status"))
page["facebook_image"] = "https://www.threevillagelocal.com/share/bestpizza-v2.jpg"
ex = call("GET", "list_seo/get?property=filename&property_value=" + SLUG).get("message")
ex = [x for x in ex if x.get("filename") == SLUG] if isinstance(ex, list) else []
r = call("PUT", "list_seo/update", dict(page, seo_id=ex[0]["seo_id"])) if ex else \
    call("POST", "list_seo/create", dict(page, seo_type="content", filename=SLUG, nickname="Best Pizza Poll 2026"))
print("page", r.get("status"), r.get("message") if r.get("status") != "success" else (r.get("message") or {}).get("seo_id", ex[0]["seo_id"] if ex else ""))
try:
    call("POST", "website_settings/refreshCache", {})
except Exception as e:
    print("cache:", e)
