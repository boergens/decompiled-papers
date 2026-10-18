"""Fig. 3C, 3D, 3E: digitize the LowECS (blue) and HighECS (orange/brown) curves and their shaded 99 %
confidence bands from the embedded 300-ppi JPEG of Fig. 3 (elife-08206-v3.pdf p. 7). Tier 3.

C and E: the x axis is categorical: 18 equally spaced ticks, one per network threshold of the 3D
segmentation (Materials and methods: 0.3 to 0.9 in steps of 0.1; then 0.95, 0.975, 0.99; then 0.995,
0.999, 0.9995, 0.9999, 0.99995, 0.99999, 0.999995, 0.999999; the printed labels 0.3, 0.5, 0.7, 0.9,
0.95, 0.975, 0.99, 0.999, 0.9999, 0.99999, 0.999999 fall on every tick up to 0.99 and on every second
tick after it). The curves are polylines with a corner at every tick: each straight segment is fitted
to the centre of the line-colour run in its interior columns, and a vertex is the mean of the two
adjacent segment fits at the tick (pal_common.polyline_vertices). The band edges are the extent of the
band tint (plus line colour) in the tick column; where the band is narrower than the drawn line
(~5 px) the edges are the line edges (flag band_hidden).
D: both curves traced column by column (centre of the line-colour run), with the band extent in each
column; the two solid points (minimum sum of the error fractions) read on an 8x zoom.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pal_common import *

a = load("fig3")
masks = {"LowECS": (blue_line(a), blue_band(a)), "HighECS": (orange_line(a), orange_band(a))}
# legend of panel C (lines + labels) is not data
for m, b in masks.values():
    m[1670:1740, 95:155] = False
    b[1670:1740, 95:155] = False
TH = ["0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "0.95", "0.975", "0.99", "0.995", "0.999", "0.9995", "0.9999",
      "0.99995", "0.99999", "0.999995", "0.999999"]
COMMON = ["Provenance: tier 3, digitized from the embedded 300-ppi JPEG (elife-08206-v3.pdf p. 7); figures/fig3_extract.py.",
          "LowECS = blue (perfused, 0.6 % ECS, data set M0027_11); HighECS = brown/orange (23.9 % ECS, M0007_33).",
          "Bands: 'Shaded regions in C-E are the 99% confidence intervals based on a Bernoulli sampling of the data' (caption)."]


def cat_panel(key, xs, ay, y0, y1, ylab, unit_note):
    rows, pts, lines = [], [], []
    for s, (m, b) in masks.items():
        v = polyline_vertices(m, xs, y0, y1)
        pl = []
        for th, x, (yp, n) in zip(TH, xs, v):
            if yp != yp:
                rows.append([s, th, "", "", "", "hidden (under the other curve)"])
                continue
            t, btm = band_extent(b, m, x, yp, y0, y1)
            flag = "band_hidden" if (btm - t) <= 7 else ""
            if n == 1:
                flag = (flag + " one-sided_vertex").strip()
            rows.append([s, th, ay(yp), ay(btm), ay(t), flag])
            pts.append((x, yp))
            pl.append((x, yp))
        lines.append((pl, (0, 200, 0)))
    hdr = [f"Pallotto et al. 2015 eLife 4:e08206, Figure 3{key.upper()}: {ylab} versus network threshold (categorical axis).",
           "Columns: series, threshold (category label of the tick), y (curve value at the tick), band_low, band_high",
           f"  (edges of the shaded confidence band at the tick), flag. {unit_note}"] + COMMON + [
           ay.describe("y") + ".",
           "x: 18 equally spaced ticks at image columns " + ", ".join(f"{x:g}" for x in xs) + ".",
           f"Uncertainty: +-1.5 px = +-{1.5 * abs(ay.m):.2g} y units; where the two lines overlap (e.g. the flat parts near the top)",
           "  the lower line is partly hidden and its value may be biased by up to 2 px.",
           "Flags: band_hidden = band not wider than the drawn line, edges are the line edges; one-sided_vertex = only one adjacent",
           "  segment visible."]
    write_csv(os.path.join(HERE, f"fig3{key}.csv"), hdr, ["series", "threshold", "y", "band_low", "band_high", "flag"], rows,
              ["{}", "{}", "{:.4g}", "{:.4g}", "{:.4g}", "{}"])
    draw(a, pts, os.path.join(WORK, f"fig3{key}_overlay.png"), lines=lines)


xsC = [97, 122, 146.25, 171, 196, 220.25, 245, 269.75, 294, 319, 343.5, 368, 393, 417.25, 442, 466.75, 491, 516]
ayC = Axis([(1452.5, 0.9), (1557.0, 0.8), (1661.0, 0.7), (1766.0, 0.6), (1400.0, 0.95), (1609.0, 0.75)])
cat_panel("c", xsC, ayC, 1335, 1764, "Adapted Rand Error", "y is the adapted Rand error (dimensionless).")
xsE = [1294, 1318, 1343, 1368, 1392, 1417, 1442, 1466, 1491, 1515.5, 1540, 1565, 1589, 1614, 1639, 1663, 1688, 1713]
ayE = Axis([(1744.0, 0), (1659.0, 10), (1575.0, 20), (1490.0, 30), (1406.0, 40), (1702.0, 5), (1364.0, 45)])
cat_panel("e", xsE, ayE, 1320, 1764, "Total Error Free Path Length (%)", "y in % of the total skeleton path length.")

# ---- panel D ----
axD = Axis([(692.0, 0), (733.0, 10), (773.0, 20), (813.0, 30), (854.0, 40), (894.0, 50), (934.0, 60), (974.5, 70), (1015.0, 80),
            (1055.0, 90), (1095.5, 100)])
ayD = Axis([(1744.0, 0), (1704.0, 10), (1664.0, 20), (1623.5, 30), (1583.0, 40), (1543.0, 50), (1502.5, 60), (1462.0, 70),
            (1422.0, 80), (1381.5, 90)])
rows, pts = [], []
for s, (m, b) in masks.items():
    prev = None
    for c in range(676, 1100):
        rr = runs(m[1330:1764, c])
        if not rr:
            continue
        r = max(rr, key=len) if prev is None else min(rr, key=lambda q: abs(q.mean() - prev))
        if prev is not None and abs(r.mean() - prev) > 25:
            continue
        prev = r.mean()
        y = 1330 + r.mean()
        t, btm = band_extent(b, m, c, y, 1330, 1764)
        rows.append([s, "curve", axD(c), ayD(y), ayD(btm), ayD(t)])
        pts.append((c, y))
for s, (x, y) in {"LowECS": (860.5, 1675.5), "HighECS": (859.5, 1702.5)}.items():
    rows.append([s, "solid point (minimum sum of error fractions)", axD(x), ayD(y), "", ""])
    pts.append((x, y))
hdr = ["Pallotto et al. 2015 eLife 4:e08206, Figure 3D: Merged Nodes (%) versus Split Edges (%), one curve per data volume,",
       "  parameterized by the network threshold (the vertices are not marked in the figure).",
       "Columns: series, kind (curve = one sample per image pixel column, ~0.25 % of x; solid point = the marked minimum),",
       "  split_edges_pct, merged_nodes_pct, band_low, band_high (edges of the shaded band in that column; equal to the",
       "  line edges where the band is narrower than the line)."] + COMMON + [
       axD.describe("x") + ".", ayD.describe("y") + ".",
       f"Uncertainty: +-1.5 px = +-{1.5 * abs(axD.m):.2g} % in x and +-{1.5 * abs(ayD.m):.2g} % in y; on steep parts the per-column",
       "  centre is the centre of a long vertical run. Solid points read on an 8x zoom, +-1 px."]
write_csv(os.path.join(HERE, "fig3d.csv"), hdr, ["series", "kind", "split_edges_pct", "merged_nodes_pct", "band_low", "band_high"],
          rows, ["{}", "{}", "{:.3f}", "{:.3f}", "{:.3f}", "{:.3f}"])
draw(a, pts, os.path.join(WORK, "fig3d_overlay.png"), r=1)
