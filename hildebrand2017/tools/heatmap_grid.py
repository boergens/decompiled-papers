"""Grid CSVs for the pair-difference heatmaps (Fig. 4g,h; Extended Data Fig. 9h,j,k) of hildebrand2017.

One CSV row per image pixel row of the heatmap, one value column per image pixel column (header = the slice number
at that column's centre). Each pixel's colour is mapped to the nearest colour of the printed colour bar; black
pixels (no reconstruction data) and pixels far from every key colour are left empty.
"""
import csv
import gzip
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cmap_common import bar_lut, lookup  # noqa: E402


def extract(a, r0, r1, c0, c1, bar, vmax, fx, n_pairs, pair_names, out_path, header, ndp=2, maxdist=45):
    """a: RGB image; heatmap occupies rows r0..r1 and columns c0..c1 (inclusive); bar = (bc0, bc1, br0, br1)
    colour bar (vmax at the top edge, 0 at the bottom edge); fx(col) -> slice. Writes out_path (.csv or .csv.gz).
    Returns the value grid (NaN = empty)."""
    lut = bar_lut(a, bar[0], bar[1], bar[2], bar[3], vmax, 0.0)
    sub = a[r0:r1 + 1, c0:c1 + 1].astype(float)
    val, dist, _ = lookup(sub, lut)
    blackpx = sub.max(2) < 45
    # Thin black (no-data) stripes blend with neighbouring colours at this resolution, giving darkened key colours.
    # For those, match the colour direction (chromaticity) instead and accept if it is close to a key colour.
    far = (dist > maxdist) & ~blackpx
    lrgb, lval = lut
    ln = lrgb / np.linalg.norm(lrgb, axis=1, keepdims=True)
    fp = sub[far]
    fn = fp / np.maximum(np.linalg.norm(fp, axis=1, keepdims=True), 1e-6)
    cos = fn @ ln.T
    k = cos.argmax(1)
    ang = np.arccos(np.clip(cos[np.arange(len(k)), k], -1, 1))
    alpha = np.linalg.norm(fp, axis=1) / np.linalg.norm(lrgb[k], axis=1)
    ok = (ang < 0.12) & (alpha > 0.35)
    v2 = np.where(ok, lval[k], np.nan)
    val[far] = v2
    val[blackpx] = np.nan
    extract.stats = dict(darkened_matched=int(ok.sum()), unmatched=int((~ok).sum()), black=int(blackpx.sum()))
    st = extract.stats
    header = header + [f"pixels: {val.size} in the grid, {st['black']} black (no data, left empty), {st['darkened_matched']} darkened "
                       f"by black stripes and matched on colour direction, {st['unmatched']} not matched (left empty)."]
    rpp = (r1 + 1 - r0) / n_pairs
    opener = gzip.open if str(out_path).endswith(".gz") else open
    with opener(out_path, "wt", newline="") as f:
        for h in header:
            f.write("# " + h + "\n")
        w = csv.writer(f)
        cols = [f"{fx(c):.0f}" for c in range(c0, c1 + 1)]
        w.writerow(["px_row", "pair_index", "pair"] + cols)
        for i in range(sub.shape[0]):
            k = min(n_pairs - 1, int((i + 0.5) / rpp))
            w.writerow([r0 + i, k + 1, pair_names[k] if pair_names else ""] +
                       ["" if v != v else f"{v:.{ndp}f}" for v in val[i]])
    return val, float(np.nanmean(dist[~blackpx]))


def read_grid(path):
    """Read a grid CSV back: returns slices (array), pair_index per row, values (2D, NaN = empty)."""
    opener = gzip.open if str(path).endswith(".gz") else open
    with opener(path, "rt") as f:
        rows = [r for r in csv.reader(line for line in f if not line.startswith("#"))]
    head, body = rows[0], rows[1:]
    slices = np.array([float(x) for x in head[3:]])
    pidx = np.array([int(r[1]) for r in body])
    vals = np.array([[float(x) if x else np.nan for x in r[3:]] for r in body])
    return slices, pidx, vals
