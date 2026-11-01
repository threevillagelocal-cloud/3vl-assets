"""Veterans Day 2026 call-for-submissions graphics: IG 4:5, Story 9:16, link preview 1200x630. python render.py"""
import os, subprocess
from PIL import Image, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
CH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
TALL = ("--pw:100%;--pos:center 30%;--fade:linear-gradient(180deg,rgba(255,255,255,0) 60%,#fff 99%);--px:70px;--pr:70px;--al:center;"
        "--lw:250px;--lm:0 auto 22px;--kf:24px;--hm:22px;--hf:84px;--sm:20px;--sf:34px;--cm:30px;--cf:32px;")
SIZES = {
    "ig": (1080, 1350, TALL + "--ph:660px;--pt:630px;--sf:32px;", "Submit free by Nov 5 &middot; <em>link in bio</em>"),
    "story": (1080, 1920, TALL + "--ph:900px;--pt:860px;--hf:92px;--sf:36px;", "Submit free by Nov 5 &middot; <em>tap the link</em>"),
    "og": (1200, 630, "--pw:500px;--ph:630px;--pos:42% 30%;--fade:linear-gradient(90deg,rgba(255,255,255,0) 72%,#fff 100%);--px:540px;--pr:44px;--pt:56px;--al:left;"
                      "--lw:150px;--lm:0 0 16px;--kf:15px;--hm:16px;--hf:50px;--sm:12px;--sf:20px;--cm:20px;--cf:20px;", "Submit free by Nov 5"),
}
src = open(os.path.join(HERE, "vd.html"), encoding="utf-8").read()
for k, (w, h, vars_, cta) in SIZES.items():
    page = src.replace("<style>", "<style>:root{--w:%dpx;--h:%dpx;%s}" % (w, h, vars_), 1).replace("CTATEXT", cta)
    tmp = os.path.join(HERE, "_r.html"); open(tmp, "w", encoding="utf-8").write(page)
    out = os.path.join(HERE, "vd-%s.png" % k)
    subprocess.run([CH, "--headless=new", "--disable-gpu", "--user-data-dir=" + os.path.join(HERE, ".cp"), "--hide-scrollbars", "--allow-file-access-from-files",
                    "--force-device-scale-factor=2", "--virtual-time-budget=8000", "--window-size=%d,%d" % (w, h), "--screenshot=" + out, "file:///" + tmp.replace("\\", "/")], capture_output=True)
    im = Image.open(out).convert("RGB")
    if k == "og":
        im.filter(ImageFilter.UnsharpMask(1.2, 70, 2)).save(os.path.join(HERE, "vd-og-2400.jpg"), quality=95, subsampling=0)
    else:
        im.resize((w, h), Image.LANCZOS).save(out.replace(".png", ".jpg"), quality=93)
    os.remove(out)
os.remove(tmp); print("rendered")
