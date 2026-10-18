"""Digitize Figure 5E of Tegethoff & Briggman 2024 (PDF p.7): mean resultant force vs block hardness.
    python3 -I fig5e_extract.py -> fig5e.csv (+ ../work/fig5e_overlay.png); code in fig5ef_common.py."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig5ef_common import *  # noqa: E402,F403

fy, ry, sy = fit_axis([1763.5, 1859.5, 1955.5, 2051.0, 2146.5], [70, 60, 50, 40, 30])
fx, rx, sx = fit_axis([107.5, 228.5, 350.5, 471.5, 593.5, 714.5, 836.0], [12, 13, 14, 15, 16, 17, 18])
# (series, marker, x_px, y_px by eye in the native image, note)
APPROX = [
    ("MH Epon", "filled", 144, 1858, ""), ("MH Epon", "open", 147, 1959, ""),
    ("Spurr's", "filled", 216.5, 1971, ""), ("Spurr's", "open", 220, 2055.5, ""),
    ("Durcupan", "filled", 265.5, 1984, ""), ("Durcupan", "open", 269, 2031.5, ""),
    ("M Epon", "filled", 301.5, 1863, ""), ("M Epon", "open", 304.5, 1998, ""),
    ("LX 112", "filled", 326, 1843.5, ""), ("LX 112", "open", 329, 1902, ""),
    ("H Epon", "filled", 423, 1858, ""),
    ("VH Epon", "filled", 799.7, 1630.7, "marked with an asterisk (~100 nm sections, per the caption)"),
]
extract("e", APPROX, fx, fy, sy, sx, "mN/mm", [
    "Tegethoff & Briggman 2024 Front Neurosci 18:1286991, Figure 5E: mean resultant forces (y axis 'F_R' with an overbar,",
    "  mN/mm) plotted versus block hardness for 50 nm (filled circles) and 35 nm (open squares) sections.",
    f"Axes calibrated on the ticks 30-70 mN/mm (labels 30-90; max residual {ry:.3f}) and 12-18 HV (max residual {rx:.4f}).",
    "A grey asterisk is printed above the VH Epon marker.",
], "mean_FR_mN_per_mm")
