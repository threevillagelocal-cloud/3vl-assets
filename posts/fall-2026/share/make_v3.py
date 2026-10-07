"""Fall guide IG post + story v3 (owner 10/6/2026: real photo of Setauket, 3VL logo, no blur).
Photo = owner's own drone footage (Desktop/drone/0424 (2).mp4, frame 220: Setauket Presbyterian Church on the Village Green,
Setauket Harbor behind). Logo = blue/white version C. Yellow only on the small link pill."""
import base64, json, subprocess, time, urllib.request, websocket, os, io, cv2
from PIL import Image, ImageEnhance
HERE = os.path.dirname(os.path.abspath(__file__))
import sys
VER = sys.argv[1] if len(sys.argv) > 1 else "v3"
SRC = {"v3": (r"C:\Users\Matt\Desktop\drone\0424 (2).mp4", 220, "Setauket Village Green"),
       "v3b": (r"C:\Users\Matt\Desktop\drone\videos\0404 (2)(1).mp4", 2556, "Stony Brook Harbor"),
       "v4": (r"C:\Users\Matt\Documents\3vl-private\spotlight-photos\29564275.jpg", 0, "")}[VER]
if SRC[0].lower().endswith(".jpg"):   # still photo (v4: owner 10/6 "hayrides in a pumpkin patch scene", Pexels 29564275, free license)
    photo = Image.open(SRC[0]).convert("RGB")
else:
    c = cv2.VideoCapture(SRC[0]); c.set(cv2.CAP_PROP_POS_FRAMES, SRC[1]); ok, fr = c.read()
    photo = Image.fromarray(cv2.cvtColor(fr, cv2.COLOR_BGR2RGB))
photo = ImageEnhance.Color(photo).enhance(1.12); photo = ImageEnhance.Contrast(photo).enhance(1.05)
LOGO = r"C:\Users\Matt\Desktop\3VL logo - blue and white\C - white star, navy background.png"
def durl(im, fmt="JPEG", q=88):
    b = io.BytesIO(); (im.convert("RGB") if fmt == "JPEG" else im).save(b, fmt, quality=q); return "data:image/%s;base64," % fmt.lower() + base64.b64encode(b.getvalue()).decode()
def crop(im, w, h, cx=.46, cy=.5):
    W, H = im.size; r = w / h
    if W / H > r: nw = int(H * r); x = int(min(max(W * cx - nw / 2, 0), W - nw)); im = im.crop((x, 0, x + nw, H))
    else: nh = int(W / r); y = int(min(max(H * cy - nh / 2, 0), H - nh)); im = im.crop((0, y, W, y + nh))
    return im.resize((w * 2, h * 2), Image.LANCZOS)
lg = Image.open(LOGO).convert("RGBA"); lg.thumbnail((240, 240)); mask = Image.new("L", lg.size, 0)
from PIL import ImageDraw; ImageDraw.Draw(mask).ellipse((0, 0, lg.size[0] - 1, lg.size[1] - 1), fill=255); lg.putalpha(mask); LG = durl(lg, "PNG")
CSS = """*{box-sizing:border-box;margin:0;padding:0}html,body{overflow:hidden;font-family:'Radio Canada',sans-serif;color:#fff}
.c{position:relative;overflow:hidden;background:#13294b center/cover}
.sh{position:absolute;inset:0}
.lk{position:absolute;display:flex;align-items:center;gap:16px}.lk img{border-radius:50%;box-shadow:0 8px 22px rgba(0,0,0,.4)}
.lk b{display:block;font-weight:700;letter-spacing:-.01em}.lk span{display:block;color:#cfe0f5;letter-spacing:.14em;text-transform:uppercase}
h1{font-weight:700;letter-spacing:-.035em;line-height:.95;text-shadow:0 4px 24px rgba(0,0,0,.5)}h1 span{display:block;color:#8ec5ff}
.sub{font-weight:600;color:#fff;text-shadow:0 3px 14px rgba(0,0,0,.6)}
.pill{display:inline-block;font-weight:700;padding:12px 26px;border-radius:999px;background:#ffc53d;color:#13233a;box-shadow:0 10px 26px rgba(0,0,0,.3)}
.cr{position:absolute;color:rgba(255,255,255,.85);font-weight:600;text-shadow:0 2px 8px rgba(0,0,0,.6)}"""
T = {
 "ig": (1080, 1350, .46, """<div class="c" style="width:1080px;height:1350px;background-image:url(@@BG@@)"><div class="sh" style="background:linear-gradient(180deg,rgba(13,31,58,.82) 0%,rgba(13,31,58,.45) 30%,rgba(13,31,58,0) 52%,rgba(13,31,58,0) 70%,rgba(13,31,58,.8) 100%)"></div>
<div class="lk" style="left:64px;top:56px"><img src="@@LG@@" width="86" height="86"><div><b style="font-size:36px">Three Village Local</b><span style="font-size:18px">Your neighbors in business</span></div></div>
<h1 style="position:absolute;left:64px;right:64px;top:200px;font-size:118px">Fall in Three Village<span style="font-size:68px;margin-top:16px">Pumpkins, hayrides &amp; festivals</span></h1>
@@CRDIV1@@
<div style="position:absolute;left:64px;right:64px;bottom:70px;display:flex;justify-content:space-between;align-items:center">
<div class="sub" style="font-size:40px">30+ fall picks near home</div><span class="pill" style="font-size:34px">Link in bio &rarr;</span></div></div>"""),
 "story": (1080, 1920, .46, """<div class="c" style="width:1080px;height:1920px;background-image:url(@@BG@@)"><div class="sh" style="background:linear-gradient(180deg,rgba(13,31,58,.82) 0%,rgba(13,31,58,.4) 28%,rgba(13,31,58,0) 46%,rgba(13,31,58,0) 70%,rgba(13,31,58,.85) 100%)"></div>
<div class="lk" style="left:80px;top:240px"><img src="@@LG@@" width="100" height="100"><div><b style="font-size:42px">Three Village Local</b><span style="font-size:20px">Your neighbors in business</span></div></div>
<h1 style="position:absolute;left:80px;right:80px;top:410px;font-size:140px">Fall in Three Village<span style="font-size:80px;margin-top:20px">Pumpkins, hayrides &amp; festivals</span></h1>
@@CRDIV2@@
<div style="position:absolute;left:80px;right:80px;bottom:300px;text-align:center"><div class="sub" style="font-size:46px;margin-bottom:28px">30+ fall picks near home</div><span class="pill" style="font-size:42px">Tap the link for the full guide</span></div></div>"""),
}
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
p = subprocess.Popen([CHROME, "--headless=new", "--disable-gpu", "--remote-debugging-port=9394", "--remote-allow-origins=http://127.0.0.1:9394", "--user-data-dir=C:/Users/Matt/AppData/Local/Temp/claude-chrome-profile-fall3", "--hide-scrollbars", "about:blank"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(40):
        try: pg = [t for t in json.load(urllib.request.urlopen("http://127.0.0.1:9394/json")) if t["type"] == "page"][0]; break
        except Exception: time.sleep(.25)
    ws = websocket.create_connection(pg["webSocketDebuggerUrl"], timeout=120); n = [0]
    def cmd(m, **pa):
        n[0] += 1; ws.send(json.dumps({"id": n[0], "method": m, "params": pa}))
        while True:
            r = json.loads(ws.recv())
            if r.get("id") == n[0]: return r.get("result", {})
    cmd("Page.enable")
    for k, (w, h, cx, body) in T.items():
        html = ("<html><head><meta charset=utf-8><link href='https://fonts.googleapis.com/css2?family=Radio+Canada:wght@500;600;700&display=swap' rel=stylesheet><style>" + CSS + "</style></head><body>"
                + body.replace("@@LG@@", LG).replace("@@CRDIV1@@", ('<div class="cr" style="right:30px;top:640px;font-size:20px">' + SRC[2] + " &middot; 3VL drone</div>") if SRC[2] else "").replace("@@CRDIV2@@", ('<div class="cr" style="right:40px;top:1180px;font-size:24px">' + SRC[2] + " &middot; 3VL drone</div>") if SRC[2] else "").replace("@@BG@@", durl(crop(photo, w, h, cx))) + "<script>document.fonts.ready.then(function(){document.title='ready'})</script></body></html>")
        fn = os.path.join(HERE, k + "-" + VER + ".html"); open(fn, "w", encoding="utf-8").write(html)
        cmd("Emulation.setDeviceMetricsOverride", width=w, height=h, deviceScaleFactor=2, mobile=False)
        cmd("Page.navigate", url="file:///" + fn.replace("\\", "/"))
        for _ in range(80):
            if cmd("Runtime.evaluate", expression="document.title", returnByValue=True)["result"].get("value") == "ready": break
            time.sleep(.25)
        time.sleep(.6)
        r = cmd("Page.captureScreenshot", format="png")
        Image.open(io.BytesIO(base64.b64decode(r["data"]))).convert("RGB").resize((w, h), Image.LANCZOS).save(os.path.join(HERE, "fall-%s-%s.jpg" % (k, VER)), quality=90)
        print("done", k)
finally: p.terminate()
