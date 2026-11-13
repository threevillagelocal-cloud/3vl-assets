"""New business launch service page: "Opening a new business? Launch with the whole town watching."
Owner 11/12/2026: every service on /services gets its own premium interactive page. No prices.
site/new-business/build.py (10/18) is an older /preview-new-business on the old services design WITH launch prices, so this is a
new page in the current design instead (that builder and its page are untouched).
    python site/new-business-launch-page/build.py   -> widget "3VL Page New Business Launch Preview" + hidden /preview-new-business-launch (noindex)
    (--live -> /new-business-launch only after the owner's OK)"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "svc-kit"))
import kit as K
from kit import ic, SV, WB

HERO_LIST = [("globe", "Website live"), ("pin", "Google and Apple listings"), ("share", "Social accounts ready"), ("star", "Launch spotlight"), ("calendar", "Grand opening event")]
hl = "".join('<li style="--i:%d"><span>%s</span>%s<b>%s</b></li>' % (n, ic(i), t, ic("check")) for n, (i, t) in enumerate(HERO_LIST))
HERO_VIS = '''<div class="tnb-hv">
  <div class="tnb-board" id="tnb-board">
    <div class="tnb-bh"><div><p>Grand opening</p><h3>Your Business</h3><i>''' + ic("pin") + '''Main Street, Setauket</i></div><div class="tnb-ring"><svg viewBox="0 0 44 44" aria-hidden="true"><circle cx="22" cy="22" r="19" class="t"/><circle cx="22" cy="22" r="19" class="v" pathLength="100"/></svg><b>Launch<br>ready</b></div></div>
    <div class="tnb-cd" aria-label="Sample countdown"><div><b id="tnb-d">12</b><span>days</span></div><div><b id="tnb-h">08</b><span>hrs</span></div><div><b id="tnb-m">45</b><span>min</span></div><div><b id="tnb-s">30</b><span>sec</span></div></div>
    <ul class="tnb-hl">''' + hl + '''</ul>
    <div class="tnb-now"><span>''' + ic("star") + '''</span><div><b>Now open!</b>Featured on Three Village Local</div></div>
  </div>
</div>'''

HERO = K.hero("New business launch", "Opening a new business?", "Launch with the whole town watching.",
              "From your website and Google listing to a Three Village Local launch spotlight, social posts and a promo video: we get everything ready, then tell the whole community you&#39;re open.",
              HERO_VIS, ("Try the launch checklist", "#tvp-checklist"), cls="tnb-hero")

NAV = K.snav([("checklist", "Launch checklist"), ("timeline", "Timeline"), ("included", "What&#39;s included"), ("how", "How it works"), ("faq", "FAQ")])

GROUPS = [("Before you open", [("web", "globe", "Website live and built for AI search"), ("gbp", "pin", "Google Business Profile verified"),
                               ("apple", "pin", "Apple Maps and Bing listings claimed"), ("social", "share", "Facebook and Instagram set up and branded"),
                               ("photo", "camera", "Photos and a promo video ready")]),
          ("Opening week", [("spot", "star", "Three Village Local launch spotlight"), ("event", "calendar", "Grand opening on our events calendar"),
                            ("count", "megaphone", "Social countdown and collab posts"), ("email", "mail", "Featured in our weekly email")]),
          ("After you open", [("reviews", "star", "A plan to earn your first Google reviews"), ("ai", "sparkle", "AI search optimization so ChatGPT knows you"),
                              ("ongoing", "rocket", "Ongoing promotion to keep the momentum")])]
grp = ""
for g, items in GROUPS:
    li = "".join('<li><label><input type="checkbox" value="%s" data-l="%s"><span class="tnb-bx">%s</span><span class="tnb-ii">%s</span><span class="tnb-t">%s</span><em>We do this</em></label></li>' % (k, t, ic("check"), ic(i), t) for k, i, t in items)
    grp += '<div class="tnb-g"><h3>%s</h3><ul>%s</ul></div>' % (g, li)
N = sum(len(x[1]) for x in GROUPS)
CHECK = K.sec("checklist", "Interactive launch checklist", "How launch-ready are you?",
              "Check off what you already have. We&#39;ll handle the rest, and you can send your list straight to us.",
              '''<div class="tnb-ck tvs-up" id="tnb-ck">
    <div class="tnb-groups">''' + grp + '''</div>
    <aside class="tnb-sum"><div class="tnb-sum-in">
      <div class="tnb-big"><svg viewBox="0 0 120 120" aria-hidden="true"><circle cx="60" cy="60" r="52" class="t"/><circle cx="60" cy="60" r="52" class="v" id="tnb-arc" pathLength="100"/></svg><div><b><span id="tnb-pct">0</span>%</b><i>launch-ready</i></div></div>
      <p class="tnb-msg" id="tnb-msg">Check what you already have.</p>
      <p class="tnb-left"><b id="tnb-n">''' + str(N) + '''</b> things we can handle for you</p>
      <a class="tvs-btn tvs-blue tnb-go" href="#tvs-book">Get my launch plan</a>
      <button type="button" class="tnb-reset">Start over</button>
    </div></aside>
  </div>''')

TL = [("t6", "6 weeks out", "Plan and build", ["Your launch plan and timeline", "Brand look, photos and copy", "Website design begins"]),
      ("t2", "2 weeks out", "Get found", ["Website live, built for Google and AI", "Google, Apple and Bing listings", "Social accounts set up and branded"]),
      ("t0", "Opening week", "Tell the whole town", ["Three Village Local launch spotlight", "Countdown and collab posts", "Grand opening on our calendar and in the weekly email"]),
      ("t30", "First 30 days", "Keep the momentum", ["First Google reviews", "AI search optimization", "Promo video and ongoing promotion"])]
tlt = "".join('<button class="tvx-tab tnb-ms%s" data-tab="%s"><i></i><b>%s</b><span>%s</span></button>' % (" on" if n == 0 else "", k, w, h) for n, (k, w, h, li) in enumerate(TL))
tlp = "".join('<div class="tnb-tp" data-panel="%s"><p class="tnb-tw">%s</p><h3>%s</h3><ul>%s</ul></div>' % (k, w, h, "".join("<li>%s%s</li>" % (ic("check"), x) for x in li)) for k, w, h, li in TL)
TIMELINE = K.sec("timeline", "Your launch timeline", "From &ldquo;coming soon&rdquo; to the place everyone knows.",
                 "Tap a milestone. We work backward from your opening day so nothing is left to the last minute.",
                 '<div class="tnb-tl tvs-up" data-tabs data-auto="3800"><div class="tnb-track"><div class="tvx-tabs">' + tlt + '</div><u class="tnb-fill"></u></div>' + tlp + '</div>')

INC = K.sec("included", "What&#39;s included", "Everything a new business needs. Done for you.",
            "Pick the pieces you need. We put them together into one launch plan.",
            K.cards([("globe", "AI-ready website", "Designed, built and hosted for you, set up to be found on Google and AI search from day one."),
                     ("pin", "Google and Apple listings", "Your Google Business Profile, Apple Maps and Bing set up right, with photos, hours and services."),
                     ("star", "Launch spotlight", "A Three Village Local spotlight that introduces you to the whole community."),
                     ("megaphone", "Social media launch", "Countdown, opening day and collab posts to 100,000+ local views a month."),
                     ("video", "Promo video", "A short video that shows off your new place, sized for Reels, TikTok and your website."),
                     ("gift", "Grand opening kit", "Your opening on our events calendar, in our weekly email and in our free mobile app.")], 3))

STATS = '<section class="tvs-sec tvx-sec" id="tvp-reach">' + K.stats_band("Open your doors to an audience that&#39;s already here.", "Reach on day one") + '</section>'

HOW = K.sec("how", "How it works", "One local team. One launch plan.", "",
            K.steps([("Tell us", "Share your opening date, your business and what you have so far."),
                     ("Your plan", "We send a free launch plan by email: what to do, and when."),
                     ("We build", "Website, listings, social, photos and video, all set up for you."),
                     ("Opening day", "We tell the whole town you&#39;re open."),
                     ("Keep growing", "Reviews, AI search and ongoing promotion.")]))

FAQ = K.faq([
    ("When should I reach out?", "As early as you can. About six weeks before opening is ideal, but we can help even if you open next week, or opened last month."),
    ("I already have a website or an Instagram. Do I start over?", "No. We use what you have and fill in the gaps. The checklist above is a quick way to show us where you are."),
    ("What is a launch spotlight?", "A feature on Three Village Local that introduces your new business to the community, shared on our Facebook and Instagram (100,000+ local views a month), our website and our free mobile app."),
    ("Can you film our grand opening?", "Ask us about photos and a promo video for your opening. We plan it with you so we capture the moments that matter."),
    ("Do you set up Google and Apple listings?", "Yes. We set up and verify your Google Business Profile and claim your Apple Maps and Bing listings, with your hours, photos and services, so people can find you from day one."),
    ("How do I get started?", "Fill out the short form below, or use the checklist and tap Get my launch plan. We&#39;ll send a free, personalized launch plan by email, with no pressure and no contract."),
])

REL = K.related("new-business-launch", ["social-media", "promo-video", "ai-search", "websites", "email-articles", "join"])
CTA = K.cta("Your grand opening starts here", "Let&#39;s plan your launch.", "Tell us about your opening and we&#39;ll send a free launch plan by email.")

JS = ''';(function(){var c=document.getElementById('tnb-ck');if(!c)return;var bs=[].slice.call(c.querySelectorAll('input[type=checkbox]')),K='3vl_launch_ck';
var arc=document.getElementById('tnb-arc'),pct=document.getElementById('tnb-pct'),msg=document.getElementById('tnb-msg'),nn=document.getElementById('tnb-n');
try{var sv=JSON.parse(localStorage.getItem(K)||'[]');bs.forEach(function(b){if(sv.indexOf(b.value)>-1)b.checked=true;});}catch(x){}
function upd(save){var on=bs.filter(function(b){return b.checked;}),p=Math.round(on.length*100/bs.length);pct.textContent=p;arc.style.strokeDashoffset=100-p;nn.textContent=bs.length-on.length;
 c.setAttribute('data-p',p<34?'lo':p<67?'mid':p<100?'hi':'done');
 msg.textContent=p===0?'Check what you already have.':p<34?'Great start. Most of the heavy lifting is still ahead, and that is what we are here for.':p<67?'You are on your way. Let us take the rest off your plate.':p<100?'Almost there. We will fill in the last few pieces.':'You are ready! Now let us tell the whole town.';
 if(save){try{localStorage.setItem(K,JSON.stringify(on.map(function(b){return b.value;})));}catch(x){}}}
bs.forEach(function(b){b.addEventListener('change',function(){upd(true);if(window.tvxGA)tvxGA('svc_page_check',{item:b.value,on:b.checked?1:0});});});
c.querySelector('.tnb-reset').addEventListener('click',function(){bs.forEach(function(b){b.checked=false;});upd(true);});
c.querySelector('.tnb-go').addEventListener('click',function(){var need=bs.filter(function(b){return !b.checked;}).map(function(b){return b.getAttribute('data-l');}),have=bs.filter(function(b){return b.checked;}).map(function(b){return b.getAttribute('data-l');});
 var t='Launch checklist. Still need: '+(need.join('; ')||'nothing, ready to launch')+'. Already have: '+(have.join('; ')||'nothing yet')+'.';var tries=0;(function fill(){var f=document.querySelector('#tvs-form-slot [name=comments]');if(f){if(!f.value||f.value.indexOf('Launch checklist.')===0)f.value=t;var d=f.closest('details');if(d)d.open=true;}else if(++tries<20)setTimeout(fill,250);})();
 if(window.tvxGA)tvxGA('svc_page_checklist_cta',{ready:+pct.textContent});},true);
upd(false);})();
;(function(){var b=document.getElementById('tnb-board');if(!b)return;var t=12*86400+8*3600+45*60+30;function p(n){return (n<10?'0':'')+n;}
var d=document.getElementById('tnb-d'),h=document.getElementById('tnb-h'),m=document.getElementById('tnb-m'),s=document.getElementById('tnb-s'),iv=null;
function draw(){d.textContent=Math.floor(t/86400);h.textContent=p(Math.floor(t%86400/3600));m.textContent=p(Math.floor(t%3600/60));s.textContent=p(t%60);}
function tick(){t--;if(t<0)t=12*86400+8*3600+45*60+30;draw();}
var host=b.closest('[data-run]');if(window.tvxOnRun&&host&&!window.tvxRM)tvxOnRun(host,function(on){if(on&&!iv)iv=setInterval(tick,1000);else if(!on&&iv){clearInterval(iv);iv=null;}});draw();})();'''

CSS = '''
.tnb-hero h1{font-size:46px}
.tnb-hv{position:relative;width:100%;max-width:420px}
.tnb-board{position:relative;padding:20px;border-radius:26px;background:#fff;box-shadow:0 40px 80px -40px rgba(9,30,66,.6),0 0 0 1px rgba(15,42,82,.08);overflow:hidden}
.tnb-board:before{content:"";position:absolute;left:0;right:0;top:0;height:5px;background:linear-gradient(90deg,#1d5fbf,#4da3ff,#ffc53d,#16a37a);background-size:200% 100%;animation:tnbBar 6s linear infinite}
@keyframes tnbBar{to{background-position:200% 0}}
.tnb-bh{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;margin-bottom:14px}
.tnb-bh p{margin:0!important;font-size:12px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:#c2410c}
.tnb-bh h3{margin:2px 0 3px!important;font-size:24px}
.tnb-bh i{display:flex;align-items:center;gap:5px;font-style:normal;font-size:13px;color:var(--mut)}.tnb-bh i .tvx-svg{width:14px;height:14px}
.tnb-ring{position:relative;width:74px;height:74px;flex:none}
.tnb-ring svg{width:74px;height:74px;transform:rotate(-90deg)}
.tnb-ring .t{fill:none;stroke:#edf1f6;stroke-width:4}.tnb-ring .v{fill:none;stroke:#16a37a;stroke-width:4;stroke-linecap:round;stroke-dasharray:100;stroke-dashoffset:100;animation:tnbRing 10s cubic-bezier(.4,0,.2,1) infinite}
@keyframes tnbRing{0%,6%{stroke-dashoffset:100}60%,92%{stroke-dashoffset:0}100%{stroke-dashoffset:100}}
.tnb-ring b{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;text-align:center;font-size:10.5px;line-height:1.15;color:var(--navy)}
.tnb-cd{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:14px}
.tnb-cd div{padding:10px 0 8px;border-radius:14px;background:linear-gradient(160deg,#13294b,#1d5fbf);color:#fff;text-align:center}
.tnb-cd b{display:block;font-size:26px;line-height:1;font-variant-numeric:tabular-nums}
.tnb-cd span{font-size:11px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#bcd4f5}
.tnb-hl{list-style:none;margin:0!important;padding:0!important;display:grid;gap:7px}
.tnb-hl li{display:flex;align-items:center;gap:10px;margin:0!important;padding:9px 11px;border-radius:12px;background:#f6f9fd;border:1px solid #edf1f6;font-weight:700;font-size:14.5px;color:var(--navy);animation:tnbRow 10s infinite;animation-delay:calc(var(--i)*1s)}
.tnb-hl li>span{display:flex;width:28px;height:28px;border-radius:9px;align-items:center;justify-content:center;background:#e7f0ff;color:var(--blue);flex:none}.tnb-hl li>span .tvx-svg{width:16px;height:16px}
.tnb-hl li>b{margin-left:auto;display:flex;width:22px;height:22px;border-radius:50%;align-items:center;justify-content:center;background:#dfe6ef;color:#fff;animation:tnbTick 10s infinite;animation-delay:calc(var(--i)*1s)}
.tnb-hl li>b .tvx-svg{width:13px;height:13px;stroke-width:3}
@keyframes tnbTick{0%,8%{background:#dfe6ef;transform:scale(1)}12%{background:#16a37a;transform:scale(1.25)}16%,88%{background:#16a37a;transform:scale(1)}94%,100%{background:#dfe6ef}}
@keyframes tnbRow{0%,8%{background:#f6f9fd;border-color:#edf1f6}12%,88%{background:#f0fbf6;border-color:#cdeedd}94%,100%{background:#f6f9fd;border-color:#edf1f6}}
.tnb-now{position:absolute;left:20px;right:20px;bottom:20px;display:flex;align-items:center;gap:12px;padding:14px;border-radius:16px;background:linear-gradient(120deg,#ffc53d,#ffd978);color:#13294b;box-shadow:0 20px 40px -18px rgba(194,124,14,.7);opacity:0;transform:translateY(20px) scale(.95);animation:tnbNow 10s infinite}
.tnb-now>span{display:flex;width:40px;height:40px;border-radius:12px;align-items:center;justify-content:center;background:#13294b;color:#ffc53d}.tnb-now>span .tvx-svg{fill:#ffc53d}
.tnb-now b{display:block;font-size:18px}.tnb-now div{font-size:13.5px;font-weight:700}
@keyframes tnbNow{0%,58%{opacity:0;transform:translateY(20px) scale(.95)}64%,90%{opacity:1;transform:none}96%,100%{opacity:0;transform:translateY(20px) scale(.95)}}
.tnb-c1{left:-40px;top:20%}.tnb-c2{right:-36px;bottom:30%}
/* checklist */
.tnb-ck{display:grid;grid-template-columns:1fr 320px;gap:26px;align-items:start;max-width:1080px;margin:0 auto}
.tnb-groups{display:grid;gap:18px}
.tnb-g{padding:20px;border-radius:22px;background:#fff;border:1px solid #dfe8f6;box-shadow:0 18px 36px -30px rgba(9,30,66,.45)}
.tnb-g h3{margin:0 0 12px!important;font-size:13px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--blue)}
.tnb-g ul{list-style:none;margin:0!important;padding:0!important;display:grid;gap:8px}
.tnb-g li{margin:0!important}
.tnb-g label{display:flex;align-items:center;gap:12px;margin:0!important;padding:11px 12px;border-radius:14px;border:1px solid #e6edf6;background:#fbfcfe;cursor:pointer;font-weight:700!important;font-size:15.5px;color:var(--navy);transition:background .2s,border-color .2s,transform .15s;user-select:none}
.tnb-g label:hover{border-color:#9cc1ff;transform:translateX(2px)}
.tnb-g input{position:absolute;opacity:0;width:1px;height:1px;margin:0}
.tnb-bx{flex:none;width:26px;height:26px;border-radius:8px;border:2px solid #b9c8dc;background:#fff;display:flex;align-items:center;justify-content:center;color:#fff;transition:background .2s,border-color .2s,transform .2s}
.tnb-bx .tvx-svg{width:15px;height:15px;stroke-width:3;opacity:0;transform:scale(.4);transition:opacity .2s,transform .25s cubic-bezier(.3,1.6,.5,1)}
.tnb-g input:checked+.tnb-bx{background:#16a37a;border-color:#16a37a}.tnb-g input:checked+.tnb-bx .tvx-svg{opacity:1;transform:none}
.tnb-g input:focus-visible+.tnb-bx{outline:3px solid #8ec5ff;outline-offset:2px}
.tnb-g label:has(input:checked){background:#f0fbf6;border-color:#cdeedd}
.tnb-ii{flex:none;color:#7a8ba3}.tnb-ii .tvx-svg{width:19px;height:19px}
.tnb-t{flex:1;min-width:0;line-height:1.35}
.tnb-g em{flex:none;font-style:normal;font-size:11.5px;font-weight:800;padding:4px 9px;border-radius:999px;background:#e7f0ff;color:var(--blue);white-space:nowrap;transition:opacity .2s}
.tnb-g label:has(input:checked) em{opacity:0}
.tnb-sum{position:relative}
.tnb-sum-in{padding:24px;border-radius:24px;background:linear-gradient(160deg,#0b1f4b,#123a7a);color:#fff;text-align:center;box-shadow:0 30px 60px -36px rgba(9,30,66,.8)}
.tnb-big{position:relative;width:170px;height:170px;margin:0 auto 12px}
.tnb-big svg{width:170px;height:170px;transform:rotate(-90deg)}
.tnb-big .t{fill:none;stroke:rgba(255,255,255,.12);stroke-width:9}.tnb-big .v{fill:none;stroke:#ffc53d;stroke-width:9;stroke-linecap:round;stroke-dasharray:100;stroke-dashoffset:100;transition:stroke-dashoffset .6s cubic-bezier(.2,.8,.2,1),stroke .4s}
.tnb-ck[data-p="hi"] .tnb-big .v,.tnb-ck[data-p="done"] .tnb-big .v{stroke:#5ee0a0}
.tnb-big>div{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center}
.tnb-big b{font-size:44px;line-height:1;font-variant-numeric:tabular-nums}.tnb-big i{font-style:normal;font-size:12px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#bcd4f5;margin-top:4px}
.tnb-msg{margin:0 0 12px!important;font-size:15px;line-height:1.5;color:#dbe7f8;min-height:45px}
.tnb-left{margin:0 0 16px!important;padding:10px;border-radius:12px;background:rgba(255,255,255,.08);font-size:14px;color:#dbe7f8}.tnb-left b{color:#ffc53d;font-size:18px}
.tnb-go{display:block!important;width:100%;box-sizing:border-box;background:#ffc53d!important;color:#13294b!important}
.tvx .tnb-reset{appearance:none;margin:10px 0 0;padding:6px 10px!important;border:0!important;background:none!important;color:#bcd4f5!important;font:inherit;font-size:13.5px!important;font-weight:700!important;text-decoration:underline;cursor:pointer;box-shadow:none!important;height:auto;min-height:0;width:auto;border-radius:8px!important;text-transform:none!important;letter-spacing:0!important}
/* timeline */
.tnb-tl{max-width:1000px;margin:0 auto}
.tnb-track{position:relative;margin-bottom:22px}
.tnb-track .tvx-tabs{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:0;max-width:none;position:relative;z-index:2}
.tnb-track:before,.tnb-fill{content:"";position:absolute;left:12.5%;right:12.5%;top:23px;height:4px;border-radius:4px;background:#dce6f4;z-index:1}
.tnb-fill{right:auto;width:0;background:linear-gradient(90deg,#1d5fbf,#4da3ff,#16a37a);transition:width .6s cubic-bezier(.4,0,.2,1);text-decoration:none}
.tnb-tl[data-cur="t2"] .tnb-fill{width:25%}.tnb-tl[data-cur="t0"] .tnb-fill{width:50%}.tnb-tl[data-cur="t30"] .tnb-fill{width:75%}
.tvx .tnb-ms{flex-direction:column;gap:4px;padding:0!important;border:0!important;background:transparent!important;box-shadow:none!important;color:var(--navy)!important;border-radius:14px!important}
.tvx .tnb-ms:hover{transform:none}
.tnb-ms i{width:50px;height:50px;border-radius:50%;background:#fff;border:3px solid #cfe0f7;margin-bottom:6px;transition:background .3s,border-color .3s,transform .3s;box-sizing:border-box}
.tvx .tnb-ms.on i{background:#1d5fbf;border-color:#fff;box-shadow:0 0 0 4px rgba(29,95,191,.25);transform:scale(1.08)}
.tnb-ms b{font-size:16px}.tnb-ms span{font-size:13.5px;font-weight:700;color:var(--mut)}
.tvx .tnb-ms.on{color:var(--navy)!important;background:transparent!important}
.tnb-tp{max-width:720px;margin:0 auto;padding:24px 26px;border-radius:22px;background:#fff;border:1px solid #dfe8f6;box-shadow:0 22px 44px -32px rgba(9,30,66,.45)}
.tnb-tw{margin:0!important;font-size:12.5px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:#c2410c}
.tnb-tp h3{font-size:24px;margin:2px 0 12px!important}
.tnb-tp ul{list-style:none;margin:0!important;padding:0!important;display:grid;gap:8px}
.tnb-tp li{display:flex;gap:10px;align-items:center;margin:0!important;font-weight:700;color:var(--navy);font-size:16px}.tnb-tp li .tvx-svg{color:#16a37a;width:20px;height:20px}
@media (max-width:1100px){.tnb-c1{left:-10px}.tnb-c2{right:-10px}}
@media (max-width:900px){
 .tnb-hero h1{font-size:36px}
 .tnb-ck{grid-template-columns:1fr}.tnb-sum{order:-1}.tnb-sum-in{display:grid;grid-template-columns:120px 1fr;gap:6px 16px;align-items:center;text-align:left;padding:18px}
 .tnb-big{width:120px;height:120px;margin:0;grid-row:span 3}.tnb-big svg{width:120px;height:120px}.tnb-big b{font-size:32px}.tnb-big i{font-size:10px}
 .tnb-msg{min-height:0;font-size:14px;margin:0!important}.tnb-left{margin:0!important;padding:8px 10px;font-size:13px}.tnb-go{grid-column:1/-1;margin-top:6px}.tnb-reset{grid-column:1/-1;justify-self:center}
 .tnb-g{padding:16px 12px}.tnb-g label{font-size:14.5px;padding:10px;gap:10px}.tnb-ii{display:none}
 .tnb-track .tvx-tabs{gap:4px}.tnb-ms b{font-size:13.5px}.tnb-ms span{display:none}.tnb-ms i{width:40px;height:40px}.tnb-track:before,.tnb-fill{top:18px}
 .tnb-tp{padding:20px 18px}.tnb-tp h3{font-size:21px}.tnb-tp li{font-size:15px;align-items:flex-start}.tnb-tp li .tvx-svg{margin-top:1px}
}
@media (max-width:420px){.tnb-hero h1{font-size:31px}.tnb-g em{display:none}.tnb-sum-in{grid-template-columns:100px 1fr;gap:6px 12px}.tnb-big{width:100px;height:100px}.tnb-big svg{width:100px;height:100px}.tnb-big b{font-size:27px}.tnb-ms b{font-size:12px;line-height:1.2}.tnb-cd b{font-size:22px}.tnb-cd span{font-size:10px;letter-spacing:.04em}.tnb-board{padding:16px}.tnb-hl li{font-size:13.5px}}
'''

if __name__ == "__main__":
    K.page("New Business Launch", "new-business-launch",
           "New Business Launch: Website, Google, Social Media and Grand Opening | Three Village Local",
           "Opening a business in Setauket, Stony Brook or Port Jefferson? We set up your website, Google and Apple listings, social media and promo video, then launch you to the whole town with a Three Village Local spotlight.",
           "Launch with the whole town watching",
           [HERO, NAV, CHECK, TIMELINE, INC, STATS, HOW, FAQ, REL, CTA], bundle="new_open", css=CSS, js=JS, fb_image="/share/svc-new-business-launch-v1.jpg")
    K.main()
