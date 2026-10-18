"""Digitize Figure 7G of Tegethoff & Briggman 2024 (PDF p.10), a beeswarm plot, as per-row swarm profiles.
    python3 -I fig7g_extract.py -> fig7g.csv (+ ../work/fig7g_overlay.png). Method: swarm_common.py run_ticks()."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from swarm_common import *  # noqa: E402,F403

run_ticks("fig7g", 10, (94, 2110, 780, 2656), [2659.5, 2572, 2484, 2396.5, 2308.5, 2221, 2133], [0, 10, 20, 30, 40, 50, 60],
          [118.5, 146.5, 174.5, 202, 230, 257.5, 285.5, 341, 369, 397, 424.5, 452.5, 480, 508, 563.5, 591.5, 619.5, 647, 675, 702.5, 730.5],
          [(s, str(v)) for s in FIG7_NAMES for v in range(3, 10)],
          "Figure 7G: standard deviation of the sectional force (y axis 'deltaF_S', mN/mm) from different resins (colour-coded) cut at 35 nm and 1.2 mm/s, plotted versus knife clearance angle (deg).", "dFS_mN_per_mm", "mN/mm", FIG7_NAMES, blank=[],
          extra=["Groups: three resins (LX 112, Spurr's, H Epon, left to right), each at clearance angles 3-9 deg (x tick labels).",
                 "Series colours: LX 112 yellow, Spurr's green, H Epon orange (key printed in panel B)."])
