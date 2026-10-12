"""Claim email "plain" (owner 10/12/2026, A/B test against build_v2): reads like a short personal note from Matt,
no pictures, no buttons, one claim link. Same inputs as build_v2.

    python site/claim-email/build_plain.py <name> <private dir> [id ...]
reads  <private dir>/recipients.json  (id, email, first, company, filename, city, specialty) + claims.json
writes <private dir>/out-plain/<id>.html + <id>.subject.txt   (nothing is sent here)"""
import html, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build import claim_link, SITE, UTM, GENERIC, short_name, MAILING_ADDRESS

F = "Arial,Helvetica,sans-serif"
esc = lambda s: html.escape(str(s or ""), quote=True)


def build(r, claim):
    co = esc(short_name(r["company"]) or "your business")
    first = esc(r.get("first")) if r.get("first") and r["first"].lower() not in GENERIC else ""
    spec = esc((r.get("specialty") or "").lower())
    town = esc(r.get("city") or "Three Village")
    claim = claim + "&" + UTM
    find = ("so neighbors looking for %s in %s can find you" % (spec, town)) if spec else ("so neighbors in %s can find you" % town)
    p = '<p style="margin:0 0 16px">%s</p>'
    body = "".join([
        p % (("Hi %s," % first) if first else "Hi there,"),
        p % ("I'm Matt, I run Three Village Local. We put together a free page for %s on our site %s. "
             "Your photo, hours, map and phone number are already up." % (co, find)),
        p % ('It\'s yours if you want it. Claiming is free and takes about a minute: <a href="%s" style="color:#1a56b8">claim the %s page</a>.'
             % (esc(claim), co)),
        p % "If anything on it is wrong, just reply and I'll fix it.",
        p % ('Matt<br>Founder, Three Village Local<br><a href="%s/?%s" style="color:#1a56b8">threevillagelocal.com</a>' % (SITE, UTM)),
        '<p style="margin:28px 0 0;font-size:12px;color:#888">You are getting this because we created a free page for %s. '
        'Not the right contact, or prefer no emails from us? Reply "unsubscribe" and we will take you off.<br>%s</p>' % (co, MAILING_ADDRESS),
    ])
    doc = ('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>'
           '<body style="margin:0;padding:16px;font:15px/1.55 %s;color:#222;background:#fff"><div style="max-width:560px">%s</div></body></html>') % (F, body)
    return doc, "%s on Three Village Local" % html.unescape(co)


def main():
    name, priv, only = sys.argv[1], sys.argv[2], set(sys.argv[3:])
    recips = json.load(open(os.path.join(priv, "recipients.json"), encoding="utf-8"))
    cpath = os.path.join(priv, "claims.json")
    claims = json.load(open(cpath, encoding="utf-8")) if os.path.exists(cpath) else {}
    od = os.path.join(priv, "out-plain"); os.makedirs(od, exist_ok=True)
    skipped = []
    for r in recips:
        if only and r["id"] not in only:
            continue
        if not claims.get(r["id"]):
            claims[r["id"]] = claim_link(r["filename"])
        if not claims[r["id"]]:
            skipped.append((r["id"], "no claim link")); continue
        body, subj = build(r, claims[r["id"]])
        open(os.path.join(od, "%s.html" % r["id"]), "w", encoding="utf-8").write(body)
        open(os.path.join(od, "%s.subject.txt" % r["id"]), "w", encoding="utf-8").write(subj)
    json.dump(claims, open(cpath, "w", encoding="utf-8"), indent=1)
    print("built", len([r for r in recips if (not only or r["id"] in only)]) - len(skipped), "skipped", skipped)


if __name__ == "__main__":
    main()
