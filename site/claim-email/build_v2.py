"""Claim email v2 "premium" (owner 10/7/2026): same look as the Smart Publisher preview email the owner liked
(navy bar, white card, soft blue note box, bordered preview card with a big picture, navy fact boxes, gold + navy pill buttons),
with the official logo lockup, the business's own animated iPad picture and a line written for its specialty.

    python site/claim-email/build_v2.py <name> <private dir> [id ...]
reads  <private dir>/recipients.json  (id, email, first, company, filename, city, specialty)
uses   3vl-share/email/<name>/claim-<id>.gif  (visuals.py)
writes <private dir>/out-v2/<id>.html + <id>.subject.txt and <private dir>/claims.json   (nothing is sent here)"""
import html, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build import claim_link, SITE, UTM, GENERIC, SHARE, short_name, MAILING_ADDRESS

F = "'Helvetica Neue',Helvetica,Arial,sans-serif"
NAVY, NAVY2, GOLD, INK, MUT, LINE, SOFT, BLUE = "#1b2f45", "#13294b", "#f2a93b", "#1d2b3a", "#5b6b7c", "#dde5ee", "#f3f7fd", "#1d5fbf"
LOGO = "https://threevillagelocal-cloud.github.io/3vl-share/email/common/logo-white-440.png"
esc = lambda s: html.escape(str(s or ""), quote=True)


def pill(href, label, bg, fg):
    return ('<td style="padding:0 10px 10px 0"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td style="border-radius:999px;background:%s">'
            '<a href="%s" style="display:inline-block;padding:15px 26px;font:bold 16px %s;color:%s;text-decoration:none">%s</a></td></tr></table></td>') % (bg, esc(href), F, fg, label)


def fact(label, big, small=""):
    return ('<td valign="top" width="33%%" style="padding:0 5px 0 0"><table role="presentation" width="100%%" cellpadding="0" cellspacing="0" border="0" style="background:%s;border-radius:12px">'
            '<tr><td style="padding:14px 14px 13px;font-family:%s"><div style="font:bold 10px %s;letter-spacing:2px;color:#8ec5ff;text-transform:uppercase">%s</div>'
            '<div style="font:bold 17px/1.3 %s;color:#ffffff;margin-top:4px">%s</div>%s</td></tr></table></td>') % (
        NAVY2, F, F, label, F, big, ('<div style="font:13px/1.4 %s;color:#dbe6f3;margin-top:2px">%s</div>' % (F, small)) if small else "")


def tick(t):
    return ('<tr><td valign="top" style="padding:0 12px 12px 0;width:24px"><div style="width:22px;height:22px;border-radius:11px;background:%s;color:#fff;'
            'font:bold 13px/22px %s;text-align:center">&#10003;</div></td><td style="padding:0 0 12px;font:15px/1.55 %s;color:%s">%s</td></tr>') % (BLUE, F, F, INK, t)


def build(r, claim, base):
    co = esc(short_name(r["company"]) or "your business")
    first = esc(r.get("first")) if r.get("first") and r["first"].lower() not in GENERIC else ""
    page = "%s/%s?%s" % (SITE, r["filename"], UTM)
    claim = claim + "&" + UTM
    spec = esc(r.get("specialty") or "")
    town = esc(r.get("city") or "Three Village")
    rows = []
    # navy bar with the official logo lockup
    rows.append('<tr><td style="background:%s;padding:16px 26px"><img src="%s" width="176" alt="Three Village Local" style="display:block;border:0;width:176px;height:auto"></td></tr>' % (NAVY, LOGO))
    # greeting + soft note from Matt
    hi = ("Hi %s," % first) if first else "Hello,"
    rows.append(('<tr><td style="padding:24px 26px 4px;font:16px/1.6 %s;color:%s">%s'
                 '<div style="margin:12px 0 4px;padding:16px 18px;background:%s;border-radius:12px">Neighbors in Setauket, Stony Brook and Port Jefferson use Three Village Local '
                 'to find local businesses, so we built <b>%s</b> a page of its own: your photo, hours, map, phone and links, all set up and already live. '
                 'There is nothing to pay and nothing to set up. It just needs you to claim it.<br><br>Matt<br><span style="color:%s;font-size:14px">Founder, Three Village Local</span></div></td></tr>')
                % (F, INK, hi, SOFT, co, MUT))
    # preview card: their real page on the iPad
    rows.append(('<tr><td style="padding:14px 26px 6px"><div style="border:1px solid %s;border-radius:16px;padding:20px">'
                 '<p style="margin:0 0 6px;font:bold 12px %s;letter-spacing:2px;text-transform:uppercase;color:#b36b00">Your page is live</p>'
                 '<h1 style="margin:0 0 14px;font:bold 26px/1.2 %s;color:%s">%s</h1>'
                 '<a href="%s"><img src="%sclaim-%s.gif" width="506" alt="The %s page on Three Village Local" style="display:block;width:100%%;height:auto;border-radius:12px;border:0"></a>'
                 '<table role="presentation" width="100%%" cellpadding="0" cellspacing="0" border="0" style="margin-top:14px"><tr>%s%s%s</tr></table>'
                 '%s</div></td></tr>')
                % (LINE, F, F, NAVY, co, esc(page), base, r["id"], co,
                   fact("Visitors", "100,000+", "every month"), fact("Social", "100,000+", "views a month"), fact("Our app", "Free", "iPhone &amp; Android"),
                   ('<p style="margin:16px 0 0;font:16px/1.6 %s;color:%s">When neighbors search for <b>%s</b> in %s, your page is there with your phone number, '
                    'directions and website one tap away.</p>' % (F, INK, spec.lower(), town)) if spec else ""))
    # what claiming gives them + buttons
    rows.append(('<tr><td style="padding:20px 26px 4px"><h2 style="margin:0 0 12px;font:bold 21px/1.3 %s;color:%s">Claim it free in about a minute</h2>'
                 '<table role="presentation" cellpadding="0" cellspacing="0" border="0">%s%s%s</table></td></tr>')
                % (F, NAVY, tick("<b style=\"color:%s\">Make it yours.</b> Update your photos, hours, description and services any time." % NAVY),
                   tick("<b style=\"color:%s\">Hear from customers.</b> Messages from your page come straight to your inbox." % NAVY),
                   tick("<b style=\"color:%s\">Get found.</b> Show up on our website, in search and in the free Three Village Local app." % NAVY)))
    rows.append('<tr><td style="padding:8px 26px 0"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>%s%s</tr></table></td></tr>'
                % (pill(claim, "Claim my free page &rarr;", GOLD, NAVY), pill(page, "See my page", NAVY, "#ffffff")))
    # upgrade note
    rows.append(('<tr><td style="padding:22px 26px 4px"><table role="presentation" width="100%%" cellpadding="0" cellspacing="0" border="0" style="background:%s;border-radius:12px">'
                 '<tr><td style="padding:16px 18px;font:14px/1.55 %s;color:%s"><b style="color:%s">Want to stand out?</b> Featured and VIP members get a premium designed page, '
                 'top spots in their category, homepage and email features, and help promoting events and specials. '
                 '<a href="%s/join?%s" style="color:%s;font-weight:bold">See the plans</a></td></tr></table></td></tr>') % (SOFT, F, INK, NAVY, SITE, UTM, BLUE))
    # footer
    rows.append(('<tr><td style="padding:22px 26px 28px;font:13px/1.6 %s;color:%s;text-align:center">Questions, or something on your page to fix? Just reply to this email.<br><br>'
                 'You are getting this because we created a free page for %s on Three Village Local. Not the right contact, or prefer no emails from us? '
                 'Reply &ldquo;unsubscribe&rdquo; and we will take you off.<br>%s &middot; <a href="%s" style="color:%s">threevillagelocal.com</a></td></tr>')
                % (F, MUT, co, MAILING_ADDRESS, SITE, MUT))
    pre = "We built %s a page on Three Village Local. It is live, and it is yours to claim, free." % co
    body = ('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>'
            '<body style="margin:0;background:#eef2f6"><div style="display:none;max-height:0;overflow:hidden">%s</div>'
            '<table role="presentation" width="100%%" cellpadding="0" cellspacing="0" border="0" style="background:#eef2f6"><tr><td align="center" style="padding:18px 10px">'
            '<table role="presentation" width="100%%" cellpadding="0" cellspacing="0" border="0" style="max-width:600px;background:#ffffff;border-radius:18px;overflow:hidden">%s</table>'
            '</td></tr></table></body></html>') % (esc(pre), "".join(rows))
    subj = "%s, your page on Three Village Local is ready" % html.unescape(co)
    return body, subj


def main():
    name, priv, only = sys.argv[1], sys.argv[2], set(sys.argv[3:])
    base = "https://threevillagelocal-cloud.github.io/3vl-share/email/%s/" % name
    recips = json.load(open(os.path.join(priv, "recipients.json"), encoding="utf-8"))
    cpath = os.path.join(priv, "claims.json")
    claims = json.load(open(cpath, encoding="utf-8")) if os.path.exists(cpath) else {}
    od = os.path.join(priv, "out-v2"); os.makedirs(od, exist_ok=True)
    skipped = []
    for r in recips:
        if only and r["id"] not in only:
            continue
        if not claims.get(r["id"]):
            claims[r["id"]] = claim_link(r["filename"])
        if not claims[r["id"]] or not os.path.exists(os.path.join(SHARE, "email", name, "claim-%s.gif" % r["id"])):
            skipped.append((r["id"], "no claim link" if not claims[r["id"]] else "no picture")); continue
        body, subj = build(r, claims[r["id"]], base)
        open(os.path.join(od, "%s.html" % r["id"]), "w", encoding="utf-8").write(body)
        open(os.path.join(od, "%s.subject.txt" % r["id"]), "w", encoding="utf-8").write(subj)
    json.dump(claims, open(cpath, "w", encoding="utf-8"), indent=1)
    print("built", len([r for r in recips if (not only or r["id"] in only)]) - len(skipped), "skipped", skipped)


if __name__ == "__main__":
    main()
