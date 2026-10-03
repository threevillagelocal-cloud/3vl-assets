"""Claim / enroll email (owner 10/2/2026): one email per "Waiting to claim" listing. We already built their page; it is live;
they claim it (free) to make it theirs and get customer messages. Their own listing shown on an iPad (visuals.py).

    python site/claim-email/build.py <name> <private dir> [id ...]
reads  <private dir>/recipients.json (addresses: PRIVATE, never in this repo); pictures in 3vl-share/email/<name>/
writes <private dir>/out/<id>.html + <id>.subject.txt, and <private dir>/claims.json (claim links)   (nothing is sent here)"""
import html, json, os, re, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.dirname(os.path.dirname(HERE))
SHARE = os.path.join(os.path.dirname(ASSETS), "3vl-share")
sys.path.insert(0, os.path.join(ASSETS, "weekender"))
from email_build import solid_bg, esc, btn, FONT, NAVY, NAVY2, GOLD, INK, MUT, LINE, BG, MAILING_ADDRESS
from member_email_build import p, kicker, h2, short_name

SITE = "https://www.threevillagelocal.com"
COMMON = "https://threevillagelocal-cloud.github.io/3vl-share/email/2026-10-02/"   # logo + app badges
UTM = "utm_source=email&utm_medium=email&utm_campaign=claim-2026-10"
GENERIC = ("info", "admin", "office", "contact", "hello", "sales", "manager")


def claim_link(filename):
    h = urllib.request.urlopen(urllib.request.Request("%s/%s" % (SITE, filename), headers={"User-Agent": "Mozilla/5.0 3VL-claim-email"}), timeout=60).read().decode("utf-8", "ignore")
    m = re.search(r'href="(/join\?claim=[0-9a-f]+)"', h)
    return SITE + m.group(1) if m else None


def tick(t):
    return ('<tr><td valign="top" style="padding:0 12px 14px 0;width:26px"><div style="width:24px;height:24px;border-radius:12px;background:%s;color:%s;'
            'font:bold 14px/24px %s;text-align:center">&#10003;</div></td><td style="padding:0 0 14px;font:15px/1.55 %s;color:%s">%s</td></tr>'
            % (GOLD, NAVY, FONT, FONT, INK, t))


def build(r, claim, base):
    co = esc(short_name(r["company"]) or "your business")
    first = esc(r["first"]) if r["first"] and r["first"].lower() not in GENERIC else ""
    page = "%s/%s?%s" % (SITE, r["filename"], UTM)
    claim = claim + "&" + UTM
    rows = []
    # masthead (short strip)
    rows.append('<tr><td style="background:%s;padding:18px 28px"><table role="presentation" width="100%%" cellpadding="0" cellspacing="0" border="0"><tr>'
                '<td width="52"><img src="%slogo.png" width="44" height="44" alt="Three Village Local" style="display:block;border:0"></td>'
                '<td style="padding-left:12px"><p style="margin:0;font:bold 19px %s;color:#fff">Three Village <span style="color:%s">Local</span></p>'
                '<p style="margin:2px 0 0;font:13px %s;color:#c9d6e3">Your neighbors in business</p></td></tr></table></td></tr>'
                % (NAVY, COMMON, FONT, GOLD, FONT))
    # headline + the iPad
    hi = ("Hi %s," % first) if first else "Hello,"
    rows.append('<tr><td style="padding:30px 28px 6px">%s<h1 style="margin:0 0 14px;font:bold 30px/1.2 %s;color:%s">We built your page for you. It&rsquo;s live.</h1>%s%s</td></tr>'
                % (kicker("For " + co), FONT, NAVY, p(hi, 16, INK, 10),
                   p("Neighbors in Setauket, Stony Brook and Port Jefferson use Three Village Local to find local businesses. So we went ahead and "
                     "set up a page for <b>%s</b>: your details, photo, hours and a map, all done. It&rsquo;s already live, and here it is:" % co, 16, INK, 18)))
    rows.append('<tr><td style="padding:0 28px 6px"><a href="%s"><img src="%sclaim-%s.gif" width="544" alt="Your page for %s, live on Three Village Local" '
                'style="display:block;width:100%%;height:auto;border-radius:14px;border:0"></a></td></tr>' % (esc(page), base, r["id"], co))
    # what claiming gives them
    rows.append('<tr><td style="padding:26px 28px 4px">%s%s<table role="presentation" cellpadding="0" cellspacing="0" border="0">%s%s%s</table></td></tr>'
                % (h2("The work is done. Just claim it."),
                   p("Claiming takes about a minute and it&rsquo;s free. Once it&rsquo;s yours, you can:", 16, INK, 16),
                   tick("<b style=\"color:%s\">Make it yours.</b> Update your photos, hours, description and services any time." % NAVY),
                   tick("<b style=\"color:%s\">Hear from customers.</b> Messages from your page come straight to your inbox." % NAVY),
                   tick("<b style=\"color:%s\">Get found.</b> Show up when neighbors search on our website and the free Three Village Local app." % NAVY)))
    rows.append('<tr><td align="center" style="padding:10px 28px 6px">%s<p style="margin:14px 0 0;font:14px %s;color:%s">'
                '<a href="%s" style="color:%s;font-weight:bold">See your page as customers see it</a></p></td></tr>'
                % (btn(claim, "Claim my free page &rarr;").replace("<table ", '<table align="center" ', 1), FONT, MUT, esc(page), NAVY))
    # light upgrade note
    rows.append('<tr><td style="padding:28px 28px 4px"><table role="presentation" width="100%%" cellpadding="0" cellspacing="0" border="0" style="background:#fff;border:1px solid %s;border-radius:14px">'
                '<tr><td style="padding:18px 20px">%s</td></tr></table></td></tr>'
                % (LINE, p("<b style=\"color:%s\">Want to stand out even more?</b> Featured spots on our homepage, banner ads and help promoting your "
                           "events and specials are available too. <a href=\"%s/join?%s\" style=\"color:%s;font-weight:bold\">See the options</a>" % (NAVY, SITE, UTM, NAVY), 14, INK, 0)))
    # footer
    rows.append('<tr><td style="padding:26px 28px 30px;text-align:center">%s%s%s</td></tr>'
                % (p("Questions, or something on your page to fix? Just reply to this email.<br>The Three Village Local team", 14, NAVY, 12),
                   p("You are getting this because we created a free page for %s on Three Village Local. Not the right contact, or prefer no emails "
                     "from us? Reply &ldquo;unsubscribe&rdquo; and we will take you off." % co, 13, MUT, 6),
                   p(MAILING_ADDRESS + ' &middot; <a href="%s" style="color:%s">threevillagelocal.com</a>' % (SITE, MUT), 13, MUT, 0)))
    pre = "We set up your page on Three Village Local and it is already live. Claim it free in about a minute."
    body = ('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Your page is ready</title></head>'
            '<body style="margin:0;padding:0;background:%s"><div style="display:none;max-height:0;overflow:hidden;opacity:0">%s</div>'
            '<table role="presentation" width="100%%" cellpadding="0" cellspacing="0" border="0" style="background:%s"><tr><td align="center" style="padding:18px 10px">'
            '<table role="presentation" width="100%%" cellpadding="0" cellspacing="0" border="0" style="width:100%%;max-width:600px;background:#f7f9fb;border-radius:18px;overflow:hidden">'
            '%s</table></td></tr></table></body></html>') % (BG, pre, BG, "".join(rows))
    body = solid_bg(body)
    subject = "%s, your page on Three Village Local is ready" % html.unescape(co)
    return body, subject


def main():
    name, priv = sys.argv[1], sys.argv[2]
    only = set(sys.argv[3:])
    recips = json.load(open(os.path.join(priv, "recipients.json"), encoding="utf-8"))
    cp = os.path.join(priv, "claims.json")
    claims = json.load(open(cp, encoding="utf-8")) if os.path.exists(cp) else {}
    base = "https://threevillagelocal-cloud.github.io/3vl-share/email/%s/" % name
    od = os.path.join(priv, "out")
    os.makedirs(od, exist_ok=True)
    n, skipped = 0, []
    for r in recips:
        if only and r["id"] not in only:
            continue
        if not claims.get(r["id"]):
            claims[r["id"]] = claim_link(r["filename"])
            json.dump(claims, open(cp, "w", encoding="utf-8"), indent=1)
        if not claims[r["id"]] or not os.path.exists(os.path.join(SHARE, "email", name, "claim-%s.gif" % r["id"])):
            skipped.append((r["id"], "no claim link" if not claims[r["id"]] else "no picture")); continue
        body, subj = build(r, claims[r["id"]], base)
        open(os.path.join(od, "%s.html" % r["id"]), "w", encoding="utf-8").write(body)
        open(os.path.join(od, "%s.subject.txt" % r["id"]), "w", encoding="utf-8").write(subj)
        n += 1
    print("built", n, "emails ->", od, "| skipped:", skipped)


if __name__ == "__main__":
    main()
