"""Share images for '5 Ways AI Can Help Your Long Island Business This Week' (business-owner recipe v7: navy text panel + bright photo).
og 960x640 (BD post_image, text inside the 1.91 band) + ig 1080x1350. No prices on images."""
import base64, io, os, subprocess, tempfile
from PIL import Image, ImageEnhance, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out"); os.makedirs(OUT, exist_ok=True)
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
photo = Image.open(os.path.join(HERE, "..", "src-photos", "36729750.jpg")).convert("RGB")
for f, v in ((ImageEnhance.Brightness, 1.06), (ImageEnhance.Color, 1.18), (ImageEnhance.Contrast, 1.06)):
    photo = f(photo).enhance(v)
LOGO = r"C:\Users\Matt\Desktop\three village local 2\logo\group (44).png"


def durl(im, fmt="JPEG"):
    b = io.BytesIO(); im.save(b, fmt, quality=90) if fmt == "JPEG" else im.save(b, fmt)
    return "data:image/%s;base64,%s" % (fmt.lower(), base64.b64encode(b.getvalue()).decode())


def crop(w, h, fx=0.5, fy=0.3):
    W, H = photo.size; r = w / h
    if W / H > r:
        nw = int(H * r); x = int((W - nw) * fx); im = photo.crop((x, 0, x + nw, H))
    else:
        nh = int(W / r); y = int((H - nh) * fy); im = photo.crop((0, y, W, y + nh))
    return durl(im.resize((w * 2, h * 2), Image.LANCZOS))


lg = Image.open(LOGO).convert("RGBA"); lg.thumbnail((700, 300)); LG = durl(lg, "PNG")
CHIPS = [("&#128172;", "Answers 24/7"), ("&#9997;&#65039;", "Drafts replies"), ("&#128202;", "One dashboard"), ("&#128269;", "Found by AI")]
CSS = """*{box-sizing:border-box;margin:0;padding:0}html,body{overflow:hidden;font-family:'Radio Canada',sans-serif;color:#fff;background:#13233a}
.c{position:relative;overflow:hidden;background:#13233a}.ph{position:absolute;background-size:cover;background-position:center}
.k{display:inline-block;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:#8ec5ff}
h1{font-weight:800;line-height:1.02;letter-spacing:-.02em}h1 span{color:#8ec5ff}
.sub{font-weight:700}.sub u{text-decoration:none;background:linear-gradient(transparent 78%,#ffc53d 78%)}
.chips{display:flex;flex-wrap:wrap}.chip{display:inline-flex;align-items:center;gap:8px;background:#fff;color:#13233a;font-weight:700;border-radius:999px;box-shadow:0 8px 22px rgba(0,0,0,.25)}"""
chips = lambda px: "".join('<span class="chip" style="font-size:%dpx;padding:%dpx %dpx">%s %s</span>' % (px, px * .42, px * .75, e, t) for e, t in CHIPS)

OG = """<div class="c" style="width:960px;height:640px"><div class="ph" style="background-image:url(@@PH@@);left:330px;right:0;top:0;bottom:0"></div>
<div style="position:absolute;left:0;top:0;bottom:0;width:640px;background:linear-gradient(90deg,#13233a 0%,#13233a 62%,rgba(19,35,58,0) 100%)"></div>
<div style="position:absolute;left:46px;top:92px;width:520px">
<p class="k" style="font-size:17px;margin-bottom:12px">Business owners</p>
<h1 style="font-size:50px">5 Ways AI Can Help Your Long Island Business <span>This Week</span></h1>
<p class="sub" style="font-size:27px;margin:16px 0 18px"><u>No tech skills</u> needed.</p>
<div class="chips" style="gap:8px">@@C16@@</div><img src="@@LG@@" style="width:190px;margin-top:22px;display:block"></div></div>"""

IG = """<div class="c" style="width:1080px;height:1350px"><div class="ph" style="background-image:url(@@PH@@);left:0;right:0;top:620px;bottom:0"></div>
<div style="position:absolute;left:0;right:0;top:620px;height:200px;background:linear-gradient(180deg,#13233a 0%,rgba(19,35,58,0) 100%)"></div>
<div style="position:absolute;left:0;right:0;bottom:0;height:300px;background:linear-gradient(0deg,rgba(13,25,44,.92) 0%,rgba(13,25,44,0) 100%)"></div>
<div style="position:absolute;left:64px;right:64px;top:70px"><p class="k" style="font-size:30px;margin-bottom:18px">Business owners</p>
<h1 style="font-size:92px">5 Ways AI Can Help Your Long Island Business <span>This Week</span></h1>
<p class="sub" style="font-size:46px;margin:22px 0 26px"><u>No tech skills</u> needed.</p><div class="chips" style="gap:12px">@@C28@@</div></div>
<div style="position:absolute;left:64px;bottom:60px"><img src="@@LG@@" style="width:300px"></div></div>"""


def render(name, frag, w, h, ph):
    page = ('<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Radio+Canada:wght@500;600;700;800&display=swap" rel="stylesheet">'
            '<style>' + CSS + '</style></head><body>' + frag.replace("@@C16@@", chips(16)).replace("@@C28@@", chips(28)).replace("@@LG@@", LG).replace("@@PH@@", ph) + '</body></html>')
    t = os.path.join(tempfile.gettempdir(), "ai5-%s.html" % name); open(t, "w", encoding="utf-8").write(page)
    png = t.replace(".html", ".png")
    subprocess.run([CHROME, "--headless=new", "--user-data-dir=" + os.path.join(tempfile.gettempdir(), "ai5-chrome"), "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=2", "--window-size=%d,%d" % (w, h), "--virtual-time-budget=8000", "--screenshot=" + png, "file:///" + t.replace("\\", "/")], capture_output=True)
    im = Image.open(png).convert("RGB").crop((0, 0, w * 2, h * 2)).resize((w, h), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1, 40, 2))
    im.save(os.path.join(OUT, name), quality=95)
    print("ok", name)


render("ai-5-ways-li-business-og.jpg", OG, 960, 640, crop(630, 640, 0.62, 0.3))
render("ai-5-ways-li-business-ig.jpg", IG, 1080, 1350, crop(1080, 730, 0.15, 0.0))
