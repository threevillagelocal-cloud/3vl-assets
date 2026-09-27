import json, subprocess, time, urllib.request, websocket, base64, io, pathlib
from PIL import Image
H=pathlib.Path(__file__).resolve().parent
p = subprocess.Popen([r"C:\Program Files\Google\Chrome\Application\chrome.exe", "--headless=new", "--disable-gpu",
  "--remote-debugging-port=9372", "--remote-allow-origins=http://127.0.0.1:9372",
  "--user-data-dir=C:/Users/Matt/AppData/Local/Temp/claude-chrome-profile-ad", "about:blank"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(40):
        try: page=[t for t in json.load(urllib.request.urlopen("http://127.0.0.1:9372/json")) if t["type"]=="page"][0]; break
        except Exception: time.sleep(.25)
    ws=websocket.create_connection(page["webSocketDebuggerUrl"],timeout=60); n=[0]
    def cmd(m,**pa):
        n[0]+=1; ws.send(json.dumps({"id":n[0],"method":m,"params":pa}))
        while True:
            r=json.loads(ws.recv())
            if r.get("id")==n[0]: return r.get("result",{})
    cmd("Page.enable")
    import sys
    for name,W,Hh in [tuple([a.split(":")[0]]+[int(x) for x in a.split(":")[1:]]) for a in sys.argv[1:]]:
        cmd("Emulation.setDeviceMetricsOverride", width=W, height=Hh, deviceScaleFactor=1, mobile=False)
        cmd("Page.navigate",url=(H/(name+".html")).as_uri()); time.sleep(3)
        d=cmd("Page.captureScreenshot",format="png",clip={"x":0,"y":0,"width":W,"height":Hh,"scale":1})
        im=Image.open(io.BytesIO(base64.b64decode(d["data"]))).convert("RGB")
        im.save(H/(name+".jpg"),quality=92,subsampling=0); print(name,im.size)
finally: p.terminate()
