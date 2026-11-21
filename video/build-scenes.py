from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import math, random

OUT = Path("video/assets")
OUT.mkdir(parents=True, exist_ok=True)
W,H = 1280,720
FONT_REG = r"C:\Windows\Fonts\msjh.ttc"
FONT_BOLD = r"C:\Windows\Fonts\msjhbd.ttc"

def font(size, bold=False):
    p = FONT_BOLD if bold else FONT_REG
    return ImageFont.truetype(p, size)

def gradient(top,bottom):
    im=Image.new("RGB",(W,H))
    pix=im.load()
    for y in range(H):
        t=y/(H-1)
        col=tuple(round(top[i]*(1-t)+bottom[i]*t) for i in range(3))
        for x in range(W): pix[x,y]=col
    return im

def poly(draw, pts, fill, outline=None, width=1):
    draw.polygon(pts, fill=fill)
    if outline: draw.line(pts+[pts[0]], fill=outline, width=width, joint="curve")

def person(draw,x,y,scale,top,scarf=False,bag=False,older=False,child=False):
    # Stylized editorial cut-paper traveler; shared consultant costume stays fixed.
    head_r=int(22*scale)
    skin=(238,190,150)
    draw.ellipse((x-head_r,y-head_r*2,x+head_r,y),fill=skin)
    # hair cap / side bob
    draw.pieslice((x-head_r-3,y-head_r*2-5,x+head_r+3,y+7),180,360,fill=(37,44,42))
    if not child:
        draw.rounded_rectangle((x-head_r-3,y-head_r,x-head_r+5,y+18),radius=7,fill=(37,44,42))
        draw.rounded_rectangle((x+head_r-5,y-head_r,x+head_r+3,y+18),radius=7,fill=(37,44,42))
    torso_w=int(58*scale); torso_h=int(96*scale)
    draw.rounded_rectangle((x-torso_w//2,y, x+torso_w//2,y+torso_h),radius=int(15*scale),fill=top)
    if scarf:
        draw.polygon([(x-9*scale,y+4*scale),(x+10*scale,y+7*scale),(x+18*scale,y+65*scale),(x+5*scale,y+74*scale)],fill=(222,107,76))
    if bag:
        draw.line((x+torso_w//2-5,y+8*scale,x+torso_w//2+19*scale,y+torso_h*0.72),fill=(225,204,157),width=max(3,int(5*scale)))
        draw.rounded_rectangle((x+torso_w//2+6*scale,y+torso_h*.58,x+torso_w//2+30*scale,y+torso_h*.88),radius=7,fill=(225,204,157))
    if older:
        draw.ellipse((x-head_r-2,y-head_r*2-2,x+head_r+2,y+2),outline=(216,216,206),width=3)
    leg_y=y+torso_h
    draw.line((x-10*scale,leg_y,x-15*scale,leg_y+62*scale),fill=(47,57,55),width=max(5,int(12*scale)))
    draw.line((x+10*scale,leg_y,x+15*scale,leg_y+62*scale),fill=(47,57,55),width=max(5,int(12*scale)))
    draw.line((x-15*scale,leg_y+62*scale,x-30*scale,leg_y+64*scale),fill=(42,50,48),width=max(4,int(10*scale)))
    draw.line((x+15*scale,leg_y+62*scale,x+30*scale,leg_y+64*scale),fill=(42,50,48),width=max(4,int(10*scale)))

def overlay(im, label, title, subtitle, foot):
    d=ImageDraw.Draw(im,"RGBA")
    # dark translucent title field
    d.rounded_rectangle((54,48,690,235),radius=24,fill=(12,35,35,198),outline=(255,255,255,40),width=2)
    d.text((82,70),label,font=font(24,True),fill=(205,228,119))
    d.text((80,111),title,font=font(49,True),fill=(255,250,237))
    d.text((82,178),subtitle,font=font(24),fill=(239,239,223))
    # footer source/context band
    d.rectangle((0,653,W,H),fill=(11,30,31,220))
    d.text((55,672),foot,font=font(18),fill=(246,243,229))
    d.text((1032,674),"示意畫面",font=font(20,True),fill=(225,126,91))
    return im.convert("RGB")

# Segment 1: coastal layers / intertidal observation
im=gradient((237,180,111),(32,112,123)); d=ImageDraw.Draw(im,"RGBA")
# luminous sun haze
glow=Image.new("RGBA",(W,H),(0,0,0,0)); gd=ImageDraw.Draw(glow)
for r,a in [(160,12),(115,18),(74,28)]:
    gd.ellipse((910-r,154-r,910+r,154+r),fill=(255,221,151,a))
im=Image.alpha_composite(im.convert("RGBA"),glow); d=ImageDraw.Draw(im,"RGBA")
d.ellipse((865,109,955,199),fill=(255,221,151,245))
# distant sea bands
for i,(y,c) in enumerate([(320,(80,156,157,255)),(380,(47,125,139,255)),(450,(25,91,111,255)),(520,(19,75,90,255))]):
    d.polygon([(0,y+18),(350,y-16),(720,y+10),(1280,y-25),(1280,720),(0,720)],fill=c)
# abstract rocky coast foreground
poly(d,[(0,410),(110,360),(208,386),(307,331),(390,353),(470,330),(530,406),(626,433),(674,520),(0,569)],(72,83,69,255))
poly(d,[(0,485),(163,427),(260,451),(388,407),(491,455),(590,469),(642,570),(0,632)],(50,65,56,255))
# foam curved lines
for off in [0,40,80]:
    d.arc((490+off,425+off//3,1000+off,610+off//3),195,330,fill=(216,234,217,150),width=4)
# people: parent, child, host
person(d,860,430,.92,(206,151,103,255),child=False)
person(d,936,480,.62,(228,116,82,255),child=True)
person(d,1015,427,.92,(28,78,72,255),scarf=True,bag=True)
im=overlay(im,"01  親子・自然觀察","一起發現海岸細節","地形 × 潮間帶觀察｜出發前確認開放範圍","來源：和平島地質公園／觀光署開放資料｜查詢日 2026-11-21")
im.save(OUT/"scene-01.png",quality=95)

# Segment 2: mountain ridge / view point
im=gradient((252,197,128),(53,112,113)); d=ImageDraw.Draw(im,"RGBA")
d.ellipse((930,92,1050,212),fill=(255,222,164,220))
poly(d,[(0,390),(180,230),(340,356),(520,205),(728,371),(922,248),(1140,365),(1280,280),(1280,720),(0,720)],(78,116,95,255))
poly(d,[(0,465),(205,300),(404,450),(620,292),(828,459),(1040,338),(1280,456),(1280,720),(0,720)],(44,91,76,255))
poly(d,[(0,535),(230,420),(430,515),(650,394),(838,533),(1070,423),(1280,505),(1280,720),(0,720)],(28,71,65,255))
# winding path / viewpoint platform
d.line([(580,720),(630,630),(670,550),(723,502),(808,480)],fill=(219,183,132,255),width=36,joint="curve")
d.line([(580,720),(630,630),(670,550),(723,502),(808,480)],fill=(245,208,153,255),width=18,joint="curve")
d.rounded_rectangle((796,449,1024,475),radius=7,fill=(205,184,148,255))
d.line((814,473,814,517),fill=(225,204,163,255),width=5); d.line((1005,473,1005,517),fill=(225,204,163,255),width=5)
# couple and consultant at platform
person(d,885,348,.70,(70,85,126,255))
person(d,940,350,.70,(177,91,75,255))
person(d,1010,340,.76,(28,78,72,255),scarf=True,bag=True)
# abstract camera in hands
d.rounded_rectangle((862,386,901,411),radius=6,fill=(30,43,43,255)); d.ellipse((875,390,891,406),fill=(200,205,192,255))
im=overlay(im,"02  情侶・景觀提案","把風景留成記憶","二延平步道景觀特色｜天候與路況待確認","來源：觀光署二延平步道頁／景點開放資料｜查詢日 2026-11-21")
im.save(OUT/"scene-02.png",quality=95)

# Segment 3: forest and consultation
im=gradient((242,198,124),(43,104,82)); d=ImageDraw.Draw(im,"RGBA")
# sunlit canopy bands and tree layers
for x,y,r,c in [(105,190,170,(122,151,84,255)),(315,125,180,(79,133,77,255)),(540,208,185,(57,112,78,255)),(800,126,190,(72,131,83,255)),(1110,190,230,(48,104,73,255))]:
    d.ellipse((x-r,y-r,x+r,y+r),fill=c)
# trunks and forest floor
for x,w in [(60,58),(250,43),(457,53),(690,45),(902,55),(1160,72)]:
    d.polygon([(x,100),(x+w,100),(x+w+35,650),(x-20,650)],fill=(46,68,48,230))
poly(d,[(0,490),(200,442),(415,490),(620,431),(858,480),(1066,438),(1280,477),(1280,720),(0,720)],(39,80,57,255))
# host + older couple, keep space under headline
person(d,828,398,.78,(28,78,72,255),scarf=True,bag=True)
person(d,905,412,.73,(118,124,96,255),older=True)
person(d,976,412,.73,(139,96,78,255),older=True)
# consultation card floating as editorial paper block
d.rounded_rectangle((1030,402,1208,540),radius=16,fill=(246,240,220,242))
for yy in [435,468,501]:
    d.rounded_rectangle((1050,yy,1186,yy+8),radius=4,fill=(119,147,111,190))
im=overlay(im,"03  熟齡・需求先行","先談需求，再選路線","步行與無障礙適配｜依旅客需求逐段確認","來源：觀光署阿里山頁／景點開放資料｜查詢日 2026-11-21")
im.save(OUT/"scene-03.png",quality=95)

print("Wrote 3 original illustrated scenes to", OUT)

