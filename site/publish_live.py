"""Publish the "instant design" files to the always-current folder the site loads them from.

Why: the blog, categories, business results and events designs must start from the page HEAD so BD's plain
layout is never shown (owner, 10/1/2026). The HEAD code box (BD admin > Design Settings > Custom CSS / HEAD)
cannot be changed by the API, so it points at a fixed address that never needs editing:
    https://threevillagelocal-cloud.github.io/3vl-share/live/
This script copies the current files from this repo into ../3vl-share/live and pushes. Live in about a minute
(browsers may keep the old copy for up to 10 minutes).

Run after ANY change to these files:   python site/publish_live.py
"""
import os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.dirname(HERE)
SHARE = os.path.join(os.path.dirname(ASSETS), "3vl-share")
FILES = [   # (source in 3vl-assets, destination under 3vl-share/live)
    ("site/p3/p3.js", "p3/p3.js"),
    ("site/p3/p3.css", "p3/p3.css"),
    ("site/p3/smartsearch.js", "p3/smartsearch.js"),
    ("site/p3/evpage.js", "p3/evpage.js"),             # event pages + next-step block (loads evpage.css itself)
    ("site/p3/evpage.css", "p3/evpage.css"),   # search box; needs p3.js (window.tvlSS)
    ("site/p3/vip_meta.json", "p3/vip_meta.json"),
    ("site/p3/img/cafe-hero.jpg", "p3/img/cafe-hero.jpg"),
    ("site/p3/img/village-hero.jpg", "p3/img/village-hero.jpg"),
    ("site/p3/img/now-glow.jpg", "p3/img/now-glow.jpg"),
    ("events-cal/tvl-cal.js", "events-cal/tvl-cal.js"),
    ("events-cal/tvl-cal.css", "events-cal/tvl-cal.css"),
    ("site/hdr/tvl-bi.woff2", "hdr/tvl-bi.woff2"),      # header icons (subset fonts, see site/hdr/build_hdr.py)
    ("site/hdr/tvl-fa.woff2", "hdr/tvl-fa.woff2"),
    ("site/hdr/logo-540.webp", "hdr/logo-540.webp"),    # small copy of the site logo
]


def git(*a):
    return subprocess.run(["git", "-C", SHARE] + list(a), capture_output=True, text=True)


def main():
    if not os.path.isdir(os.path.join(SHARE, ".git")):
        sys.exit("3vl-share clone not found next to 3vl-assets: " + SHARE)
    git("pull", "--rebase", "--autostash")
    for src, dst in FILES:
        s, d = os.path.join(ASSETS, src), os.path.join(SHARE, "live", dst)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copyfile(s, d)
    git("add", "live")
    if not git("status", "--porcelain", "live").stdout.strip():
        print("live folder already up to date")
        return
    sha = subprocess.run(["git", "-C", ASSETS, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    msg = (sys.argv[1] if len(sys.argv) > 1 else "Publish instant-design files") + " (3vl-assets %s)" % sha
    r = git("commit", "-m", msg)
    print(r.stdout.strip() or r.stderr.strip())
    r = git("push")
    print(r.stderr.strip() or "pushed")
    print("Live at https://threevillagelocal-cloud.github.io/3vl-share/live/ in about a minute.")


if __name__ == "__main__":
    main()
