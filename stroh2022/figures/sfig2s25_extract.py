"""Digitize Figure 2—figure supplement 2 and 5 of Ströh et al. 2022 (eLife figure-supplement JPEGs, 1800 x 1020 px).

Both are MATLAB pages with the same layout as the source-data PDFs (see sd_extract.py): 12 line plots (top row
intensity vs time at x = 200 ... 1200 μm; middle row intensity vs depth at t = 30 ... 1200 min; blue = data, black =
model in supplement 5; black circles in supplement 2), colour map(s) with colour bar, and two projection images.
The JPEG frame lines are blurred grey (not RGB 38), so the frame mask is "neutral and darker than 170".
Tick labels were read by eye from the images (they are regular: y 0.5, 0.6, ... upward from the lowest tick;
x 500, 1000; maps 0-1200 at the image edges; colour bars as given below).

    python3 -I sfig2s25_extract.py  -> sfig2s2_traces.csv, sfig2s2_map_data.csv, sfig2s5_traces.csv,
                                       sfig2s5_map_data.csv, sfig2s5_map_model.csv (+ ../work/ overlays)
"""
import csv
import os
import sys

import cv2
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "../tools"))
from sdlayout import groups  # noqa: E402
from digitize_common import trace_envelope  # noqa: E402
from main_common import map_grid  # noqa: E402

SUPP = os.path.join(HERE, "../source/elife_figure_supplements")
DEPTHS = [200, 400, 600, 800, 1000, 1200]
TIMES = [30, 60, 120, 360, 600, 1200]
# colour-bar tick labels read by eye (top to bottom)
CBAR = {"fig2-figsupp2.jpg": [[0.85, 0.8, 0.75, 0.7, 0.65, 0.6, 0.55, 0.5, 0.45]],
        "fig2-figsupp5.jpg": [[0.9, 0.8, 0.7, 0.6, 0.5], [0.9, 0.8, 0.7, 0.6, 0.5]]}
TITLE = {"fig2-figsupp2.jpg": "2%Os1.wash, IAC20220409_B20220406", "fig2-figsupp5.jpg": "OsLiver, IAC20211203_L20211201"}


def fmask(a):
    ai = a.astype(int)
    return ((ai.max(2) - ai.min(2)) < 35) & (ai.mean(2) < 170)


def line_boxes(m):
    rows = groups(np.where(m.sum(1) > 300)[0])
    out = []
    for r0, r1 in zip(rows[:-1], rows[1:]):
        if not 180 <= r1 - r0 <= 300:
            continue
        cols = groups(np.where(m[r0:r1 + 1].mean(0) > 0.6)[0])
        i = 0
        while i < len(cols) - 1:
            c0, c1 = cols[i], cols[i + 1]
            if 180 <= c1 - c0 <= 300 and m[r0, c0:c1].mean() > 0.5 and m[r1, c0:c1].mean() > 0.5:
                out.append((r0, r1, c0, c1)); i += 2
            else:
                i += 1
    return out


def ticks(m, b, L=2):
    r0, r1, c0, c1 = b
    ys = groups(np.where(m[r0 + 2:r1 - 1, c0 + 1:c0 + 1 + L].all(1) & m[r0 + 2:r1 - 1, c1 - L:c1].all(1))[0] + r0 + 2)
    xs = groups(np.where(m[r1 - L:r1, c0 + 2:c1 - 1].all(0) & m[r0 + 1:r0 + 1 + L, c0 + 2:c1 - 1].all(0))[0] + c0 + 2)
    return ys, xs


def run(name, stem):
    a = np.array(Image.open(os.path.join(SUPP, name)).convert("RGB"))
    ai = a.astype(int)
    m = fmask(a)
    bx = line_boxes(m)
    assert len(bx) == 12, bx
    rows_ = sorted(set(b[0] for b in bx))
    # JPEG chroma subsampling washes the thin blue line out to about (80, 80, 120): blue = clearly bluish and dark-ish;
    # black = neutral and dark
    blue = (ai[:, :, 2] - ai[:, :, 0] > 25) & (ai.mean(2) < 205)
    blk = (ai[:, :, 2] - ai[:, :, 0] < 15) & ((ai.max(2) - ai.min(2)) < 25) & (ai.mean(2) < 175)
    cal = {}
    for b in bx:
        ys, xs = ticks(m, b)
        cal[b] = (ys, xs)
    # boxes whose ticks are hidden by curves borrow them from a sibling of the same row (same size)
    out_rows, ov = [], a.copy()
    notes = []
    for b in bx:
        r0, r1, c0, c1 = b
        ys, xs = cal[b]
        if len(ys) < 3 or len(xs) < 2:
            s = max((q for q in bx if q[0] == r0 and q != b), key=lambda q: len(cal[q][0]) + len(cal[q][1]))
            ys = cal[s][0]; xs = [x - s[2] + c0 for x in cal[s][1]]
            notes.append(f"{b}: ticks borrowed from {s}")
        step = float(np.min(np.diff(ys)))   # some ticks may be hidden: the smallest gap is one step
        # the 0.5 tick lies 28-32 px above the bottom frame in every plot (it may be hidden by a curve)
        yv = [round(0.5 + round(((r1 - 30) - y) / step) * 0.1, 3) for y in ys]
        my, by = np.polyfit(ys, yv, 1)
        xv = [500, 1000] if len(xs) == 2 else None
        mx, bxx = np.polyfit(xs, xv, 1)
        row = rows_.index(r0)
        col = sorted(q[2] for q in bx if q[0] == r0).index(c0)
        panel = f"x={DEPTHS[col]} μm" if row == 0 else f"t={TIMES[col]} min"
        series = [("data", blue)]
        if np.isfinite(trace_envelope(blk, c0 + 2, c1 - 1, r0 + 2, r1 - 1, 0)[:, 1]).mean() > 0.3:
            series.append(("model", blk))
        circles = []
        if row == 1:
            sub = (blk[r0:r1, c0:c1] * 255).astype(np.uint8)
            cs = cv2.HoughCircles(sub, cv2.HOUGH_GRADIENT, dp=1, minDist=25, param1=50, param2=12, minRadius=6, maxRadius=11)
            if cs is not None:
                for x, y, r in cs[0]:
                    ang = np.linspace(0, 2 * np.pi, 48, endpoint=False)
                    ok = np.mean([sub[min(sub.shape[0] - 1, max(0, int(y + r * np.sin(t)))), min(sub.shape[1] - 1, max(0, int(x + r * np.cos(t))))] > 0
                                  for t in ang])
                    if ok > 0.6:
                        circles.append((x + c0, y + r0, r))
        for name_, mask in series:
            mk = mask.copy()
            yy, xx = np.mgrid[r0:r1, c0:c1]
            for cx, cy, r in circles:
                mk[r0:r1, c0:c1] &= ~(abs(np.hypot(xx - cx, yy - cy) - r) <= 2.5)
            env = trace_envelope(mk, c0 + 2, c1 - 1, r0 + 2, r1 - 1, half_width=0)
            for c, ym, yu, yl in env:
                if ym == ym:
                    out_rows.append([TITLE[name], panel, name_, f"{mx * c + bxx:.5g}", f"{my * ym + by:.5g}",
                                     f"{my * yu + by:.5g}", f"{my * yl + by:.5g}", ""])
                    ov[int(ym), int(c)] = (255, 0, 255) if name_ == "data" else (255, 140, 0)
        for cx, cy, r in circles:
            out_rows.append([TITLE[name], panel, "circle", f"{mx * cx + bxx:.5g}", f"{my * cy + by:.5g}", "", "", f"{abs(mx) * r:.3g}"])
    with open(os.path.join(HERE, f"{stem}_traces.csv"), "w", newline="") as f:
        f.write(f"# Ströh et al. 2022 eLife, Figure 2—figure supplement {stem[-1]}: line plots of the MATLAB page"
                f" '{TITLE[name]}' (title as printed).\n")
        f.write("# Columns: sample = page title; panel = plot title ('x=200 μm': intensity vs time t at that depth;"
                " 't=30 min': intensity vs depth x at that time); series = data (blue) | model (black) | circle (black"
                " circle marker, x/y = centre, r_x = radius in x units); x = time (min) or depth (μm); y = Intensity"
                " (a.u.) at the line centre in that pixel column; y_upper / y_lower = top / bottom of the line there.\n")
        f.write("# Provenance: tier 3, digitized from the eLife figure-supplement JPEG (1800 x 1020 px) by"
                " sfig2s25_extract.py; tick marks found in the image, tick labels read by eye (y: 0.5 at the lowest tick,"
                " +0.1 per tick; x: 500, 1000).\n")
        f.write("# Uncertainty: about ±5.3 min or ±5.3 μm (1 px) and ±0.002-0.005 (a.u.) (1 px) plus JPEG blur (±1 px).\n")
        w = csv.writer(f)
        w.writerow(["sample", "panel", "series", "x", "y", "y_upper", "y_lower", "r_x"])
        w.writerows(out_rows)
    Image.fromarray(ov).save(os.path.join(HERE, f"../work/{stem}_overlay.png"))
    # colour maps (bottom row, left part): find saturated squares
    sat = (ai.max(2) - ai.min(2)) > 40
    cols = np.where(sat[740:980, :1250].mean(0) > 0.5)[0]
    runs_ = []
    for c in cols:
        if runs_ and c - runs_[-1][-1] <= 2:
            runs_[-1].append(c)
        else:
            runs_.append([c])
    blocks = [(r[0], r[-1]) for r in runs_ if r[-1] - r[0] > 10]
    maps = [q for q in blocks if q[1] - q[0] > 150]
    bars = [q for q in blocks if 15 < q[1] - q[0] < 40]
    for k, ((mc0, mc1), (bc0, bc1)) in enumerate(zip(maps, bars)):
        rr = groups(np.where(sat[700:, (mc0 + mc1) // 2])[0] + 700)
        rr = np.where(sat[700:, (mc0 + mc1) // 2])[0] + 700
        mr0, mr1 = int(rr.min()), int(rr.max())
        br = np.where(sat[700:, (bc0 + bc1) // 2])[0] + 700
        br0, br1 = int(br.min()), int(br.max())
        # colour-bar ticks: dark marks just inside the right edge of the bar
        g = ai.mean(2)
        # tick marks: short dark dips in the brightness of the bar's right-most columns (JPEG colour fringes hide
        # their grey colour)
        col = g[:, bc1 - 3:bc1].mean(1)
        tk = groups([r for r in range(br0 + 3, br1 - 2)
                     if col[r] < np.median(col[max(br0, r - 8):r + 9]) - 25])
        vals = CBAR[name][k]
        if len(tk) < len(vals) and np.std(np.diff(tk)) < 2:
            vals = vals[:len(tk)]          # lowest ticks not visible on the dark blue end of the bar; top ones match
        if len(tk) != len(vals):
            raise SystemExit(f"{name} map {k}: colour-bar ticks {tk} vs labels {vals}")
        kind = "data" if k == 0 else "model"
        map_grid(a, (mr0, mr1, mc0, mc1), (br0 + 1, br1 - 1, bc0 + 3, bc1 - 3), list(zip(tk, vals)),
                 os.path.join(HERE, f"{stem}_map_{kind}.csv"), [
            f"Ströh et al. 2022 eLife, Figure 2—figure supplement {stem[-1]}, colour map '{kind}' of '{TITLE[name]}'.",
            "Grid: first column y = Depth x (μm) at the pixel-row centre (top row first); header = Time t (min) at the",
            "  pixel-column centres; cells = Intensity (a.u.) read through the colour bar (nearest bar colour).",
            "Provenance: tier 3, digitized from the eLife figure-supplement JPEG by sfig2s25_extract.py; map edges = axis",
            f"  limits 0 and 1200 (labels at the edges); colour-bar ticks at rows {tk} labelled {vals} (read by eye).",
            "Uncertainty: ±2.7 min / ±2.7 μm (half a pixel); values quantized to the bar's colour steps and JPEG noise.",
        ])
        Image.fromarray(a[mr0 - 30:mr1 + 40, mc0 - 80:bc1 + 80]).save(os.path.join(HERE, f"../work/{stem}_map_{kind}_src.png"))
    print(stem, len(out_rows), "rows;", len(maps), "maps;", notes)


if __name__ == "__main__":
    run("fig2-figsupp2.jpg", "sfig2s2")
    run("fig2-figsupp5.jpg", "sfig2s5")
