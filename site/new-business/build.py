"""New-business launch page (owner 10/18/2026): same look as /services, geared to getting a new business set up.
Shares page.css / page.js and the showcase, reach and booking sections with site/services-page (pulled from its page.html,
so they stay in sync).
    python site/new-business/build.py            -> widget "3VL Page New Business" + hidden preview /preview-new-business
    python site/new-business/build.py --live     -> /new-business (indexable)"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SV = os.path.join(HERE, "..", "services-page")
sys.path.insert(0, SV)
import deploy as D

D.NAME = "3VL Page New Business"
D.SLUG = "new-business" if D.LIVE else "preview-new-business"
D.TITLE = "New Business Launch: Website, Google, Social Media & Grand Opening | Three Village Local"
D.DESC = ("Opening a business in Stony Brook, Setauket or Port Jefferson? We set up your website, Google profile, social media "
          "and grand opening promotion, then announce you to the whole town on Three Village Local.")


def section(src, cls):
    i = src.index('<section class="' + cls)
    j = src.index('</section>', i) + len('</section>')
    return src[i:j]


src = open(os.path.join(SV, "page.html"), encoding="utf-8").read()

HTML = '''<div class="tvs tvs-nb" id="tvs">

<section class="tvs-hero">
  <div class="tvs-hphoto" role="img" aria-label="Local shop owner smiling in the doorway of his store"></div>
  <div class="tvs-hfade"></div>
  <div class="tvs-hin tvs-up">
    <p class="tvs-kick"><span class="tvs-dot"></span>New business launch</p>
    <h1>Opening soon?<br><span>We get you ready for day one.</span></h1>
    <p class="tvs-sub">Website, Google, social media and a grand opening the whole town hears about. One local team sets it all up so you can focus on opening your doors.</p>
    <div class="tvs-ctas">
      <a class="tvs-btn tvs-blue" href="#tvs-bundles">See launch packages</a>
      <a class="tvs-btn tvs-ghost" href="#tvs-book">Book a free call</a>
    </div>
    <ul class="tvs-trust">
      <li><b>1 team</b>does it all</li>
      <li><b>No</b>long contracts</li>
      <li><b>Local</b>real people</li>
    </ul>
  </div>
  <div class="tvs-float tvs-f1 tvs-up" aria-hidden="true">
    <div class="tvs-fic">&#127881;</div><div><b>Grand opening this Saturday</b><span>Shared with 100,000+ local views</span></div>
  </div>
  <div class="tvs-float tvs-f2 tvs-up" aria-hidden="true">
    <div class="tvs-fic tvs-ficg">&#10003;</div><div><b>Google profile verified</b><span>You now show up on Maps</span></div>
  </div>
</section>

<section class="tvs-sec tvs-need">
  <div class="tvs-head tvs-up">
    <p class="tvs-eyebrow">Your opening checklist</p>
    <h2>Everything a new business needs. Done for you.</h2>
    <p>Most new owners spend weeks figuring this out between contractors and inspections. Hand us the list.</p>
  </div>
  <div class="tvs-ngrid">
    <div class="tvs-nt tvs-up"><span>&#128187;</span><b>Website + domain</b><p>Fast on phones, your name.com, set up in your account.</p></div>
    <div class="tvs-nt tvs-up"><span>&#9993;&#65039;</span><b>Business email</b><p>you@yourbusiness.com instead of a Gmail address.</p></div>
    <div class="tvs-nt tvs-up"><span>&#128205;</span><b>Google Business Profile</b><p>Created, verified, photos, hours, so you show up on Maps.</p></div>
    <div class="tvs-nt tvs-up"><span>&#128506;&#65039;</span><b>Apple Maps, Bing, Yelp</b><p>Listed everywhere people search, all matching.</p></div>
    <div class="tvs-nt tvs-up"><span>&#128241;</span><b>Instagram + Facebook</b><p>Pages set up and branded, ready to post.</p></div>
    <div class="tvs-nt tvs-up"><span>&#127912;</span><b>Brand kit</b><p>Logo cleanup, colors and post templates that match.</p></div>
    <div class="tvs-nt tvs-up"><span>&#127909;</span><b>Photos and video</b><p>Show off your space before the doors even open.</p></div>
    <div class="tvs-nt tvs-up tvs-ntstar"><span>&#11088;</span><b>Grand opening on 3VL</b><p>Announced to the town on our mobile app, website and social.</p></div>
  </div>
</section>

<section class="tvs-sec tvs-tl">
  <div class="tvs-head tvs-up">
    <p class="tvs-eyebrow">How a launch runs</p>
    <h2>From "coming soon" to the place everyone knows.</h2>
  </div>
  <ol class="tvs-tlist">
    <li class="tvs-up"><em>Weeks before</em><b>Get set up</b><p>Website, Google, email, listings and social pages built and ready.</p></li>
    <li class="tvs-up"><em>Coming soon</em><b>Build the buzz</b><p>Sneak peeks and "coming soon" posts on your pages and ours.</p></li>
    <li class="tvs-up"><em>Opening day</em><b>Tell the whole town</b><p>Grand opening spotlight across Three Village Local.</p></li>
    <li class="tvs-up"><em>First 90 days</em><b>Keep them coming</b><p>Monthly posts, Reels and reviews so the buzz does not fade.</p></li>
  </ol>
</section>

''' + section(src, 'tvs-sec tvs-work') + '''

''' + section(src, 'tvs-sec tvs-social') + '''

<section class="tvs-sec tvs-bundles" id="tvs-bundles">
  <div class="tvs-head tvs-up">
    <p class="tvs-eyebrow">Launch packages</p>
    <h2>Pick your launch. We handle the rest.</h2>
    <p>One setup price to get you open, then monthly social media to keep the momentum. Members save, VIP members save the most.</p>
  </div>
  <div class="tvs-tiers tvs-up" role="tablist" aria-label="Choose your membership to see your price">
    <button type="button" role="tab" data-t="all">Not a member</button>
    <button type="button" role="tab" data-t="free">Member</button>
    <button type="button" role="tab" data-t="featured">Featured</button>
    <button type="button" role="tab" data-t="vip" class="on">VIP<em>Best price</em></button>
  </div>
  <div class="tvs-cards">
    <article class="tvs-card tvs-up" data-b="open">
      <p class="tvs-cname">Open Ready</p>
      <p class="tvs-cfor">The must-haves, done right before you open</p>
      <p class="tvs-was"></p>
      <p class="tvs-price"><sup>$</sup><b>599</b></p>
      <p class="tvs-mo">+ <b>$99</b>/mo</p>
      <p class="tvs-save"></p>
      <ul>
        <li>1-page website + your domain</li>
        <li>Business email</li>
        <li>Google Business Profile created + verified</li>
        <li>Apple Maps, Bing and Yelp listings</li>
        <li>Instagram + Facebook pages set up</li>
        <li>Monthly: 4 custom social posts</li>
        <li class="tvs-star">Grand opening post on Three Village Local</li>
      </ul>
      <a class="tvs-btn tvs-line tvs-wide" href="#tvs-book" data-pick="new_open">Get open ready</a>
    </article>
    <article class="tvs-card tvs-pop tvs-up" data-b="grand">
      <p class="tvs-badge">Most popular</p>
      <p class="tvs-cname">Grand Opening</p>
      <p class="tvs-cfor">Open with a buzz the whole town notices</p>
      <p class="tvs-was"></p>
      <p class="tvs-price"><sup>$</sup><b>1,199</b></p>
      <p class="tvs-mo">+ <b>$349</b>/mo</p>
      <p class="tvs-save"></p>
      <ul>
        <li>Everything in Open Ready</li>
        <li>Website up to 5 pages</li>
        <li>Brand kit: logo cleanup, colors, templates</li>
        <li>Grand opening Reel made for you</li>
        <li class="tvs-star">Coming soon + grand opening spotlight on 3VL</li>
        <li>Your opening on the 3VL events calendar</li>
        <li>Monthly: 8 custom posts + 1 animated Reel</li>
      </ul>
      <a class="tvs-btn tvs-blue tvs-wide" href="#tvs-book" data-pick="new_grand">Plan my grand opening</a>
    </article>
    <article class="tvs-card tvs-up" data-b="debut">
      <p class="tvs-cname">Big Debut</p>
      <p class="tvs-cfor">For openings that want to make a splash</p>
      <p class="tvs-was"></p>
      <p class="tvs-price"><sup>$</sup><b>2,199</b></p>
      <p class="tvs-mo">+ <b>$699</b>/mo</p>
      <p class="tvs-save"></p>
      <ul>
        <li>Everything in Grand Opening</li>
        <li>Promo video of your business</li>
        <li>Drone aerials of your location</li>
        <li class="tvs-star">A spotlight story on Three Village Local</li>
        <li>Opening-week ad setup on Facebook + Instagram (ad budget separate)</li>
        <li>Monthly: 12 custom posts + 2 animated Reels</li>
        <li>Priority promotion for your events and specials</li>
      </ul>
      <a class="tvs-btn tvs-line tvs-wide" href="#tvs-book" data-pick="new_debut">Make my debut</a>
    </article>
  </div>
  <p class="tvs-fine tvs-up">You approve every post before it goes out. Half of setup to start, the rest at launch. Monthly is month to month. Cancel anytime.</p>
</section>

<section class="tvs-sec tvs-faq">
  <div class="tvs-head tvs-up"><p class="tvs-eyebrow">Questions</p><h2>Good questions, straight answers.</h2></div>
  <div class="tvs-qs tvs-up">
    <details><summary>When should we start?</summary><p>Four to six weeks before opening is ideal. That gives Google time to verify you and us time to build the buzz. Opening sooner? We move fast.</p></details>
    <details><summary>Do I own my website, domain and social pages?</summary><p>Yes. Everything is set up in your name and your accounts. If you ever leave, you keep it all.</p></details>
    <details><summary>I do not have a logo yet. Can you help?</summary><p>Yes. Grand Opening and Big Debut include a brand kit: we clean up or refresh your logo and set your colors and post templates.</p></details>
    <details><summary>Is there a contract?</summary><p>No long contracts. Setup is paid once, and the monthly plan is month to month.</p></details>
    <details><summary>Do I have to be a Three Village Local member?</summary><p>No. Anyone can book. Members save, and VIP members save the most.</p></details>
  </div>
</section>

''' + section(src, 'tvs-sec tvs-book') + '''

<a class="tvs-sticky" href="#tvs-book">Book a free call</a>
</div>'''

HTML = HTML.replace("<h2>Book your free 15-minute call.</h2>", "<h2>Tell us about your opening.</h2>")
HTML = HTML.replace("<p>Tell us a little about your business.", "<p>Tell us what you are opening and when.")

CSS = '''
/* new-business page extras */
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
@media (max-width:900px){.tvs-ngrid{grid-template-columns:repeat(2,1fr)}.tvs-tlist{grid-template-columns:1fr 1fr;row-gap:26px}.tvs-tlist:before{display:none}}
@media (max-width:520px){.tvs-ngrid{gap:10px}.tvs-nt{padding:16px 14px}.tvs-tlist{grid-template-columns:1fr}}
'''

_rd = D.rd


def rd(f):
    if f == "page.html":
        assert "\\" not in HTML
        return HTML
    s = _rd(f)
    return s + CSS if f == "page.css" else s


D.rd = rd
D.main()
