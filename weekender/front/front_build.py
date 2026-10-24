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
    h = d["hero"]
    return (
        '<header class="wk-hero wk-hero2 wk-yhero"><picture><source media="(max-width:720px)" srcset="%s"><img class="wk-hbg" src="%s" alt="%s" width="1600" height="1067" fetchpriority="high"></picture>'
        '<div class="wk-hin"><p class="wk-ykick"><span class="wk-livepill"><i></i>Live from Three Village</span></p>'
        '<h1 class="wk-yh1">What&rsquo;s happening in Three Village</h1>'
        '<p class="wk-dek">Events, specials, weather and local news for Setauket, Stony Brook and Port Jefferson, updated all day.</p>'
        '<div class="wk-hstats">'
        '<div class="wk-hs"><span class="wk-hsl">Today</span><b id="wk-hdate">--</b><span class="wk-hsc" id="wk-hclock">--:--</span></div>'
        '<a class="wk-hs" href="#wk-sched"><span class="wk-hsl"><i class="wk-hdot"></i>Happening now</span><b id="wk-hnow">--</b><span class="wk-hsc" id="wk-hnext">checking&hellip;</span></a>'
        '<a class="wk-hs" href="#wk-wx"><span class="wk-hsl">Setauket weather</span><b><span class="wk-hwi2" id="wk-hwi2"></span><span id="wk-htemp">--</span>&deg;</b><span class="wk-hsc" id="wk-hsky">loading&hellip;</span></a>'
        '</div></div><p class="wk-pcred">%s</p></header>'
    ) % (img(h["img"], True), img(h["img"]), esc(h.get("alt") or "Three Village, Long Island this week"), esc(h["credit"]))


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
