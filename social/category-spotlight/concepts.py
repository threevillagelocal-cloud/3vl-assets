"""Two fun 'uncle' directions for the category spotlight (Restaurants sample), IG 4:5. Output out/concept-A.jpg, out/concept-B.jpg."""
import base64, io, json, os, subprocess, time, urllib.request, websocket
from PIL import Image, ImageEnhance
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "out")
PJ = r"C:\Users\Matt\Documents\3vl-private\members\pj-lobster-house"
idx = json.load(open(os.path.join(PJ, "ig", "index.json"), encoding="utf-8"))
def ig(i): return os.path.join(PJ, "ig", idx[i]["file"].split("/", 1)[1])
def durl(path_or_im, w=1200, h=None, q=86, pop=1.25):
    im = path_or_im if isinstance(path_or_im, Image.Image) else Image.open(path_or_im)
    im = im.convert("RGB")
    if h:
        W, H = im.size; r = w / h
        if W / H > r: nw = int(H * r); im = im.crop(((W - nw) // 2, 0, (W - nw) // 2 + nw, H))
        else: nh = int(W / r); im = im.crop((0, (H - nh) // 2, W, (H - nh) // 2 + nh))
        im = im.resize((w, h), Image.LANCZOS)
    im = ImageEnhance.Color(im).enhance(pop); im = ImageEnhance.Contrast(im).enhance(1.05)
    b = io.BytesIO(); im.save(b, "JPEG", quality=q); return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
IDX = {str(m["id"]): m for m in json.load(urllib.request.urlopen("https://raw.githubusercontent.com/threevillagelocal-cloud/3vl-assets/master/search/index.json"))["members"]}
def logo(uid):
    if str(uid) == "664": im = Image.open(os.path.join(PJ, "logo.webp")).convert("RGBA")
    else:
        u = IDX[str(uid)]["l"]; im = Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})).read())).convert("RGBA")
    bg = Image.new("RGB", im.size, "white"); bg.paste(im, mask=im.split()[3]); bg.thumbnail((360, 360))
    b = io.BytesIO(); bg.save(b, "JPEG", quality=90); return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
LOGOS = "".join('<div class="lg" style="background-image:url(%s)"></div>' % logo(i) for i in (292, 664, 31, 25, 46))
FONT = "<link href='https://fonts.googleapis.com/css2?family=Radio+Canada:wght@500;600;700&family=Permanent+Marker&display=swap' rel='stylesheet'>"
BASE = """*{box-sizing:border-box;margin:0;padding:0}html,body{width:1080px;height:1350px;overflow:hidden;font-family:'Radio Canada',sans-serif}
.stk{position:absolute;display:grid;place-items:center;border-radius:50%;background:#fff;box-shadow:0 12px 28px rgba(0,0,0,.28);font-size:76px}
.lg{width:150px;height:150px;border-radius:22px;background:#fff center/contain no-repeat;box-shadow:0 8px 20px rgba(0,0,0,.18);border:6px solid #fff}
.cta{display:inline-block;font-weight:700;font-size:34px;padding:16px 34px;border-radius:999px;background:#ffc53d;color:#13233a;box-shadow:0 10px 24px rgba(0,0,0,.2)}"""
A = """<div style="position:absolute;inset:0;background:url(@@P1@@) center/cover"></div>
<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,0) 55%,rgba(0,0,0,.45) 100%)"></div>
<div style="position:absolute;left:60px;top:60px;right:200px;background:#fff;border-radius:34px;padding:38px 44px;box-shadow:0 22px 50px rgba(0,0,0,.3)">
<div style="font-family:'Permanent Marker',cursive;font-size:44px;color:#1f5fae;transform:rotate(-2deg);margin-bottom:6px">Hey neighbor,</div>
<div style="font-weight:700;font-size:118px;line-height:.92;color:#13233a;letter-spacing:-.03em">Hungry?</div>
<div style="font-weight:700;font-size:46px;line-height:1.12;color:#13233a;margin-top:14px">65 local spots that'll treat you like family.</div></div>
<div class="stk" style="right:60px;top:90px;width:150px;height:150px;transform:rotate(12deg)">&#129438;</div>
<div class="stk" style="right:120px;top:300px;width:120px;height:120px;transform:rotate(-10deg);font-size:62px">&#127829;</div>
<div class="stk" style="left:70px;top:640px;width:130px;height:130px;transform:rotate(-14deg);font-size:66px">&#127828;</div>
<div style="position:absolute;left:40px;right:40px;bottom:40px;background:#fff;border-radius:30px;padding:24px 28px;box-shadow:0 18px 40px rgba(0,0,0,.3)">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px"><b style="font-size:30px;color:#13233a">Your neighbors on Three Village Local</b><span class="cta" style="font-size:28px;padding:12px 24px">Link in bio</span></div>
<div style="display:flex;justify-content:space-between">@@LOGOS@@</div></div>"""
B = """<div style="position:absolute;inset:0;background:#fffaf2"></div>
<div style="position:absolute;inset:0;background:radial-gradient(circle at 85% 8%,rgba(31,95,174,.12) 0,rgba(31,95,174,0) 40%),radial-gradient(circle at 5% 95%,rgba(255,197,61,.18) 0,rgba(255,197,61,0) 40%)"></div>
<div style="position:absolute;left:64px;right:64px;top:64px">
<div style="font-family:'Permanent Marker',cursive;font-size:46px;color:#1f5fae;transform:rotate(-2deg)">Hey neighbor, you hungry?</div>
<div style="font-weight:700;font-size:104px;line-height:.95;color:#13233a;letter-spacing:-.03em;margin-top:14px">Eat like a <span style="background:linear-gradient(180deg,transparent 58%,#ffd76a 58%,#ffd76a 92%,transparent 92%);padding:0 6px">local</span>.</div>
<div style="font-weight:600;font-size:40px;color:#3c4556;margin-top:16px">65 Three Village spots, from lobster to waffles.</div></div>
<div style="position:absolute;left:64px;top:560px;width:560px;height:420px;border-radius:28px;background:url(@@P1@@) center/cover;border:12px solid #fff;box-shadow:0 22px 46px rgba(0,0,0,.2)"></div>
<div style="position:absolute;right:64px;top:520px;width:340px;height:250px;border-radius:24px;background:url(@@P2@@) center/cover;border:10px solid #fff;box-shadow:0 18px 40px rgba(0,0,0,.2)"></div>
<div style="position:absolute;right:64px;top:800px;width:340px;height:250px;border-radius:24px;background:url(@@P3@@) center/cover;border:10px solid #fff;box-shadow:0 18px 40px rgba(0,0,0,.2)"></div>
<div class="stk" style="left:560px;top:500px;width:130px;height:130px;transform:rotate(12deg);font-size:68px">&#129438;</div>
<div class="stk" style="left:40px;top:930px;width:110px;height:110px;transform:rotate(-12deg);font-size:56px">&#127860;</div>
<div style="position:absolute;left:64px;right:64px;bottom:56px;display:flex;justify-content:space-between;align-items:center">@@LOGOS@@</div>
<div style="position:absolute;right:64px;bottom:250px"><span class="cta">See them all &rarr; link in bio</span></div>"""
P1, P2, P3 = durl(ig(1), 1080, 1350), durl(ig(10), 680, 500), durl(ig(4), 680, 500)
P1b = durl(ig(1), 1120, 840)
pages = {"A": A.replace("@@P1@@", P1), "B": B.replace("@@P1@@", P1b).replace("@@P2@@", P2).replace("@@P3@@", P3)}
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
p = subprocess.Popen([CHROME, "--headless=new", "--disable-gpu", "--remote-debugging-port=9384", "--remote-allow-origins=http://127.0.0.1:9384", "--user-data-dir=C:/Users/Matt/AppData/Local/Temp/claude-chrome-profile-concepts", "--hide-scrollbars", "about:blank"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(40):
        try: pg = [t for t in json.load(urllib.request.urlopen("http://127.0.0.1:9384/json")) if t["type"] == "page"][0]; break
        except Exception: time.sleep(.25)
    ws = websocket.create_connection(pg["webSocketDebuggerUrl"], timeout=180); n = [0]
    def cmd(m, **pa):
        n[0] += 1; ws.send(json.dumps({"id": n[0], "method": m, "params": pa}))
        while True:
            r = json.loads(ws.recv())
            if r.get("id") == n[0]: return r.get("result", {})
    cmd("Page.enable"); cmd("Emulation.setDeviceMetricsOverride", width=1080, height=1350, deviceScaleFactor=1, mobile=False)
    for k, body in pages.items():
        html = "<!doctype html><html><head><meta charset='utf-8'>" + FONT + "<style>" + BASE + "</style></head><body>" + body.replace("@@LOGOS@@", LOGOS) + "<script>document.fonts.ready.then(function(){setTimeout(function(){document.title='ready'},300)})</script></body></html>"
        f = os.path.join(OUT, "_c%s.html" % k); open(f, "w", encoding="utf-8").write(html)
        cmd("Page.navigate", url="file:///" + f.replace("\\", "/"))
        for _ in range(80):
            time.sleep(.3)
            if cmd("Runtime.evaluate", expression="document.title", returnByValue=True)["result"].get("value") == "ready": break
        Image.open(io.BytesIO(base64.b64decode(cmd("Page.captureScreenshot", format="png")["data"]))).convert("RGB").save(os.path.join(OUT, "concept-%s.jpg" % k), quality=88)
        os.remove(f); print(k)
finally: p.terminate()
