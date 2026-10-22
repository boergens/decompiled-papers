#!/usr/bin/env python3
"""Re-plot Supplemental Figure 2, panel b, from sfig2btop.csv and sfig2bbottom.csv (same layout as panel a;
the drawing code is in sfig2a.py).

    python3 -I sfig2b.py   -> sfig2b_replot.png
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sfig2a import replot  # noqa: E402

if __name__ == "__main__":
    replot("b")
