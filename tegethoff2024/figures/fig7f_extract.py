"""Digitize Figure 7F of Tegethoff & Briggman 2024 (PDF p.10), a beeswarm plot, as per-row swarm profiles.
    python3 -I fig7f_extract.py -> fig7f.csv (+ ../work/fig7f_overlay.png). Method: swarm_common.py run_ticks()."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from swarm_common import *  # noqa: E402,F403

run_ticks("fig7f", 10, (911, 1410, 1600, 1953), [1956.5, 1869, 1781.5, 1694, 1606.5, 1519, 1431.5], [0, 2, 4, 6, 8, 10, 12],
          [935.5, 963.5, 991, 1019, 1046.5, 1074.5, 1102, 1157.5, 1185.5, 1213, 1241, 1268.5, 1296.5, 1324, 1379.5, 1407.5, 1435, 1463, 1490.5, 1518.5, 1546],
          [(s, str(v)) for s in FIG7_NAMES for v in range(3, 10)],
          "Figure 7F: mean transverse force (y axis 'F_T' with an overbar, mN/mm) from different resins (colour-coded) cut at 35 nm and 1.2 mm/s, plotted versus knife clearance angle (deg).", "mean_FT_mN_per_mm", "mN/mm", FIG7_NAMES, blank=[],
          extra=["Groups: three resins (LX 112, Spurr's, H Epon, left to right), each at clearance angles 3-9 deg (x tick labels).",
                 "Series colours: LX 112 yellow, Spurr's green, H Epon orange (key printed in panel B)."])
