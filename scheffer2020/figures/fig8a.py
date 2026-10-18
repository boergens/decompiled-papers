#!/usr/bin/env python3
"""Re-plot scheffer2020 Figure 8A from fig8a.csv: bubble matrix of the 35 regions; dot radius drawn from r_px
(source-image pixels; one cell = ~29.9 px), so dot sizes match the original; the values are in the CSV."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

HERE = Path(__file__).resolve().parent
LABELS = ["AB(L)", "AB(R)", "AL(R)", "AME(R)", "AOTU(R)", "ATL(R)", "AVLP(R)", "BU(R)", "CA(R)", "CRE(R)", "EB",
          "EPA(R)", "FB", "GOR(R)", "IB", "ICL(R)", "LAL(R)", "LH(R)", "NO", "PB", "PED(R)", "PLP(R)", "PVLP(R)",
          "SCL(R)", "SIP(R)", "SLP(R)", "SMP(R)", "SPS(R)", "VES(R)", "WED(R)", "a'L(R)", "aL(R)", "b'L(R)", "bL(R)",
          "gL(R)"]
rows = list(csv.DictReader(l for l in open(HERE / "fig8a.csv") if not l.startswith("#")))
CELL = 29.9
fig, ax = plt.subplots(figsize=(7, 7))
for r in rows:
    x = LABELS.index(r["col_region"])
    y = LABELS.index(r["row_region"])
    ax.add_patch(Circle((x, y), float(r["r_px"]) / CELL, color="tab:blue"))
ax.set_xlim(-0.5, 34.5)
ax.set_ylim(34.5, -0.5)
ax.set_aspect("equal")
ax.set_xticks(range(35))
ax.set_xticklabels(LABELS, rotation=90, fontsize=7)
ax.set_yticks(range(35))
ax.set_yticklabels(LABELS, fontsize=7)
ax.grid(True, color="0.9")
ax.set_axisbelow(True)
ax.text(33.5, 0.5, "(A)", ha="right", va="top", fontsize=12)
fig.tight_layout()
fig.savefig(HERE / "fig8a_replot.png", dpi=150)
