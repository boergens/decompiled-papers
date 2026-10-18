"""Digitize Figure 7 of Gabričević, Lente & Fábián 2020 (poc.4045.pdf p. 6): k_obs of the slow process vs pH, log y axis.

Source: the embedded raster image of Figure 7 (1003 x 717 px). Three marker series with fit curves in the series colour.
    python3 -I fig7_extract.py   -> fig7.csv (+ ../work/fig7_overlay.png)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np  # noqa: E402
from gab_common import (load, gray, tick_positions, tick_positions_v, fit_axis, scatter, colour_mask, track,  # noqa: E402
                        write_csv, cross_overlay, overlay, WORK)

a = load("fig7")
dark = gray(a) < 120
BOT, LEFT = (597, 598), (158, 159)
xt = tick_positions(dark, BOT, 1, 10, 161, 995)          # major ticks 11.5 ... 13.0
assert len(xt) == 4, xt
fx, rx, sx = fit_axis(xt, [11.5, 12.0, 12.5, 13.0])
xminor = tick_positions(dark, BOT, 1, 5, 161, 995)       # all ticks, every 0.1 pH
yall = tick_positions_v(dark, LEFT, -1, 5, 7, 596)        # major + minor ticks of the log axis
ymaj = tick_positions_v(dark, LEFT, -1, 10, 7, 596)       # the two labelled decades
assert len(ymaj) == 2, ymaj
# log axis: labelled ticks 1x10^-3 and 1x10^-4; the minor ticks are 2..9 x 10^-4 and 3..9 x 10^-5
yvals = [1e-3] + [k * 1e-4 for k in range(9, 1, -1)] + [1e-4] + [k * 1e-5 for k in range(9, 2, -1)]
assert len(yall) == len(yvals), (yall, len(yvals))
fy, ry, sy = fit_axis(ymaj, [1e-3, 1e-4], log=True)
_, ry_all, _ = fit_axis(yall, yvals, log=True)
yres = np.max(np.abs(np.log10(fy(np.array(yall))) - np.log10(yvals)))
_, rx_all, _ = fit_axis(xminor, [11.5 + 0.1 * i for i in range(len(xminor))])

LEGEND = (440, 300, 760, 480)
# marker colour, opening size, and the (darker, thinner) colour of the fit curve as it appears in the JPEG
series = [("trans-DCE", (255, 0, 0), 9, (200, 40, 40)), ("cis-DCE", (0, 0, 255), 5, (20, 10, 185)),
          ("TCE", (0, 128, 0), 9, (30, 95, 30))]
box = (161, 7, 995, 595)
PAR = {"TCE": (2.3e-5, 6.4e-5, 12.4), "cis-DCE": (1.5e-4, 3.4e-4, 11.9), "trans-DCE": (2.5e-4, 1.44e-3, 11.9)}
rows, pts, lpts, checks = [], [], [], []
for name, ref, op, lref in series:
    found = scatter(a, [(name, ref)], box, exclude=[LEGEND], open_=op, min_area=30)
    rows += [(n, "marker", float(fx(x)), float(fy(y)), w, h, f) for n, x, y, w, h, f in found]
    pts += [(x, y) for n, x, y, w, h, f in found]
    m = colour_mask(a, lref, alpha_min=0.45, alpha_max=1.6, tol=70) | colour_mask(a, ref, alpha_min=0.45, alpha_max=1.4, tol=55)
    keep = np.zeros_like(m)
    keep[box[1]:box[3], box[0]:box[2]] = True
    keep[LEGEND[1]:LEGEND[3], LEGEND[0]:LEGEND[2]] = False
    m &= keep
    # seed on the line midway between the first two markers
    xs_m = sorted((x, y) for n, x, y, w, h, f in found)
    c0 = int((xs_m[0][0] + xs_m[1][0]) / 2)
    yy = np.where(m[:, c0])[0]
    seed = int(np.median(yy))
    tr = track(m, c0, seed, box[0], box[2], box[1], box[3], max_jump=3, max_gap=35, max_run=7)
    for c, (t, b) in tr.items():
        rows.append((name, "line", float(fx(c)), float(fy((t + b) / 2)), "", "", ""))
        lpts.append((c, (t + b) / 2))
    # compare with Equation (1) and the paper's parameters (p. 6), [H+] = 10^-pH
    ka, kb, pK = PAR[name]
    X = fx(np.array(sorted(tr)))
    Y = fy(np.array([(tr[c][0] + tr[c][1]) / 2 for c in sorted(tr)]))
    H = 10.0 ** -X
    model = (H * ka + 10 ** -pK * kb) / (H + 10 ** -pK)
    dev = np.log10(Y / model)
    checks.append(f"{name} line from pH {X.min():.3f} to {X.max():.3f}, vs Equation (1) with the paper's parameters"
                  f" (k_acid {ka:g}, k_base {kb:g}, pK {pK}): mean {100 * (10 ** dev.mean() - 1):+.1f} %, max abs"
                  f" {100 * (10 ** np.abs(dev).max() - 1):.1f} %")
rows.sort(key=lambda r: (r[1] != "marker", r[0], r[2]))
cross_overlay(a, pts, os.path.join(WORK, "fig7_overlay.png"))
from PIL import Image  # noqa: E402
overlay(np.array(Image.open(os.path.join(WORK, "fig7_overlay.png"))), lpts[::3], os.path.join(WORK, "fig7_overlay.png"),
        colour=(0, 255, 255))
write_csv(os.path.join(HERE, "fig7.csv"), [
    "Gabričević, Lente & Fábián 2020, J Phys Org Chem 33:e4045, Figure 7: dependence of the pseudo-first order rate",
    "  constant of the slow process on the pH. Logarithmic y axis. Markers + fit curves (Equation (1)) in the series colours.",
    "Columns: series (legend names); kind = marker or line (one row per pixel column of the fit curve); pH;",
    "  kobs_s-1 = k_obs (s-1); marker_w_px/marker_h_px = marker blob size in the source image; note.",
    "Provenance: tier 3, digitized from the embedded raster image (1003 x 717 px; no vector data in the PDF) by",
    f"  fig7_extract.py. x calibrated on the 4 labelled ticks (11.5-13.0), max residual {rx:.2g} (all {len(xminor)} ticks at",
    f"  0.1 steps: {rx_all:.2g}); y (log10) on the two labelled ticks 1x10^-3 and 1x10^-4; the 15 unlabelled minor ticks",
    f"  (2-9x10^-4, 3-9x10^-5) then lie within {yres:.3f} decades of their log positions, which confirms the log scale.",
    "  Markers: bounding-box centre of the colour blob after removing the thin fit curve (morphological opening).",
    f"Uncertainty: about +-{2 * abs(sx):.3f} pH units in x and +-{2 * abs(sy) * np.log(10) * 100:.1f} % in k_obs (2 px).",
    "Check of the traced curves: " + "; ".join(checks[:1]) + ";",
    "  " + "; ".join(checks[1:2]) + ";",
    "  " + "; ".join(checks[2:]) + ".",
], ["series", "kind", "pH", "kobs_s-1", "marker_w_px", "marker_h_px", "note"], rows, fmt="{:.5g}")
print("fig7", rx, rx_all, yres, checks)
for r in rows:
    if r[1] == "marker":
        print("  ", r)
