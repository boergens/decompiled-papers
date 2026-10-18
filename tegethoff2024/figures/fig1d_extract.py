"""Digitize Figure 1D of Tegethoff & Briggman 2024 (PDF p.4): hardness map, dot colours read through the colour bar.
    python3 -I fig1d_extract.py   -> fig1d.csv (+ ../work/fig1d_overlay.png). Geometry and method: fig1_maps.py."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig1_maps import run  # noqa: E402

run("d")
