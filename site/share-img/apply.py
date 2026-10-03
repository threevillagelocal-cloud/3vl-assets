"""Put share images + new titles/descriptions LIVE on BD.
For each listing: 301 /share/<slug>.jpg -> GitHub Pages image, then set seo_social_page_image + the 4 SEO text fields.
Backup of the previous values: backups/seo_before_<date>.json (from seo_src.json).  Log: apply_log.json
Usage: python apply.py [user_id ...]   (no ids = everyone in seo_plan.json)"""
import json, os, subprocess, sys, time, urllib.parse, shutil
from bdkey import key
import gen

HERE = os.path.dirname(os.path.abspath(__file__))
KEY = key(); SITE = "https://www.threevillagelocal.com"
PAGES = "https://threevillagelocal-cloud.github.io/3vl-share/l/"
SPECIAL = {"282": "share/setauket-frame-shop-v3.jpg", "272": "share/northshore-properties-realty-v2.jpg", "301": "share/tina-lollo-v2.jpg", "261": "share/frank-prinzevalli-v2.jpg", "287": "share/evan-teich-v2.jpg", "233": "share/eric-sinensky-v2.jpg", "276": "share/jodi-fein-v2.jpg", "298": "share/howard-hanna-coach-realtors-v2.jpg", "435": "share/kristin-bodkin-v2.jpg"}  # FB already cached older frame-shop URLs


def call(method, path, data):
    body = urllib.parse.urlencode(data)
    for _ in range(5):
        out = subprocess.run(["curl", "-s", "-X", method, "-H", "X-Api-Key: " + KEY, "-H", "Content-Type: application/x-www-form-urlencoded",
                              "--data-binary", body, SITE + path], capture_output=True, text=True, encoding="utf-8").stdout
        time.sleep(1.2)
        try:
            d = json.loads(out)
        except Exception:
            d = {"status": "error", "message": out[:200]}
        if "too many" in str(d.get("message", "")).lower():
            time.sleep(65); continue
        return d
    return {"status": "error", "message": "rate limited"}


def existing_share_redirects():
    got, page = {}, ""
    while True:
        q = "?limit=100&property=old_filename&property_value=share/&property_operator=starts_with" + ("&page=" + page if page else "")
        out = subprocess.run(["curl", "-s", "-H", "X-Api-Key: " + KEY, SITE + "/api/v2/redirect_301/get" + q], capture_output=True, text=True, encoding="utf-8").stdout
        time.sleep(1.2)
        d = json.loads(out); msg = d.get("message")
        if not isinstance(msg, list):
            break
        for r in msg:
            got[r["old_filename"]] = r
        page = str(d.get("next_page") or "")
        if not page:
            break
    return got


def main():
    os.makedirs(os.path.join(HERE, "backups"), exist_ok=True)
    bk = os.path.join(HERE, "backups", "seo_before_2026-09-28.json")
    if not os.path.exists(bk):
        shutil.copy(os.path.join(HERE, "seo_src.json"), bk)
    plan = {p["user_id"]: p for p in json.load(open(os.path.join(HERE, "seo_plan.json"), encoding="utf-8"))}
    ms = {m["user_id"]: m for m in json.load(open(os.path.join(HERE, "members.json"), encoding="utf-8"))}
    ids = sys.argv[1:] or list(plan)
    have = existing_share_redirects()
    print(len(have), "existing /share/ redirects")
    logp = os.path.join(HERE, "apply_log.json")
    log = json.load(open(logp, encoding="utf-8")) if os.path.exists(logp) else {}
    for i, uid in enumerate(ids):
        if log.get(uid, {}).get("ok"):
            continue
        m, p = ms[uid], plan[uid]
        s = gen.slug(m)
        if not os.path.exists(os.path.join(HERE, "out", s + ".jpg")):
            log[uid] = {"ok": False, "why": "no image"}; continue
        old = SPECIAL.get(uid, "share/%s.jpg" % s)
        target = PAGES + s + ".jpg"
        r = have.get(old)
        if r and r.get("new_filename") != target:
            res = call("PUT", "/api/v2/redirect_301/update", {"redirect_id": r["redirect_id"], "new_filename": target})
        elif not r:
            res = call("POST", "/api/v2/redirect_301/create", {"old_filename": old, "new_filename": target})
        else:
            res = {"status": "success"}
        if res.get("status") != "success":
            log[uid] = {"ok": False, "why": "redirect: %s" % str(res.get("message"))[:150]}; continue
        data = {"user_id": uid, "seo_social_page_image": SITE + "/" + old}
        for f in ("seo_page_title", "seo_page_description", "seo_social_page_title", "seo_social_page_description"):
            if p.get(f):
                data[f] = p[f]
        res = call("PUT", "/api/v2/user/update", data)
        ok = res.get("status") == "success"
        log[uid] = {"ok": ok, "slug": s, "share": old} if ok else {"ok": False, "why": "user: %s" % str(res.get("message"))[:150]}
        if i % 20 == 0:
            json.dump(log, open(logp, "w", encoding="utf-8"), indent=0)
            print(i, s, ok, flush=True)
    json.dump(log, open(logp, "w", encoding="utf-8"), indent=0)
    print("OK", sum(1 for v in log.values() if v.get("ok")), "FAILED", [(k, v.get("why")) for k, v in log.items() if not v.get("ok")])


if __name__ == "__main__":
    main()
