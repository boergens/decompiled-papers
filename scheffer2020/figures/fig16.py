"""Re-plot Fig. 16 from fig16.csv -> fig16_replot.png: the point cloud as the band between its ink envelopes,
the whole markers that could be read individually, and the two reference lines."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
with open(HERE / "fig16.csv", newline="") as f:
    rows = list(csv.DictReader(r for r in f if not r.startswith("#")))
get = lambda k: ([float(r["x"]) for r in rows if r["kind"] == k], [float(r["y"]) for r in rows if r["kind"] == k])
fig, ax = plt.subplots(figsize=(10, 6.8))
ax.fill_between([5, 100, 100], [0, 95, 0], color="#f2f2f2")
xu, yu = get("envelope_upper")
xl, yl = get("envelope_lower")
ax.fill_between(xu, yl, yu, color="#0b71b4", alpha=0.35, lw=0, label="point cloud (ink envelope)")
xm, ym = get("marker")
ax.plot(xm, ym, "+", color="#0b71b4", ms=6, mew=1.5, label="individually read markers")
for k, c, lab in (("line_orange", "#e6a028", "Additional synapses: Five synapses"), ("line_grey", "#999999", "Fewer synapses: Five synapses")):
    x, y = get(k)
    ax.plot(x, y, color=c, lw=1.5, label=lab)
ax.set_xlim(-0.5, 100)
ax.set_ylim(0, 100)
ax.set_xticks(range(0, 101, 20))
ax.set_yticks(range(0, 101, 20))
ax.set_xlabel("Synapse count at 30% completeness")
ax.set_ylabel("Synapse count at 50% completeness")
ax.set_title("Change in synapse count for paths during successive refinement")
ax.legend(loc="upper left", fontsize=8, frameon=False)
fig.tight_layout()
fig.savefig(HERE / "fig16_replot.png", dpi=100)
