"""Re-plot Fig. 14 of Sun & Gamstedt 2019 (PEEQ band maps, t_u = 85 nm) from fig14<panel>.csv -> fig14_replot.png.

Each pixel is drawn in its band's key colour (bands from the CSV header: 0 blue ... 7 red); knife grey, background
white, annotation areas light grey, unclassified pixels black.
"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
PANELS = "a,b".split(",")
KEY = {"0": (0, 0, 255), "1": (0, 145, 255), "2": (0, 255, 218), "3": (0, 255, 72), "4": (72, 255, 0),
       "5": (218, 255, 0), "6": (255, 145, 0), "7": (255, 0, 0), ".": (255, 255, 255), "K": (124, 124, 124),
       "A": (235, 235, 235), "#": (0, 0, 0)}
LABELS = ["0-5e-4", "5e-4-5e-3", "5e-3-0.05", "0.05-0.1", "0.1-0.5", "0.5-1", "1-2", "2-3"]
fig, axes = plt.subplots(len(PANELS), 1, figsize=(7, 3.6 * len(PANELS)))
for ax, p in zip(np.atleast_1d(axes), PANELS):
    with open(HERE / f"fig14{p}.csv") as f:
        rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
    codes = np.array([list(r["codes"]) for r in rows])
    img = np.zeros(codes.shape + (3,), np.uint8)
    for k, c in KEY.items():
        img[codes == k] = c
    ax.imshow(img, interpolation="nearest")
    ax.set_title(f"Fig. 14({p})  PEEQ bands (image pixels)", fontsize=9)
    ax.set_xticks([])
    ax.set_yticks([])
handles = [plt.Rectangle((0, 0), 1, 1, color=np.array(KEY[str(i)]) / 255) for i in range(8)]
fig.legend(handles, LABELS, loc="lower center", ncol=4, fontsize=8, title="PEEQ band")
fig.tight_layout(rect=(0, 0.06, 1, 1))
fig.savefig(HERE / "fig14_replot.png", dpi=110)
