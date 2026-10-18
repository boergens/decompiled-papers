"""Re-plot Figure 13(a) of Wei et al. 2025 from fig13a.csv -> fig13a_replot.png"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
with open(HERE / "fig13a.csv") as f:
    rows = list(csv.DictReader(line for line in f if not line.startswith("#")))
fig, ax = plt.subplots(figsize=(4.2, 3.4))
style = {"Fx": ("k", "s", "none"), "Fy": ("red", "o", "red"), "Fz": ("magenta", "^", "none")}
for s, (c, m, fc) in style.items():
    pts = sorted((int(r["x_nominal_A"]), float(r["force_nN"])) for r in rows if r["series"] == s and r["force_nN"])
    x = np.array([p[0] for p in pts]); y = np.array([p[1] for p in pts])
    ax.plot(x, y, ls="--", color=c, lw=1, marker=m, ms=3.5, mfc=fc, mec=c, label="$F_" + s[1] + "$")
ax.set_xlim(*[-2.5, 60])
ax.set_ylim(*[-10, 10])
ax.set_xticks(np.arange(0.0, 60 + 0.01, 10))
ax.set_yticks(np.arange(-10, 10 + 0.01, 5))
ax.set_xlabel("Sliding distance (Å)")
ax.set_ylabel("Force (nN)")
ax.legend(loc="lower left", frameon=False, fontsize=8)
fig.tight_layout()
fig.savefig(HERE / "fig13a_replot.png", dpi=150)
