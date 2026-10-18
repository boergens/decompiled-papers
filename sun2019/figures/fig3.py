"""Re-plot Figure 3 of Sun & Gamstedt 2019 from fig3.csv -> fig3_replot.png"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
with open(HERE / "fig3.csv") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
fig, ax = plt.subplots(figsize=(5.5, 3.4))
ax2 = ax.twinx()
for s, axis, mk, ls in [("chip thickness", ax, "o", "-"), ("shear plane angle", ax2, "s", "--")]:
    rr = [r for r in rows if r["series"] == s]
    axis.plot([int(r["category_index"]) for r in rr], [float(r["value"]) for r in rr],
              color="k", marker=mk, ls=ls, label=s)
ax.set_xticks(range(6))
ax.set_xticklabels([r["cutting_thickness_nm"] for r in rows[:6]])
ax.set_xlim(-0.5, 5.5)   # category axis: one slot per category
ax.set_ylim(0, 300)
ax2.set_ylim(40, 60)
ax.set_xlabel("Cutting thickness (nm)")
ax.set_ylabel("Chip thickness (nm)")
ax2.set_ylabel("Shear plane angle (°)")
fig.legend(loc="upper left", bbox_to_anchor=(0.15, 0.95), frameon=False)
fig.tight_layout()
fig.savefig(HERE / "fig3_replot.png", dpi=150)
