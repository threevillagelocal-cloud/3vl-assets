"""Business owner's toolkit share images (same premium style as the fall guide): og 1200x630, ig 1080x1350, story 1080x1920.
Rendered at 2x in headless Chrome, saved to 3vl-share/biz-guide-2026/. Run: python make.py"""
import base64, io, os, subprocess, tempfile
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = r"C:\Users\Matt\Documents\3vl-private\biz-guide-src"
OUT = r"C:\Users\Matt\Documents\3vl-share\biz-guide-2026"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def durl(im, q=84):
    b = io.BytesIO(); im.convert("RGB").save(b, "JPEG", quality=q)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


def crop(im, w, h):
    W, H = im.size; r = w / h
    if W / H > r:
        nw = int(H * r); im = im.crop(((W - nw) // 2, 0, (W - nw) // 2 + nw, H))
    else:
        nh = int(W / r); im = im.crop((0, (H - nh) // 2, W, (H - nh) // 2 + nh))
    return durl(im.resize((w * 2, h * 2), Image.LANCZOS))


hero = Image.open(os.path.join(SRC, "_hero_src.jpg"))
BG = durl(hero.resize((1400, int(hero.height * 1400 / hero.width))).filter(ImageFilter.GaussianBlur(10)))
A = Image.open(os.path.join(SRC, "_payroll_src.jpg"))
B = Image.open(os.path.join(SRC, "_insure_src.jpg"))

CSS = """*{box-sizing:border-box;margin:0;padding:0}html,body{overflow:hidden;background:#0c1018;font-family:'Radio Canada',sans-serif;color:#fff}
.c{position:relative;overflow:hidden}.bg{position:absolute;inset:-20px;background:url(BG) center/cover}
.vig{position:absolute;inset:0;background:linear-gradient(90deg,rgba(10,26,52,.92) 0%,rgba(12,34,68,.74) 45%,rgba(12,34,68,.38) 100%)}
.pill{display:inline-block;font-weight:700;letter-spacing:.06em;padding:10px 22px;border-radius:999px;background:rgba(255,255,255,.14);border:2px solid rgba(255,255,255,.35)}
h1{font-weight:700;line-height:1.02;letter-spacing:-.02em}h1 span{display:block;color:#8ec5ff}
.sub{font-weight:600}
.card{position:absolute;border-radius:22px;border:7px solid #fff;box-shadow:0 22px 50px rgba(0,0,0,.45);background-size:cover;background-position:center}
.card.gold{border-color:#fff;box-shadow:0 0 0 4px #8ec5ff,0 22px 50px rgba(0,0,0,.45)}
.tag{position:absolute;background:#fff;color:#13233a;font-weight:700;border-radius:999px;padding:8px 16px;box-shadow:0 6px 16px rgba(0,0,0,.3)}
.cta{display:inline-block;font-weight:700;color:#13233a;background:#ffc53d;border-radius:999px;padding:12px 26px}"""

OG = """<div class="c" style="width:1200px;height:630px"><div class="bg"></div><div class="vig"></div>
<div style="position:absolute;left:64px;top:84px;width:640px"><span class="pill" style="font-size:24px">&#128188; FOR LOCAL BUSINESSES</span>
<h1 style="font-size:78px;margin-top:26px">The Business Owner's Toolkit<span>Save money, keep it local</span></h1>
<p class="sub" style="font-size:30px;margin-top:22px">Setauket, Stony Brook &amp; Port Jeff</p></div>
<div class="card gold" style="left:760px;top:58px;width:380px;height:250px;background-image:url(A)"></div>
<div class="tag" style="left:782px;top:268px;font-size:22px">Payroll &amp; taxes</div>
<div class="card" style="left:790px;top:332px;width:350px;height:240px;background-image:url(B)"></div>
<div class="tag" style="left:812px;top:532px;font-size:22px">Insurance &amp; more</div></div>"""

IG = """<div class="c" style="width:1080px;height:1350px"><div class="bg"></div><div class="vig" style="background:linear-gradient(180deg,rgba(10,26,52,.9) 0%,rgba(12,34,68,.72) 55%,rgba(10,26,52,.9) 100%)"></div>
<div style="position:absolute;left:70px;top:80px;right:70px"><span class="pill" style="font-size:28px">&#128188; FOR LOCAL BUSINESSES</span>
<h1 style="font-size:104px;margin-top:30px">The Business Owner's Toolkit<span style="font-size:72px;margin-top:10px">Save money with neighbors you can call</span></h1></div>
<div class="card gold" style="left:70px;top:690px;width:450px;height:430px;background-image:url(A)"></div>
<div class="tag" style="left:96px;top:1076px;font-size:28px">Payroll &amp; taxes</div>
<div class="card" style="left:560px;top:740px;width:450px;height:380px;background-image:url(B)"></div>
<div class="tag" style="left:586px;top:1076px;font-size:28px">Insurance &amp; more</div>
<div style="position:absolute;left:70px;right:70px;bottom:62px;display:flex;justify-content:space-between;align-items:center"><span class="sub" style="font-size:32px">15 local pros + free help</span><span class="cta" style="font-size:32px">Link in bio &rarr;</span></div></div>"""

STORY = """<div class="c" style="width:1080px;height:1920px"><div class="bg"></div><div class="vig" style="background:linear-gradient(180deg,rgba(10,26,52,.9) 0%,rgba(12,34,68,.7) 55%,rgba(10,26,52,.92) 100%)"></div>
<div style="position:absolute;left:70px;top:230px;right:70px"><span class="pill" style="font-size:32px">&#128188; FOR LOCAL BUSINESSES</span>
<h1 style="font-size:118px;margin-top:36px">The Business Owner's Toolkit<span style="font-size:80px;margin-top:14px">Save money with neighbors you can call</span></h1></div>
<div class="card gold" style="left:70px;top:960px;width:470px;height:520px;background-image:url(A)"></div>
<div class="tag" style="left:96px;top:1436px;font-size:30px">Payroll &amp; taxes</div>
<div class="card" style="left:560px;top:1020px;width:450px;height:460px;background-image:url(B)"></div>
<div class="tag" style="left:586px;top:1436px;font-size:30px">Insurance &amp; more</div>
<div style="position:absolute;left:0;right:0;bottom:250px;text-align:center"><span class="cta" style="font-size:40px">Tap the link to read &rarr;</span></div></div>"""


def render(name, frag, w, h, a, b):
    page = ('<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Radio+Canada:wght@500;600;700&display=swap" rel="stylesheet">'
            '<style>' + CSS.replace("BG", BG) + '</style></head><body>' + frag.replace("url(A)", "url(" + a + ")").replace("url(B)", "url(" + b + ")") + '</body></html>')
    t = os.path.join(tempfile.gettempdir(), "bz-%s.html" % name)
    open(t, "w", encoding="utf-8").write(page)
    png = t.replace(".html", ".png")
    subprocess.run([CHROME, "--headless=new", "--user-data-dir=" + os.path.join(tempfile.gettempdir(), "bz-chrome"), "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=2", "--window-size=%d,%d" % (w, h), "--virtual-time-budget=6000", "--screenshot=" + png, "file:///" + t.replace("\\", "/")], capture_output=True)
    Image.open(png).convert("RGB").crop((0, 0, w * 2, h * 2)).resize((w, h), Image.LANCZOS).save(os.path.join(OUT, "biz-%s-v1.jpg" % name), quality=88)
    print("ok", name)


render("og", OG, 1200, 630, crop(A, 380, 250), crop(B, 350, 240))
render("ig", IG, 1080, 1350, crop(A, 450, 430), crop(B, 450, 380))
render("story", STORY, 1080, 1920, crop(A, 470, 520), crop(B, 450, 460))
