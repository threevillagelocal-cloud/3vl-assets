"""3VL events calendar sync: pulls local event feeds and posts them to the BD Events calendar (/events, data_id 8).

  python scripts/events_sync.py dry      -> fetch + normalize + dedupe, write report, post nothing
  python scripts/events_sync.py publish  -> create the new events on BD (as published posts)

Sources: Village of Port Jefferson (iCal), Emma S. Clark Library (RSS), Stony Brook Village Center,
Long Island Museum and Ward Melville Heritage Org (The Events Calendar REST API).
State: state/events_map.json maps each source event id to the BD post_id, so nothing is posted twice.
"""
import datetime as dt, html, json, os, re, sys, urllib.parse, urllib.request
from email.utils import parsedate_to_datetime

SITE = "https://www.threevillagelocal.com"
KEY = os.environ.get("BD_API_KEY", "")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, "state", "events_map.json")
UA = {"User-Agent": "Mozilla/5.0 (3VL events sync; threevillagelocal.com)"}
HOUSE_USER = "43"          # Three Village Local house account
DAYS_AHEAD = 60
TODAY = dt.date.today()


def get(url, headers=None, timeout=40):
    req = urllib.request.Request(url, headers=headers or UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read()
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("cp1252", "replace")


def clean(s, n=None):
    s = html.unescape(re.sub(r"<[^>]+>", " ", s or ""))
    s = re.sub(r"\s+", " ", s).strip()
    if n and len(s) > n:
        s = s[:n].rsplit(" ", 1)[0] + "..."
    return s


VENUE_ADDR = {
    "the long island museum": "1200 Route 25A, Stony Brook, NY 11790",
    "stony brook village center": "111 Main St, Stony Brook, NY 11790",
    "the long island music and entertainment hall of fame": "97 Main St, Stony Brook, NY 11790",
    "three village inn": "150 Main St, Stony Brook, NY 11790",
    "brewster house": "18 Runs Rd, East Setauket, NY 11733",
    "ward melville heritage organization": "97P Main St, Stony Brook, NY 11790",
    "country house restaurant": "1175 N Country Rd, Stony Brook, NY 11790",
}


def ev(src, uid, title, start, end=None, venue="", addr="", url="", desc="", image="", allday=False):
    if not addr or addr.strip().lower() == (venue or "").strip().lower():
        addr = VENUE_ADDR.get((venue or "").strip().lower(), addr)
    desc = re.sub(r"^[@\s]+", "", clean(desc))
    return {"src": src, "uid": "%s:%s" % (src, uid), "title": clean(title, 120), "start": start, "end": end or start,
            "venue": clean(venue, 90), "addr": clean(addr, 140), "url": url, "desc": clean(desc, 700), "image": image, "allday": allday}


# ---------- sources ----------
def tribe(src, base, default_venue=""):
    out, page = [], 1
    start = TODAY.isoformat()
    while page < 6:
        u = "%s/wp-json/tribe/events/v1/events?per_page=50&page=%d&start_date=%s" % (base, page, start)
        try:
            d = json.loads(get(u))
        except Exception:
            break
        for e in d.get("events", []):
            v = e.get("venue") or {}
            if isinstance(v, list):
                v = v[0] if v else {}
            addr = ", ".join(x for x in (v.get("address"), v.get("city"), v.get("state") or v.get("province"), v.get("zip")) if x)
            img = (e.get("image") or {}).get("url", "") if isinstance(e.get("image"), dict) else ""
            out.append(ev(src, e["id"], e.get("title", ""), dt.datetime.fromisoformat(e["start_date"]), dt.datetime.fromisoformat(e["end_date"]),
                          v.get("venue") or default_venue, addr, e.get("url", ""), e.get("description", ""), img, bool(e.get("all_day"))))
        if not d.get("next_rest_url"):
            break
        page += 1
    return out


def portjeff():
    return civic_ical("portjeff", "https://www.portjeffny.gov/common/modules/iCalendar/iCalendar.aspx?catID=14&feed=calendar",
                      "Port Jefferson", "https://www.portjeffny.gov/calendar.aspx")


LOCAL = r"stony brook|setauket|port jeff|mt\.? sinai|mount sinai|old field|poquott|st\.? james|belle terre|miller place|west meadow|cedar beach"


def brookhaven():
    """Town of Brookhaven: only programs held in or near the Three Village area (skips town hall items)."""
    return [e for e in civic_ical("brookhaven", "https://www.brookhavenny.gov/common/modules/iCalendar/iCalendar.aspx?catID=14&feed=calendar",
                                  "Town of Brookhaven", "https://www.brookhavenny.gov/calendar.aspx")
            if re.search(LOCAL, e["addr"] + " " + e["venue"], re.I)]


def cf_email(h):
    """Decode a Cloudflare-protected email (href="/cdn-cgi/l/email-protection#...")."""
    try:
        k = int(h[:2], 16)
        return "".join(chr(int(h[i:i + 2], 16) ^ k) for i in range(2, len(h), 2))
    except Exception:
        return ""


_detail = {}


def civic_detail(url):
    """Full description, cost, contact email and phone from a CivicPlus calendar.aspx?EID= event page."""
    if url in _detail:
        return _detail[url]
    out = {}
    try:
        t = get(url, timeout=20)
        m = re.search(r'itemprop="description"[^>]*>(.*?)</div>', t, re.S)
        if m:
            d = clean(m.group(1).replace("�", " "))
            out["desc"] = d
        m = re.search(r'email-protection#([0-9a-f]+)', t)
        if m:
            out["email"] = cf_email(m.group(1))
        else:
            m = re.search(r'mailto:([^"?]+@[^"?]+)', t)
            if m:
                out["email"] = m.group(1)
        m = re.search(r'Cost:</div>\s*<div[^>]*>(.*?)</div>', t, re.S)
        if m:
            out["cost"] = clean(m.group(1))
        m = re.search(r'Phone:</div>\s*<div[^>]*>(.*?)</div>', t, re.S)
        if m:
            out["phone"] = clean(m.group(1))
    except Exception:
        pass
    _detail[url] = out
    return out



def civic_ical(src, url, default_venue, default_url):
    t = get(url)
    t = re.sub(r"\r?\n[ \t]", "", t)
    out = []
    for block in re.findall(r"BEGIN:VEVENT(.*?)END:VEVENT", t, re.S):
        f = {}
        for line in block.strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                f[k.split(";")[0]] = (v, k)
        def when(key):
            if key not in f:
                return None, False
            v, k = f[key]
            v = v.strip()
            if "VALUE=DATE" in k or len(v) == 8:
                return dt.datetime.strptime(v[:8], "%Y%m%d"), True
            base = dt.datetime.strptime(v[:15], "%Y%m%dT%H%M%S")
            if v.endswith("Z"):
                base = base.replace(tzinfo=dt.timezone.utc).astimezone(dt.timezone(dt.timedelta(hours=-4))).replace(tzinfo=None)
            return base, False
        s, allday = when("DTSTART")
        e, _ = when("DTEND")
        if not s:
            continue
        loc = f.get("LOCATION", ("", ""))[0].replace("\\,", ",").replace("\\n", " ")
        desc = f.get("DESCRIPTION", ("", ""))[0].replace("\\n", " ").replace("\\,", ",")
        loc = html.unescape(loc.replace("\\;", ";").replace("\\", ""))
        loc = re.sub(r"^\s*-\s*", "", re.sub(r"\s{2,}", " ", loc)).strip()
        venue = loc.split(" - ")[0].strip() if " - " in loc else (loc if loc and len(loc) < 60 and not re.search(r"\d{5}", loc) else default_venue)
        venue = venue.split(" > ")[0].strip()
        hint = ""
        if re.search(r"please visit|this event|ticketed|website|held at", venue + " " + loc, re.I):   # a sentence, not a place
            hint = loc.rstrip(".") + "."
            m = re.search(r"held at (?:the )?(.+?)(?: - |$)", loc, re.I)
            venue, loc = (m.group(1).strip().rstrip("."), "") if m else (default_venue, "")
        u = f.get("URL", ("", ""))[0].strip()
        link = u if u.startswith("http") else default_url
        m = re.search(r"https?://\S*calendar\.aspx\?EID=\d+", desc)
        extra = {}
        if m:
            link = m.group(0).replace("Calendar.aspx", "calendar.aspx")
            if TODAY <= s.date() <= TODAY + dt.timedelta(days=DAYS_AHEAD):   # only fetch pages for events we will show
                extra = civic_detail(link)
            desc = desc.replace(m.group(0), "").strip()
        x = ev(src, f.get("UID", (s.isoformat(), ""))[0], f.get("SUMMARY", ("", ""))[0].replace("\\,", ","), s, e,
               venue, loc or default_venue, link,
               " ".join(x for x in (extra.get("desc") or desc, hint) if x), "", allday)
        for k in ("email", "phone", "cost"):
            if extra.get(k):
                x[k] = extra[k]
        out.append(x)
    return out


def emmaclark():
    t = get("https://emmaclark.librarycalendar.com/events/feed/rss")
    out = []
    for item in re.findall(r"<item>(.*?)</item>", t, re.S):
        def tag(n):
            m = re.search(r"<%s[^>]*>(.*?)</%s>" % (n, n), item, re.S)
            return html.unescape(re.sub(r"^<!\[CDATA\[|\]\]>$", "", m.group(1).strip())) if m else ""
        link, title, desc = tag("link"), tag("title"), tag("description")
        txt = clean(desc)
        m = re.search(r"(\d{2}/\d{2}/\d{2})\s*@\s*(\d{1,2}:\d{2}\s*[ap]m)(?:\s*-\s*(\d{2}/\d{2}/\d{2})\s*@\s*(\d{1,2}:\d{2}\s*[ap]m))?", txt, re.I)
        allday = False
        if m:
            s = dt.datetime.strptime(m.group(1) + " " + m.group(2).replace(" ", "").lower(), "%m/%d/%y %I:%M%p")
            e = dt.datetime.strptime(m.group(3) + " " + m.group(4).replace(" ", "").lower(), "%m/%d/%y %I:%M%p") if m.group(3) else s
            rest = txt[m.end():]
        else:
            m = re.search(r"(\d{2}/\d{2}/\d{2})", txt)
            if not m:
                continue
            s = e = dt.datetime.strptime(m.group(1), "%m/%d/%y"); allday = True; rest = txt[m.end():]
        loc = ""
        lm = re.match(r"\s*-?\s*(Off Site|[A-Z][A-Za-z0-9 '&/-]{2,40}?(?:Room|Center|Lawn|Auditorium|Lobby|Gallery)?)\s{1,}(?=[A-Z])", rest)
        body = re.split(r"Pictures/Videos taken at or for library events", rest)[0]
        body = clean(body, 600)
        venue = "Emma S. Clark Memorial Library"
        if rest.strip().startswith("Off Site"):
            venue, body = "Off site (Emma S. Clark Library program)", clean(rest.strip()[8:].split("Pictures/Videos")[0], 600)
        cats = re.findall(r"<category>(.*?)</category>", item)
        if cats:
            body = (body + " Categories: " + ", ".join(html.unescape(c) for c in cats) + ".").strip()
        st = not allday
        out.append(ev("emmaclark", link.rstrip("/").split("/")[-1], title, s, e, venue,
                      "120 Main St, Setauket, NY 11733", link, body, "", allday))
    return out



def gz_detail(url):
    """Venue, address, contact and full-size flyer from a GrowthZone event detail page."""
    out = {}
    try:
        t = get(url, timeout=20)
        m = re.search(r'gz-event-address">\s*<strong>(.*?)</strong>(.*?)</div>', t, re.S)
        if m:
            out["venue"] = clean(m.group(1))
            out["addr"] = re.sub(r"\s+,", ",", clean(re.sub(r"<br\s*/?>", ", ", m.group(2)))).replace(" United States", "").strip(", ")
        m = re.search(r'gz-event-contact">(.*?)</div>', t, re.S)
        if m:
            ph = re.search(r'href="tel:[^"]*">([^<]+)', m.group(1))
            em = re.search(r'mailto:([^"?]+)', m.group(1))
            if ph:
                out["phone"] = clean(ph.group(1))
            if em:
                out["email"] = em.group(1)
        m = re.search(r'gz-eventcard-img" src="([^"]+)"', t)
        if m:
            out["image"] = m.group(1)
        m = re.search(r'class="[^"]*gz-event-description[^"]*"[^>]*>(.*?)</div>', t, re.S)
        if m and len(clean(m.group(1))) > 20:
            out["desc"] = clean(m.group(1))
    except Exception:
        pass
    return out


def chamber3v():
    """Three Village Chamber of Commerce (GrowthZone portal): server-rendered cards with schema.org start/end."""
    t = get("https://members.3vchamber.com/event-calendar")
    out = []
    for card in t.split('class="card gz-events-card"')[1:]:
        m = re.search(r'gz-event-card-title"[^>]*>(.*?)</a>', card, re.S)
        u = re.search(r'href="(https://members\.3vchamber\.com/event-calendar/Details/[^"?]+)', card)
        sd = re.search(r'itemprop="startDate" content="([^"]+)"', card)
        ed = re.search(r'itemprop="endDate" content="([^"]+)"', card)
        if not (m and sd):
            continue
        p = lambda x: dt.datetime.strptime(x.strip(), "%m/%d/%Y %I:%M:%S %p")
        s = p(sd.group(1)); e = p(ed.group(1)) if ed else s
        img = re.search(r'itemprop="image" src="([^"]+)"', card)
        img = img.group(1).replace("/c_limit,h_100,w_250/", "/c_limit,w_720/") if img else ""
        d = re.search(r'gz-events-description"[^>]*>(.*?)</p>', card, re.S)
        allday = s.hour == 0 and s.minute == 0
        uid = u.group(1).rsplit("-", 1)[-1] if u else s.isoformat()
        x = ev("3vchamber", uid, m.group(1), s, e, "Three Village area", "", u.group(1) if u else "https://www.3vchamber.com",
               d.group(1) if d else "", img, allday)
        if u and TODAY <= s.date() <= TODAY + dt.timedelta(days=DAYS_AHEAD):
            det = gz_detail(u.group(1))
            for k in ("venue", "addr", "phone", "email"):
                if det.get(k):
                    x[k] = det[k]
            if det.get("image"):
                x["image"] = det["image"]
            if det.get("desc") and len(det["desc"]) > len(x["desc"]):
                x["desc"] = clean(det["desc"], 700)
        out.append(x)
    return out


def squarespace(src, base, default_venue):
    d = json.loads(get(base + "/events?format=json"))
    et = dt.timezone(dt.timedelta(hours=-4))
    ms = lambda x: dt.datetime.fromtimestamp(int(x) / 1000, dt.timezone.utc).astimezone(et).replace(tzinfo=None)
    out = []
    for e in d.get("upcoming", []):
        loc = e.get("location") or {}
        addr = ", ".join(x for x in (loc.get("addressLine1"), loc.get("addressLine2")) if x)
        out.append(ev(src, e.get("id") or e.get("urlId"), e.get("title", ""), ms(e["startDate"]), ms(e.get("endDate") or e["startDate"]),
                      loc.get("addressTitle") or default_venue, addr, base + e.get("fullUrl", ""), e.get("excerpt") or e.get("body") or "",
                      e.get("assetUrl", ""), False))
    return out


SOURCES = [
    ("Three Village Chamber", chamber3v),
    ("Port Jefferson Chamber", lambda: tribe("pjchamber", "https://portjeffchamber.com", "Port Jefferson Village")),
    ("I Love Port Jeff", lambda: squarespace("iloveportjeff", "https://www.iloveportjeff.com", "Port Jefferson Village")),
    ("Town of Brookhaven (local)", brookhaven),
    ("Village of Port Jefferson", portjeff),
    ("Emma S. Clark Library", emmaclark),
    ("Stony Brook Village Center", lambda: tribe("sbv", "https://stonybrookvillage.com", "Stony Brook Village Center")),
    ("Long Island Museum", lambda: tribe("lim", "https://longislandmuseum.org", "The Long Island Museum")),
    ("Ward Melville Heritage Org", lambda: tribe("wmho", "https://wmho.org", "Ward Melville Heritage Organization")),
]


# ---------- BD ----------
def bd(method, path, data=None):
    body = urllib.parse.urlencode(data).encode() if data is not None else None
    h = {"X-Api-Key": KEY, "User-Agent": "3VL-events/1.0"}
    if body is not None:
        h["Content-Type"] = "application/x-www-form-urlencoded"
    with urllib.request.urlopen(urllib.request.Request(SITE + path, data=body, method=method, headers=h), timeout=60) as r:
        return json.load(r)


def existing_keys():
    keys, page = set(), None
    while True:
        d = bd("GET", "/api/v2/data_posts/get?limit=100&property=data_id&property_value=8" + ("&page=%s" % page if page else ""))
        for p in d.get("message") or []:
            keys.add((re.sub(r"[^a-z0-9]", "", (p.get("post_title") or "").lower()), (p.get("post_start_date") or "")[:8]))
        page = d.get("next_page")
        if not page or not d.get("message"):
            break
    return keys


def fmt_time(t):
    return t.strftime("%I:%M %p").lstrip("0")


def content(e):
    parts = []
    if e["desc"]:
        parts.append("<p>%s</p>" % html.escape(e["desc"]))
    when = e["start"].strftime("%A, %B ") + str(e["start"].day)
    if not e["allday"]:
        when += ", " + fmt_time(e["start"]) + ("" if e["end"] == e["start"] else " to " + fmt_time(e["end"]))
    parts.append("<p><strong>When:</strong> %s</p>" % when)
    if e["venue"] or e["addr"]:
        parts.append("<p><strong>Where:</strong> %s</p>" % html.escape(", ".join(x for x in (e["venue"], e["addr"]) if x)))
    if e["url"]:
        parts.append('<p><a href="%s" target="_blank" rel="noopener">Event details from the organizer &rarr;</a></p>' % html.escape(e["url"]))
    parts.append("<p><em>Plans change, so check with the organizer before you go. Listed by Three Village Local.</em></p>")
    return "".join(parts).replace("\\", "")


def main(mode):
    state = json.load(open(STATE)) if os.path.exists(STATE) else {}
    events, counts = [], {}
    for name, fn in SOURCES:
        try:
            got = fn()
        except Exception as ex:
            got = []
            counts[name] = "ERROR %s" % ex
        else:
            counts[name] = len(got)
        events += got
    horizon = TODAY + dt.timedelta(days=DAYS_AHEAD)
    SKIP = re.compile(r"cancel+ed|postponed|delayed opening|library closed|\bclosed\b|meeting|work session|advisory council|board of trustees|zoning board|planning board", re.I)
    events = [e for e in events if TODAY <= e["start"].date() <= horizon and e["title"] and not SKIP.search(e["title"])]
    have = existing_keys() if KEY else set()
    new, seen = [], set()
    for e in sorted(events, key=lambda x: x["start"]):
        k = (re.sub(r"[^a-z0-9]", "", e["title"].lower()), e["start"].strftime("%Y%m%d"))
        if e["uid"] in state or k in have or k in seen:
            continue
        seen.add(k)
        new.append(e)
    report = ["Fetched: " + ", ".join("%s %s" % (n, c) for n, c in counts.items()),
              "In the next %d days, not already on the calendar: %d" % (DAYS_AHEAD, len(new))]
    for e in new[:400]:
        report.append("%s | %s | %s | %s" % (e["start"].strftime("%a %b %d %I:%M%p") if not e["allday"] else e["start"].strftime("%a %b %d (all day)"),
                                             e["title"], e["venue"], e["src"]))
    open(os.path.join(ROOT, "events_report.txt"), "w", encoding="utf-8").write("\n".join(report))
    print("\n".join(report[:3]))
    if mode != "publish":
        return
    made = 0
    for e in new:
        data = {"data_id": "8", "data_type": "20", "user_id": HOUSE_USER, "post_status": "1",
                "post_title": e["title"], "post_content": content(e),
                "post_start_date": e["start"].strftime("%Y%m%d"), "post_expire_date": e["end"].strftime("%Y%m%d"),
                "post_location": e["addr"] or e["venue"], "post_venue": e["venue"], "post_url": e["url"]}
        if not e["allday"]:
            data["start_time"] = fmt_time(e["start"])
            data["end_time"] = fmt_time(e["end"])
        if e["image"]:
            data["post_image"] = e["image"].split("?")[0]
            data["auto_image_import"] = "1"
        try:
            r = bd("POST", "/api/v2/data_posts/create", data)
            pid = (r.get("message") or {}).get("post_id") if isinstance(r.get("message"), dict) else None
            state[e["uid"]] = pid or "created"
            made += 1
        except Exception as ex:
            print("FAILED", e["title"], ex)
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    json.dump(state, open(STATE, "w"), indent=1)
    print("Created %d events." % made)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "dry")
