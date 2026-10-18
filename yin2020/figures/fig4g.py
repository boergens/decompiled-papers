"""Re-plot Fig. 4g of Yin et al. 2020 from fig4g.csv -> fig4g_replot.png."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
with open(HERE / "fig4g.csv") as f:
    rows = list(csv.DictReader(line for line in f if not line.startswith("#")))
bars = [r for r in rows if r["series"] == "bars"]
cur = [r for r in rows if r["series"] == "fit_curve"]

fig, ax = plt.subplots(figsize=(3.6, 2.5))
ax.bar([float(r["x_s"]) for r in bars], [float(r["y_counts"]) for r in bars],
       width=[float(r["x_right_s"]) - float(r["x_s"]) for r in bars], align="edge",
       color="#9a9ad0", edgecolor="#303060", linewidth=0.5)
ax.plot([float(r["x_s"]) for r in cur], [float(r["y_counts"]) for r in cur], color="#3048b0", lw=1.5)
ax.set_xlim(0, 0.18)
ax.set_ylim(0, 40)
ax.set_xticks([0.00, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.14, 0.16, 0.18])
ax.set_yticks(range(0, 41, 5))
ax.set_xlabel("Stage step and settle time (s)", fontsize=7)
ax.set_ylabel("Counts", fontsize=7)
ax.tick_params(labelsize=6, direction="in", top=True, right=True)
fig.tight_layout()
fig.savefig(HERE / "fig4g_replot.png", dpi=200)
