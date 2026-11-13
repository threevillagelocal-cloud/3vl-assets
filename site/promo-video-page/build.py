"""Promo video service page (owner 11/12/2026: every service on /services gets its own premium interactive page). No prices.
    python site/promo-video-page/build.py          -> widget "3VL Page Promo Video Preview" + hidden /preview-promo-video (noindex)
    (--live -> /promo-video only after the owner's OK)"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "svc-kit"))
import kit as K
from kit import ic, SV

HERO_VIS = '''<div class="tpv-hv">''' + K.P.V_VIDEO + '''
  <div class="tvx-chip tpv-c1" style="animation-delay:.9s,1.8s"><span class="tvx-ic" style="--ac:#16a37a">''' + ic("cc") + '''</span><div><b>Captioned</b>for sound-off scrolling</div></div>
  <div class="tvx-chip tpv-c2" style="animation-delay:1.3s,2.4s"><span class="tvx-ic">''' + ic("share") + '''</span><div><b>100,000+ views</b>a month on our social</div></div>
  <div class="tvx-chip tpv-c3" style="animation-delay:1.7s,3s"><span class="tvx-ic" style="--ac:#e0a82e">''' + ic("crop") + '''</span><div><b>Every size</b>Reels, TikTok, website</div></div>
</div>'''

HERO = K.hero("Promo video", "Show them,", "don&#39;t just tell them.",
              "Short, scroll-stopping promo videos for your business: filmed at your place, edited with music and captions, sized for every screen, then shared with the whole Three Village community.",
              HERO_VIS, ("See the formats", "#tvp-formats"))

NAV = K.snav([("get", "What you get"), ("formats", "Formats"), ("how", "How it works"), ("reach", "Where it plays"), ("ideas", "Ideas by industry"), ("faq", "FAQ")])

GET = K.sec("get", "What you get", "A video that works as hard as you do.",
            "We handle every part of it, from the plan to the final cut. You just show us what makes your business special.",
            K.cards([("camera", "Filmed at your business", "We come to you with pro gear and a shot list, and keep it quick so you can get back to work."),
                     ("scissors", "Edited to stop the scroll", "Tight cuts, music, motion titles and your logo, so it looks like a brand, not a home video."),
                     ("cc", "Captioned for sound-off", "Most people scroll with the sound off, so every video gets bold, easy-to-read captions."),
                     ("crop", "Sized for every screen", "Reels, TikTok, Facebook, your website and more: every size you need, ready to post.")], 4))

FMTS = [("r916", "9:16", "Reel", "Reels, TikTok and Stories", "Full-screen vertical video, the format people watch most on their phones. We keep titles and captions inside the safe zone, so nothing hides under the buttons.",
         ["Instagram Reels", "Facebook Reels", "TikTok", "Stories", "YouTube Shorts"]),
        ("r45", "4:5", "Feed", "Facebook and Instagram feeds", "Takes up the most room in a feed without going full screen, so it stops the scroll on the posts neighbors already read.",
         ["Instagram feed", "Facebook feed", "Three Village Local mobile app"]),
        ("r11", "1:1", "Square", "Square, for almost anywhere", "The safe all-rounder for feeds, ads, email and your Google Business Profile updates.",
         ["Google Business Profile", "Facebook and Instagram ads", "Email"]),
        ("r169", "16:9", "Website", "Your website and YouTube", "Wide video for your homepage, your Three Village Local listing and YouTube, where people watch on bigger screens.",
         ["Your website", "YouTube", "Three Village Local listing"])]
tabs = "".join('<button class="tvx-tab%s" data-tab="%s"><b class="tpv-rt">%s</b>%s</button>' % (" on" if n == 0 else "", k, r, lab) for n, (k, r, lab, h, p, ch) in enumerate(FMTS))
panels = "".join('<div class="tpv-fi" data-panel="%s"><p class="tpv-fk">%s</p><h3>%s</h3><p>%s</p><ul class="tpv-where">%s</ul></div>' % (
    k, r, h, p, "".join("<li>%s%s</li>" % (ic("check"), c) for c in ch)) for k, r, lab, h, p, ch in FMTS)
FORMATS = K.sec("formats", "One shoot. Every size.", "Made for wherever your customers watch.",
                "Tap a format to see the same video reframed for each screen.",
                '''<div class="tpv-fmt tvs-up" data-tabs data-auto="3400">
    <div class="tvx-tabs">''' + tabs + '''</div>
    <div class="tpv-stage">
      <div class="tpv-frame-w" data-run><div class="tpv-frame">
        <video class="tvp-rv" muted playsinline loop preload="none" poster="''' + SV + '''campus-bikes-poster.webp" data-src="''' + SV + '''campus-bikes-720.mp4" width="720" height="900" aria-label="Campus Bicycles promo video, reframed for each format"></video>
        <div class="tpv-ov tpv-ov-reel" aria-hidden="true"><span>''' + ic("heart") + ic("message") + ic("share") + '''</span><p><b>@campusbicycles</b>Ride season is here. Come see us in Stony Brook.</p></div>
        <div class="tpv-ov tpv-ov-feed" aria-hidden="true"><p class="tpv-ig"><i></i><b>threevillagelocal</b> and <b>campusbicycles</b></p><p class="tpv-acts">''' + ic("heart") + ic("message") + ic("share") + '''</p></div>
        <div class="tpv-ov tpv-ov-sq" aria-hidden="true"><p>Tune-ups, rentals and rides. Stony Brook.</p></div>
        <div class="tpv-ov tpv-ov-web" aria-hidden="true"><p class="tpv-bar"><i></i><i></i><i></i><span>campusbicycles.com</span></p><p class="tpv-prog"><u></u></p></div>
      </div><span class="tpv-ratio" aria-hidden="true"></span></div>
      <div class="tpv-info">''' + panels + '''</div>
    </div>
  </div>''')

HOW = K.sec("how", "How it works", "From idea to posted in four easy steps.", "",
            K.steps([("Plan", "A quick call about what to show off, who you want to reach and the best time to film."),
                     ("Film", "We come to you and film the shots on our list. Most shoots wrap up quickly."),
                     ("Edit", "Music, captions, titles and your logo. You review a draft and ask for changes."),
                     ("Launch", "We share it across Three Village Local and hand you every size to post yourself.")]))

REACH = '''<section class="tvs-sec tvx-sec tvx-dark tpv-reach" id="tvp-reach" data-run>
  <div class="tvs-head tvs-up"><p class="tvs-eyebrow">Where it plays</p><h2>Then we show it to the whole town.</h2><p>Your video doesn&#39;t sit on a hard drive. It goes straight to the places Three Village already looks every day.</p></div>
  <div class="tpv-hub tvs-up">
    <div class="tpv-col">
      <div class="tpv-node"><span class="tvx-ic">''' + K.SOCLOGO["Instagram"] + '''</span><div><b><span data-n="100000">100,000</span>+</b><i>Facebook &amp; Instagram views a month</i></div></div>
      <div class="tpv-node"><span class="tvx-ic">''' + ic("globe") + '''</span><div><b><span data-n="45000">45,000</span>+</b><i>website page visits a month</i></div></div>
    </div>
    <div class="tpv-core"><div class="tpv-core-v"><img src="''' + SV + '''girard-poster.webp" alt="Promo video for Girard Wealth Management" loading="lazy" width="480" height="854"><span>''' + ic("play") + '''</span></div><p>Your video</p></div>
    <div class="tpv-col tpv-r">
      <div class="tpv-node"><span class="tvx-ic">''' + ic("phone") + '''</span><div><b>Mobile app</b><i>On local phones in our free mobile app</i></div></div>
      <div class="tpv-node"><span class="tvx-ic">''' + ic("users") + '''</span><div><b>Your accounts</b><i>Tagged with a collab invite, so it lives on your profile too</i></div></div>
    </div>
  </div>
  <p class="tpv-local tvs-up">''' + ic("pin") + '''100% local audience: Setauket, Stony Brook, Port Jefferson and the neighbors around them.</p>
</section>'''

IND = [("food", "utensils", "Restaurants", "Friday night, sorted.", [("0:00", "The sizzle", "A signature dish hitting the pan"), ("0:05", "The kitchen", "Your team at full speed"), ("0:12", "The invite", "A warm, full dining room")]),
       ("shop", "store", "Shops", "Found it in Three Village.", [("0:00", "New arrivals", "Fresh stock, unboxed"), ("0:05", "Owner&#39;s picks", "Favorites, up close"), ("0:12", "The invite", "Your storefront, doors open")]),
       ("home", "hammer", "Home services", "Watch this kitchen transform.", [("0:00", "Before", "The problem, honestly shown"), ("0:05", "The work", "Your crew doing it right"), ("0:12", "After", "The big reveal")]),
       ("well", "heart", "Health and wellness", "Care that feels local.", [("0:00", "Welcome", "A calm, bright space"), ("0:05", "The team", "Friendly faces, real names"), ("0:12", "First visit", "What to expect, simply")]),
       ("pro", "briefcase", "Professional services", "A neighbor you can trust.", [("0:00", "Meet you", "The person behind the name"), ("0:05", "How you help", "In plain, simple words"), ("0:12", "Next step", "One clear way to reach you")]),
       ("fit", "dumbbell", "Fitness and studios", "Your first class is waiting.", [("0:00", "Doors open", "Music up, lights on"), ("0:05", "In session", "Real classes, real energy"), ("0:12", "The finish", "High fives and smiles")])]
itabs = "".join('<button class="tvx-tab%s" data-tab="%s">%s%s</button>' % (" on" if n == 0 else "", k, ic(i), t) for n, (k, i, t, cap, fr) in enumerate(IND))
ipan = ""
for k, i, t, cap, fr in IND:
    frames = "".join('<li style="--d:%ds"><em>%s</em><b>%s</b><span>%s</span></li>' % (n, tm, a, b) for n, (tm, a, b) in enumerate(fr))
    ipan += '<div class="tpv-sb" data-panel="%s"><div class="tpv-sb-h"><span class="tvx-ic">%s</span><div><p>Storyboard idea</p><h3>%s</h3></div></div><ol>%s</ol><p class="tpv-cap">%s<b>&ldquo;%s&rdquo;</b><span>On-screen hook</span></p></div>' % (k, ic(i), t, frames, ic("cc"), cap)
IDEAS = K.sec("ideas", "Ideas by industry", "We know what makes your kind of business shine.",
              "Pick your industry to see a sample storyboard. Every video is planned around your business and your customers.",
              '<div class="tpv-ind tvs-up" data-tabs><div class="tvx-tabs">' + itabs + '</div>' + ipan + '</div>')

FAQ = K.faq([
    ("How long does filming take?", "Most shoots are quick. We plan the shots ahead of time so the visit goes fast and your customers are never in the way."),
    ("Do I need to prepare anything?", "Just pick a time that shows your business at its best. We send a simple checklist before we film."),
    ("Can I see it before it goes live?", "Always. You review a draft, ask for changes, and nothing is posted until you approve it."),
    ("Where will my video be shared?", "On Three Village Local&#39;s Facebook and Instagram (100,000+ local views a month), on our website and in our free mobile app, tagged to your accounts with a collab invite so it shows on your profile too."),
    ("Can I post it on my own website and social media?", "Yes. You get the finished video in every size you need, ready for your website, Instagram, Facebook, TikTok and Google Business Profile."),
    ("Is promo video part of a membership?", "Promo video is included with VIP memberships and discounted for Featured members. Ask for a free plan and we&#39;ll show you the options."),
    ("How do I get started?", "Fill out the short form below. We&#39;ll send you a free, personalized video plan by email, with no pressure and no contract."),
])

REL = K.related("promo-video", ["social-media", "email-articles", "new-business-launch", "ai-search", "websites", "join"])
CTA = K.cta("Lights, camera, Three Village", "Let&#39;s make something worth watching.", "Tell us about your business and we&#39;ll send a free video plan by email.")

CSS = '''
.tpv-hv{position:relative;width:100%}
.tpv-hv .tvp-vids{margin:0 auto}
.tpv-c1{left:-8px;top:8%}.tpv-c2{right:-6px;top:44%}.tpv-c3{left:2%;bottom:2%}
/* formats */
.tpv-stage{display:grid;grid-template-columns:1.1fr .9fr;gap:40px;align-items:center;max-width:1040px;margin:0 auto}
.tpv-frame-w{position:relative;height:470px;display:flex;align-items:center;justify-content:center;border-radius:26px;background:radial-gradient(circle at 50% 40%,#eaf2ff,#f6f9fd 70%);border:1px solid #e1e9f5}
.tpv-frame{--s:1;position:relative;width:calc(248px*var(--s));height:calc(440px*var(--s));border-radius:18px;overflow:hidden;background:#0f1a2b;box-shadow:0 30px 60px -28px rgba(9,30,66,.6);transition:width .7s cubic-bezier(.6,0,.2,1),height .7s cubic-bezier(.6,0,.2,1),border-radius .7s}
.tpv-frame video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
.tpv-fmt[data-cur="r45"] .tpv-frame{width:calc(340px*var(--s));height:calc(425px*var(--s))}
.tpv-fmt[data-cur="r11"] .tpv-frame{width:calc(390px*var(--s));height:calc(390px*var(--s))}
.tpv-fmt[data-cur="r169"] .tpv-frame{width:calc(560px*var(--s));height:calc(315px*var(--s));border-radius:12px}
.tpv-ratio{position:absolute;top:14px;left:14px;padding:5px 11px;border-radius:999px;background:#13294b;color:#fff;font-weight:800;font-size:13px;letter-spacing:.04em}
.tpv-fmt[data-cur="r916"] .tpv-ratio:after{content:"9:16 vertical"}.tpv-fmt[data-cur="r45"] .tpv-ratio:after{content:"4:5 feed"}.tpv-fmt[data-cur="r11"] .tpv-ratio:after{content:"1:1 square"}.tpv-fmt[data-cur="r169"] .tpv-ratio:after{content:"16:9 wide"}
.tpv-ov{position:absolute;inset:0;opacity:0;transition:opacity .4s .35s;pointer-events:none;color:#fff;font-size:12px}
.tpv-fmt[data-cur="r916"] .tpv-ov-reel,.tpv-fmt[data-cur="r45"] .tpv-ov-feed,.tpv-fmt[data-cur="r11"] .tpv-ov-sq,.tpv-fmt[data-cur="r169"] .tpv-ov-web{opacity:1}
.tpv-ov-reel span{position:absolute;right:10px;bottom:70px;display:flex;flex-direction:column;gap:14px}
.tpv-ov .tvx-svg{width:22px;height:22px;filter:drop-shadow(0 1px 3px rgba(0,0,0,.5))}
.tpv-ov-reel p{position:absolute;left:12px;right:46px;bottom:14px;margin:0!important;line-height:1.35;text-shadow:0 1px 4px rgba(0,0,0,.7)}
.tpv-ov-reel b,.tpv-ig b{display:block;font-size:12.5px}.tpv-ig b{display:inline}
.tpv-ig{position:absolute;left:0;right:0;top:0;margin:0!important;padding:10px 12px;background:linear-gradient(180deg,rgba(0,0,0,.55),transparent);display:flex;align-items:center;gap:6px;white-space:nowrap;overflow:hidden}
.tpv-ig i{width:22px;height:22px;border-radius:50%;background:linear-gradient(135deg,#feda75,#d62976 60%,#4f5bd5);border:2px solid #fff;flex:none}
.tpv-acts{position:absolute;left:12px;bottom:10px;margin:0!important;display:flex;gap:14px}
.tpv-ov-sq p{position:absolute;left:12px;right:12px;bottom:12px;margin:0!important;padding:8px 12px;border-radius:10px;background:rgba(19,41,75,.82);font-weight:700;font-size:12.5px}
.tpv-bar{position:absolute;left:0;right:0;top:0;margin:0!important;padding:7px 10px;background:#eef2f7;display:flex;align-items:center;gap:5px}
.tpv-bar i{width:8px;height:8px;border-radius:50%;background:#ff7b6b}.tpv-bar i:nth-child(2){background:#ffc85a}.tpv-bar i:nth-child(3){background:#4bd18a}
.tpv-bar span{margin-left:8px;flex:1;padding:2px 10px;border-radius:999px;background:#fff;color:#7a8696;font-size:11px}
.tpv-prog{position:absolute;left:12px;right:12px;bottom:12px;height:4px;margin:0!important;border-radius:4px;background:rgba(255,255,255,.35);overflow:hidden}
.tpv-prog u{position:absolute;left:0;top:0;bottom:0;width:100%;background:#ff3b3b;transform-origin:left;animation:tpvProg 9s linear infinite}
@keyframes tpvProg{from{transform:scaleX(0)}to{transform:scaleX(1)}}
.tpv-fk{display:inline-block;margin:0 0 10px!important;padding:5px 12px;border-radius:999px;background:#e7f0ff;color:var(--blue);font-weight:800;font-size:13px}
.tpv-fi h3{font-size:28px;line-height:1.15;margin:0 0 10px!important}
.tpv-fi>p:not(.tpv-fk){color:var(--mut);font-size:16.5px;line-height:1.6;margin:0 0 16px!important}
.tpv-where{list-style:none;margin:0!important;padding:0!important;display:flex;flex-wrap:wrap;gap:8px}
.tpv-where li{display:inline-flex;align-items:center;gap:7px;margin:0!important;padding:8px 13px;border-radius:999px;background:#fff;border:1px solid #dfe6f0;font-weight:700;font-size:14px;color:var(--navy)}
.tpv-where .tvx-svg{width:16px;height:16px;color:#16a37a}
.tvx .tpv-rt{display:inline-block;padding:2px 7px;border-radius:7px;background:#e7f0ff;color:var(--blue);font-size:12px}
.tvx .tvx-tab.on .tpv-rt{background:rgba(255,255,255,.18);color:#fff}
/* reach hub */
.tpv-hub{display:grid;grid-template-columns:1fr 210px 1fr;gap:0;align-items:center;max-width:1000px;margin:0 auto}
.tpv-col{display:grid;gap:22px}
.tpv-node{position:relative;display:flex;align-items:center;gap:14px;padding:18px;border-radius:18px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16);margin-right:44px}
.tpv-r .tpv-node{margin:0 0 0 44px}
.tpv-node:after{content:"";position:absolute;top:50%;right:-46px;width:46px;height:3px;margin-top:-1px;background:repeating-linear-gradient(90deg,#8ec5ff 0 6px,transparent 6px 12px);background-size:24px 3px;animation:tpvFlow 1s linear infinite;opacity:.8}
.tpv-r .tpv-node:after{right:auto;left:-46px;animation-direction:reverse}
@keyframes tpvFlow{from{background-position:0 0}to{background-position:24px 0}}
.tpv-node .tvx-ic{background:rgba(142,197,255,.16);color:#8ec5ff}
.tpv-node .tvx-ic svg{width:24px;height:24px}
.tpv-node b{display:block;font-size:24px;color:#fff;line-height:1.1;font-variant-numeric:tabular-nums}
.tpv-node i{display:block;font-style:normal;font-size:14px;line-height:1.4;color:#c4d5ee}
.tpv-core{text-align:center}
.tpv-core-v{position:relative;width:150px;margin:0 auto;border-radius:22px;overflow:hidden;border:3px solid rgba(255,255,255,.85);box-shadow:0 0 0 10px rgba(142,197,255,.12),0 30px 60px -20px rgba(0,0,0,.6);animation:tvxPulse 2.6s infinite}
.tpv-core-v img{display:block;width:100%;height:auto}
.tpv-core-v span{position:absolute;left:50%;top:50%;width:52px;height:52px;margin:-26px 0 0 -26px;border-radius:50%;background:rgba(255,255,255,.92);color:#13294b;display:flex;align-items:center;justify-content:center}
.tpv-core-v span svg{width:22px;height:22px;margin-left:3px;fill:#13294b}
.tpv-core p{margin:12px 0 0!important;font-weight:800;color:#fff;letter-spacing:.06em;text-transform:uppercase;font-size:13px}
.tpv-local{display:flex;align-items:center;justify-content:center;gap:10px;margin:34px auto 0!important;max-width:760px;text-align:center;color:#dbe7f8;font-weight:700;font-size:16px}
.tpv-local .tvx-svg{color:#ffc53d;flex:none}
/* storyboard */
.tpv-sb{max-width:980px;margin:0 auto;padding:26px;border-radius:24px;background:#fff;border:1px solid #dfe8f6;box-shadow:0 22px 44px -32px rgba(9,30,66,.45)}
.tpv-sb-h{display:flex;align-items:center;gap:14px;margin-bottom:20px}
.tpv-sb-h p{margin:0!important;font-size:12.5px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--blue)}
.tpv-sb-h h3{font-size:24px;margin:0!important}
.tpv-sb ol{list-style:none;margin:0!important;padding:0!important;display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.tpv-sb li{position:relative;margin:0!important;padding:16px 16px 18px;border-radius:16px;background:linear-gradient(160deg,#13294b,#1d5fbf);color:#fff;min-height:132px;animation:tvxPop .5s both;animation-delay:calc(var(--d)*.12)}
.tpv-sb li:nth-child(2){background:linear-gradient(160deg,#173b74,#2f7de1)}.tpv-sb li:nth-child(3){background:linear-gradient(160deg,#0f5d63,#16a37a)}
.tpv-sb li em{display:inline-block;font-style:normal;font-size:12px;font-weight:800;padding:3px 8px;border-radius:7px;background:rgba(255,255,255,.18);margin-bottom:28px}
.tpv-sb li b{display:block;font-size:19px;line-height:1.2}
.tpv-sb li span{display:block;font-size:14.5px;line-height:1.4;color:#d4e3f7;margin-top:3px}
.tpv-sb li:after{content:"";position:absolute;right:14px;top:14px;width:22px;height:16px;border:2px solid rgba(255,255,255,.4);border-radius:4px}
.tpv-cap{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:18px 0 0!important;padding:14px 16px;border-radius:14px;background:#f4f7fb;color:var(--navy)}
.tpv-cap b{font-size:19px}.tpv-cap span{margin-left:auto;font-size:12.5px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--mut)}
.tpv-cap .tvx-svg{color:var(--blue)}
@media (max-width:1100px){.tpv-c2{right:-10px}}
@media (max-width:900px){
 .tpv-stage{grid-template-columns:1fr;gap:22px}.tpv-frame-w{height:380px}.tpv-frame{--s:.8}.tpv-fi{text-align:center}.tpv-where{justify-content:center}.tpv-fi h3{font-size:24px}
 .tpv-hub{grid-template-columns:1fr;gap:18px;max-width:480px}.tpv-core{order:-1}.tpv-core-v{width:120px}
 .tpv-node,.tpv-r .tpv-node{margin:0}.tpv-node:after{display:none}.tpv-col{gap:12px}
 .tpv-sb{padding:18px}.tpv-sb ol{grid-template-columns:1fr}.tpv-sb li{min-height:0;display:grid;grid-template-columns:auto 1fr;gap:2px 12px;align-items:center}
 .tpv-sb li em{grid-row:span 2;margin:0}.tpv-sb li:after{display:none}
 .tpv-ind .tvx-tabs{-webkit-mask-image:linear-gradient(90deg,#000 85%,transparent);mask-image:linear-gradient(90deg,#000 85%,transparent);flex-wrap:nowrap;justify-content:flex-start;overflow-x:auto;padding:4px 2px 10px;margin-left:-4px;margin-right:-4px;scrollbar-width:none}.tpv-ind .tvx-tabs::-webkit-scrollbar{display:none}.tpv-ind .tvx-tab{flex:none}
}
@media (max-width:420px){.tpv-frame-w{height:300px}.tpv-frame{--s:.6}.tpv-fmt[data-cur="r169"] .tpv-frame{--s:.5}.tpv-fmt .tvx-tab{padding:9px 12px!important;font-size:13.5px!important}.tpv-cap span{margin-left:0}.tpv-local{font-size:14.5px;align-items:flex-start;text-align:left}}
@media (max-width:340px){.tpv-fmt[data-cur="r169"] .tpv-frame{--s:.46}}
'''

if __name__ == "__main__":
    K.page("Promo Video", "promo-video",
           "Promo Videos and Reels for Local Businesses | Three Village Local",
           "Short promo videos and reels for Three Village and Port Jefferson businesses: filmed at your place, edited with music and captions, sized for Reels, TikTok, Facebook and your website, then shared with 100,000+ local views a month.",
           "Promo videos that show off your business",
           [HERO, NAV, GET, FORMATS, HOW, REACH, IDEAS, FAQ, REL, CTA], bundle="video", css=CSS)
    K.main()
