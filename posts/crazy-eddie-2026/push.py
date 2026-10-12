"""Push post.html to the site: the preview page widget ("3VL Preview Crazy Eddie" on /preview-crazy-eddie, noindex)
and the blog draft (post 690, stays unpublished until the owner says go).    python push.py"""
import json, os, re, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
POST_ID, WIDGET = "690", "3VL Preview Crazy Eddie"


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
    return json.loads(urllib.request.urlopen(req, timeout=90).read())


html = open(os.path.join(HERE, "post.html"), encoding="utf-8").read()
js = re.search(r'<script src="[^"]+eddie\.js" defer></script>', html).group(0)
w = bd("GET", "/api/v2/data_widgets/get?property=widget_name&property_value=" + urllib.parse.quote(WIDGET))["message"][0]
print("widget", bd("PUT", "/api/v2/data_widgets/update", {"widget_id": w["widget_id"], "widget_data": html.replace(js, ""), "widget_javascript": js}).get("status"))
print("draft post", bd("PUT", "/api/v2/data_posts/update", {"post_id": POST_ID, "post_content": html}).get("status"))

