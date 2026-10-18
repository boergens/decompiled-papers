"""Re-plot Extended Data Fig. 1b (left) of Song et al. 2023 from edfig1bleft.csv -> edfig1bleft_replot.png"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from song_common import HERE, read_csv  # noqa: E402

rows = read_csv(os.path.join(HERE, "edfig1bleft.csv"))
fig, ax = plt.subplots(figsize=(3.2, 2.4))
for key, col, lab in (("uCT", "r", "µCT"), ("SEM", "tab:blue", "SEM"), ("EDS", "tab:green", "EDS")):
    r = [x for x in rows if x["series"].startswith(key)]
    ax.plot([float(x["x_um"]) for x in r], [float(x["y"]) for x in r], color=col, lw=1, label=lab)
for x in rows:
    if x["series"] == "dashed_line":
        ax.axvline(float(x["x_um"]), color="k", ls="--", lw=0.6)
ax.set_xlim(-20, 1800)
ax.set_ylim(-2.9, 3.0)
ax.set_xticks([0, 800, 1600])
ax.set_yticks([-2, 0, 2])
ax.set_xlabel("Location (µm)")
ax.set_ylabel("Os intensity (a.u.)")
ax.legend(frameon=False, fontsize=7, loc="upper center")
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "edfig1bleft_replot.png"), dpi=200)
