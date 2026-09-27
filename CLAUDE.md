
## BD page designs live in WIDGETS (since 2026-09-27)
BD's page editor (Froala) strips <style>/<script>/classes when anyone saves a page in admin. So designed pages hold ONLY a shortcode, and the HTML lives in a widget (code editor, never stripped):
- /now (page 471) -> widget 17 "3VL Page Now"
- /join (page 3) -> widget 15 "3VL Page Join"
- /promotion (page 16) -> widget 14 "3VL Page Promotion"
- /member-match (page 472) -> widget 16 "3VL Page Member Match" (page content_footer_html holds MM_DONE, written by the guard)
Page CSS stays in each page's content_css. To change a design: updateWidget (widget_data), NOT updateWebPage content. Weekly /now builds: python weekender/build.py <edition> --sha <SHA>, copy <edition>/post.html to 3vl-site-guard/post-sources/widget-17-3vl-page-now.html, commit+push there. The guard-push-widget workflow publishes it to widget 17 and it becomes the guard backup in the same step.
Page settings (share image, titles) are safe to change now, but still prefer the API.
Guard (3vl-site-guard, every 30 min) watches post-sources/page-*.html (shortcode), page-*.css, widget-*.html and auto-restores. New designed page: run workflow "Guard - move page designs into widgets" with seo_id:"Widget Name".
