"""Push post.html to the site: the preview page widget ("3VL Preview Snow Shed" on /preview-snow-shed, noindex)
and the blog draft (stays unpublished until approved).    python push.py"""
import json, os, re, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
WIDGET = "3VL Preview Snow Shed"
POST_ID = open(os.path.join(HERE, "post_id.txt")).read().strip() if os.path.exists(os.path.join(HERE, "post_id.txt")) else ""


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


if __name__ == "__main__":
    # snow.css / snow.js are served from 3vl-share (GitHub Pages); copy them there, then commit + push 3vl-share before running this
    import shutil
    for f in ("snow.css", "snow.js"):
        shutil.copy(os.path.join(HERE, f), os.path.join(HERE, "..", "..", "..", "3vl-share", "snow-shed", f))
    html = open(os.path.join(HERE, "post.html"), encoding="utf-8").read()
    js = re.search(r'<script src="[^"]+snow\.js" defer></script>', html).group(0)
    found = bd("GET", "/api/v2/data_widgets/get?property=widget_name&property_value=" + urllib.parse.quote(WIDGET))["message"]
    if found:
        print("widget", bd("PUT", "/api/v2/data_widgets/update", {"widget_id": found[0]["widget_id"], "widget_data": html.replace(js, ""), "widget_javascript": js}).get("status"))
    else:
        r = bd("POST", "/api/v2/data_widgets/create", {"widget_name": WIDGET, "widget_data": html.replace(js, ""), "widget_javascript": js})
        print("widget created", r.get("status"), (r.get("message") or {}).get("widget_id"))
    if POST_ID:
        print("draft post", bd("PUT", "/api/v2/data_posts/update", {"post_id": POST_ID, "post_content": html}).get("status"))
