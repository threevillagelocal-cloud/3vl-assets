"""Website sign-up flow (owner 10/21/2026, changed same day): "Get started" -> /website-start (project brief form, BD form website_intake
with uploads) -> BD redirects to /website-thanks -> we call to set up a free consultation, then the owner invoices. NO payment on the site.
    python site/websites-page/intake.py   -> both pages (always noindex; they are steps, not landing pages)
Plan keys/links come from 3vl-private/website-offer/stripe.json (web-ready-member, web-powered-regular, ...)."""
import json, os, sys, importlib
HERE = os.path.dirname(os.path.abspath(__file__))
SV = os.path.join(HERE, "..", "services-page")
sys.path.insert(0, SV)

LINKS = json.load(open("C:/Users/Matt/Documents/3vl-private/website-offer/stripe.json"))
NAMES = {"ready": "AI-Ready Website", "powered": "AI-Powered Website"}
PLANS = {k: {"name": NAMES[k.split("-")[1]], "member": k.endswith("member"), "setup": v["setup"], "monthly": v["monthly"], "url": v["url"]}
         for k, v in LINKS.items()}
BACK = "/websites" if "--live" in sys.argv else "/preview-websites"
JSPLANS = json.dumps(PLANS)

CSS_COMMON = '''
.tvi{max-width:860px!important}
.tvi-step{display:inline-flex;align-items:center;gap:8px;margin:18px 0 12px!important;padding:6px 14px;border-radius:999px;background:#eef4fd;color:var(--blue)!important;font-weight:800;font-size:13px!important;letter-spacing:.06em;text-transform:uppercase}
.tvi h1{font-size:40px;line-height:1.08;margin:0 0 10px}
.tvi-sub{color:var(--mut);font-size:17px;margin:0 0 20px!important}
.tvi-plan{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;padding:20px 22px;border-radius:20px;background:linear-gradient(125deg,#0b2246,#13336a 60%,#1d4f91);color:#cfe0f7;box-shadow:0 18px 40px rgba(13,35,70,.22);margin-bottom:22px}
.tvi-plan b{display:block;color:#fff;font-size:22px}
.tvi-plan em{font-style:normal;color:var(--gold);font-weight:800;font-size:12.5px;letter-spacing:.12em;text-transform:uppercase}
.tvi-plan .pr{text-align:right}.tvi-plan .pr b{font-size:30px}.tvi-plan .pr span{font-size:14px}
.tvi-plan a{color:#ffd76a!important;font-weight:700;font-size:14px}
.tvi-pick{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:22px}
.tvi-pick a{display:block;padding:18px;border-radius:16px;border:2px solid var(--line);background:#fff;color:var(--navy)!important;text-decoration:none!important}
.tvi-pick a b{display:block;font-size:18px}.tvi-pick a span{color:var(--mut);font-size:14px}
@media (max-width:640px){.tvi h1{font-size:30px}.tvi-pick{grid-template-columns:1fr}.tvi-plan .pr{text-align:left}}
'''

START_HTML = '''<div class="tvs tvi" id="tvs">
<p class="tvi-step">Your website brief</p>
<h1>Tell us about your website.</h1>
<p class="tvi-sub">A few minutes here saves a lot of back and forth. Share what you know and we will reply by email within one business day with a few ideas for your site. No payment today.</p>
<ol class="tvi-track"><li class="on"><b>1</b>Your brief</li><li><b>2</b>Ideas + plan</li><li><b>3</b>Checkout</li><li><b>4</b>We build</li><li><b>5</b>Launch</li></ol>
<div id="tvi-plan"></div>
<div class="tvi-card" id="tvi-form-slot"></div>
<p class="tvi-help">Questions first? <a href="@@BACK@@#tvs-book">Send us a message</a> or email <a href="mailto:hello@threevillagelocal.com">hello@threevillagelocal.com</a></p>
</div>'''

START_CSS = CSS_COMMON + '''
.tvi-card{background:#fff;border:1px solid var(--line);border-radius:24px;padding:26px 28px;box-shadow:0 16px 40px rgba(13,35,70,.07)}
.tvi-card form label{color:var(--navy);font-weight:700}
.tvi-card .form-control{border-radius:12px;border:1px solid #d5dce6;min-height:46px;box-shadow:none}
.tvi-card textarea.form-control{min-height:110px}
.tvi-card .form-control:focus{border-color:var(--blue);box-shadow:0 0 0 4px rgba(29,95,191,.14)}
.tvi-card input[type=file]{padding:12px;border:2px dashed #c9d6e8;border-radius:12px;background:#f7faff;width:100%}
.tvi-card .checkbox label,.tvi-card .checkbox-inline{font-weight:500;color:#34465c}
.tvi-card .tvs-submit,.tvi-card button[type=submit]{border:0!important;border-radius:999px!important;padding:17px 22px!important;font-size:18px!important;font-weight:800!important;color:#2a1c00!important;background:linear-gradient(135deg,#ffd76a,#f0ad2e)!important;box-shadow:0 14px 30px rgba(240,173,46,.4)!important}
.tvi-sec{margin:22px 0 10px!important;padding-top:14px;border-top:1px solid #eef1f6;font-size:19px!important;font-weight:800;color:var(--navy)!important}
.tvi-track{list-style:none;display:flex;gap:6px;flex-wrap:wrap;padding:0;margin:0 0 22px}.tvi-track li{display:flex;align-items:center;gap:7px;padding:7px 13px 7px 7px;border-radius:999px;background:#f1f4f9;color:var(--mut);font-size:13.5px;font-weight:700}.tvi-track b{display:flex;align-items:center;justify-content:center;width:24px;height:24px;border-radius:50%;background:#dfe6f0;color:var(--navy);font-size:12px}.tvi-track li.on{background:var(--navy);color:#fff}.tvi-track li.on b{background:#ffd76a;color:#2a1c00}
.tvi-help{text-align:center;color:var(--mut);margin:18px 0 40px!important}.tvi-help a{color:var(--blue);font-weight:700}
@media (max-width:640px){.tvi-card{padding:18px 16px}}
'''

START_JS = '''(function(){
var PLANS=@@PLANS@@,K='3vl_web_plan',root=document.getElementById('tvs');if(!root)return;
var q=(location.search.match(/[?&]plan=([a-z-]+)/)||[])[1];
if(q&&PLANS[q]){try{localStorage.setItem(K,q)}catch(e){}}else{try{q=localStorage.getItem(K)}catch(e){}}
var box=document.getElementById('tvi-plan');
function money(n){return '$'+n.toLocaleString()}
if(q&&PLANS[q]){var p=PLANS[q];box.innerHTML='<div class="tvi-plan"><div><em>'+(p.member?'Featured &amp; VIP member price':'Your plan')+'</em><b>'+p.name+'</b><a href="@@BACK@@#tvw-plans">Change plan</a></div><div class="pr"><b>'+money(p.setup)+'</b><span>paid at kickoff, includes your first month. Then '+money(p.monthly)+'/mo starting 30 days later.</span></div></div>'}
else{var h='<div class="tvi-pick">';Object.keys(PLANS).filter(function(k){return /member$/.test(k)}).forEach(function(k){var p=PLANS[k];h+='<a href="?plan='+k+'"><b>'+p.name+'</b><span>'+money(p.setup)+' to start, then '+money(p.monthly)+'/mo (Featured &amp; VIP member price)</span></a>'});box.innerHTML=h+'</div>'}
var SEC={has_domain:'Your domain',about_business:'Your business',features:'Your site',logo_file:'Logo and photos',comments:'Anything else'};
function place(){var f=document.querySelector('form[name^="website_intake"]');if(!f)return false;var slot=document.getElementById('tvi-form-slot');slot.appendChild(f);
  var h=f.querySelector('input[name="plan"]');if(h&&q)h.value=q;
  Object.keys(SEC).forEach(function(n){var el=f.querySelector('[name="'+n+'"],[name="'+n+'[]"]');var g=el&&(el.closest('.form-group')||el.parentNode);if(g&&!g.previousElementSibling||g&&!g.previousElementSibling.classList.contains('tvi-sec')){var t=document.createElement('p');t.className='tvi-sec';t.textContent=SEC[n];g&&g.parentNode.insertBefore(t,g)}});
  [].forEach.call(f.querySelectorAll('h1,h2,h3,h4,legend,.form-group'),function(el){if(el.textContent.trim()==='Tell us about your website'||(el.classList.contains('form-group')&&!el.textContent.trim()&&!el.querySelector('input,select,textarea,iframe,button')))el.style.display='none'});
  f.addEventListener('submit',function(){try{var e=f.querySelector('[name="inquiry_email"]');localStorage.setItem('3vl_web_email',e?e.value:'');if(q)localStorage.setItem(K,q)}catch(x){}try{if(window.gtag)gtag('event','websites_brief_submit',{plan:q})}catch(x){}},true);
  return true}
if(!place()){var n=0,iv=setInterval(function(){if(place()||++n>60)clearInterval(iv)},200)}
})();'''

CHECK_HTML = '''<div class="tvs tvi" id="tvs">
<p class="tvi-step">Brief received</p>
<h1>Thanks! Your brief is in.</h1>
<p class="tvi-sub">We will reply by email within one business day. You will get a few ideas for your site and a quick look at how AI and Google see your business today. Nothing to pay today.</p>
<div id="tvi-plan"></div>
<ol class="tvi-next"><li><b>Ideas and your plan</b><span>We send you our ideas by email and confirm the right package. A call is always an option, never required.</span></li><li><b>Secure checkout</b><span>Your start-up fee is paid in full when you are ready to kick off, and it includes your first month. Your monthly plan starts 30 days later.</span></li><li><b>We Build It, You Approve It, We Launch!</b><span>You review a private preview, then we go live and announce it across Three Village Local.</span></li></ol>
<p class="tvi-help">Questions in the meantime? Email <a href="mailto:hello@threevillagelocal.com">hello@threevillagelocal.com</a></p>
</div>'''

CHECK_CSS = CSS_COMMON + '''
.tvi-next{list-style:none;counter-reset:n;padding:0;margin:8px 0 0;display:grid;gap:12px}
.tvi-next li{counter-increment:n;position:relative;padding:16px 18px 16px 64px;border:1px solid var(--line);border-radius:18px;background:#fff}
.tvi-next li:before{content:counter(n);position:absolute;left:18px;top:16px;width:32px;height:32px;border-radius:50%;background:var(--blue);color:#fff;font-weight:800;display:flex;align-items:center;justify-content:center}
.tvi-next b{display:block;color:var(--navy);font-size:17px}.tvi-next span{color:var(--mut)}
.tvi-help{text-align:center;color:var(--mut);margin:22px 0 40px!important}.tvi-help a{color:var(--blue);font-weight:700}
'''

CHECK_JS = '''(function(){
var PLANS=@@PLANS@@,q;try{q=localStorage.getItem('3vl_web_plan')}catch(e){}
function money(n){return '$'+n.toLocaleString()}
if(q&&PLANS[q]){var p=PLANS[q];document.getElementById('tvi-plan').innerHTML='<div class="tvi-plan"><div><em>You picked</em><b>'+p.name+'</b></div><div class="pr"><b>'+money(p.setup)+'</b><span>paid at kickoff, includes your first month. Then '+money(p.monthly)+'/mo starting 30 days later.'+(p.member?' Featured &amp; VIP member price.':'')+'</span></div></div>'}
try{if(window.gtag)gtag('event','websites_brief_done',{plan:q})}catch(e){}
})();'''


WELCOME_HTML = '''<div class="tvs tvi tvw-wel" id="tvs">
<div class="tvw-wel-hero"><p class="tvw-wel-k">Payment received. Welcome aboard.</p>
<h1>Let&#39;s build your website.</h1>
<p>Thank you for choosing Three Village Local. Your project is officially on the calendar. Here is exactly what happens next, so you are never wondering where things stand.</p>
<div id="tvi-plan"></div></div>
<h2 class="tvw-wel-h">Your next 7 days</h2>
<ol class="tvw-tl">
<li><b>Day 1</b><div><strong>Kickoff email</strong><span>Within one business day you get a welcome email with a short checklist and your free AI visibility check: how ChatGPT, Gemini and Google describe your business today.</span></div></li>
<li><b>Days 2-4</b><div><strong>We design and write</strong><span>We build your pages, write the copy, label everything for Google and AI, and set up your lead form and tracking.</span></div></li>
<li><b>Day 5</b><div><strong>Your private preview</strong><span>You get a private link to review on your phone and computer. Reply with any changes, big or small.</span></div></li>
<li><b>Day 6</b><div><strong>Polish</strong><span>We make your changes and send it back until you love it.</span></div></li>
<li class="go"><b>Day 7</b><div><strong>Launch day</strong><span>Your site goes live and we introduce it to the whole town with your Three Village Local Launch Spotlight.</span></div></li>
</ol>
<div class="tvw-need"><h2 class="tvw-wel-h">What we need from you</h2>
<p>Gather what you can. Missing something? No problem, we will fill the gaps together.</p>
<ul><li><b>Your logo</b><span>Any format. No logo? We will set up a clean text logo.</span></li>
<li><b>5 to 15 photos</b><span>Your space, your team, your work. Phone photos are fine.</span></li>
<li><b>Your services</b><span>A simple list, plus anything you want to be known for.</span></li>
<li><b>Hours, phone and service area</b><span>Exactly how you want them shown.</span></li>
<li><b>Your domain</b><span>If you already own one, tell us where it is registered. If not, we help you register it in your name.</span></li>
<li><b>Your socials</b><span>Facebook, Instagram, YouTube or anything else you use.</span></li></ul>
<a class="tvw-wel-btn" href="mailto:hello@threevillagelocal.com?subject=Website%20kickoff%20-%20my%20files">Email us your files</a>
<p class="tvw-wel-small">Large files? Reply to your kickoff email and we will send you a private upload link.</p></div>
<h2 class="tvw-wel-h">Included with your website</h2>
<div class="tvw-perks">
<div><b>Launch Spotlight</b><span>Homepage feature, weekly email feature and a boost on your Three Village Local listing.</span></div>
<div><b>Monthly report</b><span>Every month: visitors, leads, Google searches and AI referrals, in plain English.</span></div>
<div><b>Updates included</b><span>Email or text us your changes any time. We handle them.</span></div>
<div><b>Hosting and security</b><span>Fast, secure hosting with backups. Your monthly plan starts 30 days after kickoff.</span></div>
</div>
<p class="tvi-help">Questions any time: <a href="mailto:hello@threevillagelocal.com">hello@threevillagelocal.com</a>. We reply fast.</p>
</div>'''

WELCOME_CSS = CSS_COMMON + '''
.tvw-wel-hero{margin:18px 0 26px;padding:34px 30px 26px;border-radius:26px;color:#cfe0f7;background:radial-gradient(520px 260px at 90% 0%,rgba(77,163,255,.35),transparent 70%),linear-gradient(150deg,#0d2147,#1d4fb0);box-shadow:0 30px 60px -30px rgba(9,30,66,.6)}
.tvw-wel-k{display:inline-block;margin:0 0 12px!important;padding:6px 14px;border-radius:999px;background:rgba(255,215,106,.16);color:#ffd76a;font-weight:800;font-size:13px;letter-spacing:.06em;text-transform:uppercase}
.tvw-wel-hero h1{color:#fff!important;margin:0 0 10px}
.tvw-wel-hero>p{font-size:17px;line-height:1.6;margin:0 0 18px!important}
.tvw-wel-hero .tvi-plan{margin:0;background:rgba(255,255,255,.08);box-shadow:none;border:1px solid rgba(255,255,255,.14)}
.tvw-wel-h{font-size:26px;margin:30px 0 14px!important;color:var(--navy)}
.tvw-tl{list-style:none;padding:0;margin:0;display:grid;gap:10px}
.tvw-tl li{display:grid;grid-template-columns:96px 1fr;gap:14px;align-items:start;padding:16px 18px;border:1px solid var(--line);border-radius:18px;background:#fff}
.tvw-tl li>b{display:inline-block;padding:6px 10px;border-radius:999px;background:#eef4fd;color:var(--blue);font-size:13px;text-align:center}
.tvw-tl li.go{border-color:#f0c24b;background:#fffbea}.tvw-tl li.go>b{background:#ffd76a;color:#2a1c00}
.tvw-tl strong{display:block;color:var(--navy);font-size:17px;margin-bottom:3px}.tvw-tl span{color:var(--mut);line-height:1.55}
.tvw-need{margin-top:10px;padding:6px 26px 24px;border-radius:24px;background:#f6f9fe;border:1px solid var(--line)}
.tvw-need>p{color:var(--mut);margin:0 0 14px!important}
.tvw-need ul{list-style:none;padding:0;margin:0 0 18px;display:grid;grid-template-columns:1fr 1fr;gap:10px}
.tvw-need li{padding:14px 16px 14px 44px;border-radius:14px;background:#fff;border:1px solid var(--line);position:relative}
.tvw-need li:before{content:"";position:absolute;left:16px;top:17px;width:16px;height:16px;border-radius:5px;border:2px solid var(--blue)}
.tvw-need li b{display:block;color:var(--navy)}.tvw-need li span{color:var(--mut);font-size:14.5px}
.tvw-wel-btn{display:inline-block;padding:15px 26px;border-radius:999px;font-weight:800;font-size:17px;color:#2a1c00!important;text-decoration:none!important;background:linear-gradient(135deg,#ffd76a,#f0ad2e);box-shadow:0 14px 30px rgba(240,173,46,.4)}
.tvw-wel-small{font-size:13.5px;color:var(--mut);margin:10px 0 0!important}
.tvw-perks{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.tvw-perks div{padding:18px;border-radius:18px;background:#fff;border:1px solid var(--line);box-shadow:0 12px 28px -20px rgba(13,35,70,.35)}
.tvw-perks b{display:block;color:var(--navy);font-size:17px;margin-bottom:4px}.tvw-perks span{color:var(--mut);font-size:14.5px;line-height:1.5}
@media (max-width:640px){.tvw-wel-hero{padding:26px 20px 20px}.tvw-tl li{grid-template-columns:1fr;gap:8px}.tvw-tl li>b{justify-self:start}.tvw-need{padding:4px 16px 20px}.tvw-need ul,.tvw-perks{grid-template-columns:1fr}}
'''

WELCOME_JS = '''(function(){
var PLANS=@@PLANS@@,q=(location.search.match(/[?&]plan=([a-z-]+)/)||[])[1];if(!q){try{q=localStorage.getItem('3vl_web_plan')}catch(e){}}
function money(n){return '$'+n.toLocaleString()}
if(q&&PLANS[q]){var p=PLANS[q];document.getElementById('tvi-plan').innerHTML='<div class="tvi-plan"><div><em>Your plan</em><b>'+p.name+'</b></div><div class="pr"><b>'+money(p.setup)+'</b><span>paid, includes your first month. '+money(p.monthly)+'/mo starts in 30 days.</span></div></div>'}
try{if(window.gtag)gtag('event','websites_purchase',{plan:q,value:q&&PLANS[q]?PLANS[q].setup:0,currency:'USD'})}catch(e){}
})();'''


def publish(name, slug, title, html, css, js, form):
    import deploy as D
    importlib.reload(D)
    D.NAME, D.SLUG, D.TITLE, D.DESC = name, slug, title, "Website sign-up, Three Village Local."
    D.FORM, D.LIVE = form, False
    D.HEAD = '<meta name="robots" content="noindex,nofollow">'
    files = {"page.html": html.replace("@@BACK@@", BACK), "page.css": None, "page.js": "<script>" + js.replace("@@PLANS@@", JSPLANS).replace("@@BACK@@", BACK) + "</script>"}
    base = D.rd

    def rd(f):
        if f == "page.css":
            return base("page.css") + css
        out = files[f]
        assert "\\" not in out, f
        return out
    D.rd = rd
    D.main()


publish("3VL Page Website Start", "website-start", "Start your website | Three Village Local", START_HTML, START_CSS, START_JS, "website_intake")
publish("3VL Page Website Thanks", "website-thanks", "Thanks, your brief is in | Three Village Local", CHECK_HTML, CHECK_CSS, CHECK_JS, "")
publish("3VL Page Website Welcome", "website-welcome", "Welcome, let's build your website | Three Village Local", WELCOME_HTML, WELCOME_CSS, WELCOME_JS, "")   # owner 10/22: post-payment onboarding
