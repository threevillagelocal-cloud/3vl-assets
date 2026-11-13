"""Company Digital Dashboards: custom all-in-one business dashboards built by Three Village Local.
Interactive showcase (8 dashboard screens), role views, devices, automations feed, industries, features, security, process,
sample demos, FAQ and the shared message form. Same design system as /services (imports the platform-page build).
No prices on this page: every dashboard gets a custom quote.
    python site/dashboards-page/build.py          -> widget "3VL Page Dashboards Preview" + hidden /preview-business-dashboards (noindex)
    python site/dashboards-page/build.py --live   -> widget "3VL Page Dashboards" + /business-dashboards"""
import importlib.util, json, os, re, sys
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("platbuild", os.path.join(HERE, "..", "platform-page", "build.py"))
P = importlib.util.module_from_spec(spec)
spec.loader.exec_module(P)
D = P.D
# Integrations are a DASHBOARD FEATURE (an "Integrations" screen inside every demo), not a separate page.
# dash_integrations.json comes from integ_build.py (only tools with a real API, feed or export).
INTEG = json.load(open(os.path.join(HERE, "dash_integrations.json"), encoding="utf-8"))

D.NAME = "3VL Page Dashboards" if D.LIVE else "3VL Page Dashboards Preview"
D.SLUG = "business-dashboards" if D.LIVE else "preview-business-dashboards"
D.TITLE = "Company Digital Dashboards: Your Whole Business in One Dashboard | Three Village Local"
D.DESC = ("Custom business dashboards built by Three Village Local: customers and leads, calendar, money, marketing, social media, "
          "reviews, team and automations in one place, with an AI assistant. Works on laptop, tablet and phone.")
D.FB_TITLE = "Your whole business. One dashboard."
D.FB_IMAGE = "/share/svc-business-dashboards-v1.jpg"   # BD redirect 2361 -> 3vl-share/site/services/share/svc-business-dashboards-v1.jpg
CDN = "https://cdn.jsdelivr.net/npm/simple-icons@%s/icons/" % INTEG["v"]
TOOLS = [i for i in INTEG["items"] if i["t"] != "built"]
NTOOLS = "%d+" % (len(TOOLS) // 50 * 50)
NT = {t: sum(1 for i in TOOLS if i["t"] == t) for t in ("api", "feed", "export")}
# live demos: public copies in 3vl-share (demos/dashboards); the realtor CRM is its own app
DEMO_BASE = "https://threevillagelocal-cloud.github.io/3vl-share/demos/dashboards/"
REALTOR = "https://realtors-edge.vercel.app"
LIVE_DEMOS = [  # key, tab, emoji, business, kind, address bar
    ("restaurant", "Restaurant", "&#127869;", "Harbor &amp; Vine", "Restaurant", "dashboard.harborandvine.com"),
    ("contractor", "Contractor", "&#128679;", "North Shore Builders", "Contractor", "dashboard.northshorebuilders.com"),
    ("salon", "Salon", "&#10024;", "Glow Studio", "Salon &amp; med spa", "dashboard.glowstudio.com"),
    ("gym", "Gym", "&#127947;", "Iron Harbor Fitness", "Gym &amp; studio", "dashboard.ironharborfitness.com"),
    ("landscaper", "Landscaper", "&#127807;", "Greenline Landscape Co.", "Landscaping", "dashboard.greenlinelandscape.com"),
    ("realestate", "Real estate", "&#127969;", "Realtor&#39;s Edge", "Real estate CRM", "realtors-edge.vercel.app"),
]


def demo_url(k, tour=True):
    if k == "realestate":
        return REALTOR
    return DEMO_BASE + k + ".html" + ("?embed=1&tour=1" if tour else "")


def poster(k, dev):
    return DEMO_BASE + "posters/%s-%s.webp" % (k, dev)

# ---------- hero: live embedded demos (laptop + phone), lazy loaded by dash.js ----------
ltabs = "".join('<button type="button" class="tvd-lt%s" role="tab" aria-selected="%s" data-k="%s" data-src="%s" data-full="%s" data-pd="%s" data-pp="%s" data-url="%s" data-name="%s" data-kind="%s"><span>%s</span>%s</button>' % (
    " on" if n == 0 else "", "true" if n == 0 else "false", k, demo_url(k), demo_url(k, False), poster(k, "desk"), poster(k, "phone"), u, b, kd.lower(), e, t)
    for n, (k, t, e, b, kd, u) in enumerate(LIVE_DEMOS))
APP = '''<div class="tvd-live tvs-up" id="tvd-live">
  <div class="tvd-ltabs" role="tablist" aria-label="Pick a sample business">''' + ltabs + '''</div>
  <div class="tvd-stage">
    <div class="tvd-lapf"><div class="tvd-lapf-bar"><i></i><i></i><i></i><span class="tvd-url">dashboard.harborandvine.com</span><em><b></b>Live demo</em></div>
      <div class="tvd-scr" data-w="1366" data-h="854"><img class="tvd-poster" src="''' + poster("restaurant", "desk") + '''" alt="Restaurant dashboard demo, Command Center screen" width="1366" height="854" decoding="async" fetchpriority="high"><div class="tvd-load"><i></i>Starting the live demo</div></div></div>
    <div class="tvd-phf"><div class="tvd-scr tvd-scr-p" data-w="390" data-h="844"><img class="tvd-poster" src="''' + poster("restaurant", "phone") + '''" alt="The same dashboard on a phone" width="390" height="844" decoding="async"><div class="tvd-load"><i></i>Starting</div></div></div>
  </div>
  <div class="tvd-lbar"><p><span class="tvd-pulse"><b></b>Live</span><span><b class="tvd-lname">Harbor &amp; Vine</b>, a sample <span class="tvd-lkind">restaurant</span> with made-up data. It runs itself. Hover to pause, click to take over.</span></p>
    <a class="tvs-btn tvs-blue tvd-full" href="''' + demo_url("restaurant", False) + '''" target="_blank" rel="noopener">Open the full demo &#8599;</a></div>
</div>'''

HERO = '''<section class="tvd-top-sec" id="tvd-top">
  <div class="tvd-top-in tvs-up">
    <p class="tvs-kick"><span class="tvs-dot"></span>New from Three Village Local: Company Digital Dashboards</p>
    <h1>Your whole business.<br><span>One dashboard.</span></h1>
    <p class="tvd-lede">Customers, calendar, money, marketing, social media, reviews and your team, all in one place. Built for your business by our local team, with an AI assistant that tells you what needs you today.</p>
    <div class="tvs-ctas tvd-ctas"><a class="tvs-btn tvs-blue" href="#tvs-book">Book a free demo</a><a class="tvs-btn tvs-ghost" href="#demos">See the live demos</a></div>
    <ul class="tvs-trust tvd-trust"><li><b>20+ screens</b>in one login</li><li><b>''' + NTOOLS + '''</b>tools it connects to</li><li><b>Laptop, tablet</b>and phone</li></ul>
  </div>
''' + APP + '''
</section>'''

# ---------- AI assistant ----------
QA = [("How did we do this week?", "Revenue is $24,860, up 12% on last week. Friday and Saturday dinner did most of the lifting. Lunch was flat. Want me to draft a lunch special post?"),
      ("Who are my best customers?", "Your top 20 guests spent $18,400 this year. Alicia M. visits most (31 times). 4 regulars haven&#39;t been in for 60+ days, so I queued a welcome-back offer for your OK."),
      ("Why is Tuesday slow?", "Tuesdays have been 40% under average for 6 weeks, mostly after 7 PM. Last year a 2-for-1 dessert night lifted Tuesdays 22%. I drafted that post."),
      ("Which invoices are late?", "One: #1039 for J. Alvarez, $925, 6 days late. A reminder went out this morning. Everything else is paid or not yet due."),
      ("What should I post tomorrow?", "Your fall brunch reel is ready. Thursdays 6 to 8 PM get your best reach, so I scheduled it for 6:15 PM, pending your approval.")]
chips = "".join('<button type="button" class="tvd-q" data-i="%d">%s</button>' % (i, q) for i, (q, a) in enumerate(QA))
answers = "".join('<template class="tvd-a" data-i="%d">%s</template>' % (i, a) for i, (q, a) in enumerate(QA))
AI = '''<section class="tvs-sec tvd-ai" id="tvd-ai">
  <div class="tvd-ai-in">
    <div class="tvd-ai-txt tvs-up"><p class="tvs-eyebrow">Your AI business assistant</p><h2>Ask your business anything.</h2>
      <p>No more digging through five apps and three spreadsheets. Ask a question in plain English and get the answer from your own numbers, plus what to do about it.</p>
      <ul class="tvp-ul"><li>Answers from your sales, calendar, customers and marketing</li><li>Spots problems early and suggests the fix</li><li>Drafts posts, replies and offers for your approval</li></ul></div>
    <div class="tvd-chat tvs-up" id="tvd-chat"><div class="tvd-chat-h"><b>&#10022;</b><div><strong>Ask Harbor &amp; Vine</strong><span>Your business assistant</span></div></div>
      <div class="tvd-chat-b" id="tvd-chat-b"><p class="tvd-bot">Hi Sam! Tap a question below to see what I can do.</p></div>
      <div class="tvd-qs">''' + chips + '''</div>''' + answers + '''</div>
  </div></section>'''

# ---------- roles ----------
TILES = [("&#128176;", "Revenue &amp; profit", "o"), ("&#127974;", "Bank &amp; cash", "o"), ("&#128181;", "Payroll", "o"), ("&#128273;", "Password vault", "om"),
         ("&#128200;", "Marketing stats", "om"), ("&#128101;", "Customer list", "om"), ("&#11088;", "Reviews", "om"), ("&#128197;", "Team schedule", "ome"),
         ("&#9989;", "My tasks", "ome"), ("&#128338;", "Time clock", "ome"), ("&#128203;", "Today&#39;s jobs", "ome"), ("&#128247;", "Job photos", "ome")]
tiles = "".join('<div class="tvd-tile" data-r="%s"><span>%s</span><b>%s</b><em>&#128274; Hidden</em></div>' % (r, e, n) for e, n, r in TILES)
ROLES = '''<section class="tvs-sec tvd-roles" id="tvd-roles">
  <div class="tvs-head tvs-up"><p class="tvs-eyebrow">Owner, manager and employee views</p><h2>Everyone sees what they need. Nothing more.</h2>
    <p>Give your team their own logins. You decide who sees money, customers and passwords. Tap a role to see what changes.</p></div>
  <div class="tvd-role-box tvs-up" id="tvd-role" data-role="o">
    <div class="tvd-role-pick" role="group" aria-label="Pick a role"><button type="button" class="on" data-r="o" aria-pressed="true">Owner</button><button type="button" data-r="m" aria-pressed="false">Manager</button><button type="button" data-r="e" aria-pressed="false">Employee</button></div>
    <div class="tvd-role-main"><div class="tvd-role-txt"><b id="tvd-role-t">Owner: the whole picture</b><p id="tvd-role-d">Every number, every screen, every setting. Plus your weekly owner report each Monday morning.</p><span id="tvd-role-n">12 of 12 screens</span></div>
      <div class="tvd-tiles">''' + tiles + '''</div></div>
  </div></section>'''

# ---------- devices ----------
MINI = '''<div class="tvd-mini"><div class="tvd-mini-k"><i></i><i></i><i></i></div><svg viewBox="0 0 100 34" preserveAspectRatio="none" aria-hidden="true"><path d="M0 28 L14 24 L28 26 L42 18 L56 20 L70 12 L84 14 L100 5" fill="none" stroke="#1d5fbf" stroke-width="2.4" vector-effect="non-scaling-stroke"/></svg><div class="tvd-mini-r"><u></u><u></u><u></u></div></div>'''
DEV = '''<section class="tvs-sec tvd-dev" id="tvd-dev">
  <div class="tvs-head tvs-up"><p class="tvs-eyebrow">Everywhere you need it</p><h2>At the desk, on the counter, in the truck.</h2>
    <p>A secure login website that works on any laptop, tablet or phone. Add it to your phone&#39;s home screen and it opens like a mobile app, with alerts when something needs you.</p></div>
  <div class="tvd-devs tvs-up" aria-hidden="true">
    <div class="tvd-lap"><div class="tvd-lap-s"><div class="tvd-lap-side"></div>''' + MINI + '''</div><div class="tvd-lap-b"></div></div>
    <div class="tvd-tab-d"><div class="tvd-tab-s">''' + MINI + '''</div></div>
    <div class="tvd-pho"><div class="tvd-pho-s"><div class="tvd-pho-n"><b>&#128222; Missed call texted back</b>Dana R. replied: &ldquo;Yes, Saturday works!&rdquo;</div>''' + MINI + '''</div></div>
    <span class="tvd-sync">&#10003; Synced just now</span>
  </div>
  <div class="tvd-dev-pts tvs-up"><div><b>&#128187; Laptop</b>The full command center for planning and reports.</div><div><b>&#128203; Tablet</b>Perfect at the front counter, host stand or job site.</div><div><b>&#128241; Phone</b>Approve posts, answer leads and check numbers anywhere.</div></div>
</section>'''

# ---------- automations feed ----------
FEED = [("&#128222;", "Missed call from (631) 555-0142 texted back", "g"), ("&#11088;", "Review request sent to Alicia M.", "y"), ("&#128179;", "Invoice #1043 paid online, $600", "g"),
        ("&#9200;", "Speed-to-lead alarm: new lead answered in 3 min", "b"), ("&#128197;", "Reminder texts sent for tomorrow&#39;s 46 reservations", "b"),
        ("&#128140;", "Win-back offer sent to 4 guests away 60+ days", "p"), ("&#9989;", "Instagram post approved and scheduled for Thu 6:15 PM", "b"),
        ("&#128230;", "Low stock: house red down to 6 cases, reorder drafted", "y"), ("&#128232;", "Weekly owner report delivered", "p"), ("&#127874;", "Birthday treat offered to Priya S.", "g"),
        ("&#9997;", "Catering contract e-signed by Lena W.", "g"), ("&#128269;", "Competitor watch: a new restaurant opened 1 mile away", "y")]
feed_tpl = "".join('<template class="tvd-fe"><li class="%s"><span>%s</span><p>%s</p><em>just now</em></li></template>' % (c, e, t) for e, t, c in FEED)
AUTOS = '''<section class="tvs-sec tvd-feed-sec" id="tvd-auto">
  <div class="tvd-feed-in">
    <div class="tvs-up"><p class="tvs-eyebrow">Automations</p><h2>The busywork runs itself.</h2>
      <p>Follow-ups, reminders, review requests and invoice nudges happen on their own, the same way every time. You see every one in your dashboard as it happens.</p>
      <div class="tvd-hours"><b><span id="tvd-hrs">1,029</span> tasks</b><span>done automatically this month at Harbor &amp; Vine (sample)</span></div></div>
    <div class="tvd-feed tvs-up"><div class="tvd-feed-h"><b><i></i>Live activity</b><span>Today</span></div><ul id="tvd-feed"></ul>''' + feed_tpl + '''</div>
  </div></section>'''

# ---------- industries ----------
IND = [
    ("rest", "&#127869;", "Restaurants", "Covers, food cost and five-star nights.",
     ["Covers and reservations by night", "Sales by menu item", "Food and labor cost %", "Delivery orders and payouts", "Reviews on Google, Yelp and Tripadvisor", "Staff shifts and tip-outs", "Catering and private event leads", "Slow-night alerts with promo ideas"],
     ["Toast", "Square", "OpenTable", "Resy", "7shifts", "DoorDash", "MarginEdge"]),
    ("con", "&#128679;", "Contractors", "Every lead, estimate and job on one board.",
     ["Leads by source", "Estimates sent vs. won", "Job pipeline and schedule", "Profit per job", "Photo timelines for every job", "Change orders and e-signatures", "Crew hours", "Permit and inspection dates"],
     ["Jobber", "Buildertrend", "CompanyCam", "QuickBooks Online", "JobNimbus", "Angi Leads", "Houzz Pro"]),
    ("spa", "&#128135;", "Salons &amp; med spas", "Fuller books and clients who come back.",
     ["Bookings and rebook rate", "No-shows and late cancels", "Revenue per provider", "Retail product sales", "Memberships and packages", "Client notes and before and after photos", "Consent forms", "Reviews and referrals"],
     ["Vagaro", "Boulevard", "GlossGenius", "Mangomint", "Square Appointments", "Fresha", "Instagram"]),
    ("gym", "&#127947;", "Gyms &amp; studios", "Members, classes and retention at a glance.",
     ["Active members and cancellations", "Class attendance and waitlists", "Trial to member conversion", "Personal training sessions", "Failed payments", "Check-ins by hour", "Member health scores", "Challenges and referrals"],
     ["Mindbody", "Glofox", "PushPress", "Zen Planner", "Wodify", "Trainerize", "Stripe"]),
    ("lan", "&#127807;", "Landscapers", "Routes, crews and seasons, handled.",
     ["Daily routes and crews", "Recurring contracts and renewals", "Seasonal upsells: cleanups, aeration, snow", "Job profit and material costs", "Equipment maintenance", "Weather delays", "Estimates and approvals", "Before and after photos"],
     ["LMN", "Aspire", "SingleOps", "Jobber", "Service Autopilot", "QuickBooks Online", "CompanyCam"]),
    ("re", "&#127969;", "Real estate", "Your pipeline, listings and sphere in one CRM.",
     ["Buyer and seller pipeline", "Speed to lead by source", "Listings and showing feedback", "Transactions and key dates", "Past-client touches", "Open house sign-ins", "Commission forecast", "Marketing per listing"],
     ["Follow Up Boss", "kvCORE", "OneKey MLS", "Dotloop", "SkySlope", "ShowingTime", "Zillow Premier Agent"]),
    ("off", "&#128188;", "Offices &amp; pros", "Clients, projects and billable time.",
     ["Client intake", "Projects and deadlines", "Billable hours", "Invoices and payments", "Proposals and e-signatures", "Secure client portal", "Referral sources", "Team workload"],
     ["Clio", "Karbon", "TaxDome", "QuickBooks Online", "Microsoft 365", "DocuSign", "Calendly"]),
    ("ret", "&#128717;", "Retail", "Sales, stock and shoppers in sync.",
     ["Sales by day, hour and item", "Low-stock alerts", "Best and slow sellers", "Online vs. in-store", "Loyalty and repeat shoppers", "Gift cards", "Staff schedule", "Events and foot traffic"],
     ["Shopify", "Square", "Lightspeed Retail", "Clover", "Klaviyo", "Etsy", "Instagram"]),
    ("med", "&#129463;", "Medical &amp; dental", "A smoother front desk and a fuller schedule.",
     ["Appointments and open slots", "No-shows and recalls", "New patient sources", "Production and collections", "Reviews", "Online intake forms", "Staff schedule", "Treatment acceptance"],
     ["Weave", "NexHealth", "Dentrix", "Open Dental", "Jane", "SimplePractice", "Google Calendar"]),
    ("aut", "&#128663;", "Auto repair", "Bays, repair orders and repeat customers.",
     ["Car count and bay use", "Repair orders and average ticket", "Parts orders", "Technician hours", "Approvals by text", "Service reminders", "Reviews", "Fleet accounts"],
     ["Tekmetric", "Shopmonkey", "Mitchell 1", "AutoLeap", "QuickBooks Online", "Podium", "Google Business Profile"]),
]
IDEMO = {"rest": DEMO_BASE + "restaurant.html#/integrations", "con": DEMO_BASE + "contractor.html#/integrations", "spa": DEMO_BASE + "salon.html#/integrations",
         "gym": DEMO_BASE + "gym.html#/integrations", "lan": DEMO_BASE + "landscaper.html#/integrations"}
NAMES = {i["n"] for i in INTEG["items"]}
for _x in IND:
    for _c in _x[5]:
        assert _c in NAMES, "industry chip not in the integrations list: " + _c
itabs = "".join('<button type="button" class="tvd-itab%s" data-i="%s" role="tab" aria-selected="%s"><span>%s</span>%s</button>' % (
    " on" if i == 0 else "", k, "true" if i == 0 else "false", e, n) for i, (k, e, n, t, tr, cn) in enumerate(IND))
ipanes = "".join('''<div class="tvd-ipane%s" data-i="%s" role="tabpanel"%s><div class="tvd-ip-h"><span>%s</span><div><h3>%s</h3><p>%s</p></div></div>
  <div class="tvd-ip-b"><div><p class="tvd-ip-k">Your dashboard tracks</p><ul>%s</ul></div><div><p class="tvd-ip-k">Popular connections</p><div class="tvd-ip-c">%s</div>
  <a class="tvd-ip-more" href="%s" target="_blank" rel="noopener">See Integrations inside a live demo &#8599;</a></div></div></div>''' % (
    " on" if i == 0 else "", k, "" if i == 0 else " hidden", e, n, t, "".join("<li>%s</li>" % x for x in tr),
    "".join('<span>%s</span>' % escape(c) for c in cn), IDEMO.get(k, DEMO_BASE + "restaurant.html#/integrations")) for i, (k, e, n, t, tr, cn) in enumerate(IND))
INDS = '''<section class="tvs-sec tvd-ind" id="tvd-ind">
  <div class="tvs-head tvs-up"><p class="tvs-eyebrow">Built for your industry</p><h2>Made for the way your business works.</h2><p>Every dashboard starts with what matters most in your line of work. Pick yours.</p></div>
  <div class="tvd-ind-box tvs-up"><div class="tvd-itabs" role="tablist" aria-label="Industries">''' + itabs + '''</div>''' + ipanes + '''</div>
</section>'''

# ---------- features ----------
FEATS = [("&#128222;", "Missed-call text-back", "Miss a call and the caller gets a friendly text right away, so they don&#39;t call the next business."),
         ("&#9200;", "Speed-to-lead alarm", "A new lead waiting more than 5 minutes? Your phone buzzes, then your manager&#39;s."),
         ("&#128154;", "Customer health scores", "See who&#39;s loyal and who&#39;s slipping away, then send a win-back offer in one tap."),
         ("&#128176;", "Profit view", "Real profit by job, service or menu item, not just sales."),
         ("&#128200;", "Forecasts and slow-day alerts", "See the next 30 days coming, with a heads-up and an idea before a slow day."),
         ("&#128232;", "Weekly owner report", "Every Monday: what happened, what changed and what to do next, in plain English."),
         ("&#128276;", "Smart reminders", "Appointment, follow-up and renewal reminders by text and email."),
         ("&#9997;", "Digital forms and e-signatures", "Intake forms, waivers, quotes and contracts signed on any phone."),
         ("&#128179;", "Online payments and invoice reminders", "Send invoices, take deposits and let friendly reminders do the chasing."),
         ("&#128230;", "Inventory alerts", "Know before you run out of your best sellers, with reorders drafted."),
         ("&#128247;", "Photo timelines", "Every job or visit documented with before, during and after photos."),
         ("&#129489;", "Employee tools", "Time clock, schedules, checklists and training in each person&#39;s own login."),
         ("&#128269;", "Competitor and local watch", "Track nearby competitors&#39; ratings and what&#39;s happening around town."),
         ("&#128100;", "Customer self-service portal", "Customers see their bookings, invoices and documents, and pay online."),
         ("&#128242;", "QR codes", "For reviews, menus, sign-ins and offers, each one tracked so you know what works."),
         ("&#129309;", "Referral tracking", "See who sends you business, and thank them automatically."),
         ("&#127970;", "Multi-location view", "Every location side by side, or one at a time."),
         ("&#128272;", "Password vault and quick links", "Your logins in an encrypted vault, plus one-tap links to every tool you use."),
         ("&#11088;", "Three Village Local stats built in", "See how your listing, features and promotions on Three Village Local are doing."),
         ("&#10024;", "AI assistant", "Ask your business anything and get answers from your own numbers.")]
feats = "".join('<div class="tvd-feat"><span>%s</span><div><h3>%s</h3><p>%s</p></div></div>' % f for f in FEATS)
FEAT = '''<section class="tvs-sec tvd-feats" id="tvd-feats">
  <div class="tvs-head tvs-up"><p class="tvs-eyebrow">The deep end</p><h2>Twenty ways it pays for itself.</h2><p>Every dashboard can include any of these. We start with what will make the biggest difference for you.</p></div>
  <div class="tvd-fgrid tvs-up">''' + feats + '''</div></section>'''

# ---------- integrations teaser ----------
BYN = {x["n"]: x for x in INTEG["items"]}
WALLN = [n for n in INTEG["wall"] if BYN[n].get("s")]
for _n in ["Google Sheets", "YouTube Analytics", "Google Ads", "Gusto", "Pinterest", "Google Business Profile", "Microsoft Teams", "Slack", "Etsy", "Square Appointments"]:
    if len(WALLN) < 30 and _n in BYN and BYN[_n].get("s") and _n not in WALLN and BYN[_n]["s"] not in {BYN[x]["s"] for x in WALLN}:
        WALLN.append(_n)


def wtile(x):
    if x.get("s"):
        return '<span style="--c:#%s"><i style="-webkit-mask-image:url(%s%s.svg);mask-image:url(%s%s.svg)"></i><em>%s</em></span>' % (x["h"], CDN, x["s"], CDN, x["s"], escape(x["n"]))
    w = x["n"].split()
    mono = {"OpenAI API (ChatGPT)": "GPT"}.get(x["n"], (w[0][0] + w[1][0]) if len(w) > 1 else x["n"][:2])
    return '<span class="m" style="--c:#%s"><b>%s</b><em>%s</em></span>' % (x.get("h", "1d5fbf"), escape(mono.upper()), escape(x["n"]))


wall = "".join(wtile(BYN[n]) for n in WALLN[:30])
INT = '''<section class="tvs-sec tvd-int" id="tvd-int">
  <div class="tvd-int-in tvs-up"><div class="tvd-int-txt"><p class="tvs-eyebrow">Built into every dashboard: Integrations</p><h2>Connects with ''' + NTOOLS + ''' tools.</h2>
    <p>Every dashboard has its own Integrations screen. Connect your POS, accounting, booking, Google, Microsoft 365, social media and AI tools, and the numbers flow in on their own. We only list tools with a real way in: an official sign-in or API, a standard feed, or the tool&#39;s own export.</p>
    <ul class="tvd-int-k"><li><b>''' + str(NT["api"]) + '''</b><span>connect directly with their official sign-in or API</span></li><li><b>''' + str(NT["feed"]) + '''</b><span>connect by a standard feed (MLS, calendar, email)</span></li><li><b>''' + str(NT["export"]) + '''</b><span>connect through their own report or file export</span></li></ul>
    <div class="tvs-ctas"><a class="tvs-btn tvs-blue" href="''' + DEMO_BASE + '''restaurant.html#/integrations" target="_blank" rel="noopener">See it inside a demo &#8599;</a><a class="tvs-btn tvs-ghost" href="#tvs-book">Ask about my software</a></div></div>
    <div class="tvd-wall" aria-label="A few of the tools a dashboard connects to">''' + wall + '''</div></div></section>'''

# ---------- security ----------
SEC = '''<section class="tvs-sec tvd-sec" id="tvd-sec">
  <div class="tvs-head tvs-up"><p class="tvs-eyebrow">Security and privacy</p><h2>Your business stays yours.</h2></div>
  <div class="tvd-secg tvs-up">
    <div><span>&#128190;</span><h3>You own your data</h3><p>Your customer list, numbers and files belong to you. Ask for a full export anytime.</p></div>
    <div><span>&#128101;</span><h3>Role permissions</h3><p>Owners, managers and employees each see only what you allow.</p></div>
    <div><span>&#128272;</span><h3>Encrypted password vault</h3><p>Logins are stored encrypted, and only the people you choose can open them.</p></div>
    <div><span>&#128273;</span><h3>Your own logins</h3><p>Tools connect through their official sign-in, approved by you. You can disconnect anytime.</p></div>
    <div><span>&#128584;</span><h3>We never see your passwords</h3><p>Connections use secure sign-in tokens, so your passwords are never shared with us.</p></div>
    <div><span>&#129463;</span><h3>Health records stay put</h3><p>For medical and dental offices, patient health records stay in your practice system. Your dashboard shows business numbers.</p></div>
  </div></section>'''

# ---------- process ----------
STEPS = [("Free demo", "See a dashboard built for your industry and ask anything. No pressure."),
         ("Discovery", "We learn how you work, which tools you use and what you want to see every morning."),
         ("We build it", "Our local team designs your screens, connects your tools and sets up your automations."),
         ("Launch and training", "We walk you and your team through it, on every device, until it feels easy."),
         ("Ongoing updates", "New screens, reports and automations as your business grows. Just ask.")]
steps = "".join('<li><b>%d</b><h3>%s</h3><p>%s</p></li>' % (i + 1, t, d) for i, (t, d) in enumerate(STEPS))
HOW = '''<section class="tvs-sec tvd-how" id="tvd-how">
  <div class="tvs-head tvs-up"><p class="tvs-eyebrow">How it works</p><h2>From first call to launch day.</h2><p>We do the heavy lifting. You tell us how your business runs.</p></div>
  <ol class="tvd-steps tvs-up">''' + steps + '''</ol>
  <div class="tvp-ctas tvp-ctas-c tvs-up"><a class="tvs-btn tvs-blue" href="#tvs-book">Book a free demo</a></div></section>'''

# ---------- demos ----------
DPTS = {"restaurant": ["Covers, reservations and food cost", "Catering and private events", "Slow-night promos"], "contractor": ["Leads to signed jobs", "Profit per job", "Photo timelines and permits"],
        "salon": ["Rebook rate and waitlist", "Memberships and retail", "Client formulas and photos"], "gym": ["Check-ins and classes", "Members at risk", "Trials to members"],
        "landscaper": ["Routes and crews", "Contracts and renewals", "Seasonal upsells"], "realestate": ["Speed to lead", "Pipeline and closings", "Past-client touches"]}
demos = "".join('''<div class="tvd-demo"><button type="button" class="tvd-demo-v" data-watch="%s" aria-label="Watch the %s demo live"><span class="tvd-demo-bar"><i></i><i></i><i></i><u>%s</u></span><img src="%s" alt="%s dashboard demo" width="1366" height="854" loading="lazy" decoding="async"><span class="tvd-play">&#9654; Watch it live</span></button>
  <div class="tvd-demo-t"><em>%s</em><h3>%s</h3><ul>%s</ul><a class="tvd-open" href="%s" target="_blank" rel="noopener">Open the full demo &#8599;</a></div></div>''' % (
    k, kd, u, poster(k, "desk"), kd, kd, b, "".join("<li>%s</li>" % x for x in DPTS[k]), demo_url(k, False)) for k, t, e, b, kd, u in LIVE_DEMOS)
DEMO = '''<section class="tvs-sec tvd-demos" id="demos">
  <div class="tvs-head tvs-up"><p class="tvs-eyebrow">Try the live demos</p><h2>Six sample businesses. Six real dashboards.</h2>
    <p>These are working dashboards, not pictures. Open one, switch between the owner, manager and employee views, connect an integration, approve a post. Everything runs on made-up sample data.</p></div>
  <div class="tvd-dgrid tvs-up">''' + demos + '''</div>
  <p class="tvd-note">Sample businesses and people are fictional, for demonstration only.</p>
  <div class="tvp-ctas tvp-ctas-c tvs-up"><a class="tvs-btn tvs-blue" href="#tvs-book">Book a free demo</a></div></section>'''

# ---------- FAQ ----------
FAQS = [("What is a Company Digital Dashboard?", "It is one secure place where you see and run your whole business: customers and leads, calendar, money, marketing, social media, reviews, your team and automations. Three Village Local builds it around how your business works and connects it to the tools you already use."),
        ("Do I have to stop using my current software?", "No. Keep what works. Your dashboard connects to your POS, accounting, booking and marketing tools and brings the important numbers together, so you stop jumping between them."),
        ("How much does it cost?", "Every dashboard is custom, so pricing depends on how many dashboards and logins you need, which tools we connect, the features you choose and your Three Village Local membership. Book a free demo and we will send you a clear custom quote, with no pressure."),
        ("How long does it take to build?", "It depends on the screens and connections you want. We give you a timeline with your quote, and we launch in stages, so you start using the most important screens first."),
        ("Does it work on my phone?", "Yes. It is a secure login website that works on any laptop, tablet or phone. Add it to your phone&#39;s home screen and it opens like a mobile app."),
        ("Can my employees use it?", "Yes. Each person gets their own login, and you choose what owners, managers and employees can see. For example, employees can see their schedule and jobs without seeing your bank balance."),
        ("Who owns my data, and is it secure?", "You own your data and can ask for a full export anytime. Tools connect through their official sign-in, you can disconnect them anytime, and saved logins are kept in an encrypted vault."),
        ("What if my software isn&#39;t on your list?", "Ask us. If it has an export or an API, we can usually connect it. If not, we will suggest the simplest way to get those numbers in."),
        ("Do I need to be a Three Village Local member?", "No. Any business can get a dashboard. Members get special member pricing, and their Three Village Local stats show up right inside it."),
        ("What happens after launch?", "We stay with you. We train your team, keep your connections running and add new screens, reports and automations as your business grows.")]
faq_html = "".join('<details%s><summary>%s</summary><p>%s</p></details>' % (" open" if i == 0 else "", q, a) for i, (q, a) in enumerate(FAQS))
FAQ = '''<section class="tvs-sec tvs-faq" id="tvd-faq">
  <div class="tvs-head tvs-up"><p class="tvs-eyebrow">Questions</p><h2>Good questions, straight answers.</h2></div>
  <div class="tvs-qs tvs-up">''' + faq_html + '''</div></section>'''


def plain(s):
    return s.replace("&#39;", "'").replace("&amp;", "&")


LD = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in FAQS]}
D.HEAD = '<script type="application/ld+json">' + json.dumps(LD, ensure_ascii=False, separators=(",", ":")) + "</script>"
# share tags BD does not write itself (same format as svc-kit share_meta)
_SIMG = "https://threevillagelocal-cloud.github.io/3vl-share/site/services/share/svc-business-dashboards-v1.jpg"
_SALT = "Three Village Local Company Digital Dashboards: Your business. One dashboard. Leads, money and AI on a laptop and phone."
D.HEAD += ('<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
           '<meta property="og:image:type" content="image/jpeg"><meta property="og:image:alt" content="%s">'
           '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="%s">'
           '<meta name="twitter:image:alt" content="%s">' % (_SALT, _SIMG, _SALT))
assert "\\" not in D.HEAD

CTA = '''<section class="tvw-cta3 tvs-up"><div class="tvw-cta3-in"><p class="tvw-cta3-k">Run your business from one screen</p><h2>See your dashboard in action.</h2>
<p class="tvw-cta3-s">Book a free demo. We&#39;ll show you a dashboard built for your industry and send a custom quote.</p>
<div class="tvw-cta-btns"><a class="tvs-btn tvw-btn-w" href="#tvs-book">Book a free demo</a><a class="tvs-btn tvw-btn-o" href="#demos">Try the live demos</a></div></div></section>'''

BOOK = P.BOOK.replace('<p class="tvs-eyebrow">Your free plan</p>', '<p class="tvs-eyebrow">Free demo</p>').replace(
    "<h2>Get your free plan.</h2>", "<h2>Book your free demo.</h2>")
i = BOOK.index("<p>Tell us your name, business and email.")
j = BOOK.index('<div class="tvp-proof">')
BOOK = BOOK[:i] + '''<p>Tell us your name, business and email. Within one business day we&#39;ll reach out by email to set up your free demo:</p>
    <ul class="tvp-get"><li>A walkthrough of a dashboard for your industry</li><li>Which of your tools we can connect</li><li>A custom quote, no pressure</li></ul>
    ''' + BOOK[j:]
BOOK = BOOK.replace("mailto:hello@threevillagelocal.com?subject=Our%20services", "mailto:hello@threevillagelocal.com?subject=Dashboard%20demo")
i = BOOK.index('<p class="tvp-alt">')
BOOK = BOOK[:i] + '<p class="tvp-alt">Using lots of software? <a href="' + DEMO_BASE + 'restaurant.html#/integrations" target="_blank" rel="noopener">See the Integrations screen in a live demo &#8599;</a></p>' + BOOK[BOOK.index("</p>", i) + 4:]

HTML = ('<div class="tvs tvd" id="tvs">\n\n' + HERO + "\n\n" + AI + "\n\n" + ROLES + "\n\n" + DEV + "\n\n" + AUTOS + "\n\n" + INDS + "\n\n" +
        FEAT + "\n\n" + INT + "\n\n" + SEC + "\n\n" + HOW + "\n\n" + DEMO + "\n\n" + FAQ + "\n\n" + CTA + "\n\n" + BOOK +
        '\n\n<a class="tvs-sticky tvd-sticky" href="#tvs-book">Book a free demo</a>\n</div>')
# keep hyphenated words on one line (never split at the hyphen), text only, never inside tags
HTML = re.sub(r'>([^<]+)<', lambda m: '>' + re.sub(r'(?<![A-Za-z0-9&#;.-])([A-Za-z0-9.()]+(?:-[A-Za-z0-9.,]+)+)', r'<nobr>\1</nobr>', m.group(1)) + '<', HTML)
assert "\\" not in HTML and chr(0x2014) not in HTML
assert "preview-integrations" not in HTML and 'href="/integrations' not in HTML

CSS = open(os.path.join(HERE, "dash.css"), encoding="utf-8").read()
JS = open(os.path.join(HERE, "dash.js"), encoding="utf-8").read()


def rd(f):
    if f == "page.html":
        return HTML
    s = P.rd(f)
    if f == "page.css":
        assert "\\" not in CSS
        return s + CSS
    if f == "page.js":
        s = s.replace("Get My Free Plan", "Book My Free Demo").replace(
            'data-tease="Want a quick free plan? Tell me your business name and I will point you to the right fit."',
            'data-tease="Curious what a dashboard could do for your business? Ask me."')
        assert "var pick='not_sure'" in s
        s = s.replace("var pick='not_sure'", "var pick='dashboards'")   # form 343 field "bundle": Company Digital Dashboard
        s = s + "<script>" + JS + "</script>"
        assert "\\" not in s
        return s
    return s


D.rd = rd
if __name__ == "__main__":
    D.main()
