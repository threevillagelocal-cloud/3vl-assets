"""The Weekender: build the BD post body from an edition's weekend.json.

Usage:
  python build.py 2026-10-02            -> writes <edition>/post.html (BD post_content, jsDelivr URLs)
  python build.py 2026-10-02 --local    -> writes <edition>/preview.html (local files, wrapped in the saved BD page frame)
  python build.py 2026-10-02 --sha abc123  -> pin jsDelivr URLs to a commit SHA (do this for the live post)

Rules that matter on BD:
  - post_content must contain NO backslashes (BD strips them).
  - Publish through the API only. The Froala editor strips <style>/<script>.
"""
import html, json, os, re, sys
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = "threevillagelocal-cloud/3vl-assets"

def esc(s):
    return html.escape(str(s), quote=True)

def fmt_time(iso):
    d = datetime.fromisoformat(iso)
    h = d.hour % 12 or 12
    m = "" if d.minute == 0 else ":%02d" % d.minute
    return "%d%s %s" % (h, m, "AM" if d.hour < 12 else "PM")

def dshort(iso):
    d = datetime.fromisoformat(iso)
    return d.strftime('%a, %b ') + str(d.day)


DAYNAME = {"fri": "Friday", "sat": "Saturday", "sun": "Sunday"}
TAGS = {"free": "Free", "kids": "Kids", "outdoor": "Outdoor", "music": "Music", "history": "History",
        "food": "Food", "arts": "Arts", "stage": "On Stage"}
ICON = {"free": "&#127903;&#65039;", "kids": "&#129490;", "outdoor": "&#127795;", "music": "&#127928;",
        "history": "&#128373;&#65039;", "food": "&#127822;", "arts": "&#127912;", "stage": "&#127917;"}

NOLINK_TAGS = ("a", "button", "script", "style", "h1", "h2", "h3", "title")
NOLINK_CLASSES = ('class="wk-evtitle"', 'class="wk-awt"', 'class="wk-nxt"', 'class="wk-stib"', 'class="wk-ptitle"', 'class="wk-spt"')


def linkify(html_str):
    """Link business names in visible text only: never inside tags, links, buttons, headings, titles, scripts or styles."""
    links = json.load(open(os.path.join(HERE, "biz_links.json"), encoding="utf-8"))
    pat = re.compile("|".join(re.escape(n) for n in sorted(links, key=len, reverse=True)))
    stack, out = [], []
    for p in re.split(r"(<[^>]+>)", html_str):
        if p.startswith("<"):
            name = re.match(r"</?\s*([a-zA-Z0-9]+)", p)
            tag = name.group(1).lower() if name else ""
            if p.startswith("</"):
                if stack and stack[-1] == tag:
                    stack.pop()
            elif not p.endswith("/>") and tag not in ("img", "br", "input", "link", "meta", "source", "circle", "path", "hr"):
                blocked = tag in NOLINK_TAGS or any(c in p for c in NOLINK_CLASSES)
                if blocked or stack:
                    stack.append(tag)
            out.append(p)
        elif stack or not p.strip():
            out.append(p)
        else:
            out.append(pat.sub(lambda m: '<a class="wk-biz" href="%s"%s>%s</a>' % (
                links[m.group(0)], "" if "threevillagelocal.com" in links[m.group(0)] else ' target="_blank" rel="noopener"', m.group(0)), p))
    return "".join(out)


def build(edition, local=False, sha="master"):
    d = json.load(open(os.path.join(HERE, edition, "weekend.json"), encoding="utf-8"))
    vips = json.load(open(os.path.join(HERE, "vip.json"), encoding="utf-8"))
    if local:
        base = "http://127.0.0.1:8765/weekender/"
    else:
        base = "https://cdn.jsdelivr.net/gh/%s@%s/weekender/" % (REPO, sha)
    ed = base + edition + "/"
    feed_url = base + "feed.json" if local else "https://raw.githubusercontent.com/%s/master/weekender/feed.json" % REPO
    V = d["venues"]

    def img(name, small=False):
        return ed + name + ("-720" if small else "") + ".webp"

    def day_of(iso):
        for k, v in d["days"].items():
            if iso.startswith(v):
                return k
        return ""

    def tagchips(tags):
        return "".join('<span class="wk-tag" data-t="%s">%s</span>' % (t, TAGS[t]) for t in tags)

    def gmap(v):
        return "https://www.google.com/maps/search/?api=1&amp;query=" + esc(V[v]["name"] + ", " + V[v]["addr"]).replace(" ", "+")

    def evattrs(e):
        v = V[e["venue"]]
        return ('data-id="%s" data-day="%s" data-start="%s-04:00" data-end="%s-04:00" data-tags="%s" '
                'data-lat="%s" data-lon="%s" data-title="%s" data-venue="%s" data-addr="%s" data-img="%s"') % (
            e["id"], day_of(e["start"]), e["start"], e["end"], " ".join(e["tags"]), v["ll"][0], v["ll"][1],
            esc(e["title"]), esc(v["name"]), esc(v["addr"]), img(e["img"], True) if e.get("img") else "") + ((' data-off="%s"' % esc(e["status"])) if e.get("status") else "")

    def actions(e):
        return ('<div class="wk-acts"><button type="button" class="wk-save" data-save="%s" aria-pressed="false">'
                '<span class="wk-star">&#9734;</span><span class="wk-savet">Save</span></button>'
                '<button type="button" class="wk-cal" data-cal="%s">&#128197; Add</button>'
                '<a class="wk-dir" href="%s" target="_blank" rel="noopener">&#128205; Map</a></div>') % (e["id"], e["id"], gmap(e["venue"]))

    ev = {e["id"]: e for e in d["events"]}
    n_ev = len(d["events"]) + len(d["allweekend"])
    n_free = sum(1 for e in d["events"] + d["allweekend"] if "free" in e["tags"])
    out = []
    w = out.append

    # Hide BD's own featured image + shrink BD's H1 into a kicker (same trick as the Storm Center).
    w('<style>#post-content .post-image-container,#post-content .post-image-container + hr{display:none!important}'
      '#post-content .post-title h1{font-size:13px!important;font-weight:700!important;color:#6b7785!important;'
      'text-transform:uppercase;letter-spacing:.08em;line-height:1.4!important;margin:0 0 10px!important}'
      '#post-content .post-title hr{display:none!important}'
      '.post-detail-sidebar{display:none!important}.col-md-8:has(#wk-top){width:100%!important;float:none!important;left:auto!important;right:auto!important}'
      '.posted-by-snippet{display:none!important}</style>')
    w('<link rel="preload" as="image" href="%s" media="(min-width:721px)">' % img(d["hero"]["img"]))
    w('<link rel="preload" as="image" href="%s" media="(max-width:720px)">' % img(d["hero"]["img"], True))
    ver = ("?v=%d" % int(__import__("time").time())) if local else ""
    w('<link rel="stylesheet" href="%sweekender.css%s">' % (base, ver))
    w('<div class="wk" id="wk-top" data-start="%s" data-end="%s" data-assets="%s" data-edition="%s" data-feed="%s"%s>' % (
        d["starts"], d["ends"], esc(base), edition, esc(feed_url), (' data-live="%slive/events.json"' % base) if local else ""))

    # HERO: compact live intro for Three Village Now
    w('<header class="wk-hero wk-hero2"><picture><source media="(max-width:720px)" srcset="%s"><img class="wk-hbg" src="%s" alt="" width="1600" height="1067"></picture>'
      % (img(d["hero"]["img"], True), img(d["hero"]["img"])))
    w('<div class="wk-hshade"></div>')
    w('<div class="wk-hin"><div class="wk-brandrow"><h1 class="wk-hname">Three Village <span>Now</span></h1><span class="wk-livepill"><i></i>Updated Live</span></div>')
    w('<p class="wk-dek">What&rsquo;s happening in Setauket, Stony Brook and Port Jefferson right now. Events, specials, weather and local news, updated all day.</p>')
    w('<div class="wk-hstats">'
      '<div class="wk-hs"><span class="wk-hsl">Today</span><b id="wk-hdate">--</b><span class="wk-hsc" id="wk-hclock">--:--</span></div>'
      '<a class="wk-hs" href="#wk-sched"><span class="wk-hsl"><i class="wk-hdot"></i>Happening now</span><b id="wk-hnow">--</b><span class="wk-hsc" id="wk-hnext">checking&hellip;</span></a>'
      '<a class="wk-hs" href="#wk-wx"><span class="wk-hsl">Setauket weather</span><b><span class="wk-hwi2" id="wk-hwi2"></span><span id="wk-htemp">--</span>&deg;</b><span class="wk-hsc" id="wk-hsky">loading&hellip;</span></a>'
      '</div></div><p class="wk-pcred">%s</p></header>' % esc(d["hero"]["credit"]))

    # NAV
    w('<nav class="wk-nav" aria-label="Jump to section"><span class="wk-navl">Jump to &#8594;</span><div class="wk-navin">'
      '<a href="#wk-picks">&#11088; Top Picks</a><a href="#wk-eat">&#127869;&#65039; Eat &amp; Drink</a><a href="#wk-wx">&#9728;&#65039; Weather</a>'
      '<a href="#wk-sched">&#128197; Schedule</a><a href="#wk-spy">&#128373;&#65039; Spy Day</a>'
      '<a href="#wk-stage">&#127917; On Stage</a><a href="#wk-next">&#128302; On the Radar</a>'
      '</div></nav>')
    w('<div class="wk-ticker" id="wk-ticker" hidden><span class="wk-tkl"><i></i>LIVE</span><div class="wk-tkm"><div class="wk-tkt" id="wk-tkt"></div></div></div>')

    w('<div class="wk-grid"><div class="wk-main">')
    cx = d.get("closings")
    if cx:
        w('<section class="wk-sec wk-cxsec" id="wk-cx"><div class="wk-cxhead"><span class="wk-live"><i></i>STORM</span>'
          '<p><b>This weekend&rsquo;s closings</b> %s</p><a class="wk-cxall" href="%s">Full list &amp; live radar &rarr;</a></div><div class="wk-cxrow wk-swipe">' % (esc(cx["label"]), cx["url"]))
        for it in cx["items"]:
            w('<div class="wk-cxi" data-off="%s"><p class="wk-cxn">%s</p><p class="wk-cxd">%s</p></div>' % (esc(it[0]), esc(it[1]), esc(it[2])))
        w('</div></section>')

    # TOP PICKS
    w('<section class="wk-sec" id="wk-picks"><h2 class="wk-h2"><span>Top Picks</span><small>If you only do three things</small></h2><div class="wk-picks wk-swipe">')
    for i, pid in enumerate(d["picks"]):
        e = ev[pid]
        w('<article class="wk-pick wk-rv" %s style="--i:%d"><div class="wk-pimg"><img src="%s" alt="%s" loading="lazy" width="720" height="480">'
          '<span class="wk-pnum">%02d</span><span class="wk-pstat" data-status></span></div>'
          '<div class="wk-pbody"><p class="wk-pwhen">%s &middot; %s</p><h3 class="wk-ptitle">%s</h3><p class="wk-pwhere">&#128205; %s</p>'
          '<p class="wk-pdesc">%s</p><div class="wk-tags">%s<span class="wk-price">%s</span></div>%s</div>'
          '<p class="wk-icred">%s</p></article>' % (
            evattrs(e), i, img(e["img"], True), esc(e["title"]), i + 1, dshort(e["start"]),
            fmt_time(e["start"]) + ("" if not e.get("extra") else " &amp; 4:30 PM"),
            esc(e["title"]), esc(V[e["venue"]]["name"]), esc(e["desc"]), tagchips(e["tags"]), esc(e["price"]), actions(e), esc(e.get("credit", ""))))
    w('</div></section>')

    # EAT & DRINK (exterior photo + dish inset; one card per business)
    w('<section class="wk-sec" id="wk-eat"><h2 class="wk-h2"><span>Eat &amp; Drink</span><small>Local specials, updated daily</small></h2><div class="wk-eat wk-swipe">')
    for sp in d["specials"]:
        badge = '<span class="wk-src wk-fb">f</span>' if sp["src"] == "facebook" else '<span class="wk-src wk-web">&#127760;</span>'
        main = sp.get("ext") or sp.get("img")
        pic = ('<div class="wk-eimg">%s<img src="%s" alt="%s" loading="lazy">%s</div>' % (
            ('<picture><source media="(min-width:761px)" srcset="%s"></picture>' % img(sp["extwide"])) if False else "",
            img(sp["extwide"] if (sp.get("feature") and sp.get("extwide")) else main, True), esc(sp["biz"]),
            ('<span class="wk-dish"><img src="%s" alt="" loading="lazy"></span>' % img(sp["dish"], True)) if sp.get("dish") else "")) if main else ""
        call = ('<a class="wk-call" href="tel:%s">&#128222; Call</a>' % re.sub(r"\D", "", sp["phone"])) if sp.get("phone") else ''
        w('<article class="wk-sp wk-rv%s">%s<div class="wk-spb"><p class="wk-spbiz">%s</p><p class="wk-spt">%s</p><p class="wk-spw">%s</p>'
          '<p class="wk-spd">%s</p><p class="wk-spf">%s<span>via %s</span>%s<a class="wk-dir" href="%s" target="_blank" rel="noopener">&#128205; Map</a></p></div></article>' % (
            " wk-spfeat" if sp.get("feature") else "", pic, esc(sp["biz"]), esc(sp["title"]), esc(sp["when"]), esc(sp["desc"]),
            badge, esc(sp["srcName"]), call, gmap(sp["venue"])))
    w('</div><p class="wk-note">Own a local spot with a special? <a href="https://www.threevillagelocal.com/promotion">Send it to us</a> and we&rsquo;ll feature it free.</p></section>')

    # WEATHER (compact)
    w('<section class="wk-sec" id="wk-wx"><h2 class="wk-h2"><span>Weather</span><small>Live from the National Weather Service</small></h2>'
      '<p class="wk-verdict" id="wk-verdict">&#9728;&#65039; Loading the forecast&hellip;</p><div class="wk-wx">')
    for k in ("fri", "sat", "sun"):
        bg = d.get("wxbg", {}).get(k, {})
        w('<div class="wk-wd" data-day="%s"><div class="wk-wbg"%s><img class="wk-wph" src="%s" alt="" loading="lazy"><div class="wk-wfx"></div></div>'
          '<p class="wk-wloc"><span class="wk-wlive" hidden><i></i>LIVE</span><span class="wk-wcam">&#127909;</span> %s <b class="wk-wclk"></b></p>' % (
            k, (' data-cam="%s"' % bg["cam"]) if bg.get("cam") else "", img(bg.get("photo", "hero"), True), esc(bg.get("loc", ""))))
        w('<div class="wk-wrow"><div class="wk-wleft"><p class="wk-wdn">%s</p><div class="wk-wicon"></div></div>'
          '<div class="wk-wm"><p class="wk-wt"><b class="wk-hi">--</b>&deg;<span class="wk-lo">--</span>&deg;</p><p class="wk-ws">Forecast coming soon</p></div>'
          '<div class="wk-ring"><svg viewBox="0 0 120 120" aria-hidden="true"><circle cx="60" cy="60" r="50" class="wk-rtrk"/><circle cx="60" cy="60" r="50" class="wk-rfil" transform="rotate(-90 60 60)"/></svg>'
          '<div class="wk-rin"><b class="wk-score">--</b><span>score</span></div></div></div>'
          '<div class="wk-wchips"><span title="Chance of rain">&#128167; <b class="wk-pop">--%%</b></span><span title="Wind">&#127788;&#65039; <b class="wk-wind">--</b></span>'
          '<span title="Sunset">&#127749; <b class="wk-set">--</b></span></div><p class="wk-wcred">%s</p></div>' % (DAYNAME[k][:3], esc(bg.get("credit", ""))))
    w('</div></section>')

    # SCHEDULE
    w('<section class="wk-sec" id="wk-sched"><h2 class="wk-h2"><span>The Full Schedule</span><small>Tap &#9734; to save to My Plans</small></h2>')
    w('<div class="wk-tabs" role="tablist"><button type="button" class="wk-tab is-on" data-day="all">All</button>'
      '<button type="button" class="wk-tab" data-day="fri">Fri <small>10/2</small></button><button type="button" class="wk-tab" data-day="sat">Sat <small>10/3</small></button>'
      '<button type="button" class="wk-tab" data-day="sun">Sun <small>10/4</small></button><span class="wk-tabink"></span></div>')
    w('<div class="wk-chips"><button type="button" class="wk-chip is-on" data-tag="all">Everything</button>')
    for t in ("free", "kids", "outdoor", "music", "history", "food", "stage"):
        w('<button type="button" class="wk-chip" data-tag="%s">%s %s</button>' % (t, ICON[t], TAGS[t]))
    w('</div><p class="wk-count2" id="wk-shown"></p>')
    for k in ("fri", "sat", "sun"):
        w('<div class="wk-dayblk" data-day="%s"><p class="wk-dayh"><b>%s</b><span>%s</span></p><ol class="wk-tl">' % (
            k, DAYNAME[k], datetime.fromisoformat(d["days"][k]).strftime("%B %-d") if os.name != "nt" else datetime.fromisoformat(d["days"][k]).strftime("%B %#d")))
        for e in sorted([e for e in d["events"] if day_of(e["start"]) == k], key=lambda x: x["start"]):
            thumb = ('<img src="%s" alt="" loading="lazy" width="120" height="120">' % img(e["img"], True)) if e.get("img") else (
                '<span class="wk-ticon">%s</span>' % ICON[[t for t in ("history", "music", "stage", "food", "kids", "arts", "outdoor", "free") if t in e["tags"]][0]])
            w('<li class="wk-ev wk-rv" %s><div class="wk-evt"><b>%s</b><span>%s</span></div><div class="wk-evc"><div class="wk-evthumb">%s</div><div class="wk-evbody">'
              '<p class="wk-evtitle">%s <span class="wk-pstat" data-status></span></p><p class="wk-evwhere">%s &middot; %s</p><p class="wk-evdesc" tabindex="0">%s</p>'
              '<div class="wk-tags">%s<span class="wk-price">%s</span><span class="wk-wxchip"></span></div></div>%s</div></li>' % (
                evattrs(e), fmt_time(e["start"]), "to " + fmt_time(e["end"]), thumb, esc(e["title"]), esc(V[e["venue"]]["name"]),
                esc(V[e["venue"]]["addr"].split(", ")[-1]), esc(e["desc"]), tagchips(e["tags"]), esc(e["price"]), actions(e)))
        w('</ol></div>')
    w('<div class="wk-allwk"><p class="wk-dayh"><b>All Weekend</b><span>Anytime Fri-Sun</span></p><div class="wk-allg">')
    for a in d["allweekend"]:
        w('<div class="wk-aw wk-rv" data-tags="%s"><p class="wk-awwhen">%s</p><p class="wk-awt">%s</p><p class="wk-evwhere">%s</p><p class="wk-evdesc">%s</p><div class="wk-tags">%s</div></div>' % (
            " ".join(a["tags"]), esc(a["when"]), esc(a["title"]), esc(V[a["venue"]]["name"]), esc(a["desc"]), tagchips(a["tags"])))
    w('</div></div><p class="wk-nomatch" id="wk-nomatch" hidden>Nothing matches that combo. Try another filter.</p></section>')

    w('<div class="wk-adslot" data-slot="1"></div>')

    # SPY DAY FEATURE
    s = ev["spyday"]
    w('<section class="wk-sec wk-spy" id="wk-spy"><div class="wk-spyin" style="--spybg:url(%s)"><p class="wk-spyk">' % img("spyday") + 'Saturday &middot; Setauket &middot; Free</p>'
      '<h2 class="wk-spyt">Culper Spy Day <span>Field Guide</span></h2>'
      '<p class="wk-spyd">In 1778 a handful of Setauket neighbors ran the spy ring that fed George Washington the intel he needed. '
      'Twelve years in, their hometown throws them a party. Here is how to do the whole day.</p>'
      '<div class="wk-cipher" id="wk-cipher" aria-label="Decoded message"><span class="wk-ciphl">Intercepted message</span><b data-plain="MEET AT THE VILLAGE GREEN AT TEN">&nbsp;</b></div>')
    w('<button type="button" class="wk-more wk-spytog" data-more="wk-spydet">Open the full field guide &#9662;</button><div class="wk-spydet" id="wk-spydet">')
    w('<div class="wk-trolley"><p class="wk-trh"><span>&#128651; Free hop-on, hop-off trolley</span><small>10 AM-4 PM &middot; first come, first served</small></p>'
      '<svg class="wk-route" viewBox="0 0 600 120" preserveAspectRatio="none" aria-hidden="true"><path id="wk-rpath" d="M20 90 C 120 10, 200 10, 300 60 S 480 110, 580 30" /></svg>'
      '<div class="wk-bus" id="wk-bus">&#128651;</div><ol class="wk-stops">')
    for i, t in enumerate(d["trolley"]):
        w('<li style="--i:%d"><b>%s</b><span>%s</span></li>' % (i, esc(t["stop"]), esc(t["note"])))
    w('</ol></div>')
    w('<div class="wk-spyg"><div class="wk-spyc"><p class="wk-spych">&#9201;&#65039; At the Historical Society</p><ul>'
      '<li><b>10:00</b> Flag raising with General Washington</li><li><b>11, 1 &amp; 3</b> <i>Shadow’s Rise</i> spy musical</li>'
      '<li><b>12 &amp; 2</b> Build a timber frame house with Abraham Woodhull</li><li><b>All day</b> Encampment, musket drills, invisible ink, colonial food</li>'
      '<li><b>10:30-3:30</b> SPIES! exhibit tours (ticketed)</li></ul></div>'
      '<div class="wk-spyc"><p class="wk-spych">&#127869;&#65039; Where to eat</p><ul>'
      '<li class="wk-spycc"><b>&#11088; The Country Corner</b> Suffolk&rsquo;s oldest tavern, lunch with a view of the Brewster House. Open 11, brunch 11-2</li>'
      '<li><b>On site</b> The Branded Bun truck &amp; ALatte Coffee</li><li><b>Caroline Church</b> Dilly Dilly Donuts</li>'
      '<li><b>Checkmate Inn</b> Level Up Kitchen</li><li><b>Main St</b> Culpers 1778 &amp; Elaine&rsquo;s</li>'
      '<li><b>Patriots Rock</b> McNulty’s ice cream truck</li></ul></div></div>')
    w('</div>')
    w('<p class="wk-spyf"><a class="wk-btn wk-btng" href="%s" target="_blank" rel="noopener">Full schedule &amp; digital map &rarr;</a>'
      '<button type="button" class="wk-btn wk-btno wk-save" data-save="spyday" aria-pressed="false"><span class="wk-star">&#9734;</span><span class="wk-savet">Save Spy Day</span></button></p></div></section>' % s["url"])

    w('<div class="wk-adslot" data-slot="2"></div>')

    # ON STAGE
    cab = [a for a in d["allweekend"] if a.get("video")][0]
    w('<section class="wk-sec" id="wk-stage"><h2 class="wk-h2"><span>On Stage</span><small>Theater, comedy &amp; concerts</small></h2>'
      '<div class="wk-stageg"><div class="wk-vid" data-yt="%s"><img src="%s" alt="Cabaret at Theatre Three" loading="lazy" width="720" height="405">'
      '<button type="button" class="wk-play" aria-label="Play the Cabaret trailer"><span></span></button>'
      '<p class="wk-vcap"><b>Cabaret</b> at Theatre Three &middot; %s &middot; Watch the trailer</p></div><div class="wk-stagel">' % (cab["video"], img(cab["img"], True), esc(cab["when"])))
    for sid in ("treason", "symphony", "limehof", "sedaris"):
        e = ev[sid]
        w('<a class="wk-sti" href="%s" target="_blank" rel="noopener"><span class="wk-stid">%s<b>%s</b></span><span class="wk-stib"><b>%s</b><small>%s &middot; %s</small></span><span class="wk-stip">%s</span></a>' % (
            e["url"], DAYNAME[day_of(e["start"])][:3], fmt_time(e["start"]), esc(e["title"]), esc(V[e["venue"]]["name"]), esc(V[e["venue"]]["addr"].split(", ")[-1]), esc(e["price"])))
    el = [a for a in d["allweekend"] if a["id"] == "elephant"][0]
    w('<a class="wk-sti wk-stkid" href="%s" target="_blank" rel="noopener"><span class="wk-stid">Kids<b>All wknd</b></span><span class="wk-stib"><b>%s</b><small>Theatre Three &middot; %s</small></span><span class="wk-stip">Kids</span></a>' % (
        el["url"], esc(el["title"]), esc(el["when"])))
    w('</div></div></section>')

    # NEXT WEEKEND
    w('<section class="wk-sec" id="wk-next"><h2 class="wk-h2"><span>On the Radar</span><small>Save the dates</small></h2><div class="wk-next wk-swipe">')
    for n in d["next"]:
        w('<div class="wk-nx wk-rv"%s><p class="wk-nxw">%s</p><p class="wk-nxt">%s</p><p class="wk-nxd">%s</p>%s</div>' % (
            (' style="--nx:url(%s)"' % img(n["img"], True)) if n.get("img") else "", esc(n["when"]), esc(n["title"]), esc(n["desc"]),
            ('<span class="wk-nxc">%s</span>' % esc(n["credit"])) if n.get("credit") else ""))
    w('</div></section>')

    # SUBMIT + SHARE + APP
    w('<section class="wk-sec wk-cta"><div class="wk-submit"><p class="wk-subt">Got an event or a special?</p><p class="wk-subd">Three Village Now updates every day. '
      'Send us your event, menu special or promotion and we’ll put it in front of Three Village.</p>'
      '<a class="wk-btn wk-btng" href="https://www.threevillagelocal.com/promotion">Submit it free &rarr;</a></div>'
      '<div class="wk-share"><p class="wk-subt">Send this to your crew</p><div class="wk-shb">'
      '<button type="button" class="wk-btn wk-btnw" id="wk-share">&#128172; Share Three Village Now</button>'
      '<button type="button" class="wk-btn wk-btnw" id="wk-share2">&#11088; Share my plan</button></div></div>'
      '<div class="wk-app"><p class="wk-subt">Get Three Village Now on your phone</p><p class="wk-subd">The free Three Village Local app puts today&rsquo;s events, local specials and neighbor-rated businesses right on your phone.</p>'
      '<div class="wk-appb"><a href="https://apps.apple.com/us/app/three-village-local/id6746367200" target="_blank" rel="noopener"><img src="https://raw.githubusercontent.com/threevillagelocal-cloud/3vl-assets/master/badges/app-store-badge.png" alt="Download on the App Store" width="142" height="50"></a>'
      '<a href="https://play.google.com/store/apps/details?id=com.threevillagelocal.app&amp;hl=en_US" target="_blank" rel="noopener"><img src="https://raw.githubusercontent.com/threevillagelocal-cloud/3vl-assets/master/badges/google-play-badge.png" alt="Get it on Google Play" width="168" height="50"></a></div></div></section>')
    w('<p class="wk-foot">Plans change. Check with the organizer before you head out. Sources: organizer websites, TBR News Media, and local business pages on Facebook.</p>')

    w('</div>')  # /wk-main

    # VIP RAIL
    w('<aside class="wk-rail" aria-label="Three Village Local VIP members"><div class="wk-railin"><p class="wk-railh"><span>&#11088; VIP</span> Local businesses we love</p>'
      '<div class="wk-adrot" id="wk-adrot">')
    banners = json.load(open(os.path.join(HERE, "banners.json"), encoding="utf-8"))
    for i, v in enumerate(banners):
        w('<div class="wk-ad%s" data-vip="%s" data-group="%s" aria-hidden="%s"><a class="wk-adpic" href="%s" data-vip="%s" style="--bgimg:url(%s)">'
          '<img src="%s" alt="%s" loading="%s" width="%d" height="%d"></a>'
          '<div class="wk-adbtns"><a class="wk-adcall" href="tel:%s" data-vip="%s">&#128222; Call</a><a class="wk-adview" href="%s" data-vip="%s">View on 3VL &rarr;</a></div></div>' % (
            " is-on" if i == 0 else "", esc(v["name"]), esc(v.get("group", v["id"])), "false" if i == 0 else "true", v["url"], esc(v["name"]), base + v["img"],
            base + v["img"], esc(v["name"]) + " ad", "eager" if i == 0 else "lazy", v["w"], v["h"], v["phone"], esc(v["name"]), v["url"], esc(v["name"])))
    w('<div class="wk-adprog"><i id="wk-adbar"></i></div><div class="wk-addots" id="wk-addots"></div></div>')
    w('<div class="wk-adrot2" id="wk-adrot2"></div>')
    w('<a class="wk-railcta" href="https://www.threevillagelocal.com/join">Advertise here &rarr;</a></div></aside>')

    w('</div>')  # /wk-grid

    # MY WEEKEND DRAWER
    w('<button type="button" class="wk-fab" id="wk-fab" aria-controls="wk-drawer" aria-expanded="false"><span class="wk-star">&#9733;</span> My Plans <b id="wk-fabn">0</b></button>'
      '<div class="wk-drawer" id="wk-drawer" aria-hidden="true"><div class="wk-drin"><div class="wk-drh"><p>&#11088; My Plans</p><button type="button" id="wk-drx" aria-label="Close">&times;</button></div>'
      '<div id="wk-drlist"></div><div class="wk-drf"><button type="button" class="wk-btn wk-btng" id="wk-calall">&#128197; Add all to my calendar</button>'
      '<button type="button" class="wk-btn wk-btno" id="wk-share3">&#128172; Share my plan</button></div></div></div>')
    w('<a href="#wk-top" class="wk-totop" id="wk-totop" aria-label="Back to top">&#8593;</a><div class="wk-toast" id="wk-toast" role="status"></div>')
    w('</div>')
    w('<script src="%sweekender.js%s" defer></script>' % (base, ver))

    body = "\n".join(out)
    body = body.replace("’", "&rsquo;")
    body = linkify(body)
    assert "\\" not in body, "backslash found: BD would strip it"
    return body

if __name__ == "__main__":
    edition = sys.argv[1]
    local = "--local" in sys.argv
    sha = sys.argv[sys.argv.index("--sha") + 1] if "--sha" in sys.argv else "master"
    body = build(edition, local, sha)
    if local:
        frame_path = os.path.join(HERE, "preview-frame.html")
        frame = open(frame_path, encoding="utf-8").read() if os.path.exists(frame_path) else "<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'></head><body><!--WEEKENDER--></body></html>"
        open(os.path.join(HERE, edition, "preview.html"), "w", encoding="utf-8").write(frame.replace("<!--WEEKENDER-->", body))
        print("preview written")
    else:
        open(os.path.join(HERE, edition, "post.html"), "w", encoding="utf-8").write(body)
        print("post.html written", len(body), "chars")
