"""Visuals for the /newsletter sign-up page and its social posts (10/3/2026).
A real weekly email (weekender/email/<edition>/email.html) is shown on a phone over the blurred village photo.
    python site/newsletter/visuals.py [edition]
writes ../3vl-share/site/newsletter/: phone.webp (transparent, for the page), hero-bg.jpg (page hero background),
og.jpg (1200x630 share image), ig-post.jpg (1080x1350), ig-story.jpg (1080x1920). Throwaway Chrome profile."""
import base64, io, json, os, subprocess, sys, tempfile, time, urllib.request
import websocket
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(os.path.dirname(ASSETS), "3vl-share", "site", "newsletter")
PHOTO = "file:///" + os.path.join(ASSETS, "site", "p3", "img", "village-hero.jpg").replace("\\", "/")
PORT = 9421
FONT = "<link href='https://fonts.googleapis.com/css2?family=Radio+Canada:wght@400;600;700;800&display=block' rel='stylesheet'>"

PHONE_CSS = """.ph{position:relative;width:%(w)dpx;height:%(h)dpx;border-radius:%(r)dpx;background:#0b0d10;padding:%(b)dpx;box-sizing:border-box;
 box-shadow:0 0 0 2px #2a2f36,0 30px 70px rgba(0,0,0,.5),0 0 90px rgba(242,169,59,.16)}
.ph .scr{width:100%%;height:100%%;border-radius:%(ri)dpx;overflow:hidden;background:#eef2f6 url('%(shot)s') top center/100%% auto no-repeat}
.ph:before{content:"";position:absolute;top:%(nt)dpx;left:50%%;transform:translateX(-50%%);width:%(nw)dpx;height:%(nh)dpx;border-radius:99px;background:#0b0d10;z-index:2}"""


def phone_css(w, shot):
    h = int(w * 2.05)
    return PHONE_CSS % {"w": w, "h": h, "r": int(w * .15), "b": int(w * .035), "ri": int(w * .12), "shot": shot,
                        "nt": int(w * .055), "nw": int(w * .3), "nh": int(w * .075)}


def page(w, h, inner, extra_css=""):
    return ("<!doctype html><html><head><meta charset='utf-8'>%s<style>html,body{margin:0;width:%dpx;height:%dpx;overflow:hidden;background:#0f1f31;font-family:'Radio Canada',sans-serif}"
            ".bg{position:absolute;inset:-24px;background:url('%s') center 60%%/cover;filter:blur(10px) saturate(.9) brightness(.62)}"
            ".shade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(10,22,36,.92) 0%%,rgba(10,22,36,.75) 45%%,rgba(10,22,36,.35) 100%%)}"
            "h1{margin:0;color:#fff;font-weight:800;letter-spacing:-.5px;line-height:1.04}h1 span{color:#f2a93b;display:block}"
            ".sub{color:#e8eef5;font-weight:600}.pill{display:inline-block;border-radius:999px;font-weight:800}"
            ".glass{background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.28);color:#fff}.gold{background:#f2a93b;color:#1b2f45}"
            "%s</style></head><body><div class='bg'></div><div class='shade'></div>%s</body></html>") % (FONT, w, h, PHOTO, extra_css, inner)


def main():
    ed = sys.argv[1] if len(sys.argv) > 1 else sorted(x for x in os.listdir(os.path.join(ASSETS, "weekender", "email")) if x[:2] == "20")[-1]
    email = os.path.join(ASSETS, "weekender", "email", ed, "email.html")
    os.makedirs(OUT, exist_ok=True)
    prof = tempfile.mkdtemp(prefix="nlvis-")
    p = subprocess.Popen([r"C:\Program Files\Google\Chrome\Application\chrome.exe", "--headless=new", "--disable-gpu", "--hide-scrollbars", "--remote-debugging-port=%d" % PORT,
                          "--remote-allow-origins=http://127.0.0.1:%d" % PORT, "--allow-file-access-from-files", "--user-data-dir=" + prof, "about:blank"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(80):
            try:
                pg = [t for t in json.load(urllib.request.urlopen("http://127.0.0.1:%d/json" % PORT)) if t["type"] == "page"][0]; break
            except Exception:
                time.sleep(.25)
        ws = websocket.create_connection(pg["webSocketDebuggerUrl"], timeout=120); n = [0]

        def cmd(m, **pa):
            n[0] += 1; i = n[0]; ws.send(json.dumps({"id": i, "method": m, "params": pa}))
            while True:
                r = json.loads(ws.recv())
                if r.get("id") == i:
                    return r.get("result", {})

        def snap(w, h, html, fn, fmt="jpeg", transparent=False, q=84):
            f = os.path.join(tempfile.gettempdir(), "nl_%s.html" % fn.split(".")[0])
            open(f, "w", encoding="utf-8").write(html)
            if transparent:
                cmd("Emulation.setDefaultBackgroundColorOverride", color={"r": 0, "g": 0, "b": 0, "a": 0})
            cmd("Emulation.setDeviceMetricsOverride", width=w, height=h, deviceScaleFactor=2 if transparent else 1, mobile=False)
            cmd("Page.navigate", url="file:///" + f.replace("\\", "/")); time.sleep(3.5)
            d = cmd("Page.captureScreenshot", format="png")
            im = Image.open(io.BytesIO(base64.b64decode(d["data"])))
            out = os.path.join(OUT, fn)
            if fn.endswith(".webp"):
                im.save(out, "WEBP", quality=82, method=6)
            else:
                im.convert("RGB").save(out, "JPEG", quality=q, optimize=True, progressive=True)
            if transparent:
                cmd("Emulation.clearDefaultBackgroundColorOverride")
            print(fn, im.size, os.path.getsize(out) // 1024, "KB")

        # 1. the real email at phone width (top part)
        cmd("Emulation.setDeviceMetricsOverride", width=390, height=800, deviceScaleFactor=2, mobile=True)
        cmd("Page.navigate", url="file:///" + email.replace("\\", "/")); time.sleep(8)
        d = cmd("Page.captureScreenshot", format="png", captureBeyondViewport=True, clip={"x": 0, "y": 0, "width": 390, "height": 1560, "scale": 1})
        shot = os.path.join(tempfile.gettempdir(), "nl_email.png")
        open(shot, "wb").write(base64.b64decode(d["data"]))
        S = "file:///" + shot.replace("\\", "/")
        # 2. phone on its own (page)
        snap(360, 700, "<!doctype html><html><head><style>html,body{margin:0;background:transparent}" + phone_css(300, S) + ".ph{margin:30px}</style></head><body><div class='ph'><div class='scr'></div></div></body></html>",
             "phone.webp", transparent=True)
        # 3. page hero background (no text, no phone)
        snap(1600, 700, page(1600, 700, ""), "hero-bg.jpg", q=72)
        # 4. share image 1200x630
        snap(1200, 630, page(1200, 630,
             "<div style='position:absolute;left:70px;top:150px;width:640px'><span class='pill glass' style='font-size:24px;padding:10px 22px'>&#9993;&#65039; Free weekly email</span>"
             "<h1 style='font-size:70px;margin-top:26px'>The best of<br>Three Village<span>in your inbox</span></h1>"
             "<p class='sub' style='font-size:30px;margin:22px 0 0;text-wrap:balance'>Events, food specials and local news.<br>Every week, free.</p></div>"
             "<div class='ph' style='position:absolute;right:90px;top:40px;transform:rotate(0deg)'><div class='scr'></div></div>", phone_css(330, S)), "og.jpg")
        # 5. Instagram post 1080x1350
        snap(1080, 1350, page(1080, 1350,
             "<div style='position:absolute;left:0;right:0;top:86px;text-align:center'><span class='pill glass' style='font-size:30px;padding:12px 28px'>&#9993;&#65039; Free weekly email</span>"
             "<h1 style='font-size:86px;margin-top:30px'>Never miss a weekend<span>in Three Village</span></h1></div>"
             "<div class='ph' style='position:absolute;left:50%;top:470px;transform:translateX(-50%)'><div class='scr'></div></div>"
             "<div style='position:absolute;left:0;right:0;bottom:70px;text-align:center'><span class='pill gold' style='font-size:38px;padding:20px 44px'>Sign up free &middot; link in bio</span></div>",
             phone_css(330, S) + ".ph{height:640px!important}"), "ig-post.jpg")
        # 6. Instagram story 1080x1920
        snap(1080, 1920, page(1080, 1920,
             "<div style='position:absolute;left:0;right:0;top:250px;text-align:center'><span class='pill glass' style='font-size:34px;padding:14px 32px'>&#9993;&#65039; Free weekly email</span>"
             "<h1 style='font-size:100px;margin-top:36px'>The best of<br>Three Village<span>every week</span></h1>"
             "<p class='sub' style='font-size:40px;margin:30px 60px 0'>Events, food specials and local news<br>in one short email.</p></div>"
             "<div class='ph' style='position:absolute;left:50%;top:930px;transform:translateX(-50%)'><div class='scr'></div></div>"
             "<div style='position:absolute;left:0;right:0;bottom:120px;text-align:center'><span class='pill gold' style='font-size:44px;padding:22px 50px'>Tap the link to sign up &darr;</span></div>",
             phone_css(420, S) + ".ph{height:760px!important}"), "ig-story.jpg")
    finally:
        p.terminate()


if __name__ == "__main__":
    main()
