"""Re-draw the classified contour maps of Figures 10 and 11 of Fu et al. 2025 from their grid CSVs
(fig10left/right.csv, fig11a-f.csv) in the key colours -> <name>_replot.png, each with its colour key and the
band limits read from the CSV header."""
import csv
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.colors import ListedColormap  # noqa: E402

HERE = Path(__file__).resolve().parent
KEY = [(0, 0, 255), (0, 93, 255), (0, 185, 255), (0, 255, 232), (0, 255, 139), (0, 255, 46),
       (46, 255, 0), (139, 255, 0), (232, 255, 0), (255, 185, 0), (255, 93, 0), (255, 0, 0)]
CODES = "0123456789ab"

for name in (sys.argv[1:] or ["fig10left", "fig10right"] + [f"fig11{p}" for p in "abcdef"]):
    rows, keyline = [], ""
    with open(HERE / f"{name}.csv") as f:
        lines = f.read().splitlines()
    keyline = next(line for line in lines if "Key values printed" in line)
    keyvals = keyline.split(":", 1)[1].strip().rstrip(".").split(", ")
    for r in csv.DictReader(line for line in lines if not line.startswith("#")):
        rows.append(r["codes"])
    codes = np.array([list(r) for r in rows])
    img = np.full(codes.shape + (3,), 255, np.uint8)
    for i, c in enumerate(CODES):
        img[codes == c] = KEY[i]
    img[codes == "#"] = (0, 0, 0)
    img[codes == "X"] = (235, 235, 235)
    fig = plt.figure(figsize=(codes.shape[1] / 150 + 1.6, codes.shape[0] / 150))
    ax = fig.add_axes([0, 0, codes.shape[1] / 150 / (codes.shape[1] / 150 + 1.6), 1])
    ax.imshow(img, interpolation="nearest")
    ax.axis("off")
    cax = fig.add_axes([0.86, 0.15, 0.03, 0.7])
    cb = fig.colorbar(plt.cm.ScalarMappable(cmap=ListedColormap(np.array(KEY) / 255),
                                            norm=plt.Normalize(0, 12)), cax=cax, ticks=range(13))
    cb.ax.set_yticklabels(list(reversed(keyvals)), fontsize=5)
    cb.ax.set_title("S, Mises", fontsize=6)
    fig.savefig(HERE / f"{name}_replot.png", dpi=150)
    plt.close(fig)
    print(name)
