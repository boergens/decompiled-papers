"""Build the digit templates for sdlayout.read_label from tick labels whose text was read by eye
(Figure 1—source data 1, p.1 and Figure 1—source data 2, p.1). Writes sd_templates.npz."""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sd_extract import page_images  # noqa: E402
from sdlayout import boxes, ticks, label_crop, glyphs, glyph_vec  # noqa: E402

def labels_known(a, known):
    out = []
    for kind, pos_fn, texts in known:
        for crop, text in zip(pos_fn(a), texts):
            gs = [g for g in glyphs(crop)]
            H = max(g[3] - g[2] for g in gs)
            digits = [g for g in gs if not (g[3] - g[2] < 0.35 * H and g[1] - g[0] < 0.5 * H)]
            t = text.replace(".", "")
            assert len(digits) == len(t), (text, len(digits))
            out += [(ch, glyph_vec(g, H)) for ch, g in zip(t, digits)]
    return out

T = {}
pages = dict(page_images("fig1-data1"))
a = pages[1]
bx = boxes(a)
b1 = sorted([b for b in bx if b[0] == 109], key=lambda q: q[2])[1]       # x=400 μm plot
mp = [b for b in bx if b[3] - b[2] >= 312][0]                           # data map
ys, xs = ticks(a, b1); mys, mxs = ticks(a, mp)
known = [
    ("y", lambda a: [label_crop(a, b1, "y", y) for y in ys], ["0.9", "0.8", "0.7", "0.6", "0.5"]),
    ("x", lambda a: [label_crop(a, b1, "x", x) for x in xs], ["500", "1000"]),
    ("my", lambda a: [label_crop(a, mp, "y", y) for y in mys] + [label_crop(a, mp, "y", mp[0])], ["800", "400", "1200"]),
    ("mx", lambda a: [label_crop(a, mp, "x", x) for x in mxs] + [label_crop(a, mp, "x", mp[3])], ["400", "800", "1200"]),
]
assert len(ys) == 5 and len(xs) == 2, (ys, xs)
for ch, v in labels_known(a, known):
    T.setdefault(ch, []).append(v)
a = dict(page_images("fig1-data2"))[1]
b = sorted([b for b in boxes(a) if b[0] == 109], key=lambda q: q[2])[0]
ys, xs = ticks(a, b)
assert len(ys) == 3, ys
for ch, v in labels_known(a, [("y", lambda a: [label_crop(a, b, "y", y) for y in ys], ["1.5", "1", "0.5"])]):
    T.setdefault(ch, []).append(v)
print({k: len(v) for k, v in sorted(T.items())})
np.savez(os.path.join(HERE, "sd_templates.npz"), **{k: np.array(v) for k, v in T.items()})
