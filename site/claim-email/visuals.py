"""Claim email pictures: each Waiting-to-claim listing shown live on an iPad, as an animated GIF (the page scrolls on
the screen) plus a still JPG (first frame, for Outlook and previews). Saves 3vl-share/email/<name>/claim-<id>.gif|.jpg
    python site/claim-email/visuals.py <name> [user_id ...]
Recipients come from the PRIVATE list (3vl-private/claim-email/recipients.json); nothing private is written here.
Uses a throwaway Chrome profile (never the owner's)."""
import base64, io, json, os, subprocess, sys, tempfile, time, urllib.request
import websocket
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.dirname(os.path.dirname(HERE))
SHARE = os.path.join(os.path.dirname(ASSETS), "3vl-share")
PRIV = os.environ.get("CLAIM_RECIPIENTS") or r"C:\Users\Matt\Documents\3vl-private\claim-email\recipients.json"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
SITE = "https://www.threevillagelocal.com/"
PHOTO = os.path.join(ASSETS, "site", "p3", "img", "village-hero.jpg")
W, H = 1200, 760            # picture size (shown at 600 wide in the email)
SW, SH = 1180, 820          # iPad landscape viewport
GOLD = (255, 197, 61)
PORT = 9391


def font(sz):
    for p in (os.path.join(ASSETS, "site", "share-img", "RadioCanada-Bold.ttf"), "C:/Windows/Fonts/segoeuib.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def background():
    bg = Image.open(PHOTO).convert("RGB")
    s = max(W / bg.width, H / bg.height)
    bg = bg.resize((int(bg.width * s) + 1, int(bg.height * s) + 1)).crop((0, 0, W, H)).filter(ImageFilter.GaussianBlur(10))
    shade = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(shade)
    for x in range(W):
        d.line([(x, 0), (x, H)], fill=(10, 22, 36, int(205 - 70 * x / W)))
    return Image.alpha_composite(bg.convert("RGBA"), shade)


def frame_base():
    """Background + iPad body + pill. Returns the image, the screen box, the pill dot position, font and text."""
    im = background()
    ih = H - 150
    iw = int(ih * SW / SH)
    x0, y0, bez = (W - iw) // 2, 112, 24
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((x0 - bez + 8, y0 - bez + 30, x0 + iw + bez + 8, y0 + ih + bez + 30), 54, fill=(0, 0, 0, 160))
    im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(28)))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).rounded_rectangle((x0 - bez - 12, y0 - bez - 12, x0 + iw + bez + 12, y0 + ih + bez + 12), 60, outline=GOLD + (80,), width=10)
    im = Image.alpha_composite(im, glow.filter(ImageFilter.GaussianBlur(16)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((x0 - bez, y0 - bez, x0 + iw + bez, y0 + ih + bez), 44, fill=(11, 13, 16), outline=(56, 62, 70), width=3)
    d.ellipse((x0 + iw + bez // 2 - 5, y0 + ih // 2 - 5, x0 + iw + bez // 2 + 5, y0 + ih // 2 + 5), fill=(32, 36, 42))
    f = font(30)
    txt = "Your page is live on Three Village Local"
    tw = d.textlength(txt, font=f)
    px = int((W - tw - 74) // 2)
    d.rounded_rectangle((px, 26, px + tw + 74, 78), 26, fill=(255, 255, 255))
    return im, (x0, y0, iw, ih), (px + 28, 52), f, txt


def compose(base, page, y, dot_big):
    im, (x0, y0, iw, ih), (dx, dy), f, txt = base
    out = im.copy()
    view = page.crop((0, y, page.width, y + int(page.width * ih / iw))).resize((iw, ih), Image.LANCZOS)
    m = Image.new("L", (iw, ih), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, iw - 1, ih - 1), 20, fill=255)
    out.paste(view, (x0, y0), m)
    d = ImageDraw.Draw(out)
    if dot_big:
        d.ellipse((dx - 13, dy - 13, dx + 13, dy + 13), fill=(187, 247, 208))
    d.ellipse((dx - 8, dy - 8, dx + 8, dy + 8), fill=(22, 163, 74))
    d.text((dx + 22, dy), txt, font=f, fill=(15, 31, 49), anchor="lm")
    return out.convert("RGB")


def main():
    name, ids = sys.argv[1], set(sys.argv[2:])
    rec = [r for r in json.load(open(PRIV, encoding="utf-8")) if not ids or r["id"] in ids]
    out = os.path.join(SHARE, "email", name)
    os.makedirs(out, exist_ok=True)
    prof = tempfile.mkdtemp(prefix="claimshot-")
    p = subprocess.Popen([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--remote-debugging-port=%d" % PORT,
                          "--remote-allow-origins=http://127.0.0.1:%d" % PORT, "--user-data-dir=" + prof, "about:blank"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(80):
            try:
                pg = [t for t in json.load(urllib.request.urlopen("http://127.0.0.1:%d/json" % PORT)) if t["type"] == "page"][0]; break
            except Exception:
                time.sleep(.25)
        ws = websocket.create_connection(pg["webSocketDebuggerUrl"], timeout=120); n = [0]

        def cmd(m, **pa):
            n[0] += 1; i = n[0]; ws.send(json.dumps({"id": i, "method": m, "params": pa}))
            while True:
                r = json.loads(ws.recv())
                if r.get("id") == i:
                    return r.get("result", {})

        def ev(js):
            return cmd("Runtime.evaluate", expression=js, returnByValue=True).get("result", {}).get("value")
        cmd("Page.enable")
        base = frame_base()
        iw, ih = base[1][2], base[1][3]
        for r in rec:
            cmd("Emulation.setDeviceMetricsOverride", width=SW, height=SH, deviceScaleFactor=1, mobile=False)
            cmd("Page.navigate", url=SITE + r["filename"], referrer="https://www.google.com/"); time.sleep(9)
            for y in (800, 1600, 0):
                ev("window.scrollTo(0,%d)" % y); time.sleep(1)
            d = cmd("Page.captureScreenshot", format="png", captureBeyondViewport=True, clip={"x": 0, "y": 0, "width": SW, "height": 2 * SH, "scale": 1})
            page = Image.open(io.BytesIO(base64.b64decode(d["data"]))).convert("RGB")
            view_h = int(page.width * ih / iw)
            maxy = max(0, min(page.height - view_h, 700))
            ys, durs = [0], [1700]
            for k in range(1, 15):
                t = k / 14; ys.append(int(maxy * t * t * (3 - 2 * t))); durs.append(90)
            durs[-1] = 1600
            for k in range(1, 9):
                t = k / 8; ys.append(int(maxy * (1 - t * t * (3 - 2 * t)))); durs.append(70)
            frames = [compose(base, page, y, i % 4 < 2) for i, y in enumerate(ys)]
            frames[0].save(os.path.join(out, "claim-%s.jpg" % r["id"]), "JPEG", quality=82, optimize=True, progressive=True)
            small = [f.resize((W // 2, H // 2), Image.LANCZOS) for f in frames]
            # one palette from the top, middle and bottom frames, so button colors (blue call, red join) survive
            pick = [small[0], small[len(small) // 3], small[15]]
            sheet = Image.new("RGB", (W // 2, H // 2 * len(pick)))
            for k, s in enumerate(pick):
                sheet.paste(s, (0, k * (H // 2)))
            pal = sheet.quantize(colors=255, method=Image.Quantize.MEDIANCUT)
            q = [s.quantize(palette=pal, dither=Image.Dither.FLOYDSTEINBERG) for s in small]
            gif = os.path.join(out, "claim-%s.gif" % r["id"])
            q[0].save(gif, save_all=True, append_images=q[1:], duration=durs, loop=0, optimize=True, disposal=1)
            print(r["id"], r["company"][:30], "gif", os.path.getsize(gif) // 1024, "KB, jpg",
                  os.path.getsize(gif[:-4] + ".jpg") // 1024, "KB", flush=True)
    finally:
        p.terminate()


if __name__ == "__main__":
    main()
