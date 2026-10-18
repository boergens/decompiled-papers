#!/usr/bin/env python3
"""Fig. 7a-c (p. 10): connectivity matrices as dot clouds: each connection is a transparent dot at (postsynaptic soma
depth, presynaptic soma depth); darker = more connections. Each panel's dots are one embedded raster (~1070 x 985 px,
600 ppi); the axes are vector (tick labels are text): x ticks 0 ... 700 um, y ticks 0 (top) ... 700 um.
-> fig7a.csv.gz, fig7b.csv.gz, fig7c.csv.gz (gzipped: > 2 MB each).

Single dots cannot be separated (tens of thousands overlap), so each CSV is a density map at the native resolution of
the image: one row per pixel that carries ink. 'ink' is an UNCALIBRATED darkness: 1 - G/255 for the red panels a, b
(red dots lower green and blue) and 1 - R/255 for the blue panel c; 0 = white. With alpha-blended dots, ink grows
monotonically (not linearly) with the number of overlapping dots; the per-dot alpha is not stated in the figure.
Pixel -> page via the image placement (bbox), page -> um via the tick marks of each panel."""
import gzip
import csv
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import mc  # noqa: E402
import digitize_common as dc  # noqa: E402

PAN = {
    "a": dict(bbox=(72.715, 65.592, 202.555, 183.552), xt0=72.80, ch=1, what="excitatory -> excitatory"),
    "b": dict(bbox=(255.955, 65.592, 380.995, 183.552), xt0=255.02, ch=1, what="excitatory -> inhibitory"),
    "c": dict(bbox=(434.655, 64.512, 562.935, 183.432), xt0=434.74, ch=0, what="inhibitory -> excitatory"),
}
YT = [59.87, 77.12, 94.38, 111.63, 128.88, 146.14, 163.39, 180.64]
for p, d in PAN.items():
    a = dc.embedded_image(str(mc.PDF), 10, bbox_near=d["bbox"]).astype(float)
    H, W, _ = a.shape
    X = mc.LinAxis([(d["xt0"] + 17.364 * k, 100 * k) for k in range(8)])
    Y = mc.LinAxis(list(zip(YT, range(0, 701, 100))))
    b = d["bbox"]
    xs = X(b[0] + (np.arange(W) + 0.5) / W * (b[2] - b[0]))
    ys = Y(b[1] + (np.arange(H) + 0.5) / H * (b[3] - b[1]))
    ink = 1 - a[:, :, d["ch"]] / 255
    out = Path(__file__).with_name(f"fig7{p}.csv.gz")
    n = 0
    with gzip.open(out, "wt", newline="") as f:
        for line in [
            f"Fig. 7{p} (p. 10 of microns2025.pdf): connectivity matrix, {d['what']} (caption); dot cloud density map.",
            "Provenance: tier 3, embedded raster (native resolution); UNCALIBRATED ink (see fig7abc_extract.py docstring).",
            f"One pixel = {abs(X.a) * (b[2] - b[0]) / W:.3f} um (x) x {abs(Y.a) * (b[3] - b[1]) / H:.3f} um (y).",
            "Columns: px, py (image pixel, origin top left); postsyn_depth_um (x); presyn_depth_um (y, 0 = pia at the top);",
            f"ink (0-1; 1 - {'G' if d['ch'] == 1 else 'R'}/255); R, G, B. Only pixels with ink >= 0.02 are listed.",
            X.describe("x"), Y.describe("y"),
        ]:
            f.write("# " + line + "\n")
        w = csv.writer(f)
        w.writerow(["px", "py", "postsyn_depth_um", "presyn_depth_um", "ink", "R", "G", "B"])
        for yy in range(H):
            for xx in np.where(ink[yy] >= 0.02)[0]:
                c = a[yy, xx]
                w.writerow([xx, yy, f"{xs[xx]:.2f}", f"{ys[yy]:.2f}", f"{ink[yy, xx]:.3f}", int(c[0]), int(c[1]), int(c[2])])
                n += 1
    print(out, n, "pixels", f"x {xs[0]:.1f}..{xs[-1]:.1f} um, y {ys[0]:.1f}..{ys[-1]:.1f} um")
