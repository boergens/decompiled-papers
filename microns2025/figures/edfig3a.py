#!/usr/bin/env python3
"""Re-plot Extended Data Fig. 3A from edfig3a.csv (broken y axis) -> edfig3a_replot.png."""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import mc  # noqa: E402

rows = mc.read_csv(Path(__file__).with_name("edfig3a.csv"))
cats = sorted({int(r["neurons_per_id"]) for r in rows})
pos = {c: i for i, c in enumerate(cats)}
fig, (a1, a2) = plt.subplots(2, 1, sharex=True, figsize=(7, 4), gridspec_kw=dict(height_ratios=[80, 93]))
for date, col, off in [("9/30/20", "#296790", -0.2), ("4/4/23", "#65b7ce", 0.2)]:
    s = [r for r in rows if r["date"] == date]
    for ax in (a1, a2):
        ax.bar([pos[int(r["neurons_per_id"])] + off for r in s], [float(r["bar_height"]) for r in s], width=0.3,
               color=col, label=date if ax is a1 else None)
    for r in s:
        v = float(r["bar_height"])
        (a1 if v > 200 else a2).text(pos[int(r["neurons_per_id"])] + off, v + (60 if v > 200 else 3), r["printed_label"],
                                     ha="center", fontsize=5)
a1.set_ylim(1000 - (162.97 - 150.12) / 16.06 * 1000, 6000)
a2.set_ylim(0, 200)
a1.spines["bottom"].set_visible(False)
a2.spines["top"].set_visible(False)
a1.tick_params(bottom=False)
a2.set_xticks(range(len(cats)), [str(c) for c in cats])
a2.set_xlabel("# Neurons per ID")
fig.supylabel("# Unique Root IDs")
a1.legend(fontsize=7)
fig.tight_layout()
fig.savefig(Path(__file__).with_name("edfig3a_replot.png"), dpi=150)
