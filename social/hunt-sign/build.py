"""Three Village Local scavenger hunt counter signs, 4x6 in portrait (fits the 4x6 acrylic sign holders).
Edit stores.json (slug, name, town, logo file in logos/, qr = the check-in link), then:  python build.py [slug ...]
Out: out/<slug>.pdf (print at 100% / actual size on 4x6 card stock or photo paper) + out/<slug>.png preview + out/all-signs.pdf."""
import json, os, subprocess, sys, html
import qrcode
from qrcode.constants import ERROR_CORRECT_H
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "out"); os.makedirs(OUT, exist_ok=True)
T = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
stores = json.load(open(os.path.join(HERE, "stores.json"), encoding="utf-8"))
pick = set(sys.argv[1:])
pdfs = []
for s in stores:
    if pick and s["slug"] not in pick:
        continue
    q = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=20, border=1)
    q.add_data(s["qr"]); q.make(fit=True)
    qf = os.path.join(OUT, "qr-%s.png" % s["slug"])
    q.make_image(fill_color="#0f2a4f", back_color="white").save(qf)
    h = (T.replace("{{LOGO}}", s["logo"]).replace("{{NAME}}", html.escape(s["name"])).replace("{{TOWN}}", html.escape(s.get("town", "")))
          .replace("{{QR}}", "out/qr-%s.png" % s["slug"]))
    hf = os.path.join(HERE, "_%s.html" % s["slug"]); open(hf, "w", encoding="utf-8").write(h)
    pdf, png = os.path.join(OUT, s["slug"] + ".pdf"), os.path.join(OUT, s["slug"] + ".png")
    subprocess.run(["node", os.path.join(HERE, "render.js"), hf.replace("\\", "/"), pdf, png], check=True)
    os.remove(hf); pdfs.append(pdf); print("made", s["name"])
if len(pdfs) > 1:
    import fitz
    doc = fitz.open()
    for f in pdfs:
        doc.insert_pdf(fitz.open(f))
    doc.save(os.path.join(OUT, "all-signs.pdf")); print("all-signs.pdf", len(pdfs))
