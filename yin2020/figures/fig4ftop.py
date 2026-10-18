"""Re-plot Fig. 4f (top histogram) of Yin et al. 2020 from fig4ftop.csv -> fig4ftop_replot.png."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
with open(HERE / "fig4ftop.csv") as f:
    rows = list(csv.DictReader(line for line in f if not line.startswith("#")))
left = [float(r["bin_left_fps"]) for r in rows]
width = [float(r["bin_right_fps"]) - float(r["bin_left_fps"]) for r in rows]
count = [int(r["count"]) for r in rows]

fig, ax = plt.subplots(figsize=(4.0, 2.0))
ax.bar(left, count, width=width, align="edge", color="#4053a8", edgecolor="none")
# axis box as printed: x frame from about 1.33 to 5.17 fps, y frame from 0 to the top of the box
ax.set_xlim(1.325, 5.175)
ax.set_ylim(0, 164.6)
ax.set_xticks([1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0])
ax.set_yticks([0, 25, 50, 75, 100, 125, 150])
ax.set_xlabel("Montage rate with 20 MPixel tiles (fps)", fontsize=7)
ax.set_ylabel("Counts", fontsize=7)
ax.tick_params(labelsize=7)
fig.tight_layout()
fig.savefig(HERE / "fig4ftop_replot.png", dpi=200)
