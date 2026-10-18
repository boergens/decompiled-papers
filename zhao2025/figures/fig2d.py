"""Re-plot Fig. 2d (right-hand plot) of Zhao et al. 2025 from fig2d.csv -> fig2d_replot.png"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
with open(HERE / "fig2d.csv") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
col = {"lambda=1.21": ("#d95319", "red"), "lambda=1.41": ("#0072bd", "#2083c5")}
fig, ax = plt.subplots(figsize=(4.0, 3.1))
for s, (cm, cl) in col.items():
    sel = lambda k: [(float(r["y_mm"]), float(r["x_mm"])) for r in rows if r["series"] == s and r["kind"] == k]
    p = sel("profile_point")
    ax.scatter([a for a, b in p], [b for a, b in p], s=40, facecolors="none", edgecolors=cm, label=s.replace("lambda", "λ "))
    fl = sel("parabolic_fit")
    ax.plot([a for a, b in fl], [b for a, b in fl], color=cl, lw=0.8)
    c = sel("dashed_circle_vertex")
    ax.plot([a for a, b in c], [b for a, b in c], ".", color=cl, ms=1)
ax.set_xlim(-0.9861, 1.0136)   # frame 326.45-460.23 pt mapped through the tick fit
ax.set_ylim(0.0, -1.5)         # bottom frame 0, top frame -1.5; x (mm) negative upwards as printed
ax.set_xticks([-0.5, 0, 0.5, 1]); ax.set_xticklabels(["-0.5", "0", "0.5", ""])
ax.set_yticks([0, -0.5, -1, -1.5]); ax.set_yticklabels(["", "-0.5", "-1", ""])
ax.axvline(0, color="k", lw=1)
ax.set_xlabel("y (mm)"); ax.set_ylabel("x (mm)")
ax.text(-0.85, -0.25, "r_b1 = 130 μm", color="red", fontsize=7)
ax.text(-0.85, -0.17, "r_b2 = 260 μm", color="#2083c5", fontsize=7)
ax.legend(fontsize=7, loc="lower right", frameon=False)
fig.tight_layout()
fig.savefig(HERE / "fig2d_replot.png", dpi=150)
