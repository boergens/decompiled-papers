"""Re-plot Figure 28 of Lubiw & Schaefer from fig28.csv -> fig28_replot.png"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "fig28.csv")) as f:
    rows = {r["object"]: r for r in csv.DictReader(l for l in f if not l.startswith("#"))}
P = lambda k: (float(rows[k]["x"]), float(rows[k]["y"]))
fig, ax = plt.subplots(figsize=(5.2, 3.6))
for k, c in rows.items():
    if k.startswith("circle"):
        ax.add_patch(plt.Circle(P(k), float(c["radius"]), fill=False, color="0.3", lw=2))
b, t, top = P("bottom point of D_u"), P("slope triangle corner (base right end)"), P("slope triangle corner (top)")
ax.fill([b[0], t[0], top[0]], [b[1], t[1], top[1]], color="#1565c0", alpha=0.15)
ax.plot([t[0], top[0]], [t[1], top[1]], color="#1565c0")
ax.plot([b[0], t[0]], [b[1], t[1]], color="#1565c0")
ax.text(0.5, -1.25, "1", color="#1565c0", ha="center")
ax.text(1.05, -0.12, "m = 2.0095100503047", color="#1565c0", va="center")
tp = P("top point of D_v")
ax.plot([b[0], tp[0] + 0.2], [b[1], tp[1] + 0.4], color="0.3", lw=1.5)
for k in rows:
    if not k.startswith(("circle", "slope")):
        ax.plot(*P(k), "o", color="0.3", ms=7)
ax.text(*P("centre u of D_u"), "  u", va="bottom")
ax.text(*P("centre v of D_v"), "  v", va="bottom")
ax.axhline(0, color="0.3", lw=1)
ax.axvline(0, color="0.3", lw=1)
ax.set_xlim(-2.05, 3.95)
ax.set_ylim(-1.3, 2.65)
ax.set_xticks(range(-2, 4))
ax.set_yticks(range(-1, 3))
ax.set_aspect("equal")
ax.grid(True, color="0.85")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig28_replot.png"), dpi=150)
