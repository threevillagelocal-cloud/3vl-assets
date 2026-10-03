"""Weekly email: "This Week in Three Village" (owner 10/2/2026: goes to all member businesses + newsletter subscribers, sent by BD's newsletter tool).
Builds an email-safe HTML file (600px tables, inline styles, JPG/PNG images: many mail apps cannot show WebP) from the same weekly
edition the homepage uses (weekender/<edition>/weekend.json), plus homes.json, vip.json and the latest blog posts.

    python weekender/email_build.py [edition]        -> weekender/email/<edition>/email.html (+ images pushed to 3vl-share/email/<edition>/)

Nothing is sent from here. The HTML is pasted into BD admin > Emails > Create Newsletter (BD adds the unsubscribe link)."""
import datetime, html, io, json, os, re, subprocess, sys, urllib.request

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.dirname(HERE)
SHARE = os.path.join(os.path.dirname(ASSETS), "3vl-share")
SITE = "https://www.threevillagelocal.com"
UA = {"User-Agent": "Mozilla/5.0 (compatible; 3VL-email/1.0; +https://www.threevillagelocal.com)"}
NAVY, NAVY2, GOLD, INK, MUT, LINE, BG = "#1b2f45", "#0f1f31", "#f2a93b", "#1d2b3a", "#5b6b7c", "#dde5ee", "#eef2f6"
FONT = "'Helvetica Neue',Helvetica,Arial,sans-serif"
MAILING_ADDRESS = "Three Village Local &middot; Setauket, NY 11733"   # TODO owner: a full postal address is required by law in marketing email


def solid_bg(body):
    """Also set the old bgcolor attribute wherever a cell/table has a CSS background, so light text never lands on white
    in mail apps that drop CSS backgrounds (owner saw white-on-white 10/3/2026)."""
    return re.sub(r'<(td|table)([^>]*?) style="background:(#[0-9a-fA-F]{6})', r'<\1\2 bgcolor="\3" style="background:\3', body)


def esc(s):
    return html.escape(str(s or ""), quote=True)


def latest_edition():
    eds = sorted(d for d in os.listdir(HERE) if re.match(r"\d{4}-\d\d-\d\d$", d))
    return eds[-1]


class Pics:
    """Copies the pictures the email uses as JPG (photos) / PNG (logos) into 3vl-share/email/<edition>/."""
    def __init__(self, ed):
        self.ed, self.dir, self.n = ed, os.path.join(SHARE, "email", ed), 0
        self.base = "https://threevillagelocal-cloud.github.io/3vl-share/email/%s/" % ed
        os.makedirs(self.dir, exist_ok=True)

    def get(self, src, name, w=600, h=None, logo=False):
        try:
            if src.startswith("http"):
                im = Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(src, headers=UA), timeout=40).read()))
            else:
                im = Image.open(src)
        except Exception as ex:
            print("  photo skipped:", name, ex)
            return ""
        if logo:
            im = im.convert("RGBA")
            im.thumbnail((w * 2, w * 2), Image.LANCZOS)
            out = name + ".png"
            im.save(os.path.join(self.dir, out), optimize=True)
        else:
            im = im.convert("RGB")
            if h:   # crop to the box the email shows, at 2x for sharp phones
                W, H = w * 2, h * 2
                r = max(W / im.width, H / im.height)
                im = im.resize((max(W, round(im.width * r)), max(H, round(im.height * r))), Image.LANCZOS)
                l, t = (im.width - W) // 2, (im.height - H) // 2
                im = im.crop((l, t, l + W, t + H))
            else:
                im.thumbnail((w * 2, w * 4), Image.LANCZOS)
            out = name + ".jpg"
            im.save(os.path.join(self.dir, out), "JPEG", quality=78, optimize=True, progressive=True)
        self.n += 1
        return self.base + out


def dt(iso):
    return datetime.datetime.fromisoformat(iso[:16])


def when(e):
    if e.get("when"):
        return e["when"]
    d = dt(e["start"])
    h = d.strftime("%I").lstrip("0") + (d.strftime(":%M") if d.minute else "") + (" AM" if d.hour < 12 else " PM")
    return "%s, %s %d &middot; %s" % (d.strftime("%a"), d.strftime("%b"), d.day, h)


def biz_link(name):
    """The business's own 3VL profile (same map the homepage Eat & Drink cards use)."""
    try:
        links = json.load(open(os.path.join(HERE, "biz_links.json"), encoding="utf-8"))
    except Exception:
        return ""
    key = lambda s: re.sub(r"[^a-z0-9]", "", html.unescape(s).lower().replace("’", "'"))
    want = key(name)
    return next((u for k, u in links.items() if key(k) == want), "")


def short(t, n=110):
    """One-line description: cut at a word boundary."""
    t = re.sub(r"\s+", " ", t or "").strip()
    if len(t) <= n:
        return t
    return t[:n].rsplit(" ", 1)[0].rstrip(",.;:") + "..."


def btn(href, label, bg=GOLD, fg=NAVY):
    return ('<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td style="border-radius:999px;background:%s">'
            '<a href="%s" style="display:inline-block;padding:13px 24px;font:bold 15px %s;color:%s;text-decoration:none;border-radius:999px">%s</a>'
            '</td></tr></table>' % (bg, esc(href), FONT, fg, label))


def section(title, kicker=""):
    return ('<tr><td style="padding:30px 28px 8px"><p style="margin:0 0 4px;font:bold 12px %s;letter-spacing:2px;text-transform:uppercase;color:#b36b00">%s</p>'
            '<h2 style="margin:0;font:bold 24px/1.25 %s;color:%s">%s</h2></td></tr>' % (FONT, kicker, FONT, NAVY, title))


def row(img, kicker, title, sub, desc, href, link_label):
    return ('<tr><td style="padding:12px 28px"><table role="presentation" width="100%%" cellpadding="0" cellspacing="0" border="0" style="background:#fff;border:1px solid %s;border-radius:14px">'
            '<tr><td width="130" valign="top" style="padding:0">%s</td>'
            '<td valign="top" style="padding:14px 16px">'
            '<p style="margin:0 0 4px;font:bold 12px %s;letter-spacing:1px;text-transform:uppercase;color:#b36b00">%s</p>'
            '<p style="margin:0 0 4px;font:bold 17px/1.3 %s;color:%s"><a href="%s" style="color:%s;text-decoration:none">%s</a></p>'
            '<p style="margin:0 0 8px;font:13px/1.4 %s;color:%s">%s</p>'
            '<p style="margin:0 0 8px;font:14px/1.5 %s;color:%s">%s</p>'
            '<a href="%s" style="font:bold 14px %s;color:#0b63b6;text-decoration:none">%s &rarr;</a></td></tr></table></td></tr>') % (
        LINE, ('<a href="%s"><img src="%s" width="130" height="150" alt="%s" style="display:block;width:130px;height:150px;border-radius:14px 0 0 14px;object-fit:cover;border:0"></a>' % (esc(href), img, esc(title))) if img else "",
        FONT, kicker, FONT, NAVY, esc(href), NAVY, esc(title), FONT, MUT, sub, FONT, INK, esc(desc), esc(href), FONT, link_label)


def stories(n=2):
    try:
        sys.path.insert(0, os.path.join(ASSETS, "site", "share-img"))
        from bdkey import key
        r = urllib.request.Request(SITE + "/api/v2/data_posts/get?property=data_id&property_value=14&limit=25&order_column=post_live_date&order_type=DESC",
                                   headers={"X-Api-Key": key(), "User-Agent": "Mozilla/5.0 3VL-email"})
        posts = json.loads(urllib.request.urlopen(r, timeout=60).read()).get("message", [])
        posts = [p for p in posts if p.get("post_status") == "1" and p.get("post_image")]
        posts.sort(key=lambda p: p.get("post_live_date") or "", reverse=True)
        return posts[:n]
    except Exception as ex:
        print("  stories skipped:", ex)
        return []


VIP_ID = ""   # set by --vip <member id>: personalized version for that VIP


def main():
    global VIP_ID
    args = sys.argv[1:]
    if "--vip" in args:
        i = args.index("--vip"); VIP_ID = args[i + 1]; del args[i:i + 2]
    ed = args[0] if args else latest_edition()
    d = json.load(open(os.path.join(HERE, ed, "weekend.json"), encoding="utf-8"))
    P = Pics(ed)
    ev = {e["id"]: e for e in d["events"] + d.get("allweekend", [])}
    V = d["venues"]
    picks = [ev[k] for k in d["picks"] if k in ev][:5]
    lead = next((e for e in picks if e["id"] == "spyday"), picks[0])
    guide = next((g for g in d.get("guides", []) if g[0] in lead["title"].lower()), None)
    lead_href = SITE + guide[1] if guide else (lead.get("page") or SITE)
    pic = lambda key, name, **k: P.get(os.path.join(HERE, ed, key + ".webp"), name, **k) if os.path.exists(os.path.join(HERE, ed, key + ".webp")) else ""
    start, end = dt(d["starts"]), dt(d["ends"])
    rng = "%s %d to %s%d, %d" % (start.strftime("%b"), start.day, "" if start.month == end.month else end.strftime("%b") + " ", end.day, end.year)

    o = []
    w = o.append
    others = [e["title"].split(":")[0] for e in picks if e is not lead][:2]   # whole titles only, never cut mid-word
    pre = "%s, %s, local specials and new homes for sale this weekend in Three Village." % (lead["title"], " and ".join(others))
    w('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>This Week in Three Village</title></head>')
    w('<body style="margin:0;padding:0;background:%s">' % BG)
    w('<div style="display:none;max-height:0;overflow:hidden;opacity:0">%s</div>' % esc(pre))
    w('<table role="presentation" width="100%%" cellpadding="0" cellspacing="0" border="0" style="background:%s"><tr><td align="center" style="padding:18px 10px">' % BG)
    w('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:600px;background:#f7f9fb;border-radius:18px;overflow:hidden">')
    # masthead
    w('<tr><td style="background:%s;padding:20px 28px"><table role="presentation" width="100%%" cellpadding="0" cellspacing="0" border="0"><tr>'
      '<td width="56"><img src="%s" width="48" height="48" alt="Three Village Local" style="display:block;border:0"></td>'
      '<td style="padding-left:12px"><p style="margin:0;font:bold 20px %s;color:#fff">Three Village <span style="color:%s">Local</span></p>'
      '<p style="margin:2px 0 0;font:13px %s;color:#c9d6e3">This Week in Three Village &middot; %s</p></td></tr></table></td></tr>' % (
        NAVY, P.get(os.path.join(ASSETS, "badges", "3vl-logo-160.png"), "logo", w=48, logo=True), FONT, GOLD, FONT, rng))
    # hero
    hero = pic(lead["img"], "hero", w=600, h=320)
    w('<tr><td style="padding:0"><a href="%s"><img src="%s" width="600" height="320" alt="%s" style="display:block;width:100%%;height:auto;border:0"></a></td></tr>' % (esc(lead_href), hero, esc(lead["title"])))
    w('<tr><td style="background:%s;padding:24px 28px 26px"><p style="margin:0 0 8px"><span style="display:inline-block;background:%s;color:%s;font:bold 12px %s;letter-spacing:1.5px;text-transform:uppercase;padding:6px 12px;border-radius:999px">%s</span></p>'
      '<h1 style="margin:0 0 10px;font:bold 30px/1.15 %s;color:#fff">%s</h1><p style="margin:0 0 18px;font:16px/1.55 %s;color:#dbe4ee">%s</p>%s</td></tr>' % (
        NAVY2, GOLD, NAVY, FONT, when(lead) + " &middot; " + esc(lead["price"]), FONT, esc(lead["title"]), FONT, esc(lead["desc"]),
        btn(lead_href, (guide[2] if guide else "See the details") + " &rarr;")))
    # top things to do
    w(section("Top things to do", "This weekend"))
    for i, e in enumerate([p for p in picks if p is not lead][:3]):   # short version (owner 10/2): 3 picks, one-line descriptions
        href = e.get("page") or SITE
        w(row(pic(e["img"], "pick-%d" % i, w=130, h=150), when(e), e["title"], "&#128205; " + esc(V.get(e["venue"], {}).get("name", "")) + (" &middot; " + esc(e["price"]) if e.get("price") else ""),
              short(e["desc"]), href, "Details"))
    w('<tr><td align="center" style="padding:14px 28px 4px">%s</td></tr>' % btn(SITE + "/events-calendar", "See the full calendar &rarr;", bg=NAVY, fg="#fff"))
    # eat & drink
    w(section("Eat &amp; drink specials", "Local spots"))
    for i, s in enumerate(d["specials"][:2]):
        img = pic(s.get("ext") or s.get("img"), "eat-%d" % i, w=130, h=150)
        w(row(img, esc(s["when"]), s["biz"], esc(s["title"]), short(s["desc"]), s.get("page") or biz_link(s["biz"]) or SITE, "See the spot"))
    # homes
    try:
        hm = json.load(open(os.path.join(HERE, "homes.json"), encoding="utf-8"))
    except Exception:
        hm = None
    if hm:
        th = "".join('<td width="33%%" style="padding:0 4px"><img src="%s" width="170" height="120" alt="Home for sale in the Three Village area" style="display:block;width:100%%;height:auto;border-radius:10px;border:0"></td>' % P.get(os.path.join(HERE, t), "home-%d" % i, w=170, h=120)
                     for i, t in enumerate(hm["thumbs"][:3]))
        w('<tr><td style="padding:30px 28px 6px"><table role="presentation" width="100%%" cellpadding="0" cellspacing="0" border="0" style="background:%s;border-radius:16px">'
          '<tr><td style="padding:22px 20px 8px"><p style="margin:0 0 4px;font:bold 12px %s;letter-spacing:2px;text-transform:uppercase;color:%s">Real estate</p>'
          '<p style="margin:0 0 14px;font:bold 22px/1.25 %s;color:#fff">%d new homes for sale this week in Setauket and Stony Brook</p>'
          '<table role="presentation" width="100%%" cellpadding="0" cellspacing="0" border="0"><tr>%s</tr></table></td></tr>'
          '<tr><td style="padding:12px 20px 22px">%s</td></tr></table></td></tr>' % (NAVY, FONT, GOLD, FONT, hm["count"], th, btn(hm["url"], "See all %d homes &rarr;" % hm["count"])))
    # VIP banner spotlight (owner 10/2: replaces "Local businesses we love").
    # VIP version: a picture of THEIR banner running on a live page (weekender/vip_shots.py).
    # Everyone else: one VIP banner, rotating weekly, never the owner's own (Coltrain, 122).
    banners = json.load(open(os.path.join(HERE, "banners.json"), encoding="utf-8"))
    if VIP_ID:
        mine = next(b for b in banners if b["id"] == VIP_ID)
        shot = P.base + "vip-shot-%s.jpg" % VIP_ID
        w('<tr><td style="padding:30px 28px 6px"><table role="presentation" width="100%%" cellpadding="0" cellspacing="0" border="0" style="background:%s;border-radius:16px">'
          '<tr><td style="padding:22px 20px 14px"><p style="margin:0 0 4px;font:bold 12px %s;letter-spacing:2px;text-transform:uppercase;color:%s">Your VIP banner</p>'
          '<p style="margin:0 0 6px;font:bold 22px/1.25 %s;color:#fff">Your banner is live on Three Village Local</p>'
          '<p style="margin:0 0 14px;font:15px/1.5 %s;color:#dbe4ee">Here is %s running on our site this week. It rotates across our pages and the app, with one-tap Call and View buttons for your neighbors.</p>'
          '<a href="%s"><img src="%s" width="560" alt="%s banner on Three Village Local" style="display:block;width:100%%;height:auto;border-radius:12px;border:0"></a></td></tr></table></td></tr>' % (
              NAVY, FONT, GOLD, FONT, FONT, esc(mine["name"]) + "&#39;s banner", SITE + "/categories", shot, esc(mine["name"])))
    else:
        wk = datetime.date.fromisoformat(ed).isocalendar()[1]
        pool = sorted([b for b in banners if b["id"] != "122"], key=lambda b: (int(b["id"]) * 7919 + len(b["img"]) * 31 + wk * 104729) % 1000)
        b = pool[0]
        bimg = P.get(os.path.join(HERE, b["img"]), "banner-" + b["img"].split("/")[-1].split(".")[0], w=300)
        w(section("Local business spotlight", "VIP member"))
        w('<tr><td style="padding:12px 28px 6px"><a href="%s"><img src="%s" width="544" alt="%s" style="display:block;width:100%%;height:auto;border-radius:14px;border:0"></a>'
          '<p style="margin:12px 0 0;font:14px/1.5 %s;color:%s"><b style="color:%s">%s</b> &middot; <a href="%s" style="color:#0b63b6;font-weight:bold;text-decoration:none">View on 3VL &rarr;</a></p>'
          '<p style="margin:6px 0 0;font:13px/1.5 %s;color:%s">VIP members get banner ads like this across Three Village Local and the app. <a href="%s/join" style="color:#0b63b6;font-weight:bold;text-decoration:none">See the plans &rarr;</a></p></td></tr>' % (
              esc(b["url"]), bimg, esc(b["name"]), FONT, INK, NAVY, esc(b["name"]), esc(b["url"]), FONT, MUT, SITE))
    # members: update your listing + check your leads (owner 10/2)
    w('<tr><td style="padding:30px 28px 6px"><table role="presentation" width="100%%" cellpadding="0" cellspacing="0" border="0" style="background:#fff;border:2px solid %s;border-radius:16px">'
      '<tr><td style="padding:22px 22px 22px"><p style="margin:0 0 4px;font:bold 12px %s;letter-spacing:2px;text-transform:uppercase;color:#b36b00">For our member businesses</p>'
      '<p style="margin:0 0 8px;font:bold 20px/1.3 %s;color:%s">Our new look is live. Make your listing shine.</p>'
      '<p style="margin:0 0 12px;font:15px/1.55 %s;color:%s">Three Village Local just got a full redesign. Log in and update your photos, hours, description and services so neighbors see the best version of your business. Complete listings show up more in search and get more calls.</p>'
      '<p style="margin:0 0 16px;font:15px/1.55 %s;color:%s"><b style="color:%s">Check your leads.</b> When a neighbor reaches out through Three Village Local we email you right away from <b>admin@threevillagelocal.com</b>, and the subject line tells you it is a lead. Some members have missed these, so please add that address to your contacts or safe senders list and check your spam folder once in a while. You can also see every lead in your dashboard.</p>'
      '<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding-right:10px">%s</td><td>%s</td></tr></table></td></tr></table></td></tr>' % (
          GOLD, FONT, FONT, NAVY, FONT, INK, FONT, INK, NAVY, btn(SITE + "/login", "Log in and update &rarr;", bg=NAVY, fg="#fff"), btn(SITE + "/account/leads", "See my leads &rarr;")))
    # stories
    st = stories(1)
    if st:   # short version: one story, as a single line
        p = st[0]; href, title = SITE + "/" + p["post_filename"], html.unescape(p["post_title"])
        w('<tr><td style="padding:26px 28px 4px"><p style="margin:0 0 4px;font:bold 12px %s;letter-spacing:2px;text-transform:uppercase;color:#b36b00">Latest local story</p>'
          '<p style="margin:0;font:bold 18px/1.35 %s"><a href="%s" style="color:%s;text-decoration:none">%s &rarr;</a></p></td></tr>' % (FONT, FONT, esc(href), NAVY, esc(title)))
    # for businesses + app: folded into one compact strip
    w('<tr><td style="padding:26px 28px 4px"><table role="presentation" width="100%%" cellpadding="0" cellspacing="0" border="0" style="background:#fff;border:1px solid %s;border-radius:14px">'
      '<tr><td style="padding:16px 18px;font:15px/1.5 %s;color:%s"><b style="color:%s">Have an event, a special or news?</b> Send it to us and we will share it with the neighborhood. '
      '<a href="%s/promotion" style="color:#0b63b6;font-weight:bold;text-decoration:none">Send it in &rarr;</a></td></tr></table></td></tr>' % (LINE, FONT, INK, NAVY, SITE))
    w('<tr><td align="center" style="padding:18px 28px 0">'
      '<a href="%s/app"><img src="%s" width="120" alt="Download on the App Store" style="border:0;margin:0 4px"></a><a href="%s/app"><img src="%s" width="120" alt="Get it on Google Play" style="border:0;margin:0 4px"></a></td></tr>' % (
        SITE, P.get(os.path.join(ASSETS, "badges", "app-store-badge-v2.png"), "app-store", w=150, logo=True), SITE,
        P.get(os.path.join(ASSETS, "badges", "google-play-badge-v2.png"), "google-play", w=150, logo=True)))
    # footer
    w('<tr><td style="padding:26px 28px 28px;text-align:center"><p style="margin:0 0 6px;font:13px/1.6 %s;color:%s">You are getting this because you are a Three Village Local member business or you signed up for our newsletter.</p>'
      '<p style="margin:0;font:13px/1.6 %s;color:%s">%s &middot; <a href="%s" style="color:%s">threevillagelocal.com</a></p></td></tr>' % (FONT, MUT, FONT, MUT, MAILING_ADDRESS, SITE, MUT))
    w('</table></td></tr></table></body></html>')
    body = solid_bg("".join(o))
    out = os.path.join(HERE, "email", ed)
    os.makedirs(out, exist_ok=True)
    name = "email-vip-%s.html" % VIP_ID if VIP_ID else "email.html"
    open(os.path.join(out, name), "w", encoding="utf-8").write(body)
    rest = [e["title"] for e in picks if e is not lead]
    subj = "This weekend in Three Village: %s, %s and more" % (lead["title"], rest[0] if rest else "")
    open(os.path.join(out, "subject.txt"), "w", encoding="utf-8").write(subj + "\n")
    print("%s %d KB, %d pictures | subject: %s" % (name, len(body) // 1024, P.n, subj))


if __name__ == "__main__":
    main()
