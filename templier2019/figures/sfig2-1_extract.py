"""Digitize Figure 2—figure supplement 1 of Templier 2019 (eLife 8:e45696): panels a-d.

Source: ../source/elife_figure_supplements/fig2-figsupp1.jpg (885 x 841 px, from
iiif.elifesciences.org). Raster only -> tier 3.
    python3 -I sfig2-1_extract.py
      -> sfig2-1a.csv, sfig2-1b.csv, sfig2-1c.csv   (grey-level grids of the three matrices)
         sfig2-1c_lines.csv                          (the coloured lines drawn over matrix c)
         sfig2-1d.csv                                (bar chart)
         ../work/sfig2-1*_overlay.png

Matrices (a, b, c). Each matrix is a square greyscale image in a black frame, ~381 px wide, with ticks every
74.2 px = 100 sections (labels 0, 200, 400 on the top and left axes; tick 0 on the frame edge). One image pixel
is therefore ~1.35 matrix cells: the cells are NOT resolved, and the grid is sampled at the native resolution
of the image (one value per image pixel, spec: "sampled at the map's native resolution"). The section index
of each pixel centre comes from a linear fit to the tick marks.

Lines over matrix c. Thin semi-transparent lines in the five legend colours (labelled 1, 2, 3, 4, 7) run
across matrix c horizontally and vertically. For each pixel column (row) of matrix c the median colour is
taken over the rows (columns) that carry no line of the other orientation and lie away from the diagonal band;
that colour is classified by the signs of R-G and B-G (rules in unmix()); JPEG chroma subsampling desaturates
and smears the colour of 1-px lines, which is why the full colour cannot be matched to the legend directly.
Adjacent columns of the same class are merged. At
~1.35 sections per pixel, neighbouring lines merge, so the line list is a lower bound and the positions are
+-1.5 sections.

Bar chart (d). Bars are blue; the height of each bar is the summed blue coverage of its central columns
above the x axis (sub-pixel), converted with a fit to the five y ticks (0-400). The values printed above the
bars are transcribed as `printed_value`.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../tools"))   # tools/digitize_common.py
import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402
from digitize_common import fit_axis, write_csv, overlay  # noqa: E402

IMG = os.path.join(HERE, "../source/elife_figure_supplements/fig2-figsupp1.jpg")
WORK = os.path.join(HERE, "../work")
a = np.asarray(Image.open(IMG).convert("RGB")).astype(float)
g = a.mean(2)


def ticks(profile, off, thr=170):
    idx = np.where(profile < thr)[0]
    groups = np.split(idx, np.where(np.diff(idx) > 1)[0] + 1)
    return [off + float(np.average(q, weights=255 - profile[q])) for q in groups if len(q)]


# ---------------------------------------------------------------- matrices
# frame lines (pixel index of the dark line) and tick bands, found by inspection of the profiles;
# the inner pixel ranges exclude the frame lines.
MAT = {
    "a": dict(cols=(71, 450), rows=(45, 424), xt=(37, 43, 60, 465), yt=(63, 69, 30, 440)),
    "b": dict(cols=(479, 859), rows=(46, 425), xt=(38, 44, 470, 870), yt=(471, 477, 30, 440)),
    "c": dict(cols=(71, 450), rows=(451, 830), xt=(443, 449, 60, 465), yt=(63, 69, 440, 845)),
}
VALS = [0, 100, 200, 300, 400, 500]
fits = {}
for k, m in MAT.items():
    r0, r1, c0, c1 = m["xt"]
    xt = ticks(g[r0:r1, c0:c1].mean(0), c0)
    c0, c1, r0, r1 = m["yt"]
    yt = ticks(g[r0:r1, c0:c1].mean(1), r0)
    assert len(xt) == 6 and len(yt) == 6, (k, xt, yt)
    fx, xres, xs = fit_axis(xt, VALS)
    fy, yres, ys = fit_axis(yt, VALS)
    fits[k] = (fx, fy, xres, yres, xs, ys)
    cs = np.arange(m["cols"][0], m["cols"][1] + 1)
    rs = np.arange(m["rows"][0], m["rows"][1] + 1)
    grid = g[rs[0]:rs[-1] + 1, cs[0]:cs[-1] + 1].copy()
    # the printed panel letter (a, b, c) is drawn over the upper right corner: blank its (dilated) strokes
    import cv2
    corner = (grid[:110, -110:] < 90).astype(np.uint8)
    nlab, lab, st, _ = cv2.connectedComponentsWithStats(corner, connectivity=8)
    big = [q for q in range(1, nlab) if st[q, 3] > 30]
    assert len(big) == 1, (k, [tuple(st[q]) for q in range(1, nlab)])
    glyph = cv2.dilate((lab == big[0]).astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
    gm = np.zeros(grid.shape, bool)
    gm[:110, -110:] = glyph
    grid[gm] = np.nan
    gy, gx = np.where(gm)
    letter_box = (float(fx(cs[0] + gx.min())), float(fx(cs[0] + gx.max())), float(fy(rs[0] + gy.min())), float(fy(rs[0] + gy.max())))
    n_edge = float(fx(m["cols"][1] + 1.5))       # index at the right frame line
    hdr = [
        f"Templier 2019 eLife 8:e45696, Figure 2—figure supplement 1{k}: pairwise similarity matrix of Dataset 1",
        {"a": "  (caption: 'Matrix of pairwise similarities of unordered sections computed with EM imagery').",
         "b": "  (caption: 'Reordered EM matrix').",
         "c": "  (caption: 'Matrix of pairwise similarities of unordered sections computed with fluorescent bead imagery';",
         }[k],
        "Grid CSV: one row per image pixel row inside the frame; first column y_index = section index (row axis,",
        "  0 at the top) of the pixel centre; the header gives x_index (column axis) of each pixel column; cells =",
        "  grey level of the pixel as printed (mean of R, G, B; 0 black, 255 white). Darker = higher similarity per the",
        "  legend; no colour bar, so the grey level is not a calibrated similarity.",
        "Provenance: tier 3, digitized from the eLife figure-supplement JPEG fig2-figsupp1.jpg (885 x 841 px) by",
        f"  sfig2-1_extract.py. Index fits on 6 ticks per axis (0-500 in steps of 100; labels 0, 200, 400), max",
        f"  residual {xres:.2f} (x) / {yres:.2f} (y) sections; {1 / abs(xs):.3f} px per section.",
        "Resolution: one pixel spans ~1.35 matrix cells, so single cells are not resolved: each value mixes 1-2",
        "  neighbouring cells (and JPEG blur). Uncertainty of the index of a pixel: +-1.4 sections.",
        f"Extent: the frame spans about {n_edge:.0f} sections from the 0 tick (Dataset 1 has 507 sections per the text;",
        "  the cost counts printed in panel d sum to 513 links, i.e. 514 sections). Not explained in the paper.",
        f"Empty cells: pixels under the strokes of the printed panel letter '{k}' (x index {letter_box[0]:.0f}-{letter_box[1]:.0f},",
        f"  y index {letter_box[2]:.0f}-{letter_box[3]:.0f}); the matrix is not visible there.",
    ]
    if k == "c":
        hdr.insert(2, "  the image shows a reordered matrix with coloured lines and a legend, see the README); the grey level here")
        hdr.insert(3, "  includes the coloured lines (grey = mean of R, G, B); their positions and colours are in sfig2-1c_lines.csv.")
    with open(os.path.join(HERE, f"sfig2-1{k}.csv"), "w") as f:
        for h in hdr:
            f.write("# " + h + "\n")
        f.write("y_index\\x_index," + ",".join(f"{float(fx(c)):.2f}" for c in cs) + "\n")
        for i, r in enumerate(rs):
            f.write(f"{float(fy(r)):.2f}," + ",".join("" if v != v else str(int(round(v))) for v in grid[i]) + "\n")
    print(f"sfig2-1{k}.csv: {len(rs)} x {len(cs)} px; tick residuals {xres:.3f} {yres:.3f}; frame end index {n_edge:.1f}")
    # overlay: tick fit check - mark pixel centres of index 0,100,...,500 along both axes
    pts = []
    for v in VALS:
        cx = cs[0] + (v - float(fx(cs[0]))) / (float(fx(cs[1])) - float(fx(cs[0])))
        ry = rs[0] + (v - float(fy(rs[0]))) / (float(fy(rs[1])) - float(fy(rs[0])))
        pts += [(cx, ry)] + [(cx, rr) for rr in range(rs[0], rs[-1], 6)] + [(cc, ry) for cc in range(cs[0], cs[-1], 6)]
    overlay(a.astype(np.uint8), pts, os.path.join(WORK, f"sfig2-1{k}_overlay.png"))

# ---------------------------------------------------------------- lines over matrix c
LEG = {"1": (101, 179, 101), "2": (102, 101, 254.5), "3": (101, 101, 101), "4": (215, 101.5, 218), "7": (255, 103, 100)}
# legend swatch medians are re-measured here (5 x 24 px around each swatch centre) to keep the script honest
SW = {"1": (459, 529), "2": (459, 630), "3": (459, 731), "4": (500, 529), "7": (500, 630)}
for key, (y, x) in SW.items():
    LEG[key] = tuple(np.median(a[y - 2:y + 3, x - 12:x + 12].reshape(-1, 3), axis=0))
m = MAT["c"]
sub = a[m["rows"][0]:m["rows"][1] + 1, m["cols"][0]:m["cols"][1] + 1]
n = sub.shape[0]
colmed = np.median(sub, axis=0)
rowmed = np.median(sub, axis=1)
linecols = (255 - colmed.min(1)) > 40
linerows = (255 - rowmed.min(1)) > 40
fx, fy = fits["c"][0], fits["c"][1]


def unmix(p):
    """Classify a line colour by the signs of its colour differences, which survive desaturation.

    JPEG chroma subsampling washes out (and smears between neighbouring rows) the colour of 1-px lines, so
    neither the full colour nor the hue angle is reliable; the signs of R-G and B-G are. Rules (grey levels):
    grey '3' if the chroma is < 0.12 of the tint; green '1' if G exceeds both R and B by > 15; magenta '4' if
    R-G > 15 and B-G > 15; red '7' if R-G > 30 and B-G <= 15; blue '2' if B-G > 15 and |R-G| <= 15;
    otherwise 'mixed'. Returns (label, alpha, hue cosine to that label's legend colour).
    """
    tint = 255.0 - p.mean()
    q = p - p.mean()
    r, gg, b = p
    dr, db = r - gg, b - gg
    if np.linalg.norm(q) < 0.12 * tint:
        key = "3"
    elif gg - r > 15 and gg - b > 15:
        key = "1"
    elif dr > 15 and db > 15:
        key = "4"
    elif dr > 30 and db <= 15:
        key = "7"
    elif db > 15 and abs(dr) <= 15:
        key = "2"
    else:
        key = "mixed"
    C = np.array(LEG[key] if key != "mixed" else LEG["1"])
    cq = C - C.mean()
    cos = float(np.dot(q, cq) / (np.linalg.norm(q) * np.linalg.norm(cq) + 1e-9)) if key not in ("3", "mixed") else float("nan")
    return key, float(min(1, tint / (255 - C.mean()))), cos


line_rows = []
for orient in ("vertical", "horizontal"):
    clean = []
    for i in range(n):
        far = np.abs(np.arange(n) - i) > 20
        if orient == "vertical":
            px = sub[np.where(~linerows & far)[0], i]
        else:
            px = sub[i, np.where(~linecols & far)[0]]
        clean.append(np.median(px, axis=0))
    clean = np.array(clean)
    tint = 255 - clean.min(1)
    cls = []
    for i in range(n):
        if tint[i] <= 40 or i < 2 or i > n - 3:      # skip the pixels next to the frame lines
            cls.append(None)
            continue
        cls.append(unmix(clean[i]))
    i = 0
    while i < n:
        if cls[i] is None:
            i += 1
            continue
        j = i
        while j + 1 < n and cls[j + 1] is not None and cls[j + 1][0] == cls[i][0]:
            j += 1
        pix = np.arange(i, j + 1)
        w = np.array([cls[q][1] for q in pix])
        centre = float(np.average(pix, weights=w))
        p0 = (m["cols"][0] if orient == "vertical" else m["rows"][0]) + centre
        idx = float(fx(p0)) if orient == "vertical" else float(fy(p0))
        line_rows.append((orient, cls[i][0], round(idx, 1), round(p0, 2), j - i + 1,
                          round(float(w.max()), 3), round(float(np.nanmin([cls[q][2] for q in pix])) if not all(np.isnan(cls[q][2]) for q in pix) else float("nan"), 3)))
        i = j + 1

# the matrix is symmetric, so each vertical line should have a horizontal partner at the same index
V = [(c, idx) for o, c, idx, *_ in line_rows if o == "vertical"]
Hh = [(c, idx) for o, c, idx, *_ in line_rows if o == "horizontal"]
same = sum(1 for c, i in V if any(c2 == c and abs(i2 - i) <= 2 for c2, i2 in Hh))
anyl = sum(1 for c, i in V if any(abs(i2 - i) <= 2 for c2, i2 in Hh))
counts = {}
for o, c, *_ in line_rows:
    counts[(o, c)] = counts.get((o, c), 0) + 1
write_csv(os.path.join(HERE, "sfig2-1c_lines.csv"), [
    "Templier 2019 eLife 8:e45696, Figure 2—figure supplement 1c: coloured lines drawn over the matrix.",
    "  The legend between panels b and d shows five line colours labelled 1, 2, 3, 4, 7 (green, blue, dark grey,",
    "  magenta, red); the paper's text and legend do not say what the lines mark.",
    "Columns: orientation (vertical line = constant column index, horizontal = constant row index); legend_label",
    "  (1, 2, 3, 4, 7, or 'mixed' where two colours share a pixel); index = section index of the line centre (x index",
    "  for vertical, y index for horizontal lines); pixel = its position in the image (column or row); width_px =",
    "  number of adjacent pixels merged into this line; alpha = darkening of the line relative to its legend colour",
    "  (tint / tint of the legend swatch; JPEG desaturation and partial pixel coverage make it < 1); hue_cos = cosine",
    "  between the line's chroma vector and the legend colour's (1 = same hue; lowest over the merged pixels; empty",
    "  for grey and mixed). Classification rules (signs of R-G and B-G) are in the docstring of unmix().",
    "Provenance: tier 3, digitized from fig2-figsupp1.jpg by sfig2-1_extract.py (method in its docstring).",
    "Uncertainty: +-1.5 sections in index. One pixel spans ~1.35 sections, so adjacent lines merge (width_px > 1)",
    "  and the list is a lower bound of the number of lines drawn. Lines in the dark diagonal band are not seen.",
    "Counts detected (orientation, label): " + ", ".join(f"{o[0]}{c}={v}" for (o, c), v in sorted(counts.items())),
    f"Symmetry check: of {len(V)} vertical lines, {anyl} have a horizontal line within 2 sections of the same index,",
    f"  {same} of them with the same label; the mismatches show the limits of the colour classification.",
], ["orientation", "legend_label", "index", "pixel", "width_px", "alpha", "hue_cos"],
    [tuple(str(x) if not isinstance(x, float) else x for x in r) for r in line_rows], fmt="{:.4g}")
print("sfig2-1c_lines.csv", len(line_rows), "lines;", counts)
lp = []
for o, c, idx, p0, wpx, al, res in line_rows:
    if o == "vertical":
        lp += [(p0, rr) for rr in range(m["rows"][0] - 12, m["rows"][0] - 3)]
    else:
        lp += [(cc, p0) for cc in range(m["cols"][0] - 12, m["cols"][0] - 3)]
overlay(a.astype(np.uint8), lp, os.path.join(WORK, "sfig2-1c_lines_overlay.png"))

# ---------------------------------------------------------------- bar chart d
yt = ticks(g[540:812, 511:515].mean(1), 540, thr=235)
assert len(yt) == 5, yt
fyd, ydres, yds = fit_axis(yt, [400, 300, 200, 100, 0])
xt = ticks(g[808:815, 520:880].mean(0), 520, thr=235)
assert len(xt) == 8, xt
y0 = float(yt[-1])                     # row of the zero tick = x-axis line
fill = np.median(a[700:800, 552:562].reshape(-1, 3), axis=0)     # bar fill colour (inside bar 0)
PRINTED = [375, 103, 26, 7, 1, 0, 0, 1]
drow, dpts = [], []
for k, xc in enumerate(xt):
    cols_ = np.arange(int(round(xc)) - 4, int(round(xc)) + 5)
    col_s = []
    for c in cols_:
        px = a[540:int(y0), c]                        # rows above the axis-line row
        al = np.clip((255.0 - px[:, 0]) / (255.0 - fill[0]), 0, 1) * (px[:, 2] - px[:, 0] > 30)
        col_s.append(al.sum())
    S = float(np.median(col_s))
    top = (y0 - 0.5) - S
    v = float(fyd(top))
    drow.append((str(k), v, str(PRINTED[k])))
    dpts += [(c, top) for c in cols_]
overlay(a.astype(np.uint8), dpts, os.path.join(WORK, "sfig2-1d_overlay.png"))
write_csv(os.path.join(HERE, "sfig2-1d.csv"), [
    "Templier 2019 eLife 8:e45696, Figure 2—figure supplement 1d: bar chart (no axis titles). Categories 0-7 on the",
    "  x axis, counts 0-400 on the y axis; the value of each bar is printed above it. The legend calls panel d the",
    "  'Similarity matrix of the reordered sections'; the image shows this bar chart instead (see the README).",
    "Columns: category = x tick label (0-7); height_read = bar height digitized (y units); printed_value = the",
    "  number printed above the bar (transcribed from the image, exact).",
    "Provenance: height_read is tier 3, digitized from fig2-figsupp1.jpg by sfig2-1_extract.py: summed blue",
    f"  coverage of the bar's central 9 columns above the axis; y fit on 5 ticks (0-400), max residual {ydres:.2f}.",
    f"Uncertainty of height_read: about +-{abs(yds):.1f} (1 px). printed_value sum = {sum(PRINTED)}.",
], ["category", "height_read", "printed_value"], drow, fmt="{:.4g}")
print("sfig2-1d.csv", [(r[0], round(r[1], 1), r[2]) for r in drow])

