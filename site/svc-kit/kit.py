"""Shared kit for the one-page-per-service previews (promo video, social media, AI search, email & articles, new business launch).
Built on the /services (platform-page) design system: same page.css/page.js chain, the same free-plan form (form 343 via the
BOOK section), the same pinned section nav. Each service folder has its own build.py that calls kit.page(...).
No prices anywhere (owner 11/12: not yet). Nothing here is ever published --live without the owner's OK."""
import html as _html, importlib.util, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("platbuild", os.path.join(HERE, "..", "platform-page", "build.py"))
P = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(P)
D = P.D
LIVE = D.LIVE
SH = P.SH                     # https://threevillagelocal-cloud.github.io/3vl-share/site/
SV = SH + "services/"
WB = SH + "websites/"


def url(slug):
    return ("/" if LIVE else "/preview-") + slug


# ---------- icons (inline SVG, stroke style) ----------
_I = {
    "video": '<rect x="2" y="6" width="14" height="12" rx="2"/><path d="m16 10 6-3v10l-6-3"/>',
    "camera": '<path d="M4 8h3l2-3h6l2 3h3a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1z"/><circle cx="12" cy="13.5" r="3.5"/>',
    "scissors": '<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M8.1 8.1 20 20M8.1 15.9 20 4"/>',
    "cc": '<rect x="2" y="5" width="20" height="14" rx="3"/><path d="M10 10.2a2.2 2.2 0 1 0 0 3.6M17 10.2a2.2 2.2 0 1 0 0 3.6"/>',
    "crop": '<path d="M6 2v14a2 2 0 0 0 2 2h14"/><path d="M18 22V8a2 2 0 0 0-2-2H2"/>',
    "share": '<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="m8.6 13.5 6.8 4M15.4 6.5l-6.8 4"/>',
    "phone": '<rect x="6" y="2" width="12" height="20" rx="3"/><path d="M11 18h2"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15 15 0 0 1 0 20M12 2a15 15 0 0 0 0 20"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
    "article": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h6"/>',
    "star": '<path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/>',
    "tag": '<path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L2 12V2h10l8.6 8.6a2 2 0 0 1 0 2.8z"/><circle cx="7" cy="7" r="1.5"/>',
    "users": '<circle cx="9" cy="8" r="4"/><path d="M2 21v-1a7 7 0 0 1 14 0v1M16 3.1a4 4 0 0 1 0 7.8M22 21v-1a7 7 0 0 0-4-6.3"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "chart": '<path d="M3 3v18h18"/><path d="m7 15 4-4 3 3 5-6"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m21 21-5-5"/>',
    "pin": '<path d="M12 22s7-6.5 7-12a7 7 0 0 0-14 0c0 5.5 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/>',
    "code": '<path d="m16 18 6-6-6-6M8 6l-6 6 6 6"/>',
    "sparkle": '<path d="M12 3l1.9 5.6 5.6 1.9-5.6 1.9L12 18l-1.9-5.6-5.6-1.9 5.6-1.9z"/><path d="M19 3v4M17 5h4"/>',
    "rocket": '<path d="M4.5 16.5c-1.5 1.3-2 5-2 5s3.7-.5 5-2c.7-.8.7-2.1-.1-2.9a2.2 2.2 0 0 0-2.9-.1z"/><path d="M12 15l-3-3a22 22 0 0 1 2-3.9A12.9 12.9 0 0 1 22 2c0 2.7-.8 7.5-6 11a22.4 22.4 0 0 1-4 2z"/><path d="M9 12H4s.5-3 2-4c1.6-1.1 5 0 5 0M12 15v5s3-.5 4-2c1.1-1.6 0-5 0-5"/>',
    "megaphone": '<path d="m3 11 18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "store": '<path d="M3 9l1.5-5h15L21 9M3 9v11h18V9M3 9h18M9 20v-6h6v6"/>',
    "hammer": '<path d="m15 12-8.5 8.5a2.1 2.1 0 0 1-3-3L12 9"/><path d="M17.6 15 22 10.6 13.4 2 9 6.4z"/>',
    "heart": '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21.2l8.8-8.8a5.5 5.5 0 0 0 0-7.8z"/>',
    "briefcase": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
    "dumbbell": '<path d="M6.5 6.5v11M17.5 6.5v11M3 9v6M21 9v6M6.5 12h11"/>',
    "utensils": '<path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2M7 2v20M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3zm0 0v7"/>',
    "home": '<path d="m3 10 9-7 9 7v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>',
    "gift": '<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7M7.5 8a2.5 2.5 0 0 1 0-5C11 3 12 8 12 8s1-5 4.5-5a2.5 2.5 0 0 1 0 5"/>',
    "bolt": '<path d="M13 2 3 14h9l-1 8 10-12h-9z"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    "message": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    "layers": '<path d="m12 2 10 5-10 5L2 7z"/><path d="m2 17 10 5 10-5M2 12l10 5 10-5"/>',
    "list": '<path d="M10 6h11M10 12h11M10 18h11"/><path d="m3 6 1.5 1.5L7 5M3 12l1.5 1.5L7 11M3 18l1.5 1.5L7 17"/>',
    "bot": '<rect x="4" y="8" width="16" height="12" rx="3"/><path d="M12 4v4M9 13h.01M15 13h.01M9 17h6"/>',
    "link": '<path d="M10 13a5 5 0 0 0 7.5.5l3-3a5 5 0 0 0-7-7l-1.7 1.7"/><path d="M14 11a5 5 0 0 0-7.5-.5l-3 3a5 5 0 0 0 7 7l1.7-1.7"/>',
    "eye": '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    "music": '<path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>',
    "edit": '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>',
    "play": '<path d="M7 4v16l13-8z"/>',
    "grid": '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
}


def ic(name, cls=""):
    return '<svg class="tvx-svg%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % (
        (" " + cls) if cls else "", _I[name])


# brand logos reused from the live pages
AILOGO = {}
for _m in re.finditer(r'<span class="tvw-logo">(<svg.*?</svg>)([^<]+)</span>', P.A.W.STRIP_SEC, re.S):
    AILOGO[_m.group(2).strip()] = _m.group(1)
AIROW = P.AIROW
_soc = re.findall(r'<span>(<svg viewBox="0 0 24 24">.*?</svg>)(Facebook|Instagram|TikTok)</span>', P.V_SOCIAL, re.S)
SOCLOGO = {n: s for s, n in _soc}
assert len(AILOGO) >= 6 and len(SOCLOGO) == 3, (list(AILOGO), list(SOCLOGO))

# ---------- the service catalog (for "related" cards) ----------
SERVICES = {
    "promo-video": ("video", "Promo video", "Short reels that show off your business, filmed and edited for you.", url("promo-video")),
    "social-media": ("megaphone", "Social media", "Promotion to 100,000+ local views a month, plus content for your own accounts.", url("social-media")),
    "ai-search": ("sparkle", "AI search optimization", "Get recommended by ChatGPT, Gemini, Google AI and more.", url("ai-search")),
    "email-articles": ("mail", "Email and articles", "Weekly email spotlights and custom articles neighbors read.", url("email-articles")),
    "new-business-launch": ("rocket", "New business launch", "Open your doors with the whole town watching.", url("new-business-launch")),
    "websites": ("globe", "AI-ready websites", "Designed, built and hosted to be found on Google and AI.", "/websites"),
    "ai-assistant": ("bot", "AI front desk", "An AI assistant that answers customers 24/7 and texts you every lead.", "/ai-assistant"),
    "join": ("star", "Featured and VIP memberships", "Top spots in search, homepage features and banners.", "/join"),
}


# ---------- building blocks ----------
def hero(kick, l1, l2, sub, visual, cta2=("See how it works", "#tvp-how"), stats=None, cls=""):
    stats = stats or [("45,000+", "website page visits a month"), ("100,000+", "Facebook &amp; Instagram views a month"), ("100%", "local audience")]
    st = "".join("<li><b>%s</b>%s</li>" % s for s in stats)
    return '''<section class="tvx-hero %s" id="tvx-hero">
  <div class="tvx-hin">
    <p class="tvx-crumbs"><a href="/services">Our services</a><span>/</span>%s</p>
    <h1>%s<br><span>%s</span></h1>
    <p class="tvx-sub">%s</p>
    <div class="tvs-ctas tvx-ctas"><a class="tvs-btn tvs-blue" href="#tvs-book">Get my free plan</a><a class="tvs-btn tvs-ghost" href="%s">%s</a></div>
    <ul class="tvx-trust">%s</ul>
  </div>
  <div class="tvx-hvis" data-run>%s</div>
</section>''' % (cls, kick, l1, l2, sub, cta2[1], cta2[0], st, visual)


def snav(items):
    a = "".join('<a href="#tvp-%s">%s</a>' % (k, t) for k, t in items)
    return '<nav class="tvp-snav-bar" id="tvp-snav" aria-label="On this page"><div class="tvp-snav-in">%s<a class="tvp-snav-cta" href="#tvs-book">Get my free plan</a></div></nav>' % a


def sec(id_, eyebrow, h2, p, body, cls=""):
    head = '<div class="tvs-head tvs-up"><p class="tvs-eyebrow">%s</p><h2>%s</h2>%s</div>' % (eyebrow, h2, ("<p>%s</p>" % p) if p else "")
    return '<section class="tvs-sec tvx-sec %s" id="tvp-%s">\n  %s\n  %s\n</section>' % (cls, id_, head, body)


def cards(items, cols=3, cls=""):
    """items: (icon, title, text[, accent])"""
    acc = ["#1d5fbf", "#16a37a", "#0f8fb8", "#4a5fd6", "#e0a82e", "#d2557a"]
    out = []
    for n, it in enumerate(items):
        a = it[3] if len(it) > 3 else acc[n % len(acc)]
        out.append('<div class="tvx-card tvs-up" style="--ac:%s"><span class="tvx-ic">%s</span><h3>%s</h3><p>%s</p></div>' % (a, ic(it[0]), it[1], it[2]))
    return '<div class="tvx-cards tvx-c%d %s">%s</div>' % (cols, cls, "".join(out))


def stats_band(title="A built-in local audience, every month.", eyebrow="Reach", items=None, dark=True):
    items = items or [(45000, "+", "website page visits a month", "globe"), (100000, "+", "Facebook &amp; Instagram views a month", "share"), (100, "%", "local audience: Three Village and Port Jefferson", "pin")]
    cells = "".join('<div class="tvx-stat"><span class="tvx-ic">%s</span><b><span data-n="%d">%s</span>%s</b><i>%s</i></div>' % (ic(i), n, "{:,}".format(n), suf, lab) for n, suf, lab, i in items)
    return '<div class="tvx-statsband tvs-up%s"><p class="tvs-eyebrow">%s</p><h3>%s</h3><div class="tvx-stats">%s</div></div>' % (" tvx-dk" if dark else "", eyebrow, title, cells)


def steps(items):
    li = "".join('<li><b>%d</b><h3>%s</h3><p>%s</p></li>' % (n + 1, t, p) for n, (t, p) in enumerate(items))
    return '<ol class="tvx-steps tvs-up" style="--n:%d">%s</ol>' % (len(items), li)


_FAQ_LD = []


def faq(items, title="Good questions, straight answers."):
    qs = "".join('<details%s><summary>%s</summary><p>%s</p></details>' % (" open" if n == 0 else "", q, a) for n, (q, a) in enumerate(items))
    for q, a in items:
        _FAQ_LD.append({"@type": "Question", "name": _plain(q), "acceptedAnswer": {"@type": "Answer", "text": _plain(a)}})
    return '''<section class="tvs-sec tvs-faq tvx-faq" id="tvp-faq">
  <div class="tvs-head tvs-up"><p class="tvs-eyebrow">Questions</p><h2>%s</h2></div>
  <div class="tvs-qs tvs-up">%s</div>
</section>''' % (title, qs)


def _plain(s):
    s = _html.unescape(re.sub(r"<[^>]+>", "", s))
    return s.replace('"', "'").replace("’", "'")


def related(current, keys=None, h2="Put more of the town to work for you."):
    keys = keys or [k for k in SERVICES if k != current][:6]
    c = ""
    for k in keys:
        i, t, d, h = SERVICES[k]
        c += '<a class="tvx-rel-c tvs-up" href="%s"><span class="tvx-ic">%s</span><div><b>%s</b><i>%s</i></div><em>%s</em></a>' % (h, ic(i), t, d, ic("arrow"))
    return '''<section class="tvs-sec tvx-rel" id="tvp-more">
  <div class="tvs-head tvs-up"><p class="tvs-eyebrow">Works even better together</p><h2>%s</h2><p>Every service plugs into the same local audience. Pick one, or let us build a plan around all of them.</p></div>
  <div class="tvx-rel-g">%s</div>
  <p class="tvx-rel-all tvs-up"><a href="/services">See all of our services %s</a></p>
</section>''' % (h2, c, ic("arrow"))


def cta(kick, h2, sub, alt=("See all services", "/services")):
    return '''<section class="tvw-cta3 tvs-up"><div class="tvw-cta3-in"><p class="tvw-cta3-k">%s</p><h2>%s</h2>
<p class="tvw-cta3-s">%s</p>
<div class="tvw-cta-btns"><a class="tvs-btn tvw-btn-w" href="#tvs-book">Get my free plan</a><a class="tvs-btn tvw-btn-o" href="%s">%s</a></div></div></section>''' % (kick, h2, sub, alt[1], alt[0])


def book(eyebrow):
    b = P.BOOK
    for a, z in [("<li>Clear pricing, no pressure, no contract</li>", "<li>No pressure and no contract</li>"),
                 ('<p class="tvs-eyebrow">Your free plan</p>', '<p class="tvs-eyebrow">%s</p>' % eyebrow)]:
        assert a in b, a
        b = b.replace(a, z)
    return b


def _nowrap_hyphens(h):
    """Keep hyphenated words (easy-to-read, AI-ready, launch-ready) on one line: never split words at 412/360/320."""
    out, skip = [], False
    for part in re.split(r"(<[^>]+>)", h):
        if part.startswith("<"):
            tag = part[1:].split()[0].lower().rstrip(">") if len(part) > 2 else ""
            if tag in ("script", "style", "svg"):
                skip = True
            elif tag in ("/script", "/style", "/svg"):
                skip = False
            out.append(part)
        elif skip:
            out.append(part)
        else:
            out.append(re.sub(r"(?<![\w&#;-])([A-Za-z0-9]+(?:-[A-Za-z0-9]+)+)(?![\w-])", r'<span class="tvx-nw">\1</span>', part))
    return "".join(out)


# ---------- shared CSS / JS ----------
KIT_CSS = open(os.path.join(HERE, "kit.css"), encoding="utf-8").read()
KIT_JS = open(os.path.join(HERE, "kit.js"), encoding="utf-8").read()


SHARE_ALT = {
    "svc-ai-search-v1.jpg": "Three Village Local AI search optimization: Be the answer AI recommends. A ChatGPT answer lists Your Business as the top pick.",
    "svc-business-dashboards-v1.jpg": "Three Village Local Company Digital Dashboards: Your business. One dashboard. Leads, money and AI on a laptop and phone.",
    "svc-email-articles-v1.jpg": "Three Village Local email and articles: Stories the town actually reads. A weekly email with a neighbor spotlight.",
    "svc-new-business-launch-v1.jpg": "Three Village Local new business launch: Launch with the whole town watching. A storefront grand opening with a red ribbon.",
    "svc-promo-video-v1.jpg": "Three Village Local promo videos: Show them, don't just tell them. Two phones playing local business reels.",
    "svc-social-media-v1.jpg": "Three Village Local social media: Get seen by the whole town. Facebook and Instagram posts featuring local businesses.",
}


def share_meta(fname):
    """Extra share tags for content_head (BD itself only writes og:image): twitter card + size + alt.
    Points straight at GitHub Pages (no redirect) so X/LinkedIn fetch it directly."""
    img = SV + "share/" + fname
    alt = _html.escape(SHARE_ALT[fname], quote=True)
    return ('<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
            '<meta property="og:image:type" content="image/jpeg"><meta property="og:image:alt" content="%s">'
            '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="%s">'
            '<meta name="twitter:image:alt" content="%s">' % (alt, img, alt))


def page(name, slug, title, desc, fb_title, body, bundle="not_sure", css="", js="", book_eyebrow="Your free plan", fb_image=None, prices=False):
    """body: list of section html strings (hero first). Publishes widget '3VL Page <name> Preview' + /preview-<slug>.
    prices=True: the page shows approved prices (skips the no-price check)."""
    D.NAME = ("3VL Page %s" if LIVE else "3VL Page %s Preview") % name
    D.SLUG = slug if LIVE else "preview-" + slug
    D.TITLE, D.DESC, D.FB_TITLE = title, desc, fb_title
    # fb_image: "/share/svc-<slug>-v1.jpg" = BD redirect -> 3vl-share/site/services/share/ (BD mangles external og:image URLs)
    D.FB_IMAGE = fb_image or "/share/site-hero.webp"
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": _FAQ_LD}
    svc = {"@context": "https://schema.org", "@type": "Service", "name": fb_title, "serviceType": name, "description": desc,
           "provider": {"@id": "https://www.threevillagelocal.com/#organization", "name": "Three Village Local"},
           "areaServed": ["Setauket", "East Setauket", "Stony Brook", "Port Jefferson", "Old Field", "Poquott", "Long Island, NY"]}
    D.HEAD = ('<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>'
              '<script type="application/ld+json">' + json.dumps(svc, ensure_ascii=False) + '</script>') if _FAQ_LD else ""
    _f = D.FB_IMAGE.rsplit("/", 1)[-1]
    if _f in SHARE_ALT:
        D.HEAD += share_meta(_f)
    html = ('<div class="tvs tvx" id="tvs" data-svc="%s">\n\n' % slug + "\n\n".join(body) + "\n\n" + book(book_eyebrow) +
            '\n\n<a class="tvs-sticky" href="#tvs-book">Get my free plan</a>\n</div>')
    html = _nowrap_hyphens(html)
    full_css = KIT_CSS + css + ".tvx-nw{white-space:nowrap}"
    # BD's theme has #first_container *{white-space:normal!important}: re-assert every nowrap we use with an id-level selector
    sels = []
    for m in re.finditer(r"([^{}]+)\{[^{}]*white-space:nowrap", full_css):
        for sel in m.group(1).split(","):
            sel = sel.strip()
            if sel and not sel.startswith("@") and sel not in sels:
                sels.append(sel)
    full_css += ",".join("#tvs " + x if not x.startswith(".tvs ") else "#tvs" + x[4:] for x in sels) + "{white-space:nowrap!important}"
    full_js = (KIT_JS + js)
    for nm, s in [("html", html), ("css", full_css), ("js", full_js), ("head", D.HEAD)]:
        assert "\\" not in s, nm + " has a backslash (BD strips them)"
        assert "—" not in s and "&mdash;" not in s, nm + " has an em dash"
        assert prices or "$" not in re.sub(r"<script.*?</script>", "", s, flags=re.S) or nm in ("js",), nm + " mentions a price"

    _prd = P.rd

    def rd(f):
        if f == "page.html":
            return html
        s = _prd(f)
        if f == "page.css":
            return s + full_css
        if f == "page.js":
            assert "var pick='not_sure'" in s
            s = s.replace("var pick='not_sure'", "var pick='%s'" % bundle)
            return s + "<script>" + full_js + "</script>"
        return s

    D.rd = rd
    return html


def main():
    assert not LIVE or os.environ.get("TVX_LIVE_OK") == "1", "live publish needs the owner's OK (set TVX_LIVE_OK=1)"
    if "--dry" in __import__("sys").argv:
        for f in ("page.html", "page.css", "page.js"):
            print(f, len(D.rd(f)))
        print(D.NAME, D.SLUG, len(D.HEAD))
        return
    D.main()
