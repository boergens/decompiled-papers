"""Re-plot Fig. 2a of Zhao et al. 2025 from fig2a.csv -> fig2a_replot.png"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
with open(HERE / "fig2a.csv") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
fig, ax = plt.subplots(figsize=(4.2, 3))
cols = {"lambda=1.16": "#234462", "lambda=1.28": "#3975a7", "lambda=1.41": "#6fa2ce"}
done = set()
for s, c in cols.items():
    paths = sorted({int(r["path"]) for r in rows if r["series"] == s})
    for p in paths:
        pr = [r for r in rows if r["series"] == s and int(r["path"]) == p]
        ax.plot([float(r["delta_mm"]) for r in pr], [float(r["f_N"]) for r in pr], color=c, lw=0.6,
                label=None if s in done else s.replace("lambda", "λ "))
        done.add(s)
ax.add_patch(plt.Rectangle((9.51, 0.0177), 16.42, 0.1091, fill=False, ec="red", ls="-.", lw=1.5))  # drawn box, not data
ax.text(17.7, 0.075, "Steady-state regime", color="red", ha="center", fontsize=7)
ax.set_xlim(0, 30); ax.set_ylim(0, 0.2)
ax.set_xticks([0, 10, 20, 30]); ax.set_yticks([0, 0.1, 0.2])
ax.set_xlabel("δ (mm)"); ax.set_ylabel("f (N)")
ax.legend(frameon=False, fontsize=8)
fig.tight_layout()
fig.savefig(HERE / "fig2a_replot.png", dpi=150)
