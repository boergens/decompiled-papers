"""Re-plot Figure 14(b) of Xu et al. 2017 from fig14b.csv -> fig14b_replot.png"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
with open(HERE / "fig14b.csv") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
fig, ax = plt.subplots(figsize=(5, 3))
bd = [r for r in rows if r["series"] == "boundary"]
ax.plot([float(r["angle_deg"]) for r in bd], [float(r["energy_eV"]) for r in bd], color="gold", lw=2)
for name, c in [("blue (1.1 keV) dot", "b"), ("green (600 eV) dot", "limegreen"), ("red (50 eV) dot", "r")]:
    dd = [r for r in rows if r["series"] == name]
    ax.plot([float(r["angle_deg"]) for r in dd], [float(r["energy_eV"]) for r in dd], "o-", color=c, ms=4, lw=0.8)
ax.set_xlim(0, 90)
ax.set_ylim(0, 1200)
ax.set_xticks(range(0, 91, 10))
ax.set_xlabel("Backscatter Angle (degrees)")
ax.set_ylabel("Backscatter Energy (eV)")
fig.tight_layout()
fig.savefig(HERE / "fig14b_replot.png", dpi=150)
