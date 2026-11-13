"""Integrations list for the Company Digital Dashboards demos (the "Integrations" screen inside every demo dashboard)
and the logo wall on the dashboards page.
Rule: list ONLY products with a real way in: a public API / official sign-in (OAuth), official webhooks, a feed
(RESO/IDX, CalDAV, ICS, IMAP) or an official export (CSV / report export). Anything without one is dropped.
Starts from site/integrations-page/integrations_data.py, removes the ones without a real path, adds AI + standards.
    python site/dashboards-page/integ_build.py
Writes: dash_integrations.json (here, read by build.py) and
        Documents/business-dashboards-demo/assets/integrations-data.js (window.TVL_INTEG)
Every logo URL is checked (200 + real SVG) against the pinned Simple Icons version; no logo = letter tile."""
import json, os, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
INTEG_DIR = os.path.join(HERE, "..", "integrations-page")
sys.path.insert(0, INTEG_DIR)
from integrations_data import CATS, ITEMS

DEMO = os.path.join(os.path.expanduser("~"), "Documents", "business-dashboards-demo")
VER = "16.35.0"
CDN = "https://cdn.jsdelivr.net/npm/simple-icons@%s/icons/" % VER
UA = {"User-Agent": "Mozilla/5.0"}

# no real integration path (no API, no webhooks, no feed, no usable export), or not business data
DROP = {
    "Zelle for Business", "Yelp Reservations", "Slice", "Owner.com", "Popmenu", "BentoBox", "Strava", "Snapchat", "CapCut",
    "Planoly", "Later", "Houzz Reviews", "Angi Reviews", "Better Business Bureau", "Broadly", "Waze Ads", "Adobe Express",
    "GoDaddy", "Weebly", "Framer", "Google Voice", "Ruby", "Healthgrades", "Zocdoc", "Lighthouse 360", "Phreesia",
    "CARFAX for Shops", "RepairPal", "Ylopo", "RPR", "Verkada",
    # security / device apps: not dashboard data
    "1Password", "Bitwarden", "LastPass", "Dashlane", "Google Authenticator", "Microsoft Authenticator", "Okta", "Ring",
    "Google Nest", "Arlo", "SimpliSafe", "ADT", "Kisi", "UniFi", "Wyze",
}
# connection type: api = Direct (API/OAuth), feed = Via feed, export = Via export, built = built in
TYPE = {"D": "api", "E": "export", "C": "api", "B": "built"}
FORCE = {
    "OneKey MLS": "feed", "Zillow Premier Agent": "feed", "Realtor.com": "feed", "Homes.com": "feed",
    "DoorDash": "api", "Uber Eats": "api", "Grubhub": "api", "Vagaro": "api", "Glofox": "api", "Aspire": "api",
    "OpenTable": "api", "Thumbtack": "api", "Angi Leads": "feed", "Yext": "api", "Hootsuite": "api", "Sprout Social": "api",
    "Tripadvisor": "api", "Reputation": "api", "Olo": "api",
}
TEXT = {
    "Yelp": "Rating, reviews and business details (Yelp Fusion API)",
    "DoorDash": "Delivery orders, payouts, ratings and menus (merchant API)",
    "Uber Eats": "Delivery orders, payouts, ratings and menus (merchant API)",
    "OneKey MLS": "Your listings, status changes and solds (RESO Web API / IDX feed)",
    "Zillow Premier Agent": "New buyer and seller leads routed straight into your pipeline",
    "Realtor.com": "Lead delivery into your pipeline, with source tracking",
    "Homes.com": "Lead delivery into your pipeline, with source tracking",
    "Angi Leads": "New leads delivered by the Angi lead feed, with spend reports",
    "Google Reviews": "Star rating, new reviews and replies (Business Profile API)",
}
RENAME = {"X": "X (Twitter)", "QuickBooks Online": "QuickBooks Online"}

CATS2 = [("ai", "AI & assistants")] + [c for c in CATS if c[0] != "sec"]
NEW = [
    ("OpenAI API (ChatGPT)", "ai", "api", "Powers Ask AI: plain-English answers, summaries and drafted replies", "openai"),
    ("Anthropic Claude API", "ai", "api", "Weekly owner report, review replies and post drafts from your own numbers", "anthropic"),
    ("Google Gemini API", "ai", "api", "Reads photos, menus and receipts; drafts captions and descriptions", "googlegemini"),
    ("Azure OpenAI (Microsoft Copilot models)", "ai", "api", "Copilot-grade AI running inside your own Microsoft 365 tenant", None),
    ("Perplexity API", "ai", "api", "Live web answers: competitor news, local events and trends", "perplexity"),
    ("ElevenLabs API", "ai", "api", "Natural voice for the phone assistant and video voiceovers", "elevenlabs"),
    ("Apple iCloud Calendar", "book", "feed", "Two-way calendar sync over CalDAV, on iPhone, iPad and Mac", "icloud"),
    ("Any iCal (ICS) calendar", "book", "feed", "Subscribe to or publish any calendar with a standard ICS link", None),
    ("Any IMAP email inbox", "prod", "feed", "Lead and order emails parsed into your dashboard over IMAP", None),
    ("YouTube Analytics", "social", "api", "Views, watch time, subscribers and top videos", "youtube"),
]

# industry picks: shown first on that dashboard ("Popular for restaurants"); CONN = already connected, records synced
POP = {
    "restaurant": ["Toast", "Square", "Clover", "OpenTable", "Resy", "7shifts", "DoorDash", "Uber Eats", "Grubhub", "SevenRooms", "MarginEdge",
                   "Tock", "ezCater", "QuickBooks Online", "Google Reviews", "Yelp", "Instagram", "Tripadvisor", "Mailchimp", "OpenAI API (ChatGPT)"],
    "contractor": ["Jobber", "Housecall Pro", "ServiceTitan", "CompanyCam", "QuickBooks Online", "Buildertrend", "JobNimbus", "JobTread",
                   "Procore", "DocuSign", "Angi Leads", "Thumbtack", "Houzz Pro", "Google Calendar", "Google Reviews", "Stripe", "Gusto", "Anthropic Claude API"],
    "salon": ["Square Appointments", "Vagaro", "Mindbody", "Boulevard", "GlossGenius", "Mangomint", "Fresha", "Zenoti", "Phorest", "Booksy",
              "Instagram", "Square", "Klaviyo", "Google Reviews", "Apple iCloud Calendar", "Stripe", "TikTok", "Google Gemini API"],
    "gym": ["Mindbody", "Glofox", "PushPress", "Zen Planner", "ABC Fitness", "Wodify", "Trainerize", "ClassPass", "Pike13", "WellnessLiving",
            "Stripe", "Mailchimp", "Instagram", "Google Reviews", "Twilio", "Gusto", "OpenAI API (ChatGPT)"],
    "landscaper": ["Jobber", "LMN", "Aspire", "SingleOps", "Service Autopilot", "QuickBooks Online", "CompanyCam", "Yardbook", "Route4Me",
                   "OptimoRoute", "Google Maps Platform", "Housecall Pro", "Google Calendar", "Google Reviews", "Stripe", "Perplexity API"],
}
CONN = {
    "restaurant": {"Toast": 18420, "OpenTable": 3260, "7shifts": 412, "QuickBooks Online": 1184, "Google Business Profile": 312, "Instagram": 486, "Gmail": 2210, "OpenAI API (ChatGPT)": 0},
    "contractor": {"Jobber": 1342, "CompanyCam": 8760, "QuickBooks Online": 2316, "Google Calendar": 694, "Google Business Profile": 188, "DocuSign": 141, "Anthropic Claude API": 0},
    "salon": {"Square Appointments": 6420, "Square": 9184, "Instagram": 742, "Google Business Profile": 264, "Klaviyo": 3810, "Apple iCloud Calendar": 512, "Google Gemini API": 0},
    "gym": {"PushPress": 4630, "Stripe": 7710, "Mailchimp": 2904, "Google Business Profile": 226, "Instagram": 598, "Twilio": 3412, "OpenAI API (ChatGPT)": 0},
    "landscaper": {"Jobber": 2240, "QuickBooks Online": 1912, "CompanyCam": 6140, "Google Calendar": 822, "Google Maps Platform": 1460, "Google Business Profile": 172, "Perplexity API": 0},
}
# letter-tile colors for products without a Simple Icons logo (close to each brand's own color)
MONO = {"Toast": "FF4C00", "OpenAI API (ChatGPT)": "10A37F", "Clover": "1E9E3E", "7shifts": "F26A21", "OpenTable": "DA3743", "Resy": "D4282A",
        "SevenRooms": "1F2A44", "MarginEdge": "1E5AA8", "Tock": "1A1A1A", "Grubhub": "F63440", "ezCater": "0E7C86", "Jobber": "1A9E5F",
        "Housecall Pro": "1C64F2", "ServiceTitan": "1A3B71", "CompanyCam": "1D6FE8", "Buildertrend": "F37021", "JobNimbus": "2BA64B",
        "JobTread": "2D3E50", "Procore": "F47E42", "DocuSign": "4C00FF", "Angi Leads": "FF6153", "Vagaro": "00A3AD", "Mindbody": "F05A28",
        "Boulevard": "111111", "GlossGenius": "1C1C1C", "Mangomint": "2FB386", "Fresha": "101928", "Zenoti": "0072BC", "Phorest": "0F2E4F",
        "Booksy": "00A3AD", "Klaviyo": "232426", "Glofox": "2A4BF2", "PushPress": "00C389", "Zen Planner": "F9A11B", "ABC Fitness": "E31837",
        "Wodify": "0F2C4C", "Trainerize": "1676F3", "ClassPass": "0055FF", "Pike13": "E9541D", "WellnessLiving": "2BB673", "Twilio": "F22F46",
        "LMN": "8DC63F", "SingleOps": "2E7D32", "Service Autopilot": "1565C0", "Yardbook": "4CAF50", "Route4Me": "1E88E5", "OptimoRoute": "F57C00",
        "RingCentral": "FF8800", "Azure OpenAI (Microsoft Copilot models)": "0078D4", "Any IMAP email inbox": "5B6B7F", "Any iCal (ICS) calendar": "D93025", "Plaid bank feeds": "111111",
        "Lightspeed Retail": "E4002B", "Lightspeed Restaurant": "E4002B", "Matterport": "1A1A1A", "Jotform": "FF6100"}

WALL = ["QuickBooks Online", "Square", "Toast", "Stripe", "Shopify", "Gmail", "Google Calendar", "Google Analytics 4", "Instagram", "Facebook",
        "Mailchimp", "OpenAI API (ChatGPT)", "Anthropic Claude API", "Google Gemini API", "Perplexity API", "Jobber", "DoorDash", "Uber Eats",
        "Mindbody", "Calendly", "HubSpot", "Zoom", "Dropbox", "TikTok", "Xero", "PayPal", "Yelp", "Google Drive", "Klaviyo", "WordPress"]


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()


def main():
    old = json.load(open(os.path.join(INTEG_DIR, "icons.json"), encoding="utf-8"))["icons"]
    data = json.loads(get("https://cdn.jsdelivr.net/npm/simple-icons@%s/data/simple-icons.json" % VER))
    hexes, by_title = {}, {}
    for x in data:
        s = x.get("slug") or "".join(c for c in x["title"].lower() if c.isalnum())
        hexes[s] = x.get("hex", "333333")
        by_title[x["title"].lower()] = s
    items = []
    for it in ITEMS:
        name, cat, conn, what = it[0], it[1], it[2], it[3]
        if name in DROP or cat == "sec":
            continue
        slug = old.get(name) or (it[4] if len(it) > 4 else None) or by_title.get(name.lower())
        items.append({"n": RENAME.get(name, name), "c": cat, "t": FORCE.get(name, TYPE[conn]), "w": TEXT.get(name, what), "s": slug})
    for name, cat, t, what, slug in NEW:
        items.append({"n": name, "c": cat, "t": t, "w": what, "s": slug})
    names = {i["n"] for i in items}
    assert len(names) == len(items), "duplicate names"
    for d in (POP, CONN):
        for k, v in d.items():
            for n in v:
                assert n in names, (k, n)
    for n in WALL:
        assert n in names, n
    for n in MONO:
        assert n in names, n

    def ok(s):
        try:
            r = urllib.request.urlopen(urllib.request.Request(CDN + s + ".svg", headers=UA), timeout=60)
            return s, r.status == 200 and b"<svg" in r.read(600)
        except Exception:
            return s, False

    with ThreadPoolExecutor(12) as ex:
        res = dict(ex.map(ok, sorted({i["s"] for i in items if i["s"]})))
    bad = sorted(s for s, v in res.items() if not v)
    for i in items:
        if i["s"] and res.get(i["s"]):
            i["h"] = hexes.get(i["s"], "333333")
        else:
            i["s"] = None
            if i["n"] in MONO:
                i["h"] = MONO[i["n"]]
    out = {"v": VER, "cats": CATS2, "items": items, "pop": POP, "conn": CONN, "wall": WALL}
    js = json.dumps(out, ensure_ascii=False, separators=(",", ":"))
    assert "\\" not in js
    open(os.path.join(HERE, "dash_integrations.json"), "w", encoding="utf-8").write(js)
    open(os.path.join(DEMO, "assets", "integrations-data.js"), "w", encoding="utf-8").write(
        "/* Integrations list for the demo dashboards. Generated by the dashboards page builder (integ_build.py). */\nwindow.TVL_INTEG=" + js + ";\n")
    by = {}
    for i in items:
        by[i["t"]] = by.get(i["t"], 0) + 1
    print("items", len(items), by, "with logo", sum(1 for i in items if i["s"]), "bad slugs", bad)


if __name__ == "__main__":
    main()
