"""Privacy Policy page (Three Village Local + 3VL Digital services).
    python site/privacy-page/build.py --dry    -> _local.html for a local look, publishes nothing
    python site/privacy-page/build.py          -> widget "3VL Page Privacy Preview" + hidden /preview-privacy-policy (noindex)
    python site/privacy-page/build.py --live   -> widget "3VL Page Privacy" + web page 6 (/about/privacy) body = the widget shortcode
The design lives in the widget (BD's page editor strips styles); the page body only holds the shortcode."""
import json, os, re, sys, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "services-page"))
import deploy as D   # shared BD publisher (call(), main())

LIVE = "--live" in sys.argv
EFFECTIVE = "November 13, 2026"
EMAIL = "hello@threevillagelocal.com"
SITE = "https://www.threevillagelocal.com"

TITLE = "Privacy Policy | Three Village Local"
DESC = ("How Three Village Local collects, uses and protects information on threevillagelocal.com, our mobile app, emails, "
        "AI chat assistants and 3VL Digital business services, and the choices you have.")

# ---------------- content ----------------
# Each section: (anchor id, title, html). Plain English, no em dashes, nothing we cannot back up.
S = []


def sec(i, t, h):
    S.append((i, t, h))


def ul(*items):
    return "<ul>" + "".join("<li>" + x + "</li>" for x in items) + "</ul>"


A = lambda href, txt: '<a href="%s" target="_blank" rel="noopener">%s</a>' % (href, txt)
MAIL = '<a href="mailto:%s">%s</a>' % (EMAIL, EMAIL)

sec("who", "Who we are",
    "<p><b>Three Village Local</b> (&ldquo;3VL,&rdquo; &ldquo;we,&rdquo; &ldquo;us&rdquo;) is a local business directory and community "
    "media company serving Setauket, Stony Brook, Port Jefferson and the Three Village area of Long Island, New York.</p>"
    "<p>This Privacy Policy explains what information we collect, how we use and share it, and the choices you have. It covers:</p>"
    + ul("our website, <b>threevillagelocal.com</b>, including business listings, member accounts, forms, the events calendar and the blog;",
         "the <b>Three Village Local mobile app</b>;",
         "our emails, including the Three Village Weekly newsletter;",
         "our <b>AI chat assistants</b>, on our site and on other websites where we install them; and",
         "business services we offer under the <b>3VL Digital</b> name, such as AI Front Desk chat assistants, websites and dashboards, "
         "including websites we build or host for clients, unless that website posts its own privacy policy.")
    + "<p>Questions? Email us any time at " + MAIL + ".</p>")

sec("collect", "Information we collect",
    "<h3>Information you give us</h3>"
    + ul("<b>Contact and inquiry forms</b>: your name, email, phone number and message (for example the contact form, service inquiries, "
         "the free AI report request, event and special submissions, polls and contests).",
         "<b>Newsletter sign-ups</b>: your email address.",
         "<b>Business accounts and listings</b>: when a business joins, claims a listing or upgrades, we collect the owner&rsquo;s name, email, "
         "phone, login details and business information such as address, hours, photos, website, social links and a description. "
         "Most listing details are meant to be <b>public</b> and appear on the business&rsquo;s profile.",
         "<b>Questionnaires</b>: answers business owners give us to set up a listing, matching, a website, a dashboard or a chat assistant, "
         "plus any files they upload.",
         "<b>Chat messages</b>: what you type into one of our AI chat assistants, and any name, email or phone number you choose to share there.",
         "<b>Emails, texts and calls</b> you send us.",
         "<b>Payments</b>: billing name, email and address. Card details are entered with our payment processor, Stripe (see "
         "<a href=\"#payments\">Payments</a>).")
    + "<h3>Information collected automatically</h3>"
    + ul("Device and usage data such as IP address, browser and device type, pages viewed, links clicked, searches on our site, the page "
         "that referred you and approximate location (city or region) derived from your IP address.",
         "Cookies, pixels and similar technologies (see <a href=\"#cookies\">Cookies, analytics and advertising</a>).",
         "In the mobile app, the pages you view and whether you opened the app, so we can count app usage.")
    + "<h3>Information from other sources</h3>"
    + ul("<b>Public business information</b>: some listings start from publicly available information about a business, such as its name, "
         "address, phone number, website and hours. Business owners can claim, correct or ask us to remove a listing.",
         "<b>Social media</b>: when you interact with our Facebook or Instagram pages, we can see what those platforms show us, such as your "
         "public profile name and your comments or messages.",
         "<b>Service providers and partners</b>, for example payment confirmations from Stripe or event registration details from Eventbrite."))

sec("use", "How we use information",
    ul("Run the directory, member accounts, the events calendar, the mobile app and our other services.",
       "Answer your questions and requests, and pass your inquiry to the business you contacted.",
       "Send emails you asked for, such as the newsletter, account and billing messages, and lead alerts.",
       "Process payments and manage memberships and subscriptions.",
       "Understand how our site and app are used so we can improve them, and measure and improve our advertising.",
       "Promote local businesses and events, including our members, on our site, in emails and on social media.",
       "Build, run and support services for our business clients.",
       "Keep our services safe, prevent spam and fraud, and enforce our <a href=\"/about/terms\">Terms of Use</a>.",
       "Comply with the law."))

sec("ai", "AI chat assistants",
    "<p>We run AI chat assistants on threevillagelocal.com and, under our 3VL Digital AI Front Desk service, on websites of businesses that use it.</p>"
    + ul("Your messages are sent to our AI provider, <b>Anthropic</b>, to generate replies. An assistant may also read public web pages "
         "(for example the business&rsquo;s own website) to answer you.",
         "We store chat transcripts, including the page you chatted from, to follow up on requests, review quality and improve our assistants.",
         "If you ask to be contacted, or share your name, email or phone number for that reason, we send that information and a summary of "
         "the conversation to the business (or to us, on our own site) by <b>email and/or text message</b>, so a person can get back to you.",
         "AI replies can be wrong. The assistants do not give legal, financial, medical or other professional advice.",
         "Please do not share sensitive information in a chat, such as health details, Social Security numbers, account numbers or passwords.")
    + "<p>When an assistant runs on a client&rsquo;s website, that business also receives your messages and contact details and uses them "
      "under its own practices.</p>")

sec("messages", "Emails and text messages",
    "<h3>Email</h3>"
    + ul("We send email from our Google Workspace accounts (such as " + EMAIL + "). Member account emails may be sent through our website "
         "platform&rsquo;s email delivery service.",
         "Every newsletter and marketing email has an unsubscribe link. You can also email us to unsubscribe. We will still send messages "
         "needed for an account or a purchase.",
         "To help us respond quickly, emails sent to us may be sorted and summarized with AI tools, and replies may be drafted by AI. "
         "A person reviews replies before they are sent.")
    + "<h3>Text messages</h3>"
    + ul("Some services send text alerts, for example a new-lead alert to a business that uses our AI Front Desk. We only text numbers that "
         "asked for these messages or were given to us for that purpose.",
         "Message frequency varies. Message and data rates may apply.",
         "To stop texts, reply <b>STOP</b> where replies are supported, or email " + MAIL + " and we will stop them. Reply <b>HELP</b> or "
         "email us for help.",
         "<b>We do not share mobile phone numbers with third parties or affiliates for their marketing or promotional purposes.</b> "
         "Text messaging opt-in data and consent are never shared with any third parties."))

sec("cookies", "Cookies, analytics and advertising",
    "<p>Cookies are small files a website stores in your browser. We and our providers use cookies, pixels and similar tools to:</p>"
    + ul("keep you signed in and remember settings (for example your session, a preview choice or a saved item);",
         "protect forms from spam with <b>Google reCAPTCHA</b>;",
         "measure visits and how people use the site and app with <b>Google Analytics</b>;",
         "measure and improve our ads, and show our ads to people who visited our site, with the <b>Meta Pixel</b> (Facebook and Instagram);",
         "show embedded content such as <b>Google Maps</b> and <b>YouTube</b> videos, which set their own cookies when they load.")
    + "<p><b>Your choices:</b> you can block or delete cookies in your browser settings (some features, like signing in, may stop working). "
      "You can opt out of Google Analytics with the " + A("https://tools.google.com/dlpage/gaoptout", "Google Analytics opt-out add-on")
    + " and manage ads in your " + A("https://www.facebook.com/adpreferences", "Facebook ad preferences") + ". Our site does not currently "
      "respond to browser &ldquo;Do Not Track&rdquo; signals.</p>")

sec("share", "How we share information",
    "<p><b>We do not sell your personal information for money.</b> We share information only as described here:</p>"
    + ul("<b>With businesses you contact.</b> When you send an inquiry, request a callback through a chat assistant, or respond to a listing, "
         "we pass your message and contact details to that business.",
         "<b>Public content.</b> Business listings, profiles, reviews, event and special submissions, and comments you post are public.",
         "<b>Service providers</b> who help us run our services, under their own terms, including: Brilliant Directories (website, member "
         "accounts, listings and forms), Google (Workspace email, Analytics, Maps, reCAPTCHA, YouTube), Meta (Facebook, Instagram and the "
         "Meta Pixel), Stripe (payments), Anthropic (AI chat and email assistance), Vercel and Neon (hosting and databases for our AI assistants "
         "and client websites), GitHub, jsDelivr and ImageKit (delivery of site files and images), Twinr (our mobile app and push notifications), "
         "Eventbrite (event registration) and mobile carriers or messaging providers (text alerts).",
         "<b>For legal reasons</b>: to comply with law or legal process, to protect the rights, safety and property of our users, the public or us, "
         "and to prevent fraud or abuse.",
         "<b>Business transfer</b>: if our business is sold or reorganized, information may transfer to the new owner under this policy.",
         "<b>With your permission</b>, or at your direction."))

sec("payments", "Payments",
    "<p>Payments for memberships and services are processed by <b>Stripe</b>. Card numbers are entered with and stored by Stripe; "
    "<b>we do not store full card numbers</b>. We receive payment details such as your name, email, billing address, the last four digits "
    "of your card, amount and status, so we can manage your account. Stripe handles payment data under its own "
    + A("https://stripe.com/privacy", "privacy policy") + ".</p>")

sec("app", "Mobile app",
    "<p>The Three Village Local mobile app (Apple App Store and Google Play) shows the same content as our website, so this policy applies "
    "to it the same way. The app is built and delivered with an app platform provider (Twinr), which also sends push notifications.</p>"
    + ul("If you allow notifications, a device token is used to send them. You can turn notifications off at any time in your device settings.",
         "We count app opens and pages viewed in the app with Google Analytics.",
         "Apple and Google also collect information when you download or use apps, under their own policies."))

sec("social", "Social media and events",
    ul("We post about local businesses and events on Facebook and Instagram and may tag the businesses we feature. Your activity on those "
       "platforms is covered by their privacy policies.",
       "Some of our events use <b>Eventbrite</b> for registration. Eventbrite collects your registration details under its own policy, and "
       "shares them with us as the organizer so we can run the event.",
       "If you send us photos, event details or other content to publish, we may post it on our site, app, emails and social media."))

sec("digital", "3VL Digital business services",
    "<p>Three Village Local also offers business services under the <b>3VL Digital</b> name, such as AI Front Desk chat assistants, "
    "websites, AI search work and business dashboards.</p>"
    + ul("This policy covers the websites, chat assistants and forms we run for clients <b>unless that website posts its own privacy policy</b>, "
         "in which case that policy applies to it.",
         "For client services, we handle visitor information on behalf of the business (for example, sending chat leads and form messages to it). "
         "The business decides how it uses the leads it receives.",
         "Client websites we build may use Google Analytics and form-delivery services to send form messages to the business.",
         "Business clients&rsquo; own account, billing and questionnaire information is handled as described in this policy."))

sec("retention", "How long we keep information",
    "<p>We keep information for as long as we need it for the purposes in this policy: while an account, listing or subscription is active, "
    "as long as needed to answer a request or provide a service, and longer where the law requires it (for example tax and payment records). "
    "Newsletter addresses are kept until you unsubscribe; we keep a record of the unsubscribe so we do not email you again. "
    "Chat transcripts and backups are kept until they are no longer needed for the reasons above. When we no longer need information, we delete it "
    "or keep it in a form that no longer identifies you.</p>")

sec("security", "Security",
    "<p>We use reasonable safeguards to protect information, including encrypted (HTTPS) connections, access limited to the people and "
    "providers who need it, and trusted providers for hosting and payments. No method of storing or sending information is 100% secure, "
    "so we cannot guarantee absolute security. If you think your account has been compromised, email us right away.</p>")

sec("children", "Children&rsquo;s privacy",
    "<p>Our services are for a general audience and are not directed to children under 13. We do not knowingly collect personal information "
    "from children under 13. If you believe a child has given us personal information, email " + MAIL + " and we will delete it.</p>")

sec("choices", "Your choices",
    ul("<b>Emails</b>: use the unsubscribe link in any marketing email, or email us.",
       "<b>Texts</b>: reply STOP where supported, or email us.",
       "<b>Your account or listing</b>: members can update most details by signing in to their account. Business owners can claim, correct or "
       "ask us to remove a listing by emailing us.",
       "<b>Access, correction or deletion</b>: email " + MAIL + " to ask for a copy of your information, to correct it, or to delete it. "
       "We may need to keep some information for legal reasons, such as payment records.",
       "<b>Cookies and ads</b>: see <a href=\"#cookies\">Cookies, analytics and advertising</a>.",
       "<b>Push notifications</b>: turn them off in your device settings."))

sec("states", "California and other US state privacy rights",
    "<p>Depending on where you live (for example California, Colorado, Connecticut, Virginia and other states with consumer privacy laws), "
    "and depending on whether those laws apply to us, you may have the right to:</p>"
    + ul("know what personal information we collect, use and share, and get a copy of it;",
         "correct inaccurate personal information;",
         "delete personal information, subject to exceptions;",
         "opt out of the &ldquo;sale&rdquo; or &ldquo;sharing&rdquo; of personal information, or its use for targeted advertising;",
         "limit the use of sensitive personal information (we only use account logins to run your account); and",
         "not be treated differently for using these rights.")
    + "<p><b>What this means here:</b> the categories of information we collect are listed in <a href=\"#collect\">Information we collect</a>: "
      "identifiers and contact details, account and business information, purchase records, internet and app activity, approximate location "
      "from your IP address, and what you tell us in forms, chats and emails. We use them for the purposes in <a href=\"#use\">How we use "
      "information</a> and share them with the recipients in <a href=\"#share\">How we share information</a>. We do not sell personal "
      "information for money. Our use of advertising tools such as the Meta Pixel may be considered &ldquo;sharing&rdquo; or targeted "
      "advertising under some state laws; to opt out, email us with the subject &ldquo;Opt out&rdquo; and use the cookie and ad choices "
      "above.</p>"
      "<p><b>How to make a request:</b> email " + MAIL + ". We will confirm your request and may need to verify who you are, for example "
      "by matching your email address to our records. An authorized agent may make a request for you with proof of your permission. We will "
      "respond within the time the law requires. If we deny your request, you may appeal by replying with the subject &ldquo;Appeal.&rdquo;</p>")

sec("changes", "Changes to this policy",
    "<p>We may update this policy as our services change. We will post the new version here with a new &ldquo;Last updated&rdquo; date, and "
    "for important changes we may also let you know by email or with a notice on our site.</p>")

sec("contact", "Contact us",
    "<p>Questions, requests or concerns about privacy:</p>"
    '<div class="tpp-card"><b>Three Village Local</b><span>Setauket, Stony Brook and Port Jefferson, Long Island, New York</span>'
    '<span>Email: ' + MAIL + '</span><span>Contact form: <a href="/about/contact">Send us a message</a></span></div>'
    "<p>See also our <a href=\"/about/terms\">Terms of Use</a>.</p>")

# ---------------- page ----------------
SUMMARY = ul("We collect what you give us (forms, accounts, chats, emails) and basic usage data from cookies and analytics.",
             "We use it to run Three Village Local, answer you, connect you with local businesses and improve our services.",
             "<b>We do not sell your personal information.</b> We share it with the business you contact and with providers that help us run our services.",
             "Card payments are handled by Stripe. We never store full card numbers.",
             "Unsubscribe, opt out of texts, or ask to see, fix or delete your information any time: " + MAIL + ".")

toc = "".join('<li><a href="#tpp-%s">%s</a></li>' % (i, t) for i, t, _ in S)
body = "".join('<section class="tpp-s" id="tpp-%s"><h2><span class="tpp-n">%d</span>%s</h2>%s</section>' % (i, n + 1, t, h)
               for n, (i, t, h) in enumerate(S))
# keep hyphenated words and email addresses on one line (owner rule: never split words)
NW = lambda m: '<span class="tpp-nw">' + m.group(0) + '</span>'
def _nw(html):
    parts = re.split(r'(<[^>]+>)', html)
    return "".join(x if x.startswith("<") else re.sub(r"[A-Za-z0-9.]+(?:[-@][A-Za-z0-9.]+)+", NW, x) for x in parts)
body = _nw(body)
SUMMARY = _nw(SUMMARY)
# in-text anchors point at #<id>; sections carry tpp-<id>
body = re.sub(r'href="#([a-z]+)"', r'href="#tpp-\1"', body)

HTML = ('<div id="tpp"><div class="tpp-w">'
        '<header class="tpp-hd"><p class="tpp-k">Three Village Local &middot; Legal</p><h1>Privacy Policy</h1>'
        '<p class="tpp-dt">Effective ' + EFFECTIVE + ' &middot; Last updated ' + EFFECTIVE + '</p>'
        '<p class="tpp-lead">Plain English, no surprises. This is how <b>Three Village Local</b> and our <b>3VL Digital</b> business services '
        'handle your information.</p>'
        '<div class="tpp-meta"><a href="mailto:' + EMAIL + '">' + EMAIL + '</a><a href="/about/terms">Terms of Use</a><a href="/about/contact">Contact us</a></div></header>'
        '<div class="tpp-grid"><div class="tpp-toc" role="navigation" aria-label="Contents"><p class="tpp-tt">On this page</p><ol>' + toc + '</ol></div>'
        '<article class="tpp-art"><div class="tpp-sum"><h2>The short version</h2>' + SUMMARY + '</div>' + body +
        '<p class="tpp-end">Three Village Local &middot; ' + EMAIL + ' &middot; <a href="/about/terms">Terms of Use</a> &middot; Last updated ' + EFFECTIVE + '</p>'
        '</article></div></div></div>')

CSS = """
#tpp{--n:#16304f;--b:#0b63c4;--ink:#16202e;--mu:#5a6678;--ln:#e2e8f0;--sky:#e9f2fd;--yel:#f6b71b;background:#f3f6fa;font-family:'tvl-rc','Radio Canada',system-ui,sans-serif;color:var(--ink);padding:22px 16px 48px;box-sizing:border-box;width:100%}
#tpp *{box-sizing:border-box}
#tpp .tpp-w{max-width:1120px;margin:0 auto}
#tpp .tpp-hd{background:#fff;border:1px solid var(--ln);border-top:4px solid var(--b);border-radius:16px;padding:22px 20px;margin-bottom:18px}
#tpp .tpp-k{margin:0 0 6px;font-size:13px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--b)}
#tpp h1{margin:0 0 6px;font-size:34px;line-height:1.1;font-weight:700;color:var(--n)}
#tpp .tpp-dt{margin:0 0 12px;font-size:14px;color:var(--mu)}
#tpp .tpp-lead{margin:0 0 14px;font-size:17px;line-height:1.55;max-width:720px}
#tpp .tpp-meta{display:flex;flex-wrap:wrap;gap:8px}
#tpp .tpp-meta a{display:inline-block;padding:8px 14px;border-radius:999px;background:var(--sky);color:var(--b);font-weight:600;font-size:14px;text-decoration:none}
#tpp .tpp-meta a,#tpp .tpp-end a{white-space:nowrap!important}
@media (max-width:359px){#tpp .tpp-meta a{font-size:13px;padding:8px 11px}#tpp .tpp-hd,#tpp .tpp-art{padding-left:14px;padding-right:14px}}
#tpp .tpp-meta a:hover{background:var(--b);color:#fff}
#tpp .tpp-grid{display:block}
#tpp .tpp-toc{background:#fff;border:1px solid var(--ln);border-radius:16px;padding:16px 18px;margin-bottom:18px}
#tpp .tpp-tt{margin:0 0 8px;font-size:13px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--mu)}
#tpp .tpp-toc ol{margin:0;padding:0 0 0 22px;columns:1;font-size:15px;line-height:1.35}
#tpp .tpp-toc li{margin:0 0 7px;break-inside:avoid;color:var(--mu)}
#tpp .tpp-toc a{color:var(--b);text-decoration:none;font-weight:500}
#tpp .tpp-toc a:hover{text-decoration:underline}
#tpp .tpp-art{background:#fff;border:1px solid var(--ln);border-radius:16px;padding:20px 18px}
#tpp .tpp-sum{background:var(--sky);border-left:4px solid var(--b);border-radius:12px;padding:14px 16px 6px;margin-bottom:8px}
#tpp .tpp-sum h2{margin:0 0 6px;font-size:19px;color:var(--n);font-weight:700}
#tpp .tpp-s{padding-top:18px;margin-top:14px;border-top:1px solid var(--ln);scroll-margin-top:190px}
#tpp .tpp-s:first-of-type{border-top:0}
#tpp .tpp-s h2{display:flex;align-items:center;gap:10px;margin:0 0 10px;font-size:22px;line-height:1.25;font-weight:700;color:var(--n)}
#tpp .tpp-n{flex:0 0 auto;display:inline-flex;align-items:center;justify-content:center;width:30px;height:30px;border-radius:50%;background:var(--b);color:#fff;font-size:14px;font-weight:700}
#tpp h3{margin:16px 0 6px;font-size:17px;font-weight:700;color:var(--n)}
#tpp p,#tpp li{font-size:16px;line-height:1.6;overflow-wrap:normal;word-break:normal}
#tpp p{margin:0 0 12px}
#tpp ul{margin:0 0 12px;padding-left:20px}
#tpp li{margin:0 0 7px}
#tpp .tpp-art a{color:var(--b);text-decoration:underline;text-underline-offset:2px}
#tpp .tpp-card{display:flex;flex-direction:column;gap:4px;background:#f8fafc;border:1px solid var(--ln);border-radius:12px;padding:14px 16px;margin:0 0 12px;font-size:16px;line-height:1.5}
#tpp .tpp-card b{color:var(--n);font-size:17px}
#tpp .tpp-nw{white-space:nowrap!important}
#tpp .tpp-end{margin:22px 0 0;padding-top:14px;border-top:1px solid var(--ln);font-size:14px;color:var(--mu)}
@media (min-width:640px){#tpp .tpp-toc ol{columns:2;column-gap:32px}#tpp .tpp-art{padding:28px 32px}#tpp .tpp-hd{padding:28px 32px}#tpp h1{font-size:42px}}
@media (min-width:1000px){
 #tpp{padding:32px 24px 64px}
 #tpp .tpp-grid{display:grid;grid-template-columns:280px minmax(0,1fr);gap:24px;align-items:start}
 #tpp .tpp-toc{position:sticky;top:184px;margin:0;max-height:calc(100vh - 204px);overflow:auto}
 #tpp .tpp-toc ol{columns:1;font-size:14.5px}
 #tpp .tpp-s{scroll-margin-top:184px}
 #tpp p,#tpp li{font-size:16.5px}
}
"""
CSS = re.sub(r"\s*\n\s*", "", CSS.strip())

JS = " "

for nm, s in (("html", HTML), ("css", CSS)):
    assert "\\" not in s, nm + " has a backslash (BD strips them)"
    assert "—" not in s and "–" not in s and "&mdash;" not in s and "&ndash;" not in s, nm + " has an em/en dash"
    assert "[widget=" not in s and "[form=" not in s and "%%" not in s, nm + " has a BD shortcode-like token"
assert "332-9436" not in HTML and "631" not in HTML


def rd(f):
    return {"page.html": HTML, "page.css": CSS, "page.js": JS}[f]


D.rd = rd
D.NAME = "3VL Page Privacy" if LIVE else "3VL Page Privacy Preview"
D.SLUG = "preview-privacy-policy"
D.TITLE = TITLE
D.DESC = DESC
D.FB_TITLE = "Privacy Policy | Three Village Local"
D.FB_IMAGE = ""
D.HEAD = ""
D.FORM = ""


def publish_widget():
    w = {"widget_data": HTML, "widget_style": CSS, "widget_javascript": JS}
    found = D.call("GET", "data_widgets/get?property=widget_name&property_value=" + urllib.parse.quote(D.NAME)).get("message")
    found = [x for x in found if x.get("widget_name") == D.NAME] if isinstance(found, list) else []
    if found:
        wid = found[0]["widget_id"]
        print("widget", wid, D.call("PUT", "data_widgets/update", dict(w, widget_id=wid)).get("status"))
    else:
        r = D.call("POST", "data_widgets/create", dict(w, widget_name=D.NAME, widget_viewport="front"))
        m = r.get("message"); wid = (m[0] if isinstance(m, list) else m)["widget_id"]
        print("widget create", r.get("status"), wid)
    return wid


def live():
    """Widget "3VL Page Privacy" + page 6 (/about/privacy) body = shortcode. Keeps the URL; BD hero off (our own header)."""
    assert os.environ.get("TPP_LIVE_OK") == "1", "set TPP_LIVE_OK=1 to replace /about/privacy"
    wid = publish_widget()
    page = {"seo_id": "6", "content": "[widget=%s]" % D.NAME, "enable_hero_section": "0", "title": TITLE, "meta_desc": DESC,
            "facebook_title": "Privacy Policy | Three Village Local", "facebook_desc": DESC}
    print("page 6", D.call("PUT", "list_seo/update", page).get("status"))
    try:
        D.call("POST", "website_settings/refreshCache", {})
    except Exception as e:
        print("cache:", e)
    print("widget_id", wid, SITE + "/about/privacy")


if __name__ == "__main__":
    if "--dry" in sys.argv:
        local = ('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
                 '<title>local</title><link href="https://fonts.googleapis.com/css2?family=Radio+Canada:wght@400;500;600;700&display=swap" rel="stylesheet">'
                 '<style>body{margin:0}' + CSS + '</style></head><body>' + HTML + '</body></html>')
        open(os.path.join(HERE, "_local.html"), "w", encoding="utf-8").write(local)
        print("html", len(HTML), "css", len(CSS), "sections", len(S))
    elif LIVE:
        live()
    else:
        D.main()
