"""Thanksgiving in Three Village (2026 blog). Builds post.html (BD post_content).
Facts come from 3vl-site-guard data/thanksgiving.json (each event/business there was checked against the organizer's own page),
so dates and times here always match the live /thanksgiving guide.     python build.py [--local]"""
import datetime, html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LOCAL = "--local" in sys.argv
ASSET = "" if LOCAL else "https://threevillagelocal-cloud.github.io/3vl-share/thanksgiving-blog/"
IMG = "https://threevillagelocal-cloud.github.io/3vl-share/thanksgiving-blog/"
GUIDE = "https://www.threevillagelocal.com/thanksgiving"
D = json.load(open(os.path.join(HERE, "..", "..", "..", "3vl-site-guard", "data", "thanksgiving.json"), encoding="utf-8"))
EV = {e["title"]: e for e in D["events"]}
BZ = {b["biz"]: b for b in D["biz"]}
e = html.escape


def t12(d):
    h = d.hour % 12 or 12
    return ("%d:%02d %s" % (h, d.minute, "AM" if d.hour < 12 else "PM")).replace(":00 ", " ")


def when(ev):
    s = datetime.datetime.fromisoformat(ev["start"])
    x = datetime.datetime.fromisoformat(ev["end"]) if ev.get("end") else None
    day = "%s, %s %d" % (s.strftime("%a"), s.strftime("%b"), s.day)
    if ev.get("allday"):
        return day
    return day + " &middot; " + t12(s) + ((" - " + t12(x)) if x and x > s and x.date() == s.date() else "")


def ev_row(title, icon="&#127810;", label=None, note=None):
    ev = EV[title]
    href = ev.get("page") or ev.get("link")
    ph = ('<img data-src="%s" alt="%s" width="240" height="160" loading="lazy">' % (e(ev["img"]), e(ev["title"]))) if ev.get("img") else '<span>%s</span>' % icon
    town = "Setauket" if (ev.get("town") or "") == "East Setauket" else ev.get("town", "")
    return ('<a class="tgb-ev tgb-rv" href="%s"><div class="ph">%s</div><div class="bd"><small>%s</small><b>%s</b><span class="w">%s &middot; %s%s</span></div></a>'
            % (e(href), ph, label or when(ev), e(ev["title"]), e(ev["venue"].split(",")[0]), e(town), (". " + note) if note else ""))


def biz_tile(name, what=None):
    b = BZ[name]
    href = b.get("member") or b.get("link")
    town = "Setauket" if (b.get("town") or "") == "East Setauket" else b.get("town", "")
    if b.get("img"):
        return ('<a class="tgb-b tgb-rv" href="%s"><img data-src="%s" alt="%s" width="300" height="300" loading="lazy"><span>%s<em>%s &middot; %s</em></span></a>'
                % (e(href), e(b["img"]), e(name), e(name), e(what or b["what"]), e(town)))
    return ('<a class="tgb-b noimg tgb-rv" href="%s"><span>%s<em>%s &middot; %s</em></span></a>' % (e(href), e(name), e(what or b["what"]), e(town)))


def link(name):
    b = BZ[name]
    return '<a href="%s">%s</a>' % (e(b.get("member") or b.get("link")), e(name))


def cta(big, small, btn="Open the guide", lite=False):
    return ('<a class="tgb-cta%s tgb-rv" href="%s"><i>&#129411;</i><span><b>%s</b><small>%s</small></span><em>%s &rarr;</em></a>'
            % (" lite" if lite else "", GUIDE, big, small, btn))


H = []
w = H.append
w('<link rel="stylesheet" href="%stg.css">' % ASSET)
w('<div class="tgb" id="tgb-top">')

# HERO
w('<header class="tgb-hero"><img class="tgb-hbg" src="%shero-960.webp" srcset="%shero-960.webp 960w, %shero-1600.webp 1600w" sizes="(max-width:860px) 100vw, 860px" '
  'alt="Then and now: a 1600s harvest feast by the harbor beside a modern family Thanksgiving in a Long Island dining room" width="960" height="540" fetchpriority="high">'
  '<div class="tgb-hshade"></div><i class="tgb-leaf l1"></i><i class="tgb-leaf l2"></i><i class="tgb-leaf l3"></i><i class="tgb-leaf l4"></i><i class="tgb-leaf l5"></i>'
  '<div class="tgb-hin"><p class="tgb-kick">A Three Village Thanksgiving</p>'
  '<h2 class="tgb-h1">Thanksgiving in Three Village: <span>our traditions, our tables and our local favorites</span></h2>'
  '<p class="tgb-dek">How Setauket, Stony Brook and Port Jefferson do Thanksgiving week.</p></div></header>'
  % (IMG, IMG, IMG))
w(cta("Our live Thanksgiving guide", "Every event, who&#39;s open on Thanksgiving Day, pies, catering and shop-local picks, updated daily."))
w('<nav class="tgb-nav" aria-label="Jump to section"><a href="#tgb-roots">Our roots</a><a href="#tgb-eve">Thanksgiving Eve</a><a href="#tgb-table">The table</a>'
  '<a href="#tgb-give">Giving back</a><a href="#tgb-kids">For kids</a><a href="#tgb-friday">Black Friday</a><a href="#tgb-sbs">Small Business Saturday</a>'
  '<a href="#tgb-sunday">The Sunday after</a></nav>')

# INTRO
w('<p class="tgb-lead tgb-rv">The tree lights up on Main Street the night before, the bakeries are slammed by Wednesday, and by Sunday Santa is rolling through Port Jeff. '
  'Here are the traditions, local spots and events that make Thanksgiving in Three Village.</p>')

# 1 ROOTS
w('<section class="tgb-sec" id="tgb-roots"><p class="tgb-label">Where it all started</p><h2 class="tgb-h2">A harvest table on the harbor</h2>'
  '<div class="tgb-clear"><figure class="tgb-float tgb-rv"><img data-src="%sthen-640.webp" alt="A 1600s harvest feast on a meadow by the harbor" width="640" height="357" loading="lazy">'
  '<figcaption>An imagined 1600s harvest feast by the water. Illustration created for Three Village Local.</figcaption></figure>'
  '<p class="tgb-rv">Long before there was a Main Street, this was the home of the <b>Setalcott</b> people, who fished and farmed along the harbor that still carries their name. '
  'English settlers arrived in <b>1655</b>, and Setauket grew up around the village green, the mill pond and the churches that still stand there today. '
  'Harvest gatherings, giving thanks for a good season on the water and in the fields, are about as old as the place itself.</p>'
  '<p class="tgb-rv">This year two local programs bring that history to life. At <b>The Long Island Museum</b> in Stony Brook, the Boys &amp; Girls Club of Shinnecock Nation Dance Troupe '
  'performs traditional and powwow-style dances, sharing their heritage and Indigenous culture. And the <b>Emma S. Clark Memorial Library</b> is hosting a talk on where our favorite '
  'Thanksgiving traditions came from, timed to the 100th Macy&#39;s Thanksgiving Day Parade.</p></div>'
  '<div class="tgb-evs">%s%s</div></section>'
  % (IMG, ev_row("Boys & Girls Club of Shinnecock Nation Dance Troupe", "&#129718;"), ev_row("From Pies to Parades (Zoom)", "&#127880;")))

# 2 THANKSGIVING EVE
w('<section class="tgb-sec" id="tgb-eve"><p class="tgb-label">Wednesday night</p><h2 class="tgb-h2">Thanksgiving Eve: the lights go on in Port Jeff</h2>'
  '<p class="tgb-rv">Everybody&#39;s home. The college kids are back, the cousins drove in, and the night before Thanksgiving is when Port Jefferson Village lights up for the season. '
  'The <b>Port Jefferson Business Improvement District</b> lights the village holiday tree at the corner of the Broadways and Main Street, a short walk from dinner, '
  'a drink with old friends, or a last-minute stop for something you forgot.</p>'
  '<div class="tgb-evs">%s</div>'
  '<div class="tgb-quote tgb-rv"><p>The night before Thanksgiving is the unofficial hometown reunion.</p><i></i></div></section>'
  % ev_row("Port Jefferson BID Tree Lighting", "&#127876;"))

# 3 THE TABLE
w('<section class="tgb-sec" id="tgb-table"><p class="tgb-label">The table</p><h2 class="tgb-h2">Cook it, order it, or let someone else do the dishes</h2>'
  '<div class="tgb-clear"><figure class="tgb-float tgb-rv"><img data-src="%snow-640.webp" alt="A modern family laughing around a Thanksgiving table in a Long Island dining room" width="640" height="357" loading="lazy">'
  '<figcaption>Thanksgiving today. Illustration created for Three Village Local.</figcaption></figure>'
  '<p class="tgb-rv">There are three kinds of Thanksgiving hosts in Three Village: the ones who cook every dish from scratch, the ones who order the sides and take the credit, '
  'and the smart ones who book a table and skip the dishes. Our local businesses have all three covered.</p>'
  '<p class="tgb-rv"><b>Going out?</b> %s at Danfords in Port Jefferson is serving Thanksgiving dinner from 11 AM to 5 PM, and %s in Stony Brook has a Thanksgiving buffet from 11 AM to 7 PM. '
  'Both fill up, so book early.</p>'
  '<p class="tgb-rv"><b>Ordering in?</b> <a href="%s">Uncle Giuseppe&#39;s Marketplace</a> in Port Jefferson Station is taking Thanksgiving catering orders through Saturday, Nov 21. '
  'For pies and desserts, %s in Stony Brook and %s in Setauket are the classic calls. For trays, sides and the stuff nobody wants to make, try %s, %s, %s or %s. '
  'And don&#39;t forget the bottle for the table: %s has you covered.</p></div>'
  '<div class="tgb-panel tgb-rv"><h3>&#128222; Pro tip: call this week, not next week</h3>Local bakeries and caterers book up fast in the week before Thanksgiving. '
  'Call ahead for pies, rolls and trays, and ask about pickup times on Wednesday, Nov 25.</div>'
  '<div class="tgb-biz">%s</div>'
  % (IMG, link("Black Pearl Seafood Chophouse"), link("Mirabelle Restaurant & Tavern"), e(BZ["Uncle Giuseppe's Marketplace"]["link"]),
     link("Premiere Pastry Shop"), link("Rolling Pin"), link("Setauket Gourmet Delicatessen and Caterers"), link("Pumpernickles Deli & Market"),
     link("Farm to Table Catering and Cafe by Filomena"), link("The Break Room Cafe"), link("Hamlet Wines & Liquors"),
     "".join(biz_tile(n, wt) for n, wt in (("Black Pearl Seafood Chophouse", "Open Thanksgiving, 11 AM - 5 PM"), ("Mirabelle Restaurant & Tavern", "Thanksgiving buffet, 11 AM - 7 PM"),
                                          ("Premiere Pastry Shop", None), ("Rolling Pin", None), ("Setauket Gourmet Delicatessen and Caterers", None),
                                          ("Pumpernickles Deli & Market", None), ("Farm to Table Catering and Cafe by Filomena", None), ("The Break Room Cafe", None),
                                          ("Hamlet Wines & Liquors", None)))))
w(cta("Who else is open on Thanksgiving?", "We add restaurants and catering deadlines to the live guide as they post them.", "See the list", lite=True))

# 4 GIVING BACK
w('<section class="tgb-sec" id="tgb-give"><p class="tgb-label">Giving back</p><h2 class="tgb-h2">Neighbors feeding neighbors</h2>'
  '<p class="tgb-rv">Some of the best Three Village traditions happen in a collection basket. Every November, local groups and families quietly make sure nobody in town goes without a Thanksgiving meal.</p>'
  '<div class="tgb-evs">%s</div>'
  '<div class="tgb-panel tgb-rv"><h3>&#129309; More ways to give (2026 details coming)</h3><ul>'
  '<li><b>Barton Family Thanksgiving Food Drive</b>, Stony Brook. 2025 was its 20th year, collecting non-perishables at 105 Main Street.</li>'
  '<li><b>Three Village Community Trust Thanksgiving Food Drive</b>, Setauket, with help from Three Village students.</li>'
  '<li><b>Three Village Interfaith Thanksgiving Service</b>. Local congregations gather each year; in 2025 it was at Caroline Church, with the offering going to the Ronald McDonald House at Stony Brook Children&#39;s Hospital.</li>'
  '</ul><p style="margin:10px 0 0!important">We&#39;ll add 2026 dates to the <a href="%s">live guide</a> as soon as the organizers post them.</p></div></section>'
  % (ev_row("Reboli Center Thanksgiving Food Drive", "&#129387;", label="Now through Fri, Nov 20"), GUIDE))

# 5 KIDS (one photo + compact list, owner 11/7: shorter scroll)
kids = ["Apple Pie Making (Family)", "Turkey Tea Light", "Gratitude Vases (Grades 3-5)", "Turkey Time (3 years-PreK with Caregiver)",
        "A Charlie Brown Thanksgiving Treat", "Stop Motion Animation: Balloons Over Broadway (Grades 3-5)"]
def krow(t):
    ev = EV[t]
    lib = ev["venue"].split(",")[0].replace(" Memorial Library", "").replace(" Public Library", "").replace(" Free Library", "")
    return '<li><a href="%s"><time>%s</time><b>%s</b><span>%s</span></a></li>' % (e(ev.get("page") or ev.get("link")), when(ev), e(t), e(lib))
w('<section class="tgb-sec" id="tgb-kids"><p class="tgb-label">For the kids</p><h2 class="tgb-h2">Turkey crafts, pie bakers and a Charlie Brown Thanksgiving</h2>'
  '<figure class="tgb-wide tgb-rv"><img data-src="%skids-960.webp" alt="Kids making paper turkey crafts at a library craft table" width="960" height="536" loading="lazy">'
  '<figcaption>Illustration created for Three Village Local.</figcaption></figure>'
  '<p class="tgb-rv">The <b>Emma S. Clark</b>, <b>Port Jefferson</b> and <b>Comsewogue</b> libraries have more than a dozen free Thanksgiving programs: turkey crafts, '
  'a real apple pie class and a stop-motion parade for the 100th Macy&#39;s parade. Most need registration.</p>'
  '<ul class="tgb-klist tgb-rv">%s</ul></section>' % (IMG, "".join(krow(t) for t in sorted([k for k in kids if k in EV], key=lambda k: EV[k]["start"]))))
w(cta("See all the kids programs", "The full list, with registration links, lives on our Thanksgiving guide.", "Kids &amp; family"))

# 6 BLACK FRIDAY
w('<section class="tgb-sec" id="tgb-friday"><p class="tgb-label">Friday, Nov 27</p><h2 class="tgb-h2">Black Friday, the Three Village way</h2>'
  '<p class="tgb-rv">Skip the mall. In Three Village, the day after Thanksgiving means a walk through <b>Stony Brook Village Center</b>, where the shops roll out Black Friday deals all day, '
  'a petting zoo sets up in front of D.K. Brothers and holiday carolers stroll the village from 1:30 to 3:30 PM. Over in Port Jefferson, '
  '<b>The Rinx</b> at Harborfront Park opens for the season the same day, so you can work off the stuffing on the ice.</p>'
  '<div class="tgb-evs">%s%s</div>'
  '<p class="tgb-rv">History buffs, keep an eye out too: the <b>Three Village Historical Society</b> lists a Walking Tour / Turkey Trot in Setauket on Friday, Nov 27. '
  'We&#39;ll post the time and meeting spot as soon as they share it.</p></section>'
  % (ev_row("Black Friday Festival at Stony Brook Village", "&#128717;&#65039;"), ev_row("Outdoor Ice Skating on the Harbor: Opening Day", "&#9976;&#65039;")))

# 7 SMALL BUSINESS SATURDAY
shops = ["Amazing Olive", "Chocology Unlimited", "Saturday Candy Co.", "Kate's Vintage Rose", "The East End Shirt Company",
         "Willow + Harlow Candle Company", "Sea Creations", "The Crushed Olive", "Envision Crystal"]
w('<section class="tgb-sec" id="tgb-sbs"><p class="tgb-label">Saturday, Nov 28</p><h2 class="tgb-h2">Small Business Saturday: start your holiday list here</h2>'
  '<p class="tgb-rv">This is the day that matters most to the shops that make Three Village feel like home. Port Jefferson lists Small Business Saturday on the Village calendar, '
  'and the shops, restaurants and galleries along Main Street and East Broadway are ready for you. In Stony Brook, the village center is a holiday list in itself.</p>'
  '<p class="tgb-rv">A few of our favorites: olive oils and balsamics at %s and %s, chocolate at %s, Swedish candy at %s, '
  'gifts at %s and %s, candles at %s, local tees at %s and crystals at %s.</p>'
  '<div class="tgb-biz">%s</div>%s</section>'
  % (link("Amazing Olive"), link("The Crushed Olive"), link("Chocology Unlimited"), link("Saturday Candy Co."), link("Kate's Vintage Rose"), link("Sea Creations"),
     link("Willow + Harlow Candle Company"), link("The East End Shirt Company"), link("Envision Crystal"),
     "".join(biz_tile(n) for n in shops), ev_row("Small Business Saturday in Port Jefferson", "&#128717;&#65039;")))

# 8 THE SUNDAY AFTER
w('<section class="tgb-sec" id="tgb-sunday"><p class="tgb-label">Sunday, Nov 29</p><h2 class="tgb-h2">The Sunday after: the holiday season begins</h2>'
  '<p class="tgb-rv">If Thanksgiving is the warm-up, the Sunday after is the kickoff. Santa rides down Main Street in Port Jefferson, the Three Village Historical Society fills the '
  'Setauket Neighborhood House with crafters and bakers, and Dickensian characters take over the Carriage Museum in Stony Brook as part of the Charles Dickens Festival.</p>'
  '<div class="tgb-evs">%s%s%s</div>'
  '<div class="tgb-panel navy tgb-rv"><h3>&#127917; Also this season</h3><ul>'
  '<li><b>Theatre Three</b> in Port Jefferson runs its children&#39;s holiday show, <i>Barnaby Saves Christmas</i>, November 21 to December 27, with a sensory friendly performance on Sunday, Nov 22.</li>'
  '<li><b>Gallery North</b> in Setauket opens its annual <i>Deck the Halls</i> holiday show on Thursday, Nov 19, with small original works by over 50 artists.</li>'
  '<li><b>The Reboli Center</b> in Stony Brook celebrates its winter exhibition with an artists&#39; reception on Saturday, Nov 14.</li>'
  '</ul></div></section>'
  % (ev_row("Port Jefferson Santa Parade & Visit", "&#127877;"), ev_row("Winter Holiday Market at the Setauket Neighborhood House", "&#127873;"),
     ev_row("Dickens in the Carriage Museum", "&#127913;")))

# END
w('<div class="tgb-end tgb-rv"><p class="tgb-label">Bookmark it</p><h2 class="tgb-h2">The live Thanksgiving guide has it all</h2>'
  '<p>Plans change and new events get added every week. Our guide updates every day with every confirmed event, who&#39;s open on Thanksgiving, '
  'catering deadlines, food drives and Small Business Saturday picks.</p>%s'
  '<button type="button" class="tgb-share" data-share>&#128279; Share this with your family</button></div>' % cta("Open the live Thanksgiving guide", "threevillagelocal.com/thanksgiving", "Go"))
w('<p class="tgb-src">Event and business details come from each organizer&#39;s or business&#39;s own website, calendar or posts, as listed on our Thanksgiving guide. '
  'Plans change, so please check with them before you go. The two Thanksgiving table images are illustrations created for Three Village Local.</p>')
w('</div>')
w('<script src="%stg.js" defer></script>' % ASSET)
out = "".join(H)
out = "".join(part if part.startswith("<") else re.sub(r"([A-Za-z0-9.]+(?:-[A-Za-z0-9.]+)+)", lambda m: '<span class="nw">%s</span>' % m.group(1), part)
              for part in re.split(r"(<[^>]+>)", out))
assert "\\" not in out, "no backslashes (BD strips them)"
assert "—" not in out and "&mdash;" not in out, "no em dashes"
assert "East Setauket" not in out
open(os.path.join(HERE, "post.html"), "w", encoding="utf-8").write(out)
print("post.html", len(out), "chars")
