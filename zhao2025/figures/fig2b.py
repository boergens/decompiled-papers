"""Re-plot Fig. 2b of Zhao et al. 2025 from fig2b.csv -> fig2b_replot.png"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
with open(HERE / "fig2b.csv") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
fig, ax = plt.subplots(figsize=(3.8, 2.8))
ax2 = ax.twinx()
for axis, unit, col in ((ax, "f_N", "#3395d8"), (ax2, "r_b_um", "red")):
    rr = [r for r in rows if r["unit"] == unit]
    x = [float(r["lambda"]) for r in rr]
    y = [float(r["value"]) for r in rr]
    axis.plot(x, y, "-s", color=col, ms=5)
    for r in rr:
        v = float(r["value"])
        lo = float(r["err_low"]) if r["err_low"] else v
        hi = float(r["err_high"]) if r["err_high"] else v
        axis.errorbar([float(r["lambda"])], [v], yerr=[[v - lo], [hi - v]], color=col, capsize=3)
        if "Fracture" in r["series"]:
            axis.plot([float(r["lambda"])], [v], "x", color="white", ms=4)
ax.set_xlim(1, 1.5); ax.set_ylim(0, 0.2); ax2.set_ylim(0, 320.5)
ax.set_xticks([1, 1.1, 1.2, 1.3, 1.4, 1.5]); ax.set_yticks([0, 0.05, 0.1, 0.15, 0.2]); ax2.set_yticks([0, 100, 200, 300])
ax.set_xlabel("λ"); ax.set_ylabel("f (N)"); ax2.set_ylabel("r$_b$ (μm)")
fig.tight_layout()
fig.savefig(HERE / "fig2b_replot.png", dpi=150)
