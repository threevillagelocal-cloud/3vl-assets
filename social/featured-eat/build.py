"""Weekly "Featured right now" Instagram post + story for the homepage Eat & Drink section.

Picks the same places the homepage shows (weekender.js logic: owner's ranked list in weekender/live/preference.json,
Instagram special first, else this week's hand-picked card, cap), then renders:
  out/<date>/post.jpg   1080x1350 feed post
  out/<date>/story.jpg  1080x1920 story
  out/<date>/caption.txt and meta.json (handles, names, specials)
Per-place tweaks (shorter name, subtitle, photo choice) go in overrides.json.
Usage: python social/featured-eat/build.py [YYYY-MM-DD]
"""
import html, json, os, re, shutil, subprocess, sys, tempfile, datetime
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
WK = os.path.join(ROOT, "weekender")
LIVE = os.path.join(WK, "live")


def nm(x):
    x = re.sub(r"&[a-z#0-9]+;", "", str(x or "").lower())
    x = re.sub(r"\(.*?\)", "", x)
    x = re.sub(r"[^a-z0-9]", "", x)
    return re.sub(r"^the", "", x)


def load(p, default=None):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return default


def latest_edition():
    eds = sorted(x for x in os.listdir(WK) if re.fullmatch(r"\d{4}-\d{2}-\d{2}", x) and os.path.exists(os.path.join(WK, x, "weekend.json")))
    return eds[-1]


def pick():
    pref = load(os.path.join(LIVE, "preference.json"), {})
    accts = {a["ig"].lower(): a for a in load(os.path.join(LIVE, "ig_accounts.json"), [])}
    by_name = {nm(a["name"]): a for a in accts.values()}
    ig = {}
    for s in load(os.path.join(LIVE, "specials.json"), {}).get("specials", []):
        ig.setdefault(nm(s["biz"]), s)
    ed = latest_edition()
    hand = {}
    for s in load(os.path.join(WK, ed, "weekend.json"), {}).get("specials", []):
        hand.setdefault(nm(s["biz"]), dict(s, _ed=ed))
    out, used = [], set()
    for h in pref.get("order", []):
        a = accts.get(h.lower())
        if not a:
            continue
        k = nm(a["name"])
        if k in used:
            continue
        used.add(k)
        if k in ig:
            out.append(("ig", a, ig[k]))
        elif k in hand:
            out.append(("hand", a, hand[k]))
    for k, s in hand.items():
        if k not in used and k in by_name:
            out.append(("hand", by_name[k], s))
    return out[: int(pref.get("cap", 6))]


def photo(kind, a, s, ov):
    """Path of the card photo: override, else the Instagram post image for Instagram specials, else the place's own photo."""
    cands = []
    if ov.get("photo"):
        cands.append(os.path.join(ROOT, ov["photo"]))
    if kind == "ig" and s.get("inset"):
        cands.append(os.path.join(LIVE, s["inset"]))
    if kind == "hand":
        for key in ("ext", "venue", "dish"):
            if s.get(key):
                cands.append(os.path.join(WK, s["_ed"], s[key] + ".webp"))
    bp = load(os.path.join(LIVE, "biz_photos.json"), {}).get(a["ig"], "")
    m = re.search(r"/weekender/(.+)$", bp or "")
    if m:
        cands.append(os.path.join(WK, m.group(1).replace("-720.webp", ".webp")))
        cands.append(os.path.join(WK, m.group(1)))
    if s.get("inset"):
        cands.append(os.path.join(LIVE, s["inset"]))
    for c in cands:
        if os.path.exists(c):
            return c
    return ""


def subtitle(s, a):
    t = s.get("title", "")
    t = re.sub(r"\s+(at|@)\s+.*$", "", t, flags=re.I)          # "Oktoberfest at Schnitzels" -> "Oktoberfest"
    t = re.sub(r"\s+(launch|is back|returns)$", "", t, flags=re.I)
    return t


def short_name(a):
    return re.sub(r"\s*\(.*?\)", "", a["name"]).strip()


def chrome():
    for c in (os.environ.get("CHROME", ""), r"C:/Program Files/Google/Chrome/Application/chrome.exe", "google-chrome", "google-chrome-stable", "chromium"):
        if c and (os.path.exists(c) or shutil.which(c)):
            return c
    sys.exit("Chrome not found")


def render(html_path, png, w, h, profile):
    url = "file:///" + html_path.replace("\\", "/").lstrip("/")
    subprocess.run([chrome(), "--headless=new", "--user-data-dir=" + profile, "--hide-scrollbars", "--no-sandbox",
                    "--force-device-scale-factor=2", "--window-size=%d,%d" % (w, h), "--virtual-time-budget=9000",
                    "--screenshot=" + png, url], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    day = next((a for a in sys.argv[1:] if not a.startswith("--")), None) or datetime.date.today().isoformat()
    out = os.path.join(HERE, "out", day)
    os.makedirs(out, exist_ok=True)
    ovs = load(os.path.join(HERE, "overrides.json"), {})
    items = pick()
    meta, cards = [], {"post": "", "story": ""}
    for i, (kind, a, s) in enumerate(items):
        ov = ovs.get(a["ig"].lower(), {})
        src = photo(kind, a, s, ov)
        img = "p%d.jpg" % i
        if src:
            im = Image.open(src).convert("RGB")
            im.thumbnail((1200, 1200))
            im.save(os.path.join(out, img), quality=90)
        name = ov.get("name") or short_name(a)
        sub = ov.get("sub") or subtitle(s, a)
        pos = ov.get("pos", "50% 50%")
        h = a["ig"]
        meta.append({"ig": h, "name": name, "sub": sub, "title": s.get("title", ""), "when": s.get("when", ""), "kind": kind, "photo": os.path.relpath(src, ROOT) if src else ""})
        for fmt, bump in (("post", 0), ("story", 2)):
            fs = (21 if len(h) > 26 else 24 if len(h) > 20 else 27) + bump
            cards[fmt] += ('<div class="c"><div class="p" style="background-image:url(%s);background-position:%s">'
                           '<span class="stamp" style="font-size:%dpx"><b>@</b>%s</span></div>'
                           '<div class="t"><b>%s</b><i>%s</i></div></div>') % (img, pos, fs, html.escape(h), html.escape(name), html.escape(sub))
    shutil.copy(os.path.join(HERE, "village-hero.jpg"), os.path.join(out, "bg.jpg"))
    prof = tempfile.mkdtemp(prefix="feat-chrome-")
    for fmt, (w, hgt) in (("post", (1080, 1350)), ("story", (1080, 1920))):
        t = open(os.path.join(HERE, "tpl-%s.html" % fmt), encoding="utf-8").read()
        page = os.path.join(out, fmt + ".html")
        open(page, "w", encoding="utf-8").write(t.replace("{{CARDS}}", cards[fmt]).replace("{{BG}}", "bg.jpg"))
        png = os.path.join(out, fmt + "@2x.png")
        render(page, png, w, hgt, prof)
        Image.open(png).convert("RGB").resize((w, hgt), Image.LANCZOS).save(os.path.join(out, fmt + ".jpg"), quality=92)
        os.remove(png)
    shutil.rmtree(prof, ignore_errors=True)
    if "--no-video" not in sys.argv:
        anim = open(os.path.join(HERE, "anim.js.html"), encoding="utf-8").read()
        if not os.path.isdir(os.path.join(HERE, "node_modules")):
            subprocess.run("npm install --silent --no-audit --no-fund", shell=True, cwd=HERE, check=True)
        for fmt, (w, hgt) in (("post", (1080, 1350)), ("story", (1080, 1920))):
            t = open(os.path.join(out, fmt + ".html"), encoding="utf-8").read().replace("</body>", anim + "</body>")
            ap = os.path.join(out, fmt + "-anim.html")
            open(ap, "w", encoding="utf-8").write(t)
            subprocess.run(["node", os.path.join(HERE, "capture.js"), ap, str(w), str(hgt), os.path.join(out, fmt + ".mp4")], check=True)
    icons = ["🍽️", "🍷", "🌮", "🦞", "🥨", "🍦", "🍹", "🍕"]
    lines = ["🔥 LIVE ON OUR HOMEPAGE RIGHT NOW! These local spots just landed on the Three Village Local homepage. Go check out what they've got this week 👇", ""]
    for i, m in enumerate(meta):
        bit = m["title"] + (" (" + m["when"] + ")" if m["when"] and len(m["when"]) < 40 else "")
        lines.append("%s @%s - %s" % (icons[i % len(icons)], m["ig"], bit))
    lines += ["", "Go show some love to our local spots 💛 See all the specials at the link in bio.", "",
              "#ThreeVillageLocal #StonyBrook #Setauket #PortJefferson #EatLocal #LongIslandEats #SupportLocal"]
    open(os.path.join(out, "caption.txt"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    json.dump({"date": day, "places": meta}, open(os.path.join(out, "meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for m in meta:
        print(" - @%s | %s | %s | %s" % (m["ig"], m["name"], m["sub"], m["photo"]))
    print("wrote", out)


if __name__ == "__main__":
    main()
