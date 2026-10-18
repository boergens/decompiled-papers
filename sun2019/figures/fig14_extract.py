"""Fig. 14 of Sun & Gamstedt 2019 (PDF p. 10): PEEQ contour maps with triangle elements (CPE3), t_u = 85 nm,
panels a-b -> fig14a/b.csv.

Source: the lossless embedded raster of Fig. 14 (1418 x 1493 px); panels are the strips starting at rows 0 and 764
(white gap at rows 729-763). Run: python3 -I -B figures/fig14_extract.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from fe_extract_common import run  # noqa: E402

run(14, 10, (204, 58, 544, 416), [
    ("a", 0, "0.1", "+5.04e+00, +3.00e+00, +2.00e+00, +1.00e+00, +5.00e-01, +1.00e-01, +5.00e-02, +5.00e-03, +5.00e-04, +0.00e+00"),
    ("b", 764, "1.0", "+6.05e+00, +3.00e+00, +2.00e+00, +1.00e+00, +5.00e-01, +1.00e-01, +5.00e-02, +5.00e-03, +5.00e-04, +0.00e+00"),
], "simulated plastic strains in PMMA using triangle plane strain elements, at a cutting thickness t_u = 85 nm.", 85)
