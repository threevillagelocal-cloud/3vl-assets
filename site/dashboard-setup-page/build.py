"""Company Digital Dashboards: "Build your dashboard" setup wizard. A business fills out what we need to build its custom
dashboard (10 skippable steps, uploads, a comment box on every section, a note on any option, AI helper chat). Phone first, no prices.
    python site/dashboard-setup-page/build.py          -> widget "3VL Page Dashboard Setup Preview" + hidden /preview-dashboard-setup (noindex)
    python site/dashboard-setup-page/build.py --dry    -> writes _local.html (for a local look) and prints sizes, publishes nothing
- The wizard is drawn by setup.js (no backslashes anywhere: BD strips them from widget code). Answers autosave to localStorage.
- Uploads + final submit go to the assistant's /api/intake (client "dashboard-setup").
- Chat: widget.js with data-bot="dashsetup".
- Integrations list = site/integrations-page/integrations_data.py + icons.json (Simple Icons pinned); brand colors from the same
  Simple Icons version (cached in si_hex.json)."""
import json, os, re, sys, urllib.request, zlib

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(SITE, "integrations-page"))
sys.path.insert(0, os.path.join(SITE, "services-page"))
import integrations_data as ID
import deploy as D       # the shared BD publisher (widget + page). Deliberately NOT via svc-kit/platform-page (independent of their builds)


def _kit_icons():   # the stroke icon set from svc-kit/kit.py, read from its source so this build never runs the platform-page build
    src = open(os.path.join(SITE, "svc-kit", "kit.py"), encoding="utf-8").read()
    i = src.index("_I = {")
    j = src.index(chr(10) + "}" + chr(10), i)
    ns = {}
    exec(src[i:j + 3], {}, ns)
    return ns["_I"]


class K:
    _I = _kit_icons()


LIVE = D.LIVE
assert not LIVE or os.environ.get("TVX_LIVE_OK") == "1", "live publish needs the owner's OK (set TVX_LIVE_OK=1)"
D.NAME = "3VL Page Dashboard Setup" if LIVE else "3VL Page Dashboard Setup Preview"
D.SLUG = "dashboard-setup" if LIVE else "preview-dashboard-setup"
D.TITLE = "Build Your Dashboard: Company Digital Dashboard Setup | Three Village Local"
D.DESC = ("Tell us how your business runs, who needs access and which tools you use, and Three Village Local will design your custom "
          "all-in-one business dashboard: CRM, calendar, money, marketing, reviews, team and automations.")
D.FB_TITLE = "Build your business dashboard."
D.FB_IMAGE = "/share/svc-business-dashboards-v1.jpg"
D.HEAD = ""
D.FORM = ""

# ---------- icons ----------
EXTRA = {
    "leaf": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.5 19 2c1 2 2 4.2 2 8 0 5.5-4.8 10-10 10z"/><path d="M2 21c0-3 1.9-5.4 5.1-6"/>',
    "med": '<rect x="3" y="3" width="18" height="18" rx="4"/><path d="M12 8v8M8 12h8"/>',
    "car": '<path d="M3 13l2-6h14l2 6v5H3z"/><circle cx="7.5" cy="17.5" r="1.5"/><circle cx="16.5" cy="17.5" r="1.5"/><path d="M3 13h18"/>',
    "card": '<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20M6 15h4"/>',
    "box": '<path d="m21 8-9-5-9 5v8l9 5 9-5z"/><path d="m3 8 9 5 9-5M12 13v8"/>',
    "clipboard": '<rect x="5" y="4" width="14" height="18" rx="2"/><path d="M9 2h6v4H9zM9 12h6M9 16h4"/>',
    "lock": '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
    "sign": '<path d="M3 17c3-3 5-6 6-6s-1 6 1 6 3-4 5-4 1 4 3 4 2-2 3-2"/><path d="M3 21h18"/>',
    "building": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 22v-4h6v4M8 6h1M12 6h1M16 6h-1M8 10h1M12 10h1M16 10h-1M8 14h1M12 14h1M16 14h-1"/>',
    "idcard": '<rect x="2" y="5" width="20" height="14" rx="2"/><circle cx="8" cy="11" r="2.5"/><path d="M14 10h5M14 14h4M4.5 17a4 4 0 0 1 7 0"/>',
    "funnel": '<path d="M3 4h18l-7 8v6l-4 2v-8z"/>',
    "door": '<path d="M3 21h18M6 21V4a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v17"/><path d="M14 12h.5"/>',
    "laptop": '<rect x="4" y="5" width="16" height="11" rx="1.5"/><path d="M2 19h20"/>',
    "tablet": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M11 18h2"/>',
    "monitor": '<rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/>',
    "kiosk": '<rect x="6" y="2" width="12" height="13" rx="2"/><path d="M12 15v5M8 21h8M9 11h6"/>',
    "tv": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="m17 2-5 5-5-5"/>',
    "upload": '<path d="M12 16V4M7 9l5-5 5 5"/><path d="M4 16v3a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-3"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "x": '<path d="M18 6 6 18M6 6l12 12"/>',
    "help": '<circle cx="12" cy="12" r="10"/><path d="M9.1 9a3 3 0 0 1 5.8 1c0 2-3 3-3 3M12 17h.01"/>',
    "palette": '<circle cx="13.5" cy="6.5" r="1.5"/><circle cx="17.5" cy="10.5" r="1.5"/><circle cx="8.5" cy="7.5" r="1.5"/><circle cx="6.5" cy="12.5" r="1.5"/><path d="M12 2a10 10 0 0 0 0 20c1 0 1.6-.8 1.6-1.7 0-.5-.2-.8-.5-1.1-.3-.3-.4-.7-.4-1.1 0-.9.8-1.7 1.7-1.7H16a6 6 0 0 0 6-6c0-4.9-4.5-8.4-10-8.4z"/>',
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "plug": '<path d="M9 2v6M15 2v6M6 8h12v4a6 6 0 0 1-12 0zM12 18v4"/>',
    "send": '<path d="m22 2-7 20-4-9-9-4z"/><path d="M22 2 11 13"/>',
    "image": '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="m21 15-5-5L5 21"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    "refresh": '<path d="M21 12a9 9 0 1 1-3-6.7L21 8"/><path d="M21 3v5h-5"/>',
    "back": '<path d="M19 12H5M11 18l-6-6 6-6"/>',
    "skip": '<path d="m5 4 10 8-10 8z"/><path d="M19 5v14"/>',
    "sheet": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M3 15h18M9 3v18"/>',
    "save": '<path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><path d="M17 21v-8H7v8M7 3v5h8"/>',
}
ICONS = dict(K._I)
ICONS.update(EXTRA)


def svg(name):
    return '<svg class="tds-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % ICONS[name]


# ---------- the questionnaire data ----------
INDUSTRIES = [("restaurant", "Restaurant or cafe", "utensils"), ("contractor", "Contractor or trades", "hammer"), ("salon", "Salon or spa", "scissors"),
              ("gym", "Gym or fitness", "dumbbell"), ("landscaper", "Landscaping", "leaf"), ("realestate", "Real estate", "home"),
              ("medical", "Medical or dental", "med"), ("legal", "Legal or professional", "briefcase"), ("retail", "Retail shop", "store"),
              ("auto", "Auto repair", "car"), ("other", "Something else", "grid")]
MODULES = [
    ("crm", "CRM and client profiles", "Every customer in one place: contact info, history, notes and files.", "users"),
    ("leads", "Lead pipeline", "Every new inquiry from calls, forms, chat and social, tracked until it's a yes.", "funnel"),
    ("calendar", "Calendar and scheduling", "Appointments, jobs, shifts and reminders on one shared calendar.", "calendar"),
    ("booking", "Online booking", "Customers book themselves, day or night, into your real availability.", "clock"),
    ("finance", "Finance", "Sales, invoices, expenses and cash flow, with real profit, not just sales.", "chart"),
    ("payments", "Payments and invoicing", "Send invoices, take deposits and let friendly reminders do the chasing.", "card"),
    ("marketing", "Marketing and analytics", "Website, Google Business Profile, social media and email stats in one view.", "globe"),
    ("social", "Social content studio", "Plan, create and schedule posts, with approvals before anything goes out.", "megaphone"),
    ("reviews", "Reviews and reputation", "See every review, reply fast and ask happy customers for more.", "star"),
    ("tasks", "Tasks and team", "Assign tasks, checklists and follow-ups, and see what got done.", "list"),
    ("employees", "Employee profiles, time clock and PTO", "Profiles, schedules, clock in and out, and time off requests.", "idcard"),
    ("inventory", "Inventory", "Stock levels, low-stock alerts and reorders drafted for you.", "box"),
    ("estimates", "Estimates and proposals", "Build, send and track quotes customers can accept online.", "clipboard"),
    ("jobs", "Jobs and projects", "Every job from first visit to final payment, with photo timelines.", "layers"),
    ("memberships", "Memberships and packages", "Recurring plans, class packs, gift cards and loyalty.", "gift"),
    ("automations", "Automations", "The busywork runs itself. Pick the ones you want below.", "bolt"),
    ("ai", "AI assistant", "Ask your business anything and get answers from your own numbers.", "sparkle"),
    ("chatbot", "Website chatbot leads", "Leads from an AI chat on your website land right in your pipeline.", "bot"),
    ("portal", "Customer portal", "Customers see their bookings, invoices and documents, and pay online.", "door"),
    ("forms", "Forms and e-signatures", "Intake forms, waivers, quotes and contracts signed on any phone.", "sign"),
    ("multiloc", "Multi-location", "Every location side by side, or one at a time.", "building"),
    ("vault", "Password vault and quick links", "Logins in an encrypted vault, plus one-tap links to every tool you use.", "lock"),
    ("tvl", "Three Village Local stats", "How your listing, features and promotions on Three Village Local are doing.", "pin"),
]
AUTOMATIONS = ["Missed-call text back", "Review requests after each visit", "Appointment reminders", "Win-back offers for quiet customers",
               "Invoice and payment reminders", "New lead routing to the right person", "Birthday offers", "Weekly owner report",
               "Speed-to-lead alarm", "Follow-ups after a quote", "Low-stock alerts", "Welcome messages for new customers"]
SUGGEST = {
    "restaurant": ["booking", "reviews", "social", "marketing", "employees", "inventory", "finance", "automations"],
    "contractor": ["leads", "estimates", "jobs", "payments", "forms", "calendar", "employees", "reviews"],
    "salon": ["booking", "crm", "memberships", "reviews", "social", "employees", "payments", "automations"],
    "gym": ["memberships", "booking", "crm", "payments", "social", "forms", "automations"],
    "landscaper": ["estimates", "jobs", "calendar", "payments", "leads", "employees", "automations"],
    "realestate": ["crm", "leads", "calendar", "marketing", "social", "forms", "automations"],
    "medical": ["booking", "reviews", "forms", "portal", "calendar", "employees", "automations"],
    "legal": ["crm", "leads", "forms", "portal", "calendar", "payments"],
    "retail": ["inventory", "finance", "social", "reviews", "marketing", "memberships"],
    "auto": ["estimates", "jobs", "booking", "payments", "reviews", "inventory", "automations"],
}
ROLES = [("owner", "Owner", "Sees everything"), ("partner", "Partner", "Co-owner level access"), ("manager", "Manager", "Runs the day-to-day"),
         ("front", "Front desk", "Customers, calendar and payments"), ("staff", "Staff or crew", "Their own schedule, tasks and jobs"),
         ("contractor", "Contractor or sub", "Only the jobs they're on"), ("bookkeeper", "Bookkeeper or accountant", "The money side only"),
         ("readonly", "Read-only", "Can look, can't change")]
AREAS = [("crm", "Customers"), ("leads", "Leads"), ("calendar", "Calendar"), ("finance", "Money and finance"), ("payments", "Invoices and payments"),
         ("marketing", "Marketing stats"), ("social", "Social studio"), ("reviews", "Reviews"), ("tasks", "Tasks"), ("team", "Team and time clock"),
         ("inventory", "Inventory"), ("jobs", "Jobs and estimates"), ("reports", "Reports"), ("vault", "Password vault"), ("settings", "Settings and billing")]
ALLA = [a for a, _ in AREAS]
ACCESS = {"owner": ALLA, "partner": ALLA,
          "manager": ["crm", "leads", "calendar", "payments", "marketing", "social", "reviews", "tasks", "team", "inventory", "jobs", "reports"],
          "front": ["crm", "leads", "calendar", "payments", "reviews", "tasks"], "staff": ["calendar", "tasks", "team", "jobs"],
          "contractor": ["jobs", "tasks", "calendar"], "bookkeeper": ["finance", "payments", "reports"], "readonly": ["reports", "marketing", "reviews"]}
KPI_GEN = ["Sales today, this week and this month", "Profit", "New leads", "Lead response time", "Booked appointments", "Average sale",
           "Repeat customers", "Google rating and reviews", "Website visits", "Social media reach", "Cash in the bank", "Unpaid invoices",
           "Labor cost", "Where customers come from"]
KPI_IND = {"restaurant": ["Covers per night", "Food cost", "Table turns", "Online orders", "Catering inquiries"],
           "contractor": ["Estimates out", "Jobs won", "Profit per job", "Backlog", "Change orders"],
           "salon": ["Rebook rate", "Retail sales", "Chair utilization", "No-shows"],
           "gym": ["Active members", "Members at risk", "Check-ins", "Trials to members"],
           "landscaper": ["Contract renewals", "Crew hours", "Route efficiency", "Seasonal upsells"],
           "realestate": ["Speed to lead", "Pipeline value", "Closings", "Active listings", "Past-client touches"],
           "medical": ["New patients", "No-show rate", "Recall due", "Treatment acceptance"],
           "legal": ["New matters", "Billable hours", "Collections", "Intake conversions"],
           "retail": ["Best sellers", "Inventory turns", "Basket size", "Foot traffic"],
           "auto": ["Car count", "Average repair order", "Bay utilization", "Declined work"]}

# integrations: curated list + pinned Simple Icons logos + brand colors
IC = json.load(open(os.path.join(SITE, "integrations-page", "icons.json"), encoding="utf-8"))
SIV = IC["version"]
HEXF = os.path.join(HERE, "si_hex.json")
if not os.path.exists(HEXF):
    data = json.loads(urllib.request.urlopen(urllib.request.Request("https://cdn.jsdelivr.net/npm/simple-icons@%s/data/simple-icons.json" % SIV,
                                                                    headers={"User-Agent": "Mozilla/5.0 3VL"}), timeout=60).read())
    hx = {}
    for x in data:
        s = x.get("slug") or re.sub(r"[^a-z0-9]", "", x["title"].lower().replace("+", "plus").replace(".", "dot").replace("&", "and"))
        hx[s] = x["hex"]
    want = set(IC["icons"].values())
    json.dump({k: v for k, v in sorted(hx.items()) if k in want}, open(HEXF, "w"), indent=0)
SIHEX = json.load(open(HEXF))
DJ = json.load(open(os.path.join(SITE, "dashboards-page", "dash_integrations.json"), encoding="utf-8"))
DHEX = {i["n"]: i.get("h") for i in DJ["items"] if i.get("h")}


def lum(h):
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


CATI = {k: n for n, (k, _) in enumerate(ID.CATS)}
TOOLS = []
for it in ID.ITEMS:
    name, cat, conn, what = it[:4]
    slug = IC["icons"].get(name) or ""
    hx = DHEX.get(name) or SIHEX.get(slug) or ""
    if hx and lum(hx) > 0.78:
        hx = "13294B"
    if not hx:
        hx = "%d" % (zlib.crc32(name.encode()) % 360)   # hue for the letter tile
    TOOLS.append([name, CATI[cat], conn, what, slug, hx])
NAMES = {t[0] for t in TOOLS}
POP_GEN = ["Square", "QuickBooks Online", "Google Business Profile", "Google Calendar", "Gmail", "Instagram", "Facebook", "Mailchimp",
           "Stripe", "Gusto", "Calendly", "Shopify", "Google Reviews", "Yelp", "Google Sheets", "Canva", "Zoom", "Dropbox", "Clover", "Toast"]
POP = {"gen": [n for n in POP_GEN if n in NAMES]}
for k, v in DJ["pop"].items():
    POP[k] = [n for n in v if n in NAMES][:16]
for k in POP:
    for n in ["Google Business Profile", "Gmail", "QuickBooks Online", "Instagram", "Facebook"]:
        if n not in POP[k] and len(POP[k]) < 20:
            POP[k].append(n)
NTOOLS = len(TOOLS)

CFG = {
    "api": "https://3vl-ai-assistant.vercel.app/api/intake",
    "cdn": "https://cdn.jsdelivr.net/npm/simple-icons@%s/icons/" % SIV,
    "ic": {k: svg(k).replace('"', "'") for k in ICONS},   # single quotes: json.dumps would escape double quotes with backslashes
    "ind": INDUSTRIES, "mods": MODULES, "autos": AUTOMATIONS, "sug": SUGGEST, "roles": ROLES, "areas": AREAS, "access": ACCESS,
    "kpig": KPI_GEN, "kpii": KPI_IND, "cats": [c[1] for c in ID.CATS], "tools": TOOLS, "pop": POP, "ntools": NTOOLS,
    "conn": {"D": "Direct connection", "E": "Via export", "C": "Custom build", "B": "Built in"},
}

# ---------- page shell (the steps are drawn by setup.js) ----------
I = svg
HTML = '''<div class="tds" id="tds">
<section class="tds-hero">
  <div class="tds-hin">
    <p class="tds-crumbs"><a href="/services">Our services</a><span>/</span>Company Digital Dashboards</p>
    <p class="tds-kick"><span class="tds-dot"></span>Build your dashboard</p>
    <h1>Let&#39;s build your<br><span>business dashboard.</span></h1>
    <p class="tds-sub">Tell us how your business runs, who needs access and which tools you use. Our local team designs your custom dashboard around it, then sends you a custom quote.</p>
    <ul class="tds-facts">
      <li>''' + I("clock") + '''<span>About 15 to 20 minutes</span></li>
      <li>''' + I("save") + '''<span>Saves as you go</span></li>
      <li>''' + I("skip") + '''<span>Skip anything</span></li>
      <li>''' + I("bot") + '''<span>AI helper on call</span></li>
    </ul>
    <div class="tds-resume" id="tds-resume" hidden></div>
    <div class="tds-ctas"><button type="button" class="tds-btn tds-blue" data-go="start">Start my setup''' + I("arrow") + '''</button><button type="button" class="tds-btn tds-ghost" data-ask="How does this dashboard setup work, and what will I need?">Ask a question first</button></div>
  </div>
  <div class="tds-hvis"><p class="tds-pvk"><span></span>Your dashboard, live as you answer</p><div id="tds-prev"></div></div>
</section>

<section class="tds-wiz" id="tds-wiz" aria-label="Dashboard setup">
  <aside class="tds-rail" id="tds-rail"></aside>
  <div class="tds-main">
    <div class="tds-top" id="tds-top"></div>
    <div class="tds-flash" id="tds-flash" hidden role="status"></div>
    <div class="tds-step" id="tds-step"></div>
    <div class="tds-nav" id="tds-nav"></div>
  </div>
</section>

<section class="tds-trust">
  <div>''' + I("shield") + '''<p><b>Your business stays yours.</b>What you share here is only used to design your dashboard. We never ask for passwords on this page.</p></div>
  <div>''' + I("plug") + '''<p><b>Keep the tools you love.</b>Your dashboard connects to ''' + str(NTOOLS // 50 * 50) + '''+ tools you already use and brings the numbers together.</p></div>
  <div>''' + I("phone") + '''<p><b>Works everywhere.</b>A secure login website for laptop, tablet and phone. Add it to your home screen and it opens like a mobile app.</p></div>
</section>

<div class="tds-modal" id="tds-modal" hidden role="dialog" aria-modal="true" aria-labelledby="tds-mh">
  <div class="tds-mbox">
    <div class="tds-mhead"><div><p class="tds-eyebrow">Integrations</p><h2 id="tds-mh">All ''' + str(NTOOLS) + ''' tools we connect</h2></div><button type="button" class="tds-mx" data-modal="close" aria-label="Close">''' + I("x") + '''</button></div>
    <div class="tds-mtools"><label class="tds-search">''' + I("search") + '''<input type="search" id="tds-msrch" placeholder="Search tools, like QuickBooks" aria-label="Search all integrations"></label>
      <select id="tds-mcat" aria-label="Category"><option value="">All categories</option></select></div>
    <p class="tds-mleg"><span class="cx cx-D">Direct connection</span> official sign-in or API, updates on its own <span class="cx cx-E">Via export</span> reports or files on a schedule <span class="cx cx-C">Custom build</span> needs a special feed</p>
    <div class="tds-mlist" id="tds-mlist"></div>
  </div>
</div>
<input type="text" class="tds-hp" id="tds-hp" name="company_website" tabindex="-1" autocomplete="off" aria-hidden="true">
</div>
<script src="https://3vl-ai-assistant.vercel.app/widget.js" data-bot="dashsetup" data-tease="Questions while you fill this out? Ask me anything." defer></script>'''

CSS = open(os.path.join(HERE, "setup.css"), encoding="utf-8").read()
# BD's theme has #first_container *{white-space:normal!important}: re-assert every nowrap we use with an id-level selector (as svc-kit does)
_sels = []
for _m in re.finditer(r"([^{}]+)\{[^{}]*white-space:nowrap", CSS):
    for _sel in re.sub(r"/[*].*?[*]/", "", _m.group(1), flags=re.S).split(","):
        _sel = _sel.strip()
        if _sel and not _sel.startswith("@") and not _sel.startswith("#tds") and _sel not in _sels:
            _sels.append(_sel)
CSS += ",".join("#tds " + (x[5:] if x.startswith(".tds ") else x) for x in _sels if not x.startswith(".tds{")) + "{white-space:nowrap!important}"
JS = open(os.path.join(HERE, "setup.js"), encoding="utf-8").read()
CFGJS = json.dumps(CFG, ensure_ascii=False, separators=(",", ":"))
FULL_JS = "<script>window.TDS_CFG=" + CFGJS + ";\n" + JS + "</script>"

for nm, s in [("html", HTML), ("css", CSS), ("js", FULL_JS)]:
    assert "\\" not in s, nm + " has a backslash (BD strips them)"
    assert "—" not in s and "–" not in s and "&mdash;" not in s and "&ndash;" not in s, nm + " has an em/en dash"
    assert "$" not in s, nm + " has a dollar sign (no prices)"
    assert "[widget=" not in s and "[form=" not in s and "%%" not in s, nm + " has a BD shortcode-like token"
assert FULL_JS.count("</script>") == 1


def rd(f):
    return {"page.html": HTML, "page.css": CSS, "page.js": FULL_JS}[f]


D.rd = rd

if __name__ == "__main__":
    if "--dry" in sys.argv:
        local = ('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
                 '<title>local</title><link href="https://fonts.googleapis.com/css2?family=Radio+Canada:wght@400;500;600;700&display=swap" rel="stylesheet">'
                 '<style>body{margin:0;background:#f4f7fb}' + CSS + '</style></head><body><div id="first_container" style="padding:20px 0">' + HTML + '</div>' + FULL_JS + '</body></html>')
        open(os.path.join(HERE, "_local.html"), "w", encoding="utf-8").write(local)
        print("html", len(HTML), "css", len(CSS), "js", len(FULL_JS), "tools", NTOOLS)
    else:
        D.main()
