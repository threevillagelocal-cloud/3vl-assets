"""Hero art for /smart-publisher (owner 10/3/2026: no plain navy box; show a finished article on an iPad over a subtle
tech background that still feels like the local North Shore community hub).
    python site/smart-publisher/hero_build.py
1. screenshots a real, finished 3VL article page at iPad size
2. renders hero.html (Stony Brook Village photo + faint grid/network lines + the iPad) in headless Chrome
writes ../3vl-share/site/smart-publisher/hero-wide.jpg (desktop, iPad on the right), hero-bg.jpg (no iPad, phones), ipad.png"""
import base64, io, json, os, subprocess, tempfile, time, urllib.request
import websocket
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(os.path.dirname(ASSETS), "3vl-share", "site", "smart-publisher")
# a generic sample event on the iPad (sample/event.html), not a real event or business
ARTICLE = "file:///" + os.path.join(HERE, "sample", "event.html").replace("\\", "/")
PHOTO = os.path.join(ASSETS, "site", "p3", "img", "village-hero.jpg")

HTML = """<!doctype html><html><head><meta charset="utf-8"><style>
html,body{margin:0;width:%(w)dpx;height:%(h)dpx;overflow:hidden;background:#0f1f31}
.bg{position:absolute;inset:-20px;background:url('%(photo)s') center 60%%/cover;filter:blur(3px) saturate(.9) brightness(.62)}
.shade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(10,22,36,.94) 0%%,rgba(10,22,36,.82) 38%%,rgba(10,22,36,.35) 70%%,rgba(10,22,36,.25) 100%%)}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.055) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.055) 1px,transparent 1px);background-size:56px 56px;
 -webkit-mask-image:linear-gradient(90deg,transparent 20%%,#000 60%%,#000 100%%)}
svg{position:absolute;inset:0}
.ipad{position:absolute;right:%(r)dpx;top:50%%;transform:translateY(-50%%) perspective(1800px) rotateY(-14deg) rotateX(3deg);width:%(iw)dpx;height:%(ih)dpx;border-radius:46px;background:#0b0d10;
 padding:22px;box-sizing:border-box;box-shadow:0 0 0 2px #2a2f36,0 40px 90px rgba(0,0,0,.55),0 0 120px rgba(242,169,59,.18)}
.ipad .scr{width:100%%;height:100%%;border-radius:26px;overflow:hidden;background:#fff url('%(shot)s') top center/cover}
.ipad:after{content:"";position:absolute;inset:22px;border-radius:26px;background:linear-gradient(120deg,rgba(255,255,255,.16),transparent 35%%)}
</style></head><body><div class="bg"></div><div class="shade"></div><div class="grid"></div>
<svg viewBox="0 0 %(w)d %(h)d"><g stroke="rgba(242,169,59,.35)" stroke-width="1.6" fill="none">%(lines)s</g><g fill="rgba(255,214,140,.9)">%(dots)s</g></svg>
%(ipad)s</body></html>"""


def network(w, h):
    pts = [(.6, .22), (.64, .4), (.59, .6), (.655, .76), (.55, .45)]   # a small, quiet network leading into the iPad
    P = [(int(x * w), int(y * h)) for x, y in pts]
    pairs = [(0, 1), (1, 2), (2, 3), (4, 1), (4, 2)]
    lines = "".join('<line x1="%d" y1="%d" x2="%d" y2="%d"/>' % (P[a] + P[b]) for a, b in pairs)
    dots = "".join('<circle cx="%d" cy="%d" r="%d"/>' % (x, y, 4 if i % 2 else 3) for i, (x, y) in enumerate(P))
    return lines, dots


def main():
    os.makedirs(OUT, exist_ok=True)
    prof = tempfile.mkdtemp(prefix="sphero-")
    p = subprocess.Popen([r"C:\Program Files\Google\Chrome\Application\chrome.exe", "--headless=new", "--disable-gpu", "--hide-scrollbars", "--remote-debugging-port=9387",
                          "--remote-allow-origins=http://127.0.0.1:9387", "--allow-file-access-from-files", "--user-data-dir=" + prof, "about:blank"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(80):
            try:
                pg = [t for t in json.load(urllib.request.urlopen("http://127.0.0.1:9387/json")) if t["type"] == "page"][0]; break
            except Exception:
                time.sleep(.25)
        ws = websocket.create_connection(pg["webSocketDebuggerUrl"], timeout=90); n = [0]

        def cmd(m, **pa):
            n[0] += 1; i = n[0]; ws.send(json.dumps({"id": i, "method": m, "params": pa}))
            while True:
                r = json.loads(ws.recv())
                if r.get("id") == i:
                    return r.get("result", {})
        cmd("Page.enable")
        # 1. the finished article, at iPad size (portrait 834 wide)
        cmd("Emulation.setDeviceMetricsOverride", width=834, height=1112, deviceScaleFactor=2, mobile=True)
        cmd("Page.navigate", url=ARTICLE, referrer="https://www.google.com/"); time.sleep(10)
        cmd("Runtime.evaluate", expression="window.scrollTo(0,0)"); time.sleep(1)
        d = cmd("Page.captureScreenshot", format="jpeg", quality=88)
        shot = os.path.join(tempfile.gettempdir(), "sp_article.jpg")
        open(shot, "wb").write(base64.b64decode(d["data"]))
        # 2. composites
        for name, w, h, with_ipad in (("hero-wide", 1960, 900, True), ("hero-bg", 900, 1100, False)):
            lines, dots = network(w, h)
            iw = 520; ih = int(iw * 1112 / 834) + 0
            ipad = '<div class="ipad"><div class="scr"></div></div>' if with_ipad else ""
            html = HTML % {"w": w, "h": h, "photo": "file:///" + PHOTO.replace("\\", "/"), "shot": "file:///" + shot.replace("\\", "/"),
                           "lines": lines if with_ipad else "", "dots": dots if with_ipad else "", "ipad": ipad, "r": 150, "iw": iw, "ih": min(ih, h - 110)}
            f = os.path.join(tempfile.gettempdir(), "sp_%s.html" % name)
            open(f, "w", encoding="utf-8").write(html)
            cmd("Emulation.setDeviceMetricsOverride", width=w, height=h, deviceScaleFactor=1, mobile=False)
            cmd("Page.navigate", url="file:///" + f.replace("\\", "/")); time.sleep(2.5)
            d = cmd("Page.captureScreenshot", format="jpeg", quality=82)
            im = Image.open(io.BytesIO(base64.b64decode(d["data"]))).convert("RGB")
            im.save(os.path.join(OUT, name + ".jpg"), "JPEG", quality=80, optimize=True, progressive=True)
            print(name, os.path.getsize(os.path.join(OUT, name + ".jpg")) // 1024, "KB")
        # 3. phone version of the iPad on its own (transparent), for under the heading on small screens
        f = os.path.join(tempfile.gettempdir(), "sp_ipad.html")
        open(f, "w", encoding="utf-8").write(
            '<!doctype html><html><head><style>html,body{margin:0;background:transparent}.ipad{margin:30px;width:420px;height:%dpx;border-radius:40px;background:#0b0d10;padding:18px;box-sizing:border-box;'
            'box-shadow:0 0 0 2px #2a2f36,0 24px 50px rgba(0,0,0,.35)}.scr{width:100%%;height:100%%;border-radius:24px;background:#fff url(\'%s\') top center/cover}</style></head>'
            '<body><div class="ipad"><div class="scr"></div></div></body></html>' % (int(420 * 1112 / 834 * .62), "file:///" + shot.replace("\\", "/")))
        cmd("Emulation.setDefaultBackgroundColorOverride", color={"r": 0, "g": 0, "b": 0, "a": 0})
        cmd("Emulation.setDeviceMetricsOverride", width=480, height=int(420 * 1112 / 834 * .62) + 60, deviceScaleFactor=2, mobile=False)
        cmd("Page.navigate", url="file:///" + f.replace("\\", "/")); time.sleep(2)
        d = cmd("Page.captureScreenshot", format="png")
        Image.open(io.BytesIO(base64.b64decode(d["data"]))).save(os.path.join(OUT, "ipad.webp"), "WEBP", quality=80, method=6)
        print("ipad.webp", os.path.getsize(os.path.join(OUT, "ipad.webp")) // 1024, "KB")
    finally:
        p.terminate()


if __name__ == "__main__":
    main()
