"""Build the fast-header files: small icon fonts with only the icons the site's pages use, and a small logo."""
import re, glob, json, os, subprocess, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
bi = open('bi.css', encoding='utf-8').read()
fa = open('fa.css', encoding='utf-8').read()
bimap = {m.group(1): int(m.group(2), 16) for m in re.finditer(r'\.bi-([a-z0-9-]+)::before\{content:"\\([0-9a-f]+)"\}', bi)}
famap = {}
for m in re.finditer(r'((?:\.fa-[a-z0-9-]+:before,?)+)\{content:"\\([0-9a-f]+)"\}', fa):
    for n in re.findall(r'\.fa-([a-z0-9-]+):before', m.group(1)):
        famap[n] = int(m.group(2), 16)
print('icons defined: bi %d, fa %d' % (len(bimap), len(famap)))
useb, usef = set(), set()
for f in glob.glob('pg_*.html'):
    h = open(f, encoding='utf-8', errors='replace').read()
    useb |= {t for t in re.findall(r'\bbi-([a-z0-9-]+)', h) if t in bimap}
    usef |= {t for t in re.findall(r'\bfa-([a-z0-9-]+)', h) if t in famap}
# icons our own scripts add (3vl-assets)
for root in (r'C:\Users\Matt\Documents\3vl-assets\site', r'C:\Users\Matt\Documents\3vl-assets\weekender', r'C:\Users\Matt\Documents\3vl-assets\events-cal'):
    for f in glob.glob(root + r'\**\*.js', recursive=True) + glob.glob(root + r'\**\*.css', recursive=True):
        try:
            h = open(f, encoding='utf-8', errors='replace').read()
        except Exception:
            continue
        useb |= {t for t in re.findall(r'\bbi-([a-z0-9-]+)', h) if t in bimap}
        usef |= {t for t in re.findall(r'\bfa-([a-z0-9-]+)', h) if t in famap}
print('bi used %d: %s' % (len(useb), ' '.join(sorted(useb))))
print('fa used %d: %s' % (len(usef), ' '.join(sorted(usef))))
out = {}
for name, src, cps in (('tvl-bi', 'bi.woff2', sorted({bimap[x] for x in useb})), ('tvl-fa', 'fa.woff2', sorted({famap[x] for x in usef}))):
    uni = ','.join('U+%04X' % c for c in cps)
    subprocess.check_call([sys.executable, '-m', 'fontTools.subset', src, '--unicodes=' + uni, '--flavor=woff2', '--output-file=' + name + '.woff2',
                           '--no-hinting', '--desubroutinize', '--layout-features=', '--notdef-outline', '--name-IDs=', '--glyph-names'])
    # U+0020 must lead the unicode-range in the HEAD block: without the space character the browser treats BD's
    # full icon font as the "first available font" and downloads it (131 KB + 76 KB) on every page (10/2/2026)
    out[name] = {'range': 'U+0020,' + uni, 'bytes': os.path.getsize(name + '.woff2'), 'n': len(cps)}
    print(name, out[name]['n'], 'icons', out[name]['bytes'], 'bytes')
json.dump(out, open('subsets.json', 'w'), indent=1)
im = Image.open('logo.png'); print('logo', im.size, im.mode)
for w in (700,):
    r = im.convert('RGBA').resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    r.save('logo-%d.webp' % w, 'WEBP', quality=90, method=6)
    print('logo-%d.webp' % w, os.path.getsize('logo-%d.webp' % w), 'bytes', r.size)
