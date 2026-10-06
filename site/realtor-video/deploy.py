"""Publish /agent-spotlight (realtor video landing page): widget "3VL Page Agent Spotlight" (page.html / page.css)
on a content web page, plus the share-image redirect.
    python site/realtor-video/deploy.py"""
import json, os, sys, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "share-img"))
from bdkey import key

H = {"X-Api-Key": key(), "User-Agent": "Mozilla/5.0 3VL", "Content-Type": "application/x-www-form-urlencoded"}
API = "https://www.threevillagelocal.com/api/v2/"
NAME = "3VL Page Agent Spotlight"
SLUG = "agent-spotlight"
TITLE = "Agent Spotlight Video: Calling Three Village Real Estate Agents | Three Village Local"
DESC = ("Local real estate agents: answer five fun questions about the Three Village market on video and be featured on "
        "Three Village Local's website, app, social media and weekly email. Deadline Friday, October 23.")
SHARE = "share/agent-spotlight-v1.webp"
SHARE_TARGET = "https://threevillagelocal-cloud.github.io/3vl-share/site/realtor-video/house-1600.webp"


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
    red = call("GET", "redirect_301/get?property=old_filename&property_value=" + urllib.parse.quote(SHARE)).get("message")
    if not (isinstance(red, list) and red):
        print("redirect", call("POST", "redirect_301/create", {"old_filename": SHARE, "new_filename": SHARE_TARGET}).get("status"))
    fields = dict(title=TITLE, meta_desc=DESC, facebook_title="Be one of the faces of Three Village real estate",
                  facebook_desc=DESC, facebook_image="/" + SHARE, content="[widget=%s]" % NAME)
    pg = call("GET", "list_seo/get?property=filename&property_value=" + SLUG).get("message")
    pg = [x for x in pg if x.get("filename") == SLUG] if isinstance(pg, list) else []
    if pg:
        print("page", pg[0]["seo_id"], call("PUT", "list_seo/update", dict(fields, seo_id=pg[0]["seo_id"])).get("status"))
    else:
        r = call("POST", "list_seo/create", dict(fields, seo_type="content", filename=SLUG, nickname="Agent Spotlight video (realtors)"))
        print("page create", r.get("status"), r["message"].get("seo_id") if isinstance(r.get("message"), dict) else r.get("message"))
    try:
        print("cache", call("POST", "website_settings/refreshCache", {}).get("status"))
    except Exception as e:
        print("cache refresh failed (refresh in BD admin):", e)


if __name__ == "__main__":
    main()
