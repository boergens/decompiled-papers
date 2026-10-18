#!/usr/bin/env python3
"""Re-plot Fig. 3c from fig3c.csv -> fig3c_replot.png."""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import mc  # noqa: E402

r = mc.read_csv(Path(__file__).with_name("fig3c.csv"))
fig, ax = plt.subplots(figsize=(1.3, 2.4))
for i, name in enumerate(["Post.", "Ant."]):
    for a in r:
        if a["column"] == name:
            ax.hlines(float(a["depth_um"]), i + 0.05, i + 0.95, color="k", lw=0.6)
ax.set_ylim(600, 50)
ax.set_xlim(0, 2)
ax.set_xticks([0.5, 1.5], ["Post.", "Ant."], rotation=45)
ax.set_ylabel("Distance from pial\nsurface (µm)")
for s in ("top", "right", "bottom"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(Path(__file__).with_name("fig3c_replot.png"), dpi=200)
