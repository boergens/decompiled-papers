"""Re-plot zhangk2020 Fig. 6b from fig6b.csv -> fig6b_replot.png (nm, arbitrary origin)."""
import csv
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent


def read(name):
    with open(HERE / name) as f:
        rows = list(csv.DictReader(line for line in f if not line.startswith("#")))
    return rows


def series(rows, key="series"):
    d = defaultdict(list)
    for r in rows:
        d[r[key]].append(r)
    return d


s = series(read("fig6b.csv"))
fig, ax = plt.subplots(figsize=(4.0, 2.9))
c = s["Raw data (circles)"]
ln = s["Raw data (red line vertices)"]
f = s["Fitted curve (vertices)"]
ax.plot([float(q["x_nm"]) for q in ln], [float(q["z_nm"]) for q in ln], color="red", lw=1)
ax.plot([float(q["x_nm"]) for q in c], [float(q["z_nm"]) for q in c], "o", color="red", mfc="none", ms=5, label="Raw data")
ax.plot([float(q["x_nm"]) for q in f], [float(q["z_nm"]) for q in f], color="black", lw=3, label="Fitted curve")
ax.set(xlim=(0, 99.9), ylim=(0, 80), xticks=[20, 40, 60, 80], yticks=[20, 40, 60], xticklabels=[], yticklabels=[],
       xlabel="X-position 20 nm/div.", ylabel="Z-position 20 nm/div.")
ax.legend(fontsize=7)
fig.tight_layout()
fig.savefig(HERE / "fig6b_replot.png", dpi=200)
