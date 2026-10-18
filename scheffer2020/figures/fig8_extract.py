#!/usr/bin/env python3
"""Digitize Figure 8A and 8B of scheffer2020 (bubble matrices over pairs of adjacent brain regions).

Tier 3 (digitized): the figure is one embedded lossless image (1132 x 2450 px, ~303 ppi) on PDF page 19; panel A is
the upper half, panel B the lower half. The authors' Figure 8-source data 1 is not available locally.

Both panels are matrices with the same 35 brain regions on the rows (top to bottom) and columns (left to right).
A dot in a cell encodes a value by its size: (A) the area of the boundary between the two regions in square microns,
"indicated on a log scale" (caption); (B) the number of excess crossings normalized by the boundary area. Each panel has
a size legend in its upper left corner with three symbols labelled Min/Med/Max (A: 1, 883, 15511; B: 0.0, 0.8, 2.6).

Method:
- cell centres: the light-grey (229) gridlines, located in the image, one per row and per column.
- ink weight per pixel: w = (bg - R) / (bg - 31) for blue pixels (dot colour 31,119,180; bg = 229 on gridlines,
  255 elsewhere), so anti-aliased edges count fractionally.
- a cell holds a dot if w >= 0.5 within 2 px of its gridline crossing. Dots smaller than r = 2.5 px (the gridlines
  are drawn over them) get the radius sqrt(sum(w) / pi) over a 7 x 7 px window (flag tiny_area_radius). The dot radius is the median, over 72 rays from the
  dot centre, of the distance at which w falls below 0.5 (bilinear interpolation); the centre is refined from the
  crossing by a circle fit to the ray edge points. The median ignores the few rays that run into a touching neighbour
  dot (the largest dots touch, so pixel counting or connected components fail).
- size scale: the legend symbols are drawn smaller than the data dots: the largest data dot has radius 15.5 px in both
  panels, the Max legend symbol 12.95 px (ratio 1.20 in both panels). The data are therefore calibrated on the data:
  A: radius linear in log10(value), with the shape taken from the legend (Min 1 -> 3.40 px, Med 883 -> 10.15 px,
     Max 15511 -> 12.95 px: radius linear in log10 to 0.04 px) and scaled so that the largest data dot = 15511 (Max).
     Check: the smallest data dot then comes out at 0.8 (legend Min: 1) and the median of all dots at 798
     (legend Med: 883; a 0.1 px radius error is 9 % in value here).
  B: radius proportional to value (a dot of value 0 is invisible, like the Min 0.0 legend symbol), scaled so that the
     largest data dot = 2.6 (Max). Check: with the 39 cells that have a dot in A but none in B counted as 0, the median
     comes out at 0.80 (legend Med: 0.8). (The Med legend symbol itself, 4.47 px, is ~12 % larger than this scale
     implies; a straight line through the two legend symbols would make the median 0.69 and give a visible 0.0 symbol.)
- the legend symbols sit in column AB(L), rows AB(L) to AL(R) of each panel; those three cells are skipped.

Writes figures/fig8a.csv, figures/fig8b.csv and work/fig8_overlay.png.
"""
import csv
from pathlib import Path

import cv2
import numpy as np
import pymupdf
from scipy.ndimage import map_coordinates

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PDF = ROOT / "source" / "elife-57443-v4.pdf"
WORK = ROOT / "work"
WORK.mkdir(exist_ok=True)

LABELS = ["AB(L)", "AB(R)", "AL(R)", "AME(R)", "AOTU(R)", "ATL(R)", "AVLP(R)", "BU(R)", "CA(R)", "CRE(R)", "EB",
          "EPA(R)", "FB", "GOR(R)", "IB", "ICL(R)", "LAL(R)", "LH(R)", "NO", "PB", "PED(R)", "PLP(R)", "PVLP(R)",
          "SCL(R)", "SIP(R)", "SLP(R)", "SMP(R)", "SPS(R)", "VES(R)", "WED(R)", "a'L(R)", "aL(R)", "b'L(R)", "bL(R)",
          "gL(R)"]


def load():
    doc = pymupdf.open(PDF)
    page = doc[18]
    info = max(page.get_image_info(xrefs=True), key=lambda i: pymupdf.Rect(i["bbox"]).width)
    pix = pymupdf.Pixmap(doc, info["xref"])
    if pix.n - pix.alpha != 3:
        pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
    return np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3].copy()


def line_centres(s, thr, lo, hi):
    idx = [i for i in range(int(lo), int(hi)) if s[i] > thr]
    groups, cur = [], []
    for i in idx:
        if cur and i - cur[-1] > 1:
            groups.append(cur)
            cur = []
        cur.append(i)
    if cur:
        groups.append(cur)
    return [float(np.mean(g)) for g in groups]


def rays(w, cx, cy, maxr=17.0):
    rr = np.arange(0, maxr, 0.25)
    t = np.linspace(0, 2 * np.pi, 72, endpoint=False)
    out = []
    for a in t:
        v = map_coordinates(w, [cy + rr * np.sin(a), cx + rr * np.cos(a)], order=1)
        i = int(np.argmax(v < 0.5))
        out.append(maxr if i == 0 else rr[i - 1] + (v[i - 1] - 0.5) / (v[i - 1] - v[i]) * 0.25)
    return t, np.array(out)


def radius(w, cx, cy, maxr=17.0):
    """Dot at (cx, cy)? Edge (w = 0.5) distances along 72 rays; the centre is refined by a least-squares circle fit
    to the edge points (rays running into a touching neighbour, |d - median| > 1.5 px, left out), twice.
    Returns (cx, cy, r, r10, r90) or None if the crossing itself is not ink."""
    iy, ix = int(round(cy)), int(round(cx))
    win = w[iy - 3:iy + 4, ix - 3:ix + 4]
    if win[1:6, 1:6].max() < 0.5:
        return None
    yy, xx = np.mgrid[iy - 3:iy + 4, ix - 3:ix + 4]
    if np.sqrt(win.sum() / np.pi) < 2.5:
        # tiny dot (gridlines are drawn over it): radius from its weighted area in a 7 x 7 px window
        a = win.sum()
        cx_, cy_ = float((xx * win).sum() / a), float((yy * win).sum() / a)
        r = float(np.sqrt(a / np.pi))
        return cx_, cy_, r, np.nan, np.nan
    for _ in range(2):
        t, d = rays(w, cx, cy, maxr)
        ok = np.abs(d - np.median(d)) <= 1.5
        x = cx + d[ok] * np.cos(t[ok])
        y = cy + d[ok] * np.sin(t[ok])
        if ok.sum() >= 8:
            A = np.c_[2 * x, 2 * y, np.ones(len(x))]
            c, *_ = np.linalg.lstsq(A, x ** 2 + y ** 2, rcond=None)
            if np.hypot(c[0] - cx, c[1] - cy) < 3:
                cx, cy = float(c[0]), float(c[1])
    t, d = rays(w, cx, cy, maxr)
    return cx, cy, float(np.median(d)), float(np.percentile(d, 10)), float(np.percentile(d, 90))


def centroid(w, cx, cy, h=15):
    y0, x0 = int(cy - h), int(cx - h)
    win = w[y0:y0 + 2 * h + 1, x0:x0 + 2 * h + 1]
    yy, xx = np.mgrid[y0:y0 + 2 * h + 1, x0:x0 + 2 * h + 1]
    return float((xx * win).sum() / win.sum()), float((yy * win).sum() / win.sum())


def main():
    img = load()
    H, W, _ = img.shape
    f = img.astype(float)
    neutral = (np.abs(f[:, :, 0] - f[:, :, 1]) < 8) & (np.abs(f[:, :, 1] - f[:, :, 2]) < 8)
    grid = neutral & (f.mean(2) > 200) & (f.mean(2) < 248)
    dark = f.mean(2) < 120
    fx = line_centres(dark.sum(0), 2000, 0, W)[0]  # left frame line (both panels)
    frame_rows = line_centres(dark.sum(1), 900, 0, H)  # bottom frame of A and of B
    cols = [c for c in line_centres(grid.sum(0), 600, 0, W) if fx + 5 < c < W - 5]
    assert len(cols) == 35, cols
    bgmap = np.where(grid, 229.0, 255.0)
    w = np.clip((bgmap - f[:, :, 0]) / (bgmap - 31.0), 0, 1) * ((f[:, :, 2] - f[:, :, 0]) > 30)
    overlay = cv2.cvtColor(img, cv2.COLOR_RGB2BGR).copy()
    panels = {"a": (0, frame_rows[0]), "b": (frame_rows[0] + 150, frame_rows[1])}
    res = {}
    for key, (ylo, yhi) in panels.items():
        rows = line_centres(grid[:, 300:].sum(1), 400, ylo, yhi)[-35:]
        assert len(rows) == 35, (key, rows)
        legend = []
        for (lx, ly) in [(cols[0], rows[0]), (cols[0], rows[0] + 41), (cols[0], rows[0] + 72)]:
            if w[int(ly) - 12:int(ly) + 12, int(lx) - 12:int(lx) + 12].max() < 0.5:
                continue  # invisible symbol (B: Min 0.0)
            cx, cy = centroid(w, lx, ly)
            rr_ = radius(w, cx, cy)
            legend.append((rr_[0], rr_[1], rr_[2]))
        dots = []
        for ri, ry in enumerate(rows):
            for ci, cx in enumerate(cols):
                if ci == 0 and ri < 3:
                    continue
                r = radius(w, cx, ry)
                if r is not None:
                    dots.append(dict(ri=ri, ci=ci, cx=r[0], cy=r[1], r=r[2], r10=r[3], r90=r[4], dx=r[0] - cx, dy=r[1] - ry))
        res[key] = dict(rows=rows, legend=legend, dots=dots)
    # calibrations (see docstring)
    la = [l[2] for l in res["a"]["legend"]]
    lb = [l[2] for l in res["b"]["legend"]]
    assert len(la) == 3 and len(lb) == 2, (la, lb)
    LMAX = np.log10(15511)
    ka, ra0 = np.polyfit(np.log10([1, 883, 15511]), la, 1)
    resid_a = np.array(la) - (ra0 + ka * np.log10([1, 883, 15511]))
    sa = max(d["r"] for d in res["a"]["dots"]) / (ra0 + ka * LMAX)
    sb = max(d["r"] for d in res["b"]["dots"]) / lb[1]
    val = {"a": lambda r: 10 ** ((r / sa - ra0) / ka), "b": lambda r: 2.6 * r / max(d["r"] for d in res["b"]["dots"])}
    unc = {"a": lambda r: 10 ** ((r / sa - ra0) / ka) * (10 ** (0.1 / (sa * ka)) - 1), "b": lambda r: 2.6 * 0.1 / max(d["r"] for d in res["b"]["dots"])}
    acells = {(d["ri"], d["ci"]) for d in res["a"]["dots"]}
    for key in "ab":
        R = res[key]
        vals = [val[key](d["r"]) for d in R["dots"]]
        if key == "b":
            vals_med = vals + [0.0] * len(acells - {(d["ri"], d["ci"]) for d in R["dots"]})
        else:
            vals_med = vals
        cells = {(d["ri"], d["ci"]) for d in R["dots"]}
        out = []
        for d, v in zip(R["dots"], vals):
            flag = "ok"
            if np.isnan(d["r10"]):
                flag = "tiny_area_radius"
            elif d["r90"] - d["r10"] > 1.0:
                flag = "irregular_edge"  # touching neighbour or ragged small dot
            mirror = "yes" if (d["ci"], d["ri"]) in cells else "no"
            out.append([LABELS[d["ri"]], LABELS[d["ci"]], round(d["dx"], 2), round(d["dy"], 2), round(d["r"], 2), ("" if np.isnan(d["r10"]) else round(d["r10"], 2)), ("" if np.isnan(d["r90"]) else round(d["r90"], 2)),
                        (f"{v:.3g}" if key == "a" else f"{v:.3f}"), (f"{unc[key](d['r']):.2g}"), mirror, flag])
            cv2.circle(overlay, (int(round(d["cx"])), int(round(d["cy"]))), max(1, int(round(d["r"]))), (0, 0, 255), 1)
        for (cx, cy, r) in R["legend"]:
            cv2.circle(overlay, (int(round(cx)), int(round(cy))), int(round(r)) + 2, (0, 160, 0), 1)
        if key == "a":
            cal = (f"radius = {sa:.4f} x ({ra0:.3f} + {ka:.4f} x log10(value)) px; the bracket is the legend's own scale "
                   f"(legend symbols Min 1 / Med 883 / Max 15511 measured at {la[0]:.2f} / {la[1]:.2f} / {la[2]:.2f} px, "
                   f"residuals {', '.join(f'{x:+.2f}' for x in resid_a)} px), the factor {sa:.4f} scales it so that the "
                   f"largest data dot ({max(d['r'] for d in R['dots']):.2f} px) = 15511")
            chk = (f"Check: smallest dot -> {min(vals):.2f} (legend Min: 1); median of the {len(vals)} dots -> "
                   f"{np.median(vals):.0f} (legend Med: 883)")
        else:
            cal = (f"radius = {max(d['r'] for d in R['dots']) / 2.6:.4f} x value px (proportional, zero-based), scaled so "
                   f"that the largest data dot ({max(d['r'] for d in R['dots']):.2f} px) = 2.6 (legend Max); legend "
                   f"symbols Med 0.8 / Max 2.6 measured at {lb[0]:.2f} / {lb[1]:.2f} px (legend scale = data scale / "
                   f"{sb:.3f}); Min 0.0 symbol invisible")
            chk = (f"Check: median over the {len(vals_med)} cells that have a dot in A ({len(vals_med) - len(vals)} without a "
                   f"dot in B counted as 0) -> {np.median(vals_med):.3f} (legend Med: 0.8); the Med legend symbol is "
                   f"{lb[0] / (lb[1] * 0.8 / 2.6) - 1:+.0%} off this scale")
        print(key, len(out), cal, chk)
        with open(HERE / f"fig8{key}.csv", "w", newline="") as fh:
            fh.write(f"# scheffer2020 Figure 8{key.upper()}: "
                     + ("areas of the boundaries between adjacent neuropils (square microns), shown as dot size on a log scale"
                        if key == "a" else "number of excess crossings normalized by the area of the neuropil boundary, shown as dot size")
                     + ".\n")
            fh.write("# Provenance: tier 3, digitized from the embedded raster image (lossless, 1132x2450 px) on PDF p. 19 by "
                     "figures/fig8_extract.py (method and calibration in its docstring). The authors' Figure 8-source data 1 "
                     "(online) is not available locally.\n")
            fh.write("# Rows/columns: category axes with the 35 region labels as printed; one CSV row per non-empty cell "
                     "(empty cell = no dot). row_region = label on the y axis, col_region = label on the x axis. The three "
                     "cells of column AB(L) under the size legend (rows AB(L), AB(R), AL(R)) are skipped.\n")
            fh.write(f"# Size calibration (assumed model, semi-quantitative): {cal}.\n")
            fh.write(f"# {chk}.\n")
            fh.write("# Columns: dx_px, dy_px = dot centre minus gridline crossing; r_px = dot radius in source pixels (median over 72 rays; r10_px/r90_px = 10th/90th "
                     "percentile over the rays); value = " + ("boundary area in square microns" if key == "a" else
                                                             "excess crossings per boundary area (units as in the paper)")
                     + " from the calibration; value_unc = effect of +-0.1 px in radius (mirror cells agree to 0.03-0.05 px rms; not including the calibration "
                     "model); mirror = the transposed cell also has a dot; flag (ok / tiny_area_radius = radius from the weighted area of a dot under 2.5 px, uncertain / irregular_edge = r90 - r10 > 1.0 px: "
                     "dot touches a neighbour or is ragged).\n")
            wr = csv.writer(fh)
            wr.writerow(["row_region", "col_region", "dx_px", "dy_px", "r_px", "r10_px", "r90_px", "value", "value_unc", "mirror", "flag"])
            wr.writerows(out)
    cv2.imwrite(str(WORK / "fig8_overlay.png"), overlay)


if __name__ == "__main__":
    main()
