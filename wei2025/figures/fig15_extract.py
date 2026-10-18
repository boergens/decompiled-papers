"""Fig. 15 of Wei et al. 2025 (PDF p. 12): shear strain of atoms of the six quartz indenters at hc = 4 Å, sliding distance 44 Å,
mapped through the printed colour key (0 to 0.4).

Source: embedded 300 ppi JPEG of Figure 15 (2100 x 589 px). Writes figures/fig15.csv.gz (long format, one row per
coloured pixel) and work/fig15_check.png (the six indenters re-rendered from the values, for comparison).
    python3 -I -B figures/fig15_extract.py
"""
import csv
import gzip
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
from digitize_common import embedded_image  # noqa: E402
from hue_key import key_profile, map_values, hue_deg  # noqa: E402

a = embedded_image(str(ROOT / "source" / "wei2025.pdf"), 12, bbox_near=(45.5, 561.1, 549.5, 702.4))
SYSTEMS = ["Pyramid-0°", "Pyramid-45°", "R = 10 Å", "R = 14.5 Å", "R = 20 Å", "R = 25 Å"]
# colour key: bar at rows 35-59, columns 758-894 of the image, labelled 0 (left) and 0.4 (right)
KEY = (35, 59, 758, 894)
kh, kv = key_profile(a, *KEY, 0.0, 0.4)
# the six indenters: saturated pixels in rows 0-460 (the key area blanked), split into column groups
_, s, v = hue_deg(a)
sat = (s / np.maximum(v, 1e-9) > 0.35) & (v > 0.25)
sat[:KEY[1] + 6, KEY[2] - 6:KEY[3] + 6] = False
band = sat[0:460]
colsum = band.sum(0)
cols = np.where(colsum > 3)[0]
groups = [g for g in np.split(cols, np.where(np.diff(cols) > 4)[0] + 1) if len(g) > 100]
assert len(groups) == 6, [(g[0], g[-1]) for g in groups]
boxes = []
for g in groups:
    c0, c1 = g[0], g[-1]
    rows = np.where(band[:, c0:c1 + 1].sum(1) > 3)[0]
    boxes.append((rows[0], rows[-1], c0, c1))

out_rows, check = [], np.full(a.shape[:2], np.nan)
for name, (r0, r1, c0, c1) in zip(SYSTEMS, boxes):
    val = map_values(a[r0:r1 + 1, c0:c1 + 1], kh, kv)
    check[r0:r1 + 1, c0:c1 + 1] = val
    rr, cc = np.where(~np.isnan(val))
    for y, x in zip(rr, cc):
        out_rows.append((name, int(x), int(y), round(float(val[y, x]), 3)))
    print(name, "box rows", r0, r1, "cols", c0, c1, "mapped", len(rr), "of", val.size)

with gzip.open(HERE / "fig15.csv.gz", "wt", newline="", encoding="utf-8") as f:
    for h in [
        "Wei et al. 2025, Figure 15: shear strain of the atoms of the six quartz indenters at hc = 4 Å and sliding distance 44 Å, side views (y right, z up).",
        "Columns: system (label below each indenter); map_col, map_row = pixel within that system's map box",
        "  (0,0 = top left of the box; box origins in the embedded 2100 x 589 px image of Figure 15: "
        + "; ".join(f"{n}: col {b[2]}, row {b[0]}, size {b[3] - b[2] + 1} x {b[1] - b[0] + 1} px" for n, b in zip(SYSTEMS, boxes)) + ");",
        "  1 px = 1/300 inch on the page; shear_strain = von Mises shear strain",
        "  (dimensionless) read through the printed colour key 0 (blue) .. 0.4 (red).",
        "Provenance: tier 3, digitized from the embedded 300 ppi JPEG (no vector data) by fig15_extract.py. Calibrated colour map:",
        "  the key's hue profile (centre rows, ends trimmed 4 px) is sampled per column and mapped linearly 0 -> 0.4 across the bar;",
        "  each pixel's value is the key value of the nearest hue (the atoms are shaded spheres, so brightness is not used).",
        "  Pixels without a usable hue (white gaps between atoms, dark outlines, saturation < 0.35 or brightness < 0.25) are left out.",
        "Uncertainty: the value resolution of the key is about 0.003 per key column; JPEG chroma subsampling and sphere shading",
        "  blur colours over 1-2 px, so single pixels can be off by several key steps, mostly at atom edges. Values at the ends",
        "  (0 and 0.4) include everything below 0 / above 0.4 that the renderer clamped to the end colours (strains > 0.4 show as 0.4).",
        "This is a picture of atoms, not a field: each value belongs to the atom drawn at that pixel (topmost atom in the view).",
    ]:
        f.write("# " + h + "\n")
    w = csv.writer(f)
    w.writerow(["system", "map_col", "map_row", "shear_strain"])
    w.writerows(out_rows)

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
(ROOT / "work").mkdir(exist_ok=True)
fig, ax = plt.subplots(1, 2, figsize=(14, 2.6))
ax[0].imshow(a)
ax[0].set_title("source (Figure 15)")
from matplotlib.colors import ListedColormap  # noqa: E402
r_mid = (KEY[0] + KEY[1]) // 2
keycm = ListedColormap(a[r_mid, KEY[2] + 4:KEY[3] - 3] / 255.0)
ax[1].imshow(check, cmap=keycm, vmin=0, vmax=0.4)
ax[1].set_title("values re-drawn with the printed key's colours")
for x in ax:
    x.axis("off")
fig.tight_layout()
fig.savefig(ROOT / "work" / "fig15_check.png", dpi=110)
