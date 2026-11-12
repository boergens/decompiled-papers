"""Re-plot Fig. 14 (four panels) from figures/fig14a_left.csv, fig14a_right.csv, fig14b_left.csv,
fig14b_right.csv -> figures/fig14_replot.png. The x axis is categorical (five evenly spaced labels).

    python3 -I -B figures/fig14.py
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "work"))
from replot_common import read_csv  # noqa: E402

STYLE = {"400nm": ("tab:blue", "D"), "600nm": ("tab:red", "s"), "800nm": ("yellowgreen", "^")}
CATS = [1, 10, 100, 1000, 10000]
fig, axs = plt.subplots(2, 2, figsize=(10, 7))
for (i, j), name, title, ylab, ylim, step in (
        ((0, 0), "a_left", "150nm x150nm opaque defect", "Transmission", 1.0, 0.1),
        ((0, 1), "a_right", "150nm x150nm opaque defect", "Extinction Ratio", 5000, 500),
        ((1, 0), "b_left", "5 µm x 5 µm opaque defect", "Transmission", 1.0, 0.1),
        ((1, 1), "b_right", "5 µm x 5 µm opaque defect", "Extinction Ratio", 5000, 500)):
    ax = axs[i, j]
    R = read_csv(os.path.join(HERE, "fig14%s.csv" % name))
    for s, (col, mk) in STYLE.items():
        pts = sorted((CATS.index(int(r["defect_density_cm2"])), r["value"]) for r in R if r["series"] == s)
        ax.plot([p[0] for p in pts], [p[1] for p in pts], color=col, marker=mk, label=s)
    ax.set_xticks(range(5), [str(c) for c in CATS])
    ax.set_xlim(-0.1, 4.1)
    ax.set_ylim(0, ylim)
    ax.set_yticks([k * step for k in range(11)])
    ax.grid(axis="y", color="0.85")
    ax.set(xlabel="Defect Density (cm$^{-2}$)", ylabel=ylab, title="(%s) %s" % (name[0], title))
    ax.legend(title="wavelength", fontsize=7, loc="center right")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig14_replot.png"), dpi=130)
