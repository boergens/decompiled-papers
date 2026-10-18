"""Small shared helpers for the microns2025 figure scripts (decompiler's code).

Scripts import it with
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
and use paths relative to the paper folder K = Path(__file__).resolve().parent.parent.
"""
import csv
from pathlib import Path

K = Path(__file__).resolve().parent.parent
PDF = K / "source" / "microns2025.pdf"


def write_csv(path, comments, header, rows):
    """CSV with '#' comment lines first, then one header row, then rows (csv.writer)."""
    path = Path(path)
    with open(path, "w", newline="") as f:
        for c in comments:
            for line in str(c).splitlines():
                f.write("# " + line + "\n")
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print("wrote", path, len(rows), "rows")


def read_csv(path):
    """Rows of a CSV written by write_csv as dicts (comment lines skipped)."""
    with open(path, newline="") as f:
        lines = [l for l in f if not l.startswith("#")]
    return list(csv.DictReader(lines))


def fnum(v):
    return float(v) if v not in ("", None) else float("nan")


class LinAxis:
    """page coordinate -> data value through a least-squares line on (pos, value) pairs; log10 if log=True."""

    def __init__(self, pairs, log=False):
        import numpy as np
        p = np.array([a for a, b in pairs], float)
        v = np.array([b for a, b in pairs], float)
        if log:
            v = np.log10(v)
        self.a, self.b = np.polyfit(p, v, 1)
        self.log = log
        self.resid = v - (self.a * p + self.b)

    def __call__(self, pos):
        import numpy as np
        val = self.a * np.asarray(pos, float) + self.b
        return 10 ** val if self.log else val

    def inv(self, val):
        import numpy as np
        v = np.log10(val) if self.log else np.asarray(val, float)
        return (v - self.b) / self.a

    def describe(self, name):
        import numpy as np
        unit = "log10 units" if self.log else "data units"
        return (f"{name}: value{' (log10)' if self.log else ''} = {self.a:.6g} * page_coord + {self.b:.6g}; "
                f"max |residual| on the ticks {np.max(np.abs(self.resid)):.2g} {unit}")


def overlay_pts(page_index, clip, pts, out_name, dpi=300, color=(0, 200, 0), r=1):
    """QA: render clip (PDF points) of page (0-based) and draw extracted points (PDF points) on it.
    Written to <paper>/work/<out_name>."""
    import numpy as np
    import pymupdf
    from PIL import Image, ImageDraw
    page = pymupdf.open(PDF)[page_index]
    z = dpi / 72
    pix = page.get_pixmap(clip=pymupdf.Rect(*clip), matrix=pymupdf.Matrix(z, z))
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    dr = ImageDraw.Draw(im)
    for x, y in pts:
        u, v = (x - clip[0]) * z, (y - clip[1]) * z
        dr.ellipse((u - r, v - r, u + r, v + r), outline=color)
    im.save(K / "work" / out_name)
    print("overlay ->", K / "work" / out_name)


def dedupe(vals, tol=0.1):
    """Sorted unique positions, merging values closer than tol (tick drawn twice)."""
    out = []
    for v in sorted(vals):
        if out and abs(v - out[-1]) < tol:
            continue
        out.append(v)
    return out


def colorbar_lut(page_no, bbox_near, vertical=True, trim=0):
    """Colour bar embedded image -> (colours Nx3 float, fraction 0..1 from the low end).
    For a vertical bar the low end is the bottom row. Uses digitize_common.embedded_image (soft mask applied)."""
    import numpy as np
    import digitize_common as dc
    a = dc.embedded_image(str(PDF), page_no, bbox_near=bbox_near).astype(float)
    if vertical:
        w = a.shape[1]
        col = a[:, w // 4: max(w // 4 + 1, 3 * w // 4)].mean(1)[::-1]
    else:
        h = a.shape[0]
        col = a[h // 4: max(h // 4 + 1, 3 * h // 4)].mean(0)
    if trim:
        col = col[trim:-trim]
    n = len(col)
    frac = (np.arange(n) + 0.5 + trim) / (n + 2 * trim)
    return col, frac


def nearest_colour(rgb255, cols):
    import numpy as np
    d = np.sqrt(((cols - np.asarray(rgb255, float)) ** 2).sum(1))
    i = int(d.argmin())
    return i, float(d[i])
