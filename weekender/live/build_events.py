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


def tags_for(e):
    blob = (e["title"] + " " + e["desc"]).lower()
    t = [k for k, rx in TAGS if re.search(rx, blob)]
    if re.search(r"\bfree\b", blob) or e["src"] == "emmaclark":
        t.insert(0, "free")
    return t[:3] or ["arts"]


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
            if not (today <= e["start"].date() <= horizon):
                continue
            if re.search(r"country house", e["title"] + " " + e["venue"], re.I):   # never promote (owner request)
                continue
            if re.search(r"meeting|work session|advisory council|board of trustees|zoning board|planning board|delayed opening|library closed", e["title"], re.I):
                continue
            st = status_for(e["title"])
            title = re.sub(r"^\s*(cancel+ed|postponed)\s*[-:]\s*", "", e["title"], flags=re.I).strip()
            out.append({"id": re.sub(r"[^a-z0-9]+", "-", e["uid"].lower())[:80], "title": title, "start": e["start"].isoformat(),
                        "end": e["end"].isoformat(), "allday": e["allday"], "venue": e["venue"], "addr": e["addr"], "url": e["url"],
                        "desc": e["desc"][:260], "img": e["image"], "src": e["src"], "tags": tags_for(e), "status": st})
    ed = os.path.join(os.path.dirname(HERE), "2026-10-02", "weekend.json")
    if os.path.exists(ed):
        W = json.load(open(ed, encoding="utf-8"))
        base = "https://cdn.jsdelivr.net/gh/threevillagelocal-cloud/3vl-assets@master/weekender/2026-10-02/"
        for e in W["events"]:
            v = W["venues"].get(e["venue"], {})
            out.insert(0, {"id": "cur-" + e["id"], "title": e["title"], "start": e["start"], "end": e["end"], "allday": False,
                           "venue": v.get("name", ""), "addr": v.get("addr", ""), "url": e.get("url", ""), "desc": e["desc"],
                           "img": (base + e["img"] + "-720.webp") if e.get("img") else "", "src": "3vl", "tags": e["tags"][:3],
                           "status": e.get("status", ""), "pick": e["id"] in W.get("picks", [])})
    # de-dupe same title + same day
    seen, final = set(), []
    for e in sorted(out, key=lambda x: x["start"]):
        k = (re.sub(r"[^a-z0-9]", "", e["title"].lower()), e["start"][:10])
        if k in seen:
            continue
        seen.add(k)
        final.append(e)
    closings = json.load(open(os.path.join(HERE, "closings.json"), encoding="utf-8")) if os.path.exists(os.path.join(HERE, "closings.json")) else []
    data = {"updated": dt.datetime.now(dt.timezone.utc).isoformat(), "counts": counts, "icons": ICON, "events": final, "closings": closings}
    json.dump(data, open(os.path.join(HERE, "events.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(counts, len(final))


if __name__ == "__main__":
    main()
