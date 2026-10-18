"""Re-plot zhangk2020 Fig. 4b from fig4b.csv -> fig4b_replot.png (nm, arbitrary origin)."""
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


r = read("fig4b.csv")
fig, ax = plt.subplots(figsize=(4.0, 2.9))
ax.plot([float(q["x_nm"]) for q in r], [float(q["z_nm"]) for q in r], color="red", lw=1.2)
ax.set(xlim=(0, 200), ylim=(0, 20), xticks=[50, 100, 150], yticks=[5, 10, 15], xticklabels=[], yticklabels=[],
       xlabel="X-position 50 nm/div.", ylabel="Z-position 5 nm/div.")
fig.tight_layout()
fig.savefig(HERE / "fig4b_replot.png", dpi=200)
