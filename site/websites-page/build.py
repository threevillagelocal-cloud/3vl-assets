"""Websites landing page. Owner 10/22/2026: "make the websites page look like the services page except without the social media
promotion. copy exact" + "keep the 2 packages for the websites". So this page is the /services page (same page.html sections,
page.css, page.js, hero photo, form) with the social-media service parts removed and the bundles replaced by the two website
packages (AI-Ready, AI-Powered), member vs regular pricing. "Get started" -> /website-start brief form (owner 10/21: no payment
on the site). Old standalone design kept in build_v1_2026-10-22.py.
    python site/websites-page/build.py          -> widget "3VL Page Websites Preview" + hidden /preview-websites
    python site/websites-page/build.py --live   -> widget "3VL Page Websites" + /websites (indexable)"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SV = os.path.join(HERE, "..", "services-page")
sys.path.insert(0, SV)
import deploy as D

LINKS = json.load(open("C:/Users/Matt/Documents/3vl-private/website-offer/stripe.json"))
PR = {k: (v["setup"], v["monthly"]) for k, v in LINKS.items()}

D.NAME = "3VL Page Websites" if D.LIVE else "3VL Page Websites Preview"   # preview has its own widget so it never changes the live page
D.SLUG = "websites" if D.LIVE else "preview-websites"
D.TITLE = "AI-Ready Websites for Long Island Businesses | Three Village Local"
D.DESC = ("Websites built for customers and for AI: designed, built and hosted by one local team, set up for Google and AI search, "
          "then launched to the whole town on Three Village Local. Member pricing for Three Village Local businesses.")
D.FB_TITLE = "AI-Driven Websites: Design, Build, Host"
D.FB_IMAGE = "/share/ai-websites-v1.jpg"   # BD mangles external og:image URLs; redirect 2253 -> 3vl-share/site/websites/share-ai-websites-v1.jpg

SHARE = "https://threevillagelocal-cloud.github.io/3vl-share/site/websites/"
D.HEAD = ""   # tried a hero preload 10/22: no LCP gain (BD template is the bottleneck)
START = "/website-start?plan="


def sec(src, cls):
    i = src.index('<section class="' + cls)
    return i, src.index('</section>', i) + len('</section>')


def cut(src, cls):
    i, j = sec(src, cls)
    return src[:i] + src[j:].lstrip("\n")


def swap(src, cls, new):
    i, j = sec(src, cls)
    return src[:i] + new + src[j:]


def rep(src, a, b):
    assert a in src, a[:80]
    return src.replace(a, b, 1)


def card(key, name, one, items, pop=False):
    m, r = PR["web-%s-member" % key], PR["web-%s-regular" % key]
    lis = "".join("<li%s>%s</li>" % (' class="tvs-star"' if "Three Village Local" in i else "", i) for i in items)
    return '''    <article class="tvs-card%s tvs-up" data-b="web%s">
%s      <p class="tvs-cname">%s</p>
      <p class="tvs-cfor">%s</p>
      <p class="tvs-was"></p>
      <p class="tvs-price"><sup>$</sup><b>%s</b></p>
      <p class="tvs-mo">+ <b>$%s</b>/mo</p>
      <p class="tvs-save"></p>
      <ul>
        %s
      </ul>
      <a class="tvs-btn %s tvs-wide tvw-go" data-m="%s" data-r="%s" href="%s">Get started &rarr;</a>
    </article>
''' % (" tvs-pop" if pop else "", key, '      <p class="tvs-badge">Most popular</p>\n' if pop else "", name, one, "{:,}".format(m[0]), m[1],
       "\n        ".join(lis.replace("</li><li", "</li>\n<li").split("\n")),
       "tvs-blue" if pop else "tvs-line", START + "web-%s-member" % key, START + "web-%s-regular" % key, START + "web-%s-member" % key)


READY = card("ready", "AI-Ready", "AI can find you. Built so Google and AI assistants understand and recommend your business.", [
    "Custom design, up to 5 pages, written for you",
    "Code AI can actually read, not hidden behind scripts",
    "Your business clearly labeled for Google and AI: services, hours, area, reviews",
    "A page for every service, plus FAQs the way people ask",
    "Fast, mobile-first and secure, with a lead form to your inbox",
    "Hosting, domain setup and updates included",
    "3VL Launch Spotlight + 3 months Featured on Three Village Local"])
POWERED = card("powered", "AI-Powered", "AI works for you. Everything in AI-Ready, plus tools that bring in customers on their own.", [
    "Everything in AI-Ready",
    "Your own AI assistant answering customers 24/7 and sending you the lead",
    "Fresh content, automatically: 2 blog posts or industry updates a month",
    "Your best reviews showcased on your site",
    "Online booking or quote requests",
    "Monthly feature on Three Village Local"], pop=True)

SITES = [("coltrain", "Coltrain Mortgage"), ("sbna", "SBNA"), ("lga", "LGA Marketing"), ("jm", "JM Management Solutions"), ("3vl", "Three Village Local")]
row = "".join('<img src="%ssite-%s.webp" alt="%s website, built by our team" loading="lazy" decoding="async"%s>' % (SHARE, k, n, "") for k, n in SITES)
row2 = "".join('<img src="%ssite-%s.webp" alt="" aria-hidden="true" loading="lazy" decoding="async">' % (SHARE, k) for k, n in SITES)

WORK = '''<section class="tvs-sec tvs-work" id="tvs-work">
  <div class="tvs-wtop">
    <div class="tvs-wtxt tvs-up">
      <p class="tvs-eyebrow">Real websites for real local businesses</p>
      <h2>See what you get.</h2>
      <p>Every site below was designed, built and hosted by our team, including Three Village Local itself.</p>
      <ul class="tvs-wlist">
        <li><b>Custom design</b>Built around your business, not a template</li>
        <li><b>Fast on every phone</b>Most of your visitors are on their phones</li>
        <li><b>Set up for Google and AI search</b>So ChatGPT, Gemini and Google can recommend you</li>
        <li><b>Hosted and cared for</b>Security, updates and edits handled for you</li>
      </ul>
    </div>
    <figure class="tvs-vphone tvw-phfig tvs-up">
      <div class="tvw-phone"><div class="tvw-phone-screen"><div class="tvw-phone-bar"><span>9:41</span><span class="tvw-phone-sig">&#9679;&#9679;&#9679; &#9646;</span></div><div class="tvw-phone-view"><div class="tvw-ph-page"><img src="''' + SHARE + '''phone-home.webp" alt="Three Village Local homepage on a phone" width="780" height="5400" loading="lazy" decoding="async"><div class="tvw-ph-row"><img src="''' + SHARE + '''phone-strip.webp" alt="" aria-hidden="true" width="3364" height="1062" loading="lazy" decoding="async"></div></div></div></div><span class="tvw-phone-island"></span></div>
      <figcaption>Three Village Local on a phone, <b>built by our team</b></figcaption>
    </figure>
  </div>
  <div class="tvs-mq tvs-mq1 tvw-sites"><div class="tvs-mqt">''' + row + row2 + '''</div></div>
</section>'''

BUNDLES = '''<section class="tvs-sec tvs-bundles" id="tvs-bundles">
  <div class="tvs-head tvs-up">
    <p class="tvs-eyebrow">Packages</p>
    <h2>Pick a package. We handle the rest.</h2>
    <p><b>AI-Ready</b> means AI can find you. <b>AI-Powered</b> means AI works for you. Both are designed, built and hosted by us. Prices shown are <b>Three Village Local member prices</b>.</p>
  </div>
  <div class="tvs-tiers tvs-up" role="tablist" aria-label="Choose your membership to see your price">
    <button type="button" role="tab" data-t="all">Not a member</button>
    <button type="button" role="tab" data-t="vip" class="on">3VL member<em>Member price</em></button>
  </div>
  <div class="tvs-cards tvw-two">
''' + READY + POWERED + '''  </div>
  <p class="tvs-fine tvs-up">Your start-up fee includes your first month. After that, the monthly plan covers hosting, security, updates and support, month to month. Your domain is registered in your name.</p>
</section>'''

AI_SEC = '''<section class="tvs-sec tvw-ai" id="tvw-ai">
  <div class="tvs-head tvs-up">
    <p class="tvs-eyebrow">Built for the AI era</p>
    <h2>Websites built to be found, understood and recommended by AI.</h2>
    <p>More people now ask ChatGPT, Gemini and Google's AI "who's good near me?" AI tools recommend the businesses they can actually read. Many template site builders load their words with scripts, and AI crawlers generally don't run those scripts, so to them the page can look almost empty. We build sites AI can read from the first line.</p>
  </div>
  <div class="tvw-ai-cmp tvs-up">
    <div class="tvw-ai-card tvw-ai-bad">
      <p class="tvw-ai-lab"><span>&#10005;</span>A typical template site</p>
      <div class="tvw-ai-win"><div class="tvw-ai-bar"><i></i><i></i><i></i><em>What an AI crawler sees</em></div>
        <p class="tvw-ai-code">&lt;body&gt;<br>&nbsp;&nbsp;&lt;div id="app"&gt;&lt;/div&gt;<br>&nbsp;&nbsp;&lt;script src="builder-bundle.js"&gt;&lt;/script&gt;<br>&lt;/body&gt;</p>
        <p class="tvw-ai-empty">No services. No hours. No town. Nothing to recommend.</p></div>
    </div>
    <div class="tvw-ai-card tvw-ai-good">
      <p class="tvw-ai-lab"><span>&#10003;</span>A site built by Three Village Local</p>
      <div class="tvw-ai-win"><div class="tvw-ai-bar"><i></i><i></i><i></i><em>What an AI crawler sees</em></div>
        <ul class="tvw-ai-read">
          <li><b>Business</b>Your Business, Setauket, NY</li>
          <li><b>Services</b>Lawn care, cleanups, patios</li>
          <li><b>Hours</b>Mon to Sat, 8 AM to 6 PM</li>
          <li><b>Serves</b>Stony Brook, Setauket, Port Jefferson</li>
          <li><b>Reviews</b>4.9 stars from 120 neighbors</li>
          <li><b>Contact</b>Call, text or request a quote</li>
        </ul></div>
    </div>
  </div>
  <div class="tvw-tech tvs-up">
    <p class="tvw-tech-h">The tech under the hood</p>
    <div class="tvw-tech-row">
      <span><b>Server-rendered pages</b>Every word is in the page itself, no scripts needed to read it</span>
      <span><b>Structured data</b>Schema.org labels for your services, hours, area and reviews</span>
      <span><b>AI crawler access</b>Open to ChatGPT, Perplexity, Claude and Google's AI crawlers</span>
      <span><b>llms.txt + sitemaps</b>A plain guide that tells AI tools what your business does</span>
      <span><b>Instant indexing</b>New pages pinged to search engines the day they go live</span>
      <span><b>Fast on every phone</b>Hosted on a global edge network, built to pass Core Web Vitals</span>
    </div>
  </div>
  <div class="tvw-logos tvs-up"><p>Built to be found on</p><div class="tvw-logo-row"><span class="tvw-logo"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#4285F4" d="M12.48 10.92v3.28h7.84c-.24 1.84-.853 3.187-1.787 4.133-1.147 1.147-2.933 2.4-6.053 2.4-4.827 0-8.6-3.893-8.6-8.72s3.773-8.72 8.6-8.72c2.6 0 4.507 1.027 5.907 2.347l2.307-2.307C18.747 1.44 16.133 0 12.48 0 5.867 0 .307 5.387.307 12s5.56 12 12.173 12c3.573 0 6.267-1.173 8.373-3.36 2.16-2.16 2.84-5.213 2.84-7.667 0-.76-.053-1.467-.173-2.053H12.48z"/></svg>Google</span><span class="tvw-logo"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#34A853" d="M19.527 4.799c1.212 2.608.937 5.678-.405 8.173-1.101 2.047-2.744 3.74-4.098 5.614-.619.858-1.244 1.75-1.669 2.727-.141.325-.263.658-.383.992-.121.333-.224.673-.34 1.008-.109.314-.236.684-.627.687h-.007c-.466-.001-.579-.53-.695-.887-.284-.874-.581-1.713-1.019-2.525-.51-.944-1.145-1.817-1.79-2.671L19.527 4.799zM8.545 7.705l-3.959 4.707c.724 1.54 1.821 2.863 2.871 4.18.247.31.494.622.737.936l4.984-5.925-.029.01c-1.741.601-3.691-.291-4.392-1.987a3.377 3.377 0 0 1-.209-.716c-.063-.437-.077-.761-.004-1.198l.001-.007zM5.492 3.149l-.003.004c-1.947 2.466-2.281 5.88-1.117 8.77l4.785-5.689-.058-.05-3.607-3.035zM14.661.436l-3.838 4.563a.295.295 0 0 1 .027-.01c1.6-.551 3.403.15 4.22 1.626.176.319.323.683.377 1.045.068.446.085.773.012 1.22l-.003.016 3.836-4.561A8.382 8.382 0 0 0 14.67.439l-.009-.003zM9.466 5.868L14.162.285l-.047-.012A8.31 8.31 0 0 0 11.986 0a8.439 8.439 0 0 0-6.169 2.766l-.016.018 3.665 3.084z"/></svg>Google Maps</span><span class="tvw-logo"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#10A37F" d="M12 1.5l2.3 6.2 6.2 2.3-6.2 2.3L12 18.5l-2.3-6.2L3.5 10l6.2-2.3zM19 15l1 2.6 2.5 1-2.5.9-1 2.6-.9-2.6-2.6-.9 2.6-1z"/></svg>ChatGPT</span><span class="tvw-logo"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#8E75B2" d="M11.04 19.32Q12 21.51 12 24q0-2.49.93-4.68.96-2.19 2.58-3.81t3.81-2.55Q21.51 12 24 12q-2.49 0-4.68-.93a12.3 12.3 0 0 1-3.81-2.58 12.3 12.3 0 0 1-2.58-3.81Q12 2.49 12 0q0 2.49-.96 4.68-.93 2.19-2.55 3.81a12.3 12.3 0 0 1-3.81 2.58Q2.49 12 0 12q2.49 0 4.68.96 2.19.93 3.81 2.55t2.55 3.81"/></svg>Gemini</span><span class="tvw-logo"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#1FB8CD" d="M22.3977 7.0896h-2.3106V.0676l-7.5094 6.3542V.1577h-1.1554v6.1966L4.4904 0v7.0896H1.6023v10.3976h2.8882V24l6.932-6.3591v6.2005h1.1554v-6.0469l6.9318 6.1807v-6.4879h2.8882V7.0896zm-3.4657-4.531v4.531h-5.355l5.355-4.531zm-13.2862.0676 4.8691 4.4634H5.6458V2.6262zM2.7576 16.332V8.245h7.8476l-6.1149 6.1147v1.9723H2.7576zm2.8882 5.0404v-3.8852h.0001v-2.6488l5.7763-5.7764v7.0111l-5.7764 5.2993zm12.7086.0248-5.7766-5.1509V9.0618l5.7766 5.7766v6.5588zm2.8882-5.0652h-1.733v-1.9723L13.3948 8.245h7.8478v8.087z"/></svg>Perplexity</span><span class="tvw-logo"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#D97757" d="m4.7144 15.9555 4.7174-2.6471.079-.2307-.079-.1275h-.2307l-.7893-.0486-2.6956-.0729-2.3375-.0971-2.2646-.1214-.5707-.1215-.5343-.7042.0546-.3522.4797-.3218.686.0608 1.5179.1032 2.2767.1578 1.6514.0972 2.4468.255h.3886l.0546-.1579-.1336-.0971-.1032-.0972L6.973 9.8356l-2.55-1.6879-1.3356-.9714-.7225-.4918-.3643-.4614-.1578-1.0078.6557-.7225.8803.0607.2246.0607.8925.686 1.9064 1.4754 2.4893 1.8336.3643.3035.1457-.1032.0182-.0728-.164-.2733-1.3539-2.4467-1.445-2.4893-.6435-1.032-.17-.6194c-.0607-.255-.1032-.4674-.1032-.7285L6.287.1335 6.6997 0l.9957.1336.419.3642.6192 1.4147 1.0018 2.2282 1.5543 3.0296.4553.8985.2429.8318.091.255h.1579v-.1457l.1275-1.706.2368-2.0947.2307-2.6957.0789-.7589.3764-.9107.7468-.4918.5828.2793.4797.686-.0668.4433-.2853 1.8517-.5586 2.9021-.3643 1.9429h.2125l.2429-.2429.9835-1.3053 1.6514-2.0643.7286-.8196.85-.9046.5464-.4311h1.0321l.759 1.1293-.34 1.1657-1.0625 1.3478-.8804 1.1414-1.2628 1.7-.7893 1.36.0729.1093.1882-.0183 2.8535-.607 1.5421-.2794 1.8396-.3157.8318.3886.091.3946-.3278.8075-1.967.4857-2.3072.4614-3.4364.8136-.0425.0304.0486.0607 1.5482.1457.6618.0364h1.621l3.0175.2247.7892.522.4736.6376-.079.4857-1.2142.6193-1.6393-.3886-3.825-.9107-1.3113-.3279h-.1822v.1093l1.0929 1.0686 2.0035 1.8092 2.5075 2.3314.1275.5768-.3218.4554-.34-.0486-2.2039-1.6575-.85-.7468-1.9246-1.621h-.1275v.17l.4432.6496 2.3436 3.5214.1214 1.0807-.17.3521-.6071.2125-.6679-.1214-1.3721-1.9246L14.38 17.959l-1.1414-1.9428-.1397.079-.674 7.2552-.3156.3703-.7286.2793-.6071-.4614-.3218-.7468.3218-1.4753.3886-1.9246.3157-1.53.2853-1.9004.17-.6314-.0121-.0425-.1397.0182-1.4328 1.9672-2.1796 2.9446-1.7243 1.8456-.4128.164-.7164-.3704.0667-.6618.4008-.5889 2.386-3.0357 1.4389-1.882.929-1.0868-.0062-.1579h-.0546l-6.3385 4.1164-1.1293.1457-.4857-.4554.0608-.7467.2307-.2429 1.9064-1.3114Z"/></svg>Claude</span><span class="tvw-logo"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#111111" d="M12.152 6.896c-.948 0-2.415-1.078-3.96-1.04-2.04.027-3.91 1.183-4.961 3.014-2.117 3.675-.546 9.103 1.519 12.09 1.013 1.454 2.208 3.09 3.792 3.039 1.52-.065 2.09-.987 3.935-.987 1.831 0 2.35.987 3.96.948 1.637-.026 2.676-1.48 3.676-2.948 1.156-1.688 1.636-3.325 1.662-3.415-.039-.013-3.182-1.221-3.22-4.857-.026-3.04 2.48-4.494 2.597-4.559-1.429-2.09-3.623-2.324-4.39-2.376-2-.156-3.675 1.09-4.61 1.09zM15.53 3.83c.843-1.012 1.4-2.427 1.245-3.83-1.207.052-2.662.805-3.532 1.818-.78.896-1.454 2.338-1.273 3.714 1.338.104 2.715-.688 3.559-1.701"/></svg>Siri &amp; Apple Maps</span></div></div>
</section>'''

src = open(os.path.join(SV, "page.html"), encoding="utf-8").read()
h = src
# hero: websites only, no social/video/drone/marketing services
h = rep(h, "Websites + Google + AI search + Social + Video + Drone + Marketing", "Websites + Google + AI search + Hosting")
h = rep(h, "Your website, Google, AI search, social media, video and marketing, built by one local team to work as one. Then we launch it in front of the whole town on Three Village Local.",
        "Modern websites optimized to be found and recommended by AI assistants like ChatGPT and Google, designed, built and hosted by one local team. Then we launch them to the whole town on Three Village Local.")
h = rep(h, 'href="#tvs-bundles">See the bundles</a>', 'href="#tvs-bundles">See the packages</a>')
h = re.sub(r'\n    <a class="tvs-newlink"[^\n]*</a>', "", h)
h = cut(h, "tvs-sec tvs-social")                  # "Your content, seen all over town" (social media service)
h = swap(h, "tvs-sec tvs-work", WORK)              # promo video + social posts -> real websites + phone
h = swap(h, "tvs-sec tvs-bundles", BUNDLES)        # social bundles -> the 2 website packages
h = cut(h, "tvs-founding")                        # owner 10/22: remove the founding clients box
h = cut(h, "tvs-stats")                           # owner 10/22: remove the 4-number stats strip
i, _ = sec(h, "tvs-sec tvs-show")
h = h[:i] + AI_SEC + chr(10) * 2 + h[i:]                  # owner 10/22: AI-findable message + template-site scripts + our tech
h = re.sub(r'<a class="tvs-newbiz[^\n]*</a>\n\n', "", h)
h = rep(h, "<p>We pick the right bundle together and map out your first month.</p>", "<p>We pick the right package together and map out your site.</p>")
h = rep(h, "<p>No long contracts. Bundles are a one-time build, and monthly plans are month to month.</p>",
        "<p>No long contracts. Your site is a one-time build, and the monthly plan is month to month.</p>")
h = rep(h, "<p>Half to start, the rest at launch once you love it.</p>", "<p>After your free consultation we send one simple invoice. Your start-up fee includes your first month.</p>")
h = rep(h, "<p>No. Anyone can book. Members save on every bundle, and VIP members save the most.</p>", "<p>No. Anyone can book. Three Village Local members get member pricing on both packages.</p>")
h = rep(h, "mailto:hello@threevillagelocal.com?subject=Services", "mailto:hello@threevillagelocal.com?subject=Websites")
for m in re.finditer(r".{60}[Bb]undle.{40}", h): print("LEFT:", m.group(0))
HTML = h

PRICES = ("var P={webready:{all:[%d,%d],free:[%d,%d],featured:[%d,%d],vip:[%d,%d]},webpowered:{all:[%d,%d],free:[%d,%d],featured:[%d,%d],vip:[%d,%d]},"
                    % (PR["web-ready-regular"] + PR["web-ready-member"] * 3 + PR["web-powered-regular"] + PR["web-powered-member"] * 3))
GOJS = '''<script>(function(){function upd(){var b=document.querySelector('#tvs .tvs-tiers button.on'),m=!b||b.getAttribute('data-t')!=='all';
[].forEach.call(document.querySelectorAll('#tvs .tvw-go'),function(a){a.href=m?a.getAttribute('data-m'):a.getAttribute('data-r')})}
document.addEventListener('click',function(e){if(e.target.closest&&e.target.closest('#tvs .tvs-tiers button'))setTimeout(upd,0)});upd()})();</script>'''

CSS = '''
.tvw-ai-cmp{display:grid;grid-template-columns:1fr 1fr;gap:22px;max-width:980px;margin:6px auto 0}
.tvw-ai-lab{display:flex;align-items:center;gap:9px;font-weight:800;font-size:16px;color:var(--navy);margin:0 0 10px!important}
.tvw-ai-lab span{display:inline-flex;width:24px;height:24px;border-radius:50%;align-items:center;justify-content:center;color:#fff;font-size:13px}
.tvw-ai-bad .tvw-ai-lab span{background:#d64545}.tvw-ai-good .tvw-ai-lab span{background:#16a34a}
.tvw-ai-win{border-radius:16px;overflow:hidden;border:1px solid #dfe6f0;background:#fff;box-shadow:0 18px 40px -22px rgba(13,35,70,.35);min-height:270px}
.tvw-ai-bar{display:flex;align-items:center;gap:6px;padding:10px 14px;background:#0f1b2e;color:#9fb3d6;font-size:12px}
.tvw-ai-bar i{width:9px;height:9px;border-radius:50%;background:#3a4a66}.tvw-ai-bar em{font-style:normal;margin-left:8px;letter-spacing:.04em}
.tvw-ai-code{margin:0!important;padding:18px 18px 10px;background:#0b1424;color:#7fd4ff;font:13px/1.6 Consolas,Menlo,monospace;white-space:pre;overflow:hidden}
.tvw-ai-empty{margin:0!important;padding:14px 18px 18px;background:#0b1424;color:#ff8a8a;font-weight:700;font-size:14px}
.tvw-ai-bad .tvw-ai-win{background:#0b1424}
.tvw-ai-read{list-style:none;margin:0;padding:12px 18px 16px}
.tvw-ai-read li{display:grid;grid-template-columns:90px 1fr;gap:10px;padding:8px 0;border-bottom:1px dashed #e3e9f2;font-size:14.5px;color:#1a2233}
.tvw-ai-read li:last-child{border-bottom:0}.tvw-ai-read b{color:#16a34a;font-size:12px;letter-spacing:.06em;text-transform:uppercase;padding-top:2px}
.tvw-tech{max-width:980px;margin:34px auto 0}
.tvw-tech-h{text-align:center;font-size:13px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--mut);margin:0 0 14px!important}
.tvw-tech-row{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.tvw-tech-row span{display:block;padding:14px 16px;border-radius:14px;background:linear-gradient(160deg,#0f1b2e,#13294b);color:#c9d6ee;font-size:13.5px;line-height:1.45}
.tvw-tech-row b{display:block;color:#fff;font-size:15px;margin-bottom:3px}
.tvw-logos{text-align:center;margin-top:30px}
.tvw-logos>p{margin:0 0 12px!important;font-size:13px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--mut)}
.tvw-logo-row{display:flex;flex-wrap:wrap;justify-content:center;gap:10px 12px}
.tvw-logo{display:inline-flex;align-items:center;gap:9px;padding:9px 15px;border:1px solid #dfe6f0;border-radius:999px;background:#fff;font-weight:700;font-size:14.5px;color:#1a2233}
.tvw-logo svg{width:19px;height:19px;flex:none}
@media (max-width:760px){.tvw-ai-cmp{grid-template-columns:1fr}.tvw-tech-row{grid-template-columns:1fr}.tvw-ai-code{font-size:11.5px}}

.tvw-two{grid-template-columns:repeat(2,minmax(0,1fr))!important;max-width:820px;margin-left:auto;margin-right:auto}
.tvw-phfig{display:flex;flex-direction:column;align-items:center}
.tvs-wtop:has(.tvw-phfig){grid-template-columns:1fr 290px;max-width:960px}
.tvw-phone{position:relative;width:270px;padding:10px;border-radius:48px;background:linear-gradient(145deg,#2a3242,#0a0d13);box-shadow:0 36px 64px -24px rgba(9,30,66,.5),0 0 0 2px #3a4456 inset,0 0 0 1px #11151c}
.tvw-phone-screen{position:relative;aspect-ratio:390/844;overflow:hidden;border-radius:38px;background:#13294b;display:flex;flex-direction:column}
.tvw-phone-bar{flex:none;height:40px;display:flex;align-items:center;justify-content:space-between;padding:6px 26px 0;color:#fff;font:600 12px/1 -apple-system,Segoe UI,sans-serif}
.tvw-phone-sig{font-size:8px;letter-spacing:1px}
.tvw-phone-view{position:relative;flex:1;overflow:hidden;background:#fff}
.tvw-ph-page{position:relative;animation:tvwPh 40s ease-in-out infinite;will-change:transform}
.tvw-ph-page>img{display:block!important;width:100%!important;max-width:none!important;height:auto!important;max-height:none!important;aspect-ratio:780/5400}
.tvw-ph-row{position:absolute;left:3.846%;top:51.05%;width:92.31%;height:19.67%;overflow:hidden;background:#f2f4f7}
.tvw-ph-row img{display:block!important;width:467.2%!important;max-width:none!important;height:100%!important;max-height:none!important;animation:tvwRow 40s ease-in-out infinite;will-change:transform}
.tvw-phone-island{position:absolute;top:19px;left:50%;width:80px;height:23px;margin-left:-40px;border-radius:20px;background:#05070b}
@keyframes tvwPh{0%,5%{transform:translateY(0)}20%,62%{transform:translateY(-50.2%)}84%,88%{transform:translateY(-70%)}98%,100%{transform:translateY(0)}}
@keyframes tvwRow{0%,24%{transform:translateX(0)}28%,32%{transform:translateX(-16.05%)}36%,40%{transform:translateX(-32.1%)}44%,48%{transform:translateX(-48.15%)}52%,56%{transform:translateX(-64.2%)}59%,60%{transform:translateX(-78.6%)}64%,100%{transform:translateX(0)}}
.tvw-sites .tvs-mqt img{border-radius:12px;box-shadow:0 14px 30px -14px rgba(9,30,66,.35);border:1px solid #dfe6f0;background:#fff}
@media (prefers-reduced-motion:reduce){.tvw-ph-page,.tvw-ph-row img{animation:none}}
@media (max-width:760px){.tvw-two{grid-template-columns:1fr!important}.tvs-wtop:has(.tvw-phfig){grid-template-columns:1fr}.tvw-phone{width:240px}}
'''

_rd = D.rd


def rd(f):
    if f == "page.html":
        assert "\\" not in HTML
        return HTML
    s = _rd(f)
    if f == "page.css":
        return s + CSS
    if f == "page.js":
        s = rep(s, "var P={", PRICES)
        return s + GOJS
    return s


D.rd = rd
if __name__ == "__main__":
    D.main()
