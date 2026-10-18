"""Digitize Figure 8B of Tegethoff & Briggman 2024 (PDF p.11). python3 -I fig8b_extract.py -> fig8b.csv"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig8_lines import run  # noqa: E402

run("b", (800, 70, 1398, 550), [85.5, 157.5, 229.5, 301.5, 373.5, 445.5], [120, 100, 80, 60, 40, 20],
    [797.5, 938.5, 1079.5, 1220.5, 1361.5], [0, 0.5, 1, 1.5, 2],
    "Figure 8B: mean sectional (blue) and transverse (red) forces for 50 nm sections from the block in panel A.")
