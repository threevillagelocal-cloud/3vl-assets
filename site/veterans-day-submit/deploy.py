"""Veterans Day 2026 submission page (owner 11/1/2026). Widgets 83 (hero) + honor intro, forms 347 + 348, web page /veterans-day-submit.
    python site/veterans-day-submit/deploy.py"""
import json, os, sys, urllib.parse, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "share-img"))
import bdkey
K = bdkey.key()
B = "https://www.threevillagelocal.com"
SLUG = "veterans-day-submit"


def api(method, path, data=None):
    req = urllib.request.Request(B + path, method=method, headers={"X-Api-Key": K, "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded"}, data=urllib.parse.urlencode(data).encode() if data else None)
    return json.loads(urllib.request.urlopen(req, timeout=60).read())


def rd(n):
    return open(os.path.join(HERE, n), encoding="utf-8").read()


def widget(name, html):
    r = api("GET", "/api/v2/data_widgets/get?property=widget_name&property_value=%s" % urllib.parse.quote(name))
    rows = r.get("message") if isinstance(r.get("message"), list) else []
    if rows:
        api("PUT", "/api/v2/data_widgets/update", {"widget_id": rows[0]["widget_id"], "widget_data": html})
        return rows[0]["widget_id"]
    return api("POST", "/api/v2/data_widgets/create", {"widget_name": name, "widget_data": html, "widget_type": "Widget"})["message"]["widget_id"]


w1 = widget("3VL Page Veterans Day Submit", rd("widget.html"))
w2 = widget("3VL Veterans Day Honor Intro", rd("honor.html"))
page = {
    "seo_type": "content", "filename": SLUG, "nickname": "Veterans Day Submissions",
    "title": "Honoring Our Neighbors Who Served | Veterans Day 2026 | Three Village Local",
    "meta_desc": "Veteran-owned business or Veterans Day special in Setauket, Stony Brook or Port Jefferson? Submit it free for our Veterans Day feature, or add a local veteran to our community thank-you.",
    "facebook_title": "Honoring our neighbors who served",
    "facebook_desc": "Veteran business owners, Veterans Day specials and the local veterans in your life. Be part of our community Veterans Day feature. Free to be included.",
    "facebook_image": "https://www.threevillagelocal.com/share/veterans-day-submit-v3.jpg",
    "content": "[widget=3VL Page Veterans Day Submit][form=veterans_day_submission][widget=3VL Veterans Day Honor Intro][form=veterans_thank_you]",
    "content_css": rd("page.css"),
}
r = api("GET", "/api/v2/list_seo/get?property=filename&property_value=%s" % SLUG)
rows = r.get("message") if isinstance(r.get("message"), list) else []
if rows:
    page["seo_id"] = rows[0]["seo_id"]
    print(api("PUT", "/api/v2/list_seo/update", page)["status"], "page", rows[0]["seo_id"])
else:
    print(api("POST", "/api/v2/list_seo/create", page)["status"], "page created")
print("widgets", w1, w2)
