"""Fall guide share images (premium 3VL style): og 1200x630, ig post 1080x1350, ig story 1080x1920. Renders at 2x in headless Chrome."""
import base64, json, subprocess, time, urllib.request, websocket, os, io
from PIL import Image, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
IG = r"C:\Users\Matt\AppData\Local\Temp\claude\C--Users-Matt\8cd8646e-5951-4601-a8cd-13eca8e132e2\scratchpad\fall\ig"
idx = json.load(open(os.path.join(IG, "index.json"), encoding="utf-8"))
def igf(i): return os.path.join(IG, idx[i]["file"].split("/", 1)[1])
def durl(im, q=82):
    b = io.BytesIO(); im.convert("RGB").save(b, "JPEG", quality=q); return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
bg = Image.open(igf(53)).convert("RGB"); bg = bg.resize((1400, int(bg.height * 1400 / bg.width))).filter(ImageFilter.GaussianBlur(10))
hero = Image.open(r"C:\Users\Matt\Documents\3vl-share\fall-2026\hero-1600.webp")
mums = Image.open(igf(52)); pj = Image.open(igf(46))
def card(im, w, h):
    W, H = im.size; r = w / h
    if W / H > r: nw = int(H * r); im = im.crop(((W - nw) // 2, 0, (W - nw) // 2 + nw, H))
    else: nh = int(W / r); im = im.crop((0, (H - nh) // 2, W, (H - nh) // 2 + nh))
    return durl(im.resize((w * 2, h * 2)))
CSS = """*{box-sizing:border-box;margin:0;padding:0}html,body{overflow:hidden;background:#0c1018;font-family:'Radio Canada',sans-serif;color:#fff}
.c{position:relative;overflow:hidden}.bg{position:absolute;inset:-20px;background:url(BG) center/cover;filter:saturate(1.25) brightness(1.12)}
.vig{position:absolute;inset:0;background:linear-gradient(90deg,rgba(14,40,80,.7) 0%,rgba(14,40,80,.4) 45%,rgba(14,40,80,.1) 100%)}
.pill{display:inline-block;font-weight:700;letter-spacing:.06em;padding:10px 22px;border-radius:999px;background:rgba(255,255,255,.14);border:2px solid rgba(255,255,255,.35)}
.gold{display:inline-block;font-weight:700;padding:12px 26px;border-radius:999px;background:linear-gradient(180deg,#ffd76a,#ffc53d);color:#13233a;box-shadow:0 10px 26px rgba(255,197,61,.35)}
h1{font-weight:700;letter-spacing:-.035em;line-height:.95;text-shadow:0 4px 24px rgba(0,0,0,.55)}h1 span{display:block;color:#8ec5ff}
.sub{font-weight:600;color:#eef3f8;text-shadow:0 3px 14px rgba(0,0,0,.6)}
.k{position:absolute;border-radius:26px;background:#fff center/cover;box-shadow:0 18px 40px rgba(0,0,0,.35);border:6px solid #fff}
.k.v{box-shadow:0 18px 40px rgba(0,0,0,.35),0 0 0 6px #8ec5ff,0 0 40px rgba(142,197,255,.4)}"""
T = {
 "og": (1200, 630, """<div class="c" style="width:1200px;height:630px"><div class="bg"></div><div class="vig"></div>
<div style="position:absolute;left:62px;top:0;bottom:0;width:640px;display:flex;flex-direction:column;justify-content:center">
<span class="pill" style="align-self:flex-start;font-size:26px">&#127810; 2026 GUIDE</span>
<h1 style="font-size:92px;margin-top:22px">Fall in<br>Three Village<span style="font-size:66px;margin-top:14px">Pumpkins &amp; Festivals</span></h1>
<div class="sub" style="font-size:36px;margin-top:22px">Setauket, Stony Brook &amp; Port Jeff</div></div>
<div class="k v" style="right:60px;top:70px;width:340px;height:250px;background-image:url(@@CARD1@@)"></div>
<div class="k" style="right:110px;top:345px;width:290px;height:215px;background-image:url(@@CARD2@@)"></div></div>""",
  [(340, 250, hero), (290, 215, mums)]),
 "ig": (1080, 1350, """<div class="c" style="width:1080px;height:1350px"><div class="bg"></div><div class="vig" style="background:linear-gradient(180deg,rgba(14,40,80,.62) 0%,rgba(14,40,80,.22) 42%,rgba(14,40,80,.12) 62%,rgba(14,40,80,.5) 100%)"></div>
<div style="position:absolute;left:70px;right:70px;top:80px"><span class="pill" style="font-size:30px">&#127810; THE 2026 FALL GUIDE</span>
<h1 style="font-size:124px;margin-top:30px">Fall in<br>Three Village<span style="font-size:82px;margin-top:18px">Pumpkins, hayrides &amp; festivals</span></h1></div>
<div class="k v" style="left:70px;top:760px;width:400px;height:300px;background-image:url(@@CARD1@@)"></div>
<div class="k" style="right:70px;top:800px;width:340px;height:260px;background-image:url(@@CARD2@@)"></div>
<div style="position:absolute;left:70px;right:70px;bottom:80px;display:flex;justify-content:space-between;align-items:center">
<div class="sub" style="font-size:40px">30+ picks near Setauket</div><span class="gold" style="font-size:34px">Link in bio &rarr;</span></div></div>""",
  [(400, 300, hero), (340, 260, pj)]),
 "story": (1080, 1920, """<div class="c" style="width:1080px;height:1920px"><div class="bg"></div><div class="vig" style="background:linear-gradient(180deg,rgba(14,40,80,.6) 0%,rgba(14,40,80,.2) 40%,rgba(14,40,80,.1) 62%,rgba(14,40,80,.5) 100%)"></div>
<div style="position:absolute;left:80px;right:80px;top:300px"><span class="pill" style="font-size:34px">&#127810; THE 2026 FALL GUIDE</span>
<h1 style="font-size:150px;margin-top:36px">Fall in<br>Three Village<span style="font-size:96px;margin-top:22px">Pumpkins, hayrides &amp; festivals</span></h1></div>
<div class="k v" style="left:80px;top:1090px;width:470px;height:350px;background-image:url(@@CARD1@@)"></div>
<div class="k" style="right:80px;top:1200px;width:380px;height:300px;background-image:url(@@CARD2@@)"></div>
<div style="position:absolute;left:80px;right:80px;bottom:300px;text-align:center"><span class="gold" style="font-size:42px">Tap the link for the full guide</span></div></div>""",
  [(470, 350, hero), (380, 300, mums)]),
}
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
p = subprocess.Popen([CHROME, "--headless=new", "--disable-gpu", "--remote-debugging-port=9374", "--remote-allow-origins=http://127.0.0.1:9374", "--user-data-dir=C:/Users/Matt/AppData/Local/Temp/claude-chrome-profile-fallshare", "--hide-scrollbars", "about:blank"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(40):
        try: pg = [t for t in json.load(urllib.request.urlopen("http://127.0.0.1:9374/json")) if t["type"] == "page"][0]; break
        except Exception: time.sleep(.25)
    ws = websocket.create_connection(pg["webSocketDebuggerUrl"], timeout=120); n = [0]
    def cmd(m, **pa):
        n[0] += 1; ws.send(json.dumps({"id": n[0], "method": m, "params": pa}))
        while True:
            r = json.loads(ws.recv())
            if r.get("id") == n[0]: return r.get("result", {})
    cmd("Page.enable")
    for name, (W, H, body, cards) in T.items():
        b = body
        for i, (w, h, im) in enumerate(cards): b = b.replace("@@CARD%d@@" % (i + 1), card(im, w, h))
        html = "<!doctype html><html><head><meta charset='utf-8'><link href='https://fonts.googleapis.com/css2?family=Radio+Canada:wght@500;600;700&display=swap' rel='stylesheet'><style>" + CSS.replace("BG", durl(bg, 70)) + "html,body{width:%dpx;height:%dpx}</style></head><body>%s<script>document.fonts.ready.then(function(){document.title='ready'})</script></body></html>" % (W, H, b)
        f = os.path.join(HERE, name + "-v2.html"); open(f, "w", encoding="utf-8").write(html)
        cmd("Emulation.setDeviceMetricsOverride", width=W, height=H, deviceScaleFactor=2, mobile=False)
        cmd("Page.navigate", url="file:///" + f.replace("\\", "/"))
        for _ in range(60):
            time.sleep(.3)
            if cmd("Runtime.evaluate", expression="document.title", returnByValue=True)["result"].get("value") == "ready": break
        time.sleep(.6)
        png = base64.b64decode(cmd("Page.captureScreenshot", format="png")["data"])
        im = Image.open(io.BytesIO(png)).convert("RGB").resize((W, H), Image.LANCZOS)
        im.save(os.path.join(HERE, "fall-%s-v2.jpg" % name), quality=88); print(name, W, H)
finally: p.terminate()
