"""Extended Data Figure 6 (PDF page 46) is extracted by edfig5_extract.py, one script for the two pages that share
their panel types (face grids, feature and decoding plots). This wrapper runs it for page 46 only:
    python3 -I figures/edfig6_extract.py   ->  edfig6a_r*.png, edfig6b-e.csv, edfig6*_orig.png
"""
import os, runpy, sys

script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "edfig5_extract.py")
sys.argv = [script, "edfig6"]
runpy.run_path(script, run_name="__main__")
