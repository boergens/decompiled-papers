"""Re-plot Fig 1 of Lee et al. 2018 from fig1.csv -> fig1_replot.png"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
with open(HERE / "fig1.csv") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
fig, ax = plt.subplots(figsize=(6, 6))
for r in rows:
    if r["kind"] == "point":
        x, y = float(r["year"]), float(r["volume_mm3"])
        ax.plot(x, y, "ko", ms=4)
        ax.annotate(f"[{r['label']}]", (x, y), textcoords="offset points", xytext=(0, 7), ha="center", fontsize=8)
    else:
        ax.axhline(float(r["volume_mm3"]), color="k", ls="--", lw=1.5)
ax.set_yscale("log")
ax.set_xlim(1970, 2025)
ax.set_ylim(1e-7, 1)
ax.set_xticks(range(1970, 2026, 5))
ax.set_xlabel("Year of Publication")
ax.set_ylabel("Volume of Neural Tissue Studied [mm$^3$]")
ax.legend(handles=[plt.Line2D([], [], ls="none", label=f"[{r['label']}] {r['legend']}") for r in rows if r["kind"] == "point"],
          loc="lower right", fontsize=5, handlelength=0, frameon=True)
fig.tight_layout()
fig.savefig(HERE / "fig1_replot.png", dpi=150)
