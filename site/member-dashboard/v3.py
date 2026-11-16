"""Member Dashboard v3: app-style member dashboard in the exact visual language of the Company Digital Dashboards demos
(business-dashboards-demo engine.css): dark sidebar with sections, glass topbar, "Good evening" hero with the member's photo,
KPI tiles with sparklines + count-ups, photo-rich cards, views that switch without reloads (each about one screen),
forms in drawers. Same data, tiers, locks, floor rule and offers as v2 (v2.py keeps the helpers). Real data only, no prices,
never a negative, never a 0, no em dashes."""
import datetime as dt, re
from urllib.parse import quote
import v2 as X
from v2 import e, has, ic, LOGIN, LOGIN_EDIT, UPGRADE, RANK, TIER_NAME, SITE, DIG, ICONS

VIPIMG = "https://threevillagelocal-cloud.github.io/3vl-share/live/p3/vip/"
SHOT = DIG + "/assets/img/shots/"
FB_DIGITAL = "https://www.facebook.com/profile.php?id=61596438788241"
ICONS.update({
    "bolt": '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
    "eye": '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    "trend": '<path d="m3 17 6-6 4 4 8-8"/><path d="M14 7h7v7"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
    "x": '<path d="M6 6l12 12M18 6 6 18"/>',
    "gift": '<rect x="3" y="8" width="18" height="13" rx="2"/><path d="M12 8v13M3 12h18M12 8S10.5 3 8 3a2.5 2.5 0 0 0 0 5h4zm0 0s1.5-5 4-5a2.5 2.5 0 0 1 0 5h-4z"/>',
    "layers": '<path d="m12 3 9 5-9 5-9-5z"/><path d="m3 13 9 5 9-5"/>',
})


def img(src, alt="", w=0, h=0, cls="", lazy=True):
    if not src:
        return ""
    return '<img%s src="%s" alt="%s"%s%s%s decoding="async" data-processed="true" onerror="this.style.opacity=0">' % (
        (' class="%s"' % cls) if cls else "", e(src), e(alt), (' width="%d"' % w) if w else "", (' height="%d"' % h) if h else "", ' loading="lazy"' if lazy else "")


def series(a, days=30, ch=None, home=False):
    """Cumulative daily series of real promotions (only ever rises)."""
    today = dt.date.today()
    start = today - dt.timedelta(days=days - 1)
    ev = {}
    if home or ch is None:
        for d in a.get("hp_days", []):
            ev[d] = ev.get(d, 0) + 1
    if not home:
        for it in a.get("items", []):
            if it.get("sample") or it.get("n_home") or (ch and it["ch"] not in ch):
                continue
            ev[it["date"]] = ev.get(it["date"], 0) + 1
    run = sum(v for k, v in ev.items() if k < start.isoformat())
    out = []
    for i in range(days):
        run += ev.get((start + dt.timedelta(days=i)).isoformat(), 0)
        out.append(run)
    return out


def spark(pts, cls="spark"):
    if not pts or pts[-1] == pts[0]:
        pts = [i * i for i in range(12)]   # gentle rising curve when the period was quiet (shape only, no numbers)
    W, H = 84, 30
    lo, hi = min(pts), max(max(pts), min(pts) + 1)
    n = len(pts)
    xy = ["%.1f,%.1f" % (W * i / (n - 1), H - 3 - (H - 6) * (v - lo) / (hi - lo)) for i, v in enumerate(pts)]
    return ('<svg class="%s" viewBox="0 0 %d %d" preserveAspectRatio="none" aria-hidden="true"><polyline class="draw" points="%s" fill="none" '
            'stroke="currentColor" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" vector-effect="non-scaling-stroke"/></svg>' % (cls, W, H, " ".join(xy)))


def bigchart(a, days=90, sample=False):
    if sample:
        pts = [3 + i // 6 for i in range(days)]
    else:
        pts = series(a, days)
        if pts[-1] - pts[0] < 2:
            return ""
    W, H, P = 640, 210, 6
    lo, hi = pts[0], max(pts[-1], pts[0] + 1)
    xy = [(P + (W - 2 * P) * i / (days - 1), H - P - (H - 2 * P) * (v - lo) / (hi - lo)) for i, v in enumerate(pts)]
    line = " ".join("%.1f,%.1f" % p for p in xy)
    area = "M%.1f,%d L" % (xy[0][0], H) + " L".join("%.1f,%.1f" % p for p in xy) + " L%.1f,%d Z" % (xy[-1][0], H)
    s = dt.date.today() - dt.timedelta(days=days - 1)
    grid = "".join('<line x1="0" x2="%d" y1="%d" y2="%d" class="gl"/>' % (W, y, y) for y in (40, 95, 150))
    return ('<div class="chartwrap"><svg class="bigsvg" viewBox="0 0 %d %d" preserveAspectRatio="none" role="img" aria-label="Running total of promotions, rising">'
            '<defs><linearGradient id="mg" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#2f7fe0" stop-opacity=".30"/><stop offset="1" stop-color="#2f7fe0" stop-opacity="0"/></linearGradient></defs>'
            '%s<path class="area" d="%s" fill="url(#mg)"/><polyline class="draw" points="%s" fill="none" stroke="#2f7fe0" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round" vector-effect="non-scaling-stroke"/></svg>'
            '<div class="axis"><span>%s</span><span>%s</span><span>Today</span></div></div>'
            % (W, H, grid, area, line, X.fmt(s), X.fmt(s + dt.timedelta(days=days // 2))), pts[-1] - pts[0], pts[-1])


def lock(feat, preview, compact=False):
    t, title, benefit = X.LOCK_COPY[feat]
    return ('<div class="lockwrap%s"><div class="lockprev" aria-hidden="true">%s</div><div class="lockov"><span class="lockic">%s</span><b>%s</b><i>%s</i>'
            '<a class="btn primary sm" href="%s" data-ga="dash_upgrade_click" data-product="%s">Upgrade to %s %s</a></div></div>'
            % (" compact" if compact else "", preview, ic("lock"), title, benefit, UPGRADE, feat, "Featured" if t == "f" else "VIP", ic("chev")))


def site_mock(banner_src, short):
    """Mini Three Village Local page with THEIR banner ad in the side rail (where it actually rotates)."""
    return ('<div class="sitemock" aria-hidden="true"><div class="sm-bar"><i></i><i></i><i></i><span>threevillagelocal.com</span></div>'
            '<div class="sm-body"><div class="sm-main"><b></b><p></p><p></p><p class="s"></p><div class="sm-cards"><u></u><u></u><u></u></div><p></p><p class="s"></p></div>'
            '<div class="sm-rail"><div class="sm-ad">%s<em>Your ad</em></div><p></p><p class="s"></p></div></div></div>') % img(banner_src, "Banner ad for " + short)


def spot_mock(a, others, big=False):
    photo = a.get("banner") or a.get("logo") or ""
    also = "".join('<span class="sp-a">%s<b>%s</b></span>' % (img(o["img"], "", 34, 34), e(o["name"])) for o in others[:3] if o.get("img"))
    return ('<div class="spotmock%s"><div class="sp-h">Local Business Spotlight<span>Neighbors who support Three Village Local</span></div>'
            '<div class="sp-grid"><div class="sp-main"><div class="sp-img">%s</div><div class="sp-t"><em>%s%s</em><b>%s</b><span class="sp-cta">View profile</span></div></div>'
            '<div class="sp-also"><i>Also featured</i>%s</div></div></div>') % (
        " big" if big else "", img(photo, "Your business in the homepage spotlight"), e(a.get("cat") or ""), (" &middot; " + e(a["town"])) if a.get("town") else "",
        e(a.get("short") or "Your business"), also)


def drawer_forms(tier):
    F, inp = X.form, X.inp
    out = {}
    out["event"] = F("event", "Submit an event", "We review every event and add it to our calendar and weekend picks.",
                     [inp("name", "Event name", req=True), '<div class="x-2">' + inp("date", "Date", "date", req=True) + inp("time", "Start time", "time") + '</div>',
                      inp("place", "Place", ph="Venue or address"), inp("details", "Description", "textarea"),
                      '<div class="x-2">' + inp("photo", "Photo", "file") + inp("link", "Link", "url", "Tickets or info page") + '</div>'], "Send event")
    out["special"] = F("special", "Submit a special", "Deals, new menus, seasonal offers. We feature them for neighbors.",
                       [inp("title", "Title", req=True), inp("details", "Details", "textarea"),
                        '<div class="x-2">' + inp("start", "Starts", "date") + inp("end", "Ends", "date") + '</div>',
                        '<div class="x-2">' + inp("photo", "Photo", "file") + inp("link", "Link", "url") + '</div>'], "Send special")
    out["video"] = F("video", "Request your free promo reel", "VIP perk: a fresh promo video every month, produced by 3VL Digital. Tell us what to feature.",
                     [inp("want", "What should the video show?", "textarea", req=True),
                      '<div class="x-2">' + inp("style", "Style", "select:Animated with voiceover|Filmed on location|Interview style|Not sure yet") + inp("dates", "Preferred dates", ph="Any week that works") + '</div>',
                      inp("notes", "Anything else", "textarea")], "Send request")
    out["social"] = F("social", "Request a social post", "News, a milestone or something new? We will put it on our Facebook and Instagram.",
                      [inp("what", "What should we post about?", "textarea", req=True),
                       '<div class="x-2">' + inp("photo", "Photo", "file") + inp("when", "Best timing", ph="This week, a date, any time") + '</div>'], "Send request")
    if tier == "b":   # Basic shares one page (no private token): we need a way to reach them
        out["event"] = out["event"].replace('<button', inp("business", "Your business", req=True) + '<div class="x-2">' + inp("contact_name", "Your name") + inp("contact_email", "Your email", "email", req=True) + '</div><button', 1)
    if X.RANK[tier] < X.RANK["v"]:
        out["video"] = '<div class="drawlock"><span class="lockic">%s</span><b>A free promo video every month</b><i>VIPs get a fresh promo reel every month, produced by 3VL Digital in their own brand.</i><a class="btn primary" href="%s" data-ga="dash_upgrade_click" data-product="promo_reel">Upgrade to VIP %s</a></div>' % (ic("lock"), UPGRADE, ic("chev"))
    if not has(tier, "special"):
        out["special"] = '<div class="drawlock"><span class="lockic">%s</span><b>Feature your specials</b><i>Featured and VIP members send us deals and we put them in front of neighbors.</i><a class="btn primary" href="%s">Upgrade to Featured %s</a></div>' % (ic("lock"), UPGRADE, ic("chev"))
    if not has(tier, "social_req"):
        out["social"] = '<div class="drawlock"><span class="lockic">%s</span><b>Request a social spotlight</b><i>Featured and VIP members can ask us to feature their business on our Facebook and Instagram.</i><a class="btn primary" href="%s">Upgrade to Featured %s</a></div>' % (ic("lock"), UPGRADE, ic("chev"))
    return "".join('<section class="drawpane" data-pane="%s" hidden>%s</section>' % (k, v) for k, v in out.items())


ACTIONS = [("event", "cal", "Submit an event", "Add it to our calendar and weekend picks", "blue"),
           ("special", "tag", "Submit a special", "Deals, menus and seasonal offers", "amber"),
           ("video", "video", "Your free promo reel", "VIP perk: a new video every month", "violet"),
           ("social", "insta", "Request a social post", "Facebook and Instagram, tagged", "pink"),
           ("listing", "edit", "Update my listing", "Hours, photos, services, contact", "green")]


def action_btn(k, icn, label, sub, color, tier, big=False):
    locked = (k == "special" and not has(tier, "special")) or (k == "social" and not has(tier, "social_req")) or (k == "video" and X.RANK[tier] < X.RANK["v"])
    if k == "listing":
        return '<a class="qa %s%s" href="%s" data-ga="dash_action_open" data-product="listing"><span class="qa-ic">%s</span><b>%s</b>%s</a>' % (
            color, " big" if big else "", LOGIN_EDIT, ic(icn), label, ("<i>%s</i>" % sub) if big else "")
    return '<button type="button" class="qa %s%s" data-open="%s" data-ga="dash_action_open" data-product="%s"><span class="qa-ic">%s</span><b>%s</b>%s%s</button>' % (
        color, " big" if big else "", k, k, ic(icn), label, ("<i>%s</i>" % sub) if big else "", '<em class="qa-lk">%s</em>' % ic("lock") if locked else "")


def industry_shot(cat):
    c = (cat or "").lower()
    for keys, shot in ((("restaurant", "food", "bakery", "cafe", "pizza", "bar", "deli", "catering", "eat"), "dash-restaurant"),
                       (("beauty", "salon", "spa", "hair", "nail", "esthetic", "skin", "barber", "wellness"), "dash-salon"),
                       (("fitness", "gym", "yoga", "pilates", "martial", "sport"), "dash-gym"),
                       (("landscap", "lawn", "tree", "garden", "plant"), "dash-landscaper")):
        if any(re.search(r"" + k, c) for k in keys):
            return shot
    return "dash-contractor"


LOGO_BASE = "https://threevillagelocal-cloud.github.io/3vl-share/ai-5-ways/img/logos/"
LOGOS_ROW = ('<div class="sf-logos"><span class="sf-lk">Connects to 400+ programs you already use</span><div class="sf-lg">' + "".join(
    '<span class="lg" style="--d:%d"><img src="%s%s.svg" alt="%s" width="22" height="22" loading="lazy" decoding="async" data-processed="true"></span>' % (i, LOGO_BASE, f, n)
    for i, (f, n) in enumerate((("quickbooks", "QuickBooks"), ("square", "Square"), ("stripe", "Stripe"), ("googlecalendar", "Google Calendar"), ("gmail", "Gmail"),
                                ("shopify", "Shopify"), ("mailchimp", "Mailchimp"), ("hubspot", "HubSpot"), ("facebook", "Facebook"), ("instagram", "Instagram"),
                                ("paypal", "PayPal"), ("calendly", "Calendly"))[:9])) + '<span class="lg more">+400</span></div></div>')


def sample_feature(company, first, sample_done, tier, full, cat):
    """Owner 11/15: the free dashboard sample offer is the most eye-catching card on the Overview (wide, condensed caps, glowing CTA,
    tilted dashboard mockup for THEIR industry, FREE ribbon, animated border). Thank-you state + weekly cap/waitlist kept."""
    if tier == "b" or sample_done:
        return ""
    comp = e(company) if company else "your business"
    shot = industry_shot(cat)
    if full:
        h = 'Our free sample spots are <em>full this week.</em>'
        sub = "Join the list and we will reach out to %s first." % comp
        btn = ('<button type="button" class="sf-cta" data-sample data-kind="dashboard_sample_waitlist" data-first="%s" data-ga="dash_sample_request" data-product="waitlist">'
               'Join the list %s</button>' % (e(first or ""), ic("chev")))
        fine = "No obligation"
    else:
        h = 'We make custom dashboards <em>like this</em> for <em>your business.</em>'
        sub = "Leads, jobs, team and money on one screen. Logins for you, your managers and your staff."
        btn = ('<button type="button" class="sf-cta" data-sample data-first="%s" data-ga="dash_sample_request" data-product="dashboards">'
               'Request a free working sample <span aria-hidden="true">&rarr;</span></button>' % e(first or ""))
        fine = "No obligation &middot; Built for %s" % comp
    return ('<section class="sfeat card" data-ups="dashboards" id="sfeat"><span class="sf-streak" aria-hidden="true"></span>'
            '<div class="sf-t ups-t"><span class="sf-k">3VL Digital &middot; Custom dashboards</span><h2>%s</h2><p>%s</p>%s<span class="sf-fine">%s</span>%s</div>'
            '<div class="sf-v" aria-hidden="true"><div class="sf-frame"><div class="sf-bar"><i></i><i></i><i></i><span>app.yourbusiness.com</span></div>'
            '<img src="%s%s-640.webp" srcset="%s%s-640.webp 640w, %s%s-1200.webp 1200w" sizes="(max-width: 860px) 90vw, 520px" alt="" width="640" height="400" loading="lazy" decoding="async" data-processed="true"></div></div></section>') % (
        h, sub, btn, fine, LOGOS_ROW, SHOT, shot, SHOT, shot, SHOT, shot)


def upsell_cards(company, first, sample_done, tier, full):
    """3VL Digital slot (photo-rich): free working dashboard sample first, then chatbot / websites / tip. dash3.js shows one per visit."""
    comp = e(company) if company else '<span data-md-name>your business</span>'
    c = []
    if tier == "b":
        c.append(('dashboards', '3VL Digital &middot; Coming soon', 'Custom dashboards for local businesses are coming to members.',
                  'Upgrade to Featured to get a free working sample built for your business.',
                  '<a class="btn light" href="%s" data-ga="dash_upgrade_click" data-product="sample_teaser">Upgrade to Featured %s</a>' % (UPGRADE, ic("chev")), "dash-restaurant-640.webp"))
    elif not sample_done and full:
        c.append(('dashboards', '3VL Digital &middot; Custom dashboards', 'Our free sample spots are full this week.',
                  'Join the list and we will reach out to %s first.' % comp,
                  '<button type="button" class="btn light" data-sample data-kind="dashboard_sample_waitlist" data-first="%s" data-ga="dash_sample_request" data-product="waitlist">Join the list %s</button>' % (e(first or ""), ic("chev")), "dash-contractor-640.webp"))
    elif not sample_done:
        c.append(('dashboards', '3VL Digital &middot; Free working sample', 'Want one built for %s?' % comp,
                  'Like this dashboard? We will build a free working sample for your business: leads, jobs, team and money on one screen.',
                  '<button type="button" class="btn light" data-sample data-first="%s" data-ga="dash_sample_request" data-product="dashboards">Request my free sample %s</button>' % (e(first or ""), ic("chev")), "dash-contractor-640.webp"))
    for k, kick, h, sub, btn, path, im in (
            ("chatbots", "3VL Digital &middot; AI chatbots", "Your website could answer customers at 10 PM.", "An AI chatbot trained on your business answers every question and texts you the lead.", "Try our AI chatbot", "/chatbots", "chat-ridge-560.webp"),
            ("websites", "3VL Digital &middot; Websites", "A website that works as hard as you do.", "Built from scratch to sell, and to be recommended by Google and AI.", "See AI-ready websites", "/websites", "chris-640.webp")):
        url = "%s%s?utm_source=3vl&utm_medium=member-dashboard&utm_campaign=%s-upsell" % (DIG, path, k[:-1])
        c.append((k, kick, h, sub, '<a class="btn light" href="%s" target="_blank" rel="noopener" data-ga="dash_upsell_click" data-product="%s">%s %s</a>' % (e(url), k, btn, ic("chev")), im))
    return "".join('<div class="ups" data-ups="%s"%s><div class="ups-t"><span class="ups-k">%s</span><b>%s</b><i>%s</i>%s</div><div class="ups-v">%s</div></div>'
                   % (k, "" if i == 0 else " hidden", kick, h, sub, btn, img(SHOT + im, "", 320, 200)) for i, (k, kick, h, sub, btn, im) in enumerate(c))


def page(a, ctx):
    tier = ctx["tier"]
    uid, w0 = a.get("uid", ""), ctx["w0"]
    j = X.v3_profile(uid, ctx["share_dir"]) if uid else {}
    checks = X.profile_checks(j, ctx.get("member") or {})
    first = (j.get("first") or "").strip() or a.get("short") or ""
    short = a.get("short") or ""
    real = [it for it in a.get("items", []) if not it.get("sample")]
    hp30 = [d for d in a.get("hp_days", []) if d >= w0]
    soc30 = [it for it in real if it["ch"] == "social" and it["date"] >= w0]
    em30 = [it for it in real if it["ch"] == "email" and it["date"] >= w0]
    bview = ctx["banner_views"] if (has(tier, "banner") and a.get("has_banner_ad") and ctx["banner_views"] >= 1000) else 0
    reach = ctx.get("reach") or 0
    lifetime = a.get("lifetime") or 0
    net = ctx.get("net") or {}
    others = ctx.get("others") or []
    gal = [VIPIMG + g["img"] for g in (j.get("gallery") or []) if g.get("img")]
    hero_photo = a.get("banner") or (gal[0] if gal else "") or a.get("logo") or ""
    banner_src = (ctx["raw"] + a["banner_img"]) if a.get("banner_img") else ""
    name_html = e(short) if uid else '<span data-md-name>Your business</span>'
    hello = e(first) if uid else '<span data-md-name>neighbor</span>'
    month = dt.date.today().strftime("%B %Y")

    # ---- hero summary (plain language, positive, real)
    bits = []
    if bview:
        bits.append("your banner ad on <b>every page</b> of our site")
    if hp30 and has(tier, "spotlight"):
        bits.append("<b>%d day%s</b> in our homepage spotlight" % (len(hp30), "" if len(hp30) == 1 else "s"))
    if soc30:
        bits.append("<b>%d social post%s</b> about you" % (len(soc30), "" if len(soc30) == 1 else "s"))
    if em30:
        bits.append("a feature in <b>Three Village Weekly</b>")
    if bits:
        lead = "In the last 30 days we put %s in front of neighbors%s: " % (e(short), (" up to <b>%s times</b>" % "{:,}".format(reach)) if reach else "")
        summary = lead + (", ".join(bits[:-1]) + " and " + bits[-1] if len(bits) > 1 else bits[0]) + "."
    elif tier == "b":
        summary = "You are listed on Three Village Local, where neighbors find local businesses. Here is how to get seen more."
    else:
        summary = "Your next spotlight is on the way. Have news, a special or an event? Send it to us and we will promote it."

    # ---- KPI tiles (floor rule: weak or missing numbers never show)
    k = []
    if bview:
        k.append(("eye", "Banner reach", bview, "up to ", "+", "this month", spark(series(a, 30)), "#seen"))
    if hp30 and has(tier, "spotlight"):
        k.append(("home", "Homepage spotlight", len(hp30), "", "", "days this month", spark(series(a, 30, home=True)), "#seen"))
    if (soc30 or em30) and has(tier, "timeline"):
        k.append(("insta", "Social and email", len(soc30) + len(em30), "", "", "this month", spark(series(a, 30, ch=("social", "email"))), "#promotions"))
    if lifetime >= 3 and has(tier, "timeline"):
        k.append(("megaphone", "Promotions for you", lifetime, "", "", "since you joined", spark(series(a, 90)), "#promotions"))
    if int(net.get("views") or 0) >= 1000:
        k.append(("globe", "Three Village Local", int(net["views"]) // 1000 * 1000, "", "+", "page views", spark([]), "#grow"))
    if len(k) < 4 and int(net.get("social") or 0) >= 1000:
        k.append(("share", "Social reach", int(net["social"]) // 1000 * 1000, "", "+", "social views", spark([]), "#grow"))
    if len(k) < 4 and int(net.get("subs") or 0) >= 100:
        k.append(("mail", "Weekly email", int(net["subs"]), "", "", "subscribers", spark([]), "#grow"))
    k = k[:5]
    kpis = "".join('<a class="card kpi" href="%s" data-go="%s"><span class="label">%s %s</span><span class="value num" data-count="%d" data-pre="%s" data-suf="%s">%s%s%s</span>'
                   '<span class="delta">%s</span>%s</a>' % (h, h[1:], ic(i), t, n, pre, suf, pre, "{:,}".format(n), suf, d, sp) for i, t, n, pre, suf, d, sp, h in k)

    brief = []
    if bview:
        brief.append(("{:,}+".format(bview), "Banner views this month"))
    if hp30 and has(tier, "spotlight"):
        brief.append((str(len(hp30)), "Days on our homepage"))
    if (soc30 or em30):
        brief.append((str(len(soc30) + len(em30)), "Social and email features"))
    if lifetime >= 3 and has(tier, "timeline"):
        brief.append((str(lifetime), "Promotions since you joined"))
    briefs = "".join('<div class="brief-item"><b>%s</b><span>%s</span></div>' % b for b in brief[:4])

    # ---- seen: banner + spotlight (or locks)
    if bview:
        ban_card = ('<div class="card seen" data-go="seen"><div class="card-head"><span class="card-icon blue">%s</span><div><h3>Your banner ad</h3><div class="sub">Rotating on every page</div></div>'
                    '<span class="right"><span class="pill live"><i></i>Live</span></span></div><div class="card-body seen-b">%s<div class="seen-n"><b class="num" data-count="%d" data-suf="+">%s+</b><i>times it may have been seen this month</i></div></div></div>'
                    % (ic("banner"), site_mock(banner_src, short), bview, "{:,}".format(bview)))
    elif not has(tier, "banner"):
        ban_card = '<div class="card seen">%s</div>' % lock("banner", site_mock("", ""))
    else:
        ban_card = ""
    if has(tier, "spotlight") and hp30:
        spot_card = ('<div class="card seen" data-go="seen"><div class="card-head"><span class="card-icon violet">%s</span><div><h3>On our homepage</h3><div class="sub">The Spotlight rotates our VIPs</div></div>'
                     '<span class="right"><a class="btn ghost sm" href="%s/" target="_blank" rel="noopener">See it live %s</a></span></div><div class="card-body">%s</div></div>'
                     % (ic("home"), SITE, ic("ext"), spot_mock(a, others)))
    elif not has(tier, "spotlight"):
        spot_card = '<div class="card seen">%s</div>' % lock("spotlight", spot_mock({"short": "Your business here", "cat": "Your category"}, others))
    else:
        spot_card = ""

    # ---- chart
    if has(tier, "chart"):
        bc = bigchart(a)
        chart_card = ('<div class="card"><div class="card-head"><span class="card-icon green">%s</span><div><h3>Your promotions keep adding up</h3><div class="sub">Running total, last 90 days</div></div>'
                      '<span class="right"><span class="pill up">%s +%d</span></span></div><div class="card-body">%s<p class="chart-n"><b>%s</b> promotions for you since you joined</p></div></div>'
                      % (ic("trend"), ic("trend"), bc[1], bc[0], "{:,}".format(bc[2]))) if bc else ""
    else:
        chart_card = '<div class="card">%s</div>' % lock("chart", bigchart({}, sample=True)[0])

    # ---- activity
    def row(it, big=False):
        d = dt.date.fromisoformat(it["date"])
        th = img(it.get("thumb"), "", 44, 44) if it.get("thumb") else '<span class="feed-ic">%s</span>' % ic(it["icon"] if it["icon"] in ICONS else "dot")
        link = (' <a href="%s" target="_blank" rel="noopener">See it %s</a>' % (e(it["url"]), ic("ext"))) if (it.get("url") and big) else ""
        return '<li class="act" data-f="%s"><span class="act-th">%s</span><div class="act-b"><b class="ellip">%s</b><i>%s%s</i></div><time datetime="%s">%s</time></li>' % (
            it["ch"], th, e(it["title"]), e(it["note"]), link, it["date"], X.fmt(d))
    demo = [{"date": dt.date.today().isoformat(), "ch": "web", "icon": "home", "title": "On our homepage, 7 days", "note": "Your card in the Local Business Spotlight"},
            {"date": dt.date.today().isoformat(), "ch": "social", "icon": "insta", "title": "Spotlight on Instagram and Facebook", "note": "Tagged with a collab invite"},
            {"date": dt.date.today().isoformat(), "ch": "email", "icon": "mail", "title": "Featured in Three Village Weekly", "note": "Your photo and story in our weekly email"}]
    if has(tier, "timeline") and real:
        act_card = ('<div class="card"><div class="card-head"><span class="card-icon amber">%s</span><div><h3>What we did for you</h3><div class="sub">%s</div></div>'
                    '<span class="right"><a class="btn ghost sm" href="#promotions" data-go="promotions">See all %s</a></span></div><ul class="acts">%s</ul></div>'
                    % (ic("megaphone"), ("%d promotions since you joined" % lifetime) if lifetime >= 3 else "Newest first", ic("chev"), "".join(row(it) for it in real[:4])))
        chans = sorted({it["ch"] for it in real})
        chips = ('<div class="seg" role="group" aria-label="Filter"><button type="button" class="on" data-f="all">All</button>' + "".join(
            '<button type="button" data-f="%s">%s</button>' % (c, l) for c, l in (("web", "Website"), ("social", "Social"), ("email", "Email")) if c in chans) + "</div>") if len(chans) > 1 else ""
        tl_full = ('<div class="card tl"><div class="card-head"><span class="card-icon amber">%s</span><div><h3>What we did for you</h3><div class="sub">Newest first</div></div><span class="right">%s</span></div>'
                   '<ul class="acts scroll">%s</ul></div>' % (ic("megaphone"), chips, "".join(row(it, True) for it in real)))
    elif not has(tier, "timeline"):
        act_card = '<div class="card">%s</div>' % lock("timeline", '<ul class="acts">%s</ul>' % "".join(row(it) for it in demo))
        tl_full = act_card
    else:
        act_card = ('<div class="card"><div class="card-head"><span class="card-icon amber">%s</span><div><h3>What we did for you</h3><div class="sub">Coming up next</div></div></div>'
                    '<div class="card-body empty"><b>Your next spotlight is on the way.</b><i>Send us an event or special and we will put it in front of neighbors.</i>'
                    '<button type="button" class="btn primary sm" data-open="event">Submit an event %s</button></div></div>' % (ic("megaphone"), ic("chev")))
        tl_full = act_card

    # ---- upcoming
    up = [u for u in (a.get("upcoming") or []) if not u.get("sample")]
    upc = "".join('<li><span class="date"><b>%s</b><i>%d</i></span><div><b>%s</b><i>%s</i></div></li>' % (
        dt.date.fromisoformat(u["date"]).strftime("%b"), dt.date.fromisoformat(u["date"]).day, e(u["title"]), e(u["note"])) for u in up[:4]) or (
        '<li><span class="date"><b>%s</b><i>%s</i></span><div><b>More on the way</b><i>Send us your news, specials and events and we will promote them.</i></div></li>' % (dt.date.today().strftime("%b"), "&bull;"))
    upc_card = '<div class="card"><div class="card-head"><span class="card-icon blue">%s</span><div><h3>Coming up for you</h3><div class="sub">Scheduled promotions</div></div></div><ul class="upc">%s</ul></div>' % (ic("cal"), upc)

    # ---- profile strength
    done = sum(1 for _, ok, _ in checks if ok)
    pct = round(done * 100 / len(checks))
    ring = ('<div class="ring" style="--p:%d"><svg viewBox="0 0 44 44" aria-hidden="true"><circle cx="22" cy="22" r="19" class="rt"/><circle cx="22" cy="22" r="19" class="rv draw-ring"/></svg>'
            '<b class="num" data-count="%d" data-suf="%%">%d%%</b></div>') % (pct, pct, pct)
    plist = "".join('<li class="%s"><span class="ck">%s</span><div><b>%s</b>%s</div>%s</li>' % (
        "ok" if ok else "todo", ic("check") if ok else ic("dot"), t, "" if ok else "<i>%s</i>" % tip,
        "" if ok else '<a class="fix" href="%s">Fix %s</a>' % (LOGIN_EDIT, ic("chev"))) for t, ok, tip in checks)

    # ---- quick links
    prof = a.get("profile") or ""
    qr = X.qr_data_uri(prof) if prof else ""
    rv = (j.get("reviews") or {}).get("url") if isinstance(j.get("reviews"), dict) else ""
    sh = quote(prof, safe="")
    ql = []
    if prof:
        ql.append('<div class="tool"><span class="card-icon blue">%s</span><div><b>Share your profile</b><i>Send neighbors straight to you</i><div class="row-wrap">'
                  '<button type="button" class="chip" data-copy="%s">%s Copy link</button><a class="chip" href="https://www.facebook.com/sharer/sharer.php?u=%s" target="_blank" rel="noopener">Facebook</a>'
                  '<a class="chip" href="https://www.linkedin.com/sharing/share-offsite/?url=%s" target="_blank" rel="noopener">LinkedIn</a><a class="chip" href="mailto:?subject=%s&amp;body=%s">Email</a></div></div></div>'
                  % (ic("share"), e(prof), ic("copy"), sh, sh, quote(short), sh))
    if qr:
        ql.append('<div class="tool"><img class="qr" src="%s" alt="QR code for your profile" width="64" height="64"><div><b>Your QR code</b><i>Print it on cards, flyers and your counter</i>'
                  '<div class="row-wrap"><a class="chip" href="%s" download="3vl-qr-%s.png">Download</a></div></div></div>' % (qr, qr, e(uid)))
    if rv:
        ql.append('<div class="tool"><span class="card-icon amber">%s</span><div><b>Your review link</b><i>Ask happy customers for a quick Google review</i>'
                  '<div class="row-wrap"><button type="button" class="chip" data-copy="%s">%s Copy link</button></div></div></div>' % (ic("star"), e(rv), ic("copy")))
    ql.append('<div class="tool"><span class="card-icon green">%s</span><div><b>Our free mobile app</b><i>Local news, events and your listing in one place</i>'
              '<div class="row-wrap"><a class="chip" href="%s/app" target="_blank" rel="noopener">Get the free mobile app</a></div></div></div>' % (ic("phone"), SITE))

    ups = upsell_cards(short, first if uid else "", ctx.get("sample_done", False), tier, ctx.get("samples_full", False))
    meet = ('<div class="card meet"><div class="card-body">%s<p><b>Meet 3VL Digital.</b> From the team behind Three Village Local: AI chatbots, AI-ready websites and custom dashboards for local businesses.</p>'
            '<div class="row-wrap"><a class="btn primary sm" href="%s/?utm_source=3vl&amp;utm_medium=member-dashboard&amp;utm_campaign=meet-3vl-digital" target="_blank" rel="noopener" data-ga="dash_upsell_click" data-product="meet_3vl_digital">Visit 3vldigital.com %s</a>'
            '<span class="faint small">Follow</span><a class="chip" href="https://www.instagram.com/3vl.digital/" target="_blank" rel="noopener" data-ga="dash_follow_click" data-product="instagram">Instagram</a>'
            '<a class="chip" href="%s" target="_blank" rel="noopener" data-ga="dash_follow_click" data-product="facebook">Facebook</a>'
            '<a class="chip" href="https://www.linkedin.com/company/3vldigital" target="_blank" rel="noopener" data-ga="dash_follow_click" data-product="linkedin">LinkedIn</a></div></div></div>'
            % (img(DIG + "/assets/img/brand/logo-full.webp", "3VL Digital", 150, 50, "meet-logo"), DIG, ic("chev"), FB_DIGITAL))
    news = [("Just launched", "Homepage trivia: neighbors play every Monday, with local business prizes."),
            ("Live now", "Our Thanksgiving guide is up. Send us your holiday hours and specials."),
            ("New", "AI chatbots by 3VL Digital: answer customers 24/7 on your own website.")]
    news_card = '<div class="card"><div class="card-head"><span class="card-icon pink">%s</span><div><h3>What&#39;s new at 3VL</h3></div></div><ul class="news">%s</ul></div>' % (
        ic("spark"), "".join('<li><em>%s</em><span>%s</span></li>' % n for n in news))
    netl = []
    if int(net.get("views") or 0) >= 1000:
        netl.append(("globe", int(net["views"]) // 1000 * 1000, "+", "Website page views this month"))
    if int(net.get("social") or 0) >= 1000:
        netl.append(("share", int(net["social"]) // 1000 * 1000, "+", "Facebook and Instagram views, 28 days"))
    if int(net.get("subs") or 0) >= 100:
        netl.append(("mail", int(net["subs"]), "", "Neighbors who get Three Village Weekly"))
    net_card = ('<div class="card"><div class="card-head"><span class="card-icon blue">%s</span><div><h3>Three Village Local right now</h3><div class="sub">Updated nightly</div></div></div><div class="netg">%s</div></div>'
                % (ic("trend"), "".join('<div><span class="card-icon">%s</span><b class="num" data-count="%d" data-suf="%s">%s%s</b><i>%s</i></div>' % (ic(i), n, s, "{:,}".format(n), s, t) for i, n, s, t in netl))) if netl else ""
    products = [("chatbots", "AI chatbots", "Answers your customers 24/7 and texts you every lead", "chat-ridge-560.webp", "/chatbots"),
                ("websites", "AI-ready websites", "Built to sell, and to be recommended by Google and AI", "chris-640.webp", "/websites"),
                ("dashboards", "Custom dashboards", "Leads, jobs, team and money on one screen", "dash-restaurant-640.webp", "/dashboards")]
    prod = "".join('<a class="card prod" href="%s%s?utm_source=3vl&amp;utm_medium=member-dashboard&amp;utm_campaign=grow-%s" target="_blank" rel="noopener" data-ga="dash_upsell_click" data-product="grow_%s">'
                   '<span class="prod-img">%s</span><span class="prod-t"><b>%s</b><i>%s</i></span></a>' % (DIG, p, k, k, img(SHOT + im, ""), t, d) for k, t, d, im, p in products)
    # owner 11/15: only offers that are 100% working end to end (AI visibility report + drone cards removed until they have a working request path)
    more = ([("video", "Your free promo reel", "VIP perk: a new video every month", "data-open=\"video\"")] if X.RANK[tier] >= X.RANK["v"] else []) + [
            ("insta", "Social spotlight", "Ask us to feature you on Facebook and Instagram", "data-open=\"social\""),
            ("cal", "Event promotion", "Calendar, weekend picks and weekly email", "data-open=\"event\"")]
    if RANK[tier] < RANK["v"]:
        more.insert(0, ("star", "Upgrade to VIP" if tier == "f" else "Upgrade your listing", "Banner ad, homepage spotlight and more", 'href="%s"' % UPGRADE))
    morel = "".join('<%s class="tile-l" %s data-ga="dash_upsell_click" data-product="%s"><span class="card-icon">%s</span><span><b>%s</b><i>%s</i></span>%s</%s>' % (
        "button type=\"button\"" if h.startswith("data-") else "a", h, re.sub(r"[^a-z]+", "_", t.lower()).strip("_"), ic(i), t, d, ic("chev"), "button" if h.startswith("data-") else "a") for i, t, d, h in more)

    # ---- actions grid (big tiles)
    act_big = "".join(action_btn(*x, tier=tier, big=True) for x in ACTIONS)
    act_small = "".join(action_btn(*x, tier=tier) for x in ACTIONS[:4])

    # ---- listing preview (profile view)
    listing = ('<div class="card listing"><div class="lst-cover">%s%s</div><div class="card-body"><b class="lst-n">%s</b><i class="lst-c">%s%s</i>'
               '<div class="row-wrap mt-s"><a class="btn primary sm" href="%s" target="_blank" rel="noopener">View your profile %s</a><a class="btn ghost sm" href="%s">Edit listing %s</a></div></div>'
               '%s</div>') % (img(hero_photo, "Your profile cover"), img(a.get("logo"), short + " logo", 56, 56, "lst-logo"), name_html, e(a.get("cat") or ""),
                              (" &middot; " + e(a["town"])) if a.get("town") else "", e(prof or SITE), ic("ext"), LOGIN_EDIT, ic("chev"),
                              ('<div class="gal">%s</div>' % "".join(img(g, "", 120, 90) for g in gal[:5])) if gal else "")


    # ---- spotlight calendar (last 35 days, their homepage days lit) + channel mix + banner tips
    today = dt.date.today()
    hpset = set(a.get("hp_days", []))
    cal_start = today - dt.timedelta(days=34)
    cal_start -= dt.timedelta(days=cal_start.weekday())
    cells = []
    d = cal_start
    while d <= today:
        on = d.isoformat() in hpset
        cells.append('<span class="cd%s" title="%s%s">%d</span>' % (" on" if on else "", X.fmt(d), " on the homepage" if on else "", d.day))
        d += dt.timedelta(days=1)
    cal_card = ('<div class="card"><div class="card-head"><span class="card-icon violet">%s</span><div><h3>Your spotlight days</h3><div class="sub">Lit days = your business in the homepage Spotlight</div></div></div>'
                '<div class="card-body"><div class="calh">%s</div><div class="cal">%s</div></div></div>') % (
        ic("cal"), "".join("<i>%s</i>" % x for x in ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")), "".join(cells)) if (hp30 and has(tier, "spotlight")) else ""
    mix = [("Homepage", len([x for x in a.get("hp_days", [])]), "#7c5cd6"), ("Social", len([x for x in real if x["ch"] == "social"]), "#e2725b"),
           ("Email", len([x for x in real if x["ch"] == "email"]), "#18794e"), ("Website", len([x for x in real if x["ch"] == "web" and not x.get("n_home")]), "#2f7fe0")]
    mix = [m for m in mix if m[1] > 0]
    tot = sum(m[1] for m in mix)
    if tot >= 3 and has(tier, "timeline"):
        acc, segs = 0.0, []
        for lab, n, col in mix:
            frac = n / tot
            segs.append('<circle cx="21" cy="21" r="15.9" fill="none" stroke="%s" stroke-width="6" stroke-dasharray="%.2f %.2f" stroke-dashoffset="%.2f" class="seg-c"/>' % (col, frac * 100, 100 - frac * 100, 25 - acc * 100))
            acc += frac
        mix_card = ('<div class="card"><div class="card-head"><span class="card-icon blue">%s</span><div><h3>Where we promoted you</h3><div class="sub">Every channel, since you joined</div></div></div>'
                    '<div class="card-body mixb"><div class="donut"><svg viewBox="0 0 42 42" aria-hidden="true">%s</svg><b class="num" data-count="%d">%d</b><i>total</i></div><ul class="mixl">%s</ul></div></div>') % (
            ic("layers"), "".join(segs), tot, tot, "".join('<li><span style="background:%s"></span>%s<b>%d</b></li>' % (col, lab, n) for lab, n, col in mix))
    else:
        mix_card = ""
    tips_card = ('<div class="card"><div class="card-head"><span class="card-icon amber">%s</span><div><h3>Get even more from it</h3><div class="sub">Ideas from our team</div></div></div><ul class="tipl">'
                 '<li><b>Send us something new</b><i>Specials and events give us more reasons to feature you.</i><button type="button" class="chip" data-open="event">Submit an event</button></li>'
                 '<li><b>Share your profile</b><i>Every share sends neighbors straight to your page.</i><a class="chip" href="#profile" data-go="profile">Share tools</a></li>'
                 '<li><b>Tell your customers</b><i>Print your QR code for the counter, cards and flyers.</i><a class="chip" href="#profile" data-go="profile">Get your QR code</a></li></ul></div>') % ic("spark")

    # ---- sidebar
    acct = [("tag", "Billing and payment", "/account/billing/change"), ("star", "Upgrade my plan", "/account/upgrade"), ("lock", "Change password", "/account/password")]
    acct_more = [("edit", "Edit my listing", "/account/contact"), ("mail", "Leads and inquiries", "/account/leads")]
    acct_nav = "".join('<a class="nav-acct" href="/login?login_direct_url=%s" data-acct="%s" data-ga="dash_account_click" data-product="%s">%s<span>%s</span></a>' % (
        quote(p, safe=""), p, re.sub(r"[^a-z]+", "_", t.lower()), ic(i if i in ICONS else "chev"), t) for i, t, p in acct) + '<a class="nav-acct" href="/logout" data-acct="/logout">%s<span>Sign out</span></a>' % ic("x")
    more_acct_nav = "".join('<a class="nav-acct" href="/login?login_direct_url=%s" data-acct="%s" data-ga="dash_account_click" data-product="%s">%s<span>%s</span></a>' % (
        quote(p, safe=""), p, re.sub(r"[^a-z]+", "_", t.lower()), ic(i if i in ICONS else "chev"), t) for i, t, p in acct_more) + acct_nav
    leads_nav = '<a class="nav-leads" href="/login?login_direct_url=%s" data-acct="/account/leads" data-ga="dash_account_click" data-product="leads">%s<span>Leads</span><em class="nb lead">Inquiries</em></a>' % (quote("/account/leads", safe=""), ic("mail"))
    def nav(v, icn, label, badge=""):
        return '<a href="#%s" data-go="%s"%s>%s<span>%s</span>%s</a>' % (v, v, ' class="on" aria-current="page"' if v == "overview" else "", ic(icn), label, badge)
    lockb = '<em class="nlk">%s</em>' % ic("lock")
    seen_lock = lockb if not (has(tier, "banner") and has(tier, "spotlight")) else ""
    promo_badge = ('<em class="nb">%d</em>' % len(soc30 + em30)) if (soc30 or em30) and has(tier, "timeline") else ("" if has(tier, "timeline") else lockb)
    side = ('<aside class="sidebar"><a class="brand" href="%s/" target="_blank" rel="noopener">%s<span class="brand-sub">Member dashboard</span></a><nav class="nav" aria-label="Dashboard">'
            '%s%s%s%s%s<details class="nav-grp"><summary>%s<span>Account</span>%s</summary>%s</details></nav>'
            '<a class="side-dig" href="https://3vldigital.com/?utm_source=3vl&amp;utm_medium=member-dashboard&amp;utm_campaign=sidebar" target="_blank" rel="noopener" data-ga="dash_upsell_click" data-product="sidebar_3vl_digital"><span>Visit our business AI services at</span><img src="https://3vldigital.com/assets/img/brand/logo-full-white.png" alt="3VL Digital" width="150" height="50" loading="lazy" decoding="async" data-processed="true"></a>'
            '<div class="side-foot"><div class="me">%s<div><b class="ellip">%s</b><span class="tierb t-%s">%s%s</span></div><button type="button" class="me-app" data-open="app" aria-label="Get the dashboard app on your phone" title="Get the app on your phone" data-ga="dash_action_open" data-product="get_app">%s</button></div></div></aside>') % (
        SITE, img("https://threevillagelocal-cloud.github.io/3vl-share/live/hdr/logo-white.webp", "Three Village Local", 168, 58, "brand-logo", lazy=False),
        nav("overview", "grid", "Overview"), nav("promotions", "megaphone", "Your promotions", promo_badge), leads_nav, nav("profile", "user", "Your listing"), nav("grow", "rocket", "Grow"),
        ic("lock"), '<span class="nav-chev">%s</span>' % ic("chev"), acct_nav,
        img(a.get("logo"), "", 64, 64, "me-logo") if a.get("logo") else '<span class="me-logo ph">%s</span>' % ic("user"), name_html, tier, "&#9733; " if X.RANK[tier] >= X.RANK["v"] else "", TIER_NAME[tier].upper() if X.RANK[tier] >= X.RANK["v"] else TIER_NAME[tier], ic("phone"))

    top = ('<header class="topbar"><label class="search">%s<input type="search" placeholder="Search your dashboard" aria-label="Search your dashboard" data-search></label>'
           '<span class="pill live hide-s"><i></i>Updated nightly</span>%s<div class="topbar-actions"><a class="btn primary sm hide-s" href="#actions" data-go="actions">%s Submit something</a>'
           '<a class="btn ghost sm hide-s" href="%s" target="_blank" rel="noopener">View profile %s</a><span class="avatar">%s</span></div></header>') % (
        ic("search"), ('<span class="tpill vip">&#9733; VIP MEMBER</span>' if X.RANK[tier] >= X.RANK["v"] else
                       '<span class="tpill">%s<a href="%s" data-ga="dash_upgrade_click" data-product="topbar">Upgrade</a></span>' % (TIER_NAME[tier], UPGRADE)),
        ic("send"), e(prof or SITE), ic("ext"), img(a.get("logo"), "", 34, 34) if a.get("logo") else ic("user"))

    hero_img = ('<img src="%s" alt="" fetchpriority="high" decoding="async" data-processed="true" onerror="this.style.opacity=0">' % e(hero_photo)) if hero_photo else ""
    hero = ('<section class="hero"><div class="hero-ph">%s</div><div class="hero-in"><span class="chip-ai">%s Your month &middot; %s</span>'
            '<h2><span data-greet>Hello</span>, %s.</h2><p class="hero-sum">%s</p><!--%s--><div class="brief-actions">'
            '<button type="button" class="btn gold sm" data-open="event">%s Submit an event</button>%s'
            '<a class="btn glass sm" href="#seen" data-go="seen">%s See where you show up</a></div></div></section>') % (
        hero_img, ic("spark"), month, hello, summary, ('<div class="brief">%s</div>' % briefs) if briefs else "", ic("cal"),
        ('<button type="button" class="btn glass sm" data-open="video">%s Your free promo reel</button>' % ic("video")) if X.RANK[tier] >= X.RANK["v"] else "", ic("eye"))

    prof_mini = ('<div class="card"><div class="card-head"><span class="card-icon green">%s</span><div><h3>Profile strength</h3><div class="sub">%s</div></div><span class="right">%s</span></div>'
                 '<div class="card-body"><div class="qa-grid">%s</div></div></div>') % (
        ic("user"), "Complete. Nice work." if done == len(checks) else "A complete profile gets more calls", ring, act_small) if uid else (
        '<div class="card"><div class="card-head"><span class="card-icon blue">%s</span><div><h3>Quick actions</h3><div class="sub">Send it to us and we get it out there</div></div></div><div class="card-body"><div class="qa-grid">%s</div></div></div>' % (ic("bolt"), act_small))

    sc = [c for c in (ban_card, spot_card) if c]
    if len(sc) == 1:
        sc.append(net_card or upc_card)
    elif not sc:
        sc = [net_card or upc_card, news_card]
    seen_row = '<div class="grid g-ov">%s%s</div>' % ("".join(sc), prof_mini)
    sfeat = sample_feature(short, first if uid else "", ctx.get("sample_done", False), tier, ctx.get("samples_full", False), a.get("cat"))
    third = sfeat or '<div class="card upsell" id="ups">%s</div>' % ups
    overview = ('<div class="view on" data-view="overview">%s<div class="kpis">%s</div>%s<div class="grid g-ov">%s%s%s</div></div>') % (
        hero, kpis, seen_row, chart_card or tips_card, act_card, third)

    promotions = ('<div class="view" data-view="promotions"><div class="vh"><h1>Promotions</h1><p>Everything we have done to put %s in front of neighbors.</p></div>'
                  '<div class="grid g-promo"><div class="stack">%s<div class="grid g-2">%s%s</div></div>%s</div></div>') % (name_html, chart_card or "", mix_card or news_card, upc_card, tl_full)

    seen_main = ""
    if bview:
        seen_main += ('<div class="card seen-big"><div class="card-head"><span class="card-icon blue">%s</span><div><h3>Your banner ad, on every page</h3><div class="sub">It rotates in the side rail across threevillagelocal.com</div></div>'
                      '<span class="right"><span class="pill live"><i></i>Live</span></span></div><div class="card-body sb">%s<div class="sb-side"><div class="ban-real">%s</div>'
                      '<div class="seen-n big"><b class="num" data-count="%d" data-suf="+">%s+</b><i>times your banner may have been seen this month</i></div></div></div></div>') % (
            ic("banner"), site_mock(banner_src, short), img(banner_src, "Your banner ad"), bview, "{:,}".format(bview))
    elif not has(tier, "banner"):
        seen_main += '<div class="card seen-big">%s</div>' % lock("banner", site_mock("", ""))
    if has(tier, "spotlight") and hp30:
        seen_main += ('<div class="card seen-big"><div class="card-head"><span class="card-icon violet">%s</span><div><h3>The homepage Business Spotlight</h3><div class="sub">You rotated through the big spot %d day%s this month</div></div>'
                      '<span class="right"><a class="btn ghost sm" href="%s/" target="_blank" rel="noopener">See it live %s</a></span></div><div class="card-body">%s</div></div>') % (
            ic("home"), len(hp30), "" if len(hp30) == 1 else "s", SITE, ic("ext"), spot_mock(a, others, big=True))
    elif not has(tier, "spotlight"):
        seen_main += '<div class="card seen-big">%s</div>' % lock("spotlight", spot_mock({"short": "Your business here", "cat": "Your category"}, others, big=True))
    if not seen_main:
        seen_main = net_card
    seen_more = "".join(c for c in (cal_card, tips_card, net_card) if c)
    seen = '<div class="view" data-view="seen"><div class="vh"><h1>Banner and Spotlight</h1><p>Where neighbors see %s on Three Village Local.</p></div><div class="grid g-2">%s</div><div class="grid g-3 mt">%s</div></div>' % (name_html, seen_main, seen_more)

    promotions = promotions.replace('<h1>Promotions</h1>', '<h1>Your promotions</h1>', 1).replace('</p></div><div class="grid g-promo">', '</p></div><div class="grid g-2 mb">%s</div><div class="grid g-promo">' % seen_main.replace('%', '%%').replace('%%', '%'), 1)
    if seen_more:
        promotions = promotions[:-len("</div>")] + '<div class="grid g-3 mt">%s</div></div>' % seen_more
    actions_v = ('<div class="view" data-view="actions"><div class="vh"><h1>Action center</h1><p>Send it to us and we will get it out there. Our team replies to every request.</p></div>'
                 '<div class="qa-big">%s</div><div class="grid g-3 mt">%s<div class="card how"><div class="card-head"><span class="card-icon violet">%s</span><div><h3>How it works</h3></div></div>'
                 '<ol class="steps"><li><b>Send it</b><i>Pick an action, add the details and a photo.</i></li><li><b>We review</b><i>Our team checks it and plans where it fits.</i></li>'
                 '<li><b>It goes out</b><i>Calendar, homepage, weekly email or social, tagged to you.</i></li></ol></div>%s</div></div>') % (
        act_big, upc_card, ic("layers"), news_card)

    profile_v = ('<div class="view" data-view="profile"><div class="vh"><h1>Your listing</h1><p>How neighbors see %s, plus tools to help them find you.</p><div class="row-wrap mt-s"><a class="btn primary sm" href="/login?login_direct_url=%%2Faccount%%2Fcontact">Edit my listing</a><a class="btn ghost sm" href="/login?login_direct_url=%%2Faccount%%2Fleads">See my leads</a></div></div>'
                 '<div class="grid g-prof">%s<div class="stack"><div class="card"><div class="card-head"><span class="card-icon green">%s</span><div><h3>Profile strength</h3><div class="sub">%s</div></div><span class="right">%s</span></div>'
                 '<ul class="checks">%s</ul></div><div class="card upsell">' + ups.replace('data-ups="', 'data-ups3="').replace('%', '%%') + '</div></div><div class="card"><div class="card-head"><span class="card-icon blue">%s</span><div><h3>Quick links</h3><div class="sub">Tools to help neighbors find you</div></div></div><div class="tools">%s</div></div></div></div>') % (
        name_html, listing if uid else '<div class="card listing"><div class="card-body"><b class="lst-n">%s</b><i class="lst-c">Basic member</i><div class="row-wrap mt-s"><a class="btn primary sm" href="%s">Edit listing %s</a></div></div></div>' % (name_html, LOGIN_EDIT, ic("chev")),
        ic("user"), "Complete. Nice work." if done == len(checks) else "A complete profile gets more calls", ring, plist, ic("share"), "".join(ql))

    grow_v = ('<div class="view" data-view="grow"><div class="vh"><h1>Grow with 3VL Digital</h1><p>From the team behind Three Village Local.</p></div>'
              '<div class="grid g-grow"><div class="card upsell big" id="ups2">%s</div>%s</div><div class="grid g-3 mt">%s</div><div class="grid g-3 mt"><div class="card"><div class="card-head"><span class="card-icon amber">%s</span><div><h3>More ways to grow</h3></div></div><div class="tiles">%s</div></div>%s%s</div></div>') % (
        ups.replace('data-ups="', 'data-ups2="'), meet, prod, ic("rocket"), morel, news_card, net_card)

    dash_url = ctx.get("dash_url") or ""
    app_qr = X.qr_data_uri(dash_url) if dash_url else ""
    app_pane = ('<section class="drawpane" data-pane="app" hidden><div class="apppane"><span class="card-icon blue">%s</span><h3>Put your dashboard app on your phone</h3>'
                '<p class="faint">It opens like an app, updates every morning and needs no login.</p>%s'
                '<div class="appsteps"><div><b>iPhone</b><ol><li>Open your dashboard link in <b>Safari</b></li><li>Tap <b>Share</b> (the square with an arrow)</li><li>Tap <b>Add to Home Screen</b></li></ol></div>'
                '<div><b>Android</b><ol><li>Open your dashboard link in <b>Chrome</b></li><li>Tap <b>Install app</b> (or the menu, then Add to Home screen)</li></ol>'
                '<button type="button" class="btn primary sm x-inst-go" data-install hidden>Get the app</button></div></div>%s</div></section>') % (
        ic("phone"), ('<div class="appqr"><img src="%s" alt="QR code to get your dashboard app on your phone" width="168" height="168"><i>Scan with your phone camera</i></div>' % app_qr) if app_qr else "",
        ('<button type="button" class="chip" data-copy="%s">%s Copy my dashboard link</button>' % (e(dash_url), ic("copy"))) if dash_url else "")
    more_pane = ('<section class="drawpane" data-pane="more" hidden><div class="morepane"><h3>More</h3><button type="button" class="tile-l" data-open="app">%s<span><b>Get the app on your phone</b><i>Your dashboard on your home screen</i></span></button>'
                 '<div class="nav-label">Account</div><div class="morelinks">%s</div><a class="side-dig" href="https://3vldigital.com/?utm_source=3vl&amp;utm_medium=member-dashboard&amp;utm_campaign=sidebar" target="_blank" rel="noopener" data-ga="dash_upsell_click" data-product="more_3vl_digital">'
                 '<span>Visit our business AI services at</span><img src="https://3vldigital.com/assets/img/brand/logo-full-white.png" alt="3VL Digital" width="150" height="50" loading="lazy" decoding="async" data-processed="true"></a></div></section>') % (ic("phone"), more_acct_nav)
    drawer = ('<div class="drawer" id="drawer" hidden aria-hidden="true"><div class="dr-scrim" data-close></div><div class="dr-panel" role="dialog" aria-modal="true" aria-label="Send to Three Village Local">'
              '<button type="button" class="dr-x" data-close aria-label="Close">%s</button>%s%s</div></div>') % (
        ic("x"), drawer_forms(tier) + app_pane + more_pane, '<p class="prev-note">Preview (test mode): what you send goes only to the 3VL team inbox, marked TEST.</p>' if ctx.get("preview") else "")
    status = ('<details class="pv-status"><summary>Preview status</summary><p><b>Working now</b></p><ul class="ok">'
              '<li>Switching views, numbers, charts, animations</li><li>Share links (copy, Facebook, LinkedIn, email)</li><li>QR code download</li>'
              '<li>Google review link copy</li><li>Upgrade, edit listing and view profile links (go through member login)</li><li>3VL Digital and follow links</li></ul>'
              '<p><b>Finish before go-live</b></p><ul class="todo"><li>Form submissions (event, special, promo video, social): endpoint to email you</li>'
              '<li>Free sample request + waitlist alert: same endpoint, weekly cap of 5</li><li>Home screen install: needs the private live pages + service worker</li>'
              '<li>Signed-in loader on /account/home (test with a real member login)</li></ul><p class="faint small">Monthly promo reel (free VIP perk) stays hidden until delivery works.</p></details>') if ctx.get("preview") else ""
    tabs = ('<nav class="tabbar" aria-label="Dashboard">%s</nav>' % ("".join(
        '<a href="#%s" data-go="%s"%s>%s<span>%s</span></a>' % (v, v, ' class="on"' if v == "overview" else "", ic(i), t) for v, i, t in (
            ("overview", "grid", "Home"), ("promotions", "megaphone", "Promos"), ("actions", "send", "Submit"), ("profile", "user", "Listing"), ("grow", "rocket", "Grow"))) + ('<a href="#" data-open="more">%s<span>More</span></a>' % ic("layers"))))
    attrs = (' data-preview="1"' if ctx.get("preview") else "") + (' data-endpoint="%s"' % e(ctx["endpoint"]) if ctx.get("endpoint") else "") + (' data-token="%s"' % e(ctx["token"]) if ctx.get("token") else "")
    body = ('<div class="mdx app" id="mdx" data-tier="%s" data-uid="%s"%s>%s<div class="main">%s<main class="content" id="view">%s%s%s%s%s%s'
            '<p class="foot">Questions or something to promote? Email <a href="mailto:hello@threevillagelocal.com">hello@threevillagelocal.com</a>. Updated nightly.</p></main></div>%s%s'
            '<div class="toasts" id="toasts" aria-live="polite"></div></div>') % (
        tier, uid, attrs, side, top, overview, promotions, "", actions_v, profile_v, grow_v, drawer, tabs + status)
    return body.replace('data-go="seen"', 'data-go="promotions"').replace('href="#seen"', 'href="#promotions"')


SHELL = X.SHELL.replace("family=Inter:wght@400;500;600;700;800", "family=Inter:wght@400;500;600;700;800&family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Anton")
manifest = X.manifest
INSTALL = X.INSTALL.replace('class="x-btn x-inst-go"', 'class="btn primary sm x-inst-go"')
