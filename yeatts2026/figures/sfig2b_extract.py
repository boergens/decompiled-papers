#!/usr/bin/env python3
"""Digitize Supplemental Figure 2, panel b (two stacked boxes: complex-depth-profile amplitude in dB vs depth,
without / with background subtraction) of Yeatts et al. 2026.  Same image, method and conventions as
sfig2a_extract.py (axis-box fractions, colour masks per column, tier 3); see its docstring.

    python3 -I sfig2b_extract.py   -> sfig2btop.csv, sfig2bbottom.csv (+ ../work/sfig2b_overlay.png)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sfig2a_extract import extract  # noqa: E402

if __name__ == "__main__":
    extract('b', 'Depth', 'Intensity (dB)')
