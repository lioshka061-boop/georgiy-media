from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import numpy as np
F='/usr/share/fonts/opentype/inter/InterDisplay-'
def font(w,s): return ImageFont.truetype(F+w+'.otf',s)

def key_green(path):
    im=Image.open(path).convert('RGBA'); a=np.array(im).astype(np.int16)
    r,g,b=a[...,0],a[...,1],a[...,2]
    m=(g>150)&(g>r+60)&(g>b+60)
    alpha=np.where(m,0,255).astype(np.uint8)
    # despill
    spill=(g>r+20)&(g>b+20)&~m
    a[...,1]=np.where(spill,np.maximum(r,b),g)
    out=Image.fromarray(a.astype(np.uint8),'RGBA'); out.putalpha(Image.fromarray(alpha))
    return out.crop(out.getbbox())

def cut_white(path,crop=None):
    im=Image.open(path).convert('RGB')
    if crop: im=im.crop(crop)
    a=np.array(im).astype(np.int16)
    white=(a.min(axis=2)>236)
    # flood fill from borders
    from collections import deque
    h,w=white.shape; bg=np.zeros_like(white); dq=deque()
    for x in range(w):
        for y in (0,h-1):
            if white[y,x] and not bg[y,x]: bg[y,x]=1; dq.append((y,x))
    for y in range(h):
        for x in (0,w-1):
            if white[y,x] and not bg[y,x]: bg[y,x]=1; dq.append((y,x))
    while dq:
        y,x=dq.popleft()
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
            ny,nx=y+dy,x+dx
            if 0<=ny<h and 0<=nx<w and white[ny,nx] and not bg[ny,nx]: bg[ny,nx]=1; dq.append((ny,nx))
    fg=~bg.astype(bool)
    # white/light products: background flood leaks into white panels -> fill orthogonal hull
    if fg.any():
        light=(a.min(axis=2)>200)[fg].mean()
        if light>0.35:
            # white product on white photo: cutting eats its edges -> clean white rounded card instead
            nz=np.argwhere(a.min(axis=2)<245); y0,x0=nz.min(0); y1,x1=nz.max(0)
            p=int(0.07*max(y1-y0,x1-x0)); h,w=fg.shape
            y0,x0,y1,x1=max(0,y0-p),max(0,x0-p),min(h,y1+p),min(w,x1+p)
            card=Image.new('RGB',(x1-x0+2*p,y1-y0+2*p),(255,255,255)); card.paste(im.crop((x0,y0,x1,y1)),(p,p))
            m=Image.new('L',card.size,0); ImageDraw.Draw(m).rounded_rectangle((0,0,card.width-1,card.height-1),radius=int(0.08*min(card.size)),fill=255)
            card=card.convert('RGBA'); card.putalpha(m); return card
    mask=Image.fromarray(np.where(fg,255,0).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
    out=im.convert('RGBA'); out.putalpha(mask)
    return out.crop(out.getbbox())

def fit(img,maxw,maxh):
    s=min(maxw/img.width,maxh/img.height); return img.resize((int(img.width*s),int(img.height*s)),Image.LANCZOS)

def shadow(c,img,x,y,strength=110,blur=28,dy=18):
    sh=Image.new('RGBA',img.size,(0,0,0,0)); al=img.split()[3].point(lambda v:strength if v>10 else 0)
    sh.putalpha(al); sh=sh.filter(ImageFilter.GaussianBlur(blur))
    c.alpha_composite(sh,(x,y+dy))

def bg_grad(W,H,c1,c2,center=(0.3,0.7)):
    y,x=np.mgrid[0:H,0:W]; cx,cy=center[0]*W,center[1]*H
    d=np.sqrt((x-cx)**2+(y-cy)**2)/max(W,H); t=np.clip(d*1.4,0,1)[...,None]
    arr=(np.array(c1)*(1-t)+np.array(c2)*t).astype(np.uint8)
    return Image.fromarray(arr,'RGB').convert('RGBA')

def text_block(d,x,y,lines,fnt,fill,lh=1.02):
    for ln in lines:
        d.text((x,y),ln,font=fnt,fill=fill); y+=int(fnt.size*lh)
    return y

def pill(d,x,y,txt,fnt,bgc,fg,padx=44,h=None,center_w=None):
    tw=d.textlength(txt,font=fnt); h=h or int(fnt.size*1.9)
    if center_w: x=(center_w-tw-2*padx)//2
    d.rounded_rectangle((x,y,x+tw+2*padx,y+h),radius=h//2,fill=bgc)
    d.text((x+padx,y+(h-fnt.size)//2-int(fnt.size*0.12)),txt,font=fnt,fill=fg)

def autosize(d,lines,weight,maxw,start):
    s=start
    while s>40 and max(d.textlength(l,font=font(weight,s)) for l in lines)>maxw: s-=4
    return font(weight,s)
