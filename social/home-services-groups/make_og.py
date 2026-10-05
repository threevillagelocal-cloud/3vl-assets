"""Share images (1200x630) for the five Home Services group pages. Output: ../../../3vl-share/cat/<slug>-v1.jpg"""
import base64, os, subprocess, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "..", "3vl-share", "cat")
PH = os.path.join(HERE, "..", "..", "..", "3vl-share", "site", "home-services")
LOGO = os.path.join(HERE, "..", "..", "site", "hdr", "logo-540.webp")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
GROUPS = [("landscaping-property-maintenance", "land", "Landscaping &amp; Property Maintenance"),
          ("contractor", "contr", "Contractors &amp; Remodeling"),
          ("restoration", "resto", "Flood, Fire &amp; Mold Restoration"),
          ("plumbing-electric-repairs", "repair", "Plumbers, Electricians &amp; Repairs"),
          ("cleaning-organizing", "clean", "Cleaning &amp; Organizing")]


def b64(p):
    return base64.b64encode(open(p, "rb").read()).decode()


def page(photo, title):
    return """<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Radio+Canada:wght@500;700&display=swap" rel="stylesheet">
<style>*{margin:0;box-sizing:border-box}html,body{width:1200px;height:630px;overflow:hidden;font-family:'Radio Canada',sans-serif}
.bg{position:absolute;inset:0;background:url(data:image/webp;base64,%s) center/cover}
.sh{position:absolute;inset:0;background:linear-gradient(90deg,rgba(10,26,46,.88) 0%%,rgba(10,26,46,.66) 46%%,rgba(10,26,46,.05) 78%%)}
.tx{position:absolute;left:64px;top:0;bottom:0;width:640px;display:flex;flex-direction:column;justify-content:center;color:#fff}
.k{font-size:24px;font-weight:500;letter-spacing:.06em;text-transform:uppercase;color:#cfe3f5}
h1{font-size:64px;font-weight:700;line-height:1.02;letter-spacing:-.02em;margin-top:14px;text-shadow:0 4px 20px rgba(0,0,0,.4)}
h1 u{text-decoration:none;background:linear-gradient(transparent 72%%,rgba(240,173,78,.8) 72%%)}
.lg{position:absolute;left:64px;bottom:40px;height:62px;background:#fff;border-radius:12px;padding:7px 12px}</style></head><body>
<div class="bg"></div><div class="sh"></div>
<div class="tx"><div class="k">Three Village Local</div><h1>%s<br><u style="white-space:nowrap">in Three Village</u></h1></div>
<img class="lg" src="data:image/webp;base64,%s"></body></html>""" % (b64(photo), title, b64(LOGO))


os.makedirs(OUT, exist_ok=True)
for slug, ph, title in GROUPS:
    tmp = os.path.join(tempfile.gettempdir(), "og-%s.html" % slug)
    open(tmp, "w", encoding="utf-8").write(page(os.path.join(PH, ph + "-v2.webp"), title))
    png = tmp.replace(".html", ".png")
    subprocess.run([CHROME, "--headless=new", "--user-data-dir=" + os.path.join(tempfile.gettempdir(), "og-chrome"), "--disable-gpu",
                    "--hide-scrollbars", "--force-device-scale-factor=1", "--window-size=1200,630", "--virtual-time-budget=5000",
                    "--screenshot=" + png, "file:///" + tmp.replace("\\", "/")], capture_output=True)
    from PIL import Image
    Image.open(png).convert("RGB").crop((0, 0, 1200, 630)).save(os.path.join(OUT, slug + "-v1.jpg"), quality=86)
    print("ok", slug)
