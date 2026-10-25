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


SITE = "https://www.threevillagelocal.com"
IC = {
 "search": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>',
 "star": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3.5l2.6 5.3 5.9.9-4.3 4.1 1 5.8-5.2-2.7-5.2 2.7 1-5.8-4.3-4.1 5.9-.9z"/></svg>',
 "menu": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
 "chev": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg>',
 "phone": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg>',
 "mail": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 6l8.5 7 8.5-7"/></svg>',
 "cal": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/></svg>',
 "pin": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 22s7-6.2 7-12a7 7 0 1 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/></svg>',
 "share": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="18" cy="5" r="2.5"/><circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="19" r="2.5"/><path d="M8.2 10.8l7.6-4.4M8.2 13.2l7.6 4.4"/></svg>',
}
CAT_IC = [
 ("Restaurants", "/restaurant", '<path d="M7 3v8M5 3v5a2 2 0 0 0 4 0V3M7 11v10M16 3c-2 0-3 2-3 6s1 4 3 4v8"/>'),
 ("Home Services", "/home-services", '<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-5h4v5"/>'),
 ("Contractors", "/contractor", '<path d="M3 21h18M5 21V10l7-5 7 5v11"/><path d="M9 21v-6h6v6"/>'),
 ("Health & Wellness", "/health-wellness", '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>'),
 ("Real Estate", "/real-estate-services", '<path d="M4 20V9l8-5 8 5v11z"/><path d="M9 13h6M9 16h6"/>'),
 ("Attorneys", "/attorney", '<path d="M12 4v16M5 20h14M6 8h12M6 8l-3 6a3 3 0 0 0 6 0zM18 8l-3 6a3 3 0 0 0 6 0z"/>'),
 ("Beauty", "/beauty-personal-care", '<path d="M6 4l8 8M14 4l-8 8"/><circle cx="6" cy="17" r="3"/><circle cx="16" cy="17" r="3"/>'),
 ("Financial", "/financial-services", '<rect x="3" y="6" width="18" height="12" rx="2"/><circle cx="12" cy="12" r="2.5"/>'),
 ("All categories", "/categories", '<rect x="4" y="4" width="7" height="7" rx="1.5"/><rect x="13" y="4" width="7" height="7" rx="1.5"/><rect x="4" y="13" width="7" height="7" rx="1.5"/><rect x="13" y="13" width="7" height="7" rx="1.5"/>'),
]
STD_EV = ("/this-weekend", "/events", "/events-calendar")


def _clean(t):
    t = html.unescape(re.sub(r"<[^>]+>", "", t or ""))
    t = "".join(ch for ch in t if ord(ch) < 0x2190)
    t = re.sub(r"\s+", " ", t).strip()
    if t.lower() == "local stories":
        return "Three Village Local Blog"
    return "Get the Mobile App" if t.lower() == "get the app" else t


def _abs(h):
    return SITE + h if h.startswith("/") else h


def menu():
    """BD main menu (menu 52) as [(label, url, [(label, url)...])], read from the live site's mobile menu. Defaults if that fails."""
    out = []
    try:
        h = nhb.get(SITE + "/")
        m = re.search(r'<div class="mobile-main-menu">\s*<ul class="sidebar-nav">(.*?)</ul>\s*</div>', h, re.S)
        for it in re.finditer(r"<li[^>]*><a href='([^']*)'[^>]*>(.*?)</a>(?:<ul>(.*?)</ul>)?</li>", m.group(1), re.S):
            kids = [(_clean(k.group(2)), _abs(k.group(1))) for k in re.finditer(r"<a href='([^']*)'[^>]*>(.*?)</a>", it.group(3) or "")]
            out.append((_clean(it.group(2)), _abs(it.group(1)), kids))
    except Exception:
        out = []
    if len(out) < 3:
        out = [("Home", SITE + "/", []), ("Find a Local Business", SITE + "/categories", []),
               ("Things to Do", SITE + "/events", [("This Weekend", SITE + "/this-weekend"), ("All Events", SITE + "/events"), ("Events Calendar", SITE + "/events-calendar")]),
               ("Three Village Local Blog", SITE + "/blog", []), ("Get the Mobile App", SITE + "/app", [])]
    return out


def hero(d, img, base=""):
    """Prototype header: compact white top bar (logo, search, Google rating, Contact/Login/My Plans/Join, hamburger),
    navy menu strip, category quick links, then the thin live "today" strip. The search form is .tvl-ns, so smartsearch.js
    attaches its suggestions to it (it looks for .wk-hero .wk-dek, kept as a hidden anchor)."""
    mn = menu()
    links, hl = [], ""
    for i, (t, u, kids) in enumerate(mn):
        if kids:
            links.append('<span class="yh-dd"><a href="%s">%s</a><span class="yh-ddm">%s</span></span>' % (
                esc(u), esc(t), "".join('<a href="%s">%s</a>' % (esc(ku), esc(kt)) for kt, ku in kids)))
            sp = next(((kt, ku) for kt, ku in kids if ku.replace(SITE, "").rstrip("/") not in STD_EV), None)
            if sp:
                hl = '<a class="yh-hl" href="%s">%s</a>' % (esc(sp[1]), esc(sp[0]))
        else:
            cls = "on" if i == 0 else ("yh-applink" if u.rstrip("/").endswith("/app") else "")
            links.append('<a href="%s"%s>%s</a>' % (esc(u), (' class="%s"' % cls) if cls else "", esc(t)))
    cats = "".join('<a class="yh-q" href="%s%s"><span class="yh-qi"><svg viewBox="0 0 24 24" aria-hidden="true">%s</svg></span><span>%s</span></a>' % (
        SITE, u, sv, esc(t)) for t, u, sv in CAT_IC)
    return (
        '<script>try{var u=navigator.userAgent||"";if(!/FBAN|FBAV|FB_IAB|Instagram/.test(u)&&((/iPhone|iPad|iPod/.test(u)&&!/Safari/.test(u))||(/Android/.test(u)&&u.indexOf("; wv)")>-1)))document.documentElement.classList.add("tvl-inapp");}catch(e){}</script>'
        '<div class="wk-hero y-ssanchor" hidden><p class="wk-dek"></p></div>'
        '<h1 class="y-vh">Three Village Local: events, specials, weather and local news for Setauket, Stony Brook and Port Jefferson</h1>'
        '<header class="yh" data-nosnippet><div class="yh-in">'
        '<a class="yh-logo" href="{S}/" aria-label="Three Village Local home"><img src="https://threevillagelocal-cloud.github.io/3vl-share/live/hdr/logo-540.webp" width="167" height="52" alt="Three Village Local" fetchpriority="high"></a>'
        '<form class="yh-srch tvl-ns" action="/search_results" method="get" role="search"><span class="yh-si">{SEARCH}</span>'
        '<input type="search" name="q" placeholder="Search local businesses" aria-label="Search local businesses" autocomplete="off"><button type="submit">Search</button></form>'
        '<div class="yh-r"><a class="yh-gr" href="https://maps.google.com/?cid=15405294417866042762" target="_blank" rel="noopener" aria-label="Rated 5.0 on Google"><b>5.0</b><span class="yh-grs">&#9733;&#9733;&#9733;&#9733;&#9733;</span><em>Google</em></a>'
        '<a class="yh-tl" href="{S}/about/contact">Contact</a><a class="yh-tl" href="{S}/login">Login</a>'
        '<button type="button" class="yh-plans" id="wk-fab" aria-controls="wk-drawer" aria-expanded="false" aria-label="My Plans">{STAR}<span>My Plans</span><b id="wk-fabn">0</b></button>'
        '<a class="yh-join" href="{S}/join">Businesses - Join Today</a>'
        '<button type="button" class="yh-mnu" id="yh-mnu" aria-label="Menu" aria-expanded="false" aria-controls="yh-mn">{MENU}</button></div></div>'
        '<nav class="yh-mn" id="yh-mn" aria-label="Main menu"><div class="yh-mnin">{LINKS}<span class="yh-sp"></span>{HL}'
        '<a class="yh-mob" href="{S}/about/contact">Contact</a><a class="yh-mob" href="{S}/login">Login</a><a class="yh-mob yh-mobj" href="{S}/join">Businesses - Join Today</a></div></nav>'
        '<div class="yh-ql"><div class="yh-qlin">{CATS}</div></div></header>'
        '<div class="yh-today" data-nosnippet><div class="yh-tdin">'
        '<span class="yh-tc"><b id="wk-hdate">--</b> <span id="wk-hclock">--:--</span></span>'
        '<a class="yh-tc" href="#wk-sched"><i class="yh-dot"></i><b>Happening now: <span id="wk-hnow">--</span></b><span class="yh-ts" id="wk-hnext">checking&hellip;</span></a>'
        '<a class="yh-tc" href="#wk-wx"><b>Setauket <span class="wk-hwi2" id="wk-hwi2"></span><span id="wk-htemp">--</span>&deg;</b><span class="yh-ts" id="wk-hsky">loading&hellip;</span></a>'
        '<span class="yh-tsp"></span><span class="yh-tj">Jump to <a href="#wk-picks">Things to Do</a><a href="#wk-eat">Eat &amp; Drink</a><a href="#wk-sched">Schedule</a><a href="#wk-wx">Weather</a></span>'
        '</div></div>'
    ).replace("{S}", SITE).replace("{B}", base).replace("{SEARCH}", IC["search"]).replace("{STAR}", IC["star"]).replace("{MENU}", IC["menu"]) \
     .replace("{LINKS}", "".join(links)).replace("{HL}", hl).replace("{CATS}", cats)


def _words(t):
    return set(re.findall(r"[a-z]{4,}", (t or "").lower()))


def _webp_w(path):
    """Pixel width of a .webp file from its header (no image library needed in the nightly job). 0 if unknown."""
    try:
        b = open(path, "rb").read(40)
        if b[12:16] == b"VP8X":
            return 1 + int.from_bytes(b[24:27], "little")
        if b[12:16] == b"VP8 ":
            return int.from_bytes(b[26:28], "little") & 0x3FFF
        if b[12:16] == b"VP8L":
            return 1 + (int.from_bytes(b[21:25], "little") & 0x3FFF)
    except Exception:
        pass
    return 0


ROT_MS = 1800000   # owner 10/24/2026: a different lead story every 30 minutes


def lead_open(d, ev, V, img, evattrs, actions, tagchips, dshort, fmt_time, CAL):
    """Tabs + the lead story of Top Things to Do. Every pick with its own photo gets a lead article; an inline script right after them
    picks the one for the current 30-minute slot (same for every visitor, ?slot=N to test) before the page paints and loads only its photo.
    The week's hero photo stands in for the pick it belongs to (its credit/alt names the event)."""
    tabs = ('<div class="y-tabs" role="tablist"><button type="button" role="tab" class="on" aria-selected="true" data-y="tp">Top Picks</button>'
            '<button type="button" role="tab" aria-selected="false" data-y="td">Today <b class="y-tdn"></b></button>'
            '<button type="button" role="tab" aria-selected="false" data-y="cu">Coming Up</button></div>')
    cand = [ev[p] for p in d["picks"] if p in ev]
    h = d.get("hero") or {}
    hw = _words(h.get("credit", "") + " " + h.get("alt", ""))
    hero_of = next((e for e in cand if len(_words(e["title"]) & hw) >= 2 and h.get("img")), None)
    from datetime import datetime, timedelta
    edir = os.path.dirname(HERE)
    arts, titles = [], []
    for le in cand:
        if le is hero_of:
            name, alt, credit = h["img"], h.get("alt") or le["title"], re.sub(r"^.*?Photo:\s*", "", h.get("credit", ""))
        elif le.get("img"):
            name, alt, credit = le["img"], le["title"], le.get("credit", "")
        else:
            continue
        ed = img("x")[:-len("x.webp")]
        full = img(name)
        fw = _webp_w(os.path.join(edir, d.get("_edition", ""), name + ".webp")) if d.get("_edition") else 0
        srcset = "%s 360w, %s 540w, %s 720w" % (ed + name + "-360.webp", ed + name + "-540.webp", ed + name + "-720.webp")
        if fw > 760:
            srcset += ", %s %dw" % (full, fw)
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
        until = le.get("pick_until") or le.get("until") or le.get("end") or ""
        if until and "T" not in until:
            until += "T23:59"
        if until:
            try:
                until = until[:16] + nhb.et_offset(datetime.fromisoformat(until[:16]))
            except Exception:
                until = ""
        i = len(arts)
        arts.append(
            ('<article class="y-lead"%s data-href="%s" data-until="%s" %s><a class="y-leadimg" href="%s" tabindex="-1" aria-hidden="true"><figure class="y-leadpic">'
             '<img class="wk-hbg" data-src="%s" data-srcset="%s" alt="%s" width="1600" height="1000">%s'
             '<span class="wk-pnum">01</span><span class="wk-pstat" data-status></span></figure></a>'
             '<div class="y-leadb"><p class="wk-pwhen">%s</p><h3 class="y-leadt"><a href="%s">%s</a></h3><p class="wk-pwhere">&#128205; %s</p>'
             '<p class="y-leadd">%s</p><div class="wk-tags">%s</div>%s%s</div></article>') % (
                "" if i == 0 else " hidden", esc(page), esc(until), evattrs(le), esc(page),
                esc(ed + name + "-720.webp"), esc(srcset), esc(alt),
                ('<noscript><img class="wk-hbg" src="%s" alt="%s"></noscript>' % (esc(ed + name + "-720.webp"), esc(alt))) if i == 0 else "",
                when, esc(page), esc(le["title"]), esc(V[le["venue"]]["name"]), esc(le.get("desc", "")), tagchips(le.get("tags", [])), acts,
                ('<p class="y-cred">Photo: %s</p>' % esc(credit)) if credit else ""))
        titles.append(le["title"])
    if not arts:
        return tabs + '<div class="y-tp">'
    # runs while the page is being read, before the first paint (no backslashes: BD strips them from widget code)
    js = ("<script>(function(){var L=document.getElementById('y-leads');if(!L)return;"
          "window.__yLeadPick=function(s){var a=[].slice.call(L.querySelectorAll('article.y-lead')),n=Date.now(),"
          "ok=a.filter(function(x){var u=x.getAttribute('data-until');return !u||isNaN(Date.parse(u))||Date.parse(u)>n});if(!ok.length)ok=a;"
          "var k=s%ok.length,el=ok[k];a.forEach(function(x){x.hidden=x!==el});var im=el.querySelector('img[data-src]');"
          "if(im){im.setAttribute('fetchpriority','high');im.sizes='(max-width:900px) 100vw, 560px';im.srcset=im.getAttribute('data-srcset');im.src=im.getAttribute('data-src');im.removeAttribute('data-src')}"
          "var o=ok.slice(k).concat(ok.slice(0,k)).map(function(x){return (x.querySelector('.y-leadt')||{}).textContent||''});"
          "L.parentNode.setAttribute('data-lead',o[0]);window.__ylead={slot:s,k:k,n:ok.length,order:o};return el};"
          "var q=location.search.match(/[?&]slot=([0-9]+)/),s=q?+q[1]:Math.floor(Date.now()/ROTMS);window.__yLeadFixed=!!q;window.__yLeadPick(s)})()</script>").replace("ROTMS", str(ROT_MS))
    return tabs + '<div class="y-tp" data-lead="%s"><div class="y-leads" id="y-leads">%s</div>%s' % (esc(titles[0]), "".join(arts), js)


def quick():
    return ""   # the quick-link row is part of hero() now


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


SHARE = "https://threevillagelocal-cloud.github.io/3vl-share/"


def spotlight(base=""):
    """Local Business Spotlight from each VIP's CURRENT v3 profile (3vl-share live/p3/vip/<uid>.json), read on every build.
    Photos come from 3vl-share t/vip.json: small copies (12:5 big 640/960/1280, 4:3 thumb 240) that 3vl-share t/gen.py makes
    from those profiles every 30 minutes, keyed by a hash of the source file. Every copy is HEAD-checked at build time and every
    image carries its original as a fallback (data-o / data-bgo, front.js fixImgs), so a replaced or missing copy never shows a broken image."""
    vips = _vips()
    if not vips:
        return ""
    idx = _get_json(SHARE + "t/vip.json") or {}
    OK = lambda u: bool(u) and _ok(u)
    ONERR = 'onerror="if(this.dataset.o){this.removeAttribute(&quot;srcset&quot;);this.src=this.dataset.o;this.dataset.o=&quot;&quot;}"'
    cards, logos = [], []
    for m in vips:
        uid = str(m["id"])
        j = _get_json(VIPBASE + uid + ".json") or {}
        h = j.get("hero") or {}
        x = idx.get(uid) or {}
        fresh = bool(x) and x.get("src") == h.get("img")          # copies made from the photo the profile uses today
        logo_o = (VIPBASE + j["logo"]) if j.get("logo") else nhb.sm(m.get("l"), 200)
        lc = (SHARE + x["logo"]) if fresh and x.get("logo") and not x["logo"].startswith("http") else ""
        logo = lc if lc and OK(lc) else logo_o
        logos.append('<a class="y-lg" href="%s" title="%s"><span style="background-image:url(\'%s\')" data-bgo="%s"></span><i class="y-vh">%s</i></a>' % (
            esc(m["u"]), esc(m["n"]), esc(logo), esc(logo_o), esc(m["n"])))
        if uid in NO_SPOT:
            continue
        banner = bool(h.get("banner"))
        alt = (h.get("alt") or "")
        plain = (not h.get("img")) or (not banner and ("background" in alt.lower() or "monogram" in alt.lower()))
        big_o = (VIPBASE + h["img"]) if h.get("img") else ""
        thumb_o = (VIPBASE + j["headshot"]) if banner and j.get("headshot") else big_o
        if plain:
            big, srcset, thumb = "", "", ""
        elif fresh and x.get("big640") and OK(SHARE + x["big640"]) and OK(SHARE + x.get("thumb", "")):
            big = SHARE + x["big640"]
            srcset = ", ".join("%s %sw" % (SHARE + x[k], k[3:]) for k in ("big640", "big960", "big1280") if x.get(k) and (k == "big640" or OK(SHARE + x[k])))
            thumb = SHARE + x["thumb"]
        else:
            big, srcset, thumb = big_o, "", thumb_o
        cat = j.get("category") or m.get("c") or ""
        twn = nhb.town(m.get("t"))
        desc = (j.get("sub") or j.get("tagline") or "").replace(chr(0x2014), "-").replace(chr(0x2013), "-")
        tel = re.sub(r"\D", "", m.get("ph") or j.get("phone") or "")
        color = ((j.get("theme") or {}).get("navy") or "#16304f")
        if not re.fullmatch(r"#[0-9a-fA-F]{3,8}", color):
            color = "#16304f"
        pos = "50% 50%" if (fresh or banner) else (h.get("pos") or "50% 50%")
        vis = ('<img src="%s" data-o="%s" %s alt="" loading="lazy" width="240" height="180" style="object-position:%s">' % (
                   esc(thumb), esc(thumb_o if thumb_o != thumb else ""), ONERR, esc(pos))) if thumb else \
              '<span class="y-panel" style="--c:%s"><span class="y-plogo" style="background-image:url(\'%s\')" data-bgo="%s"></span></span>' % (color, esc(logo), esc(logo_o))
        cards.append(
            '<a class="y-mc" href="%s" data-id="%s" data-img="%s" data-imgo="%s" data-srcset="%s" data-ban="%s" data-pos="%s" data-alt="%s" data-logo="%s" data-logoo="%s" data-cat="%s" data-town="%s" data-desc="%s" data-tel="%s" data-color="%s">'
            '<span class="y-mci">%s</span><span class="y-mct"><b>%s</b><small>%s</small></span></a>' % (
                esc(m["u"]), uid, esc(big), esc(big_o), esc(srcset), "1" if banner else "", esc(pos), esc(alt or m["n"]), esc(logo), esc(logo_o), esc(cat), esc(twn), esc(desc), tel, color,
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


def stories_main(skip=0, n=5):
    """Local Stories in the main column: the newest posts from /blog (lead + smaller cards). Refreshed on every nightly build."""
    st = nhb.stories(n + skip)[skip:skip + n]
    if not st:
        return ""
    cards = []
    for i, x in enumerate(st):
        full = x["img"].replace("news-pictures-thumbnails", "news-pictures") if x["img"] else ""
        pic = (nhb.sm(full, 800) if i == 0 else nhb.sm(full, 300)) if x["img"] else ""   # full post image (never BD's cropped thumbnail)
        orig = full
        big = nhb.sm(full, 800) if (x["img"] and i) else ""
        ss = (' srcset="%s 360w, %s 800w" sizes="240px"' % (esc(pic), esc(big))) if big and big != full and pic != full else ""
        img = ('<img src="%s"%s data-o="%s" onerror="if(this.dataset.o){this.src=this.dataset.o;this.dataset.o=&quot;&quot;;this.removeAttribute(&quot;srcset&quot;)}" alt="" loading="lazy" width="%d" height="%d">' % (
            esc(pic), ss, esc(orig), 800 if i == 0 else 360, 450 if i == 0 else 240)) if pic else ""
        cards.append('<a class="y-st%s" href="%s"><span class="y-sti">%s</span><span class="y-stb"><i>%s</i><b>%s</b>%s</span></a>' % (
            " y-stl" if i == 0 else "", esc(x["h"]), img, esc(x["d"]), esc(x["t"]), '<em class="y-stgo">Read the story ' + IC["chev"] + '</em>' if i == 0 else ""))
    return ('<section class="wk-sec y-stories" id="y-stories"><h2 class="wk-h2"><span>Three Village Local Blog</span><small>News and guides from around Three Village</small>'
            '<a class="wk-calbtn y-seeall" href="/blog">See the blog ' + IC["chev"] + '</a></h2>'
            '<div class="y-stg">%s</div><p class="y-endbtn"><a class="y-bigbtn" href="/blog">All blog posts %s</a></p></section>') % ("".join(cards), IC["chev"])


def stories_rail():
    """Owner 10/24: the blog lives in the main column only; nothing in the rail."""
    return ""
    st = nhb.stories(8)[5:8]
    if not st:
        return ""
    row = "".join('<a class="nh-story" href="%s"><span class="nh-sim" style="background-image:url(\'%s\')" data-bgo="%s"></span><span class="nh-sb">%s<b>%s</b></span></a>' % (
        esc(x["h"]), esc(nhb.sm(x["img"], 300)), esc(x["img"]), ("<i>%s</i>" % esc(x["d"])) if x["d"] else "", esc(x["t"])) for x in st)
    return ('<section class="wk-sec nh-sec" id="nh-stories">' + nhb.head("More Local Stories", "", "/blog", "All stories")
            + '<div class="nh-row" id="nh-srow">' + row + "</div></section>")


MIDCATS = [("Restaurants", "/restaurant"), ("Contractors", "/contractor"), ("Landscaping", "/landscaping-property-maintenance"),
           ("Plumbing & Electric", "/plumbing-electric-repairs"), ("Health & Wellness", "/health-wellness"), ("Real Estate", "/real-estate-services"),
           ("Attorneys", "/attorney"), ("Beauty", "/beauty-personal-care")]


def midsearch():
    """Second business search between Eat & Drink and the Spotlight. Same engine as the top bar (front.js, window.tvlSS)."""
    chips = "".join('<a href="%s%s">%s</a>' % (SITE, u, esc(t)) for t, u in MIDCATS)
    return ('<section class="wk-sec y-mid" id="y-midsearch" aria-labelledby="y-midh"><h2 class="y-midh" id="y-midh">Find a local business or service</h2>'
            '<p class="y-midd">Plumbers, dentists, lawyers, landscapers, pizza and more, rated by your neighbors.</p>'
            '<form class="y-msf" id="y-msf" action="/search_results" method="get" role="search"><span class="y-msi">' + IC["search"] + '</span>'
            '<input type="search" name="q" placeholder="What do you need? Try &quot;plumber&quot; or &quot;pizza&quot;" aria-label="Search local businesses and services" autocomplete="off">'
            '<button type="submit">Search</button></form><div class="y-mschips" id="y-mschips">' + chips + '<a class="y-msall" href="' + SITE + '/categories">All categories ' + IC["chev"] + '</a></div></section>')


def endbtn(href, label):
    return '<p class="y-endbtn"><a class="y-bigbtn" href="%s">%s %s</a></p>' % (href, label, IC["chev"])


def cta(base):
    root = base[:-len("weekender/")]
    return ('<section class="wk-sec wk-cta y-cta" aria-label="Get involved">'
            '<div class="y-cc"><p class="y-cct">Submit an event, business special or promotion</p>'
            '<p class="y-ccd">Three Village Local is updated every day and seen by thousands of neighbors. Send us your event, special or promotion.</p>'
            '<a class="y-btn" href="{S}/promotion">Submit it {CH}</a><p class="y-ccs">Own a local business? <a href="{S}/join">Join here</a></p></div>'
            '<div class="y-cc"><p class="y-cct">Send this to your crew</p><p class="y-ccd">Share the page with friends and family, or share the plans you saved.</p>'
            '<div class="y-ccb"><button type="button" class="y-btn o" id="wk-share">{SH}Share Three Village Local</button><button type="button" class="y-btn o" id="wk-share2">{ST}Share my plan</button></div></div>'
            '<div class="y-cc y-app"><p class="y-cct">Get Three Village Local on your phone</p>'
            '<p class="y-ccd">The free Three Village Local mobile app puts today&rsquo;s events, local specials and neighbor-rated businesses right on your phone.</p>'
            '<div class="y-badges"><a href="https://apps.apple.com/us/app/three-village-local/id6746367200" target="_blank" rel="noopener"><img src="{R}badges/app-store-badge-400.webp" width="142" height="50" alt="Download on the App Store" loading="lazy"></a>'
            '<a href="https://play.google.com/store/apps/details?id=com.threevillagelocal.app&amp;hl=en_US" target="_blank" rel="noopener"><img src="{R}badges/google-play-badge-470.webp" width="168" height="50" alt="Get it on Google Play" loading="lazy"></a></div></div></section>'
            ).replace("{S}", SITE).replace("{CH}", IC["chev"]).replace("{SH}", IC["share"]).replace("{ST}", IC["star"]).replace("{R}", root)


def footer(base):
    fb = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 8h3V4h-3a4 4 0 0 0-4 4v2H7v4h3v7h4v-7h3l1-4h-4V8z"/></svg>'
    ig = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="4" width="16" height="16" rx="5"/><circle cx="12" cy="12" r="3.5"/></svg>'
    return ('<footer class="yf"><div class="yf-in">'
            '<div class="yf-a"><img src="{B}front/img/logo-white.webp" width="149" height="50" alt="Three Village Local" loading="lazy"><p>Three Village Local is the free local guide to Setauket, Stony Brook, Port Jefferson and the Three Village area. '
            'Find trusted local businesses, this week&rsquo;s events, restaurant specials and community news, all in one place, and support the neighbors who make our community special.</p></div>'
            '<div class="yf-c"><b>Website</b><a href="{S}/about">How It Works</a><a href="{S}/about/contact">Contact Us</a><a href="{S}/newsletter">Three Village Weekly</a></div>'
            '<div class="yf-c"><b>Search</b><a href="{S}/search_results">Browse Directory</a><a href="{S}/categories">Search by Category</a></div>'
            '<div class="yf-c"><b>Explore</b><a href="{S}/whats-new">What&rsquo;s New</a><a href="{S}/restaurants-stony-brook">Restaurants in Stony Brook</a>'
            '<a href="{S}/restaurants-setauket">Restaurants in Setauket</a><a href="{S}/restaurants-port-jefferson">Restaurants in Port Jefferson</a><a href="{S}/halloween">Halloween in Three Village</a></div>'
            '<div class="yf-c"><b>Support</b><a href="{S}/login">Member Login</a><a href="{S}/login/retrieval">Reset Password</a></div></div>'
            '<div class="yf-in yf-2"><span class="yf-soc"><a href="{S}/about/contact" aria-label="Email">{MAIL}</a><a href="https://www.facebook.com/ThreeVillageLocal" aria-label="Facebook" target="_blank" rel="noopener">{FB}</a>'
            '<a href="https://www.instagram.com/threevillagelocal/" aria-label="Instagram" target="_blank" rel="noopener">{IG}</a></span><a class="yf-join" href="{S}/join">Businesses - Join Today</a></div>'
            '<p class="yf-copy">&copy; 2026 Three Village Local. All Rights Reserved. <a href="{S}/about/terms">Terms of Use</a> <a href="{S}/about/privacy">Privacy Policy</a></p></footer>'
            ).replace("{S}", SITE).replace("{B}", base).replace("{MAIL}", IC["mail"]).replace("{FB}", fb).replace("{IG}", ig)


def post(body):
    """Text clean-ups so the front layout reads like the prototype (no emoji arrows in links, plain chips, svg icons)."""
    ch = IC["chev"]
    for old, new in (("&#128197; See all things to do &rarr;", "See all things to do " + ch), ("&#127869;&#65039; See all specials &rarr;", "See all specials " + ch),
                     ("&#128197; Full calendar &rarr;", "Full calendar " + ch), ("All stories &rarr;", "All stories " + ch),
                     ("See all businesses &rarr;", "See all businesses " + ch), ("Advertise here &rarr;", "Advertise here " + ch),
                     ("View on 3VL &rarr;", "View on 3VL " + ch), ("&#128222; Call", IC["phone"] + "Call"),
                     ("See the listings &rarr;", "See the listings " + ch), ("Sign up free &rarr;", "Sign up free " + ch),
                     ('<span class="wk-nlic" aria-hidden="true">&#9993;&#65039;</span>', '<span class="wk-nlic" aria-hidden="true">' + IC["mail"] + '</span>'),
                     ("<span>&#11088; VIP</span>", "<span>VIP</span>"),
                     ("&#128197; Add</button>", IC["cal"] + "Add</button>"), ("&#128205; Map</a></div>", IC["pin"] + "Map</a></div>")):
        body = body.replace(old, new)
    # lighter photos: pick rows are ~120px wide (the 360 copy is sharp at 2x), weather thumbnails are 56px
    body = body.replace('sizes="280px"', 'sizes="120px"')
    body = body.replace('<div class="wk-adslot', '<div data-nosnippet class="wk-adslot').replace('<div class="wk-adrot', '<div data-nosnippet class="wk-adrot')   # VIP ad rotators stay out of search snippets
    body = body.replace(' data-cam="', ' data-ycam="')   # no hidden camera iframe: the thumbnail links to the live camera instead (front.js)
    body = re.sub(r'<img src="([^"]+/homes/[^"]+)"', r'<img data-ysrc="'+chr(92)+r'1"', body)   # homes thumbnails load only near the screen (front.js)
    body = re.sub(r'(<img class="wk-wph" src="[^"]+)-720[.]webp"', r'\1-360.webp"', body)
    body = re.sub(r'(<button type="button" class="wk-chip" data-tag="[a-z]+">)(?:&#[0-9]+;)+ ', r"\1", body)
    return body
