#!/usr/bin/env python3
"""Re-plot Fig. 3g from fig3g.csv (cell colours) -> fig3g_replot.png."""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import mc  # noqa: E402

r = mc.read_csv(Path(__file__).with_name("fig3g.csv"))
img = np.zeros((80, 64, 3))
for a in r:
    img[int(a["neuron_row"]) - 1, int(a["col"]) - 1] = [int(a["R"]) / 255, int(a["G"]) / 255, int(a["B"]) / 255]
fig, ax = plt.subplots(figsize=(4, 2.6))
ax.imshow(img, aspect="auto", interpolation="nearest")
ax.set_xticks([4 * k - 0.5 for k in range(17)], [""] * 17)
ax.set_yticks([])
ax.set_ylabel("Neurons")
ax.set_xlabel("Time (16 directions x 4 bins)")
fig.tight_layout()
fig.savefig(Path(__file__).with_name("fig3g_replot.png"), dpi=150)
