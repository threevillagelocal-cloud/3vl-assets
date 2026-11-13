"""Membership page v2 (/join redesign) - PREVIEW builder.
    python site/join-v2/build.py            -> widget "3VL Page Join Preview" + hidden page /preview-join (noindex)
    python site/join-v2/build.py --local    -> writes _local/index.html only (local test harness, nothing published)
    python site/join-v2/build.py --dry      -> prints sizes, publishes nothing
There is deliberately NO --live switch here: the live /join is widget 15 "3VL Page Join" (guarded copy in
3vl-site-guard post-sources/widget-15-3vl-page-join.html). Going live = copy the approved output there, with the owner's OK.

Prices in PRICE are proposed (preview only). Partner has no checkout plan yet: its button goes to the services form.
"""
import html as _html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LOCAL = "--local" in sys.argv
DRY = "--dry" in sys.argv
assert "--live" not in sys.argv, "no --live here: preview only (see docstring)"

NAME = "3VL Page Join Preview"
SLUG = "preview-join"
TITLE = "Memberships for Local Businesses: Featured, VIP and Partner | Three Village Local"
DESC = ("Get your business seen by Setauket, Stony Brook and Port Jefferson. Free listings, Featured and VIP memberships and the new "
        "Partner plan: premium profiles, homepage spotlights, social promotion, a Member Dashboard and more. Month to month.")
FB_TITLE = "Get your business seen by the neighbors."
FB_IMAGE = "/share/site-hero.webp"

SH = "https://threevillagelocal-cloud.github.io/3vl-share/site/join-v2/"
VIDEO = "https://threevillagelocal-cloud.github.io/3vl-share/live/p3/vip/img/666-loop-480.mp4"
LOGO3 = "https://threevillagelocal-cloud.github.io/3vl-share/site/icon-192.png"
PRICE = {"free": 0, "featured": 42, "vip": 135, "partner": 349}          # proposed, preview only
CHECKOUT = {"free": "/checkout/6", "featured": "/checkout/2", "vip": "/checkout/1", "partner": "/services#tvs-book"}

# ---------- icons (stroke style, shared with svc-kit) ----------
_src = open(os.path.join(HERE, "..", "svc-kit", "kit.py"), encoding="utf-8").read()
I = eval(_src[_src.index("_I = {") + 5:_src.index("\n}\n", _src.index("_I = {")) + 2])
I.update({
    "qr": '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><path d="M14 14h3v3h-3zM21 14v.01M14 21h.01M17 21h4v-3"/>',
    "bell": '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.9 1.9 0 0 0 3.4 0"/>',
    "insta": '<rect x="2" y="2" width="20" height="20" rx="5.5"/><circle cx="12" cy="12" r="4.2"/><path d="M17.6 6.4h.01"/>',
    "percent": '<path d="M19 5 5 19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/>',
    "crown": '<path d="m3 17 1.5-10 4.5 4 3-6 3 6 4.5-4L21 17z"/><path d="M3 21h18"/>',
    "x": '<path d="M18 6 6 18M6 6l12 12"/>',
    "dash": '<rect x="3" y="3" width="8" height="10" rx="1.5"/><rect x="13" y="3" width="8" height="6" rx="1.5"/><rect x="13" y="11" width="8" height="10" rx="1.5"/><rect x="3" y="15" width="8" height="6" rx="1.5"/>',
    "banner": '<rect x="2" y="6" width="20" height="12" rx="2"/><path d="M6 10h7M6 14h4"/><circle cx="17.5" cy="12" r="2"/>',
    "lock": '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
    "chev": '<path d="m9 6 6 6-6 6"/>',
    "refresh": '<path d="M21 12a9 9 0 1 1-3-6.7L21 8"/><path d="M21 3v5h-5"/>',
    "drone": '<circle cx="5" cy="5" r="2.5"/><circle cx="19" cy="5" r="2.5"/><circle cx="5" cy="19" r="2.5"/><circle cx="19" cy="19" r="2.5"/><rect x="9" y="9" width="6" height="6" rx="1.5"/><path d="M7 7l2 2M17 7l-2 2M7 17l2-2M17 17l-2-2"/>',
})


USED = []


def ic(n, cls=""):
    """inline SVG icon via one shared sprite (keeps the widget small)"""
    assert n in I, n
    if n not in USED:
        USED.append(n)
    return '<svg class="jv-svg%s" aria-hidden="true" focusable="false"><use href="#jvi-%s"/></svg>' % ((" " + cls) if cls else "", n)


def sprite():
    return ('<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>' + "".join(
        '<symbol id="jvi-%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">%s</symbol>'
        % (n, I[n]) for n in USED) + '</defs></svg>')


def img(name, alt, w, h, cls="", lazy=True, extra=""):
    return '<img class="%s" src="%s%s" alt="%s" width="%d" height="%d"%s decoding="async" data-processed="true"%s>' % (
        cls, SH, name, _html.escape(alt, quote=True), w, h, ' loading="lazy"' if lazy else "", extra)


NEW = '<em class="jv-new">New</em>'

# ---------- plan cards ----------
PLANS = [
    {"k": "free", "tag": "Be listed", "name": "Just the Basics", "sub": "A simple way to be listed on Three Village Local.",
     "lead": "", "items": [("search", "Searchable listing on our website and mobile app"), ("camera", "1 photo plus your contact info"),
                           ("pin", "Map and category placement")],
     "btn": "Start free", "realtor": "Eligible for our weekly Real Estate Listings page, space permitting."},
    {"k": "featured", "tag": "Be found", "badge": "Most businesses start here", "name": "Featured",
     "sub": "A premium profile, priority placement and steady promotion across Three Village Local.", "lead": "",
     "items": [("star", NEW + "Premium custom profile, with video"), ("dash", NEW + "Member Dashboard: see everything we did for you"),
               ("bolt", "Featured badge and priority placement above free listings"),
               ("megaphone", "Category spotlights and newsletter mentions"),
               ("insta", NEW + "Your Instagram specials and events, shared into our feeds"),
               ("percent", NEW + "10% off all of our services")],
     "btn": "Choose Featured", "realtor": "Guaranteed weekly placement in the Featured section of our Real Estate Listings, right below VIP."},
    {"k": "vip", "tag": "Be seen everywhere", "badge": "Only 3 per category", "name": "Three Village VIP",
     "value": "Over $500 a month in marketing value if purchased separately",
     "sub": "For businesses that want the neighbors to know they are the best.", "lead": "Everything in Featured, plus:",
     "items": [("banner", "Banner ad rotating across the whole website"), ("search", "Top-spot card at the top of search with one-tap call"),
               ("article", NEW + "A custom article about you, every quarter"), ("crown", NEW + "VIP of the Week homepage spotlight"),
               ("bell", "One mobile app push notification a month"), ("video", "Video promotion plus drone photos and video included"),
               ("percent", NEW + "20% off all of our services")],
     "btn": "Request VIP availability", "fine": "Once a category's 3 VIP spots are filled, it closes.",
     "realtor": "Guaranteed Top 3 weekly placement at the very top of our Real Estate Listings feature."},
    {"k": "partner", "tag": "The works", "badge": "New", "name": "Partner",
     "sub": "We run your whole local playbook, on our channels and on yours.", "lead": "Everything in VIP, plus:",
     "items": [("bot", "AI chatbot for your website: answers customers 24/7 and texts you leads"),
               ("dash", "Company Digital Dashboard for your business"), ("edit", "Monthly social content made for your own accounts"),
               ("calendar", "Quarterly strategy call"), ("bolt", "Priority on everything we do")],
     "btn": "Talk to us about Partner", "fine": "Partner is set up with you personally, so it starts with a short call. No checkout needed.",
     "realtor": "Everything in VIP, including Top 3 weekly placement."},
]


def plan_card(p):
    k = p["k"]
    price = PRICE[k]
    pr = '<div class="jv-price"><b>$%d</b>%s</div>' % (price, "<small>/month</small>" if price else "<small>forever</small>")
    li = "".join('<li><span class="jv-li-ic">%s</span><span>%s</span></li>' % (ic(i), t) for i, t in p["items"])
    more = ""
    if k != "free":
        more = ('<button type="button" class="jv-see" data-jv-open="%s" aria-haspopup="dialog">%s<span>See everything you get</span>%s</button>'
                % (k, ic("eye"), ic("chev", "jv-see-ch")))
    btn_cls = {"free": "jv-btn-line", "featured": "jv-btn-blue", "vip": "jv-btn-gold", "partner": "jv-btn-navy"}[k]
    ext = ' data-jv-plan="%s"' % k
    out = '<article class="jv-card jv-%s" aria-labelledby="jv-n-%s">' % (k, k)
    if p.get("badge"):
        out += '<p class="jv-badge">%s</p>' % p["badge"]
    out += '<p class="jv-tag">%s</p><h3 class="jv-name" id="jv-n-%s">%s</h3>%s' % (p["tag"], k, p["name"], pr)
    if p.get("value"):
        out += '<p class="jv-value">%s</p>' % p["value"]
    out += '<p class="jv-sub">%s</p>' % p["sub"]
    if p["lead"]:
        out += '<p class="jv-lead">%s</p>' % p["lead"]
    out += '<ul class="jv-list">%s</ul>%s' % (li, more)
    out += '<div class="jv-cta"><a class="jv-btn %s" href="%s"%s>%s</a>' % (btn_cls, CHECKOUT[k], ext, p["btn"])
    if p.get("fine"):
        out += '<p class="jv-fine">%s</p>' % p["fine"]
    out += '</div><details class="jv-realtor"><summary>Realtor benefit</summary><p>%s</p></details></article>' % p["realtor"]
    return out


# ---------- comparison table ----------
Y = "y"
CMP = [
    ("Your listing and profile", [
        ("Searchable listing on our website and mobile app", Y, Y, Y, Y),
        ("Map and category placement", Y, Y, Y, Y),
        ("Photos", "1 photo", "Logo + up to 5", Y, Y),
        ("Enhanced business description", "", Y, Y, Y),
        ("Premium custom profile design, with video", "", Y, "VIP profile", "VIP profile"),
        ("Link to your website from a trusted local site", "", Y, Y, Y),
    ]),
    ("Placement", [
        ("Priority placement above free listings", "", Y, Y, Y),
        ("Plan badge on your listing", "", "Featured", "VIP", "VIP"),
        ("Top-spot card at the top of search, one-tap call", "", "", Y, Y),
        ("Top category placement (3 VIPs per category)", "", "", Y, Y),
        ("Banner ad rotating across the whole website", "", "", Y, Y),
        ("VIP of the Week homepage spotlight rotation", "", "", Y, Y),
        ("Priority in our AI answer pages", "", "", Y, Y),
    ]),
    ("Promotion", [
        ("Post events and specials on our website and mobile app", "", Y, Y, Y),
        ("Category spotlights and newsletter mentions", "", Y, Y, Y),
        ("Instagram specials and events shared into our feeds", "", Y, Y, Y),
        ("VIP spotlights on social, website and mobile app", "", "", Y, Y),
        ("Spotlights in our email campaigns", "", "", Y, Y),
        ("Mobile app push notification", "", "", "1 a month", "1 a month"),
        ("Custom article about your business", "", "", "Every quarter", "Every quarter"),
        ("Video promotion and drone photos and video", "", "Member discount", "Included", "Included"),
    ]),
    ("Tools and insight", [
        ("Member Dashboard: what Three Village Local did for you", "", Y, "Full", "Full"),
        ("AI visibility check", "", "Quarterly", "Quarterly", "Quarterly"),
        ("AI search tune-up", "", "", "Yearly", "Yearly"),
        ("Review-request kit (QR counter card + text template)", "", Y, Y, Y),
        ("Discount on all of our services", "", "10%", "20%", "20%"),
    ]),
    ("Partner only", [
        ("AI chatbot for your website, texts you every lead", "", "", "", Y),
        ("Company Digital Dashboard for your business", "", "", "", Y),
        ("Monthly social content for your own accounts", "", "", "", Y),
        ("Quarterly strategy call", "", "", "", Y),
        ("Priority on everything we do", "", "", "", Y),
    ]),
    ("The fine print", [
        ("Realtor benefit: weekly Real Estate Listings", "Space permitting", "Featured section", "Top 3", "Top 3"),
        ("Month to month, no long-term contract", Y, Y, Y, Y),
    ]),
]
COLS = [("free", "Free"), ("featured", "Featured"), ("vip", "VIP"), ("partner", "Partner")]


def cell(v, col):
    lab = dict(COLS)[col]
    if v == Y:
        return '<td class="jv-c-%s" data-l="%s"><span class="jv-yes" role="img" aria-label="Included">%s</span></td>' % (col, lab, ic("check"))
    if not v:
        return '<td class="jv-c-%s jv-no" data-l="%s"><span class="jv-dash" role="img" aria-label="Not included"></span></td>' % (col, lab)
    return '<td class="jv-c-%s" data-l="%s"><span class="jv-txt">%s</span></td>' % (col, lab, v)


def compare():
    head = '<tr><th scope="col" class="jv-th-f"><span class="jv-sr">Feature</span></th>' + "".join(
        '<th scope="col" class="jv-c-%s"><b>%s</b><i>%s</i></th>' % (k, n, ("$%d/mo" % PRICE[k]) if PRICE[k] else "$0") for k, n in COLS) + "</tr>"
    body = ""
    for g, rows in CMP:
        body += '<tbody><tr class="jv-grp"><th scope="colgroup" colspan="5">%s</th></tr>' % g
        for r in rows:
            body += '<tr><th scope="row">%s</th>%s</tr>' % (r[0], "".join(cell(v, k) for v, (k, _) in zip(r[1:], COLS)))
        body += "</tbody>"
    foot = '<tr class="jv-tfoot"><th scope="row"><span class="jv-sr">Choose a plan</span></th>' + "".join(
        '<td class="jv-c-%s"><a class="jv-btn jv-btn-sm %s" href="%s" data-jv-plan="%s">%s</a></td>' % (
            k, {"free": "jv-btn-line", "featured": "jv-btn-blue", "vip": "jv-btn-gold", "partner": "jv-btn-navy"}[k], CHECKOUT[k], k,
            {"free": "Start free", "featured": "Choose Featured", "vip": "Request VIP", "partner": "Talk to us"}[k]) for k, _ in COLS) + "</tr>"
    pin = '<div class="jv-pin" id="jv-pin" aria-hidden="true">' + "".join(
        '<span class="jv-c-%s"><b>%s</b><i>%s</i></span>' % (k, n, ("$%d/mo" % PRICE[k]) if PRICE[k] else "$0") for k, n in COLS) + "</div>"
    return ('<div class="jv-tblwrap" id="jv-tblwrap">%s<table class="jv-tbl" id="jv-tbl"><caption class="jv-sr">Compare membership plans</caption>'
            '<thead>%s</thead>%s<tfoot>%s</tfoot></table></div>') % (pin, head, body, foot)


# ---------- modal building blocks ----------
def phone(inner, cls=""):
    return '<div class="jv-phone %s"><div class="jv-phone-in">%s</div></div>' % (cls, inner)


def browser(inner, url="threevillagelocal.com", cls=""):
    return ('<div class="jv-browser %s"><div class="jv-browser-bar"><i></i><i></i><i></i><span>%s %s</span></div>%s</div>'
            % (cls, ic("lock"), url, inner))


def m_sec(id_, eyebrow, h, p, body):
    return ('<section class="jvm-sec" id="jvm-%s" data-sec="%s"><div class="jvm-head"><p class="jvm-eye">%s</p><h3>%s</h3>%s</div>%s</section>'
            % (id_, id_, eyebrow, h, ("<p>%s</p>" % p) if p else "", body))


def m_profile(k):
    vip = k != "featured"
    shots = (phone(img("prof-phone-1.webp", "Castaways profile on a phone: banner photo, badges, logo and one-tap Reserve, Call, Menu and Directions buttons", 540, 958)) +
             '<div class="jv-vidcard">' + phone('<video class="jv-vid" muted loop playsinline preload="none" data-src="%s" poster="%sc-video-poster-640.webp" aria-label="Castaways video playing on their profile"></video><span class="jv-vid-tag">%s Video on your profile</span>' % (VIDEO, SH, ic("play"))) + '</div>' +
             phone(img("prof-phone-2.webp", "Castaways profile photo gallery and occasion picker", 540, 918)) +
             phone(img("prof-phone-3.webp", "Castaways profile review buttons and FAQ", 540, 925)))
    pts = [("star", "Designed for you", "A custom layout in your colors and fonts, with your best photos up front."),
           ("video", "Video support", "Your video plays right on the profile. Reels, tours, behind the scenes."),
           ("phone", "One-tap actions", "Call, reserve, book, menu and directions, sized for thumbs."),
           ("search", "Built for Google and AI", "Clean facts, hours and FAQs that search engines and AI tools can read.")]
    if vip:
        pts[0] = ("crown", "VIP profile + VIP badge", "The premium design plus the VIP badge and top category placement.")
    bul = "".join('<li><span class="jv-li-ic">%s</span><div><b>%s</b><span>%s</span></div></li>' % (ic(i), t, d) for i, t, d in pts)
    return m_sec("profile", "Your premium profile", "A profile that looks like your own website.",
                 "Real example: Castaways Steak &amp; Seafood, a Featured member in Port Jefferson.",
                 '<div class="jvm-scroller" tabindex="0" role="region" aria-label="Profile screenshots, scroll sideways">%s</div>'
                 '<div class="jvm-split"><div>%s</div><ul class="jvm-pts">%s</ul></div>'
                 '<p class="jvm-link"><a href="/castaways-steak-seafood" target="_blank" rel="noopener">Open the live Castaways profile %s</a></p>'
                 % (shots, browser(img("prof-desk.webp", "Castaways profile on a computer screen", 1100, 688), "threevillagelocal.com/castaways-steak-seafood"), bul, ic("arrow")))


TL = [  # (filter, icon, thumb, date, title, note, tiers)
    ("web", "home", "c-spread-160.webp", "Nov 12", "On our homepage: Eat &amp; Drink pick", "Your raw bar special, front and center", "fvp"),
    ("social", "insta", "c-margarita-160.webp", "Nov 11", "Your special went out on Instagram", "Auto-shared from your account into our feeds", "fvp"),
    ("web", "crown", "c-patio-160.webp", "Nov 10", "VIP of the Week on our homepage", "Your photo, story and one-tap call, all week", "vp"),
    ("email", "mail", "c-oysters-160.webp", "Nov 7", "In this week's Three Village Weekly", "Featured in our email to local subscribers", "fvp"),
    ("social", "video", "c-grill-160.webp", "Nov 5", "Your reel posted", "Facebook and Instagram, with tag and collab", "fvp"),
    ("web", "bell", "c-tuna-160.webp", "Nov 4", "Mobile app push notification sent", "Live music tonight, straight to local phones", "vp"),
    ("ai", "sparkle", "", "Nov 3", "AI visibility check: 3 fixes done", "Hours, menu link and FAQs updated for AI search", "fvp"),
    ("web", "megaphone", "c-mussels-160.webp", "Nov 1", "Category spotlight: seafood in Port Jefferson", "On our website and mobile app", "fvp"),
]


def m_dash(k):
    t = {"featured": "f", "vip": "v", "partner": "p"}[k]
    plan = {"featured": "Featured member", "vip": "VIP member", "partner": "Partner"}[k]
    kp = [("home", 6, "", "times on our homepage this month", "Featured on our homepage 6 times"),
          ("share", 100000, "+", "social views your special went out to", ""),
          ("mail", 1, "", "this week's email", "In this week's email"),
          ("sparkle", 3, "", "AI visibility fixes done", "")]
    if t != "f":
        kp[2] = ("article", 0, "", "", "")
    tiles = ""
    for n, (i, v, suf, lab, _) in enumerate(kp):
        if i == "article":
            tiles += ('<div class="jvd-kpi jvd-kpi-art"><span class="jvd-ic">%s</span><b>Dec 4</b><i>Your next quarterly article: scheduled</i>'
                      '<span class="jvd-bar"><u style="--p:72%%"></u></span></div>' % ic("article"))
            continue
        lab2 = {0: "Featured on our homepage this month", 1: "Social views your special went out to", 2: "Spot in this week&#39;s email", 3: "Fixes done in your AI visibility check"}[n]
        suf = {0: "x"}.get(n, suf)
        tiles += '<div class="jvd-kpi"><span class="jvd-ic">%s</span><b><span data-n="%d">%s</span>%s</b><i>%s</i></div>' % (ic(i), v, "{:,}".format(v), suf, lab2)
    rows = ""
    for f, i, th, d, ti, note, tiers in TL:
        if t not in tiers:
            continue
        thumb = img(th, "", 160, 160, "jvd-th") if th else '<span class="jvd-th jvd-th-ic">%s</span>' % ic(i)
        rows += ('<li data-f="%s"><span class="jvd-dot">%s</span>%s<div><b>%s</b><i>%s</i></div><time>%s</time></li>'
                 % (f, ic(i), thumb, ti, note, d))
    up_tier = {"featured": ("vip", "Go VIP", "Banner ads, VIP of the Week and a custom article every quarter."),
               "vip": ("partner", "Become a Partner", "An AI chatbot, your own Company Dashboard and monthly content."),
               "partner": None}[k]
    disc = "10%" if t == "f" else "20%"
    ups = [("video", "Promo reel", "Filmed and edited for you", "/services#tvp-video"),
           ("globe", "AI website", "Built to be found on Google and AI", "/websites"),
           ("sparkle", "AI visibility report", "See how AI tools describe you", "/free-ai-report")]
    upl = "".join('<a class="jvd-up" href="%s"><span class="jvd-ic">%s</span><div><b>%s</b><i>%s</i></div><em>%s off</em></a>' % (h, ic(i), a, b, disc) for i, a, b, h in ups)
    if up_tier:
        upl += ('<button type="button" class="jvd-up jvd-up-tier" data-jv-open="%s"><span class="jvd-ic">%s</span><div><b>%s</b><i>%s</i></div><em>%s</em></button>'
                % (up_tier[0], ic("crown"), up_tier[1], up_tier[2], ic("chev")))
    news = [("New this week", "Holiday gift guide is open. Add your gift cards and specials."),
            ("Just launched", "Homepage trivia: neighbors play every Monday, with local business prizes."),
            ("Coming up", "Small Business Saturday spotlight. Tell us your deal by Nov 24.")]
    nl = "".join('<li><em>%s</em><span>%s</span></li>' % x for x in news)
    vip_row = ""
    if t != "f":
        vip_row = ('<div class="jvd-vipstrip"><span>%s<span><b>Banner ad</b> rotating on every page</span></span><span>%s<span><b>VIP of the Week</b> Nov 16 to 22</span></span>'
                   '<span>%s<span><b>Push notification</b> 1 left this month</span></span></div>' % (ic("banner"), ic("crown"), ic("bell")))
    dash = ('<div class="jvd" data-tier="%s">'
            '<div class="jvd-top"><img src="%s" alt="" width="34" height="34" class="jvd-3vl" loading="lazy" data-processed="true"><span class="jvd-brand">Member Dashboard</span>'
            '<span class="jvd-sign">%s Signed in</span></div>'
            '<div class="jvd-hi">%s<div><p class="jvd-k">%s &middot; November</p><p class="jvd-h">Welcome back, Castaways</p>'
            '<p class="jvd-s">Here is everything Three Village Local did for you this month.</p></div></div>'
            '<div class="jvd-kpis">%s</div>%s'
            '<div class="jvd-grid"><div class="jvd-card jvd-tl"><div class="jvd-ch"><b>Your promotion timeline</b>'
            '<div class="jvd-chips" role="group" aria-label="Filter the timeline"><button type="button" class="on" data-f="all" aria-pressed="true">All</button>'
            '<button type="button" data-f="web" aria-pressed="false">Website</button><button type="button" data-f="social" aria-pressed="false">Social</button>'
            '<button type="button" data-f="email" aria-pressed="false">Email</button><button type="button" data-f="ai" aria-pressed="false">AI</button></div></div>'
            '<ol class="jvd-list">%s</ol></div>'
            '<div class="jvd-side"><div class="jvd-card"><div class="jvd-ch"><b>What&#39;s new at 3VL</b></div><ul class="jvd-news">%s</ul></div>'
            '<div class="jvd-card"><div class="jvd-ch"><b>Grow with us</b><i>Member pricing</i></div><div class="jvd-ups">%s</div></div></div></div>'
            '<p class="jvd-foot">Example dashboard with sample activity. Your real dashboard shows what we did for your business.</p></div>'
            % (t, LOGO3, ic("lock"), img("c-logo-240.webp", "Castaways logo", 240, 145, "jvd-logo"), plan, tiles, vip_row, rows, nl, upl))
    return m_sec("dash", "Your Member Dashboard", "Sign in and see what we did for you.",
                 "Every homepage feature, post, email and fix, in one place. Tap the filters to try it.", dash)


def ig_mock(photo, cap):
    return ('<div class="jv-ig"><div class="jv-ig-h"><img src="%s" alt="" width="28" height="28" loading="lazy" data-processed="true"><b>threevillagelocal</b><span>and castawayspj</span></div>'
            '%s<div class="jv-ig-a">%s%s%s</div><p><b>threevillagelocal</b> %s</p></div>'
            % (LOGO3, img(photo, "Castaways photo in a Three Village Local Instagram post", 640, 360, "jv-ig-img"), ic("heart"), ic("message"), ic("share"), cap))


def m_seen(k):
    vip = k != "featured"
    cards = [
        ("Search", "Your top-spot card at the top of search, with one-tap call." if vip else "Priority placement above free listings, with your Featured badge.", phone(img("search-phone.webp", "Castaways shown as a Featured business at the top of restaurant search", 540, 568)) if not vip else
         phone('<div class="jv-topspot"><p class="jv-ts-k">%s VIP &middot; Restaurants</p><div class="jv-ts-row">%s<div><b>Castaways Steak &amp; Seafood</b><i>Port Jefferson &middot; Open now</i></div></div>'
               '<div class="jv-ts-btns"><span>%s Call</span><span>Directions</span><span>Profile</span></div></div>%s'
               % (ic("star"), img("c-storefront-160.webp", "", 160, 160), ic("phone"), img("search-phone.webp", "Search results under the VIP top spot", 540, 568)))),
        ("Homepage", "Spotlights in our Eat &amp; Drink, picks and category sections.",
         '<div class="jv-hm"><p class="jv-hm-k">Eat &amp; Drink <span>See all specials</span></p><div class="jv-hm-c">%s<div><em>Special</em><b>Raw bar happy hour</b><i>Castaways &middot; Port Jefferson</i></div></div></div>'
         % img("c-spread-640.webp", "Castaways special on the homepage", 640, 360)),
        ("Facebook and Instagram", "Your specials and events in front of 100,000+ views a month.",
         ig_mock("c-cocktail-640.webp", "Happy hour on Main Street at @castawayspj. Raw bar, craft cocktails, live music. #threevillagelocal #yourneighborsinbusiness")),
        ("Email", "Mentions in Three Village Weekly, the local email.",
         '<div class="jv-em"><div class="jv-em-h"><b>Three Village Weekly</b><span>This week in Three Village</span></div><div class="jv-em-r">%s<div><em>Eat &amp; Drink</em><b>Castaways Steak &amp; Seafood</b><i>Raw bar specials and live music on Main Street.</i></div></div><div class="jv-em-l"><u></u><u></u><u class="s"></u></div></div>'
         % img("c-oysters-160.webp", "", 160, 160)),
        ("Mobile app", "Your events and specials in the free Three Village Local mobile app.",
         phone('<div class="jv-app"><p class="jv-app-h">Today in Three Village</p><div class="jv-app-c">%s<div><em>Tonight</em><b>Live music at Castaways</b><i>7 PM &middot; Main Street, Port Jefferson</i></div></div><div class="jv-app-c">%s<div><em>Special</em><b>Oyster happy hour</b><i>Castaways &middot; 3 to 6 PM</i></div></div></div>'
               % (img("c-patio-160.webp", "", 160, 160), img("c-oysters-160.webp", "", 160, 160)), "jv-phone-sm")),
    ]
    if vip:
        cards.insert(1, ("Push notifications", "One push a month, straight to local phones.",
                         '<div class="jv-push"><div class="jv-push-t">9:41</div><div class="jv-push-n"><img src="%s" alt="" width="34" height="34" loading="lazy" data-processed="true"><div><b>Three Village Local <i>now</i></b><span>Castaways: live music tonight on Main Street. Tap for the lineup.</span></div></div></div>' % LOGO3))
    g = "".join('<div class="jv-seen-c"><div class="jv-seen-v">%s</div><b>%s</b><p>%s</p></div>' % (v, t, d) for t, d, v in cards)
    return m_sec("seen", "Where you will be seen", "Everywhere neighbors look.",
                 "45,000+ website page visits and 100,000+ Facebook &amp; Instagram views a month. 100% local audience.",
                 '<div class="jv-seen">%s</div>' % g)


def m_vip():
    banner = ('<div class="jv-ban"><div class="jv-ban-ph">%s</div><div class="jv-ban-tx">%s<b>Live music on Main Street</b><span>Prime steaks, raw bar, craft cocktails</span><em>Reserve a table</em></div></div>'
              % (img("c-patio-640.webp", "Castaways patio photo in an example banner ad", 640, 360), img("c-logo-240.webp", "Castaways logo", 240, 145, "jv-ban-logo")))
    votw = ('<div class="jv-votw"><p class="jv-votw-k">%s VIP of the Week</p>%s<div class="jv-votw-b"><b>Castaways Steak &amp; Seafood</b><i>Port Jefferson &middot; Steak &amp; Seafood</i>'
            '<p>Prime steaks, a raw bar and live music in the heart of the village.</p><div><span>%s Call</span><span>View profile</span></div></div></div>'
            % (ic("crown"), img("c-front-720.webp", "Castaways storefront featured as VIP of the Week", 720, 239), ic("phone")))
    art = ('<div class="jv-art">%s<div class="jv-art-b"><p class="jv-art-k">Three Village Local Blog &middot; Local Favorites</p><b>Inside Castaways: Prime Steaks, a Raw Bar and Live Music on Main Street</b>'
           '<i>By the Three Village Local team &middot; 5 min read</i><p>We sat down with the Castaways crew to talk about the grill, the raw bar and why Main Street feels like summer all year...</p></div></div>'
           % img("c-spread-640.webp", "Example article photo: Castaways table spread", 640, 360))
    items = [("Banner ad across the whole website", "Your banner rotates on pages all over Three Village Local, on phones and computers.", banner),
             ("VIP of the Week", "A full week as the homepage spotlight, in rotation with the other VIPs.", votw),
             ("A custom article every quarter", "Written, designed and published by us, then shared to social and email.", art)]
    g = "".join('<div class="jv-x"><div class="jv-x-v">%s</div><div class="jv-x-t"><b>%s</b><p>%s</p></div></div>' % (v, t, d) for t, d, v in items)
    return m_sec("vip", "VIP extras", "Top of mind, all over town.", "Examples built with Castaways photos to show the format.", '<div class="jv-xs">%s</div>' % g)


def m_partner():
    chat = ('<div class="jv-chat" aria-label="Example AI chatbot conversation"><div class="jv-chat-h"><span class="jv-chat-av">%s</span><div><b>Castaways Assistant</b><i><u></u>Online 24/7</i></div></div>'
            '<div class="jv-chat-b" data-chat aria-live="off">'
            '<p class="me">Do you have a table for 6 on Saturday around 7?</p>'
            '<p class="bot">Saturday evening still has room. Want me to have the team hold a table for 6 at 7 PM? What name and cell should they use?</p>'
            '<p class="me">Dana, 631-555-0142</p>'
            '<p class="bot">Thanks, Dana! The team will text you to confirm. The raw bar specials run all weekend, too.</p>'
            '<p class="lead">%s<span><b>New lead texted to you</b>Dana &middot; party of 6 &middot; Sat 7 PM</span></p></div>'
            '<button type="button" class="jv-chat-re">%s Replay</button></div>' % (ic("bot"), ic("phone"), ic("refresh")))
    cpts = [("clock", "Answers in seconds, day and night", "Hours, menu, parking, parties, prices. Trained on your business."),
            ("message", "Every lead texted to you", "Name, number and what they want, sent to your phone right away."),
            ("globe", "Works on the website you have", "Wix, Squarespace, WordPress and more. We set it up for you.")]
    cb = "".join('<li><span class="jv-li-ic">%s</span><div><b>%s</b><span>%s</span></div></li>' % (ic(i), t, d) for i, t, d in cpts)
    s1 = m_sec("chat", "AI chatbot", "A front desk that never sleeps.", "Scripted example of the AI chatbot on a member website.",
               '<div class="jvm-split jvm-split-chat"><div>%s</div><ul class="jvm-pts">%s</ul></div>' % (chat, cb))
    dpts = [("dash", "Your whole business on one screen", "Bookings, sales, reviews, social and leads, side by side."),
            ("sparkle", "Ask your business anything", "Built-in AI answers questions about your own numbers."),
            ("phone", "On your phone and computer", "Set up, connected and kept running by our team.")]
    db = "".join('<li><span class="jv-li-ic">%s</span><div><b>%s</b><span>%s</span></div></li>' % (ic(i), t, d) for i, t, d in dpts)
    s2 = m_sec("company", "Company Digital Dashboard", "Run the business from one place.",
               "Example: a sample restaurant dashboard (fictional business, sample data).",
               '<div class="jv-cd">%s%s</div><ul class="jvm-pts jvm-pts-row">%s</ul>' % (
                   browser(img("dash-desk.webp", "Example Company Digital Dashboard for a restaurant on a computer", 1200, 750), "dashboard.yourbusiness.com"),
                   phone(img("dash-phone.webp", "The same dashboard on a phone", 480, 1039), "jv-phone-sm jv-cd-ph"), db))
    return s1 + s2


PERKS = {
    "featured": [("star", "Premium custom profile design, with video support"), ("dash", "Member Dashboard: everything we did for you"),
                 ("bolt", "Featured badge and priority placement above free listings"), ("megaphone", "Category spotlights and newsletter mentions"),
                 ("calendar", "Post events and specials on our website and mobile app"), ("insta", "Instagram specials and events shared into our feeds"),
                 ("camera", "Logo plus up to 5 photos and an enhanced description"), ("link", "A link to your website from a trusted local site"),
                 ("sparkle", "Free AI visibility check every quarter"), ("qr", "Review-request kit: QR counter card and text template"),
                 ("drone", "Member discounts on drone photos and video and video production"), ("percent", "10% off all of our services")],
    "vip": [("check", "Everything in Featured"), ("banner", "Banner ad rotating across the whole website"),
            ("search", "Top-spot card at the top of search with one-tap call"), ("crown", "Premium VIP profile, VIP badge and top category placement"),
            ("megaphone", "VIP spotlights on social, our website and mobile app"), ("mail", "Spotlights in our email campaigns"),
            ("bell", "One mobile app push notification a month"), ("video", "Video promotion plus drone photos and video included"),
            ("article", "A custom article about your business every quarter"), ("dash", "The full Member Dashboard"),
            ("home", "VIP of the Week homepage spotlight rotation"), ("bot", "Priority in our AI answer pages"),
            ("refresh", "Yearly AI search tune-up"), ("percent", "20% off all of our services")],
    "partner": [("check", "Everything in VIP"), ("bot", "AI chatbot on your website: answers 24/7, texts you leads"),
                ("dash", "Company Digital Dashboard for your business"), ("edit", "Monthly social content made for your own accounts"),
                ("calendar", "Quarterly strategy call"), ("bolt", "Priority on everything we do"), ("percent", "20% off all of our services")],
}


def m_perks(k):
    li = "".join('<li><span class="jv-li-ic">%s</span><span>%s</span></li>' % (ic(i), t) for i, t in PERKS[k])
    return m_sec("perks", "Everything included", "The full list.", "", '<ul class="jvm-perks">%s</ul>' % li)


def m_cta(k):
    p = dict((x["k"], x) for x in PLANS)[k]
    btn = {"featured": "jv-btn-blue", "vip": "jv-btn-gold", "partner": "jv-btn-navy"}[k]
    return ('<section class="jvm-sec jvm-end" id="jvm-go" data-sec="go"><p class="jvm-eye">Ready when you are</p><h3>%s, $%d a month.</h3>'
            '<p>Month to month, no long-term contract. Upgrade, downgrade or cancel anytime. Current members keep their rate.</p>'
            '<a class="jv-btn %s" href="%s" data-jv-plan="%s">%s</a></section>' % (p["name"], PRICE[k], btn, CHECKOUT[k], k, p["btn"]))


def modal_tpl(k):
    if k == "featured":
        secs = [("profile", "Profile"), ("dash", "Dashboard"), ("seen", "Where you're seen"), ("perks", "Everything")]
        body = m_profile(k) + m_dash(k) + m_seen(k) + m_perks(k)
    elif k == "vip":
        secs = [("profile", "VIP profile"), ("dash", "Dashboard"), ("vip", "VIP extras"), ("seen", "Where you're seen"), ("perks", "Everything")]
        body = m_profile(k) + m_dash(k) + m_vip() + m_seen(k) + m_perks(k)
    else:
        secs = [("chat", "AI chatbot"), ("company", "Company Dashboard"), ("vip", "VIP extras"), ("dash", "Member Dashboard"), ("perks", "Everything")]
        body = m_partner() + m_vip() + m_dash(k) + m_perks(k)
    p = dict((x["k"], x) for x in PLANS)[k]
    tabs = "".join('<button type="button" class="jvm-tab" data-go="%s">%s</button>' % s for s in secs)
    btn = {"featured": "jv-btn-blue", "vip": "jv-btn-gold", "partner": "jv-btn-navy"}[k]
    return ('<template id="jvt-%s" data-title="%s" data-price="$%d/month" data-tag="%s">'
            '<nav class="jvm-tabs" aria-label="Sections">%s</nav><div class="jvm-body">%s%s</div>'
            '<div class="jvm-bar"><div><b>%s</b><span>$%d/month &middot; month to month</span></div><a class="jv-btn %s" href="%s" data-jv-plan="%s">%s</a></div>'
            '</template>' % (k, p["name"], PRICE[k], p["tag"], tabs, body, m_cta(k), p["name"], PRICE[k], btn, CHECKOUT[k], k, p["btn"]))


# ---------- page sections ----------
def hero():
    return '''<section class="jv-hero">
<div class="jv-hin">
<p class="jv-kick"><span class="jv-dot"></span>Three Village Local Memberships</p>
<h1 class="jv-h1">Get your business <span>seen</span> by the neighbors.</h1>
<p class="jv-dek">The local promotion platform for Setauket, Stony Brook and Port Jefferson. Every plan puts you on our website and mobile app. Paid plans put you in front of the whole town, and now show you everything we did for you.</p>
<div class="jv-hctas"><a class="jv-btn jv-btn-blue" href="#jv-plans">See the plans</a><button type="button" class="jv-btn jv-btn-ghost" data-jv-open="featured" data-jv-go="dash" aria-haspopup="dialog">%s See the Member Dashboard</button></div>
<ul class="jv-stats">
<li><span class="jv-st-ic">%s</span><div><b>45,000+</b><i>website page visits a month</i></div></li>
<li><span class="jv-st-ic">%s</span><div><b>100,000+</b><i>Facebook &amp; Instagram views a month</i></div></li>
<li><span class="jv-st-ic">%s</span><div><b>100%%</b><i>local audience</i></div></li>
</ul>
</div>
<div class="jv-hvis" aria-hidden="true">
%s
<div class="jv-hcard jv-hc1"><span>%s</span><div><b>On our homepage 6 times</b><i>this month</i></div></div>
<div class="jv-hcard jv-hc2"><span>%s</span><div><b>Your special went out</b><i>to 100,000+ social views</i></div></div>
<div class="jv-hcard jv-hc3"><span>%s</span><div><b>AI visibility check</b><i>3 fixes done</i></div></div>
</div>
</section>''' % (ic("dash"), ic("globe"), ic("share"), ic("pin"),
                 phone(img("prof-phone-1.webp", "", 540, 958, lazy=False, extra=' fetchpriority="high"'), "jv-hphone"),
                 ic("home"), ic("insta"), ic("sparkle"))


def plans():
    return ('<section class="jv-sec jv-plans" id="jv-plans"><div class="jv-head"><p class="jv-eye">Plans</p><h2>Pick how loud you want to be.</h2>'
            '<p>Start free, or let us put you in front of the whole town. Every paid plan comes with a premium profile and your own Member Dashboard.</p></div>'
            '<div class="jv-cards">%s</div>'
            '<div class="jv-assure"><p class="jv-keep">%s<span><b>Already a member?</b> Current members keep their rate.</span></p>'
            '<ul><li>%s<span>Month to month, no long-term contract</span></li><li>%s<span>Upgrade, downgrade or cancel anytime</span></li><li>%s<span>Help setting up your listing</span></li></ul></div>'
            '<p class="jv-proceeds">All proceeds from paid memberships go directly toward promoting our local businesses through articles, social posts, mobile app visibility and other local marketing.</p>'
            '</section>' % ("".join(plan_card(p) for p in PLANS), ic("shield"), ic("check"), ic("check"), ic("check")))


def news():
    tiles = [
        ("dash", "Member Dashboard", "Sign in and see every homepage feature, post, email and fix we did for you.", "featured", "dash", "jv-n-big",
         '<div class="jv-mini"><p class="jv-mini-h">Welcome back, Castaways</p><div class="jv-mini-k"><span><b data-n="6">6</b><i>homepage features</i></span><span><b>100K+</b><i>social views</i></span><span><b data-n="3">3</b><i>AI fixes</i></span></div>'
         '<ul class="jv-mini-l"><li>%s<span>Your special went out on Instagram</span></li><li>%s<span>In this week&#39;s email</span></li><li>%s<span>Your reel posted</span></li></ul></div>'
         % (img("c-margarita-160.webp", "", 160, 160), img("c-oysters-160.webp", "", 160, 160), img("c-grill-160.webp", "", 160, 160))),
        ("video", "Premium profile, with video", "A custom design in your colors with video, like a mini website.", "featured", "profile", "jv-n-prof",
         '<div class="jv-n-ph">%s</div>' % img("c-front-720.webp", "Castaways premium profile banner", 720, 239)),
        ("insta", "Instagram auto-share", "Post a special or event on your Instagram and it shows up in our feeds.", "", "", "", ""),
        ("sparkle", "Quarterly AI visibility check", "We check how ChatGPT, Gemini and Google AI describe you, and fix what is off.", "", "", "", ""),
        ("qr", "Review-request kit", "A QR counter card and a text template that turn happy customers into Google reviews.", "", "", "", ""),
        ("percent", "Member pricing on services", "10% off for Featured, 20% off for VIP and Partner: videos, websites, AI and more.", "", "", "", ""),
        ("article", "VIP: a custom article every quarter", "We write, design and publish a story about your business, then share it.", "vip", "vip", "jv-n-vip", ""),
        ("crown", "VIP of the Week", "A week as our homepage spotlight, plus priority in our AI answer pages.", "vip", "vip", "jv-n-vip", ""),
    ]
    out = ""
    for i, t, d, plan, go, cls, vis in tiles:
        b = '<span class="jv-n-ic">%s</span><b>%s</b><p>%s</p>%s' % (ic(i), t, d, vis)
        if plan:
            out += '<button type="button" class="jv-n %s" data-jv-open="%s" data-jv-go="%s" aria-haspopup="dialog">%s<em>See the example %s</em></button>' % (cls, plan, go, b, ic("arrow"))
        else:
            out += '<div class="jv-n">%s</div>' % b
    return ('<section class="jv-sec jv-news" id="jv-new"><div class="jv-head"><p class="jv-eye">New for members</p><h2>More than a listing. A team working for you.</h2>'
            '<p>Paid memberships now come with tools and extras that used to cost extra.</p></div><div class="jv-ngrid">%s</div></section>' % out)


def compare_sec():
    return ('<section class="jv-sec jv-cmp" id="jv-compare"><div class="jv-head"><p class="jv-eye">Compare</p><h2>Every plan, side by side.</h2></div>%s</section>' % compare())


def services():
    c = [("globe", "Websites built for AI search", "Fast websites written so Google and AI tools recommend you.", "/websites"),
         ("bot", "AI chatbot for your website", "Answers customers 24/7 and texts you every lead.", "/ai-assistant"),
         ("sparkle", "AI search optimization", "Get read, trusted and recommended by AI search tools.", "/services#tvp-ai"),
         ("video", "Promo video and social", "Reels and promo videos shared to 100,000+ local views.", "/services#tvp-video")]
    g = "".join('<a class="jv-svc" href="%s"><span class="jv-n-ic">%s</span><div><b>%s</b><p>%s</p></div>%s</a>' % (h, ic(i), t, d, ic("arrow", "jv-svc-ar")) for i, t, d, h in c)
    return ('<section class="jv-sec jv-svcs"><div class="jv-head"><p class="jv-eye">Beyond memberships</p><h2>We do a lot more than listings.</h2>'
            '<p>The same local team builds the tools that help a business get found and win the customer. Members save 10%% to 20%%.</p></div>'
            '<div class="jv-svcg">%s</div><p class="jv-center"><a class="jv-btn jv-btn-line" href="/services">See all our services</a></p></section>' % g)


FAQ = [
    ("Is there a long-term commitment?", "No. Every plan is month to month with no long-term contract. Cancel anytime, but we think you will love the results."),
    ("I am already a member. Does my price change?", "No. Current members keep their rate. You get the new member perks that come with your plan as we roll them out."),
    ("What is the Member Dashboard?", "A sign-in page for Featured, VIP and Partner members that shows what Three Village Local did for you: homepage features, social posts, email mentions, reels, AI visibility fixes and what is scheduled next."),
    ("What comes with the premium profile?", "A custom-designed profile in your colors with your best photos, video support, one-tap call, booking and directions buttons, and clean facts that Google and AI tools can read."),
    ("How do the service discounts work?", "Featured members get 10% off all of our services. VIP and Partner members get 20% off: promo videos, websites, AI search work, drone and more."),
    ("What is the quarterly article for VIPs?", "Every quarter we write, design and publish a custom article about your business on Three Village Local, then share it on social media and in our email."),
    ("How do I start the Partner plan?", "Partner is set up with you personally, so it starts with a short call. Tap Talk to us about Partner and tell us about your business."),
    ("Can I upgrade or downgrade my plan?", "Yes, anytime. Test more exposure or scale back as your business needs change."),
    ("Who controls my business listing?", "You do. You get your own login to update your info, photos and categories (based on your plan) whenever you like."),
    ("Can I get help setting up my listing?", "Yes. We will guide you through setup and help with photos and content so your business looks its best."),
]


def faq():
    qs = "".join('<details class="jv-q"%s><summary><span class="jv-q-t">%s</span><span class="jv-q-ic" aria-hidden="true"></span></summary><p>%s</p></details>' % (" open" if n == 0 else "", q, a) for n, (q, a) in enumerate(FAQ))
    return '<section class="jv-sec jv-faq" id="jv-faq"><div class="jv-head"><p class="jv-eye">Questions</p><h2>Good questions, straight answers.</h2></div><div class="jv-qs">%s</div></section>' % qs


def final():
    return ('<section class="jv-final"><div><p class="jv-eye">Your neighbors are looking</p><h2>Make sure they find you first.</h2>'
            '<p>Month to month. Current members keep their rate.</p></div><div class="jv-final-b"><a class="jv-btn jv-btn-gold" href="#jv-plans">Choose your plan</a>'
            '<a class="jv-btn jv-btn-wline" href="/services#tvs-book">Talk to us first</a></div></section>')


def ribbon():
    return '<p class="jv-ribbon">Preview only &middot; proposed prices for review &middot; the live /join page is unchanged</p>'


def nowrap_hyphens(h):
    out, skip = [], False
    for part in re.split(r"(<[^>]+>)", h):
        if part.startswith("<"):
            tag = part[1:].split()[0].lower().rstrip(">") if len(part) > 2 else ""
            if tag in ("script", "style", "svg", "template"):
                skip = tag != "template" and True
            elif tag in ("/script", "/style", "/svg"):
                skip = False
            out.append(part)
        elif skip:
            out.append(part)
        else:
            out.append(re.sub(r"(?<![\w&#;/.-])([A-Za-z0-9]+(?:-[A-Za-z0-9]+)+)(?![\w/.-])", r'<span class="jv-nw">\1</span>', part))
    return "".join(out)


def build():
    tpls = "".join(modal_tpl(k) for k in ("featured", "vip", "partner"))
    claim = open(os.path.join(HERE, "claim.js"), encoding="utf-8").read()
    body = ribbon() + hero() + plans() + news() + compare_sec() + services() + faq() + final() + tpls
    html = '<div class="jv" id="jv">' + sprite() + body + '</div>'
    html = nowrap_hyphens(html)
    css = open(os.path.join(HERE, "page.css"), encoding="utf-8").read()
    js = "<script>" + open(os.path.join(HERE, "page.js"), encoding="utf-8").read() + "</script><script>" + claim + "</script>"
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    head = '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>'
    vis = re.sub(r"<(script|style|svg)[^>]*>.*?</\1>", " ", html, flags=re.S)
    vis = re.sub(r"<[^>]+>", " ", vis)
    for nm, s in [("html", html), ("css", css), ("js", js), ("head", head)]:
        assert "\\" not in s, nm + " has a backslash (BD strips them)"
        assert "—" not in s and "&mdash;" not in s and "–" not in s, nm + " has an em/en dash"
    bad = [m.group(0) for m in re.finditer(r"(?i)(?<!mobile )\bapps?\b", vis)]
    assert not bad, "bare 'app' in copy: %r" % bad[:5]
    return html, css, js, head


def main():
    html, css, js, head = build()
    if LOCAL:
        os.makedirs(os.path.join(HERE, "_local"), exist_ok=True)
        tpl = open(os.path.join(HERE, "_local", "shell.html"), encoding="utf-8").read()
        html = html.replace(SH, "http://127.0.0.1:8795/")
        out = tpl.replace("<!--JV-HEAD-->", head).replace("<!--JV-WIDGET-->", "<style>" + css + "</style>" + html + js)
        open(os.path.join(HERE, "_local", "index.html"), "w", encoding="utf-8").write(out)
        print("local", len(html), len(css), len(js))
        return
    if DRY:
        print("html", len(html), "css", len(css), "js", len(js), "head", len(head))
        return
    import urllib.parse, urllib.request
    sys.path.insert(0, os.path.join(HERE, "..", "share-img"))
    from bdkey import key
    H = {"X-Api-Key": key(), "User-Agent": "Mozilla/5.0 3VL", "Content-Type": "application/x-www-form-urlencoded"}
    API = "https://www.threevillagelocal.com/api/v2/"

    def call(method, path, data=None):
        body = urllib.parse.urlencode(data).encode() if data is not None else None
        return json.loads(urllib.request.urlopen(urllib.request.Request(API + path, data=body, headers=H, method=method), timeout=60).read())

    assert NAME.endswith("Preview") and SLUG.startswith("preview-")
    w = {"widget_data": html, "widget_style": css, "widget_javascript": js}
    found = call("GET", "data_widgets/get?property=widget_name&property_value=" + urllib.parse.quote(NAME)).get("message")
    found = [x for x in found if x.get("widget_name") == NAME] if isinstance(found, list) else []
    if found:
        assert str(found[0]["widget_id"]) != "15"
        print("widget", found[0]["widget_id"], call("PUT", "data_widgets/update", dict(w, widget_id=found[0]["widget_id"])).get("status"))
    else:
        r = call("POST", "data_widgets/create", dict(w, widget_name=NAME, widget_viewport="front"))
        print("widget create", r.get("status"), (r.get("message") or {}).get("widget_id"))
    page = {"content": "[widget=%s]" % NAME, "content_css": " ", "enable_hero_section": "0", "title": TITLE, "meta_desc": DESC,
            "facebook_title": FB_TITLE, "facebook_desc": DESC, "facebook_image": FB_IMAGE, "show_form": "1", "content_head": head}
    ex = call("GET", "list_seo/get?property=filename&property_value=" + SLUG).get("message")
    ex = [x for x in ex if x.get("filename") == SLUG] if isinstance(ex, list) else []
    if ex:
        print("page update", ex[0]["seo_id"], call("PUT", "list_seo/update", dict(page, seo_id=ex[0]["seo_id"])).get("status"))
    else:
        r = call("POST", "list_seo/create", dict(page, seo_type="content", filename=SLUG))
        print("page create", r.get("status"), (r.get("message") or {}).get("seo_id") if isinstance(r.get("message"), dict) else r.get("message"))
    try:
        call("POST", "website_settings/refreshCache", {})
    except Exception as e:
        print("cache:", e)
    print("https://www.threevillagelocal.com/" + SLUG)


if __name__ == "__main__":
    main()
