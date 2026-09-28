import base64, json, subprocess, time, urllib.request, websocket, sys
D="C:/Users/Matt/AppData/Local/Temp/claude/C--Users-Matt/cfb4a2ce-d006-4eb8-972f-09390cdb38e8/scratchpad/og/"
def uri(f): 
    ext='png' if f.endswith('png') else 'jpeg'
    return "data:image/%s;base64,%s"%(ext,base64.b64encode(open(D+f,'rb').read()).decode())
CSS="""
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1200px;height:630px;overflow:hidden;background:#0c1018;font-family:'Radio Canada',sans-serif;color:#fff;-webkit-font-smoothing:antialiased}
.ad{position:relative;width:1200px;height:630px;overflow:hidden}
.bg{position:absolute;inset:-40px;background-position:center 60%;background-size:cover;filter:blur(9px) saturate(1.2) brightness(.95)}
.vig{position:absolute;inset:0;background:linear-gradient(90deg,rgba(8,12,20,.88) 0%,rgba(8,12,20,.6) 48%,rgba(8,12,20,.3) 100%),linear-gradient(180deg,rgba(8,12,20,.15),rgba(8,12,20,0) 40%,rgba(8,12,20,.45))}
.head{position:absolute;left:64px;top:0;bottom:0;width:620px;display:flex;flex-direction:column;justify-content:center;align-items:flex-start}
.wm{display:inline-block;background:rgba(255,255,255,.94);border-radius:18px;padding:10px 16px;box-shadow:0 10px 26px rgba(0,0,0,.35)}
.wm img{display:block;height:58px}
.pill{display:inline-flex;align-items:center;gap:10px;font-weight:700;font-size:30px;padding:9px 22px;border-radius:999px;background:rgba(255,255,255,.14);border:1.5px solid rgba(255,255,255,.35)}
.pill.gold{background:linear-gradient(180deg,#ffd76a,#ffc53d);color:#13233a;border-color:rgba(255,255,255,.5);box-shadow:0 10px 26px rgba(255,197,61,.35);letter-spacing:.08em}
h1{font-size:96px;font-weight:700;letter-spacing:-.035em;line-height:.98;margin:26px 0 0}
h1 span{display:block;color:#ffc53d;margin-top:6px}
.sub{margin-top:30px;font-size:38px;font-weight:600;color:#eef3f8}
.card{position:absolute;right:64px;top:80px;width:420px;height:470px;border-radius:28px;background:#fff center/cover;box-shadow:0 30px 60px rgba(0,0,0,.6),0 0 0 2px rgba(255,255,255,.18);overflow:hidden}
.card.logo{top:150px;height:330px;width:450px;right:64px;display:flex;align-items:center;justify-content:center;padding:36px}
.card.logo img{max-width:100%;max-height:100%}
.vip .card{box-shadow:0 30px 60px rgba(0,0,0,.6),0 0 0 6px #ffc53d,0 0 40px rgba(255,197,61,.45)}
.tag{position:absolute;z-index:5;left:710px;top:52px;padding:10px 22px;border-radius:999px;font-size:28px;font-weight:700;color:#13233a;background:#fff;box-shadow:0 12px 26px rgba(0,0,0,.4)}
.vip .tag{left:690px;top:122px}
.stars{position:absolute;z-index:5;right:90px;bottom:122px;padding:10px 22px;border-radius:16px;background:#13233a;border:2px solid #ffc53d;font-size:28px;font-weight:700;box-shadow:0 14px 30px rgba(0,0,0,.5)}
.stars i{font-style:normal;color:#ffc53d;letter-spacing:3px;margin-right:8px}
"""
def page(kind,d):
    bg='<div class="bg" style="background-image:url(%s)"></div>'%uri('village.jpg')
    card=('<div class="card" style="background-image:url(%s)"></div>'%uri(d['img'])) if d['mode']=='photo' else ('<div class="card logo"><img src="%s"></div>'%uri(d['img']))
    pill='<span class="pill gold">&#9733; NEIGHBOR FAVORITE</span>' if kind=='vip' else '<span class="pill">&#128205; %s</span>'%d['town']
    stars='<div class="stars"><i>&#9733;&#9733;&#9733;&#9733;&#9733;</i>%s</div>'%d['rating'] if d.get('rating') else ''
    return """<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Radio+Canada:wght@500;600;700&display=swap" rel="stylesheet"><style>%s</style></head><body>
<div class="ad %s">%s<div class="vig"></div>
<div class="head">%s<h1><b class="nm">%s</b><span>%s</span></h1><div class="sub">Visit us on Three Village Local</div></div>
<div class="tag">%s</div>%s%s</div>
<script>document.fonts.ready.then(function(){var n=document.querySelector(".nm"),f=96;n.style.whiteSpace="nowrap";n.style.display="block";while(n.scrollWidth>580&&f>72){f-=2;document.querySelector("h1").style.fontSize=f+"px"}if(n.scrollWidth>580){n.style.whiteSpace="normal";n.style.textWrap="balance";document.querySelector("h1").style.fontSize="88px"}})</script></body></html>"""%(CSS,kind,bg,pill,d['name'],d['gold'],d['tag'],card,stars)
jobs=[
 ("basic","sfs",dict(town="East Setauket",name="Setauket Frame Shop",gold="Since 1974",tag="Come visit us!",img="sfs.jpg",mode="photo")),
 ("vip","raupp",dict(name="Raupp Law, P.C.",gold="East Setauket",tag="Your neighbors",rating="5.0",img="raupp_hi_trim.png",mode="logo")),
]
CHROME=r"C:\Program Files\Google\Chrome\Application\chrome.exe"
p=subprocess.Popen([CHROME,"--headless=new","--disable-gpu","--remote-debugging-port=9348","--remote-allow-origins=http://127.0.0.1:9348","--user-data-dir=C:/Users/Matt/AppData/Local/Temp/claude-chrome-profile-og","--hide-scrollbars","about:blank"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
try:
    for _ in range(40):
        try: pg=[t for t in json.load(urllib.request.urlopen("http://127.0.0.1:9348/json")) if t["type"]=="page"][0]; break
        except Exception: time.sleep(0.25)
    ws=websocket.create_connection(pg["webSocketDebuggerUrl"],timeout=60); n=[0]
    def cmd(m,**pa):
        n[0]+=1; ws.send(json.dumps({"id":n[0],"method":m,"params":pa}))
        while True:
            r=json.loads(ws.recv())
            if r.get("id")==n[0]: return r.get("result",{})
    cmd("Page.enable"); cmd("Emulation.setDeviceMetricsOverride",width=1200,height=630,deviceScaleFactor=1,mobile=False)
    for kind,key,d in jobs:
        f=D+"og_%s.html"%key; open(f,"w",encoding="utf-8").write(page(kind,d))
        cmd("Page.navigate",url="file:///"+f); time.sleep(3)
        cmd("Runtime.evaluate",expression="document.fonts.ready",awaitPromise=True)
        open(D+"og_%s.png"%key,"wb").write(base64.b64decode(cmd("Page.captureScreenshot",format="png")["data"]))
        print("ok",key)
finally: p.terminate()
