#!/usr/bin/env python3
"""Put the original panel and the re-plot side by side, to check a re-plot by eye.

Usage:
    python3 -I compare.py <original.png> <replot.png> <out.png>

Both are scaled to the same height. Look at the result with the Read tool and
check every series, axis range, tick and log/linear scale against the original.
"""
import sys

from PIL import Image

if len(sys.argv) != 4:
    sys.exit(__doc__)
a = Image.open(sys.argv[1]).convert("RGB")
b = Image.open(sys.argv[2]).convert("RGB")
h = max(400, min(1000, max(a.height, b.height)))
a = a.resize((max(1, a.width * h // a.height), h))
b = b.resize((max(1, b.width * h // b.height), h))
out = Image.new("RGB", (a.width + b.width + 20, h), "white")
out.paste(a, (0, 0))
out.paste(b, (a.width + 20, 0))
out.save(sys.argv[3])
print(sys.argv[3])
