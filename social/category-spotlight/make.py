"""Category spotlight graphics (3VL premium style, blue/white, yellow only as a small highlight).
For each category in cats.json: og (1200x630, page share image, no CTA), ig (1080x1350 feed post), story (1080x1920).
Usage: python make.py [slug ...]   -> out/<slug>-og.jpg, -ig.jpg, -story.jpg"""
import base64, io, json, os, subprocess, sys, time, urllib.request, websocket
from PIL import Image, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out"); os.makedirs(OUT, exist_ok=True)
CATS = json.load(open(os.path.join(HERE, "cats.json"), encoding="utf-8"))
IDX = {str(m["id"]): m for m in json.load(urllib.request.urlopen("https://raw.githubusercontent.com/threevillagelocal-cloud/3vl-assets/master/search/index.json"))["members"]}
UA = {"User-Agent": "Mozilla/5.0"}

def durl(im, q=86, fmt="JPEG"):
    b = io.BytesIO(); im.save(b, fmt, quality=q) if fmt == "JPEG" else im.save(b, fmt)
    return "data:image/%s;base64," % ("jpeg" if fmt == "JPEG" else "png") + base64.b64encode(b.getvalue()).decode()

def logo(uid):
    m = IDX.get(str(uid)); u = m and m.get("l")
    if not u: return None
    try:
        im = Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30).read())).convert("RGBA")
    except Exception:
        return None
    bg = Image.new("RGB", im.size, "white"); bg.paste(im, mask=im.split()[3]); bg.thumbnail((520, 520))
    return durl(bg, 90)

def bg_img(c):
    p = os.path.join(HERE, c.get("bg") or "../featured-eat/village-hero.jpg")
    im = Image.open(p).convert("RGB"); im = im.resize((1500, int(im.height * 1500 / im.width)))
    return durl(im.filter(ImageFilter.GaussianBlur(10)), 72)

CSS = """*{box-sizing:border-box;margin:0;padding:0}html,body{overflow:hidden;font-family:'Radio Canada',sans-serif;color:#fff;background:#0b1a33}
.bg{position:absolute;inset:-24px;background:url(@@BG@@) center/cover;filter:saturate(1.05)}
.v{position:absolute;inset:0}
.pill{display:inline-block;font-weight:700;letter-spacing:.07em;padding:10px 22px;border-radius:999px;background:rgba(255,255,255,.14);border:2px solid rgba(255,255,255,.35)}
h1{font-weight:700;letter-spacing:-.03em;line-height:.95;text-shadow:0 4px 24px rgba(0,0,0,.5)}h1 span{display:block;color:#8ec5ff}
.sub{font-weight:600;color:#eef3f8;text-shadow:0 3px 14px rgba(0,0,0,.6)}
.cta{display:inline-block;font-weight:700;padding:14px 30px;border-radius:999px;background:linear-gradient(180deg,#ffd76a,#ffc53d);color:#13233a;box-shadow:0 10px 26px rgba(255,197,61,.3)}
.grid{position:absolute;display:grid;gap:22px}
.k{border-radius:26px;background:#fff center/contain no-repeat;box-shadow:0 26px 54px rgba(0,0,0,.45);border:10px solid #fff}
.k.v1{box-shadow:0 26px 54px rgba(0,0,0,.45),0 0 0 6px #8ec5ff}"""

def cards(c, n):
    ids = [str(i) for i in c["feature"]][:n]
    vip = {str(i) for i in c.get("ring", [])}
    out = []
    for i in ids:
        d = logo(i)
        if d: out.append('<div class="k%s" style="background-image:url(%s)"></div>' % (" v1" if i in vip else "", d))
    return "".join(out)

def layouts(c):
    t, hook, sub = c["title"], c["hook"], c["sub"]
    return {
     "og": (1200, 630, """<div class="bg"></div><div class="v" style="background:linear-gradient(90deg,rgba(9,24,50,.92) 0%%,rgba(12,34,68,.74) 48%%,rgba(12,34,68,.35) 100%%)"></div>
<div style="position:absolute;left:62px;top:0;bottom:0;width:560px;display:flex;flex-direction:column;justify-content:center">
<span class="pill" style="align-self:flex-start;font-size:24px">&#128205; THREE VILLAGE</span>
<h1 style="font-size:%dpx;margin-top:22px">%s<span style="font-size:56px;margin-top:14px">%s</span></h1>
<div class="sub" style="font-size:32px;margin-top:22px">%s</div></div>
<div class="grid" style="right:56px;top:85px;grid-template-columns:215px 215px;grid-auto-rows:215px">%s</div>""" % (c.get("og_size", 84), t, hook, sub, cards(c, 4))),
     "ig": (1080, 1350, """<div class="bg"></div><div class="v" style="background:linear-gradient(180deg,rgba(9,24,50,.9) 0%%,rgba(12,34,68,.62) 50%%,rgba(9,24,50,.92) 100%%)"></div>
<div style="position:absolute;left:70px;right:70px;top:76px"><span class="pill" style="font-size:28px">&#128205; THREE VILLAGE LOCAL</span>
<h1 style="font-size:%dpx;margin-top:30px">%s<span style="font-size:76px;margin-top:16px">%s</span></h1></div>
<div class="grid" style="left:70px;right:70px;top:560px;grid-template-columns:repeat(3,1fr);grid-auto-rows:300px">%s</div>
<div style="position:absolute;left:70px;right:70px;bottom:78px;display:flex;justify-content:space-between;align-items:center">
<div class="sub" style="font-size:36px;max-width:560px">%s</div><span class="cta" style="font-size:32px">Link in bio &rarr;</span></div>""" % (c.get("ig_size", 116), t, hook, cards(c, 3), sub)),
     "story": (1080, 1920, """<div class="bg"></div><div class="v" style="background:linear-gradient(180deg,rgba(9,24,50,.88) 0%%,rgba(12,34,68,.55) 55%%,rgba(9,24,50,.94) 100%%)"></div>
<div style="position:absolute;left:80px;right:80px;top:230px"><span class="pill" style="font-size:32px">&#128205; THREE VILLAGE LOCAL</span>
<h1 style="font-size:%dpx;margin-top:36px">%s<span style="font-size:88px;margin-top:20px">%s</span></h1>
<div class="sub" style="font-size:44px;margin-top:28px">%s</div></div>
<div class="grid" style="left:120px;right:120px;top:960px;grid-template-columns:repeat(2,1fr);grid-auto-rows:330px">%s</div>
<div style="position:absolute;left:0;right:0;bottom:170px;text-align:center"><span class="cta" style="font-size:40px">Tap the link to see them all</span></div>""" % (c.get("story_size", 136), t, hook, sub, cards(c, 4))),
    }

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
p = subprocess.Popen([CHROME, "--headless=new", "--disable-gpu", "--remote-debugging-port=9383", "--remote-allow-origins=http://127.0.0.1:9383", "--user-data-dir=C:/Users/Matt/AppData/Local/Temp/claude-chrome-profile-catspot", "--hide-scrollbars", "about:blank"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(40):
        try: pg = [t for t in json.load(urllib.request.urlopen("http://127.0.0.1:9383/json")) if t["type"] == "page"][0]; break
        except Exception: time.sleep(.25)
    ws = websocket.create_connection(pg["webSocketDebuggerUrl"], timeout=180); n = [0]
    def cmd(m, **pa):
        n[0] += 1; ws.send(json.dumps({"id": n[0], "method": m, "params": pa}))
        while True:
            r = json.loads(ws.recv())
            if r.get("id") == n[0]: return r.get("result", {})
    cmd("Page.enable")
    for c in CATS:
        if sys.argv[1:] and c["slug"] not in sys.argv[1:]: continue
        bgd = bg_img(c)
        for name, (W, H, body) in layouts(c).items():
            html = "<!doctype html><html><head><meta charset='utf-8'><link href='https://fonts.googleapis.com/css2?family=Radio+Canada:wght@500;600;700&display=swap' rel='stylesheet'><style>" + CSS.replace("@@BG@@", bgd) + "html,body{width:%dpx;height:%dpx}</style></head><body>%s<script>document.fonts.ready.then(function(){setTimeout(function(){document.title='ready'},300)})</script></body></html>" % (W, H, body)
            f = os.path.join(OUT, "_%s-%s.html" % (c["slug"], name)); open(f, "w", encoding="utf-8").write(html)
            cmd("Emulation.setDeviceMetricsOverride", width=W, height=H, deviceScaleFactor=2, mobile=False)
            cmd("Page.navigate", url="file:///" + f.replace("\\", "/"))
            for _ in range(80):
                time.sleep(.3)
                if cmd("Runtime.evaluate", expression="document.title", returnByValue=True)["result"].get("value") == "ready": break
            im = Image.open(io.BytesIO(base64.b64decode(cmd("Page.captureScreenshot", format="png")["data"]))).convert("RGB")
            if name == "og": im.save(os.path.join(OUT, "%s-og.jpg" % c["slug"]), quality=88)          # 2400x1260, like the listing images
            else: im.resize((W, H), Image.LANCZOS).save(os.path.join(OUT, "%s-%s.jpg" % (c["slug"], name)), quality=90)
            os.remove(f)
        print("done", c["slug"])
finally: p.terminate()
