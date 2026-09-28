
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
- Ongoing events that started earlier roll forward: they're listed under Today with "Now through <end>" (/events) or "Ongoing, thru <end>" (/now).
- Sources: 10 feeds incl. LI Music & Entertainment Hall of Fame (limehof, HTML grid scrape; museum shows only).

## Gotcha: CSS escapes through the guard
The guard's restore PUT strips backslashes, so CSS like content:"97" breaks. Use the literal character in page CSS (e.g. content:"↗").
