"""Digitize Figure 16 (a-f) of Wei et al. 2025 (PDF p. 13): forces Fx, Fy, Fz vs indentation depth hc.

Source: the embedded 300 ppi raster image of Figure 16 (2100 x 1184 px, lossless). No vector data in the PDF.
    python3 -I -B figures/fig16_extract.py  -> figures/fig16a.csv ... fig16f.csv (+ work/fig16_overlay.png)

Per panel: the axis frame and the tick marks are found in the image; x is calibrated on the 5 long ticks
(hc = 5..25 Å) plus the left frame (0), y on the long ticks of the left axis. Markers are found by colour:
Fz blue filled circles, Fy red open triangles, Fx black open squares (
template matching against the legend symbols of panel (a) on each colour mask). Marker centre = centre of the
template's ink (for the open triangle this is its centroid, about 2 px below its bounding-box centre).
"""
import sys
from pathlib import Path

import cv2
import numpy as np
from scipy import ndimage as ndi

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
from digitize_common import (embedded_image, gray, frame_lines, tick_positions, tick_positions_v,  # noqa: E402
                             fit_axis, write_csv, overlay)

PDF = ROOT / "source" / "wei2025.pdf"
(ROOT / "work").mkdir(exist_ok=True)
a = embedded_image(str(PDF), 13, bbox_near=(45.5, 32.2, 549.5, 316.3))
g = gray(a)
r, gg, b = (a[..., i].astype(int) for i in range(3))
sat = a.max(2).astype(int) - a.min(2).astype(int)
dark = (g < 110) & (sat < 60)

HC = [4, 7, 10, 16, 22, 25]           # target indentation depths of the runs (text, Section 2.3)
# printed panel title, y tick values of the long ticks (top to bottom) are assigned below
PANELS = {
    "a": ("Pyramid-0°", (0, 600, 0, 700), "y = 0.269x - 0.536, R2 = 0.969", "y = -0.422x + 0.61, R2 = 0.995"),
    "b": ("Pyramid-45°", (0, 600, 700, 1400), "y = 0.29x - 0.749, R2 = 0.948", "y = -0.422x + 0.712, R2 = 0.99"),
    "c": ("Sphere (R = 14.5 Å)", (0, 600, 1400, 2100), "y = 0.146x + 2.476, R2 = 0.921", "y = -0.371x - 0.785, R2 = 0.997"),
    "d": ("Sphere (R = 10 Å)", (600, 1184, 0, 700), None, "y = -0.243x - 1.408, R2 = 0.978"),
    "e": ("Sphere (R = 20 Å)", (600, 1184, 700, 1400), "y = 0.339x + 3.758, R2 = 0.968", "y = -0.641x - 0.171, R2 = 0.995"),
    "f": ("Sphere (R = 25 Å)", (600, 1184, 1400, 2100), "y = 0.653x + 3.821, R2 = 0.992", "y = -0.676x - 1.148, R2 = 0.965"),
}
# y-axis long-tick labels, top to bottom (read from the figure): a-d 6..-10 step 2 (the 8 label sits on the
# top frame, which is not used); e, f 20..-20 step 5
YLAB = {k: list(range(6, -11, -2)) for k in "abcd"}
YLAB.update({k: list(range(20, -21, -5)) for k in "ef"})

masks = {
    "Fz": (b > r + 60) & (b > gg + 30),
    "Fy": (r > 150) & (r > gg + 70) & (r > b + 50),
    "Fx": dark,
}


def frame(key):
    r0, r1, c0, c1 = PANELS[key][1]
    sub = dark[r0:r1, c0:c1]
    T, B = [(x + r0, y + r0) for x, y in frame_lines(sub, 1, 0.6)][:2]
    L, R = [(x + c0, y + c0) for x, y in frame_lines(sub, 0, 0.6)][:2]
    return T, B, L, R


# marker templates: the legend symbols of panel (a) (lower left of the plot, left of hc = 3.2 Å)
T, B, L, R = frame("a")
TEMPL = {}
for series, m in masks.items():
    reg = m[(T[1] + B[0]) // 2:B[0] - 10, L[1] + 12:L[1] + 70]
    lab, n = ndi.label(reg)
    objs = [sl for sl in ndi.find_objects(lab) if 8 <= sl[0].stop - sl[0].start <= 24 and 8 <= sl[1].stop - sl[1].start <= 24]
    assert len(objs) == 1, (series, n, objs)
    sl = objs[0]
    t = (lab[sl] > 0).astype(np.float32)
    TEMPL[series] = np.pad(t, 3)


def find_markers(m, tmpl, box, thr):
    y0, y1, x0, x1 = box
    img = m[y0:y1, x0:x1].astype(np.float32)
    res = cv2.matchTemplate(img, tmpl, cv2.TM_CCOEFF_NORMED)
    mx = ndi.maximum_filter(res, size=13)
    peaks = np.argwhere((res == mx) & (res >= thr))
    cy_t, cx_t = ndi.center_of_mass(tmpl)        # centre of the template's ink (for the triangle: its centroid)
    out = []
    for py, px in peaks:
        out.append((x0 + px + cx_t, y0 + py + cy_t, float(res[py, px])))
    return out


pts_all = []
for key, (title, _, eq_z, eq_y) in PANELS.items():
    T, B, L, R = frame(key)
    xt = tick_positions(dark, B, -1, 8, L[1] + 2, R[0] - 1)
    assert len(xt) == 5, (key, xt)
    xpix = [(L[0] + L[1]) / 2] + xt
    fx, resx, sx = fit_axis(xpix, [0, 5, 10, 15, 20, 25])
    yt = tick_positions_v(dark, L, 1, 8, T[1] + 2, B[0] - 1)
    assert len(yt) == len(YLAB[key]), (key, yt)
    fy, resy, sy = fit_axis(yt, YLAB[key])
    rows = []
    for series, m in masks.items():
        box = (T[1] + 2, B[0] - 1, L[1] + 2, R[0] - 1)
        for cx, cy, score in find_markers(m, TEMPL[series], box, 0.55):
            xv, yv = float(fx(cx)), float(fy(cy))
            if xv < 3.2:                  # legend symbols sit left of hc = 4 Å
                continue
            near = min(HC, key=lambda v: abs(v - xv))
            if abs(near - xv) > 1.0:
                continue
            rows.append((series, near, xv, yv, cx, cy, score))
    rows.sort(key=lambda t: (t[0], t[1]))
    seen = {}
    for t in rows:
        seen.setdefault((t[0], t[1]), []).append(t)
    # several candidates for one series and hc: neighbouring pixels of a flat correlation peak, or a glyph of the
    # printed fit equation; keep the best match and list the rejected ones far from it
    rejected = []
    for k, v in seen.items():
        v.sort(key=lambda t: -t[6])
        rejected += [t for t in v[1:] if abs(t[5] - v[0][5]) > 4 or abs(t[4] - v[0][4]) > 4]
        seen[k] = [v[0]]
    rows = sorted((v[0] for v in seen.values()), key=lambda t: (t[0], t[1]))
    if rejected:
        print("rejected", key, [(t[0], t[1], round(t[3], 2), round(t[6], 2)) for t in rejected])
    missing = [(s, h) for s in masks for h in HC if (s, h) not in seen]
    pts_all += [(t[4], t[5]) for t in rows]
    out = [(t[0], t[1], t[2], t[3], round(t[6], 2)) for t in rows]
    notes = []
    for s, eq in (("Fz", eq_z), ("Fy", eq_y)):
        xs = np.array([t[1] for t in rows if t[0] == s], float)
        ys = np.array([t[3] for t in rows if t[0] == s], float)
        if len(xs) > 2:
            m_, c_ = np.polyfit(xs, ys, 1)
            r2 = 1 - np.sum((ys - (m_ * xs + c_)) ** 2) / np.sum((ys - ys.mean()) ** 2)
            notes.append(f"  {s}: least-squares fit to the digitized points (x = nominal hc): y = {m_:.3f}x {c_:+.3f}, R2 = {r2:.3f}; printed: {eq}")
    write_csv(str(HERE / f"fig16{key}.csv"), [
        f"Wei et al. 2025, Figure 16({key}), panel title '{title}': forces on the indenter along x, y, z vs indentation depth hc.",
        "Columns: series (Fx, Fy, Fz as in the legend: Fx black open squares, Fy red open triangles, Fz blue filled circles);",
        "  hc_nominal_A = the run's target indentation depth (4, 7, 10, 16, 22, 25 Å, Section 2.3) nearest to the marker;",
        "  hc_A = marker x position read from the figure (Å); force_nN = marker y position (nN);",
        "  match = normalized correlation of the marker with the legend symbol (1 = identical; lower where a dashed fit line crosses it).",
        "Provenance: tier 3, digitized from the embedded 300 ppi raster image (no vector data in the PDF) by fig16_extract.py:",
        "  markers located by template matching (the panel-(a) legend symbols as templates) on colour masks.",
        f"  x calibrated on the left frame (0) and the 5 long ticks 5-25 Å: max residual {resx:.3f} Å, {abs(sx):.4f} Å/px;",
        f"  y calibrated on the {len(YLAB[key])} long ticks {YLAB[key][0]}..{YLAB[key][-1]} nN of the left axis: max residual {resy:.3f} nN, {abs(sy):.4f} nN/px.",
        f"Uncertainty: about +-{2 * abs(sx):.2f} Å in x and +-{2 * abs(sy):.2f} nN in y (2 px).",
        "The dashed lines are the authors' linear fits; their printed equations (y = force in nN, x = hc in Å):",
        f"  Fz: {eq_z if eq_z else 'no fit line or equation printed for Fz in this panel'};  Fy: {eq_y}.",
        "Check of the printed fits against the digitized markers:",
    ] + notes + [f"Rejected weaker matches (glyphs of the printed equations/titles): " + (", ".join(f"{t[0]} at x {t[2]:.1f} Å, y {t[3]:.2f} nN (match {t[6]:.2f})" for t in rejected) or "none")] + ([f"Markers not found (hidden or overlapping): {missing}"] if missing else ["All 18 markers found (6 per series)."]),
        ["series", "hc_nominal_A", "hc_A", "force_nN", "match"], out, fmt=["{}", "{}", "{:.2f}", "{:.3f}", "{}"])
    print(key, "x res", round(resx, 3), "y res", round(resy, 3), "markers", len(rows), "missing", missing)
    for nline in notes:
        print(nline)
overlay(a, pts_all, str(ROOT / "work" / "fig16_overlay.png"))
