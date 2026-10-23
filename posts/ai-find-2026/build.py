"""Can AI Find Your Business? (owner request 10/23/2026). Blog article that sells websites made for AI + AI chatbots and collects
free AI visibility report requests (BD form ai_report, form 345, alerts to Gmail). Angle: how small local businesses can even
the AI playing field.
v2 (owner 10/23): shorter, clear that WE BUILD websites made for AI, and NO local storefront photos (they read as our clients).
Only our real client sites appear as "sites we built". Chat demos use FICTIONAL businesses (Harbor Light Bakery etc.).
    python build.py [--local]   -> post.html   (CSS/JS: bash publish_assets.sh; site: python push.py)"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LOCAL = "--local" in sys.argv
# jsDelivr answered "Package size exceeded" (10/23), so the CSS/JS are served from 3vl-share GitHub Pages (publish_assets.sh copies them)
ASSET = "" if LOCAL else "https://threevillagelocal-cloud.github.io/3vl-share/ai-find/"
WEB = "https://threevillagelocal-cloud.github.io/3vl-share/site/websites/"
REPORT_PAGE = "/free-ai-report"

# AI assistant logos: same SVG row the /websites page uses
src = open(os.path.join(HERE, "..", "..", "site", "websites-page", "build.py"), encoding="utf-8").read()
LOGOS = re.search(r'<div class="tvw-logo-row">(.*?)</div></section>', src, re.S).group(1).replace('class="tvw-logo"', 'class="aif-logo"')
LOGO = dict((m.group(2), m.group(1)) for m in re.finditer(r'<span class="aif-logo">(<svg.*?</svg>)([^<]+)</span>', LOGOS))


def chip(name, cls):
    return '<span class="aif-orb %s">%s%s</span>' % (cls, LOGO.get(name, ""), name)


H = []
w = H.append
w('<link rel="stylesheet" href="%saif.css">' % ASSET)
w('<div class="aif" id="aif-top"><div class="aif-prog"><i></i></div>')

# ---------------- HERO ----------------
w('<header class="aif-hero">'
  '<div class="aif-hl">'
  '<p class="aif-kick"><span class="aif-dot"></span>Websites made for AI, by Three Village Local</p>'
  '<h2 class="aif-h1">Can AI find <span>your business?</span></h2>'
  '<p class="aif-sub">How small local businesses can even the AI playing field, before the competition gets there first.</p>'
  '<p class="aif-dek">Customers now ask ChatGPT, Google and Siri for a recommendation and get back a few names. If AI can&rsquo;t read your website, it can&rsquo;t recommend you. <b>We build websites made for AI</b>, so it can find you, understand you and send customers your way.</p>'
  '<div class="aif-btns"><a class="aif-btn aif-btn-gold" href="#aif-report">Get my free AI report</a><a class="aif-btn aif-btn-line" href="/websites">See our AI-ready websites</a></div>'
  '</div>'
  '<div class="aif-hr" aria-hidden="true"><div class="aif-glow"></div>'
  + chip("ChatGPT", "o1") + chip("Gemini", "o2") + chip("Siri", "o3") + chip("Perplexity", "o4") +
  '<div class="aif-phone"><div class="aif-pbar"><b>AI Assistant</b><span>online</span></div>'
  '<div class="aif-chat" data-chat="hero">'
  '<div class="aif-msg aif-me">What&rsquo;s the best bakery near Stony Brook?</div>'
  '<div class="aif-typing"><i></i><i></i><i></i></div>'
  '<div class="aif-msg aif-ai">Here are 3 local favorites:<ol><li><b>Harbor Light Bakery</b> &#9733; 4.9<br><small>Custom cakes, open early</small></li><li><b>Old Field Bread Co.</b> &#9733; 4.8<br><small>Sourdough, gluten-free options</small></li><li><b>Main Street Sweets</b> &#9733; 4.7<br><small>Cookies and cupcakes</small></li></ol></div>'
  '<div class="aif-yours">Is <b>your</b> business on this list?</div>'
  '</div></div></div></header>')

# ---------------- 1. what changed + level field ----------------
w('<section class="aif-sec rv" id="aif-shift"><p class="aif-eye">01 &middot; What changed</p>'
  '<h3>AI picks a few names. Small businesses can win.</h3>'
  '<div class="aif-split"><div>'
  '<p class="aif-lead">Customers ask AI for the best plumber nearby or the dentist open on Saturday, and get a short list of names instead of a page of links.</p>'
  '<p>AI doesn&rsquo;t care how big your ad budget is. It recommends the businesses it <b>understands</b> best: what you do, where you are, when you&rsquo;re open and what customers say. A local business with a website built for AI can beat a national chain.</p>'
  '<div class="aif-logos">%s</div>' % LOGOS +
  '</div>'
  '<div class="aif-vs" aria-hidden="true"><p class="aif-vst">Who does AI understand better?</p>'
  '<div class="aif-vrow"><div class="aif-vlab"><span>&#127970;</span><b>Big chain</b><small>Huge ad budget, generic pages</small></div><div class="aif-vbar"><i style="--v:42%"></i></div></div>'
  '<div class="aif-vrow aif-vwin"><div class="aif-vlab"><span>&#127968;</span><b>Your local business</b><small>Real reviews, local know-how, a website made for AI</small></div><div class="aif-vbar"><i style="--v:94%"></i></div></div>'
  '<p class="aif-small">Illustration</p></div>'
  '</div>'
  '<div class="aif-fomo rv"><b>&#9888;&#65039; The window won&rsquo;t stay open.</b> The businesses that get AI-ready first become the names AI keeps repeating. Every month you wait, a competitor gets a little more familiar to AI.</div>'
  '</section>')

# ---------------- 2. what AI sees ----------------
w('<section class="aif-sec aif-tint rv" id="aif-see"><p class="aif-eye">02 &middot; Look behind the curtain</p>'
  '<h3>What your customer sees vs. what AI reads.</h3>'
  '<p class="aif-lead">Two websites can look the same to a person and completely different to AI. Flip the switch.</p>'
  '<div class="aif-tabs" role="tablist"><button type="button" role="tab" class="on" data-see="tpl">Template website</button><button type="button" role="tab" data-see="ai">Website made for AI</button></div>'
  '<div class="aif-see" data-mode="tpl">'
  '<div class="aif-pane aif-human"><p class="aif-ptag">&#128064; What a customer sees</p>'
  '<div class="aif-mock"><div class="aif-mbar"><i></i><i></i><i></i><span>harborlightbakery.com</span></div>'
  '<div class="aif-mhero"><b>Harbor Light Bakery</b><span>Fresh every morning in Stony Brook</span><em>Order a cake</em></div>'
  '<div class="aif-mrow"><span>Custom cakes</span><span>Breads</span><span>Open 7 AM</span></div></div></div>'
  '<div class="aif-pane aif-robot"><p class="aif-ptag">&#129302; What an AI crawler reads</p>'
  '<pre class="aif-code aif-code-tpl">&lt;div id="app"&gt;&lt;/div&gt;\n&lt;script src="builder-runtime.min.js"&gt;&lt;/script&gt;\n&lt;script src="theme-bundle.8f3a.js"&gt;&lt;/script&gt;\n&lt;script src="widgets-loader.js"&gt;&lt;/script&gt;\n&lt;!-- 1.9 MB of scripts --&gt;</pre>'
  '<pre class="aif-code aif-code-ai">Harbor Light Bakery\nBakery in Stony Brook, NY\nCustom cakes &middot; Breads &middot; Gluten-free\nOpen Tue-Sun, 7 AM - 3 PM\n&#9733; 4.9 from 212 reviews\n{"@type": "Bakery", "areaServed": "Stony Brook"}</pre>'
  '<div class="aif-verdict aif-v-tpl"><b>AI:</b> &ldquo;I couldn&rsquo;t find a business name, services or hours on this page.&rdquo;</div>'
  '<div class="aif-verdict aif-v-ai"><b>AI:</b> &ldquo;Harbor Light Bakery is a top-rated bakery in Stony Brook, known for custom cakes. Open Tuesday to Sunday from 7 AM.&rdquo;</div>'
  '</div></div>'
  '<p class="aif-small">Illustration with a sample business.</p>'
  '</section>')

# ---------------- 3. why templates ----------------
WHY = [("&#128220;", "Words hidden in scripts", "Many drag-and-drop builders assemble the page with JavaScript in the visitor&rsquo;s browser. Many AI crawlers only read the raw code and don&rsquo;t run those scripts, so they miss your services and hours."),
       ("&#128034;", "Heavy, slow code", "Templates ship code for every feature they offer, used or not. Slow pages lose customers on phones."),
       ("&#127991;&#65039;", "No labels AI can trust", "Structured data tells AI this is a business, this is the address, these are the hours. Most templates leave it out."),
       ("&#128203;", "Cookie-cutter pages", "Thousands of sites share the same layout and filler text. AI needs specific answers about you, in your town.")]
w('<section class="aif-sec rv" id="aif-why"><p class="aif-eye">03 &middot; The hidden problem</p>'
  '<h3>Why template websites trip up AI.</h3>'
  '<p class="aif-lead">It isn&rsquo;t your fault. Website builders were made to look good to people, long before AI assistants existed.</p>'
  '<div class="aif-why">%s</div>' % "".join('<div class="aif-wcard rv"><span>%s</span><b>%s</b><p>%s</p></div>' % x for x in WHY) +
  '<div class="aif-try rv"><b>Try this:</b> ask ChatGPT, &ldquo;What are the best <i>[your type of business]</i> near <i>[your town]</i>?&rdquo; Are you on the list?</div>'
  '</section>')

# ---------------- 4. we build websites made for AI ----------------
FEAT = [("&#9889;", "Clean, fast code", "Built from scratch, readable from the very first line."),
        ("&#127991;&#65039;", "Structured data", "The labels AI and Google use to understand exactly who you are."),
        ("&#10067;", "Answer pages", "Pages that answer the questions customers ask AI about your business."),
        ("&#11088;", "Reviews + Google profile", "Your best reviews and Google Business Profile working together."),
        ("&#128200;", "Monthly report", "Visitors, leads, Google searches and AI referrals, in plain English."),
        ("&#128226;", "Launched to the town", "Your new site promoted on Three Village Local.")]
SITES = [("coltrain", "Coltrain Mortgage"), ("sbna", "SBNA"), ("lga", "LGA Marketing"), ("jm", "JM Management Solutions"), ("3vl", "Three Village Local")]
sites = "".join('<figure><div class="aif-shot"><img src="%ssite-%s.webp" alt="%s website, built by our team" loading="lazy" decoding="async"></div><figcaption>%s</figcaption></figure>' % (WEB, k, n, n) for k, n in SITES)
w('<section class="aif-sec aif-build rv" id="aif-build"><p class="aif-eye">04 &middot; What we do</p>'
  '<h3>We build websites <span>made for AI.</span></h3>'
  '<p class="aif-lead">Three Village Local designs, builds and hosts custom websites that customers love and AI can read on the first try. No bloated templates, no scripts hiding your content. One local team handles everything.</p>'
  '<div class="aif-feat">%s</div>' % "".join('<div class="aif-fcard rv"><span>%s</span><b>%s</b><p>%s</p></div>' % f for f in FEAT) +
  '<p class="aif-eye aif-eye-c">Websites we&rsquo;ve built</p><div class="aif-sites">%s</div>' % sites +
  '<div class="aif-btns aif-center"><a class="aif-btn aif-btn-blue" href="/websites">See website plans &rarr;</a></div>'
  '</section>')

# ---------------- 5. chatbot ----------------
w('<section class="aif-sec aif-tint rv" id="aif-bot"><p class="aif-eye">05 &middot; Add an AI assistant</p>'
  '<h3>A custom AI chatbot that answers questions and brings in leads.</h3>'
  '<div class="aif-split aif-split-r"><div class="aif-laptop" aria-hidden="true"><div class="aif-lscreen">'
  '<div class="aif-lsite"><b>Setauket Home Comfort</b><span>Heating &middot; Cooling &middot; Plumbing</span></div>'
  '<div class="aif-widget"><div class="aif-wbar"><span class="aif-av">&#129302;</span><b>Ask us anything</b><em>replies instantly</em></div>'
  '<div class="aif-chat" data-chat="bot">'
  '<div class="aif-msg aif-me">Do you do emergency repairs on Sundays?</div>'
  '<div class="aif-typing"><i></i><i></i><i></i></div>'
  '<div class="aif-msg aif-ai">Yes! We offer 24/7 emergency service in Setauket, Stony Brook and Port Jefferson. Want a technician to call you in the next 15 minutes?</div>'
  '<div class="aif-msg aif-me">Yes please. Dan, 631-555-0142</div>'
  '<div class="aif-typing"><i></i><i></i><i></i></div>'
  '<div class="aif-msg aif-ai">Got it, Dan. Someone will call you shortly. &#128077;</div>'
  '</div></div></div>'
  '<div class="aif-lead-toast"><span>&#128276;</span><div><b>New lead</b><small>Dan &middot; 631-555-0142 &middot; emergency repair</small></div></div>'
  '</div>'
  '<div><p class="aif-lead">Trained on your business and your industry, working 24/7.</p>'
  '<ul class="aif-ticks"><li><b>Answers real questions</b> about your services, hours, prices and policies, even at 11 PM.</li>'
  '<li><b>Knows your industry,</b> so it can explain options the way you would.</li>'
  '<li><b>Captures the lead</b> the moment someone is ready: name, number, what they need.</li>'
  '<li><b>Sends it straight to you</b> by text or email.</li></ul>'
  '<p class="aif-quote">Most customers contact the first business that answers. Your assistant always answers first.</p>'
  '</div></div></section>')

# ---------------- 6. free report ----------------
w('<section class="aif-sec aif-report rv" id="aif-report"><div class="aif-rin">'
  '<div class="aif-rtxt"><p class="aif-eye">Free, no strings</p>'
  '<h3>Get your free AI visibility report.</h3>'
  '<p class="aif-lead">Find out what AI says about your business today, and what to fix first.</p>'
  '<ul class="aif-ticks"><li><b>Who AI recommends</b> for your type of business in your town</li>'
  '<li><b>How AI reads your website</b>, and what it can&rsquo;t see</li>'
  '<li><b>Speed, mobile and Google profile</b> check</li>'
  '<li><b>Your top 3 fixes</b>, in plain English</li></ul>'
  '<p class="aif-small">Free, no obligation. Sent by email within 1 business day. No website yet? Leave it blank.</p></div>'
  '<div class="aif-rform"><div class="aif-fhead"><span>&#128202;</span><b>Your free report</b></div><div id="aif-form-slot">'
  '<a class="aif-btn aif-btn-gold aif-btn-wide" href="%s">Request my free report &rarr;</a></div></div>' % REPORT_PAGE +
  '</div></section>')

# ---------------- 7. FAQ ----------------
FAQ = [("Do I need a brand new website?", "Not always. Your free report shows what can be fixed on your current site. If your builder hides your content behind scripts, a rebuild is usually faster and cheaper than patching it."),
       ("Is AI replacing Google?", "Google now shows AI answers at the top of many searches too. The same things that help AI understand you also help you on Google. You win twice."),
       ("What does it cost?", 'Plans and member pricing are on our <a href="/websites">websites page</a>. Featured and VIP members of Three Village Local get a discount.')]
w('<section class="aif-sec rv" id="aif-faq"><h3>Quick questions.</h3><div class="aif-faq">%s</div></section>'
  % "".join('<details><summary>%s</summary><p>%s</p></details>' % f for f in FAQ))

# ---------------- final CTA ----------------
w('<section class="aif-final rv"><div class="aif-fin">'
  '<h3>AI is already recommending businesses in Three Village.<br><span>Make sure yours is one of them.</span></h3>'
  '<div class="aif-btns"><a class="aif-btn aif-btn-gold" href="#aif-report">Get my free AI report</a><a class="aif-btn aif-btn-white" href="/websites">See website plans</a></div>'
  '<button type="button" class="aif-share">Share this with a business owner</button></div></section>')

w('<p class="aif-cred">The businesses in the chat examples are fictional. ChatGPT, Gemini, Google, Copilot, Perplexity, Claude, Meta AI and Siri are trademarks of their owners.</p>')
w('</div>')
w('<style>#post-content .post-image-container,#post-content .post-image-container + hr{display:none!important}</style>')
w('<script src="%saif.js" defer></script>' % ASSET)

out = "".join(H)
for bad in ("—", "–"):
    assert bad not in out, "em/en dash"
open(os.path.join(HERE, "post.html"), "w", encoding="utf-8").write(out)
print("post.html", len(out), "chars")
