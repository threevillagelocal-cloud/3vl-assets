"""For the weekly email's VIP version: a picture of each VIP's own banner running on a live Three Village Local page.
Loads the real /categories page (desktop), puts that VIP's banner in the sidebar rotator, and saves a JPG per VIP:
    3vl-share/email/<edition>/vip-shot-<id>.jpg      python weekender/vip_shots.py <edition> [id ...]
Uses a throwaway Chrome profile (never the owner's)."""
import base64, io, json, os, subprocess, sys, tempfile, time, urllib.request
import websocket
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SHARE = os.path.join(os.path.dirname(os.path.dirname(HERE)), "3vl-share")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PAGE = "https://www.threevillagelocal.com/categories"


def main():
    ed = sys.argv[1]
    only = set(sys.argv[2:])
    banners = [b for b in json.load(open(os.path.join(HERE, "banners.json"), encoding="utf-8")) if not only or b["id"] in only]
    seen, todo = set(), []
    for b in banners:   # one picture per business (a VIP can have two banner designs: use the first)
        if b["id"] not in seen:
            seen.add(b["id"]); todo.append(b)
    out = os.path.join(SHARE, "email", ed)
    os.makedirs(out, exist_ok=True)
    prof = tempfile.mkdtemp(prefix="vipshot-")
    p = subprocess.Popen([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--remote-debugging-port=9371",
                          "--remote-allow-origins=http://127.0.0.1:9371", "--user-data-dir=" + prof, "about:blank"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(80):
            try:
                pg = [t for t in json.load(urllib.request.urlopen("http://127.0.0.1:9371/json")) if t["type"] == "page"][0]; break
            except Exception:
                time.sleep(.25)
        ws = websocket.create_connection(pg["webSocketDebuggerUrl"], timeout=90); n = [0]

        def cmd(m, **pa):
            n[0] += 1; i = n[0]; ws.send(json.dumps({"id": i, "method": m, "params": pa}))
            while True:
                r = json.loads(ws.recv())
                if r.get("id") == i:
                    return r.get("result", {})
        cmd("Page.enable")
        cmd("Emulation.setDeviceMetricsOverride", width=1440, height=980, deviceScaleFactor=2, mobile=False)
        for b in todo:
            cmd("Page.navigate", url=PAGE); time.sleep(8)
            f = b["img"].split("/")[-1]
            js = """(function(){for(var i=1;i<5000;i++){clearInterval(i);clearTimeout(i)}
              var rots=[].slice.call(document.querySelectorAll('.vipx-rot'));if(!rots.length)return 'no rotator';
              var r=rots[0],hit=null;[].forEach.call(r.querySelectorAll('.vipx-ad'),function(a){var im=a.querySelector('img');var s=im&&(im.getAttribute('src')||im.getAttribute('data-src')||'');
                if(s.indexOf('%s')>-1){hit=a;if(im&&!im.getAttribute('src'))im.src=im.getAttribute('data-src')}});
              if(!hit)return 'banner not in rotator';
              [].forEach.call(r.querySelectorAll('.vipx-ad'),function(a){a.classList.toggle('on',a===hit)});
              rots.slice(1).forEach(function(r2){var ads=[].slice.call(r2.querySelectorAll('.vipx-ad'));   /* other rotators: never the same banner twice */
                var other=ads.filter(function(a){var im=a.querySelector('img');var s=im&&(im.getAttribute('src')||im.getAttribute('data-src')||'');return s.indexOf('%s')<0})[0];
                if(other){var im=other.querySelector('img');if(im&&!im.getAttribute('src'))im.src=im.getAttribute('data-src');ads.forEach(function(a){a.classList.toggle('on',a===other)})}});
              window.scrollTo(0,0);return 'ok'})()""" % (f, f)
            res = cmd("Runtime.evaluate", expression=js, returnByValue=True)["result"].get("value")
            time.sleep(2.5)
            if res != "ok":
                print("  skip", b["name"], res); continue
            shot = cmd("Page.captureScreenshot", format="jpeg", quality=88, clip={"x": 0, "y": 0, "width": 1440, "height": 900, "scale": 1})
            im = Image.open(io.BytesIO(base64.b64decode(shot["data"]))).convert("RGB")
            im = im.resize((1200, round(im.height * 1200 / im.width)), Image.LANCZOS)
            path = os.path.join(out, "vip-shot-%s.jpg" % b["id"])
            im.save(path, "JPEG", quality=80, optimize=True, progressive=True)
            print("  %s -> %s (%d KB)" % (b["name"], os.path.basename(path), os.path.getsize(path) // 1024))
    finally:
        p.terminate()


if __name__ == "__main__":
    main()
