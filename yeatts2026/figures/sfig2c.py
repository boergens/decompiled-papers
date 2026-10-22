#!/usr/bin/env python3
"""Re-plot Supplemental Figure 2, panel c (two grey-level grids) from sfig2ctop.csv and sfig2cbottom.csv.

    python3 -I sfig2c.py   -> sfig2c_replot.png

The grids are uncalibrated 8-bit grey levels (the paper's colour bar has no numbers), shown with a grey colour
map from 0 (black) to 255 (white) and a bar in those units.
"""
import csv
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def read_grid(path):
    with open(path) as f:
        rows = [r for r in csv.reader(l for l in f if not l.startswith("#"))]
    return np.array([[float(v) for v in r[1:]] for r in rows[1:]])


def main():
    fig, axes = plt.subplots(2, 1, figsize=(8, 4.4))
    for ax, name, title in zip(axes, ("top", "bottom"), ("without background subtraction", "with background subtraction")):
        grid = read_grid(os.path.join(HERE, "sfig2c%s.csv" % name))
        im = ax.imshow(grid, cmap="gray", vmin=0, vmax=255, aspect="auto", interpolation="nearest")
        ax.set_title("Supplemental Fig. 2c, %s image: %s (%d x %d px)" % (name, title, grid.shape[0], grid.shape[1]), fontsize=8)
        ax.set_xlabel("pixel column (lateral)", fontsize=7)
        ax.set_ylabel("pixel row (depth)", fontsize=7)
        ax.tick_params(labelsize=6)
        cb = fig.colorbar(im, ax=ax, fraction=0.02, pad=0.01)
        cb.set_label("grey level (uncalibrated)", fontsize=6)
        cb.ax.tick_params(labelsize=6)
    fig.tight_layout()
    out = os.path.join(HERE, "sfig2c_replot.png")
    fig.savefig(out, dpi=150)
    print(out)


if __name__ == "__main__":
    main()
