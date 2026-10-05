"""Business owner's toolkit share images v3 (owner 10/5: no Stony Brook Village photo, no logos; message = resources right here in Three Village).
Bright shop-owner-with-OPEN-sign photo (Pexels 6205772), big message, service chips. og 1200x630, ig 1080x1350, story 1080x1920 -> biz-*-v3.jpg"""
import base64, io, os, subprocess, tempfile, urllib.request
from PIL import Image, ImageEnhance

OUT = r"C:\Users\Matt\Documents\3vl-share\biz-guide-2026"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
src = os.path.join(r"C:\Users\Matt\Documents\3vl-private\biz-guide-src", "_open_src.jpg")
if not os.path.exists(src):
    b = urllib.request.urlopen(urllib.request.Request("https://images.pexels.com/photos/6205772/pexels-photo-6205772.jpeg?auto=compress&cs=tinysrgb&w=2400", headers={"User-Agent": "Mozilla/5.0"})).read()
    open(src, "wb").write(b)
photo = Image.open(src).convert("RGB")
photo = ImageEnhance.Color(ImageEnhance.Brightness(photo).enhance(1.05)).enhance(1.08)


def durl(im):
    b = io.BytesIO(); im.save(b, "JPEG", quality=86); return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


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
.c{position:relative;overflow:hidden}.ph{position:absolute;inset:0;background-size:cover;background-position:center}
.hey{font-family:'Permanent Marker',cursive;color:#ffc53d;transform:rotate(-2deg);display:inline-block;text-shadow:0 3px 12px rgba(0,0,0,.45)}
h1{font-weight:700;line-height:1;letter-spacing:-.025em;text-shadow:0 6px 26px rgba(0,0,0,.45)}
h1 span{display:block}h1 .big{white-space:nowrap;font-weight:800;letter-spacing:-.035em;line-height:.95;margin-bottom:8px}h1 u{text-decoration:none;background:linear-gradient(transparent 80%,#ffc53d 80%)}
.sub{font-weight:700;text-shadow:0 3px 14px rgba(0,0,0,.5)}
.chips{display:flex;flex-wrap:wrap}
.chip{display:inline-flex;align-items:center;gap:8px;background:#fff;color:#13233a;font-weight:700;border-radius:999px;box-shadow:0 8px 22px rgba(0,0,0,.25)}
.pin{display:inline-block;font-weight:700;border-radius:999px;background:#1f5fae;color:#fff;box-shadow:0 8px 22px rgba(0,0,0,.3)}
.cta{display:inline-block;font-weight:700;color:#13233a;background:#ffc53d;border-radius:999px;box-shadow:0 10px 26px rgba(0,0,0,.3)}"""

IG = """<div class="c" style="width:1080px;height:1350px"><div class="ph" style="background-image:url(PH)"></div>
<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(13,25,44,.86) 0%,rgba(13,25,44,.55) 30%,rgba(13,25,44,0) 48%,rgba(13,25,44,0) 58%,rgba(13,25,44,.82) 84%,rgba(13,25,44,.92) 100%)"></div>
<div style="position:absolute;left:64px;right:64px;top:60px"><h1><span class="big" style="font-size:104px">BUSINESS OWNERS:</span><span style="font-size:60px;line-height:1.08">The tools you need to run your business are available from <u>local&nbsp;neighbors!</u></span></h1></div>
<div style="position:absolute;left:64px;right:64px;bottom:150px"><p class="sub" style="font-size:38px;margin-bottom:22px">Trusted local pros for every part of your business</p>
<div class="chips" style="gap:12px">CHIPS</div></div>
<div style="position:absolute;left:64px;right:64px;bottom:52px;display:flex;justify-content:space-between;align-items:center"><span class="pin" style="font-size:28px;padding:12px 22px">&#128205; Setauket &middot; Stony Brook &middot; Port Jeff</span><span class="cta" style="font-size:32px;padding:14px 28px">Link in bio &rarr;</span></div></div>"""

STORY = """<div class="c" style="width:1080px;height:1920px"><div class="ph" style="background-image:url(PH)"></div>
<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(13,25,44,.86) 0%,rgba(13,25,44,.55) 26%,rgba(13,25,44,0) 42%,rgba(13,25,44,0) 66%,rgba(13,25,44,.85) 82%,rgba(13,25,44,.94) 100%)"></div>
<div style="position:absolute;left:64px;right:64px;top:200px"><h1><span class="big" style="font-size:100px">BUSINESS OWNERS:</span><span style="font-size:64px;line-height:1.08">The tools you need to run your business are available from <u>local&nbsp;neighbors!</u></span></h1></div>
<div style="position:absolute;left:64px;right:64px;bottom:250px"><p class="sub" style="font-size:42px;margin-bottom:24px">Trusted local pros for every part of your&nbsp;business</p>
<div class="chips" style="gap:14px">CHIPS</div></div>
<div style="position:absolute;left:0;right:0;bottom:120px;text-align:center"><span class="cta" style="font-size:42px;padding:18px 38px">Tap to meet them &rarr;</span></div></div>"""

OG = """<div class="c" style="width:1200px;height:630px"><div class="ph" style="background-image:url(PH);left:420px"></div>
<div style="position:absolute;left:0;top:0;bottom:0;width:760px;background:linear-gradient(90deg,#13233a 0%,#13233a 62%,rgba(19,35,58,0) 100%)"></div>
<div style="position:absolute;left:56px;top:54px;width:640px"><h1><span class="big" style="font-size:66px">BUSINESS OWNERS:</span><span style="font-size:40px;line-height:1.08">The tools you need to run your business are available from <u>local&nbsp;neighbors!</u></span></h1>
<p class="sub" style="font-size:28px;margin:16px 0 20px">Trusted local pros for every part of your&nbsp;business</p>
<div class="chips" style="gap:9px;max-width:660px">CHIPS</div></div></div>"""


def render(name, frag, w, h, chip_px, ph):
    page = ('<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Radio+Canada:wght@500;600;700&family=Permanent+Marker&display=swap" rel="stylesheet">'
            '<style>' + CSS + '.chip{padding:%dpx %dpx}</style></head><body>' % (int(chip_px * .42), int(chip_px * .75))
            + frag.replace("PH", ph).replace("CHIPS", chips(chip_px)) + '</body></html>')
    t = os.path.join(tempfile.gettempdir(), "bz3-%s.html" % name); open(t, "w", encoding="utf-8").write(page)
    png = t.replace(".html", ".png")
    subprocess.run([CHROME, "--headless=new", "--user-data-dir=" + os.path.join(tempfile.gettempdir(), "bz3-chrome"), "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=2", "--window-size=%d,%d" % (w, h), "--virtual-time-budget=8000", "--screenshot=" + png, "file:///" + t.replace("\\", "/")], capture_output=True)
    Image.open(png).convert("RGB").crop((0, 0, w * 2, h * 2)).resize((w, h), Image.LANCZOS).save(os.path.join(OUT, "biz-%s-v6.jpg" % name), quality=90)
    print("ok", name)


render("ig", IG, 1080, 1350, 30, crop(1080, 1350, 0.5, 0.25))
render("story", STORY, 1080, 1920, 30, crop(1080, 1920, 0.5, 0.12))
render("og", OG, 1200, 630, 20, crop(780, 630, 0.5, 0.2))
