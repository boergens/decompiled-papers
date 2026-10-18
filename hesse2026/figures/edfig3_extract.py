"""edfig3_extract.py -- recover Extended Data Figure 3 (PDF page 43) panels a-f.
Run from this folder: python3 edfig3_extract.py
Writes: edfig3a_r{1-5}_{gt_conscious,recon_state1,gt_suppressed,recon_state2}.png (Monkey A),
        edfig3d_r{1-5}_... (Monkey M), edfig3{b,c,e,f}.csv, *_orig.png (300-dpi crops), *_overlay.png (QA).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # sibling helper modules (python3 -I adds no path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # file names below are relative to figures/
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import edfig_extract_lib as L  # noqa: E402
from edfig_extract_lib import pp, fitz, fmt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
PAGE = 43
page = pp.open_page(L.PDF, PAGE)

# ---------------------------------------------------------------- panels a, d: face grids (5 rows x 4 columns each)
COLNAMES = ["gt_conscious", "recon_state1", "gt_suppressed", "recon_state2"]


def visible_image(bbox, cands):
    """Several image XObjects are stacked on the same cell in the Monkey M grid; render the cell and
    pick the candidate that matches. Returns (xref, diff of best, diff of second best)."""
    r = fitz.Rect(*bbox)
    pix = page.get_pixmap(clip=r, matrix=fitz.Matrix(143 / r.width, 143 / r.height))
    A = np.asarray(Image.frombytes("RGB", (pix.width, pix.height), pix.samples).convert("L"), float)
    scores = []
    for x in cands:
        tmp = f"/tmp/claude-1000/cand_{x}.png"
        os.makedirs(os.path.dirname(tmp), exist_ok=True)
        pp.extract_image(page, x, tmp)
        B = np.asarray(Image.open(tmp).convert("L").resize(A.shape[::-1]), float)
        os.remove(tmp)
        scores.append((float(np.abs(A - B).mean()), x))
    scores.sort()
    return scores[0][1], scores[0][0], (scores[1][0] if len(scores) > 1 else None)


def face_grid(panel, clip, col_x):
    print(f"== panel {panel}: face grid")
    ims = pp.images(page, clip)
    groups = []
    for y in sorted(im["bbox"][1] for im in ims):
        if not groups or y - groups[-1][-1] > 3:
            groups.append([y])
        else:
            groups[-1].append(y)
    rows_y = [float(np.mean(g)) for g in groups]
    assert len(rows_y) == 5, rows_y
    cells = {}
    for im in ims:
        x0, y0 = im["bbox"][0], im["bbox"][1]
        c = min(range(4), key=lambda i: abs(col_x[i] - x0))
        r = min(range(len(rows_y)), key=lambda i: abs(rows_y[i] - y0))
        cells.setdefault((r, c), []).append(im)
    assert len(cells) == 20, len(cells)
    for (r, c) in sorted(cells):
        ims_c = cells[(r, c)]
        xrefs = sorted(set(im["xref"] for im in ims_c))
        bbox = ims_c[-1]["bbox"]
        xref, best, second = visible_image(bbox, xrefs)
        out = f"edfig3{panel}_r{r+1}_{COLNAMES[c]}.png"
        w, h = pp.extract_image(page, xref, out)
        note = "" if len(xrefs) == 1 else f"  [stacked placements {len(ims_c)}, xrefs {xrefs}: render matches {xref} (mean|diff| {best:.1f} vs next {second:.1f})]"
        print(f"  row {r+1} col {c+1} {COLNAMES[c]:14s} xref {xref} -> {out} ({w}x{h}){note}")


face_grid("a", pp.R(10, 50, 250, 322), [13.9, 73.9, 133.5, 193.4])
face_grid("d", pp.R(265, 50, 505, 322), [270.7, 330.7, 390.3, 450.2])
pp.render(page, pp.R(5, 17, 250, 322), 300, "edfig3a_orig.png")
pp.render(page, pp.R(262, 17, 507, 322), 300, "edfig3d_orig.png")

# ---------------------------------------------------------------- plot panels
BLACK, ORANGE, PURPLE = "#1c0f29", "#fcae34", "#543379"
VAR_SERIES = [  # in the PDF's draw order
    dict(name="priming_average", color=BLACK, style="solid"),
    dict(name="binocular_conscious_state1", color=ORANGE, style="solid"),
    dict(name="binocular_suppressed_state1", color=ORANGE, style="dashed"),
    dict(name="binocular_conscious_state2", color=PURPLE, style="solid"),
    dict(name="binocular_suppressed_state2", color=PURPLE, style="dashed"),
]
DEC_SERIES = [dict(s, band=True) for s in VAR_SERIES]
QC_VAR = ("direct = vertex inside a dash (precision ~0.05 pt = 0.1 %); extrap = vertex in a gap, extrapolated along the adjacent straight segment (~0.1-0.4 pt); "
          "extrap_offscale = same but outside the -100..100 range (line clipped by the axes box; ~1-2 pt); interp = both adjacent segments inside one dash gap, linear interpolation of the neighbours (bound ~1.2 pt = 2.2 %); "
          "clipped = line outside the axis range (empty); gap = not recoverable (empty).")
QC_DEC = ("band_mid = value is the midpoint of the shaded band, which is exactly symmetric about the line (precision ~0.01 pt; used wherever both band edges are unclipped). "
          "Other codes (band edge clipped there, value from the dash polygons): direct = vertex inside a dash (~0.05 pt), extrap = extrapolated along the adjacent straight segment (~0.1-0.4 pt), interp = linear interpolation of the neighbours (bound ~1.2 pt), "
          "band = band collapses onto the line / lies entirely at the 0 boundary, gap/clipped = empty.")


def variance_panel(panel, monkey, clip, xreg, yreg, crop):
    print(f"== panel {panel}: explained variance ({monkey})")
    r = L.extract_panel(page, clip, [10, 20, 30, 40, 50], xreg, [-100, -50, 0, 50, 100], yreg, VAR_SERIES, 50)
    L.overlay_png(page, clip, r, VAR_SERIES, f"edfig3{panel}_overlay.png")
    pp.render(page, crop, 300, f"edfig3{panel}_orig.png")
    d = r["data"]
    hdr = ["feature_index", "feature_set", "priming_average", "binocular_conscious_state1", "binocular_conscious_state2",
           "binocular_suppressed_state1", "binocular_suppressed_state1_qc", "binocular_suppressed_state2", "binocular_suppressed_state2_qc"]
    rows = []
    for k in range(50):
        rows.append([k + 1, "shape" if k < 20 else "appearance", fmt(d["priming_average"]["y"][k]),
                     fmt(d["binocular_conscious_state1"]["y"][k]), fmt(d["binocular_conscious_state2"]["y"][k]),
                     fmt(d["binocular_suppressed_state1"]["y"][k]), d["binocular_suppressed_state1"]["code"][k],
                     fmt(d["binocular_suppressed_state2"]["y"][k]), d["binocular_suppressed_state2"]["code"][k]])
    comments = [
        f"Extended Data Figure 3{panel} (PDF page 43): explained variance of face features (%) vs feature index, sessions from {monkey} only; states inferred from one half of the neurons, features predicted from the held-out half.",
        f"Source: vector paths in the PDF. Clip region (PDF pt, origin top-left) x {clip.x0:g}-{clip.x1:g}, y {clip.y0:g}-{clip.y1:g}.",
        f"x axis: tick marks at features 10,20,30,40,50 -> slope {r['xax'].slope:.6f} pt^-1, max residual {r['xax'].resid:.2e}; every series has one vertex per feature 1..50 (checked against the solid strokes, max dev <0.01 pt).",
        f"y axis: tick marks at -100,-50,0,50,100 % -> slope {r['yax'].slope:.6f}, max residual {r['yax'].resid:.2e}. 1 pt = {abs(r['yax'].slope):.3f} %.",
        "feature_set: features 1-20 = 20 principal shape features, 21-50 = 30 principal appearance features ('Shape'/'Appearance' brackets in the figure).",
        "Solid lines (stroke vertices, precision ~0.01 pt): priming_average (black #1c0f29), binocular_conscious_state1 (orange #fcae34), binocular_conscious_state2 (purple #543379; the legend swatch uses #6d429c).",
        "Dashed lines binocular_suppressed_state1 (orange dashed) and binocular_suppressed_state2 (purple dashed) are stored as filled dash outlines (4 pt dash / 4 pt gap, 1 pt wide); centreline recovered from the dash polygons (see README). *_qc codes: " + QC_VAR,
        "Values are rounded to 0.01 %.",
    ]
    pp.write_csv(f"edfig3{panel}.csv", hdr, rows, comments)
    print(f"  wrote edfig3{panel}.csv")


def decoding_panel(panel, monkey, clip, xreg, yreg, crop):
    print(f"== panel {panel}: decoding accuracy ({monkey})")
    r = L.extract_panel(page, clip, [0, 20, 40, 60], xreg, [0, 20, 40, 60, 80, 100], yreg, DEC_SERIES, 60)
    L.overlay_png(page, clip, r, DEC_SERIES, f"edfig3{panel}_overlay.png")
    pp.render(page, crop, 300, f"edfig3{panel}_orig.png")
    d = r["data"]
    hdr = ["n_faces"]
    for s in DEC_SERIES:
        hdr += [s["name"], s["name"] + "_lo", s["name"] + "_hi"]
        if s["style"] == "dashed":
            hdr.append(s["name"] + "_qc")
    band_notes = []
    for s in DEC_SERIES:
        dd = d[s["name"]]
        for k in range(60):
            if dd["bflag"][k] == "absent":
                dd["lo"][k] = dd["hi"][k] = dd["y"][k]
        for key, label in (("hi_clipped", "upper edge clipped at 100 (true value above 100)"),
                           ("lo_clipped", "lower edge clipped at 0 (true value below 0)"),
                           ("degenerate", "band has zero height (upper = lower = line)"),
                           ("absent", "band not drawn (entirely at/below the 0 boundary): lo = hi = line value")):
            ks = [k + 1 for k in range(60) if key in dd["bflag"][k]]
            if ks:
                band_notes.append(f"{s['name']} band, n_faces {ks}: {label}.")
    rows = []
    for k in range(60):
        row = [k + 1]
        for s in DEC_SERIES:
            dd = d[s["name"]]
            row += [fmt(dd["y"][k]), fmt(dd["lo"][k]), fmt(dd["hi"][k])]
            if s["style"] == "dashed":
                row.append(dd["code"][k])
        rows.append(row)
    comments = [
        f"Extended Data Figure 3{panel} (PDF page 43): Euclidean-distance decoding accuracy (%) of the conscious (solid) and suppressed (dashed) face vs number of faces, sessions from {monkey} only; states from one half of the neurons, decoding on the held-out half.",
        f"Source: vector paths in the PDF. Clip region (PDF pt, origin top-left) x {clip.x0:g}-{clip.x1:g}, y {clip.y0:g}-{clip.y1:g}.",
        f"x axis: tick marks at 0,20,40,60 faces -> slope {r['xax'].slope:.6f}, max residual {r['xax'].resid:.2e}; every series has one vertex per n_faces = 1..60 (checked against the solid strokes).",
        f"y axis: tick marks at 0,20,...,100 % -> slope {r['yax'].slope:.6f}, max residual {r['yax'].resid:.2e}. 1 pt = {abs(r['yax'].slope):.3f} %.",
        "Columns: <series> = plotted line; <series>_lo / <series>_hi = lower / upper edge of the shaded band (filled polygon, alpha 0.2; the legend does not say what the band is - the related main-figure panels use SD).",
        "Solid lines (stroke vertices, ~0.01 pt): priming_average (black #1c0f29), binocular_conscious_state1 (orange #fcae34), binocular_conscious_state2 (purple #543379).",
        "Dashed lines binocular_suppressed_state1 (orange dashed), binocular_suppressed_state2 (purple dashed): stored as filled dash outlines (4 pt dash / 4 pt gap). *_qc codes: " + QC_DEC,
        "  Agreement of the independent dash-outline centreline recovery with the band midpoints (dash-recovery code: n vertices, max |difference| pt): " + "; ".join(f"{s['name']}: " + ", ".join(f"{c} ({n}, {m:.2f})" for c, (n, m) in sorted(d[s['name']]['agree'].items())) for s in DEC_SERIES if s['style'] == 'dashed') + ".",
        "Bands are clipped by the axes box (0..100 %); clipped edges are written as the clip value:",
    ] + ["  " + n for n in band_notes] + ["Values are rounded to 0.01 %."]
    pp.write_csv(f"edfig3{panel}.csv", hdr, rows, comments)
    print(f"  wrote edfig3{panel}.csv")


variance_panel("b", "monkey A", pp.R(27, 328, 128, 452), pp.R(27, 446.5, 128, 450.5), pp.R(27, 334, 32, 448), pp.R(0, 318, 130, 468))
decoding_panel("c", "monkey A", pp.R(152, 328, 253, 452), pp.R(150, 445.7, 253, 449.5), pp.R(152, 333, 157, 447), pp.R(128, 318, 265, 468))
variance_panel("e", "monkey M", pp.R(284, 328, 385, 452), pp.R(284, 446.5, 385, 450.5), pp.R(284, 334, 289, 448), pp.R(258, 318, 388, 468))
decoding_panel("f", "monkey M", pp.R(409, 328, 510, 452), pp.R(407, 445.7, 510, 449.5), pp.R(409, 333, 414, 447), pp.R(385, 318, 519, 468))
print("done")
