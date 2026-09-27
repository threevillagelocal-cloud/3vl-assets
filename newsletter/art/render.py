"""Render the Member Insider header art: hero.jpg (static) and stats.gif (glass tiles with a light-shine sweep).
   python render.py   (needs local Chrome; uses its own --user-data-dir)"""
import json, subprocess, time, urllib.request, websocket, base64, io, pathlib
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / "img"
p = subprocess.Popen([r"C:\Program Files\Google\Chrome\Application\chrome.exe", "--headless=new", "--disable-gpu",
                      "--remote-debugging-port=9371", "--remote-allow-origins=http://127.0.0.1:9371",
                      "--user-data-dir=C:/Users/Matt/AppData/Local/Temp/claude-chrome-profile-art", "about:blank"],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(40):
        try:
            page = [t for t in json.load(urllib.request.urlopen("http://127.0.0.1:9371/json")) if t["type"] == "page"][0]; break
        except Exception:
            time.sleep(.25)
    ws = websocket.create_connection(page["webSocketDebuggerUrl"], timeout=60); n = [0]
    def cmd(m, **pa):
        n[0] += 1; ws.send(json.dumps({"id": n[0], "method": m, "params": pa}))
        while True:
            r = json.loads(ws.recv())
            if r.get("id") == n[0]: return r.get("result", {})
    def ev(js): return cmd("Runtime.evaluate", expression=js, returnByValue=True).get("result", {}).get("value")
    def shot(sel):
        b = ev("(function(){var r=document.querySelector('%s').getBoundingClientRect();return [r.x,r.y,r.width,r.height]})()" % sel)
        d = cmd("Page.captureScreenshot", format="png", clip={"x": b[0], "y": b[1], "width": b[2], "height": b[3], "scale": 1})
        return Image.open(io.BytesIO(base64.b64decode(d["data"]))).convert("RGB")
    cmd("Page.enable")

    cmd("Emulation.setDeviceMetricsOverride", width=1200, height=700, deviceScaleFactor=1, mobile=False)
    cmd("Page.navigate", url=(HERE / "hero.html").as_uri()); time.sleep(3)
    hero = shot("#mast")
    hero.save(OUT / "hero.jpg", quality=90, subsampling=0, optimize=True)
    print("hero.jpg", hero.size, (OUT / "hero.jpg").stat().st_size)

    cmd("Emulation.setDeviceMetricsOverride", width=1080, height=600, deviceScaleFactor=1, mobile=False)
    cmd("Page.navigate", url=(HERE / "stats.html").as_uri()); time.sleep(3)
    frames, durs = [], []
    first = shot("#stats"); frames.append(first); durs.append(2600)
    STEPS, STAGGER = 14, 3
    for f in range(STEPS + STAGGER * 3):
        xs = []
        for i in range(4):
            k = min(max(f - i * STAGGER, 0), STEPS) / STEPS
            xs.append(-120 + 240 * k)
        ev("(function(){var s=document.querySelectorAll('.shine');%s})()" % ";".join("s[%d].style.setProperty('--x','%.1f%%')" % (i, x) for i, x in enumerate(xs)))
        frames.append(shot("#stats")); durs.append(60)
    ev("document.querySelectorAll('.shine').forEach(function(s){s.style.setProperty('--x','-120%')})")
    pal = frames[0].quantize(colors=255, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    q = [fr.quantize(palette=pal, dither=Image.Dither.NONE) for fr in frames]
    q[0].save(OUT / "stats.gif", save_all=True, append_images=q[1:], duration=durs, loop=0, optimize=True, disposal=1)
    first.save(OUT / "stats-first.png")
    print("stats.gif", first.size, len(frames), (OUT / "stats.gif").stat().st_size)
finally:
    p.terminate()
