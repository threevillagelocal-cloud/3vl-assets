import base64, json, subprocess, time, urllib.request, websocket, os
S="C:/Users/Matt/Documents/3vl-share/spyday-2026/"
def u(f): return "data:image/webp;base64,"+base64.b64encode(open(S+f,"rb").read()).decode()
H="""<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Radio+Canada:wght@500;600;700&family=Special+Elite&display=swap" rel="stylesheet"><style>
*{box-sizing:border-box;margin:0;padding:0}html,body{width:1200px;height:630px;overflow:hidden;background:#0c1018;font-family:'Radio Canada',sans-serif;color:#fff}
.c{position:relative;width:1200px;height:630px;overflow:hidden}
.bg{position:absolute;inset:-40px;background:url(BG) center/cover;filter:blur(10px) saturate(1.1) brightness(.9)}
.vig{position:absolute;inset:0;background:linear-gradient(90deg,rgba(8,12,20,.9) 0%,rgba(8,12,20,.7) 50%,rgba(8,12,20,.35) 100%),linear-gradient(0deg,rgba(8,12,20,.5),rgba(8,12,20,0) 50%)}
.scan{position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(255,255,255,.03) 0 1px,transparent 1px 4px)}
.head{position:absolute;left:62px;top:0;bottom:0;width:600px;display:flex;flex-direction:column;justify-content:center}
.pill{align-self:flex-start;font-weight:700;font-size:28px;letter-spacing:.06em;padding:10px 22px;border-radius:999px;background:linear-gradient(180deg,#ffd76a,#ffc53d);color:#13233a;box-shadow:0 10px 26px rgba(255,197,61,.35)}
h1{white-space:nowrap;font-size:84px;font-weight:700;letter-spacing:-.035em;line-height:.95;margin-top:26px}
h1 span{display:block;white-space:normal;color:#ffc53d;font-size:66px;line-height:1.02;margin-top:12px;width:560px}
.sub{margin-top:26px;font-size:38px;font-weight:600;color:#eef3f8}
.card{position:absolute;right:62px;top:92px;width:430px;height:450px;border-radius:28px;background:url(CARD) center 30%/cover;box-shadow:0 30px 60px rgba(0,0,0,.6),0 0 0 6px #ffc53d,0 0 40px rgba(255,197,61,.4)}
.stamp{position:absolute;right:92px;top:58px;font-family:'Special Elite',monospace;font-size:40px;letter-spacing:.12em;color:#e0453d;border:5px solid #e0453d;border-radius:10px;padding:6px 18px;background:rgba(20,12,12,.55);transform:rotate(-9deg);z-index:3}
.code{position:absolute;right:92px;bottom:118px;z-index:3;font-family:'Special Elite',monospace;font-size:30px;background:#13233a;color:#ffc53d;border:2px solid #ffc53d;border-radius:12px;padding:8px 16px}
</style></head><body><div class="c"><div class="bg"></div><div class="vig"></div><div class="scan"></div>
<div class="head"><span class="pill">SAT, OCT 3 &middot; FREE</span><h1>Culper Spy Day<span>The Ultimate Blueprint</span></h1><div class="sub">Setauket &amp; Stony Brook</div></div>
<div class="card"></div><div class="stamp">TOP SECRET</div><div class="code">711 &middot; 729</div></div>
<script>document.fonts.ready.then(function(){document.title="ready"})</script></body></html>"""
H=H.replace("BG",u("caroline-fog.webp")).replace("CARD",u("spyday.webp"))
open("share.html","w",encoding="utf-8").write(H)
CHROME=r"C:\Program Files\Google\Chrome\Application\chrome.exe"
p=subprocess.Popen([CHROME,"--headless=new","--disable-gpu","--remote-debugging-port=9364","--remote-allow-origins=http://127.0.0.1:9364","--user-data-dir=C:/Users/Matt/AppData/Local/Temp/claude-chrome-profile-spyshare","--hide-scrollbars","about:blank"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
try:
    for _ in range(40):
        try: pg=[t for t in json.load(urllib.request.urlopen("http://127.0.0.1:9364/json")) if t["type"]=="page"][0]; break
        except Exception: time.sleep(.25)
    ws=websocket.create_connection(pg["webSocketDebuggerUrl"],timeout=120); n=[0]
    def cmd(m,**pa):
        n[0]+=1; ws.send(json.dumps({"id":n[0],"method":m,"params":pa}))
        while True:
            r=json.loads(ws.recv())
            if r.get("id")==n[0]: return r.get("result",{})
    cmd("Page.enable"); cmd("Emulation.setDeviceMetricsOverride",width=1200,height=630,deviceScaleFactor=2,mobile=False)
    cmd("Page.navigate",url="file:///"+os.path.abspath("share.html").replace("\\","/"))
    for _ in range(60):
        time.sleep(.3)
        if cmd("Runtime.evaluate",expression="document.title",returnByValue=True)["result"].get("value")=="ready": break
    time.sleep(.5)
    open("share.png","wb").write(base64.b64decode(cmd("Page.captureScreenshot",format="png")["data"]))
finally: p.terminate()
from PIL import Image
Image.open("share.png").convert("RGB").save("spyday-share.jpg",quality=88)
Image.open("share.png").convert("RGB").resize((1200,630)).save("check.jpg",quality=85)
