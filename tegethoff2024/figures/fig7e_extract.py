"""Digitize Figure 7E of Tegethoff & Briggman 2024 (PDF p.10), a beeswarm plot, as per-row swarm profiles.
    python3 -I fig7e_extract.py -> fig7e.csv (+ ../work/fig7e_overlay.png). Method: swarm_common.py run_ticks()."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from swarm_common import *  # noqa: E402,F403

run_ticks("fig7e", 10, (98, 1410, 780, 1954), [1957.5, 1882.5, 1807, 1732, 1657, 1582, 1506.5, 1431.5], [0, 10, 20, 30, 40, 50, 60, 70],
          [122, 150, 178, 205.5, 233.5, 261, 289, 344.5, 372.5, 400, 428, 456, 483.5, 511.5, 567, 594.5, 622.5, 650.5, 678, 706, 733.5],
          [(s, str(v)) for s in FIG7_NAMES for v in range(3, 10)],
          "Figure 7E: mean sectional force (y axis 'F_S' with an overbar, mN/mm) from different resins (colour-coded) cut at 35 nm and 1.2 mm/s, plotted versus knife clearance angle (deg).", "mean_FS_mN_per_mm", "mN/mm", FIG7_NAMES, blank=[],
          extra=["Groups: three resins (LX 112, Spurr's, H Epon, left to right), each at clearance angles 3-9 deg (x tick labels).",
                 "Series colours: LX 112 yellow, Spurr's green, H Epon orange (key printed in panel B)."])
