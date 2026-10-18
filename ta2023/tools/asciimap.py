"""ASCII colour-class map of an image window: K dark, P purple (blue over red), B blue, R red, G green, '.' other.
Usage: python3 -I -B tools/asciimap.py page xref x0 y0 x1 y1 (embedded-image pixel window)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from figtools import load
import numpy as np
pg, xr, x0, y0, x1, y1 = map(int, sys.argv[1:7])
a = load(pg, xr).astype(int)[y0:y1, x0:x1]
r, g, b = a[..., 0], a[..., 1], a[..., 2]
sat = a.max(2) - a.min(2)
cls = np.full(r.shape, '.', dtype='<U1')
cls[(r > g + 40) & (r > b + 40)] = 'R'
cls[(g > r + 40) & (g > b + 40)] = 'G'
cls[(b > r + 40) & (b > g + 40)] = 'B'
cls[(b > g + 40) & (r > g + 40)] = 'P'
cls[(a.mean(2) < 110) & (sat < 50)] = 'K'
cls[(a.mean(2) < 160) & (a.mean(2) >= 110) & (sat < 30)] = 'k'
print('     ' + ''.join(str((x0 + i) % 10) for i in range(x1 - x0)))
for i, row in enumerate(cls):
    print(f"{y0 + i:4d} " + ''.join(row))
