"""Builds site/p3/vip_meta.json: PUBLIC listing details for VIP members (already shown on their 3VL profiles).
Never includes email, billing, IPs or anything private.  Run: BD_API_KEY=... python site/p3/build_vip_meta.py"""
import json, os, re, subprocess, time, urllib.parse
KEY = os.environ["BD_API_KEY"]
SITE = "https://www.threevillagelocal.com"
HERE = os.path.dirname(os.path.abspath(__file__))


def api(path):
    for _ in range(4):
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


def u(x):
    x = urllib.parse.unquote(x or "").strip()
    return x if x.startswith("http") else ""


vips = []
for sub in (1, 8):
    m = api("/api/v2/user/get?limit=100&property=subscription_id&property_value=%d" % sub).get("message") or []
    vips += [x for x in m if str(x.get("active")) == "2"]

reviews = api("/api/v2/users_reviews/get?limit=250").get("message") or []
svc_names = {}
meta = {}
for v in vips:
    uid = str(v["user_id"])
    rs = [r for r in reviews if str(r.get("user_id")) == uid and str(r.get("review_status")) == "2" and r.get("rating_overall")]
    rating = round(sum(float(r["rating_overall"]) for r in rs) / len(rs), 1) if rs else None
    specs = []
    for sid in [s.strip() for s in str(v.get("service") or "").split(",") if s.strip()]:
        if sid not in svc_names:
            d = api("/api/v2/list_services/get/%s" % sid).get("message") or []
            d = d[0] if isinstance(d, list) and d else {}
            svc_names[sid] = (d.get("name") or "").strip() if str(d.get("master_id", "0")) != "" else ""
        if svc_names[sid]:
            specs.append(svc_names[sid])
    exp = str(v.get("experience") or "").strip()
    meta[uid] = {
        "verified": str(v.get("verified")) == "1",
        "rating": rating, "reviews": len(rs),
        "since": exp if re.fullmatch(r"(19|20)\d\d", exp) else "",
        "cred": re.sub(r"\s+", " ", str(v.get("credentials") or "")).strip()[:160],
        "specs": specs[:6],
        "web": u(v.get("website")), "fb": u(v.get("facebook")), "ig": u(v.get("instagram")),
        "pay": re.sub(r"\s+", " ", str(v.get("affiliation") or "")).strip()[:90],
    }
json.dump(meta, open(os.path.join(HERE, "vip_meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(meta), "VIPs")
for k, m in meta.items():
    print(k, m["verified"], m["rating"], m["reviews"], m["since"], "|", m["specs"][:3], "|", bool(m["web"]))
