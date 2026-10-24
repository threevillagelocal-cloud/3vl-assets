"""Second homepage layout ("front", 10/24/2026): compact news-portal style, same data and the same weekender.js.
build.py calls these when build(..., front=True). The default homepage output does not change.
  - hero(): compact top band (search, live stats, this week's photo)
  - quick(): category quick-link row
  - spotlight(): Local Business Spotlight (one big VIP card + also featured + logo strip), replaces the Featured row
Data: search/index.json (VIP members), 3vl-share live/p3/vip/<id>.json (profile hero photo, category, one-liner, brand color)."""
import html, json, os, re, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import nowhome_build as nhb  # noqa: E402

VIPBASE = "https://threevillagelocal-cloud.github.io/3vl-share/live/p3/vip/"
NO_SPOT = {"552"}   # logo strip only
esc = nhb.esc


def _get_json(u):
    try:
        with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 3VL"}), timeout=20) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception:
        return None


def _ok(u):
    try:
        return urllib.request.urlopen(urllib.request.Request(u, method="HEAD", headers={"User-Agent": "Mozilla/5.0 3VL"}), timeout=15).status == 200
    except Exception:
        return False


def _hero(h):
    """Profile hero photo, a ~900px copy when one exists. '' when the hero is only a plain brand-color background."""
    img = (h or {}).get("img") or ""
    alt = ((h or {}).get("alt") or "").lower()
    if not img or "background" in alt or "monogram" in alt:
        return ""
    name = img.rsplit("/", 1)[-1]
    folder = img[: -len(name)]
    for c in (name.replace("-1800", "-900"), name + "-900.webp", re.sub(r"(\.webp)?$", "-900.webp", name, count=1)):
        if c != name and _ok(VIPBASE + folder + c):
            return VIPBASE + folder + c
    full = VIPBASE + img
    return full if _ok(full) else ""


def hero(d, img):
    """Compact top band: search bar (smartsearch.js inserts it after .wk-dek) + the thin live "today" strip. No photo here:
    this week's photo is the lead story inside Top Things to Do."""
    return (
        '<header class="wk-hero wk-hero2 wk-yhero"><div class="wk-hin">'
        '<h1 class="y-vh">What&rsquo;s happening in Three Village: events, specials, weather and local news for Setauket, Stony Brook and Port Jefferson</h1>'
        '<p class="wk-dek">Search local businesses</p>'
        '<div class="wk-hstats">'
        '<div class="wk-hs"><span class="wk-hsl">Today</span><b id="wk-hdate">--</b><span class="wk-hsc" id="wk-hclock">--:--</span></div>'
        '<a class="wk-hs" href="#wk-sched"><span class="wk-hsl"><i class="wk-hdot"></i>Happening now</span><b id="wk-hnow">--</b><span class="wk-hsc" id="wk-hnext">checking&hellip;</span></a>'
        '<a class="wk-hs" href="#wk-wx"><span class="wk-hsl">Setauket weather</span><b><span class="wk-hwi2" id="wk-hwi2"></span><span id="wk-htemp">--</span>&deg;</b><span class="wk-hsc" id="wk-hsky">loading&hellip;</span></a>'
        '<span class="y-jump">Jump to <a href="#wk-picks">Things to Do</a><a href="#wk-eat">Eat &amp; Drink</a><a href="#wk-sched">Schedule</a><a href="#wk-wx">Weather</a></span>'
        '</div></div></header>')


def _words(t):
    return set(re.findall(r"[a-z]{4,}", (t or "").lower()))


def lead_open(d, ev, V, img, evattrs, actions, tagchips, dshort, fmt_time, CAL):
    """Tabs + the lead story of Top Things to Do. The week's hero photo is used only when it belongs to one of the picks
    (its credit/alt names the event); otherwise the first pick with its own photo leads with that photo."""
    tabs = ('<div class="y-tabs" role="tablist"><button type="button" role="tab" class="on" aria-selected="true" data-y="tp">Top Picks</button>'
            '<button type="button" role="tab" aria-selected="false" data-y="td">Today <b class="y-tdn"></b></button>'
            '<button type="button" role="tab" aria-selected="false" data-y="cu">Coming Up</button></div>')
    cand = [ev[p] for p in d["picks"] if p in ev]
    h = d.get("hero") or {}
    hw = _words(h.get("credit", "") + " " + h.get("alt", ""))
    le = next((e for e in cand if len(_words(e["title"]) & hw) >= 2 and h.get("img")), None)
    if le is not None:
        small, big, credit = img(h["img"], True), img(h["img"]), re.sub(r"^.*?Photo:\s*", "", h.get("credit", ""))
    else:
        le = next((e for e in cand if e.get("img")), None)
        if le is None:
            return tabs + '<div class="y-tp">'
        small, big, credit = img(le["img"], True), img(le["img"]), le.get("credit", "")
    from datetime import datetime, timedelta
    if le.get("when"):
        when = esc(le["when"])
    else:
        last = (datetime.fromisoformat(le["end"]) - timedelta(hours=6)).date().isoformat() if le.get("end") else le["start"][:10]
        when = ("%s - %s" % (dshort(le["start"]), dshort(last))) if last > le["start"][:10] else "%s &middot; %s" % (dshort(le["start"]), fmt_time(le["start"]))
    page = le.get("page") or CAL
    g = next((x for x in d.get("guides", []) if x[0] in le["title"].lower()), None)
    if g:
        page = g[1]
    acts = actions(le)
    if le.get("when") and le.get("url"):
        acts = re.sub(r'<button type="button" class="wk-cal"[^<]*</button>', '<a class="wk-dir" href="%s" target="_blank" rel="noopener">&#128279; Details</a>' % esc(le["url"]), acts)
    lead = ('<article class="y-lead" data-href="%s" %s><a class="y-leadimg" href="%s" tabindex="-1" aria-hidden="true"><figure class="y-leadpic"><picture>'
            '<source media="(max-width:720px)" srcset="%s"><img class="wk-hbg" src="%s" alt="%s" width="1600" height="1067" fetchpriority="high"></picture>'
            '<span class="wk-pnum">01</span><span class="wk-pstat" data-status></span></figure></a>'
            '<div class="y-leadb"><p class="wk-pwhen">%s</p><h3 class="y-leadt"><a href="%s">%s</a></h3><p class="wk-pwhere">&#128205; %s</p>'
            '<p class="y-leadd">%s</p><div class="wk-tags">%s</div>%s%s</div></article>') % (
        esc(page), evattrs(le), esc(page), esc(small), esc(big), esc(h.get("alt") if big == img(h.get("img", "x")) else le["title"]),
        when, esc(page), esc(le["title"]), esc(V[le["venue"]]["name"]), esc(le.get("desc", "")), tagchips(le.get("tags", [])), acts,
        ('<p class="y-cred">Photo: %s</p>' % esc(credit)) if credit else "")
    return tabs + '<div class="y-tp" data-lead="%s">' % esc(le["title"]) + lead


def quick():
    chips = "".join('<a class="nh-cat" href="%s"><svg viewBox="0 0 24 24">%s</svg>%s</a>' % (u, nhb.ICO[i], esc(t)) for t, u, i in nhb.CATS)
    return ('<nav class="wk-yql" id="nh-explore" aria-label="Browse local businesses"><div class="wk-yqlin">' + chips
            + '<a class="nh-cat nh-allc" href="/categories">All categories &rarr;</a></div></nav>')


def _vips():
    try:
        idx = json.loads(nhb.get(nhb.IDX))
    except Exception:
        return []
    v = [m for m in idx.get("members", []) if m.get("p") == "vip"]
    import datetime
    day = int(datetime.datetime.now(datetime.timezone.utc).timestamp() // 86400)
    v.sort(key=lambda x: (int(x["id"]) * 7919 + day * 104729) % 1000)
    return v


def spotlight(base=""):
    """base: the pinned weekender/ address. Small photo copies in weekender/front/img/<id>-640.webp and -240.webp are used when present."""
    vips = _vips()
    if not vips:
        return ""
    cards, logos = [], []
    for m in vips:
        uid = str(m["id"])
        logo = nhb.sm(m.get("l"), 200)
        logos.append('<a class="y-lg" href="%s" title="%s"><span style="background-image:url(\'%s\')"></span><i class="y-vh">%s</i></a>' % (
            esc(m["u"]), esc(m["n"]), esc(logo), esc(m["n"])))
        if uid in NO_SPOT:
            continue
        j = _get_json(VIPBASE + uid + ".json") or {}
        h = j.get("hero") or {}
        photo = _hero(h)
        mini = photo
        if photo and base and os.path.exists(os.path.join(HERE, "img", uid + "-640.webp")):
            photo, mini = base + "front/img/%s-640.webp" % uid, base + "front/img/%s-240.webp" % uid
        cat = j.get("category") or m.get("c") or ""
        twn = nhb.town(m.get("t"))
        desc = (j.get("sub") or j.get("tagline") or "").replace(chr(0x2014), "-").replace(chr(0x2013), "-")
        tel = re.sub(r"\D", "", m.get("ph") or j.get("phone") or "")
        color = ((j.get("theme") or {}).get("navy") or "#16304f")
        if not re.fullmatch(r"#[0-9a-fA-F]{3,8}", color):
            color = "#16304f"
        vis = ('<img src="%s" alt="" loading="lazy" width="240" height="160" style="object-position:%s">' % (esc(mini), esc(h.get("pos") or "50% 50%"))) if photo else \
              '<span class="y-panel" style="--c:%s"><span class="y-plogo" style="background-image:url(\'%s\')"></span></span>' % (color, esc(logo))
        cards.append(
            '<a class="y-mc" href="%s" data-id="%s" data-img="%s" data-pos="%s" data-alt="%s" data-logo="%s" data-cat="%s" data-town="%s" data-desc="%s" data-tel="%s" data-color="%s">'
            '<span class="y-mci">%s</span><span class="y-mct"><b>%s</b><small>%s</small></span></a>' % (
                esc(m["u"]), uid, esc(photo), esc(h.get("pos") or "50% 50%"), esc(h.get("alt") or m["n"]), esc(logo), esc(cat), esc(twn), esc(desc), tel, color,
                vis, esc(m["n"]), esc(cat)))
    nav = ('<span class="y-spnav"><button type="button" class="y-spn" data-sp="-1" aria-label="Previous business"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg></button>'
           '<button type="button" class="y-spn" data-sp="1" aria-label="Next business"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg></button></span>')
    lg = "".join(logos)
    return ('<section class="wk-sec nh-sec wk-yspot" id="nh-feat"><h2 class="wk-h2"><span>Local Business Spotlight</span><small>Neighbors who support Three Village Local</small>%s</h2>'
            '<div class="y-spw" id="y-spw"><div class="y-spmain" id="y-spmain" aria-live="polite"></div>'
            '<div class="y-also"><p class="y-ah">Also featured</p><div class="y-list" id="y-list">%s</div></div></div>'
            '<div class="y-lgs"><div class="y-lgvp"><div class="y-lgtr">%s<span class="y-lgdup" aria-hidden="true">%s</span></div></div>'
            '<div class="y-lgend"><a class="nh-more" href="/search_results">See all businesses &rarr;</a><a class="y-join" href="/join">Own a business? Get featured</a></div></div>'
            '</section>') % (nav, "".join(cards), lg, lg.replace('<a class="y-lg"', '<a class="y-lg" tabindex="-1"'))
