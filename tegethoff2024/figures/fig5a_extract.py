"""Digitize Figure 5A of Tegethoff & Briggman 2024 (PDF p.7), a beeswarm plot, as per-row swarm profiles.
    python3 -I fig5a_extract.py -> fig5a.csv (+ ../work/fig5a_overlay.png). Method: swarm_common.py."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from swarm_common import *  # noqa: E402,F403

O50 = ["LX 112", "M Epon", "MH Epon", "H Epon", "VH Epon", "Durcupan", "Spurr's"]
O35 = ["LX 112", "M Epon", "MH Epon", "Durcupan", "Spurr's"]
run("fig5a", 7, (108, 10, 960, 594), [596.0, 532.5, 468.0, 404.5, 339.5, 275.5, 211.5, 147.5, 82.5], [0, 10, 20, 30, 40, 50, 60, 70, 80], two_sets(O50, O35, "50 nm", "35 nm"),
    "Figure 5A: mean sectional force (y axis 'F_S' with an overbar, mN/mm) from different resins (colour-coded) cut at 50 or 35 nm.", "mean_FS_mN_per_mm", "mN/mm", blank=(),
    extra=["Groups: the x axis has two brackets labelled '50 nm' (7 resins) and '35 nm' (5 resins; no H Epon, no VH Epon).",
           "Series colours: LX 112 yellow, M Epon dark red, MH Epon blue, H Epon orange, VH Epon light blue, Durcupan",
           "  purple, Spurr's green (key printed next to panel B)."])
