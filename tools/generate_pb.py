"""High-contrast Punjabi and Bengali conversation stickers, native/Roman/Hindi."""
import hashlib,json
from pathlib import Path
from PIL import Image, ImageDraw
import generate as base

def block(d, text, script, font_for, wrap, area, maximum, minimum=18):
    x0,y0,x1,y1=area
    for size in range(maximum,minimum-1,-1):
        f=font_for(script,size)
        lines=wrap(d,text,f,x1-x0,"ltr")
        bb=[d.textbbox((0,0),s,font=f,direction="ltr") for s in lines]
        heights=[b[3]-b[1] for b in bb]
        h=sum(heights)+5*(len(lines)-1)
        if h<=y1-y0 and all(b[2]-b[0]<=x1-x0 for b in bb):
            return f,lines,bb,heights,h
    raise ValueError("Text does not fit: "+text)

def draw_block(d, text, script, font_for, wrap, area, maximum, color,minimum=18):
    f,lines,bb,heights,h=block(d,text,script,font_for,wrap,area,maximum,minimum)
    x0,y0,x1,y1=area
    y=y0+(y1-y0-h)/2
    for s,b,lh in zip(lines,bb,heights):
        d.text(((x0+x1-b[2]+b[0])/2-b[0],y-b[1]),s,font=f,fill=color,direction="ltr")
        y+=lh+5

def render(phrase,roman,hindi,script,emotion,i,font_for,wrap):
    im=Image.new("RGBA",(512,512));d=ImageDraw.Draw(im)
    palette=["#6941C6","#A82B60","#007F83","#AC5016","#364CA7","#B43F3F"]
    c=palette[i%len(palette)]
    d.rounded_rectangle((12,109,500,500),radius=44,fill="#302244")
    d.rounded_rectangle((8,101,504,491),radius=43,fill=c,outline="#ffffff",width=5)
    d.rounded_rectangle((21,116,491,477),radius=30,fill="#fffdf7")
    d.rounded_rectangle((29,367,483,467),radius=23,fill=c)
    mood={"heart":"happy","food":"happy"}.get(emotion,emotion)
    base.face(im,256,73,65,mood)
    d=ImageDraw.Draw(im)
    if emotion=="heart":
        base.heart(d,148,64,29,"#f84e78");base.heart(d,364,75,26,"#f84e78")
    elif emotion=="food":
        d.ellipse((116,46,178,96),fill="#ffb44e",outline=c,width=4);d.ellipse((121,43,173,65),fill="#fff4d9",outline=c,width=2)
        d.ellipse((336,44,398,94),fill="#ffb44e",outline=c,width=4);d.ellipse((341,41,393,63),fill="#fff4d9",outline=c,width=2)
    else:
        base.star(d,145,68,24,c);base.star(d,367,68,24,c)
    draw_block(d,phrase,script,font_for,wrap,(30,125,482,303),86,"#21132e",26)
    draw_block(d,roman,"Latin",font_for,wrap,(30,307,482,359),36,"#38294c",17)
    draw_block(d,hindi,"Devanagari",font_for,wrap,(36,373,476,462),44,"#ffffff",19)
    return im

def append(target,font_for,wrap):
    cat=target/"catalog.json";rows=json.loads(cat.read_text(encoding="utf-8"))
    assert len(rows)==1288
    packs=json.loads((Path(__file__).parent/"pb_daily.json").read_text(encoding="utf-8"))
    hashes={hashlib.sha256(p.read_bytes()).hexdigest() for p in (target/"stickers").glob("*.png")}
    n=0
    for category,script,phrases in packs:
        for phrase,roman,hindi,emotion in phrases:
            im=render(phrase,roman,hindi,script,emotion,n,font_for,wrap)
            ident=f"{len(rows)+1:04d}";p=target/"stickers"/(ident+".png");im.save(p)
            h=hashlib.sha256(p.read_bytes()).hexdigest()
            assert h not in hashes and im.size==(512,512) and im.getextrema()[3]==(0,255)
            hashes.add(h)
            rows.append({"id":ident,"category":"Desi • "+category,"title":phrase+" · "+roman+" · "+hindi})
            n+=1
    assert n==73 and len(rows)==1361 and len(hashes)==len(rows)
    cat.write_text(json.dumps(rows,ensure_ascii=False),encoding="utf-8")
    print(f"Verified {n} new readable Punjabi/Bengali PNGs; {len(rows)} total")
