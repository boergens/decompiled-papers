"""Re-plot Figure 6(b) of Wei et al. 2025 from fig6b.csv -> fig6b_replot.png"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
with open(HERE / "fig6b.csv") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
sym = [r for r in rows if r["kind"] == "symbol"]
stk = [r for r in rows if r["kind"] == "symbol_stack"]
lin = [r for r in rows if r["kind"] == "line"]
fig, ax = plt.subplots(figsize=(4.6, 3.5))
ax.plot([float(r["hz_A"]) for r in lin], [float(r["Fz_nN"]) for r in lin], ".", ms=1.5, color="#ff0000", alpha=0.6,
        label="line (smoothed curve)")
ax.plot([float(r["hz_A"]) for r in sym], [float(r["Fz_nN"]) for r in sym], "o", ms=4, mfc="white", mec="#ff0000",
        label="Pyramid-45°")
for i, r in enumerate(stk):
    ax.plot([45, 45], [float(r["Fz_bottom_nN"]), float(r["Fz_top_nN"])], "-", lw=5, color="#ff0000", alpha=0.5,
            label="holding stack" if i == 0 else None)
ax.set_xlim(-5.02, 50.01)
ax.set_ylim(-4.0, 15.99)
ax.set_xticks([0, 10, 20, 30, 40, 50])
ax.set_yticks([-3, 0, 3, 6, 9, 12, 15])
ax.set_xlabel("Displacement of indenter $h_z$ (Å)")
ax.set_ylabel("Indenter force $F_z$ (nN)")
ax.legend(loc="upper left", fontsize=7, frameon=False)
fig.tight_layout()
fig.savefig(HERE / "fig6b_replot.png", dpi=150)
