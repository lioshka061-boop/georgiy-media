import sys; import os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from comp import *
from PIL import ImageFilter
Y=(255,203,5); K=(17,17,17); W_=(255,255,255)
def make(W,H,out,scene,photo,lines,name,price,theme='yellow',pw=0.5,gside='left'):
    tall=H/W>1.5
    if theme=='night': c=bg_grad(W,H,(30,40,72),(8,10,22),(0.5,0.4)); hc=W_; sc=(200,208,225)
    elif theme=='coffee': c=bg_grad(W,H,(96,64,40),(36,24,16),(0.5,0.4)); hc=(250,236,210); sc=(225,205,175)
    else: c=Image.new('RGBA',(W,H),Y+(255,)); hc=K; sc=(70,60,20)
    c=c.copy(); d=ImageDraw.Draw(c); m=64
    top=int(H*(0.11 if tall else 0.05))
    f=autosize(d,lines,'Black',W-2*m,140 if tall else 128); y=text_block(d,m,top,lines,f,hc)
    # bottom block
    bb=int(H*(0.78 if tall else 0.965))
    fP=font('Black',72); pt=price+' ₴'; pwid=d.textlength(pt,font=fP)
    ph=104; py=bb-ph-56
    base=py-26
    # georgiy + product
    avail=base-(y+30)
    gg=fit(scene,int(W*0.52),int(avail*1.02))
    pr=fit(photo,int(W*pw),int(avail*0.72))
    if gside=='left': gx=int(W*0.0); px=W-pr.width-int(W*0.03)
    else: gx=W-gg.width; px=int(W*0.03)
    sh=Image.new('RGBA',c.size,(0,0,0,0)); sd=ImageDraw.Draw(sh)
    sd.ellipse((px+pr.width*0.08,base-20,px+pr.width*0.92,base+20),fill=(0,0,0,80)); sh=sh.filter(ImageFilter.GaussianBlur(16)); c.alpha_composite(sh)
    c.alpha_composite(pr,(px,base-pr.height))
    c.alpha_composite(gg,(gx,base+12-gg.height))
    d=ImageDraw.Draw(c)
    # name + price
    fN=font('Bold',40); d.text((m,py+8),name,font=fN,fill=hc)
    d.text((m,py+58),'Гарантія 12 міс особисто від Георгія',font=font('Medium',30),fill=sc)
    bx=W-m-int(pwid+56); d.rounded_rectangle((bx,py,W-m,py+ph),radius=22,fill=Y if theme!='yellow' else K)
    d.text((bx+28,py+ph/2-48),pt,font=fP,fill=K if theme!='yellow' else Y)
    t='Оплата при отриманні · частинами без переплат · доставка 0 ₴'; fs=font('SemiBold',28)
    d.text(((W-d.textlength(t,font=fs))/2,py+ph+20),t,font=fs,fill=sc)
    c.convert('RGB').save(out,quality=93)

