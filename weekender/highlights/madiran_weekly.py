"""Madiran The Wine Bar weekly live music graphic + caption (owner 11/3/2026: "a weekly post for them with that week's lineup,
fb and ig, tag and collab"). Approved look = madiran-ig-2026-11-03-v2.jpg (black, white + gold lettering, storefront photo on top,
every night styled the same, no highlighted day).
Schedule comes from Madiran's own events page (weekender/live/sources.py madiran()), one-liners from madiran_performers.json
(verified facts only; unknown names say "Live music" and are listed in meta.json "unknown" for the owner's preview email).
    python weekender/highlights/madiran_weekly.py <monday YYYY-MM-DD> <out dir>
Writes <out>/madiran-ig-<monday>.jpg, caption.txt, fb.txt, meta.json. Nothing is posted here."""
import datetime as dt, html, json, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "live"))
import sources                                                     # noqa: E402

monday = dt.date.fromisoformat(sys.argv[1])
out = sys.argv[2]
os.makedirs(out, exist_ok=True)
sunday = monday + dt.timedelta(days=6)
nights = sorted((e for e in sources.madiran() if monday <= e["start"].date() <= sunday), key=lambda e: e["start"])
if not nights:
    print("no Madiran live music between", monday, "and", sunday)
    json.dump({"monday": str(monday), "nights": 0}, open(os.path.join(out, "meta.json"), "w"))
    sys.exit(0)

known = {k: v for k, v in json.load(open(os.path.join(HERE, "madiran_performers.json"), encoding="utf-8")).items() if not k.startswith("_")}


def who(e):
    t = e["title"]
    return t[len("Live Music: "):] if t.startswith("Live Music: ") else t


def split(w):
    """('Cathy Rose Salit', 'with Rod Borrie, ...') - lead act + the rest, for the two-line row."""
    m = re.match(r"(.+?)\s+(with|plus)\s+(.+)", w)
    return (m.group(1), m.group(2) + " " + m.group(3)) if m else (w, "")


def blurb(w):
    lead, rest = split(w)
    k = re.sub(r"\s*&\s*", " and ", w.lower()).strip()
    lk = re.sub(r"\s*&\s*", " and ", lead.lower()).strip()
    b = known.get(k) or known.get(lk) or ""
    if rest:
        b = (b + ", " if b else "") + rest.replace(", and ", " & ").replace(" and ", " & ")
    return b


unknown, rows, lines = [], [], []
for e in nights:
    w = who(e)
    lead, _ = split(w)
    b = blurb(w)
    if not (known.get(re.sub(r"\s*&\s*", " and ", w.lower())) or known.get(re.sub(r"\s*&\s*", " and ", lead.lower()))):
        unknown.append(lead)
    d = e["start"]
    tm = "%d-%d PM" % (d.hour - 12, e["end"].hour - 12) if d.hour >= 12 else d.strftime("%I").lstrip("0")
    name = lead.replace(", and ", " & ").replace(" and ", " & ")
    rows.append('<div class="r"><div class="d">%s<small>%s</small></div><div class="t">%s</div><div class="p"><b>%s</b><span>%s</span></div></div>'
                % (d.strftime("%a"), d.strftime("%b ") + str(d.day), tm, html.escape(name), html.escape(b or "Live music")))
    lines.append("%s %d/%d, %s: %s" % (d.strftime("%a"), d.month, d.day, tm, w.replace(", and ", " & ").replace(" and ", " & ")))

first, last = nights[0]["start"].date(), nights[-1]["start"].date()
week = "%s %d to %d" % (first.strftime("%B"), first.day, last.day) if first.month == last.month else \
       "%s %d to %s %d" % (first.strftime("%B"), first.day, last.strftime("%B"), last.day)
tpl = open(os.path.join(HERE, "madiran-weekly.tpl.html"), encoding="utf-8").read()
page = tpl.replace("{{WEEK}}", week).replace("{{ROWS}}", "\n".join(rows))
if len(rows) > 5:   # 6-7 nights: tighter rows so the footer still fits
    page = page.replace("</style>", ".rows{gap:9px;margin-top:22px}.r{padding:11px 22px}.d{font-size:40px}.p b{font-size:27px}.p span{font-size:19px}h1{margin-top:150px}</style>")

work = tempfile.mkdtemp()
for f in ("madiran-ext.jpg", "3vl-white.png"):
    shutil.copy(os.path.join(HERE, f), work)
open(os.path.join(work, "p.html"), "w", encoding="utf-8").write(page)
chrome = shutil.which("google-chrome") or shutil.which("chromium") or r"C:\Program Files\Google\Chrome\Application\chrome.exe"
shot = os.path.join(work, "shot.png")
subprocess.run([chrome, "--headless=new", "--no-sandbox", "--user-data-dir=" + os.path.join(work, "prof"), "--force-device-scale-factor=2",
                "--window-size=1080,1350", "--hide-scrollbars", "--virtual-time-budget=8000", "--screenshot=" + shot,
                "file:///" + os.path.join(work, "p.html").replace("\\", "/")], check=True, capture_output=True)
from PIL import Image, ImageFilter                                  # noqa: E402
img = Image.open(shot).convert("RGB").resize((1080, 1350), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.0, 35, 2))
name = "madiran-ig-%s.jpg" % monday
img.save(os.path.join(out, name), quality=94, subsampling=0)

# Short caption, no performer names: the lineup is already in the photo.
cap = ("🍷 Live music all week at @madiranthewinebar_eastsetauket. Lineup in the photo.\n\n{cta}\n\n"
       "#threevillagelocal #yourneighborsinbusiness #livemusic #setauket")
open(os.path.join(out, "caption.txt"), "w", encoding="utf-8").write(cap.replace("{cta}", "Details: link in bio"))
open(os.path.join(out, "fb.txt"), "w", encoding="utf-8").write(cap.replace("@madiranthewinebar_eastsetauket", "{tag0}").replace("{cta}", "Details: https://www.threevillagelocal.com/events"))
json.dump({"monday": str(monday), "week": week, "image": name, "nights": len(nights), "unknown": unknown},
          open(os.path.join(out, "meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
shutil.rmtree(work, ignore_errors=True)
print("built", name, len(nights), "nights; unknown:", unknown)
