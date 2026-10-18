"""Digitize Fig 5(g) of Lee et al. 2018 (PLoS ONE 13:e0206172) -> fig5g.csv (tier 3).

Two overlapping, semi-transparent grey histograms: 'Section pickup time' (dashed outline) and
'Section pickup and placement time' (solid outline). Where they overlap the grey is darker.
Method (embedded 300 ppi image of p. 11, xref 167):
  1. axis calibration on the tick marks: x 0/50/100 s at columns 1191/1485/1779; y 0/250 at rows 1759.5/1241;
  2. bin grids: the vertical bar outlines are found as columns darker than both neighbours; a regular grid
     (start, width) is fitted to them separately for the dashed and the solid histogram;
  3. per pixel column: top of any grey fill (= the taller bar) and top of the darker overlap fill (= the lower bar,
     when both are present);
  4. each column pair {taller, lower} is assigned to the two series so that every bar is flat across its bin
     (constraint propagation between the two bin grids).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import numpy as np  # noqa: E402
import digitize_common as dc  # noqa: E402

a = dc.embedded_image(str(ROOT / "source/lee2018_lasso.pdf"), 11)
g = dc.gray(a)
X0, X50, X100 = 1191.0, 1485.0, 1779.0      # tick columns (checked in the image: tick centres)
Y0, Y250 = 1759.5, 1241.0                    # axis line centre and 250 tick centre
fx, rx, _ = dc.fit_axis([X0, X50, X100], [0, 50, 100])
pxs = (X100 - X0) / 100
cnt = lambda row: (Y0 - row) / ((Y0 - Y250) / 250)

# 2. outline profile: share of rows where a column is darker than both neighbours by > 20
def edge_profile(r0, r1, c0, c1):
    sub = g[r0:r1, c0 - 1:c1 + 1]
    return c0, (sub[:, 1:-1] < np.minimum(sub[:, :-2], sub[:, 2:]) - 20).mean(0)

def fit_grid(r0, r1, c0, c1, w_range, s_range):
    off, prof = edge_profile(r0, r1, c0, c1)
    best = None
    for w in np.arange(*w_range, 0.01):
        for s in np.arange(*s_range, 0.25):
            pos = np.arange(s, c1, w)
            pos = pos[pos >= c0]
            v = np.mean([prof[int(round(p)) - off] for p in pos if int(round(p)) - off < len(prof)])
            if best is None or v > best[0]:
                best = (v, s, w)
    return best[1], best[2]

sd, wd = fit_grid(1700, 1755, 1195, 1380, (12.4, 13.0), (1201, 1206))     # dashed bars live at 2-35 s
ss, ws = fit_grid(1560, 1755, 1370, 1640, (15.1, 15.8), (1376, 1381))     # solid bars at 30-100 s
ss = ss - ws * np.floor((ss - X0) / ws)   # extend the solid grid to the left
sd = sd - wd * np.floor((sd - X0) / wd)

def runtop(mask, minrun):
    idx = np.where(mask)[0]
    for i in range(len(idx) - minrun + 1):
        if idx[i + minrun - 1] - idx[i] == minrun - 1:
            return idx[i]
    return None

LEG = (1489, 1812, 1236, 1380)   # legend box (columns, rows) to skip
cols = {}
for c in range(int(X0) + 2, int(X100)):
    y0 = LEG[3] if LEG[0] <= c <= LEG[1] else 1236
    col = g[y0:1758, c]
    t = runtop(col < 235, 2)
    if t is None and col[-1] < 235:
        t = len(col) - 1        # a 1-count bar: only its top outline (row 1757) shows above the axis line
    if t is None:
        cols[c] = (0.0, 0.0)
        continue
    dk = runtop((col > 140) & (col < 188), 3)
    hi = cnt(y0 + t + 0.5)                      # first row of the top outline ~ outline centre - 0.5
    lo = cnt(y0 + dk - 1.0) if dk is not None else 0.0   # overlap fill starts just below the lower bar's outline
    if lo > hi - 0.6:
        lo = hi
    cols[c] = (hi, lo)

def bins(s, w):
    e = np.arange(s, X100 + w, w)
    return [(e[i], e[i + 1]) for i in range(len(e) - 1) if e[i] < X100 - 1]

Bd, Bs = bins(sd, wd), bins(ss, ws)
# segments = intersections of a dashed bin and a solid bin; median pair over interior columns (2 px from edges)
segs = []
for i, (d0, d1) in enumerate(Bd):
    for j, (s0, s1) in enumerate(Bs):
        lo_, hi_ = max(d0, s0), min(d1, s1)
        cs = [c for c in cols if lo_ + 2 <= c <= hi_ - 2]
        if len(cs) < 2:
            continue
        his = np.median([cols[c][0] for c in cs]); los = np.median([cols[c][1] for c in cs])
        # style of the taller bar's top outline: solid lines are continuous, dashed ones have gaps
        tops = [int(np.argmax(g[1236 if not (LEG[0] <= c <= LEG[1]) else LEG[3]:1758, c] < 235)) + (1236 if not (LEG[0] <= c <= LEG[1]) else LEG[3]) for c in range(int(np.ceil(lo_)), int(np.floor(hi_)) + 1)]
        trow = int(np.median(tops)) if tops else 0
        line = [g[trow - 1:trow + 3, c].min() for c in range(int(np.ceil(lo_)) + 1, int(np.floor(hi_)))]
        cont = float(np.mean(np.array(line) < 175)) if line else float("nan")
        taller = None
        if abs(d0 - s0) < 5 and abs(d1 - s1) < 5 and his - los > 6:
            # the two bins nearly coincide, so the fill alone cannot tell which series is taller: look for the taller
            # bar's own vertical outline at its left edge, spanning from its top down to the lower bar's top
            r_hi, r_lo = int(Y0 - his * (Y0 - Y250) / 250) + 3, int(Y0 - los * (Y0 - Y250) / 250) - 3
            line = lambda e: max(float(np.mean(g[r_hi:r_lo, c] < 175)) for c in range(int(round(e)) - 1, int(round(e)) + 2))
            ld, ls = line(d0), line(s0)
            taller = "d" if ld > 0.9 and ls < 0.5 else ("s" if ls > 0.9 and ld < 0.5 else None)
            print("coinciding bins", i, j, "dashed-edge line", round(ld, 2), "solid-edge line", round(ls, 2), "->", taller)
        segs.append(dict(i=i, j=j, hi=his, lo=los, n=len(cs), cont=cont, c0=lo_, c1=hi_, taller=taller))
# 4. assignment by coordinate descent: unknown bar heights hd[i] (dashed bins), hs[j] (solid bins);
#    each segment must show max(hd, hs) as the taller fill top and min(hd, hs) as the overlap top.
def cost(a_, b_, sg):
    c_ = sg["n"] * ((max(a_, b_) - sg["hi"]) ** 2 + (min(a_, b_) - sg["lo"]) ** 2)
    if (sg["taller"] == "d" and a_ < b_) or (sg["taller"] == "s" and b_ < a_):
        c_ += 1e9
    return c_

mid = lambda B, k: fx((B[k][0] + B[k][1]) / 2)
hd = {i: float(np.median([sg["hi"] if mid(Bd, i) < 35 else sg["lo"] for sg in segs if sg["i"] == i] or [0])) for i in range(len(Bd))}
hs = {j: float(np.median([sg["lo"] if mid(Bs, j) < 35 else sg["hi"] for sg in segs if sg["j"] == j] or [0])) for j in range(len(Bs))}
for _ in range(30):
    old = (dict(hd), dict(hs))
    for i in hd:
        S = [sg for sg in segs if sg["i"] == i]
        cands = {0.0} | {sg["hi"] for sg in S} | {sg["lo"] for sg in S}
        hd[i] = min(cands, key=lambda v: (sum(cost(v, hs[sg["j"]], sg) for sg in S), v))
    for j in hs:
        S = [sg for sg in segs if sg["j"] == j]
        cands = {0.0} | {sg["hi"] for sg in S} | {sg["lo"] for sg in S}
        hs[j] = min(cands, key=lambda v: (sum(cost(hd[sg["i"]], v, sg) for sg in S), v))
    if (hd, hs) == old:
        break
TOL = 1.6
bad = [sg for sg in segs if abs(max(hd[sg["i"]], hs[sg["j"]]) - sg["hi"]) > TOL or abs(min(hd[sg["i"]], hs[sg["j"]]) - sg["lo"]) > TOL]
rows = []
for name, B, H, s, w in (("Section pickup time", Bd, hd, sd, wd), ("Section pickup and placement time", Bs, hs, ss, ws)):
    for k, (e0, e1) in enumerate(B):
        h = H.get(k, float("nan"))
        rows.append([name, float(fx(e0)), float(fx(e1)), float(h), int(round(h)) if h == h else "",
                     "unresolved" if k not in H else ""])
dc.write_csv(str(HERE / "fig5g.csv"), [
    "Lee et al. 2018, PLoS ONE 13(10):e0206172, Fig 5(g): histogram of single-section pickup and placement time (solid outline)",
    "  and single-section pickup time, only (dashed outline). x axis 'Single section cycle time [s]', 0-100; y axis 'Section count', 0-250.",
    "Columns: series (legend names), bin_left_s / bin_right_s = bin edges in s, count = bar height read off the image (count units),",
    "  count_rounded = nearest integer (counts are integers), flag.",
    "Provenance: tier 3, digitized by fig5g_extract.py from the embedded 300 ppi raster (p. 11); no vector data, no source data.",
    f"  x calibrated on ticks 0/50/100 s (5.88 px per s); y on 0 (axis line) and the 250 tick ({(Y0 - Y250) / 250:.3f} px per count).",
    f"  Bin grids fitted to the bar outlines: dashed bins {wd / pxs:.3f} s wide starting at {fx(sd):.3f} s + k*width;",
    f"  solid bins {ws / pxs:.3f} s wide at {fx(ss):.3f} s + k*width. The two histograms use different bin widths.",
    "  Where the bars overlap the darker grey is read as the lower bar; columns are assigned to the series so that each bar is flat.",
    "Uncertainty: +-1 count (about 2 px); bars of 1-2 counts are only 2-4 px tall (a 1-count bar shows only its top outline).",
    "  Empty bins (count 0) are listed over the whole axis.",
], ["series", "bin_left_s", "bin_right_s", "count", "count_rounded", "flag"], rows,
    fmt=["{}", "{:.3f}", "{:.3f}", "{:.2f}", "{}", "{}"])
(ROOT / "work").mkdir(exist_ok=True)
pts = []
for B, H in ((Bd, hd), (Bs, hs)):
    for k, (e0, e1) in enumerate(B):
        if k in H and H[k] > 0:
            yy = Y0 - H[k] * (Y0 - Y250) / 250
            pts += [(x, yy) for x in np.arange(e0 + 1, e1 - 1, 1.0)]
dc.overlay(a, pts, str(ROOT / "work/fig5g_overlay.png"))
tot = {n: sum(r[4] for r in rows if r[0] == n and r[4] != "") for n in ("Section pickup time", "Section pickup and placement time")}
print("grid dashed", sd, wd, "solid", ss, ws, "unexplained segments", len(bad), [(b["i"], b["j"], round(b["hi"], 1), round(b["lo"], 1)) for b in bad])
print("totals", tot)
