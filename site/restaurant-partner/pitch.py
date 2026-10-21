"""Personal Restaurant Partner page for one restaurant (owner 10/20/2026): their own photos dropped into mock-ups of
what we would make for them (push notification, weekly specials post, homepage card, newsletter, welcome graphic,
promo video), then the full Restaurant Partner offer from build.py.
    python site/restaurant-partner/pitch.py <config.json>
Config lives OUTSIDE this public repo (3vl-private/pitches/<slug>.json):
  {"slug", "name", "short", "town", "special", "special_note", "push", "img": base url with hero/pizza/penne/burrata/owner/welcome/calamari/dining .webp}
Builds widget "3VL Pitch <name>" + hidden page /for-<slug> (noindex)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B
D = B.D

C = json.load(open(sys.argv[1], encoding="utf-8"))
I = C["img"]
D.NAME = "3VL Pitch " + C["name"]
D.SLUG = "for-" + C["slug"]
D.LIVE = False
D.TITLE = "%s x Three Village Local: Restaurant Partner" % C["name"]
D.DESC = "What Three Village Local would do for %s as one of only 5 Restaurant Partners." % C["name"]
D.FB_TITLE = "Made for %s" % C["name"]
D.FB_IMAGE = I + "hero.webp"


def section(src, cls):
    i = src.index('<section class="' + cls)
    j = src.index('</section>', i) + len('</section>')
    return src[i:j]


R = B.HTML


def inner(sec):
    return sec[sec.index(">") + 1:sec.rindex("</section>")]


math = inner(section(R, "tvs-sec tvr-math"))
plan = inner(section(R, "tvs-sec tvs-bundles"))
plan = plan[plan.index('<div class="tvs-cards'):]  # its "One plan, one price" header repeats the math header
DEAL = ('<section class="tvs-sec tvp-deal" id="tvs-bundles"><div class="tvp-dgrid"><div class="tvp-dmath">' + math +
        '</div><div class="tvp-dplan">' + plan + '</div></div></section>')
keep = "\n\n".join([section(R, "tvs-sec tvr-spots"), DEAL, section(R, "tvs-sec tvs-faq"), section(R, "tvs-sec tvs-book")])
keep = keep.replace('<p class="tvs-cname">Restaurant Partner</p>', '<p class="tvs-cname">Three Village Local Restaurant Partner</p>')
keep = keep.replace("<h2>Claim one of the 5 spots.</h2>", "<h2>Claim %s's spot.</h2>" % C["short"])

P = dict(C, I=I, CTA=B.cta, LEFT=B.left_txt)

ICON = "https://threevillagelocal-cloud.github.io/3vl-share/site/icon-192.png"
gal = "".join('<i style="background-image:url(%s%s.webp)"></i>' % (I, g)
              for g in C.get("gallery", []) + C.get("gallery_more", []))
hrs = "".join("<p><span>%s</span><b>%s</b></p>" % (a, b) for a, b in C.get("hours", []))
chips = "".join("<em>%s</em>" % x for x in C.get("extras", []))
VIP = '''
<section class="tvs-sec tvp-vip" id="tvp-vip">
  <div class="tvp-vwrap">
    <div class="tvp-vtxt tvs-up">
      <p class="tvs-eyebrow">&#11088; Premium local marketing, not a listing</p>
      <h2>Everything %(short)s gets as a Three Village Local Restaurant Partner.</h2>
      <p>Over $1,000 a month in marketing aimed at one audience: the neighbors who live minutes from %(short)s. The listing on the phone is the smallest part. Only 5 restaurants will ever have all of this.</p>
      <div class="tvp-pk3">
        <div class="tvp-pk"><span class="tvp-pi">&#128276;</span><div><em>Headliner</em><b>Monthly push notification</b><p>%(short)s on the lock screen of every Three Village Local mobile app user.</p></div></div>
        <div class="tvp-pk"><span class="tvp-pi">&#127869;&#65039;</span><div><em>Headliner</em><b>Weekly specials, everywhere</b><p>Our website, the mobile app, Instagram and Facebook, every single week.</p></div></div>
        <div class="tvp-pk"><span class="tvp-pi">&#127909;</span><div><em>Headliner</em><b>Your promo video</b><p>Filmed at %(short)s, edited by us, shared everywhere and yours to keep.</p></div></div>
      </div>
      <div class="tvp-pk6">
        <div class="tvp-pm"><span>&#11088;</span><b>VIP listing</b><p>Top of the Restaurants page, like the phone</p></div>
        <div class="tvp-pm"><span>&#128241;</span><b>Posts + a Reel monthly</b><p>Custom content on our Instagram and Facebook</p></div>
        <div class="tvp-pm"><span>&#127968;</span><b>Top spot in Eat &amp; Drink</b><p>Homepage and mobile app</p></div>
        <div class="tvp-pm"><span>&#128232;</span><b>Friday newsletter</b><p>Where locals plan the weekend</p></div>
        <div class="tvp-pm"><span>&#127881;</span><b>Events + seasonal guides</b><p>Wine nights, holidays, Restaurant Week</p></div>
        <div class="tvp-pm"><span>&#127991;&#65039;</span><b>Partner decal + review cards</b><p>Turn happy diners into Google reviews</p></div>
      </div>
      <a class="tvp-pcta" href="#tvs-book">Claim %(short)s's spot &rarr;</a>
    </div>
    <div class="tvp-vstage tvs-up" aria-hidden="true">
      <span class="tvp-chip tvp-c1">&#9733; Top of Restaurants</span>
      <span class="tvp-chip tvp-c2">&#127869;&#65039; This week's specials</span>
      <span class="tvp-chip tvp-c3">&#128222; Tap to call</span>
      <div class="tvp-vphone"><div class="tvp-notch"></div><div class="tvp-vscreen">
        <div class="tvp-url">&#128274; threevillagelocal.com/%(profile_path)s</div>
        <div class="tvp-pop"><img src="@@ICON@@" alt=""><div><p><b>Three Village Local</b><span>now</span></p><p><b>Weekly Specials at %(name)s</b></p><p>%(special)s and more this week. Tap to see them.</p></div></div>
        <div class="tvp-vscroll">
          <div class="tvp-vcover" style="background-image:url(%(I)shero.webp)"><span class="tvp-vrib">&#9733; VIP</span></div>
          <div class="tvp-vhead"><div class="tvp-vlogo"><img src="%(I)slogo.webp" alt=""></div>
            <p class="tvp-vname">%(name)s</p><p class="tvp-vcat">%(category)s &middot; %(town)s</p>
            <p class="tvp-vbadge">&#9733; Three Village Local VIP</p></div>
          <div class="tvp-vbtns"><span>&#128222;<b>Call</b></span><span>&#128205;<b>Directions</b></span><span>&#127760;<b>Website</b></span><span>&#128717;&#65039;<b>Order</b></span></div>
          <div class="tvp-vspec"><div style="background-image:url(%(I)spenne.webp)"></div><p><em>This week's special</em><b>%(special)s</b><span>%(special_note)s</span></p></div>
          <p class="tvp-vh">Popular dishes</p>
          <div class="tvp-vdish"><i style="background-image:url(%(I)sg-pizza.webp)"><b>Pizza</b></i><i style="background-image:url(%(I)sburrata.webp)"><b>Burrata</b></i><i style="background-image:url(%(I)sg-knots.webp)"><b>Garlic knots</b></i></div>
          <div class="tvp-vbig" style="background-image:url(%(I)sdining.webp)"><span>Inside the dining room</span></div>
          <p class="tvp-vh">Photos</p><div class="tvp-vgal">@@GAL@@</div>
          <div class="tvp-vvid" style="background-image:url(%(I)sowner.webp)"><span>&#9654;</span><b>Watch: a night at %(short)s</b></div>
          <p class="tvp-vh">About</p><p class="tvp-vabout">%(about)s</p>
          <div class="tvp-vchips">@@CHIPS@@</div>

          <p class="tvp-vh">Hours</p><div class="tvp-vhrs">@@HRS@@</div>
          <p class="tvp-vh">Location</p><div class="tvp-vmap"><span>&#128205;</span><b>%(address)s</b></div>
          <a class="tvp-vcall">&#128222; %(phone)s</a>
          <div class="tvp-vfoot"><img src="@@ICON@@" alt="">Also on the Three Village Local mobile app</div>
        </div>
      </div></div>
    </div>
  </div>
</section>
''' % P
VIP = VIP.replace("@@GAL@@", gal).replace("@@HRS@@", hrs).replace("@@CHIPS@@", chips).replace("@@ICON@@", ICON)
HTML = '''<div class="tvs tvs-nb tvs-rp tvp" id="tvs">

<section class="tvs-hero">
  <div class="tvs-hphoto" role="img" aria-label="%(name)s"></div>
  <div class="tvs-hfade"></div>
  <div class="tvs-hin tvs-up">
    <p class="tvs-kick"><span class="tvs-dot"></span>Private invitation for %(name)s</p>
    <h1>Only 5 restaurants<br><span>get this. One spot could be yours.</span></h1>
    <p class="tvs-sub">The <b>Three Village Local Restaurant Partner</b> program is not a listing. It is premium local marketing that puts %(short)s in front of your neighbors in Stony Brook, Setauket and Port Jefferson every single week: push alerts to their phones, your specials on every channel, and a promo video. Open to just 5 restaurants. When the spots are gone, the program closes.</p>
    <div class="tvp-meter"><div class="tvp-mdots">@@HDOTS@@</div><p><b>%(LEFT)s</b>First come, first served</p></div>
    <div class="tvs-ctas">
      <a class="tvs-btn tvs-blue" href="#tvs-book">Claim %(short)s's spot</a>
      <a class="tvs-btn tvs-ghost" href="#tvp-vip">See what you get</a>
    </div>
  </div>
</section>

@@VIP@@
<section class="tvs-sec tvp-yours" id="tvp-yours">
  <div class="tvs-head tvs-up">
    <p class="tvs-eyebrow">Built from your photos</p>
    <h2>Here is %(short)s in front of the neighbors.</h2>
    <p>Real examples of what goes out for you every week and every month.</p>
  </div>
  <div class="tvp-tiles">
    <div class="tvp-tile tvs-up">
      <div class="tvp-mock tvp-mpush" style="--s:.6" aria-hidden="true"><div class="tvp-phone">
        <div class="tvp-lock"><p class="tvp-time">5:42</p><p class="tvp-date">Friday</p>
          <div class="tvp-notif"><img src="https://threevillagelocal-cloud.github.io/3vl-share/site/icon-192.png" alt=""><div><p><b>Three Village Local</b><span>now</span></p><p><b>%(push_title)s</b></p><p>%(push)s</p></div><img class="tvp-nthumb" src="%(I)spizza.webp" alt=""></div>
        </div>
      </div></div>
      <p class="tvp-tag">Every month</p><h3>Push to every phone</h3><p>On the lock screen of every Three Village Local mobile app user.</p>
    </div>
    <div class="tvp-tile tvs-up">
      <div class="tvp-mock" style="--s:.62" aria-hidden="true"><div class="tvp-ig">
        <div class="tvp-igtop"><img src="https://threevillagelocal-cloud.github.io/3vl-share/site/icon-192.png" alt=""><b>threevillagelocal</b></div>
        <div class="tvp-igpic" style="background-image:url('%(I)spenne.webp')">
          <div class="tvp-igfade"></div>
          <div class="tvp-igt"><p class="tvp-ig1">THIS WEEK AT</p><p class="tvp-ig2">%(name_caps)s</p><p class="tvp-ig3">%(special)s</p><p class="tvp-ig4">&#128205; %(town)s</p></div>
        </div>
        <div class="tvp-igbar">&#9825; &nbsp;&#128172; &nbsp;&#10148;</div>
      </div></div>
      <p class="tvp-tag">Every week</p><h3>Your specials, everywhere</h3><p>Instagram, Facebook, our website and the mobile app's Eat &amp; Drink.</p>
    </div>
    <div class="tvp-tile tvs-up">
      <div class="tvp-mock tvp-mmid" style="--s:.64" aria-hidden="true"><div class="tvp-mail">
        <p class="tvp-mh">Three Village Weekly <span>Friday</span></p>
        <p class="tvp-mt">Where to eat this weekend</p>
        <div class="tvp-mi"><img src="%(I)scalamari.webp" alt=""><div><b>%(name)s</b><p>%(special_note)s</p><span>See this week's specials</span></div></div>
      </div></div>
      <p class="tvp-tag">Every Friday</p><h3>The weekly newsletter</h3><p>In the email locals read to plan their weekend.</p>
    </div>
    <div class="tvp-tile tvs-up">
      <div class="tvp-mock" style="--s:.92" aria-hidden="true"><div class="tvp-vid" style="background-image:url('%(I)sowner.webp')"><span>&#9654;</span><p>Your promo video</p></div></div>
      <p class="tvp-tag">Included</p><h3>Your promo video</h3><p>Filmed at %(short)s, edited by us, yours to keep.</p>
    </div>
  </div>
</section>

''' % dict(P, name_caps=C["name"].upper(), push_title=C.get("push_title", "Tonight at " + C["name"])) + keep + '''

<a class="tvs-newbiz tvs-up" href="/services"><span class="tvs-nbi">&#128188;</span><span><b>Want more than the Restaurant Partner plan?</b>See our full menu of business services: websites, social media marketing, video, drone and more.</span><em>Full services menu &rarr;</em></a>

<a class="tvs-sticky" href="#tvs-book">%s</a>
<script>(function(){function d(){var s=document.querySelector('.tvp-vscroll'),c=document.querySelector('.tvp-vscreen');if(s&&c)s.style.setProperty('--tvp-d',(c.clientHeight-s.scrollHeight)+'px')}window.addEventListener('load',d);setTimeout(d,1500)})();</script>
<script>(function(){var n=0,t=setInterval(function(){var s=document.querySelector('#tvs-form-slot select[name="bundle"]');if(s){s.value='rest_partner';clearInterval(t)}if(++n>40)clearInterval(t)},250)})();</script>
</div>''' % B.cta

HTML = HTML.replace("@@VIP@@", VIP).replace("@@HDOTS@@", B.dots)

# exclusivity band right under the hero: what only 5 restaurants get
BAND = '''<section class="tvs-sec tvp-band tvs-up" aria-label="What Restaurant Partners get">
  <p class="tvp-bh">Premium local marketing. Not just a listing.</p>
  <ul>
    <li><span>&#128276;</span><b>Monthly push alert</b>to every mobile app user</li>
    <li><span>&#127869;&#65039;</span><b>Weekly specials</b>website, mobile app, Instagram, Facebook</li>
    <li><span>&#127909;</span><b>Promo video</b>filmed at your restaurant</li>
    <li><span>&#11088;</span><b>VIP listing</b>top of the Restaurants page</li>
    <li><span>&#128232;</span><b>Friday newsletter</b>where locals plan the weekend</li>
  </ul>
</section>
'''
HTML = HTML.replace('<section class="tvs-sec tvp-vip"', BAND + '<section class="tvs-sec tvp-vip"', 1)
# move the "5 restaurants, that is it" box up, right after the VIP phone
spots = section(HTML, "tvs-sec tvr-spots")
HTML = HTML.replace(spots, "", 1).replace('<section class="tvs-sec tvp-yours"', spots + '\n<section class="tvs-sec tvp-yours"', 1)
# our reach, right after the perks (owner: "show them what we bring to the table")
ri = B.src.index('<div class="tvs-reach')
rj = B.src.index('</section>', ri)
reach = B.src[ri:rj].rstrip()
assert reach.endswith('</div>')
reach = reach.replace('<h3>The audience behind every post</h3>', '<h3>The audience behind every %s post</h3>' % C["short"])
REACH = """<section class="tvs-sec tvp-reach" id="tvp-reach">
  <div class="tvs-head tvs-up">
    <p class="tvs-eyebrow">Our reach</p>
    <h2>What we bring to the table.</h2>
    <p>Three Village Local is where neighbors in Stony Brook, Setauket and Port Jefferson go to decide what to do and where to eat. This is not ads to strangers miles away. As a Restaurant Partner, %s is in front of the people who can be at your table tonight, every week.</p>
  </div>
  %s
</section>
""" % (C["short"], reach)
HTML = HTML.replace('<section class="tvs-sec tvr-spots', REACH + '<section class="tvs-sec tvr-spots', 1)

CSS = '''
.tvp-vwrap{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:40px;align-items:start;max-width:1080px;margin:0 auto}
.tvp-vtxt h2{color:var(--navy);font-size:36px;line-height:1.1;margin:8px 0 12px}
.tvp-pk3{display:grid;gap:12px;margin:22px 0 12px}
.tvp-pk{position:relative;display:flex;gap:16px;align-items:flex-start;padding:20px 20px 20px 18px;border-radius:20px;background:linear-gradient(125deg,#0b2246 0%,#13336a 55%,#1d4f91 100%);box-shadow:0 18px 40px rgba(13,35,70,.22),inset 0 0 0 1px rgba(255,197,61,.35);overflow:hidden}
.tvp-pk:after{content:"";position:absolute;right:-60px;top:-60px;width:180px;height:180px;border-radius:50%;background:radial-gradient(circle,rgba(255,197,61,.22),transparent 70%)}
.tvp-pi{flex:0 0 auto;width:54px;height:54px;border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:26px;background:linear-gradient(135deg,#ffd76a,#e0a51b);box-shadow:0 8px 18px rgba(224,165,27,.35)}
.tvp-pk div{flex:1;min-width:0;padding-right:96px}
.tvp-pk em{display:inline-block;font-style:normal;font-size:10.5px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:#ffc53d}
.tvp-pk b{display:block;color:#fff;font-size:19px;margin:2px 0 4px}
.tvp-pk p{margin:0!important;color:#cfe0f7!important;font-size:14.5px!important;line-height:1.45}
.tvp-pk i{position:absolute;right:16px;top:18px;font-style:normal;font-size:12px;font-weight:800;color:#2a1c00;background:#ffc53d;border-radius:999px;padding:4px 10px;z-index:1}
.tvp-pk6{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.tvp-pm{position:relative;background:#fff;border:1px solid var(--line);border-radius:16px;padding:14px 14px 14px 58px;box-shadow:0 8px 22px rgba(13,35,70,.06);transition:transform .2s,box-shadow .2s}
.tvp-pm:hover{transform:translateY(-2px);box-shadow:0 14px 30px rgba(13,35,70,.12)}
.tvp-pm span{position:absolute;left:12px;top:14px;width:36px;height:36px;border-radius:11px;background:#eef4fd;display:flex;align-items:center;justify-content:center;font-size:18px}
.tvp-pm b{display:block;color:var(--navy);font-size:15px;line-height:1.25}
.tvp-pm p{margin:2px 0 6px!important;color:var(--mut)!important;font-size:13px!important;line-height:1.35}
.tvp-pm i{font-style:normal;font-size:11.5px;font-weight:800;color:#966e22}
.tvp-pcta{display:inline-block;margin-top:18px;background:var(--blue);color:#fff!important;font-weight:800;border-radius:999px;padding:14px 26px;box-shadow:0 12px 26px rgba(29,95,191,.3);text-decoration:none!important}
.tvp-vtxt>p{color:var(--mut);font-size:17px}
.tvp-vlist{list-style:none;margin:22px 0 0;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:12px}
.tvp-vlist li{background:#fff;border:1px solid var(--line);border-radius:16px;padding:14px 16px;color:var(--mut);font-size:14px}
.tvp-vlist b{display:block;color:var(--navy);font-size:15.5px;margin-bottom:2px}
.tvp-vstage{position:sticky;top:70px;display:flex;justify-content:center;padding:30px 0;perspective:1400px}
.tvp-vstage:before{content:"";position:absolute;width:420px;height:420px;max-width:100%;border-radius:50%;background:radial-gradient(circle,rgba(255,197,61,.45),rgba(29,95,191,.12) 55%,transparent 70%);top:50%;left:50%;transform:translate(-50%,-50%);filter:blur(10px)}
.tvp-vphone{position:relative;width:320px;height:650px;border-radius:52px;background:linear-gradient(145deg,#2a3242,#0b1018);padding:12px;box-shadow:0 50px 90px rgba(13,35,70,.35),inset 0 0 0 2px #3a4456;transform:rotateY(-12deg) rotateX(4deg);transition:transform .6s}
.tvp-vstage:hover .tvp-vphone{transform:rotateY(0) rotateX(0)}
.tvp-notch{position:absolute;top:22px;left:50%;transform:translateX(-50%);width:96px;height:26px;border-radius:20px;background:#05080d;z-index:3}
.tvp-vscreen{position:relative;height:100%;border-radius:42px;overflow:hidden;background:#f5f7fb}
.tvp-url{position:absolute;top:0;left:0;right:0;z-index:2;padding:56px 14px 8px;background:rgba(245,247,251,.95);font-size:11px;color:#556;text-align:center;border-bottom:1px solid #e3e8ef;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.tvp-vscroll{padding-top:84px;animation:tvpScroll 48s linear infinite}
.tvp-vstage:hover .tvp-vscroll{animation-play-state:paused}
@keyframes tvpScroll{0%,9%{transform:translateY(0);opacity:1}88%,95%{transform:translateY(var(--tvp-d,-1800px));opacity:1}97%{transform:translateY(var(--tvp-d,-1800px));opacity:0}98%{transform:translateY(0);opacity:0}100%{transform:translateY(0);opacity:1}}
.tvp-vdish{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;padding:0 12px}
.tvp-vdish i{position:relative;aspect-ratio:3/4;border-radius:12px;background:center/cover;overflow:hidden}
.tvp-vdish b{position:absolute;left:0;right:0;bottom:0;padding:16px 6px 6px;background:linear-gradient(180deg,transparent,rgba(0,0,0,.7));color:#fff;font-size:10.5px;font-style:normal}
.tvp-vbig{position:relative;margin:12px 12px 0;height:150px;border-radius:14px;background:center/cover}
.tvp-vbig span{position:absolute;left:10px;bottom:10px;background:rgba(255,255,255,.92);color:#13233a;font-weight:800;font-size:11px;padding:4px 10px;border-radius:999px}
.tvp-vvid{position:relative;margin:12px 12px 0;height:170px;border-radius:14px;background:center/cover;overflow:hidden}
.tvp-vvid span{position:absolute;left:50%;top:42%;transform:translate(-50%,-50%);width:46px;height:46px;border-radius:50%;background:rgba(255,255,255,.92);color:#1d5fbf;font-size:17px;display:flex;align-items:center;justify-content:center;padding-left:3px}
.tvp-vvid b{position:absolute;left:0;right:0;bottom:0;padding:22px 10px 9px;background:linear-gradient(180deg,transparent,rgba(0,0,0,.75));color:#fff;font-size:12px;text-align:center}
.tvp-vduo{display:grid;grid-template-columns:1fr 1fr;gap:6px;padding:12px 12px 0}
.tvp-vduo i{aspect-ratio:4/5;border-radius:12px;background:center/cover}
.tvp-meter{display:flex;align-items:center;gap:14px;margin:0 0 24px;padding:12px 16px;border-radius:16px;background:#0f2a52;width:max-content;max-width:100%;box-sizing:border-box}
.tvp-mdots{display:flex;gap:7px}
.tvp-mdots i{width:20px;height:20px;border-radius:50%;background:var(--gold);box-shadow:0 0 0 3px rgba(255,197,61,.25);animation:tvpDot 2.4s ease-in-out infinite}
.tvp-mdots i:nth-child(2){animation-delay:.2s}.tvp-mdots i:nth-child(3){animation-delay:.4s}.tvp-mdots i:nth-child(4){animation-delay:.6s}.tvp-mdots i:nth-child(5){animation-delay:.8s}
.tvp-mdots i.tvr-taken{background:rgba(255,255,255,.2);box-shadow:none;animation:none}
@keyframes tvpDot{50%{box-shadow:0 0 0 6px rgba(255,197,61,.12)}}
.tvp-meter p{margin:0!important;color:#cfe0f7!important;font-size:13px!important;line-height:1.25}
.tvp-meter b{display:block;color:#fff;font-size:17px}
.tvp .tvs-sub b{color:var(--navy)}
.tvp-band{max-width:1080px;margin-left:auto;margin-right:auto}
.tvp-bh{text-align:center;margin:0 0 14px!important;font-weight:800;color:var(--navy)!important;font-size:15px!important;letter-spacing:.1em;text-transform:uppercase}
.tvp-band ul{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(5,1fr);gap:12px}
.tvp-band li{background:#fff;border:1px solid var(--line);border-radius:18px;padding:16px 14px;color:var(--mut);font-size:13.5px;line-height:1.35}
.tvp-band li:nth-child(-n+3){background:linear-gradient(135deg,#0f2a52,#1d4f91);border:0;color:#cfe0f7}
.tvp-band li:nth-child(-n+3) b{color:#fff}
.tvp-band span{display:block;font-size:24px;margin-bottom:6px}
.tvp-band b{display:block;color:var(--navy);font-size:15.5px;margin-bottom:2px}
@media (max-width:900px){.tvp-band ul{grid-template-columns:repeat(2,1fr)}.tvp-band li:last-child{grid-column:1/-1}}
@media (max-width:520px){.tvp-meter{gap:10px;padding:10px 12px}.tvp-mdots i{width:16px;height:16px}.tvp-meter b{font-size:15px}}
.tvp-pop{position:absolute;z-index:5;top:48px;left:8px;right:8px;display:flex;gap:9px;align-items:flex-start;background:rgba(250,250,252,.97);border-radius:18px;padding:10px 11px;box-shadow:0 12px 30px rgba(0,0,0,.28);opacity:0;transform:translateY(-120%);animation:tvpPop 13s ease-in-out 2s infinite}
.tvp-pop img{width:32px;height:32px;border-radius:8px;flex:0 0 auto;margin:0!important}
.tvp-pop div{flex:1;min-width:0}
.tvp-pop p{margin:0!important;font-size:11.5px!important;line-height:1.3;color:#111!important}
.tvp-pop p:first-child{display:flex;justify-content:space-between;color:#666!important;font-size:10.5px!important}
.tvp-pop p:first-child b{color:#666;font-weight:600}
.tvp-pop p:nth-child(2) b{font-size:13px}
@keyframes tvpPop{0%{opacity:0;transform:translateY(-120%)}5%,38%{opacity:1;transform:translateY(0)}45%,100%{opacity:0;transform:translateY(-120%)}}
.tvp-vcover{position:relative;height:170px;background:center/cover}
.tvp-vrib{position:absolute;right:12px;top:12px;background:linear-gradient(135deg,#ffd76a,#e0a51b);color:#3a2700;font-weight:900;font-size:12px;padding:5px 12px;border-radius:999px;box-shadow:0 4px 12px rgba(0,0,0,.25)}
.tvp-vhead{text-align:center;padding:0 16px;margin-top:-46px;position:relative}
.tvp-vlogo{width:92px;height:92px;margin:0 auto;border-radius:50%;background:#fff;padding:6px;box-shadow:0 0 0 4px #ffc53d,0 0 24px rgba(255,197,61,.8),0 8px 20px rgba(0,0,0,.2);animation:tvpGlow 2.4s ease-in-out infinite}
.tvp-vlogo img{width:100%;height:100%;object-fit:contain;border-radius:50%;margin:0!important}
@keyframes tvpGlow{50%{box-shadow:0 0 0 4px #ffc53d,0 0 38px rgba(255,197,61,1),0 8px 20px rgba(0,0,0,.2)}}
.tvp-vname{margin:10px 0 0!important;font-weight:900;font-size:22px!important;color:#13233a!important}
.tvp-vcat{margin:2px 0 8px!important;color:#5d6876!important;font-size:12.5px!important}
.tvp-vbadge{display:inline-block;margin:0!important;background:#13233a;color:#ffc53d!important;font-weight:800;font-size:11.5px!important;padding:5px 12px;border-radius:999px}
.tvp-vbtns{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;padding:14px 12px 4px}
.tvp-vbtns span{background:#fff;border:1px solid #e3e8ef;border-radius:12px;text-align:center;padding:8px 2px;font-size:17px}
.tvp-vbtns b{display:block;font-size:10.5px;color:#1d5fbf;margin-top:2px}
.tvp-vspec{display:flex;gap:10px;margin:12px;padding:10px;border-radius:14px;background:linear-gradient(135deg,#fff7e0,#fff);border:1px solid #f3dc9a}
.tvp-vspec div{width:72px;height:72px;border-radius:10px;background:center/cover;flex:0 0 auto}
.tvp-vspec p{margin:0!important;font-size:12px!important;color:#333!important;line-height:1.35}
.tvp-vspec em{display:block;font-style:normal;color:#b07a00;font-weight:800;font-size:10.5px;text-transform:uppercase;letter-spacing:.06em}
.tvp-vspec b{display:block;color:#13233a;font-size:15px}
.tvp-vh{margin:16px 14px 8px!important;font-weight:800;color:#13233a!important;font-size:14px!important}
.tvp-vgal{display:grid;grid-template-columns:repeat(3,1fr);gap:4px;padding:0 12px}
.tvp-vgal i{aspect-ratio:1;border-radius:8px;background:center/cover}
.tvp-vabout{margin:0 14px!important;font-size:12.5px!important;color:#444!important;line-height:1.5}
.tvp-vchips{display:flex;flex-wrap:wrap;gap:6px;padding:10px 14px 0}
.tvp-vchips em{font-style:normal;font-size:11px;font-weight:700;color:#1d5fbf;background:#e8f0fb;border-radius:999px;padding:4px 10px}
.tvp-vhrs{margin:0 14px;background:#fff;border:1px solid #e3e8ef;border-radius:12px;padding:6px 12px}
.tvp-vhrs p{display:flex;justify-content:space-between;margin:0!important;padding:5px 0;font-size:12px!important;color:#444!important;border-bottom:1px solid #f0f2f6}
.tvp-vhrs p:last-child{border:0}
.tvp-vmap{position:relative;margin:0 12px;height:120px;border-radius:12px;background:linear-gradient(135deg,#dfe9d8 25%,#cfdfc6 25%,#cfdfc6 50%,#dfe9d8 50%,#dfe9d8 75%,#cfdfc6 75%);background-size:40px 40px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px}
.tvp-vmap span{font-size:30px}
.tvp-vmap b{background:#fff;font-size:11px;color:#13233a;padding:4px 10px;border-radius:999px;box-shadow:0 2px 8px rgba(0,0,0,.15)}
.tvp-vcall{display:block;margin:14px 12px 0;text-align:center;background:#1d5fbf;color:#fff!important;font-weight:800;font-size:14px;border-radius:999px;padding:12px}
.tvp-vfoot{display:flex;align-items:center;justify-content:center;gap:8px;padding:16px 12px 30px;font-size:11px;color:#5d6876}
.tvp-vfoot img{width:22px;height:22px;border-radius:6px;margin:0!important}
.tvp-chip{position:absolute;z-index:4;background:#fff;border-radius:999px;padding:10px 16px;font-weight:800;font-size:14px;color:#13233a;box-shadow:0 14px 30px rgba(13,35,70,.18);animation:tvpFloat 5s ease-in-out infinite;white-space:nowrap}
.tvp-c1{top:70px;left:0}.tvp-c2{top:46%;right:-6px;animation-delay:1.2s}.tvp-c3{bottom:80px;left:14px;animation-delay:2.4s}
@keyframes tvpFloat{50%{transform:translateY(-10px)}}
@media (max-width:900px){.tvp-vwrap{grid-template-columns:1fr}.tvp-vtxt{text-align:center}.tvp-pk3,.tvp-pk6{text-align:left}.tvp-vstage{position:relative;top:0;order:-1}}
@media (max-width:520px){.tvp-vtxt h2{font-size:28px}.tvp-pk6{grid-template-columns:1fr}.tvp-pk{padding:16px 14px;gap:12px}.tvp-pk div{padding-right:0}.tvp-pk{flex-wrap:wrap}.tvp-pk div{flex:1 1 calc(100% - 70px)}.tvp-pk i{position:static;display:inline-block;margin:0 0 0 58px}.tvp-pk:after{display:none}.tvp-pi{width:46px;height:46px;font-size:22px}.tvp-pk b{font-size:17px}.tvp-vphone{width:290px;height:600px;transform:none}.tvp-chip{font-size:12px;padding:8px 12px}.tvp-c1{left:-4px}.tvp-c2,.tvp-c3{display:none}}
.tvp .tvs-hphoto{background-image:url('@@I@@hero.webp')!important;background-position:50% 40%}
.tvp-row{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:48px;align-items:center;max-width:1000px;margin:0 auto 64px}
.tvp-flip>*:first-child{order:2}
.tvp-txt h3{color:var(--navy);font-size:28px;margin:6px 0 10px}
.tvp-txt p{color:var(--mut);font-size:16.5px}
.tvp-tag{display:inline-block;margin:0!important;padding:5px 12px;border-radius:999px;background:#eef4fd;color:var(--blue)!important;font-weight:800;font-size:13px!important}
.tvp-phone{justify-self:center;width:290px;height:560px;border-radius:44px;background:#0b1424;padding:12px;box-shadow:0 30px 60px rgba(13,35,70,.3)}
.tvp-lock{height:100%;border-radius:34px;background:linear-gradient(160deg,#1d4f91,#0f2a52 60%,#3a2a1a);padding:44px 12px 0;text-align:center;color:#fff}
.tvp-time{font-size:64px;font-weight:300;margin:0!important;line-height:1;color:#fff!important}
.tvp-date{margin:6px 0 36px!important;color:#dbe7f7!important;font-size:16px!important}
.tvp-notif{display:flex;gap:10px;align-items:flex-start;text-align:left;background:rgba(255,255,255,.88);color:#111;border-radius:20px;padding:12px;animation:tvpIn 1s .3s both}
.tvp-notif>img{width:34px;height:34px;border-radius:8px;flex:0 0 auto}
.tvp-notif .tvp-nthumb{width:44px;height:44px;border-radius:8px;object-fit:cover}
.tvp-notif div{flex:1;min-width:0}
.tvp-notif p{margin:0!important;font-size:13px!important;line-height:1.3;color:#111!important}
.tvp-notif p:first-child{display:flex;justify-content:space-between;color:#555!important;font-size:12px!important;margin-bottom:2px!important}
.tvp-notif p:first-child b{color:#555}
@keyframes tvpIn{from{opacity:0;transform:translateY(-14px)}to{opacity:1;transform:none}}
.tvp-ig{justify-self:center;width:340px;background:#fff;border:1px solid var(--line);border-radius:18px;overflow:hidden;box-shadow:0 20px 44px rgba(13,35,70,.14)}
.tvp-igtop{display:flex;align-items:center;gap:8px;padding:10px 12px;font-size:14px}
.tvp-igtop{justify-content:flex-start;text-align:left}.tvp-igtop img{width:28px;height:28px;border-radius:50%;margin:0!important;display:inline-block}
.tvp-igpic{position:relative;aspect-ratio:4/5;background:center/cover}
.tvp-igfade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(12,14,22,0) 40%,rgba(12,14,22,.9) 100%)}
.tvp-igt{position:absolute;left:18px;right:18px;bottom:18px;color:#fff}
.tvp-igt p{margin:0!important;line-height:1.05}
.tvp-ig1{color:#ffc53d!important;font-weight:800;letter-spacing:.08em;font-size:14px!important}
.tvp-ig2{color:#fff8ea!important;font-weight:900;font-size:34px!important;margin:4px 0!important}
.tvp-ig3{color:#fff!important;font-size:18px!important;font-weight:700}
.tvp-ig4{display:inline-block;margin-top:10px!important;background:#ffc53d;color:#2a1c12!important;font-weight:800;font-size:12.5px!important;padding:5px 12px;border-radius:999px}
.tvp-igbar{padding:10px 14px;font-size:18px;color:#222}
.tvp-card{justify-self:center;width:320px;background:#fff;border:1px solid var(--line);border-radius:20px;padding:16px;box-shadow:0 20px 44px rgba(13,35,70,.14)}
.tvp-ch{margin:0 0 10px!important;font-weight:800;color:var(--navy)!important;display:flex;justify-content:space-between}
.tvp-ch span{font-size:12px;background:#de302c;color:#fff;border-radius:999px;padding:3px 10px}
.tvp-cimg{position:relative;aspect-ratio:4/3;border-radius:14px;background:center/cover}
.tvp-cimg span{position:absolute;left:10px;top:10px;background:#ffc53d;color:#2a1c12;font-weight:800;font-size:12px;border-radius:999px;padding:4px 10px}
.tvp-cn{margin:12px 0 2px!important;font-weight:800;color:var(--navy)!important;font-size:18px!important}
.tvp-cs{margin:0!important;color:#333!important;font-size:14.5px!important}
.tvp-ct{margin:8px 0 0!important;color:var(--blue)!important;font-weight:700;font-size:13.5px!important}
.tvp-mail{justify-self:center;width:360px;background:#fff;border:1px solid var(--line);border-radius:18px;padding:18px;box-shadow:0 20px 44px rgba(13,35,70,.14)}
.tvp-mh{margin:0!important;display:flex;justify-content:space-between;font-weight:800;color:var(--navy)!important;border-bottom:3px solid #ffc53d;padding-bottom:8px}
.tvp-mh span{color:var(--mut);font-weight:600;font-size:13px}
.tvp-mt{margin:12px 0!important;font-weight:800;color:var(--navy)!important;font-size:19px!important}
.tvp-mi{display:flex;gap:12px}
.tvp-mi img{width:96px;height:120px;object-fit:cover;border-radius:12px}
.tvp-mi b{color:var(--navy)}
.tvp-mi p{margin:4px 0 8px!important;font-size:14px!important;color:#333!important}
.tvp-mi span{display:inline-block;background:var(--blue);color:#fff;font-weight:700;font-size:12.5px;border-radius:999px;padding:6px 12px}
.tvp-two{justify-self:center;display:flex;gap:14px;align-items:center}
.tvp-two>img{width:200px;border-radius:14px;box-shadow:0 20px 44px rgba(13,35,70,.18)}
.tvp-vid{position:relative;width:200px;aspect-ratio:9/16;border-radius:18px;background:center/cover;box-shadow:0 20px 44px rgba(13,35,70,.18);overflow:hidden}
.tvp-vid span{position:absolute;left:50%;top:45%;transform:translate(-50%,-50%);width:58px;height:58px;border-radius:50%;background:rgba(255,255,255,.92);color:var(--blue);font-size:22px;display:flex;align-items:center;justify-content:center;padding-left:4px}
.tvp-vid p{position:absolute;left:0;right:0;bottom:0;margin:0!important;padding:30px 10px 12px;background:linear-gradient(180deg,transparent,rgba(0,0,0,.75));color:#fff!important;font-weight:800;text-align:center;font-size:14px!important}
.tvp-tiles{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;max-width:1120px;margin:0 auto}
.tvp-tile{background:#fff;border:1px solid var(--line);border-radius:22px;padding:16px 16px 18px;text-align:center;box-shadow:0 14px 34px rgba(13,35,70,.07)}
.tvp-mock{--k:1;position:relative;height:340px;border-radius:16px;background:linear-gradient(160deg,#eef4fd,#f8fafc);overflow:hidden;display:flex;justify-content:center;align-items:flex-start;padding-top:12px;margin-bottom:14px;box-sizing:border-box}
.tvp-mock>*{flex:0 0 auto;transform:scale(calc(var(--s) * var(--k)));transform-origin:top center;margin:0!important}
.tvp-mock .tvp-ig{width:340px!important}.tvp-mock .tvp-mail{width:360px!important}.tvp-mock .tvp-phone{width:290px!important;height:560px!important}
.tvp-mpush{overflow:visible;z-index:2;clip-path:inset(-200px -200px 0 -200px)}
.tvp-mpush .tvp-lock{position:relative}
.tvp-mpush .tvp-notif{position:relative;z-index:3;transform-origin:50% 50%;animation:tvpPush 5.5s cubic-bezier(.2,.9,.25,1.2) .4s infinite both;will-change:transform}
.tvp-mpush .tvp-notif:after{content:"";position:absolute;inset:-3px;border-radius:22px;box-shadow:0 0 0 0 rgba(255,197,61,.9);animation:tvpRing 5.5s ease-out .4s infinite;pointer-events:none}
@keyframes tvpPush{0%{opacity:0;transform:translateY(-70px) scale(.85)}10%{opacity:1;transform:translateY(0) scale(1)}22%,62%{transform:translateY(26px) scale(1.32) rotate(-2deg);box-shadow:0 34px 60px rgba(0,0,0,.45),0 0 0 2px rgba(255,197,61,.9);background:#fff}74%,90%{opacity:1;transform:translateY(0) scale(1);box-shadow:0 6px 16px rgba(0,0,0,.2)}100%{opacity:0;transform:translateY(-20px) scale(.95)}}
@keyframes tvpRing{0%,18%{box-shadow:0 0 0 0 rgba(255,197,61,.9)}40%{box-shadow:0 0 0 26px rgba(255,197,61,0)}100%{box-shadow:0 0 0 0 rgba(255,197,61,0)}}
@media (prefers-reduced-motion:reduce){.tvp-mpush .tvp-notif,.tvp-mpush .tvp-notif:after{animation:none}}
.tvp-mmid{align-items:center;padding-top:0}.tvp-mmid>*{transform-origin:center}
.tvp-tile h3{color:var(--navy);font-size:19px;margin:8px 0 4px}
.tvp-tile>p:not(.tvp-tag){margin:0!important;color:var(--mut);font-size:14px!important;line-height:1.45}
.tvp-deal .tvp-dgrid{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:28px;align-items:start;max-width:1120px;margin:0 auto}
.tvp-deal .tvs-head{text-align:left;margin-left:0;max-width:none}
.tvp-deal .tvr-stack{max-width:none;margin:0}
.tvp-deal .tvp-dplan{position:sticky;top:80px}
.tvp-deal .tvs-cards{display:block!important;margin:0}
.tvp-deal .tvs-card{max-width:none}
@media (max-width:980px){.tvp-tiles{grid-template-columns:repeat(2,minmax(0,1fr))}.tvp-deal .tvp-dgrid{grid-template-columns:1fr}.tvp-deal .tvp-dplan{position:static}.tvp-deal .tvs-head{text-align:center}}
@media (max-width:520px){.tvp-tiles{gap:10px}.tvp-tile{padding:10px 10px 14px;border-radius:18px}.tvp-mock{--k:.72;height:250px;margin-bottom:10px}.tvp-mmid{--k:.6}.tvp-tile h3{font-size:16px}.tvp-tile>p:not(.tvp-tag){font-size:13px!important}}
@media (max-width:820px){.tvp-row{grid-template-columns:1fr;gap:22px;margin-bottom:48px}.tvp-flip>*:first-child{order:0}.tvp-txt{text-align:center}}
@media (max-width:420px){.tvp-ig,.tvp-mail{width:100%}.tvp-two>img,.tvp-vid{width:150px}.tvp-phone{width:290px;height:540px}.tvp-lock{padding:40px 8px 0}.tvp-notif .tvp-nthumb{display:none}}
'''.replace("@@I@@", I)

_rd = B._rd


def rd(f):
    if f == "page.html":
        assert "\\" not in HTML
        return HTML
    s = _rd(f)
    return s + B.CSS + CSS if f == "page.css" else s


D.rd = rd
D.main()
