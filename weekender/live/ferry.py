"""Port Jefferson Ferry service alerts (88844ferry.com) for the homepage strip (same idea as the storm closings strip).
Reads the site's own alert data (the "Alerts" list in the page) and the schedule page's cancelled-trip markers.
Writes ferry.json next to this file; build_events.py copies it into events.json as "ferry"; weekender.js shows the strip
only when there is a SERVICE alert (cancellations, delays, weather, schedule changes). Promos (events, festivals) are ignored.
    python weekender/live/ferry.py"""
import datetime as dt, json, os, re, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://www.88844ferry.com"
BS = chr(92)
SERVICE = re.compile(r"cancel|suspend|delay|weather|wind|storm|fog|modified|reduced|limited|no service|not (?:running|operating)|"
                     r"schedule change|holiday schedule|resum|closed|disrupt|mechanical|out of service|advisory|service (?:alert|update|change)", re.I)
CANCEL_ICON = "5.5 14 2 10.5v-5L5.5 2h5L14 5.5v5L10.5 14h-5Z"   # octagon drawn next to a cancelled departure (also used once per legend)


def get(path):
    req = urllib.request.Request(SITE + path, headers={"User-Agent": "Mozilla/5.0 (3VL ferry alerts; threevillagelocal.com)"})
    return urllib.request.urlopen(req, timeout=40).read().decode("utf-8", "replace")


def alerts_in(html):
    key = "Alerts" + BS + '":['
    i = html.find(key)
    if i < 0:
        return []
    start = i + len(key) - 1
    depth = 0
    for k in range(start, len(html)):
        if html[k] == "[":
            depth += 1
        elif html[k] == "]":
            depth -= 1
            if depth == 0:
                break
    try:
        return json.loads(html[start:k + 1].encode().decode("unicode_escape"))
    except Exception as ex:
        print("could not read alerts:", ex)
        return []


def text_of(v):
    """Rich-text bodies come as nested JSON; collect the plain words."""
    if isinstance(v, str):
        return v
    if isinstance(v, dict):
        return " ".join(text_of(x) for k, x in v.items() if k in ("value", "content", "text", "children", "json", "body"))
    if isinstance(v, list):
        return " ".join(text_of(x) for x in v)
    return ""


def main():
    out = {"checked": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "alerts": [], "cancellations": False,
           "url": SITE + "/schedule"}
    try:
        home = get("/")
        sched = get("/schedule")
    except Exception as ex:
        print("ferry site unreachable:", ex)
        if os.path.exists(os.path.join(HERE, "ferry.json")):
            return   # keep the last known state rather than clearing a live alert on a network blip
        sched = home = ""
    for a in alerts_in(home) + alerts_in(sched):
        title = (a.get("title") or "").strip()
        body = re.sub(r"\s+", " ", text_of(a.get("body") or a.get("content") or a.get("description") or "")).strip()
        if not title or not SERVICE.search(title + " " + body):
            continue   # festival/event promos are not service alerts
        if any(x["title"] == title for x in out["alerts"]):
            continue
        link = (a.get("primaryLinkUrl") or "").strip() or SITE + "/schedule"
        if link.startswith("/"):
            link = SITE + link   # the ferry site gives relative links ("/info/elevator-alert"); on our page they 404'd (10/16/2026)
        out["alerts"].append({"title": title, "text": body[:240], "link": link,
                              "published": a.get("publishedAt", "")})
    # The same octagon icon marks both "Cancelled" and "Rescheduled" departures (10/21/2026: 18 rescheduled trips
    # showed as "Cancelled" on our homepage). Read the label right after each icon; the legend ("= Cancelled") is skipped.
    cancelled = rescheduled = 0
    for m in re.finditer(re.escape(CANCEL_ICON), sched):
        after = sched[m.end():m.end() + 300]
        if "= Cancelled" in after:
            continue
        r, c = after.find("Rescheduled"), after.find("Cancel")
        if r != -1 and (c == -1 or r < c):
            rescheduled += 1
        elif c != -1:
            cancelled += 1
    out["cancellations"] = cancelled > 0
    out["rescheduled"] = rescheduled > 0
    json.dump(out, open(os.path.join(HERE, "ferry.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("ferry: %d service alert(s), cancellations=%s" % (len(out["alerts"]), out["cancellations"]))


if __name__ == "__main__":
    main()
