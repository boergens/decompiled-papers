"""Decompiler's measurement (not data of the paper): scale bars against mosaic geometry in Figs. 2-5.

    python3 -I -B figures/figs2to5_scalebars_extract.py      (from the entry folder; writes figures/figs2to5_scalebars.csv)

Each of Figs. 2-5 is a mosaic of 61 single-beam subimages with a "10 um" scale bar at the lower left, a marked
rectangle, and an enlarged inset ("12 um x 10 um single-beam subimage", inset scale bar 5 um per the captions). The
text (p. 3) gives the distance between single beams as 12 um and the tiles' aspect ratio as about 0.866. This script
measures, in the native pixels of each embedded image (300 dpi in print):
  - the main scale bar: the longest thick (>= 3 rows) near-white horizontal bar in the lower-left quarter;
  - the inset scale bar: the thick (>= 8 rows) near-white bar of 150-260 px in the lower-right part;
  - the tile pitch: the stepped left and right outlines of the mosaic (first/last non-black pixel per row); the
    outline moves by half a tile from one tile row to the next (hexagonal arrangement), and each tile row is a
    plateau of the outline;
  - the marked rectangle and the lower-right inset: white frame lines (near-white runs of >= 140 px), inner size.
and derives the scale (px per um) three ways: from the "10 um" bar, from the 12 um beam distance (tile pitch), and
from the inset's 5 um bar divided by the inset magnification (inset width / marked-rectangle width).
"""
import csv
import io
import os

import numpy as np
import pymupdf
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(os.path.dirname(HERE), "source", "jmi0259-0114.pdf")
OUT = os.path.join(HERE, "figs2to5_scalebars.csv")
PAGES = {2: 3, 3: 4, 4: 5, 5: 6}  # figure -> PDF page


def image(page):
    doc = pymupdf.open(PDF)
    xref = doc[page - 1].get_images(full=True)[0][0]
    return np.asarray(Image.open(io.BytesIO(doc.extract_image(xref)["image"])).convert("L")).astype(int)


def longest_runs(mask):
    """For each row of a boolean array: (start, length) of its longest True run."""
    out = []
    for row in mask:
        best, bs, run, rs = 0, 0, 0, 0
        for i, v in enumerate(row):
            if v:
                if run == 0:
                    rs = i
                run += 1
                if run > best:
                    best, bs = run, rs
            else:
                run = 0
        out.append((bs, best))
    return out


def bar(a, x0, x1, y0, y1, lo, hi, thick):
    """Length of a near-white horizontal bar of lo..hi px with at least `thick` rows in the region."""
    runs = longest_runs(a[y0:y1, x0:x1] > 225)
    lens = [n for s, n in runs if lo <= n <= hi]
    if len(lens) < thick:
        raise SystemExit("bar not found")
    return int(np.median(lens))


def outline_pitch(a):
    h, w = a.shape
    left, right = [], []
    for y in range(h):
        off = 200 if y < 200 else 0  # skip the figure-number box in the top-left corner
        nz = np.where(a[y, off:] > 30)[0]
        left.append(nz.min() + off if len(nz) else -1)
        nzr = np.where(a[y, :w - 1] > 30)[0]
        right.append(nzr.max() if len(nzr) else -1)
    steps, rows = [], []
    for edge in (left, right):
        pl, start = [], 0
        for y in range(1, h + 1):
            if y == h or abs(edge[y] - edge[start]) > 4:
                if y - start >= 25 and edge[start] not in (-1, 0, w - 2):
                    pl.append((start, y - 1, int(np.median(edge[start:y]))))
                start = y
        trans = []  # rows where the outline jumps by half a tile (between two plateaus less than 30 rows apart)
        for p, q in zip(pl, pl[1:]):
            dx = abs(q[2] - p[2])
            if 60 <= dx <= 100 and q[0] - p[1] < 30:
                steps.append(dx)
                trans.append((p[1] + q[0]) / 2)
        rows += [b - a for a, b in zip(trans, trans[1:]) if 100 <= b - a <= 170]
    return float(np.median(steps)), (float(np.median(rows)) if rows else None), len(steps)


def frames(a):
    """Inner widths/heights of the marked rectangle (sides 140-260 px) and of the lower-right inset (sides > 400 px)."""
    h, w = a.shape
    white = a > 225
    vruns = longest_runs(white.T)  # per column
    hruns = longest_runs(white)    # per row

    def lines(runs, lo, hi, region):
        idx = [i for i, (s, n) in enumerate(runs) if lo <= n <= hi and region(i, s)]
        groups = []
        for i in idx:
            if groups and i - groups[-1][-1] <= 2:
                groups[-1].append(i)
            else:
                groups.append([i])
        return [(g[0], g[-1]) for g in groups]

    rect_v = lines(vruns, 140, 260, lambda x, s: w * 0.3 < x < w * 0.85 and h * 0.25 < s < h * 0.7)
    rect_h = lines(hruns, 140, 260, lambda y, s: h * 0.3 < y < h * 0.75 and w * 0.3 < s < w * 0.85)
    ins_v = lines(vruns, 400, 700, lambda x, s: x > w * 0.5 and s > h * 0.5)
    ins_h = lines(hruns, 400, 700, lambda y, s: y > h * 0.5 and s > w * 0.5)
    inner = lambda pair: pair[1][0] - pair[0][1] - 1
    rw = inner(rect_v[:2])
    # the rectangle's top and bottom: the pair of horizontal lines whose distance fits a 12 x 10 frame
    pairs = [(a, b) for a, b in zip(rect_h, rect_h[1:]) if 0.75 * rw <= inner((a, b)) <= 1.0 * rw]
    assert len(pairs) == 1, rect_h
    return (rw, inner(pairs[0]), inner(ins_v[:2]), inner(ins_h[:2]),
            rect_v[:2], list(pairs[0]), ins_v[:2], ins_h[:2])


def main():
    rows = []
    for fig, page in PAGES.items():
        a = image(page)
        h, w = a.shape
        main_bar = bar(a, 0, w // 4, int(h * 0.9), h, 60, 160, 3)
        inset_bar = bar(a, w // 2, w, int(h * 0.85), h, 150, 260, 8)
        half, rowp, nsteps = outline_pitch(a)
        rw, rh, iw, ih, *boxes = frames(a)
        pitch = 2 * half
        s_bar = main_bar / 10.0           # px/um if the bar is 10 um
        s_pitch = pitch / 12.0            # px/um if the tile pitch is the 12 um beam distance
        mag = iw / rw
        s_inset = inset_bar / 5.0 / mag   # px/um from the inset's 5 um bar
        rows.append({
            "figure": fig, "image_px": f"{w}x{h}", "main_bar_px": main_bar, "inset_bar_px": inset_bar,
            "tile_half_step_px": half, "tile_row_pitch_px": rowp, "n_outline_steps": nsteps,
            "rect_inner_px": f"{rw}x{rh}", "inset_inner_px": f"{iw}x{ih}", "inset_magnification": round(mag, 2),
            "px_per_um_from_10um_bar": round(s_bar, 2), "px_per_um_from_12um_pitch": round(s_pitch, 2),
            "px_per_um_from_inset_bar": round(s_inset, 2),
            "bar_length_um_by_pitch": round(main_bar / s_pitch, 1),
            "bar_length_um_by_inset_bar": round(main_bar / s_inset, 1),
            "image_width_um_by_bar": round(w / s_bar, 0), "image_width_um_by_pitch": round(w / s_pitch, 0),
            "rect_width_um_by_bar": round(rw / s_bar, 1), "inset_width_um_by_inset_bar": round(iw / (inset_bar / 5.0), 1),
            "row_pitch_over_tile_pitch": round(rowp / pitch, 3) if rowp else "",
        })
        print(fig, rows[-1], boxes)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        f.write("# Decompiler's measurement on the embedded images of Figs. 2-5 (eberle2015), NOT data of the paper.\n"
                "# Made by figures/figs2to5_scalebars_extract.py (see its docstring for the method). Lengths in native\n"
                "# image pixels (300 dpi in print); uncertainty about +-2 px per length (JPEG edges, frame thickness).\n"
                "# Assumptions: the mosaic outline steps by half the tile pitch per tile row and the tile pitch equals the\n"
                "# 12 um beam distance given on p. 3; the inset scale bars are 5 um (captions); the inset shows the marked\n"
                "# rectangle (12 um x 10 um per the captions). For Fig. 3 the lower-right inset is used.\n"
                "# Result: the printed '10 um' bars measure about 7-8 um on the other two scales, which agree with each\n"
                "# other and with the ~100 um field width of the text (p. 3) and the Fig. 1 caption.\n")
        wr = csv.DictWriter(f, fieldnames=list(rows[0]))
        wr.writeheader()
        wr.writerows(rows)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
