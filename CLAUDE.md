
## BD page designs live in WIDGETS (since 2026-09-27)
BD's page editor (Froala) strips <style>/<script>/classes when anyone saves a page in admin. So designed pages hold ONLY a shortcode, and the HTML lives in a widget (code editor, never stripped):
- /now (page 471) -> widget 17 "3VL Page Now"
- /join (page 3) -> widget 15 "3VL Page Join"
- /promotion (page 16) -> widget 14 "3VL Page Promotion"
- /app (page 17) -> widget 18 "3VL Page App" (source site/app; phone plays site/app/now-demo.mp4, re-record with scratch record.py approach when /now changes a lot)
- /member-match (page 472) -> widget 16 "3VL Page Member Match" (page content_footer_html holds MM_DONE, written by the guard)
Page CSS stays in each page's content_css. To change a design: updateWidget (widget_data), NOT updateWebPage content. Weekly /now builds: python weekender/build.py <edition> --sha <SHA>, copy <edition>/post.html to 3vl-site-guard/post-sources/widget-17-3vl-page-now.html, commit+push there. The guard-push-widget workflow publishes it to widget 17 and it becomes the guard backup in the same step.
Page settings (share image, titles) are safe to change now, but still prefer the API.
Guard (3vl-site-guard, every 30 min) watches post-sources/page-*.html (shortcode), page-*.css, widget-*.html and auto-restores. New designed page: run workflow "Guard - move page designs into widgets" with seo_id:"Widget Name".

## /now Top Picks and Eat & Drink (owner decisions, 2026-09-27)
- Top Picks: up to 6 cards in one sideways-scrolling row on desktop and mobile, with arrow buttons on desktop. Order and choice come from weekend.json "picks". A pick can be an "allweekend" item (an ongoing attraction). It then shows its "when" text (e.g. "Running until Oct. 31"), a title linked to its url, a Details button instead of Add, and no live "Happening now" badge. Set "until" for the end date.
- Eat & Drink: 6 cards, in the owner's ranked order from weekender/live/preference.json. Instagram sync is currently OFF (live=false, workflow disabled). A subtle divider line sits above the section.

## Event timing rules (owner, 2026-09-27) - /events calendar (tvl-cal.js) and /now (weekender.js)
- An event disappears as soon as its end time passes. An event with no end time is treated as 2 hours long, or as the whole day if it's all-day.
- Multi-day events show their date range (e.g. "Sep 26 - Oct 4"; plain hyphen, never an em dash).
- "Happening now" (homepage weekender.js isLive): a one-day event is live between its start and end. An event running for days or weeks is live only during its daily hours (the start/end clock times, or 10 AM-6 PM if it has none), never overnight (owner 9/28/2026).
- Ongoing events that started earlier roll forward: they're listed under Today with "Now through <end>" (/events) or "Ongoing, thru <end>" (/now).
- Sources: 10 feeds incl. LI Music & Entertainment Hall of Fame (limehof, HTML grid scrape; museum shows only).

## Gotcha: CSS escapes through the guard
The guard's restore PUT strips backslashes, so CSS like content:"97" breaks. Use the literal character in page CSS (e.g. content:"↗").

## jsDelivr "Package size exceeded 50 MB" on a new pin (9/28/2026)
A short-SHA pin (`@c51d46b03fb8`) returned "Package size exceeded the configured limit of 50 MB" instead of the file, and jsDelivr CACHES that error for that URL. The same commit worked via the FULL 40-char SHA. After every pin bump, curl each pinned file and grep for real content (not just HTTP 200). If you get the size error, pin the full SHA instead.

## 3VL graphic style (owner-approved 9/28/2026) - use for share images, promos, social
Dark blurred local photo background (Stony Brook Village street or restaurant interior, blur ~9-12px, left-heavy dark gradient). Radio Canada. Big white headline + ONE gold (#ffc53d) line + a ~38px white subline. Glass pill for info, gold pill for VIP ("★ NEIGHBOR FAVORITE"). Business photo/logo on a STRAIGHT white rounded card (never tilted); VIP card gets a gold ring + glow. NO small text, URLs, CTA buttons, chip rows, or 3VL wordmark on the graphic. Reference: site/share-img/make_mockup.py, weekender/og/share11.html.

## Listing share images (9/28/2026) - LIVE on all listings
Generator: site/share-img. Run order: fetch.py (members.json), fetch_seo.py (seo_src.json = rollback snapshot), seo_gen.py (seo_plan.json), gen.py (out/<slug>.jpg at 2x), then copy out/*.jpg to the 3vl-share repo folder l/ and push, then apply.py.
Hosting: GitHub PAGES of threevillagelocal-cloud/3vl-share (https://threevillagelocal-cloud.github.io/3vl-share/l/<slug>.jpg). NOT jsDelivr, because 80 MB is over its 50 MB package limit. NOT 3vl-assets either.
BD mangles external og URLs, so each listing uses a BD 301 redirect: /share/<slug>.jpg -> Pages URL (Frame Shop: share/setauket-frame-shop-v3.jpg). Then seo_social_page_image = https://www.threevillagelocal.com/share/<slug>.jpg plus the 4 SEO fields. apply.py is resumable (apply_log.json).
Owner rules: town shows "Setauket" for any Setauket / East Setauket listing (never "East Setauket"). The gold line is "Since YEAR", else the specialty label (<=24 chars), else the town. Better logos go in img/override/<user_id>.png. When an image changes, use a NEW /share/ filename (FB caches by URL) and re-scrape in the FB Sharing Debugger.
Excluded: user 5 (admin/blog author), 218 (Twinr). SEO backup: site/share-img/backups/ (gitignored, local).

## HOMEPAGE = the Three Village Local (Now) page (switched 9/28/2026)
- threevillagelocal.com/ shows widget 17 "3VL Page Now" through Design Settings > Homepage: Section 1 = "Custom Content 10" (contains only [widget=3VL Page Now]). The hero is hidden ("Hide Entire Hero Section"), and sections 2-5 are None. The BD home page record (seo_id 1) content field is IGNORED by BD. Its content_css keeps .homepage-section-1 transparent.
- /now 301 -> / (BD redirect 1896). The "Three Village Now" menu item (362) was deleted.
- The weekly edition + weekender/build.py still produce the page body. The NIGHTLY rebuild (3vl-site-guard "Homepage nightly rebuild", ~3:05 AM ET, runs weekender/nightly.py) drops past items, refreshes the Event schema from live/events.json, VIPs and stories, then pushes widget 17. Manual publishes still go via site-guard post-sources/widget-17-3vl-page-now.html.
- Old homepage add-ons (site/p3/home2.js, today.js) stand down when #wk-top is present. smartsearch shows its bar in the .wk-hero and also runs on the /categories hero (#p3q).
- To roll back: restore the Design Settings values listed in the owner memory (custom_30 Keyword Only Search, 96 Hero Divider, 97 Streaming Members, 98 Custom Content 5, 99 About/Join, 100 Streaming Blog), delete redirect 1896, and re-add the menu item (Three Village Now, /now, menu 52, order 5).

## Image shrinking: our own small copies (9/29/2026) - keep it when editing these files
tvl-cal.js, weekender.js, nowhome.js and nowhome_build.py pass external/BD-hosted photos through sm(url, width) -> https://threevillagelocal-cloud.github.io/3vl-share/t/<fnv1a32(url)>-<360|800>.webp (a 6 MB library photo becomes ~33 KB). The copies are made by 3vl-share t/gen.py (GitHub Action every 30 min). It collects the images from /events, /events-calendar, the homepage HTML, live/events.json, feed.json, search/index.json and /blog, and deletes copies unused for 21 days. A missing copy falls back to the original: <img> via data-o + onerror, backgrounds via data-bgo + bgfix(), and nowhome_build HEAD-checks. Our own jsDelivr .webp files are skipped. NEW code that renders event photos, logos or blog images must use sm(), and if it pulls from a NEW source, add that source to gen.py collect(). Otherwise /events goes back to 20+ MB. (wsrv.nl was used for a few hours on 9/29, then replaced at the owner's request: no third-party dependency.)
