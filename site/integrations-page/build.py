"""Integrations directory: every tool a Company Digital Dashboard can connect to, searchable and filterable.
Same design system and message form as /services (imports the platform-page build).
    python site/integrations-page/build.py          -> widget "3VL Page Integrations Preview" + hidden /preview-integrations (noindex)
    python site/integrations-page/build.py --live   -> widget "3VL Page Integrations" + /integrations
Data: integrations_data.py (add products there, then run resolve_icons.py)."""
import importlib.util, json, os, sys, zlib
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("platbuild", os.path.join(HERE, "..", "platform-page", "build.py"))
P = importlib.util.module_from_spec(spec)
spec.loader.exec_module(P)
D = P.D
sys.path.insert(0, HERE)
from integrations_data import CATS, ITEMS

D.NAME = "3VL Page Integrations" if D.LIVE else "3VL Page Integrations Preview"
D.SLUG = "integrations" if D.LIVE else "preview-integrations"
D.TITLE = "Integrations: Connect the Tools You Already Use to One Dashboard | Three Village Local"
D.DESC = ("Company Digital Dashboards by Three Village Local connect to the software local businesses already use: POS, accounting, "
          "booking, CRM, marketing, social media, reviews and more. Search 450+ tools.")
D.FB_TITLE = "Connects with the tools you already use."
DASH = "/business-dashboards" if D.LIVE else "/preview-business-dashboards"

IC = json.load(open(os.path.join(HERE, "icons.json"), encoding="utf-8"))
CDN = "https://cdn.jsdelivr.net/npm/simple-icons@%s/icons/" % IC["version"]
ICONS = IC["icons"]
TVL_ICON = "https://threevillagelocal-cloud.github.io/3vl-share/site/icon-192.png"
CATN = dict(CATS)
TYPES = {"D": "Direct connection", "E": "Via export/import", "C": "Custom build", "B": "Built in"}
N = len(ITEMS)
NROUND = "%d+" % (N // 50 * 50)


def norm(s):
    return " ".join("".join(c if c.isalnum() else " " for c in s.lower()).split())


def logo(name, cat, size=28):
    if cat == "tvl":
        return '<span class="tvi-logo tvi-tvl"><img src="%s" alt="" loading="lazy" width="%d" height="%d"></span>' % (TVL_ICON, size, size)
    s = ICONS.get(name)
    if s:
        return '<span class="tvi-logo"><img src="%s%s.svg" alt="" loading="lazy" width="%d" height="%d"></span>' % (CDN, s, size, size)
    h = zlib.crc32(name.encode()) % 360
    letters = "".join(w[0] for w in name.replace("-", " ").split()[:2] if w[0].isalnum()).upper() or name[0]
    return '<span class="tvi-logo tvi-mono" style="--h:%d">%s</span>' % (h, escape(letters[:2]))


def nw(t):
    """keep hyphenated words on one line (no split at the hyphen)"""
    return " ".join('<nobr>%s</nobr>' % w if "-" in w else w for w in escape(t).split(" "))


def card(it):
    name, cat, typ, desc = it[:4]
    s = norm(name + " " + CATN[cat] + " " + desc) + " " + norm(name).replace(" ", "")
    return ('<li class="tvi-card" data-c="%s" data-t="%s" data-s="%s">%s<div class="tvi-ct"><b>%s</b><i>%s</i></div>'
            '<em class="tvi-b tvi-b%s">%s</em></li>') % (cat, typ, escape(s), logo(name, cat), nw(name), nw(desc), typ, TYPES[typ])


groups = []
for k, label in CATS:
    its = [it for it in ITEMS if it[1] == k]
    if not its:
        continue
    groups.append('<section class="tvi-grp" data-g="%s" aria-label="%s"><h3>%s<span>%d</span></h3><ul class="tvi-grid">%s</ul></section>' % (
        k, escape(label), nw(label), len(its), "".join(card(it) for it in its)))
chips = '<button type="button" class="tvi-chip on" data-cat="all" aria-pressed="true">All<span>%d</span></button>' % N + "".join(
    '<button type="button" class="tvi-chip" data-cat="%s" aria-pressed="false">%s<span>%d</span></button>' % (k, nw(l), sum(1 for it in ITEMS if it[1] == k))
    for k, l in CATS)

HUB = ["quickbooks", "square", "google", "instagram", "shopify", "gmail", "stripe", "facebook"]
hub_logos = "".join('<span class="tvi-hl tvi-h%d"><img src="%s%s.svg" alt="" width="30" height="30"></span>' % (i, CDN, s) for i, s in enumerate(HUB))
hub_lines = "".join('<line x1="200" y1="200" x2="%d" y2="%d"/>' % xy for xy in [(200, 30), (320, 80), (370, 200), (320, 320), (200, 370), (80, 320), (30, 200), (80, 80)])

HERO = '''<section class="tvi-top" id="tvi-top">
  <div class="tvi-top-txt tvs-up">
    <p class="tvs-kick"><span class="tvs-dot"></span>Company Digital Dashboards: integrations</p>
    <h1>Connects with the tools<br><span>you already use.</span></h1>
    <p class="tvi-lede">Keep the software you know. Your dashboard pulls the numbers that matter from each one, so sales, bookings, leads, reviews and marketing finally live in one place.</p>
    <div class="tvs-ctas"><a class="tvs-btn tvs-blue" href="#tvi-dir">Search the directory</a><a class="tvs-btn tvs-ghost" href="#tvs-book">Ask about your software</a></div>
    <ul class="tvs-trust"><li><b>''' + NROUND + '''</b>tools in the directory</li><li><b>''' + str(len(CATS)) + '''</b>categories</li><li><b>3</b>ways to connect</li></ul>
  </div>
  <div class="tvi-hub tvs-up" aria-hidden="true"><svg viewBox="0 0 400 400" class="tvi-hub-svg">''' + hub_lines + '''</svg>''' + hub_logos + '''
    <div class="tvi-core"><b>Your dashboard</b><span class="tvi-bars"><i></i><i></i><i></i><i></i><i></i></span><em>All synced</em></div></div>
</section>'''

WAYS = '''<section class="tvs-sec tvi-ways" id="tvi-ways">
  <div class="tvs-head tvs-up"><p class="tvs-eyebrow">How we connect</p><h2>Three honest ways in.</h2>
  <p>If your software has a way to share data, we can bring it into your dashboard. Here is what each label in the directory means.</p></div>
  <div class="tvi-way-row">
    <div class="tvi-way tvs-up"><em class="tvi-b tvi-bD">Direct connection</em><h3>Live, automatic</h3><p>The tool has an official sign-in or API. You approve access once with your own login, and the numbers update on their own.</p></div>
    <div class="tvi-way tvs-up"><em class="tvi-b tvi-bE">Via export/import</em><h3>Scheduled reports</h3><p>The tool lets you export reports or files. We set up a simple routine so those numbers land in your dashboard.</p></div>
    <div class="tvi-way tvs-up"><em class="tvi-b tvi-bC">Custom build</em><h3>Built for you</h3><p>Needs a special feed, partner approval or a custom setup. We look at it with you and tell you exactly what is possible.</p></div>
  </div>
  <p class="tvi-fine tvs-up">Connection options depend on each product and the plan you have with it. We confirm the best method for your accounts during your free demo. Product names and logos belong to their owners; a listing here does not mean a partnership or endorsement.</p>
</section>'''

DIR = '''<section class="tvs-sec tvi-dirsec" id="tvi-dir">
  <div class="tvs-head tvs-up"><p class="tvs-eyebrow">The directory</p><h2>Find your tools.</h2><p>Search by name, or by what you need, like &ldquo;payroll&rdquo;, &ldquo;reservations&rdquo; or &ldquo;reviews&rdquo;.</p></div>
  <div class="tvi-bar" id="tvi-bar">
    <label class="tvi-search"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M16.5 16.5L21 21" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>
      <input id="tvi-q" type="search" placeholder="Search ''' + NROUND + ''' tools, like QuickBooks or booking" autocomplete="off" aria-label="Search the integrations directory"></label>
    <div class="tvi-types" role="group" aria-label="Connection type"><button type="button" class="tvi-ty on" data-typ="all" aria-pressed="true">Any connection</button><button type="button" class="tvi-ty" data-typ="D" aria-pressed="false">Direct</button><button type="button" class="tvi-ty" data-typ="E" aria-pressed="false">Export/import</button><button type="button" class="tvi-ty" data-typ="C" aria-pressed="false">Custom</button></div>
  </div>
  <div class="tvi-chips" role="group" aria-label="Categories">''' + chips + '''</div>
  <p class="tvi-count" aria-live="polite">Showing <b id="tvi-n">''' + str(N) + '''</b> of <b>''' + str(N) + '''</b> tools</p>
  <div class="tvi-groups" id="tvi-groups">''' + "".join(groups) + '''</div>
  <div class="tvi-none" id="tvi-none" hidden><b>No match in the directory yet.</b><p>That doesn&#39;t mean we can&#39;t connect it. If it has an export or an API, we can usually bring it in.</p>
    <div class="tvs-ctas"><a class="tvs-btn tvs-blue" href="#tvs-book">Ask us about it</a><button type="button" class="tvi-clear" id="tvi-clear">Clear search</button></div></div>
</section>'''

ASK = '''<section class="tvs-sec tvi-ask tvs-up"><div class="tvi-ask-in"><div><p class="tvs-eyebrow">Don&#39;t see your software?</p><h2>Ask us. We probably can.</h2>
  <p>Local businesses use thousands of tools. Tell us what you use and we&#39;ll tell you, free, how we would bring it into your dashboard.</p></div>
  <div class="tvi-ask-b"><a class="tvs-btn tvs-blue" href="#tvs-book">Ask about my software</a><a class="tvs-btn tvs-ghost" href="''' + DASH + '''">See what the dashboard does</a></div></div></section>'''

BOOK = P.BOOK.replace('<p class="tvs-eyebrow">Your free plan</p>', '<p class="tvs-eyebrow">Ask us</p>').replace(
    "<h2>Get your free plan.</h2>", "<h2>Tell us what you use.</h2>")
i = BOOK.index("<p>Tell us your name, business and email.")
j = BOOK.index('<div class="tvp-proof">')
BOOK = BOOK[:i] + '''<p>Send your name, business and email, and list the tools you use under &ldquo;Tell us more&rdquo;. Within one business day you&#39;ll hear back by email with:</p>
    <ul class="tvp-get"><li>Which of your tools we can connect, and how</li><li>What your dashboard could show on day one</li><li>A custom quote, no pressure</li></ul>
    ''' + BOOK[j:]
BOOK = BOOK.replace("mailto:hello@threevillagelocal.com?subject=Our%20services", "mailto:hello@threevillagelocal.com?subject=Dashboard%20integrations")
i = BOOK.index('<p class="tvp-alt">')
BOOK = BOOK[:i] + '<p class="tvp-alt">Want the big picture first? <a href="' + DASH + '">See Company Digital Dashboards &rarr;</a></p>' + BOOK[BOOK.index("</p>", i) + 4:]

HTML = ('<div class="tvs tvi" id="tvs">\n\n' + HERO + "\n\n" + WAYS + "\n\n" + DIR + "\n\n" + ASK + "\n\n" + BOOK +
        '\n\n<a class="tvs-sticky tvi-sticky" href="#tvs-book">Ask about your software</a>\n</div>')
assert "\\" not in HTML and "—" not in HTML

CSS = '''
.tvi-top{display:grid;grid-template-columns:1.1fr .9fr;gap:30px;align-items:center;margin:12px 0 0;padding:56px 48px 50px;border-radius:28px;background:radial-gradient(700px 380px at 90% 0%,rgba(77,163,255,.24),transparent 70%),radial-gradient(520px 300px at 0% 110%,rgba(45,240,200,.10),transparent 70%),linear-gradient(180deg,#f6f9ff,#fff 75%)}
.tvi-top h1{font-size:54px;line-height:1.04;font-weight:800;margin:0 0 18px!important;text-wrap:balance}
.tvi-top h1 span{background:linear-gradient(90deg,var(--blue),#4da3ff);-webkit-background-clip:text;background-clip:text;color:transparent}
.tvi-lede{font-size:19px;line-height:1.6;color:#3c4a5e;margin:0 0 24px!important;max-width:560px}
.tvi-hub{position:relative;width:100%;max-width:400px;aspect-ratio:1;margin:0 auto}
.tvi-hub-svg{position:absolute;inset:0;width:100%;height:100%}
.tvi-hub-svg line{stroke:#7fb0f0;stroke-width:2;stroke-dasharray:5 9;animation:tviFlow 1.1s linear infinite}
.tvi-hl{position:absolute;width:15%;aspect-ratio:1;margin:-7.5%;border-radius:22%;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 14px 30px -14px rgba(9,30,66,.45),0 0 0 1px #e3ebf7;animation:tviBob 5s ease-in-out infinite}
.tvi-hl img{width:46%!important;height:auto!important}
.tvi-h0{left:50%;top:7.5%}.tvi-h1{left:80%;top:20%;animation-delay:-.6s}.tvi-h2{left:92.5%;top:50%;animation-delay:-1.2s}.tvi-h3{left:80%;top:80%;animation-delay:-1.8s}.tvi-h4{left:50%;top:92.5%;animation-delay:-2.4s}.tvi-h5{left:20%;top:80%;animation-delay:-3s}.tvi-h6{left:7.5%;top:50%;animation-delay:-3.6s}.tvi-h7{left:20%;top:20%;animation-delay:-4.2s}
.tvi-core{position:absolute;left:50%;top:50%;width:40%;margin:-20% 0 0 -20%;aspect-ratio:1;border-radius:26%;background:linear-gradient(150deg,#0b1f4b,#1d4fa8);color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;box-shadow:0 30px 60px -24px rgba(9,30,66,.6),0 0 0 10px rgba(77,163,255,.14);animation:tviPulse 3.6s ease-in-out infinite}
.tvi-core b{font-size:15px;line-height:1.1;text-align:center}.tvi-core em{font-style:normal;font-size:11.5px;font-weight:800;color:#7ee2b0}
.tvi-bars{display:flex;align-items:flex-end;gap:4px;height:34px}.tvi-bars i{width:7px;border-radius:3px;background:#4da3ff;animation:tviBar 1.8s ease-in-out infinite}
.tvi-bars i:nth-child(1){height:40%}.tvi-bars i:nth-child(2){height:70%;animation-delay:-.3s}.tvi-bars i:nth-child(3){height:55%;animation-delay:-.6s}.tvi-bars i:nth-child(4){height:90%;animation-delay:-.9s;background:#f2c94c}.tvi-bars i:nth-child(5){height:65%;animation-delay:-1.2s}
@keyframes tviFlow{to{stroke-dashoffset:-28}}@keyframes tviBob{0%,100%{translate:0 0}50%{translate:0 -6px}}
@keyframes tviPulse{0%,100%{box-shadow:0 30px 60px -24px rgba(9,30,66,.6),0 0 0 10px rgba(77,163,255,.14)}50%{box-shadow:0 30px 60px -24px rgba(9,30,66,.6),0 0 0 20px rgba(77,163,255,.05)}}
@keyframes tviBar{0%,100%{transform:scaleY(1)}50%{transform:scaleY(.6)}}.tvi-bars i{transform-origin:bottom}
.tvi-way-row{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;max-width:1080px;margin:0 auto}
.tvi-way{padding:24px 22px;border-radius:22px;background:#fff;border:1px solid #dfe8f6;box-shadow:0 20px 44px -30px rgba(9,30,66,.4);transition:transform .25s,box-shadow .25s}
.tvi-way:hover{transform:translateY(-4px);box-shadow:0 28px 54px -28px rgba(9,30,66,.5)}
.tvi-way h3{margin:12px 0 6px!important;font-size:21px}.tvi-way p{margin:0!important;font-size:15.5px;color:var(--mut);line-height:1.55}
.tvi-fine{max-width:820px;margin:20px auto 0!important;text-align:center;font-size:13.5px!important;color:var(--mut)}
.tvi-b{display:inline-flex;align-items:center;gap:6px;font-style:normal;font-size:12px;font-weight:800;padding:5px 10px;border-radius:999px;white-space:nowrap;line-height:1.2}
.tvi-b:before{content:"";width:7px;height:7px;border-radius:50%;background:currentColor}
.tvi-bD{background:#e3f7ee;color:#0b6b55}.tvi-bE{background:#e7f0ff;color:#1d5fbf}.tvi-bC{background:#fff2d1;color:#7a5200}.tvi-bB{background:#13294b;color:#ffd36b}
.tvi-bar{display:flex;gap:12px;align-items:center;flex-wrap:wrap;max-width:1100px;margin:0 auto 14px}
.tvi-search{flex:1 1 340px;display:flex;align-items:center;gap:10px;min-height:56px;padding:0 18px;border-radius:999px;background:#fff;border:2px solid #d6e2f3;box-shadow:0 16px 34px -24px rgba(9,30,66,.45);transition:border-color .2s,box-shadow .2s;margin:0!important;cursor:text}
.tvi-search:focus-within{border-color:var(--blue);box-shadow:0 0 0 4px rgba(29,95,191,.14)}
.tvi-search svg{flex:none;width:20px;height:20px;color:#7a8ba3}
.tvi-search input{flex:1;min-width:0;border:0!important;outline:0;background:transparent!important;box-shadow:none!important;font:inherit;font-size:17px!important;color:var(--navy);height:52px!important;padding:0!important;margin:0!important}
.tvi-types{display:flex;gap:6px;flex-wrap:wrap}
#tvs .tvi-ty,#tvs .tvi-chip,#tvs .tvi-clear{appearance:none;-webkit-appearance:none;font:inherit;cursor:pointer;line-height:1.2;text-transform:none;letter-spacing:0;box-shadow:none}
#tvs .tvi-ty{min-height:44px;padding:0 15px;border-radius:999px!important;border:1px solid #d6e2f3;background:#fff;color:var(--navy);font-size:14px;font-weight:700;transition:background .2s,color .2s,border-color .2s}
#tvs .tvi-ty:hover{border-color:#9cc1ff}#tvs .tvi-ty.on{background:var(--navy);border-color:var(--navy);color:#fff}
.tvi-chips{display:flex;flex-wrap:wrap;gap:8px;max-width:1100px;margin:0 auto 14px}
#tvs .tvi-chip{flex:none;white-space:nowrap!important;display:inline-flex;align-items:center;gap:7px;min-height:44px;padding:0 14px;border-radius:999px!important;border:1px solid #dfe8f6;background:#f4f7fc;color:var(--navy);font-size:14px;font-weight:700;white-space:nowrap;transition:background .2s,color .2s,transform .2s}
#tvs .tvi-chip span{font-size:12px;font-weight:800;color:#7a8ba3}
#tvs .tvi-chip:hover{background:#e8f0fd;transform:translateY(-1px)}
#tvs .tvi-chip.on{background:var(--blue);border-color:var(--blue);color:#fff}#tvs .tvi-chip.on span{color:#cfe2ff}
.tvi-count{max-width:1100px;margin:0 auto 18px!important;font-size:15px;color:var(--mut)}.tvi-count b{color:var(--navy)}
.tvi-groups{max-width:1100px;margin:0 auto}
.tvi-grp{margin:0 0 30px}
.tvi-grp h3{display:flex;align-items:center;gap:10px;margin:0 0 12px!important;font-size:22px}.tvi-grp h3 span{font-size:13px;font-weight:800;padding:3px 9px;border-radius:999px;background:#eef3fb;color:var(--mut)}
.tvi-grid{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(min(255px,100%),1fr));gap:12px}
.tvi-card{position:relative;display:grid;grid-template-columns:46px 1fr;gap:4px 12px;align-items:start;padding:14px 14px 13px;border-radius:18px;background:#fff;border:1px solid #e3e9f2;box-shadow:0 10px 26px -22px rgba(9,30,66,.5);transition:transform .2s,box-shadow .2s,border-color .2s;margin:0!important}
.tvi-card:hover{transform:translateY(-3px);border-color:#bcd3f5;box-shadow:0 20px 38px -24px rgba(9,30,66,.5)}
.tvi-card[hidden]{display:none}.tvi-grp[hidden]{display:none}
.tvi-logo{grid-row:span 2;width:46px;height:46px;border-radius:13px;background:#f3f6fb;border:1px solid #e6ecf5;display:flex;align-items:center;justify-content:center;overflow:hidden}
.tvi-logo img{width:24px!important;height:24px!important;display:block}
.tvi-tvl{background:#fff}.tvi-tvl img{width:38px!important;height:38px!important}
.tvi-mono{border:0;color:#fff;font-weight:800;font-size:16px;letter-spacing:.02em;background:linear-gradient(140deg,hsl(var(--h) 62% 46%),hsl(calc(var(--h) + 40) 66% 36%))}
#tvs nobr{white-space:nowrap!important}.tvi-ct{min-width:0}.tvi-ct b{display:block;font-size:16px;line-height:1.25;color:var(--navy)}.tvi-ct i{display:block;font-style:normal;font-size:13.5px;line-height:1.4;color:var(--mut);margin-top:2px}
.tvi-card .tvi-b{grid-column:2;justify-self:start;margin-top:6px}
.tvi-none{max-width:640px;margin:10px auto 30px;padding:28px;border-radius:22px;background:#f6f9ff;border:1px dashed #bcd0ee;text-align:center}
.tvi-none[hidden]{display:none}.tvi-none b{display:block;font-size:20px;color:var(--navy);margin-bottom:6px}.tvi-none .tvs-ctas{justify-content:center;margin:12px 0 0}
#tvs .tvi-clear{min-height:48px;padding:0 22px;border-radius:999px!important;border:2px solid var(--line);background:#fff;color:var(--navy);font-weight:800;font-size:15px}
.tvi-ask-in{display:flex;align-items:center;justify-content:space-between;gap:28px;max-width:1100px;margin:0 auto;padding:34px 38px;border-radius:26px;background:radial-gradient(600px 260px at 100% 0%,rgba(77,163,255,.22),transparent 70%),linear-gradient(135deg,#eef5ff,#fff);border:1px solid #d6e4fb}
.tvi-ask-in h2{font-size:34px!important;margin:0 0 8px!important}.tvi-ask-in p{margin:0!important;color:var(--mut)}
.tvi-ask-b{display:flex;flex-direction:column;gap:10px;flex:none}
@media (max-width:900px){.tvi-top{grid-template-columns:1fr;padding:34px 18px 30px;border-radius:22px}.tvi-top h1{font-size:38px}.tvi-lede{font-size:17px}.tvi-hub{max-width:320px}
 .tvi-way-row{grid-template-columns:1fr}.tvi-ask-in{flex-direction:column;align-items:flex-start;padding:26px 20px}.tvi-ask-b{width:100%}.tvi-ask-in h2{font-size:28px!important}
 .tvi-chips{flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;-webkit-overflow-scrolling:touch;margin-left:-4px;margin-right:-4px;padding:2px 4px 6px}.tvi-chips::-webkit-scrollbar{display:none}
 .tvi-types{width:100%;flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none}.tvi-types::-webkit-scrollbar{display:none}#tvs .tvi-ty{flex:none}
 .tvi-search{flex-basis:100%}}
@media (max-width:420px){.tvi-top h1{font-size:31px}.tvi-search input{font-size:16px!important}.tvi-search{padding:0 14px}.tvi-grp h3{font-size:20px}.tvi-top .tvs-btn{width:100%}}
@media (prefers-reduced-motion:reduce){.tvi-hub-svg line,.tvi-hl,.tvi-core,.tvi-bars i{animation:none!important}}
'''

JS = ''';(function(){var R=document.getElementById('tvi-dir');if(!R)return;
var cards=[].slice.call(R.querySelectorAll('.tvi-card')),grps=[].slice.call(R.querySelectorAll('.tvi-grp'));
var q=document.getElementById('tvi-q'),cnt=document.getElementById('tvi-n'),none=document.getElementById('tvi-none'),cat='all',typ='all',busy=false,tm=null;
var AL='abcdefghijklmnopqrstuvwxyz0123456789';
var idx=cards.map(function(c){return ' '+(c.getAttribute('data-s')||'')+' '});
function toks(s){s=(s||'').toLowerCase();var o='';for(var i=0;i<s.length;i++){var ch=s.charAt(i);o+=AL.indexOf(ch)>-1?ch:' '}return o.split(' ').filter(function(x){return x.length>0})}
function apply(){busy=false;var t=toks(q.value),sq=t.join(''),n=0;
 cards.forEach(function(c,i){var ok=(cat==='all'||c.getAttribute('data-c')===cat)&&(typ==='all'||c.getAttribute('data-t')===typ);
  if(ok&&t.length){var s=idx[i];ok=t.every(function(w){return s.indexOf(w)>-1})||(sq.length>3&&s.indexOf(sq)>-1)}
  c.hidden=!ok;if(ok)n++});
 grps.forEach(function(g){g.hidden=!g.querySelector('.tvi-card:not([hidden])')});
 cnt.textContent=n;none.hidden=n>0;
 clearTimeout(tm);if(t.length)tm=setTimeout(function(){if(window.gtag)gtag('event','integrations_search',{search_term:q.value.slice(0,60),results:n})},1200);}
function tick(){if(!busy){busy=true;requestAnimationFrame(apply)}}
q.addEventListener('input',tick);
function pick(sel,attr,val){[].forEach.call(document.querySelectorAll(sel),function(b){var on=b.getAttribute(attr)===val;b.classList.toggle('on',on);b.setAttribute('aria-pressed',on?'true':'false')})}
[].forEach.call(document.querySelectorAll('.tvi-chip'),function(b){b.addEventListener('click',function(){cat=b.getAttribute('data-cat');pick('.tvi-chip','data-cat',cat);apply();if(window.gtag)gtag('event','integrations_category',{cat:cat})})});
[].forEach.call(document.querySelectorAll('.tvi-ty'),function(b){b.addEventListener('click',function(){typ=b.getAttribute('data-typ');pick('.tvi-ty','data-typ',typ);apply()})});
document.getElementById('tvi-clear').addEventListener('click',function(){q.value='';cat='all';typ='all';pick('.tvi-chip','data-cat','all');pick('.tvi-ty','data-typ','all');apply();q.focus()});
try{var sp=new URLSearchParams(location.search);if(sp.get('q')){q.value=sp.get('q');apply()}if(sp.get('cat')){cat=sp.get('cat');pick('.tvi-chip','data-cat',cat);apply()}}catch(x){}
/* sticky button: shows after the hero, hides at the form */
var st=document.querySelector('.tvi-sticky'),top=document.getElementById('tvi-top'),bk=document.getElementById('tvs-book');
if(st&&top&&bk&&'IntersectionObserver' in window){var hv=true,bv=false;function upd(){st.classList.toggle('on',!hv&&!bv)}
 new IntersectionObserver(function(es){hv=es[0].isIntersecting;upd()}).observe(top);new IntersectionObserver(function(es){bv=es[0].isIntersecting;upd()}).observe(bk)}
/* open "Tell us more" so the software question is easy to answer */
var n2=0;(function more(){var d=document.querySelector('#tvs-form-slot details.tvp-more');if(!d){if(++n2<40)setTimeout(more,300);return}d.open=true;var c=d.querySelector('[name=comments]');if(c)c.setAttribute('placeholder','Which software do you use? For example: Square, QuickBooks, Vagaro')})();
})();'''


def rd(f):
    if f == "page.html":
        return HTML
    s = P.rd(f)
    if f == "page.css":
        return s + CSS
    if f == "page.js":
        s = s.replace("Get My Free Plan", "Send My Question").replace(
            'data-tease="Want a quick free plan? Tell me your business name and I will point you to the right fit."',
            'data-tease="Wondering if we can connect your software? Ask me about it."')
        s = s + "<script>" + JS + "</script>"
        assert "\\" not in s
        return s
    return s


D.rd = rd
if __name__ == "__main__":
    D.main()
