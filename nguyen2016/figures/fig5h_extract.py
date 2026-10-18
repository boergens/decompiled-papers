"""Digitize Figure 5h of Nguyen et al. 2016 (Sci Rep 6:23721, PDF p.7): smallest possible voxel size, Cont vs Carbon.

Source: the embedded JPEG of Figure 5 (1210 x 1229 px, about 220 ppi); panel h at its right, middle.
Raster only (vector_dump.py finds no paths in the figure area): tier 3. Method in pairs_common.py.
    python3 -I fig5h_extract.py   -> fig5h.csv (+ ../work/fig5h_overlay.png for checking)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../tools"))   # tools/digitize_common.py
sys.path.insert(0, HERE)                                # pairs_common.py
import numpy as np  # noqa: E402
from digitize_common import embedded_image, gray, tick_positions, tick_positions_v, fit_axis, write_csv, overlay  # noqa: E402
from pairs_common import column_profile, run_edges, fit_line, ink  # noqa: E402

PDF = os.path.join(HERE, "../source/srep23721.pdf")
a = embedded_image(PDF, 7)
dark = gray(a) < 110

YAXIS, XAXIS = (927, 930), (739, 743)          # axis lines (columns / rows), long dark lines in the panel
yt = tick_positions_v(dark, YAXIS, -1, 5, 380, 760)   # ticks point left
xt = tick_positions(dark, XAXIS, 1, 5, YAXIS[1] + 1, 1205)   # category ticks below the axis
assert len(yt) == 4 and len(xt) == 2, (yt, xt)
fy, res_y, sy = fit_axis(yt, [9000, 6000, 3000, 0])
XC_TICK, XB_TICK = xt


def xcentre(row, c0, c1):
    v = np.linalg.norm(ink(a[row - 1:row + 2, c0:c1]).mean(0), axis=1)
    idx = np.where(v >= v.max() / 2)[0]
    return c0 + (idx[0] + idx[-1]) / 2


pc_cont = column_profile(a, int(round(XC_TICK)))
pc_carb = column_profile(a, int(round(XB_TICK)))


def edges(p, r0, r1):
    return run_edges(p, r0, r1, p[r0:r1].max() / 2)


# isolated markers: centre = middle of the run; radius from them
iso = {"c8500": edges(pc_cont, 438, 458), "c3700": edges(pc_cont, 604, 624), "c2300": edges(pc_cont, 651, 671),
       "b3000": edges(pc_carb, 627, 646)}
R = float(np.mean([(b - t) / 2 for t, b in iso.values()]))
# horizontal centres of isolated markers -> the category x positions actually used by the markers
XC = float(np.mean([xcentre(448, 995, 1035), xcentre(614, 995, 1035), xcentre(661, 995, 1035)]))
XB = xcentre(637, 1085, 1125)

clusterC1 = edges(pc_cont, 630, 652)     # purple over green, overlapping (Cont, ~2900-3000)
clusterC2 = edges(pc_cont, 683, 711)     # blue over purple (Cont, ~1100-1500)
clusterB = edges(pc_carb, 684, 727)      # six Carbon markers overlapping (~600-1500)

cont = [  # (colour, Cont centre row, method)
    ("purple", np.mean(iso["c8500"]), "run (isolated)"),
    ("blue", np.mean(iso["c3700"]), "run (isolated)"),
    ("purple", clusterC1[0] + R, "top edge + radius (lower part covered by the green marker)"),
    ("green", clusterC1[1] - R, "bottom edge - radius (upper part covered by the purple marker)"),
    ("green", np.mean(iso["c2300"]), "run (isolated)"),
    ("blue", clusterC2[0] + R, "top edge + radius (lower part covered by the purple marker)"),
    ("purple", clusterC2[1] - R, "bottom edge - radius (upper part covered by the blue marker)"),
]
carb_guess = [640, 703, 713, 708, 695, 717, 716]   # rough end rows of the connecting lines, read off the image
rows, pts, lines = [], [], []
for k, ((col, yc, how), yg) in enumerate(zip(cont, carb_guess)):
    y0_fit, y1_fit, rms, ncol = fit_line(a, col, XC, yc, XB, yg, R)
    if k == 0:
        yb, howb = np.mean(iso["b3000"]), "run (isolated)"
    elif col == "green" and abs(y1_fit - (clusterB[0] + R)) < 3:
        yb, howb = clusterB[0] + R, "top edge of the Carbon cluster + radius (the green marker on top of the cluster)"
    elif abs(y1_fit - (clusterB[1] - R)) < 3:
        yb, howb = clusterB[1] - R, "bottom edge of the Carbon cluster - radius (blue and purple markers nearly coincide there)"
    else:
        yb, howb = y1_fit, "end of the least-squares connecting line (marker hidden inside the Carbon cluster)"
    pair = f"{k + 1}"
    rows.append((pair, col, float(fy(yc)), float(fy(yb)), how, howb, float(fy(y1_fit))))
    pts += [(XC + dx, yc + dy) for dx, dy in ((0, 0), (-1, 0), (1, 0), (0, -1), (0, 1))]
    pts += [(XB + dx, yb + dy) for dx, dy in ((0, 0), (-1, 0), (1, 0), (0, -1), (0, 1))]
    print(pair, col, round(yc, 2), "->", round(yb, 2), "(line end", round(y1_fit, 2), "rms", round(rms, 2), ncol, "cols)")
overlay(a, pts, os.path.join(HERE, "../work/fig5h_overlay.png"))

out = []
for pair, col, vc, vb, how, howb, vline in rows:
    out.append((pair, col, "Cont", vc, how))
    out.append((pair, col, "Carbon", vb, howb))
write_csv(os.path.join(HERE, "fig5h.csv"), [
    "Nguyen et al. 2016 Sci Rep 6:23721, Figure 5h: the smallest possible voxel sizes in the successful serial imaging,",
    "  each set of tissues embedded in Control resin ('Cont') and in conductive resin ('Carbon'), joined by a line.",
    "  Axis title as printed: 'Voxel size (nm3)' (y, linear, ticks 0, 3000, 6000, 9000); x = the two categories.",
    "  Colours per the caption: blue = kidney fixed with transcardial perfusion, purple = brain (transcardial",
    "  perfusion), green = kidney fixed with resection and immersion. The panel shows 3 purple, 2 blue and 2 green",
    "  pairs (7 pairs; caption: N = 7). '*' over the bracket: p < 0.05, Wilcoxon matched-pairs signed rank test.",
    "Columns: pair (my numbering, 1-7, ordered by the Cont value read top to bottom); colour; group (Cont/Carbon);",
    "  voxel_size_nm3; method (how the marker centre was located; see pairs_common.py).",
    "Provenance: tier 3, digitized from the embedded ~220 ppi JPEG of Figure 5 by fig5h_extract.py. y calibrated on",
    f"  the 4 labelled ticks (max residual {res_y:.1f} nm3). Pairs assigned by following each connecting line.",
    f"Uncertainty: isolated markers about +-{abs(sy) * 0.7:.0f} nm3 (0.7 px); markers with an edge covered by",
    f"  another marker about +-{abs(sy) * 1.5:.0f} nm3; markers inside the Carbon cluster (600-1500 nm3) about",
    f"  +-{abs(sy) * 3:.0f} nm3 (3 px), because the connecting lines do not end exactly in the marker centres",
    "  (checked on isolated markers: up to ~2-5 px off for steep lines, <= ~2 px for shallow ones).",
    "Cross-check (decompiler's calculation, not printed in the paper): Table 1 lists 7 Normal/Conductive pairs for",
    "  Fig. 5h; (X-Y resolution)^2 x Z-step, the voxel-size formula in Methods, gives for them (nm3):",
    "  1299.6/640.0, 3698.0/974.7, 8487.2/2957.5, 1740.5/1440.0, 2371.6/1392.4, 2964.5/921.6, 1152.0/739.6.",
    "  See README for how the digitized pairs compare.",
], ["pair", "colour", "group", "voxel_size_nm3", "method"], out, fmt="{:.0f}")
print("y ticks", yt, "res", res_y, "x cat", XC, XB, "R", R)
