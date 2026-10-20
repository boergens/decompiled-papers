"""Extract Fig. 3d of Pesce et al. 2022 (main PDF p. 6): signal-to-noise ratio of SST immunolabelling in three
staining rounds (n = 30 neurons per round); mean + SD bars and individual points.

Same construction as Fig. 3a (see fig3a_extract.py): bars/whiskers/caps are vector thin fills (tier 2), the
points are raster tiles digitized from a 600-dpi render with Hough circles (tier 3).

    python3 -I -B fig3d_extract.py  -> fig3d.csv, ../work/agent_bars/fig3d_overlay.png (+ fig3d_detect.png)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
for _d in [os.path.dirname(os.path.abspath(__file__))] + [os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *([".."] * i))) for i in range(1, 6)]:
    if os.path.exists(os.path.join(_d, "tools", "digitize_common.py")):  # the collection's shared tools/, wherever this folder sits
        sys.path.insert(0, os.path.join(_d, "tools")); break
sys.path.insert(0, HERE)
from PIL import Image, ImageDraw  # noqa: E402
import pdfplot as pp  # noqa: E402
from sfig9_extract import y_axis  # noqa: E402
from fig3a_extract import bars_from_thin, find_discs, PDF, WORK  # noqa: E402

CLIP = pp.R(380, 45, 540, 175)


def main():
    page = pp.open_page(PDF, 6)
    spans, draws = pp.text_spans(page, CLIP), pp.drawings(page, CLIP)
    yax, used = y_axis(spans, draws, tick_min_len=1.5)
    print("y axis from", used, yax)
    bars = bars_from_thin(draws, cap_len=(8, 20), edge_dx=(8, 20))
    assert len(bars) == 3, len(bars)
    axes = [s for s in pp.thin_segments(draws) if pp.hexcolor(s["color"]) == "#000000" and s["len"] > 50]
    xaxis = [s for s in axes if s["orient"] == "h"][0]
    yaxis = [s for s in axes if s["orient"] == "v"][0]
    axis_y = xaxis["y0"]
    for i, b in enumerate(bars):
        lab = [s for s in spans if axis_y < s["cy"] < axis_y + 12 and abs(s["cx"] - b["xc"]) < 10]
        assert len(lab) == 1, (i, [(s["text"], s["cx"]) for s in lab])
        b["label"] = lab[0]["text"].strip()
        b["mean"], b["sd"] = yax(b["ytop"]), yax(b["ycap"]) - yax(b["ytop"])
        print(f"bar {i} '{b['label']}': x={b['xc']:.2f}, mean {b['mean']:.3f}, sd {b['sd']:.3f}; "
              f"bar-edge top - whisker foot = {(b['edge_top'] - b['ytop']) if b['edge_top'] is not None else float('nan'):+.2f} pt")
    z = 600 / 72
    box = pp.R(yaxis["x0"] + 0.5, min(yaxis["y0"], yaxis["y1"]) - 2, max(xaxis["x0"], xaxis["x1"]), axis_y - 0.3)
    discs = find_discs(page, box, z, os.path.join(WORK, "fig3d_detect.png"))
    dxs = []
    for X, Y, r, frac in discs:
        b = min(bars, key=lambda b: abs(b["xc"] - X))
        dxs.append(abs(b["xc"] - X))
        b["points"].append((X, Y, yax(Y)))
    for b in bars:
        b["points"].sort()
    print(f"{len(discs)} discs found; per bar {[len(b['points']) for b in bars]}; max |dx| from bar centre {max(dxs):.1f} pt")

    z2 = 300 / 72
    pp.render(page, CLIP, 300, os.path.join(WORK, "fig3d_orig_300.png"))
    img = Image.open(os.path.join(WORK, "fig3d_orig_300.png")).convert("RGB")
    dr = ImageDraw.Draw(img)
    for b in bars:
        X = (b["xc"] - CLIP.x0) * z2
        for yy, col, w in ((b["ytop"], (255, 0, 255), 40), (b["ycap"], (0, 200, 255), 25)):
            Y = (yy - CLIP.y0) * z2
            dr.line([(X - w, Y), (X + w, Y)], fill=col, width=2)
        for px_, py_, v in b["points"]:
            X, Y = (px_ - CLIP.x0) * z2, (py_ - CLIP.y0) * z2
            dr.ellipse([X - 7, Y - 7, X + 7, Y + 7], outline=(255, 0, 255), width=2)
    img.save(os.path.join(WORK, "fig3d_overlay.png"))

    rows = [["bar", b["label"], f"{b['mean']:.3f}", f"{b['sd']:.3f}", len(b["points"]), "", ""] for b in bars]
    for b in bars:
        rows += [["point", b["label"], "", "", "", i, f"{v:.3f}"] for i, (X, Y, v) in enumerate(b["points"])]
    pp.write_csv(os.path.join(HERE, "fig3d.csv"), ["row_type", "round", "mean", "sd", "n_points", "point_index", "value"], rows, [
        "Pesce et al. 2022 Commun Biol 5:447, Fig. 3d (main PDF p. 6): signal-to-noise ratio (y axis 'Signal to noise') of SST",
        "  immunolabelling in round 1, round 2 and round 3 of multi-round staining (x axis 'SST label'); mean + SD bars (error",
        "  bar upward only) and the individual neurons (caption: n = 30 neurons per round).",
        "Columns: row_type = 'bar' or 'point'; round = x label as printed; bar rows: mean, sd, n_points = points found; point rows:",
        "  point_index (0-based, left to right) and value (dimensionless).",
        "Provenance: bars and SD are tier 2 (vector thin fills: bar outline, whisker and cap), exact up to the PDF's precision",
        f"  (0.01 pt = {0.01 * abs(yax.slope):.4f}); y axis calibrated on the 6 labelled major ticks {', '.join(used)} (linear), max residual",
        f"  {yax.resid:.2g}. The points are tier 3: the translucent discs exist in the PDF only as small raster tiles (transparency",
        "  flattening), so they were digitized from a 600-dpi render (Hough circles of the 3.6-pt disc radius; every detection",
        f"  checked on the overlay); uncertainty about 0.25 pt = +-{0.25 * abs(yax.slope):.3f}. Points fully hidden behind another",
        "  point cannot be seen; the counts per bar are in n_points.",
    ])
    print("wrote fig3d.csv", len(rows), "rows")


if __name__ == "__main__":
    main()
