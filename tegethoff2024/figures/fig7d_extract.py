"""Digitize Figure 7D of Tegethoff & Briggman 2024 (PDF p.10), a beeswarm plot, as per-row swarm profiles.
    python3 -I fig7d_extract.py -> fig7d.csv (+ ../work/fig7d_overlay.png). Method: swarm_common.py run_ticks()."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from swarm_common import *  # noqa: E402,F403

run_ticks("fig7d", 10, (911, 705, 1600, 1251), [1254.5, 1188, 1122, 1055.5, 989, 922.5, 856, 790, 723.5], [0, 1, 2, 3, 4, 5, 6, 7, 8],
          [964, 1020, 1076, 1188.5, 1244.5, 1300.5, 1413, 1469, 1525],
          [(s, v) for s in FIG7_NAMES for v in ('0.3', '0.6', '1.2')],
          "Figure 7D: standard deviation of the transverse force (y axis 'deltaF_T', mN/mm) from different resins (colour-coded) cut at 50 nm and 6 degree clearance angle, plotted versus cutting speed (mm/s).", "dFT_mN_per_mm", "mN/mm", FIG7_NAMES, blank=[],
          extra=["Groups: three resins (LX 112, Spurr's, H Epon, left to right), each at cutting speeds 0.3, 0.6 and 1.2 mm/s (x tick labels).",
                 "Series colours: LX 112 yellow, Spurr's green, H Epon orange (key printed in panel B)."])
