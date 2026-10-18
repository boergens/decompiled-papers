"""Helpers for the gabricevic2020 digitizing scripts (figN_extract.py), on top of tools/digitize_common.py.

All plots in this paper (main PDF and the SI .docx) are raster images, so every extraction is tier 3:
  - source images: main figures are the embedded images of poc.4045.pdf (read with PyMuPDF via
    digitize_common.embedded_image); SI figures are the TIFFs inside the SI .docx (word/media/imageN.tiff),
    read straight from the .docx with zipfile + PIL;
  - axes: tick marks found with digitize_common.tick_positions[_v], labels read off the figure by eye,
    linear (or log10) fit with digitize_common.fit_axis;
  - series: colour masks that allow for anti-aliasing (a pixel is W + alpha*(ref - W) + residual, W = white),
    then either a continuity tracker (lines, dense marker bands) or connected components (scatter markers).
"""
import io
import os
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.normpath(os.path.join(HERE, "../tools"))
sys.path.insert(0, TOOLS)
import numpy as np  # noqa: E402
from digitize_common import (embedded_image, gray, tick_positions, tick_positions_v, fit_axis,  # noqa: E402,F401
                             write_csv, overlay, frame_lines)

PAPER = os.path.normpath(os.path.join(HERE, "../source"))
PDF = os.path.join(PAPER, "poc.4045.pdf")
DOCX = os.path.join(PAPER, "poc4045-sup-0001-supporting_information.docx")
WORK = os.path.normpath(os.path.join(HERE, "../work"))

# placement bboxes (PDF points) of the embedded figure images in poc.4045.pdf
MAIN = {"fig1": (3, (307, 46, 548, 219)), "fig2": (3, (307, 498, 548, 676)), "fig3": (4, (47, 505, 288, 676)),
        "fig4": (4, (309, 502, 550, 676)), "fig5": (5, (46, 46, 287, 221)), "fig6": (5, (307, 46, 548, 386)),
        "fig7": (6, (47, 46, 288, 218))}
# SI figure -> image inside the .docx (Fig. S1..S3 are image1..3.tiff, in document order)
SI = {"sfig1": "word/media/image1.tiff", "sfig2": "word/media/image2.tiff", "sfig3": "word/media/image3.tiff"}


def load(fig):
    """RGB uint8 array of the source raster of a figure, at its native resolution."""
    if fig in MAIN:
        page, bb = MAIN[fig]
        return embedded_image(PDF, page, bbox_near=bb)
    from PIL import Image
    with zipfile.ZipFile(DOCX) as z:
        return np.array(Image.open(io.BytesIO(z.read(SI[fig]))).convert("RGB"))


def colour_mask(a, ref, alpha_min=0.5, alpha_max=1.3, tol=45):
    """Pixels that look like colour `ref` blended with white (anti-aliased edges included)."""
    d = a.astype(float) - 255.0
    r = np.asarray(ref, float) - 255.0
    alpha = (d @ r) / (r @ r)
    res = np.linalg.norm(d - alpha[..., None] * r, axis=-1)
    return (alpha >= alpha_min) & (alpha <= alpha_max) & (res <= tol)


def runs_in_column(col_mask, y0, y1):
    r = np.where(col_mask[y0:y1])[0]
    if len(r) == 0:
        return []
    parts = np.split(r, np.where(np.diff(r) > 1)[0] + 1)
    return [(y0 + p[0], y0 + p[-1]) for p in parts]


def track(mask, x_seed, y_seed, x0, x1, y0, y1, max_jump=6, max_gap=25, max_run=None):
    """Follow one curve through `mask` from a seed pixel, column by column, left and right.

    In each column the run of mask pixels nearest to the prediction (last position + local slope)
    is taken if it lies within max_jump (+1 px per skipped column); otherwise the column is skipped.
    The slope is a least-squares fit over the last 10 accepted columns.
    Runs longer than max_run (e.g. a crossing curve or a legend box) are ignored.
    Returns dict x -> (top, bottom) pixel rows of the chosen run.
    """
    out = {}
    for direction in (1, -1):
        hist = [(x_seed, y_seed)]
        if direction == -1 and x_seed in out:
            hist = [(x_seed, (out[x_seed][0] + out[x_seed][1]) / 2)]
        gap = 0
        c = x_seed if direction == 1 else x_seed - 1
        while x0 <= c < x1 and gap <= max_gap:
            hx = np.array([h[0] for h in hist], float)
            if len(hist) >= 3 and np.ptp(hx) >= 3:
                slope = np.polyfit(hx, [h[1] for h in hist], 1)[0]   # local slope over the last <= 10 points
            else:
                slope = 0.0
            pred = hist[-1][1] + slope * (c - hist[-1][0])
            best, bd = None, None
            for t, b in runs_in_column(mask[:, c], y0, y1):
                if max_run is not None and b - t + 1 > max_run:
                    continue
                dd = 0 if t <= pred <= b else min(abs(t - pred), abs(b - pred))
                if bd is None or dd < bd:
                    best, bd = (t, b), dd
            if best is not None and bd <= max_jump + gap:
                out[c] = best
                hist.append((c, (best[0] + best[1]) / 2))
                hist = hist[-10:]
                gap = 0
            else:
                gap += 1
            c += direction
    return dict(sorted(out.items()))


def markers(mask, min_area=20, max_area=5000):
    """Connected components of a marker mask: (x, y, area, w, h) with x, y = centre of the component's bounding box."""
    import cv2
    n, lab, st, cen = cv2.connectedComponentsWithStats(mask.astype(np.uint8), connectivity=8)
    out = []
    for i in range(1, n):
        x, y, w, h, area = st[i]
        if min_area <= area <= max_area:
            out.append((x + (w - 1) / 2, y + (h - 1) / 2, area, w, h))
    return out


def line_fit_pixels(mask, x0, x1, y0, y1):
    """Least-squares straight line through the mask pixels in a box: returns (slope, intercept) in pixels."""
    ys, xs = np.where(mask[y0:y1, x0:x1])
    xs = xs + x0
    ys = ys + y0
    m, b = np.polyfit(xs, ys, 1)
    return m, b, xs.min(), xs.max()


def scatter(a, series, box, exclude=(), alpha_min=0.55, min_area=60, tol=45, close=0, open_=0, split=False):
    """Find the markers of each (name, rgb) series inside box = (x0, y0, x1, y1), skipping `exclude` boxes.

    Marker centre = centre of the bounding box of the colour blob (Origin centres symbols on the point).
    A blob whose width or height differs by more than 2 px from the series' median marker size is flagged as
    partly hidden; its centre is then put at median half-size from the edges that border white paper. close > 0: morphological closing with a
    close x close kernel first, so a fit line drawn across a marker does not split it. open_ > 0: opening
    with an open_ x open_ disc, which removes a thin line of the same colour as the markers. Returns a list of
    (name, x_px, y_px, w, h, flag).
    """
    out = []
    for name, ref in series:
        m = colour_mask(a, ref, alpha_min=alpha_min, tol=tol)
        keep = np.zeros_like(m)
        keep[box[1]:box[3], box[0]:box[2]] = True
        for ex in exclude:
            keep[ex[1]:ex[3], ex[0]:ex[2]] = False
        m &= keep
        if close:  # bridge a thin line drawn across a marker (it splits the blob in two)
            import cv2
            k = np.ones((close, close), np.uint8)
            m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_CLOSE, k).astype(bool)
        if open_:  # remove a thin line of the marker's own colour (fit line through the markers)
            import cv2
            k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (open_, open_))
            m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_OPEN, k).astype(bool)
        found = []
        comps = markers(m, min_area=min_area)
        med_area = np.median([c[2] for c in comps]) if comps else 0
        merged = []
        if split and comps:
            # Blobs of several overlapping markers: place copies of an isolated marker's shape (template) one by one
            # where they cover the most still-uncovered blob pixels and the fewest outside pixels (greedy fit).
            import cv2
            iso = min(comps, key=lambda c: abs(c[2] - med_area))
            ix, iy, _, iw, ih = iso
            tmpl = m[int(iy - ih / 2) - 1:int(iy + ih / 2) + 2, int(ix - iw / 2) - 1:int(ix + iw / 2) + 2].astype(np.float32)
            ty, tx = np.where(tmpl > 0)
            tcy, tcx = (ty.min() + ty.max()) / 2, (tx.min() + tx.max()) / 2
            keep_comps = []
            nlab, lab, st_, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), connectivity=8)
            for comp in comps:
                cx, cy, area, w, h = comp
                if area <= 1.6 * med_area:
                    keep_comps.append(comp)
                    continue
                pad = max(tmpl.shape)
                x0, y0 = max(0, int(cx - w / 2) - pad), max(0, int(cy - h / 2) - pad)
                # this component only (not the neighbouring markers that fall into the padded window)
                li = [i for i in range(1, nlab) if st_[i][2] == w and st_[i][3] == h and
                      abs(st_[i][0] + (w - 1) / 2 - cx) < 0.6 and abs(st_[i][1] + (h - 1) / 2 - cy) < 0.6][0]
                blob = (lab[y0:int(cy + h / 2) + pad + 1, x0:int(cx + w / 2) + pad + 1] == li).astype(np.float32)
                unc = blob.copy()
                for _ in range(10):
                    score = cv2.filter2D(unc - 2.0 * (1 - blob), -1, tmpl, anchor=(0, 0), borderType=cv2.BORDER_CONSTANT)
                    yy, xx = np.unravel_index(np.argmax(score), score.shape)
                    if score[yy, xx] < 0.4 * tmpl.sum():
                        break
                    merged.append((x0 + xx + tcx, y0 + yy + tcy))
                    h_, w_ = tmpl.shape
                    sl = unc[yy:yy + h_, xx:xx + w_]
                    sl[tmpl[:sl.shape[0], :sl.shape[1]] > 0] = 0
                    if unc.sum() < 0.05 * blob.sum():
                        break
            comps = keep_comps
        for cx, cy, area, w, h in comps:
            found.append([cx, cy, w, h])
        if not found:
            continue
        mw = np.median([f[2] for f in found])
        mh = np.median([f[3] for f in found])
        white = a.min(axis=2) > 225
        for bx, by, w, h in found:
            flag = ""
            if abs(w - mw) > 2 or abs(h - mh) > 2:
                # Partly hidden: use the edges that border white paper (intact) plus the median marker size.
                x0e, x1e = bx - (w - 1) / 2, bx + (w - 1) / 2
                y0e, y1e = by - (h - 1) / 2, by + (h - 1) / 2

                def free(rows, cols):
                    return white[np.clip(rows, 0, a.shape[0] - 1)][:, np.clip(cols, 0, a.shape[1] - 1)].mean() > 0.6
                yc = np.arange(int(y0e), int(y1e) + 1)
                xc = np.arange(int(x0e), int(x1e) + 1)
                top_ok = free(np.array([int(y0e) - 2]), xc)
                bot_ok = free(np.array([int(y1e) + 2]), xc)
                left_ok = free(yc, np.array([int(x0e) - 2]))
                right_ok = free(yc, np.array([int(x1e) + 2]))
                if abs(h - mh) > 2:
                    if top_ok and not bot_ok:
                        by = y0e + (mh - 1) / 2
                    elif bot_ok and not top_ok:
                        by = y1e - (mh - 1) / 2
                if abs(w - mw) > 2:
                    if left_ok and not right_ok:
                        bx = x0e + (mw - 1) / 2
                    elif right_ok and not left_ok:
                        bx = x1e - (mw - 1) / 2
                flag = "irregular blob (partly hidden, or reshaped where the fit line was removed); centre from the edges bordering white paper + median marker size"
            out.append((name, bx, by, int(w), int(h), flag))
        for bx, by in merged:
            out.append((name, float(bx), float(by), "", "", "one of several overlapping markers in one blob; centre from a greedy fit of copies of an isolated marker"))
    return out


def read_csv(path):
    """Rows of a decompiled CSV as dicts (comment lines starting with '#' skipped)."""
    import csv
    with open(path) as f:
        return list(csv.DictReader(l for l in f if not l.startswith("#")))


def cross_overlay(a, xy_px, out_png, colour=(255, 0, 255), r=6):
    """Like digitize_common.overlay, but draws a small cross at each point (for scatter markers)."""
    im = a.copy()
    for x, y in xy_px:
        if x == x and y == y:
            xi, yi = int(round(x)), int(round(y))
            im[max(0, yi - r):yi + r + 1, max(0, xi):xi + 1] = colour
            im[max(0, yi):yi + 1, max(0, xi - r):xi + r + 1] = colour
    from PIL import Image
    Image.fromarray(im).save(out_png)


def replot(csv_name, xcol, ycol, style, xlim, ylim, xticks, yticks, xlabel, ylabel, out_name,
           logy=False, figsize=(6, 4.3), legend="best", ytick_labels=None):
    """Draw a marker+line panel from one of this paper's CSVs (columns series, kind, <x>, <y>).

    style: {series: (marker, colour)}; rows with kind 'line' are drawn as a line in the series colour.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    rows = read_csv(os.path.join(HERE, csv_name))
    fig, ax = plt.subplots(figsize=figsize)
    for name, (mk, c) in style.items():
        ln = [r for r in rows if r["series"] == name and r["kind"] == "line"]
        if ln:
            ax.plot([float(r[xcol]) for r in ln], [float(r[ycol]) for r in ln], "-", color=c, lw=1.2)
        mr = [r for r in rows if r["series"] == name and r["kind"] == "marker"]
        if mr:
            ax.plot([float(r[xcol]) for r in mr], [float(r[ycol]) for r in mr], mk, color=c, ls="", ms=7, label=name)
    for name in sorted({r["series"] for r in rows} - set(style)):
        ln = [r for r in rows if r["series"] == name]
        ax.plot([float(r[xcol]) for r in ln], [float(r[ycol]) for r in ln], "-", color="black", lw=1.2)
    if logy:
        ax.set_yscale("log")
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xticks(xticks)
    if yticks is not None:
        ax.set_yticks(yticks)
        if ytick_labels:
            ax.set_yticklabels(ytick_labels)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if legend:
        ax.legend(loc=legend, frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, out_name), dpi=150)


def replot_bands(csv_name, xcol, ycol, style, xlim, ylim, xticks, yticks, xlabel, ylabel, out_name, figsize=(6, 4.4),
                 ycol_hi="A_upper", ycol_lo="A_lower", band_kind="data band", fit_kind="fit", ax=None, legend=True):
    """Draw 'data band' rows (filled between their upper/lower edges) and 'fit' rows (thin line) per series."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    rows = read_csv(os.path.join(HERE, csv_name))
    own = ax is None
    if own:
        fig, ax = plt.subplots(figsize=figsize)
    band_kinds = sorted({r["kind"] for r in rows if r["kind"].startswith(band_kind)})
    for name, (band_c, fit_c) in style.items():
        for kind in band_kinds:
            b = [r for r in rows if r["series"] == name and r["kind"] == kind]
            if not b:
                continue
            x = np.array([float(r[xcol]) for r in b])
            hi = np.array([float(r[ycol_hi]) for r in b])
            lo = np.array([float(r[ycol_lo]) for r in b])
            gaps = np.where(np.diff(x) > 3 * np.median(np.diff(x)))[0] + 1 if len(x) > 2 else []
            for xs, h, l in zip(np.split(x, gaps), np.split(hi, gaps), np.split(lo, gaps)):
                first = xs[0] == x[0] and kind == band_kind
                ax.fill_between(xs, l, h, color=band_c, lw=0, label=name if first else None)
        f = [r for r in rows if r["series"] == name and r["kind"] == fit_kind]
        if f:
            ax.plot([float(r[xcol]) for r in f], [float(r[ycol]) for r in f], "-", color=fit_c, lw=0.8)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if legend:
        ax.legend(loc="upper center", frameon=False)
    if own:
        fig.tight_layout()
        fig.savefig(os.path.join(HERE, out_name), dpi=150)


COLOURS = {"red": "red", "blue": "blue", "teal": "teal", "magenta": "magenta", "olive": "olive", "navy": "navy",
           "wine": "#800000", "pink": "#ff0080", "royal blue": "#0000aa", "black": "black", "green": "green",
           "dark red": "#8b0000", "dark cyan": "darkcyan", "orange": "orange", "violet": "violet", "purple": "purple",
           "dark yellow": "#b8860b", "grey": "grey", "dark blue": "#00008b", "dark green": "darkgreen", "cyan": "cyan",
           "brown": "#8b4513", "dark magenta": "darkmagenta", "dark pink": "#c71585", "light blue": "#6495ed"}


def replot_spectra(csv_name, xlim, ylim, xticks, yticks, out_name, xcol="wavelength_nm", ycol="A",
                   xlabel="$\\lambda$ (nm)", ylabel="$A$", figsize=(6, 4.3), ax=None):
    """Draw every series of a spectra CSV as a line in its named colour, breaking it where columns are missing."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    rows = read_csv(os.path.join(HERE, csv_name))
    own = ax is None
    if own:
        fig, ax = plt.subplots(figsize=figsize)
    names = list(dict.fromkeys(r["series"] for r in rows))
    for name in names:
        rr = [r for r in rows if r["series"] == name]
        x = np.array([float(r[xcol]) for r in rr])
        y = np.array([float(r[ycol]) for r in rr])
        step = np.median(np.diff(x))
        gaps = np.where(np.diff(x) > 2.5 * step)[0] + 1
        x = np.insert(x, gaps, np.nan)
        y = np.insert(y, gaps, np.nan)
        ax.plot(x, y, "-", color=COLOURS.get(name, "grey"), lw=1)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if own:
        fig.tight_layout()
        fig.savefig(os.path.join(HERE, out_name), dpi=150)
    return ax


def replot_inset(csv_name, xlim, ylim, xticks, yticks, xlabel, ylabel, out_name, xcol="ratio", ycol="A",
                 figsize=(4.5, 3.4), line_colours=None):
    """Draw an inset CSV: grey diamonds + straight dotted/dashed lines given by their two ends."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    rows = read_csv(os.path.join(HERE, csv_name))
    fig, ax = plt.subplots(figsize=figsize)
    mk = [r for r in rows if r["kind"] == "marker"]
    ax.plot([float(r[xcol]) for r in mk], [float(r[ycol]) for r in mk], "D", color="grey", ms=7, ls="")
    for name in dict.fromkeys(r["series"] for r in rows if r["kind"] == "line end"):
        ln = [r for r in rows if r["series"] == name]
        ls = ":" if "dotted" in name else "--"
        c = "red" if "red" in name else "darkorange"
        ax.plot([float(r[xcol]) for r in ln], [float(r[ycol]) for r in ln], ls, color=c, lw=1.3)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, out_name), dpi=150)
