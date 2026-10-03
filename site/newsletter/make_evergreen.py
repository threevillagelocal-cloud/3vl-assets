"""Timeless sample email for the /newsletter phone picture (owner 10/3/2026: no dated event on the sign-up page).
    python site/newsletter/make_evergreen.py   -> site/newsletter/evergreen.html (local file paths; only used by visuals.py)"""
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent.parent
W = (ASSETS / "weekender" / "2026-10-02").as_uri() + "/"
H = (ASSETS / "weekender" / "homes").as_uri() + "/"
P = (ASSETS / "site" / "p3" / "img").as_uri() + "/"
LOGO = "https://threevillagelocal-cloud.github.io/3vl-share/email/2026-10-02/logo.png"

HTML = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{margin:0;background:#eef2f6;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;color:#1d2b3a}
.m{background:#1b2f45;padding:38px 18px 14px;display:flex;align-items:center;gap:10px}.m img{width:40px;height:40px}
.m b{display:block;color:#fff;font-size:17px}.m b span{color:#f2a93b}.m i{display:block;color:#c9d6e3;font-size:12px;font-style:normal;margin-top:2px}
.hero{position:relative;height:250px;background:url('PIMGvillage-hero.jpg') center/cover}
.hero:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(15,31,49,0) 30%,rgba(15,31,49,.88) 100%)}
.hero div{position:absolute;left:18px;right:18px;bottom:18px;z-index:1;color:#fff}
.pill{display:inline-block;background:#f2a93b;color:#1b2f45;font-weight:800;font-size:11px;letter-spacing:1px;padding:5px 10px;border-radius:99px}
.hero h1{margin:8px 0 0;font-size:24px;line-height:1.15}
.sec{padding:20px 18px 6px}.k{margin:0 0 4px;font-size:11px;font-weight:800;letter-spacing:2px;color:#b36b00}
h2{margin:0 0 12px;font-size:20px;color:#1b2f45}
.row{display:flex;gap:12px;background:#fff;border-radius:14px;padding:10px;margin:0 0 10px;border:1px solid #dde5ee}
.row img{width:96px;height:72px;object-fit:cover;border-radius:10px}.row b{display:block;font-size:15px;color:#1b2f45;margin:4px 0}.row span{font-size:12px;color:#5b6b7c}
.card{background:#fff;border-radius:14px;overflow:hidden;border:1px solid #dde5ee}.card img{width:100%;height:150px;object-fit:cover;display:block}
.card div{padding:12px 14px}.card b{display:block;font-size:16px;color:#1b2f45}.card span{font-size:13px;color:#5b6b7c}
.homes{display:flex;gap:8px;align-items:center;background:#fff;border-radius:14px;padding:10px;border:1px solid #dde5ee}.homes img{width:58px;height:58px;border-radius:10px;object-fit:cover}
.homes b{font-size:14px;color:#1b2f45;margin-left:4px}</style></head><body>
<div class="m"><img src="LOGO"><div><b>Three Village <span>Local</span></b><i>Three Village Weekly</i></div></div>
<div class="hero"><div><span class="pill">THIS WEEK</span><h1>What&rsquo;s happening in Setauket, Stony Brook &amp; Port Jeff</h1></div></div>
<div class="sec"><p class="k">THIS WEEKEND</p><h2>Top things to do</h2>
<div class="row"><img src="WIMGpjharbor-720.webp"><div><b>By the harbor</b><span>Music, festivals and waterfront fun</span></div></div>
<div class="row"><img src="WIMGsbvgreen-720.webp"><div><b>Around the village</b><span>Markets, history and family days</span></div></div>
<div class="row"><img src="WIMGmarsh-720.webp"><div><b>Outdoors</b><span>Trails, beaches and nature walks</span></div></div></div>
<div class="sec"><p class="k">EAT &amp; DRINK</p><h2>Local specials</h2>
<div class="card"><img src="PIMGcafe-hero.jpg"><div><b>This week&rsquo;s specials around town</b><span>New menus, deals and happy hours</span></div></div></div>
<div class="sec"><p class="k">HOMES FOR SALE</p><h2>New listings this week</h2>
<div class="homes"><img src="HIMGh1.webp"><img src="HIMGh2.webp"><img src="HIMGh3.webp"><b>See this week&rsquo;s homes &rarr;</b></div></div>
<div class="sec" style="padding-bottom:30px"><p class="k">LOCAL STORIES</p><h2>Neighbors in business</h2></div>
</body></html>"""

out = HTML.replace("PIMG", P).replace("WIMG", W).replace("HIMG", H).replace("LOGO", LOGO)
(HERE / "evergreen.html").write_text(out, encoding="utf-8")
print("wrote", HERE / "evergreen.html")
