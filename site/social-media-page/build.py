"""Social media service page: promotion on Three Village Local + social media marketing for the business's own accounts.
Owner 11/12/2026: every service on /services gets its own premium interactive page. No prices.
    python site/social-media-page/build.py          -> widget "3VL Page Social Media Preview" + hidden /preview-social-media (noindex)
    (--live -> /social-media only after the owner's OK)"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "svc-kit"))
import kit as K
from kit import ic, SV, WB


def post(img, w, h, collab, likes, cap, alt, cls=""):
    return '''<div class="tsm-post %s"><p class="tsm-ph"><i class="tsm-av"></i><b>threevillagelocal</b><span>and <b>%s</b></span></p>
<div class="tsm-img"><img src="%s" alt="%s" loading="lazy" width="%d" height="%d"><u class="tsm-heart">%s</u></div>
<p class="tsm-act">%s%s%s</p><p class="tsm-likes">%s likes</p><p class="tsm-cap"><b>threevillagelocal</b> %s</p></div>''' % (
        cls, collab, img, alt, w, h, ic("heart"), ic("heart"), ic("message"), ic("share"), likes, cap)


FEED = (post(SV + "w-tommys-place-v2.webp", 560, 294, "tommysplace", "1,240", "Welcome to the neighborhood! Burgers, wings and game day on Main St.", "Welcome post for Tommy's Place", "tsm-wide") +
        post(SV + "w-restaurant-ig-v1.webp", 400, 500, "yourbusiness", "2,086", "Hungry? The best restaurants in Three Village are right here.", "Three Village Local restaurant roundup post") +
        post(SV + "w-namkeen-hot-chicken-v1.webp", 560, 294, "namkeenhotchicken", "980", "Nashville hot chicken with a South Asian kick. Stony Brook, go!", "Social post for Namkeen Hot Chicken", "tsm-wide") +
        post(SV + "w-fitness-sports-ig-v1.webp", 400, 500, "yourbusiness", "1,512", "Let&#39;s get moving: the best gyms and teams in town.", "Three Village Local fitness roundup post"))

HERO_VIS = '''<div class="tsm-hv">
  <div class="tvx-phone tsm-phone"><div class="tvx-screen">
    <div class="tsm-top"><b>Instagram</b><span>''' + ic("heart") + ic("message") + '''</span></div>
    <div class="tsm-stories"><i><u>3VL</u></i><i class="b"><u>Eat</u></i><i class="c"><u>Shop</u></i><i class="d"><u>Events</u></i><i class="e"><u>Live</u></i></div>
    <div class="tsm-scroll"><div class="tsm-track">''' + FEED + FEED + '''</div></div>
  </div></div>
  <div class="tvx-chip tsm-c1" style="animation-delay:.4s"><span class="tvx-ic">''' + ic("tag") + '''</span><div><b>@yourbusiness</b>tagged in every post</div></div>
  <div class="tvx-chip tsm-c2" style="animation-delay:1.4s"><span class="tvx-ic" style="--ac:#d2557a">''' + ic("users") + '''</span><div><b>Collab post</b>on both profiles</div></div>
  <div class="tvx-chip tsm-c3" style="animation-delay:2.2s"><span class="tvx-ic" style="--ac:#16a37a">''' + ic("eye") + '''</span><div><b>100,000+ views</b>a month, all local</div></div>
</div>'''

HERO = K.hero("Social media", "Seen all over town,", "every single week.",
              "Two ways to win on social: we promote your business to Three Village Local&#39;s 100,000+ monthly Facebook and Instagram views, and we can run content for your own accounts, too.",
              HERO_VIS, ("See the two ways", "#tvp-two"))

NAV = K.snav([("two", "Two ways"), ("types", "Post types"), ("collab", "Tag + collab"), ("calendar", "Content calendar"), ("how", "How it works"), ("faq", "FAQ")])

TWO = K.sec("two", "Two ways we help", "Our audience, and your own accounts.", "Use one, or put them together. Both are done for you by our local team.",
            '''<div class="tsm-two">
  <div class="tsm-way tvs-up"><p class="tsm-tag">''' + ic("megaphone") + '''Our audience</p><h3>Social media promotion on Three Village Local</h3>
    <p>We create scroll-stopping posts and reels about your business and share them with our Facebook and Instagram audience: 100,000+ local views a month.</p>
    <ul><li>''' + ic("check") + '''Custom graphics and reels, made for you</li><li>''' + ic("check") + '''Your business tagged, with a collab invite</li><li>''' + ic("check") + '''Spotlights, specials, events and launches</li><li>''' + ic("check") + '''Also shared on our website and mobile app</li></ul>
    <p class="tsm-best"><b>Best for:</b> reaching new local customers fast</p></div>
  <div class="tsm-way tsm-dk tvs-up"><p class="tsm-tag">''' + ic("calendar") + '''Your accounts</p><h3>Social media marketing for your own accounts</h3>
    <p>We plan, create and schedule content for your own Facebook and Instagram, so your page stays active and on brand without eating your week.</p>
    <ul><li>''' + ic("check") + '''A monthly content calendar you approve</li><li>''' + ic("check") + '''Branded graphics, reels and captions</li><li>''' + ic("check") + '''Posted on schedule for you</li><li>''' + ic("check") + '''A simple monthly recap</li></ul>
    <p class="tsm-best"><b>Best for:</b> a page that looks alive and builds trust</p></div>
</div>''')

TYPES = [("spot", "star", "Spotlights", "Business spotlights", "A warm introduction to the people and story behind your business, written to make neighbors want to stop in.",
          "New businesses, anniversaries, new owners", '<div class="tsm-mock"><img src="' + SV + 'w-tommys-place-v2.webp" alt="Spotlight post for Tommy&#39;s Place" loading="lazy" width="560" height="294"></div>'),
         ("special", "tag", "Specials", "Specials and offers", "Your deal of the week, a holiday menu or a limited run, designed to be shared and saved.",
          "Restaurants, shops, seasonal services", '<div class="tsm-mock"><img src="' + SV + 'w-namkeen-hot-chicken-v1.webp" alt="Special post for Namkeen Hot Chicken" loading="lazy" width="560" height="294"><span class="tsm-stk">This week only</span></div>'),
         ("event", "calendar", "Events", "Events", "Grand openings, live music, classes and pop-ups, promoted before the day and celebrated after.",
          "Openings, classes, tastings, live music", '<div class="tsm-mock tsm-ev"><img src="' + WB + 'lm-setauket-main-v2.webp" alt="Main Street in Setauket in the fall" loading="lazy" width="640" height="760"><div><span><b>SAT</b>21</span><p><i>You&#39;re invited</i>Holiday Makers Market</p><em>' + ic("pin") + 'Main Street</em></div></div>'),
         ("reel", "video", "Reels", "Reels", "Short vertical videos with music and captions. The format that reaches the most new people on Instagram and Facebook.",
          "Behind the scenes, before and after, tours", '<div class="tsm-mock tsm-reel"><img src="' + SV + 'girard-poster.webp" alt="Promo reel for Girard Wealth Management" loading="lazy" width="480" height="854"><span>' + ic("play") + '</span><em>' + ic("video") + 'Reel</em></div>'),
         ("carousel", "layers", "Carousels", "Carousels", "Swipeable posts that tell a story in a few slides: a menu, a project, a top-five list. People save these.",
          "Menus, portfolios, how-tos, roundups", '<div class="tsm-mock tsm-car"><div class="tsm-car-t"><img src="' + SV + 'w-the-pie-of-port-jeff-v2.webp" alt="Post for The Pie of Port Jeff" loading="lazy" width="560" height="294"><img src="' + SV + 'w-saturday-candy-co-v4.webp" alt="Post for Saturday Candy Co" loading="lazy" width="560" height="294"><img src="' + SV + 'w-amazing-olive-v2.webp" alt="Post for Amazing Olive" loading="lazy" width="560" height="294"></div><p class="tsm-dots"><i></i><i></i><i></i></p></div>')]
ttabs = "".join('<button class="tvx-tab%s" data-tab="%s">%s%s</button>' % (" on" if n == 0 else "", k, ic(i), t) for n, (k, i, t, h, p, b, m) in enumerate(TYPES))
tpan = "".join('<div class="tsm-tp" data-panel="%s"><div class="tsm-tp-v" data-run>%s</div><div class="tsm-tp-t"><span class="tvx-ic">%s</span><h3>%s</h3><p>%s</p><p class="tsm-best"><b>Great for:</b> %s</p></div></div>' % (k, m, ic(i), h, p, b) for k, i, t, h, p, b, m in TYPES)
TYPESEC = K.sec("types", "Sample post types", "The right post for every moment.", "Tap through the kinds of posts we make. Real examples from Three Village businesses.",
                '<div class="tsm-types tvs-up" data-tabs data-auto="4200"><div class="tvx-tabs">' + ttabs + '</div>' + tpan + '</div>')


def prof(name, sub, logo, cls="", more=()):
    tiles = '<i class="on"><img src="' + SV + 'w-tommys-place-v2.webp" alt="" loading="lazy" width="560" height="294"></i>'
    tiles += "".join('<i><img src="%s%s" alt="" loading="lazy" width="400" height="500"></i>' % (SV, m) for m in more) + "<i></i>" * (5 - len(more))
    return '<div class="tsm-prof %s"><p class="tsm-prof-h"><span>%s</span><b>%s</b><em>%s</em></p><div class="tsm-grid">%s</div></div>' % (cls, logo, name, sub, tiles)


COLLAB = '''<section class="tvs-sec tvx-sec tvx-dark tsm-collab" id="tvp-collab">
  <div class="tvs-head tvs-up"><p class="tvs-eyebrow">Tag + collab</p><h2>One post. Two profiles. Double the reach.</h2><p>Every post we make about you tags your business and comes with an Instagram collab invite. Accept it, and the post lives on your profile too.</p></div>
  <div class="tsm-cb tvs-up" data-run>
    ''' + prof("threevillagelocal", "Local audience", ic("star"), "", ("w-restaurant-ig-v1.webp", "w-fitness-sports-ig-v1.webp", "w-home-services-ig-v1.webp", "w-beauty-personal-care-ig-v1.webp", "w-medical-services-ig-v1.webp")) + '''
    <div class="tsm-link"><span>''' + ic("link") + '''</span><b>Collab</b><i></i></div>
    ''' + prof("yourbusiness", "Your followers", ic("store"), "tsm-you") + '''
  </div>
  <ol class="tsm-csteps tvs-up"><li><b>1</b>We make the post and tag you</li><li><b>2</b>We send an Instagram collab invite</li><li><b>3</b>You tap accept</li><li><b>4</b>Likes, comments and views add up on both profiles</li></ol>
</section>'''

CAL = [(2, "spot", "Meet the owner"), (5, "special", "Weekend special"), (7, "reel", "Behind the scenes"), (10, "story", "Poll: pick the new flavor"),
       (12, "event", "Holiday market booth"), (14, "reel", "60-second tour"), (16, "spot", "Customer favorite"), (19, "special", "Gift card week"),
       (22, "story", "Countdown sticker"), (24, "event", "Live music night"), (26, "reel", "How it&#39;s made"), (28, "special", "Last call for orders")]
TYPE_LAB = {"spot": "Spotlight", "reel": "Reel", "special": "Special", "event": "Event", "story": "Story"}
days = ""
cmap = {d: (t, x) for d, t, x in CAL}
for d in range(1, 29):
    if d in cmap:
        t, x = cmap[d]
        days += '<div class="tsm-d" data-t="%s"><em>%d</em><span class="tsm-ch tsc-%s"><b>%s</b>%s</span></div>' % (t, d, t, TYPE_LAB[t], x)
    else:
        days += '<div class="tsm-d"><em>%d</em></div>' % d
legend = '<button class="tsm-f on" data-f="all">All</button>' + "".join('<button class="tsm-f" data-f="%s"><i class="tsc-%s"></i>%s</button>' % (k, k, v) for k, v in TYPE_LAB.items())
agenda = "".join('<li data-t="%s"><em>%d</em><span class="tsm-ch tsc-%s"><b>%s</b>%s</span></li>' % (t, d, t, TYPE_LAB[t], x) for d, t, x in CAL)
CALSEC = K.sec("calendar", "Content calendar", "A month of content, planned with you.",
               "For your own accounts, we map out the month ahead so your page is never quiet. You approve it, we create it and post it. Tap a type to filter.",
               '''<div class="tsm-cal tvs-up" id="tsm-cal">
    <div class="tsm-cal-top"><div><p>Sample month</p><h3>Your content calendar</h3></div><div class="tsm-legend">''' + legend + '''</div></div>
    <div class="tsm-wk"><span>Mon</span><span>Tue</span><span>Wed</span><span>Thu</span><span>Fri</span><span>Sat</span><span>Sun</span></div>
    <div class="tsm-month">''' + days + '''</div>
    <ul class="tsm-agenda">''' + agenda + '''</ul>
    <p class="tsm-cal-f">''' + ic("check") + '''Every post approved by you before it goes out</p>
  </div>''')

STATS = '<section class="tvs-sec tvx-sec" id="tvp-reach">' + K.stats_band("A built-in local audience, every month.", "Reach") + '</section>'

HOW = K.sec("how", "How it works", "Simple for you. Consistent for your customers.", "",
            K.steps([("Kickoff", "A quick chat about your goals, your customers and your style."),
                     ("Create", "We design the graphics, edit the reels and write the captions."),
                     ("Approve", "You see everything first and ask for any changes."),
                     ("Post and tag", "We post on schedule, tag you and send the collab invite."),
                     ("Recap", "A simple look at what worked and what&#39;s next.")]))

FAQ = K.faq([
    ("What is the difference between promotion and marketing?", "Promotion means we post about your business on Three Village Local&#39;s own Facebook and Instagram, in front of our local audience. Marketing means we create and post content on your own accounts. Many businesses do both."),
    ("What is a collab post?", "It is an Instagram feature that lets one post appear on two profiles at once. We tag you and send a collab invite; when you accept, the post shows on your profile too and the likes, comments and views count on both."),
    ("Do I approve posts before they go out?", "Always. You see every post and caption first, and nothing goes out until you say it looks good."),
    ("Do I have to share my passwords?", "No. For your own accounts we can be added as a partner through Meta&#39;s business tools, so you stay in control and never hand over a password."),
    ("Which platforms do you post on?", "Mainly Facebook and Instagram, where Three Village spends its time online. Posts about you are also shared on our website and in our free mobile app."),
    ("How often will you post?", "It depends on your goals and your plan. We&#39;ll recommend a rhythm that fits your business in your free plan."),
    ("How do I get started?", "Fill out the short form below. We&#39;ll send a free, personalized social media plan by email, with no pressure and no contract."),
])

REL = K.related("social-media", ["promo-video", "email-articles", "new-business-launch", "ai-search", "join", "websites"])
CTA = K.cta("Let&#39;s get you noticed", "Ready to be seen all over town?", "Tell us about your business and we&#39;ll send a free social media plan by email.")

JS = ''';(function(){var c=document.getElementById('tsm-cal');if(!c)return;var fs=[].slice.call(c.querySelectorAll('.tsm-f'));
fs.forEach(function(b){b.setAttribute('type','button');b.setAttribute('aria-pressed',b.classList.contains('on')?'true':'false');b.addEventListener('click',function(){var f=b.getAttribute('data-f');fs.forEach(function(x){var on=x===b;x.classList.toggle('on',on);x.setAttribute('aria-pressed',on?'true':'false');});
 c.setAttribute('data-f',f);[].forEach.call(c.querySelectorAll('[data-t]'),function(el){el.classList.toggle('dim',f!=='all'&&el.getAttribute('data-t')!==f);});if(window.tvxGA)tvxGA('svc_page_filter',{filter:f});});});})();'''

CSS = '''
.tsm-hv{position:relative;display:flex;justify-content:center;width:100%;padding:10px 0}
.tsm-phone{width:250px;aspect-ratio:9/18}
.tsm-top{position:relative;z-index:3;display:flex;align-items:center;justify-content:space-between;padding:34px 14px 8px;background:#fff;border-bottom:1px solid #eef1f5}
.tsm-top b{font-family:Georgia,serif;font-style:italic;font-size:19px;color:#111}
.tsm-top span{display:flex;gap:12px;color:#111}.tsm-top .tvx-svg{width:19px;height:19px}
.tsm-stories{position:relative;z-index:3;display:flex;gap:9px;padding:8px 12px 10px;background:#fff;border-bottom:1px solid #eef1f5}
.tsm-stories i{width:44px;height:44px;border-radius:50%;padding:2px;background:linear-gradient(135deg,#feda75,#fa7e1e,#d62976,#4f5bd5);flex:none}
.tsm-stories u{display:flex;align-items:center;justify-content:center;width:100%;height:100%;border-radius:50%;border:2px solid #fff;background:#13294b;color:#fff;font-size:10px;font-weight:800;text-decoration:none}
.tsm-stories .b u{background:#c2410c}.tsm-stories .c u{background:#16a37a}.tsm-stories .d u{background:#1d5fbf}.tsm-stories .e u{background:#d2557a}
.tsm-scroll{position:absolute;left:0;right:0;top:132px;bottom:0;overflow:hidden}
.tsm-track{animation:tsmScroll 26s linear infinite}
@keyframes tsmScroll{from{transform:translateY(0)}to{transform:translateY(-50%)}}
.tsm-post{padding-bottom:10px;border-bottom:1px solid #f0f2f5;background:#fff}
.tsm-ph{display:flex;align-items:center;gap:6px;margin:0!important;padding:8px 10px;font-size:11px;color:#222;white-space:nowrap;overflow:hidden}
.tsm-ph b{font-weight:800}.tsm-ph span{color:#666;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;min-width:0;display:block}.tsm-ph span b{color:#222}
.tsm-av{width:24px;height:24px;border-radius:50%;flex:none;background:#13294b;border:2px solid #ffc53d}
.tsm-img{position:relative;aspect-ratio:4/5;background:#e9eef5;overflow:hidden}
.tsm-wide .tsm-img{aspect-ratio:560/294}
.tsm-img img{width:100%;height:100%;object-fit:cover;display:block}
.tsm-heart{position:absolute;left:50%;top:50%;width:70px;height:70px;margin:-35px 0 0 -35px;color:#fff;opacity:0;animation:tsmHeart 6.5s ease-in-out infinite}
.tsm-heart .tvx-svg{width:70px;height:70px;fill:#fff;filter:drop-shadow(0 4px 12px rgba(0,0,0,.35))}
.tsm-post:nth-child(2n) .tsm-heart{animation-delay:3.2s}
@keyframes tsmHeart{0%,30%{opacity:0;transform:scale(.4)}36%{opacity:1;transform:scale(1.15)}42%{transform:scale(.95)}50%{opacity:1;transform:scale(1)}58%,100%{opacity:0;transform:scale(1.1)}}
.tsm-act{display:flex;gap:12px;margin:0!important;padding:8px 10px 2px;color:#222}.tsm-act .tvx-svg{width:19px;height:19px}.tsm-act .tvx-svg:first-child{color:#e0245e;fill:#e0245e}
.tsm-likes{margin:0!important;padding:2px 10px;font-size:11px;font-weight:800;color:#222}
.tsm-cap{margin:0!important;padding:0 10px;font-size:11px;line-height:1.4;color:#333}.tsm-cap b{font-weight:800}
.tsm-c1{left:-6px;top:14%}.tsm-c2{right:-4px;top:46%}.tsm-c3{left:4%;bottom:6%}
/* two ways */
.tsm-two{display:grid;grid-template-columns:1fr 1fr;gap:20px;max-width:1080px;margin:0 auto}
.tsm-way{position:relative;padding:30px 30px 26px;border-radius:26px;background:#fff;border:1px solid #dfe8f6;box-shadow:0 22px 44px -32px rgba(9,30,66,.45);overflow:hidden}
.tsm-way:after{content:"";position:absolute;right:-60px;top:-60px;width:200px;height:200px;border-radius:50%;background:radial-gradient(circle,rgba(47,125,225,.14),transparent 70%)}
.tsm-dk{background:linear-gradient(150deg,#0b1f4b,#123a7a);border:0;color:#fff}
.tsm-tag{display:inline-flex;align-items:center;gap:8px;margin:0 0 14px!important;padding:6px 13px;border-radius:999px;background:#e7f0ff;color:var(--blue);font-weight:800;font-size:13px;letter-spacing:.08em;text-transform:uppercase}
.tsm-tag .tvx-svg{width:16px;height:16px}
.tsm-dk .tsm-tag{background:rgba(142,197,255,.16);color:#8ec5ff}
.tsm-way h3{font-size:25px;line-height:1.18;margin:0 0 10px!important}.tsm-dk h3{color:#fff!important}
.tsm-way>p{color:var(--mut);font-size:16px;line-height:1.6;margin:0 0 16px!important}.tsm-dk>p{color:#cdddf3!important}
.tsm-way ul{list-style:none;margin:0 0 18px!important;padding:0!important;display:grid;gap:9px}
.tsm-way li{display:flex;gap:10px;align-items:flex-start;margin:0!important;font-weight:700;color:var(--navy);font-size:15.5px;line-height:1.4}.tsm-dk li{color:#fff}
.tsm-way li .tvx-svg{width:20px;height:20px;color:#16a37a;margin-top:1px}.tsm-dk li .tvx-svg{color:#5ee0a0}
.tsm-best{margin:0!important;padding:11px 14px;border-radius:12px;background:#f4f7fb;font-size:14.5px;color:var(--ink2)}
.tsm-dk .tsm-best{background:rgba(255,255,255,.08);color:#dbe7f8}.tsm-best b{color:var(--navy)}.tsm-dk .tsm-best b{color:#ffc53d}
/* post types */
.tsm-tp{display:grid;grid-template-columns:1.05fr .95fr;gap:40px;align-items:center;max-width:1000px;margin:0 auto}
.tsm-tp-v{display:flex;justify-content:center;padding:26px;border-radius:26px;background:radial-gradient(circle at 50% 30%,#eaf2ff,#f6f9fd 70%);border:1px solid #e1e9f5;min-height:360px;align-items:center}
.tsm-mock{position:relative;width:100%;max-width:440px;border-radius:16px;overflow:hidden;background:#fff;box-shadow:0 30px 60px -30px rgba(9,30,66,.55);animation:tvxRise .6s both}
.tsm-mock>img{display:block;width:100%;height:auto}
.tsm-stk{position:absolute;right:14px;top:14px;padding:8px 13px;border-radius:999px;background:#ffc53d;color:#13294b;font-weight:800;font-size:13px;transform:rotate(4deg);box-shadow:0 10px 20px -10px rgba(0,0,0,.5);animation:tsmWig 2.4s ease-in-out infinite}
@keyframes tsmWig{0%,100%{transform:rotate(4deg)}50%{transform:rotate(-3deg) scale(1.06)}}
.tsm-ev{max-width:320px;aspect-ratio:4/5}.tsm-ev>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.tsm-ev>div{position:absolute;left:0;right:0;bottom:0;padding:70px 18px 18px;background:linear-gradient(180deg,transparent,rgba(9,24,52,.92) 55%);color:#fff}
.tsm-ev>div>span{float:left;margin-right:12px;width:54px;padding:6px 0;border-radius:12px;background:#fff;color:#13294b;text-align:center;font-size:24px;font-weight:800;line-height:1}
.tsm-ev>div>span b{display:block;font-size:11px;color:#c2410c;letter-spacing:.08em;margin-bottom:3px}
.tsm-ev p{margin:0!important;font-size:21px;font-weight:800;line-height:1.15}.tsm-ev p i{display:block;font-style:normal;font-size:12px;font-weight:800;color:#ffc53d;letter-spacing:.1em;text-transform:uppercase;margin-bottom:3px}
.tsm-ev em{clear:both;display:flex;align-items:center;gap:6px;padding-top:12px;font-style:normal;font-size:13px;color:#d4e3f7}.tsm-ev em .tvx-svg{width:15px;height:15px}
.tsm-reel{max-width:230px}
.tsm-reel>span{position:absolute;left:50%;top:50%;width:58px;height:58px;margin:-29px 0 0 -29px;border-radius:50%;background:rgba(255,255,255,.92);display:flex;align-items:center;justify-content:center;animation:tvxPulse 2.4s infinite}
.tsm-reel>span .tvx-svg{fill:#13294b;color:#13294b;margin-left:3px}
.tsm-reel em{position:absolute;left:10px;top:10px;display:flex;align-items:center;gap:5px;padding:5px 9px;border-radius:999px;background:rgba(0,0,0,.5);color:#fff;font-style:normal;font-size:12px;font-weight:800}.tsm-reel em .tvx-svg{width:14px;height:14px}
.tsm-car{max-width:440px}
.tsm-car-t{display:flex;width:300%;animation:tsmCar 9s infinite}
.tsm-car-t img{width:33.3333%;height:auto;display:block}
@keyframes tsmCar{0%,28%{transform:translateX(0)}33%,61%{transform:translateX(-33.3333%)}66%,95%{transform:translateX(-66.6667%)}100%{transform:translateX(0)}}
.tsm-dots{display:flex;justify-content:center;gap:6px;margin:0!important;padding:10px}
.tsm-dots i{width:7px;height:7px;border-radius:50%;background:#cfd8e3;animation:tsmDot 9s infinite}
.tsm-dots i:nth-child(2){animation-delay:3s}.tsm-dots i:nth-child(3){animation-delay:6s}
@keyframes tsmDot{0%,30%{background:#1d5fbf}34%,100%{background:#cfd8e3}}
.tsm-tp-t .tvx-ic{margin-bottom:12px}
.tsm-tp-t h3{font-size:28px;margin:0 0 10px!important}
.tsm-tp-t>p:not(.tsm-best){color:var(--mut);font-size:16.5px;line-height:1.6;margin:0 0 16px!important}
/* collab */
.tsm-cb{display:grid;grid-template-columns:1fr 150px 1fr;align-items:center;max-width:860px;margin:0 auto}
.tsm-prof{padding:16px;border-radius:20px;background:#fff;color:var(--ink);box-shadow:0 30px 60px -30px rgba(0,0,0,.6)}
.tsm-prof-h{display:grid;grid-template-columns:auto 1fr;gap:0 10px;align-items:center;margin:0 0 12px!important}
.tsm-prof-h span{grid-row:span 2;width:42px;height:42px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:#13294b;color:#ffc53d;border:2px solid #ffc53d}
.tsm-you .tsm-prof-h span{background:#16a37a;color:#fff;border-color:#9fe6c8}
.tsm-prof-h span .tvx-svg{width:20px;height:20px}
.tsm-prof-h b{font-size:15px;color:var(--navy)}.tsm-prof-h em{font-style:normal;font-size:12.5px;color:var(--mut)}
.tsm-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:4px}
.tsm-grid i{aspect-ratio:1;border-radius:6px;background:#e9eef5;overflow:hidden}
.tsm-you .tsm-grid i:nth-child(2){background:linear-gradient(135deg,#d9f3e8,#bfe8d6)}.tsm-you .tsm-grid i:nth-child(3){background:linear-gradient(135deg,#fde9cf,#f8d3a3)}.tsm-you .tsm-grid i:nth-child(4){background:linear-gradient(135deg,#e3ecfb,#c9d9f5)}.tsm-you .tsm-grid i:nth-child(5){background:linear-gradient(135deg,#f6dfe7,#eec2d2)}.tsm-you .tsm-grid i:nth-child(6){background:linear-gradient(135deg,#ece7fb,#d6cdf5)}
.tsm-grid i.on{box-shadow:0 0 0 3px #ffc53d;animation:tsmGlow 2.4s infinite}
.tsm-grid img{width:100%;height:100%;object-fit:cover;display:block}
@keyframes tsmGlow{0%,100%{box-shadow:0 0 0 3px #ffc53d}50%{box-shadow:0 0 0 6px rgba(255,197,61,.45)}}
.tsm-link{position:relative;text-align:center}
.tsm-link:before{content:"";position:absolute;left:0;right:0;top:27px;height:3px;background:repeating-linear-gradient(90deg,#8ec5ff 0 6px,transparent 6px 12px);background-size:24px 3px;animation:tpvFlow2 .9s linear infinite}
@keyframes tpvFlow2{from{background-position:0 0}to{background-position:24px 0}}
.tsm-link span{position:relative;display:inline-flex;width:56px;height:56px;border-radius:50%;align-items:center;justify-content:center;background:#ffc53d;color:#13294b;box-shadow:0 0 0 8px rgba(255,197,61,.18)}
.tsm-link b{display:block;margin-top:8px;color:#fff;font-size:13px;letter-spacing:.1em;text-transform:uppercase}
.tsm-csteps{list-style:none;display:grid;grid-template-columns:repeat(4,1fr);gap:12px;max-width:1000px;margin:34px auto 0!important;padding:0!important}
.tsm-csteps li{margin:0!important;padding:16px;border-radius:16px;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.14);color:#e3edfa;font-weight:700;font-size:15px;line-height:1.4}
.tsm-csteps b{display:flex;width:30px;height:30px;border-radius:50%;align-items:center;justify-content:center;background:#8ec5ff;color:#0b1f4b;margin-bottom:8px;font-size:14px}
/* calendar */
.tsm-cal{max-width:1080px;margin:0 auto;padding:26px;border-radius:26px;background:#fff;border:1px solid #dfe8f6;box-shadow:0 26px 50px -36px rgba(9,30,66,.5)}
.tsm-cal-top{display:flex;align-items:flex-end;justify-content:space-between;gap:16px;flex-wrap:wrap;margin-bottom:18px}
.tsm-cal-top p{margin:0!important;font-size:12.5px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--blue)}
.tsm-cal-top h3{margin:0!important;font-size:24px}
.tsm-legend{display:flex;flex-wrap:wrap;gap:6px}
.tvx .tsm-f{appearance:none;display:inline-flex;align-items:center;gap:6px;margin:0;padding:7px 12px!important;border-radius:999px!important;border:1px solid #d3dff0!important;background:#fff!important;color:var(--navy)!important;font:inherit;font-size:13.5px!important;font-weight:800!important;cursor:pointer;line-height:1.2!important;box-shadow:none!important;text-transform:none!important;letter-spacing:0!important;height:auto;min-height:0;width:auto}
.tvx .tsm-f.on{background:var(--navy)!important;color:#fff!important;border-color:var(--navy)!important}
.tsm-f i{width:10px;height:10px;border-radius:50%}
.tsc-spot{--c:#1d5fbf}.tsc-reel{--c:#7c3aed}.tsc-special{--c:#e0731f}.tsc-event{--c:#16a37a}.tsc-story{--c:#d2557a}
.tsm-f i{background:var(--c)}
.tsm-wk,.tsm-month{display:grid;grid-template-columns:repeat(7,1fr);gap:6px}
.tsm-wk span{font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--mut);padding:0 6px 6px}
.tsm-d{min-height:86px;padding:6px;border-radius:12px;background:#f6f9fd;border:1px solid #e8eef6;transition:opacity .25s}
.tsm-d em{display:block;font-style:normal;font-size:12.5px;font-weight:800;color:#8a97a8;margin-bottom:5px}
.tsm-ch{display:block;padding:6px 8px;border-radius:9px;background:color-mix(in srgb,var(--c) 12%,#fff);border-left:3px solid var(--c);font-size:12.5px;line-height:1.3;color:var(--navy);font-weight:700;transition:transform .2s}
.tsm-ch b{display:block;font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--c)}
.tsm-d:hover .tsm-ch{transform:translateY(-2px)}
.tsm-cal .dim{opacity:.25}
.tsm-agenda{display:none}
.tsm-cal-f{display:flex;align-items:center;gap:8px;margin:16px 0 0!important;font-weight:700;color:var(--navy);font-size:15px}.tsm-cal-f .tvx-svg{color:#16a37a}
.tsm-month .tsm-d[data-t]{animation:tvxPop .5s both}
@media (max-width:1100px){.tsm-c2{right:-10px}}
@media (max-width:900px){
 .tsm-two,.tsm-tp{grid-template-columns:1fr;gap:18px}.tsm-tp-v{min-height:0;padding:18px}.tsm-tp-t{text-align:center}.tsm-tp-t .tvx-ic{margin-left:auto;margin-right:auto}.tsm-tp-t h3{font-size:24px}
 .tsm-way{padding:24px 20px 20px}.tsm-way h3{font-size:22px}
 .tsm-cb{grid-template-columns:1fr 44px 1fr;max-width:560px}.tsm-prof{padding:9px;border-radius:14px}.tsm-prof-h{gap:0 7px;margin-bottom:8px!important}.tsm-prof-h span{width:28px;height:28px}.tsm-prof-h span .tvx-svg{width:14px;height:14px}.tsm-prof-h b{font-size:11.5px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.tsm-prof-h em{font-size:10.5px}.tsm-grid{gap:3px}.tsm-grid i{border-radius:4px}
 .tsm-link span{width:36px;height:36px;box-shadow:0 0 0 5px rgba(255,197,61,.18)}.tsm-link span .tvx-svg{width:17px;height:17px}.tsm-link:before{top:17px}.tsm-link b{display:none}
 .tsm-csteps{grid-template-columns:1fr 1fr;margin-top:22px!important}.tsm-csteps li{display:flex;gap:10px;align-items:center;padding:12px;font-size:14px}.tsm-csteps b{flex:none;margin:0}
 .tsm-cal{padding:18px 14px}.tsm-month{gap:4px}.tsm-wk{gap:4px}.tsm-wk span{padding:0 0 4px;text-align:center;font-size:10.5px;letter-spacing:0}
 .tsm-d{min-height:42px;padding:4px;text-align:center;border-radius:9px}.tsm-d em{margin:0}
 .tsm-d .tsm-ch{font-size:0;padding:0;width:9px;height:9px;border-radius:50%;border:0;background:var(--c);margin:4px auto 0}.tsm-d .tsm-ch b{display:none}
 .tsm-agenda{display:grid;grid-template-columns:1fr 1fr;list-style:none;margin:14px 0 0!important;padding:0!important;gap:6px}
 .tsm-agenda li{display:flex;align-items:center;gap:10px;margin:0!important;transition:opacity .25s}
 .tsm-agenda em{flex:none;width:20px;font-style:normal;font-weight:800;color:var(--mut);font-size:13px;text-align:right}
 .tsm-agenda .tsm-ch{flex:1}
 .tsm-types .tvx-tabs{flex-wrap:nowrap;justify-content:flex-start;overflow-x:auto;padding:4px 2px 10px;scrollbar-width:none;-webkit-mask-image:linear-gradient(90deg,#000 85%,transparent);mask-image:linear-gradient(90deg,#000 85%,transparent)}.tsm-types .tvx-tabs::-webkit-scrollbar{display:none}.tsm-types .tvx-tab{flex:none}
}
@media (max-width:420px){.tsm-agenda .tsm-ch{font-size:11.5px;padding:5px 6px}.tsm-agenda .tsm-ch b{font-size:9.5px}.tsm-csteps{grid-template-columns:1fr}.tsm-legend{gap:5px}.tvx .tsm-f{padding:6px 10px!important;font-size:12.5px!important}}
'''

if __name__ == "__main__":
    K.page("Social Media", "social-media",
           "Social Media Promotion and Marketing for Local Businesses | Three Village Local",
           "Get seen all over Three Village: social media promotion to 100,000+ local Facebook and Instagram views a month, plus done-for-you social media marketing for your own accounts. Tagged posts, collab posts, reels and a content calendar you approve.",
           "Social media that gets you seen all over town",
           [HERO, NAV, TWO, TYPESEC, COLLAB, CALSEC, STATS, HOW, FAQ, REL, CTA], bundle="social", css=CSS, js=JS, fb_image="/share/svc-social-media-v1.jpg")
    K.main()
