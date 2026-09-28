"""Pull the text we need for titles/meta descriptions (public listing text only) -> seo_src.json
Also snapshots each member's CURRENT SEO fields so any change can be rolled back."""
import json, os, subprocess, time, re, html
from bdkey import key

KEY = key(); SITE = "https://www.threevillagelocal.com"; HERE = os.path.dirname(os.path.abspath(__file__))


def api(path):
    for _ in range(5):
        out = subprocess.run(["curl", "-s", "-H", "X-Api-Key: " + KEY, SITE + path], capture_output=True, text=True, encoding="utf-8").stdout
        time.sleep(1.2)
        try:
            d = json.loads(out)
        except Exception:
            d = {}
        if "too many" in str(d.get("message", "")).lower():
            time.sleep(65); continue
        return d
    return {}


def text(h):
    t = re.sub(r"<(style|script)[^>]*>.*?</\1>", " ", h or "", flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


rows, page = [], ""
while True:
    d = api("/api/v2/user/get?limit=25&property=active&property_value=2&include_seo_hidden=1&include_about=1&include_services=1" + ("&page=" + page if page else ""))
    for u in d.get("message") or []:
        svcs = [s.get("name") for s in (u.get("services_schema") or []) if isinstance(s, dict) and s.get("name")]
        rows.append({"user_id": u["user_id"], "services": svcs, "search_description": u.get("search_description") or "",
                     "about": text(u.get("about_me"))[:600],
                     "current": {k: u.get(k) for k in ["seo_page_title", "seo_page_description", "seo_social_page_title", "seo_social_page_description", "seo_page_keywords"]}})
    page = str(d.get("next_page") or "")
    if not page or not d.get("message"):
        break
json.dump(rows, open(os.path.join(HERE, "seo_src.json"), "w", encoding="utf-8"), indent=1)
print(len(rows), "rows;", sum(1 for r in rows if any(r["current"].values())), "with existing SEO values;", sum(1 for r in rows if r["search_description"]), "with short description")
