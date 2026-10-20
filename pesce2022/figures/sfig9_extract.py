"""Extract Supplementary Fig. 9 of Pesce et al. 2022 (supplement p. 10): "Stripping efficiency", NeuN fluorescence
intensity (mean + SD bars, individual points) for No label/strip, Anti-NeuN staining, Post strip.

Tier 2: vector paths. Each bar is an open 4-point stroke (BL, BR, TR, TL), the error bar a vertical stroke from
the bar top to a horizontal cap (mean + SD upward only), the points translucent grey circle fills (49 flattened
points, 9.3 pt across, alpha 0.45). y axis from the tick labels '0,0', '5,0x10^2' ... '3,5x10^3' (decimal commas,
exponent as a separate small span) and the major tick marks beside them.

    python3 -I -B sfig9_extract.py  -> sfig9.csv, ../work/agent_bars/sfig9_overlay.png
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
for _d in [os.path.dirname(os.path.abspath(__file__))] + [os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *([".."] * i))) for i in range(1, 6)]:
    if os.path.exists(os.path.join(_d, "tools", "digitize_common.py")):  # the collection's shared tools/, wherever this folder sits
        sys.path.insert(0, os.path.join(_d, "tools")); break
import numpy as np  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402
import pdfplot as pp  # noqa: E402

PDF = os.path.join(HERE, "..", "source", "pesce2022_supplement.pdf")
WORK = os.path.join(HERE, "..", "work", "agent_bars")
CLIP = pp.R(55, 75, 505, 405)
BAR_COL = "#404040"


def y_axis(spans, draws, tick_min_len=2.5):
    """Linear y axis from numeric tick labels ('0,0', '5,0x10' + '2', ...) and the major tick marks beside them."""
    pairs, used = [], []
    mant = [s for s in spans if s["text"].strip().endswith("x10")]
    for s in spans:
        t = s["text"].strip()
        if s["dir"][0] < 0.99 or not re.fullmatch(r"-?\d+(,\d+)?(x10)?", t):
            continue
        if any(abs(s["bbox"][0] - m["bbox"][2]) < 1.5 and abs(s["cy"] - m["cy"]) < 6 for m in mant):
            continue                                                   # an exponent span, handled with its mantissa
        if t.endswith("x10"):
            ex = [e for e in spans if abs(e["bbox"][0] - s["bbox"][2]) < 1.5 and abs(e["cy"] - s["cy"]) < 6
                  and e["size"] < s["size"] and re.fullmatch(r"-?\d", e["text"].strip())]
            assert len(ex) == 1, (t, [e["text"] for e in ex])
            val = float(t[:-3].replace(",", ".")) * 10 ** int(ex[0]["text"])
            used.append(t + "^" + ex[0]["text"].strip())
        else:
            val = float(t.replace(",", "."))
            used.append(t)
        ticks = [g for g in pp.segments(draws, orientation="h", max_len=8, min_len=tick_min_len)
                 if pp.hexcolor(g["color"]) == "#000000" and abs((g["y0"] + g["y1"]) / 2 - s["cy"]) < 0.3 * s["size"] + 1
                 and s["bbox"][2] - 1 < min(g["x0"], g["x1"]) < s["bbox"][2] + 15]
        assert len(ticks) == 1, (t, ticks)
        pairs.append(((ticks[0]["y0"] + ticks[0]["y1"]) / 2, val))
    return pp.Axis(pairs), used


def bars_from_strokes(draws, colour):
    """Open 4-point bar outlines (BL, BR, TR, TL) + their whisker/cap strokes of the same colour."""
    bars = []
    for d in draws:
        if d["kind"] == "stroke" and len(d["points"]) == 4 and pp.hexcolor(d["color"]) == colour:
            (x0, y0), (x1, y1), (x2, y2), (x3, y3) = d["points"]
            assert abs(y0 - y1) < 0.02 and abs(y2 - y3) < 0.02 and abs(x0 - x3) < 0.02 and abs(x1 - x2) < 0.02
            bars.append(dict(xl=x0, xr=x1, xc=(x0 + x1) / 2, ytop=y2, ybot=y0, ycap=None, points=[]))
    bars.sort(key=lambda b: b["xc"])
    for d in draws:
        if d["kind"] == "stroke" and len(d["points"]) == 2 and pp.hexcolor(d["color"]) == colour:
            (x0, y0), (x1, y1) = d["points"]
            if abs(y0 - y1) < 0.02:                                       # horizontal: the cap
                b = min(bars, key=lambda b: abs(b["xc"] - (x0 + x1) / 2))
                assert abs(b["xc"] - (x0 + x1) / 2) < 0.5 and b["ycap"] is None
                b["ycap"] = y0
    for b in bars:
        whisk = [d for d in draws if d["kind"] == "stroke" and len(d["points"]) == 2 and pp.hexcolor(d["color"]) == colour
                 and abs(d["points"][0][0] - b["xc"]) < 0.5 and abs(d["points"][1][0] - b["xc"]) < 0.5]
        assert len(whisk) == 1 and b["ycap"] is not None, (b, len(whisk))
        ys = sorted(p[1] for p in whisk[0]["points"])
        assert abs(ys[0] - b["ycap"]) < 0.05 and abs(ys[1] - b["ytop"]) < 0.05, (b, ys)
    return bars


def main():
    page = pp.open_page(PDF, 10)
    spans, draws = pp.text_spans(page, CLIP), pp.drawings(page, CLIP)
    yax, used = y_axis(spans, draws)
    print("y axis from", used, yax)
    bars = bars_from_strokes(draws, BAR_COL)
    assert len(bars) == 3
    labels = [s for s in spans if "Bold" in s["font"] and s["cy"] > bars[0]["ybot"] and 12 < s["size"] < 16]
    for b in bars:
        lab = min(labels, key=lambda s: abs(s["cx"] - b["xc"]))
        assert abs(lab["cx"] - b["xc"]) < 10, (lab["text"], lab["cx"], b["xc"])
        b["label"] = lab["text"].strip()
        b["mean"], b["sd"] = yax(b["ytop"]), yax(b["ycap"]) - yax(b["ytop"])
    dxs = []
    for d in draws:
        if d["kind"] == "fill" and pp.hexcolor(d["fill"]) == BAR_COL and len(d["points"]) == 49 and d["has_curves"]:
            r = d["rect"]
            cx, cy = (r[0] + r[2]) / 2, (r[1] + r[3]) / 2
            b = min(bars, key=lambda b: abs(b["xc"] - cx))
            dxs.append(abs(cx - b["xc"]))
            b["points"].append((cx, cy, yax(cy)))
    for b in bars:
        b["points"].sort()
        print(f"{b['label']}: mean {b['mean']:.1f}, sd {b['sd']:.1f}, {len(b['points'])} points")
    print(f"points: max |dx| from bar centre {max(dxs):.1f} pt (bar half-width {(bars[0]['xr'] - bars[0]['xl']) / 2:.1f} pt)")

    z = 300 / 72
    pp.render(page, CLIP, 300, os.path.join(WORK, "sfig9_orig_300.png"))
    img = Image.open(os.path.join(WORK, "sfig9_orig_300.png")).convert("RGB")
    dr = ImageDraw.Draw(img)
    for b in bars:
        X = (b["xc"] - CLIP.x0) * z
        for yy, col, w in ((b["ytop"], (255, 0, 255), 40), (b["ycap"], (0, 200, 255), 25)):
            Y = (yy - CLIP.y0) * z
            dr.line([(X - w, Y), (X + w, Y)], fill=col, width=3)
        for cx, cy, v in b["points"]:
            X, Y = (cx - CLIP.x0) * z, (cy - CLIP.y0) * z
            dr.ellipse([X - 5, Y - 5, X + 5, Y + 5], outline=(255, 0, 255), width=2)
    img.save(os.path.join(WORK, "sfig9_overlay.png"))

    rows = [["bar", b["label"], f"{b['mean']:.2f}", f"{b['sd']:.2f}", len(b["points"]), "", ""] for b in bars]
    for b in bars:
        rows += [["point", b["label"], "", "", "", i, f"{v:.2f}"] for i, (cx, cy, v) in enumerate(b["points"])]
    pp.write_csv(os.path.join(HERE, "sfig9.csv"), ["row_type", "condition", "mean", "sd", "n_points", "point_index", "value"], rows, [
        "Pesce et al. 2022 Commun Biol 5:447, Supplementary Fig. 9 'Stripping efficiency' (supplement p. 10): NeuN immunofluorescence",
        "  intensity (y axis 'Intensity', arbitrary units, confocal) of SHORT-processed slices before labelling, after anti-NeuN",
        "  staining and after stripping; mean + SD bars (error bar drawn upward only) and the individual data points.",
        "Columns: row_type = 'bar' or 'point'; condition = x label as printed; bar rows: mean, sd, n_points = points found for",
        "  that bar; point rows: point_index (0-based, left to right within the bar) and value.",
        "Provenance: tier 2, vector paths in the PDF (bar outlines, whiskers, caps and circle fills), exact up to the PDF's",
        f"  precision (0.01 pt = {0.01 * abs(yax.slope):.2f} units). y axis calibrated on the 8 labelled major ticks 0,0 ... 3,5x10^3",
        f"  (linear); max residual {yax.resid:.3g} units. x axis categorical (3 bars).",
        f"Note: {len(bars[0]['points'])}/{len(bars[1]['points'])}/{len(bars[2]['points'])} points per bar are drawn, although the caption",
        "  says 'n = 3 samples' (the points are presumably per-cell or per-ROI measurements pooled over the 3 samples).",
    ])
    print("wrote sfig9.csv", len(rows), "rows")


if __name__ == "__main__":
    main()
