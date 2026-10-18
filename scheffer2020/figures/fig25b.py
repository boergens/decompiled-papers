"""Re-plot Fig. 25(b) from fig25b.csv -> fig25b_replot.png (one marker per cluster with its extent)."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
with open(HERE / "fig25b.csv") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
fig, ax = plt.subplots(figsize=(7, 5))
for r in rows:
    x, y = float(r["x"]), float(r["y"])
    # clusters slope down to the right: draw from (x_min, y_max) to (x_max, y_min)
    ax.plot([float(r["x_min"]), float(r["x_max"])], [float(r["y_max"]), float(r["y_min"])], "-", color="#0773b4", lw=3)
    ax.plot(x, y, "+", color="#0773b4", ms=8)
ax.set_xlim(0, 12); ax.set_ylim(0, 0.2)
ax.set_xlabel("Delay in millisec"); ax.set_ylabel("Amplitude in millivolts"); ax.set_title("Delay and Amplitude of Response")
ax.grid(True, color="w"); ax.set_facecolor("#f2f2f3")
fig.tight_layout(); fig.savefig(HERE / "fig25b_replot.png", dpi=100)
