"""Re-plot Supplementary Fig. 9c (both panels) from sfig9c.csv -> sfig9c_replot.png.

Solid series: the traced x (mean of the run) per depth, drawn as a thin line of points;
dashed series: one marker per dash centroid. Rows in the BSE axis break are left out.
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sfig_common import read_csv  # noqa: E402

COL = {"1": "#e02020", "1.5": "#e02020", "2": "#2050e0", "2.5": "#2050e0", "3": "#f0a020", "3.5": "#f0a020",
       "4": "#7030c0", "4.5": "#7030c0", "5": "#e030b0", "5.5": "#e030b0", "6": "k"}
rows = read_csv(os.path.join(HERE, "sfig9c.csv"))
fig, axes = plt.subplots(1, 2, figsize=(6.4, 2.8))
for ax, pname, xlim, xt, ylim, yt in (
        (axes[0], "Backscattered electrons", (0, 255), [0, 50, 100, 150, 200], (-530, 0), range(-500, 1, 100)),
        (axes[1], "Primary (absorbed) electrons", (0, 3150), [0, 1000, 2000, 3000], (-1420, 0), range(-1400, 1, 200))):
    for kev in COL:
        name = f"{kev} keV"
        r = [q for q in rows if q["panel"] == pname and q["series"] == name and "break" not in q["flag"]]
        if not r:
            continue
        xs = [float(q["x"]) for q in r]
        ys = [float(q["depth_nm"]) for q in r]
        if r[0]["style"] == "solid":
            ax.plot(xs, ys, ".", ms=1.5, color=COL[kev], label=name)
        else:
            ax.plot(xs, ys, "s", ms=2, mfc="none", color=COL[kev], label=name)
    if pname.startswith("Back"):
        ax.axhline(-50, color="0.6", lw=0.8)
        ax.text(250, -60, "50 nm", ha="right", va="top", fontsize=7, color="0.5")
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xticks(xt)
    ax.set_yticks(list(yt))
    ax.xaxis.tick_top()
    ax.set_title(pname, fontsize=8)
    ax.set_ylabel("depth (nm)")
    ax.tick_params(labelsize=7)
axes[1].legend(fontsize=6, frameon=False, bbox_to_anchor=(1.02, 1), loc="upper left", markerscale=2)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "sfig9c_replot.png"), dpi=150)
