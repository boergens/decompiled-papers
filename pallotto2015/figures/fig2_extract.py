"""Fig. 2B, 2C, 2D: digitize the grey open circles (one per cross-validation fold) and the red
median crosses from the embedded 300-ppi JPEG of Fig. 2 (elife-08206-v3.pdf p. 5). Tier 3.

Axes: tick marks located in the image (dark pixel runs next to the axis lines, see work/ notes);
x is linear in "ECS fraction (%)" with ticks labelled 0.6, 6, 11, 24.
Circles: normalised cross-correlation of a ring template (radius 6 px, stroke 2 px) with a mask of
light-grey pixels, peaks >= 0.38, non-maximum suppression 3 px. Overlapping circles and circles
under the red crosses are partly missed: the caption implies 9 per group (ninefold cross-validation);
the CSV lists what could be resolved and the count per group.
Medians: centroid of each red connected component (the + marks).
Writes figures/fig2b.csv, fig2c.csv, fig2d.csv and work/fig2{b,c,d}_overlay.png.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pal_common import *
from scipy import ndimage

a = load("fig2")
ring = grey_ring_mask(a).astype(np.float32)
T, c = ring_template(6.0, 2.0)
red = red_mask(a)
groups = ["0.6", "5.8", "11.3", "23.9"]   # ECS fractions of the four data sets (caption); x ticks read 0.6, 6, 11, 24

P = {
    "b": dict(region=(115, 1440, 450, 1812), ylab="Classification Error",
              x=[(150.2, 0.6), (214.0, 6), (273.0, 11), (426.0, 24)],
              y=[(1818.0, 0), (1758.0, 0.02), (1698.0, 0.04), (1638.5, 0.06), (1578.5, 0.08), (1518.8, 0.10)]),
    "c": dict(region=(620, 1440, 960, 1812), ylab="Resampled Adapted Rand Error",
              x=[(654.5, 0.6), (718.0, 6), (777.0, 11), (930.5, 24)],
              y=[(1817.0, 0), (1737.5, 0.05), (1657.5, 0.1), (1578.0, 0.15), (1498.0, 0.2)]),
    "d": dict(region=(1115, 1440, 1460, 1812), ylab="(Splits + Mergers) / Object",
              x=[(1150.0, 0.6), (1213.5, 6), (1272.5, 11), (1426.0, 24)],
              y=[(1818.25, 0), (1747.0, 0.2), (1675.0, 0.4), (1603.0, 0.6), (1531.0, 0.8), (1459.5, 1.0)]),
}
for k, p in P.items():
    ax, ay = Axis(p["x"]), Axis(p["y"])
    xt = [px for px, v in p["x"]]
    def grp(px):
        return groups[int(np.argmin([abs(px - t) for t in xt]))]
    pk = match_peaks(ring, T, c, p["region"], 0.38, 3)
    x0, y0, x1, y1 = p["region"]
    lab, n = ndimage.label(red[y0:y1, x0:x1])
    meds = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(ys) > 60:
            meds.append((x0 + xs.mean(), y0 + ys.mean()))
    rows = []
    for px, py in sorted(meds):
        rows.append(["median", grp(px), ax(px), ay(py), ""])
    for px, py, s in sorted(pk, key=lambda q: (grp(q[0]), q[1])):
        rows.append(["fold", grp(px), ax(px), ay(py), round(s, 2)])
    counts = {g: sum(1 for r in rows if r[0] == "fold" and r[1] == g) for g in groups}
    hdr = [f"Pallotto et al. 2015 eLife 4:e08206, Figure 2{k.upper()}: {p['ylab']} versus ECS fraction (%).",
           "Columns: kind (fold = one grey open circle, one cross-validation test image; median = red + marker),",
           "  group (ECS fraction of the data set, %, from the caption), x_axis (horizontal position in axis units; the",
           "  circles are jittered around the group position), y (value).",
           "Provenance: tier 3, digitized from the embedded 300-ppi JPEG (elife-08206-v3.pdf p. 5) by ring-template matching",
           "  (circles) and red-component centroids (medians); script figures/fig2_extract.py.",
           ax.describe("x") + ".", ay.describe("y") + ".",
           f"Uncertainty: about +-1 px = +-{abs(ay.m):.2g} y units for isolated circles, +-2 px for overlapping ones.",
           f"Circles resolved per group (9 expected from the ninefold cross-validation): {counts}.",
           "  Missing circles are hidden under overlapping circles or under the red median marker.",
           "match_score = template correlation (0-1) of each circle."]
    write_csv(os.path.join(HERE, f"fig2{k}.csv"), hdr, ["kind", "group", "x_axis", "y", "match_score"], rows,
              ["{}", "{}", "{:.3f}", "{:.4f}", "{}"])
    draw(a, [(px, py) for px, py, s in pk] + meds, os.path.join(WORK, f"fig2{k}_overlay.png"))
    print(k, counts, [(round(ax(px), 2), round(ay(py), 4)) for px, py in meds])
