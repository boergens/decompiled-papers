"""Digitize Fig. 3 of Bouwer et al. 2016 (PDF p. 5), Monte Carlo simulation in carbon.

Panels a (1.5 keV) and c (3 keV): electron-trajectory plots with a depth scale bar (0/25/50 nm and
0/50/100/150 nm). Thousands of trajectories cannot be separated, so the CSVs give, per source pixel
column, the deepest pixel of the black trajectories (electrons that escape as BSE) and the deepest
pixel of any trajectory (black or grey: all electrons), converted to depth with the scale bar.
Panels b and d: 3D wireframe (mesh) plots of the BSE energy spread; a perspective mesh cannot be
digitized point by point, so only the peak height is measured (fig3bd_peak.csv), see below.

Source: the embedded raster image of Fig. 3 (1972 x 1065 px, 300 ppi, RGB) in source/bouwer2016.pdf.
No vector plot paths in the PDF, so tier 3 (a, c) and tier 4 (b, d, peak height only).
    python3 -I -B figures/fig3_extract.py  -> figures/fig3a.csv, fig3c.csv, fig3bd_peak.csv (+ work overlays)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import numpy as np  # noqa: E402
from digitize_common import embedded_image, fit_axis, write_csv, overlay  # noqa: E402

PDF = HERE.parent / "source" / "bouwer2016.pdf"
a = embedded_image(str(PDF), 5, bbox_near=(61.8, 384.4, 535.0, 639.9))
ai = a.astype(int)
mx, mn = ai.max(2), ai.min(2)
dark = mx < 110


def groups(idx):
    idx = np.asarray(idx)
    if len(idx) == 0:
        return []
    return [float(np.mean(g)) for g in np.split(idx, np.where(np.diff(idx) > 1)[0] + 1)]


# ---------------------------------------------------------------- panels a and c
black = mx < 70
grey = (mx >= 70) & (mx < 215) & (mx - mn < 30)   # neutral grey trajectories (antialiased edges included)
PANELS = {
    # name: (row range of the panel, labelled scale-bar values)
    "a": ((40, 520), [0, 25, 50]),
    "c": ((560, 1065), [0, 50, 100, 150]),
}
pts_all = []
for name, ((r0, r1), labels) in PANELS.items():
    # scale bar: the long vertical dark line right of the trajectories; ticks point right
    s = dark[r0:r1, 650:850].sum(0)
    sc = 650 + int(np.argmax(s))
    t20 = dark[r0:r1, sc + 1:sc + 21].mean(1) >= 0.9      # long (labelled) ticks
    t6 = dark[r0:r1, sc + 1:sc + 7].mean(1) >= 0.9        # all ticks
    major = [r0 + v for v in groups(np.where(t20)[0])]
    minor = [r0 + v for v in groups(np.where(t6)[0])]
    assert len(major) == len(labels), (name, major)
    flin, lres, lsl = fit_axis(major, labels)

    def fpw(r, major=major, labels=labels):   # piecewise linear through the labelled ticks (extrapolated at the ends)
        return float(np.interp(r, major, labels, left=np.nan, right=np.nan)) if major[0] <= r <= major[-1] else \
            float(flin(r))

    surface = major[0]
    rows, pts = [], []
    cols = range(0, sc - 15)
    for c in cols:
        bk = np.where(black[r0:r1, c])[0]
        al = np.where((black | grey)[r0:r1, c])[0]
        if len(al) == 0:
            continue
        rb = r0 + bk.max() if len(bk) else np.nan
        ra = r0 + al.max()
        if ra <= surface + 2 and (rb != rb or rb <= surface + 2):
            continue     # only trajectories above the surface (escaped BSE drawn upward) in this column
        rows.append([c, rb, ra])
        if rb == rb:
            pts.append((c, rb))
        pts.append((c, ra))
    xs_all = [r[0] for r in rows if r[2] > surface + 10]
    xc = (min(xs_all) + max(xs_all)) / 2       # centre of the cloud's horizontal extent below the surface
    out = []
    for c, rb, ra in rows:
        out.append([c, (c - xc) / abs(1 / lsl),
                    float(flin(rb)) if rb == rb else np.nan, fpw(rb) if rb == rb else np.nan,
                    float(flin(ra)), fpw(ra)])
    overlay(a, pts, str(HERE.parent / "work" / f"fig3{name}_overlay.png"))
    pts_all += pts
    energy = {"a": "1.5-keV", "c": "3-keV"}[name]
    spacing = [round(float(v), 1) for v in np.diff(major)]
    write_csv(str(HERE / f"fig3{name}.csv"), [
        f"Bouwer et al. 2016 Adv Struct Chem Imag 2:11, Fig. 3{name}: 'Penetration depth of a {energy} electron beam'",
        "  (Monte Carlo trajectories in carbon; black = electrons emerging as BSE, grey = electrons that stay in the substrate).",
        "Columns: x_px = column of the source image (300 ppi); x_nm_if_isotropic = lateral position in nm from the centre of the",
        "  trajectory cloud's horizontal extent, ASSUMING the lateral scale equals the depth scale (the figure has no",
        "  lateral scale; this is the decompiler's assumption, use x_px if in doubt); depth_bse_* = depth of the deepest",
        "  black pixel in that column; depth_all_* = depth of the deepest black or grey pixel (all trajectories).",
        "  *_lin_nm: linear fit on the labelled scale-bar ticks; *_pw_nm: piecewise linear through the labelled ticks.",
        "  Depth 0 = the '0 nm' tick (the red surface line); positive = into the substrate; negative = above the surface",
        "  (BSE trajectories leaving the sample are drawn up to the top edge of the panel).",
        "Provenance: tier 3, digitized from the embedded 300 ppi raster image (no vector data in the PDF) by fig3_extract.py.",
        f"  Scale bar: labelled ticks {labels} nm at rows {[round(v, 1) for v in major]} (spacings {spacing} px);",
        f"  all ticks at rows {[round(v, 1) for v in minor]}. Linear fit max residual {lres:.2f} nm.",
        ("  The scale-bar ticks are unevenly spaced (0-50 nm spans more pixels than 50-100 and 100-150 nm), so the linear"
         if name == "c" else "  The labelled ticks are nearly evenly spaced; linear and piecewise depths differ by at most about 0.2 nm."),
        ("  and piecewise depths differ by up to about 2 nm; it is not known which is right." if name == "c" else
         "  (The minor ticks are spaced 35.5-39 px.)"),
        f"Uncertainty: about +-{abs(lsl):.2f} nm (1 source pixel) plus the scale-bar unevenness; isolated stray trajectory",
        "  ends make the deepest-pixel profile spiky (it is an envelope of single trajectories, not a smooth curve).",
    ], ["x_px", "x_nm_if_isotropic", "depth_bse_lin_nm", "depth_bse_pw_nm", "depth_all_lin_nm", "depth_all_pw_nm"],
        out, fmt=["{}", "{:.2f}", "{:.2f}", "{:.2f}", "{:.2f}", "{:.2f}"])
    d = np.array([r[2:] for r in out], float)
    print(name, len(out), "cols; scale", major, "lin res", round(lres, 2),
          "max depth bse lin/pw", np.nanmax(d[:, 0]).round(1), np.nanmax(d[:, 1]).round(1),
          "all lin/pw", np.nanmax(d[:, 2]).round(1), np.nanmax(d[:, 3]).round(1))

# ---------------------------------------------------------------- panels b and d: peak height only
# The mesh plots use an orthographic 3D view, so a vertical (z) distance has the same pixel length
# everywhere in the panel. Calibrate z on the tick marks of the vertical z axis (slanted ticks meet the
# axis line), take the base level at the panel centre as the midpoint of the mesh's left and right corners
# (the mesh is flat there), and the apex as the topmost line pixel above that centre.
peak = []
line = mx < 225
for name, (r0, r1), zc, zlabels in (("b", (40, 530), 1071, [1.0, 0.8, 0.6, 0.4, 0.2]),
                                    ("d", (560, 1065), 1075, [1.0, 0.8, 0.6, 0.4, 0.2, 0.0])):
    axis = np.where(dark[r0:r1, zc])[0] + r0
    tk = [r0 + v for v in groups(np.where((ai[r0:r1, zc - 6:zc - 1].mean(2) < 200).sum(1) >= 3)[0])]
    tk = [v for v in tk if v < axis.max() - 3] if name == "b" else tk[:6]
    if name == "b":
        tk = [axis.min()] + tk      # the axis line's top end is the 1 tick (no tick mark drawn there)
    assert len(tk) == len(zlabels), (name, tk)
    fz, zres, zsl = fit_axis(tk, zlabels)
    mesh = (ai[:, :, 2] - ai[:, :, 0] > 40)
    mesh[:, :zc + 5] = False
    mesh[:r0] = False
    mesh[r1:] = False
    yy, xx = np.where(mesh)
    left = (xx.min(), yy[xx == xx.min()].mean())
    right = (xx.max(), yy[xx == xx.max()].mean())
    cx = (left[0] + right[0]) / 2
    base_y = (left[1] + right[1]) / 2
    win = line[r0:r1, int(cx) - 6:int(cx) + 7]
    apex_y = r0 + np.where(win.any(1))[0].min()
    apex_x = int(cx) - 6 + np.where(win[apex_y - r0])[0].mean()
    h = (base_y - apex_y) * abs(zsl)
    peak.append([name, float(h), float(apex_x - cx), float(abs(zsl)), float(zres)])
    pts_all += [(apex_x, apex_y), left, right, (cx, base_y)]
    print(name, "peak height", round(h, 3), "apex col offset from centre", round(apex_x - cx, 1), "z/px", abs(zsl), zres)
overlay(a, pts_all, str(HERE.parent / "work" / "fig3_overlay.png"))
write_csv(str(HERE / "fig3bd_peak.csv"), [
    "Bouwer et al. 2016 Adv Struct Chem Imag 2:11, Fig. 3b and 3d: 'Line scan of a BSE signal profile' (1.5 keV, b;",
    "  3 keV, d), drawn as 3D wireframe plots of 'BSE Energy Spread' over two 'Length in nm' axes.",
    "This is a measurement by the decompiler, not a digitized data series: the 3D mesh cannot be read point by point.",
    "Columns: panel; peak_height = height of the central spike in 'BSE Energy Spread' units above the flat background",
    "  at the panel centre; apex_offset_px = horizontal offset of the apex from the centre of the mesh (a check that the",
    "  spike sits at Length 0, 0); z_per_px = z-axis scale; z_fit_residual = max residual of the z tick fit.",
    "Method: orthographic view assumed (vertical distances have the same scale everywhere); z calibrated on the z-axis",
    "  tick marks (b: 0.2-0.8 plus the axis top at 1; d: 0-1); base level = midpoint of the mesh's left and right",
    "  corners; apex = topmost line pixel above the centre. Provenance: tier 4 (geometric reading).",
    "Uncertainty: about +-0.03 (the apex line is thin and faint; the base is the background level, slightly above 0).",
], ["panel", "peak_height", "apex_offset_px", "z_per_px", "z_fit_residual"], peak,
    fmt=["{}", "{:.3f}", "{:.1f}", "{:.5f}", "{:.4f}"])
