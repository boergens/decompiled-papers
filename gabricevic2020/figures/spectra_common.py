"""Shared code for the multi-curve absorption spectra of gabricevic2020 (Fig. 1, SI Figs. S1-S3) and their insets.

Each spectrum is followed column by column through a colour mask from a seed point where it is well separated
(gab_common.track). Several spectra in one panel can share a colour and some are bunched within a few pixels
of each other; each traced point therefore carries flags:
  overlap  - another traced spectrum passes within OVERLAP_PX px in this column (the colour assignment may be
             wrong there and the value can belong to a neighbour);
  clipped  - the curve runs into the top frame (its true value is higher).
"""
import numpy as np

from gab_common import colour_mask, track, runs_in_column

OVERLAP_PX = 4


def trace_spectra(a, specs, box, exclude=(), fx=None, fy=None, top_frame=None):
    """specs: list of dicts name, rgb, seed=(col,row), optional tol, alpha_min, max_run, max_jump, max_gap,
    extra_seeds=[(col, row, col_min, col_max)], region=(func(c)->(r0,r1))).

    Returns {name: {col: (top, bottom)}} and the rows (name, x, y_mid, y_upper, y_lower, flags) in data units.
    """
    x0, y0, x1, y1 = box
    traces = {}
    for s in specs:
        m = colour_mask(a, s["rgb"], alpha_min=s.get("alpha_min", 0.5), alpha_max=s.get("alpha_max", 1.3),
                        tol=s.get("tol", 50))
        keep = np.zeros_like(m)
        keep[y0:y1, x0:x1] = True
        for e in exclude:
            keep[e[1]:e[3], e[0]:e[2]] = False
        m &= keep
        if "region" in s:
            for c in range(x0, x1):
                lo, hi = s["region"](c)
                if lo is None:
                    m[:, c] = False
                else:
                    m[:int(lo), c] = False
                    m[int(hi) + 1:, c] = False
        c0, r0 = s["seed"]
        # snap the seed to the nearest mask run in its column
        runs = runs_in_column(m[:, c0], y0, y1)
        assert runs, (s["name"], "no mask pixels at seed column")
        t, b = min(runs, key=lambda q: abs((q[0] + q[1]) / 2 - r0))
        kw = dict(max_jump=s.get("max_jump", 4), max_gap=s.get("max_gap", 12), max_run=s.get("max_run", 14))
        tr = track(m, c0, (t + b) / 2, x0, x1, y0, y1, **kw)
        # extra seeds: (col, row, col_min, col_max) for pieces of the same line that the tracker cannot reach
        # (e.g. beyond a point where all lines cross); only columns not traced yet are added
        for (ec, er, cmin, cmax) in s.get("extra_seeds", []):
            runs = runs_in_column(m[:, ec], y0, y1)
            t, b = min(runs, key=lambda q: abs((q[0] + q[1]) / 2 - er))
            for c, v in track(m, ec, (t + b) / 2, max(x0, cmin), min(x1, cmax), y0, y1, **kw).items():
                tr.setdefault(c, v)
        traces[s["name"]] = dict(sorted(tr.items()))
    rows = []
    for name, tr in traces.items():
        for c, (t, b) in tr.items():
            mid = (t + b) / 2
            flags = []
            for other, tro in traces.items():
                if other != name and c in tro and abs((tro[c][0] + tro[c][1]) / 2 - mid) <= OVERLAP_PX:
                    flags.append("overlap")
                    break
            if top_frame is not None and t <= top_frame + 2:
                flags.append("clipped")
            rows.append((name, float(fx(c)), float(fy(mid)), float(fy(t)), float(fy(b)), " ".join(flags)))
    return traces, rows


def hue_mask(a, kind):
    """Saturated red or orange pixels (the dotted/dashed lines of the insets; colour_mask confuses the two)."""
    R, G, B = (a[..., i].astype(int) for i in range(3))
    if kind == "red":
        return (R > 180) & (G < 110) & (B < 110) & (R - G > 100)
    if kind == "orange":
        return (R > 200) & (G >= 110) & (G < 200) & (B < 120) & (R - B > 110)
    raise ValueError(kind)


def straight_line(a, mask, box, fx, fy, exclude_mask=None):
    """Fit y = m x + b (in data units) to the pixels of a dotted/dashed straight line (bool mask) inside box.

    Returns slope, intercept, x range covered by the pixels, the pixel coordinates used, and the rms residual.
    """
    m = mask.copy()
    keep = np.zeros_like(m)
    keep[box[1]:box[3], box[0]:box[2]] = True
    m &= keep
    if exclude_mask is not None:
        m &= ~exclude_mask
    ys, xs = np.where(m)
    # robust: Theil-Sen line in pixels, keep pixels within 3 px of it, then least squares on those
    from scipy.stats import theilslopes
    sub = np.linspace(0, len(xs) - 1, min(len(xs), 400)).astype(int)
    pm, pb, _, _ = theilslopes(ys[sub], xs[sub])
    ok = np.abs(ys - (pm * xs + pb)) <= 3
    xs, ys = xs[ok], ys[ok]
    X, Y = fx(xs), fy(ys)
    slope, icpt = np.polyfit(X, Y, 1)
    res = Y - (slope * X + icpt)
    return slope, icpt, (X.min(), X.max()), (xs, ys), float(np.sqrt(np.mean(res ** 2)))


def extract_si_spectra(fig, cfg):
    """Main spectra panel (+ optional inset) of an SI figure; writes <fig>main.csv / <fig>inset.csv or <fig>.csv.

    cfg keys: title (list of header lines), frame dict(left, right, top, bottom) (pixel lines), xticks/xlabels,
    yticks/ylabels (labelled ticks used for the fit), specs (trace_spectra specs), inset (None or dict with frame,
    xlabels, ylabels, title, xname, yname), exclude (boxes), out (csv base name).
    """
    import os
    from gab_common import (load, gray, tick_positions, tick_positions_v, fit_axis, write_csv, overlay, cross_overlay,
                            scatter, colour_mask, HERE, WORK)
    a = load(fig)
    dark = gray(a) < 120
    F = cfg["frame"]
    xt = tick_positions(dark, (F["bottom"], F["bottom"]), 1, 10, F["left"] + 3, F["right"] - 2)
    yt = tick_positions_v(dark, (F["left"] - 1, F["left"]), -1, 10, F["top"] + 2, F["bottom"] - 2)
    assert len(xt) == len(cfg["xlabels"]) and len(yt) == len(cfg["ylabels"]), (xt, yt)
    # the left frame and the bottom frame carry the first labels (e.g. 260 nm is not printed, 0.0 is)
    fx, rx, sx = fit_axis(xt, cfg["xlabels"])
    fy, ry, sy = fit_axis(yt + [F["bottom"] + 0.0], cfg["ylabels"] + [cfg["ybottom"]])
    box = (F["left"] + 2, F["top"] + 2, F["right"] - 1, F["bottom"] - 1)
    traces, rows = trace_spectra(a, cfg["specs"], box, exclude=cfg.get("exclude", ()), fx=fx, fy=fy,
                                 top_frame=F["top"])
    names = [s["name"] for s in cfg["specs"]]
    rows.sort(key=lambda r: (names.index(r[0]), r[1]))
    cover = {n: (fx(min(tr)), fx(max(tr)), len(tr)) for n, tr in traces.items()}
    pts = [(c, (t + b) / 2) for tr in traces.values() for c, (t, b) in tr.items()]
    base = cfg["out"]
    write_csv(os.path.join(HERE, base + ".csv"), cfg["title"] + [
        "Columns: series = the line colour as it appears in the image (the figure has no legend); wavelength_nm =",
        "  lambda (nm); A = absorbance at the line centre in this pixel column; A_upper/A_lower = top and bottom of the line",
        f"  in the column; flags: 'overlap' = another traced spectrum passes within {OVERLAP_PX} px (about {OVERLAP_PX * abs(sy):.3f} A),",
        "  so the colour assignment and value are uncertain there; 'clipped' = the line runs into the top frame. One row per",
        "  pixel column where the line's colour is visible; columns where it is hidden under other lines are missing.",
        f"Provenance: tier 3, digitized from the SI figure's embedded TIFF ({a.shape[1]} x {a.shape[0]} px, 220 ppi, read from the",
        f"  .docx) by {fig}_extract.py. x calibrated on {len(xt)} labelled ticks, max residual {rx:.2g} nm (frames:",
        f"  {float(fx(F['left'])):.1f} and {float(fx(F['right'])):.1f} nm); y on {len(yt)} labelled ticks and the bottom frame"
        f" ({cfg['ybottom']}), max residual {ry:.2g};",
        f"  top frame = {float(fy(F['top'])):.3f}. Lines followed column by column through colour masks from a seed where each is clear.",
        f"Uncertainty: about +-{2 * abs(sx):.1f} nm and +-{2 * abs(sy):.3f} A (2 px) where a line is isolated; more where flagged.",
        "Coverage (nm from-to, columns): " + "; ".join(f"{n} {v[0]:.0f}-{v[1]:.0f} ({v[2]})" for n, v in cover.items()),
    ], ["series", "wavelength_nm", "A", "A_upper", "A_lower", "flags"], rows, fmt="{:.5g}")
    print(fig, "x res", rx, "y res", ry, cover)
    out = {"fx": fx, "fy": fy, "rx": rx, "ry": ry, "cover": cover, "xt": xt, "yt": yt}
    mk = []
    I = cfg.get("inset")
    if I:
        G = I["frame"]
        ixt = tick_positions(dark, (G["bottom"], G["bottom"] + 1), 1, 8, G["left"] + 3, G["right"] - 2)
        iyt = tick_positions_v(dark, (G["left"], G["left"] + 1), -1, 8, G["top"] + 2, G["bottom"] - 2)
        assert len(ixt) == len(I["xlabels"]) and len(iyt) == len(I["ylabels"]), (ixt, iyt)
        ifx, irx, isx = fit_axis([G["left"] + 0.5] + ixt, [0] + I["xlabels"])
        if I["ybottom"] is None:      # bottom frame not labelled: ticks only
            ify, iry, isy = fit_axis(iyt, I["ylabels"])
        else:
            ify, iry, isy = fit_axis(iyt + [G["bottom"] + 0.5], I["ylabels"] + [I["ybottom"]])
        ibox = (G["left"] + 3, G["top"] + 2, G["right"] - 1, G["bottom"] - 1)
        # the SI diamonds are dithered (speckled grey): close the mask before finding the blobs
        found = scatter(a, [("data", I["marker_rgb"])], ibox, alpha_min=0.6, min_area=30, split=True, tol=30, close=3)
        irows = [("data", "marker", float(ifx(x)), float(ify(y)), w, h, f) for n, x, y, w, h, f in found]
        irows.sort(key=lambda r: r[2])
        mk = [(x, y) for n, x, y, w, h, f in found]
        import cv2
        grey = cv2.dilate(colour_mask(a, I["marker_rgb"], alpha_min=0.3, tol=40).astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
        ora = hue_mask(a, "orange")
        lines = {}
        sl, ic, (xa, xb), (xs, ys), rms = straight_line(a, ora, ibox, ifx, ify, exclude_mask=grey)
        lines["orange dashed line"] = (sl, ic, xa, xb, rms, len(xs))
        red = hue_mask(a, "red") & ~ora
        # the orange dashes have red-looking cores: drop red pixels within 4 px of the orange line
        yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]
        o = np.argsort(xs)
        near = np.abs(yy - np.interp(xx, xs[o], ys[o])) <= 4
        sl2, ic2, (xa2, xb2), (xs2, ys2), rms2 = straight_line(a, red & ~near, ibox, ifx, ify, exclude_mask=grey)
        lines["red dotted line"] = (sl2, ic2, xa2, xb2, rms2, len(xs2))
        for lname, (s_, i_, a_, b_, _, _) in lines.items():
            for xv in (a_, b_):
                irows.append((lname, "line end", float(xv), float(s_ * xv + i_), "", "", ""))
        pts += list(zip(xs, ys)) + list(zip(xs2, ys2))
        write_csv(os.path.join(HERE, I["out"] + ".csv"), I["title"] + [
            f"Columns: series ('data' = grey diamonds; the two straight lines); kind = marker or 'line end' (the two ends of",
            f"  a straight line fitted to that line's pixels); ratio = {I['xname']}; {I['ycol']} = {I['yname']}; marker size; note.",
            f"Provenance: tier 3, digitized from the embedded TIFF by {fig}_extract.py. x calibrated on the inset's left frame (0,",
            f"  labelled) and {len(ixt)} labelled ticks, max residual {irx:.2g}; y on {len(iyt)} labelled ticks"
            + (f" and the bottom frame ({I['ybottom']})" if I["ybottom"] is not None else " (the bottom frame is not labelled)")
            + f", max residual {iry:.2g}; inset frame: x {float(ifx(G['left'])):.3g}-{float(ifx(G['right'])):.3g},"
            f" y {float(ify(G['bottom'])):.3g}-{float(ify(G['top'])):.3g}.",
            "  Markers: bounding-box centre of the grey blob (overlapping diamonds flagged). Lines: least-squares straight line",
            "  through the pixels of the dotted/dashed line (marker pixels and red pixels next to the orange line excluded);",
            "  " + "; ".join(f"{k}: y = {v[0]:.4g} x + {v[1]:.4g}, rms {v[4]:.3f}, {v[5]} px" for k, v in lines.items()) + ".",
            f"Uncertainty: about +-{2 * abs(isx):.3f} in ratio and +-{2 * abs(isy):.3f} in A (2 px).",
        ], ["series", "kind", "ratio", I["ycol"], "marker_w_px", "marker_h_px", "note"], irows, fmt="{:.4g}")
        print("inset res", irx, iry, lines)
        for r in irows:
            print("  ", r)
        out.update(inset_lines=lines, inset_rows=irows)
    overlay(a, pts, os.path.join(WORK, f"{fig}_overlay.png"))
    if mk:
        from PIL import Image
        cross_overlay(np.array(Image.open(os.path.join(WORK, f"{fig}_overlay.png"))), mk,
                      os.path.join(WORK, f"{fig}_overlay.png"), colour=(0, 255, 255))
    return out
