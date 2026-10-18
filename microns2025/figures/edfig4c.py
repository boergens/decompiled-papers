#!/usr/bin/env python3
"""Re-plot Extended Data Fig. 4c from edfig4c.csv -> edfig4c_replot.png."""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.collections import PatchCollection  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import mc  # noqa: E402

r = mc.read_csv(Path(__file__).with_name("edfig4c.csv"))
fig, ax = plt.subplots(figsize=(3.6, 3.2))
pc = PatchCollection([Rectangle((float(a["x_left"]), float(a["y_bottom"])), float(a["x_right"]) - float(a["x_left"]),
                                float(a["y_top"]) - float(a["y_bottom"])) for a in r], cmap="Blues", array=[float(a["count"]) for a in r])
pc.set_clim(0, 71)
ax.add_collection(pc)
ax.set_xlim((401.43 - 441.33) / 1.574, (477.92 - 441.33) / 1.574)
ax.set_ylim(0 - (129.46 - 126.47) / 2.2163, 30 + (59.98 - 54.75) / 2.2163)
ax.set_xlabel("separation score (µm)")
ax.set_ylabel("residual (µm)")
fig.colorbar(pc, ax=ax, label="count")
fig.tight_layout()
fig.savefig(Path(__file__).with_name("edfig4c_replot.png"), dpi=150)
