"""Redraw edfig6c: decoding accuracy vs number of faces (lines + shaded bands), from edfig6c.csv.
Run from inside the figure folder: python3 edfig6c.py  ->  edfig6c_replot.png (200 dpi)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.read_csv("edfig6c.csv", comment="#")
x = df["n_faces"].to_numpy()
COL = {"priming_average": "#1c0f29", "binocular_conscious_state1": "#fcae34", "binocular_conscious_state2": "#543379",
       "binocular_suppressed_state1": "#fcae34", "binocular_suppressed_state2": "#543379"}
DASH = (0, (4, 4))

plt.rcParams.update({"font.size": 7, "font.family": "DejaVu Sans", "lines.scale_dashes": False})  # dash pattern in points, as in the PDF
fig, ax = plt.subplots(figsize=(2.6, 3.0), dpi=200)
for name, col in COL.items():
    ax.fill_between(x, df[name + "_band_lo_pct"], df[name + "_band_hi_pct"], color=col, alpha=0.2, lw=0)
for name, col in COL.items():                         # lines on top of the bands
    ax.plot(x, df[name + "_pct"], color=col, lw=1.2, ls=DASH if "suppressed" in name else "-")
ax.set_xlim(0, 60); ax.set_ylim(0, 100)
ax.set_xticks([0, 20, 40, 60]); ax.set_yticks([0, 20, 40, 60, 80, 100])
ax.set_xlabel("Number of faces"); ax.set_ylabel("Decoding accuracy (%)")
ax.spines[["top", "right"]].set_visible(False)
ax.text(-0.3, 1.02, "c", transform=ax.transAxes, fontweight="bold", fontsize=9)
fig.tight_layout()
fig.savefig("edfig6c_replot.png", dpi=200)
