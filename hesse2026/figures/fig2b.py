#!/usr/bin/env python3
"""Redraw Figure 2b (example trial: spike raster of 411 cells with the inferred state shading) from
fig2b_spikes.csv and fig2b_states.csv (+ the two stimulus icons fig2b_icon_face1/2.png if present)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.patches import FancyBboxPatch

sp = pd.read_csv("fig2b_spikes.csv", comment="#")
st = pd.read_csv("fig2b_states.csv", comment="#")
ORANGE, PURPLE = "#fcae34", "#543379"

fig = plt.figure(figsize=(5.0, 2.2), dpi=200)
ax = fig.add_axes([0.07, 0.2, 0.86, 0.55])          # raster
top = fig.add_axes([0.07, 0.77, 0.86, 0.21], sharex=ax)   # strip for the period brackets and stimulus icons
for _, r in st.iterrows():
    ax.axvspan(r["t_start_s"], r["t_end_s"], color=ORANGE if r["state"] == 1 else PURPLE, alpha=0.25, lw=0)
ax.plot(sp["time_s"], sp["row_from_top"], "|", color="#333333", ms=1.3, mew=0.3)
ax.axvline(0, color="k", lw=0.6)
ax.axhline(157.5, color="k", lw=0.4)            # 157 ML cells above, 254 AM cells below
ax.set_xlim(-1, 1); ax.set_ylim(411.5, 0.5)
ax.set_xticks([-1, -0.5, 0, 0.5, 1]); ax.set_yticks([])
ax.set_xlabel("Time from flash (seconds)", fontsize=7); ax.set_ylabel("411 cells", fontsize=7)
ax.tick_params(labelsize=6)
ax.text(1.01, 79, "ML", fontsize=6.5, va="center", transform=ax.get_yaxis_transform())
ax.text(1.01, 284, "AM", fontsize=6.5, va="center", transform=ax.get_yaxis_transform())
ax.spines[["top", "right"]].set_visible(False)
# brackets over the priming (-1..0 s) and binocular (0..1 s) periods, with the stimulus icons
top.set_ylim(0, 1); top.axis("off")
for x0, x1 in [(-1, -0.02), (0.02, 1)]:
    top.plot([x0, x0, x1, x1], [0.18, 0.04, 0.04, 0.18], color="k", lw=0.6)
icons = [("fig2b_icon_face1.png", -0.577), ("fig2b_icon_face1.png", 0.443), ("fig2b_icon_face2.png", 0.562)]
w = 0.11                                           # icon width in seconds (the strip is 2 s wide)
for fn, xc in icons:
    if os.path.exists(fn):
        top.imshow(plt.imread(fn), extent=(xc - w / 2, xc + w / 2, 0.3, 0.98), aspect="auto", zorder=3, cmap="gray")
for x0, x1 in [(-0.64, -0.51), (0.38, 0.63)]:
    top.add_patch(FancyBboxPatch((x0, 0.24), x1 - x0, 0.8, boxstyle="round,pad=0.01", fc="#afabab", ec="#434343", lw=0.5, zorder=2, clip_on=False))
fig.savefig("fig2b_replot.png", dpi=200)
