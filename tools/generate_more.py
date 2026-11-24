"""Additional readable Mumbai, Gujarati and Telugu stickers."""
import hashlib,json
from pathlib import Path
from generate_pb import render

def append(target,font_for,wrap):
    catalog=target/"catalog.json"
    rows=json.loads(catalog.read_text(encoding="utf-8"))
    assert len(rows)==1361
    packs=json.loads((Path(__file__).parent/"more_daily.json").read_text(encoding="utf-8"))
    hashes={hashlib.sha256(p.read_bytes()).hexdigest() for p in (target/"stickers").glob("*.png")}
    n=0
    for category,script,phrases in packs:
        for phrase,roman,hindi,emotion in phrases:
            im=render(phrase,roman,hindi,script,emotion,100+n,font_for,wrap)
            ident=f"{len(rows)+1:04d}"
            p=target/"stickers"/(ident+".png");im.save(p)
            h=hashlib.sha256(p.read_bytes()).hexdigest()
            assert h not in hashes and im.size==(512,512) and im.getextrema()[3]==(0,255)
            hashes.add(h)
            rows.append({"id":ident,"category":"Desi • "+category,"title":phrase+" · "+roman+" · "+hindi})
            n+=1
    assert n==59 and len(rows)==1420 and len(hashes)==len(rows)
    catalog.write_text(json.dumps(rows,ensure_ascii=False),encoding="utf-8")
    print(f"Verified {n} additional conversation stickers; {len(rows)} total")
