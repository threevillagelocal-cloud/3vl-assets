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
STATE = os.path.join(HERE, "ig_seen.json")      # post id -> classification (so each post is only judged once)
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


PROMPT = """You review Instagram posts from local businesses in Three Village, Long Island (Setauket, Stony Brook, Port Jefferson) for a community "what's happening" page.
Business: {name} ({category}, {town}). Posted: {posted}. Today is {today}.
Caption:
<<<
{caption}
>>>
Decide if this post announces something a local resident could act on SOON: a food/drink special, happy hour, deal, discount, limited menu, tasting, live music, event, class, sale, or new offering.
NOT a special: generic food photos with no offer, staff shoutouts, hiring posts, memes, holiday greetings, reviews, closed/hours-only notices, anything already over.
Reply with ONLY JSON:
{{"special": true/false, "title": "short headline, max 45 chars, no emojis", "when": "short time label like 'Tue, Oct. 6 · 5-8 PM' or 'Every Friday' or 'This week'", "desc": "one friendly sentence, max 150 chars, facts from the caption only, no prices you are unsure of, no em dashes", "expires": "YYYY-MM-DD last day it applies (best guess; recurring weekly = 7 days from today)"}}"""


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
    since = NOW - timedelta(days=LOOKBACK_DAYS)
    specials, judged = [], 0
    for a in accts:
        h = a["ig"]
        d = ig("business_discovery.username(%s){username,name,profile_picture_url,media.limit(6){id,timestamp,media_type,media_url,thumbnail_url,permalink,caption}}" % h)
        time.sleep(0.4)
        if not d:
            continue
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
    # newest first, max 2 per business
    specials.sort(key=lambda s: s["posted"], reverse=True)
    per, final = {}, []
    for s in specials:
        per[s["ig"]] = per.get(s["ig"], 0) + 1
        if per[s["ig"]] <= 2:
            final.append(s)
    # forget posts older than 30 days
    cutoff = (NOW - timedelta(days=30)).isoformat()
    seen = {k: v for k, v in seen.items() if v.get("_ts", "9") >= cutoff}
    json.dump(seen, open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    json.dump({"updated": NOW.isoformat(), "specials": final}, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("judged %d new posts, %d live specials" % (judged, len(final)))
    for s in final:
        print(" -", s["biz"], "|", s["title"], "|", s["when"])


if __name__ == "__main__":
    main()
