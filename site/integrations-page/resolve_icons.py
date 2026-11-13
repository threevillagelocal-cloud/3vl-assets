"""Find a Simple Icons logo for each product in integrations_data.py and confirm every logo URL answers 200.
Writes icons.json {name: slug}. Products without a logo get a letter tile on the page.
    python site/integrations-page/resolve_icons.py"""
import json, os, re, sys, unicodedata, urllib.request
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from integrations_data import ITEMS

VER = "16.35.0"   # pinned exact version (released 2026-10-11)
CDN = "https://cdn.jsdelivr.net/npm/simple-icons@%s/icons/" % VER
UA = {"User-Agent": "Mozilla/5.0 3VL"}


def slugify(t):
    t = t.lower().replace("+", "plus").replace(".", "dot").replace("&", "and")
    t = "".join(c for c in unicodedata.normalize("NFD", t) if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", t)


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()


data = json.loads(get("https://cdn.jsdelivr.net/npm/simple-icons@%s/data/simple-icons.json" % VER))
by_title = {}
slugs = set()
for x in data:
    s = x.get("slug") or slugify(x["title"])
    slugs.add(s)
    by_title[x["title"].lower()] = s

want = {}
for it in ITEMS:
    name = it[0]
    s = it[4] if len(it) > 4 else by_title.get(name.lower())
    if s and s in slugs:
        want[name] = s
    elif s:
        print("no such slug:", name, s)


def ok(s):
    try:
        r = urllib.request.urlopen(urllib.request.Request(CDN + s + ".svg", headers=UA), timeout=60)
        body = r.read(400)
        return s, r.status == 200 and b"<svg" in body
    except Exception:
        return s, False


with ThreadPoolExecutor(12) as ex:
    res = dict(ex.map(ok, sorted(set(want.values()))))
bad = [s for s, v in res.items() if not v]
out = {n: s for n, s in want.items() if res.get(s)}
json.dump({"version": VER, "icons": out}, open(os.path.join(HERE, "icons.json"), "w", encoding="utf-8"), indent=0, sort_keys=True)
print("products", len(ITEMS), "with logo", len(out), "unique logos", len(set(out.values())), "failed", bad)
