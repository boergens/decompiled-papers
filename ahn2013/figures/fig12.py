"""Re-plot Fig. 12 (both panels) from figures/fig12left.csv and figures/fig12right.csv -> figures/fig12_replot.png.

    python3 -I -B figures/fig12.py
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "work"))
from replot_common import read_csv, series, split_gaps  # noqa: E402

fig, (ax, axr) = plt.subplots(1, 2, figsize=(11, 4))
R = read_csv(os.path.join(HERE, "fig12left.csv"))
x, y = series(R, "TM", "wavelength_nm", "value")
ax.plot(x, y, "k-", lw=1.5, label="TM")
ax.set(xlim=(400, 800), ylim=(0, 1.0), xlabel="Wavelength (nm)", ylabel="TM transmission")
ax2 = ax.twinx()
x, y = series(R, "TE", "wavelength_nm", "value")
for i, (sx, sy) in enumerate(split_gaps(x, y, 1.5)):
    ax2.plot(sx, sy, color="blue", lw=1.5, label="TE" if i == 0 else None)
ax2.set(ylim=(0, 2.0e-3), ylabel="TE transmission")
ax2.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
h1, l1 = ax.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, loc="upper right")
R = read_csv(os.path.join(HERE, "fig12right.csv"))
x, y = series(R, "ER", "wavelength_nm", "value")
axr.plot(x, y, "k-", lw=1.5)
axr.set(xlim=(400, 800), ylim=(0, 4000), xlabel="Wavelength (nm)", ylabel="Extinction Ratio")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig12_replot.png"), dpi=150)
