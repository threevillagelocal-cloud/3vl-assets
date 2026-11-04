"""AI add-ons for an EXISTING website (owner 11/3/2026): stand-alone AI Chat Assistant + AI Tune-Up for sites built and hosted by
someone else. Same look as /websites: imports that page's build and swaps the sections.
    python site/ai-assistant-page/build.py          -> widget "3VL Page AI Assistant Preview" + hidden /preview-ai-assistant
    python site/ai-assistant-page/build.py --live   -> widget "3VL Page AI Assistant" + /ai-assistant (indexable)"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "websites-page"))
import build as W
from build import D, rep, cut, swap, sec

# prices: (setup, monthly) walk-in / member. Tune-up is one-time (monthly 0).
CHAT = {"all": (799, 199), "member": (499, 149)}
TUNE = {"all": (799, 0), "member": (499, 0)}

D.NAME = "3VL Page AI Assistant" if D.LIVE else "3VL Page AI Assistant Preview"
D.SLUG = "ai-assistant" if D.LIVE else "preview-ai-assistant"
D.TITLE = "AI Chat Assistant + AI Tune-Up for Your Current Website | Three Village Local"
D.DESC = ("Add a smart AI assistant to the website you already have. It answers customers 24/7 and sends you every lead. "
          "Plus an AI Tune-Up so ChatGPT, Google and other AI tools can find and recommend you. Works with Wix, Squarespace, WordPress and more.")
D.FB_TITLE = "Turn your website into a 24/7 lead machine."

DEMO = W.sec(W.HTML, "tvs-sec tvw-bot")
DEMO = W.HTML[DEMO[0]:DEMO[1]]
DEMO = DEMO[DEMO.index('<div class="tvw-bot-demo'):DEMO.rindex('</div>\n  </div>\n</section>')]   # the animated example chat + lead card

HERO = '''<section class="tvs-hero">
  <div class="tvw-hvis tva-hvis"><div class="tva-try"><p class="tva-try-k"><span></span>Live demo: try me</p><div id="tva-live"></div></div></div>
  <div class="tvs-hin tvs-up">
    <p class="tvs-kick"><span class="tvs-dot"></span>AI for the website you already have</p>
    <h1>Turn your website<br><span>into a 24/7 lead machine.</span></h1>
    <p class="tvs-sub">Add a smart AI assistant to your current website. It answers customers the second they ask, day or night, and sends you every lead. No new website needed. Works with Wix, Squarespace, WordPress, GoDaddy and more.</p>
    <div class="tvs-ctas">
      <a class="tvs-btn tvs-blue" href="#tva-live">Try the live demo</a>
      <a class="tvs-btn tvs-ghost" href="#tvs-bundles">See pricing</a>
    </div>
    <ul class="tvs-trust">
      <li><b>No new</b>website needed</li>
      <li><b>About 7 days</b>to go live</li>
      <li><b>Every lead</b>sent to you</li>
    </ul>
  </div>
</section>'''

NEXT = '''<section class="tvs-sec tva-next" id="tva-next">
  <div class="tvs-head tvs-up">
    <p class="tvs-eyebrow">The next big thing for websites</p>
    <h2>Websites are learning to talk.</h2>
    <p>For 25 years, websites just sat there. Customers had to dig for answers, then call during business hours or give up. Now people are used to asking AI a question and getting an answer right away. The business that answers first usually wins the customer. An AI assistant makes sure that is you, even at 10 PM on a Sunday.</p>
  </div>
  <div class="tva-why tvs-up">
    <div><b>&#127769;</b><h3>Your customers shop after hours</h3><p>Nights and weekends are when people finally have time to look. Your assistant is there when you can&#39;t pick up.</p></div>
    <div><b>&#9889;</b><h3>Speed wins the job</h3><p>People reach out to more than one business. The first one to answer is usually the one they hire.</p></div>
    <div><b>&#128682;</b><h3>Most visitors leave quietly</h3><p>Most people never call or fill out a form. A friendly &ldquo;Can I help?&rdquo; turns browsers into real leads.</p></div>
  </div>
</section>'''

FEAT = '''<section class="tvs-sec tva-feat" id="tva-feat">
  <div class="tvs-head tvs-up">
    <p class="tvs-eyebrow">AI Chat Assistant</p>
    <h2>Smart, friendly, and it never misses a lead.</h2>
    <p>We build your assistant, teach it your business, and add it to your site. You just watch the leads come in.</p>
  </div>
  <div class="tva-grid">
    <div class="tva-c tvs-up"><span>&#128172;</span><h3>Answers instantly, 24/7</h3><p>Hours, prices, services, service area, parking, policies: anything you teach it, answered in seconds.</p></div>
    <div class="tva-c tvs-up"><span>&#128241;</span><h3>Captures every lead</h3><p>Name, phone and what they need, sent to your email or phone the moment they ask.</p></div>
    <div class="tva-c tvs-up"><span>&#128197;</span><h3>Books and quotes</h3><p>Sends people straight to your booking calendar, quote form or online ordering.</p></div>
    <div class="tva-c tvs-up"><span>&#129504;</span><h3>Knows your business</h3><p>Trained on your services, prices and FAQs. It answers from your information, not guesses.</p></div>
    <div class="tva-c tvs-up"><span>&#129309;</span><h3>Smart handoff</h3><p>When a question needs you, it takes a message and gets you the details instead of making something up.</p></div>
    <div class="tva-c tvs-up"><span>&#128202;</span><h3>Monthly summary</h3><p>See what customers asked, how many leads came in, and what to add next. We keep it sharp for you.</p></div>
  </div>
  <div class="tva-works tvs-up"><p>Works on the website you already have</p><div><span>Wix</span><span>Squarespace</span><span>WordPress</span><span>GoDaddy</span><span>Shopify</span><span>Weebly</span><span>Custom sites</span></div></div>
</section>'''

TUNEUP = '''<section class="tvs-sec tva-tune" id="tva-tune">
  <div class="tva-tune-in tvs-up">
    <div>
      <p class="tvs-eyebrow">AI Tune-Up</p>
      <h2>Get your current website found by AI.</h2>
      <p>ChatGPT, Gemini, Copilot and Google&#39;s AI recommend the businesses they can read and trust. We tune up your site and your listings so they know exactly who you are, what you do and where, without rebuilding anything.</p>
      <p class="tva-rep"><b>You get a before and after report:</b> what AI said about your business before we started, and what it says after.</p>
    </div>
    <ul class="tva-list">
      <li><b>Business facts AI can read</b>Hidden code that tells AI your services, hours, location and service area</li>
      <li><b>Titles and FAQs the way people ask</b>Rewritten so your pages match real questions</li>
      <li><b>Google, Bing and Apple listings</b>Google Business Profile, Bing Places (it feeds ChatGPT and Copilot) and Apple Business Connect</li>
      <li><b>Listings that match everywhere</b>Same name, address and phone across the web, so AI isn&#39;t confused</li>
      <li><b>Nothing blocking AI</b>We check your site isn&#39;t accidentally shutting AI tools out</li>
      <li><b>Connected to Google and Bing</b>Search Console and Bing Webmaster set up so changes get picked up fast</li>
    </ul>
  </div>
</section>'''


PRICING = '''<section class="tvs-sec tvs-bundles" id="tvs-bundles">
  <div class="tvs-head tvs-up">
    <p class="tvs-eyebrow">Pricing</p>
    <h2>Add AI to your website. Keep the site you have.</h2>
    <p>Both work with the website you already have, wherever it is built or hosted.</p>
  </div>
  <div class="tvs-tiers tvs-up" role="tablist" aria-label="Choose your membership to see your price">
    <button type="button" role="tab" data-t="all">Walk-in price</button>
    <button type="button" role="tab" data-t="vip" class="on">Featured &amp; VIP members<em>Member pricing</em></button>
  </div>
  <div class="tvs-cards tvw-two">
    <article class="tvs-card tvs-pop tvs-up" data-b="aichat">
      <p class="tvs-badge">Lead generator</p>
      <p class="tvs-cname">AI Chat Assistant</p>
      <p class="tvs-cfor">A smart assistant on your current website that answers customers 24/7 and sends you every lead.</p>
      <p class="tvw-plabel on">Featured &amp; VIP member price*</p>
      <p class="tvs-was"></p>
      <p class="tvs-price"><sup>$</sup><b>%(cm0)s</b></p>
      <p class="tvs-mo">+ <b>$%(cm1)s</b>/mo</p>
      <p class="tvs-save"></p>
      <ul>
        <li>Built, trained and added to your site for you</li>
        <li>Answers questions 24/7 from your own information</li>
        <li>Every lead sent to your email or phone right away</li>
        <li>Links to your booking, quote form or ordering</li>
        <li>Smart handoff when a question needs you</li>
        <li>Monthly summary and tuning: just email us changes</li>
      </ul>
      <a class="tvs-btn tvs-blue tvs-wide tvw-go tva-pick" data-pick="ai_chat" href="#tvs-book">Get my AI assistant &rarr;</a>
    </article>
    <article class="tvs-card tvs-up" data-b="aitune">
      <p class="tvs-cname">AI Tune-Up</p>
      <p class="tvs-cfor">A one-time tune-up so ChatGPT, Google and other AI tools can find, understand and recommend you.</p>
      <p class="tvw-plabel on">Featured &amp; VIP member price*</p>
      <p class="tvs-was"></p>
      <p class="tvs-price"><sup>$</sup><b>%(tm0)s</b></p>
      <p class="tvs-mo">one time</p>
      <p class="tvs-save"></p>
      <ul>
        <li>Before and after &ldquo;Can AI find you?&rdquo; report</li>
        <li>Business facts code AI can read</li>
        <li>Page titles, descriptions and FAQs rewritten</li>
        <li>Google, Bing and Apple listings cleaned up</li>
        <li>Name, address and phone matched across the web</li>
        <li>Google Search Console and Bing Webmaster set up</li>
      </ul>
      <a class="tvs-btn tvs-line tvs-wide tvw-go tva-pick" data-pick="ai_tuneup" href="#tvs-book">Get my AI Tune-Up &rarr;</a>
    </article>
  </div>
  <p class="tvs-fine tvs-up"><b>Works with the site you have.</b> Wix, Squarespace, WordPress, GoDaddy, Shopify and custom sites. Some website builders only allow added code on their paid plans; we check yours first, free. Month to month, no contract. Want a site AI can fully read from the ground up? See our <a href="/websites">AI-Ready websites</a>, where the AI assistant comes built in with AI-Powered.</p>
</section>''' % {"cm0": CHAT["member"][0], "cm1": CHAT["member"][1], "tm0": TUNE["member"][0]}

VS = '''<section class="tvs-sec tvs-vs">
  <div class="tvs-head tvs-up">
    <p class="tvs-eyebrow">Side by side</p>
    <h2>A do-it-yourself chat app vs. Three Village Local</h2>
  </div>
  <div class="tvs-table tvs-up" role="table">
    <div class="tvs-tr tvs-th" role="row"><span role="columnheader"></span><span role="columnheader">DIY chat app</span><span role="columnheader">Three Village Local</span></div>
    <div class="tvs-tr" role="row"><span role="cell">A chat bubble on your site</span><span role="cell" class="tvs-y">&#10003;</span><span role="cell" class="tvs-y">&#10003;</span></div>
    <div class="tvs-tr" role="row"><span role="cell">Set up and added to your site for you</span><span role="cell" class="tvs-n">&mdash;</span><span role="cell" class="tvs-y">&#10003;</span></div>
    <div class="tvs-tr" role="row"><span role="cell">Trained on your business by a real person</span><span role="cell" class="tvs-n">&mdash;</span><span role="cell" class="tvs-y">&#10003;</span></div>
    <div class="tvs-tr" role="row"><span role="cell">Leads sent straight to your phone or email</span><span role="cell" class="tvs-n">Varies</span><span role="cell" class="tvs-y">&#10003;</span></div>
    <div class="tvs-tr" role="row"><span role="cell">Monthly tuning and updates by email</span><span role="cell" class="tvs-n">&mdash;</span><span role="cell" class="tvs-y">&#10003;</span></div>
    <div class="tvs-tr" role="row"><span role="cell">Local team that knows Three Village</span><span role="cell" class="tvs-n">&mdash;</span><span role="cell" class="tvs-y">&#10003;</span></div>
  </div>
</section>'''

STEPS = '''<section class="tvs-sec tvs-steps">
  <div class="tvs-head tvs-up">
    <p class="tvs-eyebrow">How it works</p>
    <h2>Live on your site in about a week.</h2>
  </div>
  <ol class="tvs-ol">
    <li class="tvs-up"><b>1</b><h3>Send a message</h3><p>Tell us about your business and send us your website link.</p></li>
    <li class="tvs-up"><b>2</b><h3>We learn your business</h3><p>We read your site and gather your services, prices, hours and FAQs.</p></li>
    <li class="tvs-up"><b>3</b><h3>We add it to your site</h3><p>One small line of code. We add it, or send you simple steps.</p></li>
    <li class="tvs-up"><b>4</b><h3>Leads come in</h3><p>Customers get answers 24/7 and you get every lead.</p></li>
  </ol>
</section>'''

FAQ = '''<section class="tvs-sec tvs-faq">
  <div class="tvs-head tvs-up"><p class="tvs-eyebrow">Questions</p><h2>Good questions, straight answers.</h2></div>
  <div class="tvs-qs tvs-up">
    <details open><summary>Do I need a new website?</summary><p>No. Both add-ons work with the website you already have, no matter who built it or where it is hosted.</p></details>
    <details><summary>What if it doesn&#39;t know an answer?</summary><p>It answers from the information you give us. When a question needs you, it says so, takes the customer&#39;s name and number, and sends the details to you instead of guessing.</p></details>
    <details><summary>How do I get the leads?</summary><p>Every lead is sent to your email (and phone, if you like) right away, with the customer&#39;s name, number and what they need.</p></details>
    <details><summary>Can I change what it says?</summary><p>Anytime. New prices, specials, hours or services: just email or text us and we update it.</p></details>
    <details><summary>Will it work on my website builder?</summary><p>Almost always. Wix, Squarespace, WordPress, GoDaddy, Shopify and custom sites all work. A few builders only allow added code on their paid plans, so we check yours first, free.</p></details>
    <details><summary>What is the AI Tune-Up?</summary><p>A one-time set of fixes to your website and your Google, Bing and Apple listings so AI tools like ChatGPT can understand your business and recommend you. You get a before and after report.</p></details>
    <details><summary>Is there a contract?</summary><p>No. The AI assistant is month to month. The AI Tune-Up is a one-time fee.</p></details>
    <details><summary>Do I have to be a Three Village Local member?</summary><p>No. Anyone can sign up at our walk-in price. Featured and VIP members of Three Village Local get member pricing.</p></details>
  </div>
</section>'''

h = W.HTML
i, j = sec(h, "tvs-hero")
h = h[:i] + HERO + h[j:]
h = cut(h, "tvw-strip")
h = cut(h, "tvs-sec tvw-shift")
h = swap(h, "tvs-sec tvw-ai", NEXT + "\n\n" + FEAT + "\n\n" + TUNEUP)
h = cut(h, "tvs-sec tvw-bot")
h = swap(h, "tvs-sec tvs-bundles", PRICING)
h = swap(h, "tvs-sec tvs-vs", VS)
h = swap(h, "tvs-sec tvs-steps", STEPS)
h = swap(h, "tvs-sec tvs-faq", FAQ)
h = rep(h, "<h2>Let&#39;s build your AI-ready website.</h2>", "<h2>Let&#39;s put AI to work on your website.</h2>")
h = rep(h, "<p class=\"tvw-cta3-s\">Designed, built and hosted for you. Updates included. First month included.</p>",
        "<p class=\"tvw-cta3-s\">No new website needed. Set up for you. Every lead sent to you.</p>")
h = rep(h, '<a class="tvs-btn tvw-btn-o" href="#tvs-bundles">See the packages</a>', '<a class="tvs-btn tvw-btn-o" href="#tvs-bundles">See pricing</a>')
h = rep(h, "mailto:hello@threevillagelocal.com?subject=Websites", "mailto:hello@threevillagelocal.com?subject=AI%20for%20my%20website")
h = re.sub(r'<p class="tvw-small">.*?</p>', '<p class="tvw-small">*Member pricing is for Featured and VIP tier members of Three Village Local. Walk-in pricing applies to everyone else.</p>', h, count=1, flags=re.S)
assert "\\" not in h and "tvw-dev" not in h
HTML = h

PRICES = "aichat:{all:[%d,%d],free:[%d,%d],featured:[%d,%d],vip:[%d,%d]},aitune:{all:[%d,0],free:[%d,0],featured:[%d,0],vip:[%d,0]}," % (
    CHAT["all"] + CHAT["member"] * 3 + (TUNE["all"][0],) + (TUNE["member"][0],) * 3)
# Pricing buttons preselect the right option in the shared services form (field "bundle", form 343) and keep the hidden-field trick.
PICKJS = '''<script>(function(){var pick='ai_chat';document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('#tvs .tva-pick');if(a){pick=a.getAttribute('data-pick');set()}});
function set(){var s=document.querySelector('#tvs-form-slot select[name="bundle"]');if(s){s.value=pick;return true}return false}
var n=0,iv=setInterval(function(){if(set()||++n>60)clearInterval(iv)},300);
[].forEach.call(document.querySelectorAll('#tvs .tvs-card[data-b="aitune"] .tvs-mo'),function(m){new MutationObserver(function(){if(m.textContent!=='one time')m.textContent='one time'}).observe(m,{childList:true,subtree:true,characterData:true})})})();</script>'''

CSS = '''
.tva-hvis{padding:28px 34px 28px 24px}
.tvs-hero:has(.tva-hvis){min-height:680px}
.tva-try{width:100%;max-width:430px;margin:0 auto}
.tva-try-k{margin:0 0 10px!important;text-align:center;font-size:12.5px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--blue)}
.tva-try-k span{display:inline-block;width:8px;height:8px;border-radius:50%;background:#2fd28a;margin-right:8px;box-shadow:0 0 0 4px rgba(47,210,138,.2);vertical-align:1px}
.tva-try .tva-box{height:540px}
@media (max-width:900px){.tva-try .tva-box{height:520px;max-height:78vh}.tvs-hero:has(.tva-hvis){display:flex;flex-direction:column;min-height:0}.tva-hvis{order:2;border-radius:0 0 22px 22px!important}}
.tva-why{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;max-width:1060px;margin:0 auto}
.tva-why>div{background:#fff;border:1px solid #e3e9f2;border-radius:20px;padding:24px 22px;box-shadow:0 14px 34px -22px rgba(9,30,66,.25)}
.tva-why b{font-size:30px;display:block;margin-bottom:8px}
.tva-why h3{margin:0 0 6px!important;font-size:19px;color:var(--navy)}
.tva-why p{margin:0!important;font-size:15px;line-height:1.55;color:var(--mut)}
.tva-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;max-width:1060px;margin:0 auto}
.tva-c{background:linear-gradient(180deg,#f6f9ff,#fff);border:1px solid #dfe8f6;border-radius:20px;padding:22px}
.tva-c span{display:inline-flex;width:46px;height:46px;border-radius:14px;align-items:center;justify-content:center;font-size:23px;background:#e7f0ff;margin-bottom:10px}
.tva-c h3{margin:0 0 6px!important;font-size:18px;color:var(--navy)}
.tva-c p{margin:0!important;font-size:15px;line-height:1.55;color:var(--mut)}
.tva-works{max-width:1060px;margin:26px auto 0;text-align:center}
.tva-works p{margin:0 0 10px!important;font-size:12.5px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--mut)}
.tva-works div{display:flex;flex-wrap:wrap;justify-content:center;gap:8px}
.tva-works span{font-size:14px;font-weight:800;padding:8px 15px;border-radius:999px;background:#fff;border:1px solid #dfe6f0;color:var(--navy)}
.tva-tune-in{display:grid;grid-template-columns:1fr 1.1fr;gap:36px;align-items:start;max-width:1060px;margin:0 auto;padding:34px;border-radius:26px;background:linear-gradient(150deg,#0b1f4b,#123a7a);color:#fff}
.tva-tune-in h2{color:#fff!important;font-size:34px;line-height:1.12;margin:0 0 12px!important}
.tva-tune-in .tvs-eyebrow{color:#8fc1ff!important}
.tva-tune-in>div>p{color:#d6e3f7!important;font-size:16px;line-height:1.6}
.tva-rep{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16);border-radius:14px;padding:14px 16px}
.tva-rep b{color:#f2c94c}
.tva-list{list-style:none;margin:0;padding:0;display:grid;gap:10px}
.tva-list li{background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.14);border-radius:14px;padding:12px 14px 12px 42px;position:relative;font-size:14.5px;line-height:1.45;color:#cfdcf1}
.tva-list li:before{content:"✓";position:absolute;left:14px;top:11px;color:#5ee0a0;font-weight:800}
.tva-list li b{display:block;color:#fff;font-size:15.5px}
@media (max-width:900px){.tva-why,.tva-grid{grid-template-columns:1fr}.tva-tune-in{grid-template-columns:1fr;padding:24px 20px}.tva-tune-in h2{font-size:28px}.tva-hvis{padding:24px 14px}}
'''

_rd = W.rd


def rd(f):
    if f == "page.html":
        return HTML
    s = _rd(f)
    if f == "page.css":
        return s + CSS
    if f == "page.js":
        return rep(s, "var P={", "var P={" + PRICES) + PICKJS + '<script src="https://3vl-ai-assistant.vercel.app/widget.js" data-mount="#tva-live" defer></script>'
    return s


D.rd = rd
if __name__ == "__main__":
    D.main()
