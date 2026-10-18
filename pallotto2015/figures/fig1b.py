"""Re-plot Figure 1B from fig1b.csv -> fig1b_replot.png."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pal_common import read_csv, HERE
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
rows = read_csv(os.path.join(HERE, "fig1b.csv"))
fig, ax = plt.subplots(figsize=(4.2, 3.6))
PX = 125  # plotting position of the 'perfused' category (left of the axis break)
mk = {"olfactory bulb (x)": dict(marker="x", color="k", ls=""), "retina (o)": dict(marker="o", mfc="none", color="k", ls=""),
      "cortex (square)": dict(marker="s", mfc="none", color="k", ls="")}
for s, st in mk.items():
    pts = [(float(r["osmolarity_mOsm"]) if r["category"] == "" else PX, float(r["ecs_fraction_pct"])) for r in rows
           if r["series"] == s and r["category"] in ("", "perfused")]
    ax.plot(*zip(*pts), ms=6, **st)
for s, ls in (("olfactory bulb fit (dashed)", "--"), ("cortex fit (solid)", "-")):
    pts = [(float(r["osmolarity_mOsm"]), float(r["ecs_fraction_pct"])) for r in rows if r["series"] == s]
    ax.plot(*zip(*pts), "k" + ls, lw=1.5)
ax.set_xlim(100, 500); ax.set_ylim(0, 35)
ax.set_xticks([PX, 200, 300, 400, 500]); ax.set_xticklabels(["perfused", "200", "300", "400", "500"])
ax.set_xlabel("Fix vehicle osmolarity (mOsm)"); ax.set_ylabel("ECS fraction (%)")
fig.tight_layout(); fig.savefig(os.path.join(HERE, "fig1b_replot.png"), dpi=150)
