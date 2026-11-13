"""AI chatbot sales page (Your Digital Front Desk), chatbot only. Same design system as the other service pages (svc-kit).
The real assistant runs inline in the hero in demo mode (widget.js data-mount + data-demo).
    python site/chatbot-page/build.py          -> widget "3VL Page Chatbot Preview" + hidden /preview-chatbot (noindex)
    python site/chatbot-page/build.py --dry    -> build only, print sizes
    (--live -> /chatbot needs TVX_LIVE_OK=1)"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "svc-kit"))
import kit as K
from kit import ic

# same numbers as the /ai-assistant page (site/ai-assistant-page/build.py CHAT)
SETUP, MONTHLY = 199, 39

# platform logo row, reused from the /ai-assistant page source
_src = open(os.path.join(HERE, "..", "ai-assistant-page", "build.py"), encoding="utf-8").read()
WORKS_ROW = re.search(r'<div class="tva-works tvs-up">.*?</div></div>', _src, re.S).group(0)

WIDGET = ('<script src="https://3vl-ai-assistant.vercel.app/widget.js" data-mount="#tvc-live" data-demo="1" '
          'data-hello="Hi! I&#39;m the Digital Front Desk, the same AI assistant we build for local business websites. '
          'Ask me anything, like how it would work for your business." defer></script>')

TRY = [("I run a pizzeria. What would it answer?", "utensils"), ("How do leads reach me?", "phone"), ("What does it cost?", "tag")]
try_btns = "".join('<button type="button" class="tvc-ask" data-q="%s">%s<span>%s</span></button>' % (q, ic(i), q) for q, i in TRY)

HERO = '''<section class="tvx-hero tvc-hero" id="tvx-hero">
  <div class="tvx-hin">
    <p class="tvx-crumbs"><a href="/services">Our services</a><span>/</span>AI chatbot</p>
    <h1>Answer every customer,<br><span>even when you&#39;re closed.</span></h1>
    <p class="tvx-sub">Your Digital Front Desk is a smart AI assistant for your website. It answers questions the second they come in, day or night, and sends you every lead. Built for local businesses and set up for you.</p>
    <div class="tvs-ctas tvx-ctas"><a class="tvs-btn tvs-blue" href="#tvs-book">Get started</a><a class="tvs-btn tvs-ghost" href="#tvp-price">See pricing</a></div>
    <ul class="tvx-trust"><li><b>24/7</b>answers for your customers</li><li><b>About 1 week</b>to go live</li><li><b>Every lead</b>sent to you</li></ul>
  </div>
  <div class="tvx-hvis tvc-hvis" data-run>
    <div class="tvc-try">
      <p class="tvc-k"><span></span>Live demo: chat with it now</p>
      <div class="tvc-glow"><div id="tvc-live"><div class="tvc-wait">Loading the live demo...</div></div></div>
      <div class="tvc-asks"><p>Try asking</p>''' + try_btns + '''</div>
    </div>
  </div>
</section>'''

NAV = K.snav([("why", "Why it matters"), ("examples", "Examples"), ("what", "What it does"), ("how", "How it works"), ("price", "Pricing"), ("faq", "FAQ")])

WHY = K.sec("why", "Why it matters", "The business that answers first usually wins.",
            "People shop at night and on weekends, and they reach out to more than one business. Your Digital Front Desk makes sure you are the one who answers, even at 10 PM on a Sunday.",
            K.cards([("clock", "Customers shop after hours", "Nights and weekends are when people finally have time to look. Your assistant is there when you can&#39;t pick up."),
                     ("bolt", "Speed wins the job", "People reach out to more than one business. The first one to answer is usually the one they hire."),
                     ("message", "Most visitors leave quietly", "Most people never call or fill out a form. A friendly &ldquo;Can I help?&rdquo; turns browsers into real leads.")]))

# ---------- example conversations (sample businesses, not real clients) ----------
EX = [
    ("restaurant", "utensils", "Restaurant", "Sample pizzeria", "Friday, 9:48 PM", [
        ("c", "Are you open the day before Thanksgiving? And do you do party trays?"),
        ("b", "Yes, we&#39;re open until 10 PM that night. We do half and full party trays: baked ziti, chicken parm, eggplant and more. How many people are you feeding?"),
        ("c", "About 25, for that Saturday."),
        ("b", "A full tray of two mains plus a salad usually covers 25. Want the manager to call and lock in your order? What&#39;s your name and best number?"),
        ("c", "Jen, 631-555-0142"),
    ], ["Holiday hours", "Catering menu and portions", "Took the catering order details"],
        [("Catering order", "Jen, about 25 people"), ("When", "Saturday after Thanksgiving"), ("Wants", "Party trays, call to confirm"), ("Phone", "631-555-0142")]),
    ("contractor", "hammer", "Contractor", "Sample remodeling company", "Sunday, 8:15 PM", [
        ("c", "Do you do kitchen remodels in Port Jefferson? Ours is from the 90s."),
        ("b", "Yes, we cover Port Jefferson and the whole North Shore. Full remodels: cabinets, counters, floors and lighting, starting with a free in-home estimate. Full gut or a refresh?"),
        ("c", "Probably a full gut. How soon could someone come look?"),
        ("b", "Estimates usually book within the week. I&#39;ll have the owner text you to pick a time. What&#39;s your name and number?"),
        ("c", "Mike, 631-555-0187"),
    ], ["Service area", "What a remodel includes", "Booked a free estimate request"],
        [("Free estimate", "Mike, Port Jefferson"), ("Project", "Full kitchen remodel"), ("Next step", "Text him to pick a time"), ("Phone", "631-555-0187")]),
    ("salon", "sparkle", "Salon and spa", "Sample hair salon", "Tuesday, 6:52 AM", [
        ("c", "Do you do balayage? Anything open Saturday?"),
        ("b", "We do! Balayage takes about 3 hours and includes a toner and blowout. You can see open times and book right here: <u>Book online</u>"),
        ("c", "Saturday looks full. Is there a waitlist?"),
        ("b", "There is. I can add you and the front desk will text you if a spot opens. What&#39;s your name and number?"),
        ("c", "Sara, 631-555-0119"),
    ], ["Services and timing", "Sent her to online booking", "Added her to the waitlist"],
        [("Waitlist", "Sara, new client"), ("Service", "Balayage"), ("When", "Saturday, any time"), ("Phone", "631-555-0119")]),
    ("realtor", "home", "Real estate", "Sample real estate office", "Saturday, 11:20 PM", [
        ("c", "Is the 3 bedroom colonial on your site still available? Can I see it this weekend?"),
        ("b", "It&#39;s still listed as active. Showings are by appointment, and the listing agent can set one up this weekend. Are you already working with an agent?"),
        ("c", "No agent yet. Sunday afternoon works."),
        ("b", "Perfect. I&#39;ll send this to the listing agent right now so they can confirm a Sunday time. What&#39;s your name and best number?"),
        ("c", "Chris, 631-555-0163"),
    ], ["Listing status", "Showing policy", "Showing request to the agent"],
        [("Showing request", "Chris, no agent yet"), ("Home", "3 bedroom colonial"), ("When", "Sunday afternoon"), ("Phone", "631-555-0163")]),
    ("pro", "briefcase", "Professional services", "Sample accounting firm", "Wednesday, 10:05 PM", [
        ("c", "I got a letter from the IRS. Can you help?"),
        ("b", "I can&#39;t give tax advice in chat, but our CPAs help with IRS letters all the time. The best next step is a quick call. Want the office to reach out tomorrow morning?"),
        ("c", "Yes please, it&#39;s urgent."),
        ("b", "Understood, I&#39;ve marked it urgent. What&#39;s your name and best number? Please don&#39;t share your Social Security number here."),
        ("c", "Pat, 631-555-0128"),
    ], ["No advice, by the rules", "Kept sensitive info out", "Urgent call request, texted"],
        [("Urgent call", "Pat, IRS letter"), ("When", "Tomorrow morning"), ("Note", "Asked for a call back"), ("Phone", "631-555-0128")]),
]
tabs = "".join('<button class="tvx-tab%s" data-tab="%s">%s%s</button>' % (" on" if n == 0 else "", k, ic(i), t) for n, (k, i, t, *_r) in enumerate(EX))
panels = ""
for k, i, t, biz, when, msgs, did, lead in EX:
    bub = "".join('<p class="tvc-m tvc-%s">%s</p>' % (who, txt) for who, txt in msgs)
    dl = "".join("<li>%s%s</li>" % (ic("check"), d) for d in did)
    rows = "".join("<div><dt>%s</dt><dd>%s</dd></div>" % r for r in lead)
    panels += '''<div class="tvc-ex" data-panel="%s"%s>
  <div class="tvc-chat"><div class="tvc-chd"><span class="tvc-av">%s</span><div><b>%s</b><i>Example conversation</i></div><em>%s</em></div><div class="tvc-log">%s</div></div>
  <div class="tvc-side">
    <div class="tvc-lead"><p class="tvc-lh">%s<span><b>New lead</b>Sent to your phone and email</span></p><dl>%s</dl></div>
    <p class="tvc-dh">What it handled</p><ul class="tvc-did">%s</ul>
  </div>
</div>''' % (k, "" if k == "restaurant" else " hidden", ic(i), biz, when, bub, ic("phone"), rows, dl)
EXAMPLES = K.sec("examples", "Real examples", "See it work for a business like yours.",
                 "Example conversations for sample businesses. Every assistant is trained on your own services, hours, prices and policies.",
                 '<div class="tvc-exw tvs-up" data-tabs data-auto="9000"><div class="tvx-tabs">%s</div>%s</div>' % (tabs, panels))

WHAT = K.sec("what", "What it does", "Smart, friendly, and it never misses a lead.",
             "We build your assistant, teach it your business, and add it to your site. You just watch the leads come in.",
             K.cards([("message", "Answers instantly, 24/7", "Hours, prices, services, service area, parking, policies: anything you teach it, answered in seconds."),
                      ("phone", "Captures every lead", "Name, phone and what they need, sent to your email or phone the moment they ask."),
                      ("calendar", "Books and quotes", "Sends people straight to your booking calendar, quote form or online ordering."),
                      ("search", "Knows your business", "Custom built after we research your business, your industry and your competition. It answers from your approved information."),
                      ("users", "Live person, instantly", "If someone asks for a real person, you get an instant text and email with their name, number and what they need."),
                      ("chart", "Monthly summary", "See what customers asked and how many leads came in. Email us changes anytime and we keep it sharp.")]))

HOW = K.sec("how", "How it works", "Live on your site in about a week.", "",
            K.steps([("We set it up from your info", "Send us your website link and a few details. We study your business, industry and competition, then train and test your assistant. You approve it."),
                     ("It goes live on your site", "One small line of code on the website you already have. We add it for you, or send you simple steps."),
                     ("You get the leads", "Every lead goes to your email or phone right away. If someone asks for a real person, you get an instant text.")])
            + '\n  <div class="tvc-works tvs-up">' + WORKS_ROW.replace(' tvs-up"', '"', 1) + '</div>')

PRICE = '''<section class="tvs-sec tvx-sec tvc-price" id="tvp-price">
  <div class="tvs-head tvs-up"><p class="tvs-eyebrow">Pricing</p><h2>One simple price.</h2><p>The same price for everyone, members or not. Month to month after setup, no contract.</p></div>
  <div class="tvc-pc tvs-up">
    <div class="tvc-pa">
      <p class="tvc-badge">Your Digital Front Desk</p>
      <p class="tvc-pl">One-time setup</p>
      <p class="tvc-amt"><sup>$</sup><b>%d</b></p>
      <p class="tvc-mo">+ <b>$%d</b>/month</p>
      <a class="tvs-btn tvs-blue tvc-go" href="#tvs-book">Get started</a>
      <p class="tvc-note">Month to month. No contract.</p>
    </div>
    <div class="tvc-pb">
      <p class="tvc-grp">Everything you need</p>
      <ul>
        <li>%sCustom built: we research your business, industry and competition</li>
        <li>%sTrained, tested and added to your site for you</li>
        <li>%sAnswers customers 24/7 from your approved information</li>
        <li>%sEvery lead sent to your email or phone right away</li>
        <li>%sLinks to your booking, quote form or online ordering</li>
        <li>%sInstant text when someone asks for a real person</li>
        <li>%sMonthly summary, plus updates whenever you email us</li>
        <li>%sAI usage included, no per-chat fees</li>
      </ul>
      <p class="tvc-plus">%s<span><b>Also included at setup:</b> a one-time AI Website Optimization, so ChatGPT, Google and other AI tools can understand your business.</span></p>
    </div>
  </div>
</section>''' % ((SETUP, MONTHLY) + (ic("check"),) * 8 + (ic("sparkle"),))

FAQ = K.faq([
    ("How accurate is it? Will it make things up?", "It answers only from the information you approve: your website, services, prices, hours and policies. We test it hard before launch and you approve it. When a question needs you, it says so and takes a message instead of guessing."),
    ("Can a customer reach a real person?", "Yes. When someone asks for a person, you get an instant text and email with their name, number and what they need, so you can call them back fast."),
    ("Will it work on my website?", "Almost always. Wix, Squarespace, WordPress, GoDaddy, Shopify and custom sites all work. A few website builders only allow added code on their paid plans, so we check yours first, free. No new website needed."),
    ("How long does setup take?", "About a week. We do the research, training and testing. You review and approve it, then we add it to your site or send you simple steps."),
    ("How do I get my leads?", "Every lead is sent to your email (and phone, if you like) right away, with the customer&#39;s name, number and what they need."),
    ("Can I change what it says?", "Anytime. New prices, specials, hours or services: just email or text us and we update it."),
    ("I&#39;m a law firm, financial advisor or medical office. Is this OK for my industry?", "Yes. We set up your assistant to follow your industry&#39;s rules. It shares general information about your business, never advice, uses the disclaimers you need, only states rates or fees you approve, never asks for sensitive information, and hands anything specific to you. You approve everything before launch."),
    ("Is there a contract?", "No. One setup fee, then it is month to month with no contract."),
    ("Do I have to be a Three Village Local member?", "No. The price is the same for everyone: $%d to set up, then $%d a month." % (SETUP, MONTHLY)),
    ("Will the chatbot help AI tools recommend me?", "Not on its own: AI search tools don&#39;t read chat bubbles. The chatbot turns more of your visitors into leads. The AI Website Optimization included at setup is what helps AI tools understand your business."),
])

CTA = K.cta("Your next customer is asking right now", "Let your front desk answer.",
            "Set up for you in about a week. Every lead sent to you. Month to month, no contract.", alt=("Try the live demo", "#tvx-hero"))

CSS = '''
/* hero live demo */
.tvc-hvis{min-height:0}
.tvc-try{position:relative;width:100%;max-width:440px;margin:0 auto}
.tvc-k{margin:0 0 10px!important;padding-left:6px;font-size:12.5px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--blue)}
.tvc-k span{display:inline-block;width:8px;height:8px;border-radius:50%;background:#2fd28a;margin-right:8px;vertical-align:1px;box-shadow:0 0 0 4px rgba(47,210,138,.2);animation:tvcDot 1.6s ease-in-out infinite}
.tvc-glow{position:relative;border-radius:24px}
.tvc-glow:before{content:"";position:absolute;inset:-3px;border-radius:26px;background:linear-gradient(120deg,#4da3ff,#2fd28a,#1d5fbf,#8fd0ff,#4da3ff);background-size:300% 300%;animation:tvcGrad 6s linear infinite;pointer-events:none}
.tvc-glow:after{content:"";position:absolute;inset:-18px;border-radius:40px;background:radial-gradient(closest-side,rgba(77,163,255,.3),transparent);z-index:-1;pointer-events:none}
#tvc-live{position:relative;z-index:1;min-height:520px;border-radius:22px;background:#fff}
#tvc-live .tva-box{height:520px!important;max-height:none!important}
.tvc-wait{display:flex;align-items:center;justify-content:center;height:520px;font-weight:700;color:var(--mut)}
#tvc-live .tva-w~.tvc-wait,#tvc-live .tvc-wait:not(:only-child){display:none}
.tvc-asks{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:16px}
.tvc-asks p{flex:0 0 100%%;margin:0!important;font-size:12.5px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--mut)}
.tvx .tvc-ask{appearance:none;-webkit-appearance:none;display:inline-flex;align-items:center;gap:7px;margin:0;padding:9px 14px!important;border-radius:999px!important;border:1px solid #d3dff0!important;background:#fff!important;color:var(--navy)!important;font:inherit;font-weight:700!important;font-size:14px!important;line-height:1.25!important;text-align:left;cursor:pointer;text-transform:none!important;letter-spacing:0!important;min-height:40px;height:auto;width:auto;box-shadow:0 6px 16px -12px rgba(9,30,66,.4)!important;transition:border-color .2s,transform .2s}
.tvx .tvc-ask:hover{border-color:#9cc1ff!important;transform:translateY(-1px)}
.tvc-ask .tvx-svg{width:16px;height:16px;color:var(--blue)}
@keyframes tvcGrad{0%{background-position:0% 50%}100%{background-position:300% 50%}}
@keyframes tvcDot{0%,100%{box-shadow:0 0 0 4px rgba(47,210,138,.2)}50%{box-shadow:0 0 0 8px rgba(47,210,138,.05)}}

/* example conversations */
.tvc-exw{max-width:1000px;margin:0 auto}
.tvc-ex{display:grid;grid-template-columns:1.15fr .85fr;gap:26px;align-items:start}
.tvc-chat{border-radius:22px;background:#fff;border:1px solid #dfe8f6;box-shadow:0 30px 60px -36px rgba(9,30,66,.5);overflow:hidden}
.tvc-chd{display:flex;align-items:center;gap:12px;padding:14px 16px;background:linear-gradient(135deg,#0f2445,#1d4fa8);color:#fff}
.tvc-av{display:flex;align-items:center;justify-content:center;width:38px;height:38px;border-radius:12px;background:rgba(255,255,255,.16);flex:none}
.tvc-av .tvx-svg{width:20px;height:20px}
.tvc-chd div{flex:1;min-width:0}
.tvc-chd b{display:block;font-size:15.5px;line-height:1.2}
.tvc-chd i{display:block;font-style:normal;font-size:12.5px;color:#c4d5ee}
.tvc-chd em{font-style:normal;font-size:12.5px;font-weight:700;color:#cfe0f7;white-space:nowrap}
.tvc-log{display:flex;flex-direction:column;gap:9px;padding:18px 16px 20px;background:#f6f8fc}
.tvc-m{max-width:84%%;margin:0!important;padding:10px 14px;border-radius:16px;font-size:15px;line-height:1.45;animation:tvxUp .45s both}
.tvc-b{align-self:flex-start;background:#fff;border:1px solid #e3e9f2;color:var(--ink2);border-bottom-left-radius:5px}
.tvc-c{align-self:flex-end;background:var(--blue);color:#fff;border-bottom-right-radius:5px}
.tvc-m u{text-decoration:none;display:inline-block;margin-top:4px;padding:3px 10px;border-radius:999px;background:#e7f0ff;color:var(--blue);font-weight:800;font-size:13.5px}
.tvc-m:nth-child(2){animation-delay:.35s}.tvc-m:nth-child(3){animation-delay:.9s}.tvc-m:nth-child(4){animation-delay:1.3s}.tvc-m:nth-child(5){animation-delay:1.9s}
.tvc-lead{border-radius:20px;background:#fff;border:1px solid #cdeedd;box-shadow:0 24px 50px -34px rgba(9,30,66,.5);overflow:hidden;animation:tvxPop .5s 2.3s both}
.tvc-lh{display:flex;align-items:center;gap:12px;margin:0!important;padding:14px 16px;background:#effaf5;border-bottom:1px solid #d7f0e4}
.tvc-lh .tvx-svg{width:34px;height:34px;padding:7px;border-radius:10px;background:#16a37a;color:#fff}
.tvc-lh span{font-size:13px;color:#3f6b5b;line-height:1.3}.tvc-lh b{display:block;font-size:16px;color:#0d5c47}
.tvc-lead dl{margin:0!important;padding:8px 16px 12px}
.tvc-lead dl div{display:grid;grid-template-columns:96px 1fr;gap:10px;padding:7px 0;border-bottom:1px solid #eef2f7}
.tvc-lead dl div:last-child{border-bottom:0}
.tvc-lead dt{font-size:12.5px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--mut)}
.tvc-lead dd{margin:0!important;font-size:14.5px;font-weight:700;color:var(--navy)}
.tvc-dh{margin:22px 0 8px!important;font-size:12.5px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--blue)}
.tvc-did{list-style:none;margin:0!important;padding:0!important;display:grid;gap:8px}
.tvc-did li{display:flex;gap:9px;align-items:center;margin:0!important;font-size:15px;font-weight:700;color:var(--navy)}
.tvc-did .tvx-svg{width:20px;height:20px;padding:3px;border-radius:50%%;background:#dff7ee;color:#16a37a}

/* platforms */
.tvc-works{max-width:1060px;margin:34px auto 0;text-align:center}
.tvc-works .tva-works p{margin:0 0 10px!important;font-size:12.5px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--mut)}
.tvc-works .tva-works div{display:flex;flex-wrap:wrap;justify-content:center;gap:8px}
.tvc-works .tva-works span{display:inline-flex;align-items:center;gap:8px;font-size:14px;font-weight:800;padding:8px 15px 8px 12px;border-radius:999px;background:#fff;border:1px solid #dfe6f0;color:var(--navy)}
.tvc-works .tva-works span svg{width:auto!important;height:20px!important;max-width:46px;display:block;flex:none}

/* pricing */
.tvc-pc{display:grid;grid-template-columns:.8fr 1.2fr;max-width:960px;margin:0 auto;border-radius:26px;background:#fff;border:1px solid #dfe8f6;box-shadow:0 34px 70px -40px rgba(9,30,66,.55);overflow:hidden}
.tvc-pa{padding:34px 30px;text-align:center;background:radial-gradient(420px 260px at 50% 0%,rgba(77,163,255,.16),transparent 70%),#f6f9ff;border-right:1px solid #e3e9f2}
.tvc-badge{display:inline-block;margin:0 0 14px!important;padding:7px 15px;border-radius:999px;background:var(--navy);color:#fff!important;font-size:13px;font-weight:800;letter-spacing:.04em}
.tvc-pl{margin:0!important;font-size:12.5px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--blue)}
.tvc-amt{margin:2px 0 0!important;line-height:1;color:var(--navy)}
.tvc-amt sup{font-size:28px;font-weight:800;vertical-align:28px}
.tvc-amt b{font-size:76px;font-weight:800;letter-spacing:-.03em}
.tvc-mo{margin:6px 0 22px!important;font-size:19px;color:var(--mut)}.tvc-mo b{color:var(--navy);font-size:24px}
.tvc-go{display:block;width:100%%}
.tvc-note{margin:12px 0 0!important;font-size:13.5px;color:var(--mut)}
.tvc-pb{padding:30px 32px}
.tvc-grp{margin:0 0 12px!important;font-size:12.5px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--blue)}
.tvc-pb ul{list-style:none;margin:0!important;padding:0!important;display:grid;gap:10px}
.tvc-pb li{display:flex;gap:10px;align-items:flex-start;margin:0!important;font-size:15.5px;line-height:1.4;color:var(--ink2)}
.tvc-pb li .tvx-svg{width:20px;height:20px;padding:3px;border-radius:50%%;background:#dff7ee;color:#16a37a;margin-top:1px}
.tvc-plus{display:flex;gap:10px;align-items:flex-start;margin:20px 0 0!important;padding:14px 16px;border-radius:14px;background:#f6f9ff;border:1px solid #dfe8f6;font-size:14.5px;line-height:1.45;color:var(--ink2)}
.tvc-plus .tvx-svg{width:20px;height:20px;color:#e0a82e;margin-top:1px}
.tvc-plus b{color:var(--navy)}

@media (max-width:900px){
 .tvc-hero .tvx-hvis{order:2}
 .tvc-ex{grid-template-columns:1fr;gap:18px}
 .tvc-pc{grid-template-columns:1fr}.tvc-pa{border-right:0;border-bottom:1px solid #e3e9f2;padding:28px 20px}.tvc-pb{padding:24px 20px}
}
@media (max-width:520px){
 #tvc-live{min-height:470px}#tvc-live .tva-box{height:470px!important}.tvc-wait{height:470px}
 .tvc-try{max-width:none}.tvc-glow:after{display:none}
 .tvc-m{max-width:90%%;font-size:14.5px}.tvc-log{padding:14px 12px 16px}
 .tvc-chd em{display:none}
 .tvc-lead dl div{grid-template-columns:84px 1fr}
 .tvc-amt b{font-size:64px}
 .tvx .tvx-tab{padding:9px 13px!important;font-size:14px!important}
}
@media (prefers-reduced-motion:reduce){.tvc-glow:before,.tvc-k span{animation:none!important}}
''' .replace("%%", "%")

JS = '''
document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.tvc-ask');if(!b)return;e.preventDefault();var q=b.getAttribute('data-q');
 if(window.tvaAsk){window.tvaAsk(q);if(window.tvxGA)window.tvxGA('svc_page_demo_ask',{q:q});var lv=document.getElementById('tvc-live');if(lv&&lv.getBoundingClientRect().top<0)lv.scrollIntoView({behavior:'smooth',block:'start'});}});
(function(){var lv=document.getElementById('tvc-live');if(!lv||!('MutationObserver' in window))return;var w=lv.querySelector('.tvc-wait');var mo=new MutationObserver(function(){if(lv.querySelector('.tva-w')){if(w)w.remove();mo.disconnect();}});mo.observe(lv,{childList:true});})();
'''

if __name__ == "__main__":
    html = K.page("Chatbot", "chatbot",
                  "AI Chatbot for Local Businesses: Answer Customers 24/7 | Three Village Local",
                  "Your Digital Front Desk: a smart AI chatbot for your website that answers customers 24/7, captures every lead and sends it to you by email or text. Set up for you in about a week. Works with Wix, Squarespace, WordPress and more.",
                  "Answer every customer, even when you're closed.",
                  [HERO, NAV, WHY, EXAMPLES, WHAT, HOW, PRICE, FAQ, CTA], bundle="ai_chat", css=CSS, js=JS,
                  book_eyebrow="Get started", fb_image="/share/ai-websites-v2.jpg", prices=True)
    _rd = K.D.rd

    def rd(f):
        s = _rd(f)
        if f == "page.html":
            for a, z in [('<a class="tvp-snav-cta" href="#tvs-book">Get my free plan</a>', '<a class="tvp-snav-cta" href="#tvs-book">Get started</a>'),
                         ('<a class="tvs-btn tvw-btn-w" href="#tvs-book">Get my free plan</a>', '<a class="tvs-btn tvw-btn-w" href="#tvs-book">Get started</a>'),
                         ('<a class="tvs-sticky" href="#tvs-book">Get my free plan</a>', '<a class="tvs-sticky" href="#tvs-book">Get started</a>'),
                         ("<h2>Get your free plan.</h2>", "<h2>Get your Digital Front Desk.</h2>"),
                         ("<p>Tell us your name, business and email. Within one business day you&#39;ll get a free, personalized plan by email:</p>",
                          "<p>Tell us your name, business and website. We reply within one business day, by email or text, with next steps:</p>"),
                         ("<li>How you show up on Google and AI tools today</li><li>The 3 things we&#39;d do first for your business</li><li>No pressure and no contract</li>",
                          "<li>What your assistant will answer for your customers</li><li>Where your leads will go: email, text or both</li><li>Live in about a week, month to month, no contract</li>"),
                         ('<p class="tvp-alt">Rather start smaller? <a href="/free-ai-report">See if ChatGPT recommends your business &rarr; free AI check</a></p>', ""),
                         ("mailto:hello@threevillagelocal.com?subject=Our%20services", "mailto:hello@threevillagelocal.com?subject=AI%20chatbot")]:
                assert a in s, a
                s = s.replace(a, z)
            assert "\\" not in s and "&mdash;" not in s and "—" not in s
        if f == "page.js":
            # the shared page.js already carries the floating-bubble widget tag; this page mounts it inline instead
            s, n = re.subn(r'<script src="https://3vl-ai-assistant\.vercel\.app/widget\.js"[^>]*></script>', "", s)
            assert n == 1, n
            s += WIDGET
        return s

    K.D.rd = rd
    K.main()
