# Three Village Storm Guide: reusable template

> Renamed from "Storm Center" on 9/26/2026 (owner: less official, no media-drama tone). Folder keeps its old name so existing links keep working. Never use "Storm Center" in new copy.

The first edition went live on Sept 25, 2026 (BD post 253, /blog/storm-prep-wind-heavy-rain-this-weekend-in-three-village).
Copy this folder for every future storm. Scale features up or down per storm, but keep the quality bar.

## Files
- `article-body.html`: article HTML (no head, style or script). This is the content you edit per storm.
- `bd-post-content-2026-09.html`: exact BD post_content as published (critical inline style + preload + CSS link + body + script).
- `storm.css` / `storm.js`: all design and live data. Host under a new folder (e.g. `storm-2026-11/`), commit, then reference by commit SHA on jsDelivr.
- `social-graphics-template.html`: render with headless Chrome. `?f=wide` gives 1200x630 (FB/OG share), `?f=sq` gives 1080x1080 (Twinr push), `?f=ig` gives 1080x1350 (Instagram 4:5, link in bio).
- `hero-rain.jpg`: night-rain photo (Mateus S. Figueiredo, CC BY-SA 4.0, credit required in the header and on graphics).

## Per-storm checklist
1. In storm.js, update the `T_START / T_PEAK / T_END` countdown milestones.
2. Update the static fallbacks in article-body.html: alerts, forecast cards, timeline, tides, gauges, and the cancellations list.
3. Cancellations: search 11733 / 11790 / 11777. Sources: TBR News, portjeffny.gov calendar, stonybrookvillage.com, tvhs.org, the 88844ferry.com ferry status, Three Village CSD. Use Canceled / Check First / Moving Indoors badges.
4. Pick business cards for the storm type (flooding, power, trees, plumbing, snow removal). Pull logos with listUsers `image_main_file`.
5. Render the three graphics. Use the "Three Village Storm Guide" brand and "LIVE" chip.
6. Host the CSS/JS/images, then publish to BD via the API (never the Froala editor, which strips style and script). Run refreshSiteCache.
7. Verify on the LIVE BD page: headless screenshot (desktop plus a 390px iframe), radar tiles render, phone numbers on one line.
8. Get the user's OK on everything before the Twinr push and social posts. Twinr has no scheduling on our plan, so the push is sent live with Send Now.

## Hard-won gotchas
- BD theme CSS forces `position:relative` and a transition on imgs and `white-space:normal` on text inside posts. That breaks Leaflet tiles and wraps phone numbers. Keep the `#stm-top` / `.stm .stm-rmap` override rules with !important.
- Rain totals: sum NWS gridpoint `quantitativePrecipitation`. Do NOT add up the per-period text ranges (that gave a bogus "3.75 to 7 inches").
- Radar: RainViewer free tiles have a native max zoom of 7 (use maxNativeZoom 7). CARTO dark tiles now watermark "API KEY REQUIRED", so use Esri World_Dark_Gray Base + Reference.
- jsDelivr `@master` caches browsers for 7 days and lags after purge. Pin to a commit SHA and put the link and script straight in the post (a JS loader delayed render by ~2s).
- Wind-dial motion must stay between the measured sustained speed and the gust (honesty).
