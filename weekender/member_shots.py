"""Screenshots for the member update email: the new homepage (computer + phone), smart search in action,
a member listing, and the Smart Publisher page. Saves JPGs into 3vl-share/email/<name>/.
    python weekender/member_shots.py <name>
Uses a throwaway Chrome profile (never the owner's)."""
import base64, io, json, os, subprocess, sys, tempfile, time, urllib.request
import websocket
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.dirname(HERE)
SHARE = os.path.join(os.path.dirname(ASSETS), "3vl-share")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
SITE = "https://www.threevillagelocal.com"
PROFILE = SITE + "/setauket-frame-shop"
MOCKUP = "file:///" + os.path.join(ASSETS, "site", "smart-publisher", "mockup.html").replace("\\", "/")


def rounded(im, r):
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), r, fill=255)
    out = Image.new("RGBA", im.size)
    out.paste(im, (0, 0), m)
    return out


def main():
    name = sys.argv[1]
    out = os.path.join(SHARE, "email", name)
    os.makedirs(out, exist_ok=True)
    prof = tempfile.mkdtemp(prefix="membershot-")
    p = subprocess.Popen([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--remote-debugging-port=9373",
                          "--remote-allow-origins=http://127.0.0.1:9373", "--user-data-dir=" + prof, "about:blank"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(80):
            try:
                pg = [t for t in json.load(urllib.request.urlopen("http://127.0.0.1:9373/json")) if t["type"] == "page"][0]; break
            except Exception:
                time.sleep(.25)
        ws = websocket.create_connection(pg["webSocketDebuggerUrl"], timeout=90); n = [0]

        def cmd(m, **pa):
            n[0] += 1; i = n[0]; ws.send(json.dumps({"id": i, "method": m, "params": pa}))
            while True:
                r = json.loads(ws.recv())
                if r.get("id") == i:
                    return r.get("result", {})

        def ev(js):
            return cmd("Runtime.evaluate", expression=js, returnByValue=True, awaitPromise=True)["result"].get("value")

        def go(url, w, h, dpr=2, mob=False, wait=9):
            cmd("Emulation.setDeviceMetricsOverride", width=w, height=h, deviceScaleFactor=dpr, mobile=mob)
            cmd("Page.navigate", url=url, referrer="https://www.google.com/"); time.sleep(wait)
            for y in (1200, 2400, 0):   # wake lazy photos above the fold
                ev("window.scrollTo(0,%d)" % y); time.sleep(1)

        def shot(clip, fn, width):
            d = cmd("Page.captureScreenshot", format="png", clip=dict(clip, scale=1))
            im = Image.open(io.BytesIO(base64.b64decode(d["data"]))).convert("RGB")
            if width:
                im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
            if fn:
                im.save(os.path.join(out, fn), "JPEG", quality=80, optimize=True, progressive=True)
                print("  %s (%d KB)" % (fn, os.path.getsize(os.path.join(out, fn)) // 1024))
            return im

        cmd("Page.enable")
        # 1. homepage, computer
        go(SITE + "/", 1440, 900)
        desk = shot({"x": 0, "y": 0, "width": 1440, "height": 900}, "", 1440)
        # 2. smart search on the homepage: a neighbor types an everyday problem, not a category
        cmd("Emulation.setDeviceMetricsOverride", width=1440, height=1400, deviceScaleFactor=2, mobile=False); time.sleep(1)
        ev("""(function(){var i=document.querySelector('.tvl-ns input');if(!i)return 'no box';var b=i.form.getBoundingClientRect();
              window.scrollTo(0,Math.max(0,window.scrollY+b.top-320));i.focus();i.value='toothache';i.dispatchEvent(new Event('input',{bubbles:true}));return 'ok'})()""")
        time.sleep(3)
        # top 3 matches only, and hide the "See all" row
        ev("""(function(){[].slice.call(document.querySelectorAll('#tvlss a.ss-r')).slice(3).forEach(function(a){a.remove()});
              var s=document.querySelector('#tvlss .ss-all');if(s)s.remove();var b=document.getElementById('tvlss');window.onscroll=null;
              var st=document.createElement('style');st.textContent='#tvlss{max-height:none!important;overflow:visible!important;height:auto!important}';document.head.appendChild(st)})()""")
        time.sleep(.5)
        r = ev("""(function(){var f=document.querySelector('.tvl-ns').getBoundingClientRect(),b=document.getElementById('tvlss').getBoundingClientRect(),
              rows=document.querySelectorAll('#tvlss a.ss-r'),l=rows[rows.length-1].getBoundingClientRect();
              return {x:Math.min(f.left,b.left)-20,y:f.top-20+window.scrollY,w:Math.max(f.right,b.right)-Math.min(f.left,b.left)+40,h:l.bottom-f.top+22}})()""")
        shot({"x": r["x"], "y": r["y"], "width": r["w"], "height": r["h"]}, "search.jpg", 1120)
        # 3. homepage, phone
        go(SITE + "/", 390, 844, dpr=3, mob=True)
        phone = shot({"x": 0, "y": 0, "width": 390, "height": 844}, "", 390 * 3)
        # 4. a member listing (computer)
        go(PROFILE, 1440, 900)
        shot({"x": 0, "y": 0, "width": 1440, "height": 900}, "listing.jpg", 1120)
        # 5. Smart Publisher page (the preview mockup: hero + the first part of the form)
        go(MOCKUP, 1000, 1400, wait=3)
        ev("window.scrollTo(0,0)")
        r = ev("""(function(){var a=document.querySelector('.hero').getBoundingClientRect();
              return {x:a.left,y:a.top,w:a.width,h:a.height}})()""")
        shot({"x": r["x"], "y": r["y"], "width": r["w"], "height": r["h"]}, "publisher.jpg", 1120)

        # hero picture: the new homepage on a computer with the phone version in front
        W, H = 1200, 750
        bg = desk.resize((W, round(desk.height * W / desk.width))).crop((0, 0, W, H)).filter(ImageFilter.GaussianBlur(14))
        bg = Image.blend(bg, Image.new("RGB", bg.size, (15, 31, 49)), .62)
        scr = rounded(desk.resize((900, round(desk.height * 900 / desk.width)), Image.LANCZOS), 18)
        ph = rounded(phone.resize((270, round(phone.height * 270 / phone.width)), Image.LANCZOS), 30)
        canvas = bg.convert("RGBA")
        sh = Image.new("RGBA", canvas.size, (0, 0, 0, 0)); d = ImageDraw.Draw(sh)
        d.rounded_rectangle((70, 70, 70 + scr.width, 70 + scr.height), 18, fill=(0, 0, 0, 140))
        d.rounded_rectangle((870, 112, 870 + ph.width + 16, 112 + ph.height + 16), 38, fill=(0, 0, 0, 160))
        canvas = Image.alpha_composite(canvas, sh.filter(ImageFilter.GaussianBlur(18)))
        canvas.alpha_composite(scr, (60, 56))
        frame = rounded(Image.new("RGB", (ph.width + 16, ph.height + 16), (12, 20, 30)), 38)
        canvas.alpha_composite(frame, (862, 102)); canvas.alpha_composite(ph, (870, 110))
        canvas = canvas.convert("RGB")
        canvas.save(os.path.join(out, "hero.jpg"), "JPEG", quality=80, optimize=True, progressive=True)
        print("  hero.jpg (%d KB)" % (os.path.getsize(os.path.join(out, "hero.jpg")) // 1024))
    finally:
        p.terminate()


if __name__ == "__main__":
    main()
