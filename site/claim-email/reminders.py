"""Claim email follow-ups (owner 10/3/2026): to "Waiting to claim" listings that still have not claimed.
  r1    = Tue Oct 13: "Your page is still waiting for you" (iPad picture again, free + 1 minute up top, the weekly-email bonus)
  final = Tue Oct 20: last reminder, three short lines, one button
Honest urgency only: the page stays up either way (owner: no deletion threat); what they lose is control of it, and the
free weekly-email feature for listings claimed by Friday, Oct 23.

    python site/claim-email/reminders.py <r1|final> <name> <private dir> [id ...]
reads  <private dir>/recipients.json + claims.json (PRIVATE); pictures from 3vl-share/email/<name>/
writes <private dir>/out-<kind>/<id>.html + <id>.subject.txt   (nothing is sent here)"""
import html, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build import (esc, btn, solid_bg, FONT, NAVY, GOLD, INK, MUT, LINE, BG, MAILING_ADDRESS, SITE, COMMON, GENERIC,
                   p, kicker, h2, short_name, tick)

DEADLINE = "Friday, October 23"


def masthead():
    return ('<tr><td style="background:%s;padding:18px 28px"><table role="presentation" width="100%%" cellpadding="0" cellspacing="0" border="0"><tr>'
            '<td width="52"><img src="%slogo.png" width="44" height="44" alt="Three Village Local" style="display:block;border:0"></td>'
            '<td style="padding-left:12px"><p style="margin:0;font:bold 19px %s;color:#fff">Three Village <span style="color:%s">Local</span></p>'
            '<p style="margin:2px 0 0;font:13px %s;color:#c9d6e3">Your neighbors in business</p></td></tr></table></td></tr>'
            % (NAVY, COMMON, FONT, GOLD, FONT))


def footer(co):
    return ('<tr><td style="padding:26px 28px 30px;text-align:center">%s%s%s</td></tr>'
            % (p("Questions, or something on your page to fix? Just reply to this email.<br>The Three Village Local team", 14, NAVY, 12),
               p("You are getting this because we created a free page for %s on Three Village Local. Not the right contact, or prefer no emails "
                 "from us? Reply &ldquo;unsubscribe&rdquo; and we will take you off." % co, 13, MUT, 6),
               p(MAILING_ADDRESS + ' &middot; <a href="%s" style="color:%s">threevillagelocal.com</a>' % (SITE, MUT), 13, MUT, 0)))


def wrap(rows, pre, title):
    body = ('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>%s</title></head>'
            '<body style="margin:0;padding:0;background:%s"><div style="display:none;max-height:0;overflow:hidden;opacity:0">%s</div>'
            '<table role="presentation" width="100%%" cellpadding="0" cellspacing="0" border="0" style="background:%s"><tr><td align="center" style="padding:18px 10px">'
            '<table role="presentation" width="100%%" cellpadding="0" cellspacing="0" border="0" style="width:100%%;max-width:600px;background:#f7f9fb;border-radius:18px;overflow:hidden">'
            '%s</table></td></tr></table></body></html>') % (title, BG, pre, BG, "".join(rows))
    return solid_bg(body)


def center_btn(href, label):
    return btn(href, label).replace("<table ", '<table align="center" ', 1)


def bonus_box(co, last=False):
    head = "Ends this Friday" if last else "Bonus for claiming by %s" % DEADLINE
    return ('<tr><td style="padding:22px 28px 4px"><table role="presentation" width="100%%" cellpadding="0" cellspacing="0" border="0" '
            'style="background:#fff8e8;border:2px solid %s;border-radius:14px"><tr><td style="padding:18px 20px">%s%s</td></tr></table></td></tr>'
            % (GOLD, kicker(head),
               p("Claim your page by <b>%s</b> and we&rsquo;ll feature <b>%s</b> in our weekly email to Three Village residents, free." % (DEADLINE, co), 15, INK, 0)))


def build(kind, r, claim, base, utm):
    co = esc(short_name(r["company"]) or "your business")
    first = esc(r["first"]) if r["first"] and r["first"].lower() not in GENERIC else ""
    hi = ("Hi %s," % first) if first else "Hello,"
    page = "%s/%s?%s" % (SITE, r["filename"], utm)
    claim = claim + "&" + utm
    rows = [masthead()]
    if kind == "r1":
        rows.append('<tr><td style="padding:30px 28px 6px">%s<h1 style="margin:0 0 14px;font:bold 30px/1.2 %s;color:%s">Your page is ready. It just needs you.</h1>%s%s</td></tr>'
                    % (kicker("For " + co), FONT, NAVY, p(hi, 16, INK, 10),
                       p("Earlier this month we built a page for <b>%s</b> on Three Village Local. It&rsquo;s live and neighbors can already find it, but right now "
                         "the details are whatever we put up. Claim it and it&rsquo;s yours to update." % co, 16, INK, 16)))
        rows.append('<tr><td align="center" style="padding:0 28px 18px">%s<p style="margin:12px 0 0;font:bold 14px %s;color:%s">'
                    'Free &middot; About a minute &middot; No credit card</p></td></tr>' % (center_btn(claim, "Claim my free page &rarr;"), FONT, NAVY))
        rows.append('<tr><td style="padding:0 28px 6px"><a href="%s"><img src="%sclaim-%s.gif" width="544" alt="Your page for %s, live on Three Village Local" '
                    'style="display:block;width:100%%;height:auto;border-radius:14px;border:0"></a></td></tr>' % (esc(page), base, r["id"], co))
        rows.append(bonus_box(co))
        rows.append('<tr><td style="padding:24px 28px 4px">%s<table role="presentation" cellpadding="0" cellspacing="0" border="0">%s%s%s</table></td></tr>'
                    % (h2("Claiming is easy"),
                       tick("Tap <b style=\"color:%s\">Claim my free page</b>." % NAVY),
                       tick("Pick the free option, then enter your email and a password."),
                       tick("Done. Update your photos, hours and description whenever you like.")))
        rows.append('<tr><td align="center" style="padding:6px 28px 6px">%s<p style="margin:14px 0 0;font:14px %s;color:%s">'
                    '<a href="%s" style="color:%s;font-weight:bold">See your page as customers see it</a></p></td></tr>'
                    % (center_btn(claim, "Claim my free page &rarr;"), FONT, MUT, esc(page), NAVY))
        pre = "Your free page on Three Village Local is live. Claim it in about a minute, no credit card."
        subject = "%s, your Three Village Local page is still waiting for you" % html.unescape(co)
        title = "Your page is waiting"
    else:
        rows.append('<tr><td style="padding:30px 28px 6px">%s<h1 style="margin:0 0 14px;font:bold 28px/1.2 %s;color:%s">Last reminder: your page is still unclaimed</h1>%s%s%s</td></tr>'
                    % (kicker("For " + co), FONT, NAVY, p(hi, 16, INK, 10),
                       p("This is our last email about it. Your page for <b>%s</b> stays up either way, but only you can update it, add photos "
                         "or fix anything we got wrong." % co, 16, INK, 14),
                       p("It&rsquo;s free and takes about a minute. No credit card.", 16, INK, 6)))
        rows.append('<tr><td style="padding:10px 28px 6px"><a href="%s"><img src="%sclaim-%s.jpg" width="544" alt="Your page for %s, live on Three Village Local" '
                    'style="display:block;width:100%%;height:auto;border-radius:14px;border:0"></a></td></tr>' % (esc(page), base, r["id"], co))
        rows.append(bonus_box(co, last=True))
        rows.append('<tr><td align="center" style="padding:22px 28px 6px">%s</td></tr>' % center_btn(claim, "Claim my free page &rarr;"))
        pre = "Last reminder: claim your free page on Three Village Local. Free, about a minute."
        subject = "%s: last reminder about your free page" % html.unescape(co)
        title = "Last reminder"
    rows.append(footer(co))
    return wrap(rows, pre, title), subject


def main():
    kind, name, priv = sys.argv[1], sys.argv[2], sys.argv[3]
    only = set(sys.argv[4:])
    assert kind in ("r1", "final")
    recips = json.load(open(os.path.join(priv, "recipients.json"), encoding="utf-8"))
    claims = json.load(open(os.path.join(priv, "claims.json"), encoding="utf-8"))
    base = "https://threevillagelocal-cloud.github.io/3vl-share/email/%s/" % name
    utm = "utm_source=email&utm_medium=email&utm_campaign=claim-2026-10-" + kind
    od = os.path.join(priv, "out-" + kind)
    os.makedirs(od, exist_ok=True)
    n = 0
    for r in recips:
        if (only and r["id"] not in only) or not claims.get(r["id"]):
            continue
        body, subj = build(kind, r, claims[r["id"]], base, utm)
        open(os.path.join(od, "%s.html" % r["id"]), "w", encoding="utf-8").write(body)
        open(os.path.join(od, "%s.subject.txt" % r["id"]), "w", encoding="utf-8").write(subj)
        n += 1
    print("built", n, kind, "emails ->", od)


if __name__ == "__main__":
    main()
