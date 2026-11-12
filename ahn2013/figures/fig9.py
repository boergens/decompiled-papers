"""Re-plot Fig. 9 (a)-(d) from figures/fig9a.csv, fig9b.csv, fig9c.csv and fig9d.csv (printed part only, in_plot = 1)
-> figures/fig9_replot.png.

    python3 -I -B figures/fig9.py
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "work"))
from replot_common import read_csv, split_gaps  # noqa: E402

STYLE = {"100nmAl": (0, (8, 2, 3, 2)), "150nmAl": (0, (3, 1.5)), "200nmAl": (0, (4.5, 2.5)), "250nmAl": "-"}
fig, axs = plt.subplots(2, 2, figsize=(9, 7))
for ax, key in zip(axs.flat, "abcd"):
    R = [r for r in read_csv(os.path.join(HERE, "fig9%s.csv" % key)) if r["in_plot"] == 1]
    for name, ls in STYLE.items():
        pts = [(r["wavelength_nm"], r["value"]) for r in R if r["series"] == name]
        for i, (x, y) in enumerate(split_gaps([p[0] for p in pts], [p[1] for p in pts], 35)):
            ax.plot(x, y, color="k", ls=ls, lw=1.2, label=name if i == 0 else None)
    ax.set(xlim=(400, 800), xlabel="Wavelength (nm)", title="(%s)" % key)
    if key in "ab":
        ax.set(ylim=(0, 1), ylabel="Transmission (%)")
        ax.set_yticks([k / 10 for k in range(11)])
        ax.legend(loc="center right", fontsize=8)
    else:
        ax.set(yscale="log", ylim=(1, 1e9), ylabel="Extinction Ratio" if key == "c" else "Extinction ratio")
        ax.set_yticks([10.0 ** k for k in range(10)])
        ax.text(420, 3, "100nm pitch" if key == "c" else "130nm pitch")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig9_replot.png"), dpi=150)
