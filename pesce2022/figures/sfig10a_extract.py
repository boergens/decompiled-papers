"""Extract Supplementary Fig. 10a of Pesce et al. 2022 (supplement p. 11): SSIM index of SST neurons after clearing
vs after stripping; one bar (mean + SD) and 3 red data points.

Tier 2: vector paths (bar = open 4-point stroke, whisker + cap strokes in #404040, points = red filled circles).
y axis from the tick labels '0,0' ... '1,0' (decimal commas) and the major tick marks.

    python3 -I -B sfig10a_extract.py  -> sfig10a.csv, ../work/agent_bars/sfig10a_overlay.png
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
from sfig9_extract import y_axis, bars_from_strokes  # noqa: E402

PDF = os.path.join(HERE, "..", "source", "pesce2022_supplement.pdf")
WORK = os.path.join(HERE, "..", "work", "agent_bars")
CLIP = pp.R(335, 85, 525, 215)


def main():
    page = pp.open_page(PDF, 11)
    spans, draws = pp.text_spans(page, CLIP), pp.drawings(page, CLIP)
    yax, used = y_axis(spans, draws, tick_min_len=1.8)
    print("y axis from", used, yax)
    bars = bars_from_strokes(draws, "#404040")
    assert len(bars) == 1
    b = bars[0]
    b["mean"], b["sd"] = yax(b["ytop"]), yax(b["ycap"]) - yax(b["ytop"])
    lab = [s["text"].strip() for s in spans if s["cy"] > b["ybot"] and abs(s["cx"] - b["xc"]) < 15 and s["size"] > 6]
    print("x label spans under the bar:", lab)
    pts = []
    for d in draws:
        if d["kind"] == "fillstroke" and pp.hexcolor(d["fill"]) == "#d51606" and d["has_curves"]:
            r = d["rect"]
            pts.append(((r[0] + r[2]) / 2, (r[1] + r[3]) / 2, yax((r[1] + r[3]) / 2)))
    pts.sort()
    assert len(pts) == 3, len(pts)
    print(f"bar: mean {b['mean']:.3f}, sd {b['sd']:.3f}; points {[round(p[2], 3) for p in pts]}")

    z = 300 / 72
    pp.render(page, CLIP, 300, os.path.join(WORK, "sfig10a_orig_300.png"))
    img = Image.open(os.path.join(WORK, "sfig10a_orig_300.png")).convert("RGB")
    dr = ImageDraw.Draw(img)
    X = (b["xc"] - CLIP.x0) * z
    for yy, col, w in ((b["ytop"], (255, 0, 255), 40), (b["ycap"], (0, 200, 255), 25)):
        Y = (yy - CLIP.y0) * z
        dr.line([(X - w, Y), (X + w, Y)], fill=col, width=3)
    for cx, cy, v in pts:
        X, Y = (cx - CLIP.x0) * z, (cy - CLIP.y0) * z
        dr.ellipse([X - 6, Y - 6, X + 6, Y + 6], outline=(255, 0, 255), width=2)
    img.save(os.path.join(WORK, "sfig10a_overlay.png"))

    rows = [["bar", "SST neurons", f"{b['mean']:.4f}", f"{b['sd']:.4f}", len(pts), "", ""]]
    rows += [["point", "SST neurons", "", "", "", i, f"{v:.4f}"] for i, (cx, cy, v) in enumerate(pts)]
    pp.write_csv(os.path.join(HERE, "sfig10a.csv"), ["row_type", "label", "mean", "sd", "n_points", "point_index", "value"], rows, [
        "Pesce et al. 2022 Commun Biol 5:447, Supplementary Fig. 10a (supplement p. 11): structural similarity index (SSIM, y axis",
        "  'SSIM index', 0-1) between high-resolution images of SST-immunoreactive neurons after clearing and after stripping;",
        "  mean + SD bar (error bar upward only) and the 3 individual values (caption: mean +- SD, N = 3).",
        "Columns: row_type = 'bar' or 'point'; label = x label as printed ('SST neurons'); bar rows: mean, sd, n_points;",
        "  point rows: point_index (0-based, left to right) and value.",
        "Provenance: tier 2, vector paths in the PDF, exact up to the PDF's precision (0.01 pt = "
        f"{0.01 * abs(yax.slope):.5f} SSIM). y axis calibrated on the 6 labelled major ticks 0,0 ... 1,0 (linear); max residual {yax.resid:.2g}.",
        "Note: the PDF carries hidden text under white boxes (an earlier x label 'A' and a smaller 'SSIM index'); the visible",
        "  labels are 'SST neurons' and 'SSIM index'.",
    ])
    print("wrote sfig10a.csv")


if __name__ == "__main__":
    main()
