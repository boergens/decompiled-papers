"""Calibrated colour maps of the 3D laser scanning confocal microscope (SCM) panels of the
kubota2018 SI: Supp. Figs. 3b, 3d, 4c, 5c, 7d (tier 3, colour map through the colour bar).

Method (all at the native resolution of the embedded JPEG):
  1. sample the colour bar along its length (mean over its inner width), one sample per pixel;
  2. calibrate bar position -> value on the bar's printed labels (tick marks where the bar has
     them, otherwise the label positions; see each config) with a least-squares line;
  3. convert every map pixel and every bar sample to CIE Lab. The rendering shades the relief
     (lighting and shadows), which changes lightness and chroma but keeps the hue, so each map pixel
     gets the value of the bar sample with the nearest hue angle in the a*b* plane (ties broken by
     lightness: distance = hue difference in degrees + 0.3 x |L difference|). Pixels with chroma
     below C_MIN (greys, white or black labels, black/very dark map regions, highlights) or with no
     bar hue within HUE_MAX degrees are left empty (NaN).
The SCM images are rendered with 3D shading (lighting and shadows on the relief), so colours are
shifted by the shading and the mapped values are approximate; the printed numbers in the figures
are the authors' measurements.
"""
import os
import sys

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sfig_common import WORK, si_image  # noqa: E402
from digitize_common import fit_axis  # noqa: E402

HUE_MAX = 12.0   # degrees
C_MIN = 15.0     # minimum Lab chroma of a map pixel to be mapped

# All coordinates: pixels of the embedded image (x = column, y = row), inclusive ranges.
CONFIGS = {
    "sfig3b": dict(
        limits="the bar is black (no hue) below about -780 nm, so the deepest parts of the 10-8 keV squares are empty or too shallow, and its hue is constant (red) from about +100 nm to the top, so values there (the untreated surface) rest on lightness only and are not resolved",
        page=12, panel="Supplementary Figure 3b", map=(3, 192, 325, 325),
        bar=dict(orient="h", along=(138, 297), across=(300, 304)),
        calib=[(137, -1200), (174, -800), (213, -400), (252, 0), (290, 400)],
        calib_how="tick marks below the bar at the labels -1200, -800, -400, 0, 400 (nm)",
        exclude=[(134, 296, 300, 310)],
        bar_text="horizontal colour bar 'depth', labels -1200 -800 -400 0 400 nm; black (-1200) - blue - cyan - "
                 "green - yellow - orange - red (400 and beyond: the bar continues about 7 px past the 400 tick)",
        squares=[  # (label, printed value, x centre, y centre)  -- the depth printed above each imaged square
            ("10 keV", -808, 27, 258), ("9 keV", -708, 55, 258), ("8 keV", -614, 88, 258), ("7 keV", -511, 122, 258),
            ("6 keV", -419, 149, 257), ("5 keV", -324, 177, 255), ("4 keV", -232, 212, 257),
            ("3 keV", -163, 250, 262), ("2.5 keV", -140, 290, 267)]),
    "sfig3d": dict(
        limits="the hue changes monotonically along the whole bar (cyan to orange), so every value on the scale can be resolved",
        page=12, panel="Supplementary Figure 3d", map=(330, 192, 701, 325),
        bar=dict(orient="h", along=(482, 670), across=(304, 306)),
        calib=[(483.5, -180), (516, -100), (546.5, 0), (577.5, 100), (607.5, 200), (636.5, 300), (668.5, 380)],
        calib_how="tick marks below the bar at the labels -180 -100 0 100 200 300 380 (nm); the end labels"
                  " are not evenly spaced with the inner ones (-180 to -100 is 32.5 px but 100 nm steps are about"
                  " 30 px), so the least-squares line leaves residuals of up to about 20 nm",
        exclude=[(478, 299, 676, 312)],
        bar_text="horizontal colour bar 'depth', labels -180 -100 0 100 200 300 380 nm; cyan (-180) - green - "
                 "yellow - orange (380)",
        squares=[("10 keV", 134, 349, 247), ("9 keV", 113, 392, 247), ("8 keV", 109, 427, 247),
                 ("7 keV", 85, 460, 247), ("6 keV", 44, 492, 247), ("5 keV", 54, 524, 247),
                 ("4 keV", 45, 556, 261), ("3 keV", 21, 590, 266), ("2.5 keV", 11, 623, 270),
                 ("10 keV (right)", 136, 677, 248)]),
    "sfig4c": dict(
        limits="the bar is black/very dark (no hue) below about -330 nm, so the darkest centres of the 6 keV squares are empty, and its hue is constant (red-orange) from about +50 nm to the top, so values there rest on lightness only and are not resolved",
        page=13, panel="Supplementary Figure 4c", map=(459, 324, 719, 588),
        bar=dict(orient="v", along=(334, 514), across=(475, 477)),
        calib=[(333.8, 430), (378.5, 200), (422.5, 0), (467.0, -200), (511.0, -380)],
        calib_how="centres of the printed labels 430, 200, 0, -200, -380 (nm) beside the bar (no tick marks);"
                  " the end labels sit at the bar ends and are not evenly spaced with the inner ones, so the"
                  " least-squares line leaves residuals of up to about 25 nm",
        exclude=[(466, 324, 502, 525), (636, 500, 719, 588)],
        bar_text="vertical colour bar 'depth', labels 430 (top) 200 0 -200 -380 nm (bottom); red (430) - orange - "
                 "yellow - green - cyan - blue - black (-380)",
        squares=[(f"{kev} keV, {dw} µs", v, x, y)
                 for kev, y, xs, vals in (
                     (6, 363, (582, 614, 646, 679), (-240, -245, -250, -265)),
                     (5, 403, (572, 603, 634, 668), (-169, -131, -147, -165)),
                     (4, 443, (557, 588, 620, 652), (-80, -94, -95, -98)),
                     (3, 488, (533, 564, 596, 628), (-93, -82, -74, -92)),
                     (2, 558, (487, 518, 550, 583), (-65, -63, -67, -67)))
                 for dw, x, v in zip((0.8, 1.6, 3.2, 6.4), xs, vals)]),
    "sfig5c": dict(
        limits="the bar is black (no hue) below about -290 nm, so the dark grey centres of the 6 keV squares are empty",
        page=14, panel="Supplementary Figure 5c", map=(540, 514, 797, 940),
        bar=dict(orient="v", along=(765, 918), across=(786, 790)),
        calib=[(764, -480), (919, 0)],
        calib_how="the bar ends (black end row 764 = -480, red end row 919 = 0 nm), where the end labels"
                  " -480 and 0 are printed; the rotated inner labels -400 and -200 span rows 784-809 and 846-866,"
                  " which contain the positions this line gives them (790 and 854)",
        exclude=[(758, 745, 797, 930)],
        bar_text="vertical colour bar 'depth (nm)', labels -480 (top) -400 -200 0 (bottom), rotated; black (-480) - "
                 "blue - cyan - green - yellow - orange - red (0)",
        squares=[(f"{kev} keV, {dw} µs", v, x, y)
                 for kev, y, vals in (
                     (6, 557, (-173, -241, -242, -252)), (5, 611, (-176, -185, -205, -224)),
                     (4, 666, (-82, -139, -123, -160)), (3, 725, (-53, -95, -63, -91)),
                     (2, 785, (-39, -45, -47, -60)), (1.5, 847, (-29, -38, -38, -50)),
                     (1, 912, (-17, -25, -24, -32)))
                 for dw, x, v in zip((0.8, 1.6, 3.2, 6.4), (594, 646, 697, 750), vals)]),
    "sfig7d": dict(
        limits="the hue is constant (red) from about 400 nm to the top (800), so the dark red bumps map to the red segment by lightness only and their heights (400-800 nm) are not resolved",
        page=17, panel="Supplementary Figure 7d", map=(535, 32, 706, 456),
        bar=dict(orient="v", along=(224, 435), across=(682, 687)),
        calib=[(223, 800), (277, 600), (330, 400), (384, 200), (438, 0)],
        calib_how="centres of the printed labels 800, 600, 400, 200, 0 (nm) beside the bar (no tick marks)",
        exclude=[(640, 214, 706, 452)],
        bar_text="vertical colour bar 'depth', labels 800 (top) 600 400 200 0 nm (bottom); red (800) - orange - "
                 "yellow - green - cyan - blue - dark blue (0)",
        squares=[]),
}


def to_lab(rgb):
    f = rgb.astype(np.float32) / 255.0
    return cv2.cvtColor(f.reshape(-1, 1, 3), cv2.COLOR_RGB2LAB).reshape(-1, 3)


def bar_samples(img, bar):
    a0, a1 = bar["along"]
    c0, c1 = bar["across"]
    if bar["orient"] == "h":
        cols = img[c0:c1 + 1, a0:a1 + 1].astype(float).mean(0)
    else:
        cols = img[a0:a1 + 1, c0:c1 + 1].astype(float).mean(1)
    pos = np.arange(a0, a1 + 1, dtype=float)
    return pos, cols


def map_values(key):
    cfg = CONFIGS[key]
    img = si_image(cfg["page"])
    pos, cols = bar_samples(img, cfg["bar"])
    f, res, slope = fit_axis([p for p, _ in cfg["calib"]], [v for _, v in cfg["calib"]])
    bar_val = f(pos)
    bar_lab = to_lab(np.clip(cols, 0, 255))
    x0, y0, x1, y1 = cfg["map"]
    sub = img[y0:y1 + 1, x0:x1 + 1]
    lab = to_lab(sub)
    hue = np.degrees(np.arctan2(lab[:, 2], lab[:, 1]))
    chroma = np.hypot(lab[:, 1], lab[:, 2])
    bhue = np.degrees(np.arctan2(bar_lab[:, 2], bar_lab[:, 1]))
    bchroma = np.hypot(bar_lab[:, 1], bar_lab[:, 2])
    usable = bchroma >= C_MIN            # bar samples with a defined hue (not the black end)
    dh = np.abs((hue[:, None] - bhue[None, usable] + 180) % 360 - 180)
    dist = dh + 0.3 * np.abs(lab[:, None, 0] - bar_lab[None, usable, 0])
    j = dist.argmin(1)
    de = dh[np.arange(len(j)), j]
    val = bar_val[usable][j].astype(float)
    val[(de > HUE_MAX) | (chroma < C_MIN)] = np.nan
    val = val.reshape(sub.shape[:2])
    de = de.reshape(sub.shape[:2])
    for ex0, ey0, ex1, ey1 in cfg["exclude"]:
        val[max(0, ey0 - y0):max(0, ey1 - y0 + 1), max(0, ex0 - x0):max(0, ex1 - x0 + 1)] = np.nan
    return dict(cfg=cfg, img=img, val=val, de=de, bar_pos=pos, bar_rgb=cols, bar_val=bar_val, res=res,
                slope=slope)


def squares_check(m, half=5):
    """Mean and 5th/95th percentile of the mapped values in a (2*half+1)^2 core box of each square, and
    the surface level = median of all mapped map pixels (most of each map is untreated surface)."""
    cfg, val = m["cfg"], m["val"]
    x0, y0 = cfg["map"][:2]
    surface = float(np.nanmedian(val))
    out = []
    for label, printed, xc, yc in cfg["squares"]:
        box = val[yc - y0 - half:yc - y0 + half + 1, xc - x0 - half:xc - x0 + half + 1]
        ok = box[np.isfinite(box)]
        if not len(ok):
            out.append((label, printed, np.nan, np.nan, np.nan, 0))
            continue
        extreme = np.percentile(ok, 5) if printed < 0 else np.percentile(ok, 95)
        out.append((label, printed, float(ok.mean()) - surface, float(extreme) - surface, float(ok.mean()), len(ok)))
    return surface, out


def write(key):
    m = map_values(key)
    cfg, val = m["cfg"], m["val"]
    x0, y0, x1, y1 = cfg["map"]
    surface, sq = squares_check(m)
    path = os.path.join(HERE, f"{key}.csv")
    nan_frac = float(np.isnan(val).mean())
    with open(path, "w") as fh:
        hdr = [
            f"{cfg['panel']} (kubota2018 SI p. {cfg['page']}): 3D laser SCM surface map, colour mapped to depth (nm) through"
            " the colour bar printed in the panel",
            "provenance: tier 3, calibrated colour map; embedded raster image of SI page"
            f" {cfg['page']} read at native resolution; script sfig_scm.py ({key}_extract.py runs it)",
            f"colour bar: {cfg['bar_text']}",
            f"calibration: {cfg['calib_how']}; least-squares max residual {m['res']:.1f} nm;"
            f" one bar pixel = {abs(m['slope']):.2f} nm",
            f"mapping: nearest bar hue in the CIE Lab a*b* plane (shading changes lightness and chroma, not hue);"
            f" pixels with chroma < {C_MIN:g} or no bar hue within {HUE_MAX:g} degrees are empty (labels, arrows,"
            f" grey or black regions, highlights, dirt; {100 * nan_frac:.0f} % of this map). Bar samples without a"
            " hue (a black end) cannot be matched, so the darkest part of the scale is never assigned; the colour bar itself"
            " and its labels are blanked" + (" and so is the inset graph (bottom right)" if key == "sfig4c" else ""),
            "CAUTION: the SCM image is rendered with 3D shading (lighting and shadows on the relief) over a JPEG; the"
            " shading shifts colours, so the values are approximate (rims of the squares and slopes especially);"
            " the numbers printed in the figure are the authors' measurements",
            f"limits of the colour scale: {cfg['limits']}",
            "values are absolute positions on the colour scale, not relative to the surrounding surface;"
            f" the median of all mapped pixels (mostly untreated surface) is {surface:.0f} nm",
            f"grid: one line per pixel row; first column y_px (row in the embedded image), then one value per pixel"
            f" column x_px = {x0} ... {x1} (header row gives x_px); no length scale is applied (pixel units only)",
        ]
        if sq:
            hdr.append("cross-check (decompiler): for each imaged square, mapped value in an 11 x 11 px core box minus the"
                       " surface median, mean and 5th (depressions) or 95th (expansions) percentile, vs the printed number:")
            for label, printed, dmean, dext, mean, n in sq:
                hdr.append(f"  {label}: printed {printed}; mapped core mean - surface {dmean:.0f}; percentile - surface"
                           f" {dext:.0f} (n = {n})" if n else f"  {label}: printed {printed}; no mapped pixels in the core box")
        for h in hdr:
            fh.write("# " + h + "\n")
        fh.write("y_px," + ",".join(str(x) for x in range(x0, x1 + 1)) + "\n")
        for r in range(val.shape[0]):
            fh.write(str(y0 + r) + "," + ",".join("" if not np.isfinite(v) else f"{v:.0f}" for v in val[r]) + "\n")
    # bar samples, for the replot's colour scale
    with open(os.path.join(HERE, f"{key}_colourbar.csv"), "w") as fh:
        fh.write(f"# {cfg['panel']}: colour bar samples (mean RGB across the bar) and the calibrated value of each\n")
        fh.write("# provenance: read from the embedded image by sfig_scm.py; used by the replot for its colour scale\n")
        fh.write("bar_px,value_nm,r,g,b\n")
        for p, v, c in zip(m["bar_pos"], m["bar_val"], m["bar_rgb"]):
            fh.write(f"{p:.0f},{v:.1f},{c[0]:.0f},{c[1]:.0f},{c[2]:.0f}\n")
    from PIL import Image
    Image.fromarray(m["img"][y0:y1 + 1, x0:x1 + 1]).save(os.path.join(WORK, f"supp_{key}_orig.png"))
    return m, surface, sq


def replot(key):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    with open(os.path.join(HERE, f"{key}.csv")) as fh:
        lines = [l.rstrip("\n") for l in fh if not l.startswith("#")]
    xs = [int(x) for x in lines[0].split(",")[1:]]
    ys, grid = [], []
    for l in lines[1:]:
        p = l.split(",")
        ys.append(int(p[0]))
        grid.append([float(v) if v else np.nan for v in p[1:]])
    grid = np.array(grid)
    with open(os.path.join(HERE, f"{key}_colourbar.csv")) as fh:
        bl = [l.strip().split(",") for l in fh if not l.startswith("#")][1:]
    bv = np.array([float(q[1]) for q in bl])
    brgb = np.array([[float(q[2]), float(q[3]), float(q[4])] for q in bl]) / 255
    order = np.argsort(bv)
    cmap = ListedColormap(brgb[order])
    cmap.set_bad((0.85, 0.85, 0.85))
    h, w = grid.shape
    fig, ax = plt.subplots(figsize=(max(3, w / 60), max(2.2, h / 60)))
    im = ax.imshow(grid, cmap=cmap, vmin=bv.min(), vmax=bv.max(), extent=(xs[0] - .5, xs[-1] + .5, ys[-1] + .5, ys[0] - .5))
    fig.colorbar(im, ax=ax, label="depth (nm), from the colour bar")
    ax.set_xlabel("x (px, embedded image)")
    ax.set_ylabel("y (px)")
    ax.set_title(f"{key}: mapped depth (grey = no bar colour)", fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, f"{key}_replot.png"), dpi=120)
    plt.close(fig)


if __name__ == "__main__":
    for k in (sys.argv[1:] or CONFIGS):
        m, surface, sq = write(k)
        de = m["de"]
        print(k, "res", round(m["res"], 1), "nm/px", round(abs(m["slope"]), 2), "nan", round(float(np.isnan(m["val"]).mean()), 3),
              "dE pct 50/90/99", np.round(np.percentile(de, [50, 90, 99]), 1), "surface", round(surface) if surface == surface else None)
        for s in sq:
            print("   ", s[0], s[1], None if s[5] == 0 else (round(s[2]), round(s[3]), round(s[4])), s[5])
