"""Re-plot Fig 5(e) of Lee et al. 2018 from fig5e.csv -> fig5e_replot.png"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
with open(HERE / "fig5e.csv") as f:
    lines = list(f)
dash = [float(v) for v in next(l for l in lines if "dashed lines at" in l).split("x = ")[1].split(" px")[0].split(", ")]
rows = list(csv.DictReader(l for l in lines if not l.startswith("#")))
fig, ax = plt.subplots(figsize=(4.5, 3.2))
for name, col in (("SiN (red)", "red"), ("Luxel (blue)", "blue")):
    R = [r for r in rows if r["series"] == name]
    x = np.array([float(r["distance_px"]) for r in R])
    gap = np.where(np.diff(x) > 1)[0] + 1
    y, lo, hi = (np.insert(np.array([float(r[k]) for r in R]), gap, np.nan) for k in ("intensity", "band_low", "band_high"))
    x = np.insert(x, gap, np.nan)
    ax.fill_between(x, lo, hi, color=col, alpha=0.2, lw=0)
    ax.plot(x, y, color=col, lw=0.8, label=name)
for xd in dash:
    ax.axvline(xd, color="k", ls="--", lw=0.8)
for xm, t in ((dash[0] / 2, "Interior"), ((dash[0] + dash[1]) / 2, "Edge"), ((dash[1] + 100) / 2, "Exterior")):
    ax.text(xm, 216, t, ha="center", fontsize=8)
ax.set_xlim(0, 100)
ax.set_ylim(80, 220)
ax.set_xticks([0, 100])
ax.set_yticks([80, 220])
ax.set_xlabel("Distance [px]")
ax.set_ylabel("Pixel intensity")
fig.tight_layout()
fig.savefig(HERE / "fig5e_replot.png", dpi=150)
