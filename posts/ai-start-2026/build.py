"""5 Ways AI Can Help Your Long Island Business This Week (No Tech Skills Needed). Blog article.
    python build.py [--local]   -> post.html   (assets: bash publish_assets.sh; site: python push.py)"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LOCAL = "--local" in sys.argv
ASSET = "" if LOCAL else "https://threevillagelocal-cloud.github.io/3vl-share/ai-5-ways/"
IMG = ASSET + "img/"
D = "https://3vldigital.com"
UTM = "?utm_source=threevillagelocal&utm_medium=blog&utm_campaign=ai-5-ways"
VER = "5"


def dl(path, text, cls="", cta=""):
    """Link to 3vldigital.com with UTM + data-cta (GA4 ais_cta event in ais.js)."""
    cta = cta or path.strip("/") or "home"
    return '<a%s href="%s%s%s&amp;utm_content=%s" target="_blank" rel="noopener" data-cta="%s">%s</a>' % (
        ' class="%s"' % cls if cls else "", D, path, UTM, cta, cta, text)


LOGO_NAMES = {"quickbooks": "QuickBooks", "square": "Square", "stripe": "Stripe", "shopify": "Shopify", "mailchimp": "Mailchimp",
              "gmail": "Gmail", "googlecalendar": "Google Calendar", "google": "Google Business", "facebook": "Facebook",
              "instagram": "Instagram", "calendly": "Calendly", "paypal": "PayPal", "xero": "Xero", "hubspot": "HubSpot",
              "gusto": "Gusto", "yelp": "Yelp", "googlesheets": "Google Sheets", "zoom": "Zoom",
              "chatgpt": "ChatGPT", "gemini": "Gemini", "claude": "Claude", "microsoftcopilot": "Copilot", "perplexity": "Perplexity",
              "googleaioverviews": "Google AI", "metaai": "Meta AI", "siri": "Siri"}


def logos(keys, more=""):
    """Real brand logos (official SVGs, aspect kept via object-fit:contain) in a tidy grid."""
    cells = "".join('<span class="ais-lg"><img src="%slogos/%s.svg" alt="" width="28" height="28" loading="lazy" decoding="async"><b>%s</b></span>'
                    % (IMG, k, LOGO_NAMES[k]) for k in keys)
    if more:
        cells += '<span class="ais-lg ais-lg-more"><b>%s</b></span>' % more
    return '<div class="ais-logos">%s</div>' % cells


def cta(icon, text, links):
    """Slim contextual CTA after each way."""
    return ('<div class="ais-cta rv"><span class="ais-cta-ic">%s</span><p>%s</p><div class="ais-cta-btns">%s</div></div>'
            % (icon, text, "".join(links)))


def pic(name, alt, toast=""):
    return ('<div class="ais-pic rv"><img src="%s%s-640.webp" srcset="%s%s-480.webp 480w, %s%s-640.webp 640w" sizes="(max-width:560px) 92vw, 520px" '
            'alt="%s" width="640" height="480" loading="lazy" decoding="async">%s</div>' % (IMG, name, IMG, name, IMG, name, alt, toast))


H = []
w = H.append
w('<link rel="stylesheet" href="%sais.css?v=%s">' % (ASSET, VER))
w('<div class="ais" id="ais-top"><div class="ais-prog"><i></i></div>')

# ---------------- HERO ----------------
w('<header class="ais-hero">'
  '<div class="ais-hl">'
  '<p class="ais-kick"><span class="ais-dot"></span>A plain-English guide for local owners</p>'
  '<h2 class="ais-h1">5 Ways AI Can Help Your Long Island Business <span>This Week</span></h2>'
  '<p class="ais-sub">No tech skills needed. Seriously.</p>'
  '<p class="ais-dek">AI isn&rsquo;t coming, it&rsquo;s here. Your customers already use it to find businesses, and some of your competitors are quietly starting to use it to answer faster and work smarter. The good news: the first steps are easy. If you can send a text, you can do every one of these.</p>'
  '<div class="ais-btns"><a class="ais-btn ais-btn-gold" href="#ais-1">Show me the 5 ways</a><a class="ais-btn ais-btn-line" href="#ais-digi">Want it done for you?</a></div>'
  '<p class="ais-meta">By Three Village Local &middot; November 15, 2026 &middot; 6 min read</p>'
  '</div>'
  '<div class="ais-hpic">'
  '<div class="ais-hphoto"><img src="%shero-900.webp" srcset="%shero-900.webp 900w, %shero-1600.webp 1600w" sizes="(max-width:860px) 94vw, 560px" '
  'alt="Smiling cafe owner holding an open sign" width="900" height="675" fetchpriority="high" decoding="async"></div>' % (IMG, IMG, IMG) +
  '<div class="ais-chips" aria-hidden="true"><span class="ais-chip">&#128172; Answers 24/7</span><span class="ais-chip">&#9997;&#65039; Drafts replies</span><span class="ais-chip">&#128202; One dashboard</span></div>'
  '<div class="ais-phone" aria-hidden="true"><div class="ais-pbar"><b>Ask us anything</b><span>online</span></div>'
  '<div class="ais-chat" data-chat="hero">'
  '<div class="ais-time">9:47 PM &middot; you&rsquo;re closed</div>'
  '<div class="ais-msg ais-me">Can I order a birthday cake for Saturday?</div>'
  '<div class="ais-typing"><i></i><i></i><i></i></div>'
  '<div class="ais-msg ais-ai">Yes! Custom cakes need 48 hours, so Saturday works. Want the team to call you in the morning to finish the order?</div>'
  '<div class="ais-msg ais-me">Yes please. Jen, 631-555-0188</div>'
  '<div class="ais-typing"><i></i><i></i><i></i></div>'
  '<div class="ais-msg ais-ai">Done! Expect a call by 10 AM. &#127874;</div>'
  '</div></div></div></header>')

w('<nav class="ais-nav" aria-label="The 5 ways">'
  '<a href="#ais-1">1 &middot; Answer 24/7</a><a href="#ais-2">2 &middot; Draft replies</a><a href="#ais-3">3 &middot; One dashboard</a>'
  '<a href="#ais-4">4 &middot; Get found by AI</a><a href="#ais-5">5 &middot; Set your rules</a><a href="#ais-plan">Your 5-day plan</a></nav>')

# ---------------- WAY 1: chatbot ----------------
w('<section class="ais-sec rv" id="ais-1"><div class="ais-step">'
  + pic("chat", "Florist answering a customer on her phone",
        '<div class="ais-ptoast"><span>&#128276;</span><div><b>New lead, 9:47 PM</b><small>Jen &middot; birthday cake &middot; call back AM</small></div></div>') +
  '<div><span class="ais-num">1</span><p class="ais-eye">Quick win: stop missing after-hours customers</p>'
  '<h3>Answer every question, <span>even at 10 PM.</span></h3>'
  '<p class="ais-lead">Most customers reach out to the first business that answers. When you&rsquo;re closed, busy with a client or on a job site, an AI chatbot on your website answers for you.</p>'
  '<ul class="ais-ticks"><li><b>Answers real questions</b> about your hours, services, prices and policies, in your words.</li>'
  '<li><b>Grabs the lead</b> when someone is ready: name, number and what they need.</li>'
  '<li><b>Texts it to you</b> right away, so you call back first.</li>'
  '<li><b>Hands off to you</b> for anything it shouldn&rsquo;t answer.</li></ul>'
  '<div class="ais-box"><b>Do this week:</b> write down the 10 questions customers ask you most. That list is the heart of any good chatbot.</div>'
  '</div></div>'
  + cta("&#128172;", "<b>Want one built for you?</b> 3VL Digital builds custom AI chatbots trained on your business, live in about a week.",
        [dl("/chatbots", "See AI chatbots", "ais-cbtn", "way1-chatbots"),
         dl("/chatbots", "Try our AI chatbot live &rarr;", "ais-clink", "way1-try-live")]) +
  '<p class="ais-small ais-ctr">To try it live, tap the blue chat bubble on 3vldigital.com and ask it anything.</p>'
  '<p class="ais-next">Next: let AI write the first draft &darr;</p>'
  '</section>')

# ---------------- WAY 2: drafts ----------------
PROMPTS = [     ("review", "&#11088; Reply to a review",      'You are the owner of <i>[business name]</i>, a <i>[type of business]</i> in <i>[town]</i>. Write a warm, short reply to this Google review. Thank them by first name, mention one detail they shared, and invite them back. Under 60 words.\n\nReview: <i>[paste the review]</i>'),     ("post", "&#128248; Social post",      'Write 3 short Instagram captions for <i>[business name]</i> in <i>[town]</i> announcing <i>[this week\'s special]</i>. Friendly local voice, one emoji each, end with a reason to stop in today.'),     ("hours", "&#128197; Holiday hours email",      'Write a short, friendly email to our customers about our holiday hours: <i>[list your hours]</i>. Thank them for a great year. Under 100 words. Include a subject line.'),     ("tough", "&#128172; Tricky customer",      'A customer asked: <i>[paste their message]</i> Draft a polite, clear reply that explains <i>[our policy]</i>. Keep it kind, offer one helpful alternative, and keep it under 80 words.'), ]
w('<section class="ais-sec ais-tint rv" id="ais-2"><div class="ais-step rev">'
  + pic("draft", "Bakery owner using a tablet in her kitchen") +
  '<div><span class="ais-num">2</span><p class="ais-eye">Quick win: save an hour a day</p>'
  '<h3>Let AI write the <span>first draft.</span></h3>'
  '<p class="ais-lead">Review replies, social posts, emails, that awkward message to a customer. Free tools like ChatGPT, Gemini or Claude write a solid first draft in seconds. You just edit and send.</p>'
  '<p class="ais-ltitle">Works in any of these AI tools:</p>'
  + logos(["chatgpt", "gemini", "claude", "microsoftcopilot", "perplexity", "metaai"]) +
  '<p>The trick is telling it who you are and what you want. Pick one below, copy it, fill in the yellow parts and paste it into any AI chat.</p>'
  '</div></div>'
  '<div class="ais-pp"><div class="ais-ptabs" role="tablist">%s</div>%s'
  % ("".join('<button type="button" role="tab" data-p="%s"%s>%s</button>' % (k, ' class="on"' if i == 0 else "", t) for i, (k, t, _) in enumerate(PROMPTS)),
     "".join('<pre class="ais-prompt%s" data-p="%s">%s</pre>' % (" on" if i == 0 else "", k, p) for i, (k, _, p) in enumerate(PROMPTS))) +
  '<div class="ais-pfoot"><small>&#9989; Always read it before you send it. AI drafts, you decide.</small><button type="button" class="ais-copy">Copy this prompt</button></div></div>'
  + cta("&#9889;", "<b>Want AI working across your whole business,</b> not just in a chat window? See everything 3VL Digital builds for local businesses.",
        [dl("/products", "See our AI services", "ais-cbtn", "way2-products")]) +
  '<p class="ais-next">Next: stop logging into 8 different programs &darr;</p>'
  '</section>')

# ---------------- WAY 3: dashboard ----------------
ROLES = [("owner", "Owner", "Owner view of a real 3VL Digital dashboard: good afternoon briefing, tonight's floor, menu and covers"),
         ("mgr", "Manager", "Manager view: operations without profit or payroll"),
         ("staff", "Employee", "Employee view: their own shift, tables and tasks")]
INT = ["quickbooks", "square", "stripe", "shopify", "mailchimp", "gmail", "googlecalendar", "google", "facebook", "instagram",
       "calendly", "paypal", "xero", "hubspot", "gusto", "yelp", "googlesheets", "zoom"]
w('<section class="ais-sec rv" id="ais-3"><span class="ais-num">3</span><p class="ais-eye">Quick win: see your whole business on one screen</p>'
  '<h3>Put everything in <span>one dashboard.</span></h3>'
  '<p class="ais-lead">Leads in your inbox, jobs in a calendar, money in QuickBooks, reviews on Google, posts on Instagram. A company dashboard pulls it all into one place, on your computer and your phone, with a &ldquo;good morning&rdquo; summary of what needs you today.</p>'
  '<div class="ais-bw rv"><div class="ais-bwbar"><i></i><i></i><i></i><span>Command Center</span>'
  '<div class="ais-roles" role="tablist" aria-label="View as">%s</div></div>'
  '<div class="ais-bwshot">%s</div></div>'
  % ("".join('<button type="button" role="tab" data-r="%s"%s>%s</button>' % (k, ' class="on"' if i == 0 else "", n) for i, (k, n, _) in enumerate(ROLES)),
     "".join('<img class="ais-dimg%s" data-r="%s" src="%sdash-%s-960.webp" srcset="%sdash-%s-960.webp 960w, %sdash-%s-1600.webp 1600w" '
             'sizes="(max-width:640px) 240vw, (max-width:1100px) 96vw, 1080px" width="1600" height="980" alt="%s" loading="lazy" decoding="async">'
             % (" on" if i == 0 else "", k, IMG, k, IMG, k, IMG, k, alt) for i, (k, _, alt) in enumerate(ROLES))) +
  '<p class="ais-small ais-ctr">A real dashboard we built, shown with a sample restaurant. Tap Owner, Manager or Employee to see how each person gets their own view.</p>'
  '<div class="ais-split ais-dsplit"><div>'
  '<ul class="ais-ticks"><li><b>A &ldquo;good morning&rdquo; briefing:</b> what happened overnight, what&rsquo;s booked today and what needs you.</li>'
  '<li><b>The right view for each person:</b> owner, manager and employee each see only what they need.</li>'
  '<li><b>Leads, jobs, calendar, tasks and money at a glance</b>, all in one place.</li>'
  '<li><b>AI does the busywork:</b> follow-ups, reminders, review replies and a plain-English summary of your week.</li></ul>'
  '<div class="ais-box"><b>Do this week:</b> list every program you log into in a normal day. That list is the start of your dashboard.</div>'
  '</div><div><p class="ais-ltitle">Connects to the programs you already use:</p>'
  + logos(INT, "+ 400 more") +
  '<p class="ais-small">We integrate with over 400 of the most commonly used software programs and apps, so you get everything in one place.</p>'
  '</div></div>'
  + cta("&#128202;", "<b>Want a dashboard like this for your business?</b> Built around how you work, connected to the tools you already use.",
        [dl("/dashboards", "See company dashboards", "ais-cbtn", "way3-dashboards")]) +
  '</section>')

# ---------------- mid-article banner ----------------
w('<section class="ais-band rv"><div class="ais-band-in"><div><p class="ais-band-k">&#9889; 3VL Digital</p>'
  '<h3>Rather skip the setup? <span>We&rsquo;ll do all 5 for you.</span></h3>'
  '<p>Your chatbot, your dashboard and an AI-ready website, set up, trained and kept running by one local team.</p></div>'
  '<div class="ais-band-btns">' + dl("/book", "Book a free 15-min call", "ais-btn ais-btn-gold", "mid-book") +
  dl("/products", "See all services", "ais-btn ais-btn-white", "mid-products") + '</div></div></section>')
w('<p class="ais-next ais-ctr">Next: make sure AI recommends you &darr;</p>')

# ---------------- WAY 4: found by AI ----------------
FOUND = [("Ask AI about yourself", "Type &ldquo;best <i>[your type of business]</i> near <i>[your town]</i>&rdquo; into ChatGPT. Are you on the list?"),
         ("Finish your Google Business Profile", "Hours, services, photos and a few lines about what makes you different. AI reads it."),
         ("Put your hours and services in plain text", "On your website, as words, not only inside a photo or a PDF menu."),
         ("Answer the top questions on your site", "Parking, pricing ranges, how to book. AI loves clear answers."),
         ("Ask happy customers for a review", "Fresh reviews that mention what you do and your town help AI trust you.")]
w('<section class="ais-sec ais-tint rv" id="ais-4"><div class="ais-step rev">'
  + pic("found", "Confident salon owner standing in her salon") +
  '<div><span class="ais-num">4</span><p class="ais-eye">Quick win: show up when customers ask AI</p>'
  '<h3>Get found when people <span>ask AI.</span></h3>'
  '<p class="ais-lead">More people now ask ChatGPT, Google or Siri for a recommendation and get back just a few names. Make sure AI knows enough about you to say yours.</p>'
  '<p class="ais-ltitle">Where your customers are asking:</p>'
  + logos(["chatgpt", "googleaioverviews", "gemini", "siri", "perplexity", "microsoftcopilot"]) +
  '<p>Check these off as you go. We&rsquo;ll remember your progress on this device.</p>'
  '</div></div>'
  '<ul class="ais-check" data-save="ais-found">%s</ul>' % "".join(
      '<li><label><input type="checkbox" data-k="f%d"><div><b>%s</b><span>%s</span></div></label></li>' % (i, t, d) for i, (t, d) in enumerate(FOUND)) +
  cta("&#128269;", "<b>Website not built for AI?</b> Many template sites hide their words inside scripts AI can&rsquo;t read. We build fast sites from scratch and help AI search recommend you.",
        [dl("/websites", "See AI-ready websites", "ais-cbtn", "way4-websites"),
         dl("/ai-search", "AI search optimization &rarr;", "ais-clink", "way4-ai-search")]) +
  '<p class="ais-next">Last one: the house rules that keep AI safe &darr;</p>'
  '</section>')

# ---------------- WAY 5: rules ----------------
RULES = [("&#128274;", "Protect private info", "Never paste card numbers, Social Security numbers or medical details into a free AI chat. Use business tools with clear privacy rules."),
         ("&#128269;", "Check the facts", "AI can sound sure and still be wrong. Double-check prices, hours and policies before anything goes out."),
         ("&#129309;", "Keep a human in the loop", "AI drafts, you decide. A good chatbot hands sensitive questions to a real person."),
         ("&#128483;&#65039;", "Keep your voice", "Edit drafts so they sound like you. Your customers know you, not a robot.")]
w('<section class="ais-sec rv" id="ais-5"><span class="ais-num">5</span><p class="ais-eye">Quick win: 5 minutes, peace of mind</p>'
  '<h3>Set your AI <span>house rules.</span></h3>'
  '<p class="ais-lead">Write these on a sticky note for you and your team. They take five minutes and prevent almost every AI mistake.</p>'
  '<div class="ais-watch">%s</div>' % "".join('<div class="ais-wo rv"><span>%s</span><b>%s</b><p>%s</p></div>' % r for r in RULES) +
  cta("&#129309;", "<b>Not sure where to start, or worried about getting it wrong?</b> Talk it through with a real person on our team. No pressure, no tech talk.",
      [dl("/book", "Book a free 15-minute call", "ais-cbtn", "way5-book")]) +
  '</section>')

# ---------------- 5-day plan ----------------
PLAN = [("Mon", "Ask AI who it recommends", "for your type of business in your town. Note who shows up."),
        ("Tue", "Update your Google Business Profile", "hours, services and 5 fresh photos."),
        ("Wed", "Reply to your last 5 reviews", "using the AI prompt from way #2."),
        ("Thu", "Write your top 10 customer questions", "and your best answers. Your future chatbot&rsquo;s playbook."),
        ("Fri", "List every program you use daily", "and share your AI house rules with your team.")]
w('<section class="ais-sec ais-tint rv" id="ais-plan"><p class="ais-eye">Put it into action</p>'
  '<h3>Your 5-day <span>AI starter plan.</span></h3>'
  '<p class="ais-lead">About 15 minutes a day. Check them off and watch your score climb.</p>'
  '<div class="ais-week"><ul class="ais-check" data-save="ais-plan">%s</ul>' % "".join(
      '<li><label><input type="checkbox" data-k="p%d"><div><b><span class="ais-day">%s</span>%s</b><span>%s</span></div></label></li>' % (i, d, t, x) for i, (d, t, x) in enumerate(PLAN)) +
  '<div class="ais-wscore"><svg viewBox="0 0 120 120" aria-hidden="true"><circle class="ais-ring-bg" cx="60" cy="60" r="52"/><circle class="ais-ring" cx="60" cy="60" r="52"/></svg>'
  '<div class="ais-wnum"><b>0</b><span>of 5 done</span></div><p class="ais-wmsg">Start with Monday. It takes 2 minutes.</p>'
  '<button type="button" class="ais-share ais-save">Save this plan for later</button></div></div>'
  '</section>')

# ---------------- 3VL Digital ----------------
w('<section class="ais-digi rv" id="ais-digi"><p class="ais-dkick">&#9889; 3VL Digital</p>'
  '<h3 style="font-size:36px;line-height:1.1;font-weight:900;margin:12px 0 10px">Rather have it <span style="color:var(--blue)">done for you?</span></h3>'
  '<p class="ais-lead">3VL Digital is the tech team behind Three Village Local. We build the AI tools in this guide for local businesses, then set them up, train them and keep them running. One local team, no tech skills needed on your end.</p>'
  '<div class="ais-prods">'
  + dl("/chatbots", '<span class="ais-ic">&#128172;</span><b>AI Chatbots</b><p>A custom assistant trained on your business. Answers customers 24/7 and texts you every lead. Live in about a week.</p><em>See AI chatbots &rarr;</em>', "ais-prod", "box-chatbots")
  + dl("/websites", '<span class="ais-ic">&#127760;</span><b>AI-Ready Websites</b><p>Built from scratch, fast on every phone and written so Google and AI assistants recommend your business.</p><em>See websites &rarr;</em>', "ais-prod", "box-websites")
  + dl("/dashboards", '<span class="ais-ic">&#128202;</span><b>Company Dashboards</b><p>Leads, customers, jobs, money and marketing in one place for you and your team. Connects to 400+ programs.</p><em>See dashboards &rarr;</em>', "ais-prod", "box-dashboards") +
  '</div>'
  '<div class="ais-btns ais-center">' + dl("/products", "See all products", "ais-btn ais-btn-blue", "box-products") +
  dl("/book", "Book a free consultation", "ais-btn ais-btn-line", "box-book") + '</div>'
  '<p class="ais-small" style="text-align:center;margin-top:12px!important">Questions? Our own AI assistant on 3vldigital.com answers 24/7, or a real person will get back to you.</p>'
  '</section>')

# ---------------- FAQ ----------------
FAQ = [("Is AI expensive for a small business?", "Not to get started. Free AI chats are great for drafts. Done-for-you tools like a custom chatbot or dashboard are built, trained and maintained for your business, and we&rsquo;ll walk you through the options on a free call."),
       ("Will a chatbot sound like a robot?", "Not a good one. It&rsquo;s trained on your business and your way of talking, and it passes anything sensitive to you."),
       ("Is my customer information safe?", "Stick to the house rules in way #5. Never put private customer details into free tools, and ask any vendor how they store your data."),
       ("Do I have to be a Three Village Local member to work with 3VL Digital?", "No. 3VL Digital works with any local business, member or not."),
       ("How long does a custom chatbot take?", "About a week. We research your business, build and train the assistant, test it with you, then add it to your website.")]
w('<section class="ais-sec rv" id="ais-faq"><h3>Quick questions.</h3><div class="ais-faq">%s</div></section>'
  % "".join('<details><summary>%s</summary><p>%s</p></details>' % f for f in FAQ))

# ---------------- final ----------------
w('<section class="ais-final rv"><div class="ais-fin">'
  '<h3>Your competitors are starting with AI.<br><span>Now you have a 5-day head start.</span></h3>'
  '<div class="ais-btns"><a class="ais-btn ais-btn-gold" href="#ais-plan">Start my 5-day plan</a>' + dl("/book", "Book a free consultation", "ais-btn ais-btn-white", "final-book") + '</div>'
  '<button type="button" class="ais-share">Share this with a business owner</button></div></section>')
w('<p class="ais-cred">The chat examples and the sample restaurant in the dashboard are fictional. Photos: Pexels (Vitaly Gariev, Amina Filkins, Hanna Pad, Kampus Production). Product names and logos are trademarks of their owners, shown only to identify the tools.</p>')
w('</div>')
w('<style>#post-content .post-image-container,#post-content .post-image-container + hr{display:none!important}</style>')
w('<script src="%sais.js?v=%s" defer></script>' % (ASSET, VER))

out = "".join(H)
assert "$" not in out, "no $ amounts anywhere"
for bad in ("—", "–", "&mdash;", "&ndash;"):
    assert bad not in out, "em/en dash"
open(os.path.join(HERE, "post-local.html" if LOCAL else "post.html"), "w", encoding="utf-8").write(out)
print("post.html", len(out), "chars")
