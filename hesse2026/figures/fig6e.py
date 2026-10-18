"""Redraw Figure 6e (decoding accuracy using held-out half of neurons, PFC) from fig6e.csv.
Run from inside figures/:  python3 fig6e.py  ->  fig6e_replot.png
Same panel type as 6c: delegates to fig6c.py with PANEL = 'e'."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import sys
sys.argv = [sys.argv[0], "e"]
import fig6c
fig6c.PANEL = "e"
fig6c.main()
