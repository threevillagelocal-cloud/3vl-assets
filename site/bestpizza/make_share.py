from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
IMP=r"C:\Windows\Fonts\impact.ttf"; SEG=r"C:\Windows\Fonts\segoeuib.ttf"
LOGO=r"C:\Users\Matt\Desktop\three village local 2\logo\group (44).png"
SRC=Image.open("marg.jpg").convert("RGB")
SRC=ImageEnhance.Color(SRC).enhance(1.12); SRC=ImageEnhance.Contrast(SRC).enhance(1.05)
def cover(im,W,H,fx=.5,fy=.5):
    r=max(W/im.width,H/im.height); im=im.resize((int(im.width*r+1),int(im.height*r+1)),Image.LANCZOS)
    x=int((im.width-W)*fx); y=int((im.height-H)*fy); return im.crop((x,y,x+W,y+H))
def shadow_text(im,xy,t,f,fill,sw,blur):
    W,H=im.size; s=Image.new("RGBA",(W,H),(0,0,0,0))
    ImageDraw.Draw(s).text((xy[0]+5,xy[1]+8),t,font=f,fill=(0,0,0,190),stroke_width=sw+2,stroke_fill=(0,0,0,190))
    im=Image.alpha_composite(im,s.filter(ImageFilter.GaussianBlur(blur)))
    ImageDraw.Draw(im).text(xy,t,font=f,fill=fill,stroke_width=sw,stroke_fill=(0,0,0)); return im
def button(im,cx,cy,fs,pad):
    W,H=im.size; d=ImageDraw.Draw(im); fb=ImageFont.truetype(SEG,fs); bt="CLICK HERE TO VOTE"
    tw=d.textlength(bt,font=fb); a=int(fs*.36); bw=tw+a*2+pad*2+10; bh=int(fs*2.05); bx=cx-bw/2; by=cy-bh/2
    s=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(s).rounded_rectangle((bx,by+10,bx+bw,by+bh+10),bh/2,fill=(0,0,0,150))
    im=Image.alpha_composite(im,s.filter(ImageFilter.GaussianBlur(12))); d=ImageDraw.Draw(im)
    d.rounded_rectangle((bx,by,bx+bw,by+bh),bh/2,fill=(31,95,174),outline=(255,255,255),width=4)
    tx=bx+pad; d.text((tx,cy),bt,font=fb,fill="white",anchor="lm"); ax=tx+tw+18
    d.polygon([(ax,cy-a),(ax+int(a*1.4),cy),(ax,cy+a)],fill=(255,197,61)); return im
def logo(im,x,y,w):
    lg=Image.open(LOGO).convert("RGBA"); lg=lg.resize((w,int(lg.height*w/lg.width)),Image.LANCZOS)
    W,H=im.size; c=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(c).rounded_rectangle((x-18,y-14,x+w+18,y+lg.height+14),22,fill=(0,0,0,135))
    im=Image.alpha_composite(im,c.filter(ImageFilter.GaussianBlur(3))); im.alpha_composite(lg,(x,y)); return im
# FACEBOOK 1200x630: whole pizza on the right, text on the left
W,H=1200,630
bg=cover(SRC,W,H).filter(ImageFilter.GaussianBlur(18)); bg=ImageEnhance.Brightness(bg).enhance(.72)
fg=SRC.resize((int(SRC.width*H/SRC.height),H),Image.LANCZOS)   # 944x630, whole pizza incl crust
im=bg.convert("RGBA"); m=Image.new("L",fg.size,255); md=ImageDraw.Draw(m)
for i in range(120): md.line([(i,0),(i,H)],fill=int(255*i/120))
im.paste(fg,(W-fg.width+40,0),m)
im=logo(im,36,30,330)
f=ImageFont.truetype(IMP,128)
im=shadow_text(im,(40,160),"BEST PIZZA",f,(255,197,61),7,8)
im=shadow_text(im,(40,290),"IN TOWN?",f,(255,255,255),7,8)
im=button(im,250,515,34,34)
im.convert("RGB").save("share-fb.jpg",quality=90)
# INSTAGRAM 1080x1350: logo + headline above, whole pizza middle, button below
W,H=1080,1350
bg=cover(SRC,W,H).filter(ImageFilter.GaussianBlur(22)); bg=ImageEnhance.Brightness(bg).enhance(.7)
im=bg.convert("RGBA"); fg=SRC.resize((1150,int(SRC.height*1150/SRC.width)),Image.LANCZOS)
fg=fg.crop((70,0,70+W,fg.height)); m=Image.new("L",fg.size,255); md=ImageDraw.Draw(m)
for i in range(90): md.line([(0,i),(W,i)],fill=int(255*i/90)); md.line([(0,fg.height-1-i),(W,fg.height-1-i)],fill=int(255*i/90))
im.paste(fg,(0,455),m)
im=logo(im,(W-420)//2,40,420)
f=ImageFont.truetype(IMP,150)
for t,y,c in (("BEST PIZZA",175,(255,197,61)),("IN TOWN?",310,(255,255,255))):
    tw=ImageDraw.Draw(im).textlength(t,font=f); im=shadow_text(im,((W-tw)/2,y),t,f,c,8,9)
im=button(im,W//2,1268,44,44)
im.convert("RGB").save("share-ig.jpg",quality=90)
