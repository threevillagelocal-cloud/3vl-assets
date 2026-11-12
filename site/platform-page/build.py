"""Our Services: the whole Three Village Local platform on one page (owner 11/3/2026: "this is where it all lives").
Mission first, then the reach, the two paths (launch a new business / AI overhaul), the AI urgency, every service, how it
all works together, and the message form. Same design system as /websites and /ai-assistant.
    python site/platform-page/build.py          -> widget "3VL Page Platform Preview" + hidden /preview-our-services
    python site/platform-page/build.py --live   -> widget "3VL Page Platform" + /our-services"""
import importlib.util, os
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("aibuild", os.path.join(HERE, "..", "ai-assistant-page", "build.py"))
A = importlib.util.module_from_spec(spec)
spec.loader.exec_module(A)
D, sec = A.D, A.sec

D.NAME = "3VL Page Platform" if D.LIVE else "3VL Page Platform Preview"
D.SLUG = "services" if D.LIVE else "preview-our-services"
D.TITLE = "Our Services: Local Marketing, AI Websites, AI Assistants and Video | Three Village Local"
D.DESC = ("Three Village Local connects local businesses with the community: our website, mobile app, social media and email, "
          "plus AI websites, AI assistants, AI optimization and video. Launch a new business or give yours an AI overhaul.")
D.FB_TITLE = "We connect local businesses with the community."

AI = "/ai-assistant"
SH = "https://threevillagelocal-cloud.github.io/3vl-share/site/"
APP = "https://cdn.jsdelivr.net/gh/threevillagelocal-cloud/3vl-assets@1328a06c9ca8ab841e46fd8b85170aaef3bd1e63/site/app/"

import re as _re
_m = _re.search(r'<div class="tvw-logo-row">.*?</div>', A.W.STRIP_SEC, _re.S)
AIROW = _m.group(0)
HERO = """<section class="tvp-top" id="tvp-top">
  <div class="tvp-top-in tvs-up">
    <p class="tvs-kick"><span class="tvs-dot"></span>Our services</p>
    <h1>You know us for promoting local businesses.<br><span>That&#39;s just the beginning.</span></h1>
    <p class="tvp-lede">Every day, our <b>website</b>, free <b>mobile app</b> and <b>social media</b> put local businesses in front of the whole Three Village community. We also offer the modern tools that help a business get seen, get chosen and grow, all from one local team.</p>
    <ul class="tvs-trust tvp-trust"><li><b>45,000+</b>website page visits a month</li><li><b>100,000+</b>social views a month</li><li><b>One</b>local team</li></ul>
  </div>
  <div class="tvp-ai tvs-up"><p>We help you get found and recommended on</p>""" + AIROW + """</div>
  <div class="tvp-glance" aria-label="Everything we offer">
    <div class="tvp-gcol tvs-up">
      <div class="tvp-gh"><p>On Three Village Local</p><h2>Get promoted where locals look</h2></div>
      <a href="#tvp-seen"><span>&#11088;</span><div><b>Featured &amp; VIP memberships</b><i>Top spots in search, homepage features and banners</i></div><em>&rarr;</em></a>
      <a href="#tvp-social"><span>&#128227;</span><div><b>Social media promotion</b><i>Posts and reels shared to 100,000+ local views a month</i></div><em>&rarr;</em></a>
      <a href="#tvp-app"><span>&#128241;</span><div><b>Mobile app</b><i>Your specials and events on local phones, plus push alerts</i></div><em>&rarr;</em></a>
      <a href="#tvp-seen"><span>&#128197;</span><div><b>Events &amp; specials</b><i>On our calendar, homepage and weekly picks</i></div><em>&rarr;</em></a>
      <a href="#tvp-email"><span>&#128231;</span><div><b>Weekly email &amp; articles</b><i>Spotlights and stories neighbors actually read</i></div><em>&rarr;</em></a>
    </div>
    <div class="tvp-gcol tvp-gdark tvs-up">
      <div class="tvp-gh"><p>Tools to get seen and grow</p><h2>Done for you by our local team</h2></div>
      <a href="#tvp-web"><span>&#128187;</span><div><b>AI-optimized websites</b><i>Designed, built and hosted to be found on Google and AI</i></div><em>&rarr;</em></a>
      <a href="#tvp-bot"><span>&#129302;</span><div><b>AI chatbot: Digital Front Desk</b><i>Answers customers 24/7 and texts you every lead</i></div><em>&rarr;</em></a>
      <a href="#tvp-web"><span>&#128200;</span><div><b>SEO optimization</b><i>Rank higher on Google when locals search for what you do</i></div><em>&rarr;</em></a>
      <a href="#tvp-ai"><span>&#10024;</span><div><b>AI search optimization</b><i>Get recommended by ChatGPT, Gemini and Google AI</i></div><em>&rarr;</em></a>
      <a href="#tvp-social"><span>&#128172;</span><div><b>Social media marketing</b><i>Scroll-stopping content for your own Facebook and Instagram</i></div><em>&rarr;</em></a>
      <a href="#tvp-video"><span>&#127909;</span><div><b>Promo video</b><i>Short reels that show off your business</i></div><em>&rarr;</em></a>
    </div>
  </div>
  <div class="tvp-gfoot tvs-up"><p>Pick one, or put them together. They all work as one.</p><div class="tvs-ctas"><a class="tvs-btn tvs-blue" href="#tvs-book">Get a free plan</a><a class="tvs-btn tvs-ghost" href="#tvp-seen">Explore each service</a></div></div>
</section>"""

PATHS = '''<section class="tvs-sec tvp-paths" id="tvp-paths">
  <div class="tvs-head tvs-up"><p class="tvs-eyebrow">Where are you today?</p><h2>Two ways we help. Both start with you.</h2></div>
  <div class="tvp-two">
    <a class="tvp-path tvs-up" href="#tvp-launch"><span class="tvp-tag">New business</span><h3>Build it right.</h3>
      <p>Open your doors with the whole town watching: a website AI can find, your Google and Apple listings, a Three Village Local launch spotlight, social posts and video.</p><em>Plan my launch &rarr;</em></a>
    <a class="tvp-path tvp-dark tvs-up" href="#tvp-ai"><span class="tvp-tag">Established business</span><h3>Get an AI overhaul.</h3>
      <p>Your reputation is built. Now make sure AI tools recommend you, your website turns visitors into leads 24/7, and the whole community keeps seeing you.</p><em>Show me the overhaul &rarr;</em></a>
  </div>
</section>'''

FOMO = '''<section class="tvs-sec tvp-fomo" id="tvp-ai">
  <div class="tvp-fomo-in tvs-up">
    <p class="tvs-eyebrow">The shift is already happening</p>
    <h2>Your next customer is asking AI who to call.<br><span>Is it saying your name?</span></h2>
    <p>Nearly half of people now use AI tools like ChatGPT and Google&#39;s AI to find local businesses (BrightLocal, 2026). AI recommends the businesses it can read, understand and trust. If yours isn&#39;t one of them, those customers go to whoever is.</p>
    <div class="tvp-vs"><div><b>Without AI</b><span>Invisible to AI answers</span><span>Questions wait until morning</span><span>Leads slip to competitors</span></div>
      <div class="tvp-vs-on"><b>With Three Village Local AI</b><span>Built to be noticed and recommended</span><span>Answers in seconds, 24/7</span><span>Every lead sent straight to you</span></div></div>
    <div class="tvp-ctas tvp-ctas-c"><a class="tvs-btn tvw-btn-w" href="''' + AI + '''">See the AI overhaul</a><a class="tvs-btn tvw-btn-o" href="#tvs-book">Get my free plan</a></div>
    <a class="tvp-aicheck" href="/free-ai-report"><span>&#128269;</span><div><b>Does ChatGPT recommend your business?</b><i>Get a free AI visibility check. Takes 1 minute.</i></div><em>Check free &rarr;</em></a>
  </div>
</section>'''


def row(i, eyebrow, title, text, bullets, cta, href, visual, flip=False, extra=""):
    li = "".join("<li>%s</li>" % b for b in bullets)
    return '''<section class="tvs-sec tvp-row%s" id="tvp-%s">
  <div class="tvp-row-in">
    <div class="tvp-txt tvs-up"><p class="tvs-eyebrow">%s</p><h2>%s</h2><p>%s</p><ul class="tvp-ul">%s</ul><div class="tvp-ctas"><a class="tvs-btn tvs-blue" href="%s">%s</a>%s</div>%s</div>
    <div class="tvp-art tvs-up">%s</div>
  </div>
</section>''' % (" tvp-flip" if flip else "", i, eyebrow, title, text, li, href, cta, ('<a class="tvs-btn tvs-ghost" href="#tvs-book">Get my free plan</a>' if href != "#tvs-book" else ""), extra, visual)


V_STAGE = '''<div class="tvp-stage"><div class="tvp-sq"><span>&#128269;</span>plumber near Setauket<em>12 results</em></div>
  <div class="tvp-stage-card"><span class="tvp-vip">&#9733; VIP</span><b>Your Business</b><i>Top of search &middot; one-tap call</i>
    <div class="tvp-sc-row"><em>&#9733;&#9733;&#9733;&#9733;&#9733; 5.0</em><u>&#9742; Call</u><u>Website</u></div></div>
  <div class="tvp-res tvp-res-f"><span class="tvp-av">F</span><div><b>Featured Business</b><i>&#9733;&#9733;&#9733;&#9733;&#9733; &middot; Photos and logo</i></div><em class="tvp-badge">Featured</em></div>
  <div class="tvp-res"><span class="tvp-av">B</span><div><b>Basic listing</b><i>Name and phone</i></div></div>
  <div class="tvp-res tvp-res-2"><span class="tvp-av">B</span><div><b>Basic listing</b><i>Name and phone</i></div></div>
  <p class="tvp-cap">Top spots, homepage features, banners and spotlights</p></div>'''
V_SOCIAL = '''<div class="tvp-soc"><div class="tvp-fan"><img src="''' + SH + '''services/w-tommys-place-v2.webp" alt="Social post for Tommy's Place" loading="lazy" width="320" height="400">
  <img src="''' + SH + '''services/w-namkeen-hot-chicken-v1.webp" alt="Social post for Namkeen Hot Chicken" loading="lazy" width="320" height="400">
  <img src="''' + SH + '''services/w-savera-wood-floor-refinishing-v1.webp" alt="Social post for Savera Wood Floor Refinishing" loading="lazy" width="320" height="400"></div>
  <div class="tvp-fan tvp-fan2"><img src="''' + SH + '''services/w-the-pie-of-port-jeff-v2.webp" alt="Social post for The Pie of Port Jeff" loading="lazy" width="560" height="294"><img src="''' + SH + '''services/w-kgr-contracting-v3.webp" alt="Social post for KGR Contracting" loading="lazy" width="560" height="294"><img src="''' + SH + '''services/w-saturday-candy-co-v4.webp" alt="Social post for Saturday Candy Co" loading="lazy" width="560" height="294"></div>
  <div class="tvp-reach"><div class="tvp-reach-n"><b>100,000+</b><span>local views a month</span></div><div class="tvp-plats"><span><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="12" fill="#1877F2"/><path fill="#fff" d="M13.4 20v-6.4h2.2l.3-2.6h-2.5V9.4c0-.7.2-1.2 1.3-1.2h1.3V5.9c-.2 0-1-.1-2-.1-2 0-3.3 1.2-3.3 3.4V11H8.5v2.6h2.2V20z"/></svg>Facebook</span><span><svg viewBox="0 0 24 24"><defs><linearGradient id="tvpIgG" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#FEDA75"/><stop offset=".35" stop-color="#FA7E1E"/><stop offset=".6" stop-color="#D62976"/><stop offset="1" stop-color="#4F5BD5"/></linearGradient></defs><rect width="24" height="24" rx="6.5" fill="url(#tvpIgG)"/><rect x="5.5" y="5.5" width="13" height="13" rx="4" fill="none" stroke="#fff" stroke-width="1.8"/><circle cx="12" cy="12" r="3.1" fill="none" stroke="#fff" stroke-width="1.8"/><circle cx="16.3" cy="7.7" r="1" fill="#fff"/></svg>Instagram</span><span><svg viewBox="0 0 24 24"><rect width="24" height="24" rx="6.5" fill="#111"/><path fill="#25F4EE" d="M10.2 10.6v-1a4.6 4.6 0 1 0 3.3 4.4V8.6a5.6 5.6 0 0 0 3.3 1V8a3.3 3.3 0 0 1-3.3-3.3h-1.7v9.3a1.9 1.9 0 1 1-1.6-1.9z" transform="translate(-.6 -.4)"/><path fill="#FE2C55" d="M10.2 10.6v-1a4.6 4.6 0 1 0 3.3 4.4V8.6a5.6 5.6 0 0 0 3.3 1V8a3.3 3.3 0 0 1-3.3-3.3h-1.7v9.3a1.9 1.9 0 1 1-1.6-1.9z" transform="translate(.6 .4)"/><path fill="#fff" d="M10.2 10.6v-1a4.6 4.6 0 1 0 3.3 4.4V8.6a5.6 5.6 0 0 0 3.3 1V8a3.3 3.3 0 0 1-3.3-3.3h-1.7v9.3a1.9 1.9 0 1 1-1.6-1.9z"/></svg>TikTok</span></div>
  <div class="tvp-reach-t"><i>&#10003; Your business tagged</i><i>&#10003; Collab posts</i><i>&#10003; Reels and stories</i></div></div></div>'''
V_APP = '''<div class="tvp-phone"><img src="''' + SH + '''services/app-home-screen-v1.webp" alt="The Three Village Local homepage on a phone" loading="lazy" width="300" height="620"><div class="tvp-push"><b>Three Village Local</b>&#127881; This weekend only at Your Business...</div></div>'''
V_WEB = '''<div class="tvp-browser"><div class="tvp-bar"><i></i><i></i><i></i><span>&#128274; yourbakery.com</span></div>
  <div class="tvp-site"><div class="tvp-snav"><b>Your Bakery</b><span>Menu</span><span>Cakes</span><span>Visit</span><em>Order ahead</em></div>
  <div class="tvp-shero"><div><p class="tvp-sk">Main Street &middot; Since 1998</p><p class="tvp-sh">Fresh bread, baked every morning.</p><p class="tvp-sbtn"><i>See the menu</i><u>Directions</u></p><p class="tvp-sg"><b>G</b> 5.0 <em>&#9733;&#9733;&#9733;&#9733;&#9733;</em> Google</p></div>
  <div class="tvp-simg"><img src="''' + SH + '''websites/mock-croissants-3q.webp" alt="" loading="lazy" width="380" height="292"></div></div>
  <div class="tvp-srow"><div><b>Open today</b>7 AM - 6 PM</div><div><b>Custom cakes</b>48 hr notice</div><div><b>Gluten-free</b>Every day</div></div></div>
  <div class="tvp-gpt"><b>&#10022; AI answer</b>Locals recommend <u>Your Bakery</u> on Main Street for fresh bread and custom cakes.</div>
  <div class="tvp-ai-tag">&#10022; Read and recommended by AI</div></div>'''
V_BOT = '''<div class="tvp-chat"><div class="tvp-chat-h">&#10022; Your Business Front Desk</div><p class="me">Are you open Sunday?</p><p>Yes, 10 to 4! Want me to book you a time?</p><p class="me">Yes, Sarah, 631-555-0188</p><div class="tvp-lead">&#128241; New lead sent to you</div></div>'''
V_VIDEO = '''<div class="tvp-vids"><div class="tvp-reel"><video class="tvp-rv" muted playsinline loop preload="none" poster="''' + SH + '''services/campus-bikes-poster.webp" data-src="''' + SH + '''services/campus-bikes-720.mp4" width="720" height="900" aria-label="Promo video for Campus Bicycles in Stony Brook"></video>
  <button type="button" class="tvp-snd" aria-label="Turn sound on">&#128263; Tap for sound</button>
  <div class="tvp-rtag"><b>Campus Bicycles</b><span>Stony Brook &middot; made by Three Village Local</span></div></div>
 <div class="tvp-vph"><div class="tvp-vph-in"><span class="tvp-vph-notch"></span><video class="tvp-rv" muted playsinline loop preload="none" poster="''' + SH + '''services/girard-poster.webp" data-src="''' + SH + '''services/girard-720.mp4" width="720" height="1280" aria-label="Promo video for Girard Wealth Management, made by Three Village Local"></video>
  <button type="button" class="tvp-snd" aria-label="Turn sound on">&#128263; Tap for sound</button></div>
  <div class="tvp-rtag"><b>Girard Wealth Management</b><span>Made by Three Village Local</span></div></div></div>'''
V_EMAIL = '''<div class="tvp-mail"><div class="tvp-mail-h"><b>Three Village Weekly</b><span>Every Friday</span></div><div class="tvp-mail-b">
  <p class="tvp-mk">This weekend in Three Village</p>
  <div class="tvp-ev"><span><b>SAT</b>14</span><div><b>Holiday craft fair</b><i>Village green &middot; 10 AM</i></div></div>
  <div class="tvp-ev"><span><b>SUN</b>15</span><div><b>Live music + brunch</b><i>Main Street &middot; 11 AM</i></div></div>
  <div class="tvp-feat"><img src="''' + SH + '''services/w-tommys-place-v2.webp" alt="" loading="lazy" width="320" height="400"><div><em>&#9733; Featured business</em><b>Your Business</b><i>Meet the family behind Main Street&#39;s favorite spot.</i><u>Read the story &rarr;</u></div></div>
  <div class="tvp-mfoot">Also in the mobile app and on social</div></div></div>'''

HAVE = '''<div class="tvp-have"><p class="tvp-have-k">Already have a website?</p><h3>Keep it. We&#39;ll make it smarter.</h3>
  <a href="#tvs-book"><span>&#10024;</span><div><b>AI search optimization</b><i>We tune the site you already have so ChatGPT, Gemini and Google AI can read it and recommend you.</i></div><em>&rarr;</em></a>
  <a href="/ai-assistant"><span>&#129302;</span><div><b>Add an AI chatbot</b><i>Our Digital Front Desk works on your current website, answers customers 24/7 and texts you every lead.</i></div><em>&rarr;</em></a>
  <p class="tvp-have-f">Do one, or both. No rebuild needed.</p></div>'''

ROWS = "\n\n".join([
    row("web", "AI-Ready websites", "A website AI can read, and customers love.",
        "We design, build and host a fast, beautiful website written so Google and AI tools understand exactly what you do, then we launch it to the whole town.",
        ["Designed, written and hosted for you", "Built for Google and AI search from the first line", "Domain in your name, updates included"],
        "See AI websites", "/websites", V_WEB, False, HAVE),
    row("video", "Promo video", "Show them, don&#39;t just tell them.",
        "Short promo videos and reels that make your business look its best, shared across our site, social media and mobile app.",
        ["Filmed, edited and captioned for you", "Sized for Instagram, Facebook and your website", "Included with VIP, discounted for Featured members"],
        "Ask about promo video", "#tvs-book", V_VIDEO, True),
    row("seen", "Get seen on Three Village Local", "Be the first name neighbors see.",
        "Featured and VIP memberships put your business at the top of our directory, on our homepage and across the site, where locals already go to find who to call.",
        ["Top-of-search placement with one-tap call", "Homepage features, banners and spotlights", "Post your events and specials on the site and mobile app"],
        "See memberships", "/join", V_STAGE, False),
    row("social", "Social media promotion", "Seen all over town, every week.",
        "We create scroll-stopping posts and reels for your business and share them with more than 100,000 local views a month on Facebook and Instagram.",
        ["Custom graphics and reels, made for you", "Tagged and shared with your own accounts", "Launch posts, specials, events and spotlights"],
        "Ask about social promotion", "#tvs-book", V_SOCIAL, True),
    row("app", "The Three Village Local mobile app", "Right on their phones.",
        "Our free mobile app keeps neighbors connected to local businesses, events and specials. VIP members can send a push notification straight to local phones.",
        ["Your listing, specials and events in the mobile app", "Push notifications to local phones (VIP)", "Free for the community on iPhone and Android"],
        "See the mobile app", "/app", V_APP, False),
    row("bot", "Your Digital Front Desk", "Your best salesperson, open 24/7.",
        "A smart AI assistant on your current website answers customers in seconds, day or night, and sends you every lead. It comes with AI Website Optimization so you get noticed and recommended by AI.",
        ["Works with the website you already have", "Live person handoff: you get an instant text", "Follows your industry's rules and guidelines"],
        "Try the live demo", AI, V_BOT, True),
    row("email", "Email and articles", "Stories the community actually reads.",
        "Get featured in our weekly email and in custom articles on Three Village Local, so neighbors learn the story behind your business.",
        ["Spotlights in our weekly email", "Custom blog and article features", "Shared across social and the mobile app"],
        "Get featured", "#tvs-book", V_EMAIL, False)
])

LAUNCH = '''<section class="tvs-sec tvp-launch" id="tvp-launch">
  <div class="tvs-head tvs-up"><p class="tvs-eyebrow">Better together</p><h2>One plan. Every piece working for you.</h2>
  <p>Each service is great on its own. Together, they become a system that gets you found, chosen and remembered.</p></div>
  <ol class="tvp-flow tvs-up">
    <li><b>1</b><em>Get found</em>AI-Ready website and AI optimization so Google and AI tools recommend you</li>
    <li><b>2</b><em>Get seen</em>Three Village Local, social media, the mobile app and email put you in front of neighbors</li>
    <li><b>3</b><em>Get chosen</em>Your AI assistant answers every question and turns visitors into leads</li>
    <li><b>4</b><em>Keep growing</em>Video and fresh content keep you top of mind, every month</li>
  </ol>
  <div class="tvp-why tvs-up">
    <div><b>&#127968; Local</b>We live and work in Three Village. We know your customers because they&#39;re our neighbors too.</div>
    <div><b>&#9889; Done for you</b>You run your business. We handle the tech, the content and the promotion.</div>
    <div><b>&#10024; VIP AI service</b>Leading-edge AI, set up and tuned by a real local team, never a faceless app.</div>
  </div>
  <div class="tvp-ctas tvp-ctas-c tvs-up"><a class="tvs-btn tvs-blue" href="#tvs-book">Build my free plan</a></div>
</section>'''

VS = '''<section class="tvs-sec tvs-vs tvp-cmp">
  <div class="tvs-head tvs-up"><p class="tvs-eyebrow">More value, one local team</p><h2>A typical marketing agency vs. Three Village Local</h2>
  <p>Most agencies sell you SEO and reports. We bring the audience, the AI and the content, all working together.</p></div>
  <div class="tvs-table tvs-up" role="table">
    <div class="tvs-tr tvs-th" role="row"><span role="columnheader"></span><span role="columnheader">Typical agency</span><span role="columnheader">Three Village Local</span></div>
    <div class="tvs-tr" role="row"><span role="cell">Website and SEO</span><span role="cell" class="tvs-y">&#10003;</span><span role="cell" class="tvs-y">&#10003;</span></div>
    <div class="tvs-tr" role="row"><span role="cell">AI optimization for ChatGPT, Gemini and Google AI</span><span role="cell" class="tvs-n">Sometimes</span><span role="cell" class="tvs-y">&#10003;</span></div>
    <div class="tvs-tr" role="row"><span role="cell">A live AI front desk you can try right now</span><span role="cell" class="tvs-n">&mdash;</span><span role="cell" class="tvs-y">&#10003;</span></div>
    <div class="tvs-tr" role="row"><span role="cell">A built-in local audience: 45,000+ site visits and 100,000+ social views a month</span><span role="cell" class="tvs-n">&mdash;</span><span role="cell" class="tvs-y">&#10003;</span></div>
    <div class="tvs-tr" role="row"><span role="cell">Your business in a local mobile app, with push notifications</span><span role="cell" class="tvs-n">&mdash;</span><span role="cell" class="tvs-y">&#10003;</span></div>
    <div class="tvs-tr" role="row"><span role="cell">Promo video, made in house</span><span role="cell" class="tvs-n">Rarely</span><span role="cell" class="tvs-y">&#10003;</span></div>
    <div class="tvs-tr" role="row"><span role="cell">Clear pricing posted up front</span><span role="cell" class="tvs-n">Rarely</span><span role="cell" class="tvs-y">&#10003;</span></div>
    <div class="tvs-tr" role="row"><span role="cell">Month to month, no long contract</span><span role="cell" class="tvs-n">Varies</span><span role="cell" class="tvs-y">&#10003;</span></div>
    <div class="tvs-tr" role="row"><span role="cell">A local team that lives in your community</span><span role="cell" class="tvs-n">&mdash;</span><span role="cell" class="tvs-y">&#10003;</span></div>
  </div>
  <div class="tvp-ctas tvp-ctas-c tvs-up"><a class="tvs-btn tvs-blue" href="#tvs-book">Get my free plan</a></div>
</section>'''

CTA = '''<section class="tvw-cta3 tvs-up"><div class="tvw-cta3-in"><p class="tvw-cta3-k">Your competition isn&#39;t waiting</p><h2>Let&#39;s build your plan.</h2>
<p class="tvw-cta3-s">Tell us about your business and we&#39;ll send you a free, no-pressure plan by email.</p>
<div class="tvw-cta-btns"><a class="tvs-btn tvw-btn-w" href="#tvs-book">Send us a message</a><a class="tvs-btn tvw-btn-o" href="''' + AI + '''">Try the Digital Front Desk</a></div></div></section>'''

i, j = sec(A.HTML, "tvs-sec tvs-book")
BOOK0 = A.HTML[i:j].replace("mailto:hello@threevillagelocal.com?subject=AI%20for%20my%20website", "mailto:hello@threevillagelocal.com?subject=Our%20services")
BOOK = BOOK0.replace('<p class="tvs-eyebrow">Let\'s talk</p>', '<p class="tvs-eyebrow">Your free plan</p>').replace(
    "<h2>Tell us about your business.</h2>", "<h2>Get your free plan.</h2>").replace(
    "<p>Send us a quick message and we will reply by email, usually within one business day. Everything can happen by email or text. If you would rather talk it through, we are happy to set up a call.</p>",
    """<p>Tell us your name, business and email. Within one business day you&#39;ll get a free, personalized plan by email:</p>
    <ul class="tvp-get"><li>How you show up on Google and AI tools today</li><li>The 3 things we&#39;d do first for your business</li><li>Clear pricing, no pressure, no contract</li></ul>
    <div class="tvp-proof"><div class="tvp-proof-h"><b>5.0</b><span>&#9733;&#9733;&#9733;&#9733;&#9733;</span><em>on Google</em></div>
      <blockquote>&ldquo;A great community-based website that eases the process of finding local businesses for the services you need.&rdquo;<cite>Amy C. Raupp, Raupp Law</cite></blockquote>
      <blockquote>&ldquo;A one stop shop to plan your weekend!&rdquo;<cite>Stony Brook Harbor Kayak &amp; Paddleboard Rentals</cite></blockquote>
      <blockquote>&ldquo;Amazing resource! Thank you for all you do to support the 3V community.&rdquo;<cite>Maryann B., neighbor</cite></blockquote></div>
    <p class="tvp-alt">Rather start smaller? <a href="/free-ai-report">See if ChatGPT recommends your business &rarr; free AI check</a></p>""")
HTML = ('<div class="tvs" id="tvs">\n\n' + HERO + "\n\n" + FOMO + "\n\n" + ROWS + "\n\n" + LAUNCH + "\n\n" + VS + "\n\n" + CTA + "\n\n" + BOOK +
        '\n\n<a class="tvs-sticky" href="#tvs-book">Get my free plan</a>\n</div>')
assert "\\" not in HTML

CSS = '''
.tvp-vis{display:flex;align-items:center;justify-content:center;background:radial-gradient(600px 400px at 60% 40%,rgba(77,163,255,.22),transparent 70%),linear-gradient(160deg,#f3f8ff,#e6f0ff)!important}
.tvp-menu{position:relative;z-index:1;box-sizing:border-box;width:100%;max-width:440px;margin:0 auto;padding:18px!important;border-radius:24px!important;overflow:hidden;background:#fff;box-shadow:0 30px 70px -30px rgba(9,30,66,.45),0 0 0 1px rgba(15,42,82,.06)}
.tvp-menu-k{margin:2px 6px 10px!important;font-size:12.5px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--blue)}
.tvp-menu *{box-sizing:border-box}.tvp-menu a{display:flex;align-items:center;gap:13px;padding:10px 12px;border-radius:16px;text-decoration:none!important;color:var(--navy)!important;transition:background .2s,transform .2s;animation:tvpMIn .5s both}
.tvp-menu a+a{margin-top:2px}.tvp-menu a:hover{background:#eef4ff;transform:translateX(4px)}
.tvp-menu a span{flex:none;width:42px;height:42px;border-radius:13px;display:flex;align-items:center;justify-content:center;font-size:21px;background:#e9f1ff}
.tvp-menu a div{flex:1;min-width:0}.tvp-menu b{display:block;font-size:16px;line-height:1.25}.tvp-menu i{display:block;font-style:normal;font-size:13.5px;color:var(--mut);line-height:1.35}
.tvp-menu em{font-style:normal;font-weight:800;color:#9db3d3;transition:color .2s,transform .2s}.tvp-menu a:hover em{color:var(--blue);transform:translateX(3px)}
.tvp-menu a.tvp-m-hot{background:linear-gradient(120deg,#0b1f4b,#1d5fd1)}.tvp-menu a.tvp-m-hot b{color:#fff}.tvp-menu a.tvp-m-hot i{color:#bfe0ff}.tvp-menu a.tvp-m-hot span{background:rgba(255,255,255,.14)}.tvp-menu a.tvp-m-hot em{color:#f2c94c}
.tvp-menu a:nth-of-type(2){animation-delay:.06s}.tvp-menu a:nth-of-type(3){animation-delay:.12s}.tvp-menu a:nth-of-type(4){animation-delay:.18s}.tvp-menu a:nth-of-type(5){animation-delay:.24s}.tvp-menu a:nth-of-type(6){animation-delay:.3s}.tvp-menu a:nth-of-type(7){animation-delay:.36s}
.tvp-menu-f{margin:10px 6px 2px!important;padding-top:12px;border-top:1px solid #e6edf6;font-size:13.5px;font-weight:700;color:var(--navy);text-align:center}
@keyframes tvpMIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
section[id^="tvp-"]{scroll-margin-top:90px}
.tvp-vid{max-width:320px!important;margin:0 auto}.tvp-play{position:absolute;left:50%;top:50%;width:70px;height:70px;margin:-35px;border-radius:50%;background:rgba(255,255,255,.92);color:var(--blue);display:flex;align-items:center;justify-content:center;font-size:26px;padding-left:5px;box-shadow:0 18px 36px -12px rgba(9,30,66,.55)}
.tvp-vid-t{position:absolute;left:14px;bottom:14px;font-style:normal;font-size:12.5px;font-weight:800;color:#fff;background:rgba(9,30,66,.65);padding:5px 10px;border-radius:999px}
.tvp-orbit{position:relative;width:420px;height:420px;max-width:86%;aspect-ratio:1}
.tvp-core{position:absolute;inset:30%;border-radius:50%;background:linear-gradient(150deg,#0b1f4b,#1d4fa8);color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;box-shadow:0 30px 60px -24px rgba(9,30,66,.6),0 0 0 10px rgba(77,163,255,.15);animation:tvpPulse 4s ease-in-out infinite}
.tvp-core b{font-size:40px;letter-spacing:.02em}.tvp-core span{font-size:12px;color:#bfe0ff;line-height:1.3;margin-top:4px}
.tvp-ring{position:absolute;inset:0;border-radius:50%;border:2px dashed rgba(29,95,209,.25);animation:tvpSpin 40s linear infinite}
.tvp-ring i{position:absolute;width:86px;height:86px;margin:-43px;border-radius:24px;background:#fff;box-shadow:0 18px 40px -18px rgba(9,30,66,.45);display:flex;flex-direction:column;align-items:center;justify-content:center;font-style:normal;font-size:28px;animation:tvpSpin 40s linear infinite reverse}
.tvp-ring i em{font-style:normal;font-size:11.5px;font-weight:800;color:var(--navy);margin-top:4px}
.tvp-ring .o1{left:50%;top:0}.tvp-ring .o2{left:93.3%;top:25%}.tvp-ring .o3{left:93.3%;top:75%}.tvp-ring .o4{left:50%;top:100%}.tvp-ring .o5{left:6.7%;top:75%}.tvp-ring .o6{left:6.7%;top:25%}
.tvp-ring .o4{background:linear-gradient(150deg,#1d5fd1,#4da3ff)}.tvp-ring .o4 em{color:#fff}
@keyframes tvpSpin{to{transform:rotate(360deg)}}@keyframes tvpPulse{0%,100%{box-shadow:0 30px 60px -24px rgba(9,30,66,.6),0 0 0 10px rgba(77,163,255,.15)}50%{box-shadow:0 30px 60px -24px rgba(9,30,66,.6),0 0 0 22px rgba(77,163,255,.06)}}
.tvp-two{display:grid;grid-template-columns:1fr 1fr;gap:20px;max-width:1060px;margin:0 auto}
.tvp-path{display:block;text-decoration:none!important;color:inherit!important;padding:30px 28px;border-radius:24px;background:#fff;border:1px solid #dfe8f6;box-shadow:0 20px 44px -28px rgba(9,30,66,.4);transition:transform .25s,box-shadow .25s}
.tvp-path:hover{transform:translateY(-5px);box-shadow:0 28px 54px -26px rgba(9,30,66,.5)}
.tvp-path h3{margin:10px 0 8px!important;font-size:28px;color:var(--navy)}.tvp-path p{margin:0 0 14px!important;font-size:16px;line-height:1.6;color:var(--mut)}.tvp-path em{font-style:normal;font-weight:800;color:var(--blue)}
.tvp-tag{display:inline-block;font-size:12px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;padding:5px 11px;border-radius:999px;background:#e7f0ff;color:var(--blue)}
.tvp-dark{background:linear-gradient(150deg,#0b1f4b,#1a4596);border:0}.tvp-dark h3{color:#fff!important}.tvp-dark p{color:#d3e1f5!important}.tvp-dark em{color:#f2c94c!important}.tvp-dark .tvp-tag{background:rgba(255,255,255,.14);color:#bfe0ff}
.tvp-fomo-in{max-width:1060px;margin:0 auto;padding:44px 40px;border-radius:28px;background:radial-gradient(700px 300px at 85% 0%,rgba(77,163,255,.35),transparent 70%),linear-gradient(150deg,#081634,#0f2f6a);color:#d6e3f7;text-align:center}
.tvp-fomo-in .tvs-eyebrow{color:#8fc1ff!important}.tvp-fomo-in h2{color:#fff!important;font-size:40px;line-height:1.12;margin:0 0 14px!important}.tvp-fomo-in h2 span{color:#f2c94c}
.tvp-fomo-in>p{max-width:760px;margin:0 auto 24px!important;font-size:17px;line-height:1.6}
.tvp-vs{display:grid;grid-template-columns:1fr 1fr;gap:14px;max-width:760px;margin:0 auto 26px;text-align:left}
.tvp-vs>div{padding:18px 20px;border-radius:18px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12)}
.tvp-vs b{display:block;color:#fff;font-size:16px;margin-bottom:8px}.tvp-vs span{display:block;font-size:15px;line-height:1.5;padding-left:24px;position:relative;margin:4px 0}
.tvp-vs>div:first-child span:before{content:"✕";position:absolute;left:0;color:#ff8a80;font-weight:800}
.tvp-vs-on{background:rgba(47,210,138,.12)!important;border-color:rgba(47,210,138,.4)!important}.tvp-vs-on span:before{content:"✓";position:absolute;left:0;color:#5ee0a0;font-weight:800}
.tvp-row-in{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center;max-width:1100px;margin:0 auto}
.tvp-flip .tvp-txt{order:2}
.tvp-row:nth-of-type(even){background:linear-gradient(180deg,#f3f7fd,#fff)}
.tvp-txt h2{margin:0 0 12px!important;font-size:38px;line-height:1.1;color:var(--navy);text-wrap:balance}.tvp-txt>p{font-size:17px;line-height:1.6;color:var(--mut);margin:0 0 16px!important}
.tvp-ul{list-style:none;margin:0 0 22px;padding:0;display:grid;gap:9px}.tvp-ul li{position:relative;padding-left:30px;font-size:15.5px;color:var(--navy);font-weight:600}
.tvp-ul li:before{content:"✓";position:absolute;left:0;top:1px;width:20px;height:20px;border-radius:50%;background:#e7f0ff;color:var(--blue);font-size:12px;font-weight:800;display:flex;align-items:center;justify-content:center}
.tvp-art{position:relative;display:flex;justify-content:center}
.tvp-stage{width:100%;max-width:420px;padding:24px;border-radius:24px;background:#fff;box-shadow:0 30px 60px -32px rgba(9,30,66,.5)}
.tvp-stage-card{position:relative;padding:20px;border-radius:18px;background:linear-gradient(150deg,#0b1f4b,#1d4fa8);color:#fff;animation:tvpFloat 5s ease-in-out infinite}
.tvp-stage-card b{display:block;font-size:22px}.tvp-stage-card i{font-style:normal;font-size:13.5px;color:#bfe0ff}
.tvp-vip{position:absolute;right:14px;top:14px;font-size:12px;font-weight:800;padding:4px 10px;border-radius:999px;background:#f2c94c;color:#3a2a00}
.tvp-sq{display:flex;align-items:center;gap:10px;padding:11px 16px;margin-bottom:14px;border-radius:999px;background:#f1f5fb;border:1px solid #e1e9f4;font-size:14.5px;font-weight:700;color:var(--navy)}
.tvp-sq span{font-size:15px}.tvp-sq em{margin-left:auto;font-style:normal;font-size:12.5px;font-weight:700;color:var(--mut)}
.tvp-sc-row{display:flex;align-items:center;gap:8px;margin-top:14px;flex-wrap:wrap}.tvp-sc-row em{font-style:normal;font-size:13px;font-weight:800;color:#f2c94c;margin-right:auto}
.tvp-sc-row u{text-decoration:none;font-size:12.5px;font-weight:800;padding:6px 12px;border-radius:999px;background:rgba(255,255,255,.14);color:#fff}.tvp-sc-row u:first-of-type{background:#fff;color:var(--navy)}
.tvp-res{display:flex;align-items:center;gap:12px;margin-top:10px;padding:11px 14px;border-radius:14px;background:#f6f8fb;border:1px solid #edf1f6}
.tvp-res div{flex:1;min-width:0}.tvp-res b{display:block;font-size:14.5px;color:#7a8696}.tvp-res i{display:block;font-style:normal;font-size:12.5px;color:#a3adba}
.tvp-av{flex:none;width:34px;height:34px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:800;background:#e3e9f1;color:#9aa6b6}
.tvp-res-f{background:#fff;border-color:#cfe0fb;box-shadow:0 10px 24px -16px rgba(29,95,209,.45)}.tvp-res-f b{color:var(--navy)}.tvp-res-f i{color:#c99a1a}.tvp-res-f .tvp-av{background:linear-gradient(135deg,#1d5fd1,#4da3ff);color:#fff}
.tvp-badge{font-style:normal;font-size:11.5px;font-weight:800;letter-spacing:.04em;padding:4px 10px;border-radius:999px;background:#e7f0ff;color:var(--blue)}
.tvp-res-2{opacity:.55}
.tvp-stage-list u{display:block;height:46px;border-radius:12px;background:#f1f5fa;margin-top:10px}.tvp-stage-list u:nth-child(2){width:86%}.tvp-stage-list u:nth-child(3){width:70%}
.tvp-cap{margin:14px 0 0!important;text-align:center;font-size:13px;color:var(--mut)}
.tvp-fan{position:relative;width:100%;max-width:460px;height:400px}
.tvp-fan img{position:absolute;top:20px;width:56%!important;height:auto!important;border-radius:16px;box-shadow:0 26px 50px -22px rgba(9,30,66,.55);transition:transform .4s}
.tvp-fan img:nth-child(1){left:0;transform:rotate(-8deg)}.tvp-fan img:nth-child(2){left:22%;top:0;z-index:2}.tvp-fan img:nth-child(3){right:0;transform:rotate(8deg)}
.tvp-fan:hover img:nth-child(1){transform:rotate(-12deg) translateX(-16px)}.tvp-fan:hover img:nth-child(3){transform:rotate(12deg) translateX(16px)}
.tvp-phone{position:relative;width:250px;padding:12px;border-radius:40px;background:#0b1220;box-shadow:0 40px 70px -30px rgba(9,30,66,.65)}
.tvp-phone img{display:block;width:100%!important;height:auto!important;border-radius:30px}
.tvp-push{position:absolute;left:-50px;top:70px;width:250px;padding:12px 14px;border-radius:16px;background:rgba(255,255,255,.97);box-shadow:0 20px 40px -16px rgba(9,30,66,.5);font-size:13px;line-height:1.35;color:#3c4a5e;animation:tvpPush 6s ease-in-out infinite}
.tvp-push b{display:block;color:var(--navy);font-size:13.5px}
.tvp-browser{position:relative;width:100%;max-width:460px;border-radius:18px;background:#fff;box-shadow:0 30px 60px -30px rgba(9,30,66,.5);overflow:hidden}
.tvp-bar{display:flex;gap:6px;align-items:center;padding:10px 14px;background:#eef2f7}.tvp-bar i{width:9px;height:9px;border-radius:50%;background:#d3dbe6}.tvp-bar i:first-child{background:#ff7b6b}.tvp-bar i:nth-child(2){background:#ffc85a}.tvp-bar i:nth-child(3){background:#4bd18a}
.tvp-bar span{margin-left:10px;flex:1;padding:4px 12px;border-radius:999px;background:#fff;font-size:12px;color:#7a8696}
.tvp-ai-tag{position:absolute;right:14px;bottom:14px;padding:8px 13px;border-radius:999px;background:linear-gradient(135deg,#1d5fd1,#4da3ff);color:#fff;font-size:13px;font-weight:800;animation:tvpFloat 4s ease-in-out infinite}
.tvp-chat{width:100%;max-width:360px;padding:0 0 16px;border-radius:22px;background:#f5f8fc;box-shadow:0 30px 60px -30px rgba(9,30,66,.5);overflow:hidden}
.tvp-chat-h{padding:14px 16px;background:linear-gradient(135deg,#0b1f4b,#1d4fa8);color:#fff;font-weight:800;margin-bottom:12px}
.tvp-chat p{max-width:80%;margin:0 14px 10px!important;padding:10px 13px;border-radius:16px;background:#fff;border:1px solid #e1e8f2;font-size:14.5px;line-height:1.45;color:#1d2b3a}
.tvp-chat p.me{margin-left:auto!important;background:var(--blue);border-color:var(--blue);color:#fff}
.tvp-lead{margin:4px 14px 0;padding:10px 12px;border-radius:14px;background:#eafaf2;border:1px solid #bfe9d3;color:#14553a;font-size:13.5px;font-weight:800;animation:tvpPush 5s ease-in-out infinite}
.tvp-drone{position:relative;width:100%;max-width:480px}.tvp-drone img{display:block;width:100%!important;height:auto!important;border-radius:22px;box-shadow:0 30px 60px -30px rgba(9,30,66,.55)}
.tvp-drone .tvp-faa{position:absolute;left:-18px;bottom:-18px;width:96px!important;border-radius:50%;box-shadow:0 16px 30px -12px rgba(9,30,66,.5);animation:tvpFloat 5s ease-in-out infinite}
.tvp-mail{width:100%;max-width:380px;border-radius:18px;background:#fff;box-shadow:0 30px 60px -30px rgba(9,30,66,.5);overflow:hidden}
.tvp-mail-h{padding:14px 18px;background:#0f2a52;color:#fff;font-weight:800}.tvp-mail-b{padding:18px}
.tvp-mail-f{margin:14px 0;padding:10px 12px;border-radius:12px;background:#fff7e0;border:1px solid #f2d58a;font-size:13.5px;font-weight:800;color:#6b4e00}
.tvp-flow{list-style:none;margin:0 auto 26px;padding:0;display:grid;grid-template-columns:repeat(4,1fr);gap:14px;max-width:1100px}
.tvp-flow li{position:relative;padding:22px 20px;border-radius:20px;background:#fff;border:1px solid #dfe8f6;font-size:14.5px;line-height:1.5;color:var(--mut)}
.tvp-flow b{display:inline-flex;width:30px;height:30px;border-radius:50%;align-items:center;justify-content:center;background:var(--blue);color:#fff;font-size:14px;margin-bottom:8px}
.tvp-flow em{display:block;font-style:normal;font-weight:800;color:var(--navy);font-size:17px;margin-bottom:4px}
.tvp-flow.tvs-in li{animation:tvpIn .55s ease both}.tvp-flow.tvs-in li:nth-child(2){animation-delay:.15s}.tvp-flow.tvs-in li:nth-child(3){animation-delay:.3s}.tvp-flow.tvs-in li:nth-child(4){animation-delay:.45s}
.tvp-why{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;max-width:1100px;margin:0 auto}
.tvp-why>div{padding:22px;border-radius:20px;background:linear-gradient(180deg,#f6f9ff,#fff);border:1px solid #dfe8f6;font-size:15px;line-height:1.55;color:var(--mut)}.tvp-why b{display:block;color:var(--navy);font-size:17px;margin-bottom:6px}
@keyframes tvpFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
@keyframes tvpPush{0%,10%{opacity:0;transform:translateY(-10px)}18%,82%{opacity:1;transform:none}92%,100%{opacity:0;transform:translateY(-10px)}}
@keyframes tvpIn{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
.tvp-top{margin:12px 0 0;padding:56px 40px 46px;border-radius:28px;background:radial-gradient(700px 360px at 85% -10%,rgba(77,163,255,.22),transparent 70%),radial-gradient(520px 300px at 0% 110%,rgba(45,240,200,.10),transparent 70%),linear-gradient(180deg,#f6f9ff,#fff 70%)}
.tvp-top-in{max-width:860px;margin:0 auto;text-align:center}
.tvp-top h1{font-size:54px;line-height:1.05;font-weight:800;margin:0 0 18px!important;text-wrap:balance}
.tvp-top h1 span{background:linear-gradient(90deg,var(--blue),var(--blue2));-webkit-background-clip:text;background-clip:text;color:transparent}
.tvp-lede{font-size:20px;line-height:1.6;color:#3c4a5e;max-width:760px;margin:0 auto 24px!important}.tvp-lede b{color:var(--navy)}
.tvp-trust{justify-content:center;margin:0 0 38px!important}
.tvp-glance{display:grid;grid-template-columns:1fr 1fr;gap:22px;max-width:1080px;margin:0 auto}
.tvp-gcol{box-sizing:border-box;padding:24px 20px 18px;border-radius:26px;background:#fff;border:1px solid #dfe8f6;box-shadow:0 30px 60px -36px rgba(9,30,66,.45);text-align:left}
.tvp-gh{padding:0 8px 12px;margin-bottom:6px;border-bottom:1px solid #e6edf6}
.tvp-gh p{margin:0 0 4px!important;font-size:12.5px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--blue)}
.tvp-gh h2{font-size:23px!important;line-height:1.2;color:var(--navy)}
.tvp-gcol a{display:flex;align-items:center;gap:14px;padding:11px 10px;border-radius:16px;text-decoration:none!important;color:var(--navy)!important;transition:background .2s,transform .2s}
.tvp-gcol a:hover{background:#eef4ff;transform:translateX(4px)}
.tvp-gcol a span{flex:none;width:46px;height:46px;border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:22px;background:#e9f1ff}
.tvp-gcol a div{flex:1;min-width:0}.tvp-gcol b{display:block;font-size:17px;line-height:1.25}.tvp-gcol i{display:block;font-style:normal;font-size:14px;color:var(--mut);line-height:1.4;margin-top:2px}
.tvp-gcol em{font-style:normal;font-weight:800;color:#9db3d3;transition:color .2s,transform .2s}.tvp-gcol a:hover em{color:var(--blue);transform:translateX(3px)}
.tvp-gdark{background:radial-gradient(520px 260px at 90% 0%,rgba(77,163,255,.32),transparent 70%),linear-gradient(155deg,#0b1f4b,#173f8f);border:0;box-shadow:0 34px 70px -34px rgba(9,30,66,.7)}
.tvp-gdark .tvp-gh{border-color:rgba(255,255,255,.14)}.tvp-gdark .tvp-gh p{color:#f2c94c}.tvp-gdark .tvp-gh h2{color:#fff!important}
.tvp-gdark a{color:#fff!important}.tvp-gdark a:hover{background:rgba(255,255,255,.08)}.tvp-gdark a span{background:rgba(255,255,255,.12)}.tvp-gdark i{color:#bfd4f2}.tvp-gdark em{color:#7fa6dc}.tvp-gdark a:hover em{color:#f2c94c}
.tvp-gfoot{text-align:center;margin-top:28px}.tvp-gfoot p{margin:0 0 14px!important;font-weight:800;color:var(--navy);font-size:17px}.tvp-gfoot .tvs-ctas{justify-content:center}
@media (max-width:900px){.tvp-top{padding:34px 16px 30px;border-radius:22px}.tvp-top h1{font-size:36px}.tvp-lede{font-size:17.5px}.tvp-glance{grid-template-columns:1fr;gap:16px}.tvp-gcol{padding:18px 12px 12px}.tvp-gh h2{font-size:20px!important}.tvp-gcol b{font-size:16px}}
@media (max-width:420px){.tvp-top h1{font-size:31px}.tvp-trust{gap:16px!important}.tvp-gcol a{gap:11px;padding:10px 6px}.tvp-gcol a span{width:40px;height:40px;font-size:19px}}
.tvp-soc{width:100%;max-width:470px;display:flex;flex-direction:column;align-items:center;gap:18px}.tvp-soc .tvp-fan{height:290px}
.tvp-reach{box-sizing:border-box;width:100%;padding:18px 20px;border-radius:22px;background:#fff;border:1px solid #dfe8f6;box-shadow:0 26px 50px -30px rgba(9,30,66,.45);position:relative;z-index:3}
.tvp-reach-n{display:flex;align-items:baseline;gap:10px;margin-bottom:12px}.tvp-reach-n b{font-size:32px;line-height:1;color:var(--navy);letter-spacing:-.02em}.tvp-reach-n span{font-size:14.5px;font-weight:700;color:var(--mut)}
.tvp-plats{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px}.tvp-plats span{display:inline-flex;align-items:center;gap:7px;padding:7px 12px 7px 8px;border-radius:999px;background:#f3f6fb;border:1px solid #e3e9f2;font-size:13.5px;font-weight:800;color:var(--navy)}.tvp-plats svg{width:20px;height:20px;flex:none}
.tvp-reach-t{display:flex;gap:6px 14px;flex-wrap:wrap}.tvp-reach-t i{font-style:normal;font-size:13px;font-weight:700;color:var(--ok)}
.tvp-browser{overflow:visible!important}.tvp-browser .tvp-bar{border-radius:18px 18px 0 0}
.tvp-browser .tvp-site{padding:0!important;border-radius:0 0 18px 18px;overflow:hidden}
.tvp-snav{display:flex;align-items:center;gap:12px;padding:12px 16px;border-bottom:1px solid #eef2f7;font-size:12px;color:#6b7788}.tvp-snav b{font-size:15px!important;height:auto!important;width:auto!important;background:none!important;margin:0 auto 0 0!important;color:#3b2a1a;font-family:Georgia,serif}.tvp-snav em{font-style:normal;font-weight:800;color:#fff;background:#b5652b;padding:5px 10px;border-radius:999px}
.tvp-shero{display:grid!important;grid-template-columns:1.15fr 1fr;gap:12px;align-items:center;padding:18px 16px 10px;margin:0!important;background:linear-gradient(160deg,#fff8ef,#fff)}
.tvp-site .tvp-shero p{height:auto!important;background:none!important;border-radius:0!important}
.tvp-sk{margin:0 0 6px!important;font-size:10.5px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:#b5652b}.tvp-sh{margin:0 0 10px!important;font-family:Georgia,serif;font-size:21px;line-height:1.15;color:#2e1f12;font-weight:700}
.tvp-sbtn{display:flex;gap:6px;margin:0 0 10px!important}.tvp-sbtn i,.tvp-sbtn u{font-style:normal;text-decoration:none;font-size:11.5px;font-weight:800;padding:6px 10px;border-radius:999px}.tvp-sbtn i{background:#2e1f12;color:#fff}.tvp-sbtn u{border:1px solid #e3d5c5;color:#2e1f12;height:auto!important;flex:none!important;background:none!important}
.tvp-sg{margin:0!important;font-size:11.5px;font-weight:700;color:#5b6b7c}.tvp-sg b{display:inline-flex!important;width:16px!important;height:16px!important;margin:0!important;border-radius:50%!important;align-items:center;justify-content:center;background:#fff!important;border:1px solid #e3e9f1;color:#4285F4;font-size:10px}.tvp-sg em{font-style:normal;color:#f5a623}
.tvp-simg{display:block!important;margin:0!important}.tvp-simg img{display:block;width:100%!important;height:auto!important;filter:drop-shadow(0 14px 18px rgba(80,40,10,.25))}
.tvp-srow{display:grid!important;grid-template-columns:repeat(3,1fr);gap:8px;padding:10px 16px 18px;margin:0!important}.tvp-srow div{padding:9px 10px;border-radius:12px;background:#f7f4f0;font-size:11px;color:#6b5a48;line-height:1.3}.tvp-srow b{display:block!important;width:auto!important;height:auto!important;background:none!important;margin:0!important;font-size:12px;color:#2e1f12}
.tvp-gpt{position:absolute;right:-18px;top:62px;max-width:210px;padding:11px 13px;border-radius:16px;background:#fff;box-shadow:0 22px 44px -18px rgba(9,30,66,.5);border:1px solid #e3e9f2;font-size:12.5px;line-height:1.4;color:#3c4a5e;animation:tvpFloat 5s ease-in-out infinite;z-index:2}.tvp-gpt b{display:block;font-size:11.5px;color:var(--blue);margin-bottom:3px}.tvp-gpt u{text-decoration:none;font-weight:800;color:var(--navy)}
.tvp-vids{display:flex;align-items:center;justify-content:center;gap:22px}.tvp-vids .tvp-reel{flex:1 1 0;min-width:0;max-width:330px}
.tvp-vph{position:relative;display:flex;flex:0 0 auto;flex-direction:column;align-items:center;gap:12px}
.tvp-vph-in{position:relative;width:230px;padding:11px;border-radius:44px;background:linear-gradient(145deg,#2a3346,#0b1220 55%);box-shadow:0 40px 70px -30px rgba(9,30,66,.7),inset 0 0 0 2px #39445c}
.tvp-vph-in .tvp-rv{display:block;width:100%!important;height:auto!important;aspect-ratio:9/16;object-fit:cover;border-radius:34px;background:#0b1220;cursor:pointer}
.tvp-vph-notch{position:absolute;left:50%;top:20px;transform:translateX(-50%);width:84px;height:22px;border-radius:12px;background:#05080f;z-index:2}
.tvp-vph .tvp-snd{top:52px;bottom:auto;right:50%;transform:translateX(50%);white-space:nowrap}
.tvp-vph .tvp-rtag{position:static;text-align:center;background:none;color:inherit}
.tvp-vph .tvp-rtag b{display:block;font-size:16px;color:#0f2742}.tvp-vph .tvp-rtag span{font-size:13px;color:#5b6b7c}
@media (max-width:760px){.tvp-vids{flex-direction:column;gap:30px}.tvp-vids .tvp-reel{width:100%;max-width:340px}.tvp-vph-in{width:250px}}
.tvp-reel{position:relative;width:100%;max-width:380px;border-radius:26px;overflow:hidden;background:#0b1220;box-shadow:0 40px 70px -30px rgba(9,30,66,.65),0 0 0 8px #fff,0 0 0 9px #dfe8f6}
.tvp-rv{display:block;width:100%!important;height:auto!important;aspect-ratio:4/5;object-fit:cover;background:#0b1220;cursor:pointer}
.tvp-snd{position:absolute;right:12px;top:12px;border:0;cursor:pointer;font:inherit;font-size:13px;font-weight:800;color:#fff;background:rgba(9,20,45,.68);padding:8px 12px;border-radius:999px}
.tvp-rtag{position:absolute;left:12px;bottom:12px;right:12px;padding:10px 14px;border-radius:14px;background:rgba(255,255,255,.94);pointer-events:none}.tvp-rtag b{display:block;font-size:15px;color:var(--navy)}.tvp-rtag span{font-size:12.5px;color:var(--mut)}
.tvp-mail-h{display:flex;align-items:baseline;justify-content:space-between;gap:10px}.tvp-mail-h span{font-size:12px;font-weight:700;color:#9fc3f2}
.tvp-mail-b .tvp-mk{height:auto!important;background:none!important;margin:0 0 10px!important;font-size:11.5px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--blue)}
.tvp-ev{display:flex;align-items:center;gap:12px;padding:8px 0;border-bottom:1px solid #eef2f7}.tvp-ev span{flex:none;width:44px;height:46px;border-radius:12px;background:#eef4ff;display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:17px;font-weight:800;color:var(--navy);line-height:1}.tvp-mail-b .tvp-ev span b{display:block;height:auto;width:auto;background:none;margin:0 0 3px;border-radius:0;font-size:9.5px;letter-spacing:.08em;color:var(--blue)}
.tvp-mail-b .tvp-ev div b{display:block;height:auto;background:none;margin:0;font-size:14.5px;color:var(--navy)}.tvp-ev div i{font-style:normal;font-size:12.5px;color:var(--mut)}
.tvp-feat{display:flex;gap:12px;margin:14px 0 12px;padding:10px;border-radius:16px;background:linear-gradient(135deg,#fff8e1,#fff);border:1px solid #f2d58a}
.tvp-feat img{flex:none;width:86px!important;height:96px!important;object-fit:cover;border-radius:12px}.tvp-feat div{min-width:0}.tvp-feat em{display:block;font-style:normal;font-size:11px;font-weight:800;color:#8a6500;letter-spacing:.04em}.tvp-mail-b .tvp-feat b{display:block;height:auto;background:none;margin:2px 0;font-size:16px;color:var(--navy)}.tvp-feat i{display:block;font-style:normal;font-size:12.5px;line-height:1.35;color:#5b6b7c;margin-bottom:6px}.tvp-feat u{text-decoration:none;font-size:12.5px;font-weight:800;color:var(--blue)}
.tvp-mfoot{font-size:12px;font-weight:700;color:var(--mut);text-align:center}
@media (max-width:900px){.tvp-gpt{right:-6px;top:auto;bottom:58px}.tvp-soc .tvp-fan{height:250px}}
@media (max-width:520px){.tvp-sh{font-size:16px}.tvp-snav span{display:none}.tvp-srow div{font-size:10px;padding:7px}.tvp-gpt{max-width:165px;font-size:11.5px;right:-4px}.tvp-soc .tvp-fan{height:200px}.tvp-reach-n b{font-size:27px}.tvp-reel{max-width:330px}.tvp-feat img{width:72px!important;height:84px!important}}
.tvp-have{margin-top:26px;padding:20px 18px 16px;border-radius:22px;background:linear-gradient(150deg,#0b1f4b,#1a4596);box-shadow:0 26px 50px -30px rgba(9,30,66,.6)}
.tvp-have-k{margin:0 0 2px!important;font-size:12px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:#f2c94c}
.tvp-have h3{margin:0 0 10px!important;font-size:21px!important;color:#fff!important;line-height:1.2}
.tvp-have a{display:flex;align-items:center;gap:12px;padding:10px;border-radius:14px;text-decoration:none!important;color:#fff!important;transition:background .2s}.tvp-have a:hover{background:rgba(255,255,255,.08)}
.tvp-have a span{flex:none;width:40px;height:40px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:19px;background:rgba(255,255,255,.12)}
.tvp-have a div{flex:1;min-width:0}.tvp-have b{display:block;font-size:16px}.tvp-have i{display:block;font-style:normal;font-size:13.5px;line-height:1.4;color:#c9dbf3}
.tvp-have em{font-style:normal;font-weight:800;color:#7fa6dc}.tvp-have a:hover em{color:#f2c94c}
.tvp-have-f{margin:8px 10px 0!important;padding-top:10px;border-top:1px solid rgba(255,255,255,.14);font-size:13.5px;font-weight:700;color:#bfe0ff}
.tvp-browser .tvp-ai-tag{bottom:-17px;right:18px;box-shadow:0 12px 24px -10px rgba(29,95,209,.6)}.tvp-browser{margin-bottom:18px}.tvp-browser .tvp-gpt{top:-34px;right:-26px}
.tvp-sbtn i,.tvp-sbtn u,.tvp-sk{white-space:nowrap}
@media (max-width:520px){.tvp-gpt{position:relative;right:auto;top:auto;bottom:auto;max-width:none;margin:12px 12px 30px;animation:none}.tvp-browser .tvp-gpt{top:auto;right:auto}.tvp-sk{font-size:9px;letter-spacing:.08em}.tvp-sbtn i,.tvp-sbtn u{font-size:10.5px;padding:5px 8px}.tvp-srow{grid-template-columns:1fr 1fr}.tvp-srow div:nth-child(3){display:none}.tvp-browser .tvp-ai-tag{font-size:12px;right:12px}}
.tvp-soc{gap:6px!important}.tvp-soc .tvp-fan{height:215px!important}.tvp-soc .tvp-reach{margin-top:12px}
.tvp-fan2 img:nth-child(1){left:2%;top:10px;transform:rotate(7deg)}.tvp-fan2 img:nth-child(2){left:22%;top:26px;z-index:2;transform:none}.tvp-fan2 img:nth-child(3){right:2%;top:10px;transform:rotate(-7deg)}
.tvp-fan2:hover img:nth-child(1){transform:rotate(11deg) translateX(-16px)}.tvp-fan2:hover img:nth-child(3){transform:rotate(-11deg) translateX(16px)}
@media (max-width:900px){.tvp-soc .tvp-fan{height:200px!important}}
@media (max-width:520px){.tvp-soc .tvp-fan{height:150px!important}.tvp-fan2 img:nth-child(2){top:16px}}
.tvp-ctas{display:flex;flex-wrap:wrap;gap:12px;align-items:center}.tvp-ctas-c{justify-content:center;margin-top:26px}
.tvp-ai{max-width:1000px;margin:-14px auto 34px;text-align:center}.tvp-ai>p{margin:0 0 14px!important;font-size:13px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--mut)}
.tvp-ai .tvw-logo{box-shadow:0 8px 20px -12px rgba(9,30,66,.35)}
.tvp-get{list-style:none;margin:0 0 18px!important;padding:0;display:grid;gap:8px}.tvp-get li{position:relative;padding-left:30px;font-weight:700;color:var(--navy);font-size:16px}
.tvp-get li:before{content:"✓";position:absolute;left:0;top:1px;width:21px;height:21px;border-radius:50%;background:#e3f7ee;color:#0d7760;font-size:12px;font-weight:800;display:flex;align-items:center;justify-content:center}
.tvp-proof{margin:6px 0 16px;padding:16px 18px;border-radius:18px;background:#fff;border:1px solid #e3e9f1;box-shadow:0 16px 34px -24px rgba(9,30,66,.35)}
.tvp-proof-h{display:flex;align-items:center;gap:8px;margin-bottom:8px}.tvp-proof-h b{font-size:22px;color:var(--navy)}.tvp-proof-h span{color:#f5a623;letter-spacing:1px}.tvp-proof-h em{font-style:normal;font-size:13px;font-weight:700;color:var(--mut)}
.tvp-proof blockquote{margin:10px 0 0!important;padding:0 0 0 12px!important;border-left:3px solid #ffc53d;font-size:14.5px;line-height:1.5;color:#3c4a5e;font-style:normal}.tvp-proof cite{display:block;margin-top:3px;font-style:normal;font-size:12.5px;font-weight:800;color:var(--navy)}
.tvp-alt{font-size:14.5px!important;color:var(--mut)}.tvp-alt a{font-weight:800;color:var(--blue)!important}
.tvp-aicheck{display:flex;align-items:center;gap:14px;max-width:640px;margin:22px auto 0;padding:14px 18px;border-radius:18px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.22);text-decoration:none!important;color:#fff!important;text-align:left;transition:background .2s}
.tvp-aicheck:hover{background:rgba(255,255,255,.14)}.tvp-aicheck span{font-size:26px}.tvp-aicheck div{flex:1;min-width:0}.tvp-aicheck b{display:block;font-size:16.5px}.tvp-aicheck i{display:block;font-style:normal;font-size:13.5px;color:#bfd4f2}.tvp-aicheck em{font-style:normal;font-weight:800;color:#f2c94c;white-space:nowrap}
details.tvp-more{margin:4px 0 12px;border:1px dashed #cdd8e6;border-radius:14px;padding:10px 14px;background:#f8fafd}details.tvp-more summary{cursor:pointer;font-weight:800;color:var(--blue);font-size:15px}details.tvp-more[open] summary{margin-bottom:10px}
@media (max-width:520px){.tvp-aicheck{flex-wrap:wrap}.tvp-aicheck em{width:100%}}
@media (max-width:900px){.tvs-book{display:flex!important;flex-direction:column}.tvs-book .tvs-bside{display:contents}.tvs-book .tvs-bside>*{order:1}.tvs-book #tvs-form-slot{order:2;margin:6px 0 18px;width:100%;max-width:none;align-self:stretch;box-sizing:border-box}.tvs-book .tvp-proof,.tvs-book .tvp-alt,.tvs-book .tvs-direct{order:3}}
.tvs-sticky{right:auto!important;left:20px!important}
.tva-pop{width:360px!important}.tva-pop .tva-box{height:470px!important;max-height:calc(100vh - 130px)!important}
@media (max-width:900px){.tvs-hero.tvp-hero{display:flex;flex-direction:column}.tvp-vis{order:2;position:relative!important;width:auto!important;padding:22px 14px!important}.tvp-menu{padding:12px}.tvp-orbit{width:300px;height:300px}.tvp-ring i{width:66px;height:66px;margin:-33px;font-size:22px;border-radius:18px}.tvp-ring i em{font-size:10px}
.tvp-two,.tvp-vs,.tvp-row-in,.tvp-why{grid-template-columns:1fr}.tvp-flip .tvp-txt{order:0}.tvp-row-in{gap:30px}.tvp-txt h2{font-size:30px}.tvp-fomo-in{padding:32px 22px}.tvp-fomo-in h2{font-size:29px}.tvp-flow{grid-template-columns:1fr 1fr}
.tvp-fan{height:330px}.tvp-push{left:-20px}}
@media (max-width:520px){.tvp-flow{grid-template-columns:1fr}.tvp-fan{height:280px}.tvp-push{left:-10px;width:210px}.tva-pop{width:100%!important}.tva-pop .tva-box{height:100dvh!important;max-height:100dvh!important}}
@media (prefers-reduced-motion:reduce){.tvp-ring,.tvp-ring i,.tvp-core,.tvp-stage-card,.tvp-push,.tvp-ai-tag,.tvp-lead,.tvp-faa,.tvp-flow li{animation:none!important}}
'''

VJS = ''';(function(){document.querySelectorAll('.tvp-rv').forEach(function(v){var box=v.closest('.tvp-reel,.tvp-vph-in');var b=box&&box.querySelector('.tvp-snd');var on=false;
function go(){if(on)return;on=true;v.src=v.getAttribute('data-src');var p=v.play();if(p&&p.catch)p.catch(function(){});}
if('IntersectionObserver' in window){new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){if(!on){go();}else if(v.paused){v.play().catch(function(){});}}else if(on){v.pause();}});},{rootMargin:'250px 0px'}).observe(v);}else{go();}
function snd(){go();var turnOn=v.muted;document.querySelectorAll('.tvp-rv').forEach(function(o){if(o!==v&&!o.muted){o.muted=true;var ob=o.closest('.tvp-reel,.tvp-vph-in').querySelector('.tvp-snd');if(ob){ob.innerHTML='&#128263; Tap for sound';}}});v.muted=!turnOn?true:false;v.play().catch(function(){});if(b){b.innerHTML=v.muted?'&#128263; Tap for sound':'&#128266; Sound on';b.setAttribute('aria-label',v.muted?'Turn sound on':'Turn sound off');}if(window.gtag)gtag('event','promo_video_sound',{on:!v.muted,video:v.getAttribute('aria-label')});}
if(b)b.addEventListener('click',snd);v.addEventListener('click',snd);});})();'''
VJS2 = r''';(function(){
function slotTxt(a){var sec=a.closest('section');return sec&&sec.id?sec.id:(a.classList.contains('tvs-sticky')?'sticky':'other');}
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href="#tvs-book"],a[href="/free-ai-report"]');if(!a||!window.gtag)return;gtag('event',a.getAttribute('href')==='#tvs-book'?'services_cta':'services_aicheck',{label:(a.textContent||'').trim().slice(0,40),section:slotTxt(a)});},true);
var bk=document.getElementById('tvs-book'),st=document.querySelector('.tvs-sticky');if(bk&&st&&'IntersectionObserver' in window){new IntersectionObserver(function(es){st.style.opacity=es[0].isIntersecting?'0':'';st.style.pointerEvents=es[0].isIntersecting?'none':'';}).observe(bk);}
var tries=0;(function arrange(){var f=document.querySelector('#tvs-form-slot form');if(!f){if(++tries<40)setTimeout(arrange,250);return;}
 if(!f.querySelector('details.tvp-more')){var em=f.querySelector('[name=inquiry_email]');var g0=em&&em.closest('.form-group');var d=document.createElement('details');d.className='tvp-more';d.innerHTML='<summary>Tell us more (optional)</summary>';
  ['phone','bundle','member_tier','comments'].forEach(function(n){var el=f.querySelector('[name='+n+']');var g=el&&el.closest('.form-group');if(g)d.appendChild(g);});
  if(g0&&g0.parentNode)g0.parentNode.insertBefore(d,g0.nextSibling);}
 var started=false;f.addEventListener('focusin',function(){if(!started&&window.gtag){started=true;gtag('event','services_form_start');}});
 f.addEventListener('submit',function(){if(window.gtag)gtag('event','services_form_submit',{bundle:(f.querySelector('[name=bundle]')||{}).value||''});},true);
})();})();'''
_ard = A.rd


def rd(f):
    if f == "page.html":
        return HTML
    s = _ard(f)
    if f == "page.css":
        return s + CSS
    if f == "page.js":
        s = s.replace("Send my message", "Get My Free Plan").replace("s.value='web_consult';var g=s.closest('.form-group')||s.parentNode;g.style.display='none';", "if(!s.value||s.value==='web_consult')s.value='not_sure';")
        s = s + '<script>' + VJS + VJS2 + '</script>'
        return s.replace('widget.js" data-demo="1"', 'widget.js" data-tease="Want a quick free plan? Tell me your business name and I will point you to the right fit."').replace("var pick='ai_chat'", "var pick='not_sure'")
    return s


D.rd = rd
if __name__ == "__main__":
    D.main()
