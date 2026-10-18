"""Re-draw fig9a of Wei et al. 2025 from fig9a.csv.gz (shear strain per pixel) -> fig9a_replot.png"""
import csv
import gzip
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
data = {}
with gzip.open(HERE / "fig9a.csv.gz", "rt", encoding="utf-8") as f:
    for r in csv.DictReader(l for l in f if not l.startswith("#")):
        data.setdefault(r["system"], []).append((int(r["map_col"]), int(r["map_row"]), float(r["shear_strain"])))
fig, axs = plt.subplots(1, len(data), figsize=(2.2 * len(data), 3.6 if "fig9a" == "fig9a" else 2.4))
for ax, (name, pts) in zip(axs, data.items()):
    p = np.array(pts)
    img = np.full((int(p[:, 1].max()) + 1, int(p[:, 0].max()) + 1), np.nan)
    img[p[:, 1].astype(int), p[:, 0].astype(int)] = p[:, 2]
    im = ax.imshow(img, cmap="jet", vmin=0, vmax=0.4, interpolation="nearest")
    ax.set_title(name, fontsize=8)
    ax.axis("off")
fig.colorbar(im, ax=axs, shrink=0.6, label="shear strain")
fig.savefig(HERE / "fig9a_replot.png", dpi=130)
