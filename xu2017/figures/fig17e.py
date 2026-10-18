"""Re-plot Figure 17(e) of Xu et al. 2017 from fig17e.csv -> fig17e_replot.png"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
with open(HERE / "fig17e.csv") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
fig, ax = plt.subplots(figsize=(4.2, 3.2))
for s, c in [("800 V", "#5b9bd5"), ("1200 V", "#ed7d31")]:
    ax.plot([float(r["x_nm"]) for r in rows if r["series"] == s],
            [float(r["backscatter_percent"]) for r in rows if r["series"] == s], "o", color=c, label=s)
ax.set_xlim((0, 35))
ax.set_xticks(list(range(0, 36, 5)))
ax.set_ylim(8.0, 12.0)
ax.set_yticks([8 + 0.5 * i for i in range(9)])
ax.grid(color="0.85")
ax.set_title("Z Step Edge")
ax.set_xlabel("Nanometers")
ax.set_ylabel("Backscatter %")
ax.legend(frameon=False)
fig.tight_layout()
fig.savefig(HERE / "fig17e_replot.png", dpi=150)
