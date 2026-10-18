"""Fig. 2b (bottom: histogram of automatically reconstructed axon path lengths, log y) of Song et al. 2023 -> fig2b.csv.

Tier 1 (source data): Edmond 10.17617/3.RG58DU, data/Fig.2/Fig.2b/Fig2b_data.mat: pathLen.<dataset>.mapping70.
thresholdSets1 = one path length (um) per automatically reconstructed axon. Fig2b.m draws MATLAB histograms
('DisplayStyle','stairs', automatic binning) of H6_striatum, H13_striatum and AMK_striatum with xlim [0 100] and a
log y axis. The paper shows two: 'Hemisphere' (blue) = H6_striatum (the H6 SBEM dataset, main text) and 'Control'
(black) = AMK_striatum (control striatum dataset, acknowledged A. Khalifa). H13 is not shown.

Binning reproduces MATLAB's automatic rule (Scott's rule 3.5*std/n^(1/3) rounded by binpicker to 1, 2, 3, 5 x 10^k,
edges from 0): bin width 1 um for H6 and 0.5 um for AMK. The bin pitch of the printed stair outlines (vector paths
on PDF p. 3: 0.818 and 0.409 pt at 0.818 pt/um) confirms these widths.

Check: the stair heights in the printed figure (top edge of each bin's outline, converted with the log axis fitted
on the decade tick marks 10^0..10^6) are compared with log10(counts); the residual is written to the CSV header.
Run: python3 -I fig2b_extract.py
"""
import csv
import os

import numpy as np
import pymupdf
import scipy.io as sio

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "../source/edmond_RG58DU/extracted/data/Fig.2/Fig.2b/Fig2b_data.mat")
PDF = os.path.join(HERE, "../source/41592_2023_Article_1866.pdf")


def binpicker_width(x):
    raw = 3.5 * np.std(x, ddof=1) / len(x) ** (1 / 3)
    p = 10 ** np.floor(np.log10(raw)); rel = raw / p
    return p * (1 if rel < 1.5 else 2 if rel < 2.5 else 3 if rel < 4 else 5 if rel < 7.5 else 10)


m = sio.loadmat(SRC, squeeze_me=True, struct_as_record=False)
series = {"Hemisphere": ("H6_striatum", (0.157, 0.667, 0.882)), "Control": ("AMK_striatum", (0.0, 0.0, 0.0))}
hist = {}
for name, (key, col) in series.items():
    x = getattr(m["pathLen"], key).mapping70.thresholdSets1
    w = binpicker_width(x)
    nb = int(np.ceil(x.max() / w))
    edges = np.arange(nb + 1) * w
    c, _ = np.histogram(x, edges)  # numpy: last bin closed, like MATLAB histcounts
    keep = edges[:-1] < 100
    hist[name] = (key, len(x), w, edges[:-1][keep], edges[1:][keep], c[keep])

# --- printed figure: axis calibration from tick marks ---
page = pymupdf.open(PDF)[2]
xt, yt = {}, []
for dr in page.get_drawings():
    r = dr["rect"]
    if dr.get("color") is None or not (390 < r.x0 < 480 and 205 < r.y0 < 282):
        continue
    if abs(r.x1 - r.x0) < 0.01 and 2.5 < r.y1 - r.y0 < 4:  # major x ticks (0, 50, 100), not the y axis line
        xt[round(r.x0, 2)] = 1
    if abs(r.y1 - r.y0) < 0.01 and 3.2 < r.x1 - r.x0 < 4:  # decade y ticks, not the x axis line
        yt.append(round(r.y0, 3))
xt = sorted(xt); yt = sorted(set(yt))[::-1]
assert len(xt) == 3 and len(yt) == 7, (xt, yt)
ax_, bx_ = np.polyfit(xt, [0, 50, 100], 1)
ay_, by_ = np.polyfit(yt, np.arange(7), 1)   # log10(count)
print("x um/pt", ax_, "decade pt", 1 / ay_)
# stair outlines: the stroked line is stored as a filled outline polygon; per bin take the topmost edge
polys = {}
for dr in page.get_drawings():
    if dr.get("fill") and len(dr["items"]) > 500:
        f = dr["fill"]
        polys["Hemisphere" if f[2] > 0.5 else "Control"] = dr
diffs = {}
plotted = {}
for name, dr in polys.items():
    segs = [(it[1], it[2]) for it in dr["items"] if it[0] == "l" and abs(it[1].y - it[2].y) < 1e-3]
    _, _, w, lo, hi, c = hist[name]
    out = []
    for a, b, n in zip(lo, hi, c):
        xm = ((a + b) / 2 - bx_) / ax_
        ys = [p.y for p, q in segs if min(p.x, q.x) <= xm <= max(p.x, q.x)]
        out.append(np.nan if not ys else ay_ * min(ys) + by_)
    plotted[name] = np.array(out)
    # the stroke (0.85 pt) is wider than half a bin (0.41 / 0.20 pt), so at a bin centre the outline's top edge is
    # the vertical stroke of a neighbouring step if a neighbour is higher: compare with max of the 3 neighbours
    cn = np.maximum(c, np.maximum(np.r_[0, c[:-1]], np.r_[c[1:], 0]))
    lc = np.log10(np.where(cn > 0, cn, np.nan))
    d = plotted[name] - lc
    diffs[name] = d[np.isfinite(d)]

rows = []
for name in ("Hemisphere", "Control"):
    key, n, w, lo, hi, c = hist[name]
    for a, b, k, pl in zip(lo, hi, c, plotted[name]):
        rows.append([name, key, f"{a:g}", f"{b:g}", int(k), "" if not np.isfinite(pl) else f"{10 ** pl:.4g}"])
with open(os.path.join(HERE, "fig2b.csv"), "w", newline="") as f:
    for h in [
        "Song et al. 2023 Nat Methods, Fig. 2b bottom (histogram, log y): number of automatically reconstructed axons per",
        "  path-length bin (axon path length in um, x shown 0..100 um), hemisphere striatum (H6, blue) vs control striatum (black).",
        "Provenance: tier 1, source data: Edmond 10.17617/3.RG58DU data/Fig.2/Fig.2b/Fig2b_data.mat, pathLen.<dataset>.",
        "  mapping70.thresholdSets1, binned by fig2b_extract.py like MATLAB's automatic histogram binning (see script).",
        f"  Hemisphere = H6_striatum: {hist['Hemisphere'][1]} axons, bin width {hist['Hemisphere'][2]:g} um;"
        f" Control = AMK_striatum: {hist['Control'][1]} axons, bin width {hist['Control'][2]:g} um. Only bins starting below 100 um.",
        "  Many axons have path length 0 (first bin: >10^5 counts). H13_striatum (also in the file and in Fig2b.m) is not in the paper.",
        "Columns: series; dataset; bin_lo_um, bin_hi_um (bin [lo, hi)); count (from the source data);",
        "  plotted_count = stair height read from the printed vector outline (PDF p. 3; top edge of the stroked outline,",
        "  so about +0.4 pt = +8 % above the line centre), axes fitted on tick marks. Empty = no stair drawn (count 0, log axis).",
        "Agreement (log10 plotted - log10 max(count of the bin and its two neighbours), because the 0.85-pt stroke is wider"
        " than half a bin): Hemisphere median %.3f, 95th pct |dev| %.3f; Control median %.3f, 95th pct |dev| %.3f decades"
        " (median = half the stroke width, 0.037 decade expected)."
        % (np.median(diffs["Hemisphere"]), np.percentile(np.abs(diffs["Hemisphere"] - np.median(diffs["Hemisphere"])), 95),
           np.median(diffs["Control"]), np.percentile(np.abs(diffs["Control"] - np.median(diffs["Control"])), 95)),
        "  A few bins deviate more (max %.2f decade): zero-count bins next to drawn ones and the x = 100 um edge."
        % max(np.max(np.abs(v - np.median(v))) for v in diffs.values()),
    ]:
        f.write("# " + h + "\n")
    w_ = csv.writer(f)
    w_.writerow(["series", "dataset", "bin_lo_um", "bin_hi_um", "count", "plotted_count"])
    w_.writerows(rows)
print({k: (np.median(v), np.percentile(np.abs(v - np.median(v)), [50, 95, 100])) for k, v in diffs.items()})

# --- overlay: source-data stair levels (bin centres, line centre) on a 4x render of the plot region ---
from PIL import Image, ImageDraw  # noqa: E402
Z = 4
reg = pymupdf.Rect(390, 205, 482, 282)
pix = page.get_pixmap(clip=reg, matrix=pymupdf.Matrix(Z, Z))
im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
dd = ImageDraw.Draw(im)
for name, col in (("Hemisphere", (255, 0, 255)), ("Control", (255, 140, 0))):
    _, _, w, lo, hi, c = hist[name]
    for a_, b_, k in zip(lo, hi, c):
        if k <= 0:
            continue
        xp = (((a_ + b_) / 2 - bx_) / ax_ - reg.x0) * Z
        yp = ((np.log10(k) - by_) / ay_ - reg.y0) * Z
        dd.point([(xp, yp)], fill=col)
im.save(os.path.join(HERE, "../work/fig2b_overlay.png"))
