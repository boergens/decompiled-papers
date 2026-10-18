"""Redraw the right panel (state 2) of Extended Data Figure 8 from edfig8_right_state2.csv.
Run from inside figures/:  python3 edfig8_right_state2.py  ->  edfig8_right_state2_replot.png"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
from _edfig8_common import draw
draw("edfig8_right_state2.csv", "edfig8_right_state2", ymax=60, ylabel=None)
