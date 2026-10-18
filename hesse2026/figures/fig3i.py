#!/usr/bin/env python3
"""Redraw Figure 3i: single-trial decoding accuracy (%) per session (n = 10, thin lines) and mean (thick lines and
large markers) for decoders using the average activity, state 1 and state 2 (held-out half of neurons);
solid lines / filled markers = conscious face, dashed lines / open markers = suppressed face.
Reads fig3i.csv; writes fig3i_replot.png."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from fig3_common import GREY, ORANGE, PURPLE, read_csv, save

d = read_csv("fig3i.csv")
X = [0, 1, 2]
COLS = [GREY, ORANGE, PURPLE]
def dash(lw):
    """4 pt on / 4 pt off (the original's dash pattern) for a line of width lw (matplotlib scales dashes by lw)."""
    return (0, (4 / lw, 4 / lw))
ycols = ["average_pct", "state1_pct", "state2_pct"]

fig, ax = plt.subplots(figsize=(2.7, 3.0), dpi=200)
for _, r in d.iterrows():
    y = [r[c] for c in ycols]
    con = r["condition"] == "conscious"
    if r["line"].startswith("session_"):
        ax.plot(X, y, color="k", lw=0.3, alpha=0.5, ls="-" if con else dash(0.3), zorder=1)
    elif r["line"] == "mean_line":
        ax.plot(X, y, color="k", lw=1.5, ls="-" if con else dash(1.5), zorder=2)
    elif r["line"] == "mean_marker_filled":
        for xi, yi, c in zip(X, y, COLS):
            ax.plot(xi, yi, "o", color=c, ms=6.5, zorder=3)
    elif r["line"] == "mean_marker_open":
        for xi, yi, c in zip(X, y, COLS):
            ax.plot(xi, yi, "o", markerfacecolor="white", markeredgecolor=c, markeredgewidth=1.3, ms=6.5, zorder=3)

ax.set_xlim(-0.5, 2.5)
ax.set_xticks(X)
ax.set_xticklabels(["Average", "State 1", "State 2"])
ax.set_ylim(0, 100)
ax.set_yticks([0, 20, 40, 60, 80, 100])
ax.set_ylabel("Decoding accuracy (%)")
handles = [Line2D([], [], color="k", lw=1.5, marker="o", ms=6.5, markerfacecolor="k"),
           Line2D([], [], color="k", lw=1.5, ls=dash(1.5), marker="o", ms=6.5, markerfacecolor="white", markeredgewidth=1.3)]
ax.legend(handles, ["Conscious", "Suppressed"], loc="upper left", bbox_to_anchor=(0.05, 0.98), frameon=False,
          handlelength=3, fontsize=7)
fig.tight_layout(pad=0.3)
save(fig, "fig3i")
