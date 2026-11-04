from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
exec(open("make_share.py",encoding="utf-8").read().split("# FACEBOOK")[0])
def ctext(im,t,y,f,c,sw=8,bl=9):
    tw=ImageDraw.Draw(im).textlength(t,font=f); return shadow_text(im,((im.width-tw)/2,y),t,f,c,sw,bl)
def pill(im,cx,cy,t,fs,fill,tc):
    d=ImageDraw.Draw(im); f=ImageFont.truetype(SEG,fs); tw=d.textlength(t,font=f); h=int(fs*1.9); w=tw+fs*1.6
    d.rounded_rectangle((cx-w/2,cy-h/2,cx+w/2,cy+h/2),h/2,fill=fill,outline=(255,255,255),width=3)
    d.text((cx,cy),t,font=f,fill=tc,anchor="mm"); return im
RU="Runners-up: Station Pizza & Brew, Vincent's NYWF, Carnival"
# IG 4:5
W,H=1080,1350
bg=cover(SRC,W,H).filter(ImageFilter.GaussianBlur(22)); bg=ImageEnhance.Brightness(bg).enhance(.7)
im=bg.convert("RGBA"); fg=SRC.resize((1150,int(SRC.height*1150/SRC.width)),Image.LANCZOS)
fg=fg.crop((70,0,70+W,fg.height)); m=Image.new("L",fg.size,255); md=ImageDraw.Draw(m)
for i in range(90): md.line([(0,i),(W,i)],fill=int(255*i/90)); md.line([(0,fg.height-1-i),(W,fg.height-1-i)],fill=int(255*i/90))
im.paste(fg,(0,470),m)
im=logo(im,(W-380)//2,36,380)
im=pill(im,W//2,205,"BEST PIZZA 2026 WINNER",40,(31,95,174),"white")
im=ctext(im,"VIA PIZZA",255,ImageFont.truetype(IMP,190),(255,197,61),9,10)
im=ctext(im,"SETAUKET",455,ImageFont.truetype(IMP,70),(255,255,255),6,8)
d=ImageDraw.Draw(im); s=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(s).rounded_rectangle((60,1185,W-60,1310),30,fill=(0,0,0,170)); im=Image.alpha_composite(im,s)
f=ImageFont.truetype(SEG,34); ImageDraw.Draw(im).text((W//2,1222),"Voted #1 by our neighbors",font=f,fill=(255,197,61),anchor="mm")
f=ImageFont.truetype(SEG,29); ImageDraw.Draw(im).text((W//2,1272),RU,font=f,fill="white",anchor="mm")
im.convert("RGB").save("winner-ig.jpg",quality=90)
# FB 1200x630
W,H=1200,630
bg=cover(SRC,W,H).filter(ImageFilter.GaussianBlur(18)); bg=ImageEnhance.Brightness(bg).enhance(.72)
fg=SRC.resize((int(SRC.width*H/SRC.height),H),Image.LANCZOS)
im=bg.convert("RGBA"); m=Image.new("L",fg.size,255); md=ImageDraw.Draw(m)
for i in range(120): md.line([(i,0),(i,H)],fill=int(255*i/120))
im.paste(fg,(W-fg.width+120,0),m)
im=logo(im,36,30,300)
im=pill(im,280,200,"BEST PIZZA 2026 WINNER",28,(31,95,174),"white")
im=shadow_text(im,(36,235),"VIA PIZZA",ImageFont.truetype(IMP,140),(255,197,61),7,8)
im=shadow_text(im,(40,400),"SETAUKET",ImageFont.truetype(IMP,56),(255,255,255),5,7)
im=shadow_text(im,(40,490),"Voted #1 by our neighbors",ImageFont.truetype(SEG,34),(255,255,255),3,5)
im.convert("RGB").save("winner-fb.jpg",quality=90)
