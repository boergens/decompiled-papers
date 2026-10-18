"""Redraw Extended Data Figure 4 (box plots of explained variance per session) from the CSVs.
Run from inside figures/:  python3 edfig4.py  ->  edfig4_replot.png"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import io
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle



def read_csv(path):
    """Read a CSV whose provenance comments start with '#'. (pandas' comment='#' would also eat the
    '#rrggbb' colour values, so only whole comment lines are dropped.)"""
    with open(path) as f:
        lines = [l for l in f if not l.startswith("#")]
    return pd.read_csv(io.StringIO("".join(lines)))


boxes = read_csv("edfig4_boxes.csv")
points = read_csv("edfig4_points.csv")

plt.rcParams.update({"font.size": 6, "font.family": "DejaVu Sans"})
fig, ax = plt.subplots(figsize=(4.7, 2.3), dpi=200)

for _, b in boxes.iterrows():
    x = b.category_index
    w = b.box_width_category_units
    ax.add_patch(Rectangle((x - w / 2, b.q1_pct), w, b.q3_pct - b.q1_pct,
                           facecolor=b.color_hex, alpha=b.box_fill_alpha, edgecolor="none", zorder=2))
    ax.plot([x - w / 2, x + w / 2], [b.median_pct] * 2, color=b.color_hex, alpha=b.line_and_point_alpha, lw=1, zorder=3)
    ax.plot([x, x], [b.q3_pct, b.whisker_max_pct], color=b.color_hex, alpha=b.line_and_point_alpha, lw=1, zorder=3)
    ax.plot([x, x], [b.whisker_min_pct, b.q1_pct], color=b.color_hex, alpha=b.line_and_point_alpha, lw=1, zorder=3)
    p = points[points.category_index == b.category_index]
    ax.scatter(p.x_position, p.explained_variance_pct, s=8, color=b.color_hex, alpha=b.line_and_point_alpha,
               linewidths=0, zorder=4)

ax.axhline(0, color="black", alpha=0.7, lw=0.5, ls=(0, (1, 2)), zorder=1)
ax.set_xlim(0.4, 5.6)
ax.set_ylim(-60, 80)
ax.set_yticks(range(-60, 81, 20))
ax.set_xticks(boxes.category_index)
ax.set_xticklabels([l.replace(" State", "\nState") for l in boxes.label])
ax.set_ylabel("Explained variance (%)")
ax.spines[["top", "right"]].set_visible(False)
ax.tick_params(length=3, width=0.5, labelsize=6)
for s in ("left", "bottom"):
    ax.spines[s].set_linewidth(0.5)
fig.tight_layout()
fig.savefig("edfig4_replot.png", dpi=200)
