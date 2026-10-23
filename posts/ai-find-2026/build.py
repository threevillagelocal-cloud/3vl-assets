"""Can AI Find Your Business? (owner request 10/23/2026). Blog article that sells AI-ready websites + AI chatbots and collects
free AI visibility report requests (BD form ai_report, form 345, alerts to Gmail). Angle: how small local businesses can even
the AI playing field. Images: 3vl-share/ai-find/ (local storefront photos from weekender/ext) + 3vl-share/site/websites/.
Demo businesses in the chat animations are FICTIONAL on purpose (Harbor Light Bakery etc.), so no real business looks like a client.
    python build.py [--sha <3vl-assets commit>] [--local]   -> post.html"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SHA = sys.argv[sys.argv.index("--sha") + 1] if "--sha" in sys.argv else "master"
LOCAL = "--local" in sys.argv
ASSET = "" if LOCAL else "https://cdn.jsdelivr.net/gh/threevillagelocal-cloud/3vl-assets@%s/posts/ai-find-2026/" % SHA
IMG = "https://threevillagelocal-cloud.github.io/3vl-share/ai-find/"
WEB = "https://threevillagelocal-cloud.github.io/3vl-share/site/websites/"
REPORT_PAGE = "/free-ai-report"

# AI assistant logos: same SVG row the /websites page uses
src = open(os.path.join(HERE, "..", "..", "site", "websites-page", "build.py"), encoding="utf-8").read()
LOGOS = re.search(r'<div class="tvw-logo-row">(.*?)</div></section>', src, re.S).group(1)
LOGOS = LOGOS.replace('class="tvw-logo"', 'class="aif-logo"')

SHOPS = ["Ralph's Italian Ices, Stony Brook", "Tommy's Place, Port Jefferson", "Madiran The Wine Bar, Setauket",
         "DJ's Clam Shack, Stony Brook", "Toast Coffee + Kitchen, Port Jefferson", "Culpers 1778, Setauket",
         "Premiere Pastry, Setauket", "Kilwins, Port Jefferson", "Ixchel Mexican Cuisine, Setauket", "Little Cheese Shop, Stony Brook"]


def shop(i, eager=False):
    s = "%sshop-%d-400.webp 400w, %sshop-%d-640.webp 640w" % (IMG, i, IMG, i)
    lz = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return '<img src="%sshop-%d-400.webp" srcset="%s" sizes="(max-width:760px) 45vw, 300px" alt="%s storefront" width="400" height="300" %s>' % (IMG, i, s, SHOPS[i], lz)


H = []
w = H.append
w('<link rel="stylesheet" href="%saif.css">' % ASSET)
w('<div class="aif" id="aif-top"><div class="aif-prog"><i></i></div>')

# ---------------- HERO ----------------
w('<header class="aif-hero">'
  '<div class="aif-hl">'
  '<p class="aif-kick"><span class="aif-dot"></span>For Three Village business owners</p>'
  '<h2 class="aif-h1">Can AI find <span>your business?</span></h2>'
  '<p class="aif-sub">How small local businesses can even the AI playing field, before the competition gets there first.</p>'
  '<p class="aif-dek">Your next customer isn&rsquo;t scrolling through ten blue links. They&rsquo;re asking ChatGPT, Google or Siri one question and getting one short answer. If AI can&rsquo;t read your website, it can&rsquo;t recommend you. Here&rsquo;s why that&rsquo;s happening, how to fix it, and how to find out where you stand today, for free.</p>'
  '<div class="aif-btns"><a class="aif-btn aif-btn-gold" href="#aif-report">Get my free AI report</a><a class="aif-btn aif-btn-line" href="#aif-check">Take the 60-second check</a></div>'
  '</div>'
  '<div class="aif-hr">'
  '<div class="aif-mosaic">%s%s%s%s</div>' % (shop(0, True), shop(1, True), shop(2), shop(3)) +
  '<div class="aif-phone" aria-hidden="true"><div class="aif-pbar"><b>AI Assistant</b><span>online</span></div>'
  '<div class="aif-chat" data-chat="hero">'
  '<div class="aif-msg aif-me">What&rsquo;s the best bakery near Stony Brook?</div>'
  '<div class="aif-typing"><i></i><i></i><i></i></div>'
  '<div class="aif-msg aif-ai">Here are 3 local favorites:<ol><li><b>Harbor Light Bakery</b> &#9733; 4.9<br><small>Custom cakes, open early</small></li><li><b>Old Field Bread Co.</b> &#9733; 4.8<br><small>Sourdough, gluten-free options</small></li><li><b>Main Street Sweets</b> &#9733; 4.7<br><small>Cookies and cupcakes</small></li></ol></div>'
  '<div class="aif-yours">Is <b>your</b> business on this list?</div>'
  '</div></div>'
  '</div></header>')

# shop marquee
row = "".join(shop(i) for i in range(4, 10))
w('<div class="aif-marq" aria-label="Three Village small businesses"><div class="aif-mtrack">%s%s</div><p>Three Village runs on small businesses. AI should know yours by name.</p></div>' % (row, row.replace('alt="', 'aria-hidden="true" alt="')))

# jump nav (not sticky: it collides with the site header)
w('<nav class="aif-nav" aria-label="Jump to section"><a href="#aif-shift">The front door moved</a><a href="#aif-level">The level playing field</a>'
  '<a href="#aif-see">What AI sees</a><a href="#aif-why">Why templates fail</a><a href="#aif-build">What we build</a><a href="#aif-bot">AI chatbots</a><a href="#aif-check">60-second check</a><a href="#aif-report">Free report</a></nav>')

# ---------------- 1. the shift ----------------
w('<section class="aif-sec rv" id="aif-shift"><p class="aif-eye">01 &middot; What changed</p>'
  '<h3>The front door to your business moved.</h3>'
  '<p class="aif-lead">For twenty years, getting found meant ranking on Google. That&rsquo;s changing fast. Customers now ask AI assistants for the best plumber nearby, the dentist open on Saturday, the pizza place with a gluten-free crust. They get back a short list of names, not a page of links.</p>'
  '<p>Only a handful of businesses make that list. The rest are invisible, even if they&rsquo;ve been serving the neighborhood for decades.</p>'
  '<div class="aif-logos">%s</div>' % LOGOS +
  '<div class="aif-trio">'
  '<div class="aif-card rv"><div class="aif-ic">1</div><b>One answer, not ten links</b><p>AI picks a few businesses and names them. Nobody scrolls to page two because there is no page two.</p></div>'
  '<div class="aif-card rv"><div class="aif-ic">&#127908;</div><b>Asked out loud</b><p>In the car, in the kitchen, on the couch: &ldquo;Hey Siri, who fixes furnaces near me?&rdquo; Voice gets one answer.</p></div>'
  '<div class="aif-card rv"><div class="aif-ic">&#10003;</div><b>Recommended by name</b><p>When AI names you, customers arrive already trusting you. That&rsquo;s the warmest lead there is.</p></div>'
  '</div>'
  '<p class="aif-next">Next up: why this is the best news small businesses have had in years &darr;</p></section>')

# ---------------- 2. level playing field ----------------
w('<section class="aif-sec aif-tint rv" id="aif-level"><p class="aif-eye">02 &middot; The good news</p>'
  '<h3>For once, the playing field is level.</h3>'
  '<div class="aif-split"><div>'
  '<p class="aif-lead">AI doesn&rsquo;t care how big your ad budget is. It recommends the businesses it understands best.</p>'
  '<p>That means clear information about what you do, where you are, when you&rsquo;re open, and what real customers say about you. A family-owned shop with a well-built website can beat a national chain with a generic one.</p>'
  '<p><b>But the window won&rsquo;t stay open.</b> The businesses that get AI-ready first become the names AI keeps repeating, and that lead grows every month.</p>'
  '</div>'
  '<div class="aif-vs" aria-hidden="true"><p class="aif-vst">Who does AI understand better?</p>'
  '<div class="aif-vrow"><div class="aif-vlab"><span>&#127970;</span><b>Big chain</b><small>Huge ad budget, generic pages</small></div><div class="aif-vbar"><i style="--v:42%"></i></div></div>'
  '<div class="aif-vrow aif-vwin"><div class="aif-vlab"><span>&#127968;</span><b>Your local business</b><small>Real reviews, local know-how, AI-ready website</small></div><div class="aif-vbar"><i style="--v:94%"></i></div></div>'
  '<p class="aif-tip">AI recommends the business it understands best, not the biggest one.</p><p class="aif-small">Illustration</p></div>'
  '</div>'
  '<div class="aif-fomo rv"><b>&#9888;&#65039; Every month you wait,</b> a competitor gets a little more familiar to AI. Being first is a lot easier than catching up.</div>'
  '</section>')

# ---------------- 3. what AI sees ----------------
w('<section class="aif-sec rv" id="aif-see"><p class="aif-eye">03 &middot; Look behind the curtain</p>'
  '<h3>What your customer sees vs. what AI reads.</h3>'
  '<p class="aif-lead">Two websites can look the same to a person and completely different to AI. Flip the switch.</p>'
  '<div class="aif-tabs" role="tablist"><button type="button" role="tab" class="on" data-see="tpl">Template website</button><button type="button" role="tab" data-see="ai">AI-ready website</button></div>'
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
  '<p class="aif-small">Illustration with a sample business. Real results depend on how each site is built.</p>'
  '</section>')

# ---------------- 4. why templates ----------------
WHY = [("&#128220;", "The words are hidden inside scripts",
        "Many drag-and-drop builders assemble the page in the visitor&rsquo;s browser with JavaScript. People see a finished page. Many AI crawlers only read the raw code the server sends and don&rsquo;t run those scripts, so they can miss your services, prices and hours entirely."),
       ("&#128034;", "Heavy, slow code",
        "Templates ship code for every feature they offer, whether you use it or not. Slow pages lose customers on phones and give crawlers less to work with."),
       ("&#127991;&#65039;", "No labels AI can trust",
        "AI looks for structured data: behind-the-scenes labels that say this is a business, this is the address, these are the hours, these are the reviews. Most templates leave it out or fill it with generic defaults."),
       ("&#128203;", "Cookie-cutter pages",
        "Thousands of sites share the same layout and filler text. AI needs specific answers to the real questions customers ask about you, in your town.")]
w('<section class="aif-sec aif-dark rv" id="aif-why"><p class="aif-eye">04 &middot; The hidden problem</p>'
  '<h3>Why so many template websites trip up AI.</h3>'
  '<p class="aif-lead">It isn&rsquo;t your fault. Website builders were made to look good to people, years before AI assistants existed.</p>'
  '<div class="aif-why">%s</div>' % "".join('<div class="aif-wcard rv"><span>%s</span><b>%s</b><p>%s</p></div>' % x for x in WHY) +
  '<div class="aif-try rv"><b>Try this right now:</b> ask ChatGPT, &ldquo;What are the best <i>[your type of business]</i> near <i>[your town]</i>?&rdquo; Are you on the list? If not, keep reading.</div>'
  '</section>')

# ---------------- 5. what we build ----------------
FEAT = [("&#9889;", "Clean, fast code", "Built from scratch, readable from the very first line, quick on every phone."),
        ("&#127991;&#65039;", "Structured data on every page", "The labels AI and Google use to understand exactly who you are."),
        ("&#10067;", "Answer pages", "Pages that answer the real questions customers ask AI about your business and industry."),
        ("&#11088;", "Reviews and Google profile", "Your best reviews and your Google Business Profile working together."),
        ("&#128200;", "Monthly report", "Visitors, leads, Google searches and AI referrals, in plain English."),
        ("&#128226;", "Launched to the whole town", "Your new site promoted on Three Village Local to your neighbors.")]
SITES = [("coltrain", "Coltrain Mortgage"), ("sbna", "SBNA"), ("lga", "LGA Marketing"), ("jm", "JM Management Solutions"), ("3vl", "Three Village Local")]
sites = "".join('<figure><img src="%ssite-%s.webp" alt="%s website, built by our team" loading="lazy" decoding="async" width="960" height="600"><figcaption>%s</figcaption></figure>' % (WEB, k, n, n) for k, n in SITES)
w('<section class="aif-sec rv" id="aif-build"><p class="aif-eye">05 &middot; How we fix it</p>'
  '<h3>Websites built for people <span>and</span> for AI.</h3>'
  '<div class="aif-split"><div>'
  '<p class="aif-lead">Three Village Local designs, builds and hosts custom websites for local businesses. No bloated templates and no scripts hiding your content.</p>'
  '<p>Every page is written so a customer understands it in five seconds and an AI understands it on the first read. One local team handles the design, the build, the hosting and the updates.</p>'
  '<a class="aif-btn aif-btn-blue" href="/websites">See website plans &rarr;</a>'
  '</div><div class="aif-tablet" aria-hidden="true"><div class="aif-tscreen"><img src="%stablet-home.webp" alt="" loading="lazy" decoding="async" width="960" height="2929"></div></div></div>' % WEB +
  '<div class="aif-feat">%s</div>' % "".join('<div class="aif-fcard rv"><span>%s</span><b>%s</b><p>%s</p></div>' % f for f in FEAT) +
  '<p class="aif-eye aif-eye-c">Sites we&rsquo;ve built</p><div class="aif-sites">%s</div>' % sites +
  '</section>')

# ---------------- 6. chatbot ----------------
w('<section class="aif-sec aif-tint rv" id="aif-bot"><p class="aif-eye">06 &middot; Your 24/7 front desk</p>'
  '<h3>Your own AI assistant that answers questions and brings in leads.</h3>'
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
  '<div><p class="aif-lead">We build custom AI chatbots trained on your business and your industry.</p>'
  '<ul class="aif-ticks"><li><b>Answers real questions</b> about your services, hours, prices and policies, at 11 PM or on a holiday.</li>'
  '<li><b>Knows your industry,</b> so it can explain the difference between a repair and a replacement, or what to expect at a first visit.</li>'
  '<li><b>Captures the lead</b> the moment someone is ready: name, number, what they need.</li>'
  '<li><b>Sends it straight to you</b> by text or email, so you call back while they&rsquo;re still deciding.</li></ul>'
  '<p class="aif-quote">Most customers contact the first business that answers. Your assistant always answers first.</p>'
  '</div></div></section>')

# ---------------- 7. 60-second check ----------------
QS = ["When you ask ChatGPT for the best <i>[your business]</i> in your town, do you show up?",
      "Does your website say what you do, your town and your hours in plain words?",
      "Does your site load in under 3 seconds on a phone?",
      "Does your website have structured data (schema) for your business?",
      "Is your Google Business Profile complete, with reviews from the last few months?",
      "Can a customer get an answer or leave their info at 10 PM?"]
qs = "".join('<div class="aif-q" data-q="%d"><p><span>%d</span>%s</p><div class="aif-qb"><button type="button" data-a="1">Yes</button><button type="button" data-a="0">No</button><button type="button" data-a="0">Not sure</button></div></div>' % (i, i + 1, q) for i, q in enumerate(QS))
w('<section class="aif-sec rv" id="aif-check"><p class="aif-eye">07 &middot; Where do you stand?</p>'
  '<h3>The 60-second AI check.</h3><p class="aif-lead">Six quick questions. Be honest, nobody&rsquo;s watching.</p>'
  '<div class="aif-quiz"><div class="aif-qs">%s</div>' % qs +
  '<div class="aif-score"><svg viewBox="0 0 120 120" aria-hidden="true"><circle cx="60" cy="60" r="52" class="aif-ring-bg"/><circle cx="60" cy="60" r="52" class="aif-ring"/></svg>'
  '<div class="aif-snum"><b>0</b><span>of 6</span></div><p class="aif-smsg">Answer the questions to see your score.</p>'
  '<a class="aif-btn aif-btn-gold" href="#aif-report">Get my free AI report</a></div></div></section>')

# ---------------- 8. free report ----------------
w('<section class="aif-sec aif-report rv" id="aif-report"><div class="aif-rin">'
  '<div class="aif-rtxt"><p class="aif-eye">08 &middot; Free, no strings</p>'
  '<h3>Get your free AI visibility report.</h3>'
  '<p class="aif-lead">Find out exactly what AI says about your business today, and what to fix first.</p>'
  '<ul class="aif-ticks"><li><b>Who AI recommends</b> when people ask for your type of business in your town</li>'
  '<li><b>How AI reads your website</b>, and what it can&rsquo;t see</li>'
  '<li><b>Speed and mobile check</b> on your homepage</li>'
  '<li><b>Your Google profile</b> and reviews at a glance</li>'
  '<li><b>Your top 3 fixes</b>, in plain English</li></ul>'
  '<p class="aif-small">Free, no obligation. We send it by email within 1 business day. No website yet? Leave it blank and we&rsquo;ll show you what AI finds about you anyway.</p></div>'
  '<div class="aif-rform"><div class="aif-fhead"><span>&#128202;</span><b>Your free report</b></div><div id="aif-form-slot">'
  '<a class="aif-btn aif-btn-gold aif-btn-wide" href="%s">Request my free report &rarr;</a></div></div>' % REPORT_PAGE +
  '</div></section>')

# ---------------- 9. FAQ ----------------
FAQ = [("Do I need a brand new website?", "Not always. Your free report shows what can be fixed on your current site and what can&rsquo;t. If your builder hides your content behind scripts, a rebuild is usually faster and cheaper than patching it."),
       ("I&rsquo;m not a tech person. Is this complicated?", "Not for you. We handle the design, the build, the hosting and the updates. You tell us about your business, we do the rest."),
       ("Is AI really replacing Google?", "Google is still huge, and it now shows AI answers at the top of many searches too. The same things that help AI understand you also help you on Google. You win twice."),
       ("What does a website cost?", 'Plans and member pricing are on our <a href="/websites">websites page</a>. Three Village Local Featured and VIP members get a discount.'),
       ("Can you add an AI chatbot to my existing site?", "Often, yes. Tell us about your site in the report form and we&rsquo;ll let you know.")]
w('<section class="aif-sec rv" id="aif-faq"><p class="aif-eye">Questions</p><h3>Good questions we hear a lot.</h3><div class="aif-faq">%s</div></section>'
  % "".join('<details><summary>%s</summary><p>%s</p></details>' % f for f in FAQ))

# ---------------- final CTA ----------------
w('<section class="aif-final rv"><div class="aif-fmos">%s</div><div class="aif-fin">'
  '<h3>AI is already recommending businesses in Three Village.<br><span>Make sure one of them is yours.</span></h3>'
  '<div class="aif-btns"><a class="aif-btn aif-btn-gold" href="#aif-report">Get my free AI report</a><a class="aif-btn aif-btn-white" href="/websites">See website plans</a></div>'
  '<button type="button" class="aif-share">Share this with a business owner</button></div></section>' % "".join(shop(i) for i in (6, 7, 8, 9)))

w('<p class="aif-cred">Photos: Three Village Local. Storefronts shown are local favorites; the businesses in the chat examples are fictional. ChatGPT, Gemini, Google, Copilot, Perplexity, Claude, Meta AI and Siri are trademarks of their owners.</p>')
w('</div>')
w('<style>#post-content .post-image-container,#post-content .post-image-container + hr{display:none!important}</style>')
w('<script src="%saif.js" defer></script>' % ASSET)

open(os.path.join(HERE, "post.html"), "w", encoding="utf-8").write("".join(H))
out = "".join(H)
for bad in ("—", "–"):
    assert bad not in out, "em/en dash"
print("post.html", len(out), "chars")
