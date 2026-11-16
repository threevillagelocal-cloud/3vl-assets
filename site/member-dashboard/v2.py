"""Member Dashboard v2: ONE premium dashboard for every tier (Basic, Featured, VIP, Partner), in the visual language of the
Company Digital Dashboards demos. Features above a member's tier render as LOCKED cards (blurred preview + benefit + upgrade).
Built per member from real data only. Rules: never a negative, never a 0, weak cards hidden (floor rule), no prices, no em dashes."""
import base64, datetime as dt, html, io, json, os, re
from urllib.parse import quote

e = lambda s: html.escape(str(s or ""), quote=True)
SITE = "https://www.threevillagelocal.com"
LOGIN = "/login?login_direct_url=%2Faccount%2Fhome"
LOGIN_EDIT = "/login?login_direct_url=%2Faccount%2Fcontact"
UPGRADE = "/login?login_direct_url=%2Faccount%2Fupgrade"
RANK = {"b": 0, "f": 1, "v": 2, "p": 3}
TIER_NAME = {"b": "Basic member", "f": "Featured member", "v": "VIP member", "p": "Partner"}

# Tier map (who gets what). Anything above the member's tier shows as a locked teaser.
FEATURES = {
    "overview": "b", "network": "b", "profile": "b", "actions": "b", "quick": "b", "grow": "b", "news": "b",
    "event": "b", "video": "b",
    "special": "f", "timeline": "f", "chart": "f", "social_req": "f",
    "banner": "v", "spotlight": "v", "article": "v",
}
LOCK_COPY = {
    "timeline": ("f", "Your promotion history", "See every post, email feature and homepage day we give your business."),
    "chart": ("f", "Your promotions, adding up", "A running total of everything we do for you, updated nightly."),
    "special": ("f", "Feature your specials", "Send us your deals and we put them in front of neighbors."),
    "social_req": ("f", "Request a social spotlight", "Ask us to feature your business on our Facebook and Instagram."),
    "banner": ("v", "Your banner ad on every page", "VIPs get a banner ad that rotates across the whole website."),
    "spotlight": ("v", "Our homepage Business Spotlight", "VIPs rotate through the big spotlight on our homepage."),
}

ICONS = {
    "grid": '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
    "megaphone": '<path d="M3 11v2a1 1 0 0 0 1 1h2l5 4V6L6 10H4a1 1 0 0 0-1 1z"/><path d="M15 8a5 5 0 0 1 0 8"/><path d="M18 5a9 9 0 0 1 0 14"/>',
    "banner": '<rect x="2" y="6" width="20" height="12" rx="2"/><path d="M6 10h7M6 14h4"/><circle cx="17.5" cy="12" r="2"/>',
    "home": '<path d="M3 11 12 4l9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
    "insta": '<rect x="2" y="2" width="20" height="20" rx="5.5"/><circle cx="12" cy="12" r="4.2"/><path d="M17.6 6.4h.01"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    "rocket": '<path d="M5 15c-1.5 1.5-2 5-2 5s3.5-.5 5-2"/><path d="M9 15 6 12l7-7c2-2 6-2 6-2s0 4-2 6l-7 7z"/><circle cx="15" cy="9" r="1.5"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    "article": '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 7h8M8 11h8M8 15h5"/>',
    "check": '<path d="M5 12.5 10 17 19 7"/>', "dot": '<circle cx="12" cy="12" r="3"/>', "chev": '<path d="m9 6 6 6-6 6"/>',
    "ext": '<path d="M14 4h6v6"/><path d="M10 14 20 4"/><path d="M19 13v6a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h6"/>',
    "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/>',
    "video": '<rect x="3" y="6" width="13" height="12" rx="2"/><path d="m16 10 5-3v10l-5-3z"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
    "bot": '<rect x="4" y="8" width="16" height="11" rx="3"/><path d="M12 4v4M9 13h.01M15 13h.01M9 16h6"/>',
    "camera": '<path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/>',
    "lock": '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
    "edit": '<path d="M4 20h4L19 9l-4-4L4 16z"/><path d="m14 6 4 4"/>',
    "tag": '<path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="7.5" r="1.5"/>',
    "cal": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    "share": '<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="m8.6 13.5 6.8 4M15.4 6.5l-6.8 4"/>',
    "qr": '<rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><path d="M14 14h3v3h-3zM20 14v.01M14 20h.01M17 17h3v4"/>',
    "phone": '<rect x="7" y="2" width="10" height="20" rx="2.5"/><path d="M11 18h2"/>',
    "star": '<path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/>',
    "copy": '<rect x="8" y="8" width="13" height="13" rx="2"/><path d="M16 8V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h3"/>',
    "send": '<path d="M22 2 11 13"/><path d="M22 2 15 22l-4-9-9-4z"/>',
}


def ic(n):
    return ('<svg class="x-i" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
            'aria-hidden="true">%s</svg>' % ICONS[n])


def fmt(d):
    return "%s %d" % (d.strftime("%b"), d.day)


def has(tier, feat):
    return RANK[tier] >= RANK[FEATURES[feat]]


def qr_data_uri(url):
    try:
        import qrcode
        img = qrcode.make(url, box_size=10, border=2)
        b = io.BytesIO()
        img.save(b, format="PNG")
        return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()
    except Exception:
        return ""


def v3_profile(uid, share_dir):
    try:
        return json.load(open(os.path.join(share_dir, "live", "p3", "vip", "%s.json" % uid), encoding="utf-8"))
    except Exception:
        return {}


def profile_checks(j, member):
    intro = j.get("intro") or ""
    if isinstance(intro, dict):
        intro = " ".join(str(v) for v in intro.values())
    elif isinstance(intro, list):
        intro = " ".join(str(v) for v in intro)
    about = str(intro) + " " + str(member.get("about") or "")
    return [
        ("Photo or logo", bool(j.get("logo") or j.get("headshot") or member.get("logo")), "Add your logo or a great photo"),
        ("Business hours", bool(j.get("hours")), "Add your hours so neighbors know when to call"),
        ("Website link", bool(j.get("website")), "Link your website"),
        ("Social links", bool(j.get("instagram") or j.get("facebook") or j.get("linkedin")), "Link your Instagram or Facebook"),
        ("Description", len(re.sub(r"<[^>]+>", "", about).strip()) >= 80, "Tell neighbors what makes you different"),
    ]


def locked(feat, preview):
    t, title, benefit = LOCK_COPY[feat]
    return ('<div class="x-card x-lock"><div class="x-lock-prev" aria-hidden="true">%s</div><div class="x-lock-ov"><span class="x-lock-ic">%s</span>'
            '<b>%s</b><i>%s</i><a class="x-btn" href="%s" data-ga="dash_upgrade_click" data-product="%s">Upgrade to %s %s</a></div></div>'
            % (preview, ic("lock"), title, benefit, UPGRADE, feat, "Featured" if t == "f" else "VIP", ic("chev")))


def chart(a, days=90, sample=False):
    today = dt.date.today()
    start = today - dt.timedelta(days=days - 1)
    if sample:
        pts = [3 + i // 6 for i in range(days)]
    else:
        ev = {}
        for d in a.get("hp_days", []):
            ev[d] = ev.get(d, 0) + 1
        for it in a.get("items", []):
            if it.get("sample") or it.get("n_home"):
                continue
            ev[it["date"]] = ev.get(it["date"], 0) + 1
        run = sum(v for k, v in ev.items() if k < start.isoformat())
        pts = []
        for i in range(days):
            run += ev.get((start + dt.timedelta(days=i)).isoformat(), 0)
            pts.append(run)
        if pts[-1] - pts[0] < 3:
            return ""
    W, H, P = 640, 190, 8
    lo, hi = pts[0], max(pts[-1], pts[0] + 1)
    xy = [(P + (W - 2 * P) * i / (days - 1), H - P - (H - 2 * P) * (v - lo) / (hi - lo)) for i, v in enumerate(pts)]
    line = " ".join("%.1f,%.1f" % p for p in xy)
    area = "M%.1f,%d L" % (xy[0][0], H) + " L".join("%.1f,%.1f" % p for p in xy) + " L%.1f,%d Z" % (xy[-1][0], H)
    return ('<div class="x-card x-chart" id="x-chart"><div class="x-ch"><div><b>Your promotions keep adding up</b><i>Running total, last %d days</i></div>'
            '<span class="x-pill x-up">%s %d added</span></div>'
            '<svg class="x-svg" viewBox="0 0 %d %d" preserveAspectRatio="none" role="img" aria-label="Running total of promotions, rising">'
            '<defs><linearGradient id="xg" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#2f7fe0" stop-opacity=".28"/><stop offset="1" stop-color="#2f7fe0" stop-opacity="0"/></linearGradient></defs>'
            '<path d="%s" fill="url(#xg)"/><polyline points="%s" fill="none" stroke="#2f7fe0" stroke-width="3" stroke-linejoin="round" stroke-linecap="round" vector-effect="non-scaling-stroke"/></svg>'
            '<div class="x-axis"><span>%s</span><span>%s</span><span>Today</span></div>'
            '<p class="x-chart-n"><b>%s</b> promotions for you since you joined</p></div>'
            % (days, ic("spark"), pts[-1] - pts[0], W, H, area, line, fmt(start), fmt(start + dt.timedelta(days=days // 2)), "{:,}".format(pts[-1])))


def spotlight_card(a, others, sample=False):
    """Mini render of the homepage Local Business Spotlight with THIS business in the big slot."""
    big = a.get("banner") or a.get("logo") or ""
    cat = e(a.get("cat") or "")
    town = e(a.get("town") or "")
    also = "".join('<span class="x-sp-a"><img src="%s" alt="" width="40" height="40" loading="lazy" data-processed="true"><b>%s</b></span>'
                   % (e(o["img"]), e(o["name"])) for o in others[:3] if o.get("img"))
    return ('<div class="x-card x-spot" id="x-spot"><div class="x-ch"><div><b>You are on our homepage</b><i>The Spotlight rotates through our VIPs</i></div>'
            '<a class="x-btn x-btn-line" href="%s/" target="_blank" rel="noopener">See it live %s</a></div>'
            '<div class="x-sp"><div class="x-sp-h">Local Business Spotlight<span>Neighbors who support Three Village Local</span></div>'
            '<div class="x-sp-main"><div class="x-sp-img" style="background-image:url(\'%s\')"></div><div class="x-sp-t"><em>%s%s</em><b>%s</b>'
            '<span class="x-sp-cta">View profile</span></div></div><div class="x-sp-also"><i>Also featured</i>%s</div></div></div>'
            % (SITE, ic("ext"), e(big), cat, (" &middot; " + town) if town else "", e(a.get("short") or "Your business"), also))


def form(fid, title, sub, fields, btn):
    f = "".join(fields)
    return ('<form class="x-form" data-x-form="%s" novalidate><p class="x-form-h"><b>%s</b><i>%s</i></p>%s'
            '<button type="submit" class="x-btn">%s %s</button><p class="x-form-ok" hidden></p></form>' % (fid, title, sub, f, btn, ic("send")))


def inp(name, label, kind="text", ph="", req=False):
    if kind == "textarea":
        return '<label><span>%s</span><textarea name="%s" rows="3" placeholder="%s"%s></textarea></label>' % (label, name, e(ph), " required" if req else "")
    if kind == "file":
        return '<label><span>%s</span><input type="file" name="%s" accept="image/*"></label>' % (label, name)
    if kind.startswith("select:"):
        opts = "".join('<option>%s</option>' % o for o in kind[7:].split("|"))
        return '<label><span>%s</span><select name="%s">%s</select></label>' % (label, name, opts)
    return '<label><span>%s</span><input type="%s" name="%s" placeholder="%s"%s></label>' % (label, kind, name, e(ph), " required" if req else "")


def actions(tier):
    tabs = [("event", "cal", "Submit an event"), ("special", "tag", "Submit a special"), ("video", "video", "Request a promo video"),
            ("social_req", "insta", "Request a social post"), ("listing", "edit", "Update my listing")]
    T, P = [], []
    for i, (k, icn, label) in enumerate(tabs):
        T.append('<button type="button" role="tab" data-x-tab="%s"%s>%s<span>%s</span>%s</button>' % (
            k, ' class="on" aria-selected="true"' if i == 0 else ' aria-selected="false"', ic(icn), label,
            "" if k == "listing" or has(tier, k) else '<em class="x-lk">%s</em>' % ic("lock")))
        if k == "listing":
            body = ('<div class="x-form"><p class="x-form-h"><b>Update your listing</b><i>Change hours, photos, services or contact info any time.</i></p>'
                    '<div class="x-links"><a class="x-btn" href="%s">Edit my listing %s</a><a class="x-btn x-btn-line" href="mailto:hello@threevillagelocal.com?subject=Listing%%20update">Email us the changes</a></div></div>'
                    % (LOGIN_EDIT, ic("chev")))
        elif not has(tier, k):
            t, title, benefit = LOCK_COPY[k]
            body = ('<div class="x-form x-form-lock"><span class="x-lock-ic">%s</span><b>%s</b><i>%s</i><a class="x-btn" href="%s">Upgrade to Featured %s</a></div>'
                    % (ic("lock"), title, benefit, UPGRADE, ic("chev")))
        elif k == "event":
            body = form("event", "Submit an event", "We review every event and add it to our calendar and weekend picks.",
                        [inp("name", "Event name", req=True), '<div class="x-2">' + inp("date", "Date", "date", req=True) + inp("time", "Start time", "time") + '</div>',
                         inp("place", "Place", ph="Venue or address"), inp("details", "Description", "textarea"),
                         '<div class="x-2">' + inp("photo", "Photo", "file") + inp("link", "Link", "url", "Tickets or info page") + '</div>'], "Send event")
        elif k == "special":
            body = form("special", "Submit a special", "Deals, new menus, seasonal offers. We feature them for neighbors.",
                        [inp("title", "Title", req=True), inp("details", "Details", "textarea"),
                         '<div class="x-2">' + inp("start", "Starts", "date") + inp("end", "Ends", "date") + '</div>',
                         '<div class="x-2">' + inp("photo", "Photo", "file") + inp("link", "Link", "url") + '</div>'], "Send special")
        elif k == "video":
            body = form("video", "Request a promo video", "Tell us what you have in mind. We will reply with options.",
                        [inp("want", "What do you want the video to show?", "textarea", req=True),
                         '<div class="x-2">' + inp("style", "Style", "select:Animated with voiceover|Filmed on location|Interview style|Not sure yet") + inp("dates", "Preferred dates", ph="Any week that works") + '</div>',
                         inp("notes", "Anything else", "textarea")], "Send request")
        else:
            body = form("social", "Request a social post", "News, a milestone or something new? We will put it on our Facebook and Instagram.",
                        [inp("what", "What should we post about?", "textarea", req=True), '<div class="x-2">' + inp("photo", "Photo", "file") + inp("when", "Best timing", ph="This week, a date, any time") + '</div>'], "Send request")
        P.append('<div class="x-pane" data-x-pane="%s"%s>%s</div>' % (k, "" if i == 0 else " hidden", body))
    return ('<div class="x-card x-act" id="x-act"><div class="x-ch"><div><b>Action center</b><i>Send it to us and we will get it out there</i></div></div>'
            '<div class="x-tabs" role="tablist">%s</div>%s</div>' % ("".join(T), "".join(P)))


def quick(a, j):
    prof = a.get("profile") or ""
    qr = qr_data_uri(prof) if prof else ""
    rv = (j.get("reviews") or {}).get("url") if isinstance(j.get("reviews"), dict) else ""
    sh = quote(prof, safe="")
    items = []
    if prof:
        items.append('<div class="x-q"><span class="x-kic">%s</span><div><b>Share your profile</b><i>Send neighbors straight to you</i>'
                     '<div class="x-q-b"><button type="button" class="x-chipb" data-x-copy="%s">%s Copy link</button>'
                     '<a class="x-chipb" href="https://www.facebook.com/sharer/sharer.php?u=%s" target="_blank" rel="noopener">Facebook</a>'
                     '<a class="x-chipb" href="https://www.linkedin.com/sharing/share-offsite/?url=%s" target="_blank" rel="noopener">LinkedIn</a>'
                     '<a class="x-chipb" href="mailto:?subject=%s&amp;body=%s">Email</a></div></div></div>'
                     % (ic("share"), e(prof), ic("copy"), sh, sh, quote(a.get("short", "")), sh))
    if qr:
        items.append('<div class="x-q"><img class="x-qr" src="%s" alt="QR code for your profile" width="72" height="72"><div><b>Your QR code</b>'
                     '<i>Print it on cards, flyers and your counter</i><div class="x-q-b"><a class="x-chipb" href="%s" download="3vl-qr-%s.png">Download</a></div></div></div>'
                     % (qr, qr, e(a.get("uid", ""))))
    if rv:
        items.append('<div class="x-q"><span class="x-kic">%s</span><div><b>Your review link</b><i>Ask happy customers for a quick Google review</i>'
                     '<div class="x-q-b"><button type="button" class="x-chipb" data-x-copy="%s">%s Copy link</button></div></div></div>' % (ic("star"), e(rv), ic("copy")))
    items.append('<div class="x-q"><span class="x-kic">%s</span><div><b>Our free mobile app</b><i>Local news, events and your listing in one place</i>'
                 '<div class="x-q-b"><a class="x-chipb" href="%s/app" target="_blank" rel="noopener">Get the free mobile app</a></div></div></div>' % (ic("phone"), SITE))
    return '<div class="x-card" id="x-quick"><div class="x-ch"><div><b>Quick links</b><i>Tools to help neighbors find you</i></div></div><div class="x-qs">%s</div></div>' % "".join(items)


DIG = "https://3vldigital.com"
UPSELL = [   # 3VL Digital card, never locked, one shown per visit (dash2.js rotates). No prices.
    ("dashboards", "Like this dashboard? We build custom ones for your business.",
     "Leads, jobs, team and money on one screen, with logins for you, your managers and your staff.",
     "See custom dashboards", "/dashboards", "/assets/img/shots/dash-contractor-640.webp"),
    ("chatbots", "Your website could answer customers at 10 PM.",
     "An AI chatbot trained on your business answers every question, day or night, and texts you the lead.",
     "Try our AI chatbot", "/chatbots", "/assets/img/shots/chat-ridge-560.webp"),
    ("websites", "A website that works as hard as you do.",
     "Fast, beautiful websites built from scratch to sell and to be recommended by Google and AI.",
     "See AI-ready websites", "/websites", "/assets/img/shots/chris-640.webp"),
]


def upsell(company, first, sample_done=False, tier="v", full=False):
    """3VL Digital slot. Card 1 = FREE working dashboard sample (owner 11/15/2026, overrides the no-free-samples rule for this card only):
    one click, no form. After a request (logged nightly in sample_requests.json, or localStorage right away) the slot rotates to the others."""
    cards = []
    comp = e(company) if company else '<span data-md-name>your business</span>'
    if tier == "b":   # rollout: free members get a teaser, the sample is for paying members first
        cards.append('<div class="x-ups" data-ups="dashboards"><div class="x-ups-t"><span class="x-ups-k">3VL Digital &middot; Coming soon</span>'
                     '<b>Custom dashboards for local businesses are coming to members.</b>'
                     '<i>Upgrade to Featured to get a free working sample built for your business.</i>'
                     '<a class="x-btn x-ups-b" href="%s" data-ga="dash_upgrade_click" data-product="sample_teaser">Upgrade to Featured %s</a></div>'
                     '<div class="x-ups-v"><img src="%s/assets/img/shots/dash-contractor-640.webp" alt="" width="320" height="200" loading="lazy" decoding="async" data-processed="true"></div></div>'
                     % (UPGRADE, ic("chev"), DIG))
    elif not sample_done and full:   # weekly cap of 5 reached: one-click waitlist (alerts the owner, tagged waitlist)
        cards.append('<div class="x-ups" data-ups="dashboards"><div class="x-ups-t"><span class="x-ups-k">3VL Digital &middot; Custom dashboards</span>'
                     '<b>Our free sample spots are full this week.</b><i>Join the list and we will reach out to %s first.</i>'
                     '<button type="button" class="x-btn x-ups-b" data-sample data-kind="dashboard_sample_waitlist" data-first="%s" data-ga="dash_sample_request" data-product="waitlist">Join the list %s</button></div>'
                     '<div class="x-ups-v"><img src="%s/assets/img/shots/dash-contractor-640.webp" alt="" width="320" height="200" loading="lazy" decoding="async" data-processed="true"></div></div>'
                     % (comp, e(first or ""), ic("chev"), DIG))
    elif not sample_done:
        cards.append('<div class="x-ups" data-ups="dashboards"><div class="x-ups-t"><span class="x-ups-k">3VL Digital &middot; Custom dashboards</span>'
                     '<b>Want to see one built for %s? We will make you a free working sample.</b>'
                     '<i>Leads, jobs, team and money on one screen, with logins for you, your managers and your staff.</i>'
                     '<button type="button" class="x-btn x-ups-b" data-sample data-first="%s" data-ga="dash_sample_request" data-product="dashboards">Request my free sample %s</button>'
                     '<a class="x-ups-more" href="%s/dashboards?utm_source=3vl&amp;utm_medium=member-dashboard&amp;utm_campaign=dash-upsell" target="_blank" rel="noopener" '
                     'data-ga="dash_upsell_click" data-product="dashboards_learn">See custom dashboards</a></div>'
                     '<div class="x-ups-v"><img src="%s/assets/img/shots/dash-contractor-640.webp" alt="" width="320" height="200" loading="lazy" decoding="async" data-processed="true"></div></div>'
                     % (comp, e(first or ""), ic("chev"), DIG, DIG))
    for k, h, sub, btn, path, img in UPSELL[1:]:
        url = "%s%s?utm_source=3vl&utm_medium=member-dashboard&utm_campaign=%s-upsell" % (DIG, path, k[:-1])
        cards.append('<div class="x-ups" data-ups="%s" hidden><div class="x-ups-t"><span class="x-ups-k">3VL Digital</span><b>%s</b><i>%s</i>'
                     '<a class="x-btn x-ups-b" href="%s" target="_blank" rel="noopener" data-ga="dash_upsell_click" data-product="%s">%s %s</a></div>'
                     '<div class="x-ups-v"><img src="%s%s" alt="" width="320" height="200" loading="lazy" decoding="async" data-processed="true"></div></div>'
                     % (k, h, sub, e(url), k, btn, ic("chev"), DIG, img))
    cards.append('<div class="x-ups x-ups-tip" data-ups="tip" hidden><div class="x-ups-t"><span class="x-ups-k">Tip</span><b>Got something coming up?</b>'
                 '<i>Send us your next event or special and we will put it in front of neighbors.</i>'
                 '<a class="x-btn x-ups-b" href="#x-act" data-ga="dash_tip_click" data-product="submit_event">Submit it now %s</a></div></div>' % ic("chev"))
    return '<div class="x-card x-upsell" id="x-ups">%s</div>' % "".join(cards)


def meet_digital():
    u = "utm_source=3vl&amp;utm_medium=member-dashboard&amp;utm_campaign=meet-3vl-digital"
    return ('<div class="x-card x-meet"><img class="x-meet-logo" src="%s/assets/img/brand/logo-full.webp" alt="3VL Digital" width="160" height="40" loading="lazy" decoding="async" data-processed="true">'
            '<p><b>Meet 3VL Digital.</b> From the team behind Three Village Local: AI chatbots, AI-ready websites and custom dashboards for local businesses.</p>'
            '<a class="x-btn" href="%s/?%s" target="_blank" rel="noopener" data-ga="dash_upsell_click" data-product="meet_3vl_digital">Visit 3vldigital.com %s</a>'
            '<div class="x-meet-f"><span>Follow</span>'
            '<a href="https://www.instagram.com/3vl.digital/" target="_blank" rel="noopener" data-ga="dash_follow_click" data-product="instagram">Instagram</a>'
            '<a href="https://www.facebook.com/profile.php?id=1426154700579694" target="_blank" rel="noopener" data-ga="dash_follow_click" data-product="facebook">Facebook</a>'
            '<a href="https://www.linkedin.com/company/3vldigital" target="_blank" rel="noopener" data-ga="dash_follow_click" data-product="linkedin">LinkedIn</a></div></div>'
            % (DIG, DIG, u, ic("chev")))


def page(a, ctx):
    """a: activity dict (build.py) or a minimal dict for Basic members. ctx: tier, w0, net, banner_views, reach, share_dir, member, raw, logo3vl, others."""
    tier = ctx["tier"]
    uid, w0 = a.get("uid", ""), ctx["w0"]
    j = v3_profile(uid, ctx["share_dir"]) if uid else {}
    checks = profile_checks(j, ctx.get("member") or {})
    first = (j.get("first") or "").strip() or a.get("short") or ""
    real = [it for it in a.get("items", []) if not it.get("sample")]
    hp30 = [d for d in a.get("hp_days", []) if d >= w0]
    soc30 = [it for it in real if it["ch"] == "social" and it["date"] >= w0]
    em30 = [it for it in real if it["ch"] == "email" and it["date"] >= w0]
    bview = ctx["banner_views"] if (has(tier, "banner") and a.get("has_banner_ad") and ctx["banner_views"] >= 1000) else 0
    reach = ctx.get("reach") or 0
    lifetime = a.get("lifetime") or 0

    bits = []
    if bview:
        bits.append("your banner ad on every page of our site")
    if hp30 and has(tier, "spotlight"):
        bits.append("%d day%s in our homepage spotlight" % (len(hp30), "" if len(hp30) == 1 else "s"))
    if soc30:
        bits.append("%d social post%s about you" % (len(soc30), "" if len(soc30) == 1 else "s"))
    if em30:
        bits.append("a feature in Three Village Weekly")
    if bits:
        lead = "In the last 30 days we put %s in front of neighbors%s: " % (e(a.get("short")), (" up to %s times" % "{:,}".format(reach)) if reach else "")
        summary = lead + (", ".join(bits[:-1]) + " and " + bits[-1] if len(bits) > 1 else bits[0]) + "."
    elif tier == "b":
        summary = "You are listed on Three Village Local, where neighbors find local businesses. Here is how to get seen more."
    else:
        summary = "Your next spotlight is on the way. Have news, a special or an event? Send it to us below and we will promote it."

    tiles = []
    if bview:
        tiles.append(("banner", "up to " + "{:,}".format(bview), "Banner ad views this month", "#x-banner"))
    if hp30 and has(tier, "spotlight"):
        tiles.append(("home", str(len(hp30)), "Days in our homepage spotlight", "#x-spot"))
    if (soc30 or em30) and has(tier, "timeline"):
        tiles.append(("insta", str(len(soc30) + len(em30)), "Social posts and email features", "#x-promo"))
    if lifetime >= 3 and has(tier, "timeline"):
        tiles.append(("megaphone", "{:,}".format(lifetime), "Promotions since you joined", "#x-promo"))
    net = ctx.get("net") or {}
    if len(tiles) < 2 and int(net.get("views") or 0) >= 1000:
        tiles.append(("globe", "{:,}+".format(int(net["views"]) // 1000 * 1000), "Page views on Three Village Local this month", "#x-net"))
    if len(tiles) < 2:
        tiles.append(("share", "100,000+", "Facebook and Instagram views our posts reach monthly", "#x-net"))
    kpi = "".join('<a class="x-kpi" href="%s"><span class="x-kic">%s</span><b>%s</b><i>%s</i></a>' % (h, ic(i), v, t) for i, v, t, h in tiles)

    # banner + spotlight (VIP) or locked teasers
    if bview:
        pic = ('<img src="%s" alt="Your banner ad" width="200" height="167" loading="lazy" decoding="async" data-processed="true">' % e(ctx["raw"] + a["banner_img"])) if a.get("banner_img") else ""
        banner = ('<div class="x-card x-ban" id="x-banner">%s<div><div class="x-ch"><div><b>Your banner ad</b><i>Rotating on every page of threevillagelocal.com</i></div></div>'
                  '<p class="x-big">%s</p><p class="x-sub">times your banner may have been seen this month</p></div></div>' % (pic, "{:,}+".format(bview)))
    elif not has(tier, "banner"):
        banner = locked("banner", '<div class="x-ban-fake"><span></span><div><b>48,000+</b><i>times your banner may have been seen</i></div></div>')
    else:
        banner = ""
    if has(tier, "spotlight") and hp30:
        spot = spotlight_card(a, ctx.get("others") or [])
    elif not has(tier, "spotlight"):
        spot = locked("spotlight", spotlight_card({"short": "Your business here", "cat": "Your category", "banner": "", "logo": ""}, ctx.get("others") or []))
    else:
        spot = ""
    ch = chart(a) if has(tier, "chart") else locked("chart", chart({}, sample=True))

    def row(it):
        d = dt.date.fromisoformat(it["date"])
        th = ('<img src="%s" alt="" width="56" height="56" loading="lazy" decoding="async" data-processed="true" onerror="this.style.visibility=&#39;hidden&#39;">' % e(it["thumb"])) if it.get("thumb") else '<span class="x-tic">%s</span>' % ic(it["icon"] if it["icon"] in ICONS else "dot")
        link = (' <a href="%s" target="_blank" rel="noopener">See it %s</a>' % (e(it["url"]), ic("ext"))) if it.get("url") else ""
        return '<li data-f="%s">%s<div><b>%s</b><i>%s%s</i></div><time datetime="%s">%s</time></li>' % (it["ch"], th, e(it["title"]), e(it["note"]), link, it["date"], fmt(d))
    if has(tier, "timeline") and real:
        chans = sorted({it["ch"] for it in real})
        chips = ('<div class="x-chips" role="group" aria-label="Filter"><button type="button" class="on" data-f="all">All</button>' + "".join(
            '<button type="button" data-f="%s">%s</button>' % (c, l) for c, l in (("web", "Website"), ("social", "Social"), ("email", "Email")) if c in chans) + "</div>") if len(chans) > 1 else ""
        life = ('<p class="x-life"><b>%d promotions</b> for you since you joined</p>' % lifetime) if lifetime >= 3 else ""
        tl = '<div class="x-card x-tl" id="x-promo"><div class="x-ch"><div><b>What we did for you</b><i>Newest first</i></div>%s</div>%s<ol>%s</ol></div>' % (chips, life, "".join(row(it) for it in real))
    elif not has(tier, "timeline"):
        demo = [{"date": dt.date.today().isoformat(), "ch": "web", "icon": "home", "title": "On our homepage, 7 days", "note": "Your card in the Local Business Spotlight"},
                {"date": dt.date.today().isoformat(), "ch": "social", "icon": "insta", "title": "Spotlight on Instagram and Facebook", "note": "Tagged with a collab invite"},
                {"date": dt.date.today().isoformat(), "ch": "email", "icon": "mail", "title": "Featured in Three Village Weekly", "note": "Your photo and story in our weekly email"}]
        tl = locked("timeline", '<div class="x-tl"><ol>%s</ol></div>' % "".join(row(it) for it in demo))
    else:
        tl = ""

    up = [u for u in (a.get("upcoming") or []) if not u.get("sample")]
    upc = "".join('<li><span class="x-date"><b>%s</b><i>%d</i></span><div><b>%s</b><i>%s</i></div></li>' % (
        dt.date.fromisoformat(u["date"]).strftime("%b"), dt.date.fromisoformat(u["date"]).day, e(u["title"]), e(u["note"])) for u in up[:4])
    if not upc:
        upc = '<li><span class="x-date"><b>%s</b><i>%s</i></span><div><b>More on the way</b><i>Send us your news, specials and events in the Action center and we will promote them.</i></div></li>' % (dt.date.today().strftime("%b"), ic("dot"))

    done = sum(1 for _, ok, _ in checks if ok)
    pct = round(done * 100 / len(checks))
    pl = "".join('<li class="%s"><span class="x-ck">%s</span><div><b>%s</b>%s</div>%s</li>' % (
        "ok" if ok else "todo", ic("check") if ok else ic("dot"), t, "" if ok else '<i>%s</i>' % tip,
        "" if ok else '<a class="x-fix" href="%s">Fix this %s</a>' % (LOGIN_EDIT, ic("chev"))) for t, ok, tip in checks)
    profile = ('<div class="x-card x-prof" id="x-profile"><div class="x-ch"><div><b>Profile strength</b><i>%s</i></div>'
               '<span class="x-ring" style="--p:%d"><b>%d%%</b></span></div><ul>%s</ul></div>'
               % ("Your profile is complete. Nice work." if done == len(checks) else "A complete profile gets more calls", pct, pct, pl)) if uid else ""

    netc = ""
    nl = []
    if int(net.get("views") or 0) >= 1000:
        nl.append(("globe", "{:,}+".format(int(net["views"]) // 1000 * 1000), "Website page views this month"))
    if int(net.get("social") or 0) >= 1000:
        nl.append(("share", "{:,}+".format(int(net["social"]) // 1000 * 1000), "Facebook and Instagram views, last 28 days"))
    if int(net.get("subs") or 0) >= 100:
        nl.append(("mail", "{:,}".format(int(net["subs"])), "Neighbors who get Three Village Weekly"))
    if nl:
        netc = ('<div class="x-card" id="x-net"><div class="x-ch"><div><b>Three Village Local right now</b><i>Updated nightly</i></div></div><div class="x-netg">%s</div></div>'
                % "".join('<div><span class="x-kic">%s</span><b>%s</b><i>%s</i></div>' % (ic(x[0]), x[1], x[2]) for x in nl))

    grow = [("video", "Promo video", "We will reply with options", "#x-act"), ("bot", "AI chatbot", "Answers your customers 24/7", "/ai-assistant"),
            ("globe", "AI website", "Built to be found on Google and AI", "/websites"), ("spark", "AI visibility report", "See how AI tools describe you", "/free-ai-report"),
            ("camera", "Drone photos and video", "Aerial photos and video of your business", "/services")]
    if RANK[tier] < RANK["v"]:
        grow.insert(0, ("star", "Upgrade to VIP" if tier == "f" else "Upgrade your listing", "Banner ad, homepage spotlight and more", UPGRADE))
    gl = "".join('<a class="x-grow-b" data-ga="dash_upsell_click" data-product="%s" href="%s"><span class="x-kic">%s</span><div><b>%s</b><i>%s</i></div>%s</a>' % (
        re.sub(r"[^a-z]+", "_", t.lower()).strip("_"), (h if h.startswith(("#", "/login")) else SITE + h), ic(i), t, d, ic("chev")) for i, t, d, h in grow)
    news = [("Just launched", "Homepage trivia: neighbors play every Monday, with local business prizes."),
            ("Live now", "Our Thanksgiving guide is up. Send us your holiday hours and specials and we will add them."),
            ("New", "AI chatbots by 3VL Digital: answer customers 24/7 on your own website.")]
    nw = "".join('<li><em>%s</em><span>%s</span></li>' % x for x in news)

    nav = [("grid", "Overview", "#x-top"), ("megaphone", "Your promotions", "#x-promo" if (has(tier, "timeline") and real) else "#x-chart"),
           ("banner", "Banner", "#x-banner"), ("home", "Spotlight", "#x-spot"), ("send", "Action center", "#x-act"),
           ("user", "Profile", "#x-profile" if uid else "#x-quick"), ("rocket", "Grow", "#x-grow")]
    side = "".join('<a href="%s"%s>%s<span>%s</span>%s</a>' % (h, ' class="on"' if i == 0 else "", ic(n), t,
                   '<em class="x-lk">%s</em>' % ic("lock") if (t == "Banner" and not has(tier, "banner")) or (t == "Spotlight" and not has(tier, "spotlight")) else "")
                   for i, (n, t, h) in enumerate(nav) if not ((t == "Banner" and has(tier, "banner") and not bview) or (t == "Spotlight" and has(tier, "spotlight") and not hp30)))

    logo = ('<img class="x-blogo" src="%s" alt="%s logo" width="48" height="48" decoding="async" data-processed="true">' % (e(a["logo"]), e(a.get("short")))) if a.get("logo") else ""
    name_html = e(a.get("short")) if uid else '<span data-md-name>Your business</span>'
    hello = e(first) if uid else '<span data-md-name>neighbor</span>'
    preview_note = '<p class="x-prev-note">Preview: forms are switched off.</p>' if ctx.get("preview") else ""
    body = ('<div class="mdx" id="mdx" data-tier="%s" data-uid="%s"%s>'
            '<aside class="x-side"><div class="x-brand"><img src="%s" alt="Three Village Local" width="132" height="45" data-processed="true"></div>'
            '<nav class="x-nav" aria-label="Dashboard sections">%s</nav><div class="x-side-foot"><span class="x-tierb x-t-%s">%s</span><a href="%s">Sign in to edit</a></div></aside>'
            '<main class="x-main"><div class="x-top" id="x-top">%s<div class="x-who"><b>%s</b><i>%s%s</i></div>'
            '%s</div>'
            '<section class="x-hero"><p class="x-k"><span data-x-greet>Hello</span>, %s</p><h1>%s</h1><p class="x-sum">%s</p></section>'
            '<div class="x-kpis">%s</div>'
            '<div class="x-two">%s%s</div>'
            '%s'
            '<div class="x-grid"><div class="x-col">%s%s</div><div class="x-col">'
            '<div class="x-card"><div class="x-ch"><div><b>Coming up for you</b></div></div><ul class="x-upc">%s</ul></div>%s%s'
            '<div class="x-card"><div class="x-ch"><div><b>What&#39;s new at 3VL</b></div></div><ul class="x-news">%s</ul></div>' + meet_digital() + '</div></div>'
            '%s%s'
            '<div class="x-card" id="x-grow"><div class="x-ch"><div><b>Grow with us</b><i>Services from Three Village Local and 3VL Digital</i></div></div><div class="x-grow">%s</div></div>'
            '<p class="x-foot">Questions or something to promote? Email <a href="mailto:hello@threevillagelocal.com">hello@threevillagelocal.com</a>. Updated nightly.</p>%s'
            '</main></div>') % (
        tier, uid, ' data-preview="1"' if ctx.get("preview") else "", ctx["logo3vl"], side, tier, TIER_NAME[tier], LOGIN,
        logo, name_html, TIER_NAME[tier], (" &middot; " + e(a.get("cat"))) if a.get("cat") else "",
        ('<a class="x-btn x-btn-line" href="%s" target="_blank" rel="noopener">View your profile %s</a>' % (e(a["profile"]), ic("ext"))) if a.get("profile") else
        '<a class="x-btn x-btn-line" href="%s">Edit your listing %s</a>' % (LOGIN_EDIT, ic("chev")),
        hello, "Here is everything Three Village Local is doing for you" if RANK[tier] else "Welcome to your member dashboard", summary,
        kpi, banner, spot, ch, actions(tier), tl, upc, profile, netc, nw, quick(a, j), upsell(a.get("short") or "", first if uid else "", ctx.get("sample_done", False), tier, ctx.get("samples_full", False)), gl, preview_note)
    return body


SHELL = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex,nofollow"><meta name="referrer" content="no-referrer"><title>%s | Member Dashboard</title>
<meta name="theme-color" content="#0c1a33"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent"><meta name="apple-mobile-web-app-title" content="3VL">
<link rel="manifest" href="%s"><link rel="apple-touch-icon" sizes="180x180" href="%s">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="%s"></head><body class="x-page">%s<script src="%s" defer></script></body></html>'''


def manifest(token, icon_base):
    """Per-member web app manifest: opens straight to their private dashboard, installable on iPhone and Android."""
    return json.dumps({"name": "3VL Dashboard", "short_name": "3VL", "id": "./%s.html" % token, "start_url": "./%s.html" % token, "scope": "./",
                       "display": "standalone", "background_color": "#f4f5f7", "theme_color": "#0c1a33",
                       "icons": [{"src": icon_base + "icon-192.png", "sizes": "192x192", "type": "image/png"},
                                 {"src": icon_base + "icon-512.png", "sizes": "512x512", "type": "image/png"},
                                 {"src": icon_base + "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]}, indent=1)


INSTALL = ('<div class="x-inst" id="x-inst" hidden role="dialog" aria-label="Add your dashboard to your home screen"><img src="%s" alt="" width="44" height="44">'
           '<div class="x-inst-t"><b>Add your dashboard to your home screen</b><i class="x-inst-ios">Tap <span class="x-shr" aria-label="Share">'
           '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
           '<path d="M12 3v12"/><path d="m7 8 5-5 5 5"/><path d="M5 12v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-7"/></svg></span> Share, then <b>Add to Home Screen</b></i>'
           '<i class="x-inst-and">One tap, no app store. It opens like an app.</i></div>'
           '<button type="button" class="x-btn x-inst-go">Install</button><button type="button" class="x-inst-x" aria-label="Dismiss">&times;</button></div>')
