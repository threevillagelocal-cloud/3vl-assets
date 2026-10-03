"""Personal pictures for the member update email, one pair per business:
  s-<id>.jpg  smart search on the live homepage: the phrase picked for that business (member_search_pick.py), top 3 matches,
              that business's row highlighted
  b-<id>.jpg  the live /categories page with the VIP banner spot showing that business: a VIP's own banner, otherwise a
              clearly labeled SAMPLE banner made from the listing's name, logo, category and phone
    python weekender/member_visuals.py <name> <picks.json> [id ...]   -> 3vl-share/email/<name>/
The page is loaded once and reused, so ~240 businesses take about 20 minutes. Throwaway Chrome profile."""
import base64, io, json, os, subprocess, sys, tempfile, time, urllib.request
import websocket
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.dirname(HERE)
SHARE = os.path.join(os.path.dirname(ASSETS), "3vl-share")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
SITE = "https://www.threevillagelocal.com"

SAMPLE_CSS = """
.tvs{position:relative;width:100%;height:100%;background:radial-gradient(circle at 85% 0,rgba(255,197,61,.28),transparent 50%),linear-gradient(150deg,#1b2f45,#0f1f31);
 color:#fff;font-family:'Radio Canada','tvl-rc',system-ui,sans-serif;display:flex;flex-direction:column;justify-content:center;padding:calc(var(--u)*7) calc(var(--u)*8);box-sizing:border-box;text-align:left}
.tvs .tag{position:absolute;top:calc(var(--u)*5);right:calc(var(--u)*5);font-weight:800;font-size:calc(var(--u)*3.2);line-height:1;letter-spacing:.14em;color:#13233a;background:#ffc53d;padding:calc(var(--u)*1.6) calc(var(--u)*2.6);border-radius:99px}
.tvs .lg{width:calc(var(--u)*24);height:calc(var(--u)*24);border-radius:calc(var(--u)*4);background:#fff center/contain no-repeat;box-shadow:0 0 0 calc(var(--u)*1) rgba(255,197,61,.9);margin:0 0 calc(var(--u)*5)}
.tvs .lg.ini{display:flex;align-items:center;justify-content:center;font-weight:800;font-size:calc(var(--u)*12);line-height:1;color:#1b2f45}
.tvs .nm{font-weight:800;font-size:calc(var(--u)*9);line-height:1.05;margin:0 0 calc(var(--u)*3);overflow-wrap:break-word}
.tvs .nm.l{font-size:calc(var(--u)*7)}.tvs .nm.xl{font-size:calc(var(--u)*5.6)}
.tvs .ct{font-weight:700;font-size:calc(var(--u)*4.2);line-height:1.2;color:#ffc53d;letter-spacing:.06em;text-transform:uppercase;margin:0 0 calc(var(--u)*4)}
.tvs .ph{font-weight:800;font-size:calc(var(--u)*8);line-height:1;color:#fff;border-top:.calc(var(--u)*5) solid rgba(255,255,255,.25);padding-top:calc(var(--u)*4)}
"""


def main():
    name, picks_path = sys.argv[1], sys.argv[2]
    only = set(sys.argv[3:])
    picks = json.load(open(picks_path, encoding="utf-8"))
    idx = {str(m["id"]): m for m in json.load(open(os.path.join(ASSETS, "search", "index.json"), encoding="utf-8"))["members"]}
    banners = {}
    for b in json.load(open(os.path.join(HERE, "banners.json"), encoding="utf-8")):
        banners.setdefault(b["id"], b)
    ids = [i for i in picks if (not only or i in only) and i in idx]
    out = os.path.join(SHARE, "email", name)
    os.makedirs(out, exist_ok=True)
    prof = tempfile.mkdtemp(prefix="memvis-")
    p = subprocess.Popen([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--remote-debugging-port=9377",
                          "--remote-allow-origins=http://127.0.0.1:9377", "--user-data-dir=" + prof, "about:blank"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(80):
            try:
                pg = [t for t in json.load(urllib.request.urlopen("http://127.0.0.1:9377/json")) if t["type"] == "page"][0]; break
            except Exception:
                time.sleep(.25)
        ws = websocket.create_connection(pg["webSocketDebuggerUrl"], timeout=120); n = [0]

        def cmd(m, **pa):
            n[0] += 1; i = n[0]; ws.send(json.dumps({"id": i, "method": m, "params": pa}))
            while True:
                r = json.loads(ws.recv())
                if r.get("id") == i:
                    return r.get("result", {})

        def ev(js):
            r = cmd("Runtime.evaluate", expression=js, returnByValue=True, awaitPromise=True)
            if "exceptionDetails" in r:
                return {"err": r["exceptionDetails"].get("exception", {}).get("description", "error")[:200]}
            return r["result"].get("value")

        def save(clip, fn, width):
            d = cmd("Page.captureScreenshot", format="png", clip=dict(clip, scale=1))
            im = Image.open(io.BytesIO(base64.b64decode(d["data"]))).convert("RGB")
            im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
            im.save(os.path.join(out, fn), "JPEG", quality=80, optimize=True, progressive=True)

        def load(url, h):
            cmd("Emulation.setDeviceMetricsOverride", width=1440, height=h, deviceScaleFactor=2, mobile=False)
            cmd("Page.navigate", url=url, referrer="https://www.google.com/"); time.sleep(10)

        cmd("Page.enable")
        # ---- search pictures (homepage) ----
        load(SITE + "/", 1400)
        ev("""(function(){var i=document.querySelector('.tvl-ns input');var b=i.form.getBoundingClientRect();window.scrollTo(0,Math.max(0,window.scrollY+b.top-320));
             var st=document.createElement('style');st.textContent='#tvlss{max-height:none!important;overflow:visible!important}#tvlss a.ss-r.me{background:#fff8ea!important;box-shadow:inset 4px 0 0 #ffc53d,inset 0 0 0 2px #ffc53d;border-radius:10px}';document.head.appendChild(st)})()""")
        for k, uid in enumerate(ids):
            q, url = picks[uid].get("q"), idx[uid]["u"]
            if not q:
                continue
            r = ev("""(async function(){var i=document.querySelector('.tvl-ns input'),box=document.getElementById('tvlss');if(box)box.innerHTML='';
                 i.focus();i.value=%s;i.dispatchEvent(new Event('input',{bubbles:true}));
                 for(var t=0;t<40;t++){await new Promise(function(r){setTimeout(r,100)});var rows=document.querySelectorAll('#tvlss a.ss-r');if(rows.length&&!document.getElementById('tvlss').hidden)break}
                 var rows=[].slice.call(document.querySelectorAll('#tvlss a.ss-r'));rows.slice(3).forEach(function(a){a.remove()});
                 var all=document.querySelector('#tvlss .ss-all');if(all)all.remove();var me=false;
                 rows.slice(0,3).forEach(function(a){var on=a.getAttribute('href')===%s;a.classList.toggle('me',on);if(on)me=true});
                 await new Promise(function(r){setTimeout(r,250)});
                 var f=document.querySelector('.tvl-ns').getBoundingClientRect(),b=document.getElementById('tvlss').getBoundingClientRect(),l=document.querySelectorAll('#tvlss a.ss-r');l=l[l.length-1].getBoundingClientRect();
                 return {me:me,x:Math.min(f.left,b.left)-20,y:f.top-20+window.scrollY,w:Math.max(f.right,b.right)-Math.min(f.left,b.left)+40,h:l.bottom-f.top+30}})()""" % (json.dumps(q), json.dumps(url)))
            if not r or "err" in r or not r.get("me"):
                print("  search: %s %s -> not shown (%s)" % (uid, idx[uid]["n"], r)); continue
            save({"x": r["x"], "y": r["y"], "width": r["w"], "height": r["h"]}, "s-%s.jpg" % uid, 1120)
            if k % 20 == 0:
                print("  search %d/%d" % (k + 1, len(ids)))
        # ---- banner pictures (/categories) ----
        load(SITE + "/categories", 900)
        ev("""(function(){for(var i=1;i<5000;i++){clearInterval(i);clearTimeout(i)}var st=document.createElement('style');st.textContent=%s;document.head.appendChild(st);window.scrollTo(0,0)})()""" % json.dumps(SAMPLE_CSS))
        for k, uid in enumerate(ids):
            m, b = idx[uid], banners.get(uid)
            if b:
                spec = {"img": b["img"].split("/")[-1]}
            else:
                nm = m["n"]
                spec = {"name": nm, "cls": "xl" if len(nm) > 34 else "l" if len(nm) > 20 else "", "logo": m.get("l") or "",
                        "ini": nm.replace("The ", "")[:1].upper(), "cat": ", ".join(x for x in [m.get("c") or "", town(m.get("t") or "")] if x),
                        "ph": fmt_phone(m.get("ph") or "")}
            r = ev("""(async function(){var S=%s,r=document.querySelector('.vipx-rot');if(!r)return 'no rotator';
                 var ads=[].slice.call(r.querySelectorAll('.vipx-ad')),hit=null;
                 if(S.img){ads.forEach(function(a){var im=a.querySelector('img');var s=(im&&(im.getAttribute('src')||im.getAttribute('data-src')))||'';if(s.indexOf(S.img)>-1){hit=a;if(!im.getAttribute('src'))im.src=im.getAttribute('data-src')}});
                   if(!hit)return 'banner not found'}
                 else{hit=r.querySelector('.vipx-ad.tvs-host');if(!hit){hit=ads[ads.length-1].cloneNode(true);hit.classList.add('tvs-host');ads[ads.length-1].parentNode.appendChild(hit)}
                   var a=hit.querySelector('a')||hit,e=function(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})};
                   a.innerHTML='<div class="tvs" style="--u:'+(a.clientWidth/100)+'px"><span class="tag">SAMPLE</span>'+(S.logo?'<div class="lg" style="background-image:url(\\''+e(S.logo)+'\\')"></div>':'<div class="lg ini">'+e(S.ini)+'</div>')+
                     '<div class="nm '+S.cls+'">'+e(S.name)+'</div>'+(S.cat?'<div class="ct">'+e(S.cat)+'</div>':'')+(S.ph?'<div class="ph">'+e(S.ph)+'</div>':'')+'</div>';
                   if(S.logo){await new Promise(function(res){var im=new Image();im.onload=im.onerror=res;im.src=S.logo;setTimeout(res,4000)})}}
                 [].slice.call(r.querySelectorAll('.vipx-ad')).forEach(function(a){a.classList.toggle('on',a===hit)});
                 [].slice.call(document.querySelectorAll('.vipx-rot')).slice(1).forEach(function(r2){var o=[].slice.call(r2.querySelectorAll('.vipx-ad')).filter(function(a){var im=a.querySelector('img');var s=(im&&(im.getAttribute('src')||im.getAttribute('data-src')))||'';return !S.img||s.indexOf(S.img)<0})[0];
                   if(o){var im=o.querySelector('img');if(im&&!im.getAttribute('src'))im.src=im.getAttribute('data-src');r2.querySelectorAll('.vipx-ad').forEach(function(a){a.classList.toggle('on',a===o)})}});
                 window.scrollTo(0,0);await new Promise(function(res){setTimeout(res,1200)});return 'ok'})()""" % json.dumps(spec))
            if r != "ok":
                print("  banner: %s %s -> %s" % (uid, m["n"], r)); continue
            save({"x": 0, "y": 0, "width": 1440, "height": 900}, "b-%s.jpg" % uid, 1200)
            if k % 20 == 0:
                print("  banner %d/%d" % (k + 1, len(ids)))
    finally:
        p.terminate()


def town(t):
    """Owner rule: any Setauket / East Setauket listing shows as "Setauket"."""
    return "Setauket" if "setauket" in t.lower() else t


def fmt_phone(ph):
    d = "".join(c for c in ph if c.isdigit())
    if len(d) == 11 and d[0] == "1":
        d = d[1:]
    return "%s-%s-%s" % (d[:3], d[3:6], d[6:]) if len(d) == 10 else ""


if __name__ == "__main__":
    main()
