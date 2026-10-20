"""Restaurant category spotlight (owner direction 10/4/2026): blurred busy restaurant background, big bold headline
"The best restaurants in Three Village are right here.", real dishes from member restaurants, each tagged with the
restaurant's logo + name. Outputs out/restaurant-ig.jpg (1080x1350), -story.jpg (1080x1920), -og.jpg (2400x1260)."""
import base64, io, json, os, subprocess, time, urllib.request, websocket
from PIL import Image, ImageEnhance, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "out")
SP = r"C:\Users\Matt\AppData\Local\Temp\claude\C--Users-Matt\8cd8646e-5951-4601-a8cd-13eca8e132e2\scratchpad"
PJ = r"C:\Users\Matt\Documents\3vl-private\members\pj-lobster-house"
def j(p): return json.load(open(p, encoding="utf-8"))
rest = j(os.path.join(SP, "rest", "index.json")); fall = j(os.path.join(SP, "fall", "ig", "index.json")); pj = j(os.path.join(PJ, "ig", "index.json"))
def f(base, idx, i): return os.path.join(base, idx[i]["file"].split("/", 1)[1])
def enc(im, q=88):
    b = io.BytesIO(); im.convert("RGB").save(b, "JPEG", quality=q); return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
def fit(path, w, h, pop=1.18):
    im = Image.open(path).convert("RGB"); W, H = im.size; r = w / h
    if W / H > r: nw = int(H * r); im = im.crop(((W - nw) // 2, 0, (W - nw) // 2 + nw, H))
    else: nh = int(W / r); im = im.crop((0, (H - nh) // 2, W, (H - nh) // 2 + nh))
    im = ImageEnhance.Color(im.resize((w, h), Image.LANCZOS)).enhance(pop).filter(ImageFilter.UnsharpMask(radius=1.6, percent=55, threshold=2))
    return enc(ImageEnhance.Contrast(im).enhance(1.05))
def logo_img(im):
    im = im.convert("RGBA"); bg = Image.new("RGB", im.size, "white"); bg.paste(im, mask=im.split()[3]); bg.thumbnail((360, 360)); return enc(bg, 92)
ml = Image.open(f(os.path.join(SP, "rest"), rest, 32)); W, H = ml.size; ml = ml.crop((int(W * .05), int(H * .04), int(W * .95), int(H * .5)))
fil_logo = Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request("https://www.threevillagelocal.com/logos/profile/limage-292-75-photo.jpg", headers={"User-Agent": "Mozilla/5.0"})).read()))
DISHES = [  # owner 10/4: vibrant real dinners, no restaurant names (Pexels, free license, no credit needed)
    (os.path.join(SP, "pex", "pex-paella.jpg"), None, None, "Setauket"),
    (os.path.join(SP, "pex", "pex-pancakes.jpg"), None, None, "Stony Brook"),
    (os.path.join(SP, "pex", "pex-spaghetti.jpg"), None, None, "Port Jeff"),
]
bgsrc = Image.open(os.path.join(SP, "pex", "pex-room.jpg")).convert("RGB")   # Pexels, free license, no credit needed
def bg(w, h):
    im = bgsrc; Wb, Hb = im.size; r = w / h
    if Wb / Hb > r: nw = int(Hb * r); im = im.crop(((Wb - nw) // 2, 0, (Wb - nw) // 2 + nw, Hb))
    im = im.resize((w, int(w * im.height / im.width)) if im.height * w / im.width >= h else (int(h * im.width / im.height), h), Image.LANCZOS)
    im = ImageEnhance.Color(im).enhance(1.15).filter(ImageFilter.GaussianBlur(w / 130))
    return enc(im, 80)
CSS = """*{box-sizing:border-box;margin:0;padding:0}html,body{overflow:hidden;font-family:'Radio Canada',sans-serif;color:#fff}
.bg{position:absolute;inset:0;background:url(@@BG@@) center/cover}
.sh{position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,14,10,.55) 0%,rgba(20,14,10,.08) 42%,rgba(20,14,10,.4) 100%)}
.hey{font-family:'Permanent Marker',cursive;color:#ffd76a;transform:rotate(-2deg);text-shadow:0 3px 10px rgba(0,0,0,.45)}
h1{font-weight:700;letter-spacing:-.025em;line-height:.98;text-shadow:0 5px 26px rgba(0,0,0,.55)}
h1 u{text-decoration:none;background:linear-gradient(180deg,transparent 62%,rgba(255,197,61,.9) 62%,rgba(255,197,61,.9) 90%,transparent 90%)}
.dish{position:absolute;border-radius:26px;background:#fff;padding:12px 12px 0;box-shadow:0 24px 50px rgba(0,0,0,.45)}
.dish .ph{border-radius:18px;background:center/cover}
.dish .lg{position:absolute;border-radius:50%;background:#fff center/contain no-repeat;border:5px solid #fff;box-shadow:0 10px 24px rgba(0,0,0,.3)}
.dish .tx{color:#13233a;padding:12px 6px 14px}
.dish .tx b{display:block;font-weight:700;line-height:1.1}.dish .tx span{color:#5d6c7b;font-weight:600}
.loc{position:absolute;left:12px;bottom:12px;font-weight:700;color:#13233a;background:#fff;padding:7px 14px 7px 10px;border-radius:999px;box-shadow:0 6px 16px rgba(0,0,0,.3)}
.cta{display:inline-block;font-weight:700;padding:16px 32px;border-radius:999px;background:#ffc53d;color:#13233a;box-shadow:0 12px 28px rgba(0,0,0,.35)}"""
def dish(d, x, y, w, ph, lg, fs):
    photo, logo, name, what = d
    if not name:
        loc = ('<span class="loc" style="font-size:%dpx">&#128205; %s</span>' % (fs, what)) if what else ""
        return '<div class="dish" style="left:%dpx;top:%dpx;width:%dpx;padding-bottom:12px"><div class="ph" style="position:relative;height:%dpx;background-image:url(%s)">%s</div></div>' % (x, y, w, ph, fit(photo, (w - 24) * 2, ph * 2), loc)
    return ('<div class="dish" style="left:%dpx;top:%dpx;width:%dpx"><div class="ph" style="height:%dpx;background-image:url(%s)"></div>'
            '<div class="lg" style="width:%dpx;height:%dpx;right:-14px;top:%dpx;background-image:url(%s)"></div>'
            '<div class="tx"><b style="font-size:%dpx">%s</b><span style="font-size:%dpx">%s</span></div></div>') % (
        x, y, w, ph, fit(photo, (w - 24) * 2, ph * 2), lg, lg, ph - int(lg * .8), logo, fs, name, int(fs * .82), what)
L = {
 "ig": (1080, 1350, lambda: """<div class="bg" style="background-image:url(%s)"></div><div class="sh"></div>
<div style="position:absolute;left:64px;right:64px;top:58px"><div class="hey" style="font-size:44px">Hey neighbor, hungry?</div>
<h1 style="font-size:94px;margin-top:12px">The best restaurants in Three Village are <u>right here.</u></h1></div>
%s%s%s
<div style="position:absolute;left:0;right:0;bottom:56px;text-align:center"><span class="cta" style="font-size:36px">See all 65 &rarr; link in bio</span></div>""" % (
    bg(1080, 1350), dish(DISHES[0], 48, 500, 478, 318, 96, 27), dish(DISHES[1], 554, 500, 478, 318, 96, 27), dish(DISHES[2], 250, 860, 580, 330, 96, 27))),
 "story": (1080, 1920, lambda: """<div class="bg" style="background-image:url(%s)"></div><div class="sh"></div>
<div style="position:absolute;left:70px;right:70px;top:170px"><div class="hey" style="font-size:52px">Hey neighbor, hungry?</div>
<h1 style="font-size:112px;margin-top:16px">The best restaurants in Three Village are <u>right here.</u></h1></div>
%s%s%s
<div style="position:absolute;left:0;right:0;bottom:110px;text-align:center"><span class="cta" style="font-size:42px">Tap the link to see all 65</span></div>""" % (
    bg(1080, 1920), dish(DISHES[0], 60, 780, 465, 310, 120, 34), dish(DISHES[1], 555, 780, 465, 310, 120, 34), dish(DISHES[2], 230, 1150, 620, 400, 120, 34))),
 "og": (1200, 630, lambda: """<div class="bg" style="background-image:url(%s)"></div><div class="sh" style="background:linear-gradient(90deg,rgba(20,14,10,.78) 0%%,rgba(20,14,10,.45) 50%%,rgba(20,14,10,.2) 100%%)"></div>
<div style="position:absolute;left:56px;top:0;bottom:0;width:560px;display:flex;flex-direction:column;justify-content:center"><div class="hey" style="font-size:34px">Hey neighbor, hungry?</div>
<h1 style="font-size:66px;margin-top:10px">The best restaurants in Three Village are <u>right here.</u></h1></div>
%s%s""" % (bg(1200, 630), dish(DISHES[0], 640, 60, 250, 190, 78, 21), dish(DISHES[1], 905, 150, 250, 190, 78, 21))),
}
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
p = subprocess.Popen([CHROME, "--headless=new", "--disable-gpu", "--remote-debugging-port=9385", "--remote-allow-origins=http://127.0.0.1:9385", "--user-data-dir=C:/Users/Matt/AppData/Local/Temp/claude-chrome-profile-rest", "--hide-scrollbars", "about:blank"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(40):
        try: pg = [t for t in json.load(urllib.request.urlopen("http://127.0.0.1:9385/json")) if t["type"] == "page"][0]; break
        except Exception: time.sleep(.25)
    ws = websocket.create_connection(pg["webSocketDebuggerUrl"], timeout=180); n = [0]
    def cmd(m, **pa):
        n[0] += 1; ws.send(json.dumps({"id": n[0], "method": m, "params": pa}))
        while True:
            r = json.loads(ws.recv())
            if r.get("id") == n[0]: return r.get("result", {})
    cmd("Page.enable")
    for name, (Wd, Hd, body) in L.items():
        html = ("<!doctype html><html><head><meta charset='utf-8'><link href='https://fonts.googleapis.com/css2?family=Radio+Canada:wght@500;600;700&family=Permanent+Marker&display=swap' rel='stylesheet'><style>"
                + CSS + "html,body{width:%dpx;height:%dpx}</style></head><body>%s<script>document.fonts.ready.then(function(){setTimeout(function(){document.title='ready'},300)})</script></body></html>" % (Wd, Hd, body()))
        fp = os.path.join(OUT, "_r-%s.html" % name); open(fp, "w", encoding="utf-8").write(html)
        cmd("Emulation.setDeviceMetricsOverride", width=Wd, height=Hd, deviceScaleFactor=2, mobile=False)
        cmd("Page.navigate", url="file:///" + fp.replace("\\", "/"))
        for _ in range(80):
            time.sleep(.3)
            if cmd("Runtime.evaluate", expression="document.title", returnByValue=True)["result"].get("value") == "ready": break
        im = Image.open(io.BytesIO(base64.b64decode(cmd("Page.captureScreenshot", format="png")["data"]))).convert("RGB")
        (im if name == "og" else im.resize((Wd, Hd), Image.LANCZOS)).save(os.path.join(OUT, "restaurant-%s.jpg" % name), quality=90)
        os.remove(fp); print(name)
finally: p.terminate()
