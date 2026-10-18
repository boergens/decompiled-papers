"""Redraw Figure 4a (four colour-coded scatter plots + inset) from fig4a.csv and fig4a_inset.csv.
Run from inside figures/:  python3 fig4a.py  ->  fig4a_replot.png
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap

pts = pd.read_csv("fig4a.csv", comment="#")
ins = pd.read_csv("fig4a_inset.csv", comment="#")

# colour map of the original: linear blue (-3) -> white (1.5) -> red (6)
cmap = LinearSegmentedColormap.from_list("bwr_lin", [(0, 0, 1), (1, 1, 1), (1, 0, 0)])
VMIN, VMAX = -3, 6
ORANGE, PURPLE = "#fcae34", "#543379"

# layout copied from the original panel (positions as fractions of the panel box, 245 x 163 pt)
fig = plt.figure(figsize=(3.6, 2.4), dpi=200)
W, H = 245.0, 163.0
def box(x0, x1, ytop, ybot):   # PDF-point coordinates relative to the panel box (origin top-left)
    return [(x0 - 5) / W, (177 - ybot) / H, (x1 - x0) / W, (ybot - ytop) / H]

positions = {
    ("conscious", "state1"): box(50.66, 111.91, 25.42, 86.68),
    ("suppressed", "state1"): box(176.76, 237.76, 25.42, 86.68),
    ("conscious", "state2"): box(50.66, 111.91, 98.24, 159.5),
    ("suppressed", "state2"): box(176.76, 237.76, 98.24, 159.5),
}
sc = None
for (face, state), pos in positions.items():
    ax = fig.add_axes(pos)
    d = pts[(pts.face == face) & (pts.state == state)].sort_values("draw_order")
    sc = ax.scatter(d.projection_preferred_axis_au, d.projection_orthogonal_axis_au, c=d.response_zscored,
                    cmap=cmap, vmin=VMIN, vmax=VMAX, s=5, linewidths=0, rasterized=False)
    ax.set_xlim(-1, 1); ax.set_ylim(-1, 1)
    ax.set_xticks([-1, 1]); ax.set_yticks([-1, 1])
    ax.tick_params(labelsize=6, length=2, pad=1)
    ax.spines[["top", "right"]].set_visible(False)
    if state == "state1":
        ax.set_title(face.capitalize(), fontsize=6, pad=2)
        ax.set_xticklabels([])
    if face == "suppressed":
        ax.set_yticklabels([])
    if face == "conscious":
        fig.text((16 - 5) / W, pos[1] + pos[3] / 2, "State 1" if state == "state1" else "State 2", fontsize=6,
                 ha="center", va="center")

fig.text((121.5 - 5) / W, (177 - 174) / H + 0.01, "Projection onto preferred axis (a.u.)", fontsize=6, ha="center", va="bottom")
fig.text((37 - 5) / W, (177 - 97) / H, "Projection onto orthogonal axis (a.u.)", fontsize=6, ha="center", va="center", rotation=90)

# colour bar (an image strip in the original, labelled 6 at the top and -3 at the bottom)
cax = fig.add_axes(box(119.8, 124.5, 25.63, 57.99))
cb = fig.colorbar(sc, cax=cax, ticks=[-3, 6])
cb.outline.set_visible(False)
cax.tick_params(labelsize=6, length=0, pad=1)
cax.set_ylabel("Response\n(z-scored)", fontsize=6, rotation=90, labelpad=2)
cax.yaxis.set_label_position("right")

# inset: binned response vs projection onto the preferred axis, with error bars
iax = fig.add_axes(box(131.34, 166.33, 80.13, 121.13))
for name, col in [("state1_conscious", ORANGE), ("state2_suppressed", PURPLE)]:
    d = ins[ins.series == name].sort_values("bin_index")
    iax.errorbar(d.projection_preferred_axis_au, d.response,
                 yerr=[d.response - d.errorbar_lo, d.errorbar_hi - d.response],
                 color=col, lw=1, marker="o", ms=2, capsize=3, capthick=0.5, elinewidth=0.5)
iax.set_xlim(-1, 1); iax.set_ylim(0, 9)
iax.set_xticks([-1, 1]); iax.set_yticks([0, 9])
iax.tick_params(labelsize=6, length=1.5, pad=1)
iax.spines[["top", "right"]].set_visible(False)
iax.set_ylabel("Response", fontsize=6, labelpad=1)

fig.savefig("fig4a_replot.png", dpi=200)
print("wrote fig4a_replot.png")
