# Member spotlight share image (owner-approved 10/30/2026: "lock in that exact style")
Example: CMIT Solutions of North Suffolk (user 402), 3vl-share/l/cmit-solutions-of-north-suffolk-v4.jpg.
Layout, 1200x630 rendered at 2x (2400x1260):
- Gold ribbon banner top-left: "★ THREE VILLAGE RESIDENT OWNED". ASK THE OWNER FIRST every time whether the business really is resident owned (owner rule 10/30/2026). Confirmed: CMIT (402).
- Town pill, business name (big white), gold service line (e.g. "IT Support & Computer Services").
- Right: the OWNER'S PHOTO (rounded square, white border) with "Name / Title" under it.
- Lower left: the business's own logo, prominent but not huge (~400px wide at 1x), white/transparent version on the dark bg.
- 3VL white logo bottom-right. Dark blurred village photo background. No "Visit us" line, no "Since <this year>".
Make one: copy template.html next to the member's dave.jpg-style photo + logo, edit the text/file names, render with
puppeteer (scratch render.js: W 1200 H 630 dpr 2, jpeg), save to 3vl-share/l/<filename>-vN.jpg, BD redirect share/<filename>-vN.jpg,
set user seo_social_page_image to https://www.threevillagelocal.com/share/<filename>-vN.jpg, then Facebook Sharing Debugger "Scrape Again"
(always a NEW -vN name: ImageKit + Facebook cache the old file).
