"""Push post.html to the site: preview widget "3VL Preview AI Find" on /preview-can-ai-find-your-business (noindex, carries the
real ai_report form) and the blog DRAFT (unpublished until the owner says go).   python push.py
First run creates the widget, the preview page and the draft (ids saved to push_ids.json)."""
import json, os, re, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
WIDGET, SLUG = "3VL Preview AI Find", "preview-can-ai-find-your-business"
TITLE = "Can AI Find Your Business? How Small Local Businesses Can Even the AI Playing Field"
OG = "https://threevillagelocal-cloud.github.io/3vl-share/ai-find/can-ai-find-your-business-og.jpg"
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
js = re.search(r'<script src="[^"]+aif\.js" defer></script>', html).group(0)

found = bd("GET", "/api/v2/data_widgets/get?property=widget_name&property_value=" + urllib.parse.quote(WIDGET)).get("message")
found = [x for x in found if x.get("widget_name") == WIDGET] if isinstance(found, list) else []
wd = {"widget_data": html.replace(js, ""), "widget_javascript": js}
if found:
    print("widget", bd("PUT", "/api/v2/data_widgets/update", dict(wd, widget_id=found[0]["widget_id"])).get("status"))
else:
    print("widget create", bd("POST", "/api/v2/data_widgets/create", dict(wd, widget_name=WIDGET, widget_viewport="front")).get("status"))

if not ids.get("page"):
    r = bd("POST", "/api/v2/list_seo/create", {"seo_type": "content", "filename": SLUG, "nickname": "Preview: Can AI find your business",
                                               "title": TITLE + " | Three Village Local", "content": "[widget=%s][form=ai_report]" % WIDGET,
                                               "show_form": 1, "facebook_image": OG})
    ids["page"] = r["message"]["seo_id"]; print("page", ids["page"])

if not ids.get("post"):
    r = bd("POST", "/api/v2/data_posts/create", {"user_id": ids.get("user_id", 5), "data_id": 14, "data_type": 20, "post_status": 0,
                                                 "post_title": TITLE, "post_content": html, "post_image": OG, "original_image_url": OG,
                                                 "auto_image_import": 1,
                                                 "post_meta_title": "Can AI Find Your Business? | Three Village Local",
                                                 "post_meta_description": "AI assistants now recommend local businesses by name. Here is how small businesses in Setauket, Stony Brook and Port Jefferson can get found by AI, plus a free AI visibility report."})
    ids["post"] = r["message"]["post_id"]; print("draft post", ids["post"])
else:
    print("draft post", bd("PUT", "/api/v2/data_posts/update", {"post_id": ids["post"], "post_content": html}).get("status"))
json.dump(ids, open(IDS, "w"))
print("preview: https://www.threevillagelocal.com/" + SLUG)
