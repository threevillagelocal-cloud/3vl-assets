"""'How it works' page for the AI Assistant + AI Optimization (owner 11/3/2026): the Tune-Up first and why it sets the assistant up
for success, then our training and fact-finding, how it runs on their site, launch and upkeep. Same look as /ai-assistant.
    python site/ai-assistant-page/how.py          -> widget "3VL Page AI Assistant How Preview" + hidden /preview-ai-assistant-how
    python site/ai-assistant-page/how.py --live   -> widget "3VL Page AI Assistant How" + /ai-assistant-how-it-works"""
import importlib.util, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("aibuild", os.path.join(HERE, "build.py"))
A = importlib.util.module_from_spec(spec)
spec.loader.exec_module(A)
D, sec, cut, swap, rep = A.D, A.sec, A.cut, A.swap, A.rep

MAIN = "/ai-assistant" if D.LIVE else "/preview-ai-assistant"
D.NAME = "3VL Page AI Assistant How" if D.LIVE else "3VL Page AI Assistant How Preview"
D.SLUG = "ai-assistant-how-it-works" if D.LIVE else "preview-ai-assistant-how"
D.TITLE = "How Our AI Assistant Works: AI Optimization, Training and Launch | Three Village Local"
D.DESC = ("Step by step: we AI-optimize your current website and listings, train an AI assistant on your business, "
          "and launch it on your site to answer customers 24/7 and send you every lead.")
D.FB_TITLE = "How we build your AI assistant, step by step."

HERO = '''<section class="tvs-hero tvh-hero">
  <div class="tvw-hvis tvh-vis"><ol class="tvh-map">
    <li><b>1</b><div><em>AI optimization</em>Your facts, clean and consistent everywhere</div></li>
    <li><b>2</b><div><em>Training</em>We learn your business like a new hire</div></li>
    <li><b>3</b><div><em>Testing</em>We try to trip it up before you see it</div></li>
    <li><b>4</b><div><em>Launch</em>Live on your site, leads to your inbox</div></li>
  </ol></div>
  <div class="tvs-hin tvs-up">
    <p class="tvs-kick"><span class="tvs-dot"></span>How it works</p>
    <h1>How we build your<br><span>AI assistant.</span></h1>
    <p class="tvs-sub">It starts with AI Website Optimization so ChatGPT, Google and other AI tools understand your business. Then we train your assistant on everything your customers ask, test it, and put it to work on your site.</p>
    <div class="tvs-ctas">
      <a class="tvs-btn tvs-blue" href="%(main)s#tva-live">Try the live demo</a>
      <a class="tvs-btn tvs-ghost" href="#tvs-book">Send us a message</a>
    </div>
    <ul class="tvs-trust"><li><b>About 7 days</b>to go live</li><li><b>You approve</b>everything first</li><li><b>No new</b>website needed</li></ul>
  </div>
</section>''' % {"main": MAIN}

STEP1 = '''<section class="tvs-sec tvh-step" id="tvh-1">
  <div class="tvs-head tvs-up"><p class="tvs-eyebrow">Step 1 &middot; AI Website Optimization</p><h2>First, we optimize your website so AI notices and recommends you.</h2>
  <p>More people now ask ChatGPT, Google&#39;s AI, Copilot and Siri who to call. Those tools recommend the businesses they can read and trust. So before we build anything, we optimize your website and your listings for AI.</p></div>
  <div class="tva-grid">
    <div class="tva-c tvs-up"><span>&#128269;</span><h3>Easier to find</h3><p>Clear business facts on your site, written so Google and AI tools know exactly what you do and where.</p></div>
    <div class="tva-c tvs-up"><span>&#128205;</span><h3>Listings that match</h3><p>Google Business Profile, Bing Places and Apple Business Connect cleaned up, with the same name, address and phone everywhere.</p></div>
    <div class="tva-c tvs-up"><span>&#128222;</span><h3>More calls and directions</h3><p>A complete Google profile with services, photos and hours brings more taps to call and get directions.</p></div>
    <div class="tva-c tvs-up"><span>&#10067;</span><h3>FAQs the way people ask</h3><p>Page titles, descriptions and an FAQ written the way real customers ask AI and Google.</p></div>
    <div class="tva-c tvs-up"><span>&#128275;</span><h3>Nothing blocking AI</h3><p>We make sure your site isn&#39;t accidentally shutting AI tools out, and connect Google and Bing so updates get picked up.</p></div>
    <div class="tva-c tvs-up"><span>&#128202;</span><h3>Before and after report</h3><p>See what AI tools said about your business before we started, and what they say after.</p></div>
  </div>
  <div class="tvh-why tvs-up"><b>Why AI optimization comes first</b><p>The facts we organize for Google and AI become the exact knowledge your assistant answers from. One correct set of facts, everywhere: your website, Google, Bing, Apple and your assistant. That&#39;s what keeps your assistant accurate from day one, instead of guessing.</p></div>
</section>'''

STEP2 = '''<section class="tvs-sec tvh-step tvh-alt" id="tvh-2">
  <div class="tvs-head tvs-up"><p class="tvs-eyebrow">Step 2 &middot; Training and fact-finding</p><h2>We learn your business like a new employee would.</h2>
  <p>We read your website, your Google profile and your reviews, then send you a short fact sheet to fill in or correct. Email is fine; a quick call is optional.</p></div>
  <div class="tvh-train">
    <div class="tvh-col tvs-up"><h3>What we teach it</h3><ul>
      <li><b>Your services</b>What you do, what&#39;s included, what you don&#39;t do</li>
      <li><b>Prices</b>Only the prices or ranges you approve, or &ldquo;we&#39;ll quote it&rdquo;</li>
      <li><b>Hours and seasons</b>Regular hours, holidays, seasonal changes</li>
      <li><b>Where you work</b>Your towns, service area and locations</li>
      <li><b>Booking</b>Your calendar, quote form, ordering or reservation links</li>
      <li><b>Policies</b>Deposits, cancellations, warranties, payment, parking</li>
      <li><b>Real questions</b>Your top FAQs, plus questions from your reviews and inbox</li>
    </ul></div>
    <div class="tvh-col tvs-up"><h3>How we want it to act</h3><ul>
      <li><b>Your name</b>It&#39;s named after your business, like &ldquo;Sun-Up Awnings Assistant,&rdquo; in your colors</li>
      <li><b>Your voice</b>Friendly and casual, or polished and formal</li>
      <li><b>When to hand off</b>Which questions should go straight to you</li>
      <li><b>Do-not-say list</b>Topics, promises or prices it should never mention</li>
      <li><b>Industry rules</b>Disclaimers and guidelines for legal, financial, insurance, medical and other regulated fields</li>
      <li><b>Lead details</b>What to ask for: name, phone or email, and what they need</li>
    </ul></div>
  </div>
  <div class="tvh-test tvs-up"><span>&#129514;</span><div><b>Then we try to trip it up.</b><p>Before you ever see it, we ask your assistant dozens of real and tricky customer questions, check every answer against your facts, and fix anything that&#39;s off. Then you test it yourself and approve it before it goes live.</p></div></div>
</section>'''

STEP3 = '''<section class="tvs-sec tvh-step" id="tvh-3">
  <div class="tvs-head tvs-up"><p class="tvs-eyebrow">Step 3 &middot; On your site</p><h2>How it works for your customers.</h2>
  <p>A small chat bubble with your business name appears on your website. Here&#39;s what happens when someone uses it.</p></div>
  <ol class="tvh-flow tvs-up">
    <li><b>&#128172;</b><em>A visitor asks</em>&ldquo;Do you do weekend appointments?&rdquo;</li>
    <li><b>&#9889;</b><em>It answers in seconds</em>From your facts, day or night</li>
    <li><b>&#128587;</b><em>They&#39;re interested</em>It asks for their name and best contact</li>
    <li><b>&#128241;</b><em>You get the lead</em>Name, contact, what they need and the chat, in your inbox</li>
  </ol>
  <div class="tva-grid tvh-rules">
    <div class="tva-c tvs-up"><span>&#129309;</span><h3>Live person handoff</h3><p>If someone asks for a real person, you get an instant text and email with their details. It never guesses, and always says it&#39;s an AI assistant.</p></div>
    <div class="tva-c tvs-up"><span>&#9878;&#65039;</span><h3>Follows your industry rules</h3><p>General information only for regulated fields, the right disclaimers, and no sensitive information collected.</p></div>
    <div class="tva-c tvs-up"><span>&#128241;</span><h3>Fast on every device</h3><p>Works on phones and computers and loads after your page, so it never slows your site down.</p></div>
  </div>
</section>'''

STEP4 = '''<section class="tvs-sec tvh-step tvh-alt" id="tvh-4">
  <div class="tvs-head tvs-up"><p class="tvs-eyebrow">Step 4 &middot; Launch and keep it sharp</p><h2>Live in about a week. Better every month.</h2></div>
  <div class="tva-grid">
    <div class="tva-c tvs-up"><span>&#128640;</span><h3>We install it</h3><p>One small line of code on your Wix, Squarespace, WordPress, GoDaddy, Shopify or custom site. We add it, or send you simple steps.</p></div>
    <div class="tva-c tvs-up"><span>&#128232;</span><h3>Monthly summary</h3><p>What customers asked, how many leads came in, and what we&#39;d add next.</p></div>
    <div class="tva-c tvs-up"><span>&#9999;&#65039;</span><h3>Changes anytime</h3><p>New prices, specials or hours? Email or text us and we update your assistant.</p></div>
  </div>
  <p class="tvh-back tvs-up"><a class="tvs-btn tvs-blue" href="%(main)s#tvs-bundles">See pricing</a> <a class="tvs-btn tvs-ghost" href="%(main)s#tva-live">Try the live demo</a></p>
</section>''' % {"main": MAIN}

h = A.HTML
i, j = sec(h, "tvs-hero")
h = h[:i] + HERO + h[j:]
for c in ("tvs-sec tva-next", "tvs-sec tva-feat", "tvs-sec tva-tune", "tvs-sec tvs-bundles", "tvs-sec tvs-vs", "tvs-sec tvs-steps", "tvs-sec tvs-faq"):
    h = cut(h, c)
i, _ = sec(h, "tvw-cta3")
STRIP = A.W.STRIP_SEC.replace("<p>Get recommended on the AI tools your customers use</p>", "<p>AI optimization built to get you noticed and recommended on</p>")
h = h[:i] + STRIP + "\n\n" + STEP1 +"\n\n" + STEP2 + "\n\n" + STEP3 + "\n\n" + STEP4 + "\n\n" + h[i:]
h = re.sub(r'<p class="tvw-small">.*?</p>', "", h, count=1, flags=re.S)
h = h.replace('href="#tvs-bundles">See pricing</a>', 'href="%s#tvs-bundles">See pricing</a>' % MAIN)
assert "tva-live" not in h.replace(MAIN + "#tva-live", "")
HTML = h

CSS = '''
.tvh-vis{display:flex;align-items:center;justify-content:center;padding:36px}
.tvh-map{list-style:none;margin:0;padding:0;display:grid;gap:14px;width:100%;max-width:400px;position:relative}
.tvh-map:before{content:"";position:absolute;left:27px;top:30px;bottom:30px;width:3px;border-radius:3px;background:linear-gradient(#4da3ff,#2fd28a);transform-origin:top;animation:tvhLine 1.6s .3s ease both}
.tvh-map li{position:relative;display:flex;gap:14px;align-items:center;background:#fff;border-radius:18px;padding:14px 16px;box-shadow:0 18px 40px -24px rgba(9,30,66,.45);opacity:0;animation:tvhIn .6s ease forwards}
.tvh-map li:nth-child(1){animation-delay:.4s}.tvh-map li:nth-child(2){animation-delay:.8s}.tvh-map li:nth-child(3){animation-delay:1.2s}.tvh-map li:nth-child(4){animation-delay:1.6s}
.tvh-map b{flex:none;width:26px;height:26px;margin-left:1px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:var(--blue);color:#fff;font-size:13.5px;box-shadow:0 0 0 5px #e7f0ff;position:relative;z-index:1}
.tvh-map li:last-child b{background:#2fd28a;box-shadow:0 0 0 5px #dff7ec}
.tvh-map em{display:block;font-style:normal;font-weight:800;color:var(--navy);font-size:16px}
.tvh-map div{font-size:14px;color:var(--mut);line-height:1.4}
.tvh-alt{background:linear-gradient(180deg,#f3f7fd,#fff)}
.tvh-why{max-width:1060px;margin:22px auto 0;padding:22px 24px;border-radius:20px;background:linear-gradient(150deg,#0b1f4b,#1a4596);color:#d6e3f7}
.tvh-why b{display:block;color:#f2c94c;font-size:17px;margin-bottom:6px}
.tvh-why p{margin:0!important;font-size:16px;line-height:1.6}
.tvh-train{display:grid;grid-template-columns:1fr 1fr;gap:20px;max-width:1060px;margin:0 auto}
.tvh-col{background:#fff;border:1px solid #dfe8f6;border-radius:22px;padding:22px 24px;box-shadow:0 14px 34px -24px rgba(9,30,66,.3)}
.tvh-col h3{margin:0 0 12px!important;font-size:19px;color:var(--navy)}
.tvh-col ul{list-style:none;margin:0;padding:0;display:grid;gap:10px}
.tvh-col li{position:relative;padding-left:30px;font-size:14.5px;line-height:1.45;color:var(--mut)}
.tvh-col li:before{content:"✓";position:absolute;left:0;top:0;width:20px;height:20px;border-radius:50%;background:#e7f0ff;color:var(--blue);font-size:12px;font-weight:800;display:flex;align-items:center;justify-content:center}
.tvh-col li b{display:block;color:var(--navy);font-size:15.5px}
.tvh-test{display:flex;gap:16px;align-items:flex-start;max-width:1060px;margin:20px auto 0;padding:20px 22px;border-radius:20px;background:#eafaf2;border:1px solid #bfe9d3}
.tvh-test>span{font-size:28px;line-height:1}.tvh-test b{display:block;font-size:17px;color:#14553a;margin-bottom:4px}.tvh-test p{margin:0!important;font-size:15px;line-height:1.55;color:#2f5a45}
.tvh-flow{list-style:none;margin:0 auto 22px;padding:0;display:grid;grid-template-columns:repeat(4,1fr);gap:14px;max-width:1060px;counter-reset:f}
.tvh-flow li{position:relative;background:#fff;border:1px solid #dfe8f6;border-radius:20px;padding:20px 18px;font-size:14.5px;line-height:1.45;color:var(--mut)}
.tvh-flow li:not(:last-child):after{content:"→";position:absolute;right:-13px;top:50%;margin-top:-12px;width:24px;height:24px;border-radius:50%;background:var(--blue);color:#fff;font-size:13px;font-weight:800;display:flex;align-items:center;justify-content:center;z-index:1}
.tvh-flow b{display:block;font-size:26px;margin-bottom:6px}.tvh-flow em{display:block;font-style:normal;font-weight:800;color:var(--navy);font-size:16px;margin-bottom:2px}
.tvh-flow.tvs-in li{animation:tvhIn .55s ease both}.tvh-flow.tvs-in li:nth-child(2){animation-delay:.2s}.tvh-flow.tvs-in li:nth-child(3){animation-delay:.4s}.tvh-flow.tvs-in li:nth-child(4){animation-delay:.6s}
.tvh-flow li:last-child{background:#eafaf2;border-color:#bfe9d3}
.tvh-back{text-align:center;margin:26px 0 0!important}.tvh-back .tvs-btn{margin:4px}
@keyframes tvhIn{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
@keyframes tvhLine{from{transform:scaleY(0)}to{transform:scaleY(1)}}
@media (max-width:900px){.tvh-train{grid-template-columns:1fr}.tvh-flow{grid-template-columns:1fr 1fr}.tvh-flow li:nth-child(2):after{display:none}.tvh-vis{padding:22px 16px}.tvs-hero.tvh-hero{display:flex;flex-direction:column}.tvh-vis{order:2}}
@media (max-width:520px){.tvh-flow{grid-template-columns:1fr}.tvh-flow li:not(:last-child):after{right:50%;top:auto;bottom:-13px;margin:0 -12px 0 0;content:"↓"}}
@media (prefers-reduced-motion:reduce){.tvh-map li,.tvh-map:before,.tvh-flow li{animation:none!important;opacity:1}}
'''

_ard = A.rd


def rd(f):
    if f == "page.html":
        return HTML
    s = _ard(f)
    if f == "page.css":
        return s + CSS
    if f == "page.js":   # chat as a floating bubble here instead of the hero demo
        return s.replace(' data-mount="#tva-live" defer></script>', ' defer></script>')
    return s


D.rd = rd
if __name__ == "__main__":
    D.main()
