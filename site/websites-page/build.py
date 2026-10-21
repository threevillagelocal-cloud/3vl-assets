"""Websites landing page (owner 10/21/2026): AI-Ready vs AI-Powered websites, member pricing, pay now (Stripe) or book a consultation.
Same look as /services (shares page.css / page.js and its booking form section).
    python site/websites-page/build.py          -> widget "3VL Page Websites" + hidden preview /preview-websites
    python site/websites-page/build.py --live   -> /websites (indexable)
Checkout links live in 3vl-private/website-offer/stripe.json (made by stripe_setup.py); prices below must match them."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SV = os.path.join(HERE, "..", "services-page")
sys.path.insert(0, SV)
import deploy as D

LINKS = json.load(open("C:/Users/Matt/Documents/3vl-private/website-offer/stripe.json"))
P = {k: (v["setup"], v["monthly"], v["url"]) for k, v in LINKS.items()}

D.NAME = "3VL Page Websites"
D.SLUG = "websites" if D.LIVE else "preview-websites"
D.TITLE = "AI-Ready Websites for Long Island Businesses | Three Village Local"
D.DESC = ("Websites built for customers and for AI: designed, built and hosted for you, readable by Google and AI assistants like ChatGPT, "
          "with an optional AI chat assistant. Member pricing for Three Village Local businesses.")
D.FB_TITLE = "Can AI recommend your business?"
D.FB_IMAGE = "https://threevillagelocal-cloud.github.io/3vl-share/site/hero-1200.webp"


def section(src, cls):
    i = src.index('<section class="' + cls)
    return src[i:src.index('</section>', i) + len('</section>')]


src = open(os.path.join(SV, "page.html"), encoding="utf-8").read()
book = section(src, "tvs-sec tvs-book").replace("<h2>Book your free 15-minute call.</h2>", "<h2>Rather talk it through first?</h2>") \
    .replace("<p>Tell us a little about your business.", "<p>Book a free consultation. Tell us a little about your business and we will reach out to set up a time.")


def card(key, tag, name, one, items, featured=False):
    m, r = P["web-%s-member" % key], P["web-%s-regular" % key]
    lis = "".join("<li>%s</li>" % i for i in items)
    return '''<article class="tvw-card%s tvs-up">
  %s<p class="tvw-tag">%s</p>
  <h3>%s</h3><p class="tvw-one">%s</p>
  <div class="tvw-price"><span class="tvw-m"><b>$%s</b> setup</span><span class="tvw-r"><b>$%s</b> setup</span><em>+ $%s/mo</em></div>
  <p class="tvw-save"><span class="tvw-m">Member founding price. Regular $%s.</span><span class="tvw-r">3VL members pay $%s.</span></p>
  <ul>%s</ul>
  <a class="tvs-btn %s tvs-wide tvw-pay" data-m="%s" data-r="%s" href="%s">Start now &rarr;</a>
  <a class="tvw-consult" href="#tvs-book">Or book a free consultation</a>
</article>''' % (" tvw-feat" if featured else "", '<span class="tvw-pop">Most popular</span>' if featured else "", tag,
                 name, one, "{:,}".format(m[0]), "{:,}".format(r[0]), m[1], "{:,}".format(r[0]), "{:,}".format(m[0]), lis,
                 "tvs-white" if featured else "tvs-blue", m[2], r[2], m[2])


READY = card("ready", "AI-Ready", "AI can find you.", "Built so Google and AI assistants understand and recommend your business.", [
    "<b>Custom design</b>, up to 5 pages, written for you",
    "<b>Code AI can actually read</b>, not hidden behind scripts",
    "<b>Your business clearly labeled</b> for search engines and AI: services, hours, area, reviews",
    "<b>A page for every service</b> and FAQs the way people ask",
    "<b>Fast, mobile-first</b>, secure, with a lead form to your inbox",
    "<b>Hosting, domain setup and updates</b> included",
    "<b>Launch spotlight</b> on Three Village Local + 3 months Featured"])
POWERED = card("powered", "AI-Powered", "AI works for you.", "Everything in AI-Ready, plus tools that bring in customers on their own.", [
    "<b>Everything in AI-Ready</b>",
    "<b>Your own AI assistant</b> answering customers 24/7 and sending you the lead",
    "<b>Fresh content, automatically:</b> 2 blog posts or industry updates a month",
    "<b>Your best reviews</b> showcased on your site",
    "<b>Online booking</b> or quote requests",
    "<b>Monthly social feature</b> on Three Village Local"], featured=True)

HTML = '''<div class="tvs tvs-nb tvw" id="tvs">

<div class="tvw-thanks" id="tvw-thanks" hidden><b>Thank you, you're in!</b> Your payment went through. We'll email you within one business day to set up a quick kickoff call.</div>

<section class="tvw-hero">
  <div class="tvw-hin tvs-up">
    <p class="tvs-kick"><span class="tvs-dot"></span>Websites by Three Village Local &middot; member pricing</p>
    <h1>Your website should work for customers <span>and&nbsp;for&nbsp;AI.</span></h1>
    <p class="tvs-sub">Nearly half of people now ask AI tools like ChatGPT where to go. AI recommends the businesses it can read and understand. We build modern websites that Google and AI can discover, learn from and recommend to locals, then we launch them to the whole town.</p>
    <div class="tvs-ctas"><a class="tvs-btn tvs-blue" href="#tvw-plans">See packages</a><a class="tvs-btn tvs-ghost" href="#tvs-book">Book a free consultation</a></div>
    <ul class="tvs-trust"><li><b>You own it</b>site and domain in your name</li><li><b>Built for AI</b>and Google search</li><li><b>Launched</b>to the whole town</li></ul>
  </div>
  <div class="tvw-chat tvs-up" aria-hidden="true">
    <div class="tvw-cbar"><i></i><i></i><i></i><span>AI assistant</span></div>
    <div class="tvw-q">Who's a good landscaper in Setauket?</div>
    <div class="tvw-a"><p class="tvw-typing"><i></i><i></i><i></i></p>
      <p class="tvw-ans">Here are a few well-reviewed options near Setauket. <b>Your Business</b> offers lawn care, cleanups and patios, and they serve the Three Village area...</p>
      <span class="tvw-src">&#128279; yourbusiness.com</span><span class="tvw-src">&#128279; threevillagelocal.com</span></div>
    <p class="tvw-note">AI pulls answers from websites it can read. Is yours one of them?</p>
  </div>
</section>

<section class="tvs-sec tvw-stats tvs-up">
  <div><b>45%</b><span>of people used ChatGPT or another AI tool for a local recommendation last year, up from 6%</span></div>
  <div><b>58%</b><span>of the sources ChatGPT cites for local questions are the businesses' own websites</span></div>
  <div><b>7x</b><span>more likely to turn a lead into business when you answer within the hour</span></div>
</section>

<section class="tvs-sec" id="tvw-plans">
  <div class="tvs-head tvs-up"><p class="tvs-eyebrow">Two ways to go modern</p><h2>AI-Ready or AI-Powered?</h2>
    <p><b>AI-Ready</b> means AI can find you. <b>AI-Powered</b> means AI works for you. Both are designed, built and hosted by us.</p></div>
  <label class="tvw-toggle tvs-up"><input type="checkbox" id="tvw-mem" checked> <span>I'm a Three Village Local member</span></label>
  <div class="tvw-cards">@@READY@@@@POWERED@@</div>
  <p class="tvs-fine tvs-up">Setup is a one-time fee; the monthly plan covers hosting, security, updates and support, month to month after launch. Your domain is registered in your name (usually $10 to $20 a year, paid to the registrar). <b>Need more?</b> Own Your Market adds weekly content, an online shop and a quarterly refresh: <a href="#tvs-book">ask us</a>.</p>
</section>

<section class="tvs-sec tvw-why">
  <div class="tvs-head tvs-up"><p class="tvs-eyebrow">What AI looks for</p><h2>Why most small-business sites get skipped.</h2></div>
  <div class="tvw-grid4">
    <div class="tvs-up"><span>&#128065;&#65039;</span><b>It can't see your content</b><p>Many template sites load text with scripts. AI crawlers like ChatGPT's and Perplexity's don't run them, so your page looks empty.</p></div>
    <div class="tvs-up"><span>&#127991;&#65039;</span><b>It can't tell what you do</b><p>Without clearly labeled services, hours and service area, AI can't confidently match you to a question.</p></div>
    <div class="tvs-up"><span>&#10067;</span><b>It can't find answers</b><p>People ask full questions. Sites with real FAQs and a page per service give AI the answer to quote.</p></div>
    <div class="tvs-up"><span>&#128197;</span><b>It looks inactive</b><p>No fresh content and an old copyright year signal a business that may not be around. We keep yours current.</p></div>
  </div>
</section>

<section class="tvs-sec tvw-adv">
  <div class="tvs-head tvs-up"><p class="tvs-eyebrow">Why Three Village Local</p><h2>More than a website. A local launch.</h2></div>
  <div class="tvw-grid3">
    <div class="tvs-up tvw-g"><b>A built-in local audience</b><p>Your launch is announced on our homepage, social media and Friday email: 45,000+ website page visits and 100,000+ Facebook and Instagram views a month.</p></div>
    <div class="tvs-up"><b>You own it. No lock-in.</b><p>Your site and domain are in your name from day one. No 12-month rental, no hostage website.</p></div>
    <div class="tvs-up"><b>Done for you</b><p>Design, writing, build, domain setup, hosting, security and updates. You run your business, we run your website.</p></div>
    <div class="tvs-up tvw-g"><b>Featured on Three Village Local</b><p>Every package includes time as a Featured business, the kind of trusted local mention AI looks for.</p></div>
    <div class="tvs-up"><b>Built to be recommended</b><p>Set up for Google, ChatGPT, Gemini and Perplexity, not just to look nice.</p></div>
    <div class="tvs-up"><b>Actually local</b><p>We're your neighbors in Three Village. Meet us in person, email us anytime.</p></div>
  </div>
</section>

<section class="tvs-sec tvw-cmp tvs-up">
  <div class="tvs-head"><p class="tvs-eyebrow">Compare</p><h2>How we stack up.</h2></div>
  <div class="tvw-tbl"><table>
    <tr><th></th><th>DIY builder</th><th>$0-down rental</th><th>Typical agency</th><th class="us">Three Village Local</th></tr>
    <tr><td>Done for you</td><td class="n">No</td><td>Yes</td><td>Yes</td><td class="us">Yes</td></tr>
    <tr><td>You own your site and domain</td><td>Yes</td><td class="n">No</td><td>Sometimes</td><td class="us">Always</td></tr>
    <tr><td>Built for AI search</td><td class="n">Rarely</td><td class="n">Rarely</td><td>Extra cost</td><td class="us">Included</td></tr>
    <tr><td>AI assistant for customers</td><td>Extra app</td><td class="n">No</td><td>Extra cost</td><td class="us">AI-Powered</td></tr>
    <tr><td>Promotion to local customers</td><td class="n">No</td><td class="n">No</td><td class="n">No</td><td class="us">Included</td></tr>
  </table></div>
</section>

<section class="tvs-sec tvs-tl">
  <div class="tvs-head tvs-up"><p class="tvs-eyebrow">How it works</p><h2>From sign-up to launch.</h2></div>
  <ol class="tvs-tlist">
    <li class="tvs-up"><em>Step 1</em><b>Start now or book a call</b><p>Pay securely online, or talk it through with us first.</p></li>
    <li class="tvs-up"><em>Step 2</em><b>A quick kickoff</b><p>A short call about your business, your services and your photos. We do the writing.</p></li>
    <li class="tvs-up"><em>Step 3</em><b>Your preview</b><p>We build your site and send you a private preview to review.</p></li>
    <li class="tvs-up"><em>Step 4</em><b>Launch day</b><p>You go live, and we announce your new site across Three Village Local.</p></li>
  </ol>
</section>

<section class="tvs-sec tvs-faq">
  <div class="tvs-head tvs-up"><p class="tvs-eyebrow">Questions</p><h2>Good questions, straight answers.</h2></div>
  <div class="tvs-qs tvs-up">
    <details><summary>What's the difference between AI-Ready and AI-Powered?</summary><p>AI-Ready is the website itself, built so Google and AI assistants can read, understand and recommend you. AI-Powered adds tools that work for you every day: an AI assistant that answers customers and sends you leads, fresh content published for you, a review showcase and online booking.</p></details>
    <details><summary>Do I own my website and domain?</summary><p>Yes. Your domain is registered in your name, and the site is yours. No long-term contract and no hostage website.</p></details>
    <details><summary>What do you need from me?</summary><p>About 30 minutes for a kickoff call, your logo and any photos you like. We write the pages and handle everything technical.</p></details>
    <details><summary>Will AI definitely recommend my business?</summary><p>Nobody can promise that, and you should be wary of anyone who does. What we do is make sure AI and Google can read and understand your business clearly, which is what they rely on to recommend anyone.</p></details>
    <details><summary>How does the AI assistant work?</summary><p>It knows only your business: services, hours, area and FAQs you approve. It answers questions on your site day and night, and when someone is ready, it sends you their name, number and what they need.</p></details>
    <details><summary>I sell products. Can you handle that?</summary><p>Yes. A few products can be sold right on your site through your own Stripe account, or we connect Square or Shopify for larger stores. Ask us and we will recommend the right fit.</p></details>
    <details><summary>Who gets member pricing?</summary><p>Businesses listed on Three Village Local. Founding pricing is for the first 10 member businesses that sign up.</p></details>
  </div>
</section>

@@BOOK@@

<a class="tvs-sticky" href="#tvw-plans">See website packages</a>
<script>(function(){
var mem=document.getElementById('tvw-mem'),root=document.getElementById('tvs');
function sync(){var m=mem.checked;root.classList.toggle('tvw-reg',!m);[].forEach.call(document.querySelectorAll('.tvw-pay'),function(a){a.href=m?a.getAttribute('data-m'):a.getAttribute('data-r')})}
mem.addEventListener('change',sync);sync();
[].forEach.call(document.querySelectorAll('.tvw-pay'),function(a){a.addEventListener('click',function(){try{if(window.gtag)gtag('event','websites_checkout_click',{plan:a.closest('.tvw-card').querySelector('h3').textContent,member:mem.checked})}catch(e){}})});
if(/[?&]welcome=1/.test(location.search)){var t=document.getElementById('tvw-thanks');t.hidden=false;try{if(window.gtag)gtag('event','websites_purchase')}catch(e){}}
var n=0,iv=setInterval(function(){var s=document.querySelector('#tvs-form-slot select[name="bundle"]');if(s){s.value='web_consult';var g=s.closest('.form-group')||s.parentNode;g.style.display='none';clearInterval(iv)}if(++n>40)clearInterval(iv)},250);
})();</script>
</div>'''.replace("@@READY@@", READY).replace("@@POWERED@@", POWERED).replace("@@BOOK@@", book)

CSS = '''
.tvw-thanks{margin:12px 0 0;padding:16px 20px;border-radius:16px;background:#e8f7ef;border:1px solid #9bd8b6;color:#0d5a3a;font-size:16px}
.tvw-hero{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:40px;align-items:center;margin:14px 0 0;padding:44px 44px;border-radius:28px;background:linear-gradient(135deg,#f6f9fd,#fff 60%);border:1px solid var(--line)}
.tvw-hero h1{font-size:52px;line-height:1.04;font-weight:800;margin-bottom:16px}
.tvw-hero h1 span{background:linear-gradient(90deg,var(--blue),var(--blue2));-webkit-background-clip:text;background-clip:text;color:transparent}
.tvw-chat{background:#0f2a52;border-radius:24px;padding:18px 18px 16px;box-shadow:0 30px 70px rgba(13,35,70,.3);color:#e7effa}
.tvw-cbar{display:flex;align-items:center;gap:6px;margin-bottom:14px}.tvw-cbar i{width:10px;height:10px;border-radius:50%;background:#2a4a7a}.tvw-cbar span{margin-left:8px;font-size:12.5px;font-weight:700;color:#8ec5ff;letter-spacing:.08em;text-transform:uppercase}
.tvw-q{margin-left:auto;max-width:85%;width:max-content;background:#2f7de1;color:#fff;padding:11px 15px;border-radius:16px 16px 4px 16px;font-size:15px;font-weight:600;animation:tvwIn .5s .3s both}
.tvw-a{margin-top:12px;max-width:92%;background:#fff;color:#1d2b3a;padding:13px 15px;border-radius:16px 16px 16px 4px;font-size:14.5px;line-height:1.5;animation:tvwIn .5s 1s both}
.tvw-a p{margin:0!important}
.tvw-typing{display:flex;gap:5px;overflow:hidden;max-height:20px;animation:tvwOut .25s 2.2s forwards}.tvw-typing i{width:8px;height:8px;border-radius:50%;background:#8a95a3;animation:tvwDot 1s infinite}.tvw-typing i:nth-child(2){animation-delay:.15s}.tvw-typing i:nth-child(3){animation-delay:.3s}
.tvw-ans{opacity:0;animation:tvwIn .45s 2.45s forwards}
.tvw-ans b{background:#fff4d6;color:#0f2a52;padding:0 4px;border-radius:4px}
.tvw-src{display:inline-block;margin:10px 6px 0 0;font-size:12px;font-weight:700;color:#1d5fbf;background:#eef4fd;border-radius:999px;padding:4px 10px;opacity:0;animation:tvwIn .4s 2.8s forwards}
.tvw-note{margin:14px 0 0!important;font-size:13.5px!important;color:#ffd76a!important;font-weight:700}
@keyframes tvwIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
@keyframes tvwDot{50%{opacity:.3}}@keyframes tvwOut{to{opacity:0;max-height:0}}
.tvs-tlist{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(4,1fr);gap:14px;position:relative}
.tvs-tlist:before{content:"";position:absolute;left:0;right:0;top:15px;height:3px;background:linear-gradient(90deg,var(--blue2),var(--gold));border-radius:3px}
.tvs-tlist li{position:relative;padding-top:38px}
.tvs-tlist li:before{content:"";position:absolute;top:7px;left:0;width:19px;height:19px;border-radius:50%;background:#fff;border:4px solid var(--blue)}
.tvs-tlist em{display:block;font-style:normal;font-size:12.5px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--blue)}
.tvs-tlist b{display:block;color:var(--navy);font-size:19px;margin:4px 0}
.tvs-tlist p{margin:0!important;color:var(--mut);font-size:14.5px!important}
@media (max-width:900px){.tvs-tlist{grid-template-columns:1fr 1fr;row-gap:26px}.tvs-tlist:before{display:none}}
@media (max-width:520px){.tvs-tlist{grid-template-columns:1fr}}
.tvw-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.tvw-stats div{background:#fff;border:1px solid var(--line);border-radius:20px;padding:22px 22px;box-shadow:0 12px 30px rgba(13,35,70,.06)}
.tvw-stats b{display:block;font-size:44px;line-height:1;color:var(--blue);font-weight:800;margin-bottom:8px}
.tvw-stats span{font-size:15px;color:var(--mut)}
.tvw-toggle{display:flex;justify-content:center;align-items:center;gap:10px;margin:0 auto 22px;font-weight:700;color:var(--navy);cursor:pointer}
.tvw-toggle input{width:20px;height:20px;accent-color:var(--blue)}
.tvw-cards{display:grid;grid-template-columns:1fr 1fr;gap:20px;max-width:960px;margin:0 auto}
.tvw-card{position:relative;background:#fff;border:1.5px solid var(--line);border-radius:26px;padding:28px 26px 22px;box-shadow:0 18px 44px rgba(13,35,70,.08);display:flex;flex-direction:column}
.tvw-feat{background:linear-gradient(140deg,#0b2246,#13336a 60%,#1d4f91);border:0;color:#d7e5f8}
.tvw-pop{position:absolute;top:-13px;right:22px;background:var(--gold);color:#2a1c00;font-weight:800;font-size:12.5px;border-radius:999px;padding:5px 12px}
.tvw-tag{margin:0!important;font-size:12.5px!important;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--blue)}
.tvw-feat .tvw-tag{color:var(--gold)}
.tvw-card h3{font-size:30px;margin:4px 0 4px}.tvw-feat h3{color:#fff}
.tvw-one{margin:0 0 14px!important;color:var(--mut)}.tvw-feat .tvw-one{color:#cfe0f7}
.tvw-price{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
.tvw-price span{font-size:16px;color:var(--mut)}.tvw-price b{font-size:42px;color:var(--navy);line-height:1}
.tvw-feat .tvw-price span{color:#cfe0f7}.tvw-feat .tvw-price b{color:#fff}
.tvw-price em{font-style:normal;font-weight:800;font-size:20px;color:var(--blue)}.tvw-feat .tvw-price em{color:var(--gold)}
.tvw-save{margin:6px 0 16px!important;font-size:14px!important;font-weight:700;color:#966e22!important}.tvw-feat .tvw-save{color:#ffd76a!important}
.tvw .tvw-r{display:none}.tvw.tvw-reg .tvw-r{display:inline}.tvw.tvw-reg .tvw-m{display:none}
.tvw-card ul{list-style:none;margin:0 0 20px;padding:0;flex:1}
.tvw-card li{position:relative;padding:7px 0 7px 26px;border-bottom:1px dashed var(--line);font-size:15px}
.tvw-feat li{border-bottom-color:rgba(255,255,255,.14)}
.tvw-card li:before{content:"✓";position:absolute;left:2px;top:7px;color:var(--blue);font-weight:800}.tvw-feat li:before{color:var(--gold)}
.tvw-card li b{color:var(--navy)}.tvw-feat li b{color:#fff}
.tvw-consult{display:block;text-align:center;margin-top:12px;font-weight:700;color:var(--blue)!important;font-size:15px}.tvw-feat .tvw-consult{color:#ffd76a!important}
.tvw-grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.tvw-grid4 div{background:#fff;border:1px solid var(--line);border-radius:18px;padding:20px 18px}
.tvw-grid4 span{font-size:28px}.tvw-grid4 b{display:block;color:var(--navy);font-size:17px;margin:8px 0 4px}.tvw-grid4 p{margin:0!important;color:var(--mut);font-size:14.5px!important}
.tvw-grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.tvw-grid3 div{border-left:4px solid var(--blue);padding:4px 0 4px 16px}.tvw-grid3 div.tvw-g{border-left-color:var(--gold)}
.tvw-grid3 b{display:block;color:var(--navy);font-size:18px;margin-bottom:4px}.tvw-grid3 p{margin:0!important;color:var(--mut);font-size:15px!important}
.tvw-tbl{overflow-x:auto}.tvw-cmp table{width:100%;border-collapse:collapse;font-size:15px;min-width:620px}
.tvw-cmp th,.tvw-cmp td{padding:11px 12px;text-align:center;border-bottom:1px solid var(--line)}
.tvw-cmp th{font-size:12.5px;color:var(--mut);text-transform:uppercase;letter-spacing:.06em}
.tvw-cmp th.us{background:var(--navy);color:#fff;border-radius:10px 10px 0 0}
.tvw-cmp td:first-child,.tvw-cmp th:first-child{text-align:left;font-weight:700;color:var(--navy)}
.tvw-cmp td.us{background:#eef4fd;color:var(--blue);font-weight:800}.tvw-cmp td.n{color:#a5afbc}
@media (max-width:900px){.tvw-hero{grid-template-columns:1fr;padding:30px 22px}.tvw-hero h1{font-size:38px}.tvw-cards,.tvw-stats{grid-template-columns:1fr}.tvw-grid4{grid-template-columns:1fr 1fr}.tvw-grid3{grid-template-columns:1fr}}
@media (max-width:520px){.tvw-hero h1{font-size:32px}.tvw-grid4{grid-template-columns:1fr}.tvw-card{padding:24px 18px 18px}.tvw-price b{font-size:36px}}
'''

_rd = D.rd


def rd(f):
    if f == "page.html":
        assert "\\" not in HTML
        return HTML
    s = _rd(f)
    return s + CSS if f == "page.css" else s


D.rd = rd
if __name__ == "__main__":
    D.main()
