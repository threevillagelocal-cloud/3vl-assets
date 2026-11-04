"""'Meet Captain Culper' launch graphic (owner 11/4/2026). 4:5 (1080x1350) + square (1080x1080).
python social/culper-launch/make.py -> out/culper-launch-ig.jpg, out/culper-launch-sq.jpg"""
import base64, io, pathlib, subprocess
from PIL import Image

HERE = pathlib.Path(__file__).parent
OUT = HERE / "out"
LOGO = pathlib.Path(r"C:\Users\Matt\Desktop\three village local 2\logo\group hd clear.png")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def b64(img, fmt="PNG"):
    buf = io.BytesIO(); img.save(buf, fmt); return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


CSS = """*{margin:0;box-sizing:border-box}body{width:%(W)dpx;height:%(H)dpx;overflow:hidden;font-family:'Radio Canada',sans-serif;color:#13294b;position:relative;
background:radial-gradient(900px 600px at 85%% 10%%,#dfeaff 0%%,rgba(223,234,255,0) 70%%),radial-gradient(700px 600px at 0%% 100%%,#e8f1ff 0%%,rgba(232,241,255,0) 70%%),#f6f9fe}
.logo{position:absolute;left:58px;top:%(LT)dpx;height:%(LH)dpx}
.new{position:absolute;right:58px;top:%(NT)dpx;background:#ffc53d;color:#13294b;font-weight:700;font-size:%(NS)dpx;letter-spacing:.08em;padding:12px 22px;border-radius:999px;box-shadow:0 10px 24px -12px rgba(19,41,75,.5)}
h1{position:absolute;left:58px;top:%(HT)dpx;width:%(HW)dpx;font-size:%(HS)dpx;line-height:.98;font-weight:700;letter-spacing:-.015em}h1 b{display:block;color:#1d5fd1}
.sub{position:absolute;left:62px;top:%(ST)dpx;font-size:%(SS)dpx;font-weight:600;color:#2b3f5e}
.mascot{position:absolute;left:%(ML)dpx;bottom:%(MB)dpx;height:%(MH)dpx;filter:drop-shadow(0 26px 30px rgba(19,41,75,.28))}
.chat{position:absolute;right:58px;top:%(CT)dpx;width:%(CW)dpx;background:#fff;border-radius:30px;box-shadow:0 34px 70px -28px rgba(19,41,75,.45),0 0 0 1px rgba(19,41,75,.06);overflow:hidden}
.ch{display:flex;align-items:center;gap:14px;padding:18px 20px;background:linear-gradient(135deg,#0f2445,#1d4fa8);color:#fff}
.ch img{width:58px;height:58px;border-radius:50%%;background:#fff;object-fit:cover;object-position:center 22%%;box-shadow:0 0 0 3px #f2c94c}
.ch b{display:block;font-size:24px}.ch i{font-style:normal;font-size:16px;color:#bfe0ff}
.cb{padding:20px 18px 22px;background:#f5f8fc;display:flex;flex-direction:column;gap:12px}
.m{max-width:88%%;padding:13px 16px;border-radius:20px;font-size:%(MS)dpx;line-height:1.35;font-weight:500}
.u{align-self:flex-end;background:#1d5fd1;color:#fff;border-bottom-right-radius:6px}.a{background:#fff;border:1px solid #e1e8f2;border-bottom-left-radius:6px}
.chips{display:flex;flex-wrap:wrap;gap:9px;margin-top:4px}.chips span{background:#fff;border:2px solid #cfdcf0;border-radius:999px;padding:9px 14px;font-size:%(PS)dpx;font-weight:700}
.foot{position:absolute;left:0;right:0;bottom:0;height:%(FH)dpx;background:#13294b;color:#fff;display:flex;align-items:center;justify-content:center;gap:22px;font-size:%(FS)dpx;font-weight:700}
.foot em{font-style:normal;color:#ffc53d}"""

FMT = {
    "ig": dict(W=1080, H=1350, LT=54, LH=96, NT=72, NS=22, HT=196, HW=980, HS=112, ST=430, SS=40, ML=-20, MB=96, MH=730, CT=770, CW=540, MS=24, PS=21, FH=96, FS=33),
    "sq": dict(W=1080, H=1080, LT=46, LH=84, NT=60, NS=20, HT=162, HW=980, HS=92, ST=360, SS=34, ML=-10, MB=84, MH=560, CT=520, CW=520, MS=22, PS=19, FH=84, FS=29),
}


def render(name, f):
    mascot = Image.open(HERE / "culper-full-hd.png")
    face = Image.open(r"C:\Users\Matt\Documents\3vl-share\site\culper\culper-face.png")
    logo = Image.open(LOGO).convert("RGBA")
    page = ('<!doctype html><html><head><meta charset=utf-8><link href="https://fonts.googleapis.com/css2?family=Radio+Canada:wght@400;500;600;700&display=swap" rel=stylesheet>'
            '<style>%s</style></head><body>'
            '<img class=logo src="%s"><div class=new>&#9733; NEW FEATURE</div>'
            '<h1>Meet<b>Captain Culper</b></h1><p class=sub>Your tour guide to Three Village</p>'
            '<img class=mascot src="%s">'
            '<div class=chat><div class=ch><img src="%s"><div><b>Captain Culper</b><i>Your Three Village insider &middot; AI</i></div></div>'
            '<div class=cb>'
            '<div class="m u">I need a plumber in Setauket</div>'
            '<div class="m a">Reporting for duty! Here are trusted local plumbers near you, with their pages.</div>'
            '<div class=chips><span>&#128295; A plumber</span><span>&#127829; A place to eat</span><span>&#127881; Local events</span></div></div></div>'
            '<div class=foot>Ask him on our website &amp; mobile app <em>ThreeVillageLocal.com</em></div>'
            '</body></html>') % (CSS % f, b64(logo), b64(mascot), b64(face))
    OUT.mkdir(exist_ok=True)
    tmp = OUT / ("_%s.html" % name); tmp.write_text(page, encoding="utf-8"); png = OUT / ("_%s.png" % name)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--user-data-dir=C:/Users/Matt/AppData/Local/Temp/chrome-culper",
                    "--window-size=%d,%d" % (f["W"], f["H"]), "--virtual-time-budget=6000", "--force-device-scale-factor=2", "--screenshot=" + str(png), tmp.as_uri()], capture_output=True)
    Image.open(png).convert("RGB").resize((f["W"], f["H"]), Image.LANCZOS).save(OUT / ("culper-launch-%s.jpg" % name), quality=93)
    png.unlink(); tmp.unlink(); print("built", name)


if __name__ == "__main__":
    for n, f in FMT.items():
        render(n, f)
