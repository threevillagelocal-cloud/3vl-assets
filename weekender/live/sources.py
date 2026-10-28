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


def get(url, headers=None, timeout=40, data=None):
    req = urllib.request.Request(url, data=data, headers=headers or UA)
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
    "the reboli center for art and history": "64 Main St, Stony Brook, NY 11790",
    "sweetbriar nature center": "62 Eckernkamp Dr, Smithtown, NY 11787",
    "mather house museum": "115 Prospect St, Port Jefferson, NY 11777",
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
    start = (TODAY - dt.timedelta(days=45)).isoformat()   # reach back so multi-day events already underway are included
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
    """Emma S. Clark Library RSS. Uses the library's own photo, room and categories; drops policy/registration boilerplate
    (library feedback 9/28/2026: an adult cooking class was tagged Kids from the unattended-children notice, and
    descriptions opened with boilerplate)."""
    t = get("https://emmaclark.librarycalendar.com/events/feed/rss")
    out = []
    BOILER = [r"Please review the program description for any potential allergies[^.]*\.",
              r"Children may not be left unattended\.?[^.]*\.[^.]*\.",
              r"Registration is required\.", r"Registration is not required\.",
              r"Registration (?:starts|end|ends|opens|closes):\s*\d{2}/\d{2}/\d{4}\s*@\s*\d{1,2}:\d{2}\s*[ap]m",
              r"Simply supply the barcode number from your local library card to register\.",
              r"Parents must stay in the Children'?s Library when their children are in a Children'?s program\.",
              r"Pictures/Videos taken at or for library events.*$"]
    for item in re.findall(r"<item>(.*?)</item>", t, re.S):
        def tag(n):
            m = re.search(r"<%s[^>]*>(.*?)</%s>" % (n, n), item, re.S)
            return html.unescape(re.sub(r"^<!\[CDATA\[|\]\]>$", "", m.group(1).strip())) if m else ""
        link, title = tag("link"), tag("title")
        raw = re.search(r"<description>(.*?)</description>", item, re.S)
        raw = raw.group(1) if raw else ""
        im = re.search(r'<img[^>]+src="([^"]+)"', raw)
        image = im.group(1) if im else ""
        txt = clean(html.unescape(re.sub(r"<!\[CDATA\[.*?\]\]>", " ", raw, flags=re.S)))   # unescape first so <p> breaks become spaces
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
        rest = rest.strip()
        venue, room = "Emma S. Clark Memorial Library", ""
        if rest.startswith("Off Site"):
            venue, rest = "Off site (Emma S. Clark Library program)", rest[8:]
        elif rest.startswith("Virtual Programming"):
            venue, rest = "Online (Emma S. Clark Library program)", rest[len("Virtual Programming"):]
        else:
            rm = re.match(r"(.{3,60}?)\s+Emma S\. Clark Memorial Library\s*", rest)
            if rm:
                room, rest = rm.group(1).strip(), rest[rm.end():]
            else:
                rest = re.sub(r"^Emma S\. Clark Memorial Library\s*", "", rest)
        for rx in BOILER:
            rest = re.sub(rx, " ", rest, flags=re.I | re.S)
        rest = rest.replace("childrena little", "children a little")   # library typo, owner OK to fix (9/28)
        body = clean(rest, 600)
        cats = [html.unescape(c).strip() for c in re.findall(r"<category>(.*?)</category>", item)]
        x = ev("emmaclark", link.rstrip("/").split("/")[-1], title, s, e, venue, "120 Main St, Setauket, NY 11733", link, body, image, allday)
        if room:
            x["room"] = room
            x["venue"] = "%s, %s" % (venue, room) if len(venue) + len(room) < 88 else venue
        x["cats"] = cats
        x["reg"] = bool(re.search(r"Registration is required", txt, re.I))
        out.append(x)
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


def _et():
    try:
        from zoneinfo import ZoneInfo
        return ZoneInfo("America/New_York")
    except Exception:
        return dt.timezone(dt.timedelta(hours=-5 if TODAY.month in (11, 12, 1, 2, 3) else -4))


def squarespace(src, base, default_venue, path="/events"):
    """Squarespace events collection (?format=json). Times are converted with the real Eastern zone (the old fixed -4 offset
    put every winter event an hour early)."""
    d = json.loads(get(base + path + "?format=json"))
    et = _et()
    ms = lambda x: dt.datetime.fromtimestamp(int(x) / 1000, dt.timezone.utc).astimezone(et).replace(tzinfo=None)
    out = []
    for e in d.get("upcoming", []):
        loc = e.get("location") or {}
        addr = ", ".join(x for x in (loc.get("addressLine1"), loc.get("addressLine2")) if x)
        out.append(ev(src, e.get("id") or e.get("urlId"), e.get("title", ""), ms(e["startDate"]), ms(e.get("endDate") or e["startDate"]),
                      loc.get("addressTitle") or default_venue, addr, base + e.get("fullUrl", ""), e.get("excerpt") or e.get("body") or "",
                      e.get("assetUrl", ""), False))
    return out


def limehof():
    """Long Island Music & Entertainment Hall of Fame (Stony Brook): events page is a plain HTML grid, no feed.
    Only shows held at the museum itself (skips their off-site shows, e.g. Tilles Center)."""
    base = "https://www.limusichalloffame.org/events/"
    s = get(base)
    s = s.decode("utf-8", "replace") if isinstance(s, bytes) else s
    out, mon = [], "jan feb mar apr may jun jul aug sep oct nov dec".split()
    for blk in s.split('<div class="gridRow')[1:]:
        g = lambda c: clean(re.sub(r"<[^>]+>", " ", (re.search(r'<div class="%s">(.*?)</div>' % c, blk, re.S) or [None, ""])[1]))
        d, t, title, venue = g("date"), g("time"), g("event"), g("venue")
        m = re.match(r"([A-Za-z]{3})\w*\.?\s+(\d{1,2})", d)
        if not m or not title or "hall of fame" not in venue.lower():
            continue
        mo, day = mon.index(m.group(1).lower()) + 1, int(m.group(2))
        yr = TODAY.year + (1 if mo < TODAY.month - 2 else 0)
        tm = re.match(r"(\d{1,2}):(\d{2})\s*([ap])m", t.lower())
        h, mi = (int(tm.group(1)) % 12 + (12 if tm.group(3) == "p" else 0), int(tm.group(2))) if tm else (0, 0)
        if tm and tm.group(3) == "a" and h < 8:      # site typo guard: "3:00 am" shows are afternoon shows
            h += 12
        start = dt.datetime(yr, mo, day, h, mi)
        img = (re.search(r'<img src="([^"]+)"', blk) or [None, ""])[1]
        desc = clean(re.sub(r"<[^>]+>", " ", (re.search(r'<span id="feature"[^>]*>(.*?)</span>\s*</div>', blk, re.S) or [None, ""])[1]))
        price = g("buy")
        if price and price.lower() != "buy tickets":
            desc = (price + ". " + desc).strip()
        out.append(ev("limehof", "%s-%s" % (start.strftime("%Y%m%d%H%M"), re.sub(r"[^a-z0-9]+", "-", title.lower())[:40]), title, start,
                      start + dt.timedelta(hours=2), "The Long Island Music and Entertainment Hall of Fame", "", base, desc, img, not tm))
    return out


def staller():
    """Staller Center for the Arts (Stony Brook University). The official calendar at stallercenter.com/Calendar.php is an
    Elfsight event-calendar widget; this reads the same public widget data the page loads (show, hall, time, photo, ticket link).
    Shows the center has hidden from its calendar (visible=false) are skipped."""
    page = "https://www.stallercenter.com/Calendar.php"
    d = json.loads(get("https://core.service.elfsight.com/p/boot/?page=%s&w=%s" % (
        urllib.parse.quote(page, safe=""), "e45e5135-f1f5-4969-84d5-c6e8a75e8a93")))
    s = list(d["data"]["widgets"].values())[0]["data"]["settings"]
    halls = {x.get("id"): x.get("name", "") for x in s.get("locations") or []}
    out = []
    for e in s.get("events") or []:
        st, en = e.get("start") or {}, e.get("end") or {}
        if e.get("visible") is False or (e.get("repeatPeriod") or "noRepeat") != "noRepeat" or not st.get("date") or not e.get("name"):
            continue
        timed = bool(st.get("time"))
        start = dt.datetime.fromisoformat(st["date"] + "T" + (st.get("time") or "00:00"))
        end = dt.datetime.fromisoformat((en.get("date") or st["date"]) + "T" + (en.get("time") or st.get("time") or "00:00"))
        if end < start:
            end = start
        hall = halls.get((e.get("location") or [""])[0], "")
        venue = "Staller Center for the Arts" + (", " + hall if hall else "")
        link = ""
        for a in e.get("actions") or []:
            v = ((a.get("link") or {}).get("value") or "").strip()
            if v.startswith("http") and not v.endswith("evt="):
                link = v
                break
        img = (e.get("coverImage") or {}).get("url", "") if isinstance(e.get("coverImage"), dict) else ""
        out.append(ev("staller", e.get("id") or start.isoformat(), html.unescape(e["name"]), start, end, venue,
                      "100 Nicolls Rd, Stony Brook, NY 11794", link or page, e.get("description") or "", img, not timed))
    return out


def theatre3():
    """Theatre Three (Port Jefferson): the box office calendar (getmytix venued_events, the calendar on theatrethree.com/events-calendar).
    One entry per performance; each show's description and poster come from its event file."""
    base = "https://theatrethree.getmytix.net"
    data = base + "/_wss/clients/434/venued_events/"
    m, months = TODAY.replace(day=1), []
    for _ in range(3):   # this month + the next two (covers the 60-day sync window)
        months.append(m)
        m = (m + dt.timedelta(days=32)).replace(day=1)
    info, seen, out = {}, set(), []
    for mo in months:
        d = json.loads(get(base + "/_appajax/venued_events/ajax/veHandler?command=get_calendar_events&month=" + mo.isoformat()))
        for day in d.get("days") or []:
            for x in day.get("events") or []:
                if x.get("event_date_id") in seen or not x.get("event_date"):
                    continue
                seen.add(x.get("event_date_id"))
                eid = str(x.get("event_id"))
                if eid not in info:
                    try:
                        info[eid] = json.loads(get(data + "data/event_%s.json" % eid, timeout=20))
                    except Exception:
                        info[eid] = {}
                i = info[eid]
                tm = (x.get("event_time") or "00:00:00")[:5]
                start = dt.datetime.fromisoformat(x["event_date"] + "T" + tm)
                pic = i.get("event_image") or i.get("ticket_image") or ""
                img = data + urllib.parse.quote(pic) if pic else ""
                title = html.unescape(x.get("event_name") or x.get("display_name") or "").strip()   # display_name is cut short with "..."
                if x.get("subtitle"):
                    title += ": " + html.unescape(x["subtitle"])
                y = ev("theatre3", x["event_date_id"], title, start, start, "Theatre Three", "412 Main St, Port Jefferson, NY 11777",
                       base + "/tickets" + (i.get("permalink") or ""), i.get("description") or "", img, tm == "00:00")
                y["show_id"] = eid
                out.append(y)
    return out


def gallerynorth():
    """Gallery North (Setauket): the gallery's own events calendar (Calee app on gallerynorth.org). One-time events and
    exhibitions only; weekly multi-session classes (is_recurring) are left out."""
    from urllib.parse import urlencode
    body = urlencode({"shop": "gallerynorth.myshopify.com", "req_calling_method": "get_front_event_data",
                      "calendar_type": "original", "calendar_id": "1"}).encode()
    d = json.loads(get("https://theweeapps.com/caly-v2/api.php", data=body))
    out = []
    for e in d.get("event_data") or []:
        if str(e.get("is_recurring")) == "1" or str(e.get("is_draft_event")) == "1" or not e.get("event_title"):
            continue
        s = dt.datetime.strptime(e["start_date_time"][:16], "%Y-%m-%d %H:%M")
        en = dt.datetime.strptime((e.get("end_date_time") or e["start_date_time"])[:16], "%Y-%m-%d %H:%M")
        allday = str(e.get("is_show_time")) == "0" or (s.strftime("%H:%M") == "00:00" and en.strftime("%H:%M") == "23:59")
        if allday:
            s, en = s.replace(hour=0, minute=0), en.replace(hour=0, minute=0)
        loc = (e.get("event_location") or "").strip()
        venue = "Gallery North" if not loc or loc.lower().startswith("gallery north") else "Gallery North, " + loc
        img = e.get("event_image_s3") or ""
        url = e.get("external_url") or ""
        out.append(ev("gallerynorth", e.get("event_id"), e["event_title"], s, en, venue, "90 N Country Rd, Setauket, NY 11733",
                      url if url.startswith("http") else "https://gallerynorth.org", e.get("event_details") or "",
                      img if img.startswith("http") else "", allday))
    return out


def seawolves():
    """Stony Brook University Athletics (official SIDEARM iCal). HOME games and meets on campus only (LOCATION "Stony Brook, N.Y., <facility>")."""
    t = re.sub(r"\r?\n[ \t]", "", get("https://stonybrookathletics.com/calendar.ashx/calendar.ics"))
    et, out = _et(), []
    for block in re.findall(r"BEGIN:VEVENT(.*?)END:VEVENT", t, re.S):
        f = {}
        for line in block.strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                f[k.split(";")[0]] = (v.strip(), k)
        loc = f.get("LOCATION", ("", ""))[0].replace("\\,", ",")
        m = re.match(r"Stony Brook, N\.?Y\.?,\s*(.+)$", loc)
        title = f.get("SUMMARY", ("", ""))[0].replace("\\,", ",").strip()
        if not m or " vs " not in title or "DTSTART" not in f:
            continue
        def when(key):
            v, k = f.get(key, f["DTSTART"])
            if "VALUE=DATE" in k or len(v) == 8:
                return dt.datetime.strptime(v[:8], "%Y%m%d"), True
            d = dt.datetime.strptime(v[:15], "%Y%m%dT%H%M%S")
            if v.endswith("Z"):
                d = d.replace(tzinfo=dt.timezone.utc).astimezone(et).replace(tzinfo=None)
            return d, False
        s, allday = when("DTSTART")
        e, _ = when("DTEND")
        if allday and e > s:
            e -= dt.timedelta(days=1)   # iCal all-day end is exclusive
        title = re.sub(r"^Stony Brook University ", "Stony Brook Seawolves ", title)
        url = html.unescape(f.get("URL", ("", ""))[0]) or "https://stonybrookathletics.com/calendar"
        out.append(ev("seawolves", f.get("UID", (s.isoformat(), ""))[0], title, s, e, m.group(1).strip() + ", Stony Brook University",
                      "100 Nicolls Rd, Stony Brook, NY 11794", url, "Stony Brook University home game. Tickets, times and parking: stonybrookathletics.com.", "", allday))
    return out


def social():
    """Events a local business announced on its OWN Instagram with the date, a start time and the place written in the post
    (weekender/live/social_events.py "confirmed"; everything less clear goes to the owner's review email instead)."""
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "social_events.json")
    d = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else json.loads(
        get("https://raw.githubusercontent.com/threevillagelocal-cloud/3vl-assets/master/weekender/live/social_events.json"))
    out = []
    for x in d.get("confirmed") or []:
        try:
            s = dt.datetime.fromisoformat(x["date"] + "T" + x["start"])
        except (KeyError, ValueError):
            continue
        e = dt.datetime.fromisoformat(x["date"] + "T" + x["end"]) if x.get("end") else s
        if e < s:
            e = s
        y = ev("social", x["post"], x["title"], s, e, x.get("venue") or x.get("org", ""), x.get("addr", ""), x.get("url", ""),
               x.get("desc", ""), x.get("img", ""), False)
        y["org"], y["org_url"] = x.get("org", ""), x.get("org_url", "")
        y["desc_from"] = "the Instagram post by %s" % (x.get("org") or "the organizer")
        out.append(y)
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
    ("LI Music Hall of Fame", limehof),
    # added 10/28/2026 (owner: events were library heavy; check every reliable organizer calendar)
    ("Staller Center for the Arts", staller),
    ("Theatre Three", theatre3),
    ("Gallery North", gallerynorth),
    ("Reboli Center", lambda: squarespace("reboli", "https://rebolicenter.org", "The Reboli Center for Art and History")),
    ("Sweetbriar Nature Center", lambda: squarespace("sweetbriar", "https://www.sweetbriarnc.org", "Sweetbriar Nature Center", "/new-events")),
    ("Historical Society of Greater Port Jefferson", lambda: squarespace("pjhistorical", "https://www.portjeffhistorical.org", "Mather House Museum")),
    # ("Stony Brook Athletics (home games)", seawolves),   # owner 10/28/2026: "don't put stony brook sports on the events"
    ("Local business Instagram posts", social),
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
