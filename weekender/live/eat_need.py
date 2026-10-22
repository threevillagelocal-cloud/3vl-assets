"""Do the Eat & Drink landing pages need a refresh? Compares the specials in events.json with eat_pages.json.
Exit 0 (and print why) when a page is missing, a page's special has ended, or the homepage set changed; exit 1 otherwise.
    python weekender/live/eat_need.py"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    d = json.load(open(os.path.join(HERE, "events.json"), encoding="utf-8"))
    try:
        mp = json.load(open(os.path.join(HERE, "eat_pages.json"), encoding="utf-8"))
    except Exception:
        mp = {}
    cur = {s.get("id") for s in d.get("specials", []) + d.get("specialsAll", []) if s.get("id")}
    mapped = {k for k in mp if not k.startswith("_")}
    skip = set(mp.get("_skip", []))
    home = [s.get("id") for s in d.get("specials", [])]
    new, ended = cur - mapped - skip, mapped - cur
    why = []
    if new:
        why.append("%d new" % len(new))
    if ended:
        why.append("%d ended" % len(ended))
    if home != mp.get("_home"):
        why.append("homepage set changed")
    if why:
        print("eat pages: " + ", ".join(why))
        sys.exit(0)
    print("eat pages: up to date")
    sys.exit(1)


if __name__ == "__main__":
    main()
