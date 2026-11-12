"""Re-plot Fig. 11 (four panels) from figures/fig11a_left.csv, fig11a_right.csv, fig11b_left.csv, fig11b_right.csv
-> figures/fig11_replot.png.

    python3 -I -B figures/fig11.py
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "work"))
from replot_common import read_csv, series, split_gaps  # noqa: E402

fig, axs = plt.subplots(2, 2, figsize=(10, 8))
for ax, name, title, te_max in ((axs[0, 0], "a_left", "Defect Free WGP", 2.0e-3),
                                (axs[0, 1], "a_right", "250nm x 250nm Clear Defect", 1.0e-2)):
    R = read_csv(os.path.join(HERE, "fig11%s.csv" % name))
    x, y = series(R, "TM", "wavelength_nm", "value")
    ax.plot(x, y, "k-", lw=1.5, label="TM")
    ax.set(xlim=(400, 800), ylim=(0, 1.0), xlabel="Wavelength (nm)", ylabel="TM Transmission", title=title)
    ax2 = ax.twinx()
    x, y = series(R, "TE", "wavelength_nm", "value")
    for i, (sx, sy) in enumerate(split_gaps(x, y, 1.5)):
        ax2.plot(sx, sy, color="blue", lw=1.5, label="TE" if i == 0 else None)
    ax2.set(ylim=(0, te_max), ylabel="TE Transmission")
    ax2.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="upper right")
for ax, name, ymax in ((axs[1, 0], "b_left", 4000), (axs[1, 1], "b_right", 1000)):
    R = read_csv(os.path.join(HERE, "fig11%s.csv" % name))
    x, y = series(R, "ER", "wavelength_nm", "value")
    ax.plot(x, y, "k-", lw=1.5)
    ax.set(xlim=(400, 800), ylim=(0, ymax), xlabel="Wavelength (nm)", ylabel="Extinction Ratio",
           title="(b) " + name.split("_")[1])
axs[0, 0].text(0.02, 1.08, "(a)", transform=axs[0, 0].transAxes)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig11_replot.png"), dpi=150)
