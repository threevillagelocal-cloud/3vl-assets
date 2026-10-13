"""Nightly speed check (added 10/13/2026, owner: "i feel like we keep fixing the same issues over and over").
Runs Google's Lighthouse (phone test) twice on each key page of 3VL, Coltrain and SBNA, keeps the better run,
and keeps a 30-night history in sitecheck/speed.json. A page is flagged when its score is 12+ points below its own
median of the previous 7 nights on TWO nights in a row (one slow night is just noise). 3vl-site-guard's
site_check_mail.py emails the owner only when something is flagged.
Usage (CI): python sitecheck/speed.py"""
import json, os, subprocess, statistics, datetime, tempfile

PAGES = [
    "https://www.threevillagelocal.com/",
    "https://www.threevillagelocal.com/this-weekend",
    "https://www.threevillagelocal.com/categories",
    "https://coltrain.com/",
    "https://coltrain.com/heloc",
    "https://coltrain.com/expressequity",
    "https://www.sbna-li.com/",
    "https://www.sbna-li.com/guest",
]
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "speed.json")
DROP = 12


def run(url):
    out = os.path.join(tempfile.mkdtemp(), "lh.json")
    prof = tempfile.mkdtemp(prefix="lhprof")
    try:
        subprocess.run(["npx", "-y", "lighthouse@12.2.1", url, "--quiet", "--only-categories=performance",
                        "--output=json", "--output-path=" + out,
                        "--chrome-flags=--headless=new --no-sandbox --user-data-dir=" + prof],
                       check=True, timeout=240, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        d = json.load(open(out, encoding="utf-8"))
        a = d["audits"]
        return {"score": round((d["categories"]["performance"]["score"] or 0) * 100),
                "lcp": round(a["largest-contentful-paint"]["numericValue"] / 1000, 1),
                "tbt": round(a["total-blocking-time"]["numericValue"]),
                "mb": round(a["total-byte-weight"]["numericValue"] / 1e6, 2)}
    except Exception as e:
        print("lighthouse failed", url, e)
        return None


def main():
    hist = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {"nights": []}
    today = {"when": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), "pages": {}}
    for url in PAGES:
        runs = [r for r in (run(url), run(url)) if r]
        if runs:
            today["pages"][url] = max(runs, key=lambda r: r["score"])
            print(url, today["pages"][url])
    nights = (hist.get("nights") or [])[-29:] + [today]
    flagged = []
    for url, now in today["pages"].items():
        prev = [n["pages"][url]["score"] for n in nights[:-1] if url in n.get("pages", {})]
        if len(prev) < 4:
            continue
        base = statistics.median(prev[-8:-1] if len(prev) > 1 else prev)
        yday = prev[-1]
        if now["score"] <= base - DROP and yday <= base - DROP:
            flagged.append({"url": url, "score": now["score"], "usual": base, "lcp": now["lcp"], "tbt": now["tbt"], "mb": now["mb"]})
    json.dump({"when": today["when"], "flagged": flagged, "nights": nights}, open(OUT, "w", encoding="utf-8"), indent=1)
    print("flagged", flagged)


if __name__ == "__main__":
    main()
