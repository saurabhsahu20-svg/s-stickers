"""Deterministic original sticker illustrations. No third-party artwork."""
import hashlib, json, math, random, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from functools import lru_cache

GROUPS=[
("Love & Hearts",120,["Sweet heart","Love you","Hugs","Sending love","Heart sparkle"]),
("Laugh & Funny",100,["Big laugh","Giggles","Silly smile","LOL","Happy tears"]),
("Good Morning",70,["Good morning","Rise and shine","Hello sunshine","Fresh start","Sunny day"]),
("Good Night & Sleep",70,["Good night","Sweet dreams","Sleep well","Moonlight","Bedtime"]),
("Sadness",60,["Feeling sad","A little blue","Tears","Need a hug","Miss you"]),
("Angry",40,["Grumpy","Not happy","Annoyed","Oh no","Frustrated"]),
("Teddy Bear",70,["Teddy hug","Little bear","Cuddly bear","Bear smile","Bear friend"]),
("Cute Animals",90,["Kitten","Panda","Puppy","Bunny","Fox"]),
("Flowers",60,["Bloom","Flower for you","Fresh petals","Spring","Beautiful flower"]),
("Birthday",50,["Happy birthday","Make a wish","Birthday cake","Birthday surprise","Celebrate"]),
("Hello & Bye",40,["Hello","Hi there","Goodbye","See you","Hey"]),
("Friendship",40,["Best friends","Friends forever","Together","Thank you","You rock"]),
("Celebration & Festivals",60,["Celebrate","Happy Diwali","Happy Holi","Congratulations","Happy festival"]),
("Reactions",50,["Wow","Nice","Great","Okay","Amazing"]),
("Food & Drinks",40,["Coffee time","Tea time","Cupcake","Ice cream","Donut"]),
("Other Expressions",40,["Sparkle","Cool","Surprised","Thinking","Good vibes"])]
PALETTE=["#ff537d","#ffba38","#9c78ff","#42cbb4","#6bbdff","#ff814e","#e879d4","#80d05e"]
def rgb(h):return tuple(int(h[i:i+2],16) for i in (1,3,5))
@lru_cache(maxsize=100)
def orb(w,h,c):
    im=Image.new("RGBA",(w,h)); p=im.load(); base=rgb(c)
    for y in range(h):
      for x in range(w):
        nx=(x+.5-w/2)/(w/2);ny=(y+.5-h/2)/(h/2); r=nx*nx+ny*ny
        if r<=1:
          glow=max(0,1-math.sqrt((nx+.36)**2+(ny+.45)**2)); shade=.78+.25*(1-ny)/2
          vals=tuple(min(255,int(v*shade+(255-v)*glow*.78)) for v in base)
          p[x,y]=(*vals, min(255,int((1-r)*min(w,h)*100)))
    return im
def ellipse(im,x,y,w,h,c):im.alpha_composite(orb(w,h,c),(int(x-w/2),int(y-h/2)))
def heart(d,x,y,r,c):
    pts=[]
    for k in range(101):
      t=2*math.pi*k/100;pts.append((x+r*math.sin(t)**3,y-r*(13*math.cos(t)-5*math.cos(2*t)-2*math.cos(3*t)-math.cos(4*t))/16))
    d.polygon(pts,fill=c,outline="#a52b64",width=3)
    d.ellipse((x-r*.55,y-r*.55,x-r*.20,y-r*.35),fill="#ffe0e9")
def star(d,x,y,r,c):
    pts=[(x+math.sin(i*math.pi/5)*r*(1 if i%2==0 else .42),y-math.cos(i*math.pi/5)*r*(1 if i%2==0 else .42)) for i in range(10)]
    d.polygon(pts,fill=c)
def face(im,x,y,r,emotion,c="#ffc947"):
    ellipse(im,x,y,r*2,r*2,c);d=ImageDraw.Draw(im)
    for sign in (-1,1):
      ex=x+sign*r*.34;ey=y-r*.18
      if emotion=="sleep":d.arc((ex-r*.17,ey-r*.13,ex+r*.17,ey+r*.12),0,180,fill="#493047",width=7)
      elif emotion=="laugh":d.arc((ex-r*.17,ey-r*.08,ex+r*.17,ey+r*.2),180,360,fill="#493047",width=8)
      else:
        d.ellipse((ex-r*.085,ey-r*.16,ex+r*.085,ey+r*.16),fill="#493047")
        d.ellipse((ex-r*.035,ey-r*.10,ex+r*.025,ey-r*.035),fill="white")
      if emotion=="angry":d.line((ex-r*.16,ey-r*.28-sign*r*.1,ex+r*.16,ey-r*.28+sign*r*.1),fill="#493047",width=8)
      if emotion=="sad":d.polygon([(ex+r*.12,ey+r*.13),(ex+r*.02,ey+r*.43),(ex+r*.23,ey+r*.43)],fill="#74d8ff")
      d.ellipse((ex-r*.19,y+r*.13,ex+r*.12,y+r*.23),fill="#f69d8b")
    if emotion=="sad" or emotion=="angry":d.arc((x-r*.24,y+r*.22,x+r*.24,y+r*.56),180,360,fill="#493047",width=9)
    elif emotion=="sleep":d.ellipse((x-r*.09,y+r*.24,x+r*.09,y+r*.42),fill="#493047")
    elif emotion=="wow":d.ellipse((x-r*.16,y+r*.17,x+r*.16,y+r*.52),fill="#493047")
    else:
      d.pieslice((x-r*.32,y-r*.02,x+r*.32,y+r*.56),0,180,fill="#493047")
      d.rounded_rectangle((x-r*.12,y+r*.40,x+r*.12,y+r*.49),radius=7,fill="#ff819d")
def animal(im,kind,c):
    d=ImageDraw.Draw(im); x=256;y=218
    fur={"Panda":"#fff9ee","Kitten":c,"Puppy":"#c08a59","Bunny":"#f6e8ef","Fox":"#ff9b4b"}.get(kind,"#c68e62")
    for s in (-1,1):
      if kind in ("Kitten","Fox"):d.polygon([(x+s*40,115),(x+s*120,43),(x+s*155,170)],fill=fur,outline="#7a4d53",width=4)
      elif kind=="Bunny":ellipse(im,x+s*58,88,78,148,fur);ellipse(im,x+s*58,88,40,96,"#f8adc8")
      else:ellipse(im,x+s*112,111,98,98,"#454052" if kind=="Panda" else fur);ellipse(im,x+s*112,111,55,55,"#bd8b85")
    ellipse(im,x,y,280,250,fur);d=ImageDraw.Draw(im)
    for s in (-1,1):
      ex=x+s*59
      if kind=="Panda":ellipse(im,ex,y-13,78,91,"#454052")
      d.ellipse((ex-12,y-30,ex+12,y+3),fill="#30243a");d.ellipse((ex-7,y-26,ex-1,y-19),fill="white")
      d.ellipse((ex-25,y+30,ex+20,y+51),fill="#ffb6bc")
    ellipse(im,x,y+36,85,59,"#fff0d7");d=ImageDraw.Draw(im);d.ellipse((x-12,y+15,x+12,y+30),fill="#483040");d.arc((x-28,y+25,x+28,y+54),0,180,fill="#483040",width=5)
def font(size):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf","/System/Library/Fonts/Supplemental/Arial Bold.ttf"]:
      if Path(p).exists():return ImageFont.truetype(p,size)
    return ImageFont.load_default()
def caption(d,t,c):
    for size in range(48,23,-1):
        f=font(size); b=d.textbbox((0,0),t,font=f)
        if b[2]-b[0]<=444 and b[3]-b[1]<=62:break
    w=b[2]-b[0];h=b[3]-b[1];x=256-w/2
    d.rounded_rectangle((max(9,x-19),384,min(503,x+w+19),476),radius=25,fill="#fff9ff",outline=c,width=5)
    d.text((x-b[0],430-h/2-b[1]),t,font=f,fill="#24132e")
def make(group,idx,title,seed):
    rng=random.Random(seed); im=Image.new("RGBA",(512,512));d=ImageDraw.Draw(im);c=PALETTE[idx%len(PALETTE)]; alt=PALETTE[(idx//3+3)%len(PALETTE)]
    for k in range(7):
      x=rng.choice([rng.randint(30,105),rng.randint(407,482)]);y=rng.randint(45,365);star(d,x,y,rng.randint(6,20),PALETTE[rng.randrange(8)])
    if group==0:
      if idx%3==0:heart(d,256,210,145,c);heart(d,115,320,44,alt);heart(d,397,320,44,alt)
      else:face(im,256,210,135,"happy");d=ImageDraw.Draw(im);heart(d,180,180,35,c);heart(d,332,180,35,c);heart(d,365,315,50,alt)
    elif group in (1,4,5,10,13,15):
      emotion={1:"laugh",4:"sad",5:"angry",10:"happy",13:"wow",15:["happy","wow","sleep"][idx%3]}[group]
      face(im,256,210,145,emotion,c if group in (4,5,15) and idx%2==0 else "#ffc947")
      d=ImageDraw.Draw(im)
      if group==1:
        for s in (-1,1):d.ellipse((256+s*100-14,246,256+s*100+14,280),fill="#76d8ff")
      elif group==13:star(d,365,315,47,c)
      elif group==10:d.rounded_rectangle((343,268,435,315),radius=22,fill=c);d.ellipse((355,242,393,303),fill=c)
    elif group==2:
      for k in range(12):
        t=k*math.pi/6;d.line((256+math.cos(t)*130,207+math.sin(t)*130,256+math.cos(t)*163,207+math.sin(t)*163),fill=c,width=13)
      face(im,256,207,115,"happy","#ffcf4d")
    elif group==3:
      ellipse(im,250,207,270,270,"#ffd86c");mask=Image.new("L",im.size);ImageDraw.Draw(mask).ellipse((240,51,455,268),fill=255);im.paste((0,0,0,0),(0,0,512,512),mask);d=ImageDraw.Draw(im);star(d,345,135,45,c);star(d,390,230,20,alt);d.arc((167,207,218,240),0,180,fill="#6a4d60",width=7)
    elif group in (6,7):animal(im,title if group==7 else "Teddy",c)
    elif group==8:
      d.line((256,210,256,370),fill="#34895b",width=15);d.ellipse((157,288,254,330),fill="#64b96f");d.ellipse((258,310,358,354),fill="#64b96f")
      petals=6+idx%4
      for k in range(petals):
        t=k*2*math.pi/petals;ellipse(im,256+math.cos(t)*76,198+math.sin(t)*76,111,111,c)
      ellipse(im,256,198,106,106,"#ffd45a")
    elif group==9:
      d.rounded_rectangle((107,200,405,344),radius=28,fill=c,outline="#85456e",width=4);d.rounded_rectangle((107,190,405,236),radius=23,fill="#fff1d9")
      for k in range(3+idx%3):
        x=155+k*202/(2+idx%3);d.rounded_rectangle((x-8,126,x+8,195),radius=5,fill=alt);d.ellipse((x-12,91,x+12,126),fill="#ffc147")
      for k in range(8):d.ellipse((130+k*33,267,143+k*33,280),fill="#fff7e7")
    elif group==11:
      face(im,174,211,105,"happy",c);face(im,335,211,105,"happy",alt);d=ImageDraw.Draw(im);heart(d,256,306,50,"#ff537d")
    elif group==12:
      if idx%3==1:
        d.pieslice((90,202,422,366),0,180,fill=c,outline="#8f4263",width=5);ellipse(im,256,167,74,135,"#ffb938");ellipse(im,256,180,32,72,"#fff6a5")
      else:
        for k in range(5):ellipse(im,135+k*59,150+(k%2)*38,85,115,PALETTE[(idx+k)%8]);d=ImageDraw.Draw(im);d.line((135+k*59,210+(k%2)*38,256,355),fill="#755271",width=3)
    elif group==14:
      if title=="Ice cream":
        d.polygon([(175,206),(337,206),(256,365)],fill="#d49a55");ellipse(im,256,160,170,150,c)
      elif title=="Donut":
        ellipse(im,256,210,288,288,"#e1a263");ellipse(im,256,192,254,254,c);mask=Image.new("L",im.size);ImageDraw.Draw(mask).ellipse((217,172,295,250),fill=255);im.paste((0,0,0,0),(0,0,512,512),mask)
      elif title=="Cupcake":
        d.polygon([(140,220),(372,220),(329,351),(183,351)],fill=c);ellipse(im,256,180,235,140,alt);ellipse(im,256,106,45,45,"#ff537d")
      else:
        d.rounded_rectangle((140,160,380,330),radius=65,fill=c);d.ellipse((342,189,436,273),outline=c,width=24);d.ellipse((148,150,372,204),fill="#81513c");d.arc((219,68,270,146),90,270,fill=alt,width=9)
    d=ImageDraw.Draw(im);caption(d,title,c)
    return im
def main():
    target=Path(sys.argv[1]); dest=target/"stickers";dest.mkdir(parents=True,exist_ok=True)
    for p in dest.glob("*.png"):p.unlink()
    rows=[]; hashes=set()
    for g,(category,count,titles) in enumerate(GROUPS):
      for i in range(count):
        ident=f"{len(rows)+1:04d}";title=titles[i%len(titles)];im=make(g,i,title,10000*g+i)
        p=dest/(ident+".png");im.save(p,optimize=False)
        h=hashlib.sha256(p.read_bytes()).hexdigest();assert h not in hashes;hashes.add(h)
        assert im.size==(512,512) and im.getextrema()[3][0]==0 and im.getextrema()[3][1]==255
        rows.append({"id":ident,"category":category,"title":title})
    assert len(rows)==1000
    (target/"catalog.json").write_text(json.dumps(rows,ensure_ascii=False),encoding="utf-8")
    print("Verified 1000 unique PNG byte hashes, 16 categories, 512px RGBA.")
if __name__=="__main__":main()
