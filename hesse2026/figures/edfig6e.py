"""Redraw edfig6e: single-trial decoding accuracy per session (Average / State 1 / State 2), from edfig6e.csv.
Run from inside the figure folder: python3 edfig6e.py  ->  edfig6e_replot.png (200 dpi)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.read_csv("edfig6e.csv", comment="#", dtype={"session": str})
cols = ["average_pct", "state1_pct", "state2_pct"]
xs = np.array([0, 1, 2]); MCOL = ["#808080", "#fcae34", "#543379"]
DASH = (0, (4, 3))

plt.rcParams.update({"font.size": 7, "font.family": "DejaVu Sans", "lines.scale_dashes": False})  # dash pattern in points, as in the PDF
fig, ax = plt.subplots(figsize=(2.7, 3.0), dpi=200)
for cond, ls in (("conscious", "-"), ("suppressed", DASH)):
    sess = df[(df["condition"] == cond) & (df["session"] != "mean")]
    for _, row in sess.iterrows():                       # thin lines: individual sessions
        ax.plot(xs, row[cols].to_numpy(float), color="k", lw=0.3, ls=ls, alpha=0.5)
    mean = df[(df["condition"] == cond) & (df["session"] == "mean")].iloc[0][cols].to_numpy(float)
    ax.plot(xs, mean, color="k", lw=1.6, ls=ls, zorder=3)  # thick line: mean across sessions
    for xi, yi, col in zip(xs, mean, MCOL):               # filled = conscious, open = suppressed
        ax.plot(xi, yi, "o", ms=6, mfc=col if cond == "conscious" else "white", mec=col, mew=1.2, zorder=4)
ax.set_xlim(-0.5, 2.5); ax.set_ylim(0, 100)
ax.set_xticks(xs, ["Average", "State 1", "State 2"]); ax.set_yticks([0, 20, 40, 60, 80, 100])
ax.set_ylabel("Decoding accuracy (%)")
ax.spines[["top", "right"]].set_visible(False)
h1, = ax.plot([], [], "o", color="k", ms=6, ls="-", lw=1.4, label="Conscious")
h2, = ax.plot([], [], "o", mfc="white", mec="k", ms=6, ls=DASH, color="k", lw=1.4, label="Suppressed")
ax.legend(handles=[h1, h2], loc="upper left", frameon=False, fontsize=7, handlelength=2.4)
ax.text(-0.3, 1.02, "e", transform=ax.transAxes, fontweight="bold", fontsize=9)
fig.tight_layout()
fig.savefig("edfig6e_replot.png", dpi=200)
