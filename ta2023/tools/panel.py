"""Driver for digitizing one line+marker panel of Ta, Tran & Righi 2023 (used by figures/*_extract.py).

The data of every plot in this paper are the DFT points, drawn as filled markers at displacement steps;
the smooth curves through them are the plotting program's interpolation and carry no extra data. So a
panel is digitized marker by marker:

1. axis calibration on the detached axis lines and their outward major ticks (figtools.calib_axes);
2. per series, a colour mask; an elliptic opening of size k removes the thin curves, insets' box frames
   and arrows' shafts, leaving the filled markers as blobs; coloured atoms inside the structure insets,
   the legend and the numbered call-outs are blanked with exclusion rectangles first;
3. every remaining blob of at least amin px is a marker; its bbox centre (plus the legend-calibrated row
   offset, where the panel has a legend) is the data point, in both x and y (the displacements are measured,
   not assumed to lie on the 0.25 A step grid); blobs smaller than the series' median marker are flagged
   'partly hidden' (another marker, an inset or a label lies on top);
4. manual entries (explained in the CSV header) replace a blob or add a marker that is hidden or that the
   opening cannot separate; a hidden marker whose position cannot be read gets an empty value.
"""
import csv
from pathlib import Path

import numpy as np

from figtools import blobs, calib_axes, curve_at, dark_mask, hue_mask, load, save_overlay, square_edges

OVL = {"green": (0, 140, 0), "red": (200, 0, 0), "blue": (0, 0, 200), "black": (255, 0, 255),
       "grey": (255, 0, 255), "pink": (255, 128, 0)}


def run(cfg):
    a = load(cfg["page"], cfg["xref"])
    if "crop" in cfg:                     # sub-image (several panels in one embedded image)
        x0, y0, x1, y1 = cfg["crop"]
    else:
        x0, y0, x1, y1 = 0, 0, a.shape[1], a.shape[0]
    dark = dark_mask(a, cfg.get("dark_thr", 215), cfg.get("dark_sat", 40))
    for r in cfg.get("axis_blank", []):          # blank things lying on the axis windows (insets)
        dark[r[1]:r[3], r[0]:r[2]] = False
    dark_v = cfg["vmask"](a) if "vmask" in cfg else dark      # coloured axis lines (Figure 3, TOC graphic)
    cal = calib_axes(dark_v, cfg["vwin"], cfg["hwin"], cfg["ylow"], cfg["ystep"], cfg["xlow"], cfg["xstep"],
                     dark_h=dark, vrows=cfg.get("vrows"), hline=cfg.get("hline"), ytop=cfg.get("ytop"))
    cal2 = None
    if "vwin2" in cfg:                            # right axis (e.g. force), ticks pointing right
        from figtools import fit, ticks_v, vaxis
        d2 = cfg["vmask2"](a) if "vmask2" in cfg else dark
        cols, rows = vaxis(d2, *cfg["vwin2"])
        tv = ticks_v(d2, cols, +1, rows[0] - 3, rows[1] + 4)
        Lv = max(L for _, L in tv)
        maj = sorted([r for r, L in tv if L >= 0.75 * Lv], reverse=True)
        vals = [cfg["ylow2"] + i * cfg["ystep2"] for i in range(len(maj))]
        fy2, r2, m2, iy2 = fit(maj, vals)
        cal2 = dict(fy=fy2, res=r2, my=m2, maj=maj, vals=vals, cols=cols)
    rows_out, ovl = [], []
    for s in cfg["series"]:
        mask = s["mask"](a) if callable(s.get("mask")) else hue_mask(a, s.get("mask", s["colour"]))
        for r in cfg.get("exclude", []) + s.get("exclude", []):
            mask[r[1]:r[3], r[0]:r[2]] = False
        mask_raw = mask.copy()
        bl = [b for b in blobs(mask, s["k"], roi=cfg["plot"], close=s.get("close", 0)) if b["area"] >= s.get("amin", 60)]
        bl = [b for b in bl if not any(abs(b["bx"] - x) < 4 and abs(b["by"] - y) < 4 for x, y in s.get("drop", []))]
        fyy, my = (cal2["fy"], cal2["my"]) if s.get("axis") == 2 else (cal["fy"], cal["my"])
        if "size" in s:                      # typical (unoccluded) marker blob size, set by hand
            mw, mh = s["size"]
        elif bl:
            mw, mh = np.median([b["w"] for b in bl]), np.median([b["h"] for b in bl])
        else:
            mw = mh = 0
        found = []
        for b in bl:
            xpx, ypx = b["bx"], b["by"] + s.get("dy", 0.0)
            if b["w"] < 0.85 * mw or b["h"] < 0.85 * mh:
                st, note, unc = "partly hidden", f"visible blob {b['w']}x{b['h']} px, typical {mw:.0f}x{mh:.0f}", s.get("unc_partial", 5.0)
            else:
                st, note, unc = "ok", "", s.get("unc_ok", 2.0)
            found.append([xpx, ypx, st, note, unc])
        for m in s.get("manual", []):       # (x_px, y_px or nan, status, note, unc_px): replaces a blob within 6 px
            m = list(m)
            if isinstance(m[1], str) and m[1] == "curve":   # y from the curve on both sides of the occluder
                cm = mask_raw if s.get("curve_raw", True) else mask
                yc, n = curve_at(cm, m[0], m[5], m[6], win=m[7] if len(m) > 7 else 12)
                m = [m[0], yc, m[2], m[3] + f" (curve interpolated over {2 * m[6]} px from {n} columns)", m[4]]
            elif isinstance(m[1], str) and m[1] == "square":   # square marker from its visible edges
                cxs, cys, ws, hs = square_edges(mask_raw, m[0], m[5], m[6] if len(m) > 6 else 12)
                m = [cxs, cys + s.get("dy", 0.0), m[2], m[3] + f" (centre from the visible square edges, {ws}x{hs} px)", m[4]]
            elif isinstance(m[1], str) and m[1] in ("bottom", "top"):   # marker clipped by an inset: one edge
                b = min(bl, key=lambda d: abs(d["bx"] - m[0]))           # visible, the other from the median size
                if m[1] == "bottom":
                    yc = b["y0"] + b["h"] - 1 - (mh - 1) / 2 + s.get("dy", 0.0)
                else:
                    yc = b["y0"] + (mh - 1) / 2 + s.get("dy", 0.0)
                m = [b["bx"], yc, m[2], m[3] + f" (centre from its {m[1]} edge and the typical marker height {mh:.0f} px)", m[4]]
            found = [f for f in found if abs(f[0] - m[0]) > 6]
            found.append(m)
        found.sort(key=lambda f: f[0])
        pts = []
        for xpx, ypx, st, note, unc in found:
            yv = float(fyy(ypx)) if ypx == ypx else float("nan")
            rows_out.append([s["name"], float(cal["fx"](xpx)), yv, abs(unc * my), round(float(xpx), 1),
                             round(float(ypx), 1) if ypx == ypx else "", st, note])
            pts.append((xpx, ypx))
        ovl.append((pts, OVL.get(s["colour"], (255, 0, 255))))
    tick_pts = [(cal["vcols"][0] - 2, r) for r in cal["majv"]] + [(c, cal["hrows"][1] + 2) for c in cal["majh"]]
    if cal2:
        tick_pts += [(cal2["cols"][1] + 2, r) for r in cal2["maj"]]
    ovl.append((tick_pts, (255, 128, 0)))
    save_overlay(a, ovl, cfg["overlay"], r=cfg.get("ring", 4))
    return dict(rows=rows_out, cal=cal, cal2=cal2, image=a)


def write(path, header, rows, ycol="energy_eV"):
    """CSV: series, displacement measured from the marker, value, its uncertainty, source-image pixel
    position of the marker centre, status, note."""
    with open(path, "w", newline="") as f:
        for h in header:
            f.write("# " + h + "\n")
        w = csv.writer(f)
        w.writerow(["series", "displacement_A", ycol, ycol + "_unc", "x_px", "y_px", "status", "note"])
        for r in rows:
            name, xm, yv, yu, xpx, ypx, st, note = r
            w.writerow([name, f"{xm:.3f}", "" if yv != yv else f"{yv:.3f}", f"{yu:.2f}", xpx, ypx, st, note])


def read(path):
    with open(path) as f:
        return list(csv.DictReader(l for l in f if not l.startswith("#")))
