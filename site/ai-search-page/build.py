"""AI search optimization service page: get recommended by ChatGPT, Gemini, Google AI, Copilot, Perplexity and Claude.
Owner 11/12/2026: every service on /services gets its own premium interactive page. No prices. CTA -> /free-ai-report + free plan form.
    python site/ai-search-page/build.py          -> widget "3VL Page AI Search Preview" + hidden /preview-ai-search (noindex)
    (--live -> /ai-search only after the owner's OK)"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "svc-kit"))
import kit as K
from kit import ic

PLATS = ["ChatGPT", "Gemini", "Google AI Overviews", "Microsoft Copilot", "Perplexity", "Claude"]
SHORT = {"Google AI Overviews": "Google AI", "Microsoft Copilot": "Copilot"}
pbtn = "".join('<button class="tai-pb%s" data-p="%d" aria-label="%s">%s<span>%s</span></button>' % (" on" if n == 0 else "", n, p, K.AILOGO[p], SHORT.get(p, p)) for n, p in enumerate(PLATS))
logos = "".join('<i data-p="%d">%s</i>' % (n, K.AILOGO[p]) for n, p in enumerate(PLATS))
QS = [("bakery", "Bakery"), ("plumber", "Plumber"), ("dentist", "Dentist"), ("pizza", "Pizza"), ("landscaper", "Landscaper")]
qbtn = "".join('<button class="tai-qb%s" data-q="%s">%s</button>' % (" on" if n == 0 else "", k, t) for n, (k, t) in enumerate(QS))

HERO_VIS = '''<div class="tai-demo" id="tai-demo">
  <div class="tai-plats" role="group" aria-label="Pick an AI tool">''' + pbtn + '''</div>
  <div class="tai-win" aria-live="polite">
    <div class="tai-head"><span class="tai-lg">''' + logos + '''</span><b class="tai-name">ChatGPT</b><em>''' + ic("sparkle") + '''AI answer</em></div>
    <div class="tai-body">
      <p class="tai-q"><span class="tai-qt">What&#39;s the best bakery near Setauket?</span><i class="tai-cur"></i></p>
      <div class="tai-think"><i></i><i></i><i></i></div>
      <div class="tai-sk" aria-hidden="true"><u></u><u></u><u class="s"></u><u></u><u class="s"></u></div>
      <div class="tai-a">
        <p class="tai-intro">Here are a few local favorites near Setauket, NY:</p>
        <div class="tai-pick"><span class="tai-n">1</span><div><b class="tai-biz">Your Bakery</b><em>&#9733;&#9733;&#9733;&#9733;&#9733; 4.9 on Google</em><p class="tai-why">Known for bread baked fresh every morning and custom cakes. Locals call it a Main Street favorite.</p></div></div>
        <div class="tai-other"><span class="tai-n">2</span><div><u></u><u class="s"></u></div></div>
        <div class="tai-other"><span class="tai-n">3</span><div><u></u><u class="s"></u></div></div>
        <p class="tai-src"><span>Sources</span><i>threevillagelocal.com</i><i>Google Business Profile</i><i>yourbakery.com</i></p>
      </div>
    </div>
    <div class="tai-in"><span>Ask anything</span><b>''' + ic("arrow") + '''</b></div>
  </div>
  <div class="tai-qs" role="group" aria-label="Try another search"><span>Try:</span>''' + qbtn + '''</div>
</div>'''

HERO = K.hero("AI search optimization", "Get recommended", "by AI.",
              "When locals ask ChatGPT, Gemini, Google AI, Copilot, Perplexity or Claude who to call, we help make sure your business is the answer. We fix what AI reads, so it can find you, understand you and trust you.",
              HERO_VIS, ("Get a free AI check", "/free-ai-report"), cls="tai-hero")

NAV = K.snav([("why", "Why now"), ("fix", "What we fix"), ("report", "Sample report"), ("check", "Free AI check"), ("how", "How it works"), ("faq", "FAQ")])

STRIP = K.P.A.W.STRIP_SEC.replace("<p>Get recommended on the AI tools your customers use</p>", "<p>We help you get found and recommended on</p>")

WHY = '''<section class="tvs-sec tvx-sec tvx-dark tai-why" id="tvp-why">
  <div class="tvs-head tvs-up"><p class="tvs-eyebrow">The shift is already happening</p><h2>Your next customer is asking AI who to call.<br><span class="tai-y">Is it saying your name?</span></h2>
  <p>Nearly half of people now use AI tools like ChatGPT and Google&#39;s AI to find local businesses (BrightLocal, 2026). AI recommends the businesses it can read, understand and trust. If yours isn&#39;t one of them, those customers go to whoever is.</p></div>
  <div class="tai-ba tvs-up" id="tai-ba" data-s="before">
    <div class="tai-sw" role="group" aria-label="Before and after"><button type="button" class="tai-swb on" data-s="before">Before</button><button type="button" class="tai-swb" data-s="after">After</button><i></i></div>
    <div class="tai-bac">
      <p class="tai-baq">''' + ic("search") + '''&ldquo;Who&#39;s a good plumber near Stony Brook?&rdquo;</p>
      <div class="tai-bab tai-bef"><p>I couldn&#39;t find much about plumbers in that exact area. You might try searching online directories or asking neighbors for a recommendation.</p><span class="tai-bad">''' + ic("eye") + '''Your business: not mentioned</span></div>
      <div class="tai-bab tai-aft"><p><b>Your Plumbing Co.</b> is a well-reviewed local plumber serving Stony Brook and Setauket. Customers mention fast response times and upfront quotes. You can call them or book on their website.</p><span class="tai-good">''' + ic("check") + '''Your business: recommended first</span></div>
    </div>
  </div>
</section>'''

FIX = [("pin", "Google Business Profile", "The number one source for local answers.", ["Categories, services, hours and area complete", "Fresh photos and posts that show you&#39;re active", "A description written the way people ask"]),
       ("link", "Listings everywhere", "Same name, address and phone across the web.", ["Apple Maps, Bing Places, Yelp and key directories", "Duplicate and outdated listings cleaned up", "Your Three Village Local profile tuned too"]),
       ("code", "Business facts code", "Schema markup that AI can read.", ["Hours, service area and services spelled out", "FAQ and review details where they fit", "Tested with Google&#39;s own tools"]),
       ("article", "AI-readable pages", "Pages that answer real questions.", ["Clear service and location pages", "FAQs written how customers actually ask", "Page titles and descriptions rewritten"]),
       ("star", "Reviews", "The trust signal AI leans on.", ["A simple plan to earn more Google reviews", "Reply templates in your own voice", "Review links for texts, emails and receipts"]),
       ("bot", "llms.txt and AI access", "Nothing blocking AI from your site.", ["An llms.txt file that sums up your business", "Robots settings that let AI crawlers in", "Google Search Console and Bing Webmaster set up"])]
acc = ["#1d5fbf", "#16a37a", "#4a5fd6", "#0f8fb8", "#e0a82e", "#d2557a"]
fx = "".join('<details class="tai-fx tvs-up" style="--ac:%s"><summary><span class="tvx-ic">%s</span><div><h3>%s</h3><p>%s</p></div><em>%s</em></summary><ul>%s</ul></details>' % (
    acc[n], ic(i), t, s, "+", "".join("<li>%s%s</li>" % (ic("check"), x) for x in li)) for n, (i, t, s, li) in enumerate(FIX))
FIXSEC = K.sec("fix", "What we fix", "Six things AI checks before it recommends you.",
               "Tap any card to see exactly what we do. We handle all of it on the website and listings you already have.",
               '<div class="tai-fxg">' + fx + '</div>')

ROWS = [("Google Business Profile complete", "Missing services and photos"), ("Name, address and phone match everywhere", "3 listings don&#39;t match"),
        ("Business facts code on your site", "None found"), ("FAQs AI can quote", "No FAQ page"), ("Review strategy in place", "Few recent reviews"), ("AI crawlers allowed", "Blocked by a setting")]
rows = "".join('<li style="--i:%d"><span class="tai-x">%s</span><span class="tai-ok">%s</span><div><b>%s</b><i>%s</i></div></li>' % (n, "&#10005;", ic("check"), a, b) for n, (a, b) in enumerate(ROWS))
REPORT = K.sec("report", "Before and after", "See exactly where you stand, then watch it climb.",
               "Every client gets a before and after &ldquo;Can AI find you?&rdquo; report. Here is what one looks like.",
               '''<div class="tai-rep tvs-up" id="tai-rep" data-run>
    <div class="tai-gauge"><svg viewBox="0 0 120 120" aria-hidden="true"><circle cx="60" cy="60" r="52" class="tai-gt"/><circle cx="60" cy="60" r="52" class="tai-gv" pathLength="100"/></svg>
      <div><b id="tai-score">88</b><span>AI visibility score</span></div><p class="tai-gl"><span class="tai-bef-l">Before</span><span class="tai-aft-l">After</span></p></div>
    <div class="tai-rl"><p class="tai-rk">Sample report &middot; Your Business</p><ul>''' + rows + '''</ul>
      <button type="button" class="tai-replay">''' + ic("sparkle") + '''Run it again</button></div>
  </div>''')

CHECK = '''<section class="tvs-sec tvx-sec tai-ck" id="tvp-check">
  <div class="tai-ck-in tvs-up">
    <div class="tai-ck-t"><p class="tvs-eyebrow">Free, takes 1 minute</p><h2>Does ChatGPT recommend your business?</h2><p>Get a free AI visibility check. We look at how AI tools see your business today and send you what to fix first.</p>
      <div class="tvx-ctas"><a class="tvs-btn tvw-btn-w" href="/free-ai-report">Get my free AI check</a><a class="tvs-btn tvw-btn-o" href="#tvs-book">Or get a full free plan</a></div></div>
    <div class="tai-ck-v" aria-hidden="true"><div class="tai-orbit">''' + "".join('<span style="--a:%ddeg">%s</span>' % (n * 60, K.AILOGO[p]) for n, p in enumerate(PLATS)) + '''<b>''' + ic("store") + '''<i>You</i></b></div></div>
  </div>
</section>'''

HOW = K.sec("how", "How it works", "Done for you, start to finish.", "",
            K.steps([("Free AI check", "We see how ChatGPT, Google and other AI tools describe you today."),
                     ("Your plan", "A clear list of what to fix first, in plain English."),
                     ("We fix it", "Listings, website, business facts code, FAQs and reviews."),
                     ("Before and after", "A report that shows what changed and what&#39;s next.")]))

FAQ = K.faq([
    ("Can you guarantee ChatGPT will recommend me?", "No one can honestly guarantee what an AI tool will say. What we do is make your business easy for AI to find, read and trust, using the same signals these tools rely on, and we show you the before and after."),
    ("Which AI tools does this help with?", "ChatGPT, Gemini, Google AI Overviews, Microsoft Copilot, Perplexity, Claude, Meta AI and Siri all lean on the same kinds of signals: your Google, Bing and Apple listings, your website, your reviews and trusted local sites like Three Village Local."),
    ("Do I need a new website?", "No. We work on the website and listings you already have, whether it is on Wix, Squarespace, WordPress, GoDaddy, Shopify or a custom site."),
    ("Is this the same as SEO?", "It builds on SEO. Classic SEO helps you rank in a list of links. AI search optimization makes your business facts clear and consistent so AI tools can quote you in their answers."),
    ("What is llms.txt?", "A short, plain-text summary of your business placed on your website for AI tools to read: who you are, what you do, where you work and how to reach you."),
    ("How long until I see a difference?", "Some fixes, like listings and your Google profile, can show up within weeks. AI tools refresh on their own schedules, which is why we measure with a before and after report."),
    ("What is the free AI check?", "A quick look at how AI tools see your business today. It is free, takes about a minute to request, and we send the results by email."),
])

REL = K.related("ai-search", ["ai-assistant", "websites", "social-media", "new-business-launch", "email-articles", "promo-video"])
CTA = K.cta("Be the answer", "Let&#39;s get AI saying your name.", "Tell us about your business and we&#39;ll send a free plan by email.", ("Get a free AI check", "/free-ai-report"))

JS = ''';(function(){var d=document.getElementById('tai-demo');if(!d)return;var RM=window.tvxRM;
var P=['ChatGPT','Gemini','Google AI Overviews','Microsoft Copilot','Perplexity','Claude'];
var Q={bakery:['What&#39;s the best bakery near Setauket?','Here are a few local favorites near Setauket, NY:','Your Bakery','4.9 on Google','Known for bread baked fresh every morning and custom cakes. Locals call it a Main Street favorite.','yourbakery.com'],
plumber:['Who&#39;s a reliable plumber near Stony Brook?','These local plumbers get strong reviews around Stony Brook:','Your Plumbing Co.','5.0 on Google','Licensed, answers fast and gives upfront quotes. Customers mention same-day help with leaks.','yourplumbing.com'],
dentist:['Best family dentist in Port Jefferson?','Families in Port Jefferson often recommend:','Your Dental Studio','4.9 on Google','Gentle with kids, evening hours and a friendly front desk. Accepting new patients.','yourdental.com'],
pizza:['Where should I get pizza tonight in Setauket?','Good choices for pizza tonight around Setauket:','Your Pizzeria','4.8 on Google','Classic thin crust and grandma pies, open late, with online ordering and pickup.','yourpizzeria.com'],
landscaper:['Can you recommend a landscaper in East Setauket?','Well-reviewed landscapers serving East Setauket:','Your Landscaping','5.0 on Google','Weekly maintenance, fall cleanups and design. Quick free estimates.','yourlandscaping.com']};
var keys=['bakery','plumber','dentist','pizza','landscaper'],pi=0,qi=0,timers=[],running=false,auto=true,vis=false;
var qt=d.querySelector('.tai-qt'),win=d.querySelector('.tai-win'),nm=d.querySelector('.tai-name');
function T(f,ms){timers.push(setTimeout(f,ms));}
function clear(){timers.forEach(clearTimeout);timers=[];}
function setP(i){pi=i;[].forEach.call(d.querySelectorAll('.tai-pb'),function(b){var on=+b.getAttribute('data-p')===i;b.classList.toggle('on',on);b.setAttribute('aria-pressed',on?'true':'false');});
 [].forEach.call(d.querySelectorAll('.tai-lg i'),function(x){x.classList.toggle('on',+x.getAttribute('data-p')===i);});nm.textContent=P[i];win.setAttribute('data-p',i);}
function setQ(i){qi=i;var k=keys[i],q=Q[k];[].forEach.call(d.querySelectorAll('.tai-qb'),function(b){var on=b.getAttribute('data-q')===k;b.classList.toggle('on',on);b.setAttribute('aria-pressed',on?'true':'false');});
 d.querySelector('.tai-intro').innerHTML=q[1];d.querySelector('.tai-biz').textContent=q[2];d.querySelector('.tai-pick em').innerHTML='&#9733;&#9733;&#9733;&#9733;&#9733; '+q[3];d.querySelector('.tai-why').textContent=q[4];
 var s=d.querySelectorAll('.tai-src i');s[2].textContent=q[5];return q;}
function play(){clear();var q=setQ(qi);var tmp=document.createElement('div');tmp.innerHTML=q[0];var text=tmp.textContent;win.className='tai-win s-type';win.setAttribute('data-p',pi);
 if(RM){qt.textContent=text;win.className='tai-win s-done';return;}
 qt.textContent='';var n=0;(function ty(){n++;qt.textContent=text.slice(0,n);if(n<text.length)T(ty,28+Math.random()*30);else T(function(){win.className='tai-win s-think';T(function(){win.className='tai-win s-done';if(auto)T(next,6200);},1100);},350);})();}
function next(){if(!auto||!vis)return;setP((pi+1)%P.length);setQ((qi+1)%keys.length);play();}
[].forEach.call(d.querySelectorAll('.tai-pb'),function(b){b.addEventListener('click',function(){auto=false;setP(+b.getAttribute('data-p'));play();if(window.tvxGA)tvxGA('svc_page_demo',{ai:P[pi]});});});
[].forEach.call(d.querySelectorAll('.tai-qb'),function(b){b.addEventListener('click',function(){auto=false;setQ(keys.indexOf(b.getAttribute('data-q')));play();if(window.tvxGA)tvxGA('svc_page_demo',{q:keys[qi]});});});
setP(0);setQ(0);
if('IntersectionObserver' in window){new IntersectionObserver(function(es){var v=es[0].isIntersecting;if(v&&!vis){vis=true;if(!running){running=true;play();}else if(auto){play();}}else if(!v&&vis){vis=false;clear();}},{threshold:.2}).observe(d);}else{vis=true;play();}
})();
;(function(){var b=document.getElementById('tai-ba');if(!b)return;var bs=[].slice.call(b.querySelectorAll('.tai-swb')),user=false;
function set(s){b.setAttribute('data-s',s);bs.forEach(function(x){var on=x.getAttribute('data-s')===s;x.classList.toggle('on',on);x.setAttribute('aria-pressed',on?'true':'false');});}
bs.forEach(function(x){x.addEventListener('click',function(){user=true;set(x.getAttribute('data-s'));if(window.tvxGA)tvxGA('svc_page_toggle',{state:x.getAttribute('data-s')});});});
set('before');if('IntersectionObserver' in window&&!window.tvxRM){var done=false;new IntersectionObserver(function(es){if(es[0].isIntersecting&&!done){done=true;setTimeout(function(){if(!user)set('after');},2200);}},{threshold:.6}).observe(b);}})();
;(function(){var r=document.getElementById('tai-rep');if(!r)return;var sc=document.getElementById('tai-score'),t=[];
function run(){t.forEach(clearTimeout);t=[];r.classList.remove('go');void r.offsetWidth;sc.textContent='34';if(window.tvxRM){r.classList.add('go');sc.textContent='88';return;}
 t.push(setTimeout(function(){r.classList.add('go');var a=34,b=88,s=null;function st(ts){if(!s)s=ts;var k=Math.min(1,(ts-s)/2600);sc.textContent=Math.round(a+(b-a)*(1-Math.pow(1-k,3)));if(k<1)requestAnimationFrame(st);}requestAnimationFrame(st);},500));}
var did=false;if('IntersectionObserver' in window){new IntersectionObserver(function(es){if(es[0].isIntersecting&&!did){did=true;run();}},{threshold:.35}).observe(r);}else run();
var rb=r.querySelector('.tai-replay');if(rb)rb.addEventListener('click',run);})();'''

CSS = '''
.tai-hero{grid-template-columns:1fr 1fr}
.tai-hero .tvx-hvis{min-height:0}
.tai-demo{width:100%;max-width:500px}
.tai-plats,.tai-qs{display:flex;flex-wrap:wrap;gap:6px;justify-content:center}
.tai-plats{margin-bottom:12px}
.tvx .tai-pb,.tvx .tai-qb,.tvx .tai-swb,.tvx .tai-replay{appearance:none;-webkit-appearance:none;display:inline-flex;align-items:center;gap:6px;margin:0;font:inherit;cursor:pointer;line-height:1.2!important;box-shadow:none!important;text-transform:none!important;letter-spacing:0!important;height:auto;min-height:0;width:auto}
.tvx .tai-pb{padding:7px 11px!important;border-radius:999px!important;border:1px solid #dbe4f0!important;background:#fff!important;color:var(--navy)!important;font-size:13px!important;font-weight:800!important;transition:border-color .2s,background .2s,transform .2s}
.tai-pb svg{width:16px!important;height:16px!important;flex:none}
.tvx .tai-pb.on{border-color:var(--navy)!important;background:#13294b!important;color:#fff!important}
.tvx .tai-pb:hover{transform:translateY(-1px)}
.tai-win{position:relative;border-radius:22px;background:#fff;box-shadow:0 40px 80px -40px rgba(9,30,66,.6),0 0 0 1px rgba(15,42,82,.08);overflow:hidden}
.tai-head{display:flex;align-items:center;gap:10px;padding:13px 16px;border-bottom:1px solid #edf1f6}
.tai-lg{position:relative;width:26px;height:26px;flex:none}
.tai-lg i{position:absolute;inset:0;opacity:0;transform:scale(.6);transition:opacity .3s,transform .3s}.tai-lg i.on{opacity:1;transform:none}
.tai-lg svg{width:26px!important;height:26px!important;display:block}
.tai-name{font-size:16px;color:var(--navy)}
.tai-head em{margin-left:auto;display:inline-flex;align-items:center;gap:5px;font-style:normal;font-size:12px;font-weight:800;color:var(--mut);letter-spacing:.06em;text-transform:uppercase}.tai-head em .tvx-svg{width:14px;height:14px;color:#2f7de1}
.tai-body{padding:16px 16px 10px;min-height:322px}
.tai-q{display:flex;justify-content:flex-end;margin:0 0 14px!important}
.tai-qt{max-width:85%;padding:10px 14px;border-radius:18px 18px 4px 18px;background:#eef3fb;color:var(--navy);font-weight:700;font-size:15px;line-height:1.4;min-height:41px}
.tai-cur{display:none;width:2px;height:18px;background:var(--blue);align-self:center;margin-left:3px;animation:taiBlink .8s steps(1) infinite}
.s-type .tai-cur{display:block}
@keyframes taiBlink{50%{opacity:0}}
.tai-think{display:none;gap:5px;padding:6px 2px}.s-think .tai-think{display:flex}
.tai-think i{width:8px;height:8px;border-radius:50%;background:#9db4d3;animation:taiDot 1s infinite}.tai-think i:nth-child(2){animation-delay:.15s}.tai-think i:nth-child(3){animation-delay:.3s}
@keyframes taiDot{0%,100%{transform:translateY(0);opacity:.5}50%{transform:translateY(-5px);opacity:1}}
.tai-a{display:none}.s-done .tai-a{display:block}.tai-sk{padding:4px 0}.s-done .tai-sk{display:none}.tai-sk u{display:block;height:12px;border-radius:6px;margin:0 0 12px;text-decoration:none;background:linear-gradient(90deg,#eef2f7 25%,#f8fafc 50%,#eef2f7 75%);background-size:200% 100%;animation:taiSh 1.4s linear infinite}.tai-sk u.s{width:62%}.tai-sk u:nth-child(3){margin-bottom:22px}@keyframes taiSh{from{background-position:200% 0}to{background-position:0 0}}
.s-done .tai-a>*{animation:tvxUp .5s both}.s-done .tai-a>*:nth-child(2){animation-delay:.12s}.s-done .tai-a>*:nth-child(3){animation-delay:.3s}.s-done .tai-a>*:nth-child(4){animation-delay:.4s}.s-done .tai-a>*:nth-child(5){animation-delay:.55s}
.tai-intro{margin:0 0 10px!important;font-size:15px;color:var(--ink);line-height:1.45}
.tai-pick,.tai-other{display:flex;gap:10px;align-items:flex-start;padding:11px 12px;border-radius:14px;margin-bottom:8px}
.tai-pick{background:linear-gradient(120deg,#eef5ff,#ecfbf4);border:1px solid #cfe3fb;box-shadow:0 10px 24px -18px rgba(29,95,191,.6)}
.tai-n{flex:none;width:24px;height:24px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:#13294b;color:#fff;font-size:12.5px;font-weight:800}
.tai-other .tai-n{background:#dbe3ee;color:#7a8696}
.tai-pick b{font-size:16px;color:var(--navy);background:linear-gradient(transparent 62%,rgba(255,197,61,.55) 62%)}
.tai-pick em{display:block;font-style:normal;font-size:12.5px;color:#c27c0e;font-weight:800;margin:2px 0 3px}
.tai-why{margin:0!important;font-size:14px;line-height:1.45;color:var(--ink2)}
.tai-other div{flex:1;padding-top:3px}.tai-other u{display:block;height:9px;border-radius:5px;background:#edf1f6;margin-bottom:7px;text-decoration:none}.tai-other u.s{width:60%}
.tai-src{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin:6px 0 0!important}
.tai-src span{font-size:11.5px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--mut);margin-right:2px}
.tai-src i{font-style:normal;font-size:12px;font-weight:700;padding:4px 9px;border-radius:999px;background:#f2f5f9;color:var(--ink2)}
.tai-src i:first-of-type{background:#e7f0ff;color:var(--blue)}
.tai-in{display:flex;align-items:center;justify-content:space-between;margin:0 14px 14px;padding:10px 10px 10px 16px;border-radius:999px;border:1px solid #e1e8f2;color:#9aa6b6;font-size:14px}
.tai-in b{width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:#13294b;color:#fff}.tai-in .tvx-svg{width:16px;height:16px}
.tai-win[data-p="1"] .tai-in b{background:#4285f4}.tai-win[data-p="2"] .tai-in b{background:#34a853}.tai-win[data-p="3"] .tai-in b{background:#0078d4}.tai-win[data-p="4"] .tai-in b{background:#20808d}.tai-win[data-p="5"] .tai-in b{background:#d97757}
.tai-qs{margin-top:12px;align-items:center}
.tai-qs>span{font-size:12.5px;font-weight:800;color:var(--mut);letter-spacing:.08em;text-transform:uppercase;margin-right:2px}
.tvx .tai-qb{padding:6px 12px!important;border-radius:999px!important;border:1px dashed #b9cbe3!important;background:transparent!important;color:var(--blue)!important;font-size:13.5px!important;font-weight:800!important}
.tvx .tai-qb.on{border-style:solid!important;background:#e7f0ff!important}
/* why now */
.tai-y{color:#ffc53d}
.tai-ba{max-width:760px;margin:0 auto}
.tai-sw{position:relative;display:flex;width:240px;margin:0 auto 18px;padding:4px;border-radius:999px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.18)}
.tvx .tai-swb{position:relative;z-index:2;flex:1;justify-content:center;padding:9px 0!important;border:0!important;border-radius:999px!important;background:transparent!important;color:#cdddf3!important;font-weight:800!important;font-size:14.5px!important;transition:color .3s}
.tvx .tai-swb.on{color:#0b1f4b!important}
.tai-sw i{position:absolute;z-index:1;left:4px;top:4px;bottom:4px;width:calc(50% - 4px);border-radius:999px;background:#fff;transition:transform .45s cubic-bezier(.6,0,.2,1)}
.tai-ba[data-s="after"] .tai-sw i{transform:translateX(100%);background:#5ee0a0}
.tai-bac{position:relative;padding:22px;border-radius:22px;background:#fff;color:var(--ink);box-shadow:0 30px 60px -30px rgba(0,0,0,.6)}
.tai-baq{display:flex;align-items:center;gap:9px;margin:0 0 14px!important;font-weight:800;color:var(--navy);font-size:16px}.tai-baq .tvx-svg{color:var(--blue);width:20px;height:20px}
.tai-bab{display:none;animation:tvxUp .45s both}
.tai-ba[data-s="before"] .tai-bef,.tai-ba[data-s="after"] .tai-aft{display:block}
.tai-bab p{margin:0 0 14px!important;font-size:16px;line-height:1.6;color:var(--ink2)}
.tai-bef p{color:#7a8696}
.tai-aft b{color:var(--navy);background:linear-gradient(transparent 62%,rgba(255,197,61,.55) 62%)}
.tai-bad,.tai-good{display:inline-flex;align-items:center;gap:7px;padding:7px 12px;border-radius:999px;font-weight:800;font-size:13.5px}
.tai-bad{background:#fdecec;color:#c0392b}.tai-good{background:#e3f7ee;color:#0d7760}
.tai-bad .tvx-svg,.tai-good .tvx-svg{width:16px;height:16px}
/* what we fix */
.tai-fxg{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;max-width:1080px;margin:0 auto;align-items:start}
.tai-fx{position:relative;border-radius:20px;background:#fff;border:1px solid #dfe8f6;box-shadow:0 16px 34px -26px rgba(9,30,66,.4);overflow:hidden;transition:opacity .7s ease,transform .5s ease,box-shadow .25s}
.tai-fx:before{content:"";position:absolute;left:0;right:0;top:0;height:4px;background:var(--ac)}
.tai-fx summary{display:grid;grid-template-columns:auto 1fr auto;gap:14px;align-items:start;padding:22px 20px;cursor:pointer;list-style:none}
.tai-fx summary::-webkit-details-marker{display:none}
.tai-fx h3{font-size:18px;margin:2px 0 4px!important}.tai-fx summary p{margin:0!important;font-size:14.5px;line-height:1.45;color:var(--mut)}
.tai-fx summary em{font-style:normal;width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:#f1f5fb;color:var(--blue);font-weight:800;font-size:18px;transition:transform .3s,background .3s}
.tai-fx[open] summary em{transform:rotate(45deg);background:var(--ac);color:#fff}
.tai-fx:hover{box-shadow:0 24px 44px -26px rgba(9,30,66,.45)}
.tai-fx ul{list-style:none;margin:0!important;padding:0 20px 20px 82px!important;display:grid;gap:8px}
.tai-fx li{display:flex;gap:8px;margin:0!important;font-size:14.5px;line-height:1.4;font-weight:700;color:var(--navy);animation:tvxUp .4s both}
.tai-fx li:nth-child(2){animation-delay:.08s}.tai-fx li:nth-child(3){animation-delay:.16s}
.tai-fx li .tvx-svg{width:18px;height:18px;color:#16a37a}
/* report */
.tai-rep{display:grid;grid-template-columns:300px 1fr;gap:36px;align-items:center;max-width:960px;margin:0 auto;padding:30px;border-radius:26px;background:#fff;border:1px solid #dfe8f6;box-shadow:0 26px 50px -36px rgba(9,30,66,.5)}
.tai-gauge{position:relative;text-align:center}
.tai-gauge svg{width:240px;height:240px;transform:rotate(-90deg)}
.tai-gt{fill:none;stroke:#edf1f6;stroke-width:10}
.tai-gv{fill:none;stroke:#e0a82e;stroke-width:10;stroke-linecap:round;stroke-dasharray:100;stroke-dashoffset:66;transition:stroke-dashoffset 2.6s cubic-bezier(.2,.8,.2,1),stroke 2.6s}
.tai-rep.go .tai-gv{stroke-dashoffset:12;stroke:#16a37a}
.tai-gauge>div{position:absolute;left:0;right:0;top:50%;transform:translateY(-60%)}
.tai-gauge b{display:block;font-size:58px;line-height:1;color:var(--navy);font-variant-numeric:tabular-nums}
.tai-gauge>div span{display:block;max-width:130px;margin:4px auto 0;font-size:11.5px;line-height:1.3;font-weight:800;color:var(--mut);letter-spacing:.06em;text-transform:uppercase}
.tai-gl{margin:6px 0 0!important;font-weight:800;font-size:14px}.tai-aft-l{display:none;color:#0d7760}.tai-bef-l{color:#c27c0e}
.tai-rep.go .tai-aft-l{display:inline}.tai-rep.go .tai-bef-l{display:none}
.tai-rk{margin:0 0 12px!important;font-size:12.5px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--blue)}
.tai-rl ul{list-style:none;margin:0!important;padding:0!important;display:grid;gap:8px}
.tai-rl li{display:grid;grid-template-columns:28px 1fr;gap:12px;align-items:center;margin:0!important;padding:10px 12px;border-radius:12px;background:#f8fafd;border:1px solid #edf1f6;transition:background .4s,border-color .4s;transition-delay:calc(.35s*var(--i) + .4s)}
.tai-x,.tai-ok{grid-row:1;grid-column:1;width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;transition:opacity .3s,transform .3s;transition-delay:calc(.35s*var(--i) + .4s)}
.tai-x{background:#fdecec;color:#c0392b;font-size:13px}.tai-ok{background:#16a37a;color:#fff;opacity:0;transform:scale(.4)}.tai-ok .tvx-svg{width:16px;height:16px}
.tai-rl li>div{grid-column:2;grid-row:1}
.tai-rl b{display:block;font-size:15px;color:var(--navy)}.tai-rl i{display:block;font-style:normal;font-size:13px;color:#c0392b;transition:color .3s;transition-delay:calc(.35s*var(--i) + .4s)}
.tai-rep.go li{background:#f0fbf6;border-color:#cdeedd}.tai-rep.go .tai-ok{opacity:1;transform:none}.tai-rep.go .tai-x{opacity:0}.tai-rep.go .tai-rl i{color:transparent}
.tai-rl i:after{content:"Fixed";position:absolute;left:0;top:0;color:#0d7760;opacity:0;transition:opacity .3s;transition-delay:calc(.35s*var(--i) + .4s)}.tai-rep.go .tai-rl i:after{opacity:1}
.tai-rl i{position:relative;white-space:nowrap;overflow:hidden}
.tvx .tai-replay{margin-top:14px!important;padding:9px 14px!important;border-radius:999px!important;border:1px solid #d3dff0!important;background:#fff!important;color:var(--blue)!important;font-weight:800!important;font-size:14px!important}
.tai-replay .tvx-svg{width:16px;height:16px}
/* free check */
.tai-ck-in{display:grid;grid-template-columns:1.2fr .8fr;gap:30px;align-items:center;max-width:1080px;margin:0 auto;padding:44px 46px;border-radius:30px;background:radial-gradient(500px 300px at 90% 20%,rgba(94,224,160,.25),transparent 60%),linear-gradient(130deg,#0b1f4b,#1d5fbf 70%,#16a37a);color:#fff;overflow:hidden}
.tai-ck-in h2{color:#fff!important;font-size:38px;line-height:1.1;margin:0 0 12px!important}
.tai-ck-in .tvs-eyebrow{color:#ffc53d!important}
.tai-ck-t>p{color:#dbe7f8;font-size:17px;line-height:1.6;margin:0 0 22px!important}
.tai-ck-v{display:flex;justify-content:center}
.tai-orbit{position:relative;width:240px;height:240px;border-radius:50%;border:2px dashed rgba(255,255,255,.3);animation:taiSpin 30s linear infinite}
.tai-orbit span{position:absolute;left:50%;top:50%;width:46px;height:46px;margin:-23px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;transform:rotate(var(--a)) translate(120px) rotate(calc(-1*var(--a)));box-shadow:0 10px 24px -10px rgba(0,0,0,.5)}
.tai-orbit span svg{width:24px!important;height:24px!important;animation:taiSpin 30s linear infinite reverse}
.tai-orbit>b{position:absolute;left:50%;top:50%;width:96px;height:96px;margin:-48px;border-radius:50%;background:#ffc53d;color:#13294b;display:flex;flex-direction:column;align-items:center;justify-content:center;animation:taiSpin 30s linear infinite reverse;box-shadow:0 0 0 12px rgba(255,197,61,.2)}
.tai-orbit>b i{font-style:normal;font-size:14px;font-weight:800}
@keyframes taiSpin{to{transform:rotate(360deg)}}
.tai-orbit span{animation:none}
@media (max-width:1100px){.tai-fxg{grid-template-columns:repeat(2,1fr)}}
@media (max-width:900px){
 .tai-hero{grid-template-columns:1fr}.tai-body{min-height:300px}
 .tai-fxg{grid-template-columns:1fr}.tai-fx ul{padding-left:20px!important}
 .tai-rep{grid-template-columns:1fr;padding:22px 16px;gap:18px}.tai-gauge svg{width:200px;height:200px}.tai-gauge b{font-size:50px}
 .tai-ck-in{grid-template-columns:1fr;padding:32px 20px;text-align:center}.tai-ck-in h2{font-size:29px}.tai-ck-in .tvx-ctas{justify-content:center}.tai-orbit{width:190px;height:190px}.tai-orbit span{transform:rotate(var(--a)) translate(95px) rotate(calc(-1*var(--a)))}.tai-ck-v{order:-1}
}
@media (max-width:420px){.tai-pb span{display:none}.tvx .tai-pb{padding:8px 10px!important}.tai-pb svg{width:20px!important;height:20px!important}.tai-body{min-height:330px;padding:14px 12px 8px}.tai-qt{font-size:14px}.tai-bac{padding:16px}.tai-bab p{font-size:15px}.tai-head em{display:none}}
'''

if __name__ == "__main__":
    html = K.page("AI Search", "ai-search",
                  "AI Search Optimization: Get Recommended by ChatGPT, Gemini and Google AI | Three Village Local",
                  "Get your business recommended by ChatGPT, Gemini, Google AI Overviews, Copilot, Perplexity and Claude. We fix your Google Business Profile, listings, schema, AI-readable pages, reviews and llms.txt. Free AI visibility check.",
                  "Get recommended by ChatGPT, Gemini and Google AI",
                  [HERO, NAV, WHY, FIXSEC, REPORT, CHECK, HOW, FAQ, REL, CTA], bundle="ai_tuneup", css=CSS, js=JS, fb_image="/share/svc-ai-search-v1.jpg")
    K.main()
