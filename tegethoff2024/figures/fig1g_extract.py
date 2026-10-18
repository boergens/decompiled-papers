"""Digitize Figure 1G of Tegethoff & Briggman 2024 (PDF p.4): hardness map, dot colours read through the colour bar.
    python3 -I fig1g_extract.py   -> fig1g.csv (+ ../work/fig1g_overlay.png). Geometry and method: fig1_maps.py."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig1_maps import run  # noqa: E402

run("g")
