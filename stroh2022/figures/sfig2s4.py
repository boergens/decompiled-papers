"""Re-plot Figure 2—figure supplement 4 of Ströh et al. 2022 from sfig2s4.csv -> sfig2s4_replot.png"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from replot_common import read, plt, HERE, f  # noqa: E402

rows = read("sfig2s4.csv")
names = list(dict.fromkeys(r["parameter"] for r in rows))
fig, ax = plt.subplots(figsize=(10, 3.4))
for i, n in enumerate(names):
    r = [q for q in rows if q["parameter"] == n]
    mean = [f(q["value"]) for q in r if q["kind"] == "bar (mean)"][0]
    top = [f(q["value"]) for q in r if q["kind"] == "error bar top"][0]
    dots = [f(q["value"]) for q in r if q["kind"] == "dot"]
    ax.bar(i + 0.15, mean, width=0.15, color="k")
    ax.plot([i + 0.15, i + 0.15], [mean, top], color="k", lw=2)
    ax.plot([i + 0.11, i + 0.19], [top, top], color="k", lw=2)
    ax.scatter([i - 0.1] * len(dots), dots, color="0.8", s=40)
ax.set_xticks(range(len(names)))
ax.set_xticklabels([f'{n} in\n{[q["unit"] for q in rows if q["parameter"] == n][0]}' for n in names], fontsize=8)
ax.set_ylim(0, 10); ax.set_yticks([0, 5, 10]); ax.set_xlim(-0.6, len(names) - 0.5)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "sfig2s4_replot.png"), dpi=150)
