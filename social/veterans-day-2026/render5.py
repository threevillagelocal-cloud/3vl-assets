"""Veterans Day 2026 nomination graphics v5 (IG 4:5, ad 4:5, Story 9:16). python render5.py"""
import os, subprocess
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
CH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
IG = "--ph:600px;--pos:center 28%;--pt:560px;--lw:150px;--kf:21px;--hm:22px;--nf:22px;--hf:78px;--om:32px;--op:24px 22px;--ic:56px;--of:31px;--os:22px;--cm:32px;--cf:38px;--ff:20px;"
ST = "--ph:900px;--pos:center 30%;--pt:800px;--lw:180px;--kf:26px;--hm:30px;--nf:28px;--hf:80px;--om:44px;--op:30px 26px;--ic:64px;--of:34px;--os:25px;--cm:48px;--cf:46px;--ff:26px;"
SIZES = {
    "ig": (1080, 1350, IG, "Nominate free <em>&rarr;</em> link in bio"),
    "ad-ig": (1080, 1350, IG, "Tap to nominate <em>&rarr;</em>"),
    "story": (1080, 1920, ST, "Tap to nominate <em>&rarr;</em>"),
}
src = open(os.path.join(HERE, "vd5.html"), encoding="utf-8").read()
for k, (w, h, vars_, cta) in SIZES.items():
    page = src.replace("<style>", "<style>:root{--w:%dpx;--h:%dpx;%s}" % (w, h, vars_), 1).replace("CTATEXT", cta)
    tmp = os.path.join(HERE, "_r.html"); open(tmp, "w", encoding="utf-8").write(page)
    out = os.path.join(HERE, "vd5-%s.png" % k)
    subprocess.run([CH, "--headless=new", "--disable-gpu", "--user-data-dir=" + os.path.join(HERE, ".cp"), "--hide-scrollbars", "--allow-file-access-from-files",
                    "--force-device-scale-factor=2", "--virtual-time-budget=8000", "--window-size=%d,%d" % (w, h), "--screenshot=" + out, "file:///" + tmp.replace("\\", "/")], capture_output=True)
    Image.open(out).convert("RGB").resize((w, h), Image.LANCZOS).save(out.replace(".png", ".jpg"), quality=93)
    os.remove(out)
os.remove(tmp); print("rendered")
