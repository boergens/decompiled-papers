"""Digitize Figure 8E (left image) of Tegethoff & Briggman 2024 (PDF p.11): hardness dots read through the colour bar.
    python3 -I fig8e_extract.py   -> fig8e.csv (+ ../work/fig8e_overlay.png). Geometry and method: fig8_maps.py."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig8_maps import run  # noqa: E402

run("e")
