"""Websites landing page (owner 10/21/2026): AI-Ready vs AI-Powered websites, member pricing. "Get started" = brief form -> free consultation -> owner invoices (owner 10/21: no payment on the site).
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

D.NAME = "3VL Page Websites" if D.LIVE else "3VL Page Websites Preview"   # 10/22: preview gets its own widget so it never changes the live page
D.SLUG = "websites" if D.LIVE else "preview-websites"
D.TITLE = "AI-Ready Websites for Long Island Businesses | Three Village Local"
D.DESC = ("Websites built for customers and for AI: designed, built and hosted for you, readable by Google and AI assistants like ChatGPT, "
          "with an optional AI chat assistant. Member pricing for Three Village Local businesses.")
D.FB_TITLE = "AI-Driven Websites: Design, Build, Host"
D.FB_IMAGE = "https://threevillagelocal-cloud.github.io/3vl-share/site/websites/share-ai-websites-v1.jpg"


def section(src, cls):
    i = src.index('<section class="' + cls)
    return src[i:src.index('</section>', i) + len('</section>')]


src = open(os.path.join(SV, "page.html"), encoding="utf-8").read()
book = section(src, "tvs-sec tvs-book").replace("<h2>Book your free 15-minute call.</h2>", "<h2>Rather talk it through first?</h2>") \
    .replace("<p>Tell us a little about your business.", "<p>Book a free consultation. Tell us a little about your business and we will reach out to set up a time.")


START = "/website-start?plan="   # Get started -> project brief -> consultation, invoice after (owner 10/21)


def card(key, tag, name, one, items, featured=False):
    m, r = P["web-%s-member" % key], P["web-%s-regular" % key]
    lis = "".join("<li>%s</li>" % i for i in items)
    return '''<article class="tvw-card%s tvs-up">
  %s<p class="tvw-tag">%s</p>
  <h3>%s</h3><p class="tvw-one">%s</p>
  <p class="tvw-mp"><span class="tvw-m">3VL member price</span><span class="tvw-r">Regular price</span></p>
  <div class="tvw-price"><span class="tvw-m"><b>$%s</b> to start</span><span class="tvw-r"><b>$%s</b> to start</span></div>
  <p class="tvw-then">Includes your first month. Then <b>$%s/mo</b>.</p>
  <p class="tvw-save"><span class="tvw-m">Member founding price. Regular $%s.</span><span class="tvw-r">3VL members pay $%s.</span></p>
  <ul>%s</ul>
  <a class="tvs-btn %s tvs-wide tvw-pay" data-m="%s" data-r="%s" href="%s">Get started &rarr;</a>
  <a class="tvw-consult" href="#tvs-book">Or book a free consultation</a>
</article>''' % (" tvw-feat" if featured else "", '<span class="tvw-pop">Most popular</span>' if featured else "", tag,
                 name, one, "{:,}".format(m[0]), "{:,}".format(r[0]), m[1], "{:,}".format(r[0]), "{:,}".format(m[0]), lis,
                 "tvs-white" if featured else "tvs-blue", START + "web-%s-member" % key, START + "web-%s-regular" % key, START + "web-%s-member" % key)


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

<section class="tvs-sec tvw-logos tvs-up"><p>Built to be found on</p><div class="tvw-logo-row"><span class="tvw-logo"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#4285F4" d="M12.48 10.92v3.28h7.84c-.24 1.84-.853 3.187-1.787 4.133-1.147 1.147-2.933 2.4-6.053 2.4-4.827 0-8.6-3.893-8.6-8.72s3.773-8.72 8.6-8.72c2.6 0 4.507 1.027 5.907 2.347l2.307-2.307C18.747 1.44 16.133 0 12.48 0 5.867 0 .307 5.387.307 12s5.56 12 12.173 12c3.573 0 6.267-1.173 8.373-3.36 2.16-2.16 2.84-5.213 2.84-7.667 0-.76-.053-1.467-.173-2.053H12.48z"/></svg>Google</span><span class="tvw-logo"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#34A853" d="M19.527 4.799c1.212 2.608.937 5.678-.405 8.173-1.101 2.047-2.744 3.74-4.098 5.614-.619.858-1.244 1.75-1.669 2.727-.141.325-.263.658-.383.992-.121.333-.224.673-.34 1.008-.109.314-.236.684-.627.687h-.007c-.466-.001-.579-.53-.695-.887-.284-.874-.581-1.713-1.019-2.525-.51-.944-1.145-1.817-1.79-2.671L19.527 4.799zM8.545 7.705l-3.959 4.707c.724 1.54 1.821 2.863 2.871 4.18.247.31.494.622.737.936l4.984-5.925-.029.01c-1.741.601-3.691-.291-4.392-1.987a3.377 3.377 0 0 1-.209-.716c-.063-.437-.077-.761-.004-1.198l.001-.007zM5.492 3.149l-.003.004c-1.947 2.466-2.281 5.88-1.117 8.77l4.785-5.689-.058-.05-3.607-3.035zM14.661.436l-3.838 4.563a.295.295 0 0 1 .027-.01c1.6-.551 3.403.15 4.22 1.626.176.319.323.683.377 1.045.068.446.085.773.012 1.22l-.003.016 3.836-4.561A8.382 8.382 0 0 0 14.67.439l-.009-.003zM9.466 5.868L14.162.285l-.047-.012A8.31 8.31 0 0 0 11.986 0a8.439 8.439 0 0 0-6.169 2.766l-.016.018 3.665 3.084z"/></svg>Google Maps</span><span class="tvw-logo"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#10A37F" d="M12 1.5l2.3 6.2 6.2 2.3-6.2 2.3L12 18.5l-2.3-6.2L3.5 10l6.2-2.3zM19 15l1 2.6 2.5 1-2.5.9-1 2.6-.9-2.6-2.6-.9 2.6-1z"/></svg>ChatGPT</span><span class="tvw-logo"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#8E75B2" d="M11.04 19.32Q12 21.51 12 24q0-2.49.93-4.68.96-2.19 2.58-3.81t3.81-2.55Q21.51 12 24 12q-2.49 0-4.68-.93a12.3 12.3 0 0 1-3.81-2.58 12.3 12.3 0 0 1-2.58-3.81Q12 2.49 12 0q0 2.49-.96 4.68-.93 2.19-2.55 3.81a12.3 12.3 0 0 1-3.81 2.58Q2.49 12 0 12q2.49 0 4.68.96 2.19.93 3.81 2.55t2.55 3.81"/></svg>Gemini</span><span class="tvw-logo"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#1FB8CD" d="M22.3977 7.0896h-2.3106V.0676l-7.5094 6.3542V.1577h-1.1554v6.1966L4.4904 0v7.0896H1.6023v10.3976h2.8882V24l6.932-6.3591v6.2005h1.1554v-6.0469l6.9318 6.1807v-6.4879h2.8882V7.0896zm-3.4657-4.531v4.531h-5.355l5.355-4.531zm-13.2862.0676 4.8691 4.4634H5.6458V2.6262zM2.7576 16.332V8.245h7.8476l-6.1149 6.1147v1.9723H2.7576zm2.8882 5.0404v-3.8852h.0001v-2.6488l5.7763-5.7764v7.0111l-5.7764 5.2993zm12.7086.0248-5.7766-5.1509V9.0618l5.7766 5.7766v6.5588zm2.8882-5.0652h-1.733v-1.9723L13.3948 8.245h7.8478v8.087z"/></svg>Perplexity</span><span class="tvw-logo"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#D97757" d="m4.7144 15.9555 4.7174-2.6471.079-.2307-.079-.1275h-.2307l-.7893-.0486-2.6956-.0729-2.3375-.0971-2.2646-.1214-.5707-.1215-.5343-.7042.0546-.3522.4797-.3218.686.0608 1.5179.1032 2.2767.1578 1.6514.0972 2.4468.255h.3886l.0546-.1579-.1336-.0971-.1032-.0972L6.973 9.8356l-2.55-1.6879-1.3356-.9714-.7225-.4918-.3643-.4614-.1578-1.0078.6557-.7225.8803.0607.2246.0607.8925.686 1.9064 1.4754 2.4893 1.8336.3643.3035.1457-.1032.0182-.0728-.164-.2733-1.3539-2.4467-1.445-2.4893-.6435-1.032-.17-.6194c-.0607-.255-.1032-.4674-.1032-.7285L6.287.1335 6.6997 0l.9957.1336.419.3642.6192 1.4147 1.0018 2.2282 1.5543 3.0296.4553.8985.2429.8318.091.255h.1579v-.1457l.1275-1.706.2368-2.0947.2307-2.6957.0789-.7589.3764-.9107.7468-.4918.5828.2793.4797.686-.0668.4433-.2853 1.8517-.5586 2.9021-.3643 1.9429h.2125l.2429-.2429.9835-1.3053 1.6514-2.0643.7286-.8196.85-.9046.5464-.4311h1.0321l.759 1.1293-.34 1.1657-1.0625 1.3478-.8804 1.1414-1.2628 1.7-.7893 1.36.0729.1093.1882-.0183 2.8535-.607 1.5421-.2794 1.8396-.3157.8318.3886.091.3946-.3278.8075-1.967.4857-2.3072.4614-3.4364.8136-.0425.0304.0486.0607 1.5482.1457.6618.0364h1.621l3.0175.2247.7892.522.4736.6376-.079.4857-1.2142.6193-1.6393-.3886-3.825-.9107-1.3113-.3279h-.1822v.1093l1.0929 1.0686 2.0035 1.8092 2.5075 2.3314.1275.5768-.3218.4554-.34-.0486-2.2039-1.6575-.85-.7468-1.9246-1.621h-.1275v.17l.4432.6496 2.3436 3.5214.1214 1.0807-.17.3521-.6071.2125-.6679-.1214-1.3721-1.9246L14.38 17.959l-1.1414-1.9428-.1397.079-.674 7.2552-.3156.3703-.7286.2793-.6071-.4614-.3218-.7468.3218-1.4753.3886-1.9246.3157-1.53.2853-1.9004.17-.6314-.0121-.0425-.1397.0182-1.4328 1.9672-2.1796 2.9446-1.7243 1.8456-.4128.164-.7164-.3704.0667-.6618.4008-.5889 2.386-3.0357 1.4389-1.882.929-1.0868-.0062-.1579h-.0546l-6.3385 4.1164-1.1293.1457-.4857-.4554.0608-.7467.2307-.2429 1.9064-1.3114Z"/></svg>Claude</span><span class="tvw-logo"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#111111" d="M12.152 6.896c-.948 0-2.415-1.078-3.96-1.04-2.04.027-3.91 1.183-4.961 3.014-2.117 3.675-.546 9.103 1.519 12.09 1.013 1.454 2.208 3.09 3.792 3.039 1.52-.065 2.09-.987 3.935-.987 1.831 0 2.35.987 3.96.948 1.637-.026 2.676-1.48 3.676-2.948 1.156-1.688 1.636-3.325 1.662-3.415-.039-.013-3.182-1.221-3.22-4.857-.026-3.04 2.48-4.494 2.597-4.559-1.429-2.09-3.623-2.324-4.39-2.376-2-.156-3.675 1.09-4.61 1.09zM15.53 3.83c.843-1.012 1.4-2.427 1.245-3.83-1.207.052-2.662.805-3.532 1.818-.78.896-1.454 2.338-1.273 3.714 1.338.104 2.715-.688 3.559-1.701"/></svg>Siri &amp; Apple Maps</span></div></section>

<section class="tvs-sec tvw-stats tvs-up">
  <div><b>45%</b><span>of people used ChatGPT or another AI tool for a local recommendation last year, up from 6%</span></div>
  <div><b>58%</b><span>of the sources ChatGPT cites for local questions are the businesses' own websites</span></div>
  <div><b>7x</b><span>more likely to turn a lead into business when you answer within the hour</span></div>
</section>

<section class="tvs-sec tvw-show tvs-up">
  <div class="tvw-show-txt">
    <p class="tvs-eyebrow">Design &middot; Build &middot; Host</p>
    <h2>We build it.<br><span>Then we tell the whole town.</span></h2>
    <p>The same team that built and runs Three Village Local builds your site: fast, modern and AI-ready, on every screen. Then we launch it across Three Village Local, our social channels and the weekly email.</p>
    <ul class="tvw-show-list"><li>Designed around your business, not a template</li><li>Built for phones, tablets and desktops</li><li>Hosted, secured and updated for you</li></ul>
  </div>
  <div class="tvw-tab" aria-label="Three Village Local website on a tablet">
    <div class="tvw-tab-screen"><div class="tvw-tab-strip">
      <div class="tvw-tab-pg"><img src="https://threevillagelocal-cloud.github.io/3vl-share/site/websites/tablet-home.webp" alt="Three Village Local homepage" width="960" height="2929" loading="lazy" decoding="async"></div>
      <div class="tvw-tab-pg"><img src="https://threevillagelocal-cloud.github.io/3vl-share/site/websites/tablet-weekend.webp" alt="This Weekend page" width="960" height="2929" loading="lazy" decoding="async"></div>
      <div class="tvw-tab-pg"><img src="https://threevillagelocal-cloud.github.io/3vl-share/site/websites/tablet-eat.webp" alt="Restaurant directory" width="960" height="2929" loading="lazy" decoding="async"></div>
    </div></div>
    <span class="tvw-tab-cam"></span>
    <p class="tvw-tab-cap">threevillagelocal.com &middot; designed, built and hosted by our team</p>
  </div>
</section>

<section class="tvs-sec" id="tvw-plans">
  <div class="tvs-head tvs-up"><p class="tvs-eyebrow">Two ways to go modern</p><h2>AI-Ready or AI-Powered?</h2>
    <p><b>AI-Ready</b> means AI can find you. <b>AI-Powered</b> means AI works for you. Both are designed, built and hosted by us.</p><p class="tvw-memnote">Prices shown are <b>Three Village Local member prices</b>. Not a member? Uncheck the box to see regular pricing.</p></div>
  <label class="tvw-toggle tvs-up"><input type="checkbox" id="tvw-mem" checked> <span>I'm a Three Village Local member</span></label>
  <div class="tvw-cards">@@READY@@@@POWERED@@</div>
  <p class="tvs-fine tvs-up">Your start-up fee includes your first month. After that, the monthly plan covers hosting, security, updates and support, month to month. Your domain is registered in your name (usually $10 to $20 a year, paid to the registrar). <b>Need more?</b> Own Your Market adds weekly content, an online shop and a quarterly refresh: <a href="#tvs-book">ask us</a>.</p>
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

<section class="tvs-sec tvw-vs">
  <div class="tvs-head tvs-up"><p class="tvs-eyebrow">Side by side</p><h2>A template website vs. a Three Village Local website.</h2><p class="tvs-lede">Template services (Wix, Squarespace, GoDaddy and the monthly website rentals) get you online. We build the site that gets you found.</p></div>
  <div class="tvw-vs-grid">
    <div class="tvw-vs-hd tvs-up"><span></span><b class="t">Template website</b><b class="u">Three Village Local</b></div>
    <div class="tvw-vs-row tvs-up"><p class="tvw-vs-k">Design</p><div class="tvw-vs-t"><span>&#10005;</span>A template thousands of other businesses use</div><div class="tvw-vs-u"><span>&#10003;</span>Custom-designed for your business</div></div>
    <div class="tvw-vs-row tvs-up"><p class="tvw-vs-k">Who does the work</p><div class="tvw-vs-t"><span>&#10005;</span>You build it, or pay extra for help</div><div class="tvw-vs-u"><span>&#10003;</span>We write, build and launch it for you</div></div>
    <div class="tvw-vs-row tvs-up"><p class="tvw-vs-k">The words on your site</p><div class="tvw-vs-t"><span>&#10005;</span>You write them</div><div class="tvw-vs-u"><span>&#10003;</span>We write them the way customers search</div></div>
    <div class="tvw-vs-row tvs-up"><p class="tvw-vs-k">Can AI read it?</p><div class="tvw-vs-t"><span>&#10005;</span>Often buried in page-builder code</div><div class="tvw-vs-u"><span>&#10003;</span>Clean code Google and AI can read</div></div>
    <div class="tvw-vs-row tvs-up"><p class="tvw-vs-k">Your business details labeled for search and AI</p><div class="tvw-vs-t"><span>&#10005;</span>Usually missing</div><div class="tvw-vs-u"><span>&#10003;</span>Services, hours, area and reviews labeled</div></div>
    <div class="tvw-vs-row tvs-up"><p class="tvw-vs-k">A page for every service, plus FAQs</p><div class="tvw-vs-t"><span>&#10005;</span>One generic services page</div><div class="tvw-vs-u"><span>&#10003;</span>Built in, written for you</div></div>
    <div class="tvw-vs-row tvs-up"><p class="tvw-vs-k">Speed on phones</p><div class="tvw-vs-t"><span>&#10005;</span>Heavy templates, often slow</div><div class="tvw-vs-u"><span>&#10003;</span>Built fast, mobile-first</div></div>
    <div class="tvw-vs-row tvs-up"><p class="tvw-vs-k">Hosting, domain and updates</p><div class="tvw-vs-t"><span>&#10005;</span>Separate bills, logins and DIY updates</div><div class="tvw-vs-u"><span>&#10003;</span>All included, domain in your name</div></div>
    <div class="tvw-vs-row tvs-up"><p class="tvw-vs-k">AI chat assistant</p><div class="tvw-vs-t"><span>&#10005;</span>A paid add-on app</div><div class="tvw-vs-u"><span>&#10003;</span>Included with AI-Powered</div></div>
    <div class="tvw-vs-row tvs-up"><p class="tvw-vs-k">Fresh blog posts and updates</p><div class="tvw-vs-t"><span>&#10005;</span>You write them</div><div class="tvw-vs-u"><span>&#10003;</span>Written and posted for you (AI-Powered)</div></div>
    <div class="tvw-vs-row tvs-up"><p class="tvw-vs-k">Promotion to local customers</p><div class="tvw-vs-t"><span>&#10005;</span>None</div><div class="tvw-vs-u"><span>&#10003;</span>Launch spotlight on Three Village Local + 3 months Featured</div></div>
    <div class="tvw-vs-row tvs-up"><p class="tvw-vs-k">Help when you need it</p><div class="tvw-vs-t"><span>&#10005;</span>A support ticket or chatbot</div><div class="tvw-vs-u"><span>&#10003;</span>A local neighbor who picks up</div></div>
  </div>
</section>

<section class="tvs-sec tvs-tl">
  <div class="tvs-head tvs-up"><p class="tvs-eyebrow">How it works</p><h2>From sign-up to launch.</h2></div>
  <ol class="tvs-tlist">
    <li class="tvs-up"><em>Step 1</em><b>Tell us about your business</b><p>A quick brief online: your services, your style, your logo and photos.</p></li>
    <li class="tvs-up"><em>Step 2</em><b>Free consultation</b><p>We talk it through, confirm the right plan and send your invoice. We do the writing.</p></li>
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
.tvw-mp{margin:2px 0 6px!important}.tvw-mp span{display:inline-block;font-size:12px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;padding:5px 11px;border-radius:999px;background:#fff3d6;color:#8a5a00}.tvw-feat .tvw-mp span{background:rgba(255,215,106,.18);color:#ffd76a}
.tvw.tvw-reg .tvw-mp .tvw-r{display:inline-block}
.tvw-memnote{margin-top:10px!important;font-size:15px;color:#8a5a00!important;font-weight:600}

.tvw-logos{text-align:center;padding-top:18px;padding-bottom:6px}
.tvw-logos>p{margin:0 0 14px;font-size:13px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--sub,#5a6880)}
.tvw-logo-row{display:flex;flex-wrap:wrap;justify-content:center;gap:10px 12px}
.tvw-logo{display:inline-flex;align-items:center;gap:9px;padding:10px 16px;border:1px solid var(--line);border-radius:999px;background:#fff;font-weight:700;font-size:15px;color:#1a2233;box-shadow:0 4px 14px -8px rgba(9,30,66,.25)}
.tvw-logo svg{width:20px;height:20px;flex:none}

.tvw-show{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);gap:44px;align-items:center}
.tvw-show h2{font-size:40px;line-height:1.08;font-weight:800;margin:6px 0 14px}
.tvw-show h2 span{background:linear-gradient(90deg,var(--blue),var(--blue2));-webkit-background-clip:text;background-clip:text;color:transparent}
.tvw-show-txt>p{font-size:17px;line-height:1.6;color:var(--sub,#4a5a70)}
.tvw-show-list{list-style:none;margin:16px 0 0;padding:0}
.tvw-show-list li{position:relative;padding:6px 0 6px 30px;font-weight:600}
.tvw-show-list li:before{content:"✓";position:absolute;left:0;top:5px;width:20px;height:20px;border-radius:50%;background:var(--blue);color:#fff;font-size:12px;line-height:20px;text-align:center}
.tvw-tab{position:relative;background:linear-gradient(145deg,#1b2433,#05080d);border-radius:34px;padding:22px;box-shadow:0 30px 60px -20px rgba(9,30,66,.45),0 0 0 2px #2c3647 inset;transform:perspective(1600px) rotateY(-7deg) rotateX(3deg)}
.tvw-tab-cam{position:absolute;left:9px;top:50%;width:7px;height:7px;margin-top:-4px;border-radius:50%;background:#33415a}
.tvw-tab-screen{position:relative;aspect-ratio:4/3;overflow:hidden;border-radius:12px;background:#fff}
.tvw-tab-strip{position:absolute;inset:0;display:flex;width:300%;animation:tvwX 42s ease-in-out infinite}
.tvw-tab-pg{position:relative;width:33.3334%;height:100%;overflow:hidden}
.tvw-tab-pg img{display:block;width:100%;height:auto;animation:tvwY 42s ease-in-out infinite}
.tvw-tab-pg:nth-child(2) img{animation-name:tvwY2}.tvw-tab-pg:nth-child(3) img{animation-name:tvwY3}
.tvw-tab-cap{position:absolute;left:0;right:0;bottom:-34px;margin:0;text-align:center;font-size:13px;color:var(--sub,#5a6880)}
@keyframes tvwX{0%,29%{transform:translateX(0)}33%,62%{transform:translateX(-33.3333%)}66%,95%{transform:translateX(-66.6667%)}100%{transform:translateX(0)}}
@keyframes tvwY{0%,3%{transform:translateY(0)}27%,30%{transform:translateY(-74%)}34%,100%{transform:translateY(0)}}
@keyframes tvwY2{0%,36%{transform:translateY(0)}60%,63%{transform:translateY(-74%)}67%,100%{transform:translateY(0)}}
@keyframes tvwY3{0%,69%{transform:translateY(0)}93%,96%{transform:translateY(-74%)}100%{transform:translateY(0)}}
@media (prefers-reduced-motion:reduce){.tvw-tab-strip,.tvw-tab-pg img{animation:none}}
@media (max-width:900px){.tvw-show{grid-template-columns:1fr;gap:34px}.tvw-show h2{font-size:32px}.tvw-tab{transform:none;padding:14px;border-radius:24px}}

.tvw-vs-grid{display:grid;gap:10px;max-width:980px;margin:0 auto}
.tvw-vs-hd,.tvw-vs-row{display:grid;grid-template-columns:1.1fr 1fr 1.15fr;gap:10px;align-items:stretch}
.tvw-vs-hd b{padding:14px 16px;border-radius:16px 16px 0 0;font-size:15px;letter-spacing:.06em;text-transform:uppercase;text-align:center}
.tvw-vs-hd .t{background:#eef1f5;color:#66717e}.tvw-vs-hd .u{background:var(--navy);color:#fff}
.tvw-vs-k{margin:0!important;align-self:center;font-weight:800;color:var(--navy);font-size:16px}
.tvw-vs-t,.tvw-vs-u{display:flex;gap:10px;align-items:flex-start;padding:14px 16px;border-radius:14px;font-size:15.5px;line-height:1.4}
.tvw-vs-t{background:#f5f7fa;color:#66717e}
.tvw-vs-u{background:#eef4fd;color:var(--navy);font-weight:700;box-shadow:inset 0 0 0 1px #cfe0f7}
.tvw-vs-t span,.tvw-vs-u span{flex:none;width:22px;height:22px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:800;margin-top:1px}
.tvw-vs-t span{background:#dfe4ea;color:#8a94a1}.tvw-vs-u span{background:var(--blue);color:#fff}
@media (max-width:720px){.tvw-vs-hd{display:none}.tvw-vs-row{grid-template-columns:1fr;gap:6px;padding:14px;border:1px solid var(--line);border-radius:18px;background:#fff}
.tvw-vs-k{font-size:16.5px;margin-bottom:2px!important}.tvw-vs-t{padding:4px 2px;background:none;font-size:14.5px}.tvw-vs-u{padding:10px 12px;font-size:15px}}

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
.tvw-then{margin:6px 0 0!important;font-size:15px!important;color:var(--mut)!important}.tvw-then b{color:var(--blue)}.tvw-feat .tvw-then{color:#cfe0f7!important}.tvw-feat .tvw-then b{color:var(--gold)}
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
