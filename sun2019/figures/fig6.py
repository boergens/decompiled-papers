"""Re-plot Figure 6 of Sun & Gamstedt 2019 from fig6.csv -> fig6_replot.png"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
with open(HERE / "fig6.csv") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
fig, ax = plt.subplots(figsize=(5.5, 3.5))
ax2 = ax.twinx()
for s, axis, mk, ls in [("chip thickness", ax, "o", "-"), ("shear plane angle", ax2, "s", "--")]:
    rr = sorted((float(r["cutting_speed_mm_s"]), float(r["value"])) for r in rows if r["series"] == s)
    axis.plot(*zip(*rr), color="k", marker=mk, ls=ls, label=s)
ax.set_xlim(0, 10.5)
ax.set_xticks(range(11))
ax.set_ylim(86, 100)
ax.set_yticks(range(86, 101, 2))
ax2.set_ylim(53, 68)
ax2.set_yticks(range(53, 68, 2))
ax.set_xlabel("Cutting speed (mm/s)")
ax.set_ylabel("Chip thickness (nm)")
ax2.set_ylabel("Shear plane angle (°)")
fig.legend(loc="upper right", bbox_to_anchor=(0.85, 0.95), frameon=False)
fig.tight_layout()
fig.savefig(HERE / "fig6_replot.png", dpi=150)
