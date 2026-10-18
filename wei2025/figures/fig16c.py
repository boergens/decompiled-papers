"""Re-plot Figure 16(c) of Wei et al. 2025 from fig16c.csv -> fig16c_replot.png
(markers from the CSV rows; dashed lines from the authors' fit equations quoted in the CSV header)."""
import csv
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
lines = (HERE / "fig16c.csv").read_text(encoding="utf-8").splitlines()
head = [l for l in lines if l.startswith("#")]
rows = list(csv.DictReader(l for l in lines if not l.startswith("#")))
title = re.search(r"panel title '([^']*)'", head[0]).group(1)
eqs = {}
for l in head:
    for s, mm, cc in re.findall(r"(F[yz]): y = (-?[\d.]+)x ([-+] [\d.]+), R2", l.replace("printed: ", "")):
        if "least-squares" not in l:
            eqs[s] = (float(mm), float(cc.replace(" ", "")))
style = {"Fx": dict(marker="s", mfc="none", color="k"), "Fy": dict(marker="^", mfc="none", color="r"),
         "Fz": dict(marker="o", color="b")}
fig, ax = plt.subplots(figsize=(4.2, 3.4))
for s in ("Fx", "Fy", "Fz"):
    x = np.array([float(r["hc_A"]) for r in rows if r["series"] == s])
    y = np.array([float(r["force_nN"]) for r in rows if r["series"] == s])
    ax.plot(x, y, ls="none", ms=5, label=s, **style[s])
    if s in eqs:
        xx = np.array([4, 25.0])
        ax.plot(xx, eqs[s][0] * xx + eqs[s][1], "--", color=style[s]["color"], lw=1)
ax.set_xlim(0, 27.5)
ax.set_ylim(*(-11, 8))
ax.set_xlabel("Indentation depth $h_c$ (Å)")
ax.set_ylabel("Force (nN)")
ax.set_title(title, fontsize=9)
ax.legend(loc="lower left", fontsize=8, frameon=False)
fig.tight_layout()
fig.savefig(HERE / "fig16c_replot.png", dpi=150)
