"""Digitize Figure 5i of Nguyen et al. 2016 (Sci Rep 6:23721, PDF p.7): highest electron dose, Cont vs Carbon.

Source: the embedded JPEG of Figure 5 (1210 x 1229 px, about 220 ppi); panel i at its lower right.
Raster only (vector_dump.py finds no paths in the figure area): tier 3. Method in pairs_common.py.
    python3 -I fig5i_extract.py   -> fig5i.csv (+ ../work/fig5i_overlay.png for checking)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../tools"))   # tools/digitize_common.py
sys.path.insert(0, HERE)                                # pairs_common.py
import numpy as np  # noqa: E402
from digitize_common import embedded_image, gray, tick_positions, tick_positions_v, fit_axis, write_csv, overlay  # noqa: E402
from pairs_common import column_profile, run_edges, fit_line  # noqa: E402

PDF = os.path.join(HERE, "../source/srep23721.pdf")
a = embedded_image(PDF, 7)
dark = gray(a) < 110

YAXIS, XAXIS = (928, 932), (1144, 1148)
yt = tick_positions_v(dark, YAXIS, -1, 5, 800, 1160)
xt = tick_positions(dark, XAXIS, 1, 5, YAXIS[1] + 1, 1205)
assert len(yt) == 5 and len(xt) == 2, (yt, xt)
fy, res_y, sy = fit_axis(yt, [80, 60, 40, 20, 0])
XC_TICK, XB_TICK = xt


pc = column_profile(a, int(round(XC_TICK)))
pb = column_profile(a, int(round(XB_TICK)))


def centre(p, r0, r1):
    t, b = run_edges(p, r0, r1, p[r0:r1].max() / 2)
    return (t + b) / 2, (b - t) / 2


# every marker run in this panel is a single disc (two coinciding markers make one darker disc)
C = {k: centre(pc, *rr) for k, rr in {"c41": (982, 1001), "c36": (1001, 1021), "c25": (1041, 1060),
                                      "c16": (1075, 1092), "c12": (1091, 1108)}.items()}
B = {k: centre(pb, *rr) for k, rr in {"b69": (874, 894), "b59": (914, 933), "b51": (942, 962),
                                      "b27": (1033, 1053), "b18": (1069, 1089)}.items()}
R = float(np.mean([r for _, r in list(C.values()) + list(B.values())]))
# markers sit on the category ticks (the half-ink run along a row is widened by the attached lines here)
XC, XB = XC_TICK, XB_TICK

# pairs: (colour, Cont marker, Carbon marker), assigned by following each connecting line (checked below)
pairs = [("purple", "c41", "b51"), ("green", "c36", "b69"), ("blue", "c25", "b59"),
         ("purple", "c16", "b51"), ("green", "c16", "b27"), ("purple", "c12", "b18")]
rows, pts = [], []
for k, (col, kc, kb) in enumerate(pairs):
    yc, yb = C[kc][0], B[kb][0]
    y0f, y1f, rms, ncol = fit_line(a, col, XC, yc, XB, yb, R)
    # the connecting line of this colour must start and end near the two markers (within 5 px: the lines are
    # offset from the marker centres by up to ~4 px on steep segments; the nearest other marker is >= 14 px away)
    assert abs(y0f - yc) < 5 and abs(y1f - yb) < 5, (col, kc, kb, y0f, y1f)
    rows.append((str(k + 1), col, "Cont", float(fy(yc)), "run (single disc)" if kc != "c16" else
                 "run (purple and green markers coincide: one darker grey-green disc)"))
    rows.append((str(k + 1), col, "Carbon", float(fy(yb)), "run (single disc)" if kb != "b51" else
                 "run (two purple markers coincide: one darker purple disc)"))
    pts += [(XC + dx, yc + dy) for dx, dy in ((0, 0), (-1, 0), (1, 0), (0, -1), (0, 1))]
    pts += [(XB + dx, yb + dy) for dx, dy in ((0, 0), (-1, 0), (1, 0), (0, -1), (0, 1))]
    print(k + 1, col, round(yc, 2), "->", round(yb, 2), "line fit", round(y0f, 2), round(y1f, 2), "rms", round(rms, 2))
overlay(a, pts, os.path.join(HERE, "../work/fig5i_overlay.png"))

write_csv(os.path.join(HERE, "fig5i.csv"), [
    "Nguyen et al. 2016 Sci Rep 6:23721, Figure 5i: the highest electron doses in the successful serial imaging,",
    "  each set of tissues embedded in Control resin ('Cont') and in conductive resin ('Carbon'), joined by a line.",
    "  Axis title as printed: 'Electron dose (e-/nm2)' (y, linear, ticks 0-80 every 20); x = the two categories.",
    "  Colours per the caption: blue = kidney fixed with transcardial perfusion, purple = brain (transcardial",
    "  perfusion), green = kidney fixed with resection and immersion. The panel shows 3 purple, 1 blue and 2 green",
    "  pairs (6 pairs; caption: N = 6). '*' over the bracket: p < 0.05, Wilcoxon matched-pairs signed rank test.",
    "Columns: pair (my numbering, 1-6, ordered by the Cont value read top to bottom); colour; group (Cont/Carbon);",
    "  electron_dose_e_per_nm2; method (how the marker centre was located; see pairs_common.py).",
    "Provenance: tier 3, digitized from the embedded ~220 ppi JPEG of Figure 5 by fig5i_extract.py. y calibrated on",
    f"  the 5 labelled ticks (max residual {res_y:.2f} e-/nm2). Pairs assigned by following each connecting line.",
    "  Two places hold two coinciding markers (one darker disc each): Cont ~16 (purple + green) and Carbon ~51",
    "  (two purple); both markers get the same value there.",
    f"Uncertainty: about +-{abs(sy) * 0.7:.2f} e-/nm2 (0.7 px of the source image) for each marker centre.",
], ["pair", "colour", "group", "electron_dose_e_per_nm2", "method"], rows, fmt="{:.2f}")
print("y ticks", yt, "res", res_y, "x cat", XC, XB, "R", R)
