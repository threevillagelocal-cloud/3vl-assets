"""Build a 1200x630 share image for every listing in members.json -> out/<slug>.jpg
Approved 3VL style (9/28/2026): blurred dark village photo bg, big white name + one gold line, straight white card.
Usage: python gen.py [user_id ...]   (no ids = everyone)"""
import base64, io, json, os, re, subprocess, sys, time, urllib.request, html
import websocket
from PIL import Image, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out"); CACHE = os.path.join(HERE, "cache")
os.makedirs(OUT, exist_ok=True); os.makedirs(CACHE, exist_ok=True)
CSS = open(os.path.join(HERE, "share.css"), encoding="utf-8").read() + """
.solo .head{width:1060px}
.ad:not(.solo) .head{width:585px}
"""
VIP = {"1", "8"}
EXCLUDE = {"5", "218"}  # admin/blog-author account, Twinr (app vendor)
VISIT = {"Restaurant", "Shopping - Retail", "Beauty & Personal Care", "Sports & Fitness", "Nightlife", "Farmstand/Agriculture",
         "Pet Services", "Automotive", "Arts & Entertainment", "Hotels & Travel", "Events & Entertainment", "Health & Wellness"}


def b64(path, mime):
    return "data:%s;base64,%s" % (mime, base64.b64encode(open(path, "rb").read()).decode())


BG = b64(os.path.join(HERE, "img", "village.jpg"), "image/jpeg")


def esc(t):
    return html.escape(t or "", quote=True)


def town(c):
    c = (c or "").strip()
    return "Setauket" if c.startswith("Setauket-") else c


def slug(m):
    return re.sub(r"[^a-z0-9-]+", "-", (m["filename"] or str(m["user_id"])).lower()).strip("-")


def fetch_img(url):
    if not url or "profile-holder" in url:
        return None
    p = os.path.join(CACHE, re.sub(r"[^A-Za-z0-9._-]", "_", url.rsplit("/", 1)[-1]))
    if not os.path.exists(p):
        if subprocess.run(["curl", "-s", "-f", "-A", "Mozilla/5.0", "-o", p, url]).returncode:
            return None
    try:
        im = Image.open(p); im.load(); return im
    except Exception:
        return None


def prep(m):
    """-> (mode, data-uri); mode is 'photo', 'logo' or None"""
    ov = [os.path.join(HERE, "img", "override", "%s.%s" % (m["user_id"], e)) for e in ("png", "jpg")]
    ov = [f for f in ov if os.path.exists(f)]
    im = Image.open(ov[0]) if ov else fetch_img(m.get("image_main_file"))  # img/override/<user_id>.png|jpg = better logo/photo the owner supplied
    if im is None:
        return None, None, None
    rgba = im.convert("RGBA"); w, h = rgba.size
    flat = Image.alpha_composite(Image.new("RGBA", rgba.size, (255, 255, 255, 255)), rgba).convert("RGB")
    px = flat.load(); pts = []
    for i in range(0, w, max(1, w // 60)):
        pts += [px[i, 0], px[i, h - 1], px[i, int(h * .04)], px[i, int(h * .96)]]
    for j in range(0, h, max(1, h // 60)):
        pts += [px[0, j], px[w - 1, j], px[int(w * .04), j], px[int(w * .96), j]]
    white = sum(1 for q in pts if min(q) > 232) / len(pts)
    srt = sorted(pts, key=sum); med = srt[len(srt) // 2]
    solid = sum(1 for q in pts if max(abs(q[k] - med[k]) for k in range(3)) < 14) / len(pts)
    bgc = None
    if white > .6:
        ref, mode = (255, 255, 255), "logo"
    elif solid > .7:  # logo on a solid colour: keep it whole on a card of that colour
        ref, mode, bgc = med, "logo", "#%02x%02x%02x" % tuple(med)
    else:
        ref, mode = None, "photo"
    if ref:
        d = ImageChops.difference(flat, Image.new("RGB", flat.size, tuple(ref))).convert("L").point(lambda v: 255 if v > 26 else 0)
        bb = d.getbbox()
        if bb:
            pad = int(max(bb[2] - bb[0], bb[3] - bb[1]) * .04)
            flat = flat.crop((max(0, bb[0] - pad), max(0, bb[1] - pad), min(w, bb[2] + pad), min(h, bb[3] + pad)))
    flat.thumbnail((1400, 1400))
    buf = io.BytesIO(); flat.save(buf, "JPEG", quality=90)
    return mode, "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode(), bgc


def page(m):
    vip = str(m["subscription_id"]) in VIP
    t = town(m["city"]); cat = m.get("category") or ""
    yr = str(m.get("experience") or "").strip()
    yr = yr if re.fullmatch(r"(18|19|20)\d\d", yr) and int(yr) <= 2026 else ""
    name = (m.get("company") or " ".join(x for x in [m.get("first_name"), m.get("last_name")] if x)).strip()
    if vip:
        pill = '<span class="pill gold">&#9733; NEIGHBOR FAVORITE</span>'
    elif t:
        pill = '<span class="pill">&#128205; %s</span>' % esc(t)
    else:
        pill = ""
    if yr:
        gold = "Since " + yr
    elif vip and t:
        gold = t
    elif t and cat:
        gold = cat
    else:
        gold = t or cat or "Three Village"
    mode, uri, bgc = prep(m)
    tag = "Come visit us!" if cat in VISIT else "Your neighbors"
    if mode == "photo":
        card = '<div class="tag">%s</div><div class="card" style="background-image:url(%s)"></div>' % (tag, uri)
    elif mode == "logo":
        card = '<div class="tag">%s</div><div class="card logo"%s><img src="%s"></div>' % (tag, (' style="background:%s"' % bgc) if bgc else "", uri)
    else:
        card = ""
    stars = ('<div class="stars"><i>&#9733;&#9733;&#9733;&#9733;&#9733;</i>%.1f</div>' % m["rating"]) if (vip and m.get("rating") and card) else ""
    cls = ("vip" if vip else "basic") + ("" if card else " solo")
    fit = """document.fonts.ready.then(function(){var h=document.querySelector("h1"),n=document.querySelector(".nm"),hd=document.querySelector(".head"),W=%d,f=%d;
function tall(){var t=0;[].forEach.call(hd.children,function(c){t+=c.getBoundingClientRect().height});return t+60}
h.style.fontSize=f+"px";n.style.display="block";n.style.whiteSpace="nowrap";
while(n.scrollWidth>W&&f>%d){f-=2;h.style.fontSize=f+"px"}
if(n.scrollWidth>W){n.style.whiteSpace="normal";n.style.textWrap="balance";f=%d;h.style.fontSize=f+"px";
while((tall()>560||n.getBoundingClientRect().height>f*2.1)&&f>48){f-=2;h.style.fontSize=f+"px"}}
document.title="ready"})""" % ((580, 96, 82, 88) if card else (1060, 110, 90, 100))
    return """<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Radio+Canada:wght@500;600;700&display=swap" rel="stylesheet"><style>%s</style></head><body>
<div class="ad %s"><div class="bg" style="background-image:url(%s)"></div><div class="vig"></div>
<div class="head">%s<h1><b class="nm">%s</b><span>%s</span></h1><div class="sub">Visit us on Three Village Local</div></div>%s%s</div>
<script>%s</script></body></html>""" % (CSS, cls, BG, pill, esc(name), esc(gold), card, stars, fit)


def main():
    ms = json.load(open(os.path.join(HERE, "members.json"), encoding="utf-8"))
    ms = [m for m in ms if str(m["user_id"]) not in EXCLUDE]
    ids = set(sys.argv[1:])
    if ids:
        ms = [m for m in ms if str(m["user_id"]) in ids]
    chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    p = subprocess.Popen([chrome, "--headless=new", "--disable-gpu", "--remote-debugging-port=9349", "--remote-allow-origins=http://127.0.0.1:9349",
                          "--user-data-dir=C:/Users/Matt/AppData/Local/Temp/claude-chrome-profile-sharegen", "--hide-scrollbars", "about:blank"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(60):
            try:
                pg = [t for t in json.load(urllib.request.urlopen("http://127.0.0.1:9349/json")) if t["type"] == "page"][0]; break
            except Exception:
                time.sleep(.25)
        ws = websocket.create_connection(pg["webSocketDebuggerUrl"], timeout=60); n = [0]

        def cmd(mth, **pa):
            n[0] += 1; ws.send(json.dumps({"id": n[0], "method": mth, "params": pa}))
            while True:
                r = json.loads(ws.recv())
                if r.get("id") == n[0]:
                    return r.get("result", {})
        cmd("Page.enable")
        cmd("Emulation.setDeviceMetricsOverride", width=1200, height=630, deviceScaleFactor=2, mobile=False)
        tmp = os.path.join(CACHE, "_page.html"); done = []
        for i, m in enumerate(ms):
            open(tmp, "w", encoding="utf-8").write(page(m))
            cmd("Page.navigate", url="file:///" + tmp.replace("\\", "/"))
            for _ in range(60):
                time.sleep(.15)
                if cmd("Runtime.evaluate", expression="document.title", returnByValue=True).get("result", {}).get("value") == "ready":
                    break
            time.sleep(.25)
            png = base64.b64decode(cmd("Page.captureScreenshot", format="png")["data"])
            Image.open(io.BytesIO(png)).convert("RGB").save(os.path.join(OUT, slug(m) + ".jpg"), "JPEG", quality=88, optimize=True, progressive=True)
            done.append({"user_id": m["user_id"], "slug": slug(m)})
            if i % 25 == 0:
                print(i, slug(m), flush=True)
        if not ids:
            json.dump(done, open(os.path.join(OUT, "_index.json"), "w"), indent=0)
        print("done", len(done))
    finally:
        p.terminate()


if __name__ == "__main__":
    main()
