"""Business owner's toolkit SHOWSTOPPER share images (v2, owner 10/5): bright real Stony Brook Village photo, big bold headline,
a 3x3 "toolkit" of real local experts' logos with field labels. og 1200x630, ig 1080x1350, story 1080x1920 -> 3vl-share/biz-guide-2026/biz-*-v2.jpg"""
import base64, io, os, subprocess, tempfile, urllib.request
from PIL import Image, ImageChops, ImageEnhance

SRC = r"C:\Users\Matt\Documents\3vl-private\biz-guide-src"
OUT = r"C:\Users\Matt\Documents\3vl-share\biz-guide-2026"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
SITE = "https://www.threevillagelocal.com/"
TOOLS = [  # (logo url, label, emoji, paying member)
    (SITE + "logos/profile/limage-138-61-photo.png", "Payroll", "&#128176;", True),
    (SITE + "pictures/profile/pimage-217-340-photo.jpg", "Taxes", "&#129534;", True),
    (SITE + "logos/profile/limage-240-52-photo.webp", "Bookkeeping", "&#128210;", True),
    (SITE + "logos/profile/limage-254-0-photo.png", "Insurance", "&#128737;&#65039;", False),
    (SITE + "logos/profile/limage-78-159-photo.webp", "Planning", "&#128200;", True),
    (SITE + "logos/profile/limage-137-223-photo.png", "Estate planning", "&#128220;", True),
    (SITE + "logos/profile/limage-228-310-photo.png", "Elder law", "&#9878;&#65039;", True),
    (None, "IT &amp; security", "&#128274;", False),
    (None, "Networking", "&#129309;", False),
]


def durl(im, fmt="PNG"):
    b = io.BytesIO(); im.save(b, fmt, **({"quality": 86} if fmt == "JPEG" else {}))
    return "data:image/%s;base64,%s" % ("jpeg" if fmt == "JPEG" else "png", base64.b64encode(b.getvalue()).decode())


def trim(im):
    rgb = im.convert("RGB"); bg = Image.new("RGB", rgb.size, rgb.getpixel((2, 2)))
    box = ImageChops.difference(rgb, bg).point(lambda p: 255 if p > 18 else 0).getbbox()
    return im.crop(box) if box else im


def fetch(url):
    return Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})).read())).convert("RGBA")


# logo urls for the two members whose files were found by listing (CD, CMIT, SBNA)
import json
pick = json.load(open(r"C:\Users\Matt\AppData\Local\Temp\claude\C--Users-Matt\d716503d-2251-415f-b256-0a083efdf61e\scratchpad\bizpick.json", encoding="utf-8"))
TOOLS[3] = (pick["254"]["img"],) + TOOLS[3][1:]
TOOLS[7] = (pick["402"]["img"],) + TOOLS[7][1:]
TOOLS[8] = (pick["153"]["img"],) + TOOLS[8][1:]
logos = []
for url, lab, em, vip in TOOLS:
    im = fetch(url)
    if "limage-78" not in url:   # keep Girard / CMIT as full color squares
        im = trim(im)
    im.thumbnail((520, 520))
    logos.append((durl(im), lab, em, vip, "sq" if "limage-78" in url else ""))

photo = Image.open(os.path.join(SRC, "_hero_src.jpg")).convert("RGB")
photo = ImageEnhance.Color(ImageEnhance.Contrast(ImageEnhance.Brightness(photo).enhance(1.18)).enhance(1.08)).enhance(1.25)


def photo_url(w, h, focus=0.5):
    W, H = photo.size; r = w / h
    if W / H > r:
        nw = int(H * r); x = int((W - nw) * focus); im = photo.crop((x, 0, x + nw, H))
    else:
        nh = int(W / r); im = photo.crop((0, (H - nh) // 2, W, (H - nh) // 2 + nh))
    return durl(im.resize((w * 2, h * 2), Image.LANCZOS), "JPEG")


def tiles(th, lab_px):
    out = []
    for src, lab, em, vip, sq in logos:
        out.append('<div class="t%s"><div class="lg%s" style="height:%dpx"><img src="%s"></div><span style="font-size:%dpx">%s %s</span></div>'
                   % (" vip" if vip else "", " sq" if sq else "", th, src, lab_px, em, lab))
    return "".join(out)


CSS = """*{box-sizing:border-box;margin:0;padding:0}html,body{overflow:hidden;font-family:'Radio Canada',sans-serif;color:#fff;background:#13233a}
.c{position:relative;overflow:hidden}.ph{position:absolute;inset:0;background-size:cover;background-position:center}
.hey{font-family:'Permanent Marker',cursive;color:#ffc53d;transform:rotate(-2deg);display:inline-block;text-shadow:0 3px 12px rgba(0,0,0,.5)}
h1{font-weight:700;line-height:.98;letter-spacing:-.025em;text-shadow:0 6px 28px rgba(0,0,0,.5)}
h1 .nw{white-space:nowrap}h1 u{text-decoration:none;background:linear-gradient(transparent 80%,#ffc53d 80%)}
.sub{font-weight:700;color:#fff;text-shadow:0 3px 14px rgba(0,0,0,.55)}.sub b{color:#8ec5ff}
.kit{position:absolute;background:#fff;border-radius:30px;box-shadow:0 30px 70px rgba(0,0,0,.45);display:grid;grid-template-columns:repeat(3,1fr)}
.kit .hd{grid-column:1/-1;display:flex;align-items:center;justify-content:center;gap:12px;color:#13233a;font-weight:700}
.t{display:flex;flex-direction:column;align-items:center;gap:10px}
.lg{width:100%;overflow:hidden;background:#fff;border:3px solid #e3eaf3;border-radius:20px;display:flex;align-items:center;justify-content:center;padding:12%;box-shadow:0 8px 20px rgba(19,35,58,.10)}
.lg img{max-width:100%;max-height:100%;object-fit:contain}
.lg.sq{padding:0;overflow:hidden}.lg.sq img{width:100%;height:100%;max-width:none;max-height:none;object-fit:cover}
.vip .lg{border-color:#ffc53d;box-shadow:0 0 0 3px rgba(255,197,61,.35),0 8px 20px rgba(19,35,58,.12)}
.t span{color:#13233a;font-weight:700;white-space:nowrap}
.cta{display:inline-block;font-weight:700;color:#13233a;background:#ffc53d;border-radius:999px;box-shadow:0 10px 26px rgba(0,0,0,.35)}
.pill{display:inline-block;font-weight:700;border-radius:999px;background:rgba(255,255,255,.18);border:2px solid rgba(255,255,255,.55);backdrop-filter:blur(6px)}"""

IG = """<div class="c" style="width:1080px;height:1350px"><div class="ph" style="background-image:url(PH)"></div>
<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(13,25,44,.82) 0%,rgba(13,25,44,.5) 26%,rgba(13,25,44,.0) 42%)"></div>
<div style="position:absolute;left:64px;right:64px;top:56px"><span class="hey" style="font-size:52px">Hey business owners!</span>
<h1 style="font-size:96px;margin-top:12px">Your local <span class="nw"><u>toolkit</u> &#129520;</span></h1>
<p class="sub" style="font-size:38px;margin-top:14px">Trusted neighbors for <b>every part</b> of your business</p></div>
<div class="kit" style="left:52px;right:52px;top:452px;padding:28px 28px 30px;gap:20px 20px">TILES</div>
<div style="position:absolute;left:0;right:0;bottom:46px;text-align:center"><span class="cta" style="font-size:38px;padding:16px 36px">See all the local pros &rarr; link in bio</span></div></div>"""

STORY = """<div class="c" style="width:1080px;height:1920px"><div class="ph" style="background-image:url(PH)"></div>
<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(13,25,44,.85) 0%,rgba(13,25,44,.5) 24%,rgba(13,25,44,.0) 40%,rgba(13,25,44,.0) 82%,rgba(13,25,44,.45) 100%)"></div>
<div style="position:absolute;left:64px;right:64px;top:210px"><span class="hey" style="font-size:58px">Hey business owners!</span>
<h1 style="font-size:104px;margin-top:14px">Your local <span class="nw"><u>toolkit</u> &#129520;</span></h1>
<p class="sub" style="font-size:42px;margin-top:16px">Trusted neighbors for <b>every part</b> of&nbsp;your&nbsp;business</p></div>
<div class="kit" style="left:52px;right:52px;top:700px;padding:32px 30px 36px;gap:24px 22px">TILES</div>
<div style="position:absolute;left:0;right:0;bottom:230px;text-align:center"><span class="cta" style="font-size:44px;padding:18px 40px">Tap the link to meet them &rarr;</span></div></div>"""

OG = """<div class="c" style="width:1200px;height:630px"><div class="ph" style="background-image:url(PH)"></div>
<div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(13,25,44,.86) 0%,rgba(13,25,44,.6) 36%,rgba(13,25,44,.1) 58%,rgba(13,25,44,0) 100%)"></div>
<div style="position:absolute;left:56px;top:70px;width:560px"><span class="hey" style="font-size:38px">Hey business owners!</span>
<h1 style="font-size:84px;margin-top:12px">Your local <span class="nw"><u>toolkit</u> &#129520;</span></h1>
<p class="sub" style="font-size:31px;margin-top:16px">Trusted neighbors for <b>every part</b> of your business</p>
<span class="pill" style="font-size:24px;padding:10px 22px;margin-top:26px">Setauket &middot; Stony Brook &middot; Port Jeff</span></div>
<div class="kit" style="left:640px;top:34px;width:524px;padding:20px;gap:14px 14px">TILES</div></div>"""


def render(name, frag, w, h, lab_px, focus, th):
    page = ('<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Radio+Canada:wght@500;600;700&family=Permanent+Marker&display=swap" rel="stylesheet">'
            '<style>' + CSS + '</style></head><body>' + frag.replace("PH", photo_url(w, h, focus)).replace("TILES", tiles(th, lab_px)) + '</body></html>')
    t = os.path.join(tempfile.gettempdir(), "bz2-%s.html" % name); open(t, "w", encoding="utf-8").write(page)
    png = t.replace(".html", ".png")
    subprocess.run([CHROME, "--headless=new", "--user-data-dir=" + os.path.join(tempfile.gettempdir(), "bz2-chrome"), "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=2", "--window-size=%d,%d" % (w, h), "--virtual-time-budget=8000", "--screenshot=" + png, "file:///" + t.replace("\\", "/")], capture_output=True)
    Image.open(png).convert("RGB").crop((0, 0, w * 2, h * 2)).resize((w, h), Image.LANCZOS).save(os.path.join(OUT, "biz-%s-v2.jpg" % name), quality=90)
    print("ok", name)


render("ig", IG, 1080, 1350, 26, 0.55, 168)
render("story", STORY, 1080, 1920, 28, 0.55, 210)
render("og", OG, 1200, 630, 19, 0.3, 112)
