"""Layout helpers for the MATLAB source-data pages of Ströh et al. 2022 (used by sd_extract.py)."""
import numpy as np
from PIL import Image
def frame_mask(a):
    a=a.astype(int)
    return (abs(a[:,:,0]-38)<=6)&(abs(a[:,:,1]-38)<=6)&(abs(a[:,:,2]-38)<=6)
def groups(idx):
    g=[]
    for i in idx:
        if g and i<=g[-1][-1]+1: g[-1].append(i)
        else: g.append([i])
    return [int(round(np.mean(x))) for x in g]
def boxes(a):
    """Axes boxes (r0,r1,c0,c1) of the MATLAB figure page: frame lines are RGB(38,38,38)."""
    m=frame_mask(a)
    rows=groups(np.where(m.sum(1)>250)[0])
    out=[]
    for r0,r1 in zip(rows[:-1],rows[1:]):
        if not 250<=r1-r0<=400: continue
        cov=m[r0:r1+1].mean(0)
        cols=groups(np.where(cov>0.6)[0])
        i=0
        while i<len(cols)-1:
            c0,c1=cols[i],cols[i+1]
            if 250<=c1-c0<=400 and m[r0,c0:c1].mean()>0.5 and m[r1,c0:c1].mean()>0.5:
                out.append((r0,r1,c0,c1)); i+=2
            else: i+=1
    return out
if __name__=='__main__':
    import sys
    a=np.array(Image.open(sys.argv[1]).convert('RGB'))
    for b in boxes(a): print(b, b[1]-b[0], b[3]-b[2])

def ticks(a, box, L=3):
    """Tick positions (rows on the y axis, columns on the x axis) found as frame-coloured marks pointing
    inward from BOTH opposite frame sides (MATLAB box on mirrors ticks), so data lines are not mistaken."""
    m=frame_mask(a); r0,r1,c0,c1=box
    left=m[r0+2:r1-1,c0+1:c0+1+L].all(1); right=m[r0+2:r1-1,c1-L:c1].all(1)
    ys=groups(np.where(left&right)[0]+r0+2)
    bot=m[r1-L:r1,c0+2:c1-1].all(0); top=m[r0+1:r0+1+L,c0+2:c1-1].all(0)
    xs=groups(np.where(bot&top)[0]+c0+2)
    return ys,xs

def ocr(img, digits=True):
    import subprocess, tempfile, os
    from PIL import Image
    im=Image.fromarray(img).convert('L')
    im=im.resize((im.width*4, im.height*4), Image.LANCZOS)
    with tempfile.TemporaryDirectory() as d:
        p=os.path.join(d,'x.png'); im.save(p)
        cfg=['-c','tessedit_char_whitelist=0123456789.-'] if digits else []
        out=subprocess.run(['tesseract',p,'-','--psm','7']+cfg,capture_output=True,text=True).stdout
    return out.strip()

def label_crop(a, box, axis, pos):
    r0,r1,c0,c1=box
    if axis=='y':
        crop=a[int(pos)-13:int(pos)+14, max(0,c0-75):c0-4]
    else:
        crop=a[r1+4:r1+32, int(pos)-40:int(pos)+41]
    # trim to dark pixels
    g=crop.mean(2)<140
    if not g.any(): return None
    rr=np.where(g.any(1))[0]; cc=np.where(g.any(0))[0]
    return np.pad(crop[rr[0]:rr[-1]+1, cc[0]:cc[-1]+1], ((8,8),(8,8),(0,0)), constant_values=255)

def parse_float(s):
    s=s.replace(' ','')
    try: return float(s)
    except ValueError: return None

def robust_ticks(pos, txt, nice=None):
    """Tick values from the read labels: take the linear pos->value map that the most labels agree with (within 2 %
    of the label range); labels that agree are used as read, the others are replaced by that map's value rounded to
    the labels' number of decimals. Returns (values, n_agree, notes)."""
    vals = [parse_float(t) for t in txt]
    idx = [i for i, v in enumerate(vals) if v is not None]
    best = None
    for i in idx:
        for j in idx:
            if j <= i or vals[i] == vals[j] or pos[i] == pos[j]:
                continue
            m = (vals[j] - vals[i]) / (pos[j] - pos[i]); b = vals[i] - m * pos[i]
            span = abs(vals[j] - vals[i]) * max(1, (max(pos) - min(pos)) / abs(pos[j] - pos[i]))
            agree = [k for k in idx if abs(m * pos[k] + b - vals[k]) <= 0.02 * span]
            if best is None or len(agree) > len(best[2]):
                best = (m, b, agree)
    if best is None:
        return None, 0, "no fit"
    m, b, agree = best
    dec = max([len(t.split(".")[1]) if "." in t else 0 for t in (txt[k] for k in agree)] + [0])
    out, notes = [], []
    for k, p in enumerate(pos):
        if k in agree:
            out.append(vals[k])
        else:
            out.append(round(m * p + b, dec))
            notes.append(f"{txt[k]!r}->{out[-1]}")
    return out, len(agree), "; ".join(notes)

def colorbar(a, box):
    """Find the colour bar right of a map box: returns (r0,r1,c0,c1) of its colour strip."""
    r0,r1,c0,c1=box
    aa=a.astype(int)
    sat=(aa.max(2)-aa.min(2))>25
    cols=np.where(sat[r0+5:r1-5, c1+5:c1+250].mean(0)>0.9)[0]+c1+5
    g=[]
    for c in cols:
        if g and c==g[-1][-1]+1: g[-1].append(c)
        else: g.append([c])
    g=max(g,key=len)
    bc0,bc1=g[0],g[-1]
    mid=(bc0+bc1)//2
    rows=np.where(sat[:,mid])[0]; rows=rows[(rows>r0-20)&(rows<r1+20)]
    return int(rows.min()),int(rows.max()),int(bc0),int(bc1)

# ---- glyph-template OCR for tick labels (tesseract misreads many of these small labels) ----
def glyphs(crop, side="right"):
    """Connected components of a label crop, left to right: list of (x0, x1, y0, y1, binary glyph)."""
    import cv2
    g = (crop.astype(float).mean(2) < 150).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(g, connectivity=8)
    out = []
    for i in range(1, n):
        x, y, w, h, area = st[i]
        if area < 3:
            continue
        out.append((x, x + w, y, y + h, (lab[y:y + h, x:x + w] == i)))
    out.sort(key=lambda q: q[0])
    # keep the right-most (side="right") or left-most run of glyphs (gaps <= 7 px): drops letters of the rotated
    # axis title next to y labels / colour-bar labels
    if out and side == "left":
        keep = [out[0]]
        for g in out[1:]:
            if g[0] - keep[-1][1] <= 7:
                keep.append(g)
            else:
                break
        out = keep
    elif out:
        keep = [out[-1]]
        for g in reversed(out[:-1]):
            if keep[0][0] - g[1] <= 7 or (g[0] >= keep[0][0]):
                keep.insert(0, g)
            else:
                break
        out = sorted(keep, key=lambda q: q[0])
    return out

def glyph_vec(gl, H):
    """Normalised glyph descriptor: the glyph placed in a box of the label's text height, resized to 10x14."""
    from PIL import Image
    x0, x1, y0, y1, m = gl
    im = Image.fromarray((m * 255).astype(np.uint8)).resize((10, 14), Image.BILINEAR)
    return np.concatenate([np.asarray(im, float).ravel() / 255, [3 * (y1 - y0) / H, 3 * (x1 - x0) / H]])

def read_label(crop, templates, side="right"):
    """Read a numeric tick label by nearest-template matching of each glyph. Returns (text, worst distance)."""
    gs = glyphs(crop, side)
    if not gs:
        return "", 99
    H = max(g[3] - g[2] for g in gs)
    txt, worst = "", 0
    for g in gs:
        if g[3] - g[2] < 0.35 * H and g[1] - g[0] < 0.5 * H:   # small blob near the baseline: decimal point
            txt += "."
            continue
        v = glyph_vec(g, H)
        best = min(templates.items(), key=lambda kv: min(np.abs(v - t).sum() for t in kv[1]))
        d = min(np.abs(v - t).sum() for t in best[1])
        worst = max(worst, d)
        txt += best[0]
    return txt, worst
