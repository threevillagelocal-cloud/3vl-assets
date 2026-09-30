"""Category page share images (9/30/2026): same approved premium style as the listing images, plus a hook question
and a 2x2 grid of real member photos from that category. -> out_cat/<filename>-v1.jpg (2400x1260)
Usage: python catgen.py [filename ...]   (no args = everything in CATS)"""
import base64, io, json, os, sys, time, subprocess, urllib.request, html
import websocket
from PIL import Image
import gen

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out_cat"); os.makedirs(OUT, exist_ok=True)

# filename: (profession_id, pill, hook line 1, gold line)
CATS = {  # only categories with 10+ businesses (owner 9/30)
    "restaurant": ("4", "&#127869;&#65039; Local Restaurants", "Looking for a new dinner spot?", "Eat local in Three Village"),
    "real-estate-services": ("31", "&#127969; Real Estate", "Thinking about a move?", "Agents who know the area"),
    "home-services": ("27", "&#127968; Home Services", "Need a pro for the house?", "Local help you can trust"),
    "medical-services": ("21", "&#129658; Doctors &amp; Medical", "Need a new doctor?", "Local care close to home"),
    "shopping": ("29", "&#128717;&#65039; Shop Local", "Looking for the perfect gift?", "Local shops you&rsquo;ll love"),
    "fitness-sports": ("43", "&#128170; Sports &amp; Fitness", "Ready to get moving?", "Gyms, classes &amp; sports"),
    "financial-services": ("20", "&#128188; Financial Services", "Need help with your money?", "Local advisors &amp; tax pros"),
    "education": ("19", "&#127891; Education", "Need a tutor or a class?", "Learning for all ages"),
    "beauty-personal-care": ("35", "&#128135; Beauty &amp; Personal Care", "Time for a fresh look?", "Local salons &amp; spas"),
    "automotive": ("28", "&#128663; Automotive", "Car need some love?", "Local shops you can trust"),
    "health-wellness": ("34", "&#127807; Health &amp; Wellness", "Time to feel your best?", "Local wellness near you"),
}

CSS = gen.CSS + """
.head{width:640px}
h1{font-size:76px;line-height:1.0;letter-spacing:-.03em;margin-top:22px;text-wrap:balance}
h1 span{font-size:50px;margin-top:14px;line-height:1.05}
.sub{font-size:34px;margin-top:24px}
.grid{position:absolute;right:56px;top:75px;width:480px;height:480px;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:16px}
.grid div{border-radius:22px;background:#fff center/cover no-repeat;box-shadow:0 22px 44px rgba(0,0,0,.55),0 0 0 2px rgba(255,255,255,.18)}
.grid div.logo{background-size:contain;background-origin:content-box;padding:18px}
"""


def picks(pid, n=4):
    ms = [m for m in json.load(open(os.path.join(HERE, "members.json"), encoding="utf-8")) if str(m["profession_id"]) == pid and str(m["user_id"]) not in gen.EXCLUDE]
    ms.sort(key=lambda m: (str(m["subscription_id"]) not in gen.VIP, -(float(m.get("rating") or 0))))  # VIPs first
    photos, logos = [], []
    for m in ms:
        mode, uri, bgc = gen.prep(m)
        if mode == "photo":
            photos.append((uri, None))
        elif mode in ("logo", "fit") and uri:
            logos.append((uri, bgc or "#fff"))
        if len(photos) >= n:
            break
    return (photos + logos)[:n]


def page(fn):
    pid, pill, hook, gold = CATS[fn]
    tiles = "".join('<div%s style="background-image:url(%s)%s"></div>' % (' class="logo"' if bg else "", u, (";background-color:" + bg) if bg else "") for u, bg in picks(pid))
    return """<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Radio+Canada:wght@500;600;700&display=swap" rel="stylesheet"><style>%s</style></head><body>
<div class="ad"><div class="bg" style="background-image:url(%s)"></div><div class="vig"></div>
<div class="head"><span class="pill">%s</span><h1>%s<span>%s</span></h1><div class="sub">On Three Village Local</div></div>
<div class="grid">%s</div></div><script>document.fonts.ready.then(function(){document.title="ready"})</script></body></html>""" % (CSS, gen.BG, pill, html.escape(hook), gold, tiles)


def main():
    fns = sys.argv[1:] or list(CATS)
    chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    p = subprocess.Popen([chrome, "--headless=new", "--disable-gpu", "--remote-debugging-port=9350", "--remote-allow-origins=http://127.0.0.1:9350",
                          "--user-data-dir=C:/Users/Matt/AppData/Local/Temp/claude-chrome-profile-catgen", "--hide-scrollbars", "about:blank"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(60):
            try:
                pg = [t for t in json.load(urllib.request.urlopen("http://127.0.0.1:9350/json")) if t["type"] == "page"][0]; break
            except Exception:
                time.sleep(.25)
        ws = websocket.create_connection(pg["webSocketDebuggerUrl"], timeout=60); n = [0]

        def cmd(mth, **pa):
            n[0] += 1; ws.send(json.dumps({"id": n[0], "method": mth, "params": pa}))
            while True:
                r = json.loads(ws.recv())
                if r.get("id") == n[0]:
                    return r.get("result", {})
        cmd("Page.enable")
        cmd("Emulation.setDeviceMetricsOverride", width=1200, height=630, deviceScaleFactor=2, mobile=False)
        tmp = os.path.join(gen.CACHE, "_cat.html")
        for fn in fns:
            open(tmp, "w", encoding="utf-8").write(page(fn))
            cmd("Page.navigate", url="file:///" + tmp.replace("\\", "/"))
            for _ in range(80):
                time.sleep(.15)
                if cmd("Runtime.evaluate", expression="document.title", returnByValue=True).get("result", {}).get("value") == "ready":
                    break
            time.sleep(.4)
            png = base64.b64decode(cmd("Page.captureScreenshot", format="png")["data"])
            Image.open(io.BytesIO(png)).convert("RGB").save(os.path.join(OUT, fn + "-v1.jpg"), "JPEG", quality=88, optimize=True, progressive=True)
            print("ok", fn, flush=True)
    finally:
        p.terminate()


if __name__ == "__main__":
    main()
