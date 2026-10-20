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
keep = "\n\n".join(section(R, c) for c in ("tvs-sec tvr-spots", "tvs-sec tvs-need", "tvs-sec tvr-math", "tvs-sec tvs-bundles",
                                            "tvs-sec tvs-faq", "tvs-sec tvs-book"))
keep = keep.replace("<h2>Claim one of the 5 spots.</h2>", "<h2>Claim %s's spot.</h2>" % C["short"])

P = dict(C, I=I, CTA=B.cta, LEFT=B.left_txt)
HTML = '''<div class="tvs tvs-nb tvs-rp tvp" id="tvs">

<section class="tvs-hero">
  <div class="tvs-hphoto" role="img" aria-label="%(name)s"></div>
  <div class="tvs-hfade"></div>
  <div class="tvs-hin tvs-up">
    <p class="tvs-kick"><span class="tvs-dot"></span>Made for %(name)s</p>
    <h1>%(short)s, this is what<br><span>the whole town would see.</span></h1>
    <p class="tvs-sub">We took your own photos and showed what Three Village Local would do for %(short)s every week as one of only 5 Restaurant Partners in Stony Brook, Setauket and Port Jefferson.</p>
    <div class="tvs-ctas">
      <a class="tvs-btn tvs-blue" href="#tvp-yours">See it with your name on it</a>
      <a class="tvs-btn tvs-ghost" href="#tvs-book">%(CTA)s</a>
    </div>
    <ul class="tvs-trust">
      <li><b>5 spots</b>that is it</li>
      <li><b>Push alerts</b>to every mobile app user</li>
      <li><b>Promo video</b>included</li>
    </ul>
  </div>
</section>

<section class="tvs-sec tvp-yours" id="tvp-yours">
  <div class="tvs-head tvs-up">
    <p class="tvs-eyebrow">Your restaurant, our reach</p>
    <h2>Here is %(short)s on Three Village Local.</h2>
    <p>Real examples built from your photos. As a Restaurant Partner, this is what goes out for you every week and every month.</p>
  </div>

  <div class="tvp-row tvs-up">
    <div class="tvp-phone" aria-hidden="true">
      <div class="tvp-lock"><p class="tvp-time">5:42</p><p class="tvp-date">Friday</p>
        <div class="tvp-notif"><img src="https://threevillagelocal-cloud.github.io/3vl-share/site/icon-192.png" alt=""><div><p><b>Three Village Local</b><span>now</span></p><p><b>%(push_title)s</b></p><p>%(push)s</p></div><img class="tvp-nthumb" src="%(I)spizza.webp" alt=""></div>
      </div>
    </div>
    <div class="tvp-txt">
      <p class="tvp-tag">&#11088; Every month</p>
      <h3>Your push notification</h3>
      <p>Once a month, %(short)s lands on the lock screen of every Three Village Local mobile app user, right when they are deciding where to eat.</p>
    </div>
  </div>

  <div class="tvp-row tvp-flip tvs-up">
    <div class="tvp-ig" aria-hidden="true">
      <div class="tvp-igtop"><img src="https://threevillagelocal-cloud.github.io/3vl-share/site/icon-192.png" alt=""><b>threevillagelocal</b></div>
      <div class="tvp-igpic" style="background-image:url('%(I)spenne.webp')">
        <div class="tvp-igfade"></div>
        <div class="tvp-igt"><p class="tvp-ig1">THIS WEEK AT</p><p class="tvp-ig2">%(name_caps)s</p><p class="tvp-ig3">%(special)s</p><p class="tvp-ig4">&#128205; %(town)s</p></div>
      </div>
      <div class="tvp-igbar">&#9825; &nbsp;&#128172; &nbsp;&#10148;</div>
    </div>
    <div class="tvp-txt">
      <p class="tvp-tag">&#11088; Every week</p>
      <h3>Your weekly specials, everywhere</h3>
      <p>Text us your specials and we turn them into posts like this for our Instagram and Facebook, plus the website, the mobile app and the Friday newsletter.</p>
    </div>
  </div>

  <div class="tvp-row tvs-up">
    <div class="tvp-card" aria-hidden="true">
      <p class="tvp-ch">&#127869;&#65039; Eat &amp; Drink <span>Today</span></p>
      <div class="tvp-cimg" style="background-image:url('%(I)sburrata.webp')"><span>Partner</span></div>
      <p class="tvp-cn">%(name)s</p>
      <p class="tvp-cs">%(special_note)s</p>
      <p class="tvp-ct">%(town)s &middot; See specials &rarr;</p>
    </div>
    <div class="tvp-txt">
      <p class="tvp-tag">Homepage + mobile app</p>
      <h3>A regular top spot in Eat &amp; Drink</h3>
      <p>The first thing neighbors see when they open our homepage or the mobile app to figure out dinner.</p>
    </div>
  </div>

  <div class="tvp-row tvp-flip tvs-up">
    <div class="tvp-mail" aria-hidden="true">
      <p class="tvp-mh">Three Village Weekly <span>Friday</span></p>
      <p class="tvp-mt">Where to eat this weekend</p>
      <div class="tvp-mi"><img src="%(I)scalamari.webp" alt=""><div><b>%(name)s</b><p>%(special_note)s</p><span>See this week's specials</span></div></div>
    </div>
    <div class="tvp-txt">
      <p class="tvp-tag">Every Friday</p>
      <h3>In the weekly newsletter</h3>
      <p>Your specials in the email locals read to plan their weekend.</p>
    </div>
  </div>

  <div class="tvp-row tvs-up">
    <div class="tvp-two" aria-hidden="true">
      <img src="%(I)swelcome.webp" alt="">
      <div class="tvp-vid" style="background-image:url('%(I)sowner.webp')"><span>&#9654;</span><p>Your promo video</p></div>
    </div>
    <div class="tvp-txt">
      <p class="tvp-tag">&#11088; Included</p>
      <h3>Your welcome post and promo video</h3>
      <p>A welcome announcement to the whole town, and a promo video filmed at %(short)s, edited by us and yours to keep.</p>
    </div>
  </div>
</section>

''' % dict(P, name_caps=C["name"].upper(), push_title=C.get("push_title", "Tonight at " + C["name"])) + keep + '''

<a class="tvs-newbiz tvs-up" href="/services"><span class="tvs-nbi">&#128188;</span><span><b>Want more than the Restaurant Partner plan?</b>See our full menu of business services: websites, social media marketing, video, drone and more.</span><em>Full services menu &rarr;</em></a>

<a class="tvs-sticky" href="#tvs-book">%s</a>
<script>(function(){var n=0,t=setInterval(function(){var s=document.querySelector('#tvs-form-slot select[name="bundle"]');if(s){s.value='rest_partner';clearInterval(t)}if(++n>40)clearInterval(t)},250)})();</script>
</div>''' % B.cta

CSS = '''
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
