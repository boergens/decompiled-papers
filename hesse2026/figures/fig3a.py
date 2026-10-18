#!/usr/bin/env python3
"""Redraw Figure 3a: box plot (median, IQR, range) of the per-session log-likelihood gain of the two-state over the
one-state model, with the 19 session points. Reads fig3a_box.csv and fig3a_points.csv; writes fig3a_replot.png."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import matplotlib.pyplot as plt

from fig3_common import read_csv, save

box = read_csv("fig3a_box.csv").set_index("statistic")["log_likelihood_diff"]
pts = read_csv("fig3a_points.csv")
DARK = "#262626"
BOX_W = 0.5                 # box width in x units
BOX_W_PT = 18.13            # box width in the original (pt), to scale the recorded point jitter

fig, ax = plt.subplots(figsize=(1.7, 1.55), dpi=200)
ax.axhline(0, color="#808080", lw=0.7, ls=(0, (5, 3)), zorder=0)                      # "neither model has an advantage"
ax.add_patch(plt.Rectangle((-BOX_W / 2, box["q1"]), BOX_W, box["q3"] - box["q1"], facecolor=DARK, alpha=0.3,
                           edgecolor="none", zorder=1))
ax.add_patch(plt.Rectangle((-BOX_W / 2, box["q1"]), BOX_W, box["q3"] - box["q1"], facecolor="none",
                           edgecolor=DARK, lw=1.0, zorder=2))
ax.plot([-BOX_W / 2, BOX_W / 2], [box["median"]] * 2, color=DARK, lw=1.0, zorder=2)      # median
ax.plot([0, 0], [box["q3"], box["whisker_high_max"]], color=DARK, lw=1.0, zorder=2)      # whiskers = range
ax.plot([0, 0], [box["whisker_low_min"], box["q1"]], color=DARK, lw=1.0, zorder=2)
ax.plot([-BOX_W / 4, BOX_W / 4], [box["whisker_high_max"]] * 2, color=DARK, lw=1.0, zorder=2)
ax.plot([-BOX_W / 4, BOX_W / 4], [box["whisker_low_min"]] * 2, color=DARK, lw=1.0, zorder=2)
ax.scatter(pts["x_jitter_pt"] / BOX_W_PT * BOX_W, pts["log_likelihood_diff"], s=9, color=DARK, lw=0, zorder=3)

ax.set_xlim(-0.75, 0.75)
ax.set_xticks([])
ax.set_ylim(-0.06, 0.82)
ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8])
ax.set_ylabel("Log-likelihood\n(two-state – one-state)")
ax.spines["bottom"].set_visible(False)
fig.tight_layout(pad=0.3)
save(fig, "fig3a")
