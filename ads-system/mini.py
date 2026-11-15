import sys,math; import os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from comp import *
from PIL import ImageFilter
Y=(255,203,5); K=(17,17,17); G=(110,110,110)
gt=key_green(os.path.join(os.path.dirname(os.path.abspath(__file__)),'scenes','thumbs.png'))

def star(d,cx,cy,r,col):
    pts=[]
    for i in range(10):
        a=math.pi/2+i*math.pi/5; rr=r if i%2==0 else r*0.45
        pts.append((cx+rr*math.cos(a),cy-rr*math.sin(a)))
    d.polygon(pts,fill=col)

def stamp(c,cx,cy,r):
    d=ImageDraw.Draw(c)
    d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=K)
    d.ellipse((cx-r+8,cy-r+8,cx+r-8,cy+r-8),outline=Y,width=3)
    f1=font('Black',int(r*0.42)); t='12 МІС'; tw=d.textlength(t,font=f1); d.text((cx-tw/2,cy-r*0.62),t,font=f1,fill=Y)
    for i,(t,sz,col) in enumerate([('ГАРАНТІЯ',0.20,(255,255,255)),('ОСОБИСТО ВІД',0.15,(255,255,255)),('ГЕОРГІЯ',0.22,Y)]):
        f=font('ExtraBold',int(r*sz)); tw=d.textlength(t,font=f)
        d.text((cx-tw/2,cy-r*0.08+[0,0.25,0.45][i]*r),t,font=f,fill=col)

def make(W,H,out,photo,name,spec,price,maxw=0.9):
    tall=H/W>1.5
    c=Image.new('RGBA',(W,H),(255,255,255,255)); d=ImageDraw.Draw(c); m=60
    top=int(H*(0.10 if tall else 0.045))
    # wordmark
    d.ellipse((m,top+8,m+26,top+34),fill=Y); d.text((m+38,top),'У ГЕОРГІЯ',font=font('Black',38),fill=K)
    # stamp
    r=105 if not tall else 115; stamp(c,W-m-r+10,top+r-10,r)
    # title
    ty=top+(110 if not tall else 150)
    fT=font('Black',88)
    while d.textlength(name,font=fT)>W-2*m-2*r+10 and ty<top+200: fT=font('Black',fT.size-4)
    d.text((m,ty),name,font=fT,fill=K)
    d.text((m,ty+104),spec,font=font('Medium',38),fill=G)
    # bottom zone
    pb_h=150; pb_y=int(H*(0.78 if tall else 0.80))  # price block top
    # product
    ptop=ty+175; pbot=pb_y-30
    p=fit(photo,int(W*(min(0.80,maxw) if tall else maxw)),pbot-ptop); px=(W-p.width-(30 if tall else 0))+(0 if tall else 0) if tall else (W-p.width)//2+30; py=pbot-p.height
    sh=Image.new('RGBA',c.size,(0,0,0,0)); sd=ImageDraw.Draw(sh)
    sd.ellipse((px+p.width*0.08,pbot-22,px+p.width*0.92,pbot+22),fill=(0,0,0,70)); sh=sh.filter(ImageFilter.GaussianBlur(18)); c.alpha_composite(sh)
    c.alpha_composite(p,(px,py))
    # georgiy bottom-left
    gg=fit(gt,int(W*0.30),int(H*(0.26 if tall else 0.33))); gx=-10; gy=(pbot+40 if tall else H+25)-gg.height
    # price block
    d=ImageDraw.Draw(c)
    fP=font('Black',96); pt=price+' ₴'; pw=d.textlength(pt,font=fP)
    bw=int(pw+70); bx=W-m-bw
    d.rounded_rectangle((bx,pb_y,bx+bw,pb_y+pb_h),radius=24,fill=Y)
    d.text((bx+35,pb_y+pb_h/2-62),pt,font=fP,fill=K)
    fs=font('SemiBold',32); st='або частинами без переплат'; sw=d.textlength(st,font=fs)
    d.text((W-m-sw,pb_y+pb_h+16),st,font=fs,fill=K)
    # stars line
    sy=pb_y+pb_h+70
    fr=font('SemiBold',32); txt='680+ відгуків покупців'; tw=d.textlength(txt,font=fr)
    sx=W-m-tw-5*40-14
    for i in range(5): star(d,sx+18+i*40,sy+20,17,Y)
    d.text((W-m-tw,sy),txt,font=fr,fill=G)
    c.alpha_composite(gg,(gx,gy))
    c.convert('RGB').save(out,quality=93)

