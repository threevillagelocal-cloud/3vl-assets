"""Restaurant Partner page (owner 10/20/2026): all-in-one restaurant promotion, HARD LIMIT of 5 restaurants.
Same look as /services (shares page.css / page.js and its reach, showcase and booking sections).
    python site/restaurant-partner/build.py            -> widget "3VL Page Restaurant Partner" + hidden preview /preview-restaurants
    python site/restaurant-partner/build.py --live     -> /restaurants (indexable)
When a restaurant signs, raise TAKEN and rebuild. At 5 the page switches to "all spots taken, join the waitlist"."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SV = os.path.join(HERE, "..", "services-page")
sys.path.insert(0, SV)
import deploy as D

TAKEN = 0          # signed Restaurant Partners (max 5)
SPOTS = 5
PRICE = 399        # per month, 6-month partnership
IMG = "https://threevillagelocal-cloud.github.io/3vl-share/site/restaurants/"

D.NAME = "3VL Page Restaurant Partner"
D.SLUG = "restaurants" if D.LIVE else "preview-restaurants"
D.TITLE = "Restaurant Partner: Promotion for Stony Brook, Setauket & Port Jefferson Restaurants | Three Village Local"
D.DESC = ("The all-in-one restaurant promotion platform for Stony Brook, Setauket and Port Jefferson: VIP listing, weekly specials, "
          "social media, homepage, mobile app, newsletter and a promo video. Only 5 restaurants.")

D.FB_TITLE = "Where should we eat tonight? Make the answer you."
D.FB_IMAGE = IMG + "hero-1080.webp"

LEFT = max(0, SPOTS - TAKEN)
FULL = LEFT == 0
dots = "".join('<i class="%s"></i>' % ("tvr-taken" if i < TAKEN else "") for i in range(SPOTS))
left_txt = "All 5 spots are taken" if FULL else ("%d of %d spots left" % (LEFT, SPOTS))
cta = "Join the waitlist" if FULL else "Claim a spot"


def section(src, cls):
    i = src.index('<section class="' + cls)
    j = src.index('</section>', i) + len('</section>')
    return src[i:j]


src = open(os.path.join(SV, "page.html"), encoding="utf-8").read()

HTML = '''<div class="tvs tvs-nb tvs-rp" id="tvs">

<section class="tvs-hero">
  <div class="tvs-hphoto" role="img" aria-label="Seafood paella in a pan on a wooden table"></div>
  <div class="tvs-hfade"></div>
  <div class="tvs-hin tvs-up">
    <p class="tvs-kick"><span class="tvs-dot"></span>Restaurant Partner &middot; only 5 restaurants</p>
    <h1>Where should we eat tonight?<br><span>Make the answer you.</span></h1>
    <p class="tvs-sub">The all-in-one restaurant promotion platform for Stony Brook, Setauket and Port Jefferson. Your specials, your food and your story in front of the whole town, every week.</p>
    <div class="tvs-ctas">
      <a class="tvs-btn tvs-blue" href="#tvs-inc">See what is included</a>
      <a class="tvs-btn tvs-ghost" href="#tvs-book">@@CTA@@</a>
    </div>
    <ul class="tvs-trust">
      <li><b>5 spots</b>that is it</li>
      <li><b>Weekly</b>specials everywhere</li>
      <li><b>Push alerts</b>to every mobile app user</li>
    </ul>
  </div>
  <div class="tvs-float tvs-f1 tvs-up" aria-hidden="true">
    <div class="tvs-fic">&#127837;</div><div><b>Tonight's special is live</b><span>Website, mobile app, Instagram + Facebook</span></div>
  </div>
  <div class="tvs-float tvs-f2 tvs-up" aria-hidden="true">
    <div class="tvs-fic tvs-ficg">&#128276;</div><div><b>Push sent to every mobile app user</b><span>"Tonight: your special, your table"</span></div>
  </div>
</section>

<section class="tvs-sec tvr-spots tvs-up" aria-label="Spots available">
  <div class="tvr-sbox">
    <div>
      <p class="tvs-eyebrow tvs-eylite">Exclusive by design</p>
      <h2>5 restaurants. That is it.</h2>
      <p>We only take five Restaurant Partners, so every one gets real attention and neighbors see a short list they can trust, not a wall of ads. When the five are gone, they are gone.</p>
    </div>
    <div class="tvr-count">
      <div class="tvr-dots" aria-hidden="true">@@DOTS@@</div>
      <p><b>@@LEFT@@</b></p>
      <a class="tvs-btn tvs-white" href="#tvs-book">@@CTA@@</a>
    </div>
  </div>
</section>

<section class="tvs-sec tvs-need" id="tvs-inc">
  <div class="tvs-head tvs-up">
    <p class="tvs-eyebrow">Everything in one plan</p>
    <h2>Every way neighbors decide where to eat. Covered.</h2>
    <p>Locals check our mobile app, our homepage, our Instagram and our Friday email to figure out dinner. As a Restaurant Partner you are in all of them, every week.</p>
  </div>
  <div class="tvr-feat">
    <div class="tvs-nt tvs-up tvs-ntstar"><span>&#128276;</span><b>Monthly mobile app push notification</b><p>Once a month your restaurant goes straight to the phone of every Three Village Local mobile app user. The fastest way to fill tables tonight.</p></div>
    <div class="tvs-nt tvs-up tvs-ntstar"><span>&#127869;&#65039;</span><b>Weekly specials on our website, mobile app and social</b><p>Text us your specials. They go on our website, the mobile app's Eat &amp; Drink, Instagram and Facebook every week.</p></div>
    <div class="tvs-nt tvs-up tvs-ntstar"><span>&#127909;</span><b>Your promo video</b><p>Filmed at your restaurant, edited by us, shared across Three Village Local and yours to keep.</p></div>
  </div>
  <div class="tvs-ngrid">
    <div class="tvs-nt tvs-up"><span>&#11088;</span><b>VIP listing</b><p>Top of the Restaurants page with a premium profile, menu, photos and order links.</p></div>
    <div class="tvs-nt tvs-up"><span>&#128241;</span><b>Social media posts</b><p>Custom posts and a Reel every month on our Instagram and Facebook.</p></div>
    <div class="tvs-nt tvs-up"><span>&#127968;</span><b>Homepage + mobile app</b><p>A regular top spot in Eat &amp; Drink on our homepage and in the free mobile app.</p></div>
    <div class="tvs-nt tvs-up"><span>&#128232;</span><b>Weekly newsletter</b><p>Your specials in the Friday email locals read to plan their weekend.</p></div>
    <div class="tvs-nt tvs-up"><span>&#127881;</span><b>Events + holidays</b><p>Wine nights, live music, Mother's Day, Restaurant Week, pushed on our calendar and social.</p></div>
    <div class="tvs-nt tvs-up"><span>&#128197;</span><b>Seasonal guides</b><p>A spot in our fall, holiday and summer guides that neighbors save and share.</p></div>
    <div class="tvs-nt tvs-up"><span>&#127991;&#65039;</span><b>Partner window decal + review cards</b><p>A "3VL Restaurant Partner" decal and table cards that turn happy diners into Google reviews.</p></div>
    <div class="tvs-nt tvs-up"><span>&#129302;</span><b>Google + AI search</b><p>When neighbors ask Google or ChatGPT where to eat, our pages help put you in the answer.</p></div>
  </div>
</section>

<section class="tvs-sec tvs-tl">
  <div class="tvs-head tvs-up">
    <p class="tvs-eyebrow">How a week works</p>
    <h2>You cook. We handle the rest.</h2>
  </div>
  <ol class="tvs-tlist">
    <li class="tvs-up"><em>Monday</em><b>Text us your specials</b><p>A photo and a line is plenty. We write it up and make it look great.</p></li>
    <li class="tvs-up"><em>Tuesday</em><b>They are everywhere</b><p>Website, mobile app, Instagram and Facebook, all pointing to you.</p></li>
    <li class="tvs-up"><em>Friday</em><b>In the weekly email</b><p>Right when locals are deciding where to go this weekend.</p></li>
    <li class="tvs-up"><em>Every month</em><b>Your push + new content</b><p>A push notification to every mobile app user, plus fresh posts and a Reel.</p></li>
  </ol>
</section>

''' + section(src, 'tvs-sec tvs-social') + '''

''' + section(src, 'tvs-sec tvs-work') + '''

<section class="tvs-sec tvr-math">
  <div class="tvs-head tvs-up">
    <p class="tvs-eyebrow">Do the math</p>
    <h2>Over $1,000 a month in marketing. For $@@PRICE@@.</h2>
    <p>Here is what each piece would cost on its own. As a Restaurant Partner you get all of it, every month.</p>
  </div>
  <div class="tvr-stack tvs-up">
    <ul>
      <li class="tvs-up tvr-hl"><span>Monthly push notification to every mobile app user</span><b>$150/mo</b></li>
      <li class="tvs-up tvr-hl"><span>Weekly specials on our website, mobile app and social</span><b>$150/mo</b></li>
      <li class="tvs-up tvr-hl"><span>Promo video filmed at your restaurant</span><b>$1,200 one time</b></li>
      <li class="tvs-up "><span>VIP listing with top placement</span><b>$115/mo</b></li>
      <li class="tvs-up "><span>Custom posts + a Reel every month on Instagram and Facebook</span><b>$299/mo</b></li>
      <li class="tvs-up "><span>Featured in the Friday newsletter</span><b>$100/mo</b></li>
      <li class="tvs-up "><span>Regular top spot in Eat &amp; Drink on the homepage and mobile app</span><b>$150/mo</b></li>
      <li class="tvs-up "><span>Event, holiday and seasonal guide promotion</span><b>$100/mo</b></li>
      <li class="tvs-up "><span>Partner window decal + review table cards</span><b>$99 one time</b></li>
    </ul>
    <div class="tvr-tot"><span>Total value</span><s>$1,064/mo + $1,299 one time</s></div>
    <div class="tvr-you"><span>Your price</span><b>$@@PRICE@@<small>/mo</small></b></div>
    <p class="tvr-pay">About two extra tables a week covers it. Everything after that is profit.</p>
  </div>
</section>

<section class="tvs-sec tvs-bundles" id="tvs-bundles">
  <div class="tvs-head tvs-up">
    <p class="tvs-eyebrow">One plan, one price</p>
    <h2>Restaurant Partner</h2>
    <p>Everything above in one monthly plan. No setup fee. No hidden costs.</p>
  </div>
  <div class="tvs-cards tvr-one">
    <article class="tvs-card tvs-pop tvs-up" data-b="rest">
      <p class="tvs-badge">@@LEFT@@</p>
      <p class="tvs-cname">Restaurant Partner</p>
      <p class="tvs-cfor">The all-in-one promotion plan for local restaurants</p>
      <p class="tvs-price"><sup>$</sup><b>@@PRICE@@</b></p>
      <p class="tvs-mo">per month, 6-month partnership</p>
      <ul>
        <li class="tvs-star">Monthly push notification to every mobile app user</li>
        <li class="tvs-star">Weekly specials on our website, mobile app and social</li>
        <li class="tvs-star">Promo video filmed at your restaurant</li>
        <li>VIP listing with top placement</li>
        <li>Featured in the Friday newsletter</li>
        <li>Regular top spot in Eat &amp; Drink on the homepage and mobile app</li>
        <li>Custom posts + a Reel every month on Instagram and Facebook</li>
        <li>Event, holiday and seasonal guide promotion</li>
        <li>Partner window decal + review table cards</li>
      </ul>
      <a class="tvs-btn tvs-blue tvs-wide" href="#tvs-book" data-pick="rest_partner">@@CTA@@</a>
    </article>
  </div>
  <p class="tvs-fine tvs-up">You approve every post before it goes out. After 6 months the plan is month to month. Already a VIP member? Your VIP rolls into the partnership, so you never pay twice.</p>
</section>

<section class="tvs-sec tvs-faq">
  <div class="tvs-head tvs-up"><p class="tvs-eyebrow">Questions</p><h2>Good questions, straight answers.</h2></div>
  <div class="tvs-qs tvs-up">
    <details><summary>Why only 5 restaurants?</summary><p>So it stays worth it. Five partners means each one is seen often, and neighbors get a short list of places we stand behind instead of an ad for everyone.</p></details>
    <details><summary>What happens when the 5 spots are taken?</summary><p>The plan closes. Restaurants can join the waitlist, and when a spot opens the next one on the list gets the first call.</p></details>
    <details><summary>What is the push notification?</summary><p>Once a month we send an alert about your restaurant straight to the phone of everyone who has the Three Village Local mobile app. It is the fastest way to fill tables on a slow night.</p></details>
    <details><summary>How do I send my specials?</summary><p>Text or email us a photo and a line about it. We write it up, design it and post it. You approve before it goes out.</p></details>
    <details><summary>Who films the promo video?</summary><p>Our team comes to your restaurant at a time that works for you, films, edits and posts it. You keep the video to use anywhere.</p></details>
    <details><summary>I am already a VIP member. Do I pay for both?</summary><p>No. Your VIP membership rolls into the partnership.</p></details>
    <details><summary>Is there a contract?</summary><p>A 6-month partnership to start, which covers the promo video. After that it is month to month.</p></details>
  </div>
</section>

''' + section(src, 'tvs-sec tvs-book') + '''

<a class="tvs-sticky" href="#tvs-book">@@CTA@@</a>
<script>(function(){var n=0,t=setInterval(function(){var s=document.querySelector('#tvs-form-slot select[name="bundle"]');if(s){s.value='rest_partner';clearInterval(t)}if(++n>40)clearInterval(t)},250)})();</script>
</div>'''

HTML = (HTML.replace("@@CTA@@", cta).replace("@@LEFT@@", left_txt).replace("@@DOTS@@", dots)
        .replace("@@PRICE@@", "{:,}".format(PRICE)))
HTML = HTML.replace("<h2>Book your free 15-minute call.</h2>",
                    "<h2>Join the waitlist.</h2>" if FULL else "<h2>Claim one of the 5 spots.</h2>")
HTML = HTML.replace("<p>Tell us a little about your business.",
                    "<p>Tell us about your restaurant." if not FULL else "<p>Tell us about your restaurant and we will call you when a spot opens.")
HTML = HTML.replace("Social media, done for you. In every bundle.", "Social media, done for you.")
HTML = HTML.replace("<h2>Your content, posted twice.</h2>", "<h2>Your food, in front of the whole town.</h2>")
HTML = HTML.replace("<p>We create it and post it on your pages. Then Three Village Local shares it on our Instagram, Facebook, mobile app and website. Your followers see it, and so does the whole town.</p>",
                    "<p>We create the posts and share them on Three Village Local's Instagram, Facebook, mobile app and website. Your regulars see it, and so does everyone deciding where to eat tonight.</p>")
HTML = HTML.replace("?subject=Services", "?subject=Restaurant%20Partner")

CSS = '''
/* new-business tiles + timeline (shared look) */
.tvs-ngrid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.tvs-nt{background:#fff;border:1px solid var(--line);border-radius:18px;padding:20px 18px;transition:transform .2s,box-shadow .2s}
.tvs-nt:hover{transform:translateY(-3px);box-shadow:0 14px 30px rgba(13,35,70,.1)}
.tvs-nt span{font-size:26px}
.tvs-nt b{display:block;color:var(--navy);font-size:16.5px;margin:8px 0 4px}
.tvs-nt p{margin:0!important;color:var(--mut);font-size:14px!important;line-height:1.45}
.tvs-ntstar{background:linear-gradient(135deg,#0f2a52,#1d4f91);border:0}
.tvs-ntstar b{color:#fff}.tvs-ntstar p{color:#cfe0f7}
.tvs-tlist{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(4,1fr);gap:14px;position:relative}
.tvs-tlist:before{content:"";position:absolute;left:0;right:0;top:15px;height:3px;background:linear-gradient(90deg,var(--blue2),var(--gold));border-radius:3px}
.tvs-tlist li{position:relative;padding-top:38px}
.tvs-tlist li:before{content:"";position:absolute;top:7px;left:0;width:19px;height:19px;border-radius:50%;background:#fff;border:4px solid var(--blue)}
.tvs-tlist em{font-style:normal;font-size:12.5px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--blue)}
.tvs-tlist b{display:block;color:var(--navy);font-size:19px;margin:4px 0}
.tvs-tlist p{margin:0!important;color:var(--mut);font-size:14.5px!important}
/* restaurant partner */
.tvs-rp .tvs-hphoto{background-image:url('@@IMG@@hero-1080.webp');background-position:50% 50%}
.tvr-sbox{border-radius:26px;padding:38px 44px;display:flex;align-items:center;justify-content:space-between;gap:34px;background:linear-gradient(120deg,var(--navy,#0f2a52) 0%,#1d4f91 100%);color:#fff;box-shadow:0 26px 60px rgba(15,42,82,.25)}
.tvr-sbox h2{color:#fff;font-size:34px;margin:0 0 8px}
.tvr-sbox p{color:#d7e5f8;margin:0;max-width:560px}
.tvr-count{text-align:center;flex:0 0 auto}
.tvr-dots{display:flex;gap:10px;justify-content:center;margin-bottom:12px}
.tvr-dots i{width:34px;height:34px;border-radius:50%;background:var(--gold);box-shadow:0 0 0 4px rgba(255,197,61,.25)}
.tvr-dots i.tvr-taken{background:rgba(255,255,255,.18);box-shadow:none}
.tvr-count p{margin:0 0 14px!important;color:#fff!important;font-size:18px}
.tvr-stack{max-width:760px;margin:0 auto;background:#fff;border:1px solid var(--line);border-radius:26px;padding:26px 30px;box-shadow:0 16px 40px rgba(19,41,75,.06)}
.tvr-stack ul{list-style:none;margin:0;padding:0}
.tvr-stack li{display:flex;justify-content:space-between;gap:18px;padding:11px 0;border-bottom:1px dashed var(--line);font-size:15.5px}
.tvr-stack li b{color:var(--navy);white-space:nowrap}
.tvr-tot,.tvr-you{display:flex;justify-content:space-between;align-items:baseline;gap:18px;padding-top:16px}
.tvr-tot span{font-weight:800;color:var(--mut)}.tvr-tot s{color:var(--mut);font-weight:700;font-size:17px}
.tvr-you span{font-weight:800;color:var(--navy);font-size:20px}.tvr-you b{color:var(--blue);font-size:44px;line-height:1}.tvr-you small{font-size:18px}
.tvr-pay{margin:14px 0 0!important;padding:12px 16px;border-radius:14px;background:#fff7e0;color:#5a4410!important;font-weight:700;text-align:center}
.tvr-feat{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:14px}
.tvr-feat .tvs-nt{padding:26px 24px}.tvr-feat .tvs-nt span{font-size:34px}.tvr-feat .tvs-nt b{font-size:19px}.tvr-feat .tvs-nt p{font-size:15px!important}
.tvr-stack li.tvr-hl{background:#eef4fd;margin:0 -14px;padding:11px 14px;border-radius:12px;border-bottom:0;font-weight:700;color:var(--navy)}
.tvr-stack li.tvr-hl+li.tvr-hl{margin-top:6px}
.tvr-stack li.tvr-hl span:before{content:"★ ";color:#e0a51b}
.tvr-one{grid-template-columns:minmax(0,520px)!important;justify-content:center}
@media (max-width:900px){.tvr-feat{grid-template-columns:1fr}.tvs-ngrid{grid-template-columns:repeat(2,1fr)}.tvs-tlist{grid-template-columns:1fr 1fr;row-gap:26px}.tvs-tlist:before{display:none}
 .tvr-sbox{flex-direction:column;align-items:flex-start;padding:28px 24px}.tvr-count{text-align:left}.tvr-dots{justify-content:flex-start}}
@media (max-width:520px){.tvr-stack{padding:18px 16px}.tvr-stack li{font-size:14.5px;flex-direction:column;gap:2px}.tvr-tot,.tvr-you{flex-direction:column;gap:4px}.tvs-ngrid{gap:10px}.tvs-nt{padding:16px 14px}.tvs-tlist{grid-template-columns:1fr}.tvr-sbox h2{font-size:27px}.tvr-dots i{width:28px;height:28px}
 .tvs-rp .tvs-hphoto{background-image:url('@@IMG@@hero-720.webp')}}
'''.replace("@@IMG@@", IMG)

_rd = D.rd


def rd(f):
    if f == "page.html":
        assert "\\" not in HTML
        return HTML
    s = _rd(f)
    return s + CSS if f == "page.css" else s


D.rd = rd
if __name__ == "__main__":
    D.main()
