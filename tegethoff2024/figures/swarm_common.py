"""Shared driver for the beeswarm panels (Figure 5A-D, Figure 7A-H); called by fig5?_extract.py / fig7?_extract.py.

A beeswarm puts one marker per cut, spread sideways so markers overlap less. The markers (~4.5 px across) are packed
too densely to be separated, so each swarm is given as a per-pixel-row profile: for every row of the image (one row =
a small interval of the y quantity) the number of coloured pixels of the swarm and its left/right extent. Because a
beeswarm spreads markers sideways, n_px / (area of one marker) estimates how many markers have their area in that row;
summed over the rows it estimates the number of markers in the swarm (a lower limit where markers overlap).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tg_common import *  # noqa: E402,F403

FIG7_NAMES = ["LX 112", "Spurr's", "H Epon"]


def run(panel, key, box, yticks, yvals, group_labels, title, ycol, yunit, blank=(), names=None, dot_area=15.0,
        min_gap=6, extra=()):
    a = img(key).copy()
    for (bx0, by0, bx1, by1) in blank:          # legend text etc.
        a[by0:by1, bx0:bx1] = 255
    fy, ry, sy = fit_axis(yticks, yvals)
    pal = [RESIN_RGB[RESINS.index(n)] for n in names] if names else None
    gs = swarm_groups(a, box, names=names, pal=pal, dot_area=dot_area, min_gap=min_gap)
    labels = group_labels(gs)
    assert len(labels) == len(gs), (len(labels), len(gs), [(g["series"], g["x0"]) for g in gs])
    rows, pts, summ = [], [], []
    for gi, (g, (ser, grp)) in enumerate(zip(gs, labels)):
        assert g["series"] == ser, (gi, g["series"], ser)
        for r, npx, l, rr, est in g["prof"]:
            rows.append((ser, grp, gi + 1, float(fy(r)), npx, est, l - g["xc"], rr - g["xc"]))
            pts += [(l, r), (rr, r)]
        n, q, lo, hi = summarize(g["prof"], fy)
        summ.append(f"  group {gi + 1}: {ser}, {grp}: est. markers {n:.0f}; quartiles {q[0]:.3g} / {q[1]:.3g} / {q[2]:.3g};"
                    f" range {lo:.3g} to {hi:.3g}; colour share {g['share']:.2f}")
    overlay(a, pts, os.path.join(WORK, f"{panel}_overlay.png"))
    write_csv(os.path.join(HERE, f"{panel}.csv"), [
        f"Tegethoff & Briggman 2024 Front Neurosci 18:1286991, {title}",
        "Beeswarm plot given as per-pixel-row profiles of each swarm (the markers are too densely packed to separate).",
        f"Columns: series = resin (colour key); group = the x-axis group; group_index = 1.. left to right;",
        f"  {ycol} = y value of the pixel row ({yunit}); n_px = coloured pixels of the swarm in that row;",
        f"  est_markers = n_px / {dot_area:g} px (area of one isolated marker): markers whose area falls in this row;",
        "  summed over a group it estimates the group size (a lower limit: markers overlap in dense swarm cores);",
        "  left_px / right_px = left and right edge of the swarm in this row, in source-image pixels from the swarm's",
        "  column centre (x has no numeric meaning within a group: it is the beeswarm's sideways spread).",
        "Provenance: tier 3, digitized from the embedded ~310-336 ppi JPEG (no vector data in the PDF) by "
        + f"{panel}_extract.py (code in swarm_common.py,",
        "  tg_common.py): groups found as column clusters of each resin colour (Lab nearest MATLAB default colour),",
        "  profiles taken from all saturated pixels in the group's columns.",
        f"  y calibrated on {len(yticks)} tick marks (max residual {ry:.3g} {yunit}).",
        f"Uncertainty: one pixel row = {abs(sy):.3g} {yunit}; marker diameter ~4.5 px = {4.5 * abs(sy):.3g} {yunit}, so a",
        "  single marker spreads over ~5 rows (profiles are smoothed by that much); JPEG blur adds ~1 px.",
        "Group summaries (from the profiles; quartiles of the estimated marker distribution):",
    ] + summ + list(extra), ["series", "group", "group_index", ycol, "n_px", "est_markers", "left_px", "right_px"], rows)
    print(panel, len(gs), "groups; y residual", ry)
    for s in summ:
        print(s)


def two_sets(order1, order2, l1, l2):
    """group_labels for panels with two blocks of groups (e.g. 50 nm then 35 nm)."""
    def f(gs):
        return [(s, l1) for s in order1] + [(s, l2) for s in order2]
    return f


def groups_from_ticks(a, box, centres, series, names, dot_area, min_sat=40):
    """Groups centred on known x tick columns; each group's columns run halfway to the neighbouring ticks."""
    x0, y0, x1, y1 = box
    m = sat(a) >= min_sat
    m[:y0], m[y1:], m[:, :x0], m[:, x1:] = False, False, False, False
    pal = [RESIN_RGB[RESINS.index(n)] for n in names]
    lab = classify(a, pal, max_dist=45, min_sat=min_sat)
    sp = np.median(np.diff(centres))
    out = []
    for i, c in enumerate(centres):
        lo = (centres[i - 1] + c) / 2 if i and c - centres[i - 1] < 1.5 * sp else c - sp / 2
        hi = (centres[i + 1] + c) / 2 if i + 1 < len(centres) and centres[i + 1] - c < 1.5 * sp else c + sp / 2
        g0, g1 = int(np.ceil(lo)), int(np.floor(hi))
        sub = lab[y0:y1, g0:g1 + 1]
        cnt = [(sub == k).sum() for k in range(len(names))]
        dom = names[int(np.argmax(cnt))]
        assert dom == series[i], (i, c, dom, series[i], cnt)
        prof = swarm_profile(m, g0, g1 + 1, y0, y1, dot_area)
        # profile extents relative to the tick column
        out.append(dict(series=dom, x0=g0, x1=g1, xc=float(c), prof=prof, share=max(cnt) / max(1, sum(cnt))))
    return out


def run_ticks(panel, key, box, yticks, yvals, centres, labels, title, ycol, yunit, names, blank=(), dot_area=14.0,
              extra=()):
    """Like run(), with the groups placed on given x tick columns (Figure 7: adjacent swarms of one colour touch)."""
    a = img(key).copy()
    for (bx0, by0, bx1, by1) in blank:
        a[by0:by1, bx0:bx1] = 255
    fy, ry, sy = fit_axis(yticks, yvals)
    gs = groups_from_ticks(a, box, centres, [l[0] for l in labels], names, dot_area)
    rows, pts, summ = [], [], []
    for gi, (g, (ser, grp)) in enumerate(zip(gs, labels)):
        for r, npx, l, rr, est in g["prof"]:
            rows.append((ser, grp, gi + 1, float(fy(r)), npx, est, l - g["xc"], rr - g["xc"]))
            pts += [(l, r), (rr, r)]
        n, q, lo, hi = summarize(g["prof"], fy)
        summ.append(f"  group {gi + 1}: {ser}, {grp}: est. markers {n:.0f}; quartiles {q[0]:.3g} / {q[1]:.3g} / {q[2]:.3g};"
                    f" range {lo:.3g} to {hi:.3g}; colour share {g['share']:.2f}")
    overlay(a, pts, os.path.join(WORK, f"{panel}_overlay.png"))
    write_csv(os.path.join(HERE, f"{panel}.csv"), [
        f"Tegethoff & Briggman 2024 Front Neurosci 18:1286991, {title}",
        "Beeswarm plot given as per-pixel-row profiles of each swarm (the markers are too densely packed to separate).",
        "Columns: series = resin (colour key); group = the x tick label of the group; group_index = 1.. left to right;",
        f"  {ycol} = y value of the pixel row ({yunit}); n_px = coloured pixels of the swarm in that row;",
        f"  est_markers = n_px / {dot_area:g} px (area of one isolated marker): markers whose area falls in this row;",
        "  summed over a group it estimates the group size (a lower limit: markers overlap in dense swarm cores);",
        "  left_px / right_px = left and right edge of the swarm in this row, in source-image pixels from the group's x",
        "  tick (x has no numeric meaning within a group: it is the beeswarm's sideways spread).",
        "Provenance: tier 3, digitized from the embedded ~336 ppi JPEG (no vector data in the PDF) by "
        + f"{panel}_extract.py (code in swarm_common.py,",
        "  tg_common.py): each group = the columns halfway to the neighbouring x ticks; profile from all saturated",
        "  pixels there; the group's resin checked against the dominant colour (MATLAB default colours).",
        f"  y calibrated on {len(yticks)} tick marks (max residual {ry:.3g} {yunit}).",
        f"Uncertainty: one pixel row = {abs(sy):.3g} {yunit}; marker diameter ~4 px = {4 * abs(sy):.3g} {yunit}, so a",
        "  single marker spreads over ~4 rows; JPEG blur adds ~1 px. Where neighbouring swarms touch, a few markers may be",
        "  counted in the wrong group.",
        "Group summaries (from the profiles; quartiles of the estimated marker distribution):",
    ] + summ + list(extra), ["series", "group", "group_index", ycol, "n_px", "est_markers", "left_px", "right_px"], rows)
    print(panel, len(gs), "groups; y residual", ry)
    for s in summ:
        print(s)
