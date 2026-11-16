"""VIP Member Dashboard - PREVIEW builder (owner 11/13/2026: Member Dashboard is VIP only).

    python site/member-dashboard/build.py              -> data/<uid>.json for every VIP + _local/<uid>.html previews
    python site/member-dashboard/build.py 115 499      -> only those members

Nothing is published and nothing is emailed. Design target = m_dash() in site/join-v2/build.py.
Rules baked in: shows what 3VL DID for the member, never GA4 visits/clicks; no em dashes; mobile-safe words.

Real data sources (all read-only):
  homepage   3vl-site-guard git history of post-sources/widget-17-3vl-page-now.html (Local Business Spotlight order, y-mc data-id)
  social     3vl-news-monitor social/scheduled/*.json + *.posted.json, social/featured-rotation.json
  email      3vl-site-guard data/weekly/<date>/featured.json + 3vl-news-monitor outbox/sent/*weekly-sending-<date>*
  banner     3vl-assets weekender/banners.json (VIP banner ad rotating sitewide)
  members    3vl-site-guard data/members.json, 3vl-assets weekender/vip.json
Not logged anywhere yet (shown as SAMPLE, clearly marked): quarterly article, VIP of the Week, mobile app push,
reels/videos, AI visibility fixes. See manual_log.example.json for the proposed log format.
"""
import datetime as dt, glob, html, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.environ.get("DOCS_DIR") or os.path.abspath(os.path.join(HERE, "..", "..", ".."))   # nightly job: repos side by side in DOCS_DIR
ASSETS = os.path.join(DOCS, "3vl-assets")
GUARD = os.environ.get("GUARD_DIR") or os.path.join(DOCS, "3vl-site-guard")
NEWS = os.path.join(DOCS, "3vl-news-monitor")
SHARE = "https://threevillagelocal-cloud.github.io/3vl-share/"
SITE = "https://www.threevillagelocal.com"
TODAY = dt.date.today()
e = lambda s: html.escape(str(s or ""), quote=True)


def jload(p, default=None):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return default


def slug(u):
    u = (u or "").split("?")[0].rstrip("/")
    return u.split("threevillagelocal.com/")[-1] if "threevillagelocal.com/" in u else ""


def floor_k(n):
    """Friendly rounding (owner 11/15/2026): totals round DOWN to the thousand, so 12,263 -> 12,000. Never rounds up."""
    n = int(n or 0)
    return (n // 1000) * 1000 if n >= 1000 else n


def nice(n, plus=True):
    """12,263 -> '12,000+' ; 640 -> '640'. Callers hide anything under their floor, so '0' never renders."""
    n = int(n or 0)
    return ("{:,}".format(floor_k(n)) + ("+" if plus and n >= 1000 else "")) if n >= 1000 else "{:,}".format(n)


# Floor rule (owner 11/15/2026): a weak or zero number is never shown. The card or row is hidden instead.
FLOOR_REACH = 1000    # last-30-days reach total under this -> the reach card is hidden
FLOOR_HOME_VIEWS = 100   # homepage views on spotlight days under this -> show the day count only, no view number
FLOOR_NET_VIEWS = 1000   # network page views under this -> row hidden
FLOOR_SUBS = 100      # weekly subscribers under this -> row hidden
FLOOR_HL = 10         # VIP highlights under this -> row hidden


def fmt(d):
    return "%s %d" % (d.strftime("%b"), d.day)


# ---------------------------------------------------------------- members
def vips(plans=("vip",)):
    mem = jload(os.path.join(GUARD, "data", "members.json"), {}).get("members", [])
    short = {str(v["id"]): v for v in jload(os.path.join(ASSETS, "weekender", "vip.json"), [])}
    out = {}
    for m in mem:
        if m.get("plan") not in plans:
            continue
        uid = str(m["id"])
        s = short.get(uid, {})
        out[uid] = {"tier": "v" if m.get("plan") == "vip" else "f", "uid": uid, "name": m["name"], "short": s.get("name") or m["name"], "cat": m.get("category") or s.get("cat") or "",
                    "town": m.get("city") or "", "url": m["url"], "slugs": {slug(m["url"]), slug(s.get("url"))} - {""}}
    return out


def member_images(uid):
    """logo + banner from the member's v3 profile files in 3vl-share (local checkout), with fallbacks"""
    img = os.path.join(DOCS, "3vl-share", "live", "p3", "vip", "img")
    have = set(os.listdir(img)) if os.path.isdir(img) else set()
    logo = next((SHARE + "live/p3/vip/img/" + f for f in ("%s-v3-logo.png" % uid, "%s-logo.png" % uid, "%s-logo.webp" % uid) if f in have), "")
    ban = next((SHARE + "live/p3/vip/img/" + f for f in ("%s-banner-900.webp" % uid, "%s-banner2-900.webp" % uid, "%s-hero-900.webp" % uid,
                                                          "%s-banner.webp" % uid, "%s-hero.webp" % uid) if f in have), "")
    t = os.path.join(DOCS, "3vl-share", "t")
    th = sorted(glob.glob(os.path.join(t, "vip-%s-*-t240.webp" % uid)))
    thumb = SHARE + "t/" + os.path.basename(th[0]) if th else ban
    return logo, ban, thumb


# ---------------------------------------------------------------- homepage (git history of the nightly homepage)
def homepage_history():
    cache_p = os.environ.get("HP_CACHE") or os.path.join(HERE, "_cache", "homepage.json")
    cache = jload(cache_p, {}) or {}
    f = "post-sources/widget-17-3vl-page-now.html"
    log = subprocess.run(["git", "-C", GUARD, "log", "--format=%H %cd", "--date=format-local:%Y-%m-%d", "--", f],
                         capture_output=True, text=True, encoding="utf-8").stdout.split("\n")
    by_day = {}
    for ln in log:
        if not ln.strip():
            continue
        sha, day = ln.split()
        by_day.setdefault(day, []).append(sha)   # newest first within the day
    days = {}
    for day, shas in sorted(by_day.items()):
        for sha in shas:
            if sha not in cache:
                s = subprocess.run(["git", "-C", GUARD, "show", "%s:%s" % (sha, f)], capture_output=True, text=True, encoding="utf-8").stdout
                cache[sha] = re.findall(r'class="y-mc" href="[^"]*" data-id="(\d+)"', s)
            if cache[sha]:
                days[day] = cache[sha]
                break
    os.makedirs(os.path.dirname(cache_p), exist_ok=True)
    json.dump(cache, open(cache_p, "w", encoding="utf-8"))
    return days   # {"2026-11-13": ["78","115",...]} order = spotlight order (first = the day's opening card)


# ---------------------------------------------------------------- weekly email
def weekly_issues():
    sent_dir = os.path.join(NEWS, "outbox", "sent")
    names = os.listdir(sent_dir) if os.path.isdir(sent_dir) else []
    out = []
    for p in sorted(glob.glob(os.path.join(GUARD, "data", "weekly", "*", "featured.json"))):
        date = os.path.basename(os.path.dirname(p))
        sent = any("weekly-sending-%s" % date in n for n in names)
        notsent = any("weekly-notsent-%s" % date in n for n in names)
        status = "sent" if sent else ("skipped" if notsent else "pending")
        f = dict(jload(p, {}) or {})
        for n in names:   # "going out right now to 288 people" in the send notice
            if "weekly-sending-%s" % date in n:
                m = re.search(r"to (\d[\d,]*) people", (jload(os.path.join(sent_dir, n), {}) or {}).get("html", ""))
                if m:
                    f["_recipients"] = int(m.group(1).replace(",", ""))
        out.append((date, status, f))
    return out


# ---------------------------------------------------------------- social
def social_posts():
    d = os.path.join(NEWS, "social", "scheduled")
    out = []
    for p in sorted(glob.glob(os.path.join(d, "*.json"))):
        if p.endswith(".posted.json"):
            continue
        j = jload(p, {})
        posted = jload(p[:-5] + ".posted.json")
        out.append((os.path.basename(p)[:-5], j, posted))
    return out


def rotation():
    return jload(os.path.join(NEWS, "social", "featured-rotation.json"), {}).get("rotation", [])


# ---------------------------------------------------------------- banner start dates + member articles
def banner_since():
    """{uid: first date the member's VIP banner appeared in weekender/banners.json} from git history (oldest first)."""
    f = "weekender/banners.json"
    log = subprocess.run(["git", "-C", ASSETS, "log", "--reverse", "--format=%H %cd", "--date=format-local:%Y-%m-%d", "--", f],
                         capture_output=True, text=True, encoding="utf-8").stdout.split("\n")
    since = {}
    for ln in log:
        if not ln.strip():
            continue
        sha, day = ln.split()
        raw = subprocess.run(["git", "-C", ASSETS, "show", "%s:%s" % (sha, f)], capture_output=True, text=True, encoding="utf-8").stdout
        try:
            ids = {str(b.get("id")) for b in json.loads(raw)}
        except Exception:
            continue
        for i in ids:
            since.setdefault(i, day)
    return since


def member_articles(m):
    """Articles about or by the member that we published (homepage extra stories with a byline)."""
    out = []
    names = {m["short"].lower(), m["name"].lower()}
    for x in jload(os.path.join(ASSETS, "weekender", "front", "extra_stories.json"), []) or []:
        txt = (x.get("t", "") + " " + x.get("by", "") + " " + x.get("h", "")).lower()
        if any(n and n in txt for n in names) or any(sl and sl in x.get("h", "") for sl in m["slugs"]):
            out.append({"date": x["date"], "ch": "web", "icon": "article", "thumb": x.get("img", ""), "title": "Your article on our homepage and blog",
                        "note": x.get("t", ""), "url": x.get("h", "")})
    return out


# ---------------------------------------------------------------- sample (not logged yet)
def samples(m):
    """Placeholders for things we do not log yet. Every one carries sample=True and is badged SAMPLE on the page."""
    return [
        {"date": "2026-11-03", "ch": "ai", "icon": "sparkle", "title": "AI visibility check: 3 fixes done", "note": "Hours, services and FAQs tuned so ChatGPT and Google AI describe you right", "sample": True},
        {"date": "2026-11-05", "ch": "web", "icon": "bell", "title": "Mobile app push notification sent", "note": "Your news, straight to local phones", "sample": True},
    ], [
        {"date": "2026-11-16", "icon": "crown", "title": "VIP of the Week on our homepage", "note": "Nov 16 to 22, in rotation with the other VIPs", "sample": True},
        {"date": "2026-12-04", "icon": "article", "title": "Your quarterly article", "note": "Written, designed and published by our team", "sample": True},
    ]


# ---------------------------------------------------------------- per-member activity
def activity(m, hp, issues, posts, rot, banners, bsince=None):
    uid, items, upcoming = m["uid"], [], []
    logo, ban, thumb = member_images(uid)
    names = [m["short"].lower(), m["name"].lower().split(" at ")[0].split(",")[0]]

    # homepage: one row per week, plus counts per month
    hp_month = {}
    hp_days = []
    weeks = {}
    for day, ids in sorted(hp.items()):
        if uid not in ids:
            continue
        d = dt.date.fromisoformat(day)
        mk = day[:7]
        hm = hp_month.setdefault(mk, {"days": 0, "lead": 0})
        hm["days"] += 1
        hp_days.append(day)
        lead = ids[0] == uid
        hm["lead"] += lead
        wk = d - dt.timedelta(days=d.weekday())
        w = weeks.setdefault((wk, mk), {"days": [], "lead": []})
        w["days"].append(d)
        if lead:
            w["lead"].append(d)
    for wk, w in sorted(weeks.items()):
        a, b = w["days"][0], w["days"][-1]
        span = fmt(a) if a == b else "%s to %s" % (fmt(a), fmt(b) if a.month != b.month else str(b.day))
        note = ("Your card in the Local Business Spotlight, every day %s" if a != b else "Your card in the Local Business Spotlight on %s") % span
        if w["lead"]:
            note += ". You opened the spotlight on %s" % ", ".join(fmt(x) for x in w["lead"])
        items.append({"date": b.isoformat(), "ch": "web", "icon": "home", "thumb": thumb, "title": "On our homepage, %d day%s" % (len(w["days"]), "" if len(w["days"]) == 1 else "s"),
                      "note": note, "url": SITE + "/", "n_home": len(w["days"])})

    # weekly email
    for date, status, f in issues:
        hit = None
        if uid in [str(x) for x in f.get("vip", [])]:
            hit = ("Featured neighbor in Three Village Weekly", "Your photo, story and one-tap call in our weekly email")
        elif uid in [str(x) for x in f.get("new", [])]:
            hit = ("Welcomed in Three Village Weekly", "Introduced to local subscribers as a new member")
        else:
            for s in f.get("specials", []):
                if slug(s.get("profile")) in m["slugs"]:
                    hit = ("Your special in Three Village Weekly", s.get("title") or "")
                    break
        if not hit:
            continue
        row = {"date": date, "ch": "email", "icon": "mail", "title": hit[0], "note": hit[1], "recipients": f.get("_recipients", 0)}
        if status == "sent":
            items.append(row)
        elif status == "pending" and dt.date.fromisoformat(date) >= TODAY - dt.timedelta(days=2):
            row["title"] = row["title"].replace("Featured neighbor in", "Featured neighbor in this week's")
            row["note"] = "Going out to local subscribers this week"
            upcoming.append(row)

    # social posts (posted + scheduled)
    seen = set()
    for pid, j, posted in posts:
        title = (j.get("title") or "").lower()
        if slug(j.get("article")) not in m["slugs"] and not any(n and n in title for n in names):
            continue
        if any(n and re.search(r"\b(no|without|minus)\s+" + re.escape(n), title) for n in names):   # a post that explicitly left them out
            continue
        when = (j.get("when") or "")[:10]
        kind = pid.split("-")[0]
        key = (kind, when)
        if key in seen:
            continue
        seen.add(key)
        r = next((x for x in rot if str(x.get("uid")) == uid and x.get("date") == when), None)
        fb = bool(posted and posted.get("Facebook Page")) or bool(r and r.get("status") == "posted")
        ttl = {"spotlight": "VIP Spotlight on Instagram%s" % (" and Facebook" if fb or not posted else ""),
               "welcome": "Welcome to Three Village Local post", "featured": "Featured spotlight post"}.get(kind, j.get("title") or "Social post")
        if kind not in ("spotlight", "welcome", "featured"):
            ttl = re.sub(r"\s*\([^)]*\)", "", ttl).strip()   # internal notes in parentheses never reach members
            for n in (m["short"], m["name"]):
                if ttl.lower().startswith(n.lower()):
                    ttl = "Your" + ttl[len(n):]
                    break
        bits = []
        if j.get("tags") and j["tags"] != "[]":
            bits.append("tagged")
        if j.get("collaborators"):
            bits.append("collab invite")
        note = "Posted on our Facebook and Instagram" if fb else "Posted on our Instagram"
        if bits:
            note += ", " + " and ".join(bits)
        row = {"date": when, "ch": "social", "icon": "insta", "thumb": j.get("ig_image") or "", "title": ttl, "note": note,
               "url": (posted or {}).get("Instagram") or ""}
        if posted:
            items.append(row)
        elif when and dt.date.fromisoformat(when) >= TODAY:
            row["note"] = "Scheduled for %s at noon, Facebook and Instagram" % fmt(dt.date.fromisoformat(when))
            upcoming.append(row)
    for r in rot:   # planned spotlights that do not have a post file yet
        if str(r.get("uid")) == uid and r.get("status") in ("planned", "scheduled") and dt.date.fromisoformat(r["date"]) >= TODAY \
                and ("spotlight", r["date"]) not in seen:
            upcoming.append({"date": r["date"], "ch": "social", "icon": "insta", "title": "VIP Spotlight on Facebook and Instagram",
                             "note": "Planned for %s at noon" % fmt(dt.date.fromisoformat(r["date"]))})

    # VIP banner ad (rotating on every page since it went up) + articles we published for them
    if uid in banners and (bsince or {}).get(uid):
        items.append({"date": bsince[uid], "ch": "web", "icon": "banner", "title": "Your banner ad went up on every page",
                      "note": "Rotating across the whole Three Village Local website ever since", "n_banner": 1})
    items += member_articles(m)

    smp_done, smp_next = ([], []) if LIVE else samples(m)
    items += smp_done
    upcoming += smp_next
    items.sort(key=lambda x: x["date"], reverse=True)
    upcoming.sort(key=lambda x: x["date"])

    # month summaries (real items only; samples never count)
    months = {}
    for it in items:
        mk = it["date"][:7]
        s = months.setdefault(mk, {"home_days": 0, "home_lead": 0, "social": 0, "email": 0, "total": 0})
        if not it.get("sample") and it["ch"] in ("social", "email"):
            s[it["ch"]] += 1
    for mk, hm in hp_month.items():
        s = months.setdefault(mk, {"home_days": 0, "home_lead": 0, "social": 0, "email": 0, "total": 0})
        s["home_days"], s["home_lead"] = hm["days"], hm["lead"]
    for s in months.values():
        s["total"] = s["home_days"] + s["social"] + s["email"]
    nxt_social = next((u for u in upcoming if u.get("ch") == "social"), None)
    # lifetime promotions: every homepage day, post, email feature, article and the banner placement (real items only)
    lifetime = sum(it.get("n_home", 0) or (0 if it.get("sample") else 1) for it in items)
    return {"tier": m.get("tier", "v"), "hp_days": hp_days, "uid": uid, "name": m["name"], "short": m["short"], "cat": m["cat"], "town": m["town"], "profile": m["url"],
            "logo": logo, "banner": ban, "has_banner_ad": uid in banners, "banner_img": banners.get(uid, ""), "months": months, "items": items, "upcoming": upcoming,
            "next_social": nxt_social and nxt_social["date"], "lifetime": lifetime, "built": dt.datetime.now().isoformat(timespec="minutes")}


# ---------------------------------------------------------------- render
_src = open(os.path.join(HERE, "..", "svc-kit", "kit.py"), encoding="utf-8").read()
I = eval(_src[_src.index("_I = {") + 5:_src.index("\n}\n", _src.index("_I = {")) + 2])
I.update({
    "insta": '<rect x="2" y="2" width="20" height="20" rx="5.5"/><circle cx="12" cy="12" r="4.2"/><path d="M17.6 6.4h.01"/>',
    "bell": '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.9 1.9 0 0 0 3.4 0"/>',
    "crown": '<path d="m3 17 1.5-10 4.5 4 3-6 3 6 4.5-4L21 17z"/><path d="M3 21h18"/>',
    "banner": '<rect x="2" y="6" width="20" height="12" rx="2"/><path d="M6 10h7M6 14h4"/><circle cx="17.5" cy="12" r="2"/>',
    "lock": '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
    "chev": '<path d="m9 6 6 6-6 6"/>',
    "percent": '<path d="M19 5 5 19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/>',
    "ext": '<path d="M14 4h6v6"/><path d="M10 14 20 4"/><path d="M19 13v6a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h6"/>',
})
USED = []


def ic(n, cls=""):
    if n not in USED:
        USED.append(n)
    return '<svg class="md-svg%s" aria-hidden="true" focusable="false"><use href="#mdi-%s"/></svg>' % ((" " + cls) if cls else "", n)


def sprite():
    return ('<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>' + "".join(
        '<symbol id="mdi-%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">%s</symbol>'
        % (n, I[n]) for n in USED) + '</defs></svg>')


# Owner exception 11/13/2026 to the no-raw-traffic rule, for this ONE stat. {n} = data/banner_reach.json "views"
# (sitewide GA4 page views, last 30 days, refreshed nightly by banner_reach.py). Change wording here only.
BANNER_LABEL = "Your banner ad may have been seen up to {n} times in the past 30 days"
# Month-over-month % (last 30 days vs the 30 before, real GA4) shows only when it is UP; a drop hides the pill (owner OK pending).
AI_LINE = "Plus AI assistants like ChatGPT, Gemini and Google AI read our pages to recommend local businesses."   # no number, owner 11/13
BANNER_LIVE_URL =SHARE + "live/member-dashboard/banner_reach.json"   # where the nightly job would publish it (not live yet)
LOGO3VL = ("https://threevillagelocal-cloud.github.io/3vl-share/live/md/3vl-navy-440.webp" if "--live" in sys.argv else "../img/3vl-navy-440.webp")   # official navy lockup
RAW = "https://raw.githubusercontent.com/threevillagelocal-cloud/3vl-assets/master/weekender/"


def banner_card(a):
    r = jload(os.path.join(HERE, "data", "banner_reach.json"), {}) or {}
    n = floor_k(r.get("views") or 0)
    if not (a["has_banner_ad"] and n >= 1000):   # floor rule
        return ""
    pre, post = BANNER_LABEL.split("{n}")
    pic = ('<img class="md-ban-img" src="%s" alt="Your banner ad" width="180" height="150" loading="lazy" decoding="async" data-processed="true">' % e(RAW + a["banner_img"])) if a.get("banner_img") else ""
    pct = r.get("change_pct")
    chg = ('<em class="md-ban-up" data-ban-pct>Up %d%% vs the 30 days before</em>' % pct) if isinstance(pct, int) and pct > 0 else '<em class="md-ban-up" data-ban-pct hidden></em>'
    return ('<div class="md-ban" data-live="%s">%s<div class="md-ban-t"><p class="md-ban-k">%s Your banner ad</p>'
            '<p class="md-ban-n"><b data-n="%d" data-ban-n>%s</b>%s</p><p class="md-ban-l">%s<span data-ban-n2>%s</span>%s</p>'
            '<p class="md-ban-ai">%s %s</p></div></div>'
            % (e(BANNER_LIVE_URL), pic, ic("banner"), n, "{:,}".format(n), chg, e(pre), "{:,}".format(n), e(post), ic("sparkle"), e(AI_LINE)))


LIVE = "--live" in sys.argv or "--live-preview" in sys.argv   # --live-preview: live content rules, local files only
WRITE_LIVE = "--live" in sys.argv
LIVE_DIR = os.path.join(os.path.dirname(ASSETS), "3vl-share", "live", "md")
SAMPLE = '<em class="md-sample" title="Placeholder: we do not log this yet">Sample</em>'
MONTHS = {"2026-10": "October", "2026-11": "November", "2026-12": "December"}

W0 = (TODAY - dt.timedelta(days=30)).isoformat()   # rolling last-30-days window start


def reach30(a):
    """Rolling last 30 days: real reach we can measure, broken down. Banner = sitewide page views (a ceiling, so 'up to')."""
    r = jload(os.path.join(HERE, "data", "banner_reach.json"), {}) or {}
    home_daily = r.get("home_daily", {})
    banner = int(r.get("views", 0)) if a["has_banner_ad"] else 0
    days = [d for d in a.get("hp_days", []) if d >= W0]
    home = sum(home_daily.get(d, 0) for d in days)
    emails = [it for it in a["items"] if it["ch"] == "email" and it["date"] >= W0 and not it.get("sample")]
    email = sum(it.get("recipients", 0) for it in emails)
    social = [it for it in a["items"] if it["ch"] == "social" and it["date"] >= W0 and not it.get("sample")]
    total = banner + home + email
    if total < FLOOR_REACH:   # floor rule: a weak month hides the whole card (the timeline still shows what we did)
        return ""
    banner, total = floor_k(banner), floor_k(total)
    parts = []
    if banner:
        parts.append(("banner", "Banner ad", "up to %s views" % "{:,}".format(banner)))
    if days:
        pl = "" if len(days) == 1 else "s"
        parts.append(("home", "Homepage spotlight", ("%s views on your %d day%s" % (nice(home), len(days), pl)) if home >= FLOOR_HOME_VIEWS
                      else "Featured %d day%s" % (len(days), pl)))
    if emails:
        parts.append(("mail", "Three Village Weekly", "sent to %s subscribers" % nice(email) if email >= FLOOR_SUBS else "%d feature%s" % (len(emails), "" if len(emails) == 1 else "s")))
    if social:
        parts.append(("insta", "Facebook and Instagram", "%d post%s about you" % (len(social), "" if len(social) == 1 else "s")))
    rows = "".join('<li><span class="md-ic">%s</span><b>%s</b><em>%s</em></li>' % (ic(i), t, v) for i, t, v in parts)
    return ('<div class="md-kpis md-reach" data-m="r30"><div class="md-reach-tot"><span class="md-ic">%s</span><b>%s<span data-n="%d" data-plus="%s">%s</span></b>'
            '<i>Times neighbors may have seen your business in the last 30 days</i></div><ul class="md-reach-l">%s</ul></div>'
            % (ic("megaphone"), "Up to " if banner else "", total, "" if banner else "+", "{:,}".format(total) + ("" if banner or total < 1000 else "+"), rows))


def kpis(a, mk):
    s = a["months"].get(mk, {"home_days": 0, "home_lead": 0, "social": 0, "email": 0, "total": 0})
    t = []
    t.append(('<div class="md-kpi"><span class="md-ic">%s</span><b><span data-n="%d">%d</span></b><i>Times we put you in front of neighbors in %s</i></div>'
              % (ic("megaphone"), s["total"], s["total"], MONTHS.get(mk, mk))))
    lead = ' <small>Opened it %d day%s</small>' % (s["home_lead"], "" if s["home_lead"] == 1 else "s") if s["home_lead"] else ""
    t.append('<div class="md-kpi"><span class="md-ic">%s</span><b><span data-n="%d">%d</span></b><i>Days in our homepage Business Spotlight%s</i></div>'
             % (ic("home"), s["home_days"], s["home_days"], lead))
    if s["social"] or s["email"]:
        t.append('<div class="md-kpi"><span class="md-ic">%s</span><b><span data-n="%d">%d</span></b><i>Social posts and email features about you</i></div>'
                 % (ic("insta"), s["social"] + s["email"], s["social"] + s["email"]))
    elif a["next_social"] and mk == TODAY.strftime("%Y-%m"):
        d = dt.date.fromisoformat(a["next_social"])
        t.append('<div class="md-kpi md-kpi-next"><span class="md-ic">%s</span><b>%s</b><i>Your next social spotlight: scheduled</i></div>' % (ic("insta"), fmt(d)))
    else:
        t.append('<div class="md-kpi"><span class="md-ic">%s</span><b>100,000+</b><i>Monthly Facebook and Instagram views our posts reach</i></div>' % ic("share"))
    if LIVE:   # no sample tiles on live dashboards
        if a["has_banner_ad"]:
            t.append('<div class="md-kpi"><span class="md-ic">%s</span><b>Every page</b><i>Your banner ad rotates across the whole website</i></div>' % ic("banner"))
        elif "100,000+" not in "".join(t):
            t.append('<div class="md-kpi"><span class="md-ic">%s</span><b>100,000+</b><i>Monthly Facebook and Instagram views our posts reach</i></div>' % ic("share"))
    else:
        t.append('<div class="md-kpi md-kpi-art"><span class="md-ic">%s</span><b>Dec 4</b><i>Your next quarterly article: scheduled %s</i>'
                 '<span class="md-bar"><u style="--p:72%%"></u></span></div>' % (ic("article"), SAMPLE))
    return '<div class="md-kpis" data-m="%s"%s>%s</div>' % (mk, "" if mk == TODAY.strftime("%Y-%m") else " hidden", "".join(t))


def row(it):
    th = ('<img class="md-th" src="%s" alt="" width="88" height="88" loading="lazy" decoding="async" data-processed="true">' % e(it["thumb"])
          if it.get("thumb") else '<span class="md-th md-th-ic md-th-%s">%s</span>' % (it["ch"], ic(it["icon"])))
    d = dt.date.fromisoformat(it["date"])
    link = ('<a class="md-open" href="%s" target="_blank" rel="noopener">See it %s</a>' % (e(it["url"]), ic("ext"))) if it.get("url") else ""
    return ('<li data-f="%s" data-m="%s"><span class="md-dot">%s</span>%s<div class="md-txt"><b>%s%s</b><i>%s</i>%s</div><time datetime="%s">%s</time></li>'
            % (it["ch"], "r30" if it["date"] >= W0 else "old", ic(it["icon"]), th, e(it["title"]), SAMPLE if it.get("sample") else "", e(it["note"]), link, it["date"], fmt(d)))


def timeline(a, ai):
    """'What we did for you': every real promotion, newest first, plus a lifetime count. Only grows. Hidden when empty (floor rule)."""
    real = [it for it in a["items"] if not it.get("sample")] if LIVE else a["items"]
    if not real:
        return ""
    n = a.get("lifetime") or len(real)
    chans = sorted({it["ch"] for it in real})
    chips = '<button type="button" class="on" data-f="all" aria-pressed="true">All</button>' + "".join(
        '<button type="button" data-f="%s" aria-pressed="false">%s</button>' % (c, l) for c, l in
        (("web", "Website"), ("social", "Social"), ("email", "Email"), ("ai", "AI")) if c in chans and (ai or c != "ai"))
    since = ('<p class="md-life"><b>%d promotions</b> for you since you joined</p>' % n) if n >= 3 else ""
    return ('<div class="md-card md-tl"><div class="md-ch"><b>What we did for you</b>'
            '<div class="md-chips" role="group" aria-label="Filter the list">%s</div></div>%s'
            '<ol class="md-list">%s</ol><p class="md-empty" hidden>More on the way.</p></div>'
            % (chips if len(chans) > 1 else "", since, "".join(row(it) for it in real)))


def page(a):
    if a.get("tier") == "f":
        return page_featured(a)
    USED.clear()
    cur = TODAY.strftime("%Y-%m")
    mtabs = '<div class="md-mtabs" role="group" aria-label="Choose a month"><button type="button" data-m="r30" aria-pressed="true" class="on">Last 30 days</button></div>'   # rolling window (owner 11/13)
    tiles = reach30(a)
    if not tiles:   # floor rule hid the reach card: no orphan period tab
        mtabs = ""
    vip = ['<span>%s<span><b>Top-spot card</b> at the top of %s search</span></span>' % (ic("search"), e(a["cat"] or "your category"))]
    if a["has_banner_ad"]:
        vip.insert(0, '<span>%s<span><b>Banner ad</b> rotating on every page</span></span>' % ic("banner"))
    if not LIVE:
        vip.append('<span>%s<span><b>VIP of the Week</b> Nov 16 to 22</span>%s</span>' % (ic("crown"), SAMPLE))
        vip.append('<span>%s<span><b>Push notification</b> 1 left this month</span>%s</span>' % (ic("bell"), SAMPLE))
    rows = "".join(row(it) for it in a["items"])
    up = "".join('<li><span class="md-up-d"><b>%s</b><i>%s</i></span><div><b>%s%s</b><i>%s</i></div></li>' % (
        dt.date.fromisoformat(u["date"]).strftime("%b"), dt.date.fromisoformat(u["date"]).day, e(u["title"]), SAMPLE if u.get("sample") else "", e(u["note"]))
                 for u in a["upcoming"][:5])
    if not up:
        up = '<li><span class="md-up-d"><b>%s</b><i>&#8226;</i></span><div><b>More on the way</b><i>Have news, a special or an event? Reply to us at hello@threevillagelocal.com and we will promote it.</i></div></li>' % TODAY.strftime("%b")
    news = [("Just launched", "Homepage trivia: neighbors play every Monday, with local business prizes."),
            ("Live now", "Our Thanksgiving guide is up. Send us your holiday hours and specials and we will add them."),
            ("New for VIPs", "20% off all of our services: promo videos, websites, AI search work and drone.")]
    nl = "".join('<li><em>%s</em><span>%s</span></li>' % x for x in news)
    ups = [("video", "Promo reel", "Filmed and edited for you", "/services#tvp-video"),
           ("globe", "AI website", "Built to be found on Google and AI", "/websites"),
           ("sparkle", "AI visibility report", "See how AI tools describe you", "/free-ai-report"),
           ("camera", "Drone photos and video", "Included with VIP, book a shoot", "/services")]
    upl = services_list("v")
    first = a["short"]
    logo = ('<span class="md-logo"><img src="%s" alt="%s logo" width="168" height="100" decoding="async" data-processed="true"></span>' % (e(a["logo"]), e(first))) if a["logo"] else ""
    out = ('<div class="md" id="md" data-tier="v">'
           '<div class="md-top"><img src="%s" alt="Three Village Local" width="132" height="45" class="md-3vl" data-processed="true">'
           '<span class="md-brand">Member Dashboard</span><span class="md-sign">%s Signed in</span></div>'
           '<div class="md-hi"%s><div class="md-hi-in">%s<div><p class="md-k">%s VIP member</p><h1 class="md-h">Welcome back, %s</h1>'
           '<p class="md-s">Here is everything Three Village Local did for you.</p></div></div>'
           '<a class="md-prof" href="%s" target="_blank" rel="noopener">View your profile %s</a></div>'
           '%s%s%s'
           '<div class="md-vipstrip">%s</div>%s'
           '<div class="md-grid">%s'
           '<div class="md-side"><div class="md-card"><div class="md-ch"><b>Coming up for you</b></div><ul class="md-upc">%s</ul></div>'
           '<div class="md-card"><div class="md-ch"><b>What&#39;s new at 3VL</b></div><ul class="md-news">%s</ul></div></div>'
           '<div class="md-card md-grow"><div class="md-ch"><b>Grow with us</b><i>VIP pricing</i></div><div class="md-ups">%s</div></div></div>'
           '<p class="md-foot">Questions or something to promote? Email <a href="mailto:hello@threevillagelocal.com">hello@threevillagelocal.com</a> and we will get it out there.</p>'
           '</div>') % (LOGO3VL, ic("lock"), (' style="--ban:url(%s)"' % e(a["banner"])) if a["banner"] else "", logo, ic("crown"), e(first), e(a["profile"]), ic("chev"),
                        banner_card(a), mtabs, tiles, "".join(vip), net_card(), timeline(a, True), up, nl, upl)
    return sprite() + nowrap_hyphens(out)


# ---------------------------------------------------------------- all-member pieces (owner 11/13: every member gets the new dashboard)
NET = {}   # filled in main(): network stats shown to every member


def services_list(tier):
    off = {"v": "20% off", "f": "10% off", "b": ""}[tier]
    ups = [("video", "Promo reel", "Filmed and edited for you", "/services#tvp-video"),
           ("bot", "AI chatbot", "Answers customers 24/7, texts you leads", "/ai-assistant"),
           ("globe", "AI website", "Built to be found on Google and AI", "/websites"),
           ("sparkle", "AI visibility report", "See how AI tools describe you", "/free-ai-report"),
           ("camera", "Drone photos and video", "Included with VIP, book a shoot" if tier == "v" else "Aerial photos and video of your business", "/services")]
    return "".join('<a class="md-upb" href="%s"><span class="md-ic">%s</span><div><b>%s</b><i>%s</i></div>%s</a>' % (
        SITE + h, ic(i), t, d, ("<em>%s</em>" % ("Included" if (tier == "v" and "Included" in d) else off)) if off else '<em class="md-go">See it</em>')
        for i, t, d, h in ups)


FB_LOGO = ('<svg class="md-brandlogo" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="12" fill="#1877F2"/>'
           '<path fill="#fff" d="M15.1 12.9l.4-2.8h-2.7V8.3c0-.8.4-1.5 1.6-1.5h1.2V4.4s-1.1-.2-2.2-.2c-2.2 0-3.7 1.3-3.7 3.8v2.1H7.3v2.8h2.4V24h3.1V12.9z"/></svg>')
IG_LOGO = ('<svg class="md-brandlogo" viewBox="0 0 24 24" aria-hidden="true"><defs><radialGradient id="mdig" cx="30%" cy="107%" r="150%">'
           '<stop offset="0" stop-color="#fdf497"/><stop offset=".05" stop-color="#fdf497"/><stop offset=".45" stop-color="#fd5949"/>'
           '<stop offset=".6" stop-color="#d6249f"/><stop offset=".9" stop-color="#285AEB"/></radialGradient></defs>'
           '<rect width="24" height="24" rx="6.5" fill="url(#mdig)"/><rect x="5.5" y="5.5" width="13" height="13" rx="4" fill="none" stroke="#fff" stroke-width="1.8"/>'
           '<circle cx="12" cy="12" r="3.1" fill="none" stroke="#fff" stroke-width="1.8"/><circle cx="16.3" cy="7.7" r="1.05" fill="#fff"/></svg>')


def social_li():
    """Real Meta numbers, last 28 days (Meta's insights window): FB page_media_view + IG views, from 3vl-news-monitor data/hq/social.json."""
    d = jload(os.path.join(NEWS, "data", "hq", "social.json"), {}) or {}
    fb = int(((d.get("fb") or {}).get("cur") or {}).get("page_media_view") or 0)
    ig = int(((d.get("ig") or {}).get("cur") or {}).get("views") or 0)
    nf = nice
    if (fb + ig) < 1000:
        return '<li><span class="md-ic">%s</span><b>100,000+</b><i>Facebook and Instagram views our posts reach every month</i></li>' % ic("share")
    return ('<li class="md-soc"><b>%s</b><i>Facebook and Instagram views in the last 28 days</i>'
            '<span class="md-soc-r">%s<em>%s</em></span><span class="md-soc-r">%s<em>%s</em></span></li>'
            % (nf(fb + ig), FB_LOGO, nf(fb), IG_LOGO, nf(ig)))


def net_card():
    n = NET
    up = ('<small>Up %d%%</small>' % n["pct"]) if isinstance(n.get("pct"), int) and n["pct"] > 0 else ""   # never a negative (owner 11/15)
    st = [("social", "", "")]
    if int(n.get("views") or 0) >= FLOOR_NET_VIEWS:
        st.insert(0, ("chart", nice(n["views"]), "Website page views in the last 30 days" + (" " + up if up else "")))
    if int(n.get("vip_hl") or 0) >= FLOOR_HL:
        st.append(("crown", nice(n["vip_hl"]), "Times we highlighted our VIP members in the last 30 days"))
    if int(n.get("subs") or 0) >= FLOOR_SUBS:
        st.append(("mail", nice(n["subs"]), "Neighbors who get Three Village Weekly by email"))
    li = "".join(social_li() if i == "social" else '<li><span class="md-ic">%s</span><b>%s</b><i>%s</i></li>' % (ic(i), v, t) for i, v, t in st)
    return ('<div class="md-card md-net"><div class="md-ch"><b>Three Village Local right now</b><i>Updated nightly</i></div>'
            '<ul class="md-net-l">%s</ul></div>' % li)


def upsell(tier):
    vip = ('<div class="md-sell md-sell-v"><p class="md-k">%s Three Village VIP</p><b>Be seen everywhere in Three Village</b>'
           '<p>Your banner ad on every page, the top spot in search, homepage spotlights, a custom article every quarter and this full dashboard of everything we did for you.</p>'
           '<div class="md-sell-b"><a class="md-btn md-btn-gold" href="/join#plan-vip" data-vip-pop>See what VIP gets you</a>'
           '<a class="md-btn md-btn-line" href="/checkout/1">Request VIP</a></div><small>Only 3 VIP spots per category</small></div>') % ic("crown")
    if tier == "f":
        return vip
    fea = ('<div class="md-sell md-sell-f"><p class="md-k">%s Featured</p><b>Get found first</b>'
           '<p>A premium profile with video, priority placement above free listings, category spotlights, your Instagram specials in our feeds and 10%% off our services.</p>'
           '<div class="md-sell-b"><a class="md-btn md-btn-blue" href="/checkout/2">Upgrade to Featured</a><a class="md-btn md-btn-line" href="/join">Compare plans</a></div></div>') % ic("star")
    return fea + vip


def news_list(tier):
    news = [("Just launched", "Homepage trivia: neighbors play every Monday, with local business prizes."),
            ("Live now", "Our Thanksgiving guide is up. Send us your holiday hours and specials and we will add them.")]
    news.append(("For VIPs", "20% off all of our services: promo videos, websites, AI search work and drone.") if tier == "v"
                else ("For members", "Send us your news, specials and events at hello@threevillagelocal.com and we will help promote them."))
    return "".join('<li><em>%s</em><span>%s</span></li>' % x for x in news)


def head(kicker, title, sub, profile="", logo="", ban=""):
    lg = ('<span class="md-logo"><img src="%s" alt="" width="168" height="100" decoding="async" data-processed="true"></span>' % e(logo)) if logo else ""
    prof = ('<a class="md-prof" href="%s" target="_blank" rel="noopener">View your profile %s</a>' % (e(profile), ic("chev"))) if profile else \
        ('<a class="md-prof" data-md-prof href="/account/contact">Edit your listing %s</a>' % ic("chev"))
    return ('<div class="md-top"><img src="%s" alt="Three Village Local" width="132" height="45" class="md-3vl" data-processed="true">'
            '<span class="md-brand">Member Dashboard</span><span class="md-sign">%s Signed in</span></div>'
            '<div class="md-hi"%s><div class="md-hi-in">%s<div><p class="md-k">%s</p><h1 class="md-h">%s</h1><p class="md-s">%s</p></div></div>%s</div>'
            % (LOGO3VL, ic("lock"), (' style="--ban:url(%s)"' % e(ban)) if ban else "", lg, kicker, title, sub, prof))


def page_featured(a):
    USED.clear()
    rows = "".join(row(it) for it in a["items"])
    up = "".join('<li><span class="md-up-d"><b>%s</b><i>%s</i></span><div><b>%s</b><i>%s</i></div></li>' % (
        dt.date.fromisoformat(u["date"]).strftime("%b"), dt.date.fromisoformat(u["date"]).day, e(u["title"]), e(u["note"])) for u in a["upcoming"][:4])
    if not up:
        up = '<li><span class="md-up-d"><b>%s</b><i>&#8226;</i></span><div><b>More on the way</b><i>Have news, a special or an event? Email hello@threevillagelocal.com and we will help promote it.</i></div></li>' % TODAY.strftime("%b")
    top = ('<div class="md" id="md" data-tier="f">' + head("%s Featured member" % ic("star"), "Welcome back, %s" % e(a["short"]),
                                                    "Here is what Three Village Local did for you lately.", a["profile"], a["logo"], a["banner"])
           + (('<div class="md-mtabs" role="group" aria-label="Time period"><button type="button" data-m="r30" aria-pressed="true" class="on">Last 30 days</button></div>' + reach30(a)) if reach30(a) else "")
           + net_card())
    out = top + ('<div class="md-grid">%s'
           '<div class="md-side"><div class="md-card"><div class="md-ch"><b>Coming up for you</b></div><ul class="md-upc">%s</ul></div>'
           '<div class="md-card"><div class="md-ch"><b>What&#39;s new at 3VL</b></div><ul class="md-news">%s</ul></div></div>'
           '<div class="md-card md-grow md-sells">%s</div>'
           '<div class="md-card md-grow"><div class="md-ch"><b>Our services</b><i>10%% off for Featured</i></div><div class="md-ups">%s</div></div></div>'
           '<p class="md-foot">Questions or something to promote? Email <a href="mailto:hello@threevillagelocal.com">hello@threevillagelocal.com</a> and we will get it out there.</p></div>'
           ) % (timeline(a, False), up, news_list("f"), upsell("f"), services_list("f"))
    return sprite() + nowrap_hyphens(out)


def page_basic():
    """One shared page for every Basic member (no personal data; p3.js fills in the name)."""
    USED.clear()
    out = ('<div class="md" id="md" data-tier="b">' + head("%s Basic member" % ic("check"), "Welcome back, <span data-md-name>neighbor</span>",
                                                    "You are listed on Three Village Local. Here is how the neighbors find local businesses, and how to get seen more.") +
           '%s<div class="md-card md-grow md-sells">%s</div>'
           '<div class="md-card md-grow"><div class="md-ch"><b>Our services</b><i>Save 10%% with Featured, 20%% with VIP</i></div><div class="md-ups">%s</div></div>'
           '<p class="md-foot">Need help with your listing? Email <a href="mailto:hello@threevillagelocal.com">hello@threevillagelocal.com</a> and a real person will help.</p></div>'
           ) % (net_card(), upsell("b"), services_list("b"))
    return sprite() + nowrap_hyphens(out)


def nowrap_hyphens(h):   # same rule as join-v2: hyphenated words never break across lines
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
            out.append(re.sub(r"(?<![\w&#;/.-])([A-Za-z0-9']+(?:-[A-Za-z0-9']+)+)(?![\w/.-])", r'<span class="md-nw">\1</span>', part))
    return "".join(out)


SHELL = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex"><title>Member Dashboard Preview</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Radio+Canada:wght@400;600;700&display=swap" rel="stylesheet">
<style>body{margin:0;background:#f4f7fb}.bd-fake{background:#fff;border-bottom:1px solid #e3e9f1;padding:12px 16px;font:600 14px system-ui;color:#5b6b7c}
.pv-rib{max-width:1180px;margin:12px auto 0;padding:0 16px;font:700 12.5px system-ui;color:#7a5a00}.pv-rib span{display:block;background:#fff6dc;border:1px dashed #e9c25a;border-radius:12px;padding:8px 12px}
.wrap{max-width:1180px;margin:0 auto;padding:12px 16px 40px}</style>
<style>%s</style></head><body><div class="bd-fake">threevillagelocal.com/account/home (BD member area, simulated)</div>
<div class="pv-rib"><span>PREVIEW for owner review. Real activity from our logs only. Nothing here is live.</span></div>
<div class="wrap">%s</div><script>%s</script></body></html>'''


def token(uid):
    import hashlib
    sp = os.path.join(HERE, "data", ".salt")
    if not os.path.exists(sp):
        open(sp, "w").write(os.urandom(16).hex())
    return hashlib.sha256((open(sp).read().strip() + uid).encode()).hexdigest()[:14]


# ---------------------------------------------------------------- v2: private addresses + dashboard-style page
V2 = "--v2" in sys.argv
TOKENS_P = os.path.join(GUARD, "data", "member_dashboard", "tokens.json")   # PRIVATE repo only, never 3vl-share


def tokens_for(uids):
    """uid -> long random token (secrets.token_urlsafe(24) = 32 chars). New members get one; existing ones never change."""
    import secrets
    t = jload(TOKENS_P, {}) or {}
    changed = False
    for u in uids:
        if u not in t:
            t[u] = secrets.token_urlsafe(24)
            changed = True
    if changed:
        os.makedirs(os.path.dirname(TOKENS_P), exist_ok=True)
        json.dump(t, open(TOKENS_P, "w", encoding="utf-8"), indent=1, sort_keys=True)
    return t


def lookup_key(uid, email):
    """What p3.js computes in the browser for the signed-in member: sha256('3vlmd|' + uid + '|' + lowercased account email)."""
    import hashlib
    return hashlib.sha256(("3vlmd|%s|%s" % (uid, (email or "").strip().lower())).encode()).hexdigest()


def account_emails(uids):
    """Account emails from the BD API (nightly job only, env BD_API_KEY). Used to write lookup keys; never stored or published."""
    key = os.environ.get("BD_API_KEY")
    if not key:
        return {}
    import requests
    out = {}
    for u in uids:
        try:
            r = requests.get("https://www.threevillagelocal.com/api/v2/user/get/%s" % u, headers={"X-Api-Key": key}, timeout=30).json()
            m = r.get("message")
            m = m[0] if isinstance(m, list) and m else m
            if isinstance(m, dict) and m.get("email"):
                out[u] = m["email"]
        except Exception as ex:
            print("email lookup failed", u, ex)
    return out


ENDPOINT = "https://3vl-ai-assistant.vercel.app/api/member-submit"
PV_DIR = "live/md/pv/D312ZnN2JxLHNwlhEuRlUSp6"   # owner preview folder (hidden, noindex)


def speedup(html, css_path):
    """Owner 11/15 speed pass: inline the CSS (no render-blocking request), fonts non-blocking, preload the hero photo,
    and images inside views that are not open yet only load when the view opens (data-src, see dash3.js hydrate)."""
    import re as _re
    css = open(css_path, encoding="utf-8").read()
    html = _re.sub(r'<link rel="stylesheet" href="[^"]+">', lambda m: "<style>" + css + "</style>", html, count=1)
    html = _re.sub(r'<link href="(https://fonts\.googleapis\.com/[^"]+)" rel="stylesheet">',
                   lambda m: '<link rel="preload" as="style" href="%s"><link rel="stylesheet" href="%s" media="print" onload="this.media=\'all\'">' % (m.group(1), m.group(1)), html, count=1)
    hm = _re.search(r'class="hero-ph"><img src="([^"]+)"', html)
    if hm:
        html = html.replace("</title>", '</title><link rel="preload" as="image" href="%s" fetchpriority="high">' % hm.group(1), 1)
    out, pos = [], 0
    for m in _re.finditer(r'<div class="view" data-view="[a-z]+">', html):
        out.append(html[pos:m.start()])
        end = html.find('<div class="view', m.end())
        end = end if end > 0 else html.find('<div class="drawer"', m.end())
        chunk = html[m.start():end]
        chunk = _re.sub(r'<img((?:(?!>).)*?) src="(https?://[^"]+)"', r'<img\1 data-src="\2"', chunk)
        chunk = _re.sub(r' srcset="([^"]+)"', r' data-srcset="\1"', chunk)
        out.append(chunk)
        pos = end
    out.append(html[pos:])
    return "".join(out)


def announcements_for(uid, tier):
    """Active one-time popups for this member (member-specific first, then "all"). Source: guard data/member_dashboard/announcements.json."""
    import datetime as _dt
    today = _dt.datetime.now().strftime("%Y-%m-%d")
    items = (jload(os.path.join(GUARD, "data", "member_dashboard", "announcements.json"), {}) or {}).get("items", [])
    out = []
    for it in items:
        if not it.get("id") or not it.get("title"):
            continue
        if str(it.get("start") or "0000") > today or str(it.get("end") or "9999") < today:
            continue
        who = str(it.get("uid") or "all")
        if who != "all" and who != str(uid or ""):
            continue
        if it.get("tiers") and tier not in it["tiers"]:
            continue
        j = {k: it[k] for k in ("id", "title", "emoji", "body", "frame", "button", "end") if it.get(k)}
        for k in ("image", "image_640"):
            if it.get(k):
                j[k] = it[k] if it[k].startswith("http") else SHARE + "live/md/" + it[k]
        out.append((0 if who != "all" else 1, j))
    out.sort(key=lambda x: x[0])
    return [j for _, j in out]


def ann_script(uid, tier):
    a = announcements_for(uid, tier)
    if not a:
        return ""
    return '<script type="application/json" id="mdann">%s</script>' % json.dumps(a, ensure_ascii=False).replace("</", "<\/")


def inst_html(icon, company=""):
    import importlib
    X = importlib.import_module("v3" if V3_FLAG else "v2")
    """Phone install bubble (owner 11/15: call it their dashboard APP). Installed app name stays "3VL Dashboard"."""
    h = X.INSTALL % icon
    if company and V3_FLAG:
        h = h.replace("<b>Get your 3VL Dashboard app</b>", "<b>Add your %s dashboard app to your home screen</b>" % e(company), 1)
    return h


V3_FLAG = "--v3" in sys.argv


def requested_samples():
    """uid -> date of a dashboard sample request: legacy guard file + the submit endpoint's record files in news-monitor."""
    out = {}
    for u, v in (jload(os.path.join(GUARD, "data", "member_dashboard", "sample_requests.json"), {}) or {}).items():
        out[u] = v
    rd = os.path.join(NEWS, "data", "member_dashboard", "requests")
    if os.path.isdir(rd):
        for fn in sorted(os.listdir(rd)):
            if fn.endswith("_dashboard_sample.json"):
                j = jload(os.path.join(rd, fn), {}) or {}
                if j.get("uid"):
                    out[str(j["uid"])] = {"date": str(j.get("at", ""))[:10]}
    return out


def write_members_map(toks, mem, acts, tier_of, emails):
    """Private token -> member map for the submit endpoint (sha256 keys only), written to the PRIVATE news-monitor repo."""
    import hashlib
    m = {}
    for u, t in toks.items():
        a = acts.get(u) or {}
        mm = mem.get(u) or {}
        first = ""
        try:
            import v2 as X2
            first = (X2.v3_profile(u, os.path.join(DOCS, "3vl-share")).get("first") or "").strip()
        except Exception:
            pass
        ph = "".join(ch for ch in str(mm.get("phone") or "") if ch.isdigit())
        m[hashlib.sha256(t.encode()).hexdigest()] = {"uid": u, "company": a.get("short") or mm.get("name") or "", "first": first, "tier": tier_of(u),
                                                      "phone": ("%s-%s-%s" % (ph[:3], ph[3:6], ph[6:10])) if len(ph) == 10 else ph, "profile": mm.get("url") or a.get("profile") or "",
                                                      "email": emails.get(u, "")}
    p = os.path.join(NEWS, "data", "member_dashboard", "members_map.json")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(m, open(p, "w", encoding="utf-8"), indent=1, sort_keys=True)
    return p


def build_v2(acts, V, NETd, r):
    """One dashboard for every tier. VIP + Featured get their own private token page; Basic members share one page (name filled in)."""
    V3 = "--v3" in sys.argv
    if V3:
        import v3 as X
    else:
        import v2 as X
    PFX = "v3-" if V3 else "v2-"
    mem = {str(m["id"]): m for m in (jload(os.path.join(GUARD, "data", "members.json"), {}) or {}).get("members", [])}
    tier_of = lambda u: {"vip": "v", "noticed": "f", "partner": "p"}.get((mem.get(u) or {}).get("plan"), "b")
    ids = list(acts.keys())
    toks = tokens_for(ids)
    share_dir = os.path.join(DOCS, "3vl-share")
    local_css, local_js = ("../dash3.css", "../dash3.js") if V3 else ("../dash2.css", "../dash2.js")
    live_css, live_js = (SHARE + "live/md/md3.css", SHARE + "live/md/md3.js") if V3 else (SHARE + "live/md/md2.css", SHARE + "live/md/md2.js")
    bviews = floor_k(r.get("views") or 0)
    soc = jload(os.path.join(NEWS, "data", "hq", "social.json"), {}) or {}
    net = dict(NETd)
    net["social"] = int(((soc.get("fb") or {}).get("cur") or {}).get("page_media_view") or 0) + int(((soc.get("ig") or {}).get("cur") or {}).get("views") or 0)
    others_all = []
    for u, a in acts.items():
        if a["tier"] == "v":
            lg, ban, th = member_images(u)
            if th:
                others_all.append({"uid": u, "name": a["short"], "img": th})
    preview = not WRITE_LIVE
    samples = requested_samples()   # {uid: date}: the submit endpoint's records + legacy file
    wk0 = (dt.date.today() - dt.timedelta(days=dt.date.today().weekday())).isoformat()   # Monday of this week
    week_n = sum(1 for v in samples.values() if str(v.get("date") if isinstance(v, dict) else v)[:10] >= wk0)
    samples_full = week_n >= 5   # weekly cap (the endpoint enforces it too)
    want = [x for x in sys.argv[1:] if x.isdigit()]
    built = []

    def ctx_for(u, a, tier):
        hd = r.get("home_daily", {})
        home = sum(hd.get(d, 0) for d in a.get("hp_days", []) if d >= W0)
        email = sum(it.get("recipients", 0) for it in a.get("items", []) if it["ch"] == "email" and it["date"] >= W0 and not it.get("sample"))
        tot = (bviews if a.get("has_banner_ad") and tier in ("v", "p") else 0) + home + email
        tok = toks.get(u, "")
        live_url = (SHARE + "live/md/v/%s.html" % tok) if tok else ""
        pv = (u == "115") or not u
        return {"endpoint": ENDPOINT if (WRITE_LIVE or "--pv" in sys.argv) else "", "token": tok if (WRITE_LIVE or "--pv" in sys.argv) else "",
                "dash_url": live_url if WRITE_LIVE else ("https://threevillagelocal-cloud.github.io/3vl-share/%s/kgr.html" % PV_DIR if pv else ""),
                "sample_done": u in samples, "samples_full": samples_full, "tier": tier, "w0": W0, "net": net, "banner_views": bviews, "reach": floor_k(tot) if tot >= FLOOR_REACH else 0, "share_dir": share_dir,
                "member": mem.get(u, {}), "raw": RAW, "logo3vl": LOGO3VL, "preview": preview, "others": [o for o in others_all if o["uid"] != u]}

    def write(name, title, body, installable=True):
        b = body.replace(SHARE + "live/md/3vl-navy-440.webp", "../img/3vl-navy-440.webp")
        if installable:
            b = b.replace("</main></div>", "</main>" + inst_html("../img/icon-180.png", title if name != "basic" else "") + "</div>")
            open(os.path.join(HERE, "_local", PFX + "%s.webmanifest" % name), "w", encoding="utf-8").write(X.manifest(PFX + name, "../img/"))
        page_html = X.SHELL % (e(title), PFX + "%s.webmanifest" % name, "../img/icon-180.png", local_css, b, local_js)
        if V3:
            page_html = speedup(page_html, os.path.join(HERE, "dash3.css"))
            if "--pv" in sys.argv:
                page_html = page_html.replace('id="mdx" ', 'id="mdx" data-test="1" ', 1)
        open(os.path.join(HERE, "_local", PFX + "%s.html" % name), "w", encoding="utf-8").write(page_html)

    for u in ids:
        if want and u not in want:
            continue
        a, tier = acts[u], tier_of(u)
        body = X.page(a, ctx_for(u, a, tier)) + (ann_script(u, tier) if V3 else "")
        for bad in ("\u2014", "\u2013", "&mdash;", "&ndash;"):
            assert bad not in body, "dash in v2 " + u
        write(u, a["short"], body)
        if WRITE_LIVE:
            os.makedirs(os.path.join(LIVE_DIR, "v"), exist_ok=True)
            ib = SHARE + "live/md/"
            lb = body.replace('<div class="mdx"', '<div class="mdx" data-sw="sw.js"', 1).replace("</main></div>", "</main>" + inst_html(ib + "icon-180.png", a["short"]) + "</div>")
            lh = X.SHELL % (e(a["short"]), "%s.webmanifest" % toks[u], ib + "icon-180.png", live_css, lb, live_js)
            if V3:
                lh = speedup(lh, os.path.join(HERE, "dash3.css"))
            open(os.path.join(LIVE_DIR, "v", "%s.html" % toks[u]), "w", encoding="utf-8").write(lh)
            open(os.path.join(LIVE_DIR, "v", "%s.webmanifest" % toks[u]), "w", encoding="utf-8").write(X.manifest(toks[u], ib))
        built.append(u)
    # Basic members: one shared page (no personal data; the loader fills in the business name)
    basic = X.page({"uid": "", "short": "", "items": [], "hp_days": []}, ctx_for("", {"items": [], "hp_days": []}, "b")) + (ann_script("", "b") if V3 else "")
    write("basic", "Member Dashboard", basic, installable=False)
    if WRITE_LIVE:
        import shutil
        open(os.path.join(LIVE_DIR, "basic2.html"), "w", encoding="utf-8").write(X.SHELL % ("Member Dashboard", "", SHARE + "live/md/icon-180.png", live_css, basic, live_js))
        for n in ("icon-180.png", "icon-192.png", "icon-512.png"):
            shutil.copy(os.path.join(HERE, "img", n), os.path.join(LIVE_DIR, n))
        shutil.copy(os.path.join(HERE, "sw.js"), os.path.join(LIVE_DIR, "v", "sw.js"))   # same origin + scope as the private pages
        shutil.copy(os.path.join(HERE, "dash2.css"), os.path.join(LIVE_DIR, "md2.css"))
        shutil.copy(os.path.join(HERE, "dash2.js"), os.path.join(LIVE_DIR, "md2.js"))
        shutil.copy(os.path.join(HERE, "dash3.css"), os.path.join(LIVE_DIR, "md3.css"))
        shutil.copy(os.path.join(HERE, "dash3.js"), os.path.join(LIVE_DIR, "md3.js"))
        kdir = os.path.join(LIVE_DIR, "k")   # lookup keys for the signed-in loader: k/<sha256(uid|email)>.txt holds that member's token only
        shutil.rmtree(kdir, ignore_errors=True)
        os.makedirs(kdir, exist_ok=True)
        emails = account_emails(ids)
        for u, em in emails.items():
            open(os.path.join(kdir, lookup_key(u, em) + ".txt"), "w").write(toks[u])
        print("members map:", write_members_map({u: toks[u] for u in ids}, mem, acts, tier_of, emails))
        shutil.rmtree(os.path.join(LIVE_DIR, "m"), ignore_errors=True)   # retire the guessable member-number pages
    if "--map" in sys.argv and not WRITE_LIVE:   # write the endpoint's members map without publishing pages
        print("members map:", write_members_map({u: toks[u] for u in ids}, mem, acts, tier_of, account_emails(ids)))
    if "--shots" in sys.argv:
        shots(built)
    return built


def shots(uids):
    """Crisp 1200px-wide desktop screenshots for the VIP email: shots/<uid>.png"""
    from playwright.sync_api import sync_playwright
    os.makedirs(os.path.join(HERE, "shots"), exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for u in uids:
            pg = b.new_page(viewport={"width": 1200, "height": 900}, device_scale_factor=2)
            pg.goto("file:///" + os.path.join(HERE, "_local", "v2-%s.html" % u).replace("\\", "/"))
            pg.wait_for_timeout(1500)
            pg.screenshot(path=os.path.join(HERE, "shots", "%s.png" % u), full_page=True)
            pg.close()
        b.close()


def main():
    want = [a for a in sys.argv[1:] if a.isdigit()]
    V = vips(("vip", "noticed"))
    hp = homepage_history()
    issues, posts, rot = weekly_issues(), social_posts(), rotation()
    banners = {str(b["id"]): b.get("img", "") for b in jload(os.path.join(ASSETS, "weekender", "banners.json"), [])}
    os.makedirs(os.path.join(HERE, "data"), exist_ok=True)
    os.makedirs(os.path.join(HERE, "_local"), exist_ok=True)
    css = open(os.path.join(HERE, "dash.css"), encoding="utf-8").read()
    js = open(os.path.join(HERE, "dash.js"), encoding="utf-8").read()
    r = jload(os.path.join(HERE, "data", "banner_reach.json"), {}) or {}
    bsince = banner_since()
    acts = {uid: activity(m, hp, issues, posts, rot, banners, bsince) for uid, m in V.items()}
    hl = 0
    for a in acts.values():
        if a["tier"] == "v":
            hl += len([d for d in a.get("hp_days", []) if d >= W0]) + len([it for it in a["items"] if it["ch"] in ("social", "email") and it["date"] >= W0])
    subs = next((f.get("_recipients") for d, st, f in sorted(issues, reverse=True) if f.get("_recipients")), 0)
    NET.update({"views": int(r.get("views", 0)), "pct": r.get("change_pct"), "vip_hl": hl, "subs": subs})
    print("network", NET)
    for uid, m in V.items():
        if want and uid not in want:
            continue
        a = acts[uid]
        json.dump(a, open(os.path.join(HERE, "data", uid + ".json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        body = page(a)
        for bad in ("—", "–", "&mdash;", "&ndash;"):
            assert bad not in body, "em/en dash in %s" % uid
        vis = re.sub(r"<[^>]+>", " ", re.sub(r"<(svg|script|style)[^>]*>.*?</\1>", " ", body, flags=re.S))
        assert not re.search(r"(?i)(?<!mobile )\bapps?\b", vis), "bare 'app' in copy for %s" % uid
        open(os.path.join(HERE, "_local", uid + ".html"), "w", encoding="utf-8").write(SHELL % (css, body, js))
        if WRITE_LIVE:   # signed-in dashboard fragment, loaded by p3.js on /account/home for members in its MD list
            os.makedirs(LIVE_DIR, exist_ok=True)
            os.makedirs(os.path.join(LIVE_DIR, "m"), exist_ok=True)
            open(os.path.join(LIVE_DIR, "m", "%s.html" % uid), "w", encoding="utf-8").write(body)
        s = a["months"].get(TODAY.strftime("%Y-%m"), {})
        print(uid, m["short"], "| items", len(a["items"]), "| upcoming", len(a["upcoming"]), "| this month", s)

    if V2:
        print("v2 built:", build_v2(acts, V, dict(NET), r))

    bb = page_basic()
    open(os.path.join(HERE, "_local", "basic.html"), "w", encoding="utf-8").write(SHELL % (css, bb, js))
    if WRITE_LIVE:
        open(os.path.join(LIVE_DIR, "basic.html"), "w", encoding="utf-8").write(bb)
        import shutil
        shutil.copy(os.path.join(HERE, "dash.css"), os.path.join(LIVE_DIR, "md.css"))
        shutil.copy(os.path.join(HERE, "dash.js"), os.path.join(LIVE_DIR, "md.js"))
        shutil.copy(os.path.join(HERE, "img", "3vl-navy-440.webp"), os.path.join(LIVE_DIR, "3vl-navy-440.webp"))


if __name__ == "__main__":
    main()
