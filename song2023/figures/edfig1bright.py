"""Re-plot Extended Data Fig. 1b (right) of Song et al. 2023 from edfig1bright.csv -> edfig1bright_replot.png
(report Conc +- half the 2-sigma error, which is what the printed error bars show; see CSV header)."""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from song_common import HERE, read_csv  # noqa: E402

rows = read_csv(os.path.join(HERE, "edfig1bright.csv"))
locs = ["Periphery", "Middle", "Center"]
fig, ax = plt.subplots(figsize=(2.6, 2.3))
for el, col in (("Os", "#d62728"), ("Fe", "#7f7060"), ("U", "#1f2f7a"), ("Pb", "#22aa44")):
    r = {x["location"]: x for x in rows if x["element"] == el}
    y = [float(r[l]["conc_wt"]) for l in locs]
    e = [float(r[l]["error_2sig"]) / 2 for l in locs]
    ax.errorbar(range(3), y, yerr=e, color=col, capsize=3, lw=1.2, label=el)
ax.set_xticks(range(3), locs)
ax.set_ylim(0, 33)
ax.set_yticks([0, 10, 20, 30])
ax.set_xlim(-0.4, 2.3)
ax.set_ylabel("WT.%")
ax.legend(frameon=False, fontsize=8, loc="center right")
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "edfig1bright_replot.png"), dpi=200)
