"""Classify the pixels of the Abaqus von Mises contour plots of fu2025 (Figs. 10 and 11) into the 12 bands of
their colour keys. Adapted from ~/ephemeral/oct_17_papers/sun2019/tools/fe_contour.py (written for that paper).

The keys use Abaqus' default 12-band rainbow (swatch colours measured in the Fig. 10 key, lossless image):
blue (0,0,255) ... red (255,0,0). The model is drawn with Abaqus' lighting, so a band's colour in the model is its
key colour times 216/255 (the most frequent model colours are (0,0,216), (0,79,216), (0,157,216), (0,216,197),
(0,216,118), (216,0,0); checked in both figures). Each pixel gets the code of the nearest of these model colours if
it is within MAX_DIST (RGB distance), else '.' (white), '#' (anything else: black outlines, knife lines, black
annotation text and arrows, anti-aliased band boundaries) or 'X' (annotation boxes given by the caller: colour
key, panel label, title box).
Band codes, low to high stress: '0','1',...,'9','a','b' (band k lies between key values k and k+1, counted from
the bottom of the key).
"""
import numpy as np

KEY = [(0, 0, 255), (0, 93, 255), (0, 185, 255), (0, 255, 232), (0, 255, 139), (0, 255, 46),
       (46, 255, 0), (139, 255, 0), (232, 255, 0), (255, 185, 0), (255, 93, 0), (255, 0, 0)]
NAMES = ["blue", "mid blue", "light blue", "cyan", "aquamarine", "spring green", "green", "yellow-green",
         "yellow", "orange", "dark orange", "red"]
CODES = "0123456789ab"
SHADE = 216 / 255


def classify(a, annotation_boxes, max_dist=30):
    """a: RGB uint8 panel image. Returns an array of single-character codes."""
    f = a.astype(float)
    ref = [np.array(c, float) * SHADE for c in KEY]
    d = np.stack([np.sqrt(((f - r) ** 2).sum(2)) for r in ref], 0)
    best = d.argmin(0)
    out = np.full(a.shape[:2], "#", dtype="<U1")
    ok = d.min(0) <= max_dist
    out[ok] = np.array(list(CODES))[best[ok]]
    out[np.sqrt(((f - 255) ** 2).sum(2)) <= 20] = "."
    for (c0, r0, c1, r1) in annotation_boxes:
        out[r0:r1, c0:c1] = "X"
    return out


def render(codes):
    """Codes -> RGB image in the key colours (for re-plots and checks)."""
    pal = {CODES[i]: c for i, c in enumerate(KEY)}
    pal.update({".": (255, 255, 255), "X": (235, 235, 235), "#": (0, 0, 0)})
    img = np.zeros(codes.shape + (3,), np.uint8)
    for k, c in pal.items():
        img[codes == k] = c
    return img


def write_grid(path, header_lines, codes):
    import csv
    with open(path, "w", newline="") as f:
        for h in header_lines:
            f.write("# " + h + "\n")
        w = csv.writer(f)
        w.writerow(["row", "codes"])
        for i, row in enumerate(codes):
            w.writerow([i, "".join(row)])


def band_text(key_values):
    """key_values: the 13 printed values, top to bottom. Returns 'code: colour, lo-hi' for the 12 bands."""
    v = list(reversed(key_values))
    return "; ".join(f"{CODES[i]}: {NAMES[i]}, {v[i]}-{v[i + 1]}" for i in range(12))
