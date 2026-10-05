"""Business owner's toolkit, v2 (owner 10/5: v1 "a bit bulky and clunky. we need something a little more streamlined and simplified").
Light, compact, no guide kit: short hero, 6-item checklist, one-row-per-business directory grouped by need, free help, FAQ, CTA.
    python build2.py   -> post2.html (BD post content) + preview2.html"""
import html, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = "https://threevillagelocal-cloud.github.io/3vl-share/biz-guide-2026/"
SITE = "https://www.threevillagelocal.com/"
L = SITE + "logos/profile/"
P = SITE + "pictures/profile/"


def tel(p):
    return "".join(ch for ch in p if ch.isdigit())


def row(name, what, town, phone=None, profile=None, logo=None, fav=False, web=None):
    ini = "".join(w[0] for w in name.replace("(", "").split()[:2]).upper()
    mark = '<img src="%s" alt="" loading="lazy" width="44" height="44">' % logo if logo else '<span>%s</span>' % ini
    star = '<em class="bx-fav">&#9733; Neighbor favorite</em>' if fav else ""
    btn = []
    if phone:
        btn.append('<a class="bx-call" href="tel:%s" aria-label="Call %s">Call</a>' % (tel(phone), html.escape(name)))
    if profile:
        btn.append('<a class="bx-view" href="%s%s">%s</a>' % (SITE, profile, "Join free" if profile == "join" else "View"))
    elif web:
        btn.append('<a class="bx-view" href="%s" target="_blank" rel="noopener">Website</a>' % web)
    return ('<div class="bx-row"><div class="bx-logo">%s</div><div class="bx-info">%s<b>%s</b><p>%s</p><small>%s%s</small></div><div class="bx-btns">%s</div></div>'
            % (mark, star, name, what, town, (" &middot; <span class=\"bx-ph\">%s</span>" % phone) if phone else "", "".join(btn)))


GROUPS = [
    ("payroll", "&#128176;", "Payroll &amp; HR", "Stop doing payroll at midnight. Let a local pro handle pay runs, filings and HR paperwork.", [
        row("Zuma Payroll (TJ Sirani)", "Payroll and HR compliance for 1 to 10,000 employees. TJ is a Three Village resident of almost 40 years.", "Melville", "631-525-6201", "tj-sirani-at-zuma-payroll", L + "limage-138-61-photo.png", True)]),
    ("money", "&#129534;", "Taxes &amp; bookkeeping", "Clean books all year make tax time a quick review instead of a scramble.", [
        row("JLW Accounting and Tax Services", "Management accounting and tax preparation for small, new and growing businesses.", "Setauket", "631-338-8858", "jlw-accounting-and-tax-services", P + "pimage-217-340-photo.jpg", True),
        row("JM Management Solutions", "Bookkeeping for small to mid-sized businesses.", "Patchogue", "631-987-1532", "jm-management-solutions-inc", L + "limage-240-52-photo.webp", True)]),
    ("insure", "&#128737;&#65039;", "Business insurance", "Review your coverage once a year. A local agent can close gaps and shop your rates.", [
        row("GH Insurance Co.", "Business, home, life and employee benefits.", "Wading River", "631-602-0422", "gh-insurance-co"),
        row("CD Insurance Agency", "Independent broker that shops multiple carriers, plus group benefits.", "Hauppauge", "631-582-4400", "cd-insurance-agency-inc"),
        row("AssuredPartners (Oren Wiener)", "Property and casualty coverage.", "Melville", "631-844-5236", "assured-partners-oren-wiener"),
        row("Ed Reilly State Farm Agency", "Business, auto, home and life, right in town.", "Setauket", "631-941-7194", "state-farm")]),
    ("plan", "&#128200;", "Retirement &amp; planning", "Take care of your own future too: ask about a retirement plan for you and your team.", [
        row("Girard Wealth Management Group", "Frank Girard, CFP&reg;, ChFC&reg;, CLU&reg;, 25 years of experience, lives and works in Three Village.", "Setauket", "631-527-0205", "girard-wealth-management-group", L + "limage-78-159-photo.webp", True),
        row("Sandpiper Wealth", "Fee-based financial planning.", "Setauket", "917-697-3747", "sandpiper-wealth-llc")]),
    ("legal", "&#9878;&#65039;", "Legal", "Wills, succession and trademarks: a little planning now saves a lot later.", [
        row("Raupp Law PC", "Estate planning and elder law.", "Setauket", "631-769-4440", "raupp-law-pc", L + "limage-228-310-photo.png", True),
        row("Southard Estate Planning", "Wills, trusts, probate and estate planning.", "Setauket", "631-818-1725", "southard-estate-planning", L + "limage-137-223-photo.png", True),
        row("Intellectulaw (P.B. Tufariello)", "Trademarks, copyrights, patents and business agreements.", "Mount Sinai", "631-476-8734", "intellectulaw-the-law-offices-of-p-b-tufariello-p-c")]),
    ("tech", "&#128187;", "Tech &amp; IT", "Backups and security keep one bad email from shutting you down.", [
        row("CMIT Solutions of North Suffolk", "IT, cybersecurity and cloud for small and mid-sized businesses.", "Stony Brook", "631-204-3060", "cmit-solutions-of-north-suffolk"),
        row("ProSysCon Computer Technologies", "IT support and computer services.", "East Setauket", "631-546-5706", "prosyscon-computer-technologies-inc")]),
    ("grow", "&#129309;", "Networking &amp; getting found", "Your best customers live down the road.", [
        row("SBNA: Small Business Networking Alliance", "Local networking and referrals, without the nonsense.", "Stony Brook", None, "sbna-small-business-networking-alliance"),
        row("Three Village Local", "100,000+ local website and app visitors and 100,000+ social media views every month. Start with a free listing.", "Setauket, Stony Brook &amp; Port Jeff", None, "join")]),
]

FREE = [
    row("Stony Brook Small Business Development Center", "Free, confidential one-on-one advising on plans, marketing, finances and funding.", "Stony Brook University", "631-632-9837", None, None, False, "https://www.stonybrook.edu/sbdc/"),
    row("SCORE Long Island", "Free mentoring from volunteer business owners, online or in person.", "Long Island", None, None, None, False, "https://www.score.org/longisland"),
    row("Three Village Chamber of Commerce", "Meet other local owners and get involved in town.", "East Setauket", "631-689-8838", None, None, False, "https://www.3vchamber.com"),
]

CHECK = ["Hand off payroll so filings are never late",
         "Keep business and personal accounts separate",
         "Reconcile your books every month",
         "Calendar your quarterly estimated taxes",
         "Review your business insurance once a year",
         "Ask about a retirement plan for you and your team"]

FAQ = [
    ("How can a small business in Three Village save money on payroll?",
     "Outsourcing payroll to a local service like Zuma Payroll (TJ Sirani, a Three Village resident) handles pay runs, payroll tax filings and HR compliance, which helps you avoid late-filing penalties and saves hours every pay period."),
    ("Where can I find an accountant or bookkeeper near Setauket?",
     "JLW Accounting and Tax Services in Setauket handles management accounting and tax preparation for small businesses, and JM Management Solutions in Patchogue offers bookkeeping. Both are on Three Village Local."),
    ("Is there free help for small business owners near Stony Brook?",
     "Yes. The Stony Brook Small Business Development Center offers free, confidential advising (631-632-9837), SCORE Long Island offers free mentoring, and the Three Village Chamber of Commerce connects local owners."),
]

nav = "".join('<a href="#bx-%s">%s</a>' % (g[0], g[2]) for g in GROUPS) + '<a href="#bx-free">Free help</a>'
groups = "".join('<section class="bx-grp" id="bx-%s"><h3><span>%s</span>%s</h3><p class="bx-why">%s</p>%s</section>' % (g[0], g[1], g[2], g[3], "".join(g[4])) for g in GROUPS)
checks = "".join('<label class="bx-ck"><input type="checkbox" data-k="%d"><i></i><span>%s</span></label>' % (i, c) for i, c in enumerate(CHECK))
faq = "".join('<details class="bx-q"><summary>%s</summary><p>%s</p></details>' % q for q in FAQ)
faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]})

body = """<div class="bx" id="bx-top">
<header class="bx-head"><div class="bx-ht"><p class="bx-kick">Your neighbors in business</p><h2>The Business Owner's Toolkit</h2><p class="bx-sub">Local pros who help you save money and run smarter.</p></div><img class="bx-hlogo" src="https://threevillagelocal-cloud.github.io/3vl-share/live/hdr/logo-540.webp" alt="Three Village Local, your neighbors in business" width="540" height="168"></header>

<p class="bx-lead">Fall is the perfect time of year to make changes in your business. Get your payroll, books, insurance and plans in order now, and you walk into <b>2027</b> ready to grow instead of scrambling. These are the Three Village neighbors who can help, plus free resources most owners never use. <span>Reach out this fall and start the new year ahead.</span></p>

<nav class="bx-nav" aria-label="Jump to">NAV</nav>

GROUPS

<section class="bx-grp" id="bx-free"><h3><span>&#127381;</span>Free help most owners never use</h3><p class="bx-why">Free, local and built to help small businesses.</p>FREE</section>

<div class="bx-cta"><div><b>Own a business in Three Village?</b><p>Get found by your neighbors on our website and free app.</p></div><a href="https://www.threevillagelocal.com/join">List my business free</a></div>

<section class="bx-faq"><h3>Quick answers</h3>@@FAQ@@</section>

<p class="bx-src">Business details from each business's Three Village Local profile. Free resources checked October 5, 2026. General information, not tax, legal or financial advice.</p>
</div>
<script>(function(){var r=document.getElementById('bx-top');if(!r)return;r.classList.add('bx-js');var rows=[].slice.call(r.querySelectorAll('.bx-row'));if(!('IntersectionObserver' in window)||matchMedia('(prefers-reduced-motion: reduce)').matches){rows.forEach(function(x){x.classList.add('bx-in')});return}var io=new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;var el=e.target,sib=[].slice.call(el.parentNode.querySelectorAll('.bx-row'));el.style.transitionDelay=(sib.indexOf(el)*90)+'ms';el.classList.add('bx-in');io.unobserve(el)})},{rootMargin:'0px 0px -8% 0px'});rows.forEach(function(x){io.observe(x)})})();</script>
<script type="application/ld+json">FAQLD</script>
<style>
#post-content .post-image-container,#post-content .post-image-container + hr{display:none!important}
.bx{--n:#13233a;--b:#1f5fae;--m:#5c6b80;--l:#e6ebf2;max-width:780px;margin:0 auto;color:var(--n);font-family:'tvl-rc','Radio Canada',system-ui,sans-serif}
.bx *{box-sizing:border-box}.bx p{margin:0!important}
body:has(#bx-top) .post-detail-body h1{position:absolute!important;width:1px!important;height:1px!important;overflow:hidden!important;clip:rect(0 0 0 0)!important;white-space:nowrap!important}
.bx-head{display:flex;align-items:center;justify-content:space-between;gap:18px;background:var(--n);color:#fff;border-radius:16px;padding:20px 22px;margin:4px 0 18px}
.bx-ht{min-width:0}
.bx-hlogo{flex:0 0 auto;width:210px!important;height:auto!important;margin:0!important}
.bx .bx-kick{font-size:12px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#ffc53d}
.bx-head h2{font-size:clamp(26px,4.4vw,36px);line-height:1.08;margin:5px 0 5px!important;color:#fff!important;font-weight:700}
.bx .bx-sub{font-size:15.5px;color:#c9d8ea}
.bx .bx-lead{font-size:19px;font-weight:600;line-height:1.55;margin:0 2px 16px!important;color:var(--n)}.bx-lead b{color:var(--b)}.bx-lead span{display:block;margin-top:8px;color:var(--b)}
.bx-js .bx-row{opacity:0;transform:translateY(18px) scale(.985);transition:opacity .55s ease,transform .55s cubic-bezier(.2,.7,.2,1),box-shadow .2s}
.bx-js .bx-row.bx-in{opacity:1;transform:none}
.bx-row:hover{transform:translateY(-2px)!important;box-shadow:0 10px 24px rgba(19,35,58,.1)}
.bx-in .bx-logo{animation:bxpop .6s ease both;animation-delay:inherit}
@keyframes bxpop{0%{transform:scale(.6);opacity:0}70%{transform:scale(1.08)}100%{transform:scale(1);opacity:1}}
.bx-fav{animation:bxglow 2.6s ease-in-out infinite}@keyframes bxglow{50%{color:#d08a00}}
@media (prefers-reduced-motion:reduce){.bx-js .bx-row{opacity:1;transform:none;transition:none}.bx-in .bx-logo,.bx-fav{animation:none}}
.bx-nav{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 18px}
.bx-nav a{font-size:13.5px;font-weight:600;color:var(--b);background:#eef4fb;border-radius:999px;padding:7px 13px;text-decoration:none;white-space:nowrap}
.bx-grp{margin:0 0 24px;scroll-margin-top:80px}
.bx-grp h3{display:flex;align-items:center;gap:10px;font-size:21px;margin:0 0 4px;color:var(--n)}.bx-grp h3 span{font-size:20px}
.bx .bx-why{font-size:14.5px;color:var(--m);margin:0 0 10px!important}
.bx-row{display:flex;align-items:center;gap:14px;padding:12px 14px;border:1px solid var(--l);border-radius:14px;margin-bottom:8px;background:#fff;transition:box-shadow .2s}
.bx-row:hover{box-shadow:0 6px 18px rgba(19,35,58,.08)}
.bx-logo{flex:0 0 46px;height:46px;border-radius:12px;border:1px solid var(--l);display:flex;align-items:center;justify-content:center;overflow:hidden;background:#fff}
.bx-logo img{width:44px!important;height:44px!important;object-fit:contain;margin:0!important}.bx-logo span{font-weight:700;color:var(--b);font-size:15px}
.bx-info{flex:1;min-width:0}.bx-info b{display:block;font-size:16px;line-height:1.25}.bx .bx-info p{font-size:14px;color:#3f4e62;line-height:1.4;margin-top:2px!important}
.bx-info small{display:block;font-size:12.5px;color:var(--m);margin-top:3px}.bx-ph{white-space:nowrap}
.bx-fav{display:inline-block;font-style:normal;font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#a06a00;margin-bottom:2px}
.bx-btns{display:flex;gap:6px;flex:0 0 auto}
.bx-btns a{font-size:13.5px;font-weight:700;border-radius:10px;padding:8px 13px;text-decoration:none;white-space:nowrap}
.bx-call{background:var(--b);color:#fff!important}.bx-view{background:#eef4fb;color:var(--b)!important}
.bx-cta{display:flex;flex-wrap:wrap;gap:14px;align-items:center;justify-content:space-between;background:var(--n);color:#fff;border-radius:16px;padding:18px 20px;margin:6px 0 26px}
.bx-cta b{font-size:18px}.bx .bx-cta p{color:#c9d8ea;font-size:14.5px;margin-top:3px!important}
.bx-cta a{background:#fff;color:var(--n)!important;font-weight:700;border-radius:10px;padding:10px 16px;text-decoration:none;white-space:nowrap}
.bx-faq h3{font-size:19px;margin:0 0 8px}.bx-q{border-top:1px solid var(--l);padding:10px 2px}.bx-q summary{cursor:pointer;font-weight:700;font-size:15.5px}
.bx .bx-q p{font-size:14.5px;color:#3f4e62;line-height:1.5;margin-top:6px!important}
.bx .bx-src{font-size:12px;color:var(--m);margin-top:18px!important;line-height:1.5}
@media(max-width:560px){.bx-head{flex-direction:column-reverse;align-items:flex-start;gap:12px;padding:18px}.bx-hlogo{width:170px!important}.bx-row{flex-wrap:wrap}.bx-btns{width:100%;padding-left:60px}.bx-btns a{flex:1;text-align:center}}
</style>""".replace("IMG", IMG).replace("NAV", nav).replace("CHECKS", checks).replace("GROUPS", groups).replace("FREE", "".join(FREE)).replace("FAQLD", faq_ld).replace("@@FAQ@@", faq)

open(os.path.join(HERE, "post2.html"), "w", encoding="utf-8").write(body)
pv = ('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Business Owner\'s Toolkit Preview</title>'
      '<link href="https://fonts.googleapis.com/css2?family=Radio+Canada:wght@500;600;700&display=swap" rel="stylesheet">'
      '<style>body{margin:0;background:#f3f4f6;font-family:\'Radio Canada\',sans-serif}.wrap{max-width:900px;margin:0 auto;padding:20px 12px;background:#fff}</style></head>'
      '<body><div class="wrap"><div id="post-content">' + body + '</div></div></body></html>')
open(os.path.join(HERE, "preview2.html"), "w", encoding="utf-8").write(pv)
print("ok", len(body))
