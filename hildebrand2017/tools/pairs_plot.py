"""Re-plot a 6 x 6 pair matrix CSV (Fig. 4e, 4j, Extended Data Fig. 9f) with the 'winter' blue-green map."""
import csv

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

COL = {"MeMv": "#1f5fb4", "MeMd": "#8ab4e8", "MeLr": "#f2e442", "MeLm": "#f26b21", "MeLc": "#4cb050", "Mauthner": "#7b2a7b"}


def plot(csv_path, out_png, top_u, top_l, unit_u, unit_l, title):
    with open(csv_path) as f:
        rows = list(csv.DictReader(line for line in f if not line.startswith("#")))
    names = [None] * 6
    U = np.full((6, 6), np.nan)
    L = np.full((6, 6), np.nan)
    for r in rows:
        i, j = int(r["row"]) - 1, int(r["col"]) - 1
        names[i] = r["row_axon"]
        if r["triangle"] == "upper":
            U[i, j] = float(r["value"]) / top_u
        else:
            L[i, j] = float(r["value"]) / top_l
    fig, ax = plt.subplots(figsize=(3, 2.6))
    M = np.where(np.isnan(U), L, U)
    im = ax.imshow(M, cmap="winter", vmin=0, vmax=1)
    for k, n in enumerate(names):
        ax.scatter(6, k, color=COL[n], s=60)
        ax.scatter(k, 6, color=COL[n], s=60)
    ax.set_xlim(-0.5, 6.5)
    ax.set_ylim(6.5, -0.5)
    ax.set_xticks(np.arange(-0.5, 6), minor=True)
    ax.set_yticks(np.arange(-0.5, 6), minor=True)
    ax.grid(which="minor", color="w", lw=2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title, fontsize=8)
    cb = fig.colorbar(im, ticks=[0, 1])
    cb.ax.set_yticklabels([f"0{unit_u} / 0", f"{top_u:g}{unit_u} / {top_l:g} {unit_l}"], fontsize=7)
    fig.tight_layout()
    fig.savefig(out_png, dpi=150)
