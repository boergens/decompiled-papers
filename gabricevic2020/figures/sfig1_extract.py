"""Digitize SI Fig. S1 of Gabričević, Lente & Fábián 2020: spectral change of OsO4 with t-DCE (t = 10 s top, 5 h bottom).

Source: word/media/image1.tiff in poc4045-sup-0001-supporting_information.docx (893 x 631 px, 220 ppi, lossless
palette TIFF). Two lines: red (top) and blue (bottom); a thin black arrow (not data) points from the red to the blue peak.
    python3 -I sfig1_extract.py   -> sfig1.csv (+ ../work/sfig1_overlay.png)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spectra_common import extract_si_spectra  # noqa: E402

extract_si_spectra("sfig1", dict(
    out="sfig1",
    title=["Gabričević, Lente & Fábián 2020, Supporting Information Fig. S1: spectral change of OsO4 with t-DCE reaction;",
           "  per the caption the top spectrum is t = 10 s and the bottom one t = 5 h ([Os(VIII)] = 0.75 mmol/dm3,",
           "  [t-DCE] = 8 mmol/dm3, [NaOH] = 0.1 mol/dm3, I = 0.1 mol/dm3, T = 25 °C). Here: red = top, blue = bottom."],
    frame=dict(left=134, right=803, top=63, bottom=536),
    xlabels=[300, 350, 400, 450, 500], ylabels=[1.5, 1.0, 0.5], ybottom=0.0,
    specs=[dict(name="red", rgb=(247, 0, 0), seed=(300, 181), max_run=20),
           dict(name="blue", rgb=(0, 0, 255), seed=(300, 397), max_run=20)],
))
