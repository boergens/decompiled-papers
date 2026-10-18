"""Re-plot Fig. 4 of Sun & Gamstedt 2019 (AFM height maps) from fig4a.csv and fig4b.csv -> fig4_replot.png."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent


def load(p):
    rows = []
    with open(HERE / f"fig4{p}.csv") as f:
        for line in f:
            if line.startswith("#") or line.startswith("row,"):
                continue
            rows.append([float(v) if v else np.nan for v in line.rstrip("\n").split(",")[1:]])
    return np.array(rows)


fig, axes = plt.subplots(1, 2, figsize=(10, 3.9))
for ax, p in zip(axes, "ab"):
    z = load(p)
    im = ax.imshow(z, cmap="afmhot", vmin=-25, vmax=25, interpolation="nearest")
    ax.set_title(f"Fig. 4({p})  height (nm), image pixels; empty = masked", fontsize=8)
    ax.set_xticks([])
    ax.set_yticks([])
fig.colorbar(im, ax=axes, fraction=0.025, label="height (nm)")
fig.savefig(HERE / "fig4_replot.png", dpi=110)
