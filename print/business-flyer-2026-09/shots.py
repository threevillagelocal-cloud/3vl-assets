import json,subprocess,time,urllib.request,websocket,base64,sys
CH=r"C:\Program Files\Google\Chrome\Application\chrome.exe"
p=subprocess.Popen([CH,"--headless=new","--hide-scrollbars","--remote-debugging-port=9406","--remote-allow-origins=http://127.0.0.1:9406","--user-data-dir=C:/Users/Matt/AppData/Local/Temp/claude-chrome-profile-flyer","about:blank"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
try:
    for _ in range(40):
        try: pg=[t for t in json.load(urllib.request.urlopen("http://127.0.0.1:9406/json")) if t["type"]=="page"][0];break
        except Exception: time.sleep(.25)
    ws=websocket.create_connection(pg["webSocketDebuggerUrl"],timeout=90);i=[0]
    def cmd(m,**pa):
        i[0]+=1;ws.send(json.dumps({"id":i[0],"method":m,"params":pa}))
        while True:
            r=json.loads(ws.recv())
            if r.get("id")==i[0]: return r.get("result",{})
    cmd("Emulation.setDeviceMetricsOverride",width=390,height=844,deviceScaleFactor=3,mobile=True)
    for name,url,sel in [("vip","https://www.threevillagelocal.com/",'#nh-feat'),("profile","https://www.threevillagelocal.com/setauket-frame-shop",'.p3-prof,#p3prof,.profile-header,h1'),("events","https://www.threevillagelocal.com/events",'.tvc-card')]:
        cmd("Page.navigate",url=url);time.sleep(9)
        y=0
        if sel:
            y=cmd("Runtime.evaluate",expression=("(function(){var OFF={vip:150,profile:130,events:150}.NAME;var e=document.querySelector('%s');return e?Math.max(0,e.getBoundingClientRect().top+scrollY-OFF):0})()"%sel).replace("NAME",name),returnByValue=True)["result"]["value"]
        cmd("Runtime.evaluate",expression="window.scrollTo(0,%d)"%y);time.sleep(2.5)
        cmd("Runtime.evaluate",expression="[].forEach.call(document.querySelectorAll('body *'),function(e){var c=getComputedStyle(e);if(c.position==='fixed'){var b=e.getBoundingClientRect();if(b.top>300)e.style.display='none'}})")
        time.sleep(.5)
        d=cmd("Page.captureScreenshot",format="png")["data"];open(name+".png","wb").write(base64.b64decode(d));print(name,y)
finally: p.terminate()
