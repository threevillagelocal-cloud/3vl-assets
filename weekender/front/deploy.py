"""Publish the front layout to its hidden preview page.
    python weekender/front/deploy.py <full sha>
Builds build(..., front=True) at <sha>, warms the CDN, creates/updates widget "3VL Page Home Preview" and page /preview-home (noindex),
and writes the body to ../3vl-site-guard/post-sources/widget-<id>-3vl-page-home-preview.html (the guard backup; the nightly job keeps it current)."""
import json, os, re, sys, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
WK = os.path.dirname(HERE)
sys.path.insert(0, WK)
sys.path.insert(0, os.path.join(WK, "..", "site", "share-img"))
from bdkey import key            # noqa: E402
import build as B                # noqa: E402
import nightly as N              # noqa: E402
import nowhome_build as nhb      # noqa: E402

H = {"X-Api-Key": key(), "User-Agent": "Mozilla/5.0 3VL", "Content-Type": "application/x-www-form-urlencoded"}
API = "https://www.threevillagelocal.com/api/v2/"
NAME = "3VL Page Home Preview"
SLUG = "preview-home"
GUARD = os.path.join(WK, "..", "..", "3vl-site-guard", "post-sources")
CSS = ("/* front layout preview: lower main sections are laid out only near the screen (same idea as the homepage) */\n"
       ".wk-y .wk-main>.wk-sec:not(#wk-picks){content-visibility:auto;contain-intrinsic-size:auto 700px}\n"
       "#first_container{background-image:none!important}\n"
       "/* this page draws its own (prototype) header and footer: BD's header, menu and footer never show, from the first paint */\n"
       "body>.header,body>.footer,.mobile-main-menu,.banner-ad-unit,body>.footer-clear-element{display:none!important}\n"
       "html,body{background:#f3f6fa!important;margin:0!important;padding:0!important}\n"
       "#main-content,#first_container{margin:0!important;padding:0!important;background:#f3f6fa!important}\n"
       "#first_container>.container{width:100%!important;max-width:none!important;padding:0!important;margin:0!important}\n"
       "#first_container>.container>.row{margin:0!important}\n"
       "#first_container>.container>.row>.col-md-12{padding:0!important;width:100%!important;float:none!important}\n"
       "#first_container>.container>.clearfix{margin:0!important;padding:0!important;height:0!important}"+chr(10)+
       "#wk-top{padding:0!important}")


def call(method, path, data=None):
    body = urllib.parse.urlencode(data).encode() if data is not None else None
    return json.loads(urllib.request.urlopen(urllib.request.Request(API + path, data=body, headers=H, method=method), timeout=90).read())


def preload(body):
    m = re.search(r'<picture><source media="\(max-width:720px\)" srcset="([^"]+)"><img class="wk-hbg" src="([^"]+)"', body)
    if not m:
        return ""
    return ('<!-- 3VL hero preload (bd_guard.py) --><link rel="preload" as="image" href="%s" media="(max-width:720px)" fetchpriority="high">'
            '<link rel="preload" as="image" href="%s" media="(min-width:721px)" fetchpriority="high"><!-- /3VL hero preload -->') % (m.group(1), m.group(2))


def main():
    sha = sys.argv[1]
    assert re.fullmatch(r"[0-9a-f]{40}", sha), "pass the full 40-character commit SHA"
    ed = N.latest_edition()
    d = json.load(open(os.path.join(WK, ed, "weekend.json"), encoding="utf-8"))
    N.adjust(d, nhb.now_et())
    body = B.build(ed, False, sha, d=d, front=True)
    assert "\\" not in body, "backslash in body"
    bad = N.warm(body, ed, sha)
    if bad:
        sys.exit("CDN not ready: %s" % bad[0])
    found = call("GET", "data_widgets/get?property=widget_name&property_value=" + urllib.parse.quote(NAME)).get("message")
    found = [x for x in found if x.get("widget_name") == NAME] if isinstance(found, list) else []
    if found:
        wid = found[0]["widget_id"]
        print("widget", wid, call("PUT", "data_widgets/update", {"widget_id": wid, "widget_data": body}).get("status"))
    else:
        r = call("POST", "data_widgets/create", {"widget_name": NAME, "widget_viewport": "front", "widget_data": body})
        wid = (r.get("message") or {}).get("widget_id")
        print("widget create", r.get("status"), wid)
    page = {"content": "[widget=%s]" % NAME, "content_css": CSS, "content_head": preload(body), "enable_hero_section": "0",
            "title": "Three Village Local | Homepage preview", "meta_desc": "Preview of the Three Village Local homepage layout.",
            "show_form": "1"}   # show_form 1 = noindex on this site (same as the other preview pages)
    ex = call("GET", "list_seo/get?property=filename&property_value=" + SLUG).get("message")
    ex = [x for x in ex if x.get("filename") == SLUG] if isinstance(ex, list) else []
    if ex:
        print("page update", ex[0]["seo_id"], call("PUT", "list_seo/update", dict(page, seo_id=ex[0]["seo_id"])).get("status"))
    else:
        r = call("POST", "list_seo/create", dict(page, seo_type="content", filename=SLUG))
        print("page create", r.get("status"), (r.get("message") or {}).get("seo_id") if isinstance(r.get("message"), dict) else r.get("message"))
    if os.path.isdir(GUARD):
        fn = os.path.join(GUARD, "widget-%s-3vl-page-home-preview.html" % wid)
        open(fn, "w", encoding="utf-8", newline="\n").write(body)
        print("guard copy:", fn)
    try:
        call("POST", "website_settings/refreshCache", {})
    except Exception as e:
        print("cache:", e)
    print("https://www.threevillagelocal.com/" + SLUG)


if __name__ == "__main__":
    main()
