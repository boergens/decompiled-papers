"""Fig. 13 of Sun & Gamstedt 2019 (PDF p. 9): PEEQ contour maps, t_u = 200 nm, panels a-c -> fig13a/b/c.csv.

Source: the lossless embedded raster of Fig. 13 (1418 x 2254 px); panels are the strips starting at rows 0, 764, 1525
(white gaps at rows 729-763 and 1490-1524). Run: python3 -I -B figures/fig13_extract.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from fe_extract_common import run  # noqa: E402

run(13, 9, (204, 58, 544, 599), [
    ("a", 0, "0.01", "+5.32e+00, +3.00e+00, +2.00e+00, +1.00e+00, +5.00e-01, +1.00e-01, +5.00e-02, +5.00e-03, +5.00e-04, +0.00e+00"),
    ("b", 764, "0.1", "+3.00e+00, +2.00e+00, +1.00e+00, +5.00e-01, +1.00e-01, +5.00e-02, +5.00e-03, +5.00e-04, +0.00e+00"),
    ("c", 1525, "1.0", "+3.68e+00, +3.00e+00, +2.00e+00, +1.00e+00, +5.00e-01, +1.00e-01, +5.00e-02, +5.00e-03, +5.00e-04, +0.00e+00"),
], "simulated plastic strains in PMMA cutting at a cutting thickness t_u = 200 nm under different cutting speeds.", 200)
