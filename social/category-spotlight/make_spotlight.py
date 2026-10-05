"""Category spotlight graphics - LOCKED STYLE (owner approved the restaurant version 10/4/2026, "this is the style to use
for all categories"): blurred busy scene of the industry with people, marker "Hey neighbor, ..." line, bold headline
"The best <X> in Three Village are right here." with a yellow underline, three vivid photos on white cards each with a
town pin (Setauket / Stony Brook / Port Jeff), yellow CTA. Photos: Pexels (free license, no credit), kept in
Documents/3vl-private/spotlight-photos/<pexels id>.jpg.
Usage: python make_spotlight.py [slug ...]  -> out/<slug>-ig.jpg (1080x1350), -story.jpg (1080x1920), -og.jpg (2400x1260)"""
import base64, io, json, os, subprocess, sys, time, urllib.request, websocket
from PIL import Image, ImageEnhance, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "out"); os.makedirs(OUT, exist_ok=True)
PH = r"C:\Users\Matt\Documents\3vl-private\spotlight-photos"
TOWNS = ["Setauket", "Stony Brook", "Port Jeff"]
CATS = [  # slug, marker line, headline before "right here.", count, background photo, three photos
 ("restaurant", "Hey neighbor, hungry?", "The best restaurants in Three Village are", 65, "pex-room", ["pex-paella", "pex-pancakes", "pex-spaghetti"]),
 ("real-estate-services", "Hey neighbor, thinking of moving?", "The best local agents in Three Village are", 38, "7415063", ["8364960", "8470803", "34134899"]),
 ("home-services", "Hey neighbor, need a hand?", "The best home pros in Three Village are", 34, "5767799", ["4030055", "3999647", "36884223"]),
 ("medical-services", "Hey neighbor, feeling under the weather?", "The best local doctors in Three Village are", 22, "7579823", ["7578806", "14235198", "4506073"]),
 ("financial-services", "Hey neighbor, got big plans?", "The best money pros in Three Village are", 13, "8441812", ["29094497", "7680748", "7477711"]),
 ("attorney", "Hey neighbor, need some advice?", "The best local lawyers in Three Village are", 8, "7876197", ["8112160", "261621", "6077326"]),
 ("beauty-personal-care", "Hey neighbor, treat yourself!", "The best salons &amp; spas in Three Village are", 12, "5368632", ["14615063", "9335961", "9992819"]),
 ("shopping", "Hey neighbor, shop local!", "The best shops in Three Village are", 19, "8311880", ["8386663", "18699670", "9658801"]),
 ("fitness-sports", "Hey neighbor, let's get moving!", "The best gyms &amp; teams in Three Village are", 17, "11183203", ["38116744", "8436610", "31012869"]),
 ("education", "Hey neighbor, never stop learning!", "The best tutors &amp; classes in Three Village are", 12, "5212340", ["5311406", "5635577", "8501533"]),
]
def enc(im, q=88):
    b = io.BytesIO(); im.convert("RGB").save(b, "JPEG", quality=q); return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
def photo(pid): return Image.open(os.path.join(PH, pid + ".jpg")).convert("RGB")
def fit(pid, w, h, pop=1.18):
    im = photo(pid); W, H = im.size; r = w / h
    if W / H > r: nw = int(H * r); im = im.crop(((W - nw) // 2, 0, (W - nw) // 2 + nw, H))
    else: nh = int(W / r); im = im.crop((0, (H - nh) // 2, W, (H - nh) // 2 + nh))
    im = ImageEnhance.Color(im.resize((w, h), Image.LANCZOS)).enhance(pop).filter(ImageFilter.UnsharpMask(radius=1.6, percent=55, threshold=2))
    return enc(ImageEnhance.Contrast(im).enhance(1.05))
def bg(pid, w, h):
    im = photo(pid); Wb, Hb = im.size; r = w / h
    if Wb / Hb > r: nw = int(Hb * r); im = im.crop(((Wb - nw) // 2, 0, (Wb - nw) // 2 + nw, Hb))
    else: nh = int(Wb / r); im = im.crop((0, (Hb - nh) // 2, Wb, (Hb - nh) // 2 + nh))
    im = ImageEnhance.Color(im.resize((w, h), Image.LANCZOS)).enhance(1.15).filter(ImageFilter.GaussianBlur(w / 130))
    return enc(im, 80)
CSS = """*{box-sizing:border-box;margin:0;padding:0}html,body{overflow:hidden;font-family:'Radio Canada',sans-serif;color:#fff}
.bg{position:absolute;inset:0;background:center/cover}
.sh{position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,14,10,.55) 0%,rgba(20,14,10,.08) 42%,rgba(20,14,10,.4) 100%)}
.hey{font-family:'Permanent Marker',cursive;color:#ffd76a;transform:rotate(-2deg);text-shadow:0 3px 10px rgba(0,0,0,.45)}
h1{font-weight:700;letter-spacing:-.025em;line-height:.98;text-shadow:0 5px 26px rgba(0,0,0,.55)}
h1 u{text-decoration:none;background:linear-gradient(180deg,transparent 62%,rgba(255,197,61,.9) 62%,rgba(255,197,61,.9) 90%,transparent 90%)}
.card{position:absolute;border-radius:26px;background:#fff;padding:12px;box-shadow:0 24px 50px rgba(0,0,0,.45)}
.card .ph{position:relative;border-radius:18px;background:center/cover}
.loc{position:absolute;left:12px;bottom:12px;font-weight:700;color:#13233a;background:#fff;padding:7px 14px 7px 10px;border-radius:999px;box-shadow:0 6px 16px rgba(0,0,0,.3)}
.cta{display:inline-block;font-weight:700;padding:16px 32px;border-radius:999px;background:#ffc53d;color:#13233a;box-shadow:0 12px 28px rgba(0,0,0,.35)}"""
def card(pid, town, x, y, w, ph, fs):
    return ('<div class="card" style="left:%dpx;top:%dpx;width:%dpx"><div class="ph" style="height:%dpx;background-image:url(%s)">'
            '<span class="loc" style="font-size:%dpx">&#128205; %s</span></div></div>') % (x, y, w, ph, fit(pid, (w - 24) * 2, ph * 2), fs, town)
def layouts(c):
    slug, hey, head, n, bgp, ph = c
    H = '%s <u>right here.</u>' % head
    return {
     "ig": (1080, 1350, """<div class="bg" style="background-image:url(%s)"></div><div class="sh"></div>
<div style="position:absolute;left:64px;right:64px;top:58px"><div class="hey" style="font-size:44px">%s</div><h1 style="font-size:94px;margin-top:12px">%s</h1></div>
%s%s%s<div style="position:absolute;left:0;right:0;bottom:56px;text-align:center"><span class="cta" style="font-size:36px">See all %d &rarr; link in bio</span></div>""" % (
        bg(bgp, 1080, 1350), hey, H, card(ph[0], TOWNS[0], 48, 500, 478, 318, 27), card(ph[1], TOWNS[1], 554, 500, 478, 318, 27), card(ph[2], TOWNS[2], 250, 860, 580, 330, 27), n)),
     "story": (1080, 1920, """<div class="bg" style="background-image:url(%s)"></div><div class="sh"></div>
<div style="position:absolute;left:70px;right:70px;top:170px"><div class="hey" style="font-size:52px">%s</div><h1 style="font-size:112px;margin-top:16px">%s</h1></div>
%s%s%s<div style="position:absolute;left:0;right:0;bottom:110px;text-align:center"><span class="cta" style="font-size:42px">Tap the link to see all %d</span></div>""" % (
        bg(bgp, 1080, 1920), hey, H, card(ph[0], TOWNS[0], 60, 780, 465, 310, 34), card(ph[1], TOWNS[1], 555, 780, 465, 310, 34), card(ph[2], TOWNS[2], 230, 1150, 620, 400, 34), n)),
     "og": (1200, 630, """<div class="bg" style="background-image:url(%s)"></div><div class="sh" style="background:linear-gradient(90deg,rgba(20,14,10,.78) 0%%,rgba(20,14,10,.45) 50%%,rgba(20,14,10,.2) 100%%)"></div>
<div style="position:absolute;left:56px;top:0;bottom:0;width:560px;display:flex;flex-direction:column;justify-content:center"><div class="hey" style="font-size:34px">%s</div><h1 style="font-size:66px;margin-top:10px">%s</h1></div>
%s%s""" % (bg(bgp, 1200, 630), hey, H, card(ph[0], TOWNS[0], 640, 60, 250, 190, 21), card(ph[1], TOWNS[1], 905, 150, 250, 190, 21))),
    }
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
p = subprocess.Popen([CHROME, "--headless=new", "--disable-gpu", "--remote-debugging-port=9386", "--remote-allow-origins=http://127.0.0.1:9386", "--user-data-dir=C:/Users/Matt/AppData/Local/Temp/claude-chrome-profile-spot", "--hide-scrollbars", "about:blank"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(40):
        try: pg = [t for t in json.load(urllib.request.urlopen("http://127.0.0.1:9386/json")) if t["type"] == "page"][0]; break
        except Exception: time.sleep(.25)
    ws = websocket.create_connection(pg["webSocketDebuggerUrl"], timeout=180); k = [0]
    def cmd(m, **pa):
        k[0] += 1; ws.send(json.dumps({"id": k[0], "method": m, "params": pa}))
        while True:
            r = json.loads(ws.recv())
            if r.get("id") == k[0]: return r.get("result", {})
    cmd("Page.enable")
    for c in CATS:
        if sys.argv[1:] and c[0] not in sys.argv[1:]: continue
        for name, (Wd, Hd, body) in layouts(c).items():
            html = ("<!doctype html><html><head><meta charset='utf-8'><link href='https://fonts.googleapis.com/css2?family=Radio+Canada:wght@500;600;700&family=Permanent+Marker&display=swap' rel='stylesheet'><style>"
                    + CSS + "html,body{width:%dpx;height:%dpx}</style></head><body>%s<script>document.fonts.ready.then(function(){setTimeout(function(){document.title='ready'},300)})</script></body></html>" % (Wd, Hd, body))
            fp = os.path.join(OUT, "_s-%s.html" % name); open(fp, "w", encoding="utf-8").write(html)
            cmd("Emulation.setDeviceMetricsOverride", width=Wd, height=Hd, deviceScaleFactor=2, mobile=False)
            cmd("Page.navigate", url="file:///" + fp.replace("\\", "/"))
            for _ in range(80):
                time.sleep(.3)
                if cmd("Runtime.evaluate", expression="document.title", returnByValue=True)["result"].get("value") == "ready": break
            im = Image.open(io.BytesIO(base64.b64decode(cmd("Page.captureScreenshot", format="png")["data"]))).convert("RGB")
            (im if name == "og" else im.resize((Wd, Hd), Image.LANCZOS)).save(os.path.join(OUT, "%s-%s.jpg" % (c[0], name)), quality=90)
            os.remove(fp)
        print("done", c[0])
finally: p.terminate()
