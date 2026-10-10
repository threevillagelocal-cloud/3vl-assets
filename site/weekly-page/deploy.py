"""Publish the web version of a Three Village Weekly issue at /weekly (widget "3VL Page Weekly").
Source: 3vl-site-guard/data/weekly/<date>/subscriber.html (the staged email, same for every reader).
    python site/weekly-page/deploy.py 2026-10-09"""
import datetime, io, json, os, re, sys, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "share-img"))
from bdkey import key

H = {"X-Api-Key": key(), "User-Agent": "Mozilla/5.0 3VL", "Content-Type": "application/x-www-form-urlencoded"}
API = "https://www.threevillagelocal.com/api/v2/"
NAME, SLUG = "3VL Page Weekly", "weekly"


def call(method, path, data=None):
    body = urllib.parse.urlencode(data).encode() if data is not None else None
    return json.loads(urllib.request.urlopen(urllib.request.Request(API + path, data=body, headers=H, method=method), timeout=60).read())


def build(date, src=None):
    src = src or os.path.join(HERE, "..", "..", "..", "3vl-site-guard", "data", "weekly", date, "subscriber.html")
    h = io.open(src, encoding="utf-8").read()
    style = re.search(r"<style>(.*?)</style>", h, re.S).group(1)
    body = re.search(r"<body[^>]*>(.*)</body>", h, re.S).group(1)
    body = re.sub(r'^\s*<div style="display:none[^"]*">.*?</div>', "", body, count=1, flags=re.S)   # inbox preheader
    body = body.replace("utm_medium=email", "utm_medium=web")
    body = re.sub(r"[^<>]*Reply &ldquo;unsubscribe&rdquo; to stop\.", "", body)
    nice = datetime.date.fromisoformat(date).strftime("%B %-d, %Y") if os.name != "nt" else datetime.date.fromisoformat(date).strftime("%B %#d, %Y")
    head = ('<div class="tvw-top"><div><p class="tvw-k">Three Village Weekly</p><h1>This week&rsquo;s issue &middot; %s</h1>'
            '<p class="tvw-s">The local email neighbors read every Friday: things to do, new businesses and local news.</p></div>'
            '<a class="tvw-b" href="/newsletter?utm_source=weekly-web&amp;utm_medium=web&amp;utm_campaign=weekly-%s">Get it free every Friday</a></div>' % (nice, date))
    html = '<div id="tvw">%s<div class="tvw-mail">%s</div></div>' % (head, body)
    css = (style + "#tvw{max-width:760px;margin:0 auto;padding:6px 0 30px;font-family:'Radio Canada','tvl-rc',system-ui,sans-serif}"
           "#tvw .tvw-top{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:14px;margin:8px 0 18px}"
           "#tvw .tvw-k{margin:0;font-size:12px;font-weight:800;letter-spacing:.16em;text-transform:uppercase;color:#1f5fae}"
           "#tvw h1{margin:4px 0 4px;font-size:clamp(24px,4vw,32px);line-height:1.15;color:#13233a}"
           "#tvw .tvw-s{margin:0;font-size:15px;color:#4a586b}"
           "#tvw .tvw-b{display:inline-block;padding:12px 22px;border-radius:999px;background:#13233a;color:#fff!important;font-weight:700;text-decoration:none!important}"
           "#tvw .tvw-mail{border-radius:18px;overflow:hidden;box-shadow:0 10px 30px rgba(19,35,58,.08)}"
           "#tvw .tvw-mail img{max-width:100%;height:auto}")
    for s in (html, css):
        assert "\\" not in s
    return html, css, nice


def main(date, src=None):
    html, css, nice = build(date, src)
    w = {"widget_data": html, "widget_style": css}
    found = call("GET", "data_widgets/get?property=widget_name&property_value=" + urllib.parse.quote(NAME)).get("message")
    found = [x for x in found if x.get("widget_name") == NAME] if isinstance(found, list) else []
    if found:
        print("widget", call("PUT", "data_widgets/update", dict(w, widget_id=found[0]["widget_id"])).get("status"))
    else:
        print("widget create", call("POST", "data_widgets/create", dict(w, widget_name=NAME, widget_viewport="front")).get("status"))
    page = {"content": "[widget=%s]" % NAME, "content_css": " ", "enable_hero_section": "0",
            "title": "Three Village Weekly: This Week's Issue (%s) | Three Village Local" % nice,
            "meta_desc": "Read this week's Three Village Weekly: things to do this weekend, new local businesses and news from Setauket, Stony Brook and Port Jefferson.",
            "facebook_title": "Three Village Weekly: %s" % nice}
    ex = call("GET", "list_seo/get?property=filename&property_value=" + SLUG).get("message")
    ex = [x for x in ex if x.get("filename") == SLUG] if isinstance(ex, list) else []
    r = call("PUT", "list_seo/update", dict(page, seo_id=ex[0]["seo_id"])) if ex else call("POST", "list_seo/create", dict(page, seo_type="content", filename=SLUG, nickname="Three Village Weekly (web)"))
    print("page", r.get("status"), r.get("message") if r.get("status") != "success" else "")
    try:
        call("POST", "website_settings/refreshCache", {})
    except Exception as e:
        print("cache:", e)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)   # optional 2nd arg: corrected copy of the issue
