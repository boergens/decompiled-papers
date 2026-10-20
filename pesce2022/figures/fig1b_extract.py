"""Extract Fig. 1b of Pesce et al. 2022 (6 treatments on SWITCH-processed slices x 4 excitation wavelengths).

Same method and sources as fig1a_extract.py (vector copy of Fig. 1 in the Peer Review File p. 21, checked
against the published raster of main PDF p. 3); see that file's docstring.

    python3 -I -B fig1b_extract.py  -> fig1b.csv, ../work/agent_bars/fig1b_overlay.png, fig1b_overlay_published.png
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fig1a_extract import extract  # noqa: E402

if __name__ == "__main__":
    extract("b")
