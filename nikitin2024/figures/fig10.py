"""Re-plot Figure 10 of Nikitin et al. 2024 from fig10.csv -> fig10_replot.png (same axes, ranges and series)."""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
series = {}
with open(os.path.join(HERE, "fig10.csv"), newline="") as f:
    rows = [r for r in csv.reader(l for l in f if not l.startswith("#"))]
hdr, rows = rows[0], rows[1:]
for name, x, y, lo, hi in rows:
    s = series.setdefault(name, {"x": [], "y": [], "lo": [], "hi": []})
    s["x"].append(float(x))
    s["y"].append(float(y))
    s["lo"].append(float(lo) if lo else float("nan"))
    s["hi"].append(float(hi) if hi else float("nan"))

fig, ax = plt.subplots(figsize=(6.9, 3.55), dpi=150)
frc = series["FRC"]
ax.fill_between(frc["x"], frc["lo"], frc["hi"], color="black", alpha=0.25, linewidth=0)
ax.plot(frc["x"], frc["y"], color="black", linewidth=0.8, label="FRC")
sm = series["smoothed FRC"]
ax.plot(sm["x"], sm["y"], color="red", linewidth=1.0, label="smoothed FRC")
th = series["1/2-bit threshold"]
ax.plot(th["x"], th["y"], color="tab:blue", linewidth=1.0, label="1/2-bit threshold")
ax.set_xlim(0, 1.0)
ax.set_ylim(0, 1.0)
ax.set_xlabel("Spatial/Nyquist frequency")
ax.set_ylabel("Correlation")
ax.grid(True, color="0.85")
ax.legend(loc="upper right")
ax.annotate("1.69 um", xy=(0.54, 0.21), xytext=(0.63, 0.43), arrowprops=dict(arrowstyle="->", color="black"))
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig10_replot.png"))
print("wrote fig10_replot.png")
