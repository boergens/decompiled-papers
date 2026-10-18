"""Redraw the left panel (state 1) of Extended Data Figure 8 from edfig8_left_state1.csv.
Run from inside figures/:  python3 edfig8_left_state1.py  ->  edfig8_left_state1_replot.png"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
from _edfig8_common import draw
draw("edfig8_left_state1.csv", "edfig8_left_state1", ymax=50, ylabel="Cell count")
