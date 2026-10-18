#!/usr/bin/env python3
"""Re-plot Extended Data Fig. 2B from edfig2b.csv -> edfig2b_replot.png."""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import mc  # noqa: E402

rows = mc.read_csv(Path(__file__).with_name("edfig2b.csv"))
fig, ax = plt.subplots(figsize=(4.2, 4))
for cls in ["Excitatory", "Neurogliaform", "Martinotti", "Bipolar", "Basket"]:
    s = [r for r in rows if r["cell_class"] == cls]
    ax.scatter([float(r["n_edits"]) for r in s], [float(r["n_output_synapses"]) for r in s], s=2,
               color=s[0]["colour"], label=cls)
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(10 ** ((337.17 - 422.11) / 94.04 + 2), 10 ** ((559.44 - 422.11) / 94.04 + 2))
ax.set_ylim(10 ** (2 - (278.69 - 216.95) / 69.435), 10 ** (2 + (216.95 - 57.85) / 69.435))
ax.set_xlabel("Number of edits")
ax.set_ylabel("Number of output synapses")
ax.legend(fontsize=7, loc="upper left")
fig.tight_layout()
fig.savefig(Path(__file__).with_name("edfig2b_replot.png"), dpi=150)
