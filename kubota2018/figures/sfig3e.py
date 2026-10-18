"""Re-plot Supplementary Fig. 3e from sfig3e.csv -> sfig3e_replot.png."""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sfig_common import read_csv  # noqa: E402

rows = read_csv(os.path.join(HERE, "sfig3e.csv"))
fig, ax = plt.subplots(figsize=(2.2, 2.6))
ax.axhline(0, color="0.7", lw=0.8)
for name, kw in (("cc-Kapton", dict(mfc="white", mec="k")), ("CNT/PET", dict(mfc="k", mec="k"))):
    r = [q for q in rows if q["series"] == name]
    ax.plot([float(q["eht_keV"]) for q in r], [float(q["depth_height_nm"]) for q in r], "o", ms=4, ls="none",
            label=name, **kw)
ax.set_xlim(-0.4, 10.4)
ax.set_xticks(range(0, 11, 2))
ax.set_ylim(-860, 160)
ax.set_yticks(range(-800, 1, 200))
ax.set_xlabel("EHT (keV)")
ax.set_ylabel("Depth/height (nm)")
ax.legend(frameon=False, fontsize=7, loc="lower left")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "sfig3e_replot.png"), dpi=150)
