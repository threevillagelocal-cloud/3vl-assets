"""Push post.html: hidden preview page /preview-thanksgiving-traditions (noindex) + blog DRAFT (unpublished until the owner OKs).
Copy tg.css / tg.js to 3vl-share/thanksgiving-blog and push 3vl-share first.     python push.py"""
import json, os, re, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
IDS = os.path.join(HERE, "ids.json")
ids = json.load(open(IDS)) if os.path.exists(IDS) else {}
WIDGET = "3VL Preview Thanksgiving Traditions"
SLUG = "preview-thanksgiving-traditions"
TITLE = "Thanksgiving in Three Village: Our Traditions, Our Tables and Our Local Favorites"
OG = "https://threevillagelocal-cloud.github.io/3vl-share/thanksgiving-blog/thanksgiving-traditions-share-a1.jpg"
DESC = ("How Setauket, Stony Brook and Port Jefferson do Thanksgiving: local traditions, who is open on Thanksgiving Day, pies and catering, "
        "food drives, Black Friday, Small Business Saturday and the Santa Parade.")


def key():
    cfg = json.load(open(os.path.expanduser("~/.claude.json"), encoding="utf-8"))
    def find(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "brilliant-directories" and isinstance(v, dict):
                    return v
                r = find(v)
                if r:
                    return r
    a = find(cfg).get("args", [])
    return a[a.index("--api-key") + 1]


K = key()


def bd(m, path, d=None):
    req = urllib.request.Request("https://www.threevillagelocal.com" + path, data=urllib.parse.urlencode(d).encode() if d else None, method=m,
                                 headers={"X-Api-Key": K, "Content-Type": "application/x-www-form-urlencoded", "User-Agent": "3VL"})
    return json.loads(urllib.request.urlopen(req, timeout=120).read())


html = open(os.path.join(HERE, "post.html"), encoding="utf-8").read()
js = re.search(r'<script src="[^"]+tg\.js" defer></script>', html).group(0)
found = bd("GET", "/api/v2/data_widgets/get?property=widget_name&property_value=" + urllib.parse.quote(WIDGET)).get("message")
found = [x for x in found if x.get("widget_name") == WIDGET] if isinstance(found, list) else []
wd = {"widget_data": html.replace(js, ""), "widget_javascript": js}
if found:
    print("widget", bd("PUT", "/api/v2/data_widgets/update", dict(wd, widget_id=found[0]["widget_id"])).get("status"))
else:
    print("widget create", bd("POST", "/api/v2/data_widgets/create", dict(wd, widget_name=WIDGET, widget_viewport="front")).get("status"))
if not ids.get("page"):
    r = bd("POST", "/api/v2/list_seo/create", {"seo_type": "content", "filename": SLUG, "nickname": "Preview: Thanksgiving traditions blog",
                                               "title": "Thanksgiving in Three Village | Three Village Local", "content": "[widget=%s]" % WIDGET,
                                               "show_form": 1, "facebook_image": OG})
    ids["page"] = r["message"]["seo_id"]; print("page", ids["page"])
if not ids.get("post"):
    r = bd("POST", "/api/v2/data_posts/create", {"user_id": 5, "data_id": 14, "data_type": 20, "post_status": 0, "post_title": TITLE, "post_content": html,
                                                 "post_image": OG, "original_image_url": OG, "auto_image_import": 1,
                                                 "post_meta_title": "Thanksgiving in Three Village: Traditions & Local Favorites",
                                                 "post_meta_description": DESC})
    ids["post"] = r["message"]["post_id"]; print("draft post", ids["post"], r["message"].get("post_filename"))
else:
    print("draft post", bd("PUT", "/api/v2/data_posts/update", {"post_id": ids["post"], "post_content": html}).get("status"))
json.dump(ids, open(IDS, "w"))
try:
    bd("POST", "/api/v2/website_settings/refreshCache", {})
except Exception as ex:
    print("cache:", ex)
print("preview: https://www.threevillagelocal.com/" + SLUG)
