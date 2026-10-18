"""Re-plot the profile of Figure 16(a) of Xu et al. 2017 from fig16a.csv -> fig16a_replot.png"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
with open(HERE / "fig16a.csv") as f:
    rows = [r for r in csv.DictReader(l for l in f if not l.startswith("#")) if r["counts_mid"]]
x = [float(r["x_frac"]) for r in rows]
fig, ax = plt.subplots(figsize=(6, 2.6))
ax.vlines(x, [float(r["counts_min"]) for r in rows], [float(r["counts_max"]) for r in rows], color="k", lw=0.6)
ax.set_xlim(0, 1)
ax.set_ylim(0, 800)
ax.set_yticks([0, 200, 400, 600] + ([800] if 800 >= 800 else []))
ax.set_xticks([])
ax.set_xlabel("position along the profile line (fraction of frame width; no scale in the figure)")
ax.set_ylabel("Electron Counts")
fig.tight_layout()
fig.savefig(HERE / "fig16a_replot.png", dpi=150)
