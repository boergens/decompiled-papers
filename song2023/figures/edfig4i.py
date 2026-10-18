"""Re-plot Extended Data Fig. 4i (plot) of Song et al. 2023 from edfig4i.csv -> edfig4i_replot.png"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from song_common import HERE, read_csv  # noqa: E402

r = read_csv(os.path.join(HERE, "edfig4i.csv"))
fig, ax = plt.subplots(figsize=(2.2, 2))
for s, m in (("No OsO4", "o"), ("With OsO4", "s")):
    q = [x for x in r if x["series"] == s]
    ax.plot([float(x["duration_h"]) for x in q], [float(x["expansion_ratio"]) for x in q], "k-" + m, ms=5, lw=1.5,
            label=s.replace("OsO4", "OsO$_4$"))
ax.set_xlim(0, 110); ax.set_ylim(1.0, 2.0)
ax.set_xticks([0, 50, 100]); ax.set_yticks([1.0, 1.4, 1.8])
ax.set_xlabel("Duration (h)"); ax.set_ylabel("Expansion Ratio")
ax.legend(frameon=False, fontsize=7)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig(os.path.join(HERE, "edfig4i_replot.png"), dpi=200)
