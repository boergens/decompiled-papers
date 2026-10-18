"""Digitize Figure 2a of Templier 2019 (eLife 8:e45696, PDF p.4): the four pairwise similarity matrices.

Source: the embedded JPEG of Figure 2 (9615 x 2297 px, ~1313 ppi; no vector paths on the page).
    python3 -I fig2a_extract.py   -> fig2a.csv (+ ../work/fig2a_overlay*.png, ../work/fig2a_rebuilt.png)

Method
- Each matrix is drawn as a grid of square grey cells inside a black axes frame. The frame lines
  (minima of the mean grey profile across each matrix) sit on the outer edges of the cell grid: the
  frame-to-frame distance is 995 px = 204 cells of 4.877 px. A period/phase fit of the grey-level
  edges inside each matrix gives the same period (4.8775 px) and puts the cell edges where the frame
  grid predicts (within 0.4 px), and the labelled ticks 0, 100, 200 (and unlabelled ticks at 50, 150)
  fall on cell centres 0, 50, ..., 200 (within 1.6 px). So the matrices have 204 x 204 cells,
  index k centred on axis value k.
- Each cell is sampled as the median grey level (mean of R, G, B) of its inner pixels (a square of
  half-width 1.5 px around the centre, clipped to the area inside the frame lines), which avoids the
  JPEG ringing at cell edges and the frame.
- Panel 4 carries two horizontal and two vertical semi-transparent red lines (the caption's "two red
  lines"); cells whose inner pixels are mostly red are flagged and get no grey value.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../tools"))   # tools/digitize_common.py
import numpy as np  # noqa: E402
from digitize_common import embedded_image, gray, frame_lines, write_csv, overlay  # noqa: E402

PDF = os.path.join(HERE, "../source/elife-45696-v3.pdf")
WORK = os.path.join(HERE, "../work")
a = embedded_image(PDF, 4)
g = gray(a)
dark = g < 100
N = 204

# frame lines of each matrix: minima of the mean grey profile across the panel (each line ~3 px wide)
def line_centre(profile, lo, hi):
    """Darkness-weighted centre of the dark line inside profile[lo:hi] (index in profile coordinates)."""
    seg = 255 - profile[lo:hi]
    k = int(np.argmax(seg))
    w = seg[max(0, k - 2):k + 3]
    idx = np.arange(max(0, k - 2), max(0, k - 2) + len(w))
    return lo + float((w * idx).sum() / w.sum())


APPROX = {1: (352, 1347, 102, 1097), 2: (1420, 2415, 104, 1099), 3: (351, 1345, 1145, 2140), 4: (1418, 2413, 1147, 2142)}
PANELS = {}
for m, (l0, r0, t0, b0) in APPROX.items():
    colp = g[t0 + 150:b0 - 150, :].mean(0)
    rowp = g[:, l0 + 150:r0 - 150].mean(1)
    PANELS[m] = (line_centre(colp, l0 - 6, l0 + 6), line_centre(colp, r0 - 6, r0 + 6),
                 line_centre(rowp, t0 - 6, t0 + 6), line_centre(rowp, b0 - 6, b0 + 6))


def edge_fit(profile):
    """Period and phase of the cell edges in a 1-D grey profile (sum of |gradient|)."""
    best = None
    for P in np.arange(4.85, 4.92, 0.0025):
        for ph in np.arange(0, P, 0.05):
            idx = np.round(ph + np.arange(0, (len(profile) - ph) / P) * P).astype(int)
            idx = idx[idx < len(profile)]
            sc = profile[idx].mean()
            if best is None or sc > best[0]:
                best = (sc, P, ph)
    return best[1], best[2]


# the printed panel numbers 1-4 are drawn over the upper right cells of each matrix: mask their strokes
import cv2  # noqa: E402
labelmask = np.zeros(g.shape, bool)
label_bbox = {}
for m, (L, R, T, B) in PANELS.items():
    y0, x0 = int(T) + 3, int(L) + 150 * 5
    sub = (g[y0:int(T) + 200, x0:int(R) - 3] < 110).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(sub, connectivity=8)
    big = [k for k in range(1, n) if st[k, 3] > 40]      # glyph is ~105 px tall; matrix cells are ~5 px
    assert len(big) == 1, (m, big)
    k = big[0]
    glyph = cv2.dilate((lab == k).astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
    labelmask[y0:y0 + sub.shape[0], x0:x0 + sub.shape[1]] |= glyph
    label_bbox[m] = (x0 + st[k, 0], y0 + st[k, 1], x0 + st[k, 0] + st[k, 2], y0 + st[k, 1] + st[k, 3])
ai = a.astype(int)
redmask = (ai[:, :, 0] - ai[:, :, 1] > 60) & (ai[:, :, 0] - ai[:, :, 2] > 60)

rows, pts, rebuilt = [], [], np.full(a.shape[:2], 255.0)
periods = []
for m, (L, R, T, B) in PANELS.items():
    px, py = (R - L) / N, (B - T) / N
    periods.append((px, py))
    sub = g[int(T) + 4:int(B) - 3, int(L) + 4:int(R) - 3]
    Px, phx = edge_fit(np.abs(np.diff(sub, axis=1)).sum(0))
    Py, phy = edge_fit(np.abs(np.diff(sub, axis=0)).sum(1))
    # residual of the fitted cell edges against the frame-based grid (in px, modulo one cell)
    ex = ((int(L) + 4 + phx + 0.5 - L) / px) % 1
    ey = ((int(T) + 4 + phy + 0.5 - T) / py) % 1
    ex, ey = min(ex, 1 - ex) * px, min(ey, 1 - ey) * py
    print(f"matrix {m}: frame grid {px:.4f} x {py:.4f} px/cell; edge fit {Px:.4f} x {Py:.4f} px/cell, "
          f"edge offset from frame grid {ex:.2f} px (x), {ey:.2f} px (y)")
    assert abs(Px - px) < 0.01 and abs(Py - py) < 0.01 and ex < 1.0 and ey < 1.0
    xin0, xin1 = L + 2.5, R - 2.5                  # clear of the frame lines (3 px wide + antialiasing)
    yin0, yin1 = T + 2.5, B - 2.5
    for i in range(N):                              # row index (y, from the top)
        yc = T + (i + 0.5) * py
        ya, yb = max(yc - 1.5, yin0), min(yc + 1.5, yin1)
        for j in range(N):                          # column index (x, from the left)
            xc = L + (j + 0.5) * px
            xa, xb = max(xc - 1.5, xin0), min(xc + 1.5, xin1)
            ys = slice(int(np.ceil(ya)), int(np.floor(yb)) + 1)
            xs = slice(int(np.ceil(xa)), int(np.floor(xb)) + 1)
            patch = g[ys, xs]
            red = redmask[ys, xs].mean() > 0.4
            if labelmask[ys, xs].any():
                v = np.nan
                flag = "panel_label"
            elif red:
                v = np.nan
                flag = "red_line"
            else:
                v = float(np.median(patch))
                flag = "partly_hidden" if min(patch.shape) < 3 else ""
            rows.append((m, i, j, v, (1 - v / 255) if v == v else np.nan, flag))
            if i % 17 == 0 and j % 17 == 0:
                pts.append((xc, yc))
            y0p, y1p = int(round(T + i * py)), int(round(T + (i + 1) * py))
            x0p, x1p = int(round(L + j * px)), int(round(L + (j + 1) * px))
            rebuilt[y0p:y1p, x0p:x1p] = v if v == v else 128

# checks: rebuild the matrices from the samples and compare with the source pixels
for m, (L, R, T, B) in PANELS.items():
    ys = slice(int(T) + 3, int(B) - 2)
    xs = slice(int(L) + 3, int(R) - 2)
    diff = np.abs(rebuilt[ys, xs] - g[ys, xs])
    ok = ~redmask[ys, xs] & ~labelmask[ys, xs]
    print(f"matrix {m}: frame L={L:.1f} R={R:.1f} T={T:.1f} B={B:.1f}; median |rebuilt-source| = "
          f"{np.median(diff[ok]):.1f} grey levels, 95th pct {np.percentile(diff[ok], 95):.1f}")
from PIL import Image  # noqa: E402
Image.fromarray(np.clip(rebuilt[:2300, :2500], 0, 255).astype(np.uint8)).save(os.path.join(WORK, "fig2a_rebuilt.png"))
# overlays: every 17th cell centre over the whole panel, and all cell centres over two zoomed corners
overlay(a[:2300, :2500], pts, os.path.join(WORK, "fig2a_overlay.png"))
allc = []
for m in (1, 4):
    L, R, T, B = PANELS[m]
    for i in list(range(0, 12)) + list(range(N - 12, N)):
        for j in list(range(0, 12)) + list(range(N - 12, N)):
            allc.append((L + (j + 0.5) * (R - L) / N, T + (i + 0.5) * (B - T) / N))
big = a.copy()
for x, y in allc:
    big[int(round(y)), int(round(x))] = (255, 0, 255)
Image.fromarray(big[90:170, 340:420]).resize((640, 640), Image.NEAREST).save(os.path.join(WORK, "fig2a_overlay_m1_topleft.png"))
Image.fromarray(big[2075:2150, 2350:2425]).resize((600, 600), Image.NEAREST).save(os.path.join(WORK, "fig2a_overlay_m4_bottomright.png"))

pmean = np.mean(periods)
L4, R4, T4, B4 = PANELS[4]
sub4 = redmask[int(T4):int(B4), int(L4):int(R4)]
rr_ = np.where(sub4.sum(1) > 0.8 * sub4.shape[1])[0] + int(T4)
cc_ = np.where(sub4.sum(0) > 0.8 * sub4.shape[0])[0] + int(L4)
def groups(v):
    return [list(q) for q in np.split(v, np.where(np.diff(v) > 1)[0] + 1)]
red_rows = [float(round((np.mean(q) - T4) / ((B4 - T4) / N) - 0.5, 2)) for q in groups(rr_)]
red_cols = [float(round((np.mean(q) - L4) / ((R4 - L4) / N) - 0.5, 2)) for q in groups(cc_)]
print("red lines (cell-index units): rows", red_rows, "cols", red_cols)
diag = {m: sum(1 for (mm, i, j, v, d, f) in rows if mm == m and i == j and v == v and v < 60) for m in PANELS}
diag_red = {m: sum(1 for (mm, i, j, v, d, f) in rows if mm == m and i == j and f == "red_line") for m in PANELS}
print("black (<60) diagonal cells per matrix:", diag, "diagonal cells under red lines:", diag_red)
write_csv(os.path.join(HERE, "fig2a.csv"), [
    "Templier 2019 eLife 8:e45696, Figure 2a: pairwise similarity matrices of the 'Section-order retrieval for Dataset 2'.",
    "  Matrix 1 = EM imagery before reordering, 2 = EM imagery after reordering, 3 = fluorescent beads imagery",
    "  before reordering, 4 = beads after reordering (caption: panels 1 and 2 EM, 3 and 4 beads; before/after).",
    "Columns: matrix = printed panel number 1-4; row = cell index from the top (y axis, ticks 0-200);",
    "  col = cell index from the left (x axis, ticks 0-200); grey = grey level of the cell as printed (0 black - 255 white);",
    "  darkness = 1 - grey/255 (caption: 'Darker pixels depict higher similarity whereas white pixels depict no",
    "  similarity'; the figure has no colour bar, so this is NOT a calibrated similarity value, only a monotonic proxy);",
    "  flag = 'red_line' where one of the red lines drawn in matrix 4 covers the cell (grey left empty);",
    "  'partly_hidden' where the frame line covers most of the cell (first/last row/column; sampled on <3 px);",
    "  'panel_label' where the strokes of the printed panel number (1-4, upper right of each matrix, about rows 3-25 and",
    "  columns 183-198) cover the cell (grey left empty; the matrix value there is not visible).",
    "Provenance: tier 3, digitized from the embedded JPEG (9615 x 2297 px, ~1313 ppi) by fig2a_extract.py. No vector data.",
    f"  Grid: 204 x 204 cells per matrix, {pmean:.4f} px per cell, from the frame lines (checked against a period/phase",
    "  fit of the cell edges inside each matrix, which agrees within 0.01 px per cell and 0.3 px in phase);",
    "  ticks 0, 50, 100, 150, 200 sit on the centres of cells 0, 50, 100, 150, 200 (within ~1.6 px).",
    "  The figure grid has 204 cells per side although the text gives 203 sections",
    f"  for Dataset 2; the count was checked on the cell edges and on the diagonal (black diagonal cells, grey < 60: {diag};",
    f"  in matrix 4, {diag_red[4]} diagonal cells are under the red lines).",
    "  Cells 0 and 203 are partly hidden under the frame lines and were sampled on their visible part.",
    "Uncertainty: grey level about +-5 (JPEG compression; median |rebuilt - source| is printed by the script).",
    f"  The red lines in matrix 4 lie over rows {red_rows} and columns {red_cols} (all 204 cells of each; centre of each line",
    "  in cell-index units within 0.1 of these integers).",
], ["matrix", "row", "col", "grey", "darkness", "flag"],
    [(str(m), str(i), str(j), v, d, f) for m, i, j, v, d, f in rows], fmt="{:.4g}")
print("fig2a.csv", len(rows), "rows; px per cell", periods)
