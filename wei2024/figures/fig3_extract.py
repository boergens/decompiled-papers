"""Fig. 3 (a-h): digitize the 9-6 LJ (blue) and 12-6 LJ (Fitting) (orange) curves of all eight panels.

Tier 3 (digitized). Source: the embedded 300 ppi JPEG of Fig. 3 on PDF page 6 (xref 94, 2004 x 1739 px).
Excel charts: light-grey gridlines at r = 0, 3, ..., 15 A and E = -0.1, 0, ..., 0.5 kcal/mol give the
calibration (all gridlines found in the image, linear least-squares fit). Each series is a ~4 px line with
~10 px round markers; markers overlap into a band where the curve is flat.
Output per panel: figures/fig3<p>.csv with
  kind=line   : centre line of the series (skeleton of the line-and-marker band, every skeleton pixel);
  kind=marker : centres of markers that stand apart (only on the steep wall; elsewhere they merge).
Writes overlays to work/fig3<p>_overlay.png.
"""
import csv
import sys
from pathlib import Path

import numpy as np
from scipy import ndimage as ndi

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import digitize_common as dc  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PDF = ROOT / "source" / "wei2024.pdf"
WORK = ROOT / "work"
WORK.mkdir(exist_ok=True)

# rough panel boxes (x0, y0, x1, y1) in image pixels enclosing each plot area; gridlines are searched inside
PANELS = {
    "a": (95, 40, 640, 440), "b": (775, 40, 1320, 440), "c": (1455, 40, 2004, 440),
    "d": (95, 640, 640, 1035), "e": (775, 640, 1320, 1035), "f": (1455, 640, 2004, 1035),
    "g": (325, 1245, 870, 1640), "h": (1025, 1245, 1570, 1640),
}
XT = [0, 3, 6, 9, 12, 15]
YT = [0.5, 0.4, 0.3, 0.2, 0.1, 0.0, -0.1]


def groups(idx):
    out = []
    for i in idx:
        if out and i <= out[-1][-1] + 1:
            out[-1].append(i)
        else:
            out.append([i])
    return [float(np.mean(g)) for g in out]


def series_masks(a):
    r, g, b = (a[..., i].astype(int) for i in range(3))
    blue = (b > 170) & (b - r > 50) & (g > 110)
    orange = (r > 190) & (r - b > 90) & (g > 70) & (g < 190)
    return blue, orange


def centre_line(mask, x0, x1, y0, y1):
    """Centre line of a thick curve: Zhang-Suen thinning (OpenCV) of the closed colour mask; returns skeleton pixels."""
    import cv2
    m = mask[y0:y1, x0:x1].astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    lab, n = ndi.label(m)
    if n:
        sizes = ndi.sum(m, lab, range(1, n + 1))
        m = np.isin(lab, 1 + np.where(sizes >= 15)[0]).astype(np.uint8)
    sk = cv2.ximgproc.thinning(m * 255, thinningType=cv2.ximgproc.THINNING_ZHANGSUEN) > 0
    yy, xx = np.where(sk)
    return [(x0 + x, y0 + y) for x, y in zip(xx, yy)]


def centre_line_old(mask, x0, x1, y0, y1, steep_len=9):
    pts = []
    steep_rows = set()
    prev = None
    for c in range(x0, x1):
        rr = np.where(mask[y0:y1, c])[0]
        if len(rr) == 0:
            prev = None
            continue
        runs = np.split(rr, np.where(np.diff(rr) > 2)[0] + 1)
        for run in runs:
            if len(run) > steep_len:
                steep_rows.update(range(y0 + run[0], y0 + run[-1] + 1))
            else:
                pts.append((c, y0 + run.mean()))
    for r in sorted(steep_rows):
        cc = np.where(mask[r, x0:x1])[0]
        if len(cc) == 0:
            continue
        runs = np.split(cc, np.where(np.diff(cc) > 2)[0] + 1)
        for run in runs:
            if len(run) <= steep_len + 4:
                pts.append((x0 + run.mean(), r))
    # drop column points that belong to a steep wall (already sampled by rows)
    return pts


def markers(mask, x0, x1, y0, y1):
    m = mask[y0:y1, x0:x1]
    dt = ndi.distance_transform_edt(m)
    core = dt >= 3.5
    lab, n = ndi.label(core)
    out = []
    for i, sl in enumerate(ndi.find_objects(lab), 1):
        h = sl[0].stop - sl[0].start
        w = sl[1].stop - sl[1].start
        if h > 6 or w > 6:      # merged band, not a single marker
            continue
        yy, xx = np.where(lab[sl] == i)
        out.append((x0 + sl[1].start + xx.mean(), y0 + sl[0].start + yy.mean()))
    return out


def main():
    a = dc.embedded_image(str(PDF), 6)
    gm = a.astype(int)
    grey = (np.abs(gm[..., 0] - gm[..., 1]) < 10) & (np.abs(gm[..., 1] - gm[..., 2]) < 10) & (gm[..., 0] > 150) & (gm[..., 0] < 235)
    blue, orange = series_masks(a)
    report = []
    for p, (bx0, by0, bx1, by1) in PANELS.items():
        sub = grey[by0:by1, bx0:bx1]
        cols = groups(np.where(sub.sum(0) > 0.35 * (by1 - by0))[0])
        rows = groups(np.where(sub.sum(1) > 0.35 * (bx1 - bx0))[0])
        cols = [bx0 + c for c in cols]
        rows = [by0 + r for r in rows]
        assert len(cols) == 6 and len(rows) == 7, (p, cols, rows)
        fx, rx, _ = dc.fit_axis(cols, XT)
        fy, ry, _ = dc.fit_axis(rows, YT)
        px0, px1 = int(round(cols[0])) + 2, int(round(cols[-1]))
        py0, py1 = int(round(rows[0])) - 1, int(round(rows[-1])) + 1
        out_rows, ov = [], []
        for name, m in (("9-6 LJ", blue), ("12-6 LJ (Fitting)", orange)):
            line = centre_line(m, px0, px1, py0, py1)
            mk = markers(m, px0, px1, py0, py1)
            # markers right of the curve minimum are fragments of the merged band (blue partly hidden by orange)
            xmin = max(line, key=lambda q: q[1])[0] if line else 1e9
            mk = [q for q in mk if q[0] <= xmin]
            for kind, pts in (("line", line), ("marker", mk)):
                pts = sorted(pts)
                for x, y in pts:
                    flag = "clipped_at_top" if y <= rows[0] + 3 else ""
                    out_rows.append([name, kind, round(float(fx(x)), 4), round(float(fy(y)), 5), flag])
                    ov.append((x, y))
        hdr = [
            f"Fig. 3{p}: van der Waals potential energy E of C-C atom pairs vs distance r; panel title '{['1.6','2.0','2.6','2.8','3.0','3.2','3.3','3.4'][list(PANELS).index(p)]} ~ 12.5 A' (fitting distance interval)",
            "series: '9-6 LJ' (blue, original 9-6 LJ potential) and '12-6 LJ (Fitting)' (orange, fitted 12-6 LJ potential), legend names as printed",
            "kind: line = centre of the drawn line (skeleton pixels of the line-and-marker band, OpenCV Zhang-Suen thinning; several points per column where the curve is steep); marker = centre of an isolated round marker (data point), only left of the curve minimum; markers merge into a band where the curve is flat and are not listed there",
            "r_A: distance r in angstrom; E_kcal_per_mol: energy in kcal/mol",
            "provenance: tier 3, digitized from the embedded 300 ppi JPEG (PDF p. 6, xref 94) by colour masks; figures/fig3_extract.py",
            f"calibration: linear fit on the 6 vertical gridlines r = 0,3,...,15 (max residual {rx:.3g} A) and 7 horizontal gridlines E = -0.1...0.5 (max residual {ry:.3g} kcal/mol)",
            f"uncertainty: about +-{abs(fx(1)-fx(0)):.3f} A and +-{abs(fy(1)-fy(0)):.4f} kcal/mol per pixel; line points +-2 px (line half width), markers +-1 px",
            "flag clipped_at_top: the curve leaves the plot at the top frame E = 0.5 (the chart clips it); values there are not the curve's maximum",
            "the orange series is drawn over the blue one: where the curves coincide the blue line is hidden and has no points (gaps in 9-6 LJ)",
            "odd (decompiler's check): the 9-6 LJ curve, the same potential in every panel, sits at larger r in panels b-h than in a, by about (interval start - 1.6 A): E = 0.2 kcal/mol at r = 3.2, 3.6, -, 4.4, 4.6, 4.8, 4.8, 5.0 A in a-h. Panel a agrees with Table 1's 9-6 parameters of atom type c (eps 0.054 kcal/mol, sigma 4.01 A: E(3.1 A) = 0.336, minimum -0.054 at 4.01 A); the r values are given as plotted, not corrected",
        ]
        path = HERE / f"fig3{p}.csv"
        with open(path, "w", newline="") as f:
            for h in hdr:
                f.write("# " + h + "\n")
            w = csv.writer(f)
            w.writerow(["series", "kind", "r_A", "E_kcal_per_mol", "flag"])
            w.writerows(out_rows)
        crop = a[by0 - 10:by1 + 10, bx0:bx1]
        dc.overlay(crop, [(x - bx0, y - by0 + 10) for x, y in ov], str(WORK / f"fig3{p}_overlay.png"), colour=(0, 0, 0))
        report.append((p, len(out_rows), rx, ry))
    for r in report:
        print(*r)


if __name__ == "__main__":
    main()
