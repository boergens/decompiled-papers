#!/usr/bin/env python3
"""Re-plot Fig. 6f from fig6f.csv -> fig6f_replot.png."""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import mc  # noqa: E402

r = mc.read_csv(Path(__file__).with_name("fig6f.csv"))
fig, ax = plt.subplots(figsize=(3.3, 2.4))
for cls in ["Excitatory", "Neurogliaform", "Martinotti", "Bipolar", "Basket"]:
    s = [a for a in r if a["cell_class"] == cls]
    ax.scatter([float(a["n_output_synapses"]) for a in s], [float(a["pct_with_postsynaptic_soma"]) for a in s],
               s=1.5, color=s[0]["colour"], label=cls)
ax.set_xscale("log")
ax.set_xlim(10 ** ((396.5 - 441.83) / 42.415 + 2), 10 ** ((540 - 441.83) / 42.415 + 2))
ax.set_ylim(55, 101)
ax.set_xlabel("Number of output synapses")
ax.set_ylabel("Percentage with post-\nsynaptic soma")
ax.legend(fontsize=6, loc="upper left", markerscale=3)
fig.tight_layout()
fig.savefig(Path(__file__).with_name("fig6f_replot.png"), dpi=150)
