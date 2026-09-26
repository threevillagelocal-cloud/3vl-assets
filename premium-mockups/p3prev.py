"""Load a live 3VL page in a private headless Chrome, inject the new calendar (not published), screenshot desktop+phone."""
import base64, json, subprocess, sys, time, urllib.request, websocket
URL, OUT, MODE, W, H, MOB = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6] == "1"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
A = "C:/Users/Matt/AppData/Local/Temp/claude/C--Users-Matt/9198bbd2-d524-49ae-b687-c350243c81b5/scratchpad/premium/"
css = open(A + "p3.css", encoding="utf-8").read(); js = open(A + "p3.js", encoding="utf-8").read()
meta = "{}"
p = subprocess.Popen([CHROME, "--headless=new", "--disable-gpu", "--remote-debugging-port=9336", "--remote-allow-origins=http://127.0.0.1:9336",
                      "--user-data-dir=C:/Users/Matt/AppData/Local/Temp/claude-chrome-profile-p3prev", "--hide-scrollbars", "about:blank"],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(40):
        try:
            page = [t for t in json.load(urllib.request.urlopen("http://127.0.0.1:9336/json")) if t["type"] == "page"][0]; break
        except Exception:
            time.sleep(0.25)
    ws = websocket.create_connection(page["webSocketDebuggerUrl"], timeout=60); n = [0]
    def cmd(m, **pa):
        n[0] += 1; ws.send(json.dumps({"id": n[0], "method": m, "params": pa}))
        while True:
            r = json.loads(ws.recv())
            if r.get("id") == n[0]: return r.get("result", {})
    cmd("Emulation.setDeviceMetricsOverride", width=W, height=H, deviceScaleFactor=1 if not MOB else 2, mobile=MOB)
    cmd("Page.enable"); cmd("Page.navigate", url=URL); time.sleep(7)
    inj = """(function(){var s=document.createElement('style');s.textContent=%s;document.head.appendChild(s);var x=document.createElement('script');x.textContent=%s;document.body.appendChild(x)})()""" % (json.dumps(css), json.dumps(js))
    r = cmd("Runtime.evaluate", expression=inj); time.sleep(5)
    if r.get("exceptionDetails"): print("ERR", r["exceptionDetails"])
    h = cmd("Runtime.evaluate", expression="document.documentElement.scrollHeight", returnByValue=True)["result"]["value"]
    y = 0; i = 0
    while y < min(h, H * 3) and i < 3:
        cmd("Runtime.evaluate", expression="window.scrollTo(0,%d)" % y); time.sleep(1.5)
        open("%s_%d.jpg" % (OUT, i), "wb").write(base64.b64decode(cmd("Page.captureScreenshot", format="jpeg", quality=78)["data"])); y += H; i += 1
    print(h, i)
finally:
    p.terminate()
