"""Digitize Figure 5F of Tegethoff & Briggman 2024 (PDF p.7): mean of the per-cut standard deviation of the sectional
force vs block hardness.
    python3 -I fig5f_extract.py -> fig5f.csv (+ ../work/fig5f_overlay.png); code in fig5ef_common.py."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig5ef_common import *  # noqa: E402,F403

fy, ry, sy = fit_axis([1571.5, 1667.5, 1763.5, 1859.5, 1955.0, 2050.5, 2146.5], [30, 25, 20, 15, 10, 5, 0])
fx, rx, sx = fit_axis([1009, 1130.5, 1251.5, 1373.5, 1494.5, 1616.5, 1737.5], [12, 13, 14, 15, 16, 17, 18])
HID = "open square mostly hidden behind the filled circle; position estimated from its visible edge"
APPROX = [
    ("MH Epon", "filled", 1045, 2127.5, ""), ("MH Epon", "open", 1048, 1893, ""),
    ("Spurr's", "filled", 1117.5, 2129.5, ""), ("Spurr's", "open", 1122, 2128.5, HID),
    ("Durcupan", "filled", 1166.5, 2127.5, ""), ("Durcupan", "open", 1170, 2068.5, ""),
    ("M Epon", "filled", 1203, 2128.5, ""), ("M Epon", "open", 1206, 1832.5, ""),
    ("LX 112", "filled", 1227.5, 2129, ""), ("LX 112", "open", 1231, 2128.5, HID),
    ("H Epon", "filled", 1324.5, 1807.5, ""),
    ("VH Epon", "filled", 1701.5, 2126, ""),
]
extract("f", APPROX, fx, fy, sy, sx, "mN/mm", [
    "Tegethoff & Briggman 2024 Front Neurosci 18:1286991, Figure 5F: mean of the standard deviation of sectional force",
    "  (y axis 'deltaF_S (mN/mm)') plotted versus block hardness for 50 nm (filled circles) and 35 nm (open squares).",
    f"Axes calibrated on the ticks 0-30 mN/mm (max residual {ry:.3f}) and 13-18 HV plus the y axis line as 12 HV",
    f"  (max residual {rx:.4f}). Markers near 1 mN/mm overlap each other; their bars, if any, are hidden.",
], "mean_dFS_mN_per_mm")
