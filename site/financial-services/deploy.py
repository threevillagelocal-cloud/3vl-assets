"""Publish the /financial-services hub: widget "3VL Page Financial Services Hub" (page.html / page.css), placed on web page 51
(the Financial Services category page, empty on purpose since 10/5/2026; members live in 4 group categories).
    python site/financial-services/deploy.py"""
import json, os, sys, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "share-img"))
from bdkey import key

H = {"X-Api-Key": key(), "User-Agent": "Mozilla/5.0 3VL", "Content-Type": "application/x-www-form-urlencoded"}
API = "https://www.threevillagelocal.com/api/v2/"
NAME = "3VL Page Financial Services Hub"


def call(method, path, data=None):
    body = urllib.parse.urlencode(data).encode() if data is not None else None
    return json.loads(urllib.request.urlopen(urllib.request.Request(API + path, data=body, headers=H, method=method), timeout=60).read())


def rd(f):
    return open(os.path.join(HERE, f), encoding="utf-8").read()


def main():
    w = dict(widget_data=rd("page.html"), widget_style=rd("page.css"), widget_javascript="")
    found = call("GET", "data_widgets/get?property=widget_name&property_value=" + urllib.parse.quote(NAME)).get("message")
    found = [x for x in found if x.get("widget_name") == NAME] if isinstance(found, list) else []
    if found:
        print("widget update", found[0]["widget_id"], call("PUT", "data_widgets/update", dict(w, widget_id=found[0]["widget_id"])).get("status"))
    else:
        r = call("POST", "data_widgets/create", dict(w, widget_name=NAME, widget_viewport="front"))
        print("widget create", r["message"]["widget_id"], r.get("status"))
    print("page 51", call("PUT", "list_seo/update", dict(seo_id=51, content="[widget=%s]" % NAME, custom_html_placement="3")).get("status"))
    try:
        print("cache", call("POST", "website_settings/refreshCache", {}).get("status"))
    except Exception as e:
        print("cache refresh failed (refresh in BD admin):", e)


if __name__ == "__main__":
    main()
