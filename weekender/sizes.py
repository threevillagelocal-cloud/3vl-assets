"""Smaller copies of an edition's card photos (speed pass 10/3/2026).
For every <name>-720.webp in weekender/<edition>/ make <name>-360.webp and <name>-540.webp (quality 70), so phones and small
cards download a picture that fits (build.py and weekender.js offer them through srcset; the -720 stays the fallback).
    python weekender/sizes.py <edition>      (run before build.py for every new edition; nightly.py warms these files too)"""
import os, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    ed = sys.argv[1]
    d = os.path.join(HERE, ed)
    n = 0
    for f in sorted(os.listdir(d)):
        if not f.endswith("-720.webp"):
            continue
        im = Image.open(os.path.join(d, f)).convert("RGB")
        for w in (360, 540):
            out = os.path.join(d, f.replace("-720.webp", "-%d.webp" % w))
            if os.path.exists(out) or im.width <= w:
                if im.width <= w and not os.path.exists(out):
                    im.save(out, "WEBP", quality=70, method=6)
                    n += 1
                continue
            im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).save(out, "WEBP", quality=70, method=6)
            n += 1
    print("made", n, "copies in", ed)


if __name__ == "__main__":
    main()
