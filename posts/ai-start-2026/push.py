"""Push post.html to the site: preview widget "3VL Preview 5 Ways AI" on /preview-5-ways-ai-long-island-business (noindex)
and the blog DRAFT (unpublished until the owner says go).   python push.py   (ids saved to push_ids.json)"""
import json, os, re, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
WIDGET, SLUG = "3VL Preview 5 Ways AI", "preview-5-ways-ai-long-island-business"
TITLE = "5 Ways AI Can Help Your Long Island Business This Week (No Tech Skills Needed)"
OG = "https://threevillagelocal-cloud.github.io/3vl-share/ai-5-ways/ai-5-ways-li-business-og.jpg"
IDS = os.path.join(HERE, "push_ids.json")


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


ids = json.load(open(IDS)) if os.path.exists(IDS) else {}
html = open(os.path.join(HERE, "post.html"), encoding="utf-8").read()
js = re.search(r'<script src="[^"]+ais.js[^"]*" defer></script>', html).group(0)

found = bd("GET", "/api/v2/data_widgets/get?property=widget_name&property_value=" + urllib.parse.quote(WIDGET)).get("message")
found = [x for x in found if x.get("widget_name") == WIDGET] if isinstance(found, list) else []
wd = {"widget_data": html.replace(js, ""), "widget_javascript": js}
if found:
    print("widget", bd("PUT", "/api/v2/data_widgets/update", dict(wd, widget_id=found[0]["widget_id"])).get("status"))
else:
    print("widget create", bd("POST", "/api/v2/data_widgets/create", dict(wd, widget_name=WIDGET, widget_viewport="front")).get("status"))

if not ids.get("page"):
    r = bd("POST", "/api/v2/list_seo/create", {"seo_type": "content", "filename": SLUG, "nickname": "Preview: 5 Ways AI",
                                               "title": TITLE + " | Three Village Local", "content": "[widget=%s]" % WIDGET,
                                               "show_form": 1, "facebook_image": OG})
    ids["page"] = r["message"]["seo_id"]; print("page", ids["page"])

if not ids.get("post"):
    r = bd("POST", "/api/v2/data_posts/create", {"user_id": 43, "data_id": 14, "data_type": 20, "post_status": 0,
                                                 "post_title": TITLE, "post_content": html, "post_image": OG, "original_image_url": OG,
                                                 "auto_image_import": 1,
                                                 "post_meta_title": "5 Ways AI Can Help Your Long Island Business This Week | Three Village Local",
                                                 "post_meta_description": "No tech skills needed. 5 easy ways Long Island small businesses can use AI this week: answer customers 24/7, draft replies, one dashboard, get found by AI and stay safe."})
    ids["post"] = r["message"]["post_id"]; print("draft post", ids["post"])
else:
    print("draft post", bd("PUT", "/api/v2/data_posts/update", {"post_id": ids["post"], "post_content": html}).get("status"))
json.dump(ids, open(IDS, "w"))
print("preview: https://www.threevillagelocal.com/" + SLUG)
