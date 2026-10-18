"""Re-draw Fig. 8C of Hayworth et al. 2014 as a 4 x 4 grid of the printed quality values -> fig8c_replot.png"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
with open(HERE / "fig8c_values.csv") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
fig, ax = plt.subplots(figsize=(4, 4))
for r in rows:
    i, j = int(r["row"]), int(r["col"])
    ax.add_patch(plt.Rectangle((j - 1, 4 - i), 1, 1, fill=True, fc="0.6", ec="k"))
    ax.text(j - 0.15, 4 - i + 0.5, r["quality_value"], ha="right", va="center",
            color="limegreen" if r["label_colour"] == "green" else "red", fontsize=12)
ax.set_xlim(0, 4)
ax.set_ylim(0, 4)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("Fig. 8C tile quality values (as printed)", fontsize=9)
fig.tight_layout()
fig.savefig(HERE / "fig8c_replot.png", dpi=150)
