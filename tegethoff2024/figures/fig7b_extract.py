"""Digitize Figure 7B of Tegethoff & Briggman 2024 (PDF p.10), a beeswarm plot, as per-row swarm profiles.
    python3 -I fig7b_extract.py -> fig7b.csv (+ ../work/fig7b_overlay.png). Method: swarm_common.py run_ticks()."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from swarm_common import *  # noqa: E402,F403

run_ticks("fig7b", 10, (911, 5, 1600, 541), [544.5, 491.5, 438.5, 385.5, 332, 279, 226, 173, 119.5, 66.5, 13.5], [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20],
          [964.5, 1020.5, 1077, 1189, 1245, 1301, 1413.5, 1469.5, 1525.5],
          [(s, v) for s in FIG7_NAMES for v in ('0.3', '0.6', '1.2')],
          "Figure 7B: mean transverse force (y axis 'F_T' with an overbar, mN/mm) from different resins (colour-coded) cut at 50 nm and 6 degree clearance angle, plotted versus cutting speed (mm/s).", "mean_FT_mN_per_mm", "mN/mm", FIG7_NAMES, blank=[(1450, 0, 1629, 150)],
          extra=["Groups: three resins (LX 112, Spurr's, H Epon, left to right), each at cutting speeds 0.3, 0.6 and 1.2 mm/s (x tick labels).",
                 "Series colours: LX 112 yellow, Spurr's green, H Epon orange (key printed in panel B)."])
