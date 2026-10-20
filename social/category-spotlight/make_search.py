"""Category spotlight v2 "search bar" (owner 10/7/2026): bright high-end photo of the category, official logo lockup,
headline, a big search bar with the category typed in, "Best matches in Three Village" dropdown with real members
(VIP gold pill, Featured blue tag), CTA line.  Outputs per category: <slug>-search-ig.jpg (1080x1350),
-search-story.jpg (1080x1920), -search-og.jpg (2400x1260 share image).

    python social/category-spotlight/make_search.py <slug> [<slug> ...]      (photos in 3vl-private/spotlight-v2/bg/)"""
import base64, json, os, subprocess, sys, html, pathlib, io, urllib.request
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
ASSETS = HERE.parent.parent
BG = pathlib.Path(r"C:\Users\Matt\Documents\3vl-private\spotlight-v2\bg")
OUT = pathlib.Path(r"C:\Users\Matt\Documents\3vl-private\spotlight-v2\out")
LOGO = pathlib.Path(r"C:\Users\Matt\Desktop\three village local 2\logo\group (44).png")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
COUNT = "340+"

CATS = {   # slug -> typed search, headline, photo (Pexels, free license), members (VIP first), highlight word, BD category page
    "restaurant": {"q": "Restaurants", "h": "Where to eat tonight?<br>Your neighbors are right here.", "bg": "restaurant-761854.jpg", "pos": "center 40%", "members": [292, 687, 25], "page": "restaurant"},
    "real-estate-services": {"q": "Real estate agent", "h": "Buying or selling?<br>Your neighbors are right here.", "bg": "realestate-12700529.jpg", "pos": "center 55%", "members": [71, 112, 684], "page": "real-estate-services"},
    "home-services": {"q": "Contractor", "h": "Need a contractor?<br>Your neighbors are right here.", "bg": "kitchen-36511374.jpg", "pos": "center 62%", "members": [115, 554, 259], "hl": "Contract", "page": "home-services"},
    "medical-services": {"q": "Doctor", "h": "Need a doctor?<br>Your neighbors are right here.", "bg": "medical-39192383.jpg", "pos": "center 40%", "members": [364, 499, 91], "page": "medical-services"},
    "financial-services": {"q": "Financial advisor", "h": "Planning your future?<br>Your neighbors are right here.", "bg": "financial-8815847.jpg", "pos": "center 40%", "members": [78, 217, 240], "page": "financial-services"},
    "attorney": {"q": "Attorney", "h": "Need an attorney?<br>Your neighbors are right here.", "bg": "attorney-6077091.jpg", "pos": "center 45%", "members": [137, 228, 299], "page": "attorney"},
    "beauty-personal-care": {"q": "Hair salon", "h": "Time for a refresh?<br>Your neighbors are right here.", "bg": "beauty-27165067.jpg", "pos": "center 50%", "members": [173, 685, 89], "page": "beauty-personal-care"},
    "shopping": {"q": "Boutique", "h": "Shopping local?<br>Your neighbors are right here.", "bg": "shopping-5490970.jpg", "pos": "center 50%", "members": [190, 160, 106], "hl": "Boutique", "page": "shopping"},
    "fitness-sports": {"q": "Fitness", "h": "Ready to get moving?<br>Your neighbors are right here.", "bg": "fitness-7031705.jpg", "pos": "center 55%", "members": [59, 88, 97], "page": "fitness-sports"},
    "education": {"q": "Tutoring", "h": "Classes and tutors?<br>Your neighbors are right here.", "bg": "education-8088099.jpg", "pos": "center 50%", "members": [296, 63, 75], "page": "education"},
}


def b64(path_or_bytes, mime="image/jpeg"):
    data = path_or_bytes if isinstance(path_or_bytes, bytes) else open(path_or_bytes, "rb").read()
    return "data:%s;base64,%s" % (mime, base64.b64encode(data).decode())


def logo_png(url):
    raw = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30).read()
    im = Image.open(io.BytesIO(raw)).convert("RGBA"); im.thumbnail((240, 240))
    buf = io.BytesIO(); im.save(buf, "PNG"); return b64(buf.getvalue(), "image/png")


def blurred(path):
    from PIL import ImageFilter, ImageEnhance
    im = Image.open(path).convert("RGB"); im.thumbnail((900, 900))
    im = ImageEnhance.Brightness(im.filter(ImageFilter.GaussianBlur(28))).enhance(0.72)
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=80); return buf.getvalue()


SHORT = {71: "Team Passamenti, Better Homes and Gardens", 112: "O'Dwyer-Brainard Team, Daniel Gale", 684: "Victor Stabile, Douglas Elliman",
         292: "Farm to Table by Filomena", 499: "Orthopedic Associates of LI", 78: "Girard Wealth Management", 217: "JLW Accounting and Tax"}


def members(ids, hl):
    idx = {m["id"]: m for m in json.load(open(ASSETS / "search" / "index.json", encoding="utf-8"))["members"]}
    rows = []
    for i in ids:
        m = dict(idx[i]); m["n"] = SHORT.get(i, m["n"])
        name = html.escape(m["n"])
        if hl and hl.lower() in m["n"].lower():
            k = m["n"].lower().index(hl.lower()); name = html.escape(m["n"][:k]) + '<span class=hl>' + html.escape(m["n"][k:k + len(hl)]) + '</span>' + html.escape(m["n"][k + len(hl):])
        tag = '<span class=vip>&#9733; VIP</span>' if m["p"] == "vip" else ('<span class=ft>Featured</span>' if m["p"] == "noticed" else "")
        rows.append('<div class=row><img src="%s"><div><b>%s %s</b><span>%s &middot; %s</span></div></div>' % (logo_png(m["l"]), name, tag, html.escape(m["c"]), html.escape(m["t"])))
    return "".join(rows)


CSS = """*{margin:0;box-sizing:border-box}body{width:%(W)dpx;height:%(H)dpx;overflow:hidden;font-family:'Radio Canada',sans-serif;position:relative;background:#13294b url(%(BLUR)s) center/cover}
.ph{position:absolute;left:0;right:0;top:0;height:%(PH)dpx;background:url(%(BG)s) %(POS)s/cover;-webkit-mask-image:linear-gradient(180deg,#000 72%%,transparent 100%%);mask-image:linear-gradient(180deg,#000 72%%,transparent 100%%)}
.sh{position:absolute;inset:0;background:linear-gradient(180deg,rgba(13,31,58,.55) 0%%,rgba(13,31,58,0) %(T1)d%%,rgba(13,31,58,0) %(T2)d%%,rgba(13,31,58,.62) %(T3)d%%,rgba(13,31,58,.80) 100%%)}
.top{position:absolute;left:52px;top:44px}.top img{height:%(LH)dpx;filter:drop-shadow(0 6px 18px rgba(0,0,0,.45))}
h1{position:absolute;left:56px;right:56px;top:%(HT)dpx;color:#fff;font-size:%(HS)dpx;line-height:1.03;font-weight:700;letter-spacing:-.02em;text-shadow:0 4px 24px rgba(0,0,0,.55)}
.bar{position:absolute;left:44px;right:44px;top:%(BT)dpx;height:128px;border-radius:999px;background:rgba(255,255,255,.97);display:flex;align-items:center;padding:0 16px 0 44px;box-shadow:0 24px 60px rgba(0,0,0,.40)}
.bar svg{flex:none}.q{flex:1;font-size:56px;color:#13294b;font-weight:500;margin-left:24px;letter-spacing:-.01em}.cur{display:inline-block;width:4px;height:58px;background:#1d5fbf;vertical-align:-8px;margin-left:4px}
.go{flex:none;height:96px;padding:0 42px;border-radius:999px;background:#1d5fbf;color:#fff;font-size:36px;font-weight:700;display:flex;align-items:center}
.dd{position:absolute;left:70px;right:70px;top:%(DT)dpx;background:#fff;border-radius:28px;padding:26px 30px 10px;box-shadow:0 24px 60px rgba(0,0,0,.38)}
.dd p{font-size:20px;letter-spacing:.14em;color:#1d5fbf;font-weight:700;margin-bottom:10px}
.row{display:flex;align-items:center;gap:22px;padding:14px 0;border-top:1px solid #e6ecf3}.row img{width:78px;height:78px;border-radius:16px;object-fit:contain;background:#fff;border:1px solid #e2e8f0}
.row div{min-width:0}.row b{display:block;font-size:31px;color:#13294b;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.row span{font-size:22px;color:#5b6b7c}.row b .hl{font-size:inherit;color:#1d5fbf;font-weight:700}
.vip{display:inline-block;font-size:17px;vertical-align:5px;margin-left:8px;padding:4px 10px;border-radius:999px;background:#ffc53d;color:#13294b;font-weight:700}
.ft{display:inline-block;font-size:15px;vertical-align:6px;margin-left:8px;padding:3px 9px;border-radius:999px;background:#eaf2fd;border:1px solid #c7dbf6;color:#1d5fbf;font-weight:700;letter-spacing:.06em;text-transform:uppercase}
.cta{position:absolute;left:0;right:0;bottom:%(CB)dpx;text-align:center;color:#fff;font-size:30px;font-weight:600;text-shadow:0 2px 12px rgba(0,0,0,.5)}.cta b{color:#8ec5ff}"""

OG_CSS = """*{margin:0;box-sizing:border-box}body{width:1200px;height:630px;overflow:hidden;font-family:'Radio Canada',sans-serif;position:relative;background:#13294b}
.ph{position:absolute;right:0;top:0;bottom:0;width:640px;background:url(%(BG)s) %(POS)s/cover}
.sh{position:absolute;inset:0;background:linear-gradient(90deg,#13294b 0%%,#13294b 46%%,rgba(19,41,75,.55) 58%%,rgba(19,41,75,0) 72%%)}
.top{position:absolute;left:44px;top:34px}.top img{height:70px}
h1{position:absolute;left:44px;width:640px;top:136px;color:#fff;font-size:44px;line-height:1.05;font-weight:700;letter-spacing:-.02em}
.bar{position:absolute;left:36px;width:660px;top:262px;height:84px;border-radius:999px;background:#fff;display:flex;align-items:center;padding:0 10px 0 30px;box-shadow:0 18px 40px rgba(0,0,0,.35)}
.bar svg{flex:none;width:38px;height:38px}.q{flex:1;font-size:36px;color:#13294b;font-weight:500;margin-left:16px}.cur{display:inline-block;width:3px;height:38px;background:#1d5fbf;vertical-align:-6px;margin-left:3px}
.go{flex:none;height:64px;padding:0 28px;border-radius:999px;background:#1d5fbf;color:#fff;font-size:24px;font-weight:700;display:flex;align-items:center}
.dd{position:absolute;left:52px;width:628px;top:362px;background:#fff;border-radius:20px;padding:16px 22px 4px;box-shadow:0 18px 40px rgba(0,0,0,.3)}
.dd p{font-size:13px;letter-spacing:.14em;color:#1d5fbf;font-weight:700;margin-bottom:6px}
.row{display:flex;align-items:center;gap:16px;padding:9px 0;border-top:1px solid #e6ecf3}.row img{width:54px;height:54px;border-radius:12px;object-fit:contain;background:#fff;border:1px solid #e2e8f0}
.row b{display:block;font-size:21px;color:#13294b;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:520px}.row span{font-size:15px;color:#5b6b7c}.row b .hl{font-size:inherit;font-weight:700;color:#1d5fbf}
.vip{display:inline-block;font-size:12px;vertical-align:3px;margin-left:6px;padding:3px 8px;border-radius:999px;background:#ffc53d;color:#13294b;font-weight:700}
.ft{display:inline-block;font-size:11px;vertical-align:4px;margin-left:6px;padding:2px 7px;border-radius:999px;background:#eaf2fd;border:1px solid #c7dbf6;color:#1d5fbf;font-weight:700;letter-spacing:.06em;text-transform:uppercase}
.cta{position:absolute;left:44px;bottom:22px;color:#fff;font-size:19px;font-weight:600}.cta b{color:#8ec5ff}"""

FORMATS = {   # W, H, logo h, headline top/size, bar top, dropdown top, cta bottom, shade stops
    "ig": dict(W=1080, H=1350, PH=760, LH=104, HT=530, HS=64, BT=700, DT=850, CB=42, T1=14, T2=30, T3=50),
    "story": dict(W=1080, H=1920, PH=1100, LH=116, HT=860, HS=70, BT=1060, DT=1214, CB=150, T1=10, T2=30, T3=52),
}


def render(html_text, w, h, out_jpg, scale=1):
    tmp = OUT / ("_r_%s.html" % out_jpg.stem); tmp.write_text(html_text, encoding="utf-8")
    png = OUT / ("_r_%s.png" % out_jpg.stem)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--user-data-dir=C:/Users/Matt/AppData/Local/Temp/chrome-spot2",
                    "--window-size=%d,%d" % (w, h), "--virtual-time-budget=6000", "--force-device-scale-factor=%d" % scale, "--screenshot=" + str(png), tmp.as_uri()], capture_output=True)
    Image.open(png).convert("RGB").save(out_jpg, quality=90); png.unlink(); tmp.unlink()


def build(slug):
    c = CATS[slug]; OUT.mkdir(parents=True, exist_ok=True)
    bg = b64(BG / c["bg"]); blur = b64(blurred(BG / c["bg"])); logo = b64(LOGO, "image/png"); rows = members(c["members"], c.get("hl"))
    search = ('<svg width="58" height="58" viewBox="0 0 24 24" fill="none" stroke="#13294b" stroke-width="2.4" stroke-linecap="round"><circle cx="10.5" cy="10.5" r="7"/><path d="M16 16l5 5"/></svg>'
              '<div class=q>%s<span class=cur></span></div><div class=go>Search</div>' % html.escape(c["q"]))
    for fmt, f in FORMATS.items():
        css = CSS % dict(f, BG=bg, BLUR=blur, POS=c.get("pos", "center"))
        cta = ("Search %s local businesses at <b>ThreeVillageLocal.com</b>" % COUNT) if fmt == "ig" else ("Tap the link to search %s local businesses" % COUNT)
        page = ('<!doctype html><html><head><meta charset=utf-8><link href="https://fonts.googleapis.com/css2?family=Radio+Canada:wght@400;500;600;700&display=swap" rel=stylesheet>'
                '<style>%s</style></head><body><div class=ph></div><div class=sh></div><div class=top><img src="%s"></div><h1>%s</h1><div class=bar>%s</div>'
                '<div class=dd><p>BEST MATCHES IN THREE VILLAGE</p>%s</div><div class=cta>%s</div></body></html>') % (css, logo, c["h"], search, rows, cta)
        render(page, f["W"], f["H"], OUT / ("%s-search-%s.jpg" % (slug, fmt)))
        print("built", slug, fmt)
    rows2 = "".join(rows.split("<div class=row>")[:3]).replace("</div></div></div>", "</div></div>", 0)
    rr = rows.split("<div class=row>")[1:3]
    og = ('<!doctype html><html><head><meta charset=utf-8><link href="https://fonts.googleapis.com/css2?family=Radio+Canada:wght@400;500;600;700&display=swap" rel=stylesheet>'
          '<style>%s</style></head><body><div class=ph></div><div class=sh></div><div class=top><img src="%s"></div><h1>%s</h1><div class=bar>%s</div>'
          '<div class=dd><p>BEST MATCHES IN THREE VILLAGE</p>%s</div><div class=cta>Search %s local businesses at <b>ThreeVillageLocal.com</b></div></body></html>') % (
        OG_CSS % dict(BG=bg, POS=c.get("pos", "center")), logo, c["h"], search, "".join("<div class=row>" + x for x in rr), COUNT)
    render(og, 1200, 630, OUT / ("%s-search-og.jpg" % slug), scale=2)
    print("built", slug, "og")


if __name__ == "__main__":
    for s in sys.argv[1:] or CATS:
        build(s)
