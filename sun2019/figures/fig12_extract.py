"""Fig. 12 of Sun & Gamstedt 2019 (PDF p. 8): PEEQ contour maps, t_u = 85 nm, panels a-c -> fig12a/b/c.csv.

Source: the lossless embedded raster of Fig. 12 (1418 x 2255 px); panels are the strips starting at rows 0, 764, 1526
(white gaps between them at rows 729-763 and 1491-1525). Run: python3 -I -B figures/fig12_extract.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from fe_extract_common import run  # noqa: E402

run(12, 8, (204, 58, 544, 599), [
    ("a", 0, "0.01", "+7.24e+00, +3.00e+00, +2.00e+00, +1.00e+00, +5.00e-01, +1.00e-01, +5.00e-02, +5.00e-03, +5.00e-04, +0.00e+00"),
    ("b", 764, "0.1", "+3.00e+00, +2.00e+00, +1.00e+00, +5.00e-01, +1.00e-01, +5.00e-02, +5.00e-03, +5.00e-04, +0.00e+00"),
    ("c", 1526, "1.0", "+3.00e+00, +2.00e+00, +1.00e+00, +5.00e-01, +1.00e-01, +5.00e-02, +5.00e-03, +5.00e-04, +0.00e+00"),
], "simulated plastic strains in PMMA cutting at a cutting thickness t_u = 85 nm under different cutting speeds.", 85)
