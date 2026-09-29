import json,subprocess,time,urllib.request,websocket,base64
CH=r"C:\Program Files\Google\Chrome\Application\chrome.exe"
p=subprocess.Popen([CH,"--headless=new","--hide-scrollbars","--remote-debugging-port=9407","--remote-allow-origins=http://127.0.0.1:9407","--user-data-dir=C:/Users/Matt/AppData/Local/Temp/claude-chrome-profile-flyer3","about:blank"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
try:
    for _ in range(40):
        try: pg=[t for t in json.load(urllib.request.urlopen("http://127.0.0.1:9407/json")) if t["type"]=="page"][0];break
        except Exception: time.sleep(.25)
    ws=websocket.create_connection(pg["webSocketDebuggerUrl"],timeout=90);i=[0]
    def cmd(m,**pa):
        i[0]+=1;ws.send(json.dumps({"id":i[0],"method":m,"params":pa}))
        while True:
            r=json.loads(ws.recv())
            if r.get("id")==i[0]: return r.get("result",{})
    for name,url,w,h,y,mob in [("d_home","https://www.threevillagelocal.com/",1440,900,0,False),
                          ("d_spot","https://www.threevillagelocal.com/blog/fall-season-spotlight-roseland-school-of-dance-kicks-off-classes-this-week",1280,860,0,False),
                          ("m_spot","https://www.threevillagelocal.com/blog/fall-season-spotlight-roseland-school-of-dance-kicks-off-classes-this-week",390,844,0,True)]:
        cmd("Emulation.setDeviceMetricsOverride",width=w,height=h,deviceScaleFactor=2,mobile=mob)
        cmd("Page.navigate",url=url);time.sleep(10)
        cmd("Runtime.evaluate",expression="window.scrollTo(0,%d);[].forEach.call(document.querySelectorAll('body *'),function(e){var c=getComputedStyle(e);if(c.position==='fixed'){var b=e.getBoundingClientRect();if(b.top>200)e.style.display='none'}})"%y);time.sleep(2)
        open(name+".png","wb").write(base64.b64decode(cmd("Page.captureScreenshot",format="png")["data"]));print(name)
finally: p.terminate()
