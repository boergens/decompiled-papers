"""Redraw Extended Data Fig. 3c (monkey A, decoding accuracy) from edfig3c.csv.
Run from this folder: python3 edfig3c.py  -> edfig3c_replot.png (200 dpi)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import csv

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PANEL = "edfig3c"


def read_csv(path):
    with open(path) as f:
        rows = list(csv.reader(l for l in f if not l.startswith("#")))
    hdr, body = rows[0], rows[1:]
    col = lambda name: np.array([float(r[hdr.index(name)]) if r[hdr.index(name)] != "" else np.nan for r in body])
    return hdr, body, col


hdr, body, col = read_csv(PANEL + ".csv")
x = col("n_faces")
BLACK, ORANGE, PURPLE = "#1c0f29", "#fcae34", "#543379"
DASH = (0, (4, 4))
series = [  # (column, colour, linestyle, legend label) in the original draw order
    ("priming_average", BLACK, "-", "Priming, average"),
    ("binocular_conscious_state1", ORANGE, "-", "Binocular conscious, state 1"),
    ("binocular_suppressed_state1", ORANGE, DASH, "Binocular suppressed, state 1"),
    ("binocular_conscious_state2", PURPLE, "-", "Binocular conscious, state 2"),
    ("binocular_suppressed_state2", PURPLE, DASH, "Binocular suppressed, state 2"),
]

plt.rcParams.update({"font.size": 6, "font.family": "DejaVu Sans", "axes.linewidth": 0.5,
                     "xtick.major.width": 0.5, "ytick.major.width": 0.5})
fig = plt.figure(figsize=(2.3, 3.4), dpi=200)
ax = fig.add_axes([0.22, 0.40, 0.70, 0.52])
for name, c, ls, lab in series:  # band then line for each series, as in the original
    ax.fill_between(x, col(name + "_lo"), col(name + "_hi"), color=c, alpha=0.2, lw=0)
    ax.plot(x, col(name), color=c, ls=ls, lw=1.0, label=lab)
ax.set_xlim(0, 60)
ax.set_ylim(0, 100)
ax.set_xticks([0, 20, 40, 60])
ax.set_yticks([0, 20, 40, 60, 80, 100])
ax.set_xlabel("Number of faces")
ax.set_ylabel("Decoding accuracy (%)")
ax.spines[["top", "right"]].set_visible(False)
ax.tick_params(length=3)
h, l = ax.get_legend_handles_labels()
order = [0, 1, 3, 2, 4]
ax.legend([h[i] for i in order], [l[i] for i in order], loc="upper left", bbox_to_anchor=(-0.28, -0.2),
          frameon=False, fontsize=6, handlelength=2.5, labelspacing=0.7, ncol=1)
fig.savefig(PANEL + "_replot.png", dpi=200)
print(f"wrote {PANEL}_replot.png")
