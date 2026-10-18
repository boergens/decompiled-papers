"""Re-plot Figure 8 of Sun & Gamstedt 2019 from fig8.csv -> fig8_replot.png"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
with open(HERE / "fig8.csv") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
colours = {"v0=0.25 mm s-1": "black", "v0=0.5 mm s-1": "red", "v0=1.0 mm s-1": "blue",
           "v0=3.0 mm s-1": "green", "v0=10.0 mm s-1": "magenta"}
fig, ax = plt.subplots(figsize=(5.5, 4.8))
for s, c in colours.items():
    rr = [r for r in rows if r["series"] == s]
    ax.plot([float(r["distance_nm"]) for r in rr], [float(r["height_nm"] or "nan") for r in rr], color=c, lw=1.2,
            label=s.replace("v0", "$v_0$").replace("s-1", "s$^{-1}$"))
ax.set_xlim(-60, 530)
ax.set_ylim(0, 10)
ax.set_xticks(range(0, 501, 100))
ax.set_yticks(range(0, 11))
ax.set_xlabel("Distance (nm)")
ax.set_ylabel("Relative height (nm)")
ax.legend(fontsize=7, loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=3, frameon=False)
fig.tight_layout()
fig.savefig(HERE / "fig8_replot.png", dpi=150)
