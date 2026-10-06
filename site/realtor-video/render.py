import json, subprocess, time, urllib.request, websocket, base64, pathlib
D = pathlib.Path(__file__).parent
SHARE = pathlib.Path(r"C:\Users\Matt\Documents\3vl-share")
PAGES = "https://threevillagelocal-cloud.github.io/3vl-share/"
css = (D / "page.css").read_text(encoding="utf-8")
html = (D / "page.html").read_text(encoding="utf-8")
doc = ("<html><head><meta name=viewport content='width=device-width,initial-scale=1'>"
       "<link href='https://fonts.googleapis.com/css2?family=Radio+Canada:wght@400;600;700;800&display=swap' rel=stylesheet>"
       "<style>body{margin:0;background:#f4f6f8}.wrap{padding:24px 16px}" + css + "</style></head><body><div class=wrap>" + html + "</div></body></html>")
# use local copies of files not pushed yet
for f in ["site/realtor-video/house-1600.webp", "site/realtor-video/house-900.webp"]:
    doc = doc.replace(PAGES + f, (SHARE / f).as_uri())
(D / "preview.html").write_text(doc, encoding="utf-8")

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
p = subprocess.Popen([CHROME, "--headless=new", "--disable-gpu", "--remote-debugging-port=9378", "--remote-allow-origins=http://127.0.0.1:9378",
                      "--allow-file-access-from-files", "--user-data-dir=C:/Users/Matt/AppData/Local/Temp/claude-chrome-profile-rv", "about:blank"],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(40):
        try:
            pg = [t for t in json.load(urllib.request.urlopen("http://127.0.0.1:9378/json")) if t["type"] == "page"][0]; break
        except Exception:
            time.sleep(.25)
    ws = websocket.create_connection(pg["webSocketDebuggerUrl"], timeout=120); n = [0]
    def cmd(m, **pa):
        n[0] += 1; ws.send(json.dumps({"id": n[0], "method": m, "params": pa}))
        while True:
            r = json.loads(ws.recv())
            if r.get("id") == n[0]: return r.get("result", {})
    cmd("Page.enable")
    for name, w, h, mob in [("computer", 1200, 900, False), ("phone", 412, 900, True)]:
        cmd("Emulation.setDeviceMetricsOverride", width=w, height=h, deviceScaleFactor=2 if mob else 1, mobile=mob)
        cmd("Page.navigate", url=(D / "preview.html").as_uri()); time.sleep(4)
        full = cmd("Runtime.evaluate", expression="document.documentElement.scrollHeight", returnByValue=True)["result"]["value"]
        r = cmd("Page.captureScreenshot", format="jpeg", quality=82, captureBeyondViewport=True,
                clip={"x": 0, "y": 0, "width": w, "height": full, "scale": 1})
        (D / f"pv-{name}.jpg").write_bytes(base64.b64decode(r["data"]))
        print(name, full)
finally:
    p.terminate()
