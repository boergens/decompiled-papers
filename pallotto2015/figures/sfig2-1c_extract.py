"""Figure 2-figure supplement 1C: cumulative distributions of the number of ground-truth intracellular
pixels per object for the four 2D data sets.

1) sfig2-1c.csv (tier 3, the printed curves): digitized from elife_figure_supplements/elife-08206-fig2-figsupp1-v3.jpg.
   Colour masks per legend colour, traced column by column in both directions from visible points at columns 300
   and 430 (pal_common.trace_both; below / above the 50 % line respectively); the median crosses (x marks at 50 %) are blanked for the tracing and
   given separately (centres read on an 8x zoom, +-1 px).
2) sfig2-1c_sourcedata.csv (computed from the eLife source data, Figure 2-source data 1-4,
   elife-08206-fig2-data{1..4}-v3.tif, frame 2 = expert labels; grey 171 = intracellular, 85 =
   extracellular, 0 = membrane, as identified by the area fractions 0.59 / 5.78 / 11.36 / 24.1 % for
   grey 85, matching the ECS fractions 0.6 / 5.8 / 11.3 / 23.9 %): connected components (four
   connectivity, as in Materials and methods) of the intracellular pixels, computed separately in each
   of the nine 640 x 576 sub-images of the top-left 1920 x 1728 pixels (the labelled region and its
   subdivision for the ninefold cross-validation, Materials and methods). The paper does not say exactly
   how the plotted distributions were binned or which objects were kept: the printed curves are 0 below
   ~18 pixels and are drawn as straight segments between points about 0.25 decade apart, while the
   source-data distributions contain objects of 1-17 pixels (3-6 % of objects). The medians agree to
   within ~5 % (0.6 %: 746 vs printed cross 746; 23.9 %: 274 vs 277; 5.8 %: 449 vs ~475; 11.3 %: 490 vs 468).
   Variants (whole 2016 x 1736 image; one 1920 x 1728 block without subdivision; other crop offsets) give
   medians 4-15 % higher; see work/ notes in the README.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pal_common import *

a = load("fig2-figsupp1")
A = a.astype(int)
R, G, B = A[..., 0], A[..., 1], A[..., 2]
ax = Axis([(277.5, 100), (411.0, 1000), (544.5, 1e4)], log=True)
ay = Axis([(1343.0, 0), (1217.5, 25), (1092.0, 50), (966.5, 75), (841.5, 100)])
M = {"0.6% ECS": (R > 40) & (R < 115) & (G > 30) & (G < 100) & (B > 100) & (B < 180) & (B - G > 40),
     "5.8% ECS": (R > 55) & (R < 125) & (G > 80) & (G < 140) & (B > 15) & (B < 85) & (G - B > 30) & (G - R > 8),
     "11.3% ECS": (R > 200) & (G > 100) & (G < 180) & (B < 80),
     "23.9% ECS": (R > 95) & (R < 175) & (G < 50) & (B < 50)}
SEED_LO = {"0.6% ECS": 1259.5, "5.8% ECS": 1211.0, "11.3% ECS": 1241.5, "23.9% ECS": 1189.5}   # rows at column 300
SEED = {"0.6% ECS": 1014.5, "5.8% ECS": 1004.0, "11.3% ECS": 980.5, "23.9% ECS": 932.5}   # visible rows at column 430
XM = {"23.9% ECS": (336.5, 1091.0), "11.3% ECS": (367.0, 1091.0), "5.8% ECS": (368.5, 1091.0), "0.6% ECS": (394.0, 1091.0)}
rows, pts = [], []
for s, m in M.items():
    m = m.copy()
    m[1076:1107, 320:412] = False          # median crosses
    lo = dict(trace_both(m, 147, 676, 820, 1350, 300, SEED_LO[s]))   # below the median crosses
    hi = dict(trace_both(m, 147, 676, 820, 1350, 430, SEED[s]))      # above them
    tr = sorted({**{c: y for c, y in lo.items() if y > 1092}, **{c: y for c, y in hi.items() if y <= 1092}}.items())
    for c, y in tr:
        rows.append([s, "curve", ax(c), ay(y)])
        pts.append((c, y))
for s, (x, y) in XM.items():
    rows.append([s, "median cross", ax(x), ay(y)])
    pts.append((x, y))
hdr = ["Pallotto et al. 2015 eLife 4:e08206, Figure 2-figure supplement 1C: Cumulative Distribution Function (%) of 2D GT Pixels / Object.",
       "Columns: series (legend of panel A), kind (curve sample per pixel column, or the median cross), pixels_per_object (log axis), cdf_pct.",
       "Provenance: tier 3, digitized from elife_figure_supplements/elife-08206-fig2-figsupp1-v3.jpg; figures/sfig2-1c_extract.py.",
       "  A distribution computed from the eLife source data is in sfig2-1c_sourcedata.csv (see that file and the script docstring).",
       ax.describe("x") + "; the frame spans 10 (left) to 1e5 (right).", ay.describe("y") + ".",
       f"Uncertainty: +-1.5 px = +-{1.5 * abs(ax.m):.2g} decade in x, +-{1.5 * abs(ay.m):.2g} % in y. The four curves overlap, mainly below",
       "  ~100 pixels and above ~5000 pixels; columns where a colour is hidden are missing. The 5.8% median cross lies under the 11.3% one",
       "  (only its outline is visible): its position is uncertain by +-3 px."]
write_csv(os.path.join(HERE, "sfig2-1c.csv"), hdr, ["series", "kind", "pixels_per_object", "cdf_pct"], rows,
          ["{}", "{}", "{:.4g}", "{:.3f}"])
draw(a, pts, os.path.join(WORK, "sfig2-1c_overlay.png"), r=1)

# ---- source data ----
from PIL import Image
from scipy import ndimage
st4 = ndimage.generate_binary_structure(2, 1)
srows = []
meds = {}
for i, s in enumerate(["0.6% ECS", "5.8% ECS", "11.3% ECS", "23.9% ECS"], start=1):
    t = Image.open(os.path.join(SUPP, f"elife-08206-fig2-data{i}-v3.tif"))
    t.seek(1)
    ics = np.array(t)[:1728, :1920] == 171
    sizes = []
    for r in range(3):
        for q in range(3):
            lab, n = ndimage.label(ics[r * 576:(r + 1) * 576, q * 640:(q + 1) * 640], st4)
            sizes += list(np.bincount(lab.ravel())[1:])
    v = np.sort(np.array(sizes))
    meds[s] = (len(v), float(np.median(v)))
    u, cnt = np.unique(v, return_counts=True)
    cdf = np.cumsum(cnt) / len(v) * 100
    for uu, cc, nn in zip(u, cdf, cnt):
        srows.append([s, int(uu), int(nn), cc])
hdr = ["Pallotto et al. 2015 eLife 4:e08206, Figure 2-figure supplement 1C, recomputed from the eLife source data (Figure 2-source data 1-4).",
       "Columns: series, pixels_per_object (object size, pixels), n_objects (objects of exactly this size), cdf_pct (% of objects <= this size).",
       "Provenance: computed from elife_figure_supplements/elife-08206-fig2-data{1..4}-v3.tif (expert labels, frame 2) by",
       "  figures/sfig2-1c_extract.py: 4-connected components of the intracellular label in each of the nine 640 x 576 sub-images of the",
       "  top-left 1920 x 1728 pixels. This is a reconstruction: the paper does not state the exact procedure behind the plotted curves,",
       "  which start at ~18 pixels; this file keeps all objects (from 1 pixel). Use sfig2-1c.csv for the printed curves.",
       "Objects and medians: " + "; ".join(f"{k}: n = {n}, median {m:g} px" for k, (n, m) in meds.items()) + "."]
write_csv(os.path.join(HERE, "sfig2-1c_sourcedata.csv"), hdr, ["series", "pixels_per_object", "n_objects", "cdf_pct"], srows,
          ["{}", "{}", "{}", "{:.3f}"])
from collections import Counter
print(Counter(r[0] for r in rows), meds)
