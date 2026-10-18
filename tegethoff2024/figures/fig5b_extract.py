"""Digitize Figure 5B of Tegethoff & Briggman 2024 (PDF p.7), a beeswarm plot, as per-row swarm profiles.
    python3 -I fig5b_extract.py -> fig5b.csv (+ ../work/fig5b_overlay.png). Method: swarm_common.py."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from swarm_common import *  # noqa: E402,F403

O50 = ["LX 112", "M Epon", "MH Epon", "H Epon", "VH Epon", "Durcupan", "Spurr's"]
O35 = ["LX 112", "M Epon", "MH Epon", "Durcupan", "Spurr's"]
run("fig5b", 7, (1003, 10, 1917, 592), [595.5, 403.5, 210.5], [0, 5, 10], two_sets(O50, O35, "50 nm", "35 nm"),
    "Figure 5B: mean transverse force (y axis 'F_T' with an overbar, mN/mm) from different resins cut at 50 or 35 nm nominal section thickness.", "mean_FT_mN_per_mm", "mN/mm", blank=((1715, 0, 1917, 600), (1630, 0, 1917, 345)),
    extra=["Groups: the x axis has two brackets labelled '50 nm' (7 resins) and '35 nm' (5 resins; no H Epon, no VH Epon).",
           "Series colours: LX 112 yellow, M Epon dark red, MH Epon blue, H Epon orange, VH Epon light blue, Durcupan",
           "  purple, Spurr's green (key printed next to panel B)."])
