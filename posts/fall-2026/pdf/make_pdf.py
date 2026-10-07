"""Printable Fall Guide PDF (2 pages, US Letter) via local headless Chrome Page.printToPDF."""
import base64, io, json, os, subprocess, time, urllib.request, websocket, qrcode
HERE = os.path.dirname(os.path.abspath(__file__))
URL = "https://www.threevillagelocal.com/blog/fall-in-three-village-2026-guide"
q = qrcode.QRCode(border=1, box_size=10); q.add_data(URL + "?utm_source=pdf"); q.make()
b = io.BytesIO(); q.make_image(fill_color="#13233a", back_color="white").save(b, "PNG")
QR = "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()
from PIL import Image
hb = io.BytesIO(); Image.open(r"C:\Users\Matt\Documents\3vl-share\fall-2026\hero-1600.webp").convert("RGB").resize((1300, 867)).save(hb, "JPEG", quality=72)
hero = "data:image/jpeg;base64," + base64.b64encode(hb.getvalue()).decode()
q2 = qrcode.QRCode(border=1, box_size=10); q2.add_data("https://www.threevillagelocal.com/newsletter?utm_source=pdf"); q2.make()
b2 = io.BytesIO(); q2.make_image(fill_color="#13233a", back_color="white").save(b2, "PNG")
QR2 = "data:image/png;base64," + base64.b64encode(b2.getvalue()).decode()

def item(t, when, where, note=""):
    return '<div class="it"><b>%s</b><span class="w">%s</span><span class="a">%s</span>%s</div>' % (t, when, where, ('<span class="n">%s</span>' % note) if note else "")

P1 = "".join([
 '<h3>&#127875; Farms close to home</h3>',
 item("Benner's Farm open weekends", "Oct 10, 11, 17, 18 &middot; 12-4 PM", "56 Gnarled Hollow Rd, East Setauket", "Farm animals &amp; pumpkins. $12 adults, $10 kids. Website also lists Oct 11: check first."),
 item("Benner's Haunted Hayrides", "Oct 9, 10, 16, 17, 30 &middot; 6-9 PM", "Benner's Farm, East Setauket", "$17/person, online tickets only. First hour is Not-So-Spooky."),
 item("AnnMarie's Farm Stand", "Tue-Sun 12-5:30 (Sun to 5)", "72 N Country Rd, Setauket", "Organic farm produce since 1994."),
 '<h3>&#127806; Village festivals</h3>',
 item("Scarecrow Competition", "Vote Oct 3-25 &middot; free", "Stony Brook Village Center, 111 Main St", "Ballots in village shops. Winners Oct 31."),
 item("Port Jefferson Scarecrow Walk", "Oct 5 - Nov 2 &middot; free", "East Main St, Port Jefferson"),
 item("Witches &amp; Warlocks Weekend", "Sat-Sun Oct 10-11", "Village-wide, Port Jefferson", "Headless Horseman, Witches Quest, Night Market at Danfords 7-9 PM Sat."),
 item("Port Jefferson Harvest Festival", "Oct 17-18 &middot; 12-5 PM", "Village-wide, Port Jefferson", "Activities $5 each or 4 for $45. Costumed Dog Parade Sat 12:30."),
 item("Halloween Family Fun Day", "Sun Oct 25 &middot; 1-4 PM &middot; free", "The Long Island Museum, 1200 Rt 25A", "Costumes, pumpkin painting, crafts."),
 item("Stony Brook Village Halloween Festival", "Sat Oct 31 &middot; 2 PM", "Stony Brook Village Center"),
])
P2 = "".join([
 '<h3>&#127769; A little spooky</h3>',
 item("Sweetbriar Nature Center", "Oct 4, 9, 10, 24", "62 Eckernkamp Dr, Smithtown", "Trick-or-treat trail, lantern walk, Spooktacular ($20), Spooky Species."),
 item("TVHS Spirits Tour", "Sat Oct 17", "Three Village Historical Society", "\"Founding Families.\" Details at tvhs.org."),
 '<h3>&#127809; Leaf walks</h3>',
 item("Frank Melville Memorial Park", "Dawn to dusk &middot; free", "1 Old Field Rd, Setauket"),
 item("West Meadow Beach &amp; Preserve", "Free", "Trustees Rd, Stony Brook", "2-mile trail, best sunsets."),
 item("Avalon Nature Preserve", "7 AM-7 PM, closed Mon &middot; free", "200 Harbor Rd, Stony Brook", "Boardwalk area still closed after 2024 storm."),
 item("Caleb Smith State Park Preserve", "9-5, closed Mon", "581 W Jericho Tpke, Smithtown", "$8 car fee weekends."),
 '<h3>&#128663; Worth the drive</h3>',
 item("Harbes Orchard", "Daily through Nov 1", "5698 Sound Ave, Riverhead", "Apples, pumpkins, corn maze. Go early: Sound Ave jams."),
 item("Hank's Pumpkintown", "Daily through Nov 1", "240 Montauk Hwy, Water Mill", "$24 weekend maze wristband, pumpkins $0.79/lb."),
])
CAL = "".join('<div class="c"><b>%s</b><span>%s</span></div>' % x for x in [
 ("Oct 3-25", "Vote: SB Village scarecrows"), ("Oct 5", "PJ Scarecrow Walk opens"), ("Oct 9", "PJ Fall Art Walk opens &middot; Hayrides"),
 ("Oct 10-11", "Witches &amp; Warlocks Weekend"), ("Oct 15-18", "SBU Homecoming"), ("Oct 17", "Harvest Festival &middot; Dog Parade &middot; Spirits Tour &middot; SBFD Open House"),
 ("Oct 18", "Harvest Festival day 2"), ("Oct 24", "PJ Chowder Crawl &middot; TVHS 250 Festival"), ("Oct 25", "LI Museum Halloween Fun Day"),
 ("Oct 30", "Last farmers market &middot; Hayrides"), ("Oct 31", "SB Village Halloween Festival")])
HTML = """<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Radio+Canada:wght@500;600;700&display=swap" rel="stylesheet">
<style>@page{size:Letter;margin:0}*{box-sizing:border-box;margin:0;padding:0}body{font-family:'Radio Canada',sans-serif;color:#13233a;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.pg{width:8.5in;height:11in;position:relative;overflow:hidden;page-break-after:always;padding:.45in .5in}
.top{height:3.05in;margin:-.45in -.5in .25in;position:relative;background:url(@@HERO@@) center 40%/cover;color:#fff}
.top::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(10,16,28,.92),rgba(10,16,28,.55))}
.tin{position:absolute;inset:0;z-index:1;padding:.42in .5in}.kick{font-size:11pt;letter-spacing:.18em;font-weight:700;color:#ffc53d}
h1{font-size:40pt;line-height:1.02;margin:.1in 0 .12in}h1 span{color:#ffc53d}.dek{font-size:12pt;color:#e5ebf2}
.qr{position:absolute;right:.5in;top:.42in;z-index:1;background:#fff;border-radius:12px;padding:7px;text-align:center;width:1.45in}.qr img{width:100%;display:block}.qr p{font-size:7.5pt;font-weight:700;color:#13233a;margin-top:2px}
h3{font-size:15pt;margin:.2in 0 .09in;padding-bottom:3px;border-bottom:2px solid #ffc53d}
.cols{columns:2;column-gap:.32in}.it{break-inside:avoid;margin:0 0 .15in;font-size:11pt;line-height:1.35}.it b{display:block;font-size:12.4pt}
.w{display:block;color:#b06d00;font-weight:700}.a{display:block;color:#4a5466}.n{display:block;color:#2f3747}
.cal{display:grid;grid-template-columns:1fr 1fr;gap:5px .25in;margin-top:.06in}.c{font-size:11pt;display:flex;gap:8px}.c b{min-width:.8in;color:#b06d00}
.ft{position:absolute;left:.5in;right:.5in;bottom:.3in;display:flex;justify-content:space-between;font-size:8.5pt;color:#6b7383;border-top:1px solid #dde2ea;padding-top:6px}
.brand{font-weight:700;color:#13233a}.brand span{color:#e0a020}.box{background:#f6f2e8;border-radius:12px;padding:.18in .22in;margin-top:.2in}
</style></head><body>
<div class="pg"><div class="top"><div class="tin"><p class="kick">THE 2026 FALL GUIDE</p><h1>Fall in Three Village<br><span>Pumpkins, Hayrides &amp; Festivals</span></h1>
<p class="dek">Setauket &middot; Stony Brook &middot; Port Jefferson &middot; checked Oct 4, 2026</p></div>
<div class="qr"><img src="@@QR@@"><p>Full guide, map &amp; updates</p></div></div>
<div class="cols">@@P1@@</div>
<div class="ft"><span class="brand">Three Village <span>Local</span></span><span>threevillagelocal.com &middot; Schedules can change; confirm with organizers.</span><span>1 / 2</span></div></div>
<div class="pg"><div class="cols">@@P2@@</div>
<div class="box"><h3 style="margin-top:0">&#128197; October at a glance</h3><div class="cal">@@CAL@@</div></div>
<div class="box" style="background:#13233a;color:#fff;display:flex;justify-content:space-between;align-items:center"><div><b style="font-size:13pt">Get guides like this every week</b><br><span style="font-size:10pt;color:#cfd8e3">Three Village Weekly: events, specials and local stories. Free at threevillagelocal.com/newsletter</span></div><img src="@@QR2@@" style="width:.95in;background:#fff;border-radius:8px;padding:4px"></div>
<div class="ft"><span class="brand">Three Village <span>Local</span></span><span>Your local guide to Setauket, Stony Brook &amp; Port Jefferson</span><span>2 / 2</span></div></div>
<script>document.fonts.ready.then(function(){document.title='ready'})</script></body></html>"""
html = HTML.replace("@@P1@@", P1).replace("@@P2@@", P2).replace("@@CAL@@", CAL).replace("@@QR2@@", QR2).replace("@@QR@@", QR).replace("@@HERO@@", hero)
f = os.path.join(HERE, "guide.html"); open(f, "w", encoding="utf-8").write(html)
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
p = subprocess.Popen([CHROME, "--headless=new", "--disable-gpu", "--remote-debugging-port=9375", "--remote-allow-origins=http://127.0.0.1:9375", "--user-data-dir=C:/Users/Matt/AppData/Local/Temp/claude-chrome-profile-fallpdf", "about:blank"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(40):
        try: pg = [t for t in json.load(urllib.request.urlopen("http://127.0.0.1:9375/json")) if t["type"] == "page"][0]; break
        except Exception: time.sleep(.25)
    ws = websocket.create_connection(pg["webSocketDebuggerUrl"], timeout=120); n = [0]
    def cmd(m, **pa):
        n[0] += 1; ws.send(json.dumps({"id": n[0], "method": m, "params": pa}))
        while True:
            r = json.loads(ws.recv())
            if r.get("id") == n[0]: return r.get("result", {})
    cmd("Page.enable"); cmd("Page.navigate", url="file:///" + f.replace("\\", "/"))
    for _ in range(60):
        time.sleep(.3)
        if cmd("Runtime.evaluate", expression="document.title", returnByValue=True)["result"].get("value") == "ready": break
    time.sleep(.5)
    pdf = base64.b64decode(cmd("Page.printToPDF", printBackground=True, preferCSSPageSize=True, paperWidth=8.5, paperHeight=11, marginTop=0, marginBottom=0, marginLeft=0, marginRight=0)["data"])
    out = os.path.join(HERE, "three-village-fall-guide-2026.pdf"); open(out, "wb").write(pdf); print("pdf", len(pdf) // 1024, "KB")
finally: p.terminate()
import pymupdf
d = pymupdf.open(out); print("pages", d.page_count)
for i, pgx in enumerate(d): pgx.get_pixmap(dpi=60).save(os.path.join(HERE, "p%d.png" % (i + 1)))
