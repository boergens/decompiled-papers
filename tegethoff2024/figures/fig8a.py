"""Re-plot Figure 8A (left image) of Tegethoff & Briggman 2024 from fig8a.csv -> fig8a_replot.png"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig8_mapplot import plot  # noqa: E402

plot("a")
