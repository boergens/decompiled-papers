"""Re-plot Figure 2c of He et al. 2018 from fig2c.csv -> fig2c_replot.png (15 small bar charts, 3 x 5)."""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "fig2c.csv")) as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
COL = {"blue": "#4f81bd", "red": "#c0504d", "green": "#9bbb59", "purple": "#8064a2"}
energies = sorted({r["energy_keV"] for r in rows}, key=float)
fig, axs = plt.subplots(3, 5, figsize=(10, 4.5))
for ax, e in zip(axs.flat, energies):
    r = [q for q in rows if q["energy_keV"] == e]
    nmaj, nmin = int(r[0]["n_major"]), int(r[0]["n_minor"])
    for y in np.linspace(0, 1, nmaj + nmin):        # all gridlines, equally spaced in the box
        ax.axhline(y, color="0.92", lw=0.6, zorder=0)
    for y in np.linspace(0, 1, nmaj):                # major gridlines
        ax.axhline(y, color="0.75", lw=0.8, zorder=0)
    ax.bar(range(4), [float(q["height_frac"]) for q in r], width=1.0, color=[COL[q["colour"]] for q in r])
    ax.set_xlim(-1.5, 4.5)
    ax.set_ylim(0, 1.25)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title(f"{e} keV", fontsize=10)
fig.supxlabel("Depth (nm)")
fig.supylabel("Relative intensity")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig2c_replot.png"), dpi=150)
