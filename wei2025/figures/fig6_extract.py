"""Digitize Figure 6 (a-f) of Wei et al. 2025 (PDF p. 7): indentation force Fz vs indenter displacement hz.

Source: the embedded 300 ppi raster of Figure 6 (2100 x 1175 px, lossless); no vector data in the PDF.
    python3 -I -B figures/fig6_extract.py  -> figures/fig6a.csv ... fig6f.csv, work/fig6?_overlay.png

Each panel is an Origin line+symbol plot. Symbols (the sampled data) are found by template matching with
the panel's own legend symbol; the smoothed connecting line is traced as every run of line-coloured pixels
in each pixel column (the loading/unloading loop is multivalued in x).
"""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
from digitize_common import embedded_image, write_csv  # noqa: E402
from figA_axes import refine_frame, ticks, fit  # noqa: E402
from figA_markers import (legend_template, line_mask, column_runs, series_mask, dt_peaks,  # noqa: E402
                         ncc_peaks_gray, merge_points, candidate_scores, draw_cross)

PDF = HERE.parent / "source" / "wei2025.pdf"
WORK = HERE.parent / "work"
WORK.mkdir(exist_ok=True)

a = embedded_image(str(PDF), 7, bbox_near=(45.5, 32.5, 549.5, 314.3))
dark = a.astype(float).mean(2) < 110

# panel: approximate frame (left, right, top, bottom) in px, legend name, series colour, y labels of the
# major ticks from top to bottom, value at the top frame line, text boxes to exclude (c0, c1, r0, r1)
P = {
    "a": dict(box=(79, 670, 3, 438), name="Pyramid-0°", col=(0, 0, 0), ylab=[15, 12, 9, 6, 3, 0, -3],
              excl=[(428, 546, 154, 192), (628, 664, 155, 280), (362, 512, 383, 416)]),
    "b": dict(box=(785, 1377, 3, 438), name="Pyramid-45°", col=(255, 0, 0), ylab=[15, 12, 9, 6, 3, 0, -3], excl=[]),
    "c": dict(box=(1492, 2084, 6, 441), name="Sphere (R=14.5 Å)", col=(255, 0, 255), ylab=[15, 12, 9, 6, 3, 0, -3], excl=[]),
    "d": dict(box=(79, 670, 614, 1048), name="Sphere (R=10 Å)", col=(0, 0, 255), ylab=[15, 12, 9, 6, 3, 0, -3], excl=[]),
    "e": dict(box=(784, 1375, 613, 1048), name="Sphere (R =20 Å)", col=(128, 128, 0), ylab=[30, 25, 20, 15, 10, 5, 0, -5], excl=[]),
    "f": dict(box=(1500, 2084, 618, 1048), name="Sphere (R=25 Å)", col=(128, 0, 255), ylab=[40, 30, 20, 10, 0], excl=[]),
}
XLAB = [0, 10, 20, 30, 40]   # labelled major ticks inside the frame; the right frame line is the 50 tick
R_MARK = 6                   # symbol radius in px (legend symbol 12 px across)


def calib(k, p):
    fr = refine_frame(dark, p["box"])
    L, R, T, B = fr
    bx = [t for t, n in ticks(dark, fr, "bottom") if n >= 6]
    ly = [t for t, n in ticks(dark, fr, "left") if n >= 6]
    assert len(bx) == len(XLAB), (k, bx)
    assert len(ly) == len(p["ylab"]), (k, ly)
    mx, bxx, rx = fit(bx, XLAB)
    my, byy, ry = fit(ly, p["ylab"])
    chk_x = mx * R + bxx           # should be 50
    return fr, (mx, bxx, rx, chk_x), (my, byy, ry), bx, ly


for k, p in P.items():
    fr, (mx, bxx, rx, chk_x), (my, byy, ry), bx, ly = calib(k, p)
    L, R, T, B = fr
    X = lambda c: mx * np.asarray(c) + bxx  # noqa: E731
    Y = lambda r: my * np.asarray(r) + byy  # noqa: E731
    Li, Ri, Ti, Bi = int(L), int(R), int(T), int(B)
    legbox = (Li + 30, Li + 330, Ti + 30, Ti + 110)
    T_, (cx, cy), _ = legend_template(a, (Li + 40, Li + 140, Ti + 40, Ti + 110))
    excl = [legbox] + p["excl"]
    region = (Li + 3, Ri - 2, Ti + 3, Bi - 2)
    sm = series_mask(a, p["col"])
    cand = merge_points(dt_peaks(sm, region, thr=4.0),
                        ncc_peaks_gray(a, (int(round(cx)), int(round(cy))), region, thr=0.45))
    cand = np.array([c for c in cand if not any(e[0] <= c[0] <= e[1] and e[2] <= c[1] <= e[3] for e in excl)])
    # accept a candidate if it is clearly symbol-like by either test, or moderately by both
    scs = candidate_scores(a, sm, (int(round(cx)), int(round(cy))), cand[:, :2])
    ok = np.array([(d >= 4.5) or (n >= 0.6) or (d >= 4.0 and n >= 0.45) for d, n in scs], bool)
    cand = cand[ok]

    # holding stack at hz = 45 Å: vertical extents of (i) rows where the series is >= 8 px wide within
    # +-9 px of the hz = 45 column and (ii) symbol candidates there (centre +-6 px). Overlapping extents are
    # merged; a merged extent >= 29 px tall (>= ~3 overlapping symbols) is a stack.
    c45 = (45 - bxx) / mx
    band = sm[:, int(c45) - 9:int(c45) + 10]
    wide = band.sum(1) >= 8
    wide[:Ti + 3] = False
    wide[Bi - 2:] = False
    ext = []
    r = 0
    while r < len(wide):
        if wide[r]:
            r2 = r
            while r2 + 1 < len(wide) and wide[r2 + 1]:
                r2 += 1
            ext.append((r, r2))
            r = r2 + 1
        else:
            r += 1
    near = [i for i, c in enumerate(cand) if abs(c[0] - c45) <= 9]
    ext += [(cand[i][1] - R_MARK, cand[i][1] + R_MARK) for i in near]
    ext.sort()
    merged = []
    for e0, e1 in ext:
        if merged and e0 <= merged[-1][1] + 2:
            merged[-1][1] = max(merged[-1][1], e1)
        else:
            merged.append([e0, e1])
    stacks = [(e0 + R_MARK, e1 - R_MARK, 0) for e0, e1 in merged if e1 - e0 + 1 >= 29]
    in_stack = np.array([abs(c[0] - c45) <= 9 and any(t - 3 <= c[1] <= b_ + 3 for t, b_, _ in stacks)
                         for c in cand], bool)
    mk = cand[~in_stack]
    xs, ys = X(mk[:, 0]), Y(mk[:, 1])
    src = ["dt" if v == 0 else "ncc" for v in mk[:, 2]]

    rows = []
    for i in np.argsort(xs):
        rows.append(["symbol", float(xs[i]), float(ys[i]), "", "", "", src[i], round(float(xs[i]))])
    stack_rows = []
    for yt_px, yb_px, nmem in stacks:
        yt, yb = Y(yt_px), Y(yb_px)
        stack_rows.append(["symbol_stack", 45.0, float((yt + yb) / 2), float(yt), float(yb), "", "", 45, "stack"])

    # upper/lower within each 1 Å bin of hz (symbols are 1 Å apart)
    bins = {}
    for r_ in rows:
        bins.setdefault(r_[7], []).append(r_)
    for b, rs in bins.items():
        if len(rs) == 1:
            rs[0].append("single")
        else:
            rs.sort(key=lambda r_: -r_[2])
            rs[0].append("upper")
            for r_ in rs[1:-1]:
                r_.append("middle")
            rs[-1].append("lower")
    sym = rows
    rows = rows + stack_rows

    # line trace: line-coloured pixels minus symbols, legend and text
    lm = line_mask(a, p["col"], t_min=0.6, resid_max=90 if k == "a" else 70)
    yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]
    for x0, y0, _ in cand:  # symbols (stack members included)
        lm[(xx - x0) ** 2 + (yy - y0) ** 2 <= (R_MARK + 1) ** 2] = False
    for e in excl:
        lm[e[2]:e[3] + 1, e[0]:e[1] + 1] = False
    runs = column_runs(lm, Li + 13, Ri - 3, Ti + 4, Bi - 12, min_len=2)  # skip the inward ticks
    line_rows = [["line", float(X(c)), float(Y(r)), "", "", n, "", "", ""] for c, r, n in runs]

    out_rows = rows + line_rows
    out_rows.sort(key=lambda r: (r[0] != "symbol", r[0] != "symbol_stack", r[1]))
    xu = abs(mx) * 1.0
    yu = abs(my) * 1.0
    write_csv(str(HERE / f"fig6{k}.csv"), [
        f"Wei et al. 2025, Figure 6({k}): indentation force Fz (nN) vs displacement of the indenter hz (Å), series '{p['name']}'.",
        "Columns: kind = symbol (a plotted data symbol), symbol_stack (overlapping symbols at hz = 45 Å, the holding stage, that",
        "  cannot be separated: hz = 45 (the holding stage), Fz = midpoint, Fz_top/Fz_bottom = centres of its top and bottom",
        "  symbol; the number of samples in the stack cannot be counted), line (the smoothed connecting curve: centre of one",
        "  vertical run of line pixels in one pixel column; several rows per column where the loop is multivalued; n_px = run length in px);",
        "  hz_A, Fz_nN = position; found_by = which detector produced the candidate (dt or ncc); hz_bin = nearest whole Å (the symbols are 1 Å apart);",
        "  branch = position of the symbol among those in the same 1 Å bin (upper/lower/middle/single). In the figure the upper",
        "  branch of the loop is the loading curve and the lower the unloading curve (panel (a) labels them 'Loading' and 'Unloading');",
        "  for hz < ~20 Å both branches lie on Fz = 0 and their symbols overlap, so a bin there may hold one or two symbols.",
        "Provenance: tier 3, digitized by fig6_extract.py from the embedded 300 ppi raster (no vector data in the PDF).",
        "  Symbols (12 px discs): candidates = peaks of the distance transform (DT) of the series-colour mask (the line is",
        "  ~5 px wide) and grayscale template matches (NCC) with the panel's own legend symbol; kept if DT >= 4.5 px or",
        "  NCC >= 0.6 or (DT >= 4.0 and NCC >= 0.45); stack = overlapping symbols",
        "  (merged vertical extent >= 29 px, i.e. >= ~3 symbols) within +-9 px of hz = 45 Å. Line: pixels on the white-to-series-colour mixing line, with symbols, legend and text removed.",
        f"Calibration: x on the 5 labelled major ticks 0-40 Å (max residual {rx:.3f} Å; the right frame line maps to {chk_x:.2f}, labelled 50);",
        f"  y on the {len(p['ylab'])} labelled major ticks {p['ylab'][0]} to {p['ylab'][-1]} nN (max residual {ry:.3f} nN).",
        f"Plot frame: hz {X(L):.2f} to {X(R):.2f} Å, Fz {Y(B):.2f} to {Y(T):.2f} nN (linear axes).",
        f"Uncertainty: about +-{2 * xu:.2f} Å in x and +-{2 * yu:.2f} nN in y (2 px) for symbols; line rows +-{3 * yu:.2f} nN",
        "  (the line is ~5 px wide). Symbols partly hidden by other symbols may be missed or slightly displaced. The line is",
        "  mostly covered by the symbols (1 Å apart = ~10.7 px, symbols 12 px across), so line rows exist mainly on steep parts.",
    ] + (["Panel (a): the shaded ellipses (Loading, blue; Holding, orange; Unloading, green) and their labels are annotations,",
          "  not data; text boxes were masked out, so line pixels under the labels are missing."] if k == "a" else []),
        ["kind", "hz_A", "Fz_nN", "Fz_top_nN", "Fz_bottom_nN", "n_px", "found_by", "hz_bin", "branch"], out_rows,
        fmt=["{}", "{:.3f}", "{:.3f}", "{:.3f}", "{:.3f}", "{}", "{}", "{}", "{}"])

    # overlay: symbols as + crosses (magenta), line centres (cyan dots)
    from PIL import Image
    im = a.copy()
    lc = (0, 160, 255) if k in ("a", "e") else (0, 0, 0)
    sc_ = (255, 0, 255) if k in ("a", "d", "e") else (0, 200, 0)
    for c, r, _ in runs:
        im[int(round(r)), int(c)] = lc
    for yt_px, yb_px, _ in stacks:
        for yy_ in (yt_px, yb_px):
            im[int(round(yy_)), int(c45) - 9:int(c45) + 10] = (255, 140, 0)
    for x0, y0, _ in mk:
        draw_cross(im, x0, y0, sc_, size=5, thick=1)
    Image.fromarray(im[Ti - 3:Bi + 4, Li - 3:Ri + 4]).save(WORK / f"fig6{k}_overlay.png")
    print(k, "frame", fr, "x res", round(rx, 3), "right frame ->", round(chk_x, 2), "y res", round(ry, 3),
          "symbols", len(sym), "stacks", [(round(float(Y(a0)), 2), round(float(Y(a1)), 2)) for a0, a1, _ in stacks], "line pts", len(runs))
