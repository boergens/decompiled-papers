"""Digitize Figure 7A of Tegethoff & Briggman 2024 (PDF p.10), a beeswarm plot, as per-row swarm profiles.
    python3 -I fig7a_extract.py -> fig7a.csv (+ ../work/fig7a_overlay.png). Method: swarm_common.py run_ticks()."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from swarm_common import *  # noqa: E402,F403

run_ticks("fig7a", 10, (92, 5, 780, 541), [544.5, 485.5, 426.5, 367.5, 308.5, 249.5, 190.5, 131.5, 72.5, 13.5], [0, 10, 20, 30, 40, 50, 60, 70, 80, 90],
          [145, 201, 257.5, 369.5, 425.5, 481.5, 594, 650, 706],
          [(s, v) for s in FIG7_NAMES for v in ('0.3', '0.6', '1.2')],
          "Figure 7A: mean sectional force (y axis 'F_S' with an overbar, mN/mm) from different resins (colour-coded) cut at 50 nm and 6 degree clearance angle, plotted versus cutting speed (mm/s).", "mean_FS_mN_per_mm", "mN/mm", FIG7_NAMES, blank=[],
          extra=["Groups: three resins (LX 112, Spurr's, H Epon, left to right), each at cutting speeds 0.3, 0.6 and 1.2 mm/s (x tick labels).",
                 "Series colours: LX 112 yellow, Spurr's green, H Epon orange (key printed in panel B)."])
