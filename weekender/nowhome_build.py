"""Server-rendered homepage sections for /now (9/28/2026, owner-approved):
  - Featured Local Businesses (all VIPs) after Top Things to Do
  - Browse Local Businesses chips + Latest Local Stories before the business CTA
  - schema.org Event JSON-LD for this edition's events
Same markup/classes as site/p3/nowhome.js, so the page looks identical; the JS only rotates the VIP order daily and refreshes stories.
Rendered into the HTML so Google and AI crawlers (which often don't run JS) can see the business + story links."""
import datetime, html, json, os, re, subprocess
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://www.threevillagelocal.com"
IDX = "https://raw.githubusercontent.com/threevillagelocal-cloud/3vl-assets/master/search/index.json"
ET = ZoneInfo("America/New_York")

ICO = {"utensils": '<path d="M7 3v8M5 3v5a2 2 0 0 0 4 0V3M7 11v10M17 3c-2 0-3 3-3 6s1 4 3 4v8"/>',
       "home": '<path d="M3 10.5L12 3l9 7.5M5 9v12h14V9M10 21v-6h4v6"/>',
       "hammer": '<path d="M13 7l-9 9 3 3 9-9M12 4h5l3 3v2l-2 2-5-5z"/>',
       "pulse": '<path d="M20.8 5.6a5 5 0 0 0-7.1 0L12 7.3l-1.7-1.7a5 5 0 1 0-7.1 7.1L12 21l8.8-8.3a5 5 0 0 0 0-7.1z"/>',
       "key": '<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M17 6l3 3M15 8l2 2"/>',
       "scale": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 6a3 3 0 0 0 6 0L5 7M19 7l-3 6a3 3 0 0 0 6 0l-3-6"/>',
       "scissors": '<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4L8.1 15.9M14.5 14.5L20 20M8.1 8.1L12 12"/>',
       "dollar": '<circle cx="12" cy="12" r="9"/><path d="M15 9.5c-.5-1-1.6-1.5-3-1.5-1.7 0-3 .8-3 2s1.3 1.8 3 2 3 .9 3 2.1-1.3 2-3 2c-1.5 0-2.6-.6-3-1.6M12 6.5v11"/>'}
CATS = [("Restaurants", "/restaurant", "utensils"), ("Home Services", "/home-services", "home"), ("Contractors", "/contractor", "hammer"),
        ("Health & Wellness", "/health-wellness", "pulse"), ("Real Estate", "/real-estate-services", "key"), ("Attorneys", "/attorney", "scale"),
        ("Beauty", "/beauty-personal-care", "scissors"), ("Financial", "/financial-services", "dollar")]


def esc(s):
    return html.escape(str(s or ""), quote=True)


def get(url):
    return subprocess.run(["curl", "-s", "-L", "-A", "Mozilla/5.0", url], capture_output=True, text=True, encoding="utf-8", errors="ignore").stdout


def town(t):
    t = (t or "").strip()
    return "Setauket" if re.match(r"^(East\s+)?Setauket", t, re.I) else t


def head(t, small="", link="", lt=""):
    l = ('<a class="nh-more" href="%s">%s &rarr;</a>' % (link, lt)) if link else ""
    sm = (small + (" &middot; " if l else "") if small else "") + l
    return '<h2 class="wk-h2"><span>%s</span>%s</h2>' % (t, ("<small>%s</small>" % sm) if sm else "")


def featured():
    try:
        idx = json.loads(get(IDX))
    except Exception:
        return ""
    try:
        meta = json.load(open(os.path.join(HERE, "..", "site", "p3", "vip_meta.json"), encoding="utf-8"))
    except Exception:
        meta = {}
    v = [m for m in idx.get("members", []) if m.get("p") == "vip"]
    day = int(datetime.datetime.now(ET).timestamp() // 86400)
    v.sort(key=lambda x: (int(x["id"]) * 7919 + day * 104729) % 1000)  # same fair daily rotation as nowhome.js
    cards = []
    for m in v:
        mt = meta.get(str(m["id"])) or {}
        r, n = mt.get("rating"), mt.get("reviews")
        line = (('<span class="nh-st">&#9733; %.1f</span>' % float(r)) + ("(%s) &middot; " % n if n else "&middot; ")) if r else ""
        line += esc(town(m.get("t")) or m.get("c") or "")
        cards.append('<a class="nh-biz" href="%s" data-biz="%s" data-id="%s"><span class="nh-logo" style="background-image:url(\'%s\')"></span>'
                     '<span class="nh-t"><b class="nh-n">%s</b><span class="nh-m">%s</span><span class="nh-vip">&#9733; VIP</span></span></a>' % (
                         esc(m["u"]), esc(m["n"]), esc(m["id"]), esc(m.get("l")), esc(m["n"]), line))
    if not cards:
        return ""
    return ('<section class="wk-sec nh-sec" id="nh-feat">' + head("Featured Local Businesses", "Neighbors who support Three Village Local", "/search_results", "See all businesses")
            + '<div class="nh-row" id="nh-frow">' + "".join(cards) + "</div></section>")


def stories(n=3):
    h = get(SITE + "/blog")
    out = []
    for b in re.split(r'<div class="row-fluid search_result', h)[1:]:
        a = re.search(r'<a class="h3[^"]*"[^>]*href="([^"]+)"[^>]*>\s*(.*?)\s*</a>', b, re.S)
        im = re.search(r'class="search_result_image[^"]*"[^>]*src="([^"]+)"', b)
        d = re.search(r"Posted\s+(\d+)/(\d+)/(\d+)", b)
        if not a:
            continue
        dt = datetime.date(int(d.group(3)), int(d.group(1)), int(d.group(2))) if d else None
        out.append({"h": a.group(1), "t": html.unescape(re.sub(r"<[^>]+>", "", a.group(2))).strip(), "img": im.group(1) if im else "",
                    "d": ("%s %d, %d" % (["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"][dt.month - 1], dt.day, dt.year)) if dt else "",
                    "ts": dt.toordinal() if dt else 0})
    out.sort(key=lambda x: -x["ts"])
    return out[:n]


def explore():
    chips = "".join('<a class="nh-cat" href="%s"><svg viewBox="0 0 24 24">%s</svg>%s</a>' % (u, ICO[i], esc(t)) for t, u, i in CATS)
    st = stories()
    srow = "".join('<a class="nh-story" href="%s"><span class="nh-sim" style="background-image:url(\'%s\')"></span><span class="nh-sb">%s<b>%s</b></span></a>' % (
        esc(x["h"]), esc(x["img"]), ("<i>%s</i>" % esc(x["d"])) if x["d"] else "", esc(x["t"])) for x in st)
    return ('<section class="wk-sec nh-sec" id="nh-explore">' + head("Browse Local Businesses")
            + '<div class="nh-cats">' + chips + '<a class="nh-cat nh-allc" href="/categories">All categories &rarr;</a></div>'
            + ('<div style="height:38px"></div>' + head("Latest Local Stories", "", "/blog", "All stories") + '<div class="nh-row" id="nh-srow">' + srow + "</div>" if srow else "")
            + "</section>")


def _iso(s):
    dt = datetime.datetime.fromisoformat(s)
    return dt.replace(tzinfo=ET).isoformat()


def event_schema(d, img):
    """schema.org Event list for Google event results + AI answers. Only events with a real start time and a venue."""
    V = d.get("venues", {})
    items = []
    for e in d.get("events", []) + d.get("allweekend", []):
        if not e.get("start") or e.get("status"):
            continue
        v = V.get(e.get("venue"), {})
        ongoing = bool(e.get("when"))
        ev = {"@type": "Event", "name": e["title"], "description": e.get("desc", ""),
              "startDate": _iso(d["starts"] + "T00:00") if ongoing and d.get("starts") else _iso(e["start"]),
              "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
              "eventStatus": "https://schema.org/EventScheduled",
              "location": {"@type": "Place", "name": v.get("name") or e.get("venue", ""),
                           "address": {"@type": "PostalAddress", "streetAddress": (v.get("addr") or "").split(",")[0].strip(),
                                       "addressLocality": (v.get("addr") or ",").split(",")[-1].strip() or "Setauket", "addressRegion": "NY", "addressCountry": "US"}}}
        if e.get("end") and not ongoing:
            ev["endDate"] = _iso(e["end"])
        if ongoing and e.get("until"):
            ev["endDate"] = _iso(e["until"] + ("T23:59" if "T" not in e["until"] else ""))
        if e.get("img"):
            ev["image"] = [img(e["img"])]
        if e.get("url"):
            ev["url"] = e["url"]
        if "free" in (e.get("tags") or []) or str(e.get("price", "")).lower() == "free":
            ev["isAccessibleForFree"] = True
            ev["offers"] = {"@type": "Offer", "price": "0", "priceCurrency": "USD", "availability": "https://schema.org/InStock", "url": e.get("url", SITE + "/")}
        if v.get("ll"):
            ev["location"]["geo"] = {"@type": "GeoCoordinates", "latitude": v["ll"][0], "longitude": v["ll"][1]}
        items.append(ev)
    if not items:
        return ""
    data = {"@context": "https://schema.org", "@type": "ItemList", "name": "Things to do in the Three Village area this week",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": ev} for i, ev in enumerate(items)]}
    def clean(o):  # BD strips backslashes from post content, so the JSON must not need any escape characters
        if isinstance(o, dict):
            return {k: clean(x) for k, x in o.items()}
        if isinstance(o, list):
            return [clean(x) for x in o]
        if isinstance(o, str):
            o = o.replace('"', "”").replace("\\", "").replace("<", "").replace(">", "")
            return re.sub(r"\s+", " ", o).strip()
        return o
    js = json.dumps(clean(data), ensure_ascii=False)
    if "\\" in js:
        return ""  # never ship JSON that BD would corrupt
    return '<script type="application/ld+json">%s</script>' % js
