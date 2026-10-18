"""Re-plot Figure 15(b) of Xu et al. 2017 from fig15b.csv -> fig15b_replot.png"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
with open(HERE / "fig15b.csv") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
d = {}
for r in rows:
    d.setdefault(r["series"], ([], []))
    d[r["series"]][0].append(float(r["landing_energy"]))
    d[r["series"]][1].append(float(r["scattering_ratio_Os_C"]))
fig, ax = plt.subplots(figsize=(3.2, 3.6))
ax.plot(*d["curve"], ".", color="k", ms=1)
ax.plot(*d["markers"], "o", color="#2e3192", ms=7)
ax.set_yscale("log")
ax.set_xlim(0.4, 1.4)
ax.set_ylim(10, 1000)
ax.set_xticks([0.6, 1.0, 1.4])
ax.set_xlabel("Landing Energy (eV)")
ax.set_ylabel("Scattering Ratio Os/C")
fig.tight_layout()
fig.savefig(HERE / "fig15b_replot.png", dpi=150)
