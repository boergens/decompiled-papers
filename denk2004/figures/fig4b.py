"""Re-plot Figure 4B of Denk & Horstmann 2004 from fig4b.csv -> fig4b_replot.png"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Ellipse  # noqa: E402

HERE = Path(__file__).resolve().parent
with open(HERE / "fig4b.csv") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
fig, ax = plt.subplots(figsize=(4.2, 4.2))
pts = [r for r in rows if r["kind"] != "cluster"]
ax.plot([float(r["shift_x_nm"]) for r in pts], [float(r["shift_y_nm"]) for r in pts], "k.", ms=4)
for r in rows:
    if r["kind"] == "cluster":   # the unsplittable central cluster: its ink extent as an ellipse
        x0, x1, y0, y1 = (float(r[k]) for k in ("bbox_x_min_nm", "bbox_x_max_nm", "bbox_y_min_nm", "bbox_y_max_nm"))
        ax.add_patch(Ellipse(((x0 + x1) / 2, (y0 + y1) / 2), x1 - x0, y1 - y0, color="k"))
ax.set_xlim(-200, 200)
ax.set_ylim(-200, 200)
ax.spines["left"].set_position("zero")
ax.spines["bottom"].set_position("zero")
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.set_xticks([-200, -100, 100, 200])
ax.set_yticks([-200, -100, 100, 200])
ax.set_xlabel("shift_x (nm)", loc="right")
ax.set_ylabel("shift_y (nm)", loc="top")
ax.set_aspect("equal")
fig.tight_layout()
fig.savefig(HERE / "fig4b_replot.png", dpi=150)
