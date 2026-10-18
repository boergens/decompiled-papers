#!/usr/bin/env python3
"""Redraw Figure 3g: decoding accuracy (%) vs number of faces (target + randomly selected distractors) for the
held-out half of neurons: priming average (black), conscious face decoded from state 1 (orange solid) / state 2
(purple solid), suppressed face decoded from state 1 (orange dashed) / state 2 (purple dashed); shaded bands as in
the figure. Reads fig3g.csv; writes fig3g_replot.png."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from fig3_common import BLACK, ORANGE, PURPLE, read_csv, save

d = read_csv("fig3g.csv")
x = d["number_of_faces"]
DASH = (0, (4, 4))
series = [("priming_average", BLACK, "-"), ("conscious_state1", ORANGE, "-"), ("conscious_state2", PURPLE, "-"),
          ("suppressed_state1", ORANGE, DASH), ("suppressed_state2", PURPLE, DASH)]

fig, ax = plt.subplots(figsize=(2.7, 3.1), dpi=200)
for name, col, ls in series:
    ax.fill_between(x, d[f"{name}_lo_pct"], d[f"{name}_hi_pct"], color=col, alpha=0.2, lw=0)
for name, col, ls in series:
    ax.plot(x, d[f"{name}_pct"], color=col, lw=1, ls=ls)

ax.set_xlim(0, 60)
ax.set_ylim(0, 100)
ax.set_xticks([0, 20, 40, 60])
ax.set_yticks([0, 20, 40, 60, 80, 100])
ax.set_xlabel("Number of faces")
ax.set_ylabel("Decoding accuracy (%)")

# legend (shared by panels f and g in the original): solid lines left, dashed lines right
handles = [Line2D([], [], color=BLACK, lw=1), Line2D([], [], color=ORANGE, lw=1), Line2D([], [], color=PURPLE, lw=1),
           Line2D([], [], color="none"), Line2D([], [], color=ORANGE, lw=1, ls=DASH), Line2D([], [], color=PURPLE, lw=1, ls=DASH)]
labels = ["Priming, average", "Binocular conscious, state 1", "Binocular conscious, state 2",
          "", "Binocular suppressed, state 1", "Binocular suppressed, state 2"]
ax.legend(handles, labels, ncol=2, frameon=False, loc="upper center", bbox_to_anchor=(0.42, -0.17),
          handlelength=2.2, columnspacing=1.2, fontsize=5.5)
fig.tight_layout(pad=0.3, rect=(0, 0.04, 1, 0.97))
save(fig, "fig3g")
