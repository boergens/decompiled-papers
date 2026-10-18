"""Re-plot Figure 2a of Ströh et al. 2022 from fig2a.csv -> fig2a_replot.png"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
lines = [l for l in open(os.path.join(HERE, "fig2a.csv")) if not l.startswith("#")]
xs = [float(v) for v in lines[0].strip().split(",")[1:]]
ys, grid = [], []
for l in lines[1:]:
    p = l.rstrip("\n").split(",")
    ys.append(float(p[0]))
    grid.append([float(v) if v else np.nan for v in p[1:]])
fig, ax = plt.subplots(figsize=(3.4, 2.8))
im = ax.imshow(np.array(grid), extent=(0, 1200, 0, 1200), origin="upper", cmap="viridis", vmin=0.5 - (1 - 0.5) * 7.25 / 61.75, vmax=1)
ax.set_xticks([0, 400, 800, 1200]); ax.set_yticks([0, 400, 800, 1200])
ax.set_xlabel("Time (min)"); ax.set_ylabel("Depth (μm)")
cb = fig.colorbar(im, ax=ax, ticks=[0.5, 1])
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig2a_replot.png"), dpi=150)
