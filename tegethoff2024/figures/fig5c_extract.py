"""Digitize Figure 5C of Tegethoff & Briggman 2024 (PDF p.7), a beeswarm plot, as per-row swarm profiles.
    python3 -I fig5c_extract.py -> fig5c.csv (+ ../work/fig5c_overlay.png). Method: swarm_common.py."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from swarm_common import *  # noqa: E402,F403

O50 = ["LX 112", "M Epon", "MH Epon", "H Epon", "VH Epon", "Durcupan", "Spurr's"]
O35 = ["LX 112", "M Epon", "MH Epon", "Durcupan", "Spurr's"]
run("fig5c", 7, (108, 790, 960, 1372), [1376.5, 1304.0, 1231.5, 1159.5, 1087.5, 1015.5, 943.0], [0, 5, 10, 15, 20, 25, 30], two_sets(O50, O35, "50 nm", "35 nm"),
    "Figure 5C: standard deviation of the sectional force (y axis 'deltaF_S', mN/mm) at 50 or 35 nm nominal section thickness.", "dFS_mN_per_mm", "mN/mm", blank=(),
    extra=["Groups: the x axis has two brackets labelled '50 nm' (7 resins) and '35 nm' (5 resins; no H Epon, no VH Epon).",
           "Series colours: LX 112 yellow, M Epon dark red, MH Epon blue, H Epon orange, VH Epon light blue, Durcupan",
           "  purple, Spurr's green (key printed next to panel B)."])
