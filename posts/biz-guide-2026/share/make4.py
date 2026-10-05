"""Business owner's toolkit share images v7 (owner 10/5: "use this guy" - owner-supplied photo of a smiling shop owner in his doorway,
Desktop 1571250577304.jpg, 1080x720 landscape). Navy text panel + photo band so the landscape photo is not over-cropped.
og 1200x630, ig 1080x1350, story 1080x1920 -> biz-*-v7.jpg"""
import base64, io, os, subprocess, tempfile
from PIL import Image, ImageEnhance

OUT = r"C:\Users\Matt\Documents\3vl-share\biz-guide-2026"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
photo = Image.open(os.path.join(r"C:\Users\Matt\Documents\3vl-private\biz-guide-src", "_owner_guy.jpg")).convert("RGB")
photo = ImageEnhance.Color(photo).enhance(1.06)


def durl(im):
    b = io.BytesIO(); im.save(b, "JPEG", quality=88); return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


def crop(w, h, fx=0.5, fy=0.3):
    W, H = photo.size; r = w / h
    if W / H > r:
        nw = int(H * r); x = int((W - nw) * fx); im = photo.crop((x, 0, x + nw, H))
    else:
        nh = int(W / r); y = int((H - nh) * fy); im = photo.crop((0, y, W, y + nh))
    return durl(im.resize((w * 2, h * 2), Image.LANCZOS))


CHIPS = [("&#128176;", "Payroll"), ("&#129534;", "Taxes"), ("&#128210;", "Bookkeeping"), ("&#128737;&#65039;", "Insurance"),
         ("&#128200;", "Planning"), ("&#9878;&#65039;", "Legal"), ("&#128187;", "IT"), ("&#129309;", "Networking")]


def chips(px):
    return "".join('<span class="chip" style="font-size:%dpx">%s %s</span>' % (px, e, t) for e, t in CHIPS)


CSS = """*{box-sizing:border-box;margin:0;padding:0}html,body{overflow:hidden;font-family:'Radio Canada',sans-serif;color:#fff;background:#13233a}
.c{position:relative;overflow:hidden;background:#13233a}.ph{position:absolute;left:0;right:0;background-size:cover;background-position:center}
h1{font-weight:700;line-height:1;letter-spacing:-.025em}
h1 span{display:block}h1 .big{white-space:nowrap;font-weight:800;letter-spacing:-.035em;line-height:.95;margin-bottom:10px}h1 u{text-decoration:none;background:linear-gradient(transparent 80%,#ffc53d 80%)}
.sub{font-weight:700;text-shadow:0 3px 14px rgba(0,0,0,.5)}
.chips{display:flex;flex-wrap:wrap}
.chip{display:inline-flex;align-items:center;gap:8px;background:#fff;color:#13233a;font-weight:700;border-radius:999px;box-shadow:0 8px 22px rgba(0,0,0,.25)}
.pin{display:inline-block;font-weight:700;border-radius:999px;background:#1f5fae;color:#fff;box-shadow:0 8px 22px rgba(0,0,0,.3)}
.cta{display:inline-block;font-weight:700;color:#13233a;background:#ffc53d;border-radius:999px;box-shadow:0 10px 26px rgba(0,0,0,.3)}"""

HEAD = '<h1><span class="big" style="font-size:%dpx">BUSINESS OWNERS:</span><span style="font-size:%dpx;line-height:1.08">The tools you need to run your business are available from <u>local&nbsp;neighbors!</u></span></h1>'

IG = """<div class="c" style="width:1080px;height:1350px"><div class="ph" style="background-image:url(PH);top:400px;bottom:0"></div>
<div style="position:absolute;left:0;right:0;top:400px;height:200px;background:linear-gradient(180deg,#13233a 0%,rgba(19,35,58,0) 100%)"></div>
<div style="position:absolute;left:0;right:0;bottom:0;height:440px;background:linear-gradient(0deg,rgba(13,25,44,.95) 0%,rgba(13,25,44,.8) 55%,rgba(13,25,44,0) 100%)"></div>
<div style="position:absolute;left:64px;right:64px;top:56px">""" + HEAD % (104, 60) + """</div>
<div style="position:absolute;left:64px;right:64px;bottom:150px"><p class="sub" style="font-size:36px;margin-bottom:20px">Trusted local pros for every part of your business</p>
<div class="chips" style="gap:12px">CHIPS</div></div>
<div style="position:absolute;left:64px;right:64px;bottom:52px;display:flex;justify-content:space-between;align-items:center"><span class="pin" style="font-size:28px;padding:12px 22px">&#128205; Setauket &middot; Stony Brook &middot; Port Jeff</span><span class="cta" style="font-size:32px;padding:14px 28px">Link in bio &rarr;</span></div></div>"""

STORY = """<div class="c" style="width:1080px;height:1920px"><div class="ph" style="background-image:url(PH);top:560px;height:1060px"></div>
<div style="position:absolute;left:0;right:0;top:560px;height:240px;background:linear-gradient(180deg,#13233a 0%,rgba(19,35,58,0) 100%)"></div>
<div style="position:absolute;left:0;right:0;top:1120px;bottom:0;background:linear-gradient(0deg,#13233a 0%,#13233a 40%,rgba(13,25,44,.78) 66%,rgba(13,25,44,0) 100%)"></div>
<div style="position:absolute;left:64px;right:64px;top:200px">""" + HEAD % (100, 64) + """</div>
<div style="position:absolute;left:64px;right:64px;bottom:290px"><p class="sub" style="font-size:42px;margin-bottom:24px">Trusted local pros for every part of your&nbsp;business</p>
<div class="chips" style="gap:14px">CHIPS</div></div>
<div style="position:absolute;left:0;right:0;bottom:150px;text-align:center"><span class="cta" style="font-size:42px;padding:18px 38px">Tap to meet them &rarr;</span></div></div>"""

OG = """<div class="c" style="width:1200px;height:630px"><div class="ph" style="background-image:url(PH);left:300px;top:0;bottom:0"></div>
<div style="position:absolute;left:0;top:0;bottom:0;width:820px;background:linear-gradient(90deg,#13233a 0%,#13233a 58%,rgba(19,35,58,0) 100%)"></div>
<div style="position:absolute;left:56px;top:56px;width:620px">""" + HEAD % (66, 40) + """
<p class="sub" style="font-size:26px;margin:18px 0 18px">Trusted local pros for every part of your&nbsp;business</p>
<div class="chips" style="gap:9px;max-width:620px">CHIPS</div></div></div>"""


def render(name, frag, w, h, chip_px, ph):
    page = ('<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Radio+Canada:wght@500;600;700;800&display=swap" rel="stylesheet">'
            '<style>' + CSS + '.chip{padding:%dpx %dpx}</style></head><body>' % (int(chip_px * .42), int(chip_px * .75))
            + frag.replace("PH", ph).replace("CHIPS", chips(chip_px)) + '</body></html>')
    t = os.path.join(tempfile.gettempdir(), "bz4-%s.html" % name); open(t, "w", encoding="utf-8").write(page)
    png = t.replace(".html", ".png")
    subprocess.run([CHROME, "--headless=new", "--user-data-dir=" + os.path.join(tempfile.gettempdir(), "bz4-chrome"), "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=2", "--window-size=%d,%d" % (w, h), "--virtual-time-budget=8000", "--screenshot=" + png, "file:///" + t.replace("\\", "/")], capture_output=True)
    Image.open(png).convert("RGB").crop((0, 0, w * 2, h * 2)).resize((w, h), Image.LANCZOS).save(os.path.join(OUT, "biz-%s-v7.jpg" % name), quality=90)
    print("ok", name)


render("ig", IG, 1080, 1350, 30, crop(1080, 950, 0.62, 0.3))
render("story", STORY, 1080, 1920, 30, crop(1080, 1060, 0.72, 0.3))
render("og", OG, 1200, 630, 20, crop(900, 630, 0.75, 0.3))
