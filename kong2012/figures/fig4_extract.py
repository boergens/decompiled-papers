"""FIG. 4 (drawing sheet 4, PDF page 5) -> figures/fig4.csv: the two bars and their error bars, digitized (tier 3).

Source: the USPTO scan, one 2560 x 3300 px 1-bit image per page (300 ppi of the letter page; the PDF declares
1 pt = 1 px). The sheet is printed sideways; the page is rendered at native resolution with PyMuPDF and rotated
90 degrees clockwise (numpy), so the chart is upright: y axis at the left with ticks at 0, 2, 4, 6, 8 and the
label "Live/.. l Cell Ratio" (defectively printed), baseline at the bottom, bar 206 (open) left, bar 208
(hatched) right, each with an error bar capped above the bar, an asterisk above bar 206.
Method: the y axis is the longest vertical dark line in the drawing box, the ticks are the short horizontal
dark runs attached to its right side; a least-squares linear map rows -> value is fitted on the five ticks (the
0 tick is the baseline). A bar's x extent is read from the dark columns just above the baseline; its top is the
highest row in which a horizontal dark run covers the bar width; the error bar's cap is the highest short
horizontal run above the top in the bar's middle columns. Uncertainty: the lines are 3-5 px wide, so about
+-2 px = +-0.02 ratio units.
Writes fig4.csv and the overlay check work/fig4_overlay.png. Run: python3 -I -B figures/fig4_extract.py (from anywhere)
"""
import os
import sys

import numpy as np
import pymupdf
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TOOLS = next(p for p in (os.path.join(ROOT, *[".."] * k, "tools") for k in range(1, 5)) if os.path.isdir(p))
sys.path.insert(0, TOOLS)
from digitize_common import fit_axis, write_csv  # noqa: E402

PDF = os.path.join(ROOT, "source", "US8109184B2.pdf")
PAGE = 5
# drawing box on the sheet as printed (x0, y0, x1, y1), native pixels (from work/make_figures.py)
BOX = (572, 1077, 2087, 2413)


def upright_page():
    doc = pymupdf.open(PDF)
    pix = doc[PAGE - 1].get_pixmap(matrix=pymupdf.Matrix(1, 1), colorspace=pymupdf.csGRAY)
    a = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width)
    return np.rot90(a, k=-1)          # 90 degrees clockwise: new_x = H-1-y, new_y = x


def runs(bool_1d):
    idx = np.where(bool_1d)[0]
    out = []
    for i in idx:
        if out and i == out[-1][1] + 1:
            out[-1][1] = i
        else:
            out.append([i, i])
    return [tuple(r) for r in out]


def main():
    g = upright_page()
    H0 = 3300
    x0, y0, x1, y1 = H0 - 1 - BOX[3], BOX[0], H0 - 1 - BOX[1], BOX[2]     # box in upright coordinates
    dark = g < 128
    sub = dark[y0:y1, x0:x1]
    # y axis: the column with the most dark pixels in the left 40 % of the box
    colsum = sub[:, : (x1 - x0) * 2 // 5].sum(0)
    ax_col = int(np.argmax(colsum))
    ax_cols = runs(colsum >= 0.8 * colsum[ax_col])
    ax_c0, ax_c1 = [r for r in ax_cols if r[0] <= ax_col <= r[1]][0]
    axis_rows = np.where(sub[:, ax_col])[0]
    # baseline: the row with the most dark pixels in the lower half
    rowsum = sub.sum(1)
    base_row = int(np.argmax(rowsum[(y1 - y0) // 2:]) + (y1 - y0) // 2)
    base_rows = [r for r in runs(rowsum >= 0.8 * rowsum[base_row]) if r[0] <= base_row <= r[1]][0]
    # ticks: short horizontal runs attached to the right of the axis line, 12..60 px long
    band = sub[:, ax_c1 + 1: ax_c1 + 60]
    tick_rows = []
    for r0, r1 in runs(band[:, :12].all(1)):
        tick_rows.append((r0 + r1) / 2)
    tick_rows = [t for t in tick_rows if axis_rows.min() - 5 <= t <= axis_rows.max() + 5]
    tick_rows = sorted(tick_rows)
    assert len(tick_rows) == 5, tick_rows
    # the lowest tick is the 0 tick on the baseline; values 8,6,4,2,0 from top
    vals = [8, 6, 4, 2, 0]
    f, resid, _slope = fit_axis(np.array(tick_rows), np.array(vals, float))   # returns (f, residual, slope)
    print("axis col", ax_c0 + x0, ax_c1 + x0, "baseline rows", base_rows[0] + y0, base_rows[1] + y0)
    print("tick rows (upright page px)", [t + y0 for t in tick_rows], "fit residual", resid)
    # bars: dark columns in the row 12 px above the baseline, right of the axis
    probe = sub[base_rows[0] - 12, ax_c1 + 60:]
    bar_runs = [(a + ax_c1 + 60, b + ax_c1 + 60) for a, b in runs(probe)]
    # group runs closer than 40 px (bar edges and hatching) into bars
    bars = []
    for a, b in bar_runs:
        if bars and a - bars[-1][1] < 220:        # the two edges of the open bar are ~190 px apart, the bars ~290
            bars[-1][1] = b
        else:
            bars.append([a, b])
    assert len(bars) == 2, bars
    rows_out = []
    pts = []
    for (bx0, bx1), label, series, hatch in zip(bars, ("206", "208"),
                                              ("vibrating, sliding-blade microtome (present invention)",
                                               "prior vibrating microtome"), ("open", "hatched")):
        cov = sub[:, bx0:bx1 + 1].mean(1)          # dark coverage of each row across the bar width
        # top edge: the first run of rows with coverage >= 0.8 above the baseline (the open bar's interior
        # and the hatching stay below 0.3; the error-bar stem in the middle columns does not matter here)
        edge_runs = [rr for rr in runs(cov >= 0.8) if rr[1] < base_rows[0] - 3]
        tr = edge_runs[-1]
        top_c = (tr[0] + tr[1]) / 2
        # error bar cap: the next run above the top edge with coverage >= 0.3 (the cap spans the bar width;
        # the asterisk above bar 206 covers < 0.25 of it)
        cap_runs = [rr for rr in runs(cov >= 0.3) if rr[1] < tr[0] - 3]
        cr = cap_runs[-1]
        cap_c = (cr[0] + cr[1]) / 2
        v, vcap = float(f(top_c)), float(f(cap_c))
        print(f"bar {label}: x {bx0 + x0}-{bx1 + x0}, top row {top_c + y0:.1f} -> {v:.3f}, cap row {cap_c + y0:.1f} -> {vcap:.3f}")
        rows_out.append([series, label, hatch, round(v, 2), round(vcap - v, 2), "*" if label == "206" else ""])
        pts += [((bx0 + bx1) / 2 + x0, top_c + y0), ((bx0 + bx1) / 2 + x0, cap_c + y0)]
    pts += [(ax_col + x0, t + y0) for t in tick_rows]
    header = [
        "FIG. 4 of US 8,109,184 B2 (drawing sheet 4, PDF page 5): bar graph of live/dead cell ratios, two bars",
        "columns: series = what the bar stands for (from the description: 206 = slices prepared with the vibrating,",
        "  sliding-blade microtome of the invention, 208 = a prior vibrating microtome); numeral = the reference numeral",
        "  printed at the bar; fill = how the bar is drawn; value = bar height (live/dead cell ratio, the y axis,",
        "  no unit); err_high = length of the error bar above the bar top (ratio units; no bar below the top is drawn);",
        "  mark = the asterisk printed above bar 206 (its meaning is not stated in the patent)",
        "provenance: tier 3, digitized from the 300-ppi bilevel scan of the sheet (figures/fig4_extract.py); axis",
        "  calibrated on the five printed ticks 0, 2, 4, 6, 8 by a least-squares line; the printed ticks are unevenly",
        "  spaced (fit residual 0.10 ratio units), so the uncertainty is about +-0.1 ratio units (the line widths alone",
        "  would give +-0.02)",
        "the x axis has no labels or ticks: the bars are categories, left = 206, right = 208",
    ]
    write_csv(os.path.join(HERE, "fig4.csv"), header, ["series", "numeral", "fill", "value", "err_high", "mark"],
              rows_out, fmt="{:.2f}")
    os.makedirs(os.path.join(ROOT, "work"), exist_ok=True)
    rgb = np.stack([g] * 3, axis=2)[y0 - 40:y1 + 40, x0 - 40:x1 + 40].copy()
    # digitize_common.overlay() draws 3 px marks, invisible on a 300-ppi scan: draw 15 px crosses instead
    for px, py in pts:
        xi, yi = int(round(px - x0 + 40)), int(round(py - y0 + 40))
        rgb[yi - 1:yi + 2, xi - 7:xi + 8] = (255, 0, 255)
        rgb[yi - 7:yi + 8, xi - 1:xi + 2] = (255, 0, 255)
    Image.fromarray(rgb).save(os.path.join(ROOT, "work", "fig4_overlay.png"))
    print("wrote fig4.csv and work/fig4_overlay.png")


if __name__ == "__main__":
    main()
