"""Email and articles service page: weekly email spotlights + custom articles / blog features.
Owner 11/12/2026: every service on /services gets its own premium interactive page. No prices.
    python site/email-articles-page/build.py          -> widget "3VL Page Email Articles Preview" + hidden /preview-email-articles (noindex)
    (--live -> /email-articles only after the owner's OK)"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "svc-kit"))
import kit as K
from kit import ic, SV, WB

MAIL = '''<div class="tea-mail"><div class="tea-mail-s"><div class="tea-mail-t">
  <div class="tea-mh"><b>Three Village Weekly</b><span>Friday</span></div>
  <div class="tea-mhero"><img src="''' + WB + '''lm-setauket-main-v2.webp" alt="Main Street in Setauket in the fall" width="640" height="760" fetchpriority="high"><p><i>This weekend</i>Fall colors, live music and a new favorite on Main Street</p></div>
  <div class="tea-spot"><em>''' + ic("star") + '''Neighbor spotlight</em><div class="tea-spot-r"><img src="''' + WB + '''mock-croissants-3q.webp" alt="" loading="lazy" width="380" height="292"><div><b>Your Business</b><i>Meet the family behind Main Street&#39;s favorite spot.</i><u>Read the story</u></div></div></div>
  <div class="tea-ev"><span><b>SAT</b>14</span><div><b>Holiday craft fair</b><i>Village green &middot; 10 AM</i></div></div>
  <div class="tea-ev"><span><b>SUN</b>15</span><div><b>Live music and brunch</b><i>Main Street &middot; 11 AM</i></div></div>
  <p class="tea-mfoot">Also in the free mobile app and on social</p>
</div></div></div>'''

HERO_VIS = '''<div class="tea-hv">
  <div class="tea-toast">''' + '<span class="tvx-ic">' + ic("mail") + '''</span><div><p><b>Three Village Local</b><em>now</em></p><p>Neighbor spotlight: meet Your Business</p></div></div>
  ''' + MAIL + '''
  <div class="tvx-chip tea-c2" style="animation-delay:1.6s"><span class="tvx-ic">''' + ic("link") + '''</span><div><b>One tap</b>to your page and website</div></div>
</div>'''

HERO = K.hero("Email and articles", "Stories the community", "actually reads.",
              "Get featured in our weekly email and in custom articles on Three Village Local, so neighbors learn the story behind your business, then share it all over town.",
              HERO_VIS, ("See the email", "#tvp-email"))

NAV = K.snav([("get", "What you get"), ("email", "The email"), ("article", "The article"), ("included", "What&#39;s included"), ("how", "How it works"), ("faq", "FAQ")])

GET = K.sec("get", "What you get", "Your story, told well and seen everywhere.",
            "People choose a business they feel they know. We make sure they know yours.",
            K.cards([("mail", "Weekly email spotlight", "Your business featured in our weekly email: a big photo, a few warm lines and one tap to your page."),
                     ("article", "Custom article feature", "A full story on Three Village Local about the people behind your business, written by our team."),
                     ("share", "Shared all over town", "Every feature is shared on our Facebook and Instagram, our website and our free mobile app.")], 3))

PARTS = [("subj", "1", "Your name in the subject line", "The first thing neighbors see in their inbox is your business name, which is what gets the email opened."),
         ("photo", "2", "Your best photo, big and bright", "A real photo of your place, your people or your work. We use yours or help you get a great one."),
         ("story", "3", "Your story in a few warm lines", "Short, friendly and specific: what you do, who is behind it and why neighbors will love it."),
         ("button", "4", "One tap to your page", "A clear button to your story, website, menu or booking page, so interest turns into a visit.")]
ptabs = "".join('<button class="tvx-tab tea-pt%s" data-tab="%s"><b>%s</b><span>%s</span></button>' % (" on" if n == 0 else "", k, num, t) for n, (k, num, t, d) in enumerate(PARTS))
ppan = "".join('<p class="tea-pd" data-panel="%s">%s</p>' % (k, d) for k, num, t, d in PARTS)
ANAT = K.sec("email", "Inside the email", "Every spotlight is built to be opened and clicked.",
             "Tap through the four parts of a spotlight.",
             '''<div class="tea-anat tvs-up" data-tabs data-auto="3600">
    <div class="tea-amock" aria-hidden="true">
      <div class="tea-ain"><p class="tea-a-from"><i></i><b>Three Village Local</b><em>Fri</em></p><p class="tea-a-subj">Neighbor spotlight: meet Your Business</p></div>
      <div class="tea-abody"><div class="tea-a-photo"><img src="''' + WB + '''mock-latte-3q.webp" alt="" loading="lazy" width="380" height="365"><span class="tea-hs" data-go="photo">2</span></div>
        <div class="tea-a-story"><b>Meet the family behind Your Business</b><p>For twenty years, the Rivera family has opened their doors before sunrise. Here is what keeps neighbors coming back...</p><span class="tea-hs" data-go="story">3</span></div>
        <p class="tea-a-btn"><u>Read the story</u><span class="tea-hs" data-go="button">4</span></p></div>
      <span class="tea-hs tea-hs1" data-go="subj">1</span>
    </div>
    <div class="tea-aside"><div class="tvx-tabs">''' + ptabs + '''</div>''' + ppan + '''</div>
  </div>''')

ART = K.sec("article", "Custom articles", "A feature story that keeps working for you.",
            "Articles live on Three Village Local, where neighbors and search engines can find them long after the email goes out.",
            '''<div class="tea-art tvs-up">
    <div class="tea-br" data-run><p class="tea-bar"><i></i><i></i><i></i><span>''' + ic("search") + '''<em>threevillagelocal.com/blog/meet-your-business</em></span></p><p class="tea-prog"><u></u></p>
      <div class="tea-page"><div class="tea-scroll">
        <p class="tea-k">Neighbor spotlight</p><h3>Meet the family behind Your Business</h3><p class="tea-by"><i></i>By Three Village Local &middot; 4 min read</p>
        <img class="tea-hero" src="''' + WB + '''lm-setauket-harbor-v2.webp" alt="Setauket Harbor on a sunny day" loading="lazy" width="640" height="420">
        <p class="tea-p">Long before the first customer walks in, the lights are already on. For the family behind Your Business, mornings start early and end with a lot of familiar faces.</p>
        <blockquote>&ldquo;We wanted a place where everyone feels like a regular.&rdquo;</blockquote>
        <div class="tea-l"><u></u><u></u><u class="s"></u></div>
        <div class="tea-g"><img src="''' + WB + '''mock-coffee.webp" alt="" loading="lazy" width="300" height="368"><img src="''' + WB + '''mock-croissant-a.webp" alt="" loading="lazy" width="380" height="238"></div>
        <div class="tea-l"><u></u><u class="s"></u></div>
        <div class="tea-biz"><b>Visit Your Business</b><i>''' + ic("pin") + '''Main Street, Setauket</i><p><span>Call</span><span>Website</span><span>Directions</span></p></div>
      </div></div></div>
    <ul class="tea-why">
      <li>''' + ic("globe") + '''<div><b>Stays up on our site</b>Neighbors can find your story any time, not just the week it runs.</div></li>
      <li>''' + ic("link") + '''<div><b>A real link to your website</b>A mention on a trusted local site helps Google and AI tools understand who you are.</div></li>
      <li>''' + ic("share") + '''<div><b>Shared everywhere we are</b>Facebook, Instagram, the weekly email and our free mobile app.</div></li>
      <li>''' + ic("heart") + '''<div><b>Yours to share</b>Post it, frame it, link to it from your own site and social media.</div></li>
    </ul>
  </div>''')

INC = K.sec("included", "What&#39;s included", "We do the work. You get the spotlight.", "",
            K.cards([("message", "A friendly interview", "A short chat, in person or by phone, about your story and what makes you different."),
                     ("edit", "Written by our team", "Warm, clear and local, in a voice neighbors trust. You approve every word."),
                     ("camera", "Great photos", "We use your best photos or help you get new ones."),
                     ("mail", "Your name up front", "Your business name in the email subject line and the article headline."),
                     ("link", "Links that matter", "To your website, your Three Village Local listing, your menu or booking page."),
                     ("phone", "Everywhere at once", "Shared on Facebook, Instagram, our website and our free mobile app.")], 3))

STATS = '<section class="tvs-sec tvx-sec" id="tvp-reach">' + K.stats_band("Your story, in front of the whole community.", "Reach") + '</section>'

HOW = K.sec("how", "How it works", "From hello to headline in four steps.", "",
            K.steps([("Chat", "A short interview about your business, your people and your story."),
                     ("Write", "Our team writes your spotlight and article and picks the photos."),
                     ("Approve", "You read it first and ask for any changes."),
                     ("Publish and share", "It goes out in the email, on our site, on social and in the mobile app.")]))

FAQ = K.faq([
    ("Who writes the email spotlight and the article?", "Our team does, after a short, friendly interview with you. You read everything first and nothing is published until you approve it."),
    ("Can I use my own photos?", "Yes. Your own photos are often the best. If you need new ones, we can help you get them."),
    ("Where will my feature be seen?", "In our weekly email, on Three Village Local (45,000+ website page visits a month), on our Facebook and Instagram (100,000+ local views a month) and in our free mobile app."),
    ("Can I link to the article from my own website?", "Please do. Share it on your website, social media, newsletter and in-store. It is your story."),
    ("Do articles help with Google and AI search?", "A feature on a trusted local site, with a link to your website, is the kind of signal that helps Google and AI tools understand who you are and where you work."),
    ("How do I get started?", "Fill out the short form below. We&#39;ll send a free, personalized plan by email, with no pressure and no contract."),
])

REL = K.related("email-articles", ["social-media", "promo-video", "ai-search", "new-business-launch", "join", "websites"])
CTA = K.cta("Every business has a story", "Let&#39;s tell yours to the whole town.", "Tell us about your business and we&#39;ll send a free plan by email.")

JS = ''';(function(){var a=document.querySelector('.tea-anat');if(!a)return;[].forEach.call(a.querySelectorAll('.tea-hs'),function(h){h.addEventListener('click',function(){var t=a.querySelector('.tvx-tab[data-tab="'+h.getAttribute('data-go')+'"]');if(t)t.click();});});})();'''

CSS = '''
.tea-hv{position:relative;width:100%;max-width:440px;padding:40px 0 10px}
.tea-toast{position:relative;z-index:5;display:flex;gap:11px;align-items:center;width:88%;margin:0 auto -18px;padding:11px 14px;border-radius:16px;background:rgba(255,255,255,.96);box-shadow:0 22px 44px -20px rgba(9,30,66,.5),0 0 0 1px rgba(15,42,82,.06);animation:teaToast 9s cubic-bezier(.2,.8,.2,1) infinite}
.tea-toast .tvx-ic{width:38px;height:38px;border-radius:11px;background:#13294b;color:#ffc53d}.tea-toast .tvx-svg{width:20px;height:20px}
.tea-toast p{margin:0!important;font-size:13.5px;line-height:1.35;color:var(--ink2)}.tea-toast p:first-child{display:flex;justify-content:space-between;gap:8px}.tea-toast b{color:var(--navy)}.tea-toast em{font-style:normal;color:#9aa6b6;font-size:12px}
@keyframes teaToast{0%{opacity:0;transform:translateY(-24px) scale(.95)}6%,88%{opacity:1;transform:none}96%,100%{opacity:0;transform:translateY(-10px) scale(.97)}}
.tea-mail{position:relative;height:470px;border-radius:22px;background:#fff;box-shadow:0 40px 80px -40px rgba(9,30,66,.6),0 0 0 1px rgba(15,42,82,.08);overflow:hidden}
.tea-mail-s{position:absolute;inset:0;overflow:hidden}
.tea-mail-t{animation:teaScroll 18s ease-in-out infinite}
@keyframes teaScroll{0%,18%{transform:translateY(0)}45%,70%{transform:translateY(-190px)}92%,100%{transform:translateY(0)}}
.tea-mh{display:flex;align-items:center;justify-content:space-between;padding:30px 18px 14px;background:#13294b;color:#fff}.tea-mh b{font-size:17px}.tea-mh span{font-size:12px;font-weight:800;color:#ffc53d;letter-spacing:.08em;text-transform:uppercase}
.tea-mhero{position:relative;height:210px;overflow:hidden}.tea-mhero img{width:100%;height:100%;object-fit:cover;display:block}
.tea-mhero p{position:absolute;left:0;right:0;bottom:0;margin:0!important;padding:40px 18px 14px;background:linear-gradient(180deg,transparent,rgba(9,24,52,.85));color:#fff;font-weight:800;font-size:18px;line-height:1.25}
.tea-mhero i{display:block;font-style:normal;font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;color:#ffc53d;margin-bottom:3px}
.tea-spot{margin:14px;padding:12px;border-radius:16px;background:linear-gradient(120deg,#eef5ff,#fff8e6);border:1px solid #f2dca0;box-shadow:0 0 0 0 rgba(255,197,61,.5);animation:teaGlow 3s ease-in-out infinite}
@keyframes teaGlow{0%,100%{box-shadow:0 0 0 0 rgba(255,197,61,.45)}50%{box-shadow:0 0 0 7px rgba(255,197,61,0)}}
.tea-spot em{display:inline-flex;align-items:center;gap:5px;font-style:normal;font-size:11.5px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#a16207;margin-bottom:8px}.tea-spot em .tvx-svg{width:14px;height:14px;fill:#ffc53d;color:#c27c0e}
.tea-spot-r{display:flex;gap:12px;align-items:center}.tea-spot-r img{width:92px;height:78px;object-fit:cover;border-radius:12px;flex:none;background:#f4ece0}
.tea-spot b{display:block;font-size:16.5px;color:var(--navy)}.tea-spot i{display:block;font-style:normal;font-size:13px;line-height:1.4;color:var(--ink2);margin:2px 0 6px}
.tea-spot u{display:inline-block;padding:6px 12px;border-radius:999px;background:#1d5fbf;color:#fff;font-size:12.5px;font-weight:800;text-decoration:none}
.tea-ev{display:flex;gap:12px;align-items:center;margin:0 14px 10px;padding:10px;border-radius:12px;background:#f6f9fd}
.tea-ev>span{width:44px;flex:none;text-align:center;border-radius:10px;background:#fff;border:1px solid #e3e9f1;padding:4px 0;font-weight:800;font-size:18px;color:var(--navy);line-height:1.05}.tea-ev>span b{display:block;font-size:10px;color:#c2410c;letter-spacing:.08em}
.tea-ev div b{display:block;font-size:14.5px;color:var(--navy)}.tea-ev div i{font-style:normal;font-size:12.5px;color:var(--mut)}
.tea-mfoot{margin:6px 14px 14px!important;text-align:center;font-size:12.5px;color:var(--mut)}
.tea-c1{left:-34px;top:46%}.tea-c2{right:-30px;bottom:8%}
/* anatomy */
.tea-anat{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:center;max-width:1000px;margin:0 auto}
.tea-amock{position:relative;border-radius:22px;background:#fff;border:1px solid #dfe8f6;box-shadow:0 30px 60px -36px rgba(9,30,66,.55);overflow:visible}
.tea-ain{padding:16px 18px;border-bottom:1px solid #edf1f6}
.tea-a-from{display:flex;align-items:center;gap:8px;margin:0 0 6px!important;font-size:13.5px}.tea-a-from i{width:26px;height:26px;border-radius:50%;background:#13294b;border:2px solid #ffc53d}.tea-a-from b{color:var(--navy)}.tea-a-from em{margin-left:auto;font-style:normal;color:#9aa6b6;font-size:12.5px}
.tea-a-subj{margin:0!important;font-weight:800;font-size:16.5px;color:var(--navy);padding:6px 8px;border-radius:10px;transition:box-shadow .3s,background .3s}
.tea-abody{padding:16px 18px 20px}
.tea-a-photo{position:relative;border-radius:14px;transition:box-shadow .3s}.tea-a-photo img{display:block;width:100%;height:190px;object-fit:cover;border-radius:14px;background:#f4ece0}
.tea-a-story{position:relative;margin:14px 0 12px;padding:8px;border-radius:12px;transition:box-shadow .3s,background .3s}
.tea-a-story b{display:block;font-size:17px;color:var(--navy);margin-bottom:4px}.tea-a-story p{margin:0!important;font-size:14px;line-height:1.5;color:var(--ink2)}
.tea-a-btn{position:relative;display:inline-block;margin:0 0 0 8px!important;padding:4px;border-radius:999px;transition:box-shadow .3s}
.tea-a-btn u{display:inline-block;padding:10px 18px;border-radius:999px;background:#1d5fbf;color:#fff;font-weight:800;font-size:14px;text-decoration:none}
.tea-anat[data-cur="subj"] .tea-a-subj,.tea-anat[data-cur="story"] .tea-a-story{background:#fff8e6;box-shadow:0 0 0 3px #ffc53d}
.tea-anat[data-cur="photo"] .tea-a-photo,.tea-anat[data-cur="button"] .tea-a-btn{box-shadow:0 0 0 4px #ffc53d}
.tea-hs{position:absolute;z-index:3;width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:#13294b;color:#fff;font-weight:800;font-size:14px;cursor:pointer;box-shadow:0 0 0 4px rgba(19,41,75,.15);transition:transform .25s,background .25s}
.tea-a-photo .tea-hs{right:-12px;top:-12px}.tea-a-story .tea-hs{right:-12px;top:-10px}.tea-a-btn .tea-hs{right:-34px;top:8px}.tea-hs1{left:-12px;top:44px}
.tea-anat[data-cur="subj"] .tea-hs1,.tea-anat[data-cur="photo"] .tea-a-photo .tea-hs,.tea-anat[data-cur="story"] .tea-a-story .tea-hs,.tea-anat[data-cur="button"] .tea-a-btn .tea-hs{background:#ffc53d;color:#13294b;transform:scale(1.15);animation:tvxPulse 1.6s infinite}
.tea-aside .tvx-tabs{flex-direction:column;align-items:stretch;margin:0 0 14px}
.tvx .tea-pt{justify-content:flex-start;gap:12px;padding:14px 16px!important;border-radius:16px!important;text-align:left;font-size:16px!important}
.tea-pt b{flex:none;width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:#e7f0ff;color:var(--blue);font-size:14px}
.tvx .tea-pt.on b{background:#ffc53d;color:#13294b}
.tea-pd{margin:0!important;padding:16px 18px;border-radius:16px;background:#f4f7fb;font-size:16px;line-height:1.6;color:var(--ink2)}
/* article */
.tea-art{display:grid;grid-template-columns:1.15fr .85fr;gap:40px;align-items:center;max-width:1080px;margin:0 auto}
.tea-br{position:relative;border-radius:18px;background:#fff;box-shadow:0 40px 80px -44px rgba(9,30,66,.6),0 0 0 1px rgba(15,42,82,.08);overflow:hidden}
.tea-bar{display:flex;align-items:center;gap:6px;margin:0!important;padding:10px 14px;background:#eef2f7;border-bottom:1px solid #e1e8f2}
.tea-bar i{width:9px;height:9px;border-radius:50%;background:#ff7b6b;flex:none}.tea-bar i:nth-child(2){background:#ffc85a}.tea-bar i:nth-child(3){background:#4bd18a}
.tea-bar span{margin-left:10px;flex:1;min-width:0;display:flex;align-items:center;gap:6px;padding:4px 12px;border-radius:999px;background:#fff;font-size:12px;color:#7a8696;white-space:nowrap;overflow:hidden}.tea-bar .tvx-svg{width:13px;height:13px;flex:none}.tea-bar em{font-style:normal;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap!important}
.tea-prog{position:relative;height:3px;margin:0!important;background:#edf1f6}.tea-prog u{position:absolute;left:0;top:0;bottom:0;width:100%;background:linear-gradient(90deg,#1d5fbf,#2fd28a);transform-origin:left;animation:teaProg 16s ease-in-out infinite}
@keyframes teaProg{0%,8%{transform:scaleX(.05)}80%,90%{transform:scaleX(1)}100%{transform:scaleX(.05)}}
.tea-page{position:relative;height:440px;overflow:hidden}
.tea-scroll{padding:22px 26px;animation:teaArt 16s ease-in-out infinite}
@keyframes teaArt{0%,8%{transform:translateY(0)}80%,90%{transform:translateY(-470px)}100%{transform:translateY(0)}}
.tea-k{margin:0 0 6px!important;font-size:12px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:#c2410c}
.tea-scroll h3{font-size:26px;line-height:1.15;margin:0 0 8px!important;font-family:Georgia,serif;letter-spacing:-.01em}
.tea-by{display:flex;align-items:center;gap:8px;margin:0 0 14px!important;font-size:13px;color:var(--mut)}.tea-by i{width:22px;height:22px;border-radius:50%;background:#13294b;border:2px solid #ffc53d}
.tea-hero{display:block;width:100%;height:200px;object-fit:cover;border-radius:12px;margin-bottom:14px}
.tea-p{margin:0 0 12px!important;font-size:15px;line-height:1.65;color:var(--ink2);font-family:Georgia,serif}
.tea-scroll blockquote{margin:0 0 14px!important;padding:6px 0 6px 16px;border-left:4px solid #ffc53d;font-family:Georgia,serif;font-size:20px;line-height:1.35;color:var(--navy);font-style:italic}
.tea-l{margin-bottom:14px}.tea-l u{display:block;height:9px;border-radius:5px;background:#edf1f6;margin-bottom:8px;text-decoration:none}.tea-l u.s{width:65%}
.tea-g{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:14px}.tea-g img{width:100%;height:120px;object-fit:cover;border-radius:10px;display:block;background:#f4ece0}
.tea-biz{padding:14px;border-radius:14px;background:#f4f7fb;border:1px solid #e3e9f1}.tea-biz b{display:block;font-size:16px;color:var(--navy)}
.tea-biz i{display:flex;align-items:center;gap:5px;font-style:normal;font-size:13px;color:var(--mut);margin:3px 0 10px}.tea-biz i .tvx-svg{width:14px;height:14px}
.tea-biz p{display:flex;gap:6px;margin:0!important}.tea-biz span{padding:6px 12px;border-radius:999px;background:#1d5fbf;color:#fff;font-size:12.5px;font-weight:800}.tea-biz span+span{background:#fff;color:var(--navy);border:1px solid #d3dff0}
.tea-why{list-style:none;margin:0!important;padding:0!important;display:grid;gap:12px}
.tea-why li{display:flex;gap:14px;align-items:flex-start;margin:0!important;padding:16px;border-radius:18px;background:#fff;border:1px solid #dfe8f6}
.tea-why li>.tvx-svg{flex:none;width:42px;height:42px;padding:10px;border-radius:12px;background:#e7f0ff;color:var(--blue)}
.tea-why b{display:block;font-size:16.5px;color:var(--navy);margin-bottom:2px}.tea-why div{font-size:14.5px;line-height:1.5;color:var(--mut)}
@media (max-width:1100px){.tea-c1{left:-10px}.tea-c2{right:-10px}}
@media (max-width:900px){
 .tea-hv{padding-top:30px}.tea-mail{height:430px}
 .tea-anat,.tea-art{grid-template-columns:1fr;gap:24px}
 .tea-aside .tvx-tabs{display:grid;grid-template-columns:1fr 1fr;gap:8px}.tvx .tea-pt{padding:11px 12px!important;font-size:14px!important;gap:9px}.tea-pt b{width:26px;height:26px;font-size:13px}
 .tea-amock{margin:0 10px}.tea-a-photo img{height:160px}
 .tea-page{height:400px}.tea-scroll{padding:18px}
}
@media (max-width:420px){.tea-mail{height:400px}.tea-mhero{height:170px}.tea-toast{width:94%}.tea-a-btn .tea-hs{right:-30px}.tvx .tea-pt{font-size:13px!important;line-height:1.25!important}.tea-scroll h3{font-size:22px}.tea-page{height:380px}}
'''

if __name__ == "__main__":
    K.page("Email Articles", "email-articles",
           "Weekly Email Spotlights and Custom Articles for Local Businesses | Three Village Local",
           "Get your business featured in the Three Village Local weekly email and in custom articles neighbors read, then shared on Facebook, Instagram, our website and our free mobile app.",
           "Stories the community actually reads",
           [HERO, NAV, GET, ANAT, ART, INC, STATS, HOW, FAQ, REL, CTA], bundle="email_articles", css=CSS, js=JS, fb_image="/share/svc-email-articles-v1.jpg")
    K.main()
