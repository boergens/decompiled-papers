"""Re-plot zhangk2020 Fig. 5 from fig5.csv -> fig5_replot.png (two y axes, arbitrary origins)."""
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


s = series(read("fig5.csv"))
fig, ax = plt.subplots(figsize=(4.4, 3.2))
ax2 = ax.twinx()
i = s["Inside sensor"]
o = s["Outside sensor"]
ax.plot([float(q["t_s"]) for q in i], [float(q["y_nm"]) for q in i], color="blue", lw=1)
ax2.plot([float(q["t_s"]) for q in o], [float(q["y_nm"]) for q in o], color="red", lw=1)
# frame: left to right frame = 27.0 s; inside axis 0-494.7 nm, outside axis 0-275.0 nm (bottom to top frame)
ax.set(xlim=(0, 27.0), ylim=(0, 494.68), xticks=[2.0, 7.0, 12.0, 17.0, 22.0], xticklabels=[],
       yticks=[54.68, 164.71, 274.85, 384.54], yticklabels=[],
       xlabel="Time 5 s/div.", ylabel="Output of inside sensor 110 nm/div.")
ax2.set(ylim=(0, 274.96), yticks=[24.96, 74.99, 124.78, 174.82, 224.86], yticklabels=[],
        ylabel="Output of outside sensor 50 nm/div.")
fig.tight_layout()
fig.savefig(HERE / "fig5_replot.png", dpi=200)
