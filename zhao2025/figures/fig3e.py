"""Re-plot Fig. 3e (plot) of Zhao et al. 2025 from fig3e.csv -> fig3e_replot.png"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
with open(HERE / "fig3e.csv") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
fig, ax = plt.subplots(figsize=(3.6, 2.6))
s = [r for r in rows if r["series"] == "lambda=1.45"]
ax.plot([float(r["y_um"]) for r in s], [float(r["phi_y_percent"]) for r in s], color="#e74c3c", label="λ = 1.45")
first = True
for piece in sorted({r["piece"] for r in rows if r["series"] == "lambda=1.21"}, key=lambda p: int(p[4:])):
    s = [r for r in rows if r["series"] == "lambda=1.21" and r["piece"] == piece]
    ax.plot([float(r["y_um"]) for r in s], [float(r["phi_y_percent"]) for r in s], color="#e74c3c", lw=1,
            label="λ = 1.21 (dashes)" if first else None)
    first = False
s = [r for r in rows if r["series"] == "phi_b line"]
ax.plot([float(r["y_um"]) for r in s], [float(r["phi_y_percent"]) for r in s], "k-.", lw=1.5)
ax.text(140, 0.03, "φb=0.02%")
ax.set_xlim(0, 200); ax.set_ylim(0, 0.5)
ax.set_xlabel("y (μm)"); ax.set_ylabel("φy %")
ax.legend(fontsize=7)
fig.tight_layout()
fig.savefig(HERE / "fig3e_replot.png", dpi=150)
