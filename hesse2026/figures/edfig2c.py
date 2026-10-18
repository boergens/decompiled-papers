"""Redraw Extended Data Fig. 2c from edfig2c.csv. Run from this folder: python3 edfig2c.py
Writes edfig2c_replot.png (200 dpi)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import csv

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def read_csv(path):
    with open(path) as f:
        rows = list(csv.reader(l for l in f if not l.startswith("#")))
    hdr, body = rows[0], rows[1:]
    col = lambda name: np.array([float(r[hdr.index(name)]) if r[hdr.index(name)] != "" else np.nan for r in body])
    return hdr, body, col


hdr, body, col = read_csv("edfig2c.csv")
x = col("n_faces")
BLACK, GREY = "#1c0f29", "#808080"
series = [  # (column, colour, linestyle, legend label)
    ("priming_average", BLACK, "-", "Priming, average"),
    ("priming_average_predicting_flashed", BLACK, (0, (4, 4)), "Priming, average, predicting flashed"),
    ("binocular_conscious_average", GREY, "-", "Binocular conscious, average"),
    ("binocular_suppressed_average", GREY, (0, (4, 4)), "Binocular suppressed, average"),
]

plt.rcParams.update({"font.size": 6, "font.family": "DejaVu Sans", "axes.linewidth": 0.5,
                     "xtick.major.width": 0.5, "ytick.major.width": 0.5})
fig = plt.figure(figsize=(2.3, 3.2), dpi=200)
ax = fig.add_axes([0.22, 0.36, 0.70, 0.55])
for name, c, ls, lab in series:
    lo, hi = col(name + "_lo"), col(name + "_hi")
    ax.fill_between(x, lo, hi, color=c, alpha=0.2, lw=0)
for name, c, ls, lab in series:
    ax.plot(x, col(name), color=c, ls=ls, lw=1.0, label=lab)
ax.set_xlim(0, 60)
ax.set_ylim(0, 100)
ax.set_xticks([0, 20, 40, 60])
ax.set_yticks([0, 20, 40, 60, 80, 100])
ax.set_xlabel("Number of faces")
ax.set_ylabel("Decoding accuracy (%)")
ax.spines[["top", "right"]].set_visible(False)
ax.tick_params(length=3)
ax.legend(loc="upper left", bbox_to_anchor=(-0.28, -0.2), frameon=False, fontsize=6, handlelength=2.5,
          labelspacing=0.8, ncol=1)
fig.savefig("edfig2c_replot.png", dpi=200)
print("wrote edfig2c_replot.png")
