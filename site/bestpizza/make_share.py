from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import sys
IMP=r"C:\Windows\Fonts\impact.ttf"; SEG=r"C:\Windows\Fonts\segoeuib.ttf"
LOGO=r"C:\Users\Matt\Desktop\three village local 2\logo\group (44).png"
def cover(im,W,H,fx=.5,fy=.5):
    r=max(W/im.width,H/im.height); im=im.resize((int(im.width*r+1),int(im.height*r+1)),Image.LANCZOS)
    x=int((im.width-W)*fx); y=int((im.height-H)*fy); return im.crop((x,y,x+W,y+H))
def stroked(d,xy,t,f,fill,sw):
    d.text(xy,t,font=f,fill=fill,stroke_width=sw,stroke_fill=(0,0,0))
def make(src,W,H,out,fx=.5,fy=.5,s=1.0,lines_y=None):
    base=cover(Image.open(src).convert("RGB"),W,H,fx,fy)
    base=ImageEnhance.Color(base).enhance(1.12); base=ImageEnhance.Contrast(base).enhance(1.05)
    # soft shadow band behind text (black, not navy) for readability
    sh=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(sh)
    im=base.convert("RGBA")
    f1=ImageFont.truetype(IMP,int(190*s)); f2=ImageFont.truetype(IMP,int(190*s))
    t1,t2="BEST PIZZA","IN TOWN?"
    y0=lines_y if lines_y else int(H*.08)
    txt=Image.new("RGBA",(W,H),(0,0,0,0)); dt=ImageDraw.Draw(txt)
    for t,f,y,c in ((t1,f1,y0,(255,197,61)),(t2,f2,y0+int(190*s*1.0),(255,255,255))):
        w=dt.textlength(t,font=f); x=(W-w)/2
        # drop shadow
        shd=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(shd).text((x+6*s,y+8*s),t,font=f,fill=(0,0,0,170),stroke_width=int(10*s),stroke_fill=(0,0,0,170))
        im=Image.alpha_composite(im,shd.filter(ImageFilter.GaussianBlur(8*s)))
        dt.text((x,y),t,font=f,fill=c,stroke_width=int(9*s),stroke_fill=(0,0,0))
    im=Image.alpha_composite(im,txt)
    # vote button
    d=ImageDraw.Draw(im); fb=ImageFont.truetype(SEG,int(46*s)); bt="CLICK HERE TO VOTE"
    bw=d.textlength(bt,font=fb)+int(150*s); bh=int(96*s); bx=(W-bw)/2; by=H-bh-int(70*s)
    shd=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(shd).rounded_rectangle((bx,by+10*s,bx+bw,by+bh+10*s),bh/2,fill=(0,0,0,150))
    im=Image.alpha_composite(im,shd.filter(ImageFilter.GaussianBlur(12*s))); d=ImageDraw.Draw(im)
    d.rounded_rectangle((bx,by,bx+bw,by+bh),bh/2,fill=(31,95,174),outline=(255,255,255),width=int(4*s))
    tw=d.textlength(bt,font=fb); tx=bx+(bw-tw-int(40*s))/2; d.text((tx,by+bh/2),bt,font=fb,fill="white",anchor="lm"); ax=tx+tw+int(18*s); ay=by+bh/2; a=int(16*s); d.polygon([(ax,ay-a),(ax+int(22*s),ay),(ax,ay+a)],fill=(255,197,61))
    # logo top-left on a soft dark chip for legibility
    lg=Image.open(LOGO).convert("RGBA"); lw=int(230*s); lg=lg.resize((lw,int(lg.height*lw/lg.width)),Image.LANCZOS)
    chip=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(chip).rounded_rectangle((int(28*s)-14,int(26*s)-12,int(28*s)+lw+14,int(26*s)+lg.height+12),18,fill=(0,0,0,120))
    im=Image.alpha_composite(im,chip.filter(ImageFilter.GaussianBlur(2))); im.alpha_composite(lg,(int(28*s),int(26*s)))
    im.convert("RGB").save(out,quality=90)
make("cheese.jpg",1200,630,"share-fb.jpg",fx=.6,fy=.45,s=.62,lines_y=95)
make("cheese.jpg",1080,1350,"share-ig.jpg",fx=.55,fy=.5,s=1.0,lines_y=150)
