"""Figure 3-figure supplement 1, panels A-C: cumulative distributions for the LowECS (blue) and HighECS
(brown/orange) volumes.

A (sfig3-1a.csv) - tier 1, computed from the eLife source data: Figure 3-source data 3 (M0007_33 =
  HighECS) and 4 (M0027_11 = LowECS) training cubes, six 128 x 128 x 128 uint16 label volumes each
  (elife-08206-fig3-data{3,4}-v3.zip, unzipped to work/zips/). Label 0 = membrane, 1 = ECS (identified by
  its volume fraction: 0.1-1.3 % of the LowECS cubes, 9-37 % of the HighECS cubes), >= 2 = one intracellular
  object (Materials and methods: 'ICS voxels from distinct neurites had different integer labels and ...
  ECS voxels were all labeled with the same integer label'). One object = one label value >= 2 in one cube;
  its voxel count is its size. The empirical CDF drawn over the published JPEG lies on the printed curves
  (work/sfig3-1_srcdata_overlay.png), and the medians (LowECS 11 779, HighECS 3 673 voxels) sit at the
  printed crosses.
B, C (sfig3-1b.csv, sfig3-1c.csv) - tier 3, digitized from elife_figure_supplements/elife-08206-fig3-figsupp1-v3.jpg
  (colour masks, pal_common.trace_both from seeds below and above the 50 % line; the median crosses blanked
  and given separately, read on a zoom +-2 px).
  Companion files sfig3-1b_sourcedata.csv / sfig3-1c_sourcedata.csv: path length and node count of every
  non-empty skeleton in Figure 3-source data 1 (M0027_11, LowECS) and 2 (M0007_33, HighECS), Knossos NML
  files, voxel size from the files (9.8 x 9.8 x 25 nm). These reproduce the printed LowECS curves closely but
  not the HighECS curves (full-file HighECS median 11.47 um and 19 nodes vs printed 10.1 um and 17 nodes;
  241 and 219 non-empty skeletons vs 220 and 217 in the text): the plotted data were evidently restricted
  in a way the paper does not describe, so B and C stay tier 3.
"""
import os, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pal_common import *
from PIL import Image
import xml.etree.ElementTree as ET

a = load("fig3-figsupp1")
Z = os.path.join(WORK, "zips")
if not os.path.isdir(os.path.join(Z, "d1")):
    import zipfile
    for i in range(1, 5):
        zipfile.ZipFile(os.path.join(SUPP, f"elife-08206-fig3-data{i}-v3.zip")).extractall(os.path.join(Z, f"d{i}"))
SER = {"LowECS": ("d4", "d1"), "HighECS": ("d3", "d2")}

# ---------- A: tier 1 ----------
axA = Axis([(300.0, 100), (414.5, 1000), (529.5, 1e4), (643.5, 1e5), (758.5, 1e6)], log=True)
ayA = Axis([(671.5, 0), (523.5, 25), (375.5, 50), (228.5, 75), (80.5, 100)])
rows, lines, meds = [], [], {}
for s, (dc, dn) in SER.items():
    sizes = []
    for f in sorted(glob.glob(os.path.join(Z, dc, "*.tif"))):
        t = Image.open(f)
        v = np.array([np.array(t.seek(i) or t) for i in range(t.n_frames)])
        u, c = np.unique(v, return_counts=True)
        for lab, n in zip(u, c):
            if lab >= 2:
                sizes.append((os.path.basename(f)[:-4], int(lab), int(n)))
    sizes.sort(key=lambda q: q[2])
    N = len(sizes)
    meds[s] = (N, float(np.median([q[2] for q in sizes])))
    pl = []
    for k, (cube, lab, n) in enumerate(sizes, start=1):
        rows.append([s, cube, lab, n, 100.0 * k / N])
        pl += [(axA.inv(n), ayA.inv(100.0 * (k - 1) / N)), (axA.inv(n), ayA.inv(100.0 * k / N))]
    lines.append((pl, (255, 0, 255) if s == "LowECS" else (0, 200, 0)))
hdr = ["Pallotto et al. 2015 eLife 4:e08206, Figure 3-figure supplement 1A: Cumulative Distribution Function (%) of 3D GT Voxels / Object.",
       "Columns: series, cube (training cube file name), label (integer label in that cube), voxels (object size), cdf_pct",
       "  (empirical CDF in %, objects sorted by size; the printed curve is this step function).",
       "Provenance: tier 1, computed from the eLife source data (Figure 3-source data 3 = M0007_33 = HighECS, 4 = M0027_11 = LowECS",
       "  training cubes) by figures/sfig3-1_extract.py; labels >= 2 are intracellular objects (0 = membrane, 1 = ECS).",
       "Objects and medians: " + "; ".join(f"{k}: n = {n}, median {m:g} voxels" for k, (n, m) in meds.items()) + ".",
       "Check: drawn over the published JPEG (work/sfig3-1a_tier1_overlay.png), the step functions lie on the printed curves."]
write_csv(os.path.join(HERE, "sfig3-1a.csv"), hdr, ["series", "cube", "label", "voxels", "cdf_pct"], rows,
          ["{}", "{}", "{}", "{}", "{:.4f}"])
draw(a, [], os.path.join(WORK, "sfig3-1a_tier1_overlay.png"), lines=lines)


# ---------- B, C: tier 3 + source-data companions ----------
def digitize(key, ax, ay, region, seeds, xbox, xmarks, xlab, unit):
    x0, y0, x1, y1 = region
    rows, pts = [], []
    for s, m in (("LowECS", blue_line(a)), ("HighECS", orange_line(a))):
        m = m.copy()
        bx0, by0, bx1, by1 = xbox
        m[by0:by1, bx0:bx1] = False
        (cl, yl), (ch, yh) = seeds[s]
        ymid = ay.inv(50)
        lo = dict(trace_both(m, x0, x1, y0, y1, cl, yl))
        hi = dict(trace_both(m, x0, x1, y0, y1, ch, yh))
        tr = sorted({**{c: y for c, y in lo.items() if y > ymid}, **{c: y for c, y in hi.items() if y <= ymid}}.items())
        for c, y in tr:
            rows.append([s, "curve", ax(c), ay(y)])
            pts.append((c, y))
    for s, (x, y) in xmarks.items():
        rows.append([s, "median cross", ax(x), ay(y)])
        pts.append((x, y))
    hdr = [f"Pallotto et al. 2015 eLife 4:e08206, Figure 3-figure supplement 1{key.upper()}: Cumulative Distribution Function (%) of {xlab}.",
           f"Columns: series (LowECS blue, HighECS brown), kind (curve sample per pixel column, or median cross), x ({unit}), cdf_pct.",
           "Provenance: tier 3, digitized from elife_figure_supplements/elife-08206-fig3-figsupp1-v3.jpg; figures/sfig3-1_extract.py.",
           f"  Skeleton statistics computed from the NML source data are in sfig3-1{key}_sourcedata.csv (they do not reproduce the",
           "  printed HighECS curve; see the script docstring).",
           ax.describe("x") + ".", ay.describe("y") + ".",
           f"Uncertainty: +-1.5 px = +-{1.5 * abs(ax.m):.2g} {'decade' if ax.log else unit} in x, +-{1.5 * abs(ay.m):.2g} % in y. The curves overlap",
           "  over much of their length (HighECS drawn on top); hidden LowECS columns are missing. Median crosses: both series' crosses",
           "  coincide (HighECS on top)."]
    write_csv(os.path.join(HERE, f"sfig3-1{key}.csv"), hdr, ["series", "kind", "x", "cdf_pct"], rows, ["{}", "{}", "{:.4g}", "{:.3f}"])
    draw(a, pts, os.path.join(WORK, f"sfig3-1{key}_overlay.png"), r=1)


axB = Axis([(1429.0, 1), (1631.0, 10), (1834.0, 100)], log=True)
ayB = Axis([(672.0, 0), (525.0, 25), (377.5, 50), (230.0, 75), (83.0, 100)])
digitize("b", axB, ayB, (1229, 55, 1872, 699),
         {"LowECS": ((1500, 621.0), (1730, 130.5)), "HighECS": ((1500, 631.5), (1700, 189.0))},
         (1615, 360, 1650, 395), {"LowECS": (1632.0, 377.0), "HighECS": (1632.0, 377.0)},
         "Path Length / Skeleton (um)", "um")
axC = Axis([(1233.5, 0), (1446.0, 50), (1658.5, 100)])
ayC = Axis([(1607.0, 0), (1462.0, 25), (1317.0, 50), (1172.0, 75), (1027.0, 100)])
digitize("c", axC, ayC, (1236, 1000, 1869, 1634),
         {"LowECS": ((1255, 1532.0), (1400, 1102.5)), "HighECS": ((1255, 1565.0), (1400, 1129.5))},
         (1285, 1300, 1322, 1335), {"LowECS": (1302.0, 1317.0), "HighECS": (1303.5, 1317.0)},
         "Nodes / Skeleton", "nodes")

# source-data companions
for key in ("b", "c"):
    rows = []
    stats = {}
    for s, (dc, dn) in SER.items():
        f = glob.glob(os.path.join(Z, dn, "*.nml"))[0]
        r = ET.parse(f).getroot()
        sc = r.find("parameters/scale").attrib
        scale = np.array([float(sc[k]) for k in "xyz"])
        vals = []
        for t in r.findall("thing"):
            nd = {n.get("id"): np.array([float(n.get(k)) for k in "xyz"]) for n in t.findall("nodes/node")}
            if not nd:
                continue
            L = sum(np.linalg.norm((nd[e.get("source")] - nd[e.get("target")]) * scale) for e in t.findall("edges/edge")) / 1000
            vals.append((t.get("id"), L, len(nd)))
        v = sorted(vals, key=lambda q: q[1] if key == "b" else q[2])
        N = len(v)
        stats[s] = (os.path.basename(f), N, sum(q[2] for q in v), sum(q[1] for q in v) / 1000, np.median([q[1] for q in v]),
                    np.median([q[2] for q in v]))
        for k, (tid, L, n) in enumerate(v, start=1):
            rows.append([s, tid, L, n, 100.0 * k / N])
    hdr = [f"Pallotto et al. 2015 eLife 4:e08206, Figure 3-figure supplement 1{key.upper()}, recomputed from the eLife source data (Figure 3-",
           "  source data 1 = M0027_11 = LowECS, 2 = M0007_33 = HighECS dense skeletonizations, Knossos NML).",
           "Columns: series, skeleton_id (NML thing id), path_length_um (sum of edge lengths, voxel size from the file),",
           f"  n_nodes, cdf_pct (empirical CDF of {'path length' if key == 'b' else 'node count'}, %; rows sorted by it).",
           "Provenance: computed by figures/sfig3-1_extract.py from all non-empty skeletons in each file. NOT identical to the plotted",
           "  data for HighECS (see the script docstring); use sfig3-1" + key + ".csv for the printed curves.",
           "Totals: " + "; ".join(f"{k} ({fn}): {N} skeletons, {nn} nodes, {Lt:.3f} mm, median {ml:.2f} um, median {mn:g} nodes"
                                   for k, (fn, N, nn, Lt, ml, mn) in stats.items()) + ".",
           "Text: LowECS 220 skeletons, 3.29 mm, median 10.2 um; HighECS 217, 3.40 mm, 10.1 um; nodes n = 5130 / 5364;",
           "  Figure 3-figure supplement 1 caption: medians 10.2 / 10.1 um and 16 / 17 nodes."]
    write_csv(os.path.join(HERE, f"sfig3-1{key}_sourcedata.csv"), hdr, ["series", "skeleton_id", "path_length_um", "n_nodes", "cdf_pct"],
              rows, ["{}", "{}", "{:.4f}", "{}", "{:.4f}"])
print(meds, stats)
