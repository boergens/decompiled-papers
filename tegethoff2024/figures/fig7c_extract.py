"""Digitize Figure 7C of Tegethoff & Briggman 2024 (PDF p.10), a beeswarm plot, as per-row swarm profiles.
    python3 -I fig7c_extract.py -> fig7c.csv (+ ../work/fig7c_overlay.png). Method: swarm_common.py run_ticks()."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from swarm_common import *  # noqa: E402,F403

run_ticks("fig7c", 10, (96, 705, 780, 1250), [1253, 1165, 1077, 988.5, 900.5, 812.5, 724], [0, 10, 20, 30, 40, 50, 60],
          [148.5, 204.5, 260, 372, 428, 484, 595.5, 651.5, 707.5],
          [(s, v) for s in FIG7_NAMES for v in ('0.3', '0.6', '1.2')],
          "Figure 7C: standard deviation of the sectional force (y axis 'deltaF_S', mN/mm) from different resins (colour-coded) cut at 50 nm and 6 degree clearance angle, plotted versus cutting speed (mm/s).", "dFS_mN_per_mm", "mN/mm", FIG7_NAMES, blank=[],
          extra=["Groups: three resins (LX 112, Spurr's, H Epon, left to right), each at cutting speeds 0.3, 0.6 and 1.2 mm/s (x tick labels).",
                 "Series colours: LX 112 yellow, Spurr's green, H Epon orange (key printed in panel B)."])
