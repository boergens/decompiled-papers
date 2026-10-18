"""Fig. 5C: FWHM labeling distance (um), mean +/- SEM, for conv fix and ECS fix, VAChT and VGAT.
Tier 3, digitized from the embedded 300-ppi JPEG of Fig. 5 (elife-08206-v3.pdf p. 10).

For each point the dark pixels (grey < 128) in a 25-px-wide window around its x tick are analysed:
the marker (filled circle) is the set of rows at least 8 px wide, its centre = the mean; the error-bar
ends are the outermost dark rows (the caps' centres are 1 px inside them).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pal_common import *

a = load("fig5")
g = a.astype(float).mean(2)
ay = Axis([(493.5, 0), (427.5, 5), (361.5, 10), (295.5, 15), (229.5, 20), (163.5, 25), (98.5, 30)])
rows, pts = [], []
for (grp, cond, x) in (("VAChT", "conv fix", 1487.5), ("VAChT", "ECS fix", 1588.5), ("VGAT", "conv fix", 1688.5),
                       ("VGAT", "ECS fix", 1788.5)):
    x0 = int(x) - 12
    sub = g[95:480, x0:x0 + 25] < 128
    w = sub.sum(1)
    rr = np.where(w > 0)[0]
    top, bot = 95 + rr[0] + 1.0, 95 + rr[-1] - 1.0          # cap centres (caps are ~2-3 px thick)
    mk = np.where(w >= 8)[0]
    yc = 95 + (mk[0] + mk[-1]) / 2
    rows.append([grp, cond, ay(yc), ay(bot), ay(top), (ay(top) - ay(bot)) / 2])
    pts += [(x, yc), (x, top), (x, bot)]
hdr = ["Pallotto et al. 2015 eLife 4:e08206, Figure 5C: FWHM labeling distance (um), mean +/- SEM (caption), conv fix vs ECS fix.",
       "Columns: antibody, condition, mean_um (marker centre), err_low_um, err_high_um (error-bar ends), half_bar_um (half the bar length).",
       "Provenance: tier 3, digitized from the embedded 300-ppi JPEG (elife-08206-v3.pdf p. 10); figures/fig5c_extract.py.",
       ay.describe("y") + ".",
       f"Uncertainty: +-1 px = +-{abs(ay.m):.2g} um. Where the bar is shorter than the marker (VAChT conv fix) the 'ends' are the",
       "  marker edges, so the bar length is an upper bound of what is visible.",
       "Text (p. 10): VAChT 28.1 +/- 2.4 um (ECS-preserved) vs 6.8 +/- 0.5 um (control); VGAT 16.9 +/- 1.0 um vs 6.1 +/- 0.4 um.",
       "  n = 20 retina slices from two animals (caption)."]
write_csv(os.path.join(HERE, "fig5c.csv"), hdr, ["antibody", "condition", "mean_um", "err_low_um", "err_high_um", "half_bar_um"], rows,
          ["{}", "{}", "{:.2f}", "{:.2f}", "{:.2f}", "{:.2f}"])
draw(a, pts, os.path.join(WORK, "fig5c_overlay.png"))
for r in rows: print(r)
