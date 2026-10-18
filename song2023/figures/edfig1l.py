"""Re-plot Extended Data Fig. 1l of Song et al. 2023 from edfig1l.csv -> edfig1l_replot.png"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from song_common import HERE, read_csv  # noqa: E402

rows = read_csv(os.path.join(HERE, "edfig1l.csv"))
fig, ax = plt.subplots(figsize=(3.4, 2.4))
for series, col, dx in (("This protocol (Fig.1b bottom row, Os24)", "b", 0.02), ("This protocol (m, Os3)", "m", 0),
                        ("Hua (Fig.1b upper row)", "k", -0.02)):
    r = [x for x in rows if x["series"] == series]
    ax.errorbar([i + dx for i in range(3)], [float(x["mean"]) for x in r], yerr=[float(x["sd"]) for x in r],
                fmt="-o", mfc="none", color=col, capsize=2, lw=1, ms=4, label=series)
ax.set_xticks(range(3), ["Periphery", "Intermediate", "Core"])
ax.set_xlim(-0.3, 2.2)
ax.set_ylim(0, 100)
ax.set_yticks([0, 50, 100])
ax.set_ylabel("Intensity difference\nmembrane vs. background")
ax.legend(frameon=False, fontsize=5, loc="lower left")
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "edfig1l_replot.png"), dpi=200)
