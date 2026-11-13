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
INTEG_DIR = os.path.join(HERE, "..", "integrations-page")
sys.path.insert(0, INTEG_DIR)
from integrations_data import ITEMS as INTEG_ITEMS

D.NAME = "3VL Page Dashboards" if D.LIVE else "3VL Page Dashboards Preview"
D.SLUG = "business-dashboards" if D.LIVE else "preview-business-dashboards"
D.TITLE = "Company Digital Dashboards: Your Whole Business in One Dashboard | Three Village Local"
D.DESC = ("Custom business dashboards built by Three Village Local: customers and leads, calendar, money, marketing, social media, "
          "reviews, team and automations in one place, with an AI assistant. Works on laptop, tablet and phone.")
D.FB_TITLE = "Your whole business. One dashboard."
INTEG = "/integrations" if D.LIVE else "/preview-integrations"
IC = json.load(open(os.path.join(INTEG_DIR, "icons.json"), encoding="utf-8"))
CDN = "https://cdn.jsdelivr.net/npm/simple-icons@%s/icons/" % IC["version"]
NTOOLS = "%d+" % (len(INTEG_ITEMS) // 50 * 50)

# ---------- small helpers ----------
SV = {
    "cc": "M4 4h7v7H4zM13 4h7v4h-7zM13 10h7v10h-7zM4 13h7v7H4z",
    "crm": "M16 19v-1a4 4 0 0 0-4-4H7a4 4 0 0 0-4 4v1M9.5 10a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7M21 19v-1a4 4 0 0 0-3-3.9M16 3.1a3.5 3.5 0 0 1 0 6.8",
    "cal": "M4 6h16v14H4zM4 10h16M8 3v5M16 3v5",
    "fin": "M12 2v20M17 6.5C17 4.6 14.8 4 12 4S7 5 7 7.5 9.5 10.5 12 11s5 1.5 5 4-2.2 3.5-5 3.5-5-1-5-3",
    "mkt": "M4 20V11M10 20V5M16 20v-8M21 20H3",
    "soc": "M4 5h16v11H9l-5 4z",
    "rev": "M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z",
    "auto": "M13 2L4 14h7l-1 8 9-12h-7z",
}


def ico(k, cls="tvd-ic"):
    return '<svg class="%s" viewBox="0 0 24 24" aria-hidden="true"><path d="%s"/></svg>' % (cls, SV[k])


def pts(vals, w=300, h=100, pad=8):
    lo, hi = min(vals), max(vals)
    out = []
    for i, v in enumerate(vals):
        x = round(i * w / (len(vals) - 1), 1)
        y = round(h - pad - (v - lo) / ((hi - lo) or 1) * (h - 2 * pad), 1)
        out.append((x, y))
    return out


def line_d(vals, w=300, h=100):
    return "M" + " L".join("%s %s" % p for p in pts(vals, w, h))


def area(vals, gid, color="#1d5fbf", w=300, h=100, cls=""):
    d = line_d(vals, w, h)
    return ('<svg class="tvd-area %s" viewBox="0 0 %d %d" preserveAspectRatio="none" aria-hidden="true"><defs><linearGradient id="%s" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="%s" stop-opacity=".28"/><stop offset="1" stop-color="%s" stop-opacity="0"/></linearGradient></defs>'
            '<path class="tvd-fill" d="%s L%d %d L0 %dZ" fill="url(#%s)"/><path class="tvd-draw" pathLength="1" d="%s" fill="none" stroke="%s" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round" vector-effect="non-scaling-stroke"/></svg>') % (
        cls, w, h, gid, color, color, d, w, h, h, gid, d, color)


def spark(vals, color="#1d5fbf"):
    return '<svg class="tvd-spark" viewBox="0 0 100 30" preserveAspectRatio="none" aria-hidden="true"><path class="tvd-draw" pathLength="1" d="%s" fill="none" stroke="%s" stroke-width="2" vector-effect="non-scaling-stroke"/></svg>' % (line_d(vals, 100, 30), color)


def num(v, dec=0, pre="", suf=""):
    shown = ("{:,.%df}" % dec).format(v)
    return '%s<span data-c="%s" data-d="%d">%s</span>%s' % (pre, v, dec, shown, suf)


def kpi(label, value, delta, vals, up=True, color="#1d5fbf"):
    return '<div class="tvd-kpi"><em>%s</em><b>%s</b><u class="%s">%s</u>%s</div>' % (label, value, "up" if up else "dn", delta, spark(vals, color))


# ---------- dashboard screens ----------
CC = '''<div class="tvd-pane on" data-p="cc" role="tabpanel" aria-label="Command Center">
  <div class="tvd-ph"><div><h4>Good morning, Sam</h4><p>Thursday &middot; Harbor &amp; Vine, both locations</p></div><span class="tvd-pill">&#9679; Live</span></div>
  <div class="tvd-brief"><b>&#10022; Your day</b>46 reservations tonight, 3 catering leads to call back, and next Tuesday looks slow. I drafted a 2-for-1 dessert post for your approval.</div>
  <div class="tvd-kpis">''' + kpi("Revenue this week", num(24860, 0, "$"), "&#9650; 12%", [8, 9, 8, 11, 10, 12, 14]) + kpi("New leads", num(38), "&#9650; 9", [3, 5, 4, 6, 5, 7, 8], True, "#16a34a") + kpi("Bookings", num(112), "&#9650; 14%", [10, 12, 11, 13, 15, 14, 17], True, "#7c4dff") + kpi("Google rating", num(4.9, 1, "", " &#9733;"), "+6 reviews", [4, 4, 5, 5, 5, 6, 6], True, "#f59e0b") + '''</div>
  <div class="tvd-2">
    <div class="tvd-card"><div class="tvd-ch"><b>Revenue, last 12 weeks</b><span>&#9650; 18% vs last year</span></div>''' + area([52, 55, 51, 58, 62, 60, 66, 64, 71, 69, 76, 82], "tvdg1") + '''<div class="tvd-xl"><i>Aug</i><i>Sep</i><i>Oct</i><i>Nov</i></div></div>
    <div class="tvd-card"><div class="tvd-ch"><b>Needs attention</b><span>4</span></div>
      <ul class="tvd-todo"><li><i class="r"></i><div><b>Catering lead waiting 12 min</b><span>Website chat &middot; party of 40</span></div><em>Call</em></li>
      <li><i class="y"></i><div><b>Instagram post needs approval</b><span>2-for-1 dessert Tuesday</span></div><em>Review</em></li>
      <li><i class="y"></i><div><b>Invoice #1039 is 6 days late</b><span>Reminder sent this morning</span></div><em>View</em></li>
      <li><i class="g"></i><div><b>New 5-star review on Google</b><span>AI reply drafted</span></div><em>Post</em></li></ul></div>
  </div></div>'''

def lead(n, v, tag, age, hot=False):
    return '<div class="tvd-lead%s"><b>%s</b><span>%s</span><p><em>%s</em><i>%s</i></p></div>' % (" hot" if hot else "", n, v, tag, age)


CRM = '''<div class="tvd-pane" data-p="crm" role="tabpanel" aria-label="Customers and leads" hidden>
  <div class="tvd-ph"><div><h4>Customers &amp; leads</h4><p>Catering and private events pipeline</p></div><span class="tvd-pill">23 open</span></div>
  <div class="tvd-kpis">''' + kpi("Pipeline value", num(48200, 0, "$"), "&#9650; $6.1k", [20, 24, 23, 28, 31, 35, 40]) + kpi("Win rate", num(41, 0, "", "%"), "&#9650; 5 pts", [30, 32, 35, 34, 38, 39, 41], True, "#16a34a") + kpi("Avg. response", num(4, 0, "", " min"), "&#9660; 9 min", [14, 12, 11, 9, 7, 5, 4], True, "#7c4dff") + kpi("Repeat guests", num(63, 0, "", "%"), "&#9650; 4%", [55, 56, 58, 59, 60, 62, 63], True, "#f59e0b") + '''</div>
  <div class="tvd-kan">
    <div class="tvd-col"><h5>New <span>3</span></h5>''' + lead("Dana R.", "Rehearsal dinner, 40", "Website chat", "12 min", True) + lead("Mike T.", "Office lunch, 25", "Google call", "1 hr") + '''</div>
    <div class="tvd-col"><h5>Contacted <span>2</span></h5>''' + lead("Priya S.", "Birthday, 18", "Instagram", "Today") + lead("Coastal Realty", "Holiday party", "Referral", "2 days") + '''</div>
    <div class="tvd-col"><h5>Quote sent <span>2</span></h5>''' + lead("Lena W.", "$3,400", "E-signed", "Viewed 2x") + lead("J. Alvarez", "$1,850", "Follow-up Fri", "3 days") + '''</div>
    <div class="tvd-col"><h5>Booked <span>4</span></h5>''' + lead("The Kims", "$2,900", "Deposit paid", "Dec 6") + lead("Harbor PTA", "$1,200", "Deposit paid", "Dec 13") + '''</div>
  </div>
  <div class="tvd-card tvd-health"><div class="tvd-ch"><b>Customer health</b><span>Win-back ready</span></div>
    <p><b>Alicia M.</b><span class="tvd-hb"><i style="width:92%" class="g"></i></span><em class="g">92 &middot; Loyal</em></p>
    <p><b>Tom &amp; Rae B.</b><span class="tvd-hb"><i style="width:64%" class="y"></i></span><em class="y">64 &middot; Offer sent</em></p>
    <p><b>Greg P.</b><span class="tvd-hb"><i style="width:38%" class="r"></i></span><em class="r">38 &middot; 60 days away</em></p></div>
</div>'''

def evb(t, s, c, h):
    return '<i class="%s" style="height:%dpx"><b>%s</b>%s</i>' % (c, h, t, s)


CAL = '''<div class="tvd-pane" data-p="cal" role="tabpanel" aria-label="Calendar" hidden>
  <div class="tvd-ph"><div><h4>Calendar</h4><p>Reservations, events and staff, one view</p></div><span class="tvd-pill">This week</span></div>
  <div class="tvd-alert"><b>&#9888; Slow day ahead</b>Tuesday dinner is pacing 40% under normal. <u>Promote it</u></div>
  <div class="tvd-week">
    <div><h6>Mon</h6>''' + evb("Lunch", "38 covers", "b", 46) + evb("Staff", "6 on", "p", 30) + evb("Dinner", "82 covers", "b", 70) + '''</div>
    <div class="slow"><h6>Tue</h6>''' + evb("Lunch", "31 covers", "b", 40) + evb("Staff", "5 on", "p", 30) + evb("Dinner", "36 covers", "y", 44) + '''</div>
    <div><h6>Wed</h6>''' + evb("Lunch", "44 covers", "b", 50) + evb("Tasting", "Wine dinner", "g", 56) + evb("Staff", "7 on", "p", 30) + '''</div>
    <div><h6>Thu</h6>''' + evb("Lunch", "40 covers", "b", 46) + evb("Dinner", "96 covers", "b", 78) + evb("Staff", "8 on", "p", 30) + '''</div>
    <div><h6>Fri</h6>''' + evb("Party", "Kims, 40", "g", 54) + evb("Dinner", "128 covers", "b", 92) + '''</div>
    <div><h6>Sat</h6>''' + evb("Brunch", "74 covers", "b", 62) + evb("Dinner", "140 covers", "b", 96) + '''</div>
    <div><h6>Sun</h6>''' + evb("Brunch", "88 covers", "b", 70) + evb("Staff", "6 on", "p", 30) + '''</div>
  </div>
  <div class="tvd-row3"><div><b>''' + num(28) + '''</b><span>reminder texts sent today</span></div><div><b>''' + num(2) + '''</b><span>no-shows this week (down from 9)</span></div><div><b>''' + num(96, 0, "", "%") + '''</b><span>shifts confirmed</span></div></div>
</div>'''

BARS = [(62, 48), (66, 50), (71, 52), (69, 51), (78, 55), (86, 61)]
bars = "".join('<g><rect class="tvd-bar" x="%d" y="%d" width="16" height="%d" rx="3" fill="#1d5fbf" style="animation-delay:%.2fs"/><rect class="tvd-bar" x="%d" y="%d" width="16" height="%d" rx="3" fill="#c9d8ef" style="animation-delay:%.2fs"/></g>' % (
    12 + i * 48, 110 - r, r, i * .08, 30 + i * 48, 110 - e, e, i * .08 + .04) for i, (r, e) in enumerate(BARS))
FIN = '''<div class="tvd-pane" data-p="fin" role="tabpanel" aria-label="Finance" hidden>
  <div class="tvd-ph"><div><h4>Money</h4><p>From QuickBooks, Square and your bank feed</p></div><span class="tvd-pill">November</span></div>
  <div class="tvd-kpis">''' + kpi("Revenue (month)", num(86400, 0, "$"), "&#9650; 9%", [60, 62, 66, 65, 70, 74, 78]) + kpi("Expenses", num(61250, 0, "$"), "&#9650; 3%", [50, 52, 51, 53, 54, 55, 56], False, "#94a3b8") + kpi("Profit", num(25150, 0, "$"), "29% margin", [10, 11, 14, 12, 16, 18, 21], True, "#16a34a") + kpi("Cash in 30 days", num(41900, 0, "$"), "Forecast", [30, 31, 33, 32, 35, 38, 41], True, "#7c4dff") + '''</div>
  <div class="tvd-2">
    <div class="tvd-card"><div class="tvd-ch"><b>Revenue vs. expenses</b><span class="tvd-leg"><i class="b"></i>Revenue <i class="l"></i>Expenses</span></div>
      <svg class="tvd-bars" viewBox="0 0 300 120" preserveAspectRatio="none" aria-hidden="true"><line x1="0" y1="110" x2="300" y2="110" stroke="#e2e8f0"/>''' + bars + '''</svg><div class="tvd-xl"><i>Jun</i><i>Jul</i><i>Aug</i><i>Sep</i><i>Oct</i><i>Nov</i></div></div>
    <div class="tvd-card tvd-donut-c"><div class="tvd-ch"><b>Where the money goes</b></div>
      <div class="tvd-donut"><svg viewBox="0 0 42 42" aria-hidden="true"><circle cx="21" cy="21" r="15.9" fill="none" stroke="#eef2f7" stroke-width="6"/>
        <circle class="tvd-seg" cx="21" cy="21" r="15.9" fill="none" stroke="#1d5fbf" stroke-width="6" pathLength="100" stroke-dasharray="31 69" stroke-dashoffset="25"/>
        <circle class="tvd-seg" cx="21" cy="21" r="15.9" fill="none" stroke="#4da3ff" stroke-width="6" pathLength="100" stroke-dasharray="28 72" stroke-dashoffset="-6"/>
        <circle class="tvd-seg" cx="21" cy="21" r="15.9" fill="none" stroke="#f2c94c" stroke-width="6" pathLength="100" stroke-dasharray="12 88" stroke-dashoffset="-34"/>
        <circle class="tvd-seg" cx="21" cy="21" r="15.9" fill="none" stroke="#16a34a" stroke-width="6" pathLength="100" stroke-dasharray="29 71" stroke-dashoffset="-46"/></svg><b>29%<span>profit</span></b></div>
      <ul class="tvd-key"><li><i style="background:#1d5fbf"></i>Food &amp; drink 31%</li><li><i style="background:#4da3ff"></i>Labor 28%</li><li><i style="background:#f2c94c"></i>Rent &amp; other 12%</li><li><i style="background:#16a34a"></i>Profit 29%</li></ul></div>
  </div>
  <ul class="tvd-inv"><li><b>#1042 Coastal Realty</b><span>$2,350</span><em class="g">Paid</em></li><li><b>#1043 Harbor PTA</b><span>$600</span><em class="y">Due Fri</em></li><li><b>#1039 J. Alvarez</b><span>$925</span><em class="r">6 days late &middot; reminder sent</em></li></ul>
</div>'''

def src(n, p, c):
    return '<p><span>%s</span><i><u class="tvd-grow" style="width:%d%%;background:%s"></u></i><b>%d%%</b></p>' % (n, p * 2, c, p)


MKT = '''<div class="tvd-pane" data-p="mkt" role="tabpanel" aria-label="Marketing" hidden>
  <div class="tvd-ph"><div><h4>Marketing</h4><p>Website, Google, social and email in one place</p></div><span class="tvd-pill">Last 30 days</span></div>
  <div class="tvd-kpis">''' + kpi("Website visits", num(4820), "&#9650; 18%", [30, 34, 33, 38, 41, 44, 48]) + kpi("Calls from Google", num(146), "&#9650; 22", [10, 12, 13, 12, 15, 17, 19], True, "#16a34a") + kpi("Social reach", num(31400), "&#9650; 31%", [12, 15, 14, 19, 22, 25, 31], True, "#d62976") + kpi("Email opens", num(46, 0, "", "%"), "&#9650; 3 pts", [40, 41, 43, 42, 44, 45, 46], True, "#f59e0b") + '''</div>
  <div class="tvd-2">
    <div class="tvd-card"><div class="tvd-ch"><b>Where customers found you</b></div><div class="tvd-src">''' + src("Google search", 42, "#1d5fbf") + src("Google Maps", 21, "#4da3ff") + src("Instagram", 14, "#d62976") + src("Three Village Local", 11, "#f2a93b") + src("Email", 7, "#16a34a") + '''</div></div>
    <div class="tvd-card tvd-tvl"><div class="tvd-ch"><b>&#9733; Three Village Local</b><span>Built in</span></div>
      <p><span>Profile views</span><b>&#9650; 32%</b></p><p><span>Website clicks</span><b>&#9650; 18%</b></p><p><span>Calls from your listing</span><b>&#9650; 11%</b></p><p><span>Featured this week</span><b>Homepage + email</b></p></div>
  </div></div>'''

def post(img, cap, status, cls, when, approve=False):
    btn = '<div class="tvd-pact"><button type="button" class="tvd-approve">Approve</button><button type="button" class="tvd-edit">Edit</button></div>' if approve else ""
    return '<div class="tvd-post %s"><div class="tvd-pimg" style="--pg:%s"><span>%s</span></div><p>%s</p><em>%s</em><i>%s</i>%s</div>' % (cls, img[0], img[1], cap, status, when, btn)


SOC = '''<div class="tvd-pane" data-p="soc" role="tabpanel" aria-label="Social content studio" hidden>
  <div class="tvd-ph"><div><h4>Content studio</h4><p>Plan, approve and schedule every post</p></div><span class="tvd-pill">Next 7 days</span></div>
  <div class="tvd-posts">''' + post(("linear-gradient(140deg,#7a2e3b,#d9825b)", "&#127856;"), "2-for-1 dessert Tuesday. Bring a friend!", "Needs your OK", "wait", "Tue 4 PM", True) + post(("linear-gradient(140deg,#0f4c5c,#5fb3a1)", "&#127863;"), "Wine dinner Wednesday, 5 courses", "Scheduled", "ok", "Wed 11 AM") + post(("linear-gradient(140deg,#2b2d42,#8d99ae)", "&#127926;"), "Live jazz this Friday from 7 PM", "Scheduled", "ok", "Thu 6 PM") + post(("linear-gradient(140deg,#b5651d,#f2c94c)", "&#129360;"), "New fall brunch menu reel", "Draft", "draft", "Sat 9 AM") + '''</div>
  <div class="tvd-row3"><div><b>Thu 6 to 8 PM</b><span>your best time to post</span></div><div><b>''' + num(8940) + '''</b><span>views on your top reel</span></div><div><b>''' + num(12) + '''</b><span>posts planned this month</span></div></div>
</div>'''

REV = '''<div class="tvd-pane" data-p="rev" role="tabpanel" aria-label="Reviews" hidden>
  <div class="tvd-ph"><div><h4>Reviews</h4><p>Every platform, one inbox</p></div><span class="tvd-pill">&#9650; 19 this month</span></div>
  <div class="tvd-2 tvd-2b">
    <div class="tvd-card tvd-score"><b>''' + num(4.9, 1) + '''</b><span class="tvd-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span><em>''' + num(312) + ''' reviews</em>
      <div class="tvd-plat"><p><span>Google</span><b>4.9</b><i>214</i></p><p><span>Yelp</span><b>4.6</b><i>61</i></p><p><span>Facebook</span><b>5.0</b><i>29</i></p><p><span>Tripadvisor</span><b>4.8</b><i>8</i></p></div></div>
    <div class="tvd-card tvd-revs">
      <div class="tvd-rv"><p class="tvd-rh"><b>Jen K. on Google</b><span>&#9733;&#9733;&#9733;&#9733;&#9733;</span></p><p>&ldquo;Best short rib in town and the staff made our anniversary so special.&rdquo;</p>
        <div class="tvd-reply"><em>&#10022; AI drafted reply</em>Thank you, Jen! Happy anniversary from all of us. See you soon.<button type="button" class="tvd-post-reply">Post reply</button></div></div>
      <div class="tvd-rv"><p class="tvd-rh"><b>Marco D. on Yelp</b><span>&#9733;&#9733;&#9733;&#9733;&#9734;</span></p><p>&ldquo;Great food, a bit of a wait on Saturday.&rdquo;</p><p class="tvd-flag">&#128276; Flagged for the manager</p></div>
    </div>
  </div></div>'''

def tog(name, sub, on, runs):
    return '<li><div><b>%s</b><span>%s</span></div><em>%s</em><button type="button" class="tvd-sw%s" role="switch" aria-checked="%s" aria-label="%s"><i></i></button></li>' % (
        name, sub, runs, " on" if on else "", "true" if on else "false", name)


AUTO = '''<div class="tvd-pane" data-p="auto" role="tabpanel" aria-label="Automations" hidden>
  <div class="tvd-ph"><div><h4>Automations</h4><p>Running quietly in the background</p></div><span class="tvd-pill">7 active</span></div>
  <div class="tvd-saved"><b>''' + num(41.5, 1) + ''' hours</b><span>saved this month by your automations</span></div>
  <ul class="tvd-autos">''' + tog("Missed-call text-back", "Texts every missed caller within a minute", True, "37 runs") + tog("Speed-to-lead alarm", "Buzzes you if a lead waits 5 minutes", True, "12 runs") + tog("Review request after visit", "Thank-you text with your Google link", True, "84 runs") + tog("Invoice reminders", "Friendly nudges at 3, 7 and 14 days", True, "9 runs") + tog("Win-back offer", "Guests away 60 days get a welcome-back offer", True, "21 runs") + tog("Birthday treat", "A free dessert on their birthday week", False, "Off") + '''</ul>
</div>'''

TABS = [("cc", "Command Center"), ("crm", "Customers &amp; leads"), ("cal", "Calendar"), ("fin", "Money"), ("mkt", "Marketing"), ("soc", "Content studio"), ("rev", "Reviews"), ("auto", "Automations")]
tabs = "".join('<button type="button" class="tvd-tab%s" role="tab" data-p="%s" aria-selected="%s">%s<span>%s</span></button>' % (
    " on" if i == 0 else "", k, "true" if i == 0 else "false", ico(k), n) for i, (k, n) in enumerate(TABS))

APP = '''<div class="tvd-appwrap tvs-up"><div class="tvd-app" id="tvd-app">
  <div class="tvd-chrome"><i></i><i></i><i></i><span>&#128274; dashboard.harborandvine.com</span><em><b></b>Live preview: click around</em></div>
  <div class="tvd-body">
    <nav class="tvd-side" role="tablist" aria-label="Dashboard screens"><div class="tvd-brand"><b>HV</b><span>Harbor &amp; Vine</span></div>''' + tabs + '''</nav>
    <div class="tvd-main"><div class="tvd-top"><div class="tvd-ask">&#10022; Ask your business anything...</div><div class="tvd-me"><b>SM</b><span>Owner</span></div></div>
''' + CC + CRM + CAL + FIN + MKT + SOC + REV + AUTO + '''
    </div></div>
  <div class="tvd-toast" id="tvd-toast" role="status" aria-live="polite"></div>
</div>
<p class="tvd-note">Sample business shown. Yours is built around how you work, with your numbers.</p></div>'''

HERO = '''<section class="tvd-top-sec" id="tvd-top">
  <div class="tvd-top-in tvs-up">
    <p class="tvs-kick"><span class="tvs-dot"></span>New from Three Village Local: Company Digital Dashboards</p>
    <h1>Your whole business.<br><span>One dashboard.</span></h1>
    <p class="tvd-lede">Customers, calendar, money, marketing, social media, reviews and your team, all in one place. Built for your business by our local team, with an AI assistant that tells you what needs you today.</p>
    <div class="tvs-ctas tvd-ctas"><a class="tvs-btn tvs-blue" href="#tvs-book">Book a free demo</a><a class="tvs-btn tvs-ghost" href="#demos">See the live demos</a></div>
    <ul class="tvs-trust tvd-trust"><li><b>8 screens</b>in one login</li><li><b>''' + NTOOLS + '''</b>tools it connects to</li><li><b>Laptop, tablet</b>and phone</li></ul>
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
      <p>Follow-ups, reminders, review requests and invoice nudges happen on their own, the same way every time. Your dashboard keeps score of the hours you get back.</p>
      <div class="tvd-hours"><b><span id="tvd-hrs">41.5</span> hours</b><span>saved this month at Harbor &amp; Vine (sample)</span></div></div>
    <div class="tvd-feed tvs-up"><div class="tvd-feed-h"><b><i></i>Live activity</b><span>Today</span></div><ul id="tvd-feed"></ul>''' + feed_tpl + '''</div>
  </div></section>'''

# ---------- industries ----------
IND = [
    ("rest", "&#127869;", "Restaurants", "Covers, food cost and five-star nights.",
     ["Covers and reservations by night", "Sales by menu item", "Food and labor cost %", "Delivery orders and payouts", "Reviews on Google, Yelp and Tripadvisor", "Staff shifts and tip-outs", "Catering and private event leads", "Slow-night alerts with promo ideas"],
     ["Toast", "Square", "OpenTable", "Resy", "7shifts", "DoorDash", "MarginEdge"]),
    ("con", "&#128679;", "Contractors", "Every lead, estimate and job on one board.",
     ["Leads by source", "Estimates sent vs. won", "Job pipeline and schedule", "Profit per job", "Photo timelines for every job", "Change orders and e-signatures", "Crew hours", "Permit and inspection dates"],
     ["Jobber", "Buildertrend", "CompanyCam", "QuickBooks Online", "JobNimbus", "Angi", "Houzz Pro"]),
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
     ["Follow Up Boss", "kvCORE", "OneKey MLS", "Dotloop", "SkySlope", "ShowingTime", "Zillow"]),
    ("off", "&#128188;", "Offices &amp; pros", "Clients, projects and billable time.",
     ["Client intake", "Projects and deadlines", "Billable hours", "Invoices and payments", "Proposals and e-signatures", "Secure client portal", "Referral sources", "Team workload"],
     ["Clio", "Karbon", "TaxDome", "QuickBooks Online", "Microsoft 365", "DocuSign", "Calendly"]),
    ("ret", "&#128717;", "Retail", "Sales, stock and shoppers in sync.",
     ["Sales by day, hour and item", "Low-stock alerts", "Best and slow sellers", "Online vs. in-store", "Loyalty and repeat shoppers", "Gift cards", "Staff schedule", "Events and foot traffic"],
     ["Shopify", "Square", "Lightspeed Retail", "Clover", "Klaviyo", "Etsy", "Instagram"]),
    ("med", "&#129463;", "Medical &amp; dental", "A smoother front desk and a fuller schedule.",
     ["Appointments and open slots", "No-shows and recalls", "New patient sources", "Production and collections", "Reviews", "Online intake forms", "Staff schedule", "Treatment acceptance"],
     ["Weave", "NexHealth", "Dentrix", "Open Dental", "Jane", "SimplePractice", "Zocdoc"]),
    ("aut", "&#128663;", "Auto repair", "Bays, repair orders and repeat customers.",
     ["Car count and bay use", "Repair orders and average ticket", "Parts orders", "Technician hours", "Approvals by text", "Service reminders", "Reviews", "Fleet accounts"],
     ["Tekmetric", "Shopmonkey", "Mitchell 1", "AutoLeap", "QuickBooks Online", "Podium", "Google Business Profile"]),
]
itabs = "".join('<button type="button" class="tvd-itab%s" data-i="%s" role="tab" aria-selected="%s"><span>%s</span>%s</button>' % (
    " on" if i == 0 else "", k, "true" if i == 0 else "false", e, n) for i, (k, e, n, t, tr, cn) in enumerate(IND))
ipanes = "".join('''<div class="tvd-ipane%s" data-i="%s" role="tabpanel"%s><div class="tvd-ip-h"><span>%s</span><div><h3>%s</h3><p>%s</p></div></div>
  <div class="tvd-ip-b"><div><p class="tvd-ip-k">Your dashboard tracks</p><ul>%s</ul></div><div><p class="tvd-ip-k">Popular connections</p><div class="tvd-ip-c">%s</div>
  <a class="tvd-ip-more" href="%s">See all %s integrations &rarr;</a></div></div></div>''' % (
    " on" if i == 0 else "", k, "" if i == 0 else " hidden", e, n, t, "".join("<li>%s</li>" % x for x in tr),
    "".join('<a href="%s?q=%s">%s</a>' % (INTEG, escape(c.replace(" ", "+")), escape(c)) for c in cn), INTEG, NTOOLS) for i, (k, e, n, t, tr, cn) in enumerate(IND))
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
WALL = ["quickbooks", "square", "stripe", "shopify", "google", "googleanalytics", "instagram", "facebook", "gmail", "googlecalendar", "mailchimp", "yelp",
        "doordash", "calendly", "hubspot", "zoom", "dropbox", "tiktok", "xero", "paypal", "wix", "wordpress", "trello", "notion"]
wall = "".join('<span><img src="%s%s.svg" alt="" loading="lazy" width="28" height="28"></span>' % (CDN, s) for s in WALL)
INT = '''<section class="tvs-sec tvd-int" id="tvd-int">
  <div class="tvd-int-in tvs-up"><div class="tvd-int-txt"><p class="tvs-eyebrow">Connects to what you already use</p><h2>Keep your tools. Lose the tab juggling.</h2>
    <p>Your dashboard pulls the numbers that matter from the software you already pay for: POS, accounting, booking, CRM, email, social media, reviews and more. If it has an export or an API, we can usually connect it.</p>
    <div class="tvs-ctas"><a class="tvs-btn tvs-blue" href="''' + INTEG + '''">Search ''' + NTOOLS + ''' integrations</a><a class="tvs-btn tvs-ghost" href="#tvs-book">Ask about my software</a></div></div>
    <div class="tvd-wall" aria-hidden="true">''' + wall + '''</div></div></section>'''

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
DEMOS = [("Harbor &amp; Vine", "Restaurant", "#7a2e3b", "#d9825b", "&#127863;", ["Covers and food cost", "Reservations and reviews", "Slow-night promos"]),
         ("North Shore Builders", "Contractor", "#9a3412", "#f59e0b", "&#128679;", ["Leads to signed jobs", "Profit per job", "Photo timelines"]),
         ("Glow Studio", "Salon &amp; med spa", "#9d174d", "#f472b6", "&#10024;", ["Rebook rate", "Memberships", "Client photos and forms"]),
         ("Iron Harbor Fitness", "Gym", "#111827", "#ef4444", "&#127947;", ["Members and churn", "Class attendance", "Failed payments"]),
         ("Greenline Landscape Co.", "Landscaping", "#14532d", "#4ade80", "&#127807;", ["Routes and crews", "Renewals", "Seasonal upsells"]),
         ("Realtor&#39;s Edge", "Real estate CRM", "#0b1f4b", "#4da3ff", "&#127969;", ["Speed to lead", "Pipeline and closings", "Past-client touches"])]
demos = "".join('''<div class="tvd-demo" style="--a:%s;--b:%s"><div class="tvd-demo-v" aria-hidden="true"><div class="tvd-demo-bar"><span>%s</span><i></i><i></i><i></i></div>
  <div class="tvd-demo-k"><u></u><u></u><u></u></div><svg viewBox="0 0 100 30" preserveAspectRatio="none"><path d="M0 26 L15 22 L30 24 L45 15 L60 17 L75 9 L100 4" fill="none" stroke="currentColor" stroke-width="2.4" vector-effect="non-scaling-stroke"/></svg></div>
  <div class="tvd-demo-t"><em>%s</em><h3>%s</h3><ul>%s</ul><span class="tvd-soon">Demo coming soon</span></div></div>''' % (
    a, b, e, k, n, "".join("<li>%s</li>" % x for x in pts_), ) for n, k, a, b, e, pts_ in DEMOS)
DEMO = '''<section class="tvs-sec tvd-demos" id="demos">
  <div class="tvs-head tvs-up"><p class="tvs-eyebrow">See the live demos</p><h2>Six sample businesses. Six dashboards.</h2>
    <p>Interactive demos for each sample business are coming soon. Want to see one now? Book a free demo and we&#39;ll walk you through the one closest to your business.</p></div>
  <div class="tvd-dgrid tvs-up">''' + demos + '''</div>
  <p class="tvd-note">Sample businesses for demonstration only.</p>
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
assert "\\" not in D.HEAD

CTA = '''<section class="tvw-cta3 tvs-up"><div class="tvw-cta3-in"><p class="tvw-cta3-k">Run your business from one screen</p><h2>See your dashboard in action.</h2>
<p class="tvw-cta3-s">Book a free demo. We&#39;ll show you a dashboard built for your industry and send a custom quote.</p>
<div class="tvw-cta-btns"><a class="tvs-btn tvw-btn-w" href="#tvs-book">Book a free demo</a><a class="tvs-btn tvw-btn-o" href="''' + INTEG + '''">See integrations</a></div></div></section>'''

BOOK = P.BOOK.replace('<p class="tvs-eyebrow">Your free plan</p>', '<p class="tvs-eyebrow">Free demo</p>').replace(
    "<h2>Get your free plan.</h2>", "<h2>Book your free demo.</h2>")
i = BOOK.index("<p>Tell us your name, business and email.")
j = BOOK.index('<div class="tvp-proof">')
BOOK = BOOK[:i] + '''<p>Tell us your name, business and email. Within one business day we&#39;ll reach out by email to set up your free demo:</p>
    <ul class="tvp-get"><li>A walkthrough of a dashboard for your industry</li><li>Which of your tools we can connect</li><li>A custom quote, no pressure</li></ul>
    ''' + BOOK[j:]
BOOK = BOOK.replace("mailto:hello@threevillagelocal.com?subject=Our%20services", "mailto:hello@threevillagelocal.com?subject=Dashboard%20demo")
i = BOOK.index('<p class="tvp-alt">')
BOOK = BOOK[:i] + '<p class="tvp-alt">Using lots of software? <a href="' + INTEG + '">Check our integrations directory &rarr;</a></p>' + BOOK[BOOK.index("</p>", i) + 4:]

HTML = ('<div class="tvs tvd" id="tvs">\n\n' + HERO + "\n\n" + AI + "\n\n" + ROLES + "\n\n" + DEV + "\n\n" + AUTOS + "\n\n" + INDS + "\n\n" +
        FEAT + "\n\n" + INT + "\n\n" + SEC + "\n\n" + HOW + "\n\n" + DEMO + "\n\n" + FAQ + "\n\n" + CTA + "\n\n" + BOOK +
        '\n\n<a class="tvs-sticky tvd-sticky" href="#tvs-book">Book a free demo</a>\n</div>')
# keep hyphenated words on one line (never split at the hyphen), text only, never inside tags
HTML = re.sub(r'>([^<]+)<', lambda m: '>' + re.sub(r'(?<![A-Za-z0-9&#;.-])([A-Za-z0-9.()]+(?:-[A-Za-z0-9.,]+)+)', r'<nobr>\1</nobr>', m.group(1)) + '<', HTML)
assert "\\" not in HTML and chr(0x2014) not in HTML

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
        s = s + "<script>" + JS + "</script>"
        assert "\\" not in s
        return s
    return s


D.rd = rd
if __name__ == "__main__":
    D.main()
