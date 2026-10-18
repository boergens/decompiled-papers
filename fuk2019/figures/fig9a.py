"""Re-plot Fig. 9a from figures/fig9a.csv -> figures/fig9a_replot.png."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
data = {}
with open(HERE / "fig9a.csv") as f:
    for r in csv.DictReader(line for line in f if not line.startswith("#")):
        data.setdefault(r["series"], ([], []))
        data[r["series"]][0].append(float(r["time_ps"]))
        data[r["series"]][1].append(float(r["msd_A2"]))
colours = {"300K": "black", "350K": "red", "400K": "blue", "450K": "magenta", "500K": "green", "550K": "navy", "600K": "#8000ff"}
fig, ax = plt.subplots(figsize=(5.8, 4.1))
for s, (x, y) in data.items():
    ax.plot(x, y, ".", ms=1.5, color=colours[s], label=s)
ax.axvline(15, color="red", ls="--", lw=1)
ax.set_xlim(0, 25)
ax.set_ylim(0, 8)
ax.set_xlabel("Time (ps)")
ax.set_ylabel("MSD(Å$^2$)")
ax.legend(loc="upper left", fontsize=7, markerscale=5)
ax.text(0.97, 0.95, "(a)", transform=ax.transAxes, ha="right", va="top", fontsize=14, weight="bold")
fig.tight_layout()
fig.savefig(HERE / "fig9a_replot.png", dpi=150)
