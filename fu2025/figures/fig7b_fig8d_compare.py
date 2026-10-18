"""Check: are the curves of Figure 7b (simulated, plain PMMA) the same as those of Figure 8d (simulated,
PMMA/1.0 wt% CNTs)? Compares the digitized CSVs of Fig. 7b with Fig. 8a-d, series by series: median force per
5 µs time bin, then the median absolute difference over the bins both have. Prints one line per panel.
    python3 -I fig7b_fig8d_compare.py
"""
from pathlib import Path
HERE = Path(__file__).resolve().parent
import csv
import numpy as np
def load(p):
    d={}
    for r in csv.DictReader(l for l in open(HERE / p) if not l.startswith('#')):
        d.setdefault(r['series'],[]).append((float(r['time_us']),float(r['force_N_per_m'])))
    return d
def binned(pts, edges):
    t,y=map(np.array,zip(*pts)); out=[]
    for a,b in zip(edges[:-1],edges[1:]):
        s=y[(t>=a)&(t<b)]; out.append(np.median(s) if len(s) else np.nan)
    return np.array(out)
edges=np.arange(0,790,5)
A=load('fig7b.csv')
for k in 'abcd':
    B=load(f'fig8{k}.csv'); res=[]
    for s in A:
        x=binned(A[s],edges); y=binned(B[s],edges); ok=~np.isnan(x)&~np.isnan(y)
        res.append(f"{s.split()[-1]}: med|d|={np.median(np.abs(x[ok]-y[ok])):.2f} n={ok.sum()}")
    print('7b vs 8'+k, '; '.join(res))
