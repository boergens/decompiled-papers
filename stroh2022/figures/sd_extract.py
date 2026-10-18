"""Digitize the eLife "Source data" PDFs of Ströh et al. 2022 (Figure 1—source data 1-5, Figure 2—source data 1-2).

Each source-data PDF is image-only: one 2441 x 1370 px raster per page, a MATLAB figure for one sample with
  - a page title (solution, sample ID),
  - top row: 6 line plots, intensity (a.u.) vs time t (min) at depths x = 200 ... 1200 μm,
  - middle row: 6 line plots, intensity (a.u.) vs depth x (μm) at t = 30 ... 1200 min,
    (blue = measured data; black = model, only in Figure 1—source data 1; small black circles on some depth plots),
  - bottom row: colour map "data" (and "model: R2adj=..., SEres=..." in Figure 1—source data 1), depth x vs time t,
    with colour bar "Intensity (a.u.)", and two projection images "t=0min" / "t=...min" (not data plots).

This script finds every axes box (frame colour RGB 38,38,38), the tick marks (mirrored on both sides of the box),
reads the tick labels by matching each glyph to digit templates taken from labels read by eye
(sd_templates.py; checked by a robust linear fit, sdlayout.robust_ticks), takes the printed titles from sd_titles.py (read by eye;
tesseract OCR is kept in the calibration file as a check), fits the
pixel->data map per axis, traces the blue and black lines per pixel column (top/bottom of the line in each column,
so the noise range of the data in that column is kept), finds the black circles (Hough transform), and maps every
colour-map pixel through the colour bar.

    python3 -I sd_extract.py fig1-data1        (or any of fig1-data1..5, fig2-data1..2, or 'all')

Outputs (next to this script):
    sd/<stem>_traces.csv      all line-plot traces of that PDF (tidy rows)
    sd/<stem>_maps/<stem>_pNN_<data|model>.csv   colour-map grids (one row per pixel row)
    sd/<stem>_calibration.csv per page and axes: tick values and fit residuals; OCR'd titles
    ../work/sd_ov/<stem>_pNN.png overlays of the extracted points on the page image
"""
import csv
import os
import subprocess
import sys

import numpy as np
import pymupdf
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "../tools"))
from sdlayout import boxes, ticks, label_crop, robust_ticks, colorbar, frame_mask, groups, read_label  # noqa: E402
from digitize_common import trace_envelope  # noqa: E402
from sd_titles import T as TITLES  # noqa: E402  (titles read by eye; OCR only as a check)

TPLF = os.path.join(HERE, "sd_templates.npz")  # digit templates, made by sd_templates.py
TPL = {k: v for k, v in np.load(TPLF).items()} if os.path.exists(TPLF) else None
SRC = os.path.join(HERE, "../source")
OUT = os.path.join(HERE, "sd")
OV = os.path.join(HERE, "../work/sd_ov")
DEPTHS = [200, 400, 600, 800, 1000, 1200]
TIMES = [30, 60, 120, 360, 600, 1200]
FILES = {
    "fig1-data1": "Figure 1—source data 1 (OsO4, n=13)",
    "fig1-data2": "Figure 1—source data 2 (Ferro-redOs, n=6)",
    "fig1-data3": "Figure 1—source data 3 (Ferro-redOs + 5.56% formamide, n=4)",
    "fig1-data4": "Figure 1—source data 4 (Ferro-redOs + 11.25% formamide, n=4)",
    "fig1-data5": "Figure 1—source data 5 (Ferri-redOs, n=2)",
    "fig2-data1": "Figure 2—source data 1 (washout in K4[Fe(CN)6], n=6)",
    "fig2-data2": "Figure 2—source data 2 (washout in K3[Fe(CN)6], n=4)",
}


def page_images(stem):
    doc = pymupdf.open(os.path.join(SRC, f"elife-72147-{stem}-v2.pdf"))
    for i, p in enumerate(doc):
        pix = pymupdf.Pixmap(doc, p.get_images()[0][0])
        a = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3].copy()
        yield i + 1, a


def ocr_text(img, scale=3):
    import tempfile
    im = Image.fromarray(img).convert("L")
    im = im.resize((im.width * scale, im.height * scale), Image.LANCZOS)
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "x.png")
        im.save(p)
        return subprocess.run(["tesseract", p, "-", "--psm", "7"], capture_output=True, text=True).stdout.strip()


def fit(px, val):
    A = np.vstack([px, np.ones(len(px))]).T
    (m, b), *_ = np.linalg.lstsq(A, np.asarray(val, float), rcond=None)
    res = float(np.max(np.abs(A @ [m, b] - val))) if len(px) > 2 else float("nan")
    return m, b, res


def blue_mask(a):
    ai = a.astype(int)
    return (ai[:, :, 2] > 200) & (ai[:, :, 2] - ai[:, :, 0] > 60) & (abs(ai[:, :, 0] - ai[:, :, 1]) < 25)


def black_mask(a):
    ai = a.astype(int)
    neutral = (abs(ai[:, :, 0] - ai[:, :, 1]) < 15) & (abs(ai[:, :, 1] - ai[:, :, 2]) < 15)
    return neutral & (ai.mean(2) < 150) & ~frame_mask(a)


def find_circles(blk, box):
    """Black circle markers (radius ~9-12 px) inside a box: returns list of (cx, cy, r) in page pixels."""
    import cv2
    r0, r1, c0, c1 = box
    sub = (blk[r0 - 15:r1 + 15, c0 - 15:c1 + 15] * 255).astype(np.uint8)
    cs = cv2.HoughCircles(sub, cv2.HOUGH_GRADIENT, dp=1, minDist=30, param1=50, param2=14, minRadius=8, maxRadius=14)
    out = []
    if cs is not None:
        for x, y, r in cs[0]:
            # keep only real rings: >= 70 % of the ring pixels dark
            ang = np.linspace(0, 2 * np.pi, 60, endpoint=False)
            xx = np.round(x + r * np.cos(ang)).astype(int)
            yy = np.round(y + r * np.sin(ang)).astype(int)
            ok = np.mean([sub[max(0, j - 1):j + 2, max(0, i - 1):i + 2].any() for i, j in zip(xx, yy)])
            if ok >= 0.7:
                out.append((x + c0 - 15, y + r0 - 15, r))
    return out


def run(stem):
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(os.path.join(OUT, f"{stem}_maps"), exist_ok=True)
    os.makedirs(OV, exist_ok=True)
    trace_rows, cal_rows = [], []
    for pno, a in page_images(stem):
        title_ocr = ocr_text(a[0:40, 600:1840])
        title = TITLES[stem][pno - 1][0]
        bx = boxes(a)
        lines = [b for b in bx if b[3] - b[2] < 312]
        maps = [b for b in bx if b[3] - b[2] >= 312]
        assert len(lines) == 12, (stem, pno, bx)
        rows = sorted(set(b[0] for b in lines))
        blue, blk = blue_mask(a), black_mask(a)
        ov = a.copy()
        # calibration per box; a box whose ticks are hidden by the curves borrows them from a sibling box of the
        # same row (same size, so the same tick offsets relative to the frame), noted in the calibration file
        cal = {}
        for b in lines:
            ys, xs = ticks(a, b)
            yv, nag, note = robust_ticks(ys, [read_label(label_crop(a, b, "y", y), TPL)[0] for y in ys]) if len(ys) >= 2 else (None, 0, "")
            xv, xnag, xnote = robust_ticks(xs, [read_label(label_crop(a, b, "x", x), TPL)[0] for x in xs]) if len(xs) >= 2 else (None, 0, "")
            cal[b] = dict(ys=ys, yv=yv, ny=nag, ynote=note, xs=xs, xv=xv, nx=xnag, xnote=xnote)
        for b in lines:
            c = cal[b]
            sib = [s for s in lines if s[0] == b[0] and s != b and abs((s[3] - s[2]) - (b[3] - b[2])) <= 1]
            if c["yv"] is None or c["ny"] < 2:
                s = max(sib, key=lambda q: (cal[q]["ny"], -abs(q[2] - b[2])))
                c.update(ys=cal[s]["ys"], yv=cal[s]["yv"], ny=cal[s]["ny"], ynote=f"y ticks borrowed from box at col {s[2]}")
            if c["xv"] is None or c["nx"] < 2:
                s = max(sib, key=lambda q: (cal[q]["nx"], -abs(q[2] - b[2])))
                c.update(xs=[x - s[2] + b[2] for x in cal[s]["xs"]], xv=cal[s]["xv"], nx=cal[s]["nx"],
                         xnote=f"x ticks borrowed from box at col {s[2]}")
        for b in lines:
            r0, r1, c0, c1 = b
            row = rows.index(r0)
            col = sorted(x[2] for x in lines if x[0] == r0).index(c0)
            ptitle = ocr_text(a[r0 - 32:r0 - 4, c0 + 20:c1 - 20])
            panel = f"x={DEPTHS[col]} μm" if row == 0 else f"t={TIMES[col]} min"
            c = cal[b]
            ys, yv, nag, note, xs, xv, xnote = c["ys"], c["yv"], c["ny"], c["ynote"], c["xs"], c["xv"], c["xnote"]
            my, by, yres = fit(ys, yv)
            mx, bx_, xres = fit(xs, xv)
            x_at_c0 = mx * c0 + bx_
            cal_rows.append([stem, pno, panel, f"{c0},{c1},{r0},{r1}", "y", " ".join(map(str, yv)), nag, note,
                             f"{yres:.4g}", " ".join(map(str, xv)), xnote, f"{xres:.4g}", f"{x_at_c0:.1f}", ptitle, title_ocr])
            for name, mask in (("data", blue), ("model", blk)):
                mk = mask.copy()
                circles = []
                if name == "model":
                    circles = find_circles(blk, b)
                    yy, xx = np.mgrid[r0:r1, c0:c1]
                    for cx, cy, r in circles:
                        ring = (abs(np.hypot(xx - cx, yy - cy) - r) <= 2.5)
                        mk[r0:r1, c0:c1] &= ~ring
                    for cx, cy, r in circles:
                        trace_rows.append([stem, pno, title, panel, "circle", f"{mx * cx + bx_:.5g}",
                                           f"{my * cy + by:.5g}", "", "", f"{abs(mx) * r:.3g}"])
                        for t in np.linspace(0, 2 * np.pi, 40):
                            ov[int(cy + r * np.sin(t)), int(cx + r * np.cos(t))] = (0, 200, 0)
                # exclude the frame lines themselves and the tick marks (3 px inside the frame)
                env = trace_envelope(mk, c0 + 1, c1, r0 + 1, r1, half_width=0, min_px=1)
                if name == "model" and np.isfinite(env[:, 1]).sum() < 0.2 * len(env):
                    continue  # no model curve in this plot
                for c, ym, yu, yl in env:
                    if ym == ym:
                        trace_rows.append([stem, pno, title, panel, name, f"{mx * c + bx_:.5g}", f"{my * ym + by:.5g}",
                                           f"{my * yu + by:.5g}", f"{my * yl + by:.5g}", ""])
                        ov[int(round(ym)), int(c)] = (255, 0, 255) if name == "data" else (255, 140, 0)
        # colour maps
        for k, b in enumerate(sorted(maps, key=lambda q: q[2])):
            r0, r1, c0, c1 = b
            mtitle_ocr = ocr_text(a[r0 - 34:r0 - 2, c0 - 60:c1 + 60])
            kind = "data" if k == 0 else "model"
            t_ = TITLES[stem][pno - 1]
            mtitle = "data" if kind == "data" else f"model: R2adj={t_[1]}, SEres={t_[2]}"
            ys, xs = ticks(a, b)
            yv, nag, note = robust_ticks(ys, [read_label(label_crop(a, b, "y", y), TPL)[0] for y in ys])
            xv, xnag, xnote = robust_ticks(xs, [read_label(label_crop(a, b, "x", x), TPL)[0] for x in xs])
            my, by, yres = fit(ys, yv)
            mx, bx_, xres = fit(xs, xv)
            cb = colorbar(a, b)
            m = frame_mask(a)
            cbt = groups(np.where(m[cb[0]:cb[1] + 1, cb[3] - 2:cb[3] + 1].all(1))[0] + cb[0])
            crop = lambda t: np.pad(a[t - 13:t + 14, cb[3] + 4:cb[3] + 75], ((6, 6), (6, 6), (0, 0)), constant_values=255)
            cblab = [read_label(crop(t), TPL, side="left")[0] for t in cbt]
            cv, cnag, cnote = robust_ticks(cbt, cblab)
            mc, bc, cres = fit(cbt, cv)
            cal_rows.append([stem, pno, f"map {kind}", f"{c0},{c1},{r0},{r1}", "y", " ".join(map(str, yv)), nag, note,
                             f"{yres:.4g}", " ".join(map(str, xv)), xnote, f"{xres:.4g}",
                             f"colourbar rows {cb[0]}-{cb[1]} ticks {' '.join(map(str, cv))} res {cres:.3g} {cnote}",
                             mtitle_ocr, title_ocr])
            # colour bar lookup: mean colour of the inner bar columns per row
            bar = a[cb[0]:cb[1] + 1, cb[2] + 3:cb[3] - 3].astype(float).mean(1)
            barval = mc * np.arange(cb[0], cb[1] + 1) + bc
            img = a[r0 + 1:r1, c0 + 1:c1].astype(float)
            val = np.empty(img.shape[:2])
            dist = np.empty(img.shape[:2])
            for i in range(img.shape[0]):
                d = ((img[i][:, None, :] - bar[None, :, :]) ** 2).sum(2)
                val[i] = barval[d.argmin(1)]
                dist[i] = np.sqrt(d.min(1))
            val[dist > 40] = np.nan  # tick marks / not on the colour scale
            tcol = mx * np.arange(c0 + 1, c1) + bx_
            drow = my * np.arange(r0 + 1, r1) + by
            fn = os.path.join(OUT, f"{stem}_maps", f"{stem}_p{pno:02d}_{kind}.csv")
            with open(fn, "w") as f:
                f.write(f"# Ströh et al. 2022 eLife, {FILES[stem]}, PDF page {pno} ('{title}'), colour map '{kind}'"
                        f" ({mtitle}).\n")
                f.write("# Grid: one row per pixel row of the map (depth_um, top = deepest), one column per pixel column"
                        " (header = time t in min). Values = Intensity (a.u.) read through the colour bar.\n")
                f.write(f"# Provenance: tier 3, digitized from the authors' source-data plots (raster page image, 2441x1370 px)"
                        f" by sd_extract.py. Axes fitted on ticks {xv} (time) and {yv} (depth); colour bar ticks {cv},"
                        f" fit residual {cres:.3g}.\n")
                f.write(f"# Uncertainty: ±{abs(mx):.1f} min and ±{abs(my):.1f} μm (1 px); the colour bar is drawn in"
                        f" discrete bands, so values are quantized to about ±{abs(mc) * 3:.3f}. Empty = pixel not on the"
                        " colour scale (tick marks).\n")
                f.write("depth_um," + ",".join(f"{t:.1f}" for t in tcol) + "\n")
                for dr, rowv in zip(drow, val):
                    f.write(f"{dr:.1f}," + ",".join("" if v != v else f"{v:.4f}" for v in rowv) + "\n")
        Image.fromarray(ov).save(os.path.join(OV, f"{stem}_p{pno:02d}.png"))
        print(stem, pno, title, flush=True)
    with open(os.path.join(OUT, f"{stem}_traces.csv"), "w", newline="") as f:
        f.write(f"# Ströh et al. 2022 eLife, {FILES[stem]}: per-sample line plots of the source-data PDF"
                f" elife-72147-{stem}-v2.pdf (one PDF page per sample).\n")
        f.write("# Columns: page = PDF page; sample = page title as printed (read by eye, sd_titles.py);"
                " panel = plot title ('x=200 μm' = intensity vs time t at that depth; 't=30 min' = intensity vs depth x at"
                " that time); series = data (blue) | model (black, Figure 1—source data 1 only) | circle (black circle"
                " marker: x, y = its centre, r_x = its radius in x units);\n")
        f.write("#   x = time t (min) for 'x=' panels or depth x (μm) for 't=' panels; y = Intensity (a.u.) at the centre"
                " of the line in that pixel column; y_upper / y_lower = top / bottom of the line in that column (the"
                " noisy data trace covers a vertical range per column).\n")
        f.write("# Provenance: tier 3, digitized from the authors' source-data plots (raster images, no numbers in the"
                " PDF) by sd_extract.py: axes calibrated on the tick marks, tick labels read by glyph-template matching (sd_templates.py) and checked (see"
                f" {stem}_calibration.csv), one row per pixel column.\n")
        f.write("# Uncertainty: about ±4.1 min or ±4.1 μm in x (1 px) and ±0.003-0.005 (a.u.) in y (1 px), plus the"
                " line width. Where the blue and black lines overlap, the hidden one has no row for that column.\n")
        w = csv.writer(f)
        w.writerow(["page", "sample", "panel", "series", "x", "y", "y_upper", "y_lower", "r_x"])
        for r in trace_rows:
            w.writerow(r[1:])
    with open(os.path.join(OUT, f"{stem}_calibration.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["file", "page", "panel", "box_c0_c1_r0_r1", "axis", "y_tick_values", "y_labels_agreeing",
                    "y_ocr_corrections", "y_fit_max_residual", "x_tick_values", "x_ocr_corrections", "x_fit_max_residual",
                    "x_at_left_frame_or_colourbar", "panel_title_ocr", "page_title_ocr (the CSVs use sd_titles.py)"])
        w.writerows(cal_rows)


if __name__ == "__main__":
    stems = list(FILES) if sys.argv[1] == "all" else sys.argv[1:]
    for s in stems:
        run(s)
