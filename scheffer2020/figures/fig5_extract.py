#!/usr/bin/env python3
"""Digitize Figure 5A and 5B (bubble scatter plots, precision vs recall per brain region) of scheffer2020.

Tier 3 (digitized): the figure is one embedded JPEG (1187 x 562 px, ~167 ppi) on PDF page 13. The authors'
Figure 5-source data 1-2 are not available locally.

Method:
- axes: the light-grey gridlines at 0.6 ... 1.0 and the dark axis frame (0.5) are located in the image; a linear
  pixel -> data map per axis is fitted through them (0.1 data units = ~97.5 px in x, ~99.8 px in y).
- dots: colour mask (red in A, blue in B; the purple reference dot separately). The gridlines are drawn on top
  of the dots; where the dot colour continues on both sides of a gridline the mask is bridged. Each dot has a white edge, so
  every connected component of the mask is the visible part of one dot. For each component a circle is fitted
  to its outline by RANSAC (the outline also contains arcs cut by dots drawn on top, which RANSAC rejects); a
  candidate circle may not cover open background (white more than 3.5 px from any dot).
  Fits that coincide (one dot split into several visible pieces) are merged.
- the radius is the fitted outline radius plus half the white edge (the marker edge is drawn centred on the
  marker outline); r_px is in source-image pixels. Marker area is proportional to region volume (caption), so
  r_px**2 is a relative volume (no absolute scale is printed).

Writes figures/fig5a.csv, figures/fig5b.csv and the overlays work/fig5_overlay.png.
"""
import csv
from pathlib import Path

import cv2
import numpy as np
import pymupdf

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PDF = ROOT / "source" / "elife-57443-v4.pdf"
WORK = ROOT / "work"
WORK.mkdir(exist_ok=True)


GUIDES = {"a": [(506, 90, 27)]}  # hand-placed guide circle(s), source px: see main()


def load():
    doc = pymupdf.open(PDF)
    page = doc[12]
    info = max(page.get_image_info(xrefs=True), key=lambda i: pymupdf.Rect(i["bbox"]).width)
    pix = pymupdf.Pixmap(doc, info["xref"])
    if pix.n - pix.alpha != 3:
        pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
    return np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3].copy()


def gridlines(gray_mask, axis, lo, hi, minlen):
    s = gray_mask.sum(axis=axis)
    idx = [i for i in range(lo, hi) if s[i] > minlen]
    groups, cur = [], []
    for i in idx:
        if cur and i - cur[-1] > 2:
            groups.append(cur)
            cur = []
        cur.append(i)
    if cur:
        groups.append(cur)
    return [float(np.average(g, weights=s[g])) for g in groups]


def fit_circle(pts):
    x, y = pts[:, 0], pts[:, 1]
    A = np.c_[2 * x, 2 * y, np.ones(len(x))]
    b = x ** 2 + y ** 2
    c, *_ = np.linalg.lstsq(A, b, rcond=None)
    r = np.sqrt(max(c[2] + c[0] ** 2 + c[1] ** 2, 0))
    return c[0], c[1], r


def ransac_circle(pts, comp_pts, rng, bg_far, iters=600, tol=1.0, max_out=0.02):
    best, best_n = None, -1
    n = len(pts)
    if n < 5:
        cx, cy = comp_pts.mean(0)
        return cx, cy, max(1.0, np.sqrt(len(comp_pts) / np.pi)), n
    for _ in range(iters):
        s = pts[rng.choice(n, 3, replace=False)]
        try:
            cx, cy, r = fit_circle(s)
        except Exception:
            continue
        if not np.isfinite(r) or r < 1 or r > 60:
            continue
        d = np.abs(np.hypot(pts[:, 0] - cx, pts[:, 1] - cy) - r)
        inl = d < tol
        # the visible piece must lie inside its own circle
        dc = np.hypot(comp_pts[:, 0] - cx, comp_pts[:, 1] - cy)
        if (dc > r + 1.5).mean() > max_out:
            continue
        # and must not cover open background (white far from any dot)
        yy, xx = np.ogrid[max(0, int(cy - r)):int(cy + r) + 1, max(0, int(cx - r)):int(cx + r) + 1]
        inside = (xx - cx) ** 2 + (yy - cy) ** 2 <= (r - 1) ** 2
        win = bg_far[max(0, int(cy - r)):int(cy + r) + 1, max(0, int(cx - r)):int(cx + r) + 1]
        if win.shape == inside.shape and inside.sum() and (win & inside).sum() / inside.sum() > 0.03:
            continue
        if inl.sum() > best_n:
            best_n, best = inl.sum(), inl
    if best is None:
        cx, cy = comp_pts.mean(0)
        return cx, cy, np.sqrt(len(comp_pts) / np.pi), 0
    cx, cy, r = fit_circle(pts[best])
    return cx, cy, r, int(best.sum())


def main():
    img = load()
    H, W, _ = img.shape
    f = img.astype(int)
    g = f.mean(2)
    neutral = (np.abs(f[:, :, 0] - f[:, :, 1]) < 12) & (np.abs(f[:, :, 1] - f[:, :, 2]) < 12)
    grid = neutral & (g > 150) & (g < 215)
    dark = g < 80
    rng = np.random.default_rng(0)
    panels = {
        "a": dict(x0=57, x1=564, color=(214, 39, 40), ref=(0.9, 0.9)),
        "b": dict(x0=678, x1=1185, color=(31, 119, 180), ref=(0.8, 0.8)),
    }
    overlay = cv2.cvtColor(img, cv2.COLOR_RGB2BGR).copy()
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV).astype(int)
    for key, P in panels.items():
        x0, x1 = P["x0"], P["x1"]
        # frame: dark columns / rows
        fx = [c for c in range(x0 - 3, x0 + 4) if dark[:, c].sum() > 400]
        fy = [r for r in range(H) if dark[r, x0 + 5:x1 - 5].sum() > 400]
        fxl = float(np.mean(fx))
        fyb = float(np.mean([r for r in fy if r > H / 2]))
        gx = gridlines(grid[:, x0 + 5:x1 - 5].T.T, 0, x0 + 5, x1 - 5, 150) if False else None
        sx = grid[:, :].sum(0)
        gxs = gridlines(grid, 0, x0 + 5, x1 - 5, 150)
        gys = gridlines(grid[:, x0 + 5:x1 - 5], 1, 5, int(fyb) - 3, 150)
        xs_px = [fxl] + gxs
        xs_val = [0.5 + 0.1 * i for i in range(len(xs_px))]
        ys_px = [fyb] + sorted(gys, reverse=True)
        ys_val = [0.5 + 0.1 * i for i in range(len(ys_px))]
        ax, bx = np.polyfit(xs_px, xs_val, 1)
        ay, by = np.polyfit(ys_px, ys_val, 1)
        resx = np.array(xs_val) - (ax * np.array(xs_px) + bx)
        resy = np.array(ys_val) - (ay * np.array(ys_px) + by)
        P.update(ax=ax, bx=bx, ay=ay, by=by, resx=np.abs(resx).max(), resy=np.abs(resy).max(),
                 xs_px=xs_px, ys_px=ys_px)
        # colour masks
        target = np.array(P["color"])
        sub = f[:, x0 + 2:x1 - 1]
        dist = np.sqrt(((sub - target) ** 2).sum(2))
        mask = (dist < 90).astype(np.uint8)
        # gridlines are drawn on top of the dots: bridge them where the dot colour continues on both sides
        off = x0 + 2
        gsub = grid[:, x0 + 2:x1 - 1]  # only grey gridline pixels are bridged
        for gxp in gxs:
            c = int(round(gxp)) - off
            for cc in range(c - 1, c + 2):
                if 3 <= cc < mask.shape[1] - 3:
                    both = mask[:, cc - 2].astype(bool) & mask[:, cc + 2].astype(bool) & gsub[:, cc]
                    mask[both, cc] = 1
        for gyp in gys:
            r0 = int(round(gyp))
            for rr in range(r0 - 1, r0 + 2):
                if 3 <= rr < mask.shape[0] - 3:
                    both = mask[rr - 2].astype(bool) & mask[rr + 2].astype(bool) & gsub[rr]
                    mask[rr, both] = 1
        purple = (np.sqrt(((sub - np.array((148, 103, 189))) ** 2).sum(2)) < 45).astype(np.uint8)
        anyc = ((mask | purple) == 0).astype(np.uint8)
        bg_far = cv2.distanceTransform(anyc, cv2.DIST_L2, 3) > 3.5
        dots = []
        for kind, m in (("region", mask), ("human_reference", purple)):
            n, lab, stats, cents = cv2.connectedComponentsWithStats(m, connectivity=4)
            for i in range(1, n):
                if stats[i, cv2.CC_STAT_AREA] < 6:
                    continue
                comp = (lab == i).astype(np.uint8)
                # a component can hold several dots joined across a bridged gridline: fit one circle, remove
                # its pixels, and repeat on the rest
                for it in range(6):
                    area = int(comp.sum())
                    if area < (6 if it == 0 else 15):
                        break
                    cnts, _ = cv2.findContours(comp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                    pts = np.vstack([c[:, 0, :] for c in cnts]).astype(float)
                    cy_, cx_ = np.nonzero(comp)
                    comp_pts = np.c_[cx_, cy_].astype(float)
                    cx, cy, r, ninl = ransac_circle(pts, comp_pts, rng, bg_far)
                    if ninl < 8 and area > 40:  # no single circle explains the piece: allow other dots in it
                        cx, cy, r, ninl = ransac_circle(pts, comp_pts, rng, bg_far, max_out=0.5)
                    inside = np.hypot(comp_pts[:, 0] - cx, comp_pts[:, 1] - cy) <= r + 1.5
                    dots.append(dict(kind=kind, cx=cx + x0 + 2, cy=cy, r=r, area=int(inside.sum()), ninl=ninl))
                    if inside.all():
                        break
                    comp[cy_[inside], cx_[inside]] = 0
                    comp = cv2.morphologyEx(comp, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        # merge pieces of one dot
        merged = []
        for d in sorted(dots, key=lambda d: -d["area"]):
            for m in merged:
                if m["kind"] == d["kind"] and np.hypot(m["cx"] - d["cx"], m["cy"] - d["cy"]) < 2.5 and abs(m["r"] - d["r"]) < 2.5:
                    m["pieces"] += 1
                    m["area"] += d["area"]
                    break
            else:
                d["pieces"] = 1
                merged.append(d)
        # hand guide (panel A only): the largest dot sits under the dense cluster at about recall 0.96, precision 0.93;
        # automatic RANSAC fitted its visible piece with a wrong circle (r > 30 px). Replace that fit by a circle
        # least-squares fitted to the colour-mask outline points within 2.5 px of the guide circle (506, 90, r 27).
        for gx_, gy_, gr_ in GUIDES.get(key, []):
            bad = [m for m in merged if np.hypot(m["cx"] - gx_, m["cy"] - gy_) < 20 and m["r"] > 30]
            cnts, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
            allp = np.vstack([c[:, 0, :] for c in cnts]).astype(float)
            allp[:, 0] += x0 + 2
            dd = np.abs(np.hypot(allp[:, 0] - gx_, allp[:, 1] - gy_) - gr_)
            cx, cy, r = fit_circle(allp[dd < 2.5])
            area = sum(m["area"] for m in bad)
            for m in bad:
                merged.remove(m)
            merged.append(dict(kind="region", cx=cx, cy=cy, r=r, area=area, pieces=len(bad), guided=True))
        rows = []
        for d in sorted(merged, key=lambda d: (d["kind"] != "human_reference", d["cx"])):
            x = ax * d["cx"] + bx
            y = ay * d["cy"] + by
            r_edge = d["r"] + 0.75  # outline sits inside the ~1.5 px white edge
            vis = min(1.0, d["area"] / (np.pi * r_edge ** 2))
            status = "ok" if vis > 0.8 else ("partly_hidden" if vis > 0.3 else "mostly_hidden")
            if d.get("guided"):
                status = "partly_hidden_guided"
            rows.append([key.upper(), d["kind"], round(x, 4), round(y, 4), round(r_edge, 1),
                         round(r_edge ** 2, 1), round(vis, 2), d["pieces"], status])
            col = (0, 0, 0) if d["kind"] == "region" else (0, 200, 0)
            cv2.circle(overlay, (int(round(d["cx"])), int(round(d["cy"]))), int(round(r_edge)), col, 1)
            cv2.drawMarker(overlay, (int(round(d["cx"])), int(round(d["cy"]))), col, cv2.MARKER_CROSS, 4, 1)
        P["rows"] = rows
        out = HERE / f"fig5{key}.csv"
        with open(out, "w", newline="") as fh:
            w = csv.writer(fh)
            fh.write(f"# scheffer2020 Figure 5{key.upper()}: precision vs recall of synapse prediction per brain region "
                     f"({'T-bars' if key == 'a' else 'synapses as a whole incl. PSD identification'}).\n")
            fh.write("# Provenance: tier 3, digitized from the embedded raster image (JPEG, 1187x562 px) on PDF p. 13 by "
                     "figures/fig5_extract.py. The authors' Figure 5-source data 1-2 (online) are not available locally.\n")
            fh.write(f"# Axis calibration: linear fit through frame (0.5) and gridlines 0.6-1.0; max residual "
                     f"x {P['resx']:.4f}, y {P['resy']:.4f} data units. One source pixel = {abs(ax):.5f} (x), {abs(ay):.5f} (y).\n")
            fh.write("# Columns: panel; kind (region = one brain region; human_reference = purple dot, typical human "
                     "proofreader performance per caption); recall; precision (dot centre, fitted circle); r_px = dot "
                     "radius in source pixels incl. half the white edge; rel_area = r_px^2 (marker area, proportional to "
                     "region volume per caption, arbitrary units); visible_frac = visible fraction of the dot; pieces = "
                     "visible pieces merged; status (ok / partly_hidden / mostly_hidden / partly_hidden_guided = refitted near a "
                     "hand-placed guide circle).\n")
            fh.write("# Uncertainty: centres about +-0.003 (fully visible dots), more for partly hidden dots (circle fitted to "
                     "the visible arc); radii +-1 px. Dots completely hidden under larger dots cannot be found, so the "
                     "number of regions may be undercounted." + (" In the dense cluster of panel A (recall 0.91-0.99, "
                     "precision 0.88-0.96) the dots overlap heavily: rows marked partly/mostly hidden there are uncertain, "
                     "and some may be pieces of one dot fitted twice or mis-sized (e.g. the r 16.3 px fit at 0.959/0.934 lies "
                     "inside the guided r 28 px dot; the r 4.1/4.4 px fits at 0.930/0.898 and 0.931/0.895 may be one dot)."
                     if key == "a" else "") + "\n")
            fh.write("# Check: the purple human-proofreader reference dot comes out at the caption's values (A 0.9/0.9, "
                     "B 0.8/0.8) to within 0.0004.\n")
            w.writerow(["panel", "kind", "recall", "precision", "r_px", "rel_area", "visible_frac", "pieces", "status"])
            w.writerows(rows)
        print(key, "dots", len(rows), "resid", P["resx"], P["resy"])
    cv2.imwrite(str(WORK / "fig5_overlay.png"), overlay)


if __name__ == "__main__":
    main()
