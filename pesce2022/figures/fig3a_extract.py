"""Extract Fig. 3a of Pesce et al. 2022 (main PDF p. 6): labelling efficiency of CR (upper chart) and PV (lower chart)
in SHORT-processed slices, signal (S) and background (B) intensity at three depths (0, 350, 700 um); mean + SD bars
and individual points (8 neurons per bar).

Bars and error bars are vector (tier 2): the hollow bars are drawn as thin #404040 fills (0.7 pt edges), the SD
whisker is a thin vertical fill from the bar top to a horizontal cap (mean + SD upward only). The individual
points are NOT vector: the transparency flattener turned every translucent grey disc into small raster tiles
(15 x 15 px for a whole 3.6-pt disc, smaller pieces where discs overlap), so the points are recovered by
digitizing a 600-dpi render of each chart's plot area (OpenCV Hough circles of the known radius) and mapped
through the vector-calibrated y axis (tier 3, uncertainty about +-0.25 pt).

    python3 -I -B fig3a_extract.py  -> fig3a.csv (chart column CR/PV), ../work/agent_bars/fig3a_overlay.png
                                       (+ fig3a_CR_detect.png, fig3a_PV_detect.png at 600 dpi)
fig3d_extract.py imports the helpers from this file.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
for _d in [os.path.dirname(os.path.abspath(__file__))] + [os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *([".."] * i))) for i in range(1, 6)]:
    if os.path.exists(os.path.join(_d, "tools", "digitize_common.py")):  # the collection's shared tools/, wherever this folder sits
        sys.path.insert(0, os.path.join(_d, "tools")); break
sys.path.insert(0, HERE)
import cv2  # noqa: E402
import numpy as np  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402
import pdfplot as pp  # noqa: E402
from sfig9_extract import y_axis  # noqa: E402

PDF = os.path.join(HERE, "..", "source", "pesce2022.pdf")
WORK = os.path.join(HERE, "..", "work", "agent_bars")
BAR_COL = "#404040"
DISC_PT = 3.636          # diameter of a point marker (one 15 x 15 px raster tile) in PDF points


def bars_from_thin(draws, cap_len=(4, 15), edge_dx=(2, 7)):
    """Bars of a chart whose outline/whisker are thin fills: one bar per horizontal cap of length in cap_len.

    edge_dx: distance range (pt) of the bar's vertical outline edges from the bar centre, for a cross-check only.
    """
    segs = [s for s in pp.thin_segments(draws) if pp.hexcolor(s["color"]) == BAR_COL]
    caps = [s for s in segs if s["orient"] == "h" and cap_len[0] < s["len"] < cap_len[1]]
    bars = []
    for c in sorted(caps, key=lambda s: (s["x0"] + s["x1"]) / 2):
        xc, ycap = (c["x0"] + c["x1"]) / 2, c["y0"]
        wh = [s for s in segs if s["orient"] == "v" and abs(s["x0"] - xc) < 0.4]
        if wh:      # the whisker (may be split into pieces where a point tile covers it)
            ys = [y for s in wh for y in (s["y0"], s["y1"])]
            ylo, yhi = min(ys), max(ys)
        else:   # a whisker shorter than it is wide (tiny SD) is a small fill rect that thin_segments reports as horizontal
            wh = [r for d in draws if d["kind"] == "fill" and pp.hexcolor(d["fill"]) == BAR_COL for r in d["rects"]
                  if abs((r[0] + r[2]) / 2 - xc) < 0.4 and r[2] - r[0] < 1.2 and r[3] - r[1] < 3]
            assert len(wh) == 1, (xc, ycap, wh)
            ylo, yhi = wh[0][1], wh[0][3]
        assert abs(yhi - ycap) < 0.05 or abs(ylo - ycap) < 0.05, (ycap, ylo, yhi)
        ytop = ylo if abs(yhi - ycap) < 0.05 else yhi          # the whisker end that is not the cap = bar top
        edges = [s for s in segs if s["orient"] == "v" and edge_dx[0] < abs(s["x0"] - xc) < edge_dx[1]]
        edge_top = min((min(s["y0"], s["y1"]) for s in edges), key=lambda y: abs(y - ytop)) if edges else None
        bars.append(dict(xc=xc, ycap=ycap, ytop=ytop, edge_top=edge_top, points=[]))
    return bars


def grey_extent(page, box, z, x0, x1):
    """Top and bottom (page y) of the grey disc pixels between page x0 and x1 in `box` (for clusters of hidden discs)."""
    tmp = os.path.join(WORK, "_tmp_render.png")
    pp.render(page, box, int(72 * z), tmp)
    a = np.asarray(Image.open(tmp).convert("RGB")).astype(int)
    g = a.mean(2)
    grey = ((g > 95) & (g < 215) & (a.max(2) - a.min(2) < 25)).astype(np.uint8)
    grey = cv2.morphologyEx(grey, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8)).astype(bool)   # drop anti-aliased line edges
    os.remove(tmp)
    c0, c1 = max(0, int((x0 - box.x0) * z)), min(grey.shape[1], int((x1 - box.x0) * z))
    rows = np.where(grey[:, c0:c1].any(1))[0]
    return box.y0 + rows.min() / z, box.y0 + rows.max() / z


def find_discs(page, box, z, out_png=None, radius_px=15):
    """Centres (page coordinates) of the grey point discs in `box`, by Hough circles on a render at 72*z dpi.

    Conservative settings: discs that overlap by more than about half their diameter are reported once (a circle
    of the disc radius fits anywhere along a flat cluster, so lower thresholds only add fake centres).
    """
    tmp = os.path.join(WORK, "_tmp_render.png")
    pp.render(page, box, int(72 * z), tmp)
    a = np.asarray(Image.open(tmp).convert("RGB")).astype(int)
    g = a.mean(2)
    sat = a.max(2) - a.min(2)
    grey = (g > 95) & (g < 215) & (sat < 25)                     # the discs (bars/whiskers are darker, #404040)
    blur = cv2.GaussianBlur(g.astype(np.uint8), (5, 5), 1.5)
    circ = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, dp=1, minDist=int(0.8 * radius_px), param1=80, param2=12,
                            minRadius=radius_px - 3, maxRadius=radius_px + 3)
    found = []
    for x, y, r in (circ[0] if circ is not None else []):
        yy, xx = np.ogrid[:g.shape[0], :g.shape[1]]
        inside = (yy - y) ** 2 + (xx - x) ** 2 <= (radius_px - 4) ** 2
        frac = grey[inside].mean() if inside.any() else 0
        if frac > 0.5:                                           # a real disc is grey inside (overlaps are darker grey)
            found.append((box.x0 + x / z, box.y0 + y / z, float(r), float(frac)))
    if out_png:
        im = Image.open(tmp).convert("RGB")
        d = ImageDraw.Draw(im)
        for X, Y, r, frac in found:
            x, y = (X - box.x0) * z, (Y - box.y0) * z
            d.ellipse([x - r, y - r, x + r, y + r], outline=(255, 0, 255), width=2)
            d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(255, 0, 255))
        im.save(out_png)
    os.remove(tmp)
    return found


def main():
    page = pp.open_page(PDF, 6)
    charts = {"CR": dict(clip=pp.R(60, 45, 230, 168)), "PV": dict(clip=pp.R(60, 183, 230, 306))}
    z = 600 / 72
    rows = []
    notes = []
    for name, C in charts.items():
        spans, draws = pp.text_spans(page, C["clip"]), pp.drawings(page, C["clip"])
        yax, used = y_axis(spans, draws, tick_min_len=1.5)
        print(f"[{name}] y axis from {used}: {yax}")
        bars = bars_from_thin(draws)
        assert len(bars) == 6, len(bars)
        axes = [s for s in pp.thin_segments(draws) if pp.hexcolor(s["color"]) == "#000000" and s["len"] > 50]
        xaxis = [s for s in axes if s["orient"] == "h"][0]
        yaxis = [s for s in axes if s["orient"] == "v"][0]
        axis_y = xaxis["y0"]
        for i, b in enumerate(bars):
            lab = [s for s in spans if s["cy"] > axis_y and s["cy"] < axis_y + 10 and abs(s["cx"] - b["xc"]) < 3]
            assert len(lab) == 1, (name, i, [(s["text"], s["cx"]) for s in lab])
            b["sb"] = lab[0]["text"].strip()
            b["depth"] = (0, 350, 700)[i // 2]
            b["mean"], b["sd"] = yax(b["ytop"]), yax(b["ycap"]) - yax(b["ytop"])
            print(f"[{name}] bar {i} '{b['sb']}' {b['depth']} um: x={b['xc']:.2f}, mean {b['mean']:.1f}, sd {b['sd']:.1f}; "
                  f"bar-edge top - whisker foot = {(b['edge_top'] - b['ytop']) if b['edge_top'] is not None else float('nan'):+.2f} pt")
        assert [b["sb"] for b in bars] == ["S", "B"] * 3
        other = [s["text"].strip() for s in spans if axis_y < s["cy"] < axis_y + 10 and s["text"].strip()
                 and s["cx"] > yaxis["x0"] + 3 and all(abs(s["cx"] - b["xc"]) > 3 for b in bars) and s["size"] < 6]
        if other:
            notes.append(f"{name} chart: extra x-axis labels {other} printed at tick positions that carry no bar.")
            print(f"[{name}] extra tick labels without bars: {other}")
        # points: raster discs in the plot area (the box reaches 2.5 pt below the x axis: the B discs sit on it)
        box = pp.R(yaxis["x0"] + 0.5, min(yaxis["y0"], yaxis["y1"]) - 2, max(xaxis["x0"], xaxis["x1"]), axis_y + 2.5)
        discs = find_discs(page, box, z, os.path.join(WORK, f"fig3a_{name}_detect.png"))
        dxs = []
        for X, Y, r, frac in discs:
            b = min(bars, key=lambda b: abs(b["xc"] - X))
            dxs.append(abs(b["xc"] - X))
            b["points"].append((X, Y, yax(Y)))
        for b in bars:
            b["points"].sort()
            if len(b["points"]) < 8:          # hidden discs: give the value range the cluster covers
                top, bot = grey_extent(page, box, z, b["xc"] - 7, b["xc"] + 7)
                lo, hi = sorted((yax(bot - DISC_PT / 2), yax(top + DISC_PT / 2)))
                if bot - top >= DISC_PT:          # a cluster taller than one disc: centres between top+r and bottom-r
                    where = f"the hidden ones lie within the cluster's range {lo:.0f} to {hi:.0f}"
                else:                             # a flat cluster (one disc high, its lower part covered by the x axis line)
                    where = (f"the cluster is one disc high (its lower part is covered by the x axis line), so the hidden values are"
                             f" at most {hi:.0f} and close to the detected ones (printed mean {b['mean']:.0f}, SD {b['sd']:.0f})")
                notes.append(f"{name} {b['sb']} {b['depth']} um: only {len(b['points'])} of 8 discs separable (the others coincide with or "
                             f"overlap them); {where}.")
        print(f"[{name}] {len(discs)} discs found; per bar {[len(b['points']) for b in bars]}; max |dx| from bar centre {max(dxs):.1f} pt")
        C.update(bars=bars, yax=yax, used=used)
        for b in bars:
            rows.append(["bar", name, b["depth"], b["sb"], f"{b['mean']:.1f}", f"{b['sd']:.1f}", len(b["points"]), "", ""])
    for name, C in charts.items():
        for b in C["bars"]:
            rows += [["point", name, b["depth"], b["sb"], "", "", "", i, f"{v:.1f}"] for i, (X, Y, v) in enumerate(b["points"])]

    # overlay on a 300-dpi render of the whole panel
    full = pp.R(60, 45, 230, 310)
    z2 = 300 / 72
    pp.render(page, full, 300, os.path.join(WORK, "fig3a_orig_300.png"))
    img = Image.open(os.path.join(WORK, "fig3a_orig_300.png")).convert("RGB")
    dr = ImageDraw.Draw(img)
    for name, C in charts.items():
        for b in C["bars"]:
            X = (b["xc"] - full.x0) * z2
            for yy, col, w in ((b["ytop"], (255, 0, 255), 22), (b["ycap"], (0, 200, 255), 14)):
                Y = (yy - full.y0) * z2
                dr.line([(X - w, Y), (X + w, Y)], fill=col, width=2)
            for px_, py_, v in b["points"]:
                X, Y = (px_ - full.x0) * z2, (py_ - full.y0) * z2
                dr.ellipse([X - 7, Y - 7, X + 7, Y + 7], outline=(255, 0, 255), width=2)
    img.save(os.path.join(WORK, "fig3a_overlay.png"))

    unc = {n: 0.25 * abs(C["yax"].slope) for n, C in charts.items()}
    header = ["row_type", "chart", "depth_um", "signal_background", "mean", "sd", "n_points", "point_index", "value"]
    pp.write_csv(os.path.join(HERE, "fig3a.csv"), header, rows, [
        "Pesce et al. 2022 Commun Biol 5:447, Fig. 3a (main PDF p. 6): labelling efficiency of two neuron markers, CR (upper chart)",
        "  and PV (lower chart), in SHORT-processed slices imaged by LSFM: fluorescence intensity (y axis 'Intensity', arbitrary",
        "  units) of the signal (S, neuronal somata) and background (B) at three depths, 0 um (0-240 um, maximal light exposure),",
        "  350 um (240-470 um, slice middle) and 700 um (490-700 um, opposite the excitation side); mean + SD bars (error bar",
        "  upward only) and the individual values (caption: 8 different neurons / background regions per bar).",
        "Columns: row_type = 'bar' or 'point'; chart = CR or PV; depth_um = 0, 350 or 700 (the depth labels are printed on the",
        "  micrograph strip under each chart; the S/B pairs are assigned to them left to right); signal_background = S or B as",
        "  printed under the bar; bar rows: mean, sd, n_points = points found; point rows: point_index (0-based, left to right)",
        "  and value.",
        "Provenance: bars and SD are tier 2 (vector thin fills: bar outline, whisker and cap), exact up to the PDF's precision",
        f"  (0.01 pt = {0.01 * abs(charts['CR']['yax'].slope):.1f} units in CR, {0.01 * abs(charts['PV']['yax'].slope):.2f} in PV); y axes calibrated on the",
        f"  labelled major ticks (CR: {', '.join(charts['CR']['used'])}; PV: {', '.join(charts['PV']['used'])}), linear; max residuals",
        f"  {charts['CR']['yax'].resid:.3g} (CR) and {charts['PV']['yax'].resid:.3g} (PV) units. The points are tier 3: the translucent",
        "  discs exist in the PDF only as small raster tiles (transparency flattening), so they were digitized from a 600-dpi",
        "  render (Hough circles of the 3.6-pt disc radius; every detection checked on the overlay); uncertainty about 0.25 pt =",
        f"  +-{unc['CR']:.0f} units (CR) / +-{unc['PV']:.0f} units (PV). Points hidden behind or overlapping another point by more than",
        "  about half a disc cannot be separated; the counts found per bar are given in n_points (caption: n = 8), and for the",
        "  bars with fewer than 8 the notes below give the value range covered by the cluster (so the hidden values lie in it).",
    ] + notes)
    print("wrote fig3a.csv", len(rows), "rows")


if __name__ == "__main__":
    main()
