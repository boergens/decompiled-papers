"""Shared code for the 6 x 6 pair-difference matrices of Fig. 4e, Fig. 4j and Extended Data Fig. 9f."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cmap_common import bar_lut, sample_cells  # noqa: E402
from digitize_common import write_csv  # noqa: E402

PAIRS = ["MeMv", "MeMd", "MeLr", "MeLm", "MeLc", "Mauthner"]  # order of the colour dots (Fig. 4f key)


def run(a, lefts, tops, cw, ch, bar, upper, lower, csv_path, header, check_png=None):
    """bar = (c0, c1, r_top, r_bot); upper/lower = (name, unit, top_value) for the upper (j > i) / lower (j < i)
    triangle; both scales run from 0 at the bottom edge of the bar to top_value at its top edge."""
    c0, c1, rt, rb = bar
    lut_u = bar_lut(a, c0, c1, rt, rb, upper[2], 0.0)
    lut_l = bar_lut(a, c0, c1, rt, rb, lower[2], 0.0)
    cu = sample_cells(a, lefts, tops, cw, ch, lut_u)
    cl = sample_cells(a, lefts, tops, cw, ch, lut_l)
    rows, pts = [], []
    for i in range(6):
        for j in range(6):
            if i == j:
                continue
            q, name, unit = (cu, upper[0], upper[1]) if j > i else (cl, lower[0], lower[1])
            v, d, c = q[(i, j)]
            rows.append((PAIRS[i], PAIRS[j], i + 1, j + 1, "upper" if j > i else "lower", name, unit, v, d))
            pts.append(c)
    write_csv(csv_path, header + ["columns: row_axon; col_axon; row; col; triangle; quantity; unit; value; rgb_dist"],
              ["row_axon", "col_axon", "row", "col", "triangle", "quantity", "unit", "value", "rgb_dist"], rows,
              fmt=["{}", "{}", "{}", "{}", "{}", "{}", "{}", "{:.3g}", "{:.1f}"])
    return rows, pts
