"""Re-plot Fig. 4d and 4e of Hua et al. 2015 from fig4d.csv and fig4e.csv (tier 1, authors' .mat data)
-> fig4d_replot.png, fig4e_replot.png and fig4de_replot.png (both panels with the shared colour bar, as printed)."""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.colors import LogNorm  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def load(panel):
    M = np.full((8, 8), np.nan)
    with open(os.path.join(HERE, f"fig4{panel}.csv")) as f:
        for r in csv.DictReader(l for l in f if not l.startswith("#")):
            M[int(r["T"]), int(r["N"])] = float(r["n_edges"]) if r["n_edges"] else np.nan
    return M


D, E = load("d"), load("e")
TOP = np.nanmax(D)          # MATLAB CLim upper limit = max of the measured histogram
show = lambda M: np.where(np.isnan(M) | (M < 1), 1.0, M)   # <=1, 0 and NaN shown as the lowest colour


def draw(ax, M, title):
    im = ax.imshow(show(M), cmap="jet", norm=LogNorm(1, TOP), origin="upper", extent=(-0.5, 7.5, 7.5, -0.5))
    ax.set_xticks([0, 3, 6])
    ax.set_yticks([0, 3, 6])
    ax.set_title(title)
    return im


fig, axs = plt.subplots(1, 2, figsize=(5, 2.4))
draw(axs[0], D, "Meas.")
im = draw(axs[1], E, "Fit")
axs[0].set_ylabel("Agreeing votes\nfor an edge ($T$)")
fig.supxlabel("Total votes for an edge ($N$)", fontsize=10)
cb = fig.colorbar(im, ax=axs, ticks=[1, 10, 100, 1000])
cb.ax.set_yticklabels(["1", "10", "100", "1,000"])
cb.set_label("# edges")
fig.savefig(os.path.join(HERE, "fig4de_replot.png"), dpi=150, bbox_inches="tight")
for p, M, t in (("d", D, "Meas."), ("e", E, "Fit")):
    fig, ax = plt.subplots(figsize=(2.8, 2.4))
    im = draw(ax, M, t)
    ax.set_xlabel("Total votes for an edge ($N$)")
    ax.set_ylabel("Agreeing votes for an edge ($T$)")
    cb = fig.colorbar(im, ax=ax, ticks=[1, 10, 100, 1000])
    cb.set_label("# edges")
    fig.savefig(os.path.join(HERE, f"fig4{p}_replot.png"), dpi=150, bbox_inches="tight")
