"""Digitize Figure 5E of Horstmann et al. 2012 (PLoS ONE 7: e35172), PDF p. 6: histogram of the
distances between the presynaptic membrane and the synaptic vesicle membranes ("No. SVs" vs
"Distance SV to AZ [nm]").

Source: the embedded 200 ppi JPEG of Figure 5 (1008 x 1217 px, xref 28); panel E is in its lower
right corner. The PDF holds no vector paths on this page, so this is tier 3 (digitized).

    python3 -I -B fig5e_extract.py   -> fig5e.csv (+ ../work/fig5e_overlay.png for checking)

Method: the y axis line (columns 586-589) and the x axis line (rows 1130-1133) are found as long
dark lines; the y ticks (0, 5, 10) and the x ticks (0, 40, ..., 320) are the short dark marks on
the outside of these lines (tick_positions / tick_positions_v). The bars are open black rectangles
spaced 20 nm apart, centred on multiples of 20 nm. For each bar position the two side lines are
looked for in a pixel row just above the x axis; where both are found, the top edge is the dark
run in the bar's centre column, and its centre row is converted to counts.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))   # tools/digitize_common.py (copied from the osmium tools)
import numpy as np  # noqa: E402
from digitize_common import (embedded_image, gray, tick_positions, tick_positions_v, fit_axis,  # noqa: E402
                             write_csv, overlay)

PDF = HERE.parent / "source" / "horstmann2012_s3em.pdf"
a = embedded_image(str(PDF), 6)
d = gray(a) < 110

YAX = (586, 589)     # y axis line (columns)
XAX = (1130, 1133)   # x axis line (rows)
yt = tick_positions_v(d, YAX, -1, 6, 880, 1140)
xt = tick_positions(d, XAX, +1, 6, 560, 1000)
assert len(yt) == 3 and len(xt) == 9, (yt, xt)
fy, yres, yslope = fit_axis(yt, [10, 5, 0])
fx, xres, xslope = fit_axis(xt, list(range(0, 321, 40)))

ROW = XAX[0] - 10             # a row just above the x axis, crossing every bar's side lines
rows, pts = [], []
for k in range(0, 18):
    centre_nm = 20 * k
    c = float((centre_nm - fx(0.0)) / xslope)   # inverse of the linear x fit (extrapolates past 320 nm)
    ci = int(round(c))
    lo, hi = ci - 13, ci + 14
    seg = np.where(d[ROW, lo:hi])[0] + lo
    left = seg[seg < ci - 3]
    right = seg[seg > ci + 3]
    if k == 0:
        left = seg[(seg > YAX[1] + 1) & (seg < ci - 3)] if len(seg) else seg
    if len(right) == 0 or (len(left) == 0 and k > 0):
        # no bar drawn: count 0 (the bar outline would sit on the x axis line)
        rows.append((centre_nm, 0.0, 0, "no bar drawn"))
        continue
    col = d[880:XAX[0] - 1, ci]
    r = np.where(col)[0]
    runs = np.split(r, np.where(np.diff(r) > 1)[0] + 1)
    top = runs[0] + 880                 # first dark run from the top = the bar's top edge
    yc = float(top.mean())
    v = float(fy(yc))
    left_edge = float(left.min()) if len(left) else float("nan")
    right_edge = float(right.max())
    pts += [(ci, yc), (left_edge, ROW), (right_edge, ROW)]
    for x in np.arange(left_edge, right_edge + 1):
        pts.append((x, yc))
    rows.append((centre_nm, v, int(round(v)), ""))

overlay(a, pts, str(HERE.parent / "work" / "fig5e_overlay.png"))

total = sum(r[2] for r in rows)
write_csv(str(HERE / "fig5e.csv"), [
    "Horstmann et al. 2012 PLoS ONE 7: e35172, Figure 5E: histogram of the distribution of distances between",
    "  the presynaptic membrane and the synaptic vesicle membranes, for the release site shown in Fig. 5D.",
    "Columns: bin_centre_nm = centre of the bar on the x axis 'Distance SV to AZ [nm]' (bars are 20 nm apart and",
    "  centred on multiples of 20 nm; neither the figure nor the caption gives the bin edges or bin width);",
    "  count_digitized = height of the bar's top edge in units of the y axis 'No. SVs'; count = count_digitized",
    "  rounded to the nearest integer (counts of vesicles are integers); note = 'no bar drawn' for empty bins.",
    "Provenance: tier 3, digitized from the embedded 200 ppi JPEG of Figure 5 (no vector paths in the PDF) by",
    f"  fig5e_extract.py. y calibrated on the 3 labelled ticks 0, 5, 10 (max residual {yres:.3f} counts,",
    f"  {abs(1 / yslope):.2f} px per count); x calibrated on the 9 labelled ticks 0-320 nm (max residual {xres:.2f} nm).",
    f"Uncertainty: about +-{abs(yslope):.3f} counts (1 px) on count_digitized, +-1 nm on bin positions.",
    f"Sum of counts = {total} (the text on p. 5 gives n = 82 synaptic vesicles for this release site).",
], ["bin_centre_nm", "count_digitized", "count", "note"], rows, fmt=["{:.0f}", "{:.3f}", "{}", "{}"])
print("wrote fig5e.csv:", [(r[0], round(r[1], 2)) for r in rows], "sum", total, "res", yres, xres)
