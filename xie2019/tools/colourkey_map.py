"""Map the pixels of an OVITO-style atom rendering coloured through a printed jet colour key back to values
(xie2019 Figs. 6, 8, 9, 11). Written for xie2019, after the bar-LUT idea of sun2019's afm_map.py.

The atoms are drawn as shaded spheres with highlights, so a pixel's colour is the key colour darkened (shading) or
paled (highlight, fog) by an amount that varies across each sphere. Matching RGB therefore fails; the jet key's
hue, however, runs monotonically from blue (240 deg) through cyan, green and yellow to red (0 deg), and hue is
unchanged by darkening and paling. So bar and pixels are matched on hue: a pixel gets the median value of the bar
rows whose hue is within TOL_H of the closest bar hue. Consequence: the dark ends of the key (dark blue -> blue,
red -> dark red) differ from their neighbours only in brightness, not in hue, so values in those runs cannot be
told apart and come out as the middle of the run (the run limits are reported by ambiguous_ends()).

Only coloured pixels are mapped (max channel >= MIN_V, saturation (max-min)/max >= MIN_S): white background,
grey tool atoms, black text and outlines and grey anti-aliasing stay empty (NaN).
"""
import gzip

import numpy as np

TOL_H = 2.0      # degrees
MAX_DH = 15.0    # pixels farther than this in hue from every bar row stay empty (fig11 renders the key blue at ~250 deg)
MIN_V = 70
MIN_S = 0.30


def norm(rgb):
    rgb = np.asarray(rgb, float)
    m = rgb.max(-1, keepdims=True)
    return 255.0 * rgb / np.maximum(m, 1.0)


def hue(rgb):
    """Hue in degrees, with magenta-red hues (> 300) wrapped to negative values (jet's red end is ~0)."""
    rgb = np.asarray(rgb, float)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    mx, mn = rgb.max(-1), rgb.min(-1)
    c = np.maximum(mx - mn, 1e-9)
    h = np.where(mx == r, ((g - b) / c) % 6, np.where(mx == g, (b - r) / c + 2, (r - g) / c + 4)) * 60.0
    return np.where(h > 300, h - 360, h)


def bar_lut(a, c0, c1, row_top, row_bot, v_top, v_bot, margin=2):
    """Bar colours (normalized to unit brightness, for drawing) and values per bar row."""
    rows = np.arange(row_top + margin, row_bot - margin + 1)
    col = a[rows][:, c0:c1 + 1].astype(float).mean(1)
    vals = v_top + (v_bot - v_top) * (rows - row_top) / (row_bot - row_top)
    return norm(col), vals


def ambiguous_ends(lut_rgb, lut_val):
    """Value ranges at the two ends of the bar whose hue is within TOL_H of the end hue."""
    hb = hue(lut_rgb)
    out = []
    for end in (0, -1):
        v = lut_val[np.abs(hb - hb[end]) <= TOL_H]
        out.append((float(v.min()), float(v.max())))
    return out


def map_image(img, lut_rgb, lut_val):
    """Return an array of values (NaN where not mapped)."""
    h, w, _ = img.shape
    f = img.reshape(-1, 3).astype(int)
    mx, mn = f.max(1), f.min(1)
    ok = (mx >= MIN_V) & ((mx - mn) / np.maximum(mx, 1) >= MIN_S)
    out = np.full(h * w, np.nan)
    u, inv = np.unique(f[ok], axis=0, return_inverse=True)
    inv = inv.ravel()
    hu, hb = hue(u), hue(lut_rgb)
    vals = np.full(len(u), np.nan)
    for s in range(0, len(u), 5000):
        d = np.abs(hu[s:s + 5000, None] - hb[None, :])
        dmin = d.min(1)
        near = d <= (dmin[:, None] + TOL_H)
        v = np.where(near, lut_val[None, :], np.nan)
        med = np.nanmedian(v, axis=1)
        med[dmin > MAX_DH] = np.nan
        vals[s:s + 5000] = med
    out[np.where(ok)[0]] = vals[inv]
    return out.reshape(h, w)


def write_grid_gz(path, header_lines, z, decimals):
    fmt = f"{{:.{decimals}f}}"
    with gzip.open(path, "wt", newline="") as f:
        for hl in header_lines:
            f.write("# " + hl + "\n")
        f.write("row," + ",".join(f"c{j}" for j in range(z.shape[1])) + "\n")
        for i, row in enumerate(z):
            f.write(str(i) + "," + ",".join("" if v != v else fmt.format(v) for v in row) + "\n")


def read_grid_gz(path):
    with gzip.open(path, "rt") as f:
        lines = [l for l in f if not l.startswith("#")]
    rows = [l.rstrip("\n").split(",")[1:] for l in lines[1:]]
    return np.array([[float(x) if x else np.nan for x in r] for r in rows])


def trim_box(img, box, white=235):
    """Shrink a (c0, r0, c1, r1) box (inclusive-exclusive) to its non-white content."""
    c0, r0, c1, r1 = box
    sub = img[r0:r1, c0:c1].min(2) < white
    rs, cs = np.where(sub.any(1))[0], np.where(sub.any(0))[0]
    return (c0 + int(cs[0]), r0 + int(rs[0]), c0 + int(cs[-1]) + 1, r0 + int(rs[-1]) + 1)


def extract_figure(cfg, here):
    """Run one figure: cfg keys pdf, page, bbox, shape, bar=(c0, c1, row_top, row_bot, v_top, v_bot), panels={name: box},
    mask_boxes={name: [boxes in image px]}, decimals, stem, header (list of lines; '{ends}', '{panel}', '{box}' filled in).
    Writes <stem><panel>.csv.gz and ../work/<stem>_map_check.png (mapped values drawn in jet over the image)."""
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from digitize_common import embedded_image
    a = embedded_image(cfg["pdf"], cfg["page"], bbox_near=cfg["bbox"])
    assert a.shape[:2] == cfg["shape"], a.shape
    c0, c1, rt, rb, vt, vb = cfg["bar"]
    lut_rgb, lut_val = bar_lut(a, c0, c1, rt, rb, vt, vb)
    ends = ambiguous_ends(lut_rgb, lut_val)
    full = np.full(a.shape[:2], np.nan)
    stats = {}
    for name, box in cfg["panels"].items():
        x0, y0, x1, y1 = trim_box(a, box)
        sub = a[y0:y1, x0:x1]
        z = map_image(sub, lut_rgb, lut_val)
        for (m0, n0, m1, n1) in cfg.get("mask_boxes", {}).get(name, []):
            z[max(0, n0 - y0):max(0, n1 - y0), max(0, m0 - x0):max(0, m1 - x0)] = np.nan
        if cfg.get("post"):
            z = cfg["post"](name, sub, z)
        full[y0:y1, x0:x1] = z
        flagged = np.isfinite(z) & ((z <= max(ends[1]) + 1e-9) & (z >= min(ends[1]) - 1e-9) | (z <= max(ends[0]) + 1e-9) & (z >= min(ends[0]) - 1e-9))
        hdr = [h.format(panel=name, box=f"columns {x0}-{x1 - 1}, rows {y0}-{y1 - 1}", ends=f"{ends[0][0]:.3g} to {ends[0][1]:.3g} and {ends[1][0]:.3g} to {ends[1][1]:.3g}")
               for h in cfg["header"]]
        hdr.append(f"Grid: {z.shape[0]} rows x {z.shape[1]} columns; {int(np.isfinite(z).sum())} mapped pixels "
                   f"({100 * np.isfinite(z).mean():.1f} %), {int(flagged.sum())} of them in an end-ambiguous run.")
        write_grid_gz(str(here / f"{cfg['stem']}{name}.csv.gz"), hdr, z, cfg["decimals"])
        stats[name] = (z.shape, float(np.isfinite(z).mean()), float(np.nanmin(z)) if np.isfinite(z).any() else None,
                       float(np.nanmax(z)) if np.isfinite(z).any() else None)
    # check image: mapped values re-coloured through the LUT (normalized colours), unmapped pixels light grey
    chk = np.full(a.shape, 225, np.uint8)
    ok = np.isfinite(full)
    idx = np.clip(np.searchsorted(-lut_val if lut_val[0] > lut_val[-1] else lut_val,
                                  -full[ok] if lut_val[0] > lut_val[-1] else full[ok]), 0, len(lut_val) - 1)
    chk[ok] = lut_rgb[idx].astype(np.uint8)
    from PIL import Image
    work = here.parent / "work"
    work.mkdir(exist_ok=True)
    Image.fromarray(np.concatenate([a, chk], 1)).save(str(work / f"{cfg['stem']}_map_check.png"))
    return ends, stats


def replot_figure(here, stem, panels, layout, vmin, vmax, label, out_png):
    """Re-plot the panels of one figure from their grid CSVs with a jet colour map and a colour bar."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    nr, nc = layout
    fig, axs = plt.subplots(nr, nc, figsize=(5 * nc, 2.2 * nr * (1.6 if stem in ("fig8", "fig11") else 1)), squeeze=False)
    im = None
    for ax, name in zip(axs.ravel(), panels):
        z = read_grid_gz(str(here / f"{stem}{name}.csv.gz"))
        im = ax.imshow(z, cmap="jet", vmin=min(vmin, vmax), vmax=max(vmin, vmax), interpolation="nearest")
        ax.set_title(f"{name})", loc="left", fontsize=9)
        ax.set_xticks([])
        ax.set_yticks([])
    for ax in axs.ravel()[len(panels):]:
        ax.axis("off")
    fig.colorbar(im, ax=axs.ravel().tolist(), label=label, shrink=0.8)
    fig.savefig(str(here / out_png), dpi=110)


def mask_outline_colour(sub, z, hue_lo, hue_hi, max_v, grow=2):
    """Blank pixels of a drawn outline (e.g. the authors' dark blue-grey ellipses): hue in [hue_lo, hue_hi] and
    brightness (max channel) below max_v, grown by `grow` px."""
    from scipy.ndimage import binary_dilation
    h = hue(sub)
    m = (h >= hue_lo) & (h <= hue_hi) & (sub.max(2) < max_v) & (sub.max(2) > 40)
    z = z.copy()
    z[binary_dilation(m, iterations=grow)] = np.nan
    return z
