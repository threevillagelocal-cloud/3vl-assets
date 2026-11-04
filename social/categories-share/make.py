"""/categories share images (owner 11/4/2026: "refresh to our new premium style ... reflect the webpage and the great local businesses").
Mirrors the page: "Explore Three Village" hero + search bar + category tiles. No business names or logos (category share rule 11/2).
python social/categories-share/make.py -> out/categories-og.jpg (2400x1260), categories-ig.jpg (1080x1350), categories-sq.jpg (1080x1080)"""
import base64, io, pathlib, subprocess
from PIL import Image, ImageFilter

HERE = pathlib.Path(__file__).parent
OUT = HERE / "out"
BG = pathlib.Path(r"C:\Users\Matt\Documents\3vl-private\spotlight-v2\bg")
LOGO = pathlib.Path(r"C:\Users\Matt\Desktop\three village local 2\logo\group hd clear.png")   # navy-text lockup for the light background
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
COUNT = "500+"   # search/index.json had 535 live listings on 11/4/2026

TILES = [("Restaurants", "restaurant-761854.jpg", "center 45%", '<path d="M7 3v8a2 2 0 0 0 2 2v8M11 3v8M3 3v8a2 2 0 0 0 2 2M17 21V3c-2 0-3 3-3 7h3"/>'),
         ("Home Services", "kitchen-36511374.jpg", "center 60%", '<path d="M3 11l9-7 9 7M5 10v10h14V10"/>'),
         ("Health &amp; Wellness", "medical-39192383.jpg", "center 40%", '<path d="M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.5-7 10-7 10z"/>'),
         ("Beauty", "beauty-27165067.jpg", "center 45%", '<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4L8.1 15.9M14.5 14.5L20 20M8.1 8.1L12 12"/>'),
         ("Real Estate", "realestate-12700529.jpg", "center 55%", '<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M17 6l3 3M15 8l2 2"/>'),
         ("Shop Local", "shopping-5490970.jpg", "center 50%", '<path d="M5 8h14l-1 12H6L5 8zM9 8V6a3 3 0 0 1 6 0v2"/>')]


def b64(img, fmt="JPEG"):
    buf = io.BytesIO(); img.save(buf, fmt, quality=88)
    return "data:image/%s;base64,%s" % ("png" if fmt == "PNG" else "jpeg", base64.b64encode(buf.getvalue()).decode())


def photo(name, w=700):
    im = Image.open(BG / name).convert("RGB"); im.thumbnail((w, w * 2)); return b64(im)


def backdrop():
    im = Image.open(BG / "restaurant-3201920.jpg").convert("RGB"); im.thumbnail((1400, 1400))
    return b64(im.filter(ImageFilter.GaussianBlur(10)))


def tiles_html():
    out = []
    for name, f, pos, icon in TILES:
        out.append('<div class=t style="background-image:url(%s);background-position:%s"><span><svg viewBox="0 0 24 24" fill="none" stroke="#1d5fd1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">%s</svg>%s</span></div>' % (photo(f), pos, icon, name))
    return "".join(out)


BASE = """*{margin:0;box-sizing:border-box}body{width:%(W)dpx;height:%(H)dpx;overflow:hidden;font-family:'Radio Canada',sans-serif;position:relative;background:#f4f8fe;color:#13294b}
.bg{position:absolute;inset:0;background:radial-gradient(900px 500px at 0%% 0%%,#ffffff 0%%,rgba(255,255,255,0) 70%%),radial-gradient(800px 600px at 100%% 100%%,#e3eeff 0%%,rgba(227,238,255,0) 70%%)}.sh{display:none}
.logo{position:absolute;%(LOGO)s}
.k{position:absolute;%(KPOS)s;font-size:%(KS)dpx;font-weight:700;letter-spacing:.2em;color:#1d5fd1}
h1{position:absolute;%(HPOS)s;font-size:%(HS)dpx;line-height:1.02;font-weight:700;letter-spacing:-.01em}h1 b{color:#1d5fd1;font-weight:700}
.sub{position:absolute;%(SPOS)s;font-size:%(SS)dpx;line-height:1.3;font-weight:500;color:#44546b}
.bar{position:absolute;%(BPOS)s;display:flex;align-items:center;gap:%(BG2)dpx;background:#fff;border-radius:999px;border:2px solid #d5e2f5;box-shadow:0 18px 40px -18px rgba(19,41,75,.35)}
.bar svg{flex:none}.bar .q{flex:1;color:#13294b;font-weight:500;white-space:nowrap}.bar .q i{display:inline-block;width:3px;height:1.05em;background:#1d5fd1;vertical-align:-.15em;margin-left:3px}
.bar .go{background:#1d5fd1;color:#fff;font-weight:700;border-radius:999px}
.grid{position:absolute;%(GPOS)s;display:grid;grid-template-columns:repeat(%(COLS)d,1fr);gap:%(GAP)dpx}
.t{position:relative;border-radius:%(TR)dpx;background-size:cover;box-shadow:0 18px 36px -16px rgba(19,41,75,.45);border:4px solid #fff}
.t span{position:absolute;left:%(TL)dpx;bottom:%(TL)dpx;display:flex;align-items:center;gap:8px;background:#fff;color:#13294b;font-weight:700;font-size:%(TS)dpx;padding:%(TP)s;border-radius:999px;box-shadow:0 6px 16px -6px rgba(0,0,0,.45);white-space:nowrap}
.t svg{width:%(TI)dpx;height:%(TI)dpx;flex:none}
.cta{position:absolute;%(CPOS)s;display:inline-flex;align-items:center;gap:14px;font-size:%(CS)dpx;font-weight:700;color:#13294b}
.cta em{font-style:normal;background:#ffc53d;color:#13294b;border-radius:999px;padding:%(CP)s}"""

FMT = {
    "og": dict(W=1200, H=630, GRAD="90deg,rgba(9,24,52,.92) 0%,rgba(9,24,52,.78) 44%,rgba(9,24,52,.35) 100%",
               LOGO="left:52px;top:40px;height:84px", KPOS="left:56px;top:150px", KS=17, HPOS="left:52px;top:180px;width:600px", HS=76,
               SPOS="left:56px;top:350px;width:540px", SS=25, BPOS="left:52px;top:428px;width:560px;height:74px;padding:0 9px 0 26px", BG2=14,
               GPOS="left:668px;top:40px;width:494px;height:550px", COLS=2, GAP=14, TR=20, TL=10, TS=16, TP="7px 12px 7px 9px", TI=18,
               CPOS="left:56px;top:532px", CS=24, CP="8px 18px", BARQ=27, ICON=34, GOS="font-size:22px;padding:15px 24px"),
    "ig": dict(W=1080, H=1350, GRAD="180deg,rgba(9,24,52,.9) 0%,rgba(9,24,52,.8) 46%,rgba(9,24,52,.55) 100%",
               LOGO="left:64px;top:60px;height:104px", KPOS="left:68px;top:206px", KS=24, HPOS="left:64px;top:244px;width:960px", HS=104,
               SPOS="left:68px;top:476px;width:900px", SS=36, BPOS="left:64px;top:568px;width:952px;height:104px;padding:0 12px 0 34px", BG2=18,
               GPOS="left:64px;top:716px;width:952px;height:470px", COLS=3, GAP=16, TR=22, TL=12, TS=21, TP="8px 14px 8px 10px", TI=22,
               CPOS="left:68px;top:1226px", CS=34, CP="10px 24px", BARQ=38, ICON=46, GOS="font-size:30px;padding:20px 34px"),
    "sq": dict(W=1080, H=1080, GRAD="180deg,rgba(9,24,52,.9) 0%,rgba(9,24,52,.8) 50%,rgba(9,24,52,.55) 100%",
               LOGO="left:60px;top:50px;height:92px", KPOS="left:64px;top:176px", KS=22, HPOS="left:60px;top:208px;width:960px", HS=92,
               SPOS="left:64px;top:318px;width:960px", SS=32, BPOS="left:60px;top:390px;width:960px;height:96px;padding:0 12px 0 32px", BG2=18,
               GPOS="left:60px;top:522px;width:960px;height:410px", COLS=3, GAP=14, TR=20, TL=11, TS=20, TP="8px 13px 8px 10px", TI=21,
               CPOS="left:64px;top:968px", CS=32, CP="9px 22px", BARQ=34, ICON=42, GOS="font-size:28px;padding:18px 30px"),
}
HEAD = {"og": "Explore<br><b>Three Village</b>", "ig": "Explore<br><b>Three Village</b>", "sq": "Explore <b>Three Village</b>"}
SUB = {"og": "The local businesses your neighbors trust, all in one place.", "ig": "The local businesses your neighbors trust,<br>all in one place.",
       "sq": "The local businesses your neighbors trust, all in one place."}
CTA = {"og": "<em>Click to explore</em>", "ig": "<em>Search %s local businesses &rarr;</em>" % COUNT, "sq": "<em>Search %s local businesses &rarr;</em>" % COUNT}


def render(name, f):
    css = BASE % dict(f, BG=backdrop())
    logo = b64(Image.open(LOGO).convert("RGBA"), "PNG")
    bar = ('<svg width="%(I)d" height="%(I)d" viewBox="0 0 24 24" fill="none" stroke="#13294b" stroke-width="2.4" stroke-linecap="round"><circle cx="10.5" cy="10.5" r="7"/><path d="M16 16l5 5"/></svg>'
           '<div class=q style="font-size:%(Q)dpx">pizza, plumber, dentist<i></i></div><div class=go style="%(G)s">Search</div>') % dict(I=f["ICON"], Q=f["BARQ"], G=f["GOS"])
    page = ('<!doctype html><html><head><meta charset=utf-8><link href="https://fonts.googleapis.com/css2?family=Radio+Canada:wght@400;500;600;700&display=swap" rel=stylesheet>'
            '<style>%s</style></head><body><div class=bg></div><div class=sh></div><img class=logo src="%s"><p class=k>FIND A LOCAL BUSINESS</p><h1>%s</h1><p class=sub>%s</p>'
            '<div class=bar>%s</div><div class=grid>%s</div><div class=cta>%s</div></body></html>') % (css, logo, HEAD[name], SUB[name], bar, tiles_html(), CTA[name])
    OUT.mkdir(exist_ok=True)
    tmp = OUT / ("_%s.html" % name); tmp.write_text(page, encoding="utf-8"); png = OUT / ("_%s.png" % name)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--user-data-dir=C:/Users/Matt/AppData/Local/Temp/chrome-catshare",
                    "--window-size=%d,%d" % (f["W"], f["H"]), "--virtual-time-budget=6000", "--force-device-scale-factor=%d" % (2 if name == "og" else 1),
                    "--screenshot=" + str(png), tmp.as_uri()], capture_output=True)
    Image.open(png).convert("RGB").save(OUT / ("categories-%s.jpg" % name), quality=92); png.unlink(); tmp.unlink()
    print("built", name)


if __name__ == "__main__":
    for n, f in FMT.items():
        render(n, f)
