"""Digitize Figure 6 of Gabričević, Lente & Fábián 2020 (poc.4045.pdf p. 5): k_obs of the slow process vs substrate
concentration. One embedded raster image (1003 x 1413 px) holds both panels (no panel letters):
top = trans-DCE and cis-DCE vs [Substrate]; bottom = TCE vs [TCE]. Each has straight fit lines in the series colour.
    python3 -I fig6_extract.py   -> fig6top.csv, fig6bottom.csv (+ ../work/fig6_overlay.png)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np  # noqa: E402
from gab_common import (load, gray, tick_positions, tick_positions_v, fit_axis, scatter, colour_mask, track,  # noqa: E402
                        write_csv, cross_overlay, overlay, WORK)

a = load("fig6")
dark = gray(a) < 120
LEFT = (201, 203)
panels = {
    # name: bottom frame rows, top frame row, x tick labels (after the left frame = 0), y tick labels (top to bottom)
    "top": dict(bot=(566, 566), top=5, xl=[0.005, 0.010, 0.015, 0.020], yl=[0.009, 0.006, 0.003], y0=0.0,
                series=[("trans-DCE", (255, 0, 0)), ("cis-DCE", (0, 0, 255))], legend=(260, 40, 500, 190),
                xname="substrate_mol_dm3", xdesc="[Substrate] (mol/dm3)"),
    "bottom": dict(bot=(1301, 1301), top=740, xl=[0.001, 0.002, 0.003, 0.004], yl=[1.0e-4, 5.0e-5], y0=0.0,
                   series=[("TCE", (0, 128, 0))], legend=None, xname="TCE_mol_dm3", xdesc="[TCE] (mol/dm3)"),
}
paper_k2 = {"trans-DCE": 0.53, "cis-DCE": 0.111, "TCE": 0.036}   # k2nd from the text, p. 5 (dm3 mol-1 s-1)
all_pts, all_line = [], []
for pname, P in panels.items():
    xt = tick_positions(dark, P["bot"], 1, 10, 204, 995)
    yt = tick_positions_v(dark, LEFT, -1, 10, P["top"] + 2, P["bot"][0] - 2)
    assert len(xt) == len(P["xl"]) and len(yt) == len(P["yl"]), (pname, xt, yt)
    fx, rx, sx = fit_axis([202.0] + xt, [0.0] + P["xl"])
    fy, ry, sy = fit_axis(yt + [P["bot"][0] + 0.0], P["yl"] + [P["y0"]])
    box = (205, P["top"] + 2, 995, P["bot"][0] - 1)
    ex = [P["legend"]] if P["legend"] else []
    found = scatter(a, P["series"], box, exclude=ex, open_=9)
    rows = [(n, "marker", float(fx(x)), float(fy(y)), w, h, f) for n, x, y, w, h, f in found]
    all_pts += [(x, y) for n, x, y, w, h, f in found]
    checks = []
    for name, ref in P["series"]:
        m = colour_mask(a, ref, alpha_min=0.45, alpha_max=1.3, tol=50)
        keep = np.zeros_like(m)
        keep[box[1]:box[3], box[0]:box[2]] = True
        for e in ex:
            keep[e[1]:e[3], e[0]:e[2]] = False
        m &= keep
        # seed: the line pixel nearest the fitted origin side, 40 px right of the left frame
        c0 = 245
        runs = np.where(m[:, c0])[0]
        seed = int(runs.max())
        tr = track(m, c0, seed, 205, 995, box[1], box[3], max_jump=3, max_gap=30, max_run=7)
        xs = np.array(sorted(tr))
        ys = np.array([(tr[c][0] + tr[c][1]) / 2 for c in xs])
        for c, y in zip(xs, ys):
            rows.append((name, "line", float(fx(c)), float(fy(y)), "", "", ""))
        all_line += list(zip(xs, ys))
        X, Y = fx(xs), fy(ys)
        slope, icpt = np.polyfit(X, Y, 1)
        checks.append(f"{name}: line slope {slope:.4g} dm3 mol-1 s-1 (paper k2nd {paper_k2[name]}), intercept {icpt:.2g} s-1,"
                      f" x {X.min():.4g}-{X.max():.4g}")
    rows.sort(key=lambda r: (r[1] != "marker", r[0], r[2]))
    write_csv(os.path.join(HERE, f"fig6{pname}.csv"), [
        f"Gabričević, Lente & Fábián 2020, J Phys Org Chem 33:e4045, Figure 6 ({pname} panel; the figure has no panel letters):",
        "  pseudo-first order rate constant of the slow process vs substrate concentration, markers + straight fit lines.",
        f"Columns: series (legend names; the {pname} panel{' has no legend, series named from its x-axis title' if pname == 'bottom' else ''});",
        f"  kind = marker or line (one row per pixel column of the fit line); {P['xname']} = {P['xdesc']}; kobs_s-1 = k_obs (s-1);",
        "  marker_w_px/marker_h_px = marker blob size in the source image; note.",
        "Provenance: tier 3, digitized from the embedded raster image (1003 x 1413 px, both panels) by fig6_extract.py.",
        f"  x calibrated on the left frame (0.000, labelled) and {len(xt)} labelled ticks, max residual {rx:.2g}; y on the bottom frame",
        f"  (0, labelled) and {len(yt)} labelled ticks, max residual {ry:.2g}. Markers: centre of the bounding box of the colour blob",
        "  after removing the thin same-coloured fit line (morphological opening). Line: centre of the line in each column,",
        "  columns hidden by markers skipped.",
        f"Uncertainty: about +-{2 * abs(sx):.2g} mol/dm3 in x and +-{2 * abs(sy):.2g} s-1 in y (2 px).",
        "Check (straight-line fit to the traced line pixels): " + "; ".join(checks),
    ], ["series", "kind", P["xname"], "kobs_s-1", "marker_w_px", "marker_h_px", "note"], rows, fmt="{:.6g}")
    print(pname, len(found), "markers;", "; ".join(checks), "residuals", rx, ry)
    for r in rows:
        if r[1] == "marker":
            print("  ", r)
cross_overlay(a, all_pts, os.path.join(WORK, "fig6_overlay.png"))
from PIL import Image  # noqa: E402
overlay(np.array(Image.open(os.path.join(WORK, "fig6_overlay.png"))), all_line[::3], os.path.join(WORK, "fig6_overlay.png"),
        colour=(0, 255, 255))
