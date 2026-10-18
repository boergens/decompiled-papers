"""Redraw edfig6d: single-trial decoding accuracy vs time from flash (Average / State 1 / State 2), from edfig6d.csv.
Run from inside the figure folder: python3 edfig6d.py  ->  edfig6d_replot.png (200 dpi).
Note: the original axis label reads 'Time from flash (ms)', but the data run from -0.1 to 2.0 in 10-ms steps, i.e. the
unit is seconds (see the CSV header); the label below says seconds. Suppressed (dashed) traces have gaps where the
samples fell in the gaps of the original dashed line and could not be recovered; they are linearly interpolated for
display only (the CSV keeps them empty)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.read_csv("edfig6d.csv", comment="#")
t = df["time_from_flash_s"].to_numpy()
PANELS = [("average", "Average", "#808080", (0, 0)), ("state1", "State 1", "#fcae34", (1, 0)), ("state2", "State 2", "#543379", (1, 1))]
DASH = (0, (4, 4))

plt.rcParams.update({"font.size": 7, "font.family": "DejaVu Sans", "lines.scale_dashes": False})  # dash pattern in points, as in the PDF
fig, axs = plt.subplots(2, 2, figsize=(3.6, 3.6), dpi=200, sharex=True, sharey=True)
for name, title, col, (r, c) in PANELS:
    ax = axs[r][c]
    ax.plot(t, df[name + "_conscious_pct"], color=col, lw=1.2)
    sup = df[name + "_suppressed_pct"].interpolate(limit_area="inside")   # display-only interpolation across unrecovered samples
    ax.plot(t, sup, color=col, lw=1.2, ls=DASH)
    ax.set_title(title, fontsize=7, pad=3)
    ax.set_xlim(-0.1, 2.0); ax.set_ylim(0, 100)
    ax.set_xticks([0, 1, 2]); ax.set_yticks([0, 50, 100])
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(labelleft=True, labelbottom=True)
axs[0][1].set_axis_off()
axs[0][1].plot([], [], color="k", lw=1.2, label="Conscious"); axs[0][1].plot([], [], color="k", lw=1.2, ls=(0, (4, 3)), label="Suppressed")
axs[0][1].legend(loc="center left", frameon=False, fontsize=7, handlelength=2.0)
fig.supxlabel("Time from flash (s)", fontsize=7); fig.supylabel("Decoding accuracy (%)", fontsize=7)
axs[0][0].text(-0.45, 1.08, "d", transform=axs[0][0].transAxes, fontweight="bold", fontsize=9)
fig.tight_layout()
fig.savefig("edfig6d_replot.png", dpi=200)
