"""Digitize Figure 5D of Tegethoff & Briggman 2024 (PDF p.7), a beeswarm plot, as per-row swarm profiles.
    python3 -I fig5d_extract.py -> fig5d.csv (+ ../work/fig5d_overlay.png). Method: swarm_common.py."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from swarm_common import *  # noqa: E402,F403

O50 = ["LX 112", "M Epon", "MH Epon", "H Epon", "VH Epon", "Durcupan", "Spurr's"]
O35 = ["LX 112", "M Epon", "MH Epon", "Durcupan", "Spurr's"]
run("fig5d", 7, (1004, 790, 1917, 1370), [1373.5, 1277.5, 1181.5, 1085.5, 989.5], [0, 1, 2, 3, 4], two_sets(O50, O35, "50 nm", "35 nm"),
    "Figure 5D: standard deviation of the transverse force (y axis 'deltaF_T', mN/mm) at 50 or 35 nm nominal section thickness.", "dFT_mN_per_mm", "mN/mm", blank=(),
    extra=["Groups: the x axis has two brackets labelled '50 nm' (7 resins) and '35 nm' (5 resins; no H Epon, no VH Epon).",
           "Series colours: LX 112 yellow, M Epon dark red, MH Epon blue, H Epon orange, VH Epon light blue, Durcupan",
           "  purple, Spurr's green (key printed next to panel B)."])
