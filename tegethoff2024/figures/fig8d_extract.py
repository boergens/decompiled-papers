"""Digitize Figure 8D of Tegethoff & Briggman 2024 (PDF p.11). python3 -I fig8d_extract.py -> fig8d.csv"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig8_lines import run  # noqa: E402

run("d", (800, 690, 1398, 1162), [697.5, 769.5, 841.5, 912.5, 984.5, 1056.5], [120, 100, 80, 60, 40, 20],
    [797.5, 863.5, 929.5, 995.5, 1061.5, 1127.5, 1193.0, 1259.5, 1324.5, 1390.5],
    [0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8],
    "Figure 8D: mean sectional (blue) and transverse (red) forces for 50 nm sections from the block in panel C.")
