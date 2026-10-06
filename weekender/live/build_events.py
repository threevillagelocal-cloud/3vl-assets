"""Builds weekender/live/events.json for Three Village Now: every local event from today through the next 8 days.
Runs hourly in GitHub Actions (public sources only, no API keys). The /now page reads this file live."""
import datetime as dt, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sources as S

HERE = os.path.dirname(os.path.abspath(__file__))
TAGS = [
    ("kids", r"\bkids?\b|storytime|toddler|\btots?\b|family fun|grades? (?:pre-?k|k|[0-9])|\bteens?\b|\btweens?\b|children|\blego\b|pok.mon"),
    ("music", r"\bmusic|concert|\bband\b|jazz|blues|symphony|orchestra|live performance|\bsongs?\b|guitar|\bdj\b"),
    ("history", r"histor|culper|\bspy\b|revolution|colonial|1776|house tour|heritage|america 250|gravestone"),
    ("food", r"farmers market|\bfood|dinner|lunch|brunch|tasting|\bwine\b|\bbeer\b|chowder|charcuterie|cheese|prix fixe|cooking"),
    ("stage", r"theat|\bfilm|movie|screening|comedy|\bplay\b|musical|lecture|\btalk\b"),
    ("outdoor", r"outdoor|\bpark\b|harbor|\bwalk|trail|farmers market|festival|\bfair\b|\brace\b|\b5k\b|garden|beach|walking tour"),
    ("arts", r"\bart\b|\barts\b|paint|drawing|stitch|knit|crochet|exhibit|gallery|workshop|\bcraft"),
]
ICON = {"kids": "&#129490;", "music": "&#127928;", "history": "&#128373;&#65039;", "food": "&#127822;", "stage": "&#127917;",
        "outdoor": "&#127795;", "arts": "&#127912;", "free": "&#127903;&#65039;"}


LIB_FRONT = "https://cdn.jsdelivr.net/gh/threevillagelocal-cloud/3vl-assets@20bba76f6e4b/events-cal/img/emma-clark.jpg"   # front of the library, for library events with no photo (owner 9/28)
# Emma S. Clark Library: tags come ONLY from the library's own categories (library feedback 9/28/2026)
LIB_TAGS = {"Children": "kids", "Story Time": "kids", "Mommy & Me": "kids",
            "Music & Performance": "music", "History": "history", "Cooking & Tasting": "food",
            "Movie": "stage", "Arts & Crafts": "arts"}


def tags_for(e):
    if e.get("src") == "emmaclark" and "cats" in e:
        t = []
        for c in e["cats"]:
            k = LIB_TAGS.get(c)
            if k and k not in t:
                t.append(k)
        if re.search(r"\bfree\b", e["title"] + " " + e["desc"], re.I):
            t.insert(0, "free")
        return t[:3]
    blob = (e["title"] + " " + e["desc"]).lower()
    t = [k for k, rx in TAGS if re.search(rx, blob)]
    if re.search(r"\bfree\b", blob):
        t.insert(0, "free")
    return t[:3] or ["arts"]


SITE = "https://www.threevillagelocal.com"


def _norm(t):
    return re.sub(r"[^a-z0-9]", "", re.sub(r"\b(the|a|an|annual|\d+(st|nd|rd|th))\b", "", t.lower()))



_GENERIC = {"market", "farmers", "outdoor", "summer", "live", "music", "event", "events", "night", "family", "library", "village",
            "street", "center", "centre", "performance", "concert", "festival", "local", "weekend", "annual", "museum", "school"}


def _toks(t):
    return {w for w in re.findall(r"[a-z]{4,}", (t or "").lower())} - {"with", "from", "this", "that", "free"}


def _merge_aliases(events):
    """SEO audit 10/4/2026: the same occurrence imported from two calendars under different names (e.g. "Port Jefferson Farmers
    Market" + "Outdoor Summer Farmers Market", or three Marian Mastrorilli listings) showed up twice in the cards and in Google's
    event data. Same start minute, different source, and the same place (2+ shared venue words) or a shared distinctive title
    word -> keep the first (curated 3VL copy sorts first). Same-source pairs are left alone (libraries list real parallel events)."""
    keep = []
    for e in sorted(events, key=lambda x: (x["start"][:16], x["src"] != "3vl", not x.get("page"))):
        dup = False
        for k in keep:
            if k["start"][:16] != e["start"][:16] or k.get("src") == e.get("src"):
                continue
            vt = _toks(k.get("venue")) & _toks(e.get("venue"))
            tt = {w for w in _toks(k["title"]) & _toks(e["title"]) if len(w) >= 6 and w not in _GENERIC}
            if len(vt) >= 2 or tt:
                dup = True
                break
        if not dup:
            keep.append(e)
    gone = len(events) - len(keep)
    if gone:
        print("merged %d duplicate event listing(s) from other calendars" % gone)
    return keep

def event_pages():
    """Our own /events pages, from the site's public calendar feed: [(normalized title, 'YYYY-MM-DD' Eastern, url)].
    Lets every homepage card link to the event's page on threevillagelocal.com (10/1/2026). Empty list on any error."""
    import html, urllib.request
    try:
        req = urllib.request.Request(SITE + "/event-calendar-json", headers={"User-Agent": "Mozilla/5.0 (3VL events)"})
        rows = json.load(urllib.request.urlopen(req, timeout=40)).get("result") or []
    except Exception as ex:
        print("event pages unavailable: %s" % ex)
        return []
    try:
        from zoneinfo import ZoneInfo
        tz = ZoneInfo("America/New_York")
    except Exception:
        tz = None
    out = []
    for r in rows:
        try:
            d = dt.datetime.fromtimestamp(int(r["start"]) / 1000, dt.timezone.utc)
            d = d.astimezone(tz) if tz else d - dt.timedelta(hours=4 if 3 < d.month < 11 else 5)
            u = r["url"]
            out.append((_norm(html.unescape(r["title"])), d.strftime("%Y-%m-%d"), ("https:" + u) if u.startswith("//") else u))
        except Exception:
            continue
    return out


def page_for(pages, title, start):
    """Same title on the same day; else a longer/shorter version of the title that day; else the only page with that exact title."""
    n, day = _norm(title), start[:10]
    same = [p for p in pages if p[1] == day]
    for p in same:
        if p[0] == n:
            return p[2]
    near = [p for p in same if len(n) >= 8 and len(p[0]) >= 8 and (n in p[0] or p[0] in n)]
    if near:
        return min(near, key=lambda p: abs(len(p[0]) - len(n)))[2]
    exact = [p for p in pages if p[0] == n]
    return exact[0][2] if len(exact) == 1 else ""


_LISTINGS = {}


def listing_for(name):
    """3VL profile URL for a business name ('' if it has no listing): nightly search index + weekender/biz_links.json."""
    nm = lambda x: re.sub(r"[^a-z0-9]", "", re.sub(r"%s(.*?%s)|&[a-z#0-9]+;" % ("\\", "\\"), "", x.lower()).replace("the ", ""))
    if not _LISTINGS:
        root = os.path.dirname(HERE)
        try:
            for k, u in json.load(open(os.path.join(root, "biz_links.json"), encoding="utf-8")).items():
                if "threevillagelocal.com" in u:
                    _LISTINGS[nm(k.replace("&#x27;", "").replace("&rsquo;", ""))] = u
            for m in json.load(open(os.path.join(os.path.dirname(root), "search", "index.json"), encoding="utf-8")).get("members", []):
                _LISTINGS.setdefault(nm(m["n"]), m["u"])
        except Exception as ex:
            print("listings unavailable: %s" % ex)
        _LISTINGS.setdefault("", "")
    k = nm(name.replace("'", "").replace("\u2019", ""))
    if k in _LISTINGS:
        return _LISTINGS[k]
    near = [u for kk, u in _LISTINGS.items() if kk and len(k) >= 6 and len(kk) >= 6 and (k in kk or kk in k)]
    return near[0] if len(near) == 1 else ""


def status_for(title):
    m = re.search(r"\b(cancel+ed|postponed|rescheduled)\b", title, re.I)
    return m.group(1).capitalize().replace("Cancelled", "Canceled") if m else ""


def main():
    today = dt.date.today()
    horizon = today + dt.timedelta(days=10)
    out, counts = [], {}
    for name, fn in S.SOURCES:
        try:
            got = fn()
        except Exception as ex:
            counts[name] = "error: %s" % ex
            continue
        counts[name] = len(got)
        for e in got:
            end = e.get("end") or e["start"]
            if not (e["start"].date() <= horizon and max(e["start"], end).date() >= today):   # upcoming, or started earlier and still running
                continue
            if re.search(r"country house|bench bar|home ?baked by julia", e["title"] + " " + e["venue"], re.I):   # never promote (owner requests: Country House; The Bench Bar & Grill 10/1/2026; Homebaked By Julia 10/5/2026)
                continue
            if re.search(r"meeting|work session|advisory council|board of trustees|zoning board|planning board|delayed opening|library closed", e["title"], re.I):
                continue
            st = status_for(e["title"])
            title = re.sub(r"^\s*(cancel+ed|postponed)\s*[-:]\s*", "", e["title"], flags=re.I).strip()
            out.append({"id": re.sub(r"[^a-z0-9]+", "-", e["uid"].lower())[:80], "title": title, "start": e["start"].isoformat(),
                        "end": e["end"].isoformat(), "allday": e["allday"], "venue": e["venue"], "addr": e["addr"], "url": e["url"],
                        "desc": e["desc"][:260], "img": e["image"] or (LIB_FRONT if e["src"] == "emmaclark" else ""), "src": e["src"], "tags": tags_for(e), "status": st,
                        "fb": 0 if e["image"] or e["src"] != "emmaclark" else 1})   # fb=1: stand-in photo, never used for Top Things to Do
    ed = os.path.join(os.path.dirname(HERE), "2026-10-02", "weekend.json")
    if os.path.exists(ed):
        W = json.load(open(ed, encoding="utf-8"))
        base = "https://cdn.jsdelivr.net/gh/threevillagelocal-cloud/3vl-assets@master/weekender/2026-10-02/"
        for e in W["events"]:
            v = W["venues"].get(e["venue"], {})
            out.insert(0, {"id": "cur-" + e["id"], "title": e["title"], "start": e["start"], "end": e["end"], "allday": False,
                           "venue": v.get("name", ""), "addr": v.get("addr", ""), "url": e.get("url", ""), "desc": e["desc"],
                           "img": (base + e["img"] + "-720.webp") if e.get("img") else "", "src": "3vl", "tags": e["tags"][:3],
                           "status": e.get("status", ""), "pick": e["id"] in W.get("picks", []), "page": e.get("page", ""),
                           "pu": e.get("pick_until", "")})   # pu: when the card leaves Top Things to Do (before the event ends)
        for a in W.get("allweekend", []):
            if a["id"] in W.get("picks", []):
                v = W["venues"].get(a["venue"], {})
                out.insert(0, {"id": "cur-" + a["id"], "title": a["title"], "start": dt.date.today().isoformat() + "T00:00", "end": a.get("until") or W.get("ends", ""),
                               "allday": True, "ongoing": True, "whenText": a["when"], "venue": v.get("name", ""), "addr": v.get("addr", ""),
                               "url": a.get("url", ""), "desc": a["desc"], "img": (base + a["img"] + "-720.webp") if a.get("img") else "",
                               "src": "3vl", "tags": a["tags"][:3], "status": "", "pick": True, "page": a.get("page", "")})
        for o in out:
            if o.get("pick"):
                o["rank"] = W["picks"].index(o["id"][4:]) + 1 if o["id"][4:] in W["picks"] else 9
    # storm closings: closings.json entries with a "match" regex flag the same-day event (red ribbon on /now)
    cpath = os.path.join(HERE, "closings.json")
    closings = json.load(open(cpath, encoding="utf-8")) if os.path.exists(cpath) else []
    for e in out:
        e["start"] = e["start"][:19]; e["end"] = e["end"][:19]
        for c in closings:
            if c.get("match") and c["date"] <= e["start"][:10] <= c.get("until", c["date"]) and re.search(c["match"], e["title"], re.I):
                e["status"] = e["status"] or c["status"]
    # de-dupe same title + same day
    seen, final = set(), []
    for e in sorted(out, key=lambda x: (x["start"][:10], x["src"] != "3vl", x["start"])):   # curated copy wins
        k = (re.sub(r"[^a-z0-9]", "", re.sub(r"\b(the|a|an|annual|\d+(st|nd|rd|th))\b", "", e["title"].lower())), e["start"][:10])
        if k in seen:
            continue
        seen.add(k)
        final.append(e)
    final = _merge_aliases(final)
    final.sort(key=lambda x: x["start"])
    # each event's page on our own site (weekend.json "page" wins for hand-picked items); the homepage cards link there
    pages = event_pages()
    for e in final:
        e["page"] = e.get("page") or page_for(pages, e["title"], e["start"])
        # owner 10/2/2026: Stony Brook Village's long-running scarecrow voting event has no page of ours; its card goes to their page
        if not e["page"] and e.get("src") == "sbv" and re.search(r"scarecrow competition", e["title"], re.I):
            e["page"] = e.get("url", "")
    print("events with a 3VL page: %d of %d" % (sum(1 for e in final if e["page"]), len(final)))
    # Instagram specials (written by ig_specials.py); images live next to this file in ig/
    spath = os.path.join(HERE, "specials.json")
    specials = []
    if os.path.exists(spath):
        igbase = "https://raw.githubusercontent.com/threevillagelocal-cloud/3vl-assets/master/weekender/live/"
        today = dt.date.today().isoformat()
        for s in json.load(open(spath, encoding="utf-8")).get("specials", []):
            if (s.get("expires") or "9999") < today:
                continue
            if s.get("inset") and not s["inset"].startswith("http"):
                s["inset"] = igbase + s["inset"]
            s["page"] = listing_for(s.get("biz", ""))   # the business's 3VL profile; the card falls back to the Instagram post
            specials.append(s)
    # Standing weekly deals (weekly_deals.json, e.g. a member's day-by-day flyer, owner 10/6/2026): today's deal joins the specials
    wpath = os.path.join(HERE, "weekly_deals.json")
    if os.path.exists(wpath):
        from zoneinfo import ZoneInfo
        now_et = dt.datetime.now(ZoneInfo("America/New_York"))
        for w in json.load(open(wpath, encoding="utf-8")):
            d = (w.get("days") or {}).get(str(now_et.weekday()))
            if not d or any(s.get("biz") == w["biz"] for s in specials):
                continue
            specials.append({"id": "wd-%s-%s" % (w["ig"], now_et.strftime("%Y%m%d")), "biz": w["biz"], "ig": w["ig"], "town": w.get("town", ""),
                             "category": w.get("category", ""), "member": w.get("member", False), "title": d["title"], "when": "Today, " + now_et.strftime("%A"),
                             "desc": d["desc"], "expires": now_et.strftime("%Y-%m-%d"), "img": d.get("img", ""), "inset": d.get("img", ""),
                             "url": "", "page": listing_for(w["biz"])})
    # Owner's ranked list for the Eat & Drink cards (names, top to bottom); /now orders its cards by this
    pref = json.load(open(os.path.join(HERE, "preference.json"), encoding="utf-8"))
    names = {x["ig"].lower(): x["name"] for x in json.load(open(os.path.join(HERE, "ig_accounts.json"), encoding="utf-8"))}
    eat_order = [names[h.lower()] for h in pref.get("order", []) if h.lower() in names]
    if not pref.get("live"):
        specials = []
    data = {"updated": dt.datetime.now(dt.timezone.utc).isoformat(), "counts": counts, "icons": ICON, "events": final, "closings": closings, "specials": specials, "eatOrder": eat_order, "eatCap": int(pref.get("cap", 9))}
    json.dump(data, open(os.path.join(HERE, "events.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(counts, len(final))


if __name__ == "__main__":
    main()
