"""Re-plot Extended Data Fig. 1k of Song et al. 2023 from edfig1k.csv -> edfig1k_replot.png (plotted = yes columns)"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from song_common import HERE, read_csv  # noqa: E402

rows = [r for r in read_csv(os.path.join(HERE, "edfig1k.csv")) if r["plotted"] == "yes" and r["excluded"] == "no"]
style = {"95%": dict(color="#e02020", label="95%, 4°C"), "100% 4 deg": dict(color="#7f7fcf", label="100%, 4°C"),
         "100% RT": dict(color="k", mfc="g", label="100%, RT")}
fig, ax = plt.subplots(figsize=(2.6, 2.4))
done = set()
for col in dict.fromkeys(r["column"] for r in rows):
    r = [x for x in rows if x["column"] == col]
    st = dict(style[r[0]["group"]])
    if r[0]["group"] in done:
        st.pop("label")
    done.add(r[0]["group"])
    ax.plot([float(x["time_days"]) for x in r], [float(x["fluidity_au"]) for x in r], "-o", ms=2, lw=1.3, **st)
ax.set_xlim(0, 10.5)
ax.set_ylim(0, 4)
ax.set_xticks(range(0, 11, 2))
ax.set_xlabel("Time (days)")
ax.set_ylabel("Resin fluidity (a.u.)")
ax.legend(frameon=False, fontsize=7)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "edfig1k_replot.png"), dpi=200)
