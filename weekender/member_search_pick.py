"""For each member listing: find an everyday search phrase that brings that business up in smart search, using the real
engine (window.tvlSS) on the live homepage. Writes <out>/search_picks.json:
    {id: {"q": phrase, "rank": 0-2, "top": [[id, name, category], ...], "ok": true|false, "why": ...}}
    python weekender/member_search_pick.py <out dir>
A pick is "ok" only when the business is in the top 3 and every business shown next to it is in the same line of work,
so the example reads naturally. Others are flagged for a person to look at."""
import json, os, subprocess, sys, tempfile, time, urllib.request
import websocket

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

JS = r"""(async function(){var OVR=__OVR__;
  var SS=window.tvlSS;await SS.load();
  var idx=await (await fetch('https://raw.githubusercontent.com/threevillagelocal-cloud/3vl-assets/master/search/index.json')).json();   /* same file the engine uses */
  var BAD=/\b(best|good|nearby|near me|top|cheap|affordable|reviews?|rated|reservations?|open now|hours|deals?|coupons?|discount)\b/i;
  var out={};
  idx.members.forEach(function(m){
    if(m.p==='claim'||m.p==='house')return;
    var cand=[],seen={};
    (m.k||[]).concat((m.s||[]).map(function(s){return s.toLowerCase()})).concat([String(m.c||'').toLowerCase()]).forEach(function(q){
      q=String(q||'').replace(/\s+/g,' ').trim();if(!q||seen[q]||BAD.test(q)||q.length<4)return;
      seen[q]=1;cand.push(q)});
    var best=null,about=SS.norm([m.n,m.d,(m.s||[]).join(' ')].join(' ')),cat=String(m.c||'').toLowerCase();
    var fits=function(q){   /* every telling word of the phrase is in the business's own name, description or specialties */
      var ws=SS.norm(q).split(' ').filter(function(w){return w&&!SS.STOP[w]&&w!=='&'});
      return ws.length&&ws.every(function(w){var st=w.length>5?w.slice(0,w.length-2):w;return (' '+about).indexOf(' '+st)>-1})};
    cand.forEach(function(q,ci){
      if(q===cat||!fits(q))return;
      var res=SS.search(q,7),ids=res.map(function(x){return x.r.m.id}),rank=ids.indexOf(m.id);if(rank<0||rank>2)return;
      var top=res.slice(0,3).map(function(x){return [x.r.m.id,x.r.m.n,x.r.m.c||'',(x.r.m.s||[]).join('|')]});
      var same=top.every(function(t){return t[2]===m.c});
      var wc=q.split(' ').length;
      var sc=(rank===0?40:rank===1?22:10)+(same?20:0)+(wc===2?6:wc===3?4:wc===1?1:0)+(ci<(m.k||[]).length?3:0)-(top.length<2?6:0);
      if(!best||sc>best.sc)best={q:q,rank:rank,top:top,same:same,sc:sc}});
    var ov=(OVR[m.id]||[]),hit=null;   /* hand-picked phrases win when they put the business in the top 3 */
    ov.some(function(q){var res=SS.search(q,7),rank=res.map(function(x){return x.r.m.id}).indexOf(m.id);if(rank<0||rank>2)return false;
      hit={q:q,rank:rank,top:res.slice(0,3).map(function(x){return [x.r.m.id,x.r.m.n,x.r.m.c||'',(x.r.m.s||[]).join('|')]}),same:true};return true});
    if(ov.length&&!hit&&best)best.same=false;
    if(hit)best=hit;
    if(best)out[m.id]={n:m.n,c:m.c,p:m.p,q:best.q,rank:best.rank,top:best.top,ok:best.same,why:best.same?'':'other kinds of business show next to it'};
    else out[m.id]={n:m.n,c:m.c,p:m.p,q:'',rank:-1,top:[],ok:false,why:'no phrase that fits its own description puts it in the top 3'};
  });
  return JSON.stringify(out)})()"""


def main():
    od = sys.argv[1]
    os.makedirs(od, exist_ok=True)
    prof = tempfile.mkdtemp(prefix="sspick-")
    p = subprocess.Popen([CHROME, "--headless=new", "--disable-gpu", "--remote-debugging-port=9375",
                          "--remote-allow-origins=http://127.0.0.1:9375", "--user-data-dir=" + prof, "about:blank"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(80):
            try:
                pg = [t for t in json.load(urllib.request.urlopen("http://127.0.0.1:9375/json")) if t["type"] == "page"][0]; break
            except Exception:
                time.sleep(.25)
        ws = websocket.create_connection(pg["webSocketDebuggerUrl"], timeout=600); n = [0]

        def cmd(m, **pa):
            n[0] += 1; i = n[0]; ws.send(json.dumps({"id": i, "method": m, "params": pa}))
            while True:
                r = json.loads(ws.recv())
                if r.get("id") == i:
                    return r.get("result", {})
        cmd("Page.enable")
        cmd("Page.navigate", url="https://www.threevillagelocal.com/", referrer="https://www.google.com/"); time.sleep(10)
        ovp = os.path.join(od, "phrase_overrides.json")   # {id: [phrase, ...]} checked by a person
        ovr = json.load(open(ovp, encoding="utf-8")) if os.path.exists(ovp) else {}
        r = cmd("Runtime.evaluate", expression=JS.replace("__OVR__", json.dumps(ovr)), returnByValue=True, awaitPromise=True)
        if "exceptionDetails" in r:
            print(r["exceptionDetails"]); return
        picks = json.loads(r["result"]["value"])
        json.dump(picks, open(os.path.join(od, "search_picks.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        ok = sum(1 for v in picks.values() if v["ok"])
        print("members:", len(picks), " ok:", ok, " flagged:", len(picks) - ok)
    finally:
        p.terminate()


if __name__ == "__main__":
    main()
