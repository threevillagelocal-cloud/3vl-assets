"""Nightly rebuild of the Three Village Local homepage (/now page body, BD widget 17). Owner-approved 9/28/2026.
Runs from 3vl-site-guard's nightly workflow (it checks this repo out next to itself).

  python weekender/nightly.py <sha> <out_file>

- Uses the newest weekly edition (weekender/YYYY-MM-DD/weekend.json) for the hand-picked parts.
- Drops Top Things to Do events that are over and "Coming up" items whose date has passed.
- The Event schema comes from the hourly live feed (next 2 weeks), so Google/AI always see current events.
- Featured Local Businesses and Latest Local Stories are re-fetched on every run.
- Writes <out_file> only if the page changed, and prints CHANGED or UNCHANGED."""
import datetime, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B          # noqa: E402
import nowhome_build as nhb  # noqa: E402

MON = {m: i + 1 for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"])}


def latest_edition():
    eds = sorted(x for x in os.listdir(HERE) if re.fullmatch(r"\d{4}-\d{2}-\d{2}", x) and os.path.exists(os.path.join(HERE, x, "weekend.json")))
    return eds[-1]


def last_day(when, year):
    """'Sat, Oct. 10' / 'Oct. 10-11' / 'Oct. 15-17' / 'Oct. 30 - Nov. 2' -> the last date mentioned."""
    last = None; month = None
    for m in re.finditer(r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s*(\d{1,2})(?:\s*-\s*(\d{1,2})(?!\d))?", when, re.I):
        month = MON[m.group(1).lower()[:3]]
        day = int(m.group(3) or m.group(2))
        try:
            last = datetime.date(year, month, day)
        except ValueError:
            pass
    return last


def fix_year(dt, ref):
    """An edition in late fall can mention January dates: those belong to the next year."""
    return dt.replace(year=dt.year + 1) if dt and (ref - dt).days > 180 else dt


def adjust(d, now):
    ev = {e["id"]: e for e in d["events"] + d["allweekend"] if "start" in e}

    def over(e):
        end = e.get("until") or e.get("end") or e.get("start")
        end = end if "T" in end else end + "T23:59"
        return datetime.datetime.fromisoformat(end[:16]) < now
    before = len(d["picks"])
    d["picks"] = [p for p in d["picks"] if p in ev and not over(ev[p])]
    y = int(d.get("starts", str(now.year))[:4])
    keep = []
    for n in d.get("next", []):
        ld = fix_year(last_day(n.get("when", ""), y), datetime.date.fromisoformat(d["starts"][:10]))
        if ld is None or ld >= now.date():
            keep.append(n)
    dropped = before - len(d["picks"]), len(d.get("next", [])) - len(keep)
    d["next"] = keep
    return dropped


def main():
    sha, out = sys.argv[1], sys.argv[2]
    ed = latest_edition()
    d = json.load(open(os.path.join(HERE, ed, "weekend.json"), encoding="utf-8"))
    now = nhb.now_et()
    dp, dn = adjust(d, now)
    body = B.build(ed, False, sha, d=d)
    old = open(out, encoding="utf-8").read() if os.path.exists(out) else ""
    ends = datetime.datetime.fromisoformat(d["ends"][:16])
    print("edition %s | picks kept %d (dropped %d) | coming-up kept %d (dropped %d) | edition %s" % (
        ed, len(d["picks"]), dp, len(d.get("next", [])), dn, "CURRENT" if ends >= now else "PAST - add a new weekly edition for fresh hand-picked items"))
    if "\\" in body:
        print("ABORT: backslash in body (BD would strip it)"); sys.exit(1)
    if body == old:
        print("UNCHANGED"); return
    open(out, "w", encoding="utf-8").write(body)
    print("CHANGED", len(body), "chars")


if __name__ == "__main__":
    main()
