"""Redraw edfig5b: explained variance of face features vs feature index, from edfig5b.csv.
Run from inside the figure folder: python3 edfig5b.py  ->  edfig5b_replot.png (200 dpi)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.read_csv("edfig5b.csv", comment="#")      # the CSV has no '#' inside data fields
x = df["feature_index"].to_numpy()
COL = {"priming": "#1c0f29", "state1": "#fcae34", "state2": "#543379"}
DASH = (0, (4, 4))                                   # 4 pt on / 4 pt off, as in the original

plt.rcParams.update({"font.size": 7, "font.family": "DejaVu Sans", "lines.scale_dashes": False})  # dash pattern in points, as in the PDF
fig, ax = plt.subplots(figsize=(2.9, 3.5), dpi=200)
ax.plot(x, df["priming_average_pct"], color=COL["priming"], lw=1.2, label="Priming, average")
ax.plot(x, df["binocular_conscious_state1_pct"], color=COL["state1"], lw=1.2, label="Binocular conscious, state 1")
ax.plot(x, df["binocular_conscious_state2_pct"], color=COL["state2"], lw=1.2, label="Binocular conscious, state 2")
# dashed series: empty cells (not recoverable from the PDF) leave gaps in the line
ax.plot(x, df["binocular_suppressed_state1_pct"], color=COL["state1"], lw=1.2, ls=DASH, label="Binocular suppressed, state 1")
ax.plot(x, df["binocular_suppressed_state2_pct"], color=COL["state2"], lw=1.2, ls=DASH, label="Binocular suppressed, state 2")
ax.set_xlim(1, 50); ax.set_ylim(-100, 100)
ax.set_xticks([10, 20, 30, 40, 50]); ax.set_yticks([-100, -50, 0, 50, 100])
ax.set_xlabel("Feature #"); ax.set_ylabel("Explained variance of features (%)")
ax.spines[["top", "right"]].set_visible(False)
# Shape / Appearance brackets above the plot (positions in x-axis units, as in the original)
for x0, x1, lab in [(1.02, 19.69, "Shape"), (20.24, 50.11, "Appearance")]:
    ax.plot([x0, x0, x1, x1], [104, 108, 108, 104], color="k", lw=0.5, clip_on=False)
    ax.text((x0 + x1) / 2, 110, lab, ha="center", va="bottom", fontsize=6.5)
ax.text(-0.33, 1.06, "b", transform=ax.transAxes, fontweight="bold", fontsize=9)
fig.legend(loc="lower center", ncol=2, fontsize=5, frameon=False, bbox_to_anchor=(0.5, 0.0), handlelength=2.0, columnspacing=1.0)
fig.tight_layout(rect=(0, 0.1, 1, 1))
fig.savefig("edfig5b_replot.png", dpi=200)
