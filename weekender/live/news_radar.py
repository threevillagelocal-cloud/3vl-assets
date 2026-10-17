"""3VL news radar (owner 10/17/2026: "I need news as it happens", the daily openings/closings email was always old news).
Run by the 3VL clock every 30 minutes, 6:30 AM to 10 PM ET (owner: 15 min was overkill). Checks the places local news shows up FIRST, keeps a seen-list,
and hands anything new to 3vl-site-guard (data/news_radar/hits/), whose news-radar-mail workflow emails the owner.

Urgent items (business openings/closings, liquor license filings = "coming soon", weather warnings, ferry, closures,
emergencies) go out right away. Other local news collects and goes out as a digest at noon and 6 PM.

    python3 weekender/live/news_radar.py [--guard /tmp/guard] [--dry] [--seed]
--seed marks everything currently out there as seen without sending (first run). --dry prints, writes nothing.
Env: IG_TOKEN (optional; business Instagram captions). Never printed."""
import datetime as dt, email.utils, html, json, os, re, sys, urllib.parse, urllib.request
import xml.etree.ElementTree as ET
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
TZ = ZoneInfo("America/New_York")
UA = "Mozilla/5.0 (3VL news radar; hello@threevillagelocal.com)"
ZIPS = ["11733", "11790", "11720", "11777", "11776", "11794"]   # Three Village + Port Jeff (+ Station)
TOWNS = r"port jeff(erson)?|stony ?brook|setauket|three village|old field|poquott|st\.? james|belle terre|mount sinai|miller place|terryville"
TOWN_RE = re.compile(TOWNS, re.I)
BIZ_RE = re.compile(r"grand opening|now open|soft open|opening (soon|this|next|on|in )|coming soon|ribbon[- ]cutting|new location|"
                    r"(is |are |will be |we're |we are )?clos(ing|ed) (for good|permanently|its doors|their doors|our doors|after|at the end)|"
                    r"last day|final day|final week|shutting down|farewell|under new ownership|new owners?|moving to|"
                    r"opens? (its|their|a) |to open|has opened|reopen", re.I)
URGENT_RE = re.compile(r"road clos|closed (road|lane)|crash|collision|fire\b|brush fire|power outage|outage|evacuat|shelter in place|"
                       r"water main|boil water|lockdown|missing|police activity|shooting|stabbing|arrest|hazmat|gas leak|"
                       r"ferry|lirr|delays?|cancel|warning|storm|flood|tornado|hurricane|nor'?easter|snow emergency|school clos", re.I)
NOISE_RE = re.compile(r"live ?stream|\bstreams?\b|watch ?live|\bvs\b|\bv\.\s|game logs?|\bhdq\b|seawolves|basketball|football|soccer|lacrosse|volleyball|"
                      r"baseball|softball|obituar|real estate transactions|home sales|\bstocks?\b|earnings call|research (shows|finds)|"
                      r"study (shows|finds)|clinical trial", re.I)

GNEWS = ['"Port Jefferson"', '"Port Jeff"', '"Stony Brook" -university', 'Setauket', '"Three Village"']
FEEDS = [("TBR News Media", "https://tbrnewsmedia.com/category/three-village/feed/"),
         ("TBR News Media", "https://tbrnewsmedia.com/category/port-jefferson/feed/"),
         ("Patch", "https://patch.com/feeds/new-york/threevillage"),
         ("Patch", "https://patch.com/feeds/new-york/portjefferson"),
         ("Suffolk County Police", "https://suffolkpd.org/Alerts/Press-Releases/ctl/rss/mid/10029"),   # owner 10/17: 6th Precinct activity
         ("Reddit r/longisland", "https://www.reddit.com/r/longisland/new/.rss")]
POLICE_TOWNS = re.compile(r"setauket|stony ?brook|port jeff(erson)?|old field|poquott|belle terre|south setauket", re.I)
NWS = "https://api.weather.gov/alerts/active?zone=NYZ078"     # Northwest Suffolk
SLA = ("https://data.ny.gov/resource/f8i8-k2gm.json?$where=" +
       urllib.parse.quote("zip_code in(%s)" % ",".join("'%s'" % z for z in ZIPS)) + "&$limit=200")


def get(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def clean(s):
    s = re.sub(r"<[^>]+>", " ", html.unescape(s or ""))
    return re.sub(r"\s+", " ", s).strip()


def when(s):
    try:
        d = email.utils.parsedate_to_datetime(s)
    except (TypeError, ValueError):
        try:
            d = dt.datetime.fromisoformat((s or "").replace("Z", "+00:00"))
        except ValueError:
            return None
    return d if d.tzinfo else d.replace(tzinfo=dt.timezone.utc)


def item(src, title, link, ts=None, snippet="", kind=None, key=None):
    title, snippet = clean(title), clean(snippet)[:280]
    text = title + " " + snippet
    if kind is None:
        kind = "business" if BIZ_RE.search(text) else ("alert" if URGENT_RE.search(text) else "news")
    return {"id": key or (link or title), "source": src, "title": title, "link": link, "snippet": snippet,
            "time": ts.isoformat() if ts else "", "kind": kind, "urgent": kind in ("business", "alert", "coming_soon", "weather", "ferry"),
            "never_promote": False}   # flagged by the private mail step


def rss(src, xml, need_town, max_age_h=36):
    out, now = [], dt.datetime.now(dt.timezone.utc)
    try:
        root = ET.fromstring(xml)
    except ET.ParseError:
        return out
    ns = {"a": "http://www.w3.org/2005/Atom"}
    entries = root.findall(".//item") or root.findall(".//a:entry", ns)
    for e in entries:
        t = e.findtext("title") or e.findtext("a:title", default="", namespaces=ns)
        link = e.findtext("link") or ""
        if not link:
            l = e.find("a:link", ns)
            link = l.get("href") if l is not None else ""
        ts = when(e.findtext("pubDate") or e.findtext("a:published", default="", namespaces=ns) or e.findtext("a:updated", default="", namespaces=ns))
        desc = e.findtext("description") or e.findtext("a:content", default="", namespaces=ns) or ""
        if ts and (now - ts).total_seconds() > max_age_h * 3600:
            continue
        text = clean(t + " " + desc)
        if need_town and not TOWN_RE.search(text):
            continue
        if NOISE_RE.search(t):
            continue
        out.append(item(src, t, link, ts, desc))
    return out


def google_news():
    out = []
    for q in GNEWS:
        url = "https://news.google.com/rss/search?" + urllib.parse.urlencode({"q": q + " when:1d", "hl": "en-US", "gl": "US", "ceid": "US:en"})
        try:
            for it in rss("Google News", get(url), need_town=True):
                src = re.search(r" - ([^-]+)$", it["title"])
                if src:
                    it["source"] = src.group(1).strip()
                    it["title"] = it["title"][:src.start()].strip()
                it["id"] = "gn:" + re.sub(r"\W+", " ", it["title"].lower()).strip()   # same story, many links
                out.append(it)
        except Exception as e:
            print("google news failed:", q, type(e).__name__)
    return out


def feeds():
    out = []
    for name, url in FEEDS:
        try:
            got = rss(name, get(url), need_town=not name.startswith("TBR"))   # Patch/Reddit/police feeds cover all of Long Island
            if name == "Suffolk County Police":
                got = [dict(i, kind="police", urgent=True) for i in got if POLICE_TOWNS.search(i["title"] + " " + i["snippet"])]
            out += got
        except Exception as e:
            print("feed failed:", name, type(e).__name__)
    return out


def liquor():
    """New liquor license applications = a bar/restaurant/shop opening or changing hands, usually weeks before anyone posts."""
    out = []
    try:
        rows = json.loads(get(SLA))
    except Exception as e:
        print("SLA failed:", type(e).__name__); return out
    for r in rows:
        name = (r.get("legalname") or "").strip()
        if re.search(r"\bgas\b|dolgen|\bcvs\b|7-eleven|seven eleven|stewart|walgreen|speedway|mobil|shell", name, re.I):
            continue                              # gas stations / chains adding beer: not news
        addr = "%s, %s" % ((r.get("actual_address_of_premises") or "").strip(), (r.get("city") or "").strip())
        t = "Liquor license filed: %s (%s) at %s" % (name, r.get("description", ""), addr)
        out.append(item("NY State Liquor Authority", t, "https://data.ny.gov/d/f8i8-k2gm", when(r.get("received_date")),
                        "Status: %s. Filed %s. Usually means a new place or new owners is coming." % (r.get("status", ""), (r.get("received_date") or "")[:10]),
                        kind="coming_soon", key="sla:" + r.get("application_id", t)))
    return out


def weather():
    out = []
    try:
        d = json.loads(get(NWS))
    except Exception as e:
        print("NWS failed:", type(e).__name__); return out
    for f in d.get("features", []):
        p = f.get("properties", {})
        if p.get("severity") in ("Minor", "Unknown") and "Advisory" not in (p.get("event") or ""):
            continue
        out.append(item("National Weather Service", "%s for our area" % p.get("event", "Alert"), p.get("@id", ""),
                        when(p.get("sent")), p.get("headline", ""), kind="weather", key="nws:" + p.get("id", "")))
    return out


def ferry():
    out = []
    try:
        sys.path.insert(0, HERE)
        import ferry as F
        F.main()
        d = json.load(open(os.path.join(HERE, "ferry.json"), encoding="utf-8"))
    except Exception as e:
        print("ferry failed:", type(e).__name__); return out
    for a in d.get("alerts", []):
        t = a.get("title") or a.get("text") or ""
        if t:
            out.append(item("88844ferry.com", "Ferry: " + t, a.get("link") or "https://www.88844ferry.com", when(a.get("published") or a.get("publishedAt")),
                            a.get("text", ""), kind="ferry", key="ferry:" + t))
    return out


def instagram(state):
    """Local businesses announce openings/closings on Instagram first. Rotates through the list, ~25 accounts a run."""
    tok = os.environ.get("IG_TOKEN", "").strip()
    if not tok:
        return []
    accts = [a for a in json.load(open(os.path.join(HERE, "ig_accounts.json"), encoding="utf-8")) if a.get("ig")]
    extra = os.path.join(HERE, "radar_ig.json")
    if os.path.exists(extra):
        have = {a["ig"].lower() for a in accts}
        accts += [a for a in json.load(open(extra, encoding="utf-8")) if a.get("ig") and a["ig"].lower() not in have]
    if not accts:
        return []
    start = state.get("ig_pos", 0) % len(accts)
    batch = (accts + accts)[start:start + 25]
    state["ig_pos"] = start + len(batch)
    out, now = [], dt.datetime.now(dt.timezone.utc)
    for a in batch:
        q = "business_discovery.username(%s){username,name,media.limit(4){timestamp,permalink,caption}}" % a["ig"]
        url = "https://graph.facebook.com/v21.0/17841472800565482?" + urllib.parse.urlencode({"fields": q, "access_token": tok})
        try:
            bd = json.loads(get(url)).get("business_discovery", {})
        except Exception:
            continue
        for m in bd.get("media", {}).get("data", []):
            ts = when(m.get("timestamp"))
            cap = m.get("caption") or ""
            if not ts or (now - ts).total_seconds() > 72 * 3600 or not BIZ_RE.search(cap):
                continue
            out.append(item("Instagram @" + a["ig"], "%s posted: %s" % (a.get("name") or a["ig"], clean(cap)[:110]), m.get("permalink"), ts, cap,
                            kind="business", key="ig:" + (m.get("permalink") or cap[:60])))
    return out


def main():
    args = sys.argv[1:]
    guard = args[args.index("--guard") + 1] if "--guard" in args else "/tmp/guard"
    dry, seed = "--dry" in args, "--seed" in args
    sdir = os.path.join(guard, "data", "news_radar")
    sp = os.path.join(sdir, "state.json")
    state = json.load(open(sp, encoding="utf-8")) if os.path.exists(sp) else {}
    seen, pending = state.setdefault("seen", {}), state.setdefault("pending", [])
    if not seen and not dry:
        seed = True                               # first ever run: learn what is already out there, send nothing
    now = dt.datetime.now(TZ)
    found = google_news() + feeds() + liquor() + weather() + ferry() + instagram(state)
    new = []
    for it in found:
        if it["id"] in seen:
            continue
        seen[it["id"]] = now.isoformat()
        new.append(it)
    cut = (now - dt.timedelta(days=45)).isoformat()
    state["seen"] = {k: v for k, v in seen.items() if v >= cut}
    if seed:
        print("seeded", len(new), "items")
        new = []
    urgent = [i for i in new if i["urgent"]]
    pending += [i for i in new if not i["urgent"]]
    send = list(urgent)
    digest_time = (now.hour, now.minute // 30) in ((12, 0), (18, 0))
    if digest_time and pending:
        send += pending
        state["pending"] = []
    else:
        state["pending"] = pending[-120:]
    for i in found if dry else []:
        print(i["kind"], "|", i["source"], "|", i["title"][:100])
    print("found %d, new %d, urgent %d, digest pending %d, sending %d" % (len(found), len(new), len(urgent), len(state["pending"]), len(send)))
    if dry:
        return
    os.makedirs(os.path.join(sdir, "hits"), exist_ok=True)
    if send:
        json.dump({"at": now.isoformat(), "digest": digest_time and any(not i["urgent"] for i in send), "items": send},
                  open(os.path.join(sdir, "hits", now.strftime("%Y%m%d-%H%M") + ".json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    json.dump(state, open(sp, "w", encoding="utf-8"), indent=0, ensure_ascii=False)


if __name__ == "__main__":
    main()
