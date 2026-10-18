#!/usr/bin/env python3
"""Redraw Figure 3f: explained variance (%) of the 50 face features (1-20 shape, 21-50 appearance) predicted from the
held-out half of neurons: priming average (black), binocular conscious features from state 1 (orange solid) and
state 2 (purple solid), binocular suppressed features from state 1 (orange dashed) and state 2 (purple dashed).
Reads fig3f.csv; writes fig3f_replot.png."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from fig3_common import BLACK, ORANGE, PURPLE, read_csv, save

d = read_csv("fig3f.csv")
x = d["feature_index"]
DASH = (0, (4, 4))

fig, ax = plt.subplots(figsize=(2.7, 3.1), dpi=200)
ax.plot(x, d["priming_average_pct"], color=BLACK, lw=1)
ax.plot(x, d["binocular_conscious_state1_pct"], color=ORANGE, lw=1)
ax.plot(x, d["binocular_conscious_state2_pct"], color=PURPLE, lw=1)
# dashed series: values are empty (NaN) where no estimate exists (first/last vertex beyond the first/last dash).
# Where the original clips the line at the axis minimum (recovery == 'clipped_at_axis_min', true value <= -100 unknown)
# the vertex is drawn at -100, exactly as the original figure does.
sup1 = d["binocular_suppressed_state1_pct"].where(d["binocular_suppressed_state1_recovery"] != "clipped_at_axis_min", -100.0)
ax.plot(x, sup1, color=ORANGE, lw=1, ls=DASH)
ax.plot(x, d["binocular_suppressed_state2_pct"], color=PURPLE, lw=1, ls=DASH)

ax.set_xlim(1, 50)
ax.set_ylim(-100, 100)
ax.set_xticks([10, 20, 30, 40, 50])
ax.set_yticks([-100, -50, 0, 50, 100])
ax.set_xlabel("Feature #")
ax.set_ylabel("Explained variance of features (%)")

# brackets above the plot: shape features 1-20, appearance features 21-50
for x0, x1, label in [(1, 19.7, "Shape"), (20.3, 50, "Appearance")]:
    ax.plot([x0, x0, x1, x1], [103, 108, 108, 103], color="k", lw=0.5, clip_on=False)
    ax.text((x0 + x1) / 2, 110, label, ha="center", va="bottom", fontsize=7)

# legend (shared by panels f and g in the original): solid lines left, dashed lines right
handles = [Line2D([], [], color=BLACK, lw=1), Line2D([], [], color=ORANGE, lw=1), Line2D([], [], color=PURPLE, lw=1),
           Line2D([], [], color="none"), Line2D([], [], color=ORANGE, lw=1, ls=DASH), Line2D([], [], color=PURPLE, lw=1, ls=DASH)]
labels = ["Priming, average", "Binocular conscious, state 1", "Binocular conscious, state 2",
          "", "Binocular suppressed, state 1", "Binocular suppressed, state 2"]
ax.legend(handles, labels, ncol=2, frameon=False, loc="upper center", bbox_to_anchor=(0.42, -0.17),
          handlelength=2.2, columnspacing=1.2, fontsize=5.5)
fig.tight_layout(pad=0.3, rect=(0, 0.04, 1, 0.97))
save(fig, "fig3f")
