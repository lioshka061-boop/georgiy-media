#!/usr/bin/env python3
"""AVI ads-system: Georgiy creatives for Meta ads.
  scene  NAME "pose description"            -> scenes/NAME.png via Gemini (key: $GEMINI_KEY_FILE), logs ledger/gemini.csv
  minimal OUT PHOTO_URL "Name" "spec" PRICE [maxw]
  humor   OUT SCENE PHOTO_URL "line1|line2" "Name · spec" PRICE theme(yellow|night|coffee) [pw]
Outputs 1080x1350 JPG. PHOTO_URL may be a local path.
"""
import sys,os,json,base64,urllib.request,datetime,csv,tempfile
D=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,D)
def photo(p):
    if p.startswith('http'):
        fd,t=tempfile.mkstemp(suffix='.jpg'); os.close(fd)
        req=urllib.request.Request(p,headers={'User-Agent':'Mozilla/5.0'}); open(t,'wb').write(urllib.request.urlopen(req,timeout=60).read()); p=t
    from comp import cut_white; return cut_white(p)
def scene(name,pose):
    key=open(os.environ.get('GEMINI_KEY_FILE','/tmp/.gk')).read().strip()
    parts=[{"inline_data":{"mime_type":"image/png","data":base64.b64encode(open(os.path.join(D,'refs',r),'rb').read()).decode()}} for r in ['ref1.png','ref2.png','ref3.png']]
    parts.append({"text":"Use the pixel-art character Georgiy from the reference images (same face, hair, outfit, same pixel-art style). Draw ONLY him (plus props mentioned), full body: "+pose+". Plain solid pure green #00FF00 background everywhere, no other objects, no text, no floor shadow."})
    body={"contents":[{"parts":parts}],"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"3:4","imageSize":"2K"}}}
    req=urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent?key="+key,data=json.dumps(body).encode(),headers={"Content-Type":"application/json"})
    d=json.load(urllib.request.urlopen(req,timeout=280))
    with open(os.path.join(D,'ledger','gemini.csv'),'a',newline='') as f:
        csv.writer(f).writerow([datetime.date.today().isoformat(),'gemini-3-pro-image 2K',1,'0.14',f'scene:{name}'])
    for p in d["candidates"][0]["content"]["parts"]:
        x=p.get("inlineData") or p.get("inline_data")
        if x: open(os.path.join(D,'scenes',name+'.png'),'wb').write(base64.b64decode(x["data"])); print('ok',name); return
    print('no image',json.dumps(d)[:300]); sys.exit(1)
if __name__=='__main__':
    a=sys.argv[1:]
    if a[0]=='scene': scene(a[1],a[2])
    elif a[0]=='minimal':
        import mini; mini.make(1080,1350,a[1],photo(a[2]),a[3],a[4],a[5],float(a[6]) if len(a)>6 else 0.86); print('ok',a[1])
    elif a[0]=='humor':
        import humor; from comp import key_green
        humor.make(1080,1350,a[1],key_green(os.path.join(D,'scenes',a[2]+'.png')),photo(a[3]),a[4].split('|'),a[5],a[6],a[7] if len(a)>7 else 'yellow',float(a[8]) if len(a)>8 else 0.5); print('ok',a[1])
