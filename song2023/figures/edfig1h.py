"""Re-plot Extended Data Fig. 1h (right) of Song et al. 2023 from edfig1h.csv -> edfig1h_replot.png"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from song_common import HERE, read_csv  # noqa: E402

rows = read_csv(os.path.join(HERE, "edfig1h.csv"))
col = {"no": "#1a9a4a", "weak": "#f5e52a", "strong": "#e02020"}
conds = [("6", "3"), ("17", "3"), ("17", "6")]
fig, ax = plt.subplots(figsize=(2.4, 2.4))
xt, xl = [], []
for g, (pg, os_) in enumerate(conds):
    for p in (1, 2, 3):
        x = g * 4 + p
        for r in rows:
            if r["pg_h"] == pg and r["oso4_h"] == os_ and int(r["position"]) == p:
                lo, hi = float(r["bottom_pct"]), float(r["top_pct"])
                ax.bar(x, hi - lo, bottom=lo, color=col[r["gradient"]], edgecolor="k", width=0.85)
        ax.text(x, 103, str(p), ha="center", fontsize=7)
    xt.append(g * 4 + 2); xl.append(f"Pg {pg}\nOsO4 {os_}")
ax.set_xticks(xt, xl, fontsize=7)
ax.set_ylim(0, 100)
ax.set_yticks([0, 50, 100])
ax.set_ylabel("ratio (%)")
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "edfig1h_replot.png"), dpi=200)
