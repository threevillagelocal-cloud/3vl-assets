"""A Three Village Throwback: Remembering Snow Shed (2026). Builds post.html (BD post_content).
Facts: Greater Long Island (June 30, 2026), snowshedny.com (closing note 2026, and archived pages 2009-2025 via the
Wayback Machine), Wikipedia (Stratton), Wikimedia Commons file descriptions. Images: 3vl-share/snow-shed/.
    python build.py [--sha <3vl-assets commit>] [--local]"""
import os, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SHA = sys.argv[sys.argv.index("--sha") + 1] if "--sha" in sys.argv else "master"
LOCAL = "--local" in sys.argv
ASSET = "" if LOCAL else "https://cdn.jsdelivr.net/gh/threevillagelocal-cloud/3vl-assets@%s/posts/snow-shed-2026/" % SHA
IMG = "https://threevillagelocal-cloud.github.io/3vl-share/snow-shed/"
SHARE_DIR = os.path.join(HERE, "..", "..", "..", "3vl-share", "snow-shed")


def widths(name):
    out = []
    for w in (480, 640, 1200):
        f = os.path.join(SHARE_DIR, "%s-%d.webp" % (name, w))
        if os.path.exists(f):
            real, h = Image.open(f).size
            if real not in [x[1] for x in out]:
                out.append((w, real, h))
    return out


def lazy(name, alt, sizes="(max-width:760px) 92vw, 640px"):
    ws = widths(name)
    s = ", ".join("%s%s-%d.webp %dw" % (IMG, name, w, real) for w, real, h in ws)
    mid = [x for x in ws if x[0] == 640] or ws
    w, real, h = mid[0]
    return ('<img data-src="%s%s-%d.webp" data-srcset="%s" sizes="%s" alt="%s" loading="lazy" decoding="async" width="%d" height="%d">'
            % (IMG, name, w, s, sizes, alt, real, h))


def src(name, w=640):
    ws = widths(name)
    m = [x for x in ws if x[0] == w] or ws
    return "%s%s-%d.webp" % (IMG, name, m[0][0])


C = {  # photo credits
    "hero": "Photo: cottonbro studio / Pexels",
    "logo": "Logo: Snow Shed",
    "map": "Map: &copy; OpenStreetMap contributors",
    "rack": "Photo: Mavera Zehra &#199;o&#351;kun / Pexels",
    "tune": "Photo: Snow Shed website",
    "sx92": "Photo: Maury Markowitz / Wikimedia Commons, CC BY-SA 3.0",
    "nordica": "Photo: Jon Hodal / Wikimedia Commons, CC BY-SA 2.5",
    "skis": "Photo: Chianti / Wikimedia Commons, CC BY-SA 3.0",
    "burton": "Photo: VintageWinter / Wikimedia Commons, CC BY-SA 4.0",
    "boards": "Photo: Atlantic Ambience / Pexels",
    "jiminy": "Photo: Jrclark / Wikimedia Commons, CC BY-SA 3.0",
    "hunter": "Photo: Andy Arthur / Wikimedia Commons, CC BY 2.0",
    "vt": "Photo: getaway-vacations.com / Wikimedia Commons, CC BY-SA 4.0",
    "lift80": "Photo: Jonathon M. Whitmore / Wikimedia Commons, CC BY 2.0",
    "roof": "Photo: Valentin Angel Fernandez / Pexels",
    "kids": "Photo: laura cabot carrigan / Pexels",
    "paddle": "Photo: Robert So / Pexels",
    "stratton": "Photo: Erichardson2626 / Wikimedia Commons, CC BY-SA 4.0",
}

H = []
w = H.append
w('<link rel="stylesheet" href="%ssnow.css">' % ASSET)
w('<div class="ss" id="ss-top">')

# HERO
w('<header class="ss-hero">'
  '<img class="ss-hbg" src="%shero-80s-night-ski-960.webp" srcset="%shero-80s-night-ski-960.webp 960w, %shero-80s-night-ski-1600.webp 1600w" sizes="(max-width:860px) 100vw, 860px" '
  'alt="Two skiers in bright 1980s-style ski suits on a snowy night" width="960" height="640" fetchpriority="high">'
  '<div class="ss-hshade"></div><div class="ss-snow"></div><div class="ss-snow2"></div>'
  '<div class="ss-stripes" aria-hidden="true"><i></i><i></i><i></i></div>'
  '<div class="ss-hin"><p class="ss-kick">A Three Village Throwback</p>'
  '<h2 class="ss-h1">Remembering Snow Shed<span>1982 to 2026</span></h2>'
  '<p class="ss-dek">For 44 winters, Long Island skiers and snowboarders got fitted, tuned and sent north from a little shop on Route 112. '
  'Snow Shed has closed for good, so let&#39;s do what it did best: get everyone ready for one more great day on the mountain.</p>'
  '<div class="ss-chips"><span>&#128205; Route 112, Port Jefferson Station</span><span>&#10052;&#65039; 44 winters</span><span>&#9975;&#65039; Skis, boards, tunes</span></div></div>'
  '<p class="ss-cred">%s</p></header>' % (IMG, IMG, IMG, C["hero"]))

w('<nav class="ss-nav" aria-label="Jump to section"><a href="#ss-shop">The shop</a><a href="#ss-fit">Getting fitted</a><a href="#ss-first">Your first pair</a>'
  '<a href="#ss-gear">The gear</a><a href="#ss-road">The road trip</a><a href="#ss-summer">Summers</a><a href="#ss-time">Timeline</a><a href="#ss-bye">The goodbye</a><a href="#ss-mem">Your memories</a></nav>')

# 1. THE SHOP
w('<section class="ss-sec" id="ss-shop"><p class="ss-label">The shop on 112</p><h2 class="ss-h2">Where Long Island winters started</h2>'
  '<p class="ss-lead">Chances are, if you skied or rode anywhere around Setauket, Stony Brook, Port Jefferson or Terryville over the last four decades, '
  'your season started at Snow Shed. You walked in with a kid who had grown two boot sizes since April, '
  'walked out with a season lease, a fresh wax and a lift ticket tucked in your pocket, and pointed the car north.</p>'
  '<div class="ss-shop ss-rv"><figure class="ss-logo">%s<figcaption>%s</figcaption></figure>'
  '<div class="ss-shopb"><div class="ss-pins"><span>&#128205; 1004 Route 112, Port Jefferson Station</span><span>&#128197; Opened 1982</span>'
  '<span class="p">&#10052;&#65039; Closed 2026, after 44 years</span></div>'
  '<p>Snow Shed sold and rented skis, snowboards and cross-country gear, plus bindings, boots, winter outerwear and thermal layers. '
  'Behind the counter was a full tune shop: tune-ups, hot waxes, stone grinds, base repairs and binding mounts.</p>'
  '<p>Its logo said it simply: a mountain range, <b>Snow Shed</b>, <b>Long Island, NY</b> and <b>Since 1982</b>. '
  'This year, owner Chad signed the shop&#39;s farewell note to its customers.</p></div></div></section>'
  % (lazy("snow-shed-logo", "Snow Shed logo: a mountain range with Since 1982 and Long Island, NY", "190px"), C["logo"]))

# 2. GETTING FITTED
w('<section class="ss-sec" id="ss-fit"><p class="ss-label">Getting fitted</p><h2 class="ss-h2">The fall ritual: leases, boots and a fresh tune</h2>'
  '<div class="ss-clear"><figure class="ss-float ss-rv">%s<figcaption>%s</figcaption></figure>'
  '<p class="ss-rv">The real heart of Snow Shed was the seasonal lease. Every fall, families came in for skis, boots and poles sized for the winter ahead, '
  'then brought them back in spring. The shop&#39;s old website promised that leases and daily rentals came pre-tuned, waxed and adjusted, '
  'and added: <b>&ldquo;We take the time and effort to fit each person up properly.&rdquo;</b></p>'
  '<p class="ss-rv">There was a sweetener for families, too. On the winter 2010-11 rental page, kids 12 and under got a <b>free lift ticket to Jiminy Peak</b> '
  'with any seasonal lease. Years later, the site still listed Jiminy Peak as Snow Shed&#39;s affiliate mountain.</p></div>'
  '<div class="ss-board ss-rv"><h3>Snow Shed rental board</h3><small>As posted on snowshedny.com, winter 2010-11 (shaped skis, boots and poles)</small>'
  '<div class="ss-rows"><div>Adult, 1 day<b>$28</b></div><div>Junior, 1 day<b>$20</b></div><div>Adult, 5 days<b>$89</b></div><div>Junior, 5 days<b>$60</b></div>'
  '<div>Adult season lease, new<b>$279</b></div><div>Junior season lease, new<b>$199</b></div></div>'
  '<p class="ss-note">Daily rentals: pick up after 3 PM, back by noon. Season rentals due back April 15.</p></div>'
  '<figure class="ss-fig ss-rv">%s<figcaption>A stone grinder like the ones that kept Long Island skis sharp. %s</figcaption></figure>'
  '<p class="ss-rv">The tune shop never went out of style. On the shop&#39;s 2023-24 service menu, a full tune-up (flat filed, edges sharpened, base hot waxed) was $34.99, '
  'right next to boot heat molding, base repair and binding adjustments.'
  '</p>'
  '<div class="ss-quote ss-rv"><p>&ldquo;It&#39;s been a pleasure fitting you and your family&#39;s up every winter.&rdquo;</p><i></i><small>Snow Shed, closing announcement, June 2026</small></div></section>'
  % (lazy("rental-ski-rack", "Rows of rental skis on a rack", "(max-width:760px) 46vw, 380px"), C["rack"],
     lazy("tune-shop", "Skis going through a ski tuning machine", "(max-width:760px) 92vw, 860px"), C["tune"]))

# 3. YOUR FIRST PAIR (picker)
P = [("straight", "&#9975;&#65039;", "Long, straight skis", "the 80s", "skis-straight", "straight-vs-shaped", "Two ski bottoms: a late 1980s straight ski next to a 2007 shaped ski", C["skis"],
      "The long, straight skis", "Back when skis came up past your head and every turn was a workout. The ski on the left is a late 1980s Rossignol, 180 cm long. Was your first pair like this?",
      "My first pair of skis was..."),
     ("boots", "&#129406;", "Rear-entry boots", "the late 80s", "boots", "rear-entry-boots", "Salomon SX 92 rear-entry ski boots, one open and one closed", C["sx92"],
      "The rear-entry boots", "Step in from the back, flip the lever, go. Rear-entry boots like these Salomons were everywhere in the late 1980s. Did you have a pair?",
      "My first ski boots were..."),
     ("board", "&#127938;", "My first snowboard", "the 90s", "board", "burton-1981", "A vintage Burton snowboard from about 1981", C["burton"],
      "The first snowboard", "Most mountains didn&#39;t allow snowboards at first. Did you buy, lease or borrow your first board, and where did you first ride it?",
      "My first snowboard was..."),
     ("lease", "&#128106;", "The kids&#39; season lease", "every fall", "lease", "kids-skiing-vintage", "Children on skis in the snow outside a cabin, in black and white", C["kids"],
      "The kids&#39; season lease", "Fitted every fall, back every April, two sizes bigger next year. Did your kids learn on Snow Shed leases?",
      "My family leased our gear from Snow Shed...")]
opts = []
for k, em, t, era, key, img, alt, cred, hh, pp, q in P:
    opts.append('<button type="button" class="ss-opt%s" aria-pressed="%s" data-k="%s" data-img="%s" data-alt="%s" data-cred="%s" data-h="%s" data-p="%s" data-q="%s"><em>%s</em>%s<small>%s</small></button>'
                % (" on" if k == "straight" else "", "true" if k == "straight" else "false", k, src(img), alt, cred.replace("&copy;", "(c)"), hh, pp, q, em, t, era))
f0 = P[0]
w('<section class="ss-sec" id="ss-first"><div class="ss-pick ss-rv"><p class="ss-label">Your turn to remember</p><h2 class="ss-h2">Your first pair of skis</h2>'
  '<p>Tap the one that was yours, then tell us the story.</p><div class="ss-opts">%s</div>'
  '<div class="ss-out"><figure>%s<figcaption>%s</figcaption></figure><div><h3>%s</h3><p>%s</p>'
  '<a class="ss-btn" href="mailto:hello@threevillagelocal.com?subject=My%%20Snow%%20Shed%%20memory">&#9993;&#65039; Tell us your story</a></div></div></div></section>'
  % ("".join(opts), lazy(f0[5], f0[6], "(max-width:760px) 88vw, 200px"), f0[7], f0[8], f0[9]))

# 4. THE GEAR (gallery)
G = [("nordica-boots", "Nordica rear-entry boots", "Red, loud and very late 80s", C["nordica"], ""),
     ("rear-entry-boots", "Salomon SX 92", "Open in back, closed with a lever", C["sx92"], ""),
     ("burton-1981", "Burton, around 1981", "One of the earliest Burton boards", C["burton"], ""),
     ("straight-vs-shaped", "Straight vs. shaped", "Late 1980s ski (left) next to a 2007 ski", C["skis"], ""),
     ("board-rack", "The board wall", "Snowboards lined up next to the skis", C["boards"], "w"),
     ("lift-1980s", "Chairlift days", "Skiers at a ski area, circa 1980s", C["lift80"], "w"),
     ("kids-skiing-vintage", "First day on skis", "Vintage family ski day, New Hampshire", C["kids"], "")]
gal = "".join('<figure class="%s">%s<figcaption>%s<span>%s. %s</span></figcaption></figure>'
              % (c, lazy(n, "%s: %s" % (t, d), "(max-width:760px) 46vw, 280px" if not c else "(max-width:760px) 92vw, 570px"), t, d, cr)
              for n, t, d, cr, c in G)
w('<section class="ss-sec" id="ss-gear"><p class="ss-label">The gear we all remember</p><h2 class="ss-h2">From neon one-pieces to the snowboard wall</h2>'
  '<p class="ss-rv">Snow Shed opened in 1982, right as skiing was at its most colorful: long straight skis, rear-entry boots, and one-piece suits in colors that could be seen from the summit. '
  'Over the next 44 years the shop watched the whole sport change. Snowboards went from a curiosity to a fixture on the sales floor, '
  'and skis got shorter, wider and shaped so a beginner could carve a turn on day one.</p>'
  '<div class="ss-gal ss-rv">%s</div>'
  '<p class="ss-rv">Snowboarding had to fight its way onto the mountain. In the 1980s, Stratton in southern Vermont became the first ski area to allow snowboarding, '
  'and other mountains followed over time. By the 2010s, Snow Shed&#39;s website showed Burton, Ride, GNU and Lib Tech boards right alongside the skis.</p>'
  '<figure class="ss-fig ss-rv">%s<figcaption>Stratton Mountain, Vermont, an early home for snowboarding. %s</figcaption></figure></section>'
  % (gal, lazy("stratton", "Stratton Mountain in Vermont under snow", "(max-width:760px) 92vw, 860px"), C["stratton"]))

# 5. THE ROAD TRIP
T = [("jiminy-peak", "Jiminy Peak", "Hancock, Massachusetts. Snow Shed&#39;s affiliate mountain, and a free lift ticket for leased kids.", C["jiminy"]),
     ("hunter-mountain", "Hunter Mountain", "The Catskills. Close enough for a day trip if you left before sunrise.", C["hunter"]),
     ("vermont-lift", "Vermont", "Killington, Stratton and the big Green Mountain weekends.", C["vt"])]
w('<section class="ss-sec" id="ss-road"><p class="ss-label">The road trip</p><h2 class="ss-h2">Skis on the roof, pointed north</h2>'
  '<div class="ss-clear"><figure class="ss-float ss-rv">%s<figcaption>%s</figcaption></figure>'
  '<p class="ss-rv">Long Island has plenty going for it, but mountains aren&#39;t on the list. So a Snow Shed season always ended up on the road: '
  'off the Island before dawn, skis on the roof, a thermos in the cup holder, and a car full of people asking how much longer. '
  'Snow Shed even sold the roof racks, carrying Thule car rack systems for years.</p>'
  '<p class="ss-rv">The gear got you there. The memories were made at the top of the lift: first runs, first falls, hot chocolate in the lodge, '
  'and the long, happy, tired ride home.</p></div>'
  '<div class="ss-trip">%s</div></section>'
  % (lazy("roof-rack", "Skis loaded on a car roof rack in the snow", "(max-width:760px) 46vw, 380px"), C["roof"],
     "".join('<div class="ss-stop ss-rv"><figure>%s</figure><div><b>%s</b><small>%s</small><figcaption>%s</figcaption></div></div>'
             % (lazy(n, t, "(max-width:760px) 120px, 280px"), t, d, cr) for n, t, d, cr in T)))

# 6. SUMMERS
w('<section class="ss-sec" id="ss-summer"><div class="ss-sum ss-rv"><figure>%s<figcaption>%s</figcaption></figure>'
  '<div class="ss-sumb"><p class="ss-label">Plot twist</p><h2 class="ss-h2">Snow Shed had a summer side</h2>'
  '<p>A lot of people forget this part. Around 2009 and 2010, the shop&#39;s website called itself <b>Snow Shed Ski and Marine</b>. '
  'Next to the skis it listed wakeboards, water skis, tubes, life vests, wetsuits and boogie boards, plus Hobie, Old Town and Ocean kayaks and stand-up paddle boards. '
  'In 2009 it even listed a separate marine location with boats.</p>'
  '<p>So for a while, the same shop that sent you to Vermont in January sent you out on the Sound in July.</p></div></div></section>'
  % (lazy("summer-paddle", "Kayakers and paddle boarders on the water on a summer day", "(max-width:760px) 92vw, 430px"), C["paddle"]))

# 7. TIMELINE
TL = [("1982", "big", "Snow Shed opens at 1004 Route 112 in Port Jefferson Station."),
      ("1980s", "", "Stratton in Vermont becomes the first ski area to allow snowboarding."),
      ("2009", "", "The website lists a snow location and a marine location, and an August ski and snowboard sale."),
      ("2010", "", "Snow Shed Ski and Marine: kayaks, paddle boards, wakeboards and roof racks alongside the skis."),
      ("2010-11", "", "New junior season leases for $199, plus a free Jiminy Peak lift ticket for kids 12 and under."),
      ("2013", "", "A Kayak &amp; SUP department joins Equipment, Rentals and Services on the website."),
      ("2022", "", "Daily ski and snowboard rentals, and Jiminy Peak listed as the shop&#39;s affiliate mountain."),
      ("2023-24", "", "Tune-ups at $34.99, boot heat molding, cross-country skis and Thule racks."),
      ("June 2026", "end", "Snow Shed announces it is closing after 44 years, with a 40 to 70 percent off sale."),
      ("Fall 2026", "end", "Snow Shed rental gear goes back to Sno-Haus in Huntington Station, the shop Snow Shed chose for its customers.")]
w('<section class="ss-sec" id="ss-time"><p class="ss-label">Timeline</p><h2 class="ss-h2">44 winters on Route 112</h2><ul class="ss-tl">%s</ul></section>'
  % "".join('<li class="ss-rv %s"><span class="ss-yr">%s</span><p>%s</p></li>' % (c, y, t) for y, c, t in TL))

# 8. THE GOODBYE
w('<section class="ss-sec" id="ss-bye"><p class="ss-label">The goodbye</p><h2 class="ss-h2">A shop that took care of its people to the end</h2>'
  '<div class="ss-letter ss-rv"><p>In June 2026, Snow Shed told customers it had been fighting to keep the shop going for five years and had run out of options. '
  'Customers had until June 19 to pick up skis left for tune-ups and repairs, and the closing sale took 40 to 70 percent off. '
  'By the end of June, Greater Long Island reported a for-sale sign out front.</p>'
  '<p>What stands out is how Snow Shed said goodbye. Instead of just locking the door, owner Chad picked one shop to send his customers to: '
  '<b>Sno-Haus</b> in Huntington Station, a family-owned Long Island ski shop since 1959. In his note, he wrote that he didn&#39;t want to hand people off somewhere '
  '&ldquo;nobody knows your kid&#39;s boot size or what you skied last season.&rdquo;</p>'
  '<p>Snow Shed seasonal renters from 2025-26 were offered a free basic 2026-27 seasonal rental at Sno-Haus Huntington Station (terms apply), '
  'and Snow Shed rental gear could be returned there through October 15, 2026. If you still have questions, Sno-Haus Huntington Station is at 2 W Jericho Turnpike.</p>'
  '<p>That&#39;s the kind of thing a neighborhood shop does. <b>&ldquo;We will certainly miss all of you,&rdquo;</b> the shop wrote. Three Village will miss you too, Snow Shed.</p></div>'
  '<div class="ss-map ss-rv" style="margin-top:18px">'
  '<div class="ss-mapcard"><b>Snow Shed, 1982 to 2026</b>1004 Route 112, Port Jefferson Station, near Route 347 (Nesconset Highway)</div>'
  '%s<span class="ss-pulse"></span><span class="ss-pin" aria-hidden="true"></span><figcaption>%s</figcaption></div></section>'
  % (lazy("route-112-map", "Map of Route 112 and Route 347 in Port Jefferson Station, with a pin at 1004 Route 112", "(max-width:760px) 92vw, 860px"), C["map"]))

# 9. MEMORIES
w('<section class="ss-sec" id="ss-mem"><div class="ss-mem ss-rv"><p class="ss-label">Share your Snow Shed memory</p><h2 class="ss-h2">Did Snow Shed get you on the mountain?</h2>'
  '<p>Your first lease, a boot fitting that finally didn&#39;t hurt, a tune that saved your season, a summer kayak, or a job behind the counter: we want to hear it. '
  'We&#39;re also looking for <b>old photos of the shop</b> on Route 112 to add to this story (with your name on them, of course).</p>'
  '<p>Email us, or share it in the comments on our Facebook post.</p>'
  '<div class="ss-btns"><a class="ss-btn" href="mailto:hello@threevillagelocal.com?subject=My%20Snow%20Shed%20memory">&#9993;&#65039; Email a memory or photo</a>'
  '<a class="ss-btn fb" href="https://www.facebook.com/ThreeVillageLocal" target="_blank" rel="noopener">Share on our Facebook</a>'
  '<button type="button" class="ss-btn alt" data-share>&#128279; Send this to a friend</button></div></div>'
  '<div class="ss-more"><a href="https://www.threevillagelocal.com/blog/a-three-village-throwback-crazy-eddie-on-route-347-his-prices-were-insane"><small>Another throwback</small>Crazy Eddie on Route 347</a>'
  '<a href="https://www.threevillagelocal.com/blog/a-three-village-throwback-cooky%E2%80%99s-steak-pub-in-stony-brook"><small>Another throwback</small>Cooky&#39;s Steak Pub in Stony Brook</a></div></section>')

w('<p class="ss-src">Sources: <a href="https://greaterlongisland.com/snow-shed-port-jefferson-station-closes-44-years/" rel="nofollow">Greater Long Island</a> (Brian Harmon, June 30, 2026); '
  '<a href="https://www.snowshedny.com/" rel="nofollow">snowshedny.com</a> (the shop&#39;s closing note, and archived pages from 2009 to 2025 via the Internet Archive); '
  '<a href="https://en.wikipedia.org/wiki/Stratton_Mountain_Resort" rel="nofollow">Wikipedia</a>; Wikimedia Commons file descriptions. '
  'Photos are credited under each picture; Pexels photos are free to use, Wikimedia Commons photos are used under the licenses shown. '
  'Gear and mountain photos show the era, not Snow Shed itself.</p>')
w('</div>')
w('<script src="%ssnow.js" defer></script>' % ASSET)
out = "".join(H)
# never split words at a hyphen on phones: hyphenated words in visible text get a nowrap span (not in tags/attributes)
import re
out = "".join(part if part.startswith("<") else re.sub(r"([A-Za-z0-9.]+(?:-[A-Za-z0-9.]+)+)", lambda m: '<span class="nw">%s</span>' % m.group(1), part)
              for part in re.split(r"(<[^>]+>)", out))
assert "\\" not in out, "no backslashes (BD strips them)"
assert "—" not in out and "&mdash;" not in out, "no em dashes"
open(os.path.join(HERE, "post.html"), "w", encoding="utf-8").write(out)
print("post.html", len(out), "chars")
