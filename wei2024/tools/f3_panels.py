"""Shared panel runner for wei2024 Figs. 12 and 15 (fork F3): calibration, marker matching, CSV, review sheet."""
import csv

import numpy as np

import f3_markers as fm

XV = [0, 5, 10, 15, 20, 25, 30]
SIZES = {"open square": (7, 7), "filled circle": (7, 7), "open up-triangle": (7, 8),
         "open down-triangle": (7, 8), "open diamond": (8, 8)}
LEGEND_LOG = []


def flag_for(score):
    if score >= 0.6:
        return ""
    if score >= 0.45:
        return "partly covered (marker overlaps a line or another marker)"
    return "hidden (marker not visible; position where the series' ink best matches the marker at that column)"


def run_panel(a, fig, key, cfg, series, yvals, ylabel, yunit, title, src):
    """src: text naming the source image and the extract script."""
    L, R, T, B = cfg["frame"]
    fx, fy, inv_x, caltxt, sx, sy = fm.calib(a, cfg["frame"], cfg.get("xvals", XV), yvals)
    box = (L[1] + 2, T[1] + 2, R[0] - 1, B[0] - 1)
    grid = np.asarray(cfg.get("grid", np.arange(1, 31)), float)
    xcols = inv_x(grid)
    step = grid[1] - grid[0]
    gtxt = f"{len(grid)} marker columns (markers stand at sliding distance {grid[0]:g}, {grid[1]:g}, ... {grid[-1]:g} A, every {step:g} A;"
    rows, pts = [], []
    for name, colour, shape in series:
        full = fm.COLOURS[colour](a.astype(int))
        lb = fm.find_legend_box(full, cfg["legend"])
        _, lcen, ltl = fm.legend_template(full, lb)
        w, h = cfg.get("sizes", {}).get(shape, SIZES[shape])
        T_, cen = fm.synth_template(shape, w, h)
        # check the template centre on the legend marker: its dashed line passes through the data point
        lx, ly = ltl[0] + lcen[0], ltl[1] + lcen[1]
        lbm = np.zeros_like(full)
        lbm[lb[1]:lb[3], lb[0]:lb[2]] = full[lb[1]:lb[3], lb[0]:lb[2]]
        chk = fm.match_grid(lbm, T_, cen, [lx], (lb[1], lb[3]), tol=3, close=cfg.get("close", 3))[0]
        LEGEND_LOG.append(f"Fig. {fig}{key} {name} ({shape}, {colour}): legend line centre row {ly:.1f}, "
                          f"template-match centre row {chk[2]:.1f} (diff {chk[2] - ly:+.1f} px), score {chk[3]:.2f}")
        # black: the whole legend box (its labels are black text) and the title; other colours: the title and
        # only their own legend line (data markers may sit next to the legend's black labels)
        if colour == "black" or cfg.get("legend_blank_all"):
            blank = list(cfg["blank"])
        else:
            lgx0, lgy0, lgx1, lgy1 = cfg["legend"]
            blank = list(cfg["blank"][1:]) + [(lgx0, lb[1], lgx1, lb[3])]
        if colour == "black":  # inward tick marks along the left and bottom frame lines are black too
            blank += [(box[0], box[1], box[0] + 11, box[3]), (box[0], box[3] - 11, box[2], box[3])]
        # coloured series: the mask reaches into the frame lines (markers at the edge are drawn over the frame)
        mbox = box if colour == "black" else (L[0], T[0], R[1] + 1, B[1] + 1)
        m = fm.series_mask(a, colour, mbox, blank)
        others = None
        rows_rng = (box[1], box[3])
        if cfg.get("others"):
            # other series' ink, and for coloured series also the black frame line and ticks (a marker on the
            # bottom frame line is half covered by it), count half
            obox = (L[0], T[0], R[1] + 1, B[1] + 1)
            others = np.zeros_like(m)
            for _, oc, _ in series:
                if oc != colour:
                    others |= fm.series_mask(a, oc, obox if oc == "black" else box, cfg["blank"])
            if colour != "black":
                rows_rng = (T[0], B[1] + 1)
        res = fm.match_grid(m, T_, cen, xcols, rows_rng, tol=3, close=cfg.get("close", 3), ring=shape in cfg.get("ring", ()), others=others)
        for xe, xc, yc, score, res_flag in res:
            n_int = float(np.round(fx(xe) / step) * step)
            ov = cfg.get("override", {}).get((name, n_int))
            if ov == "nan":
                rows.append([name, float(fx(xe)), float("nan"), round(score, 3), "not drawn: marker and its line segments are absent at this sliding distance (x given = expected marker column)"])
                continue
            flag = flag_for(score)
            if "other-series" in res_flag:
                flag = (flag + "; " if flag else "") + res_flag[res_flag.index("other-series"):]
            if ov == "covered":
                flag = "partly covered (checked by eye: marker visible, partly under another series' marker)"
            if xc == xc:
                pts.append((xc, yc, colour, f"{fig}{key} {name} x={fx(xc):.1f} s={score:.2f}", score))
            rows.append([name, float(fx(xc)), float(fy(yc)), round(score, 3), flag])
    header = [
        f"wei2024 Fig. {fig}{key}: {title}. {ylabel} vs sliding distance.",
        "Columns: series (legend name), x = sliding distance (A), y = " + f"{ylabel} ({yunit})" +
        ", match = template-match score of the marker (1 = the filled marker template is fully covered by series ink), flag.",
        "Provenance: tier 3 (digitized) from " + src + ":",
        "colour mask per series, legend/title boxes blanked, " + ("3x3 closing, " if cfg.get("close", 3) else "") + "holes filled, template match with a filled synthetic marker",
        "of the legend's shape (~7 px; triangles centred on their centroid), best match within +-3 px of each of the " + gtxt + (" ink of the other series (and the black frame line) counts half and may close an outline (markers partly under another marker or on the frame);" if cfg.get("others") else "") + (" for the filled circles, where two candidates fill the template, the one with less ink in a 2-px ring around it (a compact marker, not two dashed-line arms meeting);" if cfg.get("ring") else ""),
        "x is the measured marker centre, within +-0.18 A (3 px) of the grid by construction). Values are marker centres.",
        "Calibration (inward major ticks, linear): " + caltxt,
        f"Uncertainty: about +-1 px = +-{sx:.2g} A in x and +-{sy:.2g} {yunit} in y (marker centre on a JPEG);",
        "flag: empty = clean match (score >= 0.6, little other-series ink under the template); 'partly covered' (0.45-0.6) = marker",
        "overlaps a line or another marker, centre still on the marker (checked by eye); 'hidden' (< 0.45) = marker not visible, y is",
        "where the series' own ink best fits the marker template (uncertainty up to +-4 px); 'other-series ink covers N%' = the marker",
        "sits under/over another series' marker or line, centre less certain (about +-2 px); 'not drawn' = no marker at that column.",
    ]
    return header, rows, pts


def sheet(a, pts, out, thr=0.6, half=22, z=5):
    """Tile zoomed crops (with a cyan cross) of every point whose match score < thr, for review."""
    from PIL import Image, ImageDraw
    weak = [p for p in pts if p[4] < thr]
    if not weak:
        return
    n = len(weak)
    cols = 8
    tw = 2 * half * z
    img = Image.new("RGB", (cols * tw, ((n + cols - 1) // cols) * (tw + 14)), "white")
    dr = ImageDraw.Draw(img)
    for i, (x, y, c, lab, sc) in enumerate(weak):
        xi, yi = int(round(x)), int(round(y))
        crop = a[max(0, yi - half):yi + half, max(0, xi - half):xi + half].copy()
        cy, cx = yi - max(0, yi - half), xi - max(0, xi - half)
        crop[cy, max(0, cx - 3):cx + 4] = (0, 200, 255)
        crop[max(0, cy - 3):cy + 4, cx] = (0, 200, 255)
        t = Image.fromarray(crop).resize((crop.shape[1] * z, crop.shape[0] * z), Image.NEAREST)
        X, Y = (i % cols) * tw, (i // cols) * (tw + 14)
        img.paste(t, (X, Y + 14))
        dr.text((X + 2, Y), lab, fill="black")
    img.save(out)


def write(path, header, rows):
    with open(path, "w", newline="") as f:
        for h in header:
            f.write("# " + h + "\n")
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["series", "x_A", "y", "match", "flag"])
        for r in rows:
            w.writerow([r[0], f"{r[1]:.3f}", "" if r[2] != r[2] else f"{r[2]:.4g}", r[3], r[4]])


