"""Helpers for the colour-keyed OVITO atom renderings of wei2024 (Figs. 5d, 6d, 8, 13, 14, 16).

These panels are particle renderings (shaded spheres), not fields on a grid. Each pixel is mapped
to the value of the nearest colour of the figure's own key bar (sampled from the image), when the
RGB distance to that colour is at most THR; other pixels (white background, gaps between atoms,
dark shaded sphere rims, labels, annotations) are left empty. Each pixel's colour is first scaled so
that its brightest channel is 255 (undoes the brightness shading of the spheres; the key colours
all have a brightest channel near 255), and only clearly coloured pixels are considered
(brightest channel >= MIN_MAX, (max - min) >= MIN_CHROMA * max). The result is therefore "the key
value of the colour of the rendered atom at this pixel", in image pixel coordinates (no length
calibration: the renderings carry no scale bar).

Functions:
  embedded(pdf, page, bbox)        -> RGB uint8 array of the embedded image (via digitize_common)
  find_panels(a, region, ...)      -> bounding boxes of saturated-colour blobs (the panels)
  sample_key(a, box)               -> (colours[n,3], fraction 0..1 along the bar) of a key bar
  map_panel(a, box, key, vmin, vmax, thr, exclude) -> float grid (NaN = unmapped), stats
  annotation_mask(a, lo, hi, min_area, dilate) -> mask of large single-colour annotation marks
  write_grid(path, header, grid)   -> CSV (gzip when > 2 MB); returns the path written
  read_grid(path)                  -> (grid, header lines)
"""
import csv
import gzip
import io
from pathlib import Path

import numpy as np
from scipy import ndimage as ndi
from scipy.spatial import cKDTree

import digitize_common as dc

THR = 60.0  # max RGB distance (0-441), after brightness normalisation, to the nearest key colour
MIN_MAX = 80      # pixels whose brightest channel is below this are too dark (sphere rims): unmapped
MIN_CHROMA = 0.5  # (max - min) / max below this is grey/white (background, labels, mesh): unmapped


def normalise(c):
    c = np.asarray(c, float)
    return c * (255.0 / np.maximum(c.max(axis=1), 1.0))[:, None]


def embedded(pdf, page, bbox):
    return dc.embedded_image(str(pdf), page, bbox_near=bbox).astype(np.int16)


def saturated(a, s=70):
    a = a.astype(int)
    return (a.max(axis=2) - a.min(axis=2)) >= s


def find_panels(a, region, min_area=15000, dilate=6, min_fill=0.25):
    """Boxes (x0, y0, x1, y1), exclusive ends, image pixels, of saturated blobs inside region."""
    x0, y0, x1, y1 = region
    m = saturated(a)[y0:y1, x0:x1]
    md = ndi.binary_dilation(m, iterations=dilate)
    lab, n = ndi.label(md)
    boxes = []
    for i, s in enumerate(ndi.find_objects(lab)):
        h = s[0].stop - s[0].start
        w = s[1].stop - s[1].start
        fill = m[s].sum() / float(h * w)
        if m[s].sum() >= min_area and fill >= min_fill:
            # shrink back by the dilation
            sub = m[s]
            rows = np.where(sub.any(axis=1))[0]
            cols = np.where(sub.any(axis=0))[0]
            boxes.append((x0 + s[1].start + cols[0], y0 + s[0].start + rows[0],
                          x0 + s[1].start + cols[-1] + 1, y0 + s[0].start + rows[-1] + 1))
    return sorted(boxes, key=lambda b: (round(b[1] / 100), b[0]))


def sample_key(a, box):
    """Key bar inside box: the saturated columns are the bar; colours = median of its middle rows."""
    x0, y0, x1, y1 = box
    m = saturated(a)[y0:y1, x0:x1]
    rows = np.where(m.sum(axis=1) > 0.6 * m.sum(axis=1).max())[0]
    cols = np.where(m[rows].mean(axis=0) > 0.5)[0]
    c0, c1 = cols[0], cols[-1]
    r0, r1 = rows[0], rows[-1]
    rr = slice(y0 + r0 + (r1 - r0) // 4, y0 + r1 - (r1 - r0) // 4 + 1)
    # drop the outermost column at each end (anti-aliased against the white page)
    cc = np.arange(x0 + c0 + 1, x0 + c1)
    colours = np.array([np.median(a[rr, c], axis=0) for c in cc], float)
    frac = (cc - (x0 + c0 + 1)) / float(len(cc) - 1)
    info = dict(bar_x0=int(x0 + c0), bar_x1=int(x0 + c1), bar_y0=int(y0 + r0), bar_y1=int(y0 + r1),
                n_colours=len(cc))
    return colours, frac, info


def annotation_mask(a, lo, hi, min_area=60, dilate=3, region=None):
    """Connected components of pixels with lo <= RGB <= hi (per channel) and area >= min_area."""
    a = a.astype(int)
    m = np.all((a >= np.array(lo)) & (a <= np.array(hi)), axis=2)
    if region is not None:
        keep = np.zeros_like(m)
        x0, y0, x1, y1 = region
        keep[y0:y1, x0:x1] = True
        m &= keep
    lab, n = ndi.label(m)
    if n == 0:
        return m
    sz = ndi.sum(m, lab, range(1, n + 1))
    big = np.isin(lab, 1 + np.where(sz >= min_area)[0])
    return ndi.binary_dilation(big, iterations=dilate)


def ellipse_mask(shape, cx, cy, rx, ry, width):
    """Annulus (ring) mask of an ellipse outline, for dashed annotation ellipses drawn over panels."""
    yy, xx = np.mgrid[0:shape[0], 0:shape[1]]
    r = np.sqrt(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2)
    return np.abs(r - 1) * min(rx, ry) <= width


def map_panel(a, box, key, vmin, vmax, thr=THR, exclude=None):
    colours, frac, _ = key
    x0, y0, x1, y1 = box
    sub = a[y0:y1, x0:x1].astype(float).reshape(-1, 3)
    mx = sub.max(axis=1)
    mn = sub.min(axis=1)
    chroma_ok = (mx >= MIN_MAX) & ((mx - mn) >= MIN_CHROMA * mx)
    norm = sub * (255.0 / np.maximum(mx, 1.0))[:, None]   # undo the sphere shading (brightness)
    tree = cKDTree(normalise(colours))
    d, idx = tree.query(norm)
    val = vmin + frac[idx] * (vmax - vmin)
    val[(d > thr) | ~chroma_ok] = np.nan
    grid = val.reshape(y1 - y0, x1 - x0)
    n_ex = 0
    if exclude is not None:
        ex = exclude[y0:y1, x0:x1]
        n_ex = int((ex & ~np.isnan(grid)).sum())
        grid[ex] = np.nan
    stats = dict(mapped=float(np.mean(~np.isnan(grid))), excluded=n_ex,
                 sat_unmapped=float(np.mean(saturated(a)[y0:y1, x0:x1] & np.isnan(grid))))
    return grid, stats


def write_grid(path, header, grid, digits=3):
    path = Path(path)
    buf = io.StringIO()
    for h in header:
        buf.write("# " + h + "\n")
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["row"] + [f"c{j}" for j in range(grid.shape[1])])
    for i, r in enumerate(grid):
        w.writerow([i] + ["" if np.isnan(v) else f"{v:.{digits}g}" for v in r])
    text = buf.getvalue()
    for old in (path, path.with_name(path.name + ".gz")):
        if old.exists():
            old.unlink()
    if len(text) > 2_000_000:
        path = path.with_name(path.name + ".gz")
        with gzip.open(path, "wt", newline="") as fh:
            fh.write(text)
    else:
        path.write_text(text)
    return path


def read_grid(path):
    path = Path(path)
    if not path.exists():
        path = path.with_name(path.name + ".gz")
    op = gzip.open if path.suffix == ".gz" else open
    with op(path, "rt") as fh:
        lines = fh.read().splitlines()
    head = [l for l in lines if l.startswith("#")]
    rows = list(csv.reader(l for l in lines if not l.startswith("#")))[1:]
    grid = np.array([[float(v) if v else np.nan for v in r[1:]] for r in rows])
    return grid, head


def segment_mask(shape, p0, p1, width):
    """Thick line segment mask (for dashed annotation arrows drawn over a panel)."""
    yy, xx = np.mgrid[0:shape[0], 0:shape[1]]
    p0 = np.array(p0, float)
    d = np.array(p1, float) - p0
    t = np.clip(((xx - p0[0]) * d[0] + (yy - p0[1]) * d[1]) / (d @ d), 0, 1)
    return np.hypot(xx - p0[0] - t * d[0], yy - p0[1] - t * d[1]) <= width


def run_figure(fig, pdf, page, bbox, keys, panels, exclude, csv_dir, work_dir, describe):
    """Map every panel and write <csv_dir>/<name>.csv(.gz) plus an overlay check image.

    keys:    {key_id: (search_box, vmin, vmax, quantity_with_unit)}
    panels:  [(name, box, key_id, printed_label)]
    exclude: boolean mask (image shape) of annotation pixels to leave empty, or None
    describe: one-line description of the figure for the CSV headers
    Overlay: work_dir/f4_<fig>_overlay.png = original panels (top) and the values re-coloured through
    the sampled key (bottom; unmapped pixels light grey), panel by panel.
    """
    from PIL import Image
    a = embedded(pdf, page, bbox)
    sampled = {k: sample_key(a, v[0]) for k, v in keys.items()}
    work_dir.mkdir(exist_ok=True)
    tiles = []
    report = []
    for name, box, kid, label in panels:
        box = tuple(int(v) for v in box)
        _, vmin, vmax, qty = keys[kid]
        colours, frac, kinfo = sampled[kid]
        grid, st = map_panel(a, box, sampled[kid], vmin, vmax, exclude=exclude)
        step = (vmax - vmin) / (kinfo["n_colours"] - 1)
        header = [
            f"Wei et al. 2024 (Acta Geotech. 20:1599-1620), {describe}; panel {name} (printed label: {label}).",
            f"Quantity: {qty}, read from the figure's colour key ({vmin} to {vmax}, linear along the key bar).",
            "Grid: one CSV row per image pixel row, columns c0.. = pixel columns, of the panel box "
            f"x {box[0]}-{box[2] - 1}, y {box[1]}-{box[3] - 1} (inclusive) in the embedded 300 ppi JPEG "
            f"(PDF page {page}); row 0 = top. No length scale: the renderings carry no scale bar.",
            "Provenance: tier 3 (digitized colour map), tools/f4_atommap.py: each pixel's colour scaled to "
            "brightest channel 255 (undoes sphere shading), then the value of the nearest key colour "
            f"(key bar sampled from the image: x {kinfo['bar_x0']}-{kinfo['bar_x1']}, y {kinfo['bar_y0']}-"
            f"{kinfo['bar_y1']}, {kinfo['n_colours']} colours, value step {step:.3g}) if the RGB distance "
            f"<= {THR:g}; empty = not mapped (white background, gaps between atoms, dark sphere rims, grey "
            "or black labels/outlines, annotation marks).",
            "CAUTION: these are the colours of rendered atoms (OVITO shaded spheres, overlapping in projection),"
            " not a continuous field; each pixel shows the front-most atom. Saturated ends of the key "
            f"mean '<= {vmin}' and '>= {vmax}'. JPEG compression shifts colours by a few units.",
            f"Mapped pixels: {st['mapped'] * 100:.1f} % of the box; coloured pixels left unmapped: "
            f"{st['sat_unmapped'] * 100:.1f} % of the box; annotation pixels removed: {st['excluded']}.",
        ]
        sel = np.round(np.linspace(0, len(colours) - 1, 11)).astype(int)
        header.append("Key colours sampled from the image at 0, 0.1, ..., 1 of the key bar (RGB; used by the "
                      "re-plot): " + " ".join("%d/%d/%d" % tuple(colours[i]) for i in sel))
        path = write_grid(csv_dir / f"{name}.csv", header, grid)
        # re-colour for the overlay check
        rec = np.full(grid.shape + (3,), 225, np.uint8)
        ok = ~np.isnan(grid)
        idx = np.clip(np.round((grid[ok] - vmin) / (vmax - vmin) * (len(colours) - 1)).astype(int), 0,
                      len(colours) - 1)
        rec[ok] = colours[idx].astype(np.uint8)
        orig = a[box[1]:box[3], box[0]:box[2]].astype(np.uint8)
        tiles.append(np.vstack([orig, np.full((4, orig.shape[1], 3), 0, np.uint8), rec]))
        report.append((name, path.name, grid.shape, round(st["mapped"], 3), round(st["sat_unmapped"], 3),
                       st["excluded"], float(np.nanmedian(grid)) if ok.any() else None))
    h = max(t.shape[0] for t in tiles)
    row = [np.vstack([t, np.full((h - t.shape[0], t.shape[1], 3), 255, np.uint8)]) for t in tiles]
    sep = np.full((h, 8, 3), 255, np.uint8)
    out = row[0]
    for t in row[1:]:
        out = np.hstack([out, sep, t])
    Image.fromarray(out).save(work_dir / f"f4_{fig}_overlay.png")
    return report


def replot(fig, csv_dir, panels, vmins, out_png, ncols):
    """Draw all panels of a figure from their CSVs (colour map = the key colours listed in the CSV header, NaN white)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    n = len(panels)
    nrows = (n + ncols - 1) // ncols
    f, axs = plt.subplots(nrows, ncols, figsize=(3.2 * ncols, 2.2 * nrows), squeeze=False)
    for ax in axs.flat:
        ax.axis("off")
    for ax, (name, label, kid) in zip(axs.flat, panels):
        g, _ = read_grid(csv_dir / f"{name}.csv")
        vmin, vmax, unit = vmins[kid]
        from matplotlib.colors import LinearSegmentedColormap
        kl = [h for h in _ if "Key colours sampled" in h]
        if kl:
            rgb = [tuple(int(v) / 255 for v in t.split("/")) for t in kl[0].split(": ")[-1].split()]
            cm = LinearSegmentedColormap.from_list("key", rgb)
        else:
            cm = plt.get_cmap("jet").copy()
        cm.set_bad("white")
        im = ax.imshow(np.ma.masked_invalid(g), cmap=cm, vmin=vmin, vmax=vmax, interpolation="nearest")
        ax.set_title(f"{name}\n{label}", fontsize=7)
        cb = f.colorbar(im, ax=ax, fraction=0.04, pad=0.02)
        cb.ax.tick_params(labelsize=6)
        cb.set_label(unit, fontsize=6)
    f.savefig(out_png, dpi=90, bbox_inches="tight")
