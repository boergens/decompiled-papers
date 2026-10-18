"""Redraw Figure 6d (explained variance using held-out half of neurons, PFC) from fig6d.csv.
Run from inside figures/:  python3 fig6d.py  ->  fig6d_replot.png
Same panel type as 6b: delegates to fig6b.py with PANEL = 'd'."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import sys
sys.argv = [sys.argv[0], "d"]
import fig6b
fig6b.PANEL = "d"
fig6b.main()
