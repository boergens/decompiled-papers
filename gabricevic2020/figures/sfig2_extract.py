"""Digitize SI Fig. S2 of Gabričević, Lente & Fábián 2020: stoichiometry of the OsO4 + c-DCE redox reaction.

Source: word/media/image2.tiff in poc4045-sup-0001-supporting_information.docx (893 x 631 px, 220 ppi, lossless
palette TIFF). Main panel: 10 spectra, one colour each, no legend. Inset (upper right): A (345 nm) vs
[cis-DCE]/[Os(VIII)], grey diamonds with a red dotted and an orange dashed straight line.
    python3 -I sfig2_extract.py   -> sfig2main.csv, sfig2inset.csv (+ ../work/sfig2_overlay.png)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spectra_common import extract_si_spectra  # noqa: E402

TITLE = ["Gabričević, Lente & Fábián 2020, Supporting Information Fig. S2: stoichiometry of the redox reaction between OsO4",
         "  and c-DCE; all spectra measured after completion of the reaction (24 h); [Os(VIII)] = 1 mmol/dm3,",
         "  [cDCE] = 0.05-5 mmol/dm3, [NaOH] = 0.10 mol/dm3, I = 0.10 mol/dm3, T = 25 °C (caption). The figure does not",
         "  say which spectrum belongs to which [cDCE]."]
extract_si_spectra("sfig2", dict(
    out="sfig2main",
    title=[TITLE[0] + " Main panel."] + TITLE[1:],
    frame=dict(left=134, right=803, top=63, bottom=536),
    xlabels=[300, 350, 400, 450], ylabels=[1.5, 1.0, 0.5], ybottom=0.0,
    exclude=[(486, 58, 806, 288)],
    specs=[dict(name="black", rgb=(0, 0, 0), seed=(384, 228), tol=40, alpha_min=0.75, max_run=8),
           dict(name="blue", rgb=(0, 0, 255), seed=(384, 365)),
           dict(name="red", rgb=(247, 0, 0), seed=(384, 375)),
           dict(name="dark cyan", rgb=(0, 132, 123), seed=(384, 405), tol=40),
           dict(name="magenta", rgb=(247, 0, 255), seed=(384, 415)),
           dict(name="wine", rgb=(132, 0, 0), seed=(384, 417), tol=40),
           dict(name="olive", rgb=(132, 132, 0), seed=(384, 422), tol=40),
           dict(name="pink", rgb=(247, 0, 123), seed=(300, 363), tol=40),
           dict(name="green", rgb=(0, 132, 0), seed=(384, 425), tol=40),
           dict(name="navy", rgb=(0, 0, 123), seed=(384, 428), tol=30)],
    inset=dict(out="sfig2inset", frame=dict(left=490, right=803, top=63, bottom=283),
               xlabels=[1, 2, 3, 4, 5], ylabels=[1.3, 1.0, 0.7], ybottom=0.4, marker_rgb=(132, 132, 123),
               xname="[cis-DCE]/[Os(VIII)] (x axis title)", yname="A (345 nm) (y axis title)", ycol="A_345",
               title=[TITLE[0] + " Inset: A (345 nm) vs [cis-DCE]/[Os(VIII)]."]),
))
