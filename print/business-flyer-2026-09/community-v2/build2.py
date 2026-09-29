import base64,re,io,subprocess,os,glob
from PIL import Image
D=os.path.dirname(os.path.abspath(__file__))
def b64(p,maxw=None,q=88):
    im=Image.open(p).convert('RGB')
    if maxw and im.width>maxw: im=im.resize((maxw,round(im.height*maxw/im.width)),Image.LANCZOS)
    b=io.BytesIO();im.save(b,'JPEG',quality=q);return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
qr=open('../qr.svg').read();qr=qr[qr.index('<svg'):];qr=re.sub(r'width="[^"]+" height="[^"]+"','width="100%" height="100%" shape-rendering="crispEdges"',qr,count=1)
h=open('flyer2.tpl.html',encoding='utf-8').read()
for k in ['sbv','crowd','cc','scare']: h=h.replace('{%s}'%k,b64(k+'.jpg',900))
h=h.replace('{HOME}',b64('../home.png',600)).replace('{QR}',qr)
h=h.replace('{LOGOS}',''.join('<div class="lg"><img src="%s"></div>'%b64(f,240) for f in sorted(glob.glob('logo*.jpg'))))
open('flyer2.html','w',encoding='utf-8').write(h)
CH=r"C:\Program Files\Google\Chrome\Application\chrome.exe"
out=os.path.join(D,'flyer2.pdf')
subprocess.run([CH,"--headless=new","--disable-gpu","--user-data-dir=C:/Users/Matt/AppData/Local/Temp/claude-chrome-profile-pdf","--no-pdf-header-footer","--virtual-time-budget=8000","--print-to-pdf="+out,"file:///"+os.path.join(D,'flyer2.html').replace(os.sep,'/')],capture_output=True,timeout=120)
import pymupdf
d=pymupdf.open(out);print('pages',len(d))
for i,p in enumerate(d): p.get_pixmap(dpi=110).save('prev%d.png'%(i+1))
