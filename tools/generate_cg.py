"""Chhattisgarhi everyday sticker extension, with original pictograms."""
import json, hashlib, math
from pathlib import Path
from PIL import Image, ImageDraw
import generate as base

def icon(im,x,y,kind,c):
    d=ImageDraw.Draw(im)
    ink="#583653"
    if kind=="heart":base.heart(d,x,y,32,"#ff537d")
    elif kind=="sparkle":base.star(d,x,y,31,c);base.star(d,x+26,y-24,11,"#ffc947")
    elif kind in ("yes","no"):
        d.ellipse((x-28,y-28,x+28,y+28),fill="#45bf9d" if kind=="yes" else "#ef6383")
        if kind=="yes":d.line((x-15,y,x-4,y+11,x+16,y-13),fill="white",width=7,joint="curve")
        else:d.line((x-12,y-12,x+12,y+12),fill="white",width=7);d.line((x+12,y-12,x-12,y+12),fill="white",width=7)
    elif kind=="clock":
        d.ellipse((x-30,y-30,x+30,y+30),fill="#fff5d9",outline=c,width=6)
        d.line((x,y-17,x,y,x+14,y+8),fill=ink,width=5,joint="curve")
    elif kind=="food":
        d.ellipse((x-35,y-17,x+35,y+30),fill=c,outline=ink,width=3)
        d.ellipse((x-35,y-25,x+35,y+6),fill="#fff3d4",outline=ink,width=2)
        for k in range(7):d.ellipse((x-24+k*7,y-19+(k%2)*8,x-15+k*7,y-9+(k%2)*8),fill="#f4d89d")
    elif kind=="water":
        d.polygon([(x,y-32),(x-23,y+4),(x+23,y+4)],fill="#69c8f4");d.ellipse((x-23,y-10,x+23,y+31),fill="#69c8f4");d.ellipse((x-12,y-4,x-5,y+10),fill="#e5faff")
    elif kind=="moon":
        d.ellipse((x-29,y-29,x+29,y+29),fill="#ffd66e");d.ellipse((x-8,y-35,x+34,y+9),fill="#fff9ff");base.star(d,x+26,y-13,10,c)
    elif kind=="sun":
        for k in range(8):
            t=k*math.pi/4;d.line((x+math.cos(t)*23,y+math.sin(t)*23,x+math.cos(t)*34,y+math.sin(t)*34),fill="#ffb344",width=5)
        d.ellipse((x-19,y-19,x+19,y+19),fill="#ffca4c")
    elif kind in ("wave","stop"):
        d.rounded_rectangle((x-20,y-4,x+20,y+29),radius=12,fill="#ffd99b",outline=ink,width=2)
        for k in range(4):d.rounded_rectangle((x-18+k*10,y-30+(k%3)*3,x-9+k*10,y+11),radius=5,fill="#ffd99b",outline=ink,width=1)
        d.rounded_rectangle((x-29,y-5,x-13,y+17),radius=6,fill="#ffd99b",outline=ink,width=2)
    elif kind=="eyes":
        for k in (-1,1):
            ex=x+k*16;d.ellipse((ex-14,y-19,ex+14,y+19),fill="white",outline=ink,width=2);d.ellipse((ex-5,y-8,ex+5,y+8),fill=ink)
    elif kind=="walk":
        d.ellipse((x-10,y-30,x+10,y-10),fill=c);d.line((x,y-9,x-4,y+9,x-21,y+29),fill=c,width=7,joint="curve");d.line((x-4,y+9,x+21,y+23),fill=c,width=7);d.line((x,y-5,x+19,y+2),fill=c,width=6)
    else:
        f=base.font(54);d.text((x-14,y-32),"?",font=f,fill=c,stroke_width=1,stroke_fill=ink)

def append(target,render):
    rows=json.loads((target/"catalog.json").read_text(encoding="utf-8"))
    assert len(rows)==1235
    packs=json.loads((Path(__file__).parent/"cg_daily.json").read_text(encoding="utf-8"))
    hashes={hashlib.sha256(p.read_bytes()).hexdigest() for p in (target/"stickers").glob("*.png")}
    n=0
    for pack,phrases in packs:
        for phrase,roman,emotion,kind in phrases:
            index=400+n
            mood="happy" if emotion in ("cool","quiet") else emotion
            im=render(phrase,roman,"Devanagari",mood,index)
            # More distinctive left and right symbols; cover old sparkles within mascot area only.
            d=ImageDraw.Draw(im);d.rectangle((52,37,148,118),fill=(0,0,0,0));d.rectangle((364,70,454,154),fill=(0,0,0,0))
            c=base.PALETTE[index%len(base.PALETTE)]
            icon(im,100,85,kind,c);icon(im,411,116,kind,c)
            if emotion=="cool":
                d=ImageDraw.Draw(im);d.rounded_rectangle((211,84,249,111),radius=7,fill="#38264d");d.rounded_rectangle((263,84,301,111),radius=7,fill="#38264d");d.line((249,95,263,95),fill="#38264d",width=5)
            elif emotion=="quiet":
                d=ImageDraw.Draw(im);d.rounded_rectangle((248,116,264,168),radius=8,fill="#ffdfab",outline="#805643",width=2)
            ident=f"{len(rows)+1:04d}";p=target/"stickers"/(ident+".png");im.save(p)
            h=hashlib.sha256(p.read_bytes()).hexdigest();assert h not in hashes;hashes.add(h)
            assert im.size==(512,512) and im.getextrema()[3]==(0,255)
            rows.append({"id":ident,"category":"Desi • Chhattisgarhi / "+pack,"title":phrase+" · "+roman})
            n+=1
    assert n==53 and len(rows)==1288 and len(hashes)==len(rows)
    (target/"catalog.json").write_text(json.dumps(rows,ensure_ascii=False),encoding="utf-8")
    print(f"Verified {n} new Chhattisgarhi stickers, {len(rows)} total")
