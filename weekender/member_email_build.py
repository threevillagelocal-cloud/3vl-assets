"""Member update email (owner 10/2/2026): an insider email to each member business, one at a time, about the upgrades:
the redesign, smart search (with a search that brings up THEIR business), the VIP banner spot (their own banner, or a sample
made for them), and the Smart Publisher perk for Getting Noticed and VIP. Not a "what's happening" newsletter.

    python weekender/member_email_build.py <name> <private dir> [id ...]
reads  <private dir>/recipients.json (addresses: PRIVATE, never in this repo) and search_picks.json,
       pictures in 3vl-share/email/<name>/ (member_shots.py, member_visuals.py)
writes <private dir>/out/<id>.html + <id>.subject.txt   (nothing is sent from here)"""
import html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.dirname(HERE)
SHARE = os.path.join(os.path.dirname(ASSETS), "3vl-share")
sys.path.insert(0, HERE)
from email_build import esc, btn, FONT, NAVY, NAVY2, GOLD, INK, MUT, LINE, BG, MAILING_ADDRESS   # same look as the weekly email

SITE = "https://www.threevillagelocal.com"
VIP, GN = {"1", "8"}, {"2"}


def p(t, size=16, color=INK, mb=14, extra=""):
    return '<p style="margin:0 0 %dpx;font:%dpx/1.6 %s;color:%s;%s">%s</p>' % (mb, size, FONT, color, extra, t)


def kicker(t, color="#b36b00"):
    return '<p style="margin:0 0 6px;font:bold 12px %s;letter-spacing:2px;text-transform:uppercase;color:%s">%s</p>' % (FONT, color, t)


def h2(t, color=NAVY):
    return '<h2 style="margin:0 0 12px;font:bold 25px/1.25 %s;color:%s">%s</h2>' % (FONT, color, t)


def pic(src, alt, href, radius=14):
    return ('<a href="%s"><img src="%s" width="544" alt="%s" style="display:block;width:100%%;height:auto;border-radius:%dpx;border:1px solid %s"></a>'
            % (esc(href), src, esc(alt), radius, LINE))


def block(inner, pad="34px 28px 6px"):
    return '<tr><td style="padding:%s">%s</td></tr>' % (pad, inner)


def short_name(n):
    """'Team Passamenti at Better Homes and Gardens Real Estate Realty Connect' -> 'Team Passamenti' (agent/brokerage style names)."""
    n = (n or "").strip()
    for sep in (": ", " at ", " - ", " | ", ", "):
        if sep in n and len(n) > 34:
            head = n.split(sep)[0].strip()
            if len(head.split()) >= 2:   # never cut down to one word ("Summer", "Prudential")
                return head
    return n


def build(r, pick, has_banner, base, has_search):
    co = esc(short_name(r["company"]) or "your business")
    first = esc(r["first"]) if r["first"] and r["first"].lower() not in ("info", "admin", "office") else ""
    plan = r["plan"]
    rows = []
    # masthead
    rows.append('<tr><td style="background:%s;padding:20px 28px"><table role="presentation" width="100%%" cellpadding="0" cellspacing="0" border="0"><tr>'
                '<td width="56"><img src="%slogo.png" width="48" height="48" alt="Three Village Local" style="display:block;border:0"></td>'
                '<td style="padding-left:12px"><p style="margin:0;font:bold 20px %s;color:#fff">Three Village <span style="color:%s">Local</span></p>'
                '<p style="margin:2px 0 0;font:13px %s;color:#c9d6e3">Member update &middot; October 2026</p></td></tr></table></td></tr>'
                % (NAVY, base.replace("member-2026-10/", "2026-10-02/"), FONT, GOLD, FONT))
    # intro
    hi = ("Hi %s," % first) if first else "Hello,"
    rows.append('<tr><td style="background:%s;padding:30px 28px 8px">%s'
                '<h1 style="margin:0 0 14px;font:bold 31px/1.15 %s;color:#fff">The new Three Village Local website and app are here</h1>%s%s</td></tr>'
                % (NAVY2, kicker("Inside look for " + co, GOLD), FONT,
                   p(hi, 16, "#dbe4ee", 10),
                   p("We rebuilt the Three Village Local website and app from the ground up: a premium new design on every page, a much smarter "
                     "search, and new ways to put your business in front of neighbors. You are one of the businesses that make Three Village Local "
                     "what it is, so here is a first look at what it means for <b style=\"color:#fff\">%s</b>." % co, 16, "#dbe4ee", 18)))
    rows.append('<tr><td style="background:%s;padding:0 28px 30px"><a href="%s/"><img src="%shero.jpg" width="544" alt="The new Three Village Local on a computer and a phone" '
                'style="display:block;width:100%%;height:auto;border-radius:14px;border:0"></a>'
                '<p style="margin:14px 0 0;font:14px/1.5 %s;color:#aebdcc">Faster pages, a cleaner look, and it works beautifully on phones.</p></td></tr>'
                % (NAVY2, SITE, base, FONT))
    # smart search
    if has_search:
        q, rank = pick["q"], pick["rank"]
        byname = q.lower() in (r["company"] or "").lower() or q.lower() in pick.get("n", "").lower()
        where = "came up first" if rank == 0 else "came up in the top 3"
        cap = ("We searched &ldquo;%s&rdquo; and your listing came right up. Neighbors find you by name and by what you do." % esc(q)) if byname else \
              ("We searched &ldquo;%s&rdquo; and <b>%s</b> %s." % (esc(q), co, where))
        rows.append(block(kicker("New &middot; Smart search") + h2("Neighbors find you by what they need")
                          + p("Neighbors no longer have to know which category you are in. They type what they need in plain words, and smart search "
                              "brings up the right local business, with your logo, town and plan. We tried it for you:")
                          + pic(base + "s-%s.jpg" % r["id"], "Smart search on Three Village Local", SITE + "/")
                          + p(cap, 15, NAVY, 0, "padding-top:12px")))
    # banner spot
    if plan in VIP and has_banner:
        btxt = (kicker("Your VIP banner") + h2("Your banner, live in the VIP spot")
                + p("Here is your banner running in the VIP spot on our business directory. It rotates across the website, the homepage and "
                    "the app, with one-tap Call and View buttons so neighbors can reach you right away."))
        cta = ""
    elif plan in VIP:
        btxt = (kicker("Your VIP banner") + h2("Your banner belongs right here")
                + p("Your VIP plan includes a banner in this spot, across the website, the homepage and the app. Here is a sample we made for "
                    "%s. Reply to this email with your logo and a photo and we will design the real one for you." % co))
        cta = ""
    else:
        btxt = (kicker("VIP banner ads") + h2("Picture %s here" % co)
                + p("This is a sample we made for %s, shown in the VIP spot on our business directory. VIP members get a custom banner that "
                    "rotates across the website, the homepage and the app, with one-tap Call and View buttons." % co))
        cta = '<div style="padding-top:16px">%s</div>' % btn(SITE + "/join", "See the VIP plan &rarr;", NAVY, "#fff")
    # bz- = close crop around the banner spot only (no neighboring banner, so never a competitor in someone's email)
    if os.path.exists(os.path.join(SHARE, "email", base.rstrip("/").split("/")[-1], "bz-%s.jpg" % r["id"])):
        rows.append(block(btxt + pic(base + "bz-%s.jpg" % r["id"], "VIP banner spot on Three Village Local", SITE + "/categories") + cta))
    # Smart Publisher (owner 10/3/2026: only send once it is live; "no coming soon")
    if plan in VIP:
        perk = "<b>Included in your VIP plan:</b> a page every two weeks, plus promotion on our social media. It is ready now."
        pcta = '<div style="padding-top:4px">%s</div>' % btn(SITE + "/smart-publisher", "Open Smart Publisher &rarr;")
    elif plan in GN:
        perk = "<b>Included in your Getting Noticed plan:</b> 1 page a month. It is ready now."
        pcta = '<div style="padding-top:4px">%s</div>' % btn(SITE + "/smart-publisher", "Open Smart Publisher &rarr;")
    else:
        perk = "<b>Included with Getting Noticed (1 page a month) and VIP (one every two weeks).</b> Upgrade and you can use it today."
        pcta = ('<div style="padding-top:4px">%s</div><p style="margin:12px 0 0;font:14px %s"><a href="%s/join" style="color:#fff;font-weight:bold">See the plans</a></p>'
                % (btn(SITE + "/checkout/2", "Upgrade now &rarr;"), FONT, SITE))
    rows.append('<tr><td style="padding:34px 28px 6px"><table role="presentation" width="100%%" cellpadding="0" cellspacing="0" border="0" style="background:%s;border-radius:18px">'
                '<tr><td style="padding:26px 22px">%s%s%s<img src="%spublisher.jpg" width="500" alt="3VL Smart Publisher" style="display:block;width:100%%;height:auto;border-radius:12px;border:0;margin:0 0 16px">%s%s</td></tr></table></td></tr>'
                % (NAVY, kicker("New &middot; Ready now", GOLD), h2("3VL Smart Publisher", "#fff"),
                   p("Have an event, a special or news? Give us the basics in about 2 minutes. Our smart publishing tool writes and designs a polished page about it "
                     "on Three Village Local, you preview and approve it, and it goes live when you choose.", 16, "#dbe4ee"),
                   base, p(perk, 15, "#fff", 14), pcta))
    # checklist
    rows.append('<tr><td style="padding:34px 28px 6px"><table role="presentation" width="100%%" cellpadding="0" cellspacing="0" border="0" style="background:#fff;border:2px solid %s;border-radius:16px"><tr><td style="padding:24px 22px">'
                '%s%s%s%s<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding:0 0 8px">%s</td></tr></table></td></tr></table></td></tr>'
                % (GOLD, kicker("Two quick things"), h2("Make the most of the new site"),
                   p("<b style=\"color:%s\">1. Freshen up your listing.</b> Log in and update your photos, hours, description and services. Complete "
                     "listings show up more in smart search and get more calls." % NAVY, 15),
                   p("<b style=\"color:%s\">2. Never miss a lead.</b> When a neighbor reaches out through Three Village Local, we email you right away "
                     "from <b>admin@threevillagelocal.com</b>, and the subject line tells you it is a lead. Some members have missed these, so please "
                     "add that address to your contacts or safe senders list and check your spam folder once in a while. Every lead is also in "
                     "your dashboard." % NAVY, 15, mb=18),
                   btn(SITE + "/login", "Log in and update &rarr;", NAVY, "#fff")))
    # app
    badges = base.replace("member-2026-10/", "2026-10-02/")
    rows.append('<tr><td align="center" style="padding:30px 28px 0">%s<a href="%s/app"><img src="%sapp-store.png" width="120" alt="Download on the App Store" style="border:0;margin:0 4px"></a>'
                '<a href="%s/app"><img src="%sgoogle-play.png" width="120" alt="Get it on Google Play" style="border:0;margin:0 4px"></a></td></tr>'
                % (p("<b style=\"color:%s\">Tell your customers about the free app.</b> Three Village Local is on iPhone and Android, with your listing one tap away." % NAVY, 15, INK, 14, "text-align:center"),
                   SITE, badges, SITE, badges))
    # footer
    rows.append('<tr><td style="padding:28px 28px 30px;text-align:center">%s%s%s</td></tr>'
                % (p("Questions, or want help with your listing? Just reply to this email.", 14, NAVY, 10),
                   p("You are getting this because %s is a member of Three Village Local. Prefer not to get member updates? Reply &ldquo;unsubscribe&rdquo; and we will take you off." % co, 13, MUT, 6),
                   p(MAILING_ADDRESS + ' &middot; <a href="%s" style="color:%s">threevillagelocal.com</a>' % (SITE, MUT), 13, MUT, 0)))
    pre = "A first look at the new Three Village Local website and app: smart search, a premium redesign and new member perks for %s." % co
    body = ('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Member update</title></head>'
            '<body style="margin:0;padding:0;background:%s"><div style="display:none;max-height:0;overflow:hidden;opacity:0">%s</div>'
            '<table role="presentation" width="100%%" cellpadding="0" cellspacing="0" border="0" style="background:%s"><tr><td align="center" style="padding:18px 10px">'
            '<table role="presentation" width="100%%" cellpadding="0" cellspacing="0" border="0" style="width:100%%;max-width:600px;background:#f7f9fb;border-radius:18px;overflow:hidden">'
            '%s</table></td></tr></table></body></html>') % (BG, pre, BG, "".join(rows))
    # also set the old bgcolor attribute wherever a cell/table has a background, so light text never lands on white
    # in mail apps that drop CSS backgrounds
    body = re.sub(r'<(td|table)([^>]*?) style="background:(#[0-9a-fA-F]{6})', r'<\1\2 bgcolor="\3" style="background:\3', body)
    subject = "%s: a first look at the new Three Village Local website and app" % html.unescape(co)
    return body, subject


def main():
    name, priv = sys.argv[1], sys.argv[2]
    only = set(sys.argv[3:])
    recips = json.load(open(os.path.join(priv, "recipients.json"), encoding="utf-8"))
    picks = json.load(open(os.path.join(priv, "search_picks.json"), encoding="utf-8"))
    banner_ids = {b["id"] for b in json.load(open(os.path.join(HERE, "banners.json"), encoding="utf-8"))}
    base = "https://threevillagelocal-cloud.github.io/3vl-share/email/%s/" % name
    od = os.path.join(priv, "out")
    os.makedirs(od, exist_ok=True)
    n = 0
    for r in recips:
        if only and r["id"] not in only:
            continue
        pk = picks.get(r["id"], {})
        has_s = bool(pk.get("q")) and os.path.exists(os.path.join(SHARE, "email", name, "s-%s.jpg" % r["id"]))
        body, subj = build(r, pk, r["id"] in banner_ids, base, has_s)
        open(os.path.join(od, "%s.html" % r["id"]), "w", encoding="utf-8").write(body)
        open(os.path.join(od, "%s.subject.txt" % r["id"]), "w", encoding="utf-8").write(subj)
        n += 1
    print("built", n, "emails ->", od)


if __name__ == "__main__":
    main()
