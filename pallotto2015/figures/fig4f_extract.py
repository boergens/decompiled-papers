"""Fig. 4F: stacked bars, number of contacts by cell type of the contacting cell, for tight and cleft
contacts. Tier 3, digitized from the embedded 300-ppi JPEG of Fig. 4 (elife-08206-v3.pdf p. 9).

In the centre column of each bar the segment boundaries are the thin dark outline rows between colour
runs; each boundary's row is the centre of that outline. Colours (caption): AII (blue), cone bipolar
(green), presynaptic amacrine cell (cyan), other (black).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pal_common import *

a = load("fig4").astype(int)
ay = Axis([(1216.5, 0), (1116.5, 50), (1016.5, 100), (917.5, 150)])
COL = {"AII (blue)": lambda p: p[2] > 200 and p[0] < 60 and p[1] < 60,
       "cone bipolar (green)": lambda p: p[1] > 200 and p[0] < 60 and p[2] < 60,
       "presynaptic amacrine cell (cyan)": lambda p: p[1] > 200 and p[2] > 200 and p[0] < 60,
       "other (black)": lambda p: max(p) < 40}
rows, pts = [], []
for bar, x in (("Tight contacts", 318), ("Cleft contacts", 480)):
    col = a[860:1240, x]
    lab = []
    for p in col:
        k = next((n for n, f in COL.items() if f(p)), None)
        lab.append(k)
    # colour runs (ignoring 1-3 px outline rows); outline rows are dark, i.e. would be classed 'other (black)'
    segs = []
    i = 0
    while i < len(lab):
        j = i
        while j < len(lab) and lab[j] == lab[i]:
            j += 1
        if lab[i] is not None and (j - i) > 3:
            segs.append([lab[i], 860 + i, 860 + j - 1])
        i = j
    # boundaries between consecutive segments: midway between the end of one and the start of the next
    top = 860 + int(np.argmax(col.mean(1) < 128))   # first dark row = outline on top of the bar
    bounds = [top] + [(s0[2] + s1[1]) / 2 for s0, s1 in zip(segs, segs[1:])] + [ay.inv(0)]
    for (name, r0, r1), b0, b1 in zip(segs, bounds, bounds[1:]):
        rows.append([bar, name, ay(b1), ay(b0), ay(b0) - ay(b1)])
        pts += [(x, b0), (x, b1)]
hdr = ["Pallotto et al. 2015 eLife 4:e08206, Figure 4F: # of contacts, stacked bars, color-coded by the cell type of the contacting cell.",
       "Columns: bar, segment (cell type, colour as in the caption), y_bottom, y_top (stack edges, # of contacts), count (= height).",
       "Provenance: tier 3, digitized from the embedded 300-ppi JPEG (elife-08206-v3.pdf p. 9); figures/fig4f_extract.py.",
       ay.describe("y") + ".",
       f"Uncertainty: +-1 px = +-{abs(ay.m):.2g} contacts per edge. Counts are integers in reality: the digitized heights round to",
       "  tight: 17 cone bipolar + 4 AII = 21; cleft: 130 other + 7 cone bipolar + 13 presynaptic amacrine = 150.",
       "Text (p. 8-9): 171 contacts; 150 cleft (13 chemical synapses from amacrine cells, 137 'other'); 21 tight (4 AII, 17 ON cone bipolar).",
       "  The cleft bar's 7 green (cone bipolar) contacts are counted within the text's 137 'other'."]
write_csv(os.path.join(HERE, "fig4f.csv"), hdr, ["bar", "segment", "y_bottom", "y_top", "count"], rows,
          ["{}", "{}", "{:.2f}", "{:.2f}", "{:.2f}"])
draw(a.astype(np.uint8), pts, os.path.join(WORK, "fig4f_overlay.png"))
for r in rows: print(r)
