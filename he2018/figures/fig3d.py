"""Re-plot Figure 3d of He et al. 2018 from fig3d.csv -> fig3d_replot.png"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "fig3d.csv")) as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
fig, ax = plt.subplots(figsize=(5, 3))
for name, col in (("top sub-slice", "tab:green"), ("bottom sub-slice", "red")):
    r = [q for q in rows if q["series"] == name]
    x = np.array([float(q["distance_um"]) for q in r])
    y = np.array([float(q["lead_atoms_1e3_per_voxel"]) for q in r])
    gap = np.where(np.diff(x) > 0.02)[0] + 1          # break the line where columns are missing
    ax.plot(np.insert(x, gap, np.nan), np.insert(y, gap, np.nan), color=col, lw=1, label=name)
ax.set_xlim(-0.5, 4.5)
ax.set_ylim(-2, 6)
ax.set_xticks(np.arange(-0.5, 4.6, 1))
ax.set_yticks(np.arange(-2, 6.1, 2))
ax.grid(color="0.85")
ax.set_xlabel("Distance (µm)")
ax.set_ylabel("Number of lead\natoms (10$^3$ /voxel)")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.25), ncol=2, frameon=False)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig3d_replot.png"), dpi=150)
