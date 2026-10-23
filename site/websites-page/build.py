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
PR["web-ready-regular"] = (1499, 59)     # owner 10/22: anchor regular price so member pricing reads as a real deal
PR["web-powered-regular"] = (2499, 129)

D.NAME = "3VL Page Websites" if D.LIVE else "3VL Page Websites Preview"   # preview has its own widget so it never changes the live page
D.SLUG = "websites" if D.LIVE else "preview-websites"
D.TITLE = "AI-Ready Websites for Long Island Businesses | Three Village Local"
D.DESC = ("Websites built for customers and for AI: designed, built and hosted by one local team, set up for Google and AI search, "
          "then launched to the whole town on Three Village Local. Member pricing for Three Village Local businesses.")
D.FB_TITLE = "AI-Driven Websites: Design, Build, Host"
D.FB_IMAGE = "/share/ai-websites-v1.jpg"   # BD mangles external og:image URLs; redirect 2253 -> 3vl-share/site/websites/share-ai-websites-v1.jpg

SHARE = "https://threevillagelocal-cloud.github.io/3vl-share/site/websites/"
D.HEAD = ""   # tried a hero preload 10/22: no LCP gain (BD template is the bottleneck)
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
    "Hosting, security and ongoing updates included: just message us your changes",
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
      <div class="tvw-phone"><div class="tvw-phone-screen"><div class="tvw-phone-bar"><span>9:41</span><span class="tvw-phone-sig">&#9679;&#9679;&#9679; &#9646;</span></div><div class="tvw-phone-view"><div class="tvw-ph-page"><img src="''' + SHARE + '''phone-home.webp" alt="Three Village Local homepage on a phone" width="780" height="5400" loading="lazy" decoding="async"><div class="tvw-ph-row"><img src="''' + SHARE + '''phone-strip.webp" alt="" aria-hidden="true" width="3364" height="1062" loading="lazy" decoding="async"></div></div></div></div><span class="tvw-phone-island"></span></div>
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
  <p class="tvs-fine tvs-up"><b>Half to start, the rest only when you love it.</b> Your start-up fee includes your first month. After that, your monthly plan covers hosting, security and support, plus your updates and changes: email or text us what you need and we handle it. Month to month. Your domain is registered in your name.</p>
</section>'''

ADDS_SEC = '''<section class="tvs-sec tvw-adds" id="tvw-adds">
  <div class="tvs-head tvs-up"><p class="tvs-eyebrow">Add-ons</p><h2>More we can build for you.</h2>
    <p>Add any of these to your package, now or later. Same local team, same care.</p></div>
  <div class="tvw-add-grid"><div class="tvw-add tvs-up"><span>&#129302;</span><b>AI chat assistant</b><p>Answers customer questions 24/7 on your site and sends you the lead.</p></div><div class="tvw-add tvs-up"><span>&#128197;</span><b>Online booking</b><p>Appointments, reservations or quote requests that land in your calendar.</p></div><div class="tvw-add tvs-up"><span>&#128722;</span><b>Online store + payments</b><p>Sell products, gift cards or deposits with Stripe, Square or Shopify.</p></div><div class="tvw-add tvs-up"><span>&#9993;&#65039;</span><b>Email on your domain</b><p>you@yourbusiness.com, set up with Google Workspace.</p></div><div class="tvw-add tvs-up"><span>&#128260;</span><b>Site rescue + move</b><p>Move off Wix, Squarespace or GoDaddy and fix what was holding you back.</p></div><div class="tvw-add tvs-up"><span>&#9889;</span><b>Speed tune-up</b><p>Make a slow site load fast on phones, scored on Google's own test.</p></div><div class="tvw-add tvs-up"><span>&#128200;</span><b>Lead tracking + reports</b><p>See where calls and form leads come from, in plain English each month.</p></div><div class="tvw-add tvs-up"><span>&#127919;</span><b>Ad landing pages</b><p>Pages built for Google and Facebook ads, with conversion tracking.</p></div><div class="tvw-add tvs-up"><span>&#11088;</span><b>Reviews showcase</b><p>Your best Google reviews shown on your site, updated automatically.</p></div><div class="tvw-add tvs-up"><span>&#129518;</span><b>Custom tools</b><p>Quote estimators, calculators, menus, event calendars and more.</p></div><div class="tvw-add tvs-up"><span>&#128240;</span><b>Newsletter signup</b><p>Grow an email list of local customers right from your site.</p></div><div class="tvw-add tvs-up"><span>&#9855;</span><b>Accessibility upgrades</b><p>Easier to use for everyone, built to modern accessibility standards.</p></div></div>
  <p class="tvs-fine tvs-up">Pricing depends on what you need. <a href="#tvs-book">Send us a message</a> and we will put it together for you.</p>
</section>'''

STRIP_SEC = '''<section class="tvw-strip tvs-up"><p>Get recommended on the AI tools your customers use</p><div class="tvw-logo-row"><span class="tvw-logo"><svg viewBox="0 0 256 260" aria-hidden="true"><path d="M239.184 106.203a64.72 64.72 0 0 0-5.576-53.103C219.452 28.459 191 15.784 163.213 21.74A65.586 65.586 0 0 0 52.096 45.22a64.72 64.72 0 0 0-43.23 31.36c-14.31 24.602-11.061 55.634 8.033 76.74a64.67 64.67 0 0 0 5.525 53.102c14.174 24.65 42.644 37.324 70.446 31.36a64.72 64.72 0 0 0 48.754 21.744c28.481.025 53.714-18.361 62.414-45.481a64.77 64.77 0 0 0 43.229-31.36c14.137-24.558 10.875-55.423-8.083-76.483m-97.56 136.338a48.4 48.4 0 0 1-31.105-11.255l1.535-.87l51.67-29.825a8.6 8.6 0 0 0 4.247-7.367v-72.85l21.845 12.636c.218.111.37.32.409.563v60.367c-.056 26.818-21.783 48.545-48.601 48.601M37.158 197.93a48.35 48.35 0 0 1-5.781-32.589l1.534.921l51.722 29.826a8.34 8.34 0 0 0 8.441 0l63.181-36.425v25.221a.87.87 0 0 1-.358.665l-52.335 30.184c-23.257 13.398-52.97 5.431-66.404-17.803M23.549 85.38a48.5 48.5 0 0 1 25.58-21.333v61.39a8.29 8.29 0 0 0 4.195 7.316l62.874 36.272l-21.845 12.636a.82.82 0 0 1-.767 0L41.353 151.53c-23.211-13.454-31.171-43.144-17.804-66.405zm179.466 41.695l-63.08-36.63L161.73 77.86a.82.82 0 0 1 .768 0l52.233 30.184a48.6 48.6 0 0 1-7.316 87.635v-61.391a8.54 8.54 0 0 0-4.4-7.213m21.742-32.69l-1.535-.922l-51.619-30.081a8.39 8.39 0 0 0-8.492 0L99.98 99.808V74.587a.72.72 0 0 1 .307-.665l52.233-30.133a48.652 48.652 0 0 1 72.236 50.391zM88.061 139.097l-21.845-12.585a.87.87 0 0 1-.41-.614V65.685a48.652 48.652 0 0 1 79.757-37.346l-1.535.87l-51.67 29.825a8.6 8.6 0 0 0-4.246 7.367zm11.868-25.58L128.067 97.3l28.188 16.218v32.434l-28.086 16.218l-28.188-16.218z"/></svg>ChatGPT</span><span class="tvw-logo"><svg viewBox="0 0 256 256" aria-hidden="true"><defs><filter id="lg0" width="39.274" height="43.217" x="-19.824" y="13.152" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_10859_4895" stdDeviation="2.46"/></filter><filter id="lg1" width="84.868" height="85.688" x="-15.001" y="-40.257" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_10859_4895" stdDeviation="11.891"/></filter><filter id="lg2" width="79.454" height="90.917" x="-20.776" y="11.927" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_10859_4895" stdDeviation="10.109"/></filter><filter id="lg3" width="79.731" height="81.505" x="-19.845" y="15.459" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_10859_4895" stdDeviation="10.109"/></filter><filter id="lg4" width="75.117" height="73.758" x="29.832" y="-11.552" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_10859_4895" stdDeviation="9.606"/></filter><filter id="lg5" width="78.135" height="78.758" x="-38.583" y="-16.253" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_10859_4895" stdDeviation="8.706"/></filter><filter id="lg6" width="78.877" height="77.539" x="8.107" y="-5.966" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_10859_4895" stdDeviation="7.775"/></filter><filter id="lg7" width="56.272" height="51.81" x="13.587" y="-18.488" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_10859_4895" stdDeviation="6.957"/></filter><filter id="lg8" width="70.856" height="69.306" x="-15.526" y="-31.297" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_10859_4895" stdDeviation="5.876"/></filter><filter id="lg9" width="55.502" height="51.571" x="-14.168" y="20.964" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_10859_4895" stdDeviation="7.273"/></filter><linearGradient id="lg10" x1="18.447" x2="52.153" y1="43.42" y2="15.004" gradientUnits="userSpaceOnUse"><stop stop-color="#4893fc"/><stop offset=".27" stop-color="#4893fc"/><stop offset=".777" stop-color="#969dff"/><stop offset="1" stop-color="#bd99fe"/></linearGradient></defs><path fill="#fff" d="M228.265 114.441c-19.721-8.49-36.974-20.134-51.776-34.927c-14.792-14.789-26.436-32.056-34.93-51.779a154 154 0 0 1-7.884-23.295A5.86 5.86 0 0 0 127.999 0a5.86 5.86 0 0 0-5.674 4.44a154 154 0 0 1-7.882 23.295c-8.494 19.723-20.141 36.99-34.929 51.779c-14.794 14.793-32.058 26.437-51.779 34.927a154 154 0 0 1-23.297 7.889A5.855 5.855 0 0 0 0 127.999a5.86 5.86 0 0 0 4.438 5.678a154 154 0 0 1 23.297 7.886c19.721 8.49 36.978 20.139 51.779 34.93c14.795 14.789 26.435 32.055 34.929 51.774a154 154 0 0 1 7.882 23.297a5.854 5.854 0 0 0 5.674 4.436a5.85 5.85 0 0 0 5.676-4.436a154 154 0 0 1 7.884-23.297q12.742-29.58 34.93-51.774c14.793-14.791 32.055-26.44 51.776-34.93a154 154 0 0 1 23.297-7.886a5.86 5.86 0 0 0 4.438-5.678a5.855 5.855 0 0 0-4.438-5.669a154.4 154.4 0 0 1-23.297-7.889"/><g filter="url(#lg0)" mask="url(#lg11)" transform="translate(-.101 -.049)scale(3.9436)"><ellipse cx="14.407" cy="16.95" fill="#ffe432" rx="14.407" ry="16.95" transform="rotate(19.552 -44.576 -16.496)"/></g><g filter="url(#lg1)" mask="url(#lg11)" transform="translate(-.101 -.049)scale(3.9436)"><ellipse cx="27.433" cy="2.587" fill="#fc413d" rx="18.652" ry="19.062"/></g><g filter="url(#lg2)" mask="url(#lg11)" transform="translate(-.101 -.049)scale(3.9436)"><ellipse cx="18.951" cy="57.386" fill="#00b95c" rx="19.493" ry="25.253" transform="rotate(-2.799 18.951 57.386)"/></g><g filter="url(#lg2)" mask="url(#lg11)" transform="translate(-.101 -.049)scale(3.9436)"><ellipse cx="18.951" cy="57.386" fill="#00b95c" rx="19.493" ry="25.253" transform="rotate(-2.799 18.951 57.386)"/></g><g filter="url(#lg3)" mask="url(#lg11)" transform="translate(-.101 -.049)scale(3.9436)"><ellipse cx="20.02" cy="56.211" fill="#00b95c" rx="19.107" ry="21.035" transform="rotate(-31.318 20.02 56.211)"/></g><g filter="url(#lg4)" mask="url(#lg11)" transform="translate(-.101 -.049)scale(3.9436)"><ellipse cx="67.391" cy="25.327" fill="#3186ff" rx="18.346" ry="17.667"/></g><g filter="url(#lg5)" mask="url(#lg11)" transform="translate(-.101 -.049)scale(3.9436)"><ellipse cx="21.222" cy="22.384" fill="#fbbc04" rx="21.222" ry="22.384" transform="rotate(37.252 9.752 -8.009)"/></g><g filter="url(#lg6)" mask="url(#lg11)" transform="translate(-.101 -.049)scale(3.9436)"><ellipse cx="24.469" cy="22.604" fill="#3186ff" rx="24.469" ry="22.604" transform="rotate(34.51 19.587 64.852)"/></g><g filter="url(#lg7)" mask="url(#lg11)" transform="translate(-.101 -.049)scale(3.9436)"><path fill="#749bff" d="M54.984-2.336c2.833 3.852-.808 11.34-8.131 16.727s-15.557 6.631-18.39 2.78c-2.833-3.853.807-11.342 8.13-16.728s15.558-6.631 18.39-2.78"/></g><g filter="url(#lg8)" mask="url(#lg11)" transform="translate(-.101 -.049)scale(3.9436)"><ellipse cx="19.902" cy="3.356" fill="#fc413d" rx="27.971" ry="17.388" transform="rotate(-42.848 19.902 3.356)"/></g><g filter="url(#lg9)" mask="url(#lg11)" transform="translate(-.101 -.049)scale(3.9436)"><ellipse cx="13.583" cy="46.75" fill="#ffee48" rx="14.989" ry="8.717" transform="rotate(35.592 13.583 46.75)"/></g><mask id="lg11" width="65" height="65" x="0" y="0" maskUnits="userSpaceOnUse" style="mask-type:alpha"><path d="M32.447 0c.68 0 1.273.465 1.439 1.125a39 39 0 0 0 1.999 5.905q3.23 7.5 8.854 13.125q5.627 5.626 13.125 8.855a39 39 0 0 0 5.906 1.999c.66.166 1.124.758 1.124 1.438s-.464 1.273-1.125 1.439a39 39 0 0 0-5.905 1.999q-7.5 3.23-13.125 8.854q-5.625 5.627-8.854 13.125a39 39 0 0 0-2 5.906a1.485 1.485 0 0 1-1.438 1.124c-.68 0-1.272-.464-1.438-1.125a39 39 0 0 0-2-5.905q-3.227-7.5-8.854-13.125q-5.625-5.625-13.125-8.854a39 39 0 0 0-5.905-2A1.485 1.485 0 0 1 0 32.448c0-.68.465-1.272 1.125-1.438a39 39 0 0 0 5.905-2q7.5-3.228 13.125-8.854q5.626-5.624 8.855-13.125a39 39 0 0 0 1.999-5.905A1.485 1.485 0 0 1 32.447 0"/><path fill="url(#lg10)" d="M32.447 0c.68 0 1.273.465 1.439 1.125a39 39 0 0 0 1.999 5.905q3.23 7.5 8.854 13.125q5.627 5.626 13.125 8.855a39 39 0 0 0 5.906 1.999c.66.166 1.124.758 1.124 1.438s-.464 1.273-1.125 1.439a39 39 0 0 0-5.905 1.999q-7.5 3.23-13.125 8.854q-5.625 5.627-8.854 13.125a39 39 0 0 0-2 5.906a1.485 1.485 0 0 1-1.438 1.124c-.68 0-1.272-.464-1.438-1.125a39 39 0 0 0-2-5.905q-3.227-7.5-8.854-13.125q-5.625-5.625-13.125-8.854a39 39 0 0 0-5.905-2A1.485 1.485 0 0 1 0 32.448c0-.68.465-1.272 1.125-1.438a39 39 0 0 0 5.905-2q7.5-3.228 13.125-8.854q5.626-5.624 8.855-13.125a39 39 0 0 0 1.999-5.905A1.485 1.485 0 0 1 32.447 0"/></mask></svg>Gemini</span><span class="tvw-logo"><svg viewBox="0 0 256 262" aria-hidden="true"><path fill="#4285f4" d="M255.878 133.451c0-10.734-.871-18.567-2.756-26.69H130.55v48.448h71.947c-1.45 12.04-9.283 30.172-26.69 42.356l-.244 1.622l38.755 30.023l2.685.268c24.659-22.774 38.875-56.282 38.875-96.027"/><path fill="#34a853" d="M130.55 261.1c35.248 0 64.839-11.605 86.453-31.622l-41.196-31.913c-11.024 7.688-25.82 13.055-45.257 13.055c-34.523 0-63.824-22.773-74.269-54.25l-1.531.13l-40.298 31.187l-.527 1.465C35.393 231.798 79.49 261.1 130.55 261.1"/><path fill="#fbbc05" d="M56.281 156.37c-2.756-8.123-4.351-16.827-4.351-25.82c0-8.994 1.595-17.697 4.206-25.82l-.073-1.73L15.26 71.312l-1.335.635C5.077 89.644 0 109.517 0 130.55s5.077 40.905 13.925 58.602z"/><path fill="#eb4335" d="M130.55 50.479c24.514 0 41.05 10.589 50.479 19.438l36.844-35.974C195.245 12.91 165.798 0 130.55 0C79.49 0 35.393 29.301 13.925 71.947l42.211 32.783c10.59-31.477 39.891-54.251 74.414-54.251"/></svg>Google AI Overviews</span><span class="tvw-logo"><svg viewBox="0 0 256 388" aria-hidden="true"><defs><radialGradient id="lg12" cx="93.717%" cy="77.818%" r="143.121%" fx="93.717%" fy="77.818%" gradientTransform="matrix(-.65486 -.5438 .75575 -.4712 .963 1.654)"><stop offset="0%" stop-color="#00cacc"/><stop offset="100%" stop-color="#048fce"/></radialGradient><radialGradient id="lg13" cx="13.893%" cy="71.448%" r="150.086%" fx="13.893%" fy="71.448%" gradientTransform="matrix(.55155 -.39387 .23634 .91917 -.107 .112)"><stop offset="0%" stop-color="#00bbec"/><stop offset="100%" stop-color="#2756a9"/></radialGradient><linearGradient id="lg14" x1="50%" x2="50%" y1="0%" y2="100%"><stop offset="0%" stop-color="#00bbec"/><stop offset="100%" stop-color="#2756a9"/></linearGradient></defs><path fill="url(#lg12)" d="M129.424 122.047c-7.133.829-12.573 6.622-13.079 13.928c-.218 3.147-.15 3.36 6.986 21.722c16.233 41.774 20.166 51.828 20.827 53.243c1.603 3.427 3.856 6.65 6.672 9.544c2.16 2.22 3.585 3.414 5.994 5.024c4.236 2.829 6.337 3.61 22.818 8.49c16.053 4.754 24.824 7.913 32.381 11.664c9.791 4.86 16.623 10.387 20.944 16.946c3.1 4.706 5.846 13.145 7.04 21.64c.468 3.321.47 10.661.006 13.663c-1.008 6.516-3.021 11.976-6.101 16.545c-1.638 2.43-1.068 2.023 1.313-.939c6.74-8.379 13.605-22.7 17.108-35.687c4.24-15.718 4.817-32.596 1.66-48.57c-6.147-31.108-25.786-57.955-53.444-73.06c-1.738-.95-8.357-4.42-17.331-9.085a1633 1633 0 0 1-4.127-2.154c-.907-.477-2.764-1.447-4.126-2.154c-1.362-.708-5.282-2.75-8.711-4.539l-8.528-4.446a6021 6021 0 0 1-8.344-4.357c-8.893-4.655-12.657-6.537-13.73-6.863c-1.125-.343-3.984-.782-4.701-.723c-.152.012-.838.088-1.527.168"/><path fill="url(#lg13)" d="M148.81 277.994c-.493.292-1.184.714-1.537.938c-.354.225-1.137.712-1.743 1.083a8315 8315 0 0 0-13.204 8.137a2848 2848 0 0 0-8.07 4.997a388 388 0 0 1-3.576 2.198c-.454.271-2.393 1.465-4.31 2.654a2652 2652 0 0 1-7.427 4.586a3958 3958 0 0 0-8.62 5.316a3011 3011 0 0 1-7.518 4.637c-1.564.959-3.008 1.885-3.21 2.058c-.3.257-14.205 8.87-21.182 13.121c-5.3 3.228-11.43 5.387-17.705 6.235c-2.921.395-8.45.396-11.363.003c-7.9-1.067-15.176-4.013-21.409-8.666c-2.444-1.826-7.047-6.425-8.806-8.8c-4.147-5.598-6.829-11.602-8.218-18.396c-.32-1.564-.622-2.884-.672-2.935c-.13-.13.105 2.231.528 5.319c.44 3.211 1.377 7.856 2.387 11.829c7.814 30.743 30.05 55.749 60.15 67.646c8.668 3.424 17.415 5.582 26.932 6.64c3.576.4 13.699.56 17.43.276c17.117-1.296 32.02-6.334 47.308-15.996c1.362-.86 3.92-2.474 5.685-3.585a877 877 0 0 0 4.952-3.14c.958-.615 2.114-1.341 2.567-1.614a91 91 0 0 0 2.018-1.268c.656-.424 3.461-2.2 6.235-3.944l11.092-7.006l3.809-2.406l.137-.086l.42-.265l.199-.126l2.804-1.771l9.69-6.121c12.348-7.759 16.03-10.483 21.766-16.102c2.392-2.342 5.997-6.34 6.176-6.848c.037-.104.678-1.092 1.424-2.197c3.036-4.492 5.06-9.995 6.064-16.484c.465-3.002.462-10.342-.005-13.663c-.903-6.42-2.955-13.702-5.167-18.339c-3.627-7.603-11.353-14.512-22.453-20.076c-3.065-1.537-6.23-2.943-6.583-2.924c-.168.009-10.497 6.322-22.954 14.03c-12.457 7.71-23.268 14.4-24.025 14.87s-2.056 1.263-2.888 1.764z"/><path fill="url(#lg14)" d="m.053 241.013l.054 53.689l.695 3.118c2.172 9.747 5.937 16.775 12.482 23.302c3.078 3.07 5.432 4.922 8.768 6.896c7.06 4.177 14.657 6.238 22.978 6.235c8.716-.005 16.256-2.179 24.025-6.928c1.311-.801 6.449-3.964 11.416-7.029l9.032-5.572v-127.4l-.002-58.273c-.002-37.177-.07-59.256-.188-60.988c-.74-10.885-5.293-20.892-12.948-28.461c-2.349-2.323-4.356-3.875-10.336-7.99a25160 25160 0 0 1-12.104-8.336L28.617 5.835C22.838 1.85 22.386 1.574 20.639.949C18.367.136 15.959-.163 13.67.084C6.998.804 1.657 5.622.269 12.171C.053 13.191.013 26.751.01 100.35l-.003 86.975H0z"/></svg>Microsoft Copilot</span><span class="tvw-logo"><svg viewBox="0 0 256 298" aria-hidden="true"><path fill="#3f7e8b" d="m34.831 0l84.689 78.028V.18h16.486v78.197L221.074 0v88.964H256v128.322h-34.819v79.218l-85.175-74.833v75.692H119.52v-74.459l-84.593 74.508v-80.126H0V88.964h34.831zm72.26 105.248H16.487v95.753h18.42v-30.204zm-55.68 72.775v83.052l68.109-59.988v-84.926zm85.069 22.27v-84.212l68.128 61.865v39.34h.088v42.94zm84.701.708h18.333v-95.753h-89.93l71.597 64.87zM204.588 88.964V37.457l-55.904 51.507zm-97.368 0H51.317V37.457z"/></svg>Perplexity</span><span class="tvw-logo"><svg viewBox="0 0 256 257" aria-hidden="true"><path fill="#d97757" d="m50.228 170.321l50.357-28.257l.843-2.463l-.843-1.361h-2.462l-8.426-.518l-28.775-.778l-24.952-1.037l-24.175-1.296l-6.092-1.297L0 125.796l.583-3.759l5.12-3.434l7.324.648l16.202 1.101l24.304 1.685l17.629 1.037l26.118 2.722h4.148l.583-1.685l-1.426-1.037l-1.101-1.037l-25.147-17.045l-27.22-18.017l-14.258-10.37l-7.713-5.25l-3.888-4.925l-1.685-10.758l7-7.713l9.397.649l2.398.648l9.527 7.323l20.35 15.75L94.817 91.9l3.889 3.24l1.555-1.102l.195-.777l-1.75-2.917l-14.453-26.118l-15.425-26.572l-6.87-11.018l-1.814-6.61c-.648-2.723-1.102-4.991-1.102-7.778l7.972-10.823L71.42 0l10.63 1.426l4.472 3.888l6.61 15.101l10.694 23.786l16.591 32.34l4.861 9.592l2.592 8.879l.973 2.722h1.685v-1.556l1.36-18.211l2.528-22.36l2.463-28.776l.843-8.1l4.018-9.722l7.971-5.25l6.222 2.981l5.12 7.324l-.713 4.73l-3.046 19.768l-5.962 30.98l-3.889 20.739h2.268l2.593-2.593l10.499-13.934l17.628-22.036l7.778-8.749l9.073-9.657l5.833-4.601h11.018l8.1 12.055l-3.628 12.443l-11.342 14.388l-9.398 12.184l-13.48 18.147l-8.426 14.518l.778 1.166l2.01-.194l30.46-6.481l16.462-2.982l19.637-3.37l8.88 4.148l.971 4.213l-3.5 8.62l-20.998 5.184l-24.628 4.926l-36.682 8.685l-.454.324l.519.648l16.526 1.555l7.065.389h17.304l32.21 2.398l8.426 5.574l5.055 6.805l-.843 5.184l-12.962 6.611l-17.498-4.148l-40.83-9.721l-14-3.5h-1.944v1.167l11.666 11.406l21.387 19.314l26.767 24.887l1.36 6.157l-3.434 4.86l-3.63-.518l-23.526-17.693l-9.073-7.972l-20.545-17.304h-1.36v1.814l4.73 6.935l25.017 37.59l1.296 11.536l-1.814 3.76l-6.481 2.268l-7.13-1.297l-14.647-20.544l-15.1-23.138l-12.185-20.739l-1.49.843l-7.194 77.448l-3.37 3.953l-7.778 2.981l-6.48-4.925l-3.436-7.972l3.435-15.749l4.148-20.544l3.37-16.333l3.046-20.285l1.815-6.74l-.13-.454l-1.49.194l-15.295 20.999l-23.267 31.433l-18.406 19.702l-4.407 1.75l-7.648-3.954l.713-7.064l4.277-6.286l25.47-32.405l15.36-20.092l9.917-11.6l-.065-1.686h-.583L44.07 198.125l-12.055 1.555l-5.185-4.86l.648-7.972l2.463-2.593l20.35-13.999z"/></svg>Claude</span><span class="tvw-logo"><svg viewBox="0 0 256 171" aria-hidden="true"><defs><linearGradient id="lg15" x1="13.878%" x2="89.144%" y1="55.934%" y2="58.694%"><stop offset="0%" stop-color="#0064e1"/><stop offset="40%" stop-color="#0064e1"/><stop offset="83%" stop-color="#0073ee"/><stop offset="100%" stop-color="#0082fb"/></linearGradient><linearGradient id="lg16" x1="54.315%" x2="54.315%" y1="82.782%" y2="39.307%"><stop offset="0%" stop-color="#0082fb"/><stop offset="100%" stop-color="#0064e0"/></linearGradient></defs><path fill="#0081fb" d="M27.651 112.136c0 9.775 2.146 17.28 4.95 21.82c3.677 5.947 9.16 8.466 14.751 8.466c7.211 0 13.808-1.79 26.52-19.372c10.185-14.092 22.186-33.874 30.26-46.275l13.675-21.01c9.499-14.591 20.493-30.811 33.1-41.806C161.196 4.985 172.298 0 183.47 0c18.758 0 36.625 10.87 50.3 31.257C248.735 53.584 256 81.707 256 110.729c0 17.253-3.4 29.93-9.187 39.946c-5.591 9.686-16.488 19.363-34.818 19.363v-27.616c15.695 0 19.612-14.422 19.612-30.927c0-23.52-5.484-49.623-17.564-68.273c-8.574-13.23-19.684-21.313-31.907-21.313c-13.22 0-23.859 9.97-35.815 27.75c-6.356 9.445-12.882 20.956-20.208 33.944l-8.066 14.289c-16.203 28.728-20.307 35.271-28.408 46.07c-14.2 18.91-26.324 26.076-42.287 26.076c-18.935 0-30.91-8.2-38.325-20.556C2.973 139.413 0 126.202 0 111.148z"/><path fill="url(#lg15)" d="M21.802 33.206C34.48 13.666 52.774 0 73.757 0C85.91 0 97.99 3.597 110.605 13.897c13.798 11.261 28.505 29.805 46.853 60.368l6.58 10.967c15.881 26.459 24.917 40.07 30.205 46.49c6.802 8.243 11.565 10.7 17.752 10.7c15.695 0 19.612-14.422 19.612-30.927l24.393-.766c0 17.253-3.4 29.93-9.187 39.946c-5.591 9.686-16.488 19.363-34.818 19.363c-11.395 0-21.49-2.475-32.654-13.007c-8.582-8.083-18.615-22.443-26.334-35.352l-22.96-38.352C118.528 64.08 107.96 49.73 101.845 43.23c-6.578-6.988-15.036-15.428-28.532-15.428c-10.923 0-20.2 7.666-27.963 19.39z"/><path fill="url(#lg16)" d="M73.312 27.802c-10.923 0-20.2 7.666-27.963 19.39c-10.976 16.568-17.698 41.245-17.698 64.944c0 9.775 2.146 17.28 4.95 21.82L9.027 149.482C2.973 139.413 0 126.202 0 111.148C0 83.772 7.514 55.24 21.802 33.206C34.48 13.666 52.774 0 73.757 0z"/></svg>Meta AI</span><span class="tvw-logo"><svg viewBox="0 0 256 315" aria-hidden="true"><path d="M213.803 167.03c.442 47.58 41.74 63.413 42.197 63.615c-.35 1.116-6.599 22.563-21.757 44.716c-13.104 19.153-26.705 38.235-48.13 38.63c-21.05.388-27.82-12.483-51.888-12.483c-24.061 0-31.582 12.088-51.51 12.871c-20.68.783-36.428-20.71-49.64-39.793c-27-39.033-47.633-110.3-19.928-158.406c13.763-23.89 38.36-39.017 65.056-39.405c20.307-.387 39.475 13.662 51.889 13.662c12.406 0 35.699-16.895 60.186-14.414c10.25.427 39.026 4.14 57.503 31.186c-1.49.923-34.335 20.044-33.978 59.822M174.24 50.199c10.98-13.29 18.369-31.79 16.353-50.199c-15.826.636-34.962 10.546-46.314 23.828c-10.173 11.763-19.082 30.589-16.678 48.633c17.64 1.365 35.66-8.964 46.64-22.262"/></svg>Siri</span></div></section>'''

CTA3_SEC = '''<section class="tvw-cta3 tvs-up"><div class="tvw-cta3-in"><p class="tvw-cta3-k">Your next customer is asking AI</p><h2>Let&#39;s build your AI-ready website.</h2><p class="tvw-cta3-s">Designed, built and hosted for you. Updates included. Half to start, the rest when you love it.</p><div class="tvw-cta-btns"><a class="tvs-btn tvw-btn-w" href="#tvs-book">Send us a message</a><a class="tvs-btn tvw-btn-o" href="#tvs-bundles">See the packages</a></div></div></section>'''

COMM_SEC = '''<section class="tvs-sec tvw-comm"><div class="tvw-comm-grid"><div class="tvw-comm-card tvs-up"><p class="tvw-comm-k">Built by your neighbors</p><h2>Local tech, local team. <span>Launched to the whole town.</span></h2><p>We live and work right here in Three Village. When your new site goes live, we introduce it to the neighbors on Three Village Local.</p><ul><li>Homepage spotlight</li><li>Weekly email feature</li><li>A boost on your listing</li></ul></div><div class="tvs-up"><div class="tvw-dev" role="img" aria-label="An AI-optimized website with a built-in AI assistant, shown on a laptop and a phone"><div class="tvw-lap"><div class="tvw-lap-scr"><div class="tvw-lap-d"><div class="tvw-ms-nav"><b>Your Bakery</b><span>Menu</span><span>Cakes</span><span>Visit</span><i>Order ahead</i></div><div class="tvw-ms-hero"><p class="tvw-ms-k">Main Street &middot; Since 1998</p><p class="tvw-ms-h">Fresh bread,<br>baked every morning.</p><p class="tvw-ms-btns"><i>See the menu</i><u>Get directions</u></p></div><div class="tvw-ms-row"><div><b>Open today</b><span>7 AM - 6 PM</span></div><div><b>&#9733;&#9733;&#9733;&#9733;&#9733; 4.9</b><span>312 reviews</span></div><div><b>Custom cakes</b><span>48 hr notice</span></div></div><div class="tvw-ms-chat"><div class="tvw-ms-ch"><span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="8" width="16" height="12" rx="3"/><path d="M12 8V4M9 14h.01M15 14h.01"/></svg></span><b>Ask Your Bakery</b><em>AI assistant</em></div><div class="tvw-log" id="tvwLogL"><p class="tvw-ms-q">Do you make gluten-free birthday cakes?</p><p class="tvw-ms-a">Yes! Order 48 hours ahead and pick up any day after 9 AM. Want me to start an order?</p></div><p class="tvw-ms-in" id="tvwInL">Type a question...</p></div></div></div><div class="tvw-lap-b"></div></div><div class="tvw-ph"><div class="tvw-ph-d"><span class="tvw-ph-notch"></span><div class="tvw-gpt-h"><svg viewBox="0 0 256 260" aria-hidden="true"><path d="M239.184 106.203a64.72 64.72 0 0 0-5.576-53.103C219.452 28.459 191 15.784 163.213 21.74A65.586 65.586 0 0 0 52.096 45.22a64.72 64.72 0 0 0-43.23 31.36c-14.31 24.602-11.061 55.634 8.033 76.74a64.67 64.67 0 0 0 5.525 53.102c14.174 24.65 42.644 37.324 70.446 31.36a64.72 64.72 0 0 0 48.754 21.744c28.481.025 53.714-18.361 62.414-45.481a64.77 64.77 0 0 0 43.229-31.36c14.137-24.558 10.875-55.423-8.083-76.483m-97.56 136.338a48.4 48.4 0 0 1-31.105-11.255l1.535-.87l51.67-29.825a8.6 8.6 0 0 0 4.247-7.367v-72.85l21.845 12.636c.218.111.37.32.409.563v60.367c-.056 26.818-21.783 48.545-48.601 48.601M37.158 197.93a48.35 48.35 0 0 1-5.781-32.589l1.534.921l51.722 29.826a8.34 8.34 0 0 0 8.441 0l63.181-36.425v25.221a.87.87 0 0 1-.358.665l-52.335 30.184c-23.257 13.398-52.97 5.431-66.404-17.803M23.549 85.38a48.5 48.5 0 0 1 25.58-21.333v61.39a8.29 8.29 0 0 0 4.195 7.316l62.874 36.272l-21.845 12.636a.82.82 0 0 1-.767 0L41.353 151.53c-23.211-13.454-31.171-43.144-17.804-66.405zm179.466 41.695l-63.08-36.63L161.73 77.86a.82.82 0 0 1 .768 0l52.233 30.184a48.6 48.6 0 0 1-7.316 87.635v-61.391a8.54 8.54 0 0 0-4.4-7.213m21.742-32.69l-1.535-.922l-51.619-30.081a8.39 8.39 0 0 0-8.492 0L99.98 99.808V74.587a.72.72 0 0 1 .307-.665l52.233-30.133a48.652 48.652 0 0 1 72.236 50.391zM88.061 139.097l-21.845-12.585a.87.87 0 0 1-.41-.614V65.685a48.652 48.652 0 0 1 79.757-37.346l-1.535.87l-51.67 29.825a8.6 8.6 0 0 0-4.246 7.367zm11.868-25.58L128.067 97.3l28.188 16.218v32.434l-28.086 16.218l-28.188-16.218z"/></svg><b>ChatGPT</b></div><div class="tvw-ph-chat"><div class="tvw-log" id="tvwLogP"><p class="tvw-g-q">Best bakery near Setauket for a gluten-free birthday cake?</p><p class="tvw-g-a">Locals recommend <b>Your Bakery</b> on Main Street in Stony Brook. They make gluten-free custom cakes with 48 hours notice and are rated 4.9 stars.</p><div class="tvw-gcard"><span></span><div><b>Your Bakery</b><em>yourbakery.com</em></div></div><p class="tvw-g-q">Are they open Sunday?</p><p class="tvw-g-a">Yes, <b>Your Bakery</b> is open Sunday from 7 AM to 4 PM.</p></div></div><p class="tvw-ph-in" id="tvwInP">Ask anything</p></div></div><p class="tvw-dev-tag"><span>&#10003;</span>Read and recommended by AI search</p></div></div></div></section>'''

SHIFT_SEC = '''<section class="tvs-sec tvw-shift" id="tvw-shift">
  <div class="tvs-head tvs-up">
    <p class="tvs-eyebrow">Websites aren&#39;t dead. Their job changed.</p>
    <h2>Your website isn&#39;t a digital business card anymore.</h2>
    <p>It still shows off your business, but now it has a bigger job: feeding AI tools the facts they need to recommend you. More and more people ask ChatGPT, Gemini, Copilot, Perplexity and Google&#39;s AI Overviews for answers and recommendations instead of scrolling through search results. If your site can&#39;t teach AI who you are, AI recommends someone else.</p>
  </div>
  <div class="tvw-then-now tvs-up">
    <div class="tvw-then">
      <p class="tvw-tn-lab">Then</p>
      <div class="tvw-bcard"><b>Your Business</b><span>Lawn Care &middot; Setauket</span><i>(631) 555-0100</i></div>
      <p class="tvw-tn-txt">A digital business card. People found it, read it, maybe called.</p>
    </div>
    <div class="tvw-tn-arrow" aria-hidden="true">&#8594;</div>
    <div class="tvw-now">
      <p class="tvw-tn-lab">Now</p>
      <div class="tvw-flow">
        <div class="tvw-fl tvw-fl-site"><em>Your website</em><b>Services, hours, area, reviews, FAQs</b></div>
        <div class="tvw-fl-ar" aria-hidden="true"></div>
        <div class="tvw-fl tvw-fl-ai"><em>AI reads it</em><b>ChatGPT &middot; Gemini &middot; Copilot &middot; Google AI</b></div>
        <div class="tvw-fl-ar" aria-hidden="true"></div>
        <div class="tvw-fl tvw-fl-q"><em>A neighbor asks</em><b>&ldquo;Who&#39;s a good landscaper near me?&rdquo;</b></div>
        <div class="tvw-fl-ar" aria-hidden="true"></div>
        <div class="tvw-fl tvw-fl-win"><em>AI answers</em><b>&ldquo;Try <u>Your Business</u> in Setauket...&rdquo;</b></div>
      </div>
      <p class="tvw-tn-txt">A source AI learns from, so it recommends you by name.</p>
    </div>
  </div>
  <div class="tvw-cta1 tvs-up"><p><b>Ready for a website AI recommends?</b><span>Tell us about your business. We reply by email, usually within a day.</span></p><div class="tvw-cta-btns"><a class="tvs-btn tvs-blue" href="#tvs-book">Send us a message</a><a class="tvs-btn tvs-ghost" href="#tvs-bundles">See the packages</a></div></div>
</section>'''

CHAT_SEC = '''<section class="tvs-sec tvw-bot" id="tvw-bot">
  <div class="tvw-bot-grid">
    <div class="tvw-bot-txt tvs-up">
      <p class="tvs-eyebrow">AI chat assistant</p>
      <h2>Your own AI assistant, working 24/7.</h2>
      <p>We add a friendly AI chat assistant to your site, trained on your services, prices, hours and FAQs. It answers customers instantly, day or night, and hands you the lead.</p>
      <ul class="tvw-bot-list">
        <li><b>Answers questions instantly</b>Hours, pricing, services, service area, anything you teach it</li>
        <li><b>Captures every lead</b>Name, phone and what they need, sent to you right away</li>
        <li><b>Books appointments</b>Sends people to your calendar or a quote request</li>
        <li><b>Never sleeps</b>Nights, weekends and holidays, while you&#39;re on a job</li>
      </ul>
      <p class="tvw-bot-tag"><span>Included in AI-Powered</span><span>Add-on for AI-Ready</span></p>
      <a class="tvs-btn tvs-blue tvw-bot-btn" href="#tvs-book">Add an AI assistant to my site</a>
    </div>
    <div class="tvw-bot-demo tvs-up" aria-hidden="true">
      <div class="tvw-chatw">
        <div class="tvw-chat-h"><span class="tvw-chat-av">&#129302;</span><div><b>Your Business Assistant</b><i>Online now</i></div></div>
        <div class="tvw-chat-b">
          <p class="tvw-m tvw-me tvw-d1">Do you do weekend cleanups in Stony Brook?</p>
          <p class="tvw-m tvw-bt tvw-d2">Yes! We do Saturday cleanups across Stony Brook and Setauket. Most yards take 2 to 3 hours. Want me to set up a free quote?</p>
          <p class="tvw-m tvw-me tvw-d3">Yes please. I&#39;m Dana, 631-555-0142.</p>
          <p class="tvw-m tvw-bt tvw-d4">Thanks Dana! I&#39;ve sent your request to the owner. You&#39;ll hear back today.</p>
        </div>
        <div class="tvw-chat-in"><span>Type your question...</span><b>&#10148;</b></div>
      </div>
      <div class="tvw-lead tvw-d5"><span>&#128241;</span><div><b>New lead from your website</b><i>Dana, 631-555-0142, weekend cleanup quote</i></div></div>
      <p class="tvw-bot-ex">Example conversation</p>
    </div>
  </div>
</section>'''

AI_SEC = '''<section class="tvs-sec tvw-ai" id="tvw-ai">
  <div class="tvs-head tvs-up">
    <p class="tvs-eyebrow">Built for the AI era</p>
    <h2>Websites built to be found, understood and recommended by AI.</h2>
    <p>More people now ask ChatGPT, Gemini, Copilot, Perplexity and Google's AI "who's good near me?" AI tools recommend the businesses they can actually read. Many template site builders load their words with scripts, and AI crawlers generally don't run those scripts, so to them the page can look almost empty. We build sites AI can read from the first line.</p>
  </div>
  <div class="tvw-tech tvs-up"><div class="tvw-tech-in"><div class="tvw-tech-hd"><p>The tech under the hood</p><h3>Enterprise-grade technology.<br><span>Small-business simple.</span></h3></div><div class="tvw-tk-grid"><div class="tvw-tk"><span class="tvw-tk-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="7" rx="2"/><rect x="3" y="13" width="18" height="7" rx="2"/><path d="M7 7.5h.01M7 16.5h.01"/></svg></span><div><b>Server-rendered pages</b><p>Every word lives in the page itself, so AI reads it instantly. No scripts required.</p></div></div><div class="tvw-tk"><span class="tvw-tk-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.6 13.4l-7.2 7.2a2 2 0 0 1-2.8 0L3 13V3h10l7.6 7.6a2 2 0 0 1 0 2.8z"/><circle cx="7.5" cy="7.5" r="1.5"/></svg></span><div><b>Structured data</b><p>Schema.org labels tell AI exactly what you do, where, when and how well you are rated.</p></div></div><div class="tvw-tk"><span class="tvw-tk-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="8" width="16" height="12" rx="3"/><path d="M12 8V4M9 14h.01M15 14h.01"/></svg></span><div><b>Open to AI crawlers</b><p>Welcomes the crawlers behind ChatGPT, Gemini, Copilot, Perplexity and Claude.</p></div></div><div class="tvw-tk"><span class="tvw-tk-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6M8 13h8M8 17h5"/></svg></span><div><b>llms.txt + sitemaps</b><p>A plain-language guide written just for AI tools, plus maps of every page.</p></div></div><div class="tvw-tk"><span class="tvw-tk-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M13 2L3 14h9l-1 8 10-12h-9z"/></svg></span><div><b>Instant indexing</b><p>New pages are announced to search engines the day they go live.</p></div></div><div class="tvw-tk"><span class="tvw-tk-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 14l4-4"/><path d="M3.3 17a9 9 0 1 1 17.4 0"/></svg></span><div><b>Fast on every phone</b><p>Hosted on a global edge network and built to pass Google&#39;s Core Web Vitals.</p></div></div></div></div></div>
</section>'''

src = open(os.path.join(SV, "page.html"), encoding="utf-8").read()
h = src
# hero: websites only, no social/video/drone/marketing services
HERO_VIS = '''<div class="tvw-hvis"><div class="tvw-dev" role="img" aria-label="An AI-optimized website with a built-in AI assistant, shown on a laptop and a phone"><div class="tvw-lap"><div class="tvw-lap-scr"><div class="tvw-lap-d"><div class="tvw-ms-nav"><b>Your Bakery</b><span>Menu</span><span>Cakes</span><span>Visit</span><i>Order ahead</i></div><div class="tvw-ms-hero"><p class="tvw-ms-k">Main Street &middot; Since 1998</p><p class="tvw-ms-h">Fresh bread,<br>baked every morning.</p><p class="tvw-ms-btns"><i>See the menu</i><u>Get directions</u></p></div><div class="tvw-ms-row"><div><b>Open today</b><span>7 AM - 6 PM</span></div><div><b>&#9733;&#9733;&#9733;&#9733;&#9733; 4.9</b><span>312 reviews</span></div><div><b>Custom cakes</b><span>48 hr notice</span></div></div><div class="tvw-ms-chat"><div class="tvw-ms-ch"><span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="8" width="16" height="12" rx="3"/><path d="M12 8V4M9 14h.01M15 14h.01"/></svg></span><b>Ask Your Bakery</b><em>AI assistant</em></div><div class="tvw-log" id="tvwLogL"><p class="tvw-ms-q">Do you make gluten-free birthday cakes?</p><p class="tvw-ms-a">Yes! Order 48 hours ahead and pick up any day after 9 AM. Want me to start an order?</p></div><p class="tvw-ms-in" id="tvwInL">Type a question...</p></div></div></div><div class="tvw-lap-b"></div></div><div class="tvw-ph"><div class="tvw-ph-d"><span class="tvw-ph-notch"></span><div class="tvw-gpt-h"><svg viewBox="0 0 256 260" aria-hidden="true"><path d="M239.184 106.203a64.72 64.72 0 0 0-5.576-53.103C219.452 28.459 191 15.784 163.213 21.74A65.586 65.586 0 0 0 52.096 45.22a64.72 64.72 0 0 0-43.23 31.36c-14.31 24.602-11.061 55.634 8.033 76.74a64.67 64.67 0 0 0 5.525 53.102c14.174 24.65 42.644 37.324 70.446 31.36a64.72 64.72 0 0 0 48.754 21.744c28.481.025 53.714-18.361 62.414-45.481a64.77 64.77 0 0 0 43.229-31.36c14.137-24.558 10.875-55.423-8.083-76.483m-97.56 136.338a48.4 48.4 0 0 1-31.105-11.255l1.535-.87l51.67-29.825a8.6 8.6 0 0 0 4.247-7.367v-72.85l21.845 12.636c.218.111.37.32.409.563v60.367c-.056 26.818-21.783 48.545-48.601 48.601M37.158 197.93a48.35 48.35 0 0 1-5.781-32.589l1.534.921l51.722 29.826a8.34 8.34 0 0 0 8.441 0l63.181-36.425v25.221a.87.87 0 0 1-.358.665l-52.335 30.184c-23.257 13.398-52.97 5.431-66.404-17.803M23.549 85.38a48.5 48.5 0 0 1 25.58-21.333v61.39a8.29 8.29 0 0 0 4.195 7.316l62.874 36.272l-21.845 12.636a.82.82 0 0 1-.767 0L41.353 151.53c-23.211-13.454-31.171-43.144-17.804-66.405zm179.466 41.695l-63.08-36.63L161.73 77.86a.82.82 0 0 1 .768 0l52.233 30.184a48.6 48.6 0 0 1-7.316 87.635v-61.391a8.54 8.54 0 0 0-4.4-7.213m21.742-32.69l-1.535-.922l-51.619-30.081a8.39 8.39 0 0 0-8.492 0L99.98 99.808V74.587a.72.72 0 0 1 .307-.665l52.233-30.133a48.652 48.652 0 0 1 72.236 50.391zM88.061 139.097l-21.845-12.585a.87.87 0 0 1-.41-.614V65.685a48.652 48.652 0 0 1 79.757-37.346l-1.535.87l-51.67 29.825a8.6 8.6 0 0 0-4.246 7.367zm11.868-25.58L128.067 97.3l28.188 16.218v32.434l-28.086 16.218l-28.188-16.218z"/></svg><b>ChatGPT</b></div><div class="tvw-ph-chat"><div class="tvw-log" id="tvwLogP"><p class="tvw-g-q">Best bakery near Setauket for a gluten-free birthday cake?</p><p class="tvw-g-a">Locals recommend <b>Your Bakery</b> on Main Street in Stony Brook. They make gluten-free custom cakes with 48 hours notice and are rated 4.9 stars.</p><div class="tvw-gcard"><span></span><div><b>Your Bakery</b><em>yourbakery.com</em></div></div></div></div><p class="tvw-ph-in" id="tvwInP">Ask anything</p></div></div><p class="tvw-dev-tag"><span>&#10003;</span>Read and recommended by AI search</p></div></div>'''   # owner 10/22: laptop + phone live-chat mockup moved up from the old community section
h = rep(h, '''<div class="tvs-hphoto" role="img" aria-label="Local shop owner smiling in the doorway of his store"></div>
  <div class="tvs-hfade"></div>''', HERO_VIS)   # owner 10/22: AI-answer visual instead of the shop-owner photo
h = re.sub(r'\n  <div class="tvs-float tvs-f1[^\n]*\n[^\n]*\n  </div>', '', h, count=1)
h = re.sub(r'\n  <div class="tvs-float tvs-f2[^\n]*\n[^\n]*\n  </div>', '', h, count=1)
h = rep(h, '<h1>We build it.<br><span>Then we tell the whole town.</span></h1>', '<h1>Your new website,<br><span>built for AI search.</span></h1>')   # owner 10/22: own headline (the build/tell line stays on /services)
h = rep(h, "Websites + Google + AI search + Social + Video + Drone + Marketing", "Websites + Google + AI search + Hosting")
h = rep(h, "Your website, Google, AI search, social media, video and marketing, built by one local team to work as one. Then we launch it in front of the whole town on Three Village Local.",
        "Websites that do more than show off your business: they feed AI tools like ChatGPT, Gemini and Copilot the facts they need to recommend you. Designed, built and hosted by one local team, then launched to the whole town on Three Village Local.")
h = rep(h, 'href="#tvs-bundles">See the bundles</a>', 'href="#tvs-bundles">See the packages</a>')
# owner 10/22: encourage email/messaging over calls (a call only if needed)
h = rep(h, '<a class="tvs-btn tvs-ghost" href="#tvs-book">Book a free call</a>', '<a class="tvs-btn tvs-ghost" href="#tvs-book">Send us a message</a>')
h = rep(h, '<a class="tvs-sticky" href="#tvs-book">Book a free call</a>', '<a class="tvs-sticky" href="#tvs-book">Send us a message</a>')
h = rep(h, '<h3>Free call</h3><p>Tell us about your business. 15 minutes, no pressure.</p>', '<h3>Send a message</h3><p>Tell us about your business by email or the form below. No pressure.</p>')
h = rep(h, '<h2>Book your free 15-minute call.</h2>', '<h2>Tell us about your business.</h2>')
h = rep(h, '<p>Tell us a little about your business. We will reach out within one business day.</p>', '<p>Send us a quick message and we will reply by email, usually within one business day. Everything can happen by email or text. If you would rather talk it through, we are happy to set up a call.</p>')
h = rep(h, '<li><b>No</b>long contracts</li>', '<li><b>Updates</b>included</li>')
h = rep(h, '<details><summary>Do I own my website and domain?</summary>', '<details open><summary>Are updates and changes included?</summary><p>Yes. Your monthly plan covers the everyday changes: new photos, prices, menus, hours, services, specials and seasonal updates. Just email or text us what you need and we take care of it. No tickets, no extra bills for the small stuff.</p></details>\n    <details><summary>Do I own my website and domain?</summary>')
h = re.sub(r'\n    <a class="tvs-newlink"[^\n]*</a>', "", h)
h = cut(h, "tvs-sec tvs-social")                  # "Your content, seen all over town" (social media service)
h = swap(h, "tvs-sec tvs-work", WORK)              # promo video + social posts -> real websites + phone
h = swap(h, "tvs-sec tvs-bundles", BUNDLES)        # social bundles -> the 2 website packages
h = cut(h, "tvs-founding")                        # owner 10/22: remove the founding clients box
i, _ = sec(h, "tvs-sec tvs-bundles")
h = h[:i] + CHAT_SEC + chr(10) * 2 + h[i:]      # owner 10/22: highlight the AI chatbot, visual
i, _ = sec(h, "tvs-sec tvs-vs")
h = h[:i] + ADDS_SEC + chr(10) * 2 + h[i:]      # owner 10/22: extra website tech services
h = cut(h, "tvs-stats")                           # owner 10/22: remove the 4-number stats strip
i, _ = sec(h, "tvs-sec tvs-show")
h = h[:i] + STRIP_SEC + chr(10) * 2 + SHIFT_SEC + chr(10) * 2 + AI_SEC + chr(10) * 2 + h[i:]   # owner 10/22: websites changed job (then/now), then the AI section                  # owner 10/22: AI-findable message + template-site scripts + our tech
h = re.sub(r'<a class="tvs-newbiz[^\n]*</a>\n\n', "", h)
h = rep(h, "<p>We pick the right bundle together and map out your first month.</p>", "<p>We pick the right package together and map out your site.</p>")
h = rep(h, "<p>No long contracts. Bundles are a one-time build, and monthly plans are month to month.</p>",
        "<p>No long contracts. Your site is a one-time build, and the monthly plan is month to month.</p>")
h = rep(h, "<p>Half to start, the rest at launch once you love it.</p>", "<p>Half of your start-up fee to begin, and the rest only when you love your new site. Your start-up fee includes your first month.</p>")
h = rep(h, "<p>No. Anyone can book. Members save on every bundle, and VIP members save the most.</p>", "<p>No. Anyone can book. Three Village Local members get member pricing on both packages.</p>")
h = rep(h, "mailto:hello@threevillagelocal.com?subject=Services", "mailto:hello@threevillagelocal.com?subject=Websites")
i, _ = sec(h, "tvs-sec tvs-steps")
h = h[:i] + CTA3_SEC + chr(10) * 2 + h[i:]      # owner 10/22: more calls to action
h = cut(h, "tvs-sec tvw-adds")                    # owner 10/22: removed "More we can build for you" add-ons
h = cut(h, "tvs-sec tvs-show")                    # owner 10/22: page too long, removed "Anyone can build a website" launch section
h = cut(h, "tvs-sec tvs-work")                    # owner 10/22: removed "See what you get" (phone + site examples)
for m in re.finditer(r".{60}[Bb]undle.{40}", h): print("LEFT:", m.group(0))
HTML = h

PRICES = ("var P={webready:{all:[%d,%d],free:[%d,%d],featured:[%d,%d],vip:[%d,%d]},webpowered:{all:[%d,%d],free:[%d,%d],featured:[%d,%d],vip:[%d,%d]},"
                    % (PR["web-ready-regular"] + PR["web-ready-member"] * 3 + PR["web-powered-regular"] + PR["web-powered-member"] * 3))
LIVECHAT_JS = '''<script>(function(){if(!('IntersectionObserver' in window)||(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches))return;
var P={l:"tvwLogP",n:"tvwInP",ph:"Ask anything",q:"tvw-g-q",a:"tvw-g-a",c:[["Can I order online?","Yes. You can order on yourbakery.com, and their website assistant can start the order for you."],["Best bakery near Setauket for a gluten-free birthday cake?","Locals recommend Your Bakery on Main Street in Stony Brook. They make gluten-free custom cakes with 48 hours notice and are rated 4.9 stars.",1],["Are they open Sunday?","Yes, Your Bakery is open Sunday from 7 AM to 4 PM."]]};
var L={l:"tvwLogL",n:"tvwInL",ph:"Type a question...",q:"tvw-ms-q",a:"tvw-ms-a",c:[["Yes, for Saturday please.","You got it! What name should I put it under? We will text you when it is ready."],["Can you make it nut-free too?","Absolutely. Just add a note to your order and we will take care of it."],["Do you make gluten-free birthday cakes?","Yes! Order 48 hours ahead and pick up any day after 9 AM. Want me to start an order?"]]};
var vis=false,go=false;function sl(m){return new Promise(function(r){setTimeout(r,m)})}
async function on(){while(!vis)await sl(400)}
function bub(l,c,t){var p=document.createElement('p');p.className=c+' tvw-pop';p.textContent=t;l.appendChild(p);while(l.children.length>8)l.removeChild(l.firstChild);return p}
async function talk(b){var l=document.getElementById(b.l),n=document.getElementById(b.n);if(!l||!n)return;
for(var k=0;k<b.c.length;k++){var q=b.c[k][0],a=b.c[k][1],i,w,d;await on();
n.classList.add('on');for(i=1;i<=q.length;i++){n.textContent=q.slice(Math.max(0,i-30),i);await sl(40)}await sl(350);n.textContent=b.ph;n.classList.remove('on');
bub(l,b.q,q);await sl(450);d=bub(l,b.a+' tvw-dots','');d.innerHTML='<i></i><i></i><i></i>';await sl(1300);
d.className=b.a;d.textContent='';w=a.split(' ');for(i=0;i<w.length;i++){d.textContent+=(i?' ':'')+w[i];await sl(70)}
d.innerHTML=d.textContent.replace('Your Bakery','<b>Your Bakery</b>');
if(b.c[k][2]){await sl(300);var cd=document.createElement('div');cd.className='tvw-gcard tvw-pop';cd.innerHTML='<span></span><div><b>Your Bakery</b><em>yourbakery.com</em></div>';l.appendChild(cd)}
await sl(1400)}}
async function loop(){await sl(500);for(;;){await on();await talk(P);await sl(600);await talk(L);await sl(2500)}}
var el=document.querySelector('.tvw-dev');if(!el)return;new IntersectionObserver(function(e){vis=e[0].isIntersecting;if(vis&&!go){go=true;loop()}},{threshold:.3}).observe(el)})();</script>'''
GOJS = '''<script>(function(){var nb=0,ib=setInterval(function(){[].forEach.call(document.querySelectorAll('input[type="submit"][id^="services_inquiry"],#tvs-form-slot input[type="submit"]'),function(x){if(x.value!=='Send my message'){x.value='Send my message';x.setAttribute('value','Send my message')}});var t=document.querySelector('#tvs-form-slot textarea[name="comments"]');if(t)t.placeholder='Your current website (if any), what you want more of, anything we should know';if(++nb>120)clearInterval(ib)},250);var n0=0,iv=setInterval(function(){var s=document.querySelector('#tvs-form-slot select[name="bundle"]');if(s){s.value='web_consult';var g=s.closest('.form-group')||s.parentNode;g.style.display='none';clearInterval(iv)}if(++n0>40)clearInterval(iv)},250);function upd(){var b=document.querySelector('#tvs .tvs-tiers button.on'),m=!b||b.getAttribute('data-t')!=='all';
[].forEach.call(document.querySelectorAll('#tvs .tvw-go'),function(a){a.href=m?a.getAttribute('data-m'):a.getAttribute('data-r')})}
document.addEventListener('click',function(e){if(e.target.closest&&e.target.closest('#tvs .tvs-tiers button'))setTimeout(upd,0)});upd()})();</script>'''

CSS = '''
.tvw-comm-grid{display:grid;grid-template-columns:.85fr 1.15fr;gap:40px;align-items:center;max-width:1060px;margin:0 auto}
.tvw-comm-k{margin:0 0 8px!important;font-size:12.5px;font-weight:800;letter-spacing:.16em;text-transform:uppercase;color:var(--blue)}
.tvw-comm-card h2{margin:0 0 12px!important;font-size:36px;line-height:1.1}
.tvw-comm-card h2 span{display:block;color:var(--blue)}
.tvw-comm-card>p{margin:0 0 16px!important;font-size:16.5px;line-height:1.6;color:var(--mut)}
.tvw-comm-card ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:8px}
.tvw-comm-card li{font-size:13px;font-weight:800;padding:7px 13px;border-radius:999px;background:#eef4ff;color:var(--navy)}
.tvw-dev{position:relative;container-type:inline-size;padding:1cqw 0 5cqw}
.tvw-dev *{box-sizing:border-box}
.tvw-dev p{margin:0!important}
.tvw-lap{width:86cqw;filter:drop-shadow(0 4cqw 5cqw rgba(9,30,66,.28))}
.tvw-lap-scr{padding:1.5cqw 1.5cqw 2cqw;border-radius:2.4cqw 2.4cqw 0 0;background:linear-gradient(160deg,#1c2433,#0b111c)}
.tvw-lap-d{position:relative;aspect-ratio:16/10;overflow:hidden;border-radius:.5cqw;background:#fffaf4;font-family:inherit}
.tvw-lap-b{position:relative;width:108%;margin-left:-4%;height:2.2cqw;border-radius:0 0 2.6cqw 2.6cqw;background:linear-gradient(180deg,#eef1f5,#c3c9d3 60%,#9aa2ae)}
.tvw-lap-b:before{content:"";position:absolute;left:50%;top:0;width:14%;height:.9cqw;transform:translateX(-50%);border-radius:0 0 1cqw 1cqw;background:#aab1bc}
.tvw-ms-nav{display:flex;align-items:center;gap:2.4cqw;height:5.4cqw;padding:0 2.4cqw;background:#fff;border-bottom:1px solid #f0e6da;font-size:1.35cqw;color:#5b4636}
.tvw-ms-nav b{margin-right:auto;font-family:Georgia,serif;font-size:2cqw;color:#3a2416}
.tvw-ms-nav i{font-style:normal;font-weight:700;padding:.7cqw 1.4cqw;border-radius:9cqw;background:#c2410c;color:#fff}
.tvw-ms-hero{height:25cqw;padding:4.2cqw 3cqw;background:linear-gradient(90deg,rgba(28,14,6,.82),rgba(28,14,6,.35) 55%,rgba(28,14,6,0)),url(https://threevillagelocal-cloud.github.io/3vl-share/site/websites/hero-bakery.webp) center/cover;color:#fff}
.tvw-ms-k{font-size:1.25cqw;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#fcd9a8}
.tvw-ms-h{margin:1cqw 0 1.8cqw!important;font-family:Georgia,serif;font-size:3.7cqw;line-height:1.08;font-weight:700}
.tvw-ms-btns{display:flex;gap:1cqw;font-size:1.3cqw;font-weight:700}
.tvw-ms-btns i,.tvw-ms-btns u{font-style:normal;text-decoration:none;padding:.9cqw 1.7cqw;border-radius:9cqw}
.tvw-ms-btns i{background:#c2410c}.tvw-ms-btns u{border:1px solid rgba(255,255,255,.7)}
.tvw-ms-row{display:flex;gap:1.2cqw;padding:2cqw 2.4cqw;width:46%}
.tvw-ms-row div{flex:1;padding:1.2cqw;border-radius:1cqw;background:#fff;box-shadow:0 .4cqw 1.4cqw rgba(60,30,10,.1)}
.tvw-ms-row b{display:block;font-size:1.3cqw;color:#3a2416}.tvw-ms-row span{font-size:1.15cqw;color:#8a7262}
.tvw-ms-chat{position:absolute;right:11cqw;bottom:1.6cqw;width:27cqw;border-radius:1.6cqw;background:#fff;overflow:hidden;box-shadow:0 2cqw 4cqw -1cqw rgba(13,35,70,.45);border:1px solid #e3e9f2}
.tvw-ms-ch{display:flex;align-items:center;gap:.9cqw;padding:1.2cqw 1.4cqw;background:linear-gradient(120deg,#1d5fd1,#4f8df5);color:#fff}
.tvw-ms-ch span,.tvw-ph-lbl span{display:flex;align-items:center;justify-content:center;width:2.8cqw;height:2.8cqw;border-radius:50%;background:rgba(255,255,255,.22)}
.tvw-ms-ch svg,.tvw-ph-lbl svg{width:60%;height:60%}
.tvw-ms-ch b{font-size:1.45cqw}
.tvw-ms-ch em{margin-left:auto;font-style:normal;font-size:1.05cqw;padding:.3cqw .9cqw;border-radius:9cqw;background:rgba(255,255,255,.2)}
.tvw-ms-chat .tvw-ms-q,.tvw-ms-chat .tvw-ms-a{margin:1.1cqw 1.3cqw 0!important}
.tvw-ms-q,.tvw-ms-a{width:fit-content;max-width:86%;padding:.9cqw 1.3cqw;font-size:1.3cqw;line-height:1.35}
.tvw-ms-q{margin-left:auto!important;border-radius:1.6cqw 1.6cqw .4cqw 1.6cqw;background:#1d5fd1;color:#fff}
.tvw-ms-chat .tvw-ms-q{margin-left:auto!important}
.tvw-ms-a{border-radius:1.6cqw 1.6cqw 1.6cqw .4cqw;background:#eef3fb;color:#1a2233}
.tvw-ms-in{margin:1.2cqw 1.3cqw 1.3cqw!important;padding:.9cqw 1.3cqw;border-radius:9cqw;border:1px solid #dbe3ef;font-size:1.2cqw;color:#97a3b6}
.tvw-ph{position:absolute;right:0;bottom:2cqw;width:24cqw;padding:.9cqw;border-radius:4.2cqw;background:linear-gradient(160deg,#2a3242,#0b111c);box-shadow:0 4cqw 6cqw -2cqw rgba(9,30,66,.55)}
.tvw-ph-d{position:relative;aspect-ratio:9/19;overflow:hidden;border-radius:3.4cqw;background:#fff;display:flex;flex-direction:column}
.tvw-ph-notch{position:absolute;left:50%;top:1cqw;width:7cqw;height:1.9cqw;transform:translateX(-50%);border-radius:9cqw;background:#0b111c;z-index:2}
.tvw-ph-chat{flex:1;min-height:0;overflow:hidden;display:flex;flex-direction:column;padding:1.6cqw 1.8cqw 1cqw;background:#fff}
.tvw-log{display:flex;flex-direction:column;justify-content:flex-end;overflow:hidden}
.tvw-ms-chat .tvw-log{height:16cqw}.tvw-ph-chat .tvw-log{flex:1;min-height:0}
.tvw-ms-in,.tvw-ph-in{white-space:nowrap;overflow:hidden}.tvw-ms-in.on,.tvw-ph-in.on{color:#1a2233;border-color:#1d5fd1}
.tvw-pop{animation:tvwPop .35s ease both}
.tvw-dots i{display:inline-block;width:.75cqw;height:.75cqw;margin:0 .18cqw;border-radius:50%;background:#9fb0c8;animation:tvwDot 1s ease-in-out infinite}
.tvw-dots i:nth-child(2){animation-delay:.15s}.tvw-dots i:nth-child(3){animation-delay:.3s}
.tvw-gpt-h{display:flex;align-items:center;justify-content:center;gap:.7cqw;padding:4.4cqw 0 1.3cqw;font-size:1.5cqw;color:#111;border-bottom:1px solid #f0f0f0}
.tvw-gpt-h svg{width:2cqw;height:2cqw}
.tvw-ph-chat .tvw-g-q{margin:0 0 1.3cqw auto!important;width:fit-content;max-width:86%;padding:.9cqw 1.3cqw;border-radius:1.8cqw;background:#f1f1f1;color:#111;font-size:1.3cqw;line-height:1.35}
.tvw-ph-chat .tvw-g-a{margin:0 0 1.2cqw!important;font-size:1.3cqw;line-height:1.45;color:#111}
.tvw-g-a b{background:#fff3c4;padding:0 .3cqw;border-radius:.4cqw}
.tvw-gcard{flex:none;display:flex;gap:1cqw;align-items:center;padding:.9cqw;border:1px solid #e5e5e5;border-radius:1.4cqw;margin-bottom:.6cqw}
.tvw-gcard span{flex:none;width:4.4cqw;height:4.4cqw;border-radius:.8cqw;background:#d9894a url(https://threevillagelocal-cloud.github.io/3vl-share/site/websites/hero-bakery.webp) center/cover}
.tvw-gcard b{display:block;font-size:1.3cqw;color:#111}.tvw-gcard em{display:block;font-style:normal;font-size:1.15cqw;color:#1d5fd1}
.tvw-ph-lbl{display:flex;align-items:center;gap:.8cqw;font-size:1.25cqw;font-weight:800;color:#1d5fd1;margin-bottom:1.2cqw!important}
.tvw-ph-lbl span{background:#e6eefc}
.tvw-ph-chat .tvw-ms-q,.tvw-ph-chat .tvw-ms-a{font-size:1.3cqw;max-width:92%;margin-bottom:1cqw!important}
.tvw-ph-in{margin:0 1.4cqw 1.8cqw!important;padding:.9cqw 1.3cqw;border-radius:9cqw;border:1px solid #dbe3ef;font-size:1.2cqw;color:#97a3b6}
.tvw-dev-tag{position:absolute;left:4cqw;bottom:0;display:flex;align-items:center;gap:8px;padding:9px 16px 9px 10px;border-radius:999px;background:#fff;box-shadow:0 14px 30px -14px rgba(9,30,66,.5);font-size:max(12px,2.1cqw);font-weight:800;color:#0d2147}
.tvw-dev-tag span{display:flex;align-items:center;justify-content:center;width:24px;height:24px;border-radius:50%;background:#16a34a;color:#fff;font-size:13px}
@media (max-width:860px){.tvw-comm-grid{grid-template-columns:1fr;gap:22px}.tvw-comm-card h2{font-size:28px}.tvw-dev{padding-bottom:9cqw}.tvw-lap{width:84cqw}.tvw-ph{width:30cqw;bottom:6cqw}.tvw-ms-chat{right:14cqw;width:26cqw}.tvw-ms-row{width:40%}.tvw-ms-row div:nth-child(3),.tvw-ms-ch em{display:none}.tvw-dev-tag{left:0}}

.tvw-hvis{position:absolute;top:0;right:0;bottom:0;width:50%;z-index:-1;display:flex;align-items:center;justify-content:center;padding:40px 46px 40px 20px;background:radial-gradient(520px 340px at 70% 30%,rgba(77,163,255,.20),transparent 70%),radial-gradient(420px 300px at 30% 90%,rgba(45,240,200,.14),transparent 70%),linear-gradient(160deg,#f3f8ff,#e9f2ff)}
.tvw-hvis:before{content:"";position:absolute;inset:0;background-image:linear-gradient(rgba(29,95,209,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(29,95,209,.06) 1px,transparent 1px);background-size:34px 34px;-webkit-mask-image:radial-gradient(closest-side,#000,transparent);mask-image:radial-gradient(closest-side,#000,transparent)}
.tvw-hai{position:relative;width:100%;max-width:440px;border-radius:22px;background:#fff;border:1px solid #dbe5f3;box-shadow:0 40px 70px -34px rgba(13,35,70,.55);overflow:hidden}
.tvw-hai-h{display:flex;align-items:center;gap:10px;padding:14px 18px;border-bottom:1px solid #eef2f8}
.tvw-hai-lg{display:flex;width:30px;height:30px;border-radius:9px;background:#f2f4f7;align-items:center;justify-content:center}.tvw-hai-lg svg{width:18px;height:18px}
.tvw-hai-h b{font-size:15px;color:var(--navy)}.tvw-hai-h i{margin-left:auto;font-style:normal;font-size:12px;color:var(--mut)}
.tvw-hai-b{padding:18px 18px 20px;background:#fbfcfe}
.tvw-hq{margin:0 0 14px auto!important;max-width:80%;width:fit-content;padding:11px 15px;border-radius:18px 18px 5px 18px;background:#1d5fd1;color:#fff;font-size:15px;line-height:1.4}
.tvw-ha{position:relative}
.tvw-htxt{margin:0 0 12px!important;font-size:15px;line-height:1.55;color:#1a2233}
.tvw-htxt b{background:#fff3c4;padding:0 4px;border-radius:5px}
.tvw-hsite{display:flex;gap:12px;align-items:center;padding:10px;border-radius:14px;border:1px solid #e3e9f2;background:#fff}
.tvw-hsite-img{flex:none;width:58px;height:58px;border-radius:10px;background:#d9894a url(https://threevillagelocal-cloud.github.io/3vl-share/site/websites/hero-bakery.webp) center/cover;box-shadow:inset 0 0 0 1px rgba(0,0,0,.05)}
.tvw-hsite b{display:block;font-size:15px;color:var(--navy)}.tvw-hsite em{display:block;font-style:normal;font-size:13px;color:#1d5fd1}.tvw-hsite span{display:block;font-size:12.5px;color:#b07d00;margin-top:2px}
.tvw-hdots{display:none;margin:0!important}
.tvw-hf{right:34px!important;bottom:40px!important}
.tvs-ready .tvw-h1{opacity:0;animation:tvwPop .5s ease .4s forwards}
.tvs-ready .tvw-h2 .tvw-hdots{display:flex;gap:5px;position:absolute;top:6px;left:2px;animation:tvwOut .2s linear 2s forwards}
.tvw-hdots i{width:7px;height:7px;border-radius:50%;background:#9fb0c8;animation:tvwDot 1s ease-in-out infinite}.tvw-hdots i:nth-child(2){animation-delay:.15s}.tvw-hdots i:nth-child(3){animation-delay:.3s}
.tvs-ready .tvw-h2 .tvw-htxt,.tvs-ready .tvw-h2 .tvw-hsite{opacity:0;animation:tvwPop .5s ease forwards}
.tvs-ready .tvw-h2 .tvw-htxt{animation-delay:2.1s}.tvs-ready .tvw-h2 .tvw-hsite{animation-delay:2.8s}
.tvs-ready .tvw-hf{opacity:0;animation:tvwPop .5s ease 3.6s forwards,tvsBob 6s ease-in-out 4.1s infinite}
@keyframes tvwOut{to{opacity:0;visibility:hidden}}
@keyframes tvwDot{0%,100%{opacity:.35;transform:translateY(0)}50%{opacity:1;transform:translateY(-3px)}}
@media (prefers-reduced-motion:reduce){.tvs-ready .tvw-h1,.tvs-ready .tvw-h2 .tvw-htxt,.tvs-ready .tvw-h2 .tvw-hsite,.tvs-ready .tvw-hf{opacity:1;animation:none}.tvs-ready .tvw-h2 .tvw-hdots{display:none}}
.tvw-hvis .tvw-dev{width:100%;max-width:640px}
@media (max-width:900px){.tvw-hvis{position:relative;width:auto;padding:26px 18px 30px;border-radius:22px 22px 0 0}.tvw-hf{display:none!important}}

.tvw-cta1{display:flex;align-items:center;justify-content:space-between;gap:22px;max-width:1040px;margin:34px auto 0;padding:22px 26px;border-radius:20px;background:#fff;border:1px solid #dbe5f3;box-shadow:0 18px 40px -26px rgba(13,35,70,.45)}
.tvw-cta1 p{margin:0!important}.tvw-cta1 b{display:block;font-size:20px;color:var(--navy);margin-bottom:3px}.tvw-cta1 span{font-size:15px;color:var(--mut)}
.tvw-cta-btns{display:flex;gap:10px;flex-wrap:wrap;flex:none}
.tvw-bot-btn{margin-top:20px}
.tvw-cta3{padding:20px 16px 10px}
.tvw-cta3-in{position:relative;overflow:hidden;max-width:1040px;margin:0 auto;text-align:center;border-radius:28px;padding:48px 28px;background:radial-gradient(600px 260px at 15% 0%,rgba(77,163,255,.35),transparent 70%),radial-gradient(500px 260px at 100% 100%,rgba(45,240,200,.18),transparent 70%),linear-gradient(150deg,#0d2147,#1d4fb0);box-shadow:0 40px 80px -40px rgba(9,30,66,.6)}
.tvw-cta3-k{margin:0 0 10px!important;font-size:12.5px;font-weight:800;letter-spacing:.18em;text-transform:uppercase;color:#9fdcff}
.tvw-cta3 h2{margin:0 0 10px!important;color:#fff!important;font-size:38px;line-height:1.12}
.tvw-cta3-s{margin:0 auto 22px!important;color:#c9d8f2!important;font-size:16.5px;max-width:560px}
.tvw-cta3 .tvw-cta-btns{justify-content:center}
.tvw-btn-w{background:#fff!important;color:#0d2147!important}.tvw-btn-o{background:transparent!important;color:#fff!important;border:1.5px solid rgba(255,255,255,.55)!important}
@media (min-width:761px){.tvs-sticky{display:block!important;position:fixed;right:26px;bottom:26px;z-index:999;background:var(--blue);color:#fff!important;font-weight:800;font-size:15px;border-radius:999px;padding:14px 24px;text-decoration:none!important;box-shadow:0 14px 30px rgba(19,41,75,.35);transform:translateY(160%);transition:transform .3s}.tvs-sticky.on{transform:none}}
@media (max-width:760px){.tvw-cta1{flex-direction:column;align-items:flex-start;padding:20px}.tvw-cta3 h2{font-size:28px}.tvw-cta3-in{padding:36px 20px;border-radius:22px}}

.tvw-tech{max-width:1060px;margin:40px auto 0}
.tvw-tech-in{position:relative;overflow:hidden;border-radius:28px;padding:44px 46px 38px;background:radial-gradient(600px 300px at 85% 0%,rgba(77,163,255,.22),transparent 70%),radial-gradient(500px 280px at 0% 100%,rgba(45,240,200,.12),transparent 70%),linear-gradient(160deg,#0b1730,#0d2147 60%,#0a1630);box-shadow:0 40px 80px -40px rgba(9,30,66,.6)}
.tvw-tech-in:before{content:"";position:absolute;inset:0;background-image:linear-gradient(rgba(140,180,255,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(140,180,255,.06) 1px,transparent 1px);background-size:36px 36px;-webkit-mask-image:linear-gradient(180deg,#000,transparent 85%);mask-image:linear-gradient(180deg,#000,transparent 85%);pointer-events:none}
.tvw-tech-hd{position:relative;text-align:center;margin-bottom:30px}
.tvw-tech-hd p{margin:0 0 10px!important;font-size:12.5px;font-weight:800;letter-spacing:.18em;text-transform:uppercase;color:#7fd4ff}
.tvw-tech-hd h3{margin:0!important;font-size:32px;line-height:1.15;font-weight:800;color:#fff}
.tvw-tech-hd h3 span{background:linear-gradient(90deg,#7fb8ff,#5ee7cf);-webkit-background-clip:text;background-clip:text;color:transparent}
.tvw-tk-grid{position:relative;display:grid;grid-template-columns:repeat(3,1fr);border-top:1px solid rgba(255,255,255,.08)}
.tvw-tk{display:flex;gap:14px;align-items:flex-start;padding:24px 20px 22px;border-bottom:1px solid rgba(255,255,255,.08)}
.tvw-tk:not(:nth-child(3n)){border-right:1px solid rgba(255,255,255,.08)}
.tvw-tk:nth-child(n+4){border-bottom:0}
.tvw-tk-ic{flex:none;display:flex;align-items:center;justify-content:center;width:44px;height:44px;border-radius:13px;color:#8fd0ff;background:linear-gradient(145deg,rgba(77,163,255,.22),rgba(45,240,200,.10));box-shadow:inset 0 0 0 1px rgba(143,208,255,.28),0 0 22px rgba(77,163,255,.18)}
.tvw-tk-ic svg{width:22px;height:22px}
.tvw-tk b{display:block;color:#fff;font-size:16px;margin:2px 0 5px}
.tvw-tk p{margin:0!important;color:#a9bad6;font-size:14px;line-height:1.5}
.tvs-ready .tvw-tech .tvw-tk{opacity:0;transform:translateY(10px)}
.tvs-ready .tvw-tech.tvs-in .tvw-tk{animation:tvwLit .5s ease forwards}
.tvw-tech.tvs-in .tvw-tk:nth-child(2){animation-delay:.1s}.tvw-tech.tvs-in .tvw-tk:nth-child(3){animation-delay:.2s}.tvw-tech.tvs-in .tvw-tk:nth-child(4){animation-delay:.3s}.tvw-tech.tvs-in .tvw-tk:nth-child(5){animation-delay:.4s}.tvw-tech.tvs-in .tvw-tk:nth-child(6){animation-delay:.5s}
@media (prefers-reduced-motion:reduce){.tvs-ready .tvw-tech .tvw-tk{opacity:1!important;transform:none!important;animation:none!important}}
@media (max-width:900px){.tvw-tech-in{padding:32px 20px 24px;border-radius:22px}.tvw-tech-hd h3{font-size:25px}.tvw-tk-grid{grid-template-columns:1fr}.tvw-tk{border-right:0!important;border-bottom:1px solid rgba(255,255,255,.08)!important;padding:18px 4px}.tvw-tk:last-child{border-bottom:0!important}}

.tvw-strip{text-align:center;padding-top:26px!important;padding-bottom:4px!important}
.tvw-strip>p{margin:0 0 14px!important;font-size:13px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--mut)}
.tvw-logo svg{width:20px;height:20px}

/* owner 10/22: three light CSS-only animations; they start when the section is revealed (.tvs-in) and run once */
.tvs-ready .tvw-then-now .tvw-fl,.tvs-ready .tvw-then-now .tvw-fl-ar{opacity:.28;transition:none}
.tvs-ready .tvw-then-now.tvs-in .tvw-fl,.tvs-ready .tvw-then-now.tvs-in .tvw-fl-ar{animation:tvwLit .55s ease forwards}
.tvw-then-now.tvs-in .tvw-flow>:nth-child(1){animation-delay:.5s!important}.tvw-then-now.tvs-in .tvw-flow>:nth-child(2){animation-delay:1s!important}
.tvw-then-now.tvs-in .tvw-flow>:nth-child(3){animation-delay:1.3s!important}.tvw-then-now.tvs-in .tvw-flow>:nth-child(4){animation-delay:1.8s!important}
.tvw-then-now.tvs-in .tvw-flow>:nth-child(5){animation-delay:2.1s!important}.tvw-then-now.tvs-in .tvw-flow>:nth-child(6){animation-delay:2.6s!important}
.tvs-ready .tvw-then-now.tvs-in .tvw-flow>:nth-child(7){animation:tvwLit .55s ease 2.9s forwards,tvwGlow 1.6s ease 3.5s 3}
@keyframes tvwLit{from{opacity:.28;transform:translateY(4px)}to{opacity:1;transform:none}}
@keyframes tvwGlow{0%,100%{box-shadow:0 10px 22px -16px rgba(13,35,70,.4)}50%{box-shadow:0 0 0 6px rgba(22,163,74,.18),0 10px 22px -16px rgba(13,35,70,.4)}}
.tvw-ai-win{position:relative}
.tvs-ready .tvw-ai-cmp.tvs-in .tvw-ai-win:after{content:"";position:absolute;left:0;right:0;top:38px;height:46px;pointer-events:none;background:linear-gradient(180deg,transparent,rgba(127,212,255,.28),transparent);animation:tvwScan 1.8s ease-in-out .3s 2 both}
@keyframes tvwScan{0%{transform:translateY(0);opacity:1}90%{opacity:1}100%{transform:translateY(230px);opacity:0}}
.tvs-ready .tvw-ai-cmp .tvw-ai-read li,.tvs-ready .tvw-ai-cmp .tvw-ai-empty{opacity:.12}
.tvs-ready .tvw-ai-cmp.tvs-in .tvw-ai-read li{animation:tvwLit .45s ease forwards}
.tvw-ai-cmp.tvs-in .tvw-ai-read li:nth-child(1){animation-delay:.7s!important}.tvw-ai-cmp.tvs-in .tvw-ai-read li:nth-child(2){animation-delay:1s!important}
.tvw-ai-cmp.tvs-in .tvw-ai-read li:nth-child(3){animation-delay:1.3s!important}.tvw-ai-cmp.tvs-in .tvw-ai-read li:nth-child(4){animation-delay:1.6s!important}
.tvw-ai-cmp.tvs-in .tvw-ai-read li:nth-child(5){animation-delay:1.9s!important}.tvw-ai-cmp.tvs-in .tvw-ai-read li:nth-child(6){animation-delay:2.2s!important}
.tvs-ready .tvw-ai-cmp.tvs-in .tvw-ai-empty{animation:tvwLit .5s ease 2.2s forwards}
.tvs-ready .tvw-tech .tvw-tech-row span{opacity:0;transform:translateY(12px)}
.tvs-ready .tvw-tech.tvs-in .tvw-tech-row span{animation:tvwLit .5s ease forwards}
.tvw-tech.tvs-in .tvw-tech-row span:nth-child(2){animation-delay:.12s}.tvw-tech.tvs-in .tvw-tech-row span:nth-child(3){animation-delay:.24s}
.tvw-tech.tvs-in .tvw-tech-row span:nth-child(4){animation-delay:.36s}.tvw-tech.tvs-in .tvw-tech-row span:nth-child(5){animation-delay:.48s}.tvw-tech.tvs-in .tvw-tech-row span:nth-child(6){animation-delay:.6s}
.tvs-ready .tvw-add-grid .tvw-add:nth-child(4n+2){transition-delay:.1s}.tvs-ready .tvw-add-grid .tvw-add:nth-child(4n+3){transition-delay:.2s}.tvs-ready .tvw-add-grid .tvw-add:nth-child(4n+4){transition-delay:.3s}
@media (prefers-reduced-motion:reduce){.tvs-ready .tvw-then-now .tvw-fl,.tvs-ready .tvw-then-now .tvw-fl-ar,.tvs-ready .tvw-ai-cmp .tvw-ai-read li,.tvs-ready .tvw-ai-cmp .tvw-ai-empty,.tvs-ready .tvw-tech .tvw-tech-row span{opacity:1!important;transform:none!important;animation:none!important}.tvw-ai-win:after{display:none}}

.tvw-then-now{display:grid;grid-template-columns:.8fr auto 1.4fr;gap:22px;align-items:center;max-width:1040px;margin:0 auto}
.tvw-tn-lab{margin:0 0 10px!important;font-size:12px;font-weight:800;letter-spacing:.16em;text-transform:uppercase;color:var(--mut)}
.tvw-now .tvw-tn-lab{color:var(--blue)}
.tvw-tn-txt{margin:12px 0 0!important;font-size:15px;color:var(--mut);line-height:1.5}
.tvw-bcard{border-radius:14px;padding:22px 20px;background:#fff;border:1px dashed #b9c6d8;box-shadow:0 8px 18px -14px rgba(13,35,70,.4);filter:grayscale(1);opacity:.85}
.tvw-bcard b{display:block;font-size:20px;color:#3b4656}.tvw-bcard span{display:block;font-size:14px;color:#6b7686;margin:4px 0 10px}.tvw-bcard i{font-style:normal;font-size:14px;color:#3b4656}
.tvw-tn-arrow{font-size:34px;color:var(--blue);font-weight:800}
.tvw-flow{display:grid;grid-template-columns:1fr 18px 1fr 18px 1fr 18px 1fr;align-items:stretch}
.tvw-fl{border-radius:14px;padding:14px 12px;background:#fff;border:1px solid #dfe6f0;box-shadow:0 10px 22px -16px rgba(13,35,70,.4)}
.tvw-fl em{display:block;font-style:normal;font-size:11px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--blue);margin-bottom:6px}
.tvw-fl b{display:block;font-size:13.5px;line-height:1.35;color:var(--navy)}
.tvw-fl-ai{background:linear-gradient(160deg,#0f1b2e,#1d3f78);border-color:#1d3f78}.tvw-fl-ai em{color:#7fd4ff}.tvw-fl-ai b{color:#fff}
.tvw-fl-win{background:#ecfbf1;border-color:#b7e7c7}.tvw-fl-win em{color:#16a34a}.tvw-fl-win u{text-decoration:none;background:#fff3c4;padding:0 3px;border-radius:4px}
.tvw-fl-ar{align-self:center;height:2px;background:#7fb2ff;position:relative}
.tvw-fl-ar:after{content:"";position:absolute;right:-1px;top:-4px;border-left:7px solid #7fb2ff;border-top:5px solid transparent;border-bottom:5px solid transparent}
.tvw-bot-grid{display:grid;grid-template-columns:1fr 1fr;gap:46px;align-items:center;max-width:1040px;margin:0 auto}
.tvw-bot h2{font-size:38px;line-height:1.1;margin:6px 0 12px!important}
.tvw-bot-txt>p{font-size:16.5px;color:var(--mut);line-height:1.6}
.tvw-bot-list{list-style:none;margin:16px 0 0;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:12px 20px}
.tvw-bot-list li{border-left:3px solid var(--blue2);padding:2px 0 2px 12px;font-size:14px;color:var(--mut);line-height:1.4}.tvw-bot-list b{display:block;color:var(--navy);font-size:15px}
.tvw-bot-tag{margin:18px 0 0!important;display:flex;gap:8px;flex-wrap:wrap}
.tvw-bot-tag span{font-size:13px;font-weight:800;padding:6px 12px;border-radius:999px;background:#e8f1ff;color:var(--blue)}.tvw-bot-tag span+span{background:#fff3d6;color:#8a5a00}
.tvw-bot-demo{position:relative;padding:10px 0 34px}
.tvw-chatw{max-width:380px;margin:0 auto;border-radius:22px;overflow:hidden;background:#fff;border:1px solid #dfe6f0;box-shadow:0 30px 60px -28px rgba(13,35,70,.5)}
.tvw-chat-h{display:flex;align-items:center;gap:10px;padding:14px 16px;background:linear-gradient(135deg,#1d5fd1,#2f7bf0);color:#fff}
.tvw-chat-av{width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,.2);display:flex;align-items:center;justify-content:center;font-size:19px}
.tvw-chat-h b{display:block;font-size:15px}.tvw-chat-h i{font-style:normal;font-size:12px;opacity:.85}
.tvw-chat-b{padding:16px 14px 6px;background:#f6f8fc;min-height:300px}
.tvw-m{max-width:82%;margin:0 0 10px!important;padding:10px 13px;border-radius:16px;font-size:14px;line-height:1.45}
.tvw-me{margin-left:auto!important;background:#1d5fd1;color:#fff;border-bottom-right-radius:5px}
.tvw-bt{background:#fff;color:#1a2233;border:1px solid #e1e8f2;border-bottom-left-radius:5px}
.tvw-chat-in{display:flex;justify-content:space-between;align-items:center;padding:12px 16px;border-top:1px solid #e6ecf4;color:#97a3b6;font-size:14px}.tvw-chat-in b{color:#1d5fd1}
.tvw-lead{position:absolute;right:-6px;bottom:0;display:flex;gap:10px;align-items:center;padding:12px 14px;border-radius:14px;background:#fff;border:1px solid #cfe9d8;box-shadow:0 16px 34px -18px rgba(13,35,70,.5);max-width:290px}
.tvw-lead span{font-size:22px}.tvw-lead b{display:block;font-size:14px;color:#16a34a}.tvw-lead i{font-style:normal;font-size:12.5px;color:var(--mut)}
.tvw-bot-ex{position:absolute;left:0;bottom:4px;margin:0!important;font-size:11px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#8a5a00;background:#fff3d6;border-radius:999px;padding:3px 9px}
.tvs-ready .tvw-d1,.tvs-ready .tvw-d2,.tvs-ready .tvw-d3,.tvs-ready .tvw-d4,.tvs-ready .tvw-d5{opacity:0;transform:translateY(8px);animation:tvwPop .5s ease forwards}
.tvs-ready .tvw-d1{animation-delay:.4s}.tvs-ready .tvw-d2{animation-delay:1.5s}.tvs-ready .tvw-d3{animation-delay:2.9s}.tvs-ready .tvw-d4{animation-delay:4s}.tvs-ready .tvw-d5{animation-delay:5.2s}
@keyframes tvwPop{to{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){.tvs-ready .tvw-d1,.tvs-ready .tvw-d2,.tvs-ready .tvw-d3,.tvs-ready .tvw-d4,.tvs-ready .tvw-d5{animation:none;opacity:1;transform:none}}
@media (max-width:900px){.tvw-then-now{grid-template-columns:1fr}.tvw-tn-arrow{transform:rotate(90deg);justify-self:center}.tvw-flow{grid-template-columns:1fr}.tvw-fl-ar{width:2px;height:16px;justify-self:center}.tvw-fl-ar:after{display:none}.tvw-bot-grid{grid-template-columns:1fr;gap:28px}.tvw-bot h2{font-size:30px}.tvw-bot-list{grid-template-columns:1fr}.tvw-lead{position:relative;right:auto;margin:14px auto 0}.tvw-bot-ex{position:static;display:inline-block;margin-top:10px!important}}

.tvw-add-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;max-width:1040px;margin:0 auto}
.tvw-add{background:#fff;border:1px solid #dfe6f0;border-radius:16px;padding:18px 18px 16px;box-shadow:0 10px 26px -18px rgba(13,35,70,.35)}
.tvw-add span{display:inline-flex;width:40px;height:40px;border-radius:12px;align-items:center;justify-content:center;font-size:20px;background:linear-gradient(135deg,#e8f1ff,#f3f7ff);margin-bottom:10px}
.tvw-add b{display:block;color:var(--navy);font-size:16px;margin-bottom:4px}.tvw-add p{margin:0!important;font-size:14px;color:var(--mut);line-height:1.45}
@media (max-width:980px){.tvw-add-grid{grid-template-columns:repeat(2,1fr)}}@media (max-width:520px){.tvw-add-grid{grid-template-columns:1fr}}

.tvw-ex{font-style:normal;font-size:11px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#8a5a00;background:#fff3d6;border-radius:999px;padding:3px 9px;margin-left:4px}
.tvw-check{display:flex;align-items:center;justify-content:space-between;gap:20px;max-width:980px;margin:30px auto 0;padding:20px 24px;border-radius:18px;background:linear-gradient(120deg,#eaf3ff,#f4f8ff);border:1px solid #cfe0f7}
.tvw-check b{display:block;font-size:19px;color:var(--navy);margin-bottom:4px}.tvw-check span{font-size:15px;color:var(--mut)}
.tvw-check .tvs-btn{flex:none}
@media (max-width:760px){.tvw-check{flex-direction:column;align-items:flex-start}}

.tvw-ai-cmp{display:grid;grid-template-columns:1fr 1fr;gap:22px;max-width:980px;margin:6px auto 0}
.tvw-ai-lab{display:flex;align-items:center;gap:9px;font-weight:800;font-size:16px;color:var(--navy);margin:0 0 10px!important}
.tvw-ai-lab span{display:inline-flex;width:24px;height:24px;border-radius:50%;align-items:center;justify-content:center;color:#fff;font-size:13px}
.tvw-ai-bad .tvw-ai-lab span{background:#d64545}.tvw-ai-good .tvw-ai-lab span{background:#16a34a}
.tvw-ai-win{border-radius:16px;overflow:hidden;border:1px solid #dfe6f0;background:#fff;box-shadow:0 18px 40px -22px rgba(13,35,70,.35);min-height:270px}
.tvw-ai-bar{display:flex;align-items:center;gap:6px;padding:10px 14px;background:#0f1b2e;color:#9fb3d6;font-size:12px}
.tvw-ai-bar i{width:9px;height:9px;border-radius:50%;background:#3a4a66}.tvw-ai-bar em{font-style:normal;margin-left:8px;letter-spacing:.04em}
.tvw-ai-code{margin:0!important;padding:18px 18px 10px;background:#0b1424;color:#7fd4ff;font:13px/1.6 Consolas,Menlo,monospace;white-space:pre;overflow:hidden}
.tvw-ai-empty{margin:0!important;padding:14px 18px 18px;background:#0b1424;color:#ff8a8a;font-weight:700;font-size:14px}
.tvw-ai-bad .tvw-ai-win{background:#0b1424}
.tvw-ai-read{list-style:none;margin:0;padding:12px 18px 16px}
.tvw-ai-read li{display:grid;grid-template-columns:90px 1fr;gap:10px;padding:8px 0;border-bottom:1px dashed #e3e9f2;font-size:14.5px;color:#1a2233}
.tvw-ai-read li:last-child{border-bottom:0}.tvw-ai-read b{color:#16a34a;font-size:12px;letter-spacing:.06em;text-transform:uppercase;padding-top:2px}
.tvw-tech{max-width:980px;margin:34px auto 0}
.tvw-tech-h{text-align:center;font-size:13px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--mut);margin:0 0 14px!important}
.tvw-tech-row{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.tvw-tech-row span{display:block;padding:14px 16px;border-radius:14px;background:linear-gradient(160deg,#0f1b2e,#13294b);color:#c9d6ee;font-size:13.5px;line-height:1.45}
.tvw-tech-row b{display:block;color:#fff;font-size:15px;margin-bottom:3px}
.tvw-logos{text-align:center;margin-top:30px}
.tvw-logos>p{margin:0 0 12px!important;font-size:13px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--mut)}
.tvw-logo-row{display:flex;flex-wrap:wrap;justify-content:center;gap:10px 12px}
.tvw-logo{display:inline-flex;align-items:center;gap:9px;padding:9px 15px;border:1px solid #dfe6f0;border-radius:999px;background:#fff;font-weight:700;font-size:14.5px;color:#1a2233}
.tvw-logo svg{width:19px;height:19px;flex:none}
@media (max-width:760px){.tvw-ai-cmp{grid-template-columns:1fr}.tvw-tech-row{grid-template-columns:1fr}.tvw-ai-code{font-size:11.5px}}

.tvw-two{grid-template-columns:repeat(2,minmax(0,1fr))!important;max-width:820px;margin-left:auto;margin-right:auto}
.tvw-phfig{display:flex;flex-direction:column;align-items:center}
.tvs-wtop:has(.tvw-phfig){grid-template-columns:1fr 290px;max-width:960px}
.tvw-phone{position:relative;width:270px;padding:10px;border-radius:48px;background:linear-gradient(145deg,#2a3242,#0a0d13);box-shadow:0 36px 64px -24px rgba(9,30,66,.5),0 0 0 2px #3a4456 inset,0 0 0 1px #11151c}
.tvw-phone-screen{position:relative;aspect-ratio:390/844;overflow:hidden;border-radius:38px;background:#13294b;display:flex;flex-direction:column}
.tvw-phone-bar{flex:none;height:40px;display:flex;align-items:center;justify-content:space-between;padding:6px 26px 0;color:#fff;font:600 12px/1 -apple-system,Segoe UI,sans-serif}
.tvw-phone-sig{font-size:8px;letter-spacing:1px}
.tvw-phone-view{position:relative;flex:1;overflow:hidden;background:#fff}
.tvw-ph-page{position:relative;animation:tvwPh 40s ease-in-out infinite;will-change:transform}
.tvw-ph-page>img{display:block!important;width:100%!important;max-width:none!important;height:auto!important;max-height:none!important;aspect-ratio:780/5400}
.tvw-ph-row{position:absolute;left:3.846%;top:51.05%;width:92.31%;height:19.67%;overflow:hidden;background:#f2f4f7}
.tvw-ph-row img{display:block!important;width:467.2%!important;max-width:none!important;height:100%!important;max-height:none!important;animation:tvwRow 40s ease-in-out infinite;will-change:transform}
.tvw-phone-island{position:absolute;top:19px;left:50%;width:80px;height:23px;margin-left:-40px;border-radius:20px;background:#05070b}
@keyframes tvwPh{0%,5%{transform:translateY(0)}20%,62%{transform:translateY(-50.2%)}84%,88%{transform:translateY(-70%)}98%,100%{transform:translateY(0)}}
@keyframes tvwRow{0%,24%{transform:translateX(0)}28%,32%{transform:translateX(-16.05%)}36%,40%{transform:translateX(-32.1%)}44%,48%{transform:translateX(-48.15%)}52%,56%{transform:translateX(-64.2%)}59%,60%{transform:translateX(-78.6%)}64%,100%{transform:translateX(0)}}
.tvw-sites .tvs-mqt img{border-radius:12px;box-shadow:0 14px 30px -14px rgba(9,30,66,.35);border:1px solid #dfe6f0;background:#fff}
@media (prefers-reduced-motion:reduce){.tvw-ph-page,.tvw-ph-row img{animation:none}}
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
        return s + GOJS + LIVECHAT_JS
    return s


D.rd = rd
if __name__ == "__main__":
    D.main()
