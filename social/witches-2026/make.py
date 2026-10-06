"""Witches & Warlocks Weekend 2026 hype graphics (owner 10/5/2026: "lets hype the shit out of this").
Brand recipe (locked 10/4): blurred busy scene + marker 'Hey neighbor' line + bold white headline + vivid photo cards + small yellow CTA.
Photos: Pexels (free license, no credit) in 3vl-private/ww-photos. Facts from iloveportjeff.com/witches-and-warlocks-weekend.
Outputs ww-email.jpg (1200x680), ww-ig.jpg (1080x1350), ww-story.jpg (1080x1920). python make.py"""
import base64, io, json, os, subprocess, time, urllib.request, websocket
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
PH = r"C:\Users\Matt\Documents\3vl-private\ww-photos"


def durl(p, w, h=None, blur=0):
    im = Image.open(os.path.join(PH, p)).convert("RGB")
    if h:
        r = max(w / im.width, h / im.height)
        im = im.resize((round(im.width * r) + 1, round(im.height * r) + 1))
        x, y = (im.width - w) // 2, (im.height - h) // 2
        im = im.crop((x, y, x + w, y + h))
    if blur:
        im = im.filter(ImageFilter.GaussianBlur(blur))
    b = io.BytesIO()
    im.save(b, "JPEG", quality=86)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


BG = durl("5422773.jpg", 1400, 1600, 9)
C1, C2 = durl("9147706.jpg", 900, 900), durl("10011944.jpg", 900, 900)
CSS = """*{box-sizing:border-box;margin:0}body{font-family:'Radio Canada',sans-serif;color:#fff;overflow:hidden}
.c{position:relative;overflow:hidden;background:#0d1f3a}.bg{position:absolute;inset:-30px;background:url(@BG@) center/cover;filter:saturate(1.25) brightness(1.05)}
.sh{position:absolute;inset:0;background:linear-gradient(180deg,rgba(13,31,58,.62),rgba(13,31,58,.28) 50%,rgba(13,31,58,.5))}
.hey{font-family:'Permanent Marker',cursive;color:#ffc53d;transform:rotate(-3deg);display:inline-block}
h1{font-weight:700;line-height:.95;letter-spacing:-.03em;text-shadow:0 6px 26px rgba(0,0,0,.5)}
h1 u{text-decoration:none;background:linear-gradient(transparent 78%,#ffc53d 78%,#ffc53d 92%,transparent 92%)}
.sub{font-weight:600;color:#eaf2ff;text-shadow:0 3px 14px rgba(0,0,0,.6)}
.k{position:absolute;background:#fff center/cover;border:8px solid #fff;border-radius:24px;box-shadow:0 22px 50px rgba(0,0,0,.45)}
.pill{position:absolute;background:#fff;color:#13294b;font-weight:700;border-radius:999px;padding:8px 16px;box-shadow:0 6px 16px rgba(0,0,0,.25)}
.cta{display:inline-block;background:#ffc53d;color:#13294b;font-weight:700;border-radius:999px;box-shadow:0 10px 26px rgba(255,197,61,.35)}
.chips span{display:inline-block;background:rgba(255,255,255,.16);border:2px solid rgba(255,255,255,.4);border-radius:999px;font-weight:700;margin:0 10px 12px 0}"""
CHIPS = ('<span style="padding:%s">&#127875; Headless Horseman</span><span style="padding:%s">&#127769; Night Market</span>'
         '<span style="padding:%s">&#128375;&#65039; Thriller at dusk</span>')
T = {
    "email": (1200, 680, '<div class="c" style="width:1200px;height:680px"><div class="bg"></div><div class="sh"></div>'
              '<div style="position:absolute;left:64px;top:66px;width:660px"><span class="hey" style="font-size:40px">Hey neighbor, grab your broom!</span>'
              '<h1 style="font-size:96px;margin-top:18px">Witches &amp;<br>Warlocks <u>Weekend</u></h1>'
              '<div class="sub" style="font-size:34px;margin-top:22px">Port Jefferson &middot; Sat &amp; Sun, Oct 10-11</div>'
              '<div class="chips" style="margin-top:22px;font-size:21px">' + CHIPS % (("8px 16px",) * 3) + '</div></div>'
              '<div class="k" style="right:70px;top:56px;width:340px;height:300px;background-image:url(@C1@)"><span class="pill" style="left:14px;bottom:14px;font-size:20px">&#128205; Port Jeff</span></div>'
              '<div class="k" style="right:150px;top:376px;width:300px;height:250px;background-image:url(@C2@)"></div></div>'),
    "ig": (1080, 1350, '<div class="c" style="width:1080px;height:1350px"><div class="bg"></div><div class="sh"></div>'
           '<div style="position:absolute;left:70px;right:70px;top:80px"><span class="hey" style="font-size:48px">Hey neighbor, grab your broom!</span>'
           '<h1 style="font-size:132px;margin-top:22px">Witches &amp;<br>Warlocks <u>Weekend</u></h1>'
           '<div class="sub" style="font-size:44px;margin-top:26px">Port Jefferson &middot; Sat &amp; Sun, Oct 10-11</div></div>'
           '<div class="k" style="left:70px;top:700px;width:450px;height:420px;background-image:url(@C1@)"><span class="pill" style="left:16px;bottom:16px;font-size:26px">&#128205; Port Jeff</span></div>'
           '<div class="k" style="right:70px;top:760px;width:400px;height:360px;background-image:url(@C2@)"></div>'
           '<div style="position:absolute;left:70px;right:70px;bottom:70px;text-align:center"><span class="cta" style="font-size:38px;padding:16px 34px">Come in costume &rarr; link in bio</span></div></div>'),
    "story": (1080, 1920, '<div class="c" style="width:1080px;height:1920px"><div class="bg"></div><div class="sh"></div>'
              '<div style="position:absolute;left:80px;right:80px;top:250px"><span class="hey" style="font-size:54px">Hey neighbor, grab your broom!</span>'
              '<h1 style="font-size:150px;margin-top:26px">Witches &amp;<br>Warlocks <u>Weekend</u></h1>'
              '<div class="sub" style="font-size:50px;margin-top:30px">Port Jefferson &middot; Oct 10-11</div>'
              '<div class="chips" style="margin-top:30px;font-size:32px">' + CHIPS % (("10px 20px",) * 3) + '</div></div>'
              '<div class="k" style="left:80px;top:1090px;width:480px;height:420px;background-image:url(@C1@)"><span class="pill" style="left:16px;bottom:16px;font-size:28px">&#128205; Port Jeff</span></div>'
              '<div class="k" style="right:80px;top:1210px;width:400px;height:360px;background-image:url(@C2@)"></div>'
              '<div style="position:absolute;left:80px;right:80px;bottom:230px;text-align:center"><span class="cta" style="font-size:44px;padding:18px 36px">Tap the link for the full schedule</span></div></div>'),
}
CH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
p = subprocess.Popen([CH, "--headless=new", "--disable-gpu", "--remote-debugging-port=9377", "--remote-allow-origins=http://127.0.0.1:9377",
                      "--user-data-dir=C:/Users/Matt/AppData/Local/Temp/claude-chrome-ww", "--hide-scrollbars", "about:blank"],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(40):
        try:
            pg = [t for t in json.load(urllib.request.urlopen("http://127.0.0.1:9377/json")) if t["type"] == "page"][0]
            break
        except Exception:
            time.sleep(.25)
    ws = websocket.create_connection(pg["webSocketDebuggerUrl"], timeout=120)
    n = [0]

    def cmd(m, **pa):
        n[0] += 1
        ws.send(json.dumps({"id": n[0], "method": m, "params": pa}))
        while True:
            r = json.loads(ws.recv())
            if r.get("id") == n[0]:
                return r.get("result", {})
    cmd("Page.enable")
    for name, (W, H, body) in T.items():
        page = ("<!doctype html><html><head><meta charset='utf-8'><link href='https://fonts.googleapis.com/css2?family=Radio+Canada:wght@600;700&family=Permanent+Marker&display=swap' rel='stylesheet'>"
                "<style>" + CSS.replace("@BG@", BG) + "html,body{width:%dpx;height:%dpx}" % (W, H) + "</style></head><body>"
                + body.replace("@C1@", C1).replace("@C2@", C2)
                + "<script>document.fonts.ready.then(function(){document.title='ready'})</script></body></html>")
        f = os.path.join(HERE, name + ".html")
        open(f, "w", encoding="utf-8").write(page)
        cmd("Emulation.setDeviceMetricsOverride", width=W, height=H, deviceScaleFactor=2, mobile=False)
        cmd("Page.navigate", url="file:///" + f.replace("\\", "/"))
        for _ in range(60):
            time.sleep(.3)
            if cmd("Runtime.evaluate", expression="document.title", returnByValue=True)["result"].get("value") == "ready":
                break
        time.sleep(.8)
        im = Image.open(io.BytesIO(base64.b64decode(cmd("Page.captureScreenshot", format="png")["data"]))).convert("RGB").resize((W, H), Image.LANCZOS)
        im.save(os.path.join(HERE, "ww-%s.jpg" % name), quality=88)
        os.remove(f)
        print(name)
finally:
    p.terminate()
