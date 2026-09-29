import base64,re,io,subprocess,os
from PIL import Image
D=os.path.dirname(os.path.abspath(__file__))
def b64(p,maxw=None,q=90):
    im=Image.open(p).convert('RGB')
    if maxw and im.width>maxw: im=im.resize((maxw,round(im.height*maxw/im.width)),Image.LANCZOS)
    b=io.BytesIO();im.save(b,'JPEG',quality=q);return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
qr=open('qr.svg').read();qr=qr[qr.index('<svg'):];qr=re.sub(r'width="[^"]+" height="[^"]+"','width="100%" height="100%" shape-rendering="crispEdges"',qr,1)
h=open('flyer.tpl.html',encoding='utf-8').read()
h=h.replace('{BGF}',b64('bg_front.jpg')).replace('{BGB}',b64('bg_back.jpg')).replace('{HOME}',b64('home.png',700)).replace('{VIP}',b64('vip.png',700)).replace('{PROF}',b64('profile.png',700)).replace('{EVT}',b64('events.png',700)).replace('{QR}',qr)
open('flyer.html','w',encoding='utf-8').write(h)
CH=r"C:\Program Files\Google\Chrome\Application\chrome.exe"
out=os.path.join(D,'flyer.pdf')
subprocess.run([CH,"--headless=new","--disable-gpu","--user-data-dir=C:/Users/Matt/AppData/Local/Temp/claude-chrome-profile-pdf","--no-pdf-header-footer","--virtual-time-budget=8000","--print-to-pdf="+out,"file:///"+os.path.join(D,'flyer.html').replace(os.sep,'/')],capture_output=True,timeout=120)
import fitz
d=fitz.open(out);print('pages',len(d))
for i,p in enumerate(d): p.get_pixmap(dpi=110).save('prev%d.png'%(i+1))
