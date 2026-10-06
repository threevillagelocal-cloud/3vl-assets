"""Instagram -> Three Village Now specials.

Every few hours (GitHub Actions): read the latest public posts of the local restaurants/bars and paid members in
ig_accounts.json (Instagram Business Discovery), ask Claude whether each NEW post is a special / deal / event
announcement, and write live/specials.json. Images are copied into live/ig/ (Instagram's own image links expire).

Env: IG_TOKEN (Meta system-user token), ANTHROPIC_API_KEY. Neither is ever printed.
Card layout on /now: the business's own photo is the big image, the Instagram post is the small inset.
"""
import base64, io, json, os, re, sys, time, urllib.request, urllib.parse, urllib.error
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
IGDIR = os.path.join(HERE, "ig")
STATE = os.path.join(HERE, "ig_seen_v2.json")      # post id -> classification (so each post is only judged once)
OUT = os.path.join(HERE, "specials.json")
ME, V = "17841472800565482", "v21.0"
MODEL = "claude-haiku-4-5-20251001"
LOOKBACK_DAYS = 7
IG_TOKEN = os.environ.get("IG_TOKEN", "").strip()
AKEY = os.environ.get("ANTHROPIC_API_KEY", "").strip()
NOW = datetime.now(timezone.utc)
TODAY = (NOW - timedelta(hours=4)).date()        # Eastern date


def ig(fields):
    url = "https://graph.facebook.com/%s/%s?%s" % (V, ME, urllib.parse.urlencode({"fields": fields, "access_token": IG_TOKEN}))
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        try:
            msg = json.load(e).get("error", {}).get("message", "")
        except Exception:
            msg = str(e)
        print("  IG error:", msg[:120])
        return None


def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30) as r:
        return r.read()


def save_img(url, name):
    """Download, shrink to 720px JPEG, keep in repo. Returns relative path or ''."""
    path = os.path.join(IGDIR, name + ".jpg")
    if os.path.exists(path):
        return "ig/" + name + ".jpg"
    try:
        from PIL import Image
        im = Image.open(io.BytesIO(fetch(url))).convert("RGB")
        im.thumbnail((720, 720))
        os.makedirs(IGDIR, exist_ok=True)
        im.save(path, "JPEG", quality=80, optimize=True, progressive=True)
        return "ig/" + name + ".jpg"
    except Exception as e:
        print("  image failed:", str(e)[:100])
        return ""


PROMPT = """You review Instagram posts from local businesses in Three Village, Long Island (Setauket, Stony Brook, Port Jefferson) for the "Eat & Drink / Local specials" section of a community page.
Business: {name} ({category}, {town}). Posted: {posted}. Today is {today}.
Caption:
<<<
{caption}
>>>
Say special=true ONLY if the post announces a SPECIFIC, TIME-BOUND offer or happening a resident can go to or use in the next 14 days:
- a food or drink special, happy hour, limited or seasonal menu item, tasting, prix fixe, themed night
- live music, trivia, a party, class or event at the business WITH a date or recurring day
- a sale or discount with a clear end or day
Say special=false for: ongoing services or "call us" ads, booking/catering/holiday-party promos with no event date, "coming soon"/TBA, merch, hiring, staff or customer shoutouts, generic food photos, closures/storm/hours notices, reposts, anything already over or more than 14 days away.
Reply with ONLY JSON:
{{"special": true/false, "title": "short headline, max 45 chars, no emojis", "when": "short label like 'Tue, Oct. 6 · 5-8 PM' or 'Every Friday'", "desc": "one friendly sentence, max 150 chars, facts from the caption only, no em dashes", "expires": "YYYY-MM-DD last day it applies"}}"""


def classify(acct, post):
    cap = (post.get("caption") or "").strip()
    if len(cap) < 15:
        return {"special": False}
    body = {"model": MODEL, "max_tokens": 300, "messages": [{"role": "user", "content": PROMPT.format(
        name=acct["name"], category=acct.get("category", ""), town=acct.get("town", ""), posted=post["timestamp"][:10],
        today=TODAY.isoformat(), caption=cap[:1800])}]}
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=json.dumps(body).encode(),
                                 headers={"x-api-key": AKEY, "anthropic-version": "2023-06-01", "content-type": "application/json"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                txt = json.load(r)["content"][0]["text"]
            m = re.search(r"\{.*\}", txt, re.S)
            return json.loads(m.group(0)) if m else {"special": False}
        except urllib.error.HTTPError as e:
            if e.code in (429, 529, 500) and attempt < 2:
                time.sleep(8); continue
            print("  AI error", e.code)
            return None
        except Exception as e:
            print("  AI parse error", str(e)[:80])
            return {"special": False}


def main():
    if not IG_TOKEN or not AKEY:
        sys.exit("IG_TOKEN and ANTHROPIC_API_KEY are both required")
    accts = json.load(open(os.path.join(HERE, "ig_accounts.json"), encoding="utf-8"))
    photos = json.load(open(os.path.join(HERE, "biz_photos.json"), encoding="utf-8")) if os.path.exists(os.path.join(HERE, "biz_photos.json")) else {}
    seen = json.load(open(STATE, encoding="utf-8")) if os.path.exists(STATE) else {}
    pref = json.load(open(os.path.join(HERE, "preference.json"), encoding="utf-8"))
    rank = {h.lower(): i for i, h in enumerate(pref.get("order", []))}
    accts = [a for a in accts if a["ig"].lower() in rank]      # only check places on the owner's list
    accts = [a for a in accts if not a.get("noscan")]          # e.g. chain brand accounts: their deals come from weekly_deals.json
    cache_path = os.path.join(HERE, "specials_cache.json")      # last good specials per business, used if Instagram says no
    cache = json.load(open(cache_path, encoding="utf-8")) if os.path.exists(cache_path) else {}
    since = NOW - timedelta(days=LOOKBACK_DAYS)
    specials, judged, missed = [], 0, 0
    for a in accts:
        h = a["ig"]
        d = ig("business_discovery.username(%s){username,name,profile_picture_url,media.limit(6){id,timestamp,media_type,media_url,thumbnail_url,permalink,caption}}" % h)
        time.sleep(0.4)
        if not d:
            missed += 1
            specials += cache.get(h, [])
            continue
        n0 = len(specials)
        bd = d["business_discovery"]
        for p in (bd.get("media") or {}).get("data", []):
            ts = datetime.strptime(p["timestamp"], "%Y-%m-%dT%H:%M:%S%z")
            if ts < since:
                continue
            c = seen.get(p["id"])
            if c is None:
                c = classify(a, p)
                if c is None:          # API trouble: try again next run
                    continue
                c["_ts"] = p["timestamp"]
                seen[p["id"]] = c
                judged += 1
            if not c.get("special"):
                continue
            try:
                if datetime.strptime(c.get("expires") or "", "%Y-%m-%d").date() < TODAY:
                    continue
            except ValueError:
                if (NOW - ts).days > 7:
                    continue
            inset = save_img(p.get("thumbnail_url") or p.get("media_url") or "", "p" + p["id"])
            main_img = photos.get(h, "")
            specials.append({"id": p["id"], "biz": a["name"], "ig": h, "town": a.get("town", ""), "category": a.get("category", ""),
                             "member": a.get("group") == "member", "title": c.get("title", ""), "when": c.get("when", ""),
                             "desc": c.get("desc", ""), "expires": c.get("expires", ""), "posted": p["timestamp"],
                             "url": p["permalink"], "img": main_img, "inset": inset})
        cache[h] = specials[n0:]
    # Owner's preference list: walk it top to bottom, first special per business, stop at the cap.
    specials = [s for s in specials if not s.get("expires") or s["expires"] >= TODAY.isoformat()]
    specials.sort(key=lambda s: -datetime.strptime(s["posted"], "%Y-%m-%dT%H:%M:%S%z").timestamp())
    best = {}
    for s in specials:                      # newest special per business
        if s["ig"].lower() in rank and s["ig"] not in best:
            best[s["ig"]] = s
    final = sorted(best.values(), key=lambda s: rank[s["ig"].lower()])[:int(pref.get("cap", 9))]
    candidates = final
    if not pref.get("live"):
        final = []
    # forget posts older than 30 days
    cutoff = (NOW - timedelta(days=30)).isoformat()
    seen = {k: v for k, v in seen.items() if v.get("_ts", "9") >= cutoff}
    json.dump(cache, open(cache_path, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    json.dump(seen, open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    json.dump({"updated": NOW.isoformat(), "specials": final, "candidates": candidates}, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Instagram unavailable for %d accounts (used last known)" % missed)
    print("judged %d new posts, %d live specials (live=%s)" % (judged, len(final), pref.get("live")))
    for s in candidates:
        print(" -", s["biz"], "|", s["title"], "|", s["when"])


if __name__ == "__main__":
    main()
