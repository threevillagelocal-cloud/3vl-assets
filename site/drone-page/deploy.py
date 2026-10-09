"""Publish /droneservices (realtor drone booking page, owner 10/9/2026): widget "3VL Page Drone" (page.html / page.css /
page.js) + the BD form [form=drone_services] (the widget script moves the form into its booking card).
    python site/drone-page/deploy.py"""
import json, os, sys, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "share-img"))
from bdkey import key

H = {"X-Api-Key": key(), "User-Agent": "Mozilla/5.0 3VL", "Content-Type": "application/x-www-form-urlencoded"}
API = "https://www.threevillagelocal.com/api/v2/"
NAME = "3VL Page Drone"
SEO_ID = 41
TITLE = "Drone Photography for Realtors on Long Island | $120 Listing Package | Three Village Local"
DESC = ("Aerial photos and video for your listings from a local FAA-certified, insured drone pilot. The Listing Package, typically $199, now $120: "
        "5-10 edited aerial photos plus video clips. Book online for Setauket, Stony Brook, Port Jefferson and all of Suffolk and Nassau.")


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
        print("widget create", call("POST", "data_widgets/create", dict(w, widget_name=NAME, widget_viewport="front")).get("status"))
    r = call("PUT", "list_seo/update", {"seo_id": SEO_ID, "content": "[widget=%s][form=drone_services]" % NAME, "content_css": " ",
                                        "enable_hero_section": "0", "title": TITLE, "meta_desc": DESC,
                                        "facebook_title": "Drone Photography for Realtors: $120 Listing Package", "facebook_desc": DESC,
                                        "facebook_image": "https://threevillagelocal-cloud.github.io/3vl-share/site/drone/hero-poster.webp"})
    print("page", r.get("status"), r.get("message") if r.get("status") != "success" else "")
    try:
        call("POST", "website_settings/refreshCache", {})
    except Exception as ex:
        print("cache:", ex)


if __name__ == "__main__":
    main()
