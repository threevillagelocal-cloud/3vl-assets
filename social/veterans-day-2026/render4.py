"""Veterans Day 2026 call-for-submissions graphics: IG 4:5, Story 9:16, link preview 1200x630. python render.py"""
import os, subprocess
from PIL import Image, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
CH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
TALL = ("--pw:100%;--pos:center 30%;--fade:linear-gradient(180deg,rgba(255,255,255,0) 60%,#fff 99%);--px:70px;--pr:70px;--al:center;"
        "--id:none;--it:0;--lw:250px;--lm:0 auto 22px;--kf:24px;--hm:22px;--hf:84px;--sm:20px;--sf:34px;--cm:30px;--cf:32px;")
SIZES = {
    "ig": (1080, 1350, TALL + "--ph:500px;--pos:72% 22%;--id:flex;--it:400px;--iw:360px;--ih:236px;--pt:668px;--lw:160px;--lm:0 auto 14px;--kf:22px;--hm:14px;--hf:80px;--sm:18px;--sf:46px;--cm:26px;--cf:44px;", "Submit free <em>&rarr;</em> link in bio"),
    "story": (1080, 1920, TALL + "--ph:660px;--pt:930px;--hf:96px;--sf:54px;--cf:52px;--cm:40px;--sm:26px;--pos:72% 40%;--id:flex;--it:540px;", "Tap to submit free <em>&rarr;</em>"),
    "og": (1200, 630, "--pw:520px;--ph:630px;--pos:78% 40%;--id:none;--it:0;--fade:linear-gradient(90deg,rgba(255,255,255,0) 72%,#fff 100%);--px:540px;--pr:44px;--pt:118px;--al:left;"
                      "--lw:150px;--lm:0 0 16px;--kf:15px;--hm:16px;--hf:52px;--sm:14px;--sf:28px;--cm:22px;--cf:26px;--cp:16px 34px;", "Submit free <em>&rarr;</em>"),
}
SUB = "Veteran-owned business? Veterans Day special?"
src = open(os.path.join(HERE, "vd4.html"), encoding="utf-8").read()
for k, (w, h, vars_, cta) in SIZES.items():
    page = src.replace("<style>", "<style>:root{--w:%dpx;--h:%dpx;%s}" % (w, h, vars_), 1).replace("CTATEXT", cta).replace("SUBTEXT", SUB)
    tmp = os.path.join(HERE, "_r.html"); open(tmp, "w", encoding="utf-8").write(page)
    out = os.path.join(HERE, "vd4-%s.png" % k)
    subprocess.run([CH, "--headless=new", "--disable-gpu", "--user-data-dir=" + os.path.join(HERE, ".cp"), "--hide-scrollbars", "--allow-file-access-from-files",
                    "--force-device-scale-factor=2", "--virtual-time-budget=8000", "--window-size=%d,%d" % (w, h), "--screenshot=" + out, "file:///" + tmp.replace("\\", "/")], capture_output=True)
    im = Image.open(out).convert("RGB")
    if k == "og":
        im.filter(ImageFilter.UnsharpMask(1.2, 70, 2)).save(os.path.join(HERE, "vd4-og-2400.jpg"), quality=95, subsampling=0)
    else:
        im.resize((w, h), Image.LANCZOS).save(out.replace(".png", ".jpg"), quality=93)
    os.remove(out)
os.remove(tmp); print("rendered")
