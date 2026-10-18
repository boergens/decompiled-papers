"""Helpers shared by the song2023 extract scripts (Extended Data figures are 300-ppi raster images).

page_image(p): the embedded image of PDF page p (soft mask applied), via tools/digitize_common.embedded_image.
hue_mask(a, hue_lo, hue_hi, smin, vmin): HSV colour mask (OpenCV hue 0..180).
lin(p0, v0, p1, v1): linear pixel->value map through two points; fit(pix, vals): least squares map + max residual.
Pixel coordinates are those of the embedded image (origin top left).
"""
import os
import sys

import cv2
import numpy as np

sys.path.insert(0, "/home/admin/ephemeral/oct_17_papers/song2023/tools")
from digitize_common import embedded_image, overlay, trace, trace_envelope  # noqa: E402,F401

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(HERE, "../source/41592_2023_Article_1866.pdf")
SRC = os.path.join(HERE, "../source/edmond_RG58DU/extracted/data")
WORK = os.path.join(HERE, "../work")
_cache = {}


def page_image(p):
    if p not in _cache:
        _cache[p] = embedded_image(PDF, p)
    return _cache[p]


def hsv(a):
    return cv2.cvtColor(a, cv2.COLOR_RGB2HSV).astype(int)


def hue_mask(a, hue_lo, hue_hi, smin=80, vmin=60):
    h = hsv(a)
    if hue_lo <= hue_hi:
        m = (h[..., 0] >= hue_lo) & (h[..., 0] <= hue_hi)
    else:  # wraps around red
        m = (h[..., 0] >= hue_lo) | (h[..., 0] <= hue_hi)
    return m & (h[..., 1] >= smin) & (h[..., 2] >= vmin)


def dark_mask(a, vmax=110, chroma=40):
    return (a.max(2) < vmax) & ((a.max(2) - a.min(2)) < chroma)


def fit(pix, vals, log=False):
    pix = np.asarray(pix, float)
    v = np.log10(vals) if log else np.asarray(vals, float)
    A = np.vstack([pix, np.ones_like(pix)]).T
    (m, b), *_ = np.linalg.lstsq(A, v, rcond=None)
    res = float(np.max(np.abs(A @ [m, b] - v)))
    if log:
        return (lambda p: 10 ** (m * np.asarray(p, float) + b)), (lambda q: (np.log10(q) - b) / m), res
    return (lambda p: m * np.asarray(p, float) + b), (lambda q: (np.asarray(q, float) - b) / m), res


def write_csv(path, header, cols, rows):
    import csv
    with open(path, "w", newline="") as f:
        for h in header:
            f.write("# " + h + "\n")
        w = csv.writer(f)
        w.writerow(cols)
        w.writerows(rows)


def read_csv(path):
    import csv
    return list(csv.DictReader(l for l in open(path) if not l.startswith("#")))


def docx_eds_reports(path):
    """Parse an EDAX-style EDS 'Analysis Report' Word file (.doc names, really .docx/zip) into
    [(report_title, kV, livetime, [(element, line, intensity_cps, conc_wt, error_2sig, mdl_3sig), ...])].
    Decimal commas are converted to points. Reads the XML with the standard library only."""
    import re
    import zipfile
    import xml.etree.ElementTree as ET
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    root = ET.fromstring(zipfile.ZipFile(path).read("word/document.xml"))
    body = root.find("w:body", ns)
    out, title, kv, lt = [], None, None, None

    def txt(el):
        return "".join(t.text or "" for t in el.iter("{%s}t" % ns["w"])).strip()

    pending = None
    for el in body:
        tag = el.tag.split("}")[1]
        if tag == "p":
            t = txt(el)
            if t.startswith("Analysis Report:"):
                title = t.split(":", 1)[1].strip()
            m = re.match(r"kV\s*([\d.,]+)", t)
            if m and pending:
                pending[1] = float(m.group(1).replace(",", "."))
            m = re.match(r"Elapsed Livetime\s*([\d.,]+)", t)
            if m and pending:
                pending[2] = float(m.group(1).replace(",", "."))
        elif tag == "tbl":
            rows = []
            for tr in el.findall("w:tr", ns):
                cells = [txt(tc) for tc in tr.findall("w:tc", ns)]
                if cells and re.fullmatch(r"[A-Z][a-z]?", cells[0]):
                    f = lambda s: float(s.replace(",", "."))  # noqa: E731
                    rows.append((cells[0], cells[1], f(cells[2]), f(cells[3]), f(cells[5]), f(cells[6])))
            pending = [title, None, None, rows]
            out.append(pending)
    return [tuple(p) for p in out]


def find_markers(mask, radius, min_area, max_area):
    """Centroids (x, y) of filled markers in a bool mask: morphological opening with a disk of `radius`
    removes plot lines thinner than the disk; the remaining blobs with area in [min_area, max_area] are markers."""
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * radius + 1, 2 * radius + 1))
    op = cv2.morphologyEx(mask.astype(np.uint8), cv2.MORPH_OPEN, k)
    n, lab, stats, cent = cv2.connectedComponentsWithStats(op)
    out = []
    for i in range(1, n):
        if min_area <= stats[i, cv2.CC_STAT_AREA] <= max_area:
            out.append((float(cent[i][0]), float(cent[i][1]), int(stats[i, cv2.CC_STAT_AREA])))
    return sorted(out)


def mat_tables(path, var):
    """Read MATLAB 'table' objects stored in a struct `var` of a v5 .mat file (scipy shows them as MatlabOpaque).

    MATLAB keeps the table contents in the file's __function_workspace__ (MCOS 'FileWrapper__' cell array): after
    two header cells, each object takes 7 cells (data = cell of column vectors, ndims, nrows, rownames, nvars,
    varnames, props), in object-id order. The struct field's opaque value holds its object id (5th uint32).
    Returns {field: {varname: ndarray}}. Plain scipy; no MATLAB code is run.
    """
    import io
    import scipy.io as sio
    from scipy.io.matlab._mio5 import MatFile5Reader
    m = sio.loadmat(path, squeeze_me=True, struct_as_record=False)
    s = m[var]
    ids = {}
    for fn in s._fieldnames:
        o = getattr(s, fn)
        arr = np.ravel(o["arr"][0]) if o["arr"].dtype == object else np.ravel(o["arr"])
        assert bytes(np.ravel(o["s2"])[0]) == b"table", fn
        ids[fn] = int(arr[4])
    raw = sio.loadmat(path, squeeze_me=False, struct_as_record=False)["__function_workspace__"].tobytes()
    hdr = b"MATLAB 5.0 MAT-file".ljust(116, b" ") + b"\x00" * 8 + b"\x00\x01IM"
    r = MatFile5Reader(io.BytesIO(hdr + raw[8:]), struct_as_record=False, squeeze_me=True)
    r.initialize_read()
    r.mat_stream.seek(128)
    h, nxt = r.read_var_header()
    ws = r.read_var_array(h, process=True)
    cells = list(np.ravel(ws.MCOS[0]["arr"]))
    out = {}
    for fn, oid in ids.items():
        blk = cells[2 + 7 * (oid - 1): 2 + 7 * oid]
        data, nrows, names = blk[0], blk[2], blk[5]
        cols = {str(n): np.asarray(c, float) for n, c in zip(np.ravel(names), np.ravel(data))}
        assert all(len(c) == int(nrows) for c in cols.values()), fn
        out[fn] = cols
    return out
