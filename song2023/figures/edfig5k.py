"""Re-plot Extended Data Fig. 5k of Song et al. 2023 from edfig5k.csv -> edfig5k_replot.png (intensity_axis)"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from song_common import HERE, read_csv  # noqa: E402

r = read_csv(os.path.join(HERE, "edfig5k.csv"))
fig, ax = plt.subplots(figsize=(2.2, 2))
for s, c in (("Osvi + FeCN", "r"), ("Brain FeCN", "#10a040")):
    q = [x for x in r if x["series"] == s]
    ax.plot([float(x["raman_shift_cm1"]) for x in q], [float(x["intensity_axis"]) for x in q], color=c, lw=1.2, label=s)
ax.axvline(880, color="k", ls="--", lw=1, ymax=0.55)
ax.set_xlim(750, 1010); ax.set_ylim(0, 2); ax.set_xticks([800, 900, 1000]); ax.set_yticks([0, 1, 2])
ax.legend(frameon=False, fontsize=7)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
fig.tight_layout(); fig.savefig(os.path.join(HERE, "edfig5k_replot.png"), dpi=200)
