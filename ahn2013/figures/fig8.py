"""Re-plot Fig. 8(a) and 8(b) from figures/fig8a.csv and figures/fig8b.csv -> figures/fig8_replot.png.

    python3 -I -B figures/fig8.py
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "work"))
from replot_common import read_csv  # noqa: E402

fig, axs = plt.subplots(1, 2, figsize=(11, 4))
for ax, key, ylim, xlim, step in ((axs[0], "a", 6000, 800, 1000), (axs[1], "b", 50000, 725, 5000)):
    R = read_csv(os.path.join(HERE, "fig8%s.csv" % key))
    x = [r["wavelength_nm"] for r in R]
    ax.fill_between(x, [r["er_min"] for r in R], [r["er_max"] for r in R], color="#4a86c8", lw=0)
    ax.plot(x, [r["extinction_ratio"] for r in R], color="navy", lw=0.5)
    ax.set(xlim=(400, xlim), ylim=(0, ylim), xlabel="Wavelength (nm)", ylabel="Extinction Ratio (TM/TE)",
           title="(%s)" % key)
    ax.set_yticks(range(0, ylim + 1, step))
    ax.grid(axis="y", color="0.6")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig8_replot.png"), dpi=150)
