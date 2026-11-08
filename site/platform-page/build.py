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
D.SLUG = "our-services" if D.LIVE else "preview-our-services"
D.TITLE = "Our Services: Local Marketing, AI Websites, AI Assistants and Video | Three Village Local"
D.DESC = ("Three Village Local connects local businesses with the community: our website, mobile app, social media and email, "
          "plus AI websites, AI assistants, AI optimization and video. Launch a new business or give yours an AI overhaul.")
D.FB_TITLE = "We connect local businesses with the community."

AI = "/ai-assistant"
SH = "https://threevillagelocal-cloud.github.io/3vl-share/site/"
APP = "https://cdn.jsdelivr.net/gh/threevillagelocal-cloud/3vl-assets@1328a06c9ca8ab841e46fd8b85170aaef3bd1e63/site/app/"

HERO = """<section class="tvp-top" id="tvp-top">
  <div class="tvp-top-in tvs-up">
    <p class="tvs-kick"><span class="tvs-dot"></span>Our services</p>
    <h1>You know us for promoting local businesses.<br><span>That&#39;s just the beginning.</span></h1>
    <p class="tvp-lede">Every day, our <b>website</b>, free <b>mobile app</b> and <b>social media</b> put local businesses in front of the whole Three Village community. We also offer the modern tools that help a business get seen, get chosen and grow, all from one local team.</p>
    <ul class="tvs-trust tvp-trust"><li><b>45,000+</b>website page visits a month</li><li><b>100,000+</b>social views a month</li><li><b>One</b>local team</li></ul>
  </div>
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
    <a class="tvs-btn tvw-btn-w" href="''' + AI + '''">See the AI overhaul</a>
  </div>
</section>'''


def row(i, eyebrow, title, text, bullets, cta, href, visual, flip=False):
    li = "".join("<li>%s</li>" % b for b in bullets)
    return '''<section class="tvs-sec tvp-row%s" id="tvp-%s">
  <div class="tvp-row-in">
    <div class="tvp-txt tvs-up"><p class="tvs-eyebrow">%s</p><h2>%s</h2><p>%s</p><ul class="tvp-ul">%s</ul><a class="tvs-btn tvs-blue" href="%s">%s</a></div>
    <div class="tvp-art tvs-up">%s</div>
  </div>
</section>''' % (" tvp-flip" if flip else "", i, eyebrow, title, text, li, href, cta, visual)


V_STAGE = '''<div class="tvp-stage"><div class="tvp-stage-card"><span class="tvp-vip">&#9733; VIP</span><b>Your Business</b><i>Top of search &middot; one-tap call</i></div>
  <div class="tvp-stage-list"><u></u><u></u><u></u></div><p class="tvp-cap">Top spots, homepage features, banners and spotlights</p></div>'''
V_SOCIAL = '''<div class="tvp-fan"><img src="''' + SH + '''services/w-tommys-place-v2.webp" alt="Social post for Tommy's Place" loading="lazy" width="320" height="400">
  <img src="''' + SH + '''services/w-namkeen-hot-chicken-v1.webp" alt="Social post for Namkeen Hot Chicken" loading="lazy" width="320" height="400">
  <img src="''' + SH + '''services/w-savera-wood-floor-refinishing-v1.webp" alt="Social post for Savera Wood Floor Refinishing" loading="lazy" width="320" height="400"></div>'''
V_APP = '''<div class="tvp-phone"><img src="''' + APP + '''screen.webp" alt="The Three Village Local mobile app" loading="lazy" width="300" height="620"><div class="tvp-push"><b>Three Village Local</b>&#127881; This weekend only at Your Business...</div></div>'''
V_WEB = '''<div class="tvp-browser"><div class="tvp-bar"><i></i><i></i><i></i><span>yourbusiness.com</span></div><div class="tvp-site"><b></b><p></p><p class="s"></p><div><u></u><u></u></div></div>
  <div class="tvp-ai-tag">&#10022; Read and recommended by AI</div></div>'''
V_BOT = '''<div class="tvp-chat"><div class="tvp-chat-h">&#10022; Your Business Front Desk</div><p class="me">Are you open Sunday?</p><p>Yes, 10 to 4! Want me to book you a time?</p><p class="me">Yes, Sarah, 631-555-0188</p><div class="tvp-lead">&#128241; New lead sent to you</div></div>'''
V_VIDEO = '''<div class="tvp-drone tvp-vid"><img src="''' + SH + '''services/w-tommys-place-v2.webp" alt="Promo video for Tommy's Place" loading="lazy" width="320" height="400"><b class="tvp-play">&#9654;</b><i class="tvp-vid-t">0:15 &middot; Promo reel</i></div>'''
V_EMAIL = '''<div class="tvp-mail"><div class="tvp-mail-h">Three Village Weekly</div><div class="tvp-mail-b"><b></b><p></p><p class="s"></p><div class="tvp-mail-f">&#9733; Featured: Your Business</div><p></p></div></div>'''

ROWS = "\n\n".join([
    row("seen", "Get seen on Three Village Local", "Be the first name neighbors see.",
        "Featured and VIP memberships put your business at the top of our directory, on our homepage and across the site, where locals already go to find who to call.",
        ["Top-of-search placement with one-tap call", "Homepage features, banners and spotlights", "Post your events and specials on the site and mobile app"],
        "See memberships", "/join", V_STAGE),
    row("social", "Social media promotion", "Seen all over town, every week.",
        "We create scroll-stopping posts and reels for your business and share them with more than 100,000 local views a month on Facebook and Instagram.",
        ["Custom graphics and reels, made for you", "Tagged and shared with your own accounts", "Launch posts, specials, events and spotlights"],
        "Ask about social promotion", "#tvs-book", V_SOCIAL, True),
    row("app", "The Three Village Local mobile app", "Right on their phones.",
        "Our free mobile app keeps neighbors connected to local businesses, events and specials. VIP members can send a push notification straight to local phones.",
        ["Your listing, specials and events in the mobile app", "Push notifications to local phones (VIP)", "Free for the community on iPhone and Android"],
        "See the mobile app", "/app", V_APP),
    row("web", "AI-Ready websites", "A website AI can read, and customers love.",
        "We design, build and host a fast, beautiful website written so Google and AI tools understand exactly what you do, then we launch it to the whole town.",
        ["Designed, written and hosted for you", "Built for Google and AI search from the first line", "Domain in your name, updates included"],
        "See AI websites", "/websites", V_WEB, True),
    row("bot", "Your Digital Front Desk", "Your best salesperson, open 24/7.",
        "A smart AI assistant on your current website answers customers in seconds, day or night, and sends you every lead. It comes with AI Website Optimization so you get noticed and recommended by AI.",
        ["Works with the website you already have", "Live person handoff: you get an instant text", "Follows your industry's rules and guidelines"],
        "Try the live demo", AI, V_BOT),
    row("video", "Promo video", "Show them, don&#39;t just tell them.",
        "Short promo videos and reels that make your business look its best, shared across our site, social media and mobile app.",
        ["Filmed, edited and captioned for you", "Sized for Instagram, Facebook and your website", "Included with VIP, discounted for Featured members"],
        "Ask about promo video", "#tvs-book", V_VIDEO, True),
    row("email", "Email and articles", "Stories the community actually reads.",
        "Get featured in our weekly email and in custom articles on Three Village Local, so neighbors learn the story behind your business.",
        ["Spotlights in our weekly email", "Custom blog and article features", "Shared across social and the mobile app"],
        "Get featured", "#tvs-book", V_EMAIL),
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
</section>'''

CTA = '''<section class="tvw-cta3 tvs-up"><div class="tvw-cta3-in"><p class="tvw-cta3-k">Your competition isn&#39;t waiting</p><h2>Let&#39;s build your plan.</h2>
<p class="tvw-cta3-s">Tell us about your business and we&#39;ll send you a free, no-pressure plan by email.</p>
<div class="tvw-cta-btns"><a class="tvs-btn tvw-btn-w" href="#tvs-book">Send us a message</a><a class="tvs-btn tvw-btn-o" href="''' + AI + '''">Try the Digital Front Desk</a></div></div></section>'''

i, j = sec(A.HTML, "tvs-sec tvs-book")
BOOK = A.HTML[i:j].replace("mailto:hello@threevillagelocal.com?subject=AI%20for%20my%20website", "mailto:hello@threevillagelocal.com?subject=Our%20services")
HTML = ('<div class="tvs" id="tvs">\n\n' + HERO + "\n\n" + FOMO + "\n\n" + ROWS + "\n\n" + LAUNCH + "\n\n" + VS + "\n\n" + CTA + "\n\n" + BOOK +
        '\n\n<a class="tvs-sticky" href="#tvs-book">Send us a message</a>\n</div>')
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
.tvp-txt h2{margin:0 0 12px!important;font-size:38px;line-height:1.1;color:var(--navy)}.tvp-txt>p{font-size:17px;line-height:1.6;color:var(--mut);margin:0 0 16px!important}
.tvp-ul{list-style:none;margin:0 0 22px;padding:0;display:grid;gap:9px}.tvp-ul li{position:relative;padding-left:30px;font-size:15.5px;color:var(--navy);font-weight:600}
.tvp-ul li:before{content:"✓";position:absolute;left:0;top:1px;width:20px;height:20px;border-radius:50%;background:#e7f0ff;color:var(--blue);font-size:12px;font-weight:800;display:flex;align-items:center;justify-content:center}
.tvp-art{position:relative;display:flex;justify-content:center}
.tvp-stage{width:100%;max-width:420px;padding:24px;border-radius:24px;background:#fff;box-shadow:0 30px 60px -32px rgba(9,30,66,.5)}
.tvp-stage-card{position:relative;padding:20px;border-radius:18px;background:linear-gradient(150deg,#0b1f4b,#1d4fa8);color:#fff;animation:tvpFloat 5s ease-in-out infinite}
.tvp-stage-card b{display:block;font-size:22px}.tvp-stage-card i{font-style:normal;font-size:13.5px;color:#bfe0ff}
.tvp-vip{position:absolute;right:14px;top:14px;font-size:12px;font-weight:800;padding:4px 10px;border-radius:999px;background:#f2c94c;color:#3a2a00}
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
.tvp-site{padding:22px}.tvp-site b{display:block;width:60%;height:20px;border-radius:6px;background:#dbe5f3;margin-bottom:14px}.tvp-site p{height:10px;border-radius:5px;background:#edf1f6;margin:0 0 10px!important}.tvp-site p.s{width:65%}
.tvp-site div{display:flex;gap:10px;margin-top:16px}.tvp-site u{flex:1;height:90px;border-radius:12px;background:#f1f5fa}
.tvp-ai-tag{position:absolute;right:14px;bottom:14px;padding:8px 13px;border-radius:999px;background:linear-gradient(135deg,#1d5fd1,#4da3ff);color:#fff;font-size:13px;font-weight:800;animation:tvpFloat 4s ease-in-out infinite}
.tvp-chat{width:100%;max-width:360px;padding:0 0 16px;border-radius:22px;background:#f5f8fc;box-shadow:0 30px 60px -30px rgba(9,30,66,.5);overflow:hidden}
.tvp-chat-h{padding:14px 16px;background:linear-gradient(135deg,#0b1f4b,#1d4fa8);color:#fff;font-weight:800;margin-bottom:12px}
.tvp-chat p{max-width:80%;margin:0 14px 10px!important;padding:10px 13px;border-radius:16px;background:#fff;border:1px solid #e1e8f2;font-size:14.5px;line-height:1.45;color:#1d2b3a}
.tvp-chat p.me{margin-left:auto!important;background:var(--blue);border-color:var(--blue);color:#fff}
.tvp-lead{margin:4px 14px 0;padding:10px 12px;border-radius:14px;background:#eafaf2;border:1px solid #bfe9d3;color:#14553a;font-size:13.5px;font-weight:800;animation:tvpPush 5s ease-in-out infinite}
.tvp-drone{position:relative;width:100%;max-width:480px}.tvp-drone img{display:block;width:100%!important;height:auto!important;border-radius:22px;box-shadow:0 30px 60px -30px rgba(9,30,66,.55)}
.tvp-drone .tvp-faa{position:absolute;left:-18px;bottom:-18px;width:96px!important;border-radius:50%;box-shadow:0 16px 30px -12px rgba(9,30,66,.5);animation:tvpFloat 5s ease-in-out infinite}
.tvp-mail{width:100%;max-width:380px;border-radius:18px;background:#fff;box-shadow:0 30px 60px -30px rgba(9,30,66,.5);overflow:hidden}
.tvp-mail-h{padding:14px 18px;background:#0f2a52;color:#fff;font-weight:800}.tvp-mail-b{padding:18px}.tvp-mail-b b{display:block;height:120px;border-radius:12px;background:linear-gradient(135deg,#dbe8fb,#f3f7fd);margin-bottom:14px}
.tvp-mail-b p{height:10px;border-radius:5px;background:#edf1f6;margin:0 0 10px!important}.tvp-mail-b p.s{width:60%}
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
.tvs-sticky{right:auto!important;left:20px!important}
.tva-pop{width:360px!important}.tva-pop .tva-box{height:470px!important;max-height:calc(100vh - 130px)!important}
@media (max-width:900px){.tvs-hero.tvp-hero{display:flex;flex-direction:column}.tvp-vis{order:2;position:relative!important;width:auto!important;padding:22px 14px!important}.tvp-menu{padding:12px}.tvp-orbit{width:300px;height:300px}.tvp-ring i{width:66px;height:66px;margin:-33px;font-size:22px;border-radius:18px}.tvp-ring i em{font-size:10px}
.tvp-two,.tvp-vs,.tvp-row-in,.tvp-why{grid-template-columns:1fr}.tvp-flip .tvp-txt{order:0}.tvp-row-in{gap:30px}.tvp-txt h2{font-size:30px}.tvp-fomo-in{padding:32px 22px}.tvp-fomo-in h2{font-size:29px}.tvp-flow{grid-template-columns:1fr 1fr}
.tvp-fan{height:330px}.tvp-push{left:-20px}}
@media (max-width:520px){.tvp-flow{grid-template-columns:1fr}.tvp-fan{height:280px}.tvp-push{left:-10px;width:210px}.tva-pop{width:100%!important}.tva-pop .tva-box{height:100dvh!important;max-height:100dvh!important}}
@media (prefers-reduced-motion:reduce){.tvp-ring,.tvp-ring i,.tvp-core,.tvp-stage-card,.tvp-push,.tvp-ai-tag,.tvp-lead,.tvp-faa,.tvp-flow li{animation:none!important}}
'''

_ard = A.rd


def rd(f):
    if f == "page.html":
        return HTML
    s = _ard(f)
    if f == "page.css":
        return s + CSS
    if f == "page.js":
        return s.replace('widget.js" data-demo="1"', 'widget.js" data-tease="Hi! I am live. Questions about growing your business? Ask me."').replace("var pick='ai_chat'", "var pick='not_sure'")
    return s


D.rd = rd
if __name__ == "__main__":
    D.main()
