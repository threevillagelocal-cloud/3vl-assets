"""Pull PUBLIC listing fields for all active members -> members.json (no emails/billing kept)."""
import json, subprocess, time, urllib.parse, os
from bdkey import key
KEY = key(); SITE = "https://www.threevillagelocal.com"; HERE = os.path.dirname(os.path.abspath(__file__))
def api(path):
    for _ in range(5):
        out = subprocess.run(["curl", "-s", "-H", "X-Api-Key: " + KEY, SITE + path], capture_output=True, text=True, encoding="utf-8").stdout
        time.sleep(1.2)
        try: d = json.loads(out)
        except Exception: d = {}
        if "too many" in str(d.get("message", "")).lower(): time.sleep(65); continue
        return d
    return {}
users, page = [], ""
while True:
    d = api("/api/v2/user/get?limit=100&property=active&property_value=2" + ("&page=" + page if page else ""))
    users += d.get("message") or []
    page = str(d.get("next_page") or "")
    if not page or not d.get("message"): break
cats = {}
p = ""
while True:
    d = api("/api/v2/list_professions/get?limit=100" + ("&page=" + p if p else ""))
    for c in d.get("message") or []: cats[str(c.get("profession_id"))] = c.get("name")
    p = str(d.get("next_page") or "")
    if not p or not d.get("message"): break
reviews = []; p = ""
while True:
    d = api("/api/v2/users_reviews/get?limit=100" + ("&page=" + p if p else ""))
    reviews += d.get("message") or []
    p = str(d.get("next_page") or "")
    if not p or not d.get("message"): break
KEEP = ["user_id", "state_code", "company", "first_name", "last_name", "city", "subscription_id", "profession_id", "filename", "image_main_file", "logo", "cover_photo", "experience", "quote", "verified", "listing_type"]
out = []
for u in users:
    m = {k: u.get(k) for k in KEEP}
    m["category"] = cats.get(str(u.get("profession_id")))
    rs = [r for r in reviews if str(r.get("user_id")) == str(u["user_id"]) and str(r.get("review_status")) == "2" and r.get("rating_overall")]
    m["rating"] = round(sum(float(r["rating_overall"]) for r in rs) / len(rs), 1) if rs else None
    m["reviews"] = len(rs)
    out.append(m)
json.dump(out, open(os.path.join(HERE, "members.json"), "w", encoding="utf-8"), indent=1)
print(len(out), "members;", len(cats), "categories;", len(reviews), "reviews")
