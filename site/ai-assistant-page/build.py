"""AI add-ons for an EXISTING website (owner 11/3/2026): stand-alone AI Chat Assistant + AI Website Optimization for sites built and hosted by
someone else. Same look as /websites: imports that page's build and swaps the sections.
    python site/ai-assistant-page/build.py          -> widget "3VL Page AI Assistant Preview" + hidden /preview-ai-assistant
    python site/ai-assistant-page/build.py --live   -> widget "3VL Page AI Assistant" + /ai-assistant (indexable)"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "websites-page"))
import build as W
from build import D, rep, cut, swap, sec

# prices: (setup, monthly) walk-in / member. Owner 11/3: the AI Tune-Up is included in the assistant setup (one package).
CHAT = {"all": (1199, 199), "member": (799, 149)}

D.NAME = "3VL Page AI Assistant" if D.LIVE else "3VL Page AI Assistant Preview"
D.SLUG = "ai-assistant" if D.LIVE else "preview-ai-assistant"
D.TITLE = "Your Digital Front Desk: AI Assistant + AI Website Optimization | Three Village Local"
D.DESC = ("Add a smart AI assistant to the website you already have. It answers customers 24/7 and sends you every lead. "
          "Plus AI Website Optimization built to get your business noticed and recommended by ChatGPT, Google and other AI tools. Works with Wix, Squarespace, WordPress and more.")
D.FB_TITLE = "Turn your website into a 24/7 lead machine."
HOW = "/ai-assistant-how-it-works" if D.LIVE else "/preview-ai-assistant-how"

DEMO = W.sec(W.HTML, "tvs-sec tvw-bot")
DEMO = W.HTML[DEMO[0]:DEMO[1]]
DEMO = DEMO[DEMO.index('<div class="tvw-bot-demo'):DEMO.rindex('</div>\n  </div>\n</section>')] + "</div>"   # the animated example chat + lead card (keep its own closing div)

HERO = '''<section class="tvs-hero">
  <div class="tvw-hvis tva-hvis"><div class="tva-try"><p class="tva-try-k"><span></span>How it looks on your website</p><div class="tva-mock" aria-hidden="true"><div class="tva-mock-bar"><i></i><i></i><i></i><span>yourbusiness.com</span></div><div class="tva-mock-page"><b></b><p></p><p></p><p class="s"></p><div class="tva-mock-row"><u></u><u></u><u></u></div><p></p><p class="s"></p></div><div class="tva-mock-chat">''' + DEMO + '''</div></div><div class="tva-float tva-f1"><b>&#128241;</b><div><em>New lead</em>Dana, weekend cleanup quote</div></div><div class="tva-float tva-f2"><b>&#9889;</b><div><em>Answered in seconds</em>10:42 PM, Sunday</div></div><div class="tva-float tva-f3"><b>&#10003;</b><div><em>Found by AI</em>AI optimization included</div></div></div></div>
  <div class="tvs-hin tvs-up">
    <p class="tvs-kick"><span class="tvs-dot"></span>Your Digital Front Desk</p>
    <h1>Turn your website<br><span>into a 24/7 lead machine.</span></h1>
    <p class="tvs-sub">Add a smart AI assistant to your current website. It answers customers the second they ask, day or night, and sends you every lead. Plus AI Website Optimization so your site gets noticed and recommended by AI. No new website needed.</p>
    <div class="tvs-ctas">
      <a class="tvs-btn tvs-blue" href="#" data-tva-open>Try the live demo</a>
      <a class="tvs-btn tvs-ghost" href="#tvs-bundles">See pricing</a>
    </div>
    <a class="tva-how" href="''' + HOW + '''">How does it work? See our process &rarr;</a>
    <ul class="tvs-trust">
      <li><b>No new</b>website needed</li>
      <li><b>About 7 days</b>to go live</li>
      <li><b>Every lead</b>sent to you</li>
    </ul>
  </div>
</section>'''

NEXT = '''<section class="tvs-sec tva-next" id="tva-next">
  <div class="tvs-head tvs-up">
    <p class="tvs-eyebrow">The next big thing for websites</p>
    <h2>Websites are learning to talk.</h2>
    <p>For 25 years, websites just sat there. Customers had to dig for answers, then call during business hours or give up. Now people are used to asking AI a question and getting an answer right away. The business that answers first usually wins the customer. An AI assistant makes sure that is you, even at 10 PM on a Sunday.</p>
  </div>
  <div class="tva-why tvs-up">
    <div><b>&#127769;</b><h3>Your customers shop after hours</h3><p>Nights and weekends are when people finally have time to look. Your assistant is there when you can&#39;t pick up.</p></div>
    <div><b>&#9889;</b><h3>Speed wins the job</h3><p>People reach out to more than one business. The first one to answer is usually the one they hire.</p></div>
    <div><b>&#128682;</b><h3>Most visitors leave quietly</h3><p>Most people never call or fill out a form. A friendly &ldquo;Can I help?&rdquo; turns browsers into real leads.</p></div>
  </div>
</section>'''

FEAT = '''<section class="tvs-sec tva-feat" id="tva-feat">
  <div class="tvs-head tvs-up">
    <p class="tvs-eyebrow">Your Digital Front Desk</p>
    <h2>Smart, friendly, and it never misses a lead.</h2>
    <p>We build your assistant, teach it your business, and add it to your site. You just watch the leads come in.</p>
  </div>
  <div class="tva-grid">
    <div class="tva-c tvs-up"><span>&#128172;</span><h3>Answers instantly, 24/7</h3><p>Hours, prices, services, service area, parking, policies: anything you teach it, answered in seconds.</p></div>
    <div class="tva-c tvs-up"><span>&#128241;</span><h3>Captures every lead</h3><p>Name, phone and what they need, sent to your email or phone the moment they ask.</p></div>
    <div class="tva-c tvs-up"><span>&#128197;</span><h3>Books and quotes</h3><p>Sends people straight to your booking calendar, quote form or online ordering.</p></div>
    <div class="tva-c tvs-up"><span>&#129504;</span><h3>Knows your business and your industry</h3><p>Custom built after we research your business, your industry, your competition and its rules. It answers from your approved information.</p></div>
    <div class="tva-c tvs-up"><span>&#129309;</span><h3>Live person, instantly</h3><p>If someone asks for a real person, you get an instant text and email with their name, number and what they need.</p></div>
    <div class="tva-c tvs-up"><span>&#128202;</span><h3>Monthly summary</h3><p>See what customers asked, how many leads came in, and what to add next. We keep it sharp for you.</p></div>
  </div>
  <div class="tva-reg tvs-up"><span>&#9878;&#65039;</span><div><b>Built for every kind of business, including regulated ones.</b><p>Restaurants, shops, home services and small businesses, plus law firms, financial advisors, insurance, mortgage, accounting and medical offices. We set up every assistant to follow your industry&#39;s regulations and guidelines: general information only (never legal, financial or medical advice), the right disclaimers, only the wording and rates you approve, no sensitive information collected, and anything specific goes straight to you. You approve it before it goes live.</p></div></div>
</section>'''

WORKS = '''<section class="tvs-sec tva-plat">
  <div class="tva-works tvs-up"><p>Works on the website you already have</p><div><span><svg aria-hidden="true" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path fill="#0C6EFC" d="m0 7.354 2.113 9.292h.801a1.54 1.54 0 0 0 1.506-1.218l1.351-6.34a.171.171 0 0 1 .167-.137c.08 0 .15.058.167.137l1.352 6.34a1.54 1.54 0 0 0 1.506 1.218h.805l2.113-9.292h-.565c-.62 0-1.159.43-1.296 1.035l-1.26 5.545-1.106-5.176a1.76 1.76 0 0 0-2.19-1.324c-.639.176-1.113.716-1.251 1.365l-1.094 5.127-1.26-5.537A1.33 1.33 0 0 0 .563 7.354H0zm13.992 0a.951.951 0 0 0-.951.95v8.342h.635a.952.952 0 0 0 .951-.95V7.353h-.635zm1.778 0 3.158 4.66-3.14 4.632h1.325c.368 0 .712-.181.918-.486l1.756-2.59a.12.12 0 0 1 .197 0l1.754 2.59c.206.305.55.486.918.486h1.326l-3.14-4.632L24 7.354h-1.326c-.368 0-.712.181-.918.486l-1.772 2.617a.12.12 0 0 1-.197 0L18.014 7.84a1.108 1.108 0 0 0-.918-.486H15.77z"/></svg>Wix</span><span><svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 204"><path fill="#1a1918" d="M162.931 40.67c-4.823-4.824-12.644-4.824-17.464 0L66.87 119.268c-9.651 9.643-25.287 9.643-34.931 0c-9.654-9.647-9.654-25.285 0-34.937L109.023 7.25c-9.646-9.649-25.288-9.649-34.934 0L14.467 66.87c-19.29 19.294-19.29 50.57 0 69.866c19.295 19.295 50.57 19.295 69.865 0l78.599-78.599c4.82-4.823 4.82-12.644 0-17.467m26.199-26.197c-19.295-19.297-50.57-19.297-69.865 0L40.67 93.067c-4.82 4.82-4.82 12.646 0 17.467c4.823 4.823 12.64 4.823 17.464 0l78.602-78.594c9.646-9.649 25.282-9.649 34.926 0c4.828 4.82 12.646 4.82 17.469 0c4.823-4.828 4.823-12.644 0-17.467m26.201 78.594c-4.823-4.818-12.646-4.818-17.469 0l-78.597 78.597c-9.646 9.646-25.287 9.646-34.933 0c-4.82-4.82-12.639-4.82-17.462 0c-4.83 4.825-4.83 12.646 0 17.464c19.287 19.295 50.57 19.295 69.865 0l78.596-78.594c4.82-4.82 4.82-12.646 0-17.467m26.202-26.196c-19.295-19.292-50.575-19.292-69.865 0L93.066 145.47c-4.823 4.818-4.823 12.644 0 17.464c4.826 4.826 12.647 4.826 17.467 0l78.597-78.597c9.643-9.648 25.287-9.648 34.931 0c9.646 9.647 9.646 25.285 0 34.932l-77.084 77.086c9.646 9.643 25.28 9.643 34.934 0l59.622-59.62c19.29-19.297 19.29-50.572 0-69.864"/></svg>Squarespace</span><span><svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 255"><path fill="#464342" d="M18.124 127.5c0 43.296 25.16 80.711 61.646 98.442L27.594 82.986a109 109 0 0 0-9.47 44.514m183.221-5.52c0-13.517-4.856-22.879-9.02-30.165c-5.545-9.01-10.742-16.64-10.742-25.65c0-10.055 7.626-19.415 18.368-19.415c.485 0 .944.06 1.417.088c-19.46-17.829-45.387-28.714-73.863-28.714c-38.213 0-71.832 19.606-91.39 49.302c2.566.077 4.984.13 7.039.13c11.44 0 29.15-1.387 29.15-1.387c5.897-.348 6.592 8.312.702 9.01c0 0-5.926.697-12.52 1.042L100.32 194.7l23.937-71.79l-17.042-46.692c-5.89-.345-11.47-1.042-11.47-1.042c-5.894-.346-5.203-9.358.691-9.01c0 0 18.064 1.388 28.811 1.388c11.44 0 29.151-1.388 29.151-1.388c5.9-.348 6.594 8.312.702 9.01c0 0-5.938.697-12.52 1.042l39.529 117.581l10.91-36.458c4.728-15.129 8.327-25.995 8.327-35.36m-71.921 15.088l-32.818 95.363a109.4 109.4 0 0 0 30.899 4.456c12.737 0 24.952-2.202 36.323-6.2a9.6 9.6 0 0 1-.779-1.507zm94.058-62.045a84 84 0 0 1 .737 11.247c0 11.1-2.073 23.577-8.317 39.178l-33.411 96.6c32.518-18.963 54.39-54.193 54.39-94.545c.002-19.017-4.856-36.9-13.4-52.48M127.505 0C57.2 0 0 57.196 0 127.5c0 70.313 57.2 127.507 127.505 127.507c70.302 0 127.51-57.194 127.51-127.507C255.014 57.196 197.808 0 127.506 0m0 249.163c-67.08 0-121.659-54.578-121.659-121.663c0-67.08 54.576-121.654 121.659-121.654c67.078 0 121.652 54.574 121.652 121.654c0 67.085-54.574 121.663-121.652 121.663"/></svg>WordPress</span><span><svg aria-hidden="true" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path fill="#1BDBDB" d="M20.702 2.29c-2.494-1.554-5.778-1.187-8.706.654C9.076 1.104 5.79.736 3.3 2.29c-3.941 2.463-4.42 8.806-1.07 14.167 2.47 3.954 6.333 6.269 9.77 6.226 3.439.043 7.301-2.273 9.771-6.226 3.347-5.361 2.872-11.704-1.069-14.167zM4.042 15.328a12.838 12.838 0 01-1.546-3.541 10.12 10.12 0 01-.336-3.338c.15-1.98.956-3.524 2.27-4.345 1.315-.822 3.052-.87 4.903-.137.281.113.556.24.825.382A15.11 15.11 0 007.5 7.54c-2.035 3.255-2.655 6.878-1.945 9.765a13.247 13.247 0 01-1.514-1.98zm17.465-3.541a12.866 12.866 0 01-1.547 3.54 13.25 13.25 0 01-1.513 1.984c.635-2.589.203-5.76-1.353-8.734a.39.39 0 00-.563-.153l-4.852 3.032a.397.397 0 00-.126.546l.712 1.139a.395.395 0 00.547.126l3.145-1.965c.101.306.203.606.28.916.296 1.086.41 2.214.335 3.337-.15 1.982-.956 3.525-2.27 4.347a4.437 4.437 0 01-2.25.65h-.101a4.432 4.432 0 01-2.25-.65c-1.314-.822-2.121-2.365-2.27-4.347-.074-1.123.039-2.251.335-3.337a13.212 13.212 0 014.05-6.482 10.148 10.148 0 012.849-1.765c1.845-.733 3.586-.685 4.9.137 1.316.822 2.122 2.365 2.271 4.345a10.146 10.146 0 01-.33 3.334z"/></svg>GoDaddy</span><span><svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 292"><path fill="#95bf46" d="M223.774 57.34c-.201-1.46-1.48-2.268-2.537-2.357a19614 19614 0 0 0-23.383-1.743s-15.507-15.395-17.209-17.099c-1.703-1.703-5.029-1.185-6.32-.805c-.19.056-3.388 1.043-8.678 2.68c-5.18-14.906-14.322-28.604-30.405-28.604c-.444 0-.901.018-1.358.044C129.31 3.407 123.644.779 118.75.779c-37.465 0-55.364 46.835-60.976 70.635c-14.558 4.511-24.9 7.718-26.221 8.133c-8.126 2.549-8.383 2.805-9.45 10.462C21.3 95.806.038 260.235.038 260.235l165.678 31.042l89.77-19.42S223.973 58.8 223.775 57.34M156.49 40.848l-14.019 4.339c.005-.988.01-1.96.01-3.023c0-9.264-1.286-16.723-3.349-22.636c8.287 1.04 13.806 10.469 17.358 21.32m-27.638-19.483c2.304 5.773 3.802 14.058 3.802 25.238c0 .572-.005 1.095-.01 1.624c-9.117 2.824-19.024 5.89-28.953 8.966c5.575-21.516 16.025-31.908 25.161-35.828m-11.131-10.537c1.617 0 3.246.549 4.805 1.622c-12.007 5.65-24.877 19.88-30.312 48.297l-22.886 7.088C75.694 46.16 90.81 10.828 117.72 10.828"/><path fill="#5e8e3e" d="M221.237 54.983a19614 19614 0 0 0-23.383-1.743s-15.507-15.395-17.209-17.099c-.637-.634-1.496-.959-2.394-1.099l-12.527 256.233l89.762-19.418S223.972 58.8 223.774 57.34c-.201-1.46-1.48-2.268-2.537-2.357"/><path fill="#fff" d="m135.242 104.585l-11.069 32.926s-9.698-5.176-21.586-5.176c-17.428 0-18.305 10.937-18.305 13.693c0 15.038 39.2 20.8 39.2 56.024c0 27.713-17.577 45.558-41.277 45.558c-28.44 0-42.984-17.7-42.984-17.7l7.615-25.16s14.95 12.835 27.565 12.835c8.243 0 11.596-6.49 11.596-11.232c0-19.616-32.16-20.491-32.16-52.724c0-27.129 19.472-53.382 58.778-53.382c15.145 0 22.627 4.338 22.627 4.338"/></svg>Shopify</span><span><svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 197"><path fill="#3192e7" d="M212.31 0c-19.972 0-36.617 13.278-41.722 33.15C161.385 3.29 137.83.023 128.004.023c-9.824 0-33.37 3.267-42.59 33.12C80.307 13.29 63.66.023 43.693.023C19.192.023 0 17.538 0 39.897c0 9.888 2.443 17.782 5.395 26.344l33.267 94.076c11.139 31.2 33.832 35.859 46.366 35.859c19.662 0 34.983-10.07 42.973-27.917c7.997 17.927 23.32 28.048 42.972 28.048c12.519 0 35.189-4.667 46.385-35.982l33.45-94.396l.261-.779c.382-1.21.768-2.345 1.132-3.423c1.781-5.27 3.799-11.243 3.799-18.563C256 18.154 237.626 0 212.31 0m15.769 57.875l-33.45 94.396c-4.084 11.42-10.876 19.922-23.656 19.922c-11.973 0-19.042-6.672-22.574-18.104L128.27 91.264h-.547l-20.116 62.825c-3.539 11.434-10.61 17.972-22.58 17.972c-12.782 0-19.58-8.431-23.657-19.852L28.193 58.385c-2.72-7.89-4.079-12.772-4.079-18.49c0-8.704 8.163-15.758 19.579-15.758c9.52 0 16.318 6.276 18.494 15.522l22.573 74.837h.54l22.845-73.188c2.997-10.605 8.433-17.171 19.859-17.171c11.42 0 16.857 6.555 19.848 17.16l22.846 73.199h.54l22.58-74.837c2.173-9.246 8.97-15.545 18.492-15.545c11.416 0 19.576 7.08 19.576 19.05c0 4.349-1.91 8.718-3.807 14.71"/></svg>Weebly</span><span><svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="#1d5fd1" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 7l-5 5 5 5M16 7l5 5-5 5M14 4l-4 16"/></svg>Custom sites</span></div></div>
</section>'''

TUNEUP = '''<section class="tvs-sec tva-tune" id="tva-tune">
  <div class="tva-tune-in tvs-up">
    <div>
      <p class="tvs-eyebrow">Included: AI Website Optimization</p>
      <h2>Get your website noticed and recommended by AI.</h2>
      <p>At setup we optimize your website and listings so ChatGPT, Google and other AI tools know exactly who you are, what you do and where.</p>
      <p class="tva-rep"><b>Before and after report included.</b></p>
    </div>
    <ul class="tva-list">
      <li><b>Business facts AI can read</b></li>
      <li><b>Google, Bing and Apple listings cleaned up</b></li>
      <li><b>FAQs written the way people ask</b></li>
      <li><b>Nothing blocking AI from your site</b></li>
    </ul>
  </div>
</section>'''


PRICING = '''<section class="tvs-sec tvs-bundles" id="tvs-bundles">
  <div class="tvs-head tvs-up">
    <p class="tvs-eyebrow">Pricing</p>
    <h2>One package. Found by AI, and turning visitors into leads.</h2>
    <p>Your AI assistant comes with full AI Website Optimization of your site and listings, done once at setup. Works with the website you already have.</p>
  </div>
  <div class="tvs-tiers tvs-up" role="tablist" aria-label="Choose your membership to see your price">
    <button type="button" role="tab" data-t="all">Walk-in price</button>
    <button type="button" role="tab" data-t="vip" class="on">Featured &amp; VIP members<em>Member pricing</em></button>
  </div>
  <div class="tvs-cards tva-one">
    <article class="tvs-card tvs-pop tvs-up tva-wide" data-b="aichat">
      <div class="tva-pc-a">
      <p class="tvs-badge">AI Website Optimization included</p>
      <p class="tvs-cname">Your Digital Front Desk</p>
      <p class="tvs-cfor">A smart assistant that answers your customers 24/7 and sends you every lead, plus one-time AI Website Optimization so ChatGPT, Google and other AI tools can find and understand you.</p>
      <p class="tvw-plabel on">Featured &amp; VIP member price*</p>
      <p class="tvs-was"></p>
      <p class="tvs-price"><sup>$</sup><b>%(cm0)s</b></p>
      <p class="tvs-mo">+ <b>$%(cm1)s</b>/mo</p>
      <p class="tvs-save"></p>
      <a class="tvs-btn tvs-blue tvs-wide tvw-go tva-pick" data-pick="ai_chat" href="#tvs-book">Get started &rarr;</a>
      <p class="tva-pc-note">Month to month after setup. No contract.</p>
      </div>
      <div class="tva-pc-b">
      <p class="tva-grp">Your AI assistant</p>
      <ul>
        <li>Built, trained and added to your site for you</li>
        <li>Answers questions 24/7 from your own information</li>
        <li>Every lead sent to your email or phone right away</li>
        <li>Links to your booking, quote form or ordering</li>
        <li>Live person handoff: you get an instant text</li>
        <li>Monthly summary and tuning: just email us changes</li>
      </ul>
      </div>
      <div class="tva-pc-c">
      <p class="tva-grp">Your AI Website Optimization (included, done at setup)</p>
      <ul>
        <li>Before and after &ldquo;Can AI find you?&rdquo; report</li>
        <li>Business facts code AI can read</li>
        <li>Page titles, descriptions and FAQs rewritten</li>
        <li>Google, Bing and Apple listings cleaned up</li>
        <li>Name, address and phone matched across the web</li>
        <li>Google Search Console and Bing Webmaster set up</li>
      </ul>
      </div>
    </article>
  </div>
  <p class="tvs-fine tvs-up"><b>Works with the site you have.</b> Wix, Squarespace, WordPress, GoDaddy, Shopify and custom sites. Some website builders only allow added code on their paid plans; we check yours first, free. The setup fee covers building your assistant and your full AI Website Optimization. Month to month after that, no contract. Want a site AI can fully read from the ground up? See our <a href="/websites">AI-Ready websites</a>.</p>
</section>''' % {"cm0": CHAT["member"][0], "cm1": CHAT["member"][1]}

VS = '''<section class="tvs-sec tvs-vs">
  <div class="tvs-head tvs-up">
    <p class="tvs-eyebrow">Side by side</p>
    <h2>A do-it-yourself chat app vs. Three Village Local</h2>
  </div>
  <div class="tvs-table tvs-up" role="table">
    <div class="tvs-tr tvs-th" role="row"><span role="columnheader"></span><span role="columnheader">DIY chat app</span><span role="columnheader">Three Village Local</span></div>
    <div class="tvs-tr" role="row"><span role="cell">A chat bubble on your site</span><span role="cell" class="tvs-y">&#10003;</span><span role="cell" class="tvs-y">&#10003;</span></div>
    <div class="tvs-tr" role="row"><span role="cell">Set up and added to your site for you</span><span role="cell" class="tvs-n">&mdash;</span><span role="cell" class="tvs-y">&#10003;</span></div>
    <div class="tvs-tr" role="row"><span role="cell">Trained on your business by a real person</span><span role="cell" class="tvs-n">&mdash;</span><span role="cell" class="tvs-y">&#10003;</span></div>
    <div class="tvs-tr" role="row"><span role="cell">Leads sent straight to your phone or email</span><span role="cell" class="tvs-n">Varies</span><span role="cell" class="tvs-y">&#10003;</span></div>
    <div class="tvs-tr" role="row"><span role="cell">Monthly tuning and updates by email</span><span role="cell" class="tvs-n">&mdash;</span><span role="cell" class="tvs-y">&#10003;</span></div>
    <div class="tvs-tr" role="row"><span role="cell">Local team that knows Three Village</span><span role="cell" class="tvs-n">&mdash;</span><span role="cell" class="tvs-y">&#10003;</span></div>
  </div>
</section>'''

STEPS = '''<section class="tvs-sec tvs-steps">
  <div class="tvs-head tvs-up">
    <p class="tvs-eyebrow">How it works</p>
    <h2>Live on your site in about a week.</h2>
    <p><a class="tva-how" href="''' + HOW + '''">See exactly how we train and test your assistant &rarr;</a></p>
  </div>
  <ol class="tvs-ol">
    <li class="tvs-up"><b>1</b><h3>Send a message</h3><p>Tell us about your business and send us your website link.</p></li>
    <li class="tvs-up"><b>2</b><h3>Research and development</h3><p>We study your business, your industry, your competition and its rules.</p></li>
    <li class="tvs-up"><b>3</b><h3>We add it to your site</h3><p>One small line of code. We add it, or send you simple steps.</p></li>
    <li class="tvs-up"><b>4</b><h3>Leads come in</h3><p>Customers get answers 24/7 and you get every lead.</p></li>
  </ol>
</section>'''

FAQ = '''<section class="tvs-sec tvs-faq">
  <div class="tvs-head tvs-up"><p class="tvs-eyebrow">Questions</p><h2>Good questions, straight answers.</h2></div>
  <div class="tvs-qs tvs-up">
    <details open><summary>Do I need a new website?</summary><p>No. Both add-ons work with the website you already have, no matter who built it or where it is hosted.</p></details>
    <details><summary>What if it doesn&#39;t know an answer?</summary><p>It answers from the information you give us. When a question needs you, it says so, takes the customer&#39;s name and number, and sends the details to you instead of guessing.</p></details>
    <details><summary>How do I get the leads?</summary><p>Every lead is sent to your email (and phone, if you like) right away, with the customer&#39;s name, number and what they need.</p></details>
    <details><summary>Can I change what it says?</summary><p>Anytime. New prices, specials, hours or services: just email or text us and we update it.</p></details>
    <details><summary>I&#39;m a law firm, financial advisor or medical office. Is this OK for my industry?</summary><p>Yes. We set up your assistant to follow your industry&#39;s regulations and guidelines. It shares general information about your firm and services, never advice, uses the disclaimers you need, only states rates or fees you approve, never asks for sensitive information, and hands anything specific to you. You review and approve everything before launch, and we&#39;re happy to work with your compliance person.</p></details>
    <details><summary>Will it work on my website builder?</summary><p>Almost always. Wix, Squarespace, WordPress, GoDaddy, Shopify and custom sites all work. A few builders only allow added code on their paid plans, so we check yours first, free.</p></details>
    <details><summary>What is AI Website Optimization?</summary><p>It comes with every AI assistant. At setup we make a one-time set of fixes to your website and your Google, Bing and Apple listings so AI tools like ChatGPT can understand your business. You get a before and after report.</p></details>
    <details><summary>Does the chat assistant help AI recommend me?</summary><p>Not on its own: AI search tools don&#39;t read chat bubbles. The assistant turns more of your visitors into leads, and the included AI Website Optimization is what helps AI tools find and understand you. That&#39;s why they come together.</p></details>
    <details><summary>Is there a contract?</summary><p>No. One setup fee covers your assistant and your AI Website Optimization, then it is month to month.</p></details>
    <details><summary>Do I have to be a Three Village Local member?</summary><p>No. Anyone can sign up at our walk-in price. Featured and VIP members of Three Village Local get member pricing.</p></details>
  </div>
</section>'''

h = W.HTML
i, j = sec(h, "tvs-hero")
h = h[:i] + HERO + h[j:]
h = cut(h, "tvw-strip")
h = cut(h, "tvs-sec tvw-shift")
STRIP = W.STRIP_SEC.replace("<p>Get recommended on the AI tools your customers use</p>", "<p>AI Website Optimization: built to get you noticed and recommended on</p>")
h = swap(h, "tvs-sec tvw-ai", NEXT + "\n\n" + WORKS + "\n\n" + STRIP + "\n\n" + FEAT + "\n\n" + TUNEUP)
h = cut(h, "tvs-sec tvw-bot")
h = swap(h, "tvs-sec tvs-bundles", PRICING)
h = swap(h, "tvs-sec tvs-vs", VS)
h = swap(h, "tvs-sec tvs-steps", STEPS)
h = swap(h, "tvs-sec tvs-faq", FAQ)
h = rep(h, "<h2>Let&#39;s build your AI-ready website.</h2>", "<h2>Let&#39;s put AI to work on your website.</h2>")
h = rep(h, "<p class=\"tvw-cta3-s\">Designed, built and hosted for you. Updates included. First month included.</p>",
        "<p class=\"tvw-cta3-s\">No new website needed. Set up for you. Every lead sent to you.</p>")
h = rep(h, '<a class="tvs-btn tvw-btn-o" href="#tvs-bundles">See the packages</a>', '<a class="tvs-btn tvw-btn-o" href="#tvs-bundles">See pricing</a>')
h = rep(h, "mailto:hello@threevillagelocal.com?subject=Websites", "mailto:hello@threevillagelocal.com?subject=AI%20for%20my%20website")
h = re.sub(r'<p class="tvw-small">.*?</p>', '<p class="tvw-small">*Member pricing is for Featured and VIP tier members of Three Village Local. Walk-in pricing applies to everyone else.</p>', h, count=1, flags=re.S)
assert "\\" not in h and "tvw-dev" not in h
HTML = h

PRICES = "aichat:{all:[%d,%d],free:[%d,%d],featured:[%d,%d],vip:[%d,%d]}," % (CHAT["all"] + CHAT["member"] * 3)
# Pricing buttons preselect the right option in the shared services form (field "bundle", form 343) and keep the hidden-field trick.
PICKJS = '''<script>(function(){var pick='ai_chat';document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('#tvs .tva-pick');if(a){pick=a.getAttribute('data-pick');set()}});
function set(){var s=document.querySelector('#tvs-form-slot select[name="bundle"]');if(s){s.value=pick;return true}return false}
var n=0,iv=setInterval(function(){if(set()||++n>60)clearInterval(iv)},300);})();</script>'''

OPENJS = '''<script>document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('[data-tva-open]');if(a){e.preventDefault();if(window.tvaOpen)window.tvaOpen()}});</script>'''

CSS = '''
.tva-hvis{padding:28px 34px 28px 24px}
.tvs-hero:has(.tva-hvis){min-height:680px}
.tva-hvis:before{pointer-events:none}   /* websites hero decor layer sat over the chat and swallowed clicks */
.tva-pop{width:360px!important}.tva-pop .tva-box{height:470px!important;max-height:calc(100vh - 130px)!important}
@media (max-width:520px){.tva-pop{width:100%!important}.tva-pop .tva-box{height:100dvh!important;max-height:100dvh!important}}
.tva-mock{position:relative;border-radius:18px;background:#fff;box-shadow:0 34px 70px -30px rgba(9,30,66,.5),0 0 0 1px rgba(15,42,82,.08);overflow:hidden;height:470px}
.tva-mock-bar{display:flex;align-items:center;gap:6px;padding:10px 14px;background:#eef2f7;border-bottom:1px solid #e1e8f2}
.tva-mock-bar i{width:9px;height:9px;border-radius:50%;background:#d3dbe6}.tva-mock-bar i:first-child{background:#ff7b6b}.tva-mock-bar i:nth-child(2){background:#ffc85a}.tva-mock-bar i:nth-child(3){background:#4bd18a}
.tva-mock-bar span{margin-left:10px;flex:1;padding:4px 12px;border-radius:999px;background:#fff;font-size:12px;color:#7a8696}
.tva-mock-page{padding:22px 22px 0}.tva-mock-page b{display:block;width:55%;height:18px;border-radius:6px;background:#dbe5f3;margin-bottom:14px}
.tva-mock-page p{height:9px;border-radius:5px;background:#edf1f6;margin:0 0 9px!important}.tva-mock-page p.s{width:60%}
.tva-mock-row{display:flex;gap:10px;margin:16px 0}.tva-mock-row u{flex:1;height:64px;border-radius:10px;background:#f1f5fa}
.tva-mock-chat{position:absolute;right:12px;bottom:12px;width:330px;zoom:.8;transform-origin:bottom right;animation:tvaPopIn .7s .6s cubic-bezier(.2,.9,.3,1.15) both}
.tva-mock-chat .tvw-bot-demo{margin:0!important}.tva-mock-chat .tvw-chatw{font-size:13px}.tva-mock-chat .tvw-bot-ex{display:none}
.tva-mock-chat .tvw-lead{display:none}
@keyframes tvaPopIn{from{opacity:0;transform:translateY(20px) scale(.85)}to{opacity:1;transform:none}}
.tva-glow{position:relative;border-radius:24px}
.tva-glow:before{content:"";position:absolute;inset:-3px;border-radius:26px;background:linear-gradient(120deg,#4da3ff,#2fd28a,#1d5fd1,#8fd0ff,#4da3ff);background-size:300% 300%;animation:tvaGrad 6s linear infinite;z-index:0;filter:blur(1px)}
.tva-glow:after{content:"";position:absolute;inset:-18px;border-radius:40px;background:radial-gradient(closest-side,rgba(77,163,255,.35),transparent);z-index:-1;animation:tvaPulse 3.2s ease-in-out infinite;pointer-events:none}
.tva-glow #tva-live{position:relative;z-index:1}
.tva-try{animation:tvaRise .9s cubic-bezier(.2,.8,.2,1) both}
.tva-try-k span{animation:tvaDot 1.6s ease-in-out infinite}
.tva-float{position:absolute;z-index:3;padding:8px 12px!important;display:flex;gap:10px;align-items:center;padding:10px 14px;border-radius:14px;background:#fff;box-shadow:0 18px 40px -18px rgba(9,30,66,.45);font-size:13px;line-height:1.3;color:#3c4a5e;opacity:0;pointer-events:none}
.tva-float b{font-size:18px}.tva-float em{display:block;font-style:normal;font-weight:800;color:var(--navy);font-size:13.5px}
.tva-f1{right:-50px;top:-12px;animation:tvaIn1 .7s 1.2s forwards,tvaBob 5s 2s ease-in-out infinite}
.tva-f2{left:-46px;bottom:-26px;animation:tvaIn1 .7s 2s forwards,tvaBob 6s 2.8s ease-in-out infinite}
.tva-f3{right:-40px;bottom:-26px;animation:tvaIn1 .7s 2.8s forwards,tvaBob 5.5s 3.6s ease-in-out infinite}
.tva-f3 b{color:#2fd28a}
@keyframes tvaGrad{0%{background-position:0% 50%}100%{background-position:300% 50%}}
@keyframes tvaPulse{0%,100%{opacity:.55;transform:scale(1)}50%{opacity:1;transform:scale(1.03)}}
@keyframes tvaRise{from{opacity:0;transform:translateY(26px) scale(.97)}to{opacity:1;transform:none}}
@keyframes tvaIn1{from{opacity:0;transform:translateY(12px) scale(.92)}to{opacity:1;transform:none}}
@keyframes tvaBob{0%,100%{translate:0 0}50%{translate:0 -8px}}
@keyframes tvaDot{0%,100%{box-shadow:0 0 0 4px rgba(47,210,138,.2)}50%{box-shadow:0 0 0 8px rgba(47,210,138,.05)}}
.tva-why>div,.tva-c{transition:transform .25s,box-shadow .25s}.tva-why>div:hover,.tva-c:hover{transform:translateY(-4px);box-shadow:0 22px 44px -24px rgba(9,30,66,.4)}
.tva-c span{transition:transform .3s}.tva-c:hover span{transform:scale(1.12) rotate(-6deg)}
.tva-works span{transition:transform .2s,border-color .2s}.tva-works span:hover{transform:translateY(-2px);border-color:#9cc1ff}
.tva-list li{opacity:0;transform:translateX(14px);transition:opacity .5s,transform .5s}.tva-tune-in.tvs-in .tva-list li{opacity:1;transform:none}
.tva-tune-in.tvs-in .tva-list li:nth-child(2){transition-delay:.12s}.tva-tune-in.tvs-in .tva-list li:nth-child(3){transition-delay:.24s}.tva-tune-in.tvs-in .tva-list li:nth-child(4){transition-delay:.36s}.tva-tune-in.tvs-in .tva-list li:nth-child(5){transition-delay:.48s}.tva-tune-in.tvs-in .tva-list li:nth-child(6){transition-delay:.6s}
@media (max-width:1180px){.tva-f2{left:-14px}.tva-f1,.tva-f3{right:-10px}}
@media (max-width:900px){.tva-float{display:none}}
@media (prefers-reduced-motion:reduce){.tva-glow:before,.tva-glow:after,.tva-try,.tva-try-k span,.tva-float{animation:none!important;opacity:1}.tva-list li{opacity:1;transform:none}}
.tva-try{position:relative;z-index:1;width:100%;max-width:430px;margin:0 auto}
.tva-try-k{margin:0 0 10px!important;text-align:left;padding-left:8px;font-size:12.5px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--blue)}
.tva-try-k span{display:inline-block;width:8px;height:8px;border-radius:50%;background:#2fd28a;margin-right:8px;box-shadow:0 0 0 4px rgba(47,210,138,.2);vertical-align:1px}
.tva-try .tva-box{height:540px}
@media (max-width:900px){.tva-try .tva-box{height:520px;max-height:78vh}.tvs-hero:has(.tva-hvis){display:flex;flex-direction:column;min-height:0}.tva-hvis{order:2;border-radius:0 0 22px 22px!important}}
.tva-how{display:inline-block;margin:16px 0 4px;font-weight:800;color:var(--blue)!important;text-decoration:none!important;border-bottom:2px solid rgba(29,95,209,.25)}.tva-how:hover{border-color:var(--blue)}
.tva-one{display:grid!important;grid-template-columns:minmax(0,560px)!important;justify-content:center}
@media (min-width:980px){.tva-one{grid-template-columns:minmax(0,1120px)!important}
.tva-wide{display:grid!important;grid-template-columns:1fr 1.15fr 1.15fr;gap:30px;align-items:start;padding:34px 34px 30px!important}
.tva-pc-a{padding-right:26px;border-right:1px solid #e3e9f2}.tva-pc-b{padding-right:24px;border-right:1px solid #e3e9f2}
.tva-wide .tvs-cfor{display:none}.tva-wide li{font-size:14.5px!important;margin-bottom:6px!important}#tvs-bundles{padding-top:46px!important}#tvs-bundles .tvs-head{margin-bottom:18px!important}#tvs-bundles .tvs-head p{display:none}
.tva-wide .tva-grp{margin-top:6px!important}.tva-wide ul{margin-bottom:0!important}}
.tva-pc-note{margin:10px 0 0!important;font-size:13px;color:var(--mut);text-align:center}
.tva-grp{margin:14px 0 6px!important;font-size:12.5px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--blue)}
.tva-why{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;max-width:1060px;margin:0 auto}
.tva-why>div{background:#fff;border:1px solid #e3e9f2;border-radius:20px;padding:24px 22px;box-shadow:0 14px 34px -22px rgba(9,30,66,.25)}
.tva-why b{font-size:30px;display:block;margin-bottom:8px}
.tva-why h3{margin:0 0 6px!important;font-size:19px;color:var(--navy)}
.tva-why p{margin:0!important;font-size:15px;line-height:1.55;color:var(--mut)}
.tva-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;max-width:1060px;margin:0 auto}
.tva-c{background:linear-gradient(180deg,#f6f9ff,#fff);border:1px solid #dfe8f6;border-radius:20px;padding:22px}
.tva-c span{display:inline-flex;width:46px;height:46px;border-radius:14px;align-items:center;justify-content:center;font-size:23px;background:#e7f0ff;margin-bottom:10px}
.tva-c h3{margin:0 0 6px!important;font-size:18px;color:var(--navy)}
.tva-c p{margin:0!important;font-size:15px;line-height:1.55;color:var(--mut)}
.tva-reg{display:flex;gap:16px;align-items:flex-start;max-width:1060px;margin:22px auto 0;padding:20px 22px;border-radius:20px;background:#fff;border:1px solid #dfe8f6;box-shadow:0 14px 34px -24px rgba(9,30,66,.3)}
.tva-reg>span{font-size:28px;line-height:1}
.tva-reg b{display:block;font-size:17px;color:var(--navy);margin-bottom:4px}
.tva-reg p{margin:0!important;font-size:15px;line-height:1.55;color:var(--mut)}
.tvs-sticky{right:auto!important;left:20px!important}   /* chat button owns the bottom-right corner */
.tva-plat{padding-bottom:0!important}.tva-plat+.tvw-strip{margin-top:-10px}
.tva-tune-in{align-items:center!important}.tva-list li{padding:14px 14px 14px 42px!important}
.tva-works{max-width:1060px;margin:0 auto;text-align:center}
.tva-works p{margin:0 0 10px!important;font-size:12.5px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--mut)}
.tva-works div{display:flex;flex-wrap:wrap;justify-content:center;gap:8px}
.tva-works span svg{width:auto!important;height:20px!important;max-width:46px;display:block;flex:none}
.tva-works span{display:inline-flex;align-items:center;gap:8px;font-size:14px;font-weight:800;padding:8px 15px 8px 12px;border-radius:999px;background:#fff;border:1px solid #dfe6f0;color:var(--navy)}
.tva-tune-in{display:grid;grid-template-columns:1fr 1.1fr;gap:36px;align-items:start;max-width:1060px;margin:0 auto;padding:34px;border-radius:26px;background:linear-gradient(150deg,#0b1f4b,#123a7a);color:#fff}
.tva-tune-in h2{color:#fff!important;font-size:34px;line-height:1.12;margin:0 0 12px!important}
.tva-tune-in .tvs-eyebrow{color:#8fc1ff!important}
.tva-tune-in>div>p{color:#d6e3f7!important;font-size:16px;line-height:1.6}
.tva-rep{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16);border-radius:14px;padding:14px 16px}
.tva-rep b{color:#f2c94c}
.tva-list{list-style:none;margin:0;padding:0;display:grid;gap:10px}
.tva-list li{background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.14);border-radius:14px;padding:12px 14px 12px 42px;position:relative;font-size:14.5px;line-height:1.45;color:#cfdcf1}
.tva-list li:before{content:"✓";position:absolute;left:14px;top:11px;color:#5ee0a0;font-weight:800}
.tva-list li b{display:block;color:#fff;font-size:15.5px}
@media (max-width:900px){.tva-why,.tva-grid{grid-template-columns:1fr}.tva-tune-in{grid-template-columns:1fr;padding:24px 20px}.tva-tune-in h2{font-size:28px}.tva-hvis{padding:24px 14px}}
'''

_rd = W.rd


def rd(f):
    if f == "page.html":
        return HTML
    s = _rd(f)
    if f == "page.css":
        return s + CSS
    if f == "page.js":
        return rep(s, "var P={", "var P={" + PRICES) + PICKJS + OPENJS + '<script src="https://3vl-ai-assistant.vercel.app/widget.js" data-tease="Hi! I am live. Ask me anything about AI for your website." defer></script>'
    return s


D.rd = rd
if __name__ == "__main__":
    D.main()
