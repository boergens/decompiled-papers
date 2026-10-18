"""Digitize Figure 10 of Sun & Gamstedt 2019 (PDF p. 6): modelled shear stress in the primary shear zone
(tau_PSZ, red solid) and in the bulk (tau_Bulk, black dashed) versus cutting speed, with a vertical line
labelled "Critical v0 = 4.7 mm/s".

Source: the embedded 300 ppi RGB JPEG of Fig. 10 (709 x 539 px); no vector paths in the PDF.
    python3 -I -B figures/fig10_extract.py   -> figures/fig10.csv (+ work/fig10_overlay.png)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import numpy as np  # noqa: E402
from digitize_common import (embedded_image, gray, frame_lines, tick_positions, tick_positions_v,  # noqa: E402
                             fit_axis, write_csv, overlay, trace_envelope)

PDF = str(HERE.parent / "source" / "sun2019.pdf")
a = embedded_image(PDF, 6, bbox_near=(340, 552, 510, 681))
r, g, b = (a[:, :, i].astype(int) for i in range(3))
gr = gray(a)
dark = gr < 120
rows = frame_lines(dark, 1, 0.5)
cols = frame_lines(dark, 0, 0.5)
TOP, BOT = rows[0], rows[-1]
LEFT, RIGHT = cols[0], cols[-1]
xl, xr = (LEFT[0] + LEFT[1]) / 2, (RIGHT[0] + RIGHT[1]) / 2
yb, yt = (BOT[0] + BOT[1]) / 2, (TOP[0] + TOP[1]) / 2

# x: outward ticks below the frame at 1..9 mm/s; left frame 0, right frame 10 (both labelled)
xt = tick_positions(dark, BOT, 1, 3, LEFT[1] + 2, RIGHT[0] - 1)
assert len(xt) == 9, xt
fx, resx, sx = fit_axis(xt + [xl, xr], list(range(1, 10)) + [0, 10])
# y: inward ticks at 135, 132.5, ..., 115 (labels on 115..135 in steps of 5); top frame 140 (labelled)
lt = tick_positions_v(dark, LEFT, 1, 5, TOP[1] + 2, BOT[0] - 1)
assert len(lt) == 9, lt
fy, resy, sy = fit_axis(lt + [yt], [135 - 2.5 * i for i in range(9)] + [140])

# the thin grey vertical "critical" line: the column inside the frame with the most mid-grey pixels
inner = (gr < 200)[TOP[1] + 3:BOT[0] - 3, LEFT[1] + 15:RIGHT[0] - 3]
vc = LEFT[1] + 15 + int(np.argmax(inner.sum(0)))
vline = [vc + d for d in (-1, 0, 1) if (gr[TOP[1] + 3:BOT[0] - 3, vc + d] < 230).mean() > 0.7]
v_crit = float(fx(np.mean(vline)))

x0, x1 = LEFT[1] + 6, RIGHT[0] - 1
y0, y1 = TOP[1] + 2, BOT[0] - 1
out, pts = [], []
# red solid line tau_PSZ
red = (r > 150) & (g < 140) & (b < 140) & (r - g > 60)
env = trace_envelope(red, x0, x1, y0, y1, half_width=1, min_px=1)
for c, ym, yu, yl in env:
    if ym == ym:
        out.append(("tau_PSZ", float(fx(c)), float(fy(ym)), ""))
        pts.append((c, ym))
# black dashed line tau_Bulk: dark grey pixels; skip the vertical line; follow the run nearest the previous one,
# and leave the gaps between dashes empty
blk = (gr < 170) & (a.max(2).astype(int) - a.min(2).astype(int) < 40)
for c in vline:
    blk[:, c - 1:c + 2] = False
# the printed labels (pixel boxes read off the image): "Critical v0 = 4.7 mm/s", tau_Bulk, tau_PSZ
for (ca, cb, ra, rb) in [(235, 565, 250, 305), (485, 575, 10, 88), (485, 575, 118, 165)]:
    blk[ra:rb, ca:cb] = False
blk[:, :LEFT[1] + 12] = False                            # the inward y tick marks (up to 9 px long)
prev, last_c = None, None
for c in range(x0, x1):
    rr = np.where(blk[y0:y1, c])[0] + y0
    if len(rr) == 0:
        continue
    runs = np.split(rr, np.where(np.diff(rr) > 2)[0] + 1)
    if prev is None:
        run = max(runs, key=lambda q: q.mean())          # start at the bottom left (lowest run)
    else:
        run = min(runs, key=lambda q: abs(q.mean() - prev))
        if abs(run.mean() - prev) > 6 + 3 * (c - last_c):    # not the continuation of the line
            continue
    prev, last_c = run.mean(), c
    out.append(("tau_Bulk", float(fx(c)), float(fy(prev)), ""))
    pts.append((c, prev))
out.append(("critical line", v_crit, float("nan"), "x of the vertical line drawn in the panel (label: 4.7 mm/s)"))
overlay(a, pts, str(HERE.parent / "work" / "fig10_overlay.png"), colour=(0, 200, 255))

# crossing of the two traced curves (for the README check; also written as a row)
psz = np.array([(o[1], o[2]) for o in out if o[0] == "tau_PSZ"])
blk_ = np.array([(o[1], o[2]) for o in out if o[0] == "tau_Bulk"])
diff = np.interp(blk_[:, 0], psz[:, 0], psz[:, 1]) - blk_[:, 1]
i = np.where((diff[:-1] > 0) & (diff[1:] <= 0))[0]
cross = [float(blk_[k, 0] + (blk_[k + 1, 0] - blk_[k, 0]) * diff[k] / (diff[k] - diff[k + 1])) for k in i]
print("all crossings", cross); cross = [c for c in cross if 2 < c < 8] or [float("nan")]
out.append(("crossing of traced curves", cross[0], float(np.interp(cross[0], psz[:, 0], psz[:, 1])),
            "computed by fig10_extract.py from the two traces, not printed in the paper"))
write_csv(str(HERE / "fig10.csv"), [
    "Sun & Gamstedt 2019, Nanomanuf Metrol 2:45-55, Fig. 10: shear stresses in the primary shear zone and in the",
    "  bulk material as a function of the cutting speed (model results, from ref. [8]).",
    "Columns: series ('tau_PSZ' = red solid line, label tau_PSZ; 'tau_Bulk' = black dashed line, label tau_Bulk;",
    "  'critical line' = the thin vertical line labelled 'Critical v0 = 4.7 mm/s', x only; 'crossing of traced",
    "  curves' = where the two traces cross, computed here); cutting_speed_mm_s = 'Cutting speed v0, mm/s';",
    "  shear_stress_MPa = 'Shear stress tau, MPa'. One row per pixel column of the source image; the dashed",
    "  line has gaps between its dashes.",
    "Provenance: tier 3, digitized from the embedded 300 ppi JPEG (no vector data in the PDF) by fig10_extract.py:",
    f"  linear fits on the 9 x ticks + frames (residual {resx:.3f} mm/s) and 9 y ticks + top frame (residual",
    f"  {resy:.3f} MPa); red line by colour mask (centre of the line per column), dashed line by a dark-grey mask (printed labels masked out)",
    "  following the run nearest the previous column (labels skipped). The y axis starts at about 113 MPa (no label).",
    f"Uncertainty: about +-{2 * abs(sx):.2f} mm/s and +-{2 * abs(sy):.2f} MPa (2 px; JPEG blur).",
    f"Note: the vertical line is drawn at {v_crit:.2f} mm/s, not at the 4.7 mm/s printed next to it.",
], ["series", "cutting_speed_mm_s", "shear_stress_MPa", "note"], out, fmt=["{}", "{:.4f}", "{:.3f}", "{}"])
print("wrote fig10.csv", len(out), "rows; residuals", resx, resy, "vline", vline, v_crit, "cross", cross)
print("PSZ ends", psz[0], psz[-1], "Bulk ends", blk_[0], blk_[-1])
