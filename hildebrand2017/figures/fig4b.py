"""Re-plot Fig. 4b from fig4b.csv -> fig4b_replot.png (colour scale clipped to 2000-6000 as printed)."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
with open(HERE / "fig4b.csv") as f:
    rows = list(csv.DictReader(line for line in f if not line.startswith("#")))
n = 22
M = np.zeros((n, n))
names = [""] * n
fig, ax = plt.subplots(figsize=(6, 5.4))
for r in rows:
    i, j = int(r["row"]) - 1, int(r["col"]) - 1
    M[i, j] = float(r["cost"])
    names[i] = r["left"]
im = ax.imshow(M, cmap="viridis_r", vmin=2000, vmax=6000)
for r in rows:
    if r["asterisk"]:
        ax.text(int(r["col"]) - 1, int(r["row"]) - 1, "*", ha="center", va="center",
                color="red" if r["asterisk"] == "red" else "k", fontsize=10)
ax.set_xticks(range(n), names, rotation=90, fontsize=7)
ax.set_yticks(range(n), names, fontsize=7)
ax.set_xlabel("right")
ax.set_ylabel("left")
ax.set_xticks(np.arange(-0.5, n), minor=True)
ax.set_yticks(np.arange(-0.5, n), minor=True)
ax.grid(which="minor", color="w", lw=1)
ax.tick_params(which="minor", length=0)
cb = fig.colorbar(im, ticks=[2000, 3000, 4000, 5000, 6000])
cb.set_label("cost")
fig.tight_layout()
fig.savefig(HERE / "fig4b_replot.png", dpi=150)
