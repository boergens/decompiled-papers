"""Re-plot Extended Data Fig. 4a (plot) of Song et al. 2023 from edfig4a.csv -> edfig4a_replot.png"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from song_common import HERE, read_csv  # noqa: E402

r = read_csv(os.path.join(HERE, "edfig4a.csv"))
fig, ax = plt.subplots(figsize=(2.2, 2))
ax.plot([float(x["time_h"]) for x in r], [float(x["depth_mm"]) for x in r], "k-o", ms=5, lw=1.5)
ax.set_xlim(-1, 45); ax.set_ylim(0, 2.6)
ax.set_xticks([0, 10, 20, 30, 40]); ax.set_yticks([0, 1, 2])
ax.set_xlabel("Incubation Time (h)"); ax.set_ylabel("Depth (mm)")
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig(os.path.join(HERE, "edfig4a_replot.png"), dpi=200)
