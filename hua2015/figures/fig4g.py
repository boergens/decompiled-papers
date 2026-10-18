"""Re-plot Fig. 4g of Hua et al. 2015 from fig4g.csv -> fig4g_replot.png
Solid lines: tier 1 (authors' .mat data); dashed: tier 2 (vector). Colours and legend texts as printed in the
paper; NB the printed legend does not match the data sets (see the header of fig4g.csv)."""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
data = {}
with open(os.path.join(HERE, "fig4g.csv")) as f:
    for r in csv.DictReader(l for l in f if not l.startswith("#")):
        if r["flag"] == "beyond_figure":
            continue
        key = (r["colour"], r["legend_label"], r["data_set"], r["style"].startswith("dashed"))
        data.setdefault(key, []).append((float(r["n_annotators"]), float(r["mean_inter_error_distance_um"])))
col = {"red": "r", "green": "lime", "blue": "b"}
fig, ax = plt.subplots(figsize=(2.8, 3.2))
for (c, lab, ds, dashed), pts in sorted(data.items(), key=lambda kv: ["red", "green", "blue"].index(kv[0][0])):
    x, y = zip(*pts)
    ax.plot(x, y, color=col[c], ls="--" if dashed else "-", lw=1,
            label=None if dashed else f"{lab}\n[data: {ds}]")
ax.set_yscale("log")
ax.set_ylim(1e1, 1e7)
ax.set_xlim(0, 25.634)       # axis box as drawn
ax.set_xticks([1, 10, 20])   # NB: the printed tick labelled 1 sits at the frame corner (0 on this scale)
ax.set_yticks([1e1, 1e3, 1e5, 1e7])
ax.set_xlabel("# annotators")
ax.set_ylabel("Mean inter-error distance (µm)")
ax.spines[["top", "right"]].set_visible(False)
ax.legend(frameon=False, fontsize=6, loc="center right")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig4g_replot.png"), dpi=150)
