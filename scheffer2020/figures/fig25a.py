"""Re-plot Fig. 25(a) from fig25a.csv -> fig25a_replot.png (clouds/bands drawn as extents and centre lines)."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
with open(HERE / "fig25a.csv") as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
COL = {"GA->GA": "#0773b4", "GA->EB": "#cc79a8", "GA->PB": "#189f74"}
fig, ax = plt.subplots(figsize=(7, 5))
for s, c in COL.items():
    cr = [r for r in rows if r["series"] == s and r["kind"] == "cloud_row"]
    for r in cr:
        ax.plot([float(r["x_min"]), float(r["x_max"])], [float(r["y"])] * 2, "-", color=c, lw=1)
    bc = [r for r in rows if r["series"] == s and r["kind"] == "band_centre"]
    for r in bc:
        ax.plot([float(r["x"])] * 2, [float(r["y_min"]), float(r["y_max"])], "-", color=c, lw=1)
    sm = [r for r in rows if r["series"] == s and r["kind"] == "cluster_summary"][0]
    ax.plot(float(sm["x"]), float(sm["y"]), "k+", ms=8)
    ax.plot([], [], "s", color=c, label=s.replace("->", " → "))
ax.set_xlim(0, 4); ax.set_ylim(0, 1.5)
ax.set_xlabel("Delay in millisec"); ax.set_ylabel("Amplitude in millivolts"); ax.set_title("Delay and Amplitude of Response")
ax.grid(True, color="w"); ax.set_facecolor("#f2f2f3"); ax.legend(loc="upper right")
fig.tight_layout(); fig.savefig(HERE / "fig25a_replot.png", dpi=100)
