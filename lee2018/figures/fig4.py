"""Re-plot Fig 4 of Lee et al. 2018 from fig4.csv -> fig4_replot.png (outline of the yield surface, 3D view)"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
with open(HERE / "fig4.csv") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
fig = plt.figure(figsize=(6, 6.4))
ax = fig.add_subplot(projection="3d", proj_type="ortho")
for name in dict.fromkeys(r["boundary"] for r in rows):
    R = [r for r in rows if r["boundary"] == name]
    ax.plot([float(r["m"]) for r in R], [float(r["c"]) for r in R], [float(r["yield"]) for r in R], lw=1.2, label=name)
ax.set_xlim(0, 100); ax.set_ylim(0, 80); ax.set_zlim(0, 100)
ax.set_xticks(range(0, 101, 20)); ax.set_yticks(range(0, 81, 20)); ax.set_zticks(range(0, 101, 20))
ax.set_xlabel("m (# of substrates per batch)")
ax.set_ylabel("c (# of sections per substrate)")
ax.set_zlabel("Predicted yield")
ax.view_init(elev=30, azim=-45)
ax.legend(fontsize=6, loc="upper left")
fig.tight_layout()
fig.savefig(HERE / "fig4_replot.png", dpi=150)
