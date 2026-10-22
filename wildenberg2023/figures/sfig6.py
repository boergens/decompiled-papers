"""Re-plot Supplementary Figure 6 of Wildenberg et al. 2023 from sfig6.csv -> sfig6_replot.png"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "sfig6.csv")) as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
COL = {"0.50": "#5700eb", "0.75": "#78ff00", "0.90": "#e02100", "0.99": "#1470ff"}
series = {}
for r in rows:
    series.setdefault((r["success_rate"], r["pillar_diameter_mm"]), []).append((float(r["distance_mm"]), float(r["n_traced"])))
fig, ax = plt.subplots(figsize=(5.2, 3.6))
for (rate, diam), pts in sorted(series.items()):
    pts.sort()
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=COL[rate], lw=1.6,
            ls="-" if diam == "1" else (0, (1, 1.5)), label=f"{rate}, {diam} mm")
ax.set_yscale("log")
ax.set_xlim(0, 100)
ax.set_ylim(1, 10 ** 4.846)
ax.set_xticks(range(0, 101, 10))
ax.set_xlabel("Distance (mm)")
ax.set_ylabel("No. MAs traced")
ax.legend(title="Success rate, pillar diameter", fontsize=6, title_fontsize=6, ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.22))
fig.tight_layout()
fig.savefig(os.path.join(HERE, "sfig6_replot.png"), dpi=200)
