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


def special_label(s):
    """Short tag for an Eat & Drink card (owner 10/21/2026: say if it's a special, music, etc.)."""
    t = " ".join([s.get("title") or "", s.get("desc") or ""]).lower()
    ti = (s.get("title") or "").lower()
    if re.search(r"karaoke|trivia|party|contest|workshop|class|tasting|bingo|comedy|paint", ti) and not re.search(r"happy hour|live music|jazz", ti):
        return "Event"
    if re.search(r"\blive music\b|\bjazz\b|\bacoustic\b|\bband\b|\bdj\b|\bperforming live\b|\blive performance\b|\bsinger\b", t):
        return "Live music"
    if re.search(r"happy hour", t):
        return "Happy hour"
    if re.search(r"karaoke|trivia|party|contest|workshop|class|tasting|bingo|comedy|paint", t):
        return "Event"
    return "Special"


def main():
    today = dt.date.today()
    horizon = today + dt.timedelta(days=10)
    out, counts, held = [], {}, []
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
            hit = re.search(r"country house|bench|home ?baked by julia|elaine'?s|home ?kingdom", e["title"] + " " + e["venue"], re.I)
            if hit and re.search(r"rotary", e["title"] + " " + (e.get("desc") or ""), re.I):
                hit = None   # owner 10/21/2026: always feature Three Village Rotary events, even at Elaine's
            if hit:   # never promote (owner requests: Country House; The Bench Bar & Grill 10/1/2026; Homebaked By Julia 10/5/2026; Elaine's; Home Kingdom 10/17/2026)
                # owner 10/16/2026: hold these for HIS approval instead of silently dropping them (he may let some through)
                held.append({"title": e["title"], "venue": e["venue"], "start": e["start"].isoformat(), "url": e["url"], "matched": hit.group(0)})
                continue
            if re.search(r"meeting|work session|advisory council|board of trustees|zoning board|planning board|delayed opening|library closed", e["title"], re.I):
                continue
            st = status_for(e["title"])
            title = re.sub(r"^\s*(cancel+ed|postponed)\s*[-:]\s*", "", e["title"], flags=re.I).strip()
            out.append({"id": re.sub(r"[^a-z0-9]+", "-", e["uid"].lower())[:80], "title": title, "start": e["start"].isoformat(),
                        "end": e["end"].isoformat(), "allday": e["allday"], "venue": e["venue"], "addr": e["addr"], "url": e["url"],
                        "desc": e["desc"][:260], "img": e["image"] or (LIB_FRONT if e["src"] == "emmaclark" else ""), "src": e["src"], "tags": tags_for(e), "status": st,
                        "fb": 0 if e["image"] or e["src"] != "emmaclark" else 1})   # fb=1: stand-in photo, never used for Top Things to Do
    # the NEWEST weekly edition (was hard-wired to 2026-10-02, so a new edition never reached the live feed: 10/11/2026)
    eds = sorted(x for x in os.listdir(os.path.dirname(HERE)) if re.fullmatch(r"\d{4}-\d{2}-\d{2}", x)
                 and os.path.exists(os.path.join(os.path.dirname(HERE), x, "weekend.json")))
    ed_name = eds[-1] if eds else "2026-10-02"
    ed = os.path.join(os.path.dirname(HERE), ed_name, "weekend.json")
    if os.path.exists(ed):
        W = json.load(open(ed, encoding="utf-8"))
        base = "https://cdn.jsdelivr.net/gh/threevillagelocal-cloud/3vl-assets@master/weekender/%s/" % ed_name
        for e in W["events"]:
            v = W["venues"].get(e["venue"], {})
            out.insert(0, {"id": "cur-" + e["id"], "title": e["title"], "start": e["start"], "end": e["end"], "allday": bool(e.get("allday")),
                           "venue": v.get("name", ""), "addr": v.get("addr", ""), "url": e.get("url", ""), "desc": e["desc"],
                           "img": (base + e["img"] + "-720.webp") if e.get("img") else "", "src": "3vl", "tags": e["tags"][:3],
                           "status": e.get("status", ""), "pick": e["id"] in W.get("picks", []), "page": e.get("page", ""),
                           "pu": e.get("pick_until", "")})   # pu: when the card leaves Top Things to Do (before the event ends)
        for a in W.get("allweekend", []):
            # ALL ongoing attractions go in the feed, not just the hand-picked ones: Stony Brook Village scarecrows were missing
            # from /this-weekend and the weekend post on 10/16/2026 because only picked allweekend items were added
            if True:
                v = W["venues"].get(a["venue"], {})
                until = a.get("until") or W.get("ends", "")
                if until and "T" not in until:
                    until += "T23:59"
                out.insert(0, {"id": "cur-" + a["id"], "title": a["title"], "start": dt.date.today().isoformat() + "T00:00", "end": until,
                               "allday": True, "ongoing": True, "whenText": a["when"], "venue": v.get("name", ""), "addr": v.get("addr", ""),
                               "url": a.get("url", ""), "desc": a["desc"], "img": (base + a["img"] + "-720.webp") if a.get("img") else "",
                               "src": "3vl", "tags": a["tags"][:3], "status": "", "pick": a["id"] in W.get("picks", []), "page": a.get("page", "")})
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
    specials, specials_all = [], []
    if os.path.exists(spath):
        igbase = "https://raw.githubusercontent.com/threevillagelocal-cloud/3vl-assets/master/weekender/live/"
        today = dt.date.today().isoformat()
        sj = json.load(open(spath, encoding="utf-8"))
        for lst, out in ((sj.get("specials", []), specials), (sj.get("all", []), specials_all)):
            for s in lst:
                if (s.get("expires") or "9999") < today:
                    continue
                if s.get("inset") and not s["inset"].startswith("http"):
                    s["inset"] = igbase + s["inset"]
                s["page"] = listing_for(s.get("biz", ""))   # the business's 3VL profile; the card falls back to the Instagram post
                if re.search(r"(?i)not specified|unspecified|unknown", s.get("when") or ""):
                    s["when"] = ""                           # e.g. "Recurring (time not specified)": no tag beats a robotic one
                out.append(s)
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
            if not any(s.get("biz") == w["biz"] for s in specials_all):
                specials_all.append(specials[-1])
    # Owner's ranked list for the Eat & Drink cards (names, top to bottom); /now orders its cards by this
    pref = json.load(open(os.path.join(HERE, "preference.json"), encoding="utf-8"))
    names = {x["ig"].lower(): x["name"] for x in json.load(open(os.path.join(HERE, "ig_accounts.json"), encoding="utf-8"))}
    eat_order = [names[h.lower()] for h in pref.get("order", []) if h.lower() in names]
    # "See all specials" page (owner 10/10/2026): every current special, owner's ranked order; homepage specials always included
    for s in specials:
        if not any(x.get("id") == s.get("id") for x in specials_all):
            specials_all.append(s)
    rk = {n.lower(): i for i, n in enumerate(eat_order)}
    specials_all.sort(key=lambda s: rk.get((s.get("biz") or "").lower(), 999))
    # ROTATE (owner 10/11/2026: "they have been in that spot for a long time. we need to ROTATE"): every day the list of
    # places with a current special starts a few places further down the owner's ranked order, so the homepage 6 and the
    # top of the See-all page change daily. Same order all day (Eastern date).
    # PINNED weekly highlights (owner 10/21/2026: Madiran live music as a weekly highlight): weekender/live/pinned.json,
    # each {ig, biz, town, title, when, desc, img, url, expires, label}; shown first on the homepage until it expires.
    try:
        pinned = [p for p in json.load(open(os.path.join(HERE, "pinned.json"), encoding="utf-8")) if p.get("starts", "0000") <= dt.date.today().isoformat() <= p.get("expires", "9999")]
    except Exception as ex:
        print("pinned.json:", ex)
        pinned = []
    for p in reversed(pinned):
        specials_all = [x for x in specials_all if (x.get("biz") or "").lower() != p["biz"].lower()]
        specials_all.insert(0, dict(p, pinned=True))
    first, places = {}, []
    for s in specials_all:
        k = (s.get("biz") or "").lower()
        if k not in first:
            first[k] = s; places.append(k)
    if places:
        from zoneinfo import ZoneInfo
        step = max(1, int(pref.get("rotate_step", 3)))
        off = ((dt.datetime.now(ZoneInfo("America/New_York")).date().toordinal() + 1) * step) % len(places)
        places = places[off:] + places[:off]
        pin_keys = [p["biz"].lower() for p in pinned]
        # "always" (preference.json, owner picks e.g. Namkeen 10/21/2026): these places go right after the pinned ones whenever they have a current special/deal
        names_by_ig = {x["ig"].lower(): x["name"].lower() for x in json.load(open(os.path.join(HERE, "ig_accounts.json"), encoding="utf-8"))}
        pin_keys += [names_by_ig[h.lower()] for h in pref.get("always", []) if h.lower() in names_by_ig and names_by_ig[h.lower()] not in pin_keys]
        places = [k for k in pin_keys if k in first] + [k for k in places if k not in pin_keys]
        nopromo = {names_by_ig[h.lower()] for h in pref.get("no_promo", []) if h.lower() in names_by_ig}   # owner: listing OK, no promo
        places = [k for k in places if k not in nopromo]
        # Port Jefferson STATION is never featured on the homepage unless the owner says so (owner 10/21/2026); only PJ village 11777.
        if not pref.get("allow_pjs"):
            places = [k for k in places if "port jefferson station" not in (first[k].get("town") or "").lower()]
        # TOWN MIX (owner 10/21/2026: "too much port jefferson... 2 or 3 max pj. try for 2"): homepage cards take at most
        # pj_max Port Jefferson / PJ Station places, then fill with Setauket / Stony Brook first; a 3rd PJ only if needed.
        cap_n, pj_max = int(pref.get("cap", 9)), int(pref.get("pj_max", 2))
        is_pj = lambda k: "port jeff" in (first[k].get("town") or "").lower()
        chosen = [k for k in places if not is_pj(k)]   # pinned places are first in places, so they are always kept
        pj = [k for k in places if is_pj(k)]
        need_pj = min(len(pj), 3, max(int(pref.get("pj_min", 1)), cap_n - len(chosen)))   # at least pj_min, more only if Setauket/Stony Brook run short (never over 3)
        pick_set = set(chosen[:cap_n - min(need_pj, len(pj))] + pj[:need_pj])
        places = [k for k in places if k in pick_set] + [k for k in places if k not in pick_set]
        pos = {k: i for i, k in enumerate(places)}
        specials = [dict(first[k]) for k in places][:cap_n]
        # Homepage cards (owner 10/21/2026): the big photo is the restaurant's edited EXTERIOR (weekender/ext), the post's own
        # image becomes the small inset; each card is labeled Live music / Happy hour / Event / Special.
        ext = json.load(open(os.path.join(HERE, "..", "ext", "ext.json"), encoding="utf-8")) if os.path.exists(os.path.join(HERE, "..", "ext", "ext.json")) else {}
        for s in specials:
            e = ext.get((s.get("ig") or "").lower())
            if e:
                own = s.get("img") or s.get("inset") or ""
                s["img"] = "https://raw.githubusercontent.com/threevillagelocal-cloud/3vl-assets/master/weekender/ext/" + e["file"]
                s["inset"] = own
            s["label"] = s.get("label") or special_label(s)
        specials_all.sort(key=lambda s: pos.get((s.get("biz") or "").lower(), 999))
        eat_order = [first[k]["biz"] for k in places] + [n for n in eat_order if n.lower() not in pos]
    if not pref.get("live"):
        specials, specials_all = [], []
    data = {"updated": dt.datetime.now(dt.timezone.utc).isoformat(), "counts": counts, "icons": ICON, "events": final, "closings": closings, "specials": specials,
            "specialsAll": specials_all, "eatOrder": eat_order, "eatCap": int(pref.get("cap", 9))}
    fpath = os.path.join(HERE, "ferry.json")   # Port Jefferson Ferry service alerts (ferry.py); the homepage strip only shows service alerts
    if os.path.exists(fpath):
        data["ferry"] = json.load(open(fpath, encoding="utf-8"))
    json.dump(data, open(os.path.join(HERE, "events.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    # events kept OFF the site because they match the never-promote list; the owner reviews these and may OK some (10/16/2026)
    seen, hl = set(), []
    for h in held:
        if (h["title"], h["start"][:10]) not in seen:
            seen.add((h["title"], h["start"][:10])); hl.append(h)
    json.dump({"updated": dt.datetime.now().isoformat(timespec="minutes"), "held": hl}, open(os.path.join(HERE, "held_for_owner.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(counts, len(final), "held for owner:", len(hl))


if __name__ == "__main__":
    main()
