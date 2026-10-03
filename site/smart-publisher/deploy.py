"""Publish the /smart-publisher page: widget "3VL Page Smart Publisher" (page.html / page.css / page.js) + the members-only
web page that holds only shortcodes (the BD editor strips designs, so the design lives in the widget).
    python site/smart-publisher/deploy.py"""
import json, os, sys, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "share-img"))
from bdkey import key

H = {"X-Api-Key": key(), "User-Agent": "Mozilla/5.0 3VL", "Content-Type": "application/x-www-form-urlencoded"}
API = "https://www.threevillagelocal.com/api/v2/"
NAME = "3VL Page Smart Publisher"


def call(method, path, data=None):
    body = urllib.parse.urlencode(data).encode() if data is not None else None
    return json.loads(urllib.request.urlopen(urllib.request.Request(API + path, data=body, headers=H, method=method), timeout=60).read())


def rd(f):
    return open(os.path.join(HERE, f), encoding="utf-8").read()


def main():
    w = dict(widget_data=rd("page.html"), widget_style=rd("page.css"), widget_javascript=rd("page.js"))
    found = call("GET", "data_widgets/get?property=widget_name&property_value=" + urllib.parse.quote(NAME)).get("message")
    found = [x for x in found if x.get("widget_name") == NAME] if isinstance(found, list) else []
    if found:
        wid = found[0]["widget_id"]
        print("widget update", wid, call("PUT", "data_widgets/update", dict(w, widget_id=wid)).get("status"))
    else:
        r = call("POST", "data_widgets/create", dict(w, widget_name=NAME, widget_viewport="front"))
        wid = r["message"]["widget_id"]
        print("widget create", wid, r.get("status"))
    pg = call("GET", "list_seo/get?property=filename&property_value=smart-publisher").get("message")
    page = dict(seo_type="content", filename="smart-publisher", nickname="Smart Publisher (members)",
                title="3VL Smart Publisher | Three Village Local", h1="", meta_desc="Members: turn your event, special or news into a polished page on Three Village Local.",
                content="[widget=%s][form=smart_publisher][form=smart_publisher_review]" % NAME, content_footer="members_only", show_form="1")
    if isinstance(pg, list) and pg:
        print("page update", pg[0]["seo_id"], call("PUT", "list_seo/update", dict(page, seo_id=pg[0]["seo_id"])).get("status"))
    else:
        r = call("POST", "list_seo/create", page)
        print("page create", r.get("status"), (r.get("message") or {}).get("seo_id") if isinstance(r.get("message"), dict) else r.get("message"))


if __name__ == "__main__":
    main()
