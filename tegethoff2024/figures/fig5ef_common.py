"""Shared code for Figure 5E and 5F (markers with error bars): see fig5e_extract.py / fig5f_extract.py."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tg_common import *  # noqa: E402,F403


def extract(panel, approx, fx, fy, sy, sx, ylabel, header, ycol):
    a = img(7)
    rows, pts = [], []
    for name, kind, x, y, note in approx:
        m = series_mask(a, RESIN_RGB[RESINS.index(name)])
        cxc, cyc, cxb, cyb = refine_marker(m, x, y)
        cx, cy = (cxc, cyc) if kind == "filled" else (cxb, cyb)
        top, bot = bar_ends(m, cx, cy)
        has_bar = (cy - top) > 9 or (bot - cy) > 9
        up, down = cy - top, bot - cy
        flag = note
        if has_bar and abs(up - down) > 0.08 * max(up, down) + 1:
            flag = (flag + "; " if flag else "") + "bar asymmetric (overlaps another bar or marker?)"
        if not has_bar:
            top = bot = float("nan")
            flag = (flag + "; " if flag else "") + "no bar visible beyond the marker"
        rows.append((name, "50 nm" if kind == "filled" else "35 nm", kind, float(fx(cx)), float(fy(cy)),
                     float(fy(bot)) if has_bar else float("nan"), float(fy(top)) if has_bar else float("nan"), flag))
        pts += [(cx, cy)] + ([(cx, top), (cx, bot)] if has_bar else [])
    save(mark(a, pts, r=2), f"fig5{panel}_overlay.png")
    write_csv(os.path.join(HERE, f"fig5{panel}.csv"), header + [
        "Columns: series = resin (colour key of Figure 5B); thickness = 50 nm (filled circles) or 35 nm (open squares), per",
        f"  the caption; marker; hardness_HV = x of the marker centre; {ycol} = y of the marker centre;",
        "  bar_low / bar_high = lower and upper end of its vertical error bar (not defined in the caption; the main text,",
        "  p.7, says of Figure 5E 'see standard deviation around the mean'; the bars are symmetric about the markers);",
        "  flag = notes.",
        "Provenance: tier 3, digitized from the embedded ~310 ppi JPEG (no vector data in the PDF) by fig5"
        + panel + "_extract.py:",
        "  approximate marker positions were picked by eye from a 2x zoom, then refined on the series colour mask",
        "  (centroid for circles, outline bounding box for squares); bar ends = last pixel of the series colour along the",
        "  marker's column (antialiased thin bars matched to the series colour blended with white).",
        f"Uncertainty: +-{2 * abs(sy):.2f} {ylabel} in y and +-{2 * abs(sx):.3f} HV in x (2 px).",
    ], ["series", "thickness", "marker", "hardness_HV", ycol, "bar_low", "bar_high", "flag"], rows)
    for r in rows:
        print(r)
    return rows
