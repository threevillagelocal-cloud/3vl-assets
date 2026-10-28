"""Events from local businesses' own Instagram posts (owner 10/13 + 10/28/2026: comb members' and local businesses' social media).

Runs once a day inside ig-specials.yml (no new schedule; `--check` exits 1 when the last scan was under 20 hours ago).
Read-only: Instagram Business Discovery with our own token (public posts of business accounts). It never logs in to anyone's
account, never sends messages and never posts.

Accounts: ig_accounts.json + members' Instagram links (SOCIAL_MEMBERS = path to the site guard's member list, read at run time)
+ posts that tag @threevillagelocal. A rotating batch is read each day so the Instagram rate limit stays far away from the
specials sync. Captions that look like an event are judged once by Claude Haiku (cached by post id).

Writes social_events.json:
  confirmed  the business's OWN post states the date, a start time and the place, and it is a community event (not a food or
             drink special, those belong to Eat & Drink) -> sources.social() puts it in the live feed and the /events calendar
  review     every other event-looking post, with the reason it was not added -> the owner's review email (site guard)
social_hide.json (list of post ids) keeps a post out of both lists; social_ok.json (post ids the owner approved) moves a
review item to confirmed when it has a date and start time.
Env: IG_TOKEN, ANTHROPIC_API_KEY, SOCIAL_MEMBERS (optional), SOCIAL_SKIP (optional {"ids": [], "names": []})."""
import datetime as dt, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "social_events.json")
STATE = os.path.join(HERE, "social_seen.json")
HIDE = os.path.join(HERE, "social_hide.json")
OK = os.path.join(HERE, "social_ok.json")         # post ids the owner approved from the review email
ME, V = "17841472800565482", "v21.0"
MODEL = "claude-haiku-4-5-20251001"
BATCH = int(os.environ.get("SOCIAL_BATCH", "70"))      # accounts read per day
LOOKBACK = 21                                          # days of posts
AHEAD = 45                                             # events this far out at most
NOW = dt.datetime.now(dt.timezone.utc)
TODAY = (NOW - dt.timedelta(hours=4 if 3 < NOW.month < 11 else 5)).date()
RAWBASE = "https://raw.githubusercontent.com/threevillagelocal-cloud/3vl-assets/master/weekender/live/"

MONTHS = "january february march april may june july august september october november december".split()
DATEW = re.compile(r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.?\s+\d{1,2}\b|\b\d{1,2}/\d{1,2}\b|"
                   r"\b(?:mon|tues?|wed(?:nes)?|thu(?:rs)?|fri|sat(?:ur)?|sun)(?:day)?\b|\btonight\b|\btomorrow\b", re.I)
EVENTW = re.compile(r"\bevent|join us|come (?:out|by|down|join)|workshop|\bclass\b|festival|\bfair\b|market|open house|celebrat|"
                    r"fundraiser|benefit|tournament|trivia|paint|party|story ?time|\btour\b|\bshow\b|concert|grand opening|"
                    r"ribbon cutting|vendor|trunk|halloween|holiday|santa|tree lighting|craft|kids|family|registration|"
                    r"tickets?|rsvp|sign up|seminar|meet ?(?:and|&) ?greet|book signing|live music|performance|5k|walk\b", re.I)

PROMPT = """You read Instagram posts from local businesses and organizations in Three Village, Long Island, NY (Setauket, East Setauket, Stony Brook, Port Jefferson, Port Jefferson Station) for a community events calendar.
Account: {name} (@{handle}){cat}. Posted: {posted}. Today is {today}.
Caption:
<<<
{caption}
>>>
Decide if the post announces ONE specific upcoming event that the public can attend. Use ONLY facts written in the caption; never guess.
kind:
- "community": festival, fair, market, fundraiser, class, workshop, kids or family event, open house, grand opening, tour, show, talk, book signing, sports or charity event
- "food_drink": anything that is a food or drink offer or a night out at a bar, restaurant, cafe or brewery (specials, tastings, happy hour, dinners, live music, trivia, karaoke at a bar or restaurant)
- "sale": a store sale or discount
- "other": not an event (ads, services, hiring, photos of past events, holiday greetings, "coming soon", no date)
Reply with ONLY JSON:
{{"event": true/false, "kind": "community|food_drink|sale|other", "title": "short event name, max 60 chars, no emojis",
 "date": "YYYY-MM-DD or empty", "start": "HH:MM 24h or empty", "end": "HH:MM or empty",
 "place": "venue name and/or address exactly as written, or empty", "at_business": true if it is held at the account's own location,
 "date_stated": true if the caption itself gives the day (a date, or a weekday plus enough context), "time_stated": true if a start time is written,
 "desc": "one or two plain sentences from the caption, max 220 chars, no emojis, no em dashes"}}"""


def igget(fields):
    url = "https://graph.facebook.com/%s/%s?%s" % (V, ME, urllib.parse.urlencode({"fields": fields, "access_token": os.environ.get("IG_TOKEN", "").strip()}))
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        try:
            return {"ERROR": json.load(e).get("error", {}).get("message", "")[:120]}
        except Exception:
            return {"ERROR": str(e)}
    except Exception as e:
        return {"ERROR": str(e)[:120]}


def classify(acct, post):
    body = {"model": MODEL, "max_tokens": 400, "messages": [{"role": "user", "content": PROMPT.format(
        name=acct["name"], handle=acct["ig"], cat=(", " + acct["cat"]) if acct.get("cat") else "", posted=post["timestamp"][:10],
        today=TODAY.isoformat(), caption=(post.get("caption") or "")[:1800])}]}
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=json.dumps(body).encode(),
                                 headers={"x-api-key": os.environ.get("ANTHROPIC_API_KEY", "").strip(), "anthropic-version": "2023-06-01",
                                          "content-type": "application/json"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                txt = json.load(r)["content"][0]["text"]
            m = re.search(r"\{.*\}", txt, re.S)
            return json.loads(m.group(0)) if m else {"event": False}
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 529) and attempt < 2:
                time.sleep(8)
                continue
            return None
        except Exception:
            return {"event": False}


def handle_of(u):
    m = re.search(r"instagram\.com/([A-Za-z0-9._]{2,30})", u or "")
    h = m.group(1).rstrip(".") if m else ""
    return "" if h.lower() in ("p", "reel", "stories", "explore", "accounts") else h


def accounts():
    """[{name, ig, town, cat, food, addr, page}] from ig_accounts.json + members' links; blocked businesses removed."""
    idx = {}
    try:
        for m in json.load(open(os.path.join(os.path.dirname(os.path.dirname(HERE)), "search", "index.json"), encoding="utf-8"))["members"]:
            idx[int(m["id"])] = m
    except Exception:
        pass
    skip = {"ids": [], "names": []}
    if os.environ.get("SOCIAL_SKIP") and os.path.exists(os.environ["SOCIAL_SKIP"]):
        skip.update(json.load(open(os.environ["SOCIAL_SKIP"], encoding="utf-8")))
    skip_ids = {int(x) for x in skip.get("ids", [])}
    skip_rx = re.compile("|".join(re.escape(n) for n in skip.get("names", [])) or r"(?!x)x", re.I)
    out = []
    for a in json.load(open(os.path.join(HERE, "ig_accounts.json"), encoding="utf-8")):
        out.append({"name": a["name"], "ig": a["ig"], "town": a.get("town", ""), "cat": a.get("category", ""),
                    "food": a.get("group") == "food", "addr": "", "page": ""})
    p = os.environ.get("SOCIAL_MEMBERS")
    if p and os.path.exists(p):
        for m in json.load(open(p, encoding="utf-8")):
            h = handle_of(m.get("ig"))
            if not h or int(m["id"]) in skip_ids:
                continue
            x = idx.get(int(m["id"]), {})
            cat = x.get("c", "")
            addr = ", ".join(v for v in (x.get("a"), x.get("t") or m.get("city"), ("NY " + x["z"]) if x.get("z") else "NY") if v) if x.get("a") else ""
            out.append({"name": m.get("name") or h, "ig": h, "town": x.get("t") or m.get("city", ""), "cat": cat,
                        "food": bool(re.search(r"restaurant|food|bar\b|cafe|bakery|brew|wine|deli|pizza", cat, re.I)),
                        "addr": addr, "page": x.get("u", ""), "member": True})
    keep, by = [], {}
    for a in out:
        k = a["ig"].lower()
        if skip_rx.search(a["name"]) or skip_rx.search(a["ig"]):
            continue
        if k in by:   # same account from ig_accounts.json and the member list: keep the member's address and 3VL page
            for f in ("addr", "page", "member"):
                by[k][f] = by[k].get(f) or a.get(f)
            continue
        by[k] = a
        keep.append(a)
    return keep


def stated_in(cap, d, start):
    """The date and the start time must really be in the caption (guards against a model guess)."""
    c = cap.lower()
    day = d.day
    date_ok = bool(re.search(r"\b(?:%s)[a-z]*\.?\s+%d(?:st|nd|rd|th)?\b" % (MONTHS[d.month - 1][:3], day), c)) or \
        bool(re.search(r"\b%d/%d\b" % (d.month, day), c)) or \
        bool(re.search(r"\b%d(?:st|nd|rd|th)\b" % day, c) and re.search(MONTHS[d.month - 1][:3], c))
    if not date_ok and (d - TODAY).days <= 7:   # "this Saturday" style, only for the coming week
        date_ok = bool(re.search(r"\b%s" % d.strftime("%a").lower()[:3], c))
    h = int(start[:2])
    h12 = h % 12 or 12
    time_ok = bool(re.search(r"\b%d(?::%s)?\s*(?:-\s*\d{1,2}(?::\d{2})?\s*)?(?:a\.?m|p\.?m)" % (h12, start[3:5]), c)) or \
        (start == "12:00" and "noon" in c)
    return date_ok, time_ok


def main():
    if "--check" in sys.argv:
        try:
            last = json.load(open(STATE, encoding="utf-8")).get("last_run", "")
        except Exception:
            last = ""
        due = not last or (NOW - dt.datetime.fromisoformat(last)).total_seconds() > 20 * 3600
        print("social scan due" if due else "social scan ran at %s, not due" % last)
        sys.exit(0 if due else 1)
    if not os.environ.get("IG_TOKEN") or not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("IG_TOKEN and ANTHROPIC_API_KEY are both required")
    if not os.path.exists(os.environ.get("SOCIAL_SKIP") or "-"):
        sys.exit("SOCIAL_SKIP list missing: not scanning without it")
    import ig_specials as IGS   # same image copier as the specials (Instagram's own image links expire)
    st = json.load(open(STATE, encoding="utf-8")) if os.path.exists(STATE) else {}
    seen = st.get("posts", {})
    try:
        hide = set(json.load(open(HIDE, encoding="utf-8")))
    except Exception:
        hide = set()
    try:
        okd = set(json.load(open(OK, encoding="utf-8")))
    except Exception:
        okd = set()
    accts = accounts()
    cur = int(st.get("cursor", 0)) % max(1, len(accts))
    batch = (accts[cur:] + accts[:cur])[:BATCH]
    since = NOW - dt.timedelta(days=LOOKBACK)
    fields = "id,timestamp,media_type,media_url,thumbnail_url,permalink,caption"
    posts, errs, judged = [], 0, 0
    for a in batch:
        d = igget("business_discovery.username(%s){media.limit(8){%s}}" % (a["ig"], fields))
        time.sleep(0.5)
        if "ERROR" in d:
            errs += 1
            continue
        for p in ((d.get("business_discovery") or {}).get("media") or {}).get("data", []):
            posts.append((a, p, False))
    t = igget("tags.limit(25){username,%s}" % fields)   # posts that tag @threevillagelocal (another account's post: review only)
    for p in (t.get("tags") or {}).get("data", []) if "ERROR" not in t else []:
        posts.append(({"name": p.get("username", "tagged"), "ig": p.get("username", ""), "town": "", "cat": "", "food": False,
                       "addr": "", "page": ""}, p, True))
    for a, p, tagged in posts:
        try:
            ts = dt.datetime.strptime(p["timestamp"], "%Y-%m-%dT%H:%M:%S%z")
        except Exception:
            continue
        cap = p.get("caption") or ""
        if ts < since or p["id"] in seen or len(cap) < 40 or not (DATEW.search(cap) and EVENTW.search(cap)):
            continue
        c = classify(a, p)
        if c is None:
            continue   # API trouble: try again next day
        judged += 1
        rec = {"ts": p["timestamp"], "c": c}
        if c.get("event"):
            rec.update({"acct": a, "tagged": tagged, "link": p.get("permalink", ""), "caption": cap[:600],
                        "img": IGS.save_img(p.get("thumbnail_url") or p.get("media_url") or "", "p" + p["id"])})
        seen[p["id"]] = rec
    # build the two lists from everything still current (old posts age out of the state after 45 days)
    confirmed, review = [], []
    for pid, r in sorted(seen.items(), key=lambda kv: kv[1]["ts"], reverse=True):
        c, a = r.get("c") or {}, r.get("acct")
        if not c.get("event") or not a or pid in hide:
            continue
        try:
            d = dt.date.fromisoformat(c.get("date") or "")
        except ValueError:
            d = None
        if d and d < TODAY:
            continue
        start = c.get("start") or ""
        if not re.fullmatch(r"\d{2}:\d{2}", start):
            start = ""
        reasons = []
        if r.get("tagged"):
            reasons.append("posted by another account that tagged us")
        if c.get("kind") != "community":
            reasons.append({"food_drink": "food/drink item (Eat & Drink, not the calendar)", "sale": "a sale, not an event"}.get(c.get("kind"), "may not be an event"))
        if a.get("food") and c.get("kind") == "community":
            reasons.append("restaurant/bar account: check it is not a dining promo")
        if not d:
            reasons.append("no clear date")
        elif (d - TODAY).days > AHEAD:
            reasons.append("more than %d days away" % AHEAD)
        if not start:
            reasons.append("no start time in the post")
        place = (c.get("place") or "").strip()
        venue, addr = place, ""
        if c.get("at_business") or not place or place.lower() in a["name"].lower():
            venue, addr = a["name"], a.get("addr", "")
        if not place and not (c.get("at_business") and a.get("addr")):
            reasons.append("no place in the post")
        if d and start:
            dok, tok = stated_in(r.get("caption", ""), d, start)
            if not dok:
                reasons.append("date not written plainly in the caption")
            if not tok:
                reasons.append("start time not written plainly in the caption")
        item = {"post": pid, "title": (c.get("title") or "").strip()[:80], "date": d.isoformat() if d else "", "start": start,
                "end": c.get("end") if re.fullmatch(r"\d{2}:\d{2}", c.get("end") or "") else "", "venue": venue, "addr": addr,
                "desc": (c.get("desc") or "").replace("\u2014", "-").replace("\u2013", "-")[:300], "org": a["name"], "handle": a["ig"],
                "org_url": a.get("page") or ("https://www.instagram.com/%s/" % a["ig"]), "url": r.get("link", ""),
                "img": (RAWBASE + r["img"]) if r.get("img") else "", "posted": r["ts"][:10], "kind": c.get("kind", ""),
                "member": bool(a.get("member"))}
        if pid in okd and d and start and item["title"]:
            reasons = []   # the owner said yes
        if reasons or not item["title"]:
            item["why"] = "; ".join(reasons) or "no title"
            review.append(item)
        else:
            confirmed.append(item)
    cutoff = (NOW - dt.timedelta(days=45)).isoformat()
    st = {"last_run": NOW.isoformat(), "cursor": (cur + len(batch)) % max(1, len(accts)), "accounts": len(accts),
          "posts": {k: v for k, v in seen.items() if v["ts"] >= cutoff}}
    json.dump(st, open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    json.dump({"updated": NOW.isoformat(timespec="minutes"), "confirmed": confirmed, "review": review},
              open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("social scan: %d of %d accounts read (%d unavailable), %d posts judged, %d confirmed events, %d for review"
          % (len(batch), len(accts), errs, judged, len(confirmed), len(review)))


if __name__ == "__main__":
    main()
