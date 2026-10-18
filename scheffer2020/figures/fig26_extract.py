"""Fig. 26 (p. 49): Rent's rule plot. Digitize from the embedded raster (1194 x 875 px, JPEG, native resolution).

Tier 3 for the lines and band edges, tier 3/4 for the compartment labels (see below). The authors' Figure 26-source
data 1 is not available locally.
Calibration: the decade tick marks on the frame (found by code): x = 100 ... 1e6 Tbars at columns 108, 372, 636, 900,
1164; y = 1 ... 1e6 neurons at rows 820, 690, 560, 429, 299, 168, 38 (log fits).
- Compartment points: the plot has no markers; each compartment is shown only by its text label (gnuplot-style labels,
  assumed centred on the data point). Labels are located by matching rendered DejaVu Sans text (16 px, the font of the
  figure) against the dark-ink mask, for every region name of Table 1 with '(R)', '(L)' or no suffix (Greek letters
  as the Latin a/b/g the figure prints). A label is accepted where >= 96 % of its rendered ink is dark in the image;
  shorter names inside an accepted longer label are dropped. The label centre is taken as the data point.
  Isolated labels: about +-2 px (+-0.01 decade). Labels in the two crowded clusters overlap other labels: their
  identity rests on the template match only (status 'overlapping'), positions about +-3 px.
- Lines and bands: the green line (upper bound), the blue line (lower bound), and the four edges of the grey bands
  (light grey = 3D packing only, mid grey = 3D and 2D overlap, olive grey = 2D packing only), each traced per column
  from the colour classes and fitted as a straight line in log-log space (N = c * T^p); fit parameters in the header.
Writes figures/fig26.csv and work/fig26_overlay.png.
"""
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import fc_dig as fd  # noqa: E402

a = fd.embedded(49)
fx, rx = fd.fit([108, 372, 636, 900, 1164], [1e2, 1e3, 1e4, 1e5, 1e6], log=True)
fy, ry = fd.fit([820, 690, 560, 429, 299, 168, 38], [1, 10, 1e2, 1e3, 1e4, 1e5, 1e6], log=True)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
ink = (a.astype(int).max(axis=2) < 150).astype(np.float32)
ink180 = (a.astype(int).max(axis=2) < 180).astype(np.float32)   # looser mask, used only for LOWER below
ink[:, :109] = 0; ink[:, 1164:] = 0; ink[:39] = 0; ink[820:] = 0

CODES = ["LH", "ME", "AME", "SLP", "LO", "LOP", "SIP", "SMP", "CA", "CRE", "RUB", "ROB", "SCL", "PED", "ICL", "IB", "ATL",
         "AL", "aL", "a'L", "VES", "EPA", "GOR", "SPS", "IPS", "gL", "bL", "b'L", "SAD", "AMMC", "FLA", "CAN", "PRW", "GNG",
         "BU", "LAL", "GA", "AOTU", "AVLP", "PVLP", "PLP", "WED", "FB", "EB", "PB", "NO", "AB", "MB", "OL", "LX", "INP",
         "SNP", "VLNP", "VMNP", "PENP", "CX", "AOT", "GC", "GF", "POC", "mALT"]
CANDS = [c + s for c in CODES for s in ("(R)", "(L)", "")]


def tmpl(text, size):
    f = ImageFont.truetype(FONT, size)
    l, t, r, b = f.getbbox(text)
    im = Image.new("L", (r - l + 4, b - t + 4), 0)
    ImageDraw.Draw(im).text((2 - l, 2 - t), text, fill=255, font=f)
    return (np.asarray(im) > 100).astype(np.float32)


hits = []
for c in CANDS:
    best = None
    for size in (15.75, 16.0):
        T = tmpl(c, size)
        cc = cv2.matchTemplate(ink, T, cv2.TM_CCORR) / T.sum()
        ys, xs = np.where((cc >= 0.96) & (cc == cv2.dilate(cc, np.ones((9, 9), np.uint8))))
        for x, y in zip(xs, ys):
            hits.append(dict(label=c, x0=x, y0=y, x1=x + T.shape[1], y1=y + T.shape[0], score=float(cc[y, x]), size=size))
# merge duplicates of the same label (two sizes / neighbouring peaks)
uniq = []
for h in sorted(hits, key=lambda h: -h["score"]):
    if any(u["label"] == h["label"] and abs(u["x0"] - h["x0"]) < 6 and abs(u["y0"] - h["y0"]) < 6 for u in uniq):
        continue
    uniq.append(h)
# drop a label lying inside a longer accepted label that ends with it or starts with it (e.g. 'LP(R)' in 'PLP(R)', 'FB' in ...)
keep = []
for h in uniq:
    inside = [u for u in uniq if u is not h and len(u["label"]) > len(h["label"]) and h["label"] in u["label"]
              and h["x0"] >= u["x0"] - 3 and h["x1"] <= u["x1"] + 3 and abs(h["y0"] - u["y0"]) <= 3]
    if not inside:
        keep.append(h)
# a bare name whose '(R)'/'(L)' form was also found at the same place is part of it
keep = [h for h in keep if not any(u is not h and u["label"].startswith(h["label"] + "(") and abs(u["x0"] - h["x0"]) <= 3
                                   and abs(u["y0"] - h["y0"]) <= 3 for u in keep)]
# Manual curation after looking at the overlay (work/fig26_overlay.png) and 6x zooms of the crowded clusters:
# false matches made of letters of overlapping labels are dropped; matches of a label whose '(R)' is hidden by an
# overlapping label are renamed to the printed full label (centre recomputed from the full label's width).
DROP = [("AL", 297, 557), ("AL", 475, 524), ("GC", 732, 401), ("OL", 744, 401), ("LH", 1076, 319), ("SIP(R)", 1084, 320),
        ("PB", 1085, 319), ("ME(R)", 1092, 320)]
RENAME = {"ATL": "ATL(R)", "PLP": "PLP(R)", "PVLP": "PVLP(R)", "AVLP": "AVLP(R)"}
UNCERTAIN = {"ATL(L)", "IB"}            # partly hidden; identity not certain
# clearly printed but missed at 0.96 (JPEG blur, light anti-aliasing): searched again inside the box where they are printed,
# on a looser ink mask (< 180) and with a lower threshold
LOWER = {"EB": (0.85, (920, 450, 1000, 500)), "AOTU(R)": (0.85, (840, 415, 960, 455))}


def near(h, lab, x, y):
    return h["label"] == lab and abs((h["x0"] + h["x1"]) / 2 - x) < 4 and abs((h["y0"] + h["y1"]) / 2 - y) < 4


keep = [h for h in keep if not any(near(h, *d) for d in DROP)]
for h in keep:
    if h["label"] in RENAME:
        w = tmpl(RENAME[h["label"]], h["size"]).shape[1]
        h["label"], h["x1"], h["note"] = RENAME[h["label"]], h["x0"] + w, "renamed: '(R)' hidden by an overlapping label"
for lab, (thr, (bx0, by0, bx1, by1)) in LOWER.items():
    if any(h["label"] == lab for h in keep):
        continue
    T = tmpl(lab, 16.0)
    cc = cv2.matchTemplate(ink180[by0:by1, bx0:bx1], T, cv2.TM_CCORR) / T.sum()
    y, x = np.unravel_index(np.argmax(cc), cc.shape)
    cc = cc[y:y + 1, x:x + 1]; y0_, x0_ = y, x; y, x = 0, 0
    x, y = bx0 + x0_, by0 + y0_
    cc = {(y, x): float(cc[0, 0])}
    if cc[(y, x)] >= thr:
        keep.append(dict(label=lab, x0=x, y0=y, x1=x + T.shape[1], y1=y + T.shape[0], score=cc[(y, x)], size=16.0,
                         note=f"found with threshold {thr}"))
rows = []
boxes = [(h["x0"], h["y0"], h["x1"], h["y1"]) for h in keep]
for h in sorted(keep, key=lambda h: (h["x0"] + h["x1"]) / 2):
    cx, cy = (h["x0"] + h["x1"]) / 2, (h["y0"] + h["y1"]) / 2
    ov = sum(1 for b in boxes if b != (h["x0"], h["y0"], h["x1"], h["y1"]) and b[0] < h["x1"] and b[2] > h["x0"]
             and b[1] < h["y1"] and b[3] > h["y0"])
    st = "uncertain" if h["label"] in UNCERTAIN else ("overlapping" if ov else "isolated")
    if h.get("note"):
        st += "; " + h["note"]
    rows.append(["compartment", h["label"], float(fx(cx)), float(fy(cy)), "", "", round(h["score"], 3), st])
    h["cx"], h["cy"] = cx, cy

# ---- lines and bands
cls = {"yellow": (255, 255, 228), "light": (229, 229, 229), "mid": (207, 207, 209), "olive": (229, 229, 206)}


def classify(col):
    d = {k: np.abs(col.astype(int) - np.array(v)).max(axis=1) for k, v in cls.items()}
    out = np.full(len(col), "", dtype=object)
    for k, v in d.items():
        out[v <= 6] = k
    return out


edges = {"3D top (light grey upper edge)": [], "2D top (mid grey upper edge)": [], "3D bottom (mid grey lower edge)": [],
         "2D bottom (olive lower edge)": []}
green = fd.colour_mask(a, (54, 254, 40), 60)
blue = fd.colour_mask(a, (11, 11, 247), 60)
gl, bl = [], []
for x in range(112, 1162, 2):
    c = classify(a[39:820, x])
    idx = {k: np.where(c == k)[0] + 39 for k in ("light", "mid", "olive")}
    if len(idx["light"]) > 3 and len(idx["mid"]) > 3 and len(idx["olive"]) > 3:
        edges["3D top (light grey upper edge)"].append((x, idx["light"].min() - 0.5))
        edges["2D top (mid grey upper edge)"].append((x, idx["mid"].min() - 0.5))
        edges["3D bottom (mid grey lower edge)"].append((x, idx["mid"].max() + 0.5))
        edges["2D bottom (olive lower edge)"].append((x, idx["olive"].max() + 0.5))
    g = np.where(green[39:820, x])[0]
    if len(g):
        gl.append((x, 39 + g.mean()))
    b = np.where(blue[700:820, x])[0]
    if len(b):
        bl.append((x, 700 + b.mean()))
fits = {}
for name, pts in list(edges.items()) + [("green line (upper bound)", gl), ("blue line (lower bound)", bl)]:
    p = np.array(pts, float)
    lx, ly = np.log10(fx(p[:, 0])), np.log10(fy(p[:, 1]))
    keep_m = np.ones(len(p), bool)
    for _ in range(3):                                   # refit without outliers (labels and arrows on the band edges)
        k, c0 = np.polyfit(lx[keep_m], ly[keep_m], 1)
        res = np.abs(ly - (k * lx + c0))
        keep_m = res < max(0.01, 3 * np.median(res))
    fits[name] = (k, c0, int(keep_m.sum()))
    for (x, y), ok in zip(pts, keep_m):
        if ok:
            rows.append(["line", name, float(fx(x)), float(fy(y)), "", "", "", "trace"])
fit_lines = [f"{n}: log10 N = {c0:.4f} + {k:.4f} log10 T (fit on {m} columns, outliers removed), i.e. N = {10 ** c0:.4g} * T^{k:.3f}"
             for n, (k, c0, m) in fits.items()]
for n, (k, c0, m) in fits.items():
    rows.append(["line_fit", n, "", "", round(k, 4), round(10 ** c0, 4), "", f"N = c * T^p on {m} columns"])
fd.write_csv(HERE / "fig26.csv", [
    "Fig. 26 of Scheffer et al. 2020 (eLife 9:e57443), p. 49: 'Rent's rule for hemibrain'.",
    "x = Tbars (log axis, 100 to 1e6); y = Neurons shared with other compartments (log axis, 1 to 1e6).",
    "Provenance: tier 3 (digitized from the embedded 1194 x 875 px JPEG raster); compartment positions in the crowded clusters are",
    "less certain (status overlapping). The authors' Figure 26-source data 1 was not available locally.",
    f"Calibration: decade tick marks on the frame (max residual x {rx:.4f}, y {ry:.4f} decades).",
    "kind compartment: label = compartment name as printed (a/b/g = alpha/beta/gamma, as in the figure); x, y = centre of the printed",
    "label (taken as the data point); score = fraction of the rendered label's ink found dark in the image; status isolated/overlapping/",
    "uncertain (identity not certain: partly hidden), with notes for renamed or low-threshold matches (curation listed in the script).",
    "Labels that could not be matched (illegible in the crowded clusters) are missing; see figures/fig26_extract.py for the candidate list.",
    "kind line: traced points of the bound lines and band edges (every 2nd column, outliers removed); kind line_fit: p = exponent, c = prefactor.",
    *fit_lines,
    "The blue reference labels (30x30, 100x100, 300x300 on the green line; ST7LUS5, LPC1102, STM32 near the bottom) are annotations with arrows,",
    "not plotted points, and are described in the alttext only.",
    "Columns: kind, label, x, y, p, c, score, status."], ["kind", "label", "x", "y", "p", "c", "score", "status"], rows)
pts = {"labels": [(h["cx"], h["cy"]) for h in keep]}
for n, pp in list(edges.items()):
    pts[n] = pp[::6]
pts["green"] = gl[::6]; pts["blue"] = bl[::6]
fd.overlay(a, pts, HERE.parent / "work" / "fig26_overlay.png", r=2)
im = Image.open(HERE.parent / "work" / "fig26_overlay.png"); d = ImageDraw.Draw(im)
for h in keep:
    d.rectangle([h["x0"], h["y0"], h["x1"], h["y1"]], outline=(255, 0, 0))
im.save(HERE.parent / "work" / "fig26_overlay.png")
print(len(keep), "labels:", sorted(h["label"] for h in keep))
print("\n".join(fit_lines))
