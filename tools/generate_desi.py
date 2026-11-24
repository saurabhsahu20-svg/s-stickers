"""Render original conversational stickers with native-script shaping."""
import json, sys, hashlib
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, features
import generate as base

ROOT=Path(__file__).parent
FONTROOT=Path("/usr/share/fonts/truetype/noto")
def font_for(script,size):
    if script=="Latin": return base.font(size)
    for name in ("NotoSans"+script+"-Bold.ttf","NotoSans"+script+"-Regular.ttf","NotoNaskhArabic-Bold.ttf" if script=="Arabic" else ""):
        if name and (FONTROOT/name).exists():
            return ImageFont.truetype(str(FONTROOT/name),size,layout_engine=ImageFont.Layout.RAQM)
    raise RuntimeError("Missing Noto font for "+script)

def wrap(d, phrase, font, width, direction):
    lines=[]; line=""
    for word in phrase.split():
        candidate=(line+" "+word).strip()
        if line and d.textlength(candidate,font=font,direction=direction)>width:
            lines.append(line);line=word
        else: line=candidate
    if line:lines.append(line)
    return lines

def render(phrase,roman,script,emotion,index):
    im=Image.new("RGBA",(512,512)); d=ImageDraw.Draw(im)
    c=base.PALETTE[index%len(base.PALETTE)]
    accent=base.PALETTE[(index+3)%len(base.PALETTE)]
    # Original expressive mascot and speech bubble, no borrowed sticker art.
    if emotion=="greet":
        base.star(d,108,77,30,c);base.star(d,403,88,24,accent)
        base.ellipse(im,256,116,150,150,"#ffc947")
        d=ImageDraw.Draw(im)
        for x in (230,282):d.arc((x-12,100,x+12,118),0,180,fill="#5c3c40",width=5)
        d.arc((235,120,277,147),0,180,fill="#5c3c40",width=5)
        d.rounded_rectangle((238,145,253,190),radius=7,fill="#ffd4a1",outline="#ac7354",width=2)
        d.rounded_rectangle((259,145,274,190),radius=7,fill="#ffd4a1",outline="#ac7354",width=2)
    else:
        base.face(im,256,112,85,emotion,"#ffc947" if index%3 else c)
        d=ImageDraw.Draw(im)
        base.star(d,101,75,24,accent);base.star(d,406,113,30,c)
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((23,215,489,469),radius=45,fill="#532763")
    d.polygon([(222,224),(254,183),(282,224)],fill=c)
    d.rounded_rectangle((17,205,495,454),radius=43,fill=c,outline="#fff7ff",width=7)
    d.rounded_rectangle((32,220,480,439),radius=32,fill="#fff9ff")
    direction="rtl" if script=="Arabic" else "ltr"
    for size in range(54,19,-2):
        f=font_for(script,size);lines=wrap(d,phrase,f,416,direction)
        bounds=[d.textbbox((0,0),s,font=f,direction=direction) for s in lines]
        heights=[b[3]-b[1] for b in bounds]
        h=sum(heights)+9*(len(lines)-1)
        if len(lines)<=3 and h<=(152 if roman else 196) and all(d.textlength(s,font=f,direction=direction)<=416 for s in lines):break
    area=155 if roman else 207
    y=225+(area-h)/2
    for s,b,lh in zip(lines,bounds,heights):
        d.text((256-(b[2]-b[0])/2-b[0],y-b[1]),s,font=f,fill="#39224e",direction=direction)
        y+=lh+9
    if roman:
        for size in range(27,11,-1):
            f=base.font(size)
            if d.textlength(roman,font=f)<=416:break
        b=d.textbbox((0,0),roman,font=f)
        d.text((256-(b[2]-b[0])/2-b[0],400-b[1]),roman,font=f,fill="#71428a")
    return im

def append(target):
    if not features.check_feature("raqm"): raise RuntimeError("Pillow RAQM shaping required")
    catalog=target/"catalog.json"; rows=json.loads(catalog.read_text(encoding="utf-8"))
    assert len(rows)==1000
    data=json.loads((ROOT/"desi_phrases.json").read_text(encoding="utf-8"))
    hashes={hashlib.sha256(p.read_bytes()).hexdigest() for p in (target/"stickers").glob("*.png")}
    n=0
    for language,script,phrases in data:
        for phrase,roman,emotion in phrases:
            ident=f"{len(rows)+1:04d}"
            im=render(phrase,roman,script,emotion,n)
            p=target/"stickers"/(ident+".png"); im.save(p)
            h=hashlib.sha256(p.read_bytes()).hexdigest()
            assert h not in hashes and im.size==(512,512) and im.getextrema()[3]==(0,255)
            hashes.add(h)
            rows.append({"id":ident,"category":"Desi • "+language,"title":phrase+(" · "+roman if roman else "")})
            n+=1
    assert n==235 and len(hashes)==1000+n
    catalog.write_text(json.dumps(rows,ensure_ascii=False),encoding="utf-8")
    print(f"Verified {n} Desi conversation PNGs; {len(rows)} total files")

if __name__=="__main__":
    base.main()
    append(Path(sys.argv[1]))
