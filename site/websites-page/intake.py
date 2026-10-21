"""Website sign-up flow (owner 10/21/2026): "Start now" -> /website-start (project brief form, BD form website_intake with uploads)
-> BD redirects to /website-checkout -> big button to the right Stripe payment link.
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
<p class="tvi-step">Step 1 of 2 &middot; Your website brief</p>
<h1>Tell us about your website.</h1>
<p class="tvi-sub">A few minutes here saves a lot of back and forth. Share what you know; we will fill in the rest on a quick kickoff call. Next step is secure checkout.</p>
<div id="tvi-plan"></div>
<div class="tvi-card" id="tvi-form-slot"></div>
<p class="tvi-help">Questions first? <a href="@@BACK@@#tvs-book">Book a free consultation</a> or email <a href="mailto:hello@threevillagelocal.com">hello@threevillagelocal.com</a></p>
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
.tvi-help{text-align:center;color:var(--mut);margin:18px 0 40px!important}.tvi-help a{color:var(--blue);font-weight:700}
@media (max-width:640px){.tvi-card{padding:18px 16px}}
'''

START_JS = '''(function(){
var PLANS=@@PLANS@@,K='3vl_web_plan',root=document.getElementById('tvs');if(!root)return;
var q=(location.search.match(/[?&]plan=([a-z-]+)/)||[])[1];
if(q&&PLANS[q]){try{localStorage.setItem(K,q)}catch(e){}}else{try{q=localStorage.getItem(K)}catch(e){}}
var box=document.getElementById('tvi-plan');
function money(n){return '$'+n.toLocaleString()}
if(q&&PLANS[q]){var p=PLANS[q];box.innerHTML='<div class="tvi-plan"><div><em>'+(p.member?'Member founding price':'Your plan')+'</em><b>'+p.name+'</b><a href="@@BACK@@#tvw-plans">Change plan</a></div><div class="pr"><b>'+money(p.setup)+'</b><span>to start, includes your first month. Then '+money(p.monthly)+'/mo.</span></div></div>'}
else{var h='<div class="tvi-pick">';Object.keys(PLANS).filter(function(k){return /member$/.test(k)}).forEach(function(k){var p=PLANS[k];h+='<a href="?plan='+k+'"><b>'+p.name+'</b><span>'+money(p.setup)+' to start, then '+money(p.monthly)+'/mo (member price)</span></a>'});box.innerHTML=h+'</div>'}
var SEC={has_domain:'Your domain',about_business:'Your business',features:'Your site',logo_file:'Logo and photos',comments:'Anything else'};
function place(){var f=document.querySelector('form[name^="website_intake"]');if(!f)return false;var slot=document.getElementById('tvi-form-slot');slot.appendChild(f);
  var h=f.querySelector('input[name="plan"]');if(h&&q)h.value=q;
  Object.keys(SEC).forEach(function(n){var el=f.querySelector('[name="'+n+'"],[name="'+n+'[]"]');var g=el&&(el.closest('.form-group')||el.parentNode);if(g&&!g.previousElementSibling||g&&!g.previousElementSibling.classList.contains('tvi-sec')){var t=document.createElement('p');t.className='tvi-sec';t.textContent=SEC[n];g&&g.parentNode.insertBefore(t,g)}});
  [].forEach.call(f.querySelectorAll('h1,h2,h3,h4,legend,.form-group'),function(el){if(el.textContent.trim()==='Tell us about your website')el.style.display='none'});
  f.addEventListener('submit',function(){try{var e=f.querySelector('[name="inquiry_email"]');localStorage.setItem('3vl_web_email',e?e.value:'');if(q)localStorage.setItem(K,q)}catch(x){}try{if(window.gtag)gtag('event','websites_brief_submit',{plan:q})}catch(x){}},true);
  return true}
if(!place()){var n=0,iv=setInterval(function(){if(place()||++n>60)clearInterval(iv)},200)}
})();'''

CHECK_HTML = '''<div class="tvs tvi" id="tvs">
<p class="tvi-step">Step 2 of 2 &middot; Secure checkout</p>
<h1>Thanks! Your brief is in.</h1>
<p class="tvi-sub">One last step: complete your sign-up with secure checkout. We will email you within one business day to set up your kickoff call.</p>
<div id="tvi-plan"></div>
<div id="tvi-go"></div>
<ul class="tvi-trust"><li>&#128274; Secure checkout powered by Stripe</li><li>&#10003; Your site and domain are yours</li><li>&#10003; Month to month after your first month</li></ul>
<p class="tvi-help">Questions? Email <a href="mailto:hello@threevillagelocal.com">hello@threevillagelocal.com</a> or <a href="@@BACK@@#tvs-book">book a free consultation</a></p>
</div>'''

CHECK_CSS = CSS_COMMON + '''
.tvi-btn{display:block;text-align:center;margin:6px auto 0;max-width:520px;padding:22px 24px;border-radius:18px;background:linear-gradient(135deg,#ffd76a,#f0ad2e);color:#2a1c00!important;font-size:22px;font-weight:800;text-decoration:none!important;box-shadow:0 16px 36px rgba(240,173,46,.45)}
.tvi-trust{list-style:none;padding:0;margin:22px 0 0;display:flex;flex-wrap:wrap;justify-content:center;gap:8px 22px;color:var(--mut);font-size:14.5px}
.tvi-help{text-align:center;color:var(--mut);margin:22px 0 40px!important}.tvi-help a{color:var(--blue);font-weight:700}
'''

CHECK_JS = '''(function(){
var PLANS=@@PLANS@@,q,em='';try{q=localStorage.getItem('3vl_web_plan');em=localStorage.getItem('3vl_web_email')||''}catch(e){}
var m=(location.search.match(/[?&]plan=([a-z-]+)/)||[])[1];if(m&&PLANS[m])q=m;
function money(n){return '$'+n.toLocaleString()}
var box=document.getElementById('tvi-plan'),go=document.getElementById('tvi-go');
if(q&&PLANS[q]){var p=PLANS[q];
 box.innerHTML='<div class="tvi-plan"><div><em>'+(p.member?'Member founding price':'Your plan')+'</em><b>'+p.name+'</b></div><div class="pr"><b>'+money(p.setup)+'</b><span>today, includes your first month. Then '+money(p.monthly)+'/mo.</span></div></div>';
 var u=p.url+(em?'?prefilled_email='+encodeURIComponent(em):'');
 go.innerHTML='<a class="tvi-btn" href="'+u+'">Complete secure checkout &rarr;</a>';
 go.querySelector('a').addEventListener('click',function(){try{if(window.gtag)gtag('event','websites_checkout_click',{plan:q,from:'checkout_page'})}catch(e){}});
}else{var h='<div class="tvi-pick">';Object.keys(PLANS).forEach(function(k){var p=PLANS[k];h+='<a href="'+p.url+'"><b>'+p.name+(p.member?' (member)':'')+'</b><span>'+money(p.setup)+' to start, then '+money(p.monthly)+'/mo</span></a>'});go.innerHTML=h+'</div>'}
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
publish("3VL Page Website Checkout", "website-checkout", "Secure checkout | Three Village Local", CHECK_HTML, CHECK_CSS, CHECK_JS, "")
