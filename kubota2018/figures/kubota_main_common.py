"""Shared helpers for digitizing the raster plots of the kubota2018 main article (Figs. 1, 4, 6).

The plots are embedded 300 ppi raster images that contain the axis lines, tick marks and data;
the tick labels are PDF text placed over them. So the calibration is:
  1. find the tick marks in the image (tools/digitize_common.tick_positions[_v]);
  2. convert the centre of each numeric tick label (PDF points) into image pixels through the
     image's placement bbox on the page;
  3. pair each label with the nearest tick mark and fit a linear pixel -> value map on the
     tick-mark pixel positions (not on the label positions).
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../tools"))
import numpy as np  # noqa: E402
import pymupdf  # noqa: E402
from digitize_common import embedded_image, fit_axis  # noqa: E402

PDF = os.path.join(HERE, "../source/s41467-017-02768-7.pdf")
WORK = os.path.join(HERE, "../work")


class Img:
    """An embedded image with its placement on the page (for pixel <-> PDF point conversion)."""

    def __init__(self, page, bbox_near):
        self.page = page
        self.a = embedded_image(PDF, page, bbox_near=bbox_near)
        doc = pymupdf.open(PDF)
        infos = doc[page - 1].get_image_info()
        info = min(infos, key=lambda i: sum(abs(p - q) for p, q in zip(i["bbox"], bbox_near)))
        self.bbox = info["bbox"]
        h, w = self.a.shape[:2]
        self.sx = (self.bbox[2] - self.bbox[0]) / w   # points per pixel
        self.sy = (self.bbox[3] - self.bbox[1]) / h
        self.g = self.a.astype(float).mean(2)

    def pt2px(self, x, y):
        return (x - self.bbox[0]) / self.sx, (y - self.bbox[1]) / self.sy

    def labels(self, clip, pattern=r"^[–\-−]?\d+(\.\d+)?°?$"):
        """Numeric text tokens inside clip (PDF points): list of (value, cx_px, cy_px, text).

        Spans are split into whitespace-separated tokens at character level (rawdict), because some
        tick-label rows ("120 160 200 240", "–10 1 2 3") are single PDF text spans.
        """
        doc = pymupdf.open(PDF)
        out = []
        for b in doc[self.page - 1].get_text("rawdict", clip=pymupdf.Rect(*clip))["blocks"]:
            for line in b.get("lines", []):
                for s in line["spans"]:
                    toks, cur = [], []
                    for ch in s["chars"]:
                        if ch["c"].isspace():
                            if cur:
                                toks.append(cur)
                            cur = []
                        else:
                            cur.append(ch)
                    if cur:
                        toks.append(cur)
                    for tok in toks:
                        t = "".join(ch["c"] for ch in tok)
                        if not re.match(pattern, t):
                            continue
                        x0 = min(ch["bbox"][0] for ch in tok)
                        x1 = max(ch["bbox"][2] for ch in tok)
                        y0 = min(ch["bbox"][1] for ch in tok)
                        y1 = max(ch["bbox"][3] for ch in tok)
                        cx, cy = self.pt2px((x0 + x1) / 2, (y0 + y1) / 2)
                        v = float(t.replace("–", "-").replace("−", "-").rstrip("°"))
                        out.append((v, cx, cy, t))
        return out


def match(ticks, labels, coord, tol=6.0):
    """Pair each label (value, cx, cy) with the nearest tick (pixel); coord 1 = use cx, 2 = cy."""
    pix, val = [], []
    for lab in labels:
        c = lab[coord]
        t = min(ticks, key=lambda q: abs(q - c))
        if abs(t - c) <= tol:
            pix.append(t)
            val.append(lab[0])
    return pix, val


def calib(ticks, labels, coord, tol=6.0):
    pix, val = match(ticks, labels, coord, tol)
    assert len(pix) >= 2, (ticks, labels)
    f, res, slope = fit_axis(pix, val)
    return f, res, slope, pix, val


def blobs(mask, min_area):
    """Connected components of mask: list of (cx, cy, area, (x0, y0, x1, y1))."""
    import cv2
    n, lab, st, cen = cv2.connectedComponentsWithStats(mask.astype(np.uint8), 8)
    out = []
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] >= min_area:
            x, y, w, h = st[i, :4]
            out.append((cen[i][0], cen[i][1], int(st[i, cv2.CC_STAT_AREA]), (x, y, x + w, y + h)))
    return out


def opened(mask, r):
    """Morphological opening with a disk of radius r (removes lines thinner than ~2r)."""
    import cv2
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
    return cv2.morphologyEx(mask.astype(np.uint8), cv2.MORPH_OPEN, k).astype(bool)


def read_csv(path):
    import csv
    with open(path) as f:
        return list(csv.DictReader(line for line in f if not line.startswith("#")))


def trace_three_series(im, x0, x1, axis_rows, hw=2, exclude=()):
    """Trace the red (CNT-PET), blue (Kapton) and black (cc-Kapton) ~5 px lines of a Fig. 4 spectrum panel.

    Returns {series: [(col, y_mid, y_upper, y_lower, flag)]} in pixel units, and the masks' overlay points.
    exclude: rectangles (c0, r0, c1, r1) in pixels to blank (legend). Black pixels merged with the
    x-axis line get centre = top edge + hw.
    """
    from digitize_common import trace_envelope
    a = im.a.astype(int)
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    k = (im.g < 110) & (np.ptp(a, axis=2) < 60)
    masks = {"CNT-PET": (R > 150) & (G < 110) & (B < 110),
             "Kapton": (B > 150) & (R < 120) & (G < 170),
             "cc-Kapton": k.copy()}
    masks["cc-Kapton"][axis_rows[0]:, :] = False
    out, pts = {}, []
    for name, m in masks.items():
        m[:, :x0] = False
        for c0, r0, c1, r1 in exclude:
            m[r0:r1, c0:c1] = False
        res = []
        for c, ym, yu, yl in trace_envelope(m, x0, x1, 0, axis_rows[1] + 3, hw, min_px=2):
            if ym != ym:
                continue
            flag = ""
            col = np.where(m[:axis_rows[1] + 3, int(c)])[0]
            if name == "cc-Kapton" and col.max() >= axis_rows[0] - 1:
                ym = yu = yl = col.min() + hw
                flag = "touches the axis line; centre = top edge + half width"
            res.append((c, ym, yu, yl, flag))
            pts += [(c, yu), (c, yl)]
        if name == "cc-Kapton":
            # where the black line lies on the x-axis line (value ~0) it only shows as a thickened axis
            # line (dark one row above and below it); give those columns the axis-line centre
            done = {int(r[0]) for r in res}
            yc = (axis_rows[0] + axis_rows[1]) / 2
            for c in range(x0, x1):
                if c not in done and k[axis_rows[0] - 1, c] and k[axis_rows[1] + 1, c] and not k[axis_rows[0] - 3, c]:
                    res.append((float(c), yc, yc - 1, yc + 1, "on the x-axis line (thickened axis), value ~0"))
                    pts.append((c, yc))
            res.sort(key=lambda r: r[0])
        out[name] = res
    return out, pts
