"""Websites landing page. Owner 10/22/2026: "make the websites page look like the services page except without the social media
promotion. copy exact" + "keep the 2 packages for the websites". So this page is the /services page (same page.html sections,
page.css, page.js, hero photo, form) with the social-media service parts removed and the bundles replaced by the two website
packages (AI-Ready, AI-Powered), member vs regular pricing. "Get started" -> /website-start brief form (owner 10/21: no payment
on the site). Old standalone design kept in build_v1_2026-10-22.py.
    python site/websites-page/build.py          -> widget "3VL Page Websites Preview" + hidden /preview-websites
    python site/websites-page/build.py --live   -> widget "3VL Page Websites" + /websites (indexable)"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SV = os.path.join(HERE, "..", "services-page")
sys.path.insert(0, SV)
import deploy as D

LINKS = json.load(open("C:/Users/Matt/Documents/3vl-private/website-offer/stripe.json"))
PR = {k: (v["setup"], v["monthly"]) for k, v in LINKS.items()}

D.NAME = "3VL Page Websites" if D.LIVE else "3VL Page Websites Preview"   # preview has its own widget so it never changes the live page
D.SLUG = "websites" if D.LIVE else "preview-websites"
D.TITLE = "AI-Ready Websites for Long Island Businesses | Three Village Local"
D.DESC = ("Websites built for customers and for AI: designed, built and hosted by one local team, set up for Google and AI search, "
          "then launched to the whole town on Three Village Local. Member pricing for Three Village Local businesses.")
D.FB_TITLE = "AI-Driven Websites: Design, Build, Host"
D.FB_IMAGE = "/share/ai-websites-v1.jpg"   # BD mangles external og:image URLs; redirect 2253 -> 3vl-share/site/websites/share-ai-websites-v1.jpg

SHARE = "https://threevillagelocal-cloud.github.io/3vl-share/site/websites/"
START = "/website-start?plan="


def sec(src, cls):
    i = src.index('<section class="' + cls)
    return i, src.index('</section>', i) + len('</section>')


def cut(src, cls):
    i, j = sec(src, cls)
    return src[:i] + src[j:].lstrip("\n")


def swap(src, cls, new):
    i, j = sec(src, cls)
    return src[:i] + new + src[j:]


def rep(src, a, b):
    assert a in src, a[:80]
    return src.replace(a, b, 1)


def card(key, name, one, items, pop=False):
    m, r = PR["web-%s-member" % key], PR["web-%s-regular" % key]
    lis = "".join("<li%s>%s</li>" % (' class="tvs-star"' if "Three Village Local" in i else "", i) for i in items)
    return '''    <article class="tvs-card%s tvs-up" data-b="web%s">
%s      <p class="tvs-cname">%s</p>
      <p class="tvs-cfor">%s</p>
      <p class="tvs-was"></p>
      <p class="tvs-price"><sup>$</sup><b>%s</b></p>
      <p class="tvs-mo">+ <b>$%s</b>/mo</p>
      <p class="tvs-save"></p>
      <ul>
        %s
      </ul>
      <a class="tvs-btn %s tvs-wide tvw-go" data-m="%s" data-r="%s" href="%s">Get started &rarr;</a>
    </article>
''' % (" tvs-pop" if pop else "", key, '      <p class="tvs-badge">Most popular</p>\n' if pop else "", name, one, "{:,}".format(m[0]), m[1],
       "\n        ".join(lis.replace("</li><li", "</li>\n<li").split("\n")),
       "tvs-blue" if pop else "tvs-line", START + "web-%s-member" % key, START + "web-%s-regular" % key, START + "web-%s-member" % key)


READY = card("ready", "AI-Ready", "AI can find you. Built so Google and AI assistants understand and recommend your business.", [
    "Custom design, up to 5 pages, written for you",
    "Code AI can actually read, not hidden behind scripts",
    "Your business clearly labeled for Google and AI: services, hours, area, reviews",
    "A page for every service, plus FAQs the way people ask",
    "Fast, mobile-first and secure, with a lead form to your inbox",
    "Hosting, domain setup and updates included",
    "3VL Launch Spotlight + 3 months Featured on Three Village Local"])
POWERED = card("powered", "AI-Powered", "AI works for you. Everything in AI-Ready, plus tools that bring in customers on their own.", [
    "Everything in AI-Ready",
    "Your own AI assistant answering customers 24/7 and sending you the lead",
    "Fresh content, automatically: 2 blog posts or industry updates a month",
    "Your best reviews showcased on your site",
    "Online booking or quote requests",
    "Monthly feature on Three Village Local"], pop=True)

SITES = [("coltrain", "Coltrain Mortgage"), ("sbna", "SBNA"), ("lga", "LGA Marketing"), ("jm", "JM Management Solutions"), ("3vl", "Three Village Local")]
row = "".join('<img src="%ssite-%s.webp" alt="%s website, built by our team" loading="lazy" decoding="async"%s>' % (SHARE, k, n, "") for k, n in SITES)
row2 = "".join('<img src="%ssite-%s.webp" alt="" aria-hidden="true" loading="lazy" decoding="async">' % (SHARE, k) for k, n in SITES)

WORK = '''<section class="tvs-sec tvs-work" id="tvs-work">
  <div class="tvs-wtop">
    <div class="tvs-wtxt tvs-up">
      <p class="tvs-eyebrow">Real websites for real local businesses</p>
      <h2>See what you get.</h2>
      <p>Every site below was designed, built and hosted by our team, including Three Village Local itself.</p>
      <ul class="tvs-wlist">
        <li><b>Custom design</b>Built around your business, not a template</li>
        <li><b>Fast on every phone</b>Most of your visitors are on their phones</li>
        <li><b>Set up for Google and AI search</b>So ChatGPT, Gemini and Google can recommend you</li>
        <li><b>Hosted and cared for</b>Security, updates and edits handled for you</li>
      </ul>
    </div>
    <figure class="tvs-vphone tvw-phfig tvs-up">
      <div class="tvw-phone"><div class="tvw-phone-screen"><div class="tvw-phone-bar"><span>9:41</span><span class="tvw-phone-sig">&#9679;&#9679;&#9679; &#9646;</span></div><div class="tvw-phone-view"><img src="''' + SHARE + '''phone-home.webp" alt="Three Village Local homepage on a phone" width="780" height="5400" loading="lazy" decoding="async"></div></div><span class="tvw-phone-island"></span></div>
      <figcaption>Three Village Local on a phone, <b>built by our team</b></figcaption>
    </figure>
  </div>
  <div class="tvs-mq tvs-mq1 tvw-sites"><div class="tvs-mqt">''' + row + row2 + '''</div></div>
</section>'''

BUNDLES = '''<section class="tvs-sec tvs-bundles" id="tvs-bundles">
  <div class="tvs-head tvs-up">
    <p class="tvs-eyebrow">Packages</p>
    <h2>Pick a package. We handle the rest.</h2>
    <p><b>AI-Ready</b> means AI can find you. <b>AI-Powered</b> means AI works for you. Both are designed, built and hosted by us. Prices shown are <b>Three Village Local member prices</b>.</p>
  </div>
  <div class="tvs-tiers tvs-up" role="tablist" aria-label="Choose your membership to see your price">
    <button type="button" role="tab" data-t="all">Not a member</button>
    <button type="button" role="tab" data-t="vip" class="on">3VL member<em>Member price</em></button>
  </div>
  <div class="tvs-cards tvw-two">
''' + READY + POWERED + '''  </div>
  <p class="tvs-fine tvs-up">Your start-up fee includes your first month. After that, the monthly plan covers hosting, security, updates and support, month to month. Your domain is registered in your name.</p>
</section>'''

src = open(os.path.join(SV, "page.html"), encoding="utf-8").read()
h = src
# hero: websites only, no social/video/drone/marketing services
h = rep(h, "Websites + Google + AI search + Social + Video + Drone + Marketing", "Websites + Google + AI search + Hosting")
h = rep(h, "Your website, Google, AI search, social media, video and marketing, built by one local team to work as one. Then we launch it in front of the whole town on Three Village Local.",
        "Your website, Google and AI search, designed, built and hosted by one local team. Then we launch it in front of the whole town on Three Village Local.")
h = rep(h, 'href="#tvs-bundles">See the bundles</a>', 'href="#tvs-bundles">See the packages</a>')
h = re.sub(r'\n    <a class="tvs-newlink"[^\n]*</a>', "", h)
h = cut(h, "tvs-sec tvs-social")                  # "Your content, seen all over town" (social media service)
h = swap(h, "tvs-sec tvs-work", WORK)              # promo video + social posts -> real websites + phone
h = swap(h, "tvs-sec tvs-bundles", BUNDLES)        # social bundles -> the 2 website packages
h = cut(h, "tvs-founding")                        # owner 10/22: remove the founding clients box
h = cut(h, "tvs-stats")                           # owner 10/22: remove the 4-number stats strip
h = re.sub(r'<a class="tvs-newbiz[^\n]*</a>\n\n', "", h)
h = rep(h, "<p>We pick the right bundle together and map out your first month.</p>", "<p>We pick the right package together and map out your site.</p>")
h = rep(h, "<p>No long contracts. Bundles are a one-time build, and monthly plans are month to month.</p>",
        "<p>No long contracts. Your site is a one-time build, and the monthly plan is month to month.</p>")
h = rep(h, "<p>Half to start, the rest at launch once you love it.</p>", "<p>After your free consultation we send one simple invoice. Your start-up fee includes your first month.</p>")
h = rep(h, "<p>No. Anyone can book. Members save on every bundle, and VIP members save the most.</p>", "<p>No. Anyone can book. Three Village Local members get member pricing on both packages.</p>")
h = rep(h, "mailto:hello@threevillagelocal.com?subject=Services", "mailto:hello@threevillagelocal.com?subject=Websites")
for m in re.finditer(r".{60}[Bb]undle.{40}", h): print("LEFT:", m.group(0))
HTML = h

PRICES = ("var P={webready:{all:[%d,%d],free:[%d,%d],featured:[%d,%d],vip:[%d,%d]},webpowered:{all:[%d,%d],free:[%d,%d],featured:[%d,%d],vip:[%d,%d]},"
                    % (PR["web-ready-regular"] + PR["web-ready-member"] * 3 + PR["web-powered-regular"] + PR["web-powered-member"] * 3))
GOJS = '''<script>(function(){function upd(){var b=document.querySelector('#tvs .tvs-tiers button.on'),m=!b||b.getAttribute('data-t')!=='all';
[].forEach.call(document.querySelectorAll('#tvs .tvw-go'),function(a){a.href=m?a.getAttribute('data-m'):a.getAttribute('data-r')})}
document.addEventListener('click',function(e){if(e.target.closest&&e.target.closest('#tvs .tvs-tiers button'))setTimeout(upd,0)});upd()})();</script>'''

CSS = '''
.tvw-two{grid-template-columns:repeat(2,minmax(0,1fr))!important;max-width:820px;margin-left:auto;margin-right:auto}
.tvw-phfig{display:flex;flex-direction:column;align-items:center}
.tvs-wtop:has(.tvw-phfig){grid-template-columns:1fr 290px;max-width:960px}
.tvw-phone{position:relative;width:270px;padding:10px;border-radius:48px;background:linear-gradient(145deg,#2a3242,#0a0d13);box-shadow:0 36px 64px -24px rgba(9,30,66,.5),0 0 0 2px #3a4456 inset,0 0 0 1px #11151c}
.tvw-phone-screen{position:relative;aspect-ratio:390/844;overflow:hidden;border-radius:38px;background:#13294b;display:flex;flex-direction:column}
.tvw-phone-bar{flex:none;height:40px;display:flex;align-items:center;justify-content:space-between;padding:6px 26px 0;color:#fff;font:600 12px/1 -apple-system,Segoe UI,sans-serif}
.tvw-phone-sig{font-size:8px;letter-spacing:1px}
.tvw-phone-view{position:relative;flex:1;overflow:hidden;background:#fff}
.tvw-phone-view img{display:block!important;width:100%!important;max-width:none!important;height:auto!important;max-height:none!important;aspect-ratio:780/5400;object-fit:fill;animation:tvwPh 34s ease-in-out infinite}
.tvw-phone-island{position:absolute;top:19px;left:50%;width:80px;height:23px;margin-left:-40px;border-radius:20px;background:#05070b}
@keyframes tvwPh{0%,6%{transform:translateY(0)}46%,54%{transform:translateY(-70%)}94%,100%{transform:translateY(0)}}
.tvw-sites .tvs-mqt img{border-radius:12px;box-shadow:0 14px 30px -14px rgba(9,30,66,.35);border:1px solid #dfe6f0;background:#fff}
@media (prefers-reduced-motion:reduce){.tvw-phone-view img{animation:none}}
@media (max-width:760px){.tvw-two{grid-template-columns:1fr!important}.tvs-wtop:has(.tvw-phfig){grid-template-columns:1fr}.tvw-phone{width:240px}}
'''

_rd = D.rd


def rd(f):
    if f == "page.html":
        assert "\\" not in HTML
        return HTML
    s = _rd(f)
    if f == "page.css":
        return s + CSS
    if f == "page.js":
        s = rep(s, "var P={", PRICES)
        return s + GOJS
    return s


D.rd = rd
if __name__ == "__main__":
    D.main()
