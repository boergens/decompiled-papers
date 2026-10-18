"""Redraw Extended Data Fig. 3e (monkey M, explained variance) from edfig3e.csv.
Run from this folder: python3 edfig3e.py  -> edfig3e_replot.png (200 dpi)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import csv

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PANEL = "edfig3e"


def read_csv(path):
    with open(path) as f:
        rows = list(csv.reader(l for l in f if not l.startswith("#")))
    hdr, body = rows[0], rows[1:]
    col = lambda name: np.array([float(r[hdr.index(name)]) if r[hdr.index(name)] != "" else np.nan for r in body])
    return hdr, body, col


hdr, body, col = read_csv(PANEL + ".csv")
x = col("feature_index")
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
ax = fig.add_axes([0.24, 0.40, 0.68, 0.52])
for name, c, ls, lab in series:
    ax.plot(x, col(name), color=c, ls=ls, lw=1.0, label=lab)
ax.set_xlim(1, 50)
ax.set_ylim(-100, 100)
ax.set_xticks([10, 20, 30, 40, 50])
ax.set_yticks([-100, -50, 0, 50, 100])
ax.set_xlabel("Feature #")
ax.set_ylabel("Explained variance of features (%)")
ax.spines[["top", "right"]].set_visible(False)
ax.tick_params(length=3)
# 'Shape' (features 1-20) and 'Appearance' (21-50) brackets above the axes, as in the original
for x0, x1, lab in ((1, 20, "Shape"), (21, 50, "Appearance")):
    ax.annotate("", xy=(x0, 103), xytext=(x1, 103), xycoords=("data", "data"), annotation_clip=False,
                arrowprops=dict(arrowstyle="-", lw=0.5, color="k", shrinkA=0, shrinkB=0))
    for xx in (x0, x1):
        ax.plot([xx, xx], [103, 107], color="k", lw=0.5, clip_on=False)
    ax.text((x0 + x1) / 2, 109, lab, ha="center", va="bottom", fontsize=6)
# legend in the original's order (priming, conscious 1, conscious 2, suppressed 1, suppressed 2)
h, l = ax.get_legend_handles_labels()
order = [0, 1, 3, 2, 4]
ax.legend([h[i] for i in order], [l[i] for i in order], loc="upper left", bbox_to_anchor=(-0.3, -0.2),
          frameon=False, fontsize=6, handlelength=2.5, labelspacing=0.7, ncol=1)
fig.savefig(PANEL + "_replot.png", dpi=200)
print(f"wrote {PANEL}_replot.png")
