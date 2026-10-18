"""Digitize Figure 8F of Tegethoff & Briggman 2024 (PDF p.11). python3 -I fig8f_extract.py -> fig8f.csv"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig8_lines import run  # noqa: E402

run("f", (804, 1280, 1398, 1754), [1289.5, 1361.5, 1433.5, 1505.5, 1577.5, 1649.5], [120, 100, 80, 60, 40, 20],
    [801.5, 882.5, 964.5, 1046.5, 1128.0, 1209.5, 1291.5, 1373.5], [0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4],
    "Figure 8F: mean sectional (blue) and transverse (red) forces for 50 nm sections from the block in panel E.")
