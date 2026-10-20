"""Publish the services page: widget "3VL Page Services" (page.html / page.css / page.js) + BD form [form=services_inquiry]
(the widget script moves the form into its booking card).
    python site/services-page/deploy.py            -> hidden preview at /preview-services (noindex)
    python site/services-page/deploy.py --live     -> /services (indexable)"""
import json, os, sys, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "share-img"))
from bdkey import key

H = {"X-Api-Key": key(), "User-Agent": "Mozilla/5.0 3VL", "Content-Type": "application/x-www-form-urlencoded"}
API = "https://www.threevillagelocal.com/api/v2/"
NAME = "3VL Page Services"
LIVE = "--live" in sys.argv
SLUG = "services" if LIVE else "preview-services"
TITLE = "Websites, Google, AI Search & Marketing for Local Businesses | Three Village Local"
DESC = ("Websites, Google profile setup, AI search, video and drone for local businesses, built by the Three Village Local team "
        "and launched in front of 100,000+ neighbors. Members save, VIPs save the most.")
FB_TITLE = "We build it. Then we tell the whole town."
FB_IMAGE = "https://threevillagelocal-cloud.github.io/3vl-share/site/back-office/hero-1080.webp"


def call(method, path, data=None):
    body = urllib.parse.urlencode(data).encode() if data is not None else None
    return json.loads(urllib.request.urlopen(urllib.request.Request(API + path, data=body, headers=H, method=method), timeout=60).read())


def rd(f):
    s = open(os.path.join(HERE, f), encoding="utf-8").read()
    assert "\\" not in s, f + " has a backslash (BD strips them)"
    return s


def main():
    w = {"widget_data": rd("page.html"), "widget_style": rd("page.css"), "widget_javascript": rd("page.js")}
    found = call("GET", "data_widgets/get?property=widget_name&property_value=" + urllib.parse.quote(NAME)).get("message")
    found = [x for x in found if x.get("widget_name") == NAME] if isinstance(found, list) else []
    if found:
        print("widget", found[0]["widget_id"], call("PUT", "data_widgets/update", dict(w, widget_id=found[0]["widget_id"])).get("status"))
    else:
        r = call("POST", "data_widgets/create", dict(w, widget_name=NAME, widget_viewport="front"))
        print("widget create", r.get("status"), (r.get("message") or {}).get("widget_id"))
    page = {"content": "[widget=%s][form=services_inquiry]" % NAME, "content_css": " ", "enable_hero_section": "0",
            "title": TITLE, "meta_desc": DESC, "facebook_title": FB_TITLE, "facebook_desc": DESC,
            "facebook_image": FB_IMAGE,
            "show_form": "0" if LIVE else "1"}
    ex = call("GET", "list_seo/get?property=filename&property_value=" + SLUG).get("message")
    ex = [x for x in ex if x.get("filename") == SLUG] if isinstance(ex, list) else []
    if ex:
        r = call("PUT", "list_seo/update", dict(page, seo_id=ex[0]["seo_id"]))
        print("page update", ex[0]["seo_id"], r.get("status"))
    else:
        r = call("POST", "list_seo/create", dict(page, seo_type="content", filename=SLUG))
        print("page create", r.get("status"), (r.get("message") or {}).get("seo_id") if isinstance(r.get("message"), dict) else r.get("message"))
    try:
        call("POST", "website_settings/refreshCache", {})
    except Exception as e:
        print("cache:", e)
    print("https://www.threevillagelocal.com/" + SLUG)


if __name__ == "__main__":
    main()
