"""Re-plot Fig. 1c of Pesce et al. 2022 from fig1c.csv -> fig1c_replot.png (mean line + translucent +-SD band)."""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
PANEL = "fig1c"
YMAX, YSTEP = 35000.0, 5000.0            # printed y axis range and major tick step
COLORS = ["black", "red", "blue", "green"]   # series colours in legend order, as printed

with open(os.path.join(HERE, PANEL + ".csv")) as f:
    rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
series = []
for r in rows:
    if r["series"] not in series:
        series.append(r["series"])
fig, ax = plt.subplots(figsize=(3.4, 2.5))
for name, col in zip(series, COLORS):
    sel = [r for r in rows if r["series"] == name]
    x = [float(r["x_um"]) for r in sel]
    ax.fill_between(x, [float(r["sd_lower"]) for r in sel], [float(r["sd_upper"]) for r in sel], color=col, alpha=0.25, lw=0)
    ax.plot(x, [float(r["mean"]) for r in sel], color=col, lw=0.8, label=name)
ax.set_xlim(0, 700)
ax.set_ylim(0, YMAX)
ax.set_xticks(range(0, 701, 100))
yt = [i * YSTEP for i in range(int(round(YMAX / YSTEP)) + 1)]
ax.set_yticks(yt)
ax.set_yticklabels(["0" if v == 0 else f"{v:.1e}".replace("e+0", "e") for v in yt], fontsize=7)
ax.set_xlabel("x position (µm)")
ax.set_ylabel("Intensity")
ax.legend(fontsize=6, frameon=False)
fig.tight_layout()
fig.savefig(os.path.join(HERE, PANEL + "_replot.png"), dpi=150)
