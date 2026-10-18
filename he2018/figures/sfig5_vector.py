"""Shared extraction for Supplementary Figure 5b-e of He et al. 2018 (SI PDF p.7). Used by sfig5{b,c,d,e}_extract.py.

The four charts (they look like spreadsheet charts printed to PDF) are partly vector: their frames, gridlines, axis lines and the two polynomial
trendlines ('Poly. (0-25 nm)', 'Poly. (sum)') are vector paths; the data markers (red triangles = '0-25 nm',
blue diamonds = 'sum') are small raster images placed at the data points. So everything here is read from
the PDF's own coordinates (tier 2):
  * y: the horizontal gridlines and the bottom axis line, matched to the printed tick labels (0, 200, ... or
    0, 500, ...) in order; linear least-squares fit, residual reported.
  * x: category axis. The printed labels are 1%, 3%, 5%, 7%, 9% (b, c: 9 points 1%..9%) or 10%, 40%, 70%, 100%
    (d, e: 10 points 10%..100%). The first and last category sit on the left and right frame lines (the
    trendlines start and end there and the first/last markers are centred there), so
    x = first + (page_x - frame_left) / (frame_right - frame_left) * (last - first). Checked against the
    centres of the printed x labels (residual reported).
  * markers: centre of the opaque part (soft mask > 50 %) of each marker image, mapped from image pixels to
    page coordinates through the image's placement rectangle.
  * trendlines: every vertex of the polyline as drawn.
"""
import re

import numpy as np
import pymupdf

PDF_NAME = "41598_2018_31231_MOESM1_ESM.pdf"
PANELS = {  # outer panel boxes on p.7 (PDF points) and the category range of the x axis
    "b": dict(box=(72, 273, 324, 440.55), cats=(1, 9), title="low stain level 1.0 keV"),
    "c": dict(box=(324.75, 273, 576.75, 440.5), cats=(1, 9), title="low stain level 1.4 keV"),
    "d": dict(box=(72, 441, 324, 608.75), cats=(10, 100), title="high stain level 1.0 keV"),
    "e": dict(box=(324.75, 441, 576.75, 609), cats=(10, 100), title="high stain level 1.4 keV"),
}
RED = (1.0, 0.0, 0.0)
PURPLE = (0.502, 0.392, 0.635)


def close(c, ref, tol=0.02):
    return c is not None and all(abs(a - b) < tol for a, b in zip(c, ref))


def extract(pdf_path, panel):
    P = PANELS[panel]
    box = pymupdf.Rect(*P["box"])
    doc = pymupdf.open(pdf_path)
    page = doc[6]
    frame = grid = axis_bottom = None
    curves = {}
    for d in page.get_drawings():
        r = d["rect"]
        if not (box.x0 - 1 <= r.x0 and r.x1 <= box.x1 + 1 and box.y0 - 1 <= r.y0 and r.y1 <= box.y1 + 1):
            continue
        items = d["items"]
        col = d.get("color")
        if close(col, (0, 0, 0)) and len(items) == 1 and items[0][0] == "re":
            frame = items[0][1]
        elif close(col, (0.851, 0.851, 0.851)) and all(it[0] == "l" for it in items) and r.width < box.width - 20:
            grid = sorted({round(it[1].y, 3) for it in items})
        elif close(col, (0.749, 0.749, 0.749)) and len(items) == 1 and abs(items[0][1].y - items[0][2].y) < 1e-3:
            axis_bottom = items[0][1].y
        elif (d.get("width") or 0) > 1 and len(items) > 50:
            name = "Poly. (0-25 nm)" if close(col, RED) else ("Poly. (sum)" if close(col, PURPLE) else None)
            assert name, col
            pts = [items[0][1]] + [it[-1] for it in items]
            curves[name] = [(p.x, p.y) for p in pts]
    assert frame is not None and grid and axis_bottom is not None and len(curves) == 2, (frame, grid, axis_bottom, curves.keys())

    # tick labels: numbers left of the frame (y) and percentages below it (x)
    ylab, xlab = [], []
    for b in page.get_text("dict", clip=box)["blocks"]:
        for ln in b.get("lines", []):
            for s in ln["spans"]:
                t = s["text"].replace("\t", "").replace("\r", "").replace("\xa0", "").strip()
                bb = s["bbox"]
                if re.fullmatch(r"\d+", t) and bb[2] < frame.x0:
                    ylab.append((int(t), (bb[1] + bb[3]) / 2))
                elif re.fullmatch(r"\d+%", t) and bb[1] > frame.y1:
                    xlab.append((int(t[:-1]), (bb[0] + bb[2]) / 2))
    ylab.sort()
    lines = sorted([axis_bottom] + grid, reverse=True)          # bottom to top
    assert len(lines) == len(ylab), (lines, ylab)
    A = np.vstack([lines, np.ones(len(lines))]).T
    (my, by), *_ = np.linalg.lstsq(A, [v for v, _ in ylab], rcond=None)
    y_res = float(np.max(np.abs(A @ [my, by] - [v for v, _ in ylab])))
    # label centres vs. gridlines (text placement check only)
    ylab_res = max(abs(yc - l) for (_, yc), l in zip(ylab, lines))

    c0, c1 = P["cats"]

    def fx(x):
        return c0 + (x - frame.x0) / (frame.x1 - frame.x0) * (c1 - c0)

    def fy(y):
        return my * y + by

    xlab_res = max(abs(fx(xc) - v) for v, xc in xlab)

    # markers: raster images inside the frame area
    markers = []
    for info in page.get_image_info(xrefs=True):
        r = pymupdf.Rect(info["bbox"])
        if info["width"] > 60 or not (frame.x0 - 6 <= r.x0 and r.x1 <= frame.x1 + 6 and frame.y0 - 6 <= r.y0 and r.y1 <= frame.y1 + 6):
            continue
        xref = info["xref"]
        pix = pymupdf.Pixmap(doc, xref)
        rgb = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3].astype(float)
        sm = doc.xref_get_key(xref, "SMask")
        m = pymupdf.Pixmap(doc, int(sm[1].split()[0]))
        al = np.frombuffer(m.samples, np.uint8).reshape(m.height, m.width) > 127
        ys, xs = np.where(al)
        cx = (xs.min() + xs.max() + 1) / 2 / pix.width          # centre of the opaque part, fraction of image
        cy = (ys.min() + ys.max() + 1) / 2 / pix.height
        mean = rgb[al].mean(0)
        name = "0-25 nm" if mean[0] > mean[2] else "sum"
        markers.append((name, r.x0 + cx * r.width, r.y0 + cy * r.height))
    markers.sort(key=lambda q: (q[0], q[1]))

    rows = []
    for name, x, y in markers:
        rows.append((name, "marker", float(fx(x)), float(fy(y))))
    for name, pts in curves.items():
        for x, y in pts:
            rows.append((name, "trendline vertex", float(fx(x)), float(fy(y))))
    info = dict(frame=tuple(frame), y_res=y_res, ylab_res=ylab_res, xlab_res=xlab_res, n_markers=len(markers),
                yticks=[v for v, _ in ylab], scale=my, title=P["title"], cats=P["cats"],
                marker_xy=[(x, y) for _, x, y in markers], curve_xy={k: v for k, v in curves.items()})
    return rows, info


def write(panel, here):
    import os
    import sys
    sys.path.insert(0, "/home/admin/ephemeral/oct_17_papers/he2018/tools")
    from digitize_common import write_csv
    pdf = os.path.join(here, "../source", PDF_NAME)
    rows, info = extract(pdf, panel)
    write_csv(os.path.join(here, f"sfig5{panel}.csv"), [
        f"He et al. 2018 Sci Rep 8:12985, Supplementary Figure 5{panel}: '{info['title']}' (chart title). Intensity vs. stain",
        "  composition for the cuboids of Supplementary Fig. 5a. Series names from the legend: '0-25 nm' (red triangles;",
        "  caption: intensity of cuboid 3), 'sum' (blue diamonds; caption: sum of the signals of cuboids 1 and 2), and the",
        "  second-order polynomial trendlines 'Poly. (0-25 nm)' (red line) and 'Poly. (sum)' (purple line).",
        "Columns: series; kind = 'marker' (a plotted data point) or 'trendline vertex' (a vertex of the drawn polyline);",
        "  stain_level_atomic_percent = x, 'stain level (atomic percent)', printed as percentages "
        f"({info['cats'][0]}%-{info['cats'][1]}%); counts_au = y, 'counts (a.u.)'.",
        "Provenance: tier 2, vector: read from the PDF's own coordinates by sfig5_vector.py (called by",
        f"  sfig5{panel}_extract.py). Trendlines and gridlines are vector paths; the markers are small raster images placed at",
        "  the data points (their centres are used). y axis fitted on the bottom axis line and the gridlines matched to the",
        f"  tick labels {info['yticks']}: max residual {info['y_res']:.3g} counts. x: category axis, first and last category on",
        f"  the left/right frame lines; the printed x labels' centres agree within {info['xlab_res']:.2f} percentage points.",
        f"Uncertainty: markers about +-0.3 pt (~{0.3 * abs(info['scale']):.0f} counts, {0.3 / ((info['frame'][2] - info['frame'][0]) / (info['cats'][1] - info['cats'][0])):.2f} percentage points):",
        "  the marker images are 6-7 pt wide and their centre is taken as the data point. The x values of the markers",
        "  are the nominal stain levels (1% steps or 10% steps) up to this placement error.",
    ], ["series", "kind", "stain_level_atomic_percent", "counts_au"], rows, fmt="{:.5g}")
    print(f"sfig5{panel}: {info['n_markers']} markers, y residual {info['y_res']:.3g}, x label residual {info['xlab_res']:.3f}")
    return info
