"""Business owner's toolkit article (10/2026). Builds post.html (GKBASE placeholder, like the fall guide),
post.final.html (kit pinned to a full commit SHA) and preview.html (local preview).
    python build.py <guide-kit-sha>"""
import html, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = "https://threevillagelocal-cloud.github.io/3vl-share/biz-guide-2026/"
SITE = "https://www.threevillagelocal.com/"
SHA = sys.argv[1] if len(sys.argv) > 1 else "714f26382ef83f648f17cec3633253edc7dbfd19"
E = html.escape


def card(cid, name, who, photo, tag, where, body, facts, profile=None, logo=None, phone=None, web=None, member=None, extra_cls=""):
    lg = '<span class="gk-logo" data-bg="%s"></span>' % logo if logo else ""
    mem = '<p class="gk-member">%s</p>' % member if member else ""
    fx = "".join("<span>%s</span>" % f for f in facts)
    acts = []
    if profile == "join":
        acts.append('<a class="gk-3vl" href="%sjoin">List my business free &rarr;</a>' % SITE)
    elif profile:
        acts.append('<a class="gk-3vl" href="%s%s">View on 3VL &rarr;</a>' % (SITE, profile))
    if phone:
        acts.append('<a href="tel:%s">&#128222; Call</a>' % phone.replace("-", "").replace(" ", "").replace("(", "").replace(")", ""))
    if web:
        acts.append('<a href="%s" target="_blank" rel="noopener">Website &#8599;</a>' % web)
    return """    <article class="gk-card gk-rv%s%s" id="gk-%s" data-id="%s" data-name="%s" data-who="%s" data-cost="$" data-mi="5">
      <div class="gk-cimg" data-bg="%s%s-640.webp"><span class="gk-ctag">%s</span>%s</div>
      <button type="button" class="gk-heart" aria-label="Save to my business team" aria-pressed="false">&#9829;</button>
      <div class="gk-cb">%s<h3>%s</h3><p class="gk-where">%s</p>
        <p>%s</p>
        <div class="gk-facts">%s</div>
        <div class="gk-cact">%s</div></div>
    </article>
""" % (" has-logo" if logo else "", extra_cls, cid, cid, E(name), who, IMG, photo, tag, lg, mem, name, where, body, fx, "".join(acts))


def section(sid, ch, label, title, intro, cards, nxt=None, light=False):
    n = ('  <button type="button" class="gk-next" data-to="%s"><span><small>Next up</small><b>%s</b></span><em>&darr;</em></button>\n' % nxt) if nxt else ""
    return """<section class="gk-sec%s" id="%s"%s>
  <p class="gk-label">%s</p>
  <h2 class="gk-h2">%s</h2>
  <p class="gk-p">%s</p>
  <div class="gk-grid">
%s  </div>
%s</section>

""" % (" gk-light" if light else "", sid, (' data-ch="%s"' % ch) if ch else "", label, title, intro, "".join(cards), n)


L = SITE + "logos/profile/"
P = SITE + "pictures/profile/"

payroll = [card("zuma", "Zuma Payroll (TJ Sirani)", "pay", "payroll", "Payroll &amp; HR", "175 Broadhollow Rd, Melville &middot; 631-525-6201",
                "Payroll and HR compliance for companies with 1 to 10,000 employees, run by TJ Sirani, a Three Village resident for almost 40 years. Hand off pay runs, payroll tax filings and HR paperwork to someone you can actually call, so you can get back to running the business.",
                ["&#128188; 1 to 10,000 employees", "&#127968; Three Village resident"], "tj-sirani-at-zuma-payroll", L + "limage-138-61-photo.png", "631-525-6201", "https://www.zumapay.com", "&#11088; Neighbor favorite")]

money = [card("jlw", "JLW Accounting and Tax Services", "tax books", "tax", "Accounting &amp; tax", "690 Route 25A, Setauket &middot; 631-338-8858",
              "Judi Wallace's Setauket firm specializes in management accounting for small, new and growing businesses, plus tax preparation. Good numbers all year means fewer surprises at tax time.",
              ["&#129534; Tax preparation", "&#128200; Small business accounting"], "jlw-accounting-and-tax-services", P + "pimage-217-340-photo.jpg", "631-338-8858", "https://www.jlwfinancialservices.com/", "&#11088; Neighbor favorite"),
         card("jm", "JM Management Solutions", "books", "books", "Bookkeeping", "135 Mulford St, Patchogue &middot; 631-987-1532",
              "Bookkeeping by a local company for small to mid-sized businesses. Clean, reconciled books every month make loans, taxes and big decisions a lot easier.",
              ["&#128210; Monthly bookkeeping", "&#127970; Small to mid-sized businesses"], "jm-management-solutions-inc", L + "limage-240-52-photo.webp", "631-987-1532", None, "&#11088; Neighbor favorite")]

insure = [card("gh", "GH Insurance Co.", "ins", "insure", "Insurance", "Wading River &middot; 631-602-0422",
               "A local agent consulting across all lines: home, business, life and employee benefits. One conversation can cover your shop, your vehicles and your team's benefits.",
               ["&#127970; Business", "&#128101; Employee benefits"], "gh-insurance-co", None, "631-602-0422", "https://www.ghinsuranceco.com", "On Three Village Local"),
          card("cd", "CD Insurance Agency", "ins", "insure2", "Insurance broker", "300 Wheeler Rd, Hauppauge &middot; 631-582-4400",
               "An independent broker that shops your coverage for the best pricing across home, auto, business and life, plus group benefits.",
               ["&#128269; Shops multiple carriers", "&#128101; Group benefits"], "cd-insurance-agency-inc", None, "631-582-4400", "https://www.cdinsagency.com", "On Three Village Local"),
          card("assured", "AssuredPartners (Oren Wiener)", "ins", "insure", "Property &amp; casualty", "100 Baylis Rd, Melville &middot; 631-844-5236",
               "Property and casualty insurance focused on the right protection at the right price, a good call for buildings, equipment and liability.",
               ["&#127970; Property", "&#9878;&#65039; Liability"], "assured-partners-oren-wiener", None, "631-844-5236", "https://www.assuredpartners.com/orenwiener/", "On Three Village Local"),
          card("statefarm", "Ed Reilly State Farm Agency", "ins", "insure2", "Insurance", "190 N Belle Mead Rd, Setauket &middot; 631-941-7194",
               "A Setauket agency right in town for business, auto, home and life coverage. Stop in and talk it through face to face.",
               ["&#128205; Right in Setauket", "&#128663; Business auto"], "state-farm", None, "631-941-7194", "https://www.edinsetauket.com", "On Three Village Local")]

plan = [card("girard", "Girard Wealth Management Group", "plan", "wealth", "Planning", "376 Mark Tree Rd, Setauket &middot; 631-527-0205",
             "Frank Girard (CFP&reg;, ChFC&reg;, CLU&reg;) lives and works in Three Village and brings 25 years of experience. Business owners: ask about retirement plans for you and your team and how they fit your bigger financial picture.",
             ["&#127891; CFP&reg;, ChFC&reg;, CLU&reg;", "&#128197; 25 years"], "girard-wealth-management-group", L + "limage-78-159-photo.webp", "631-527-0205", "https://www.girardwmg.com/", "&#11088; Neighbor favorite"),
        card("sandpiper", "Sandpiper Wealth", "plan", "wealth", "Planning", "Setauket &middot; 917-697-3747",
             "Fee-based financial planning in Setauket for ambitious people who want their finances to line up with their goals.",
             ["&#129517; Fee-based planning"], "sandpiper-wealth-llc", None, "917-697-3747", "https://www.sandpiperwealth.com", "On Three Village Local")]

legal = [card("raupp", "Raupp Law PC", "legal", "legal", "Estate &amp; elder law", "9 Carlton Ave, Setauket &middot; 631-769-4440",
              "Amy C. Raupp, Esq. is an experienced estate planning and elder law attorney in Setauket. A good plan protects your family and what you have built.",
              ["&#128220; Estate planning", "&#128106; Elder law"], "raupp-law-pc", L + "limage-228-310-photo.png", "631-769-4440", "https://www.raupplaw.com/", "&#11088; Neighbor favorite"),
         card("southard", "Southard Estate Planning", "legal", "legal", "Estate planning", "175 Main St, Setauket &middot; 631-818-1725",
              "Katherine Southard focuses on wills, trusts, probate and estate planning for Three Village families, including what happens to your business down the road.",
              ["&#128220; Wills &amp; trusts", "&#127970; Planning ahead"], "southard-estate-planning", L + "limage-137-223-photo.png", "631-818-1725", "https://southardestateplanning.com/", "&#11088; Neighbor favorite"),
         card("intellectulaw", "Intellectulaw (P.B. Tufariello)", "legal", "legal", "Business law", "25 Little Harbor Rd, Mount Sinai &middot; 631-476-8734",
              "Patents, trademarks and copyrights, business agreements and litigation. Protect your name and your ideas before someone else does.",
              ["&#8482;&#65039; Trademarks", "&#128221; Business agreements"], "intellectulaw-the-law-offices-of-p-b-tufariello-p-c", None, "631-476-8734", "https://www.intellectulaw.com/", "On Three Village Local")]

tech = [card("cmit", "CMIT Solutions of North Suffolk", "tech", "it", "IT &amp; cybersecurity", "2100 Nesconset Hwy, Stony Brook &middot; 631-204-3060",
             "Computer, IT, cybersecurity, cloud and AI solutions for small and mid-sized businesses, with local support backed by a nationwide team.",
             ["&#128274; Cybersecurity", "&#9729;&#65039; Cloud"], "cmit-solutions-of-north-suffolk", None, "631-204-3060", "https://cmitsolutions.com/suffolk-ny-1250/", "On Three Village Local"),
        card("prosyscon", "ProSysCon Computer Technologies", "tech", "it", "IT support", "286 Main St, East Setauket &middot; 631-546-5706",
             "IT support and computer services for businesses in East Setauket and across Long Island.",
             ["&#128187; IT support"], "prosyscon-computer-technologies-inc", None, "631-546-5706", "https://www.prosyscon.com", "On Three Village Local")]

grow = [card("sbna", "SBNA: Small Business Networking Alliance", "grow", "network", "Networking", "Stony Brook",
             "Grow your business with people who want to see you win. SBNA is local networking without the nonsense: real referrals from real neighbors in business.",
             ["&#129309; Referrals", "&#128205; Stony Brook"], "sbna-small-business-networking-alliance", None, None, None, "On Three Village Local"),
        card("3vl", "Three Village Local", "grow", "freehelp", "Get found", "Setauket, Stony Brook &amp; Port Jefferson",
             "Put your business in front of 100,000+ website and app visitors and 100,000+ monthly social media views, all local. Start with a free listing, then add articles, social features and video when you are ready.",
             ["&#128200; 100,000+ visitors a month", "&#128241; Free community app"], "join", None, None, None, "Your neighbors in business")]

free = """<section class="gk-sec gk-light" id="gk-free" data-ch="07">
  <p class="gk-label">File 07 &middot; Costs nothing</p>
  <h2 class="gk-h2">Free help most owners never use</h2>
  <p class="gk-p">Before you pay for advice on a business plan, a loan application or a new idea, check these. They are free, local and run by people whose whole job is helping small businesses.</p>
  <div class="bz-free gk-rv">
    <div class="bz-fr"><b>Stony Brook Small Business Development Center</b><p>Free, one-on-one, confidential advising on business plans, marketing, financial management and access to capital, run out of Stony Brook University's Research and Development Park. Appointments are by phone or video.</p><a href="tel:6316329837">&#128222; 631-632-9837</a><a href="https://www.stonybrook.edu/sbdc/" target="_blank" rel="noopener">Website &#8599;</a></div>
    <div class="bz-fr"><b>SCORE Long Island</b><p>Free, confidential mentoring from 60+ volunteer business owners and executives across Nassau and Suffolk, online or in person, plus free business plan templates.</p><a href="https://www.score.org/longisland" target="_blank" rel="noopener">Request a mentor &#8599;</a></div>
    <div class="bz-fr"><b>Three Village Chamber of Commerce</b><p>Meet other local owners, get involved in community events and stay on top of what is happening in town.</p><a href="tel:6316898838">&#128222; 631-689-8838</a><a href="https://www.3vchamber.com" target="_blank" rel="noopener">Website &#8599;</a></div>
  </div>
  <button type="button" class="gk-next" data-to="gk-faq"><span><small>Next up</small><b>Quick answers for busy owners</b></span><em>&darr;</em></button>
</section>

"""

CHECK = [
    ("pay", "Hand off payroll so tax deposits and filings are never late", "Late payroll tax deposits come with IRS penalties. A payroll service handles the deadlines for you."),
    ("bank", "Keep business and personal money in separate accounts", "It makes bookkeeping faster, tax prep cheaper and your records cleaner if you ever apply for a loan."),
    ("books", "Reconcile your books every month, not every April", "Monthly books catch mistakes early and turn tax season into a quick review."),
    ("qtr", "Put quarterly estimated tax dates on your calendar", "Paying on time all year helps you avoid underpayment penalties and a big April bill."),
    ("ins", "Review business insurance once a year and ask about bundling", "Your business changes every year. A quick review can close gaps and sometimes lower your premium."),
    ("ret", "Ask about a retirement plan for you and your team", "Plans like a SEP IRA, SIMPLE IRA or 401(k) can help you save for the future, and contributions may lower taxable income. Ask a pro what fits."),
    ("will", "Update your will and plan for the business's future", "Decide now who handles what if something happens, so your family is not left guessing."),
    ("tech", "Back up your files and turn on two-step login", "Small businesses are a common target for scams and ransomware. Backups and two-step login stop most of it."),
    ("list", "Claim your free Three Village Local listing", "Neighbors search our website and app every day. Make sure they can find you, call you and get directions."),
]
check_html = "".join('<label class="bz-ck"><input type="checkbox" data-k="%s"><span class="bz-box"></span><span class="bz-t"><b>%s</b><small>%s</small></span></label>' % c for c in CHECK)

FAQ = [
    ("How can a small business in Three Village save money on payroll?",
     "Outsourcing payroll to a local service like Zuma Payroll (TJ Sirani, a Three Village resident) handles pay runs, payroll tax filings and HR compliance, which helps you avoid late-filing penalties and saves hours every pay period."),
    ("Where can I find an accountant or bookkeeper near Setauket?",
     "JLW Accounting and Tax Services on Route 25A in Setauket specializes in management accounting and tax preparation for small businesses, and JM Management Solutions in Patchogue offers bookkeeping for small to mid-sized businesses. Both are on Three Village Local."),
    ("Is there free help for small business owners near Stony Brook?",
     "Yes. The Stony Brook Small Business Development Center offers free, confidential one-on-one advising (631-632-9837), SCORE Long Island offers free volunteer mentoring, and the Three Village Chamber of Commerce connects local owners."),
    ("What insurance does a small business on Long Island need?",
     "It depends on the business, but most owners talk to an agent about general liability, property coverage, commercial auto, workers' compensation and employee benefits. Local agents on Three Village Local include GH Insurance Co., CD Insurance Agency, AssuredPartners and the Ed Reilly State Farm Agency in Setauket."),
]
faq_html = "".join('<div class="gk-tip"><b>%s</b><span>%s</span></div>' % q for q in FAQ)
faq_ld = '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[%s]}' % ",".join(
    '{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}' % (__import__("json").dumps(q), __import__("json").dumps(a)) for q, a in FAQ)

body = """<link rel="stylesheet" href="GKBASE/guide.css"><div class="gk" id="gk-top" data-key="bizguide2026" data-title="My local business team">

<header class="gk-hero">
  <img class="gk-hbg" src="IMGhero-1600.webp" srcset="IMGhero-900.webp 900w, IMGhero-1600.webp 1600w" sizes="100vw" alt="Shops along the walkway in Stony Brook Village" width="1600" height="927" fetchpriority="high">
  <div class="gk-hshade"></div>
  <div class="gk-hin">
    <p class="gk-kick"><span class="gk-dot"></span>For Three Village business owners</p>
    <h2 class="gk-h1">The Business Owner's Toolkit <span>Save money with neighbors you can call</span></h2>
    <p class="gk-dek">Payroll, taxes, bookkeeping, insurance, planning, legal and tech: the local pros who help Setauket, Stony Brook and Port Jefferson businesses run smarter, plus the free help most owners never use. Tap what you need and we will bring the right people to the top.</p>
    <div class="gk-chips"><span>&#128188; 15 local pros</span><span>&#9989; Money-saving checklist</span><span>&#127379; Free help you can use today</span><span>&#128205; All close to home</span></div>
  </div>
  <p class="gk-pcred">Photo: Iracaz, CC BY-SA 3.0</p>
</header>

<nav class="gk-nav" id="gk-nav" aria-label="Jump to section"><a href="#gk-plan">What I need</a><a href="#gk-check">Checklist</a><a href="#gk-payroll">Payroll</a><a href="#gk-money">Taxes &amp; books</a><a href="#gk-insure">Insurance</a><a href="#gk-planning">Planning</a><a href="#gk-legal">Legal</a><a href="#gk-tech">Tech</a><a href="#gk-grow">Grow</a><a href="#gk-free">Free help</a><a href="#gk-faq">FAQ</a></nav>

<section class="gk-sec" id="gk-plan">
  <p class="gk-label">Start here</p>
  <h2 class="gk-h2">What do you need help with?</h2>
  <p class="gk-p">Pick one and we will move the right local pros to the top of every section. Tap the &#9825; on anyone you like to build your own business team, then share it with your partner or office manager.</p>
  <div class="gk-finder gk-rv" id="gk-finder">
    <p class="gk-fq">I need help with...</p>
    <div class="gk-frow"><button type="button" data-f="who" data-v="pay">&#128176; Payroll &amp; HR</button><button type="button" data-f="who" data-v="tax">&#129534; Taxes</button><button type="button" data-f="who" data-v="books">&#128210; Bookkeeping</button><button type="button" data-f="who" data-v="ins">&#128737;&#65039; Insurance</button><button type="button" data-f="who" data-v="plan">&#128200; Retirement &amp; planning</button><button type="button" data-f="who" data-v="legal">&#9878;&#65039; Legal</button><button type="button" data-f="who" data-v="tech">&#128187; Tech &amp; IT</button><button type="button" data-f="who" data-v="grow">&#128640; Getting more customers</button></div>
    <div class="gk-fgo"><button type="button" class="gk-btn" id="gk-fgo">Show me who can help &darr;</button><span id="gk-fout" aria-live="polite"></span></div>
  </div>
  <button type="button" class="gk-next" data-to="gk-check"><span><small>Next up</small><b>9 quick ways to stop leaking money</b></span><em>&darr;</em></button>
</section>

<section class="gk-sec gk-light" id="gk-check">
  <p class="gk-label">The money-saving checklist</p>
  <h2 class="gk-h2">9 quick ways to stop leaking money</h2>
  <p class="gk-p">Check off what you already do. Your progress is saved on this device, so you can come back and finish the list.</p>
  <div class="bz-check gk-rv" id="bz-check">
    <div class="bz-prog"><div class="bz-bar"><i id="bz-fill"></i></div><span id="bz-n">0 of 9 done</span></div>
    CHECKLIST
  </div>
  <button type="button" class="gk-next" data-to="gk-payroll"><span><small>Next up</small><b>Payroll handled by a neighbor</b></span><em>&darr;</em></button>
</section>

""".replace("IMG", IMG).replace("CHECKLIST", check_html)

body += section("gk-payroll", "01", "File 01 &middot; Payroll &amp; HR", "Payroll handled by a neighbor",
                "Payroll mistakes are expensive and stressful. Handing it to a local pro means on-time filings, fewer penalties and one less thing on your plate every Friday.",
                payroll, ("gk-money", "Taxes, accounting and bookkeeping"))
body += section("gk-money", "02", "File 02 &middot; Taxes &amp; books", "Taxes, accounting and bookkeeping",
                "Good books all year are the cheapest tax strategy there is. These local pros keep your numbers clean so tax season is a review, not a scramble.",
                money, ("gk-insure", "Protect what you have built"), light=True)
body += section("gk-insure", "03", "File 03 &middot; Business insurance", "Protect what you have built",
                "A local agent who knows Long Island can review your liability, property, vehicles and employee benefits in one sitting, and shop it if you are overpaying.",
                insure, ("gk-planning", "Plan for your future, not just this quarter"))
body += section("gk-planning", "04", "File 04 &middot; Retirement &amp; planning", "Plan for your future, not just this quarter",
                "Owners are great at taking care of everyone else. A planner can help you set up a retirement plan for yourself and your team and keep the bigger picture on track.",
                plan, ("gk-legal", "Legal help, estate plans and protecting your name"), light=True)
body += section("gk-legal", "05", "File 05 &middot; Legal", "Legal help, estate plans and protecting your name",
                "From wills and trusts to trademarks and contracts, a little legal planning now saves a lot of money and heartache later.",
                legal, ("gk-tech", "Keep your tech running and your data safe"))
body += section("gk-tech", "06", "File 06 &middot; Tech &amp; IT", "Keep your tech running and your data safe",
                "One ransomware email or a dead server can shut a small business down for days. Local IT support keeps you backed up, secure and online.",
                tech, ("gk-grow", "Get more local customers"), light=True)
body += section("gk-grow", None, "Grow", "Get more local customers",
                "The best customers live right down the road. Meet other owners who send referrals, and make sure your neighbors can find you.",
                grow, ("gk-free", "Free help most owners never use"))
body += free
body += """<section class="gk-sec gk-light" id="gk-faq">
  <p class="gk-label">Quick answers</p>
  <h2 class="gk-h2">Questions we hear from local owners</h2>
  <div class="gk-tips">FAQS</div>
  <div class="bz-cta gk-rv"><div><b>Own a business in Three Village?</b><p>Join the neighbors in business on our website and free community app. 100,000+ website and app visitors and 100,000+ social media views every month, all local.</p></div><a class="gk-btn" href="https://www.threevillagelocal.com/join">List my business free &rarr;</a></div>
</section>

<footer class="gk-src">
  <p><strong>Sources:</strong> Business details from each business's Three Village Local profile. Free resources from Stony Brook University's Small Business Development Center, SCORE Long Island and the Three Village Chamber of Commerce, checked October 5, 2026. This guide is general information, not tax, legal or financial advice. Talk to a licensed professional about your situation.</p>
  <p><strong>Photos:</strong> Hero: Stony Brook Village shops by Iracaz (CC BY-SA 3.0) via Wikimedia Commons. Section photos from Pexels (illustrative, not of the named businesses).</p>
</footer>

<div id="gk-mylist" role="region" aria-label="My business team"><b>My business team <span class="gk-mln">0</span></b><button type="button" class="gk-mlview">View</button><button type="button" class="gk-mlshare">Share</button></div>
</div>

<script>(function(){var r=document.getElementById('bz-check');if(!r)return;var K='bz-check-2026',s={};try{s=JSON.parse(localStorage.getItem(K)||'{}')}catch(e){}
var bs=[].slice.call(r.querySelectorAll('input[data-k]')),f=document.getElementById('bz-fill'),n=document.getElementById('bz-n');
function up(){var d=bs.filter(function(b){return b.checked}).length;f.style.width=(d/bs.length*100)+'%';n.textContent=d===bs.length?'All 9 done. Nice work!':d+' of '+bs.length+' done'}
bs.forEach(function(b){b.checked=!!s[b.getAttribute('data-k')];b.addEventListener('change',function(){s[b.getAttribute('data-k')]=b.checked;try{localStorage.setItem(K,JSON.stringify(s))}catch(e){}up();try{if(window.gtag)gtag('event','guide_click',{action:'checklist',guide:'bizguide2026'})}catch(e){}})});up()})();</script>
<script type="application/ld+json">FAQLD</script>
<script src="GKBASE/guide.js" defer></script>
<style>
#post-content .post-image-container,#post-content .post-image-container + hr{display:none!important}
.bz-check{background:#fff;border:1px solid #e3e9f0;border-radius:18px;padding:20px 18px;box-shadow:0 6px 22px rgba(19,35,58,.06)}
.bz-prog{display:flex;align-items:center;gap:14px;margin-bottom:12px}.bz-bar{flex:1;height:10px;border-radius:99px;background:#e8eef6;overflow:hidden}.bz-bar i{display:block;height:100%;width:0;background:linear-gradient(90deg,#1f5fae,#3d8bff);border-radius:99px;transition:width .4s}
#bz-n{font-weight:700;color:#13233a;font-size:14px;white-space:nowrap}
.bz-ck{display:flex;gap:14px;align-items:flex-start;padding:13px 4px;border-top:1px solid #eef2f7;cursor:pointer}
.bz-ck input{position:absolute;opacity:0;pointer-events:none}
.bz-box{flex:0 0 26px;height:26px;border-radius:8px;border:2px solid #9db3cf;margin-top:2px;display:flex;align-items:center;justify-content:center;transition:all .2s;background:#fff}
.bz-ck input:checked+.bz-box{background:#1f5fae;border-color:#1f5fae}.bz-ck input:checked+.bz-box:after{content:"\\2713";color:#fff;font-weight:800;font-size:16px}
.bz-ck input:focus-visible+.bz-box{outline:3px solid #8ec5ff;outline-offset:2px}
.bz-t b{display:block;color:#13233a;font-size:16px;line-height:1.3}.bz-t small{display:block;color:#5c6b80;font-size:14px;line-height:1.45;margin-top:3px}
.bz-ck input:checked~.bz-t b{color:#1f5fae}
.bz-free{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(260px,100%),1fr));gap:16px}
.bz-fr{background:#fff;border:1px solid #e3e9f0;border-radius:18px;padding:18px;box-shadow:0 6px 22px rgba(19,35,58,.06)}
.bz-fr b{display:block;color:#13233a;font-size:17px;line-height:1.25}.bz-fr p{color:#4a5a6e;font-size:14.5px;line-height:1.5;margin:8px 0 12px!important}
.bz-fr a{display:inline-block;margin:0 12px 6px 0;font-weight:700;color:#1f5fae;text-decoration:none;font-size:14px}
.bz-cta{margin-top:26px;display:flex;flex-wrap:wrap;gap:16px;align-items:center;justify-content:space-between;background:#13233a;color:#fff;border-radius:20px;padding:22px}
.bz-cta b{font-size:20px}.bz-cta p{color:#cfe0f5;margin:6px 0 0!important;font-size:15px;line-height:1.45;max-width:560px}
</style>""".replace("FAQS", faq_html).replace("FAQLD", faq_ld)

open(os.path.join(HERE, "post.html"), "w", encoding="utf-8").write(body)
kit = "https://cdn.jsdelivr.net/gh/threevillagelocal-cloud/3vl-assets@%s/posts/guide-kit" % SHA
open(os.path.join(HERE, "post.final.html"), "w", encoding="utf-8").write(body.replace("GKBASE", kit))
pv = ('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Business Owner\'s Toolkit Preview</title>'
      '<link href="https://fonts.googleapis.com/css2?family=Radio+Canada:wght@500;600;700&display=swap" rel="stylesheet">'
      '<style>body{margin:0;background:#f3f4f6;font-family:\'Radio Canada\',sans-serif}.wrap{max-width:900px;margin:0 auto;padding:20px 12px}</style></head>'
      '<body><div class="wrap"><div id="post-content">' + body.replace("GKBASE", kit) + '</div></div></body></html>')
open(os.path.join(HERE, "preview.html"), "w", encoding="utf-8").write(pv)
print("ok", len(body))
