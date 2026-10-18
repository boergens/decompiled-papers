"""Shared drawing code for the re-plot scripts (each script reads only its own CSV)."""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402,F401

HERE = os.path.dirname(os.path.abspath(__file__))


def read(name):
    with open(os.path.join(HERE, name)) as f:
        return list(csv.DictReader(l for l in f if not l.startswith("#")))


def f(v):
    return float(v) if v not in ("", None) else float("nan")


def draw_lineband(ax, rows, xcol, ycol, lo, hi, colours, dashed=(), order=None):
    names = order or list(dict.fromkeys(r["series"] for r in rows))
    for n in names:
        r = [q for q in rows if q["series"] == n]
        c = colours.get(n, "k")
        b = [q for q in r if q.get(lo) and q.get(hi)]
        if b:
            ax.fill_between([f(q[xcol]) for q in b], [f(q[lo]) for q in b], [f(q[hi]) for q in b], color=c, alpha=0.3, lw=0)
    for n in names:
        r = [q for q in rows if q["series"] == n and q[ycol]]
        c = colours.get(n, "k")
        ax.plot([f(q[xcol]) for q in r], [f(q[ycol]) for q in r], "." if n not in dashed else "s", ms=1.5,
                color=c, label=n)
