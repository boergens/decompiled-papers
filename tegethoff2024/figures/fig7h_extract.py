"""Digitize Figure 7H of Tegethoff & Briggman 2024 (PDF p.10), a beeswarm plot, as per-row swarm profiles.
    python3 -I fig7h_extract.py -> fig7h.csv (+ ../work/fig7h_overlay.png). Method: swarm_common.py run_ticks()."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from swarm_common import *  # noqa: E402,F403

run_ticks("fig7h", 10, (908, 2110, 1600, 2656), [2659.5, 2601, 2542.5, 2484, 2425.5, 2367, 2308.5, 2250, 2191.5, 2133], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
          [932.5, 960.5, 988, 1016, 1044, 1071.5, 1099.5, 1155, 1183, 1210.5, 1238.5, 1266.5, 1294, 1322, 1377.5, 1405.5, 1433, 1461, 1489, 1516.5, 1544.5],
          [(s, str(v)) for s in FIG7_NAMES for v in range(3, 10)],
          "Figure 7H: standard deviation of the transverse force (y axis 'deltaF_T', mN/mm) from different resins (colour-coded) cut at 35 nm and 1.2 mm/s, plotted versus knife clearance angle (deg).", "dFT_mN_per_mm", "mN/mm", FIG7_NAMES, blank=[],
          extra=["Groups: three resins (LX 112, Spurr's, H Epon, left to right), each at clearance angles 3-9 deg (x tick labels).",
                 "Series colours: LX 112 yellow, Spurr's green, H Epon orange (key printed in panel B)."])
