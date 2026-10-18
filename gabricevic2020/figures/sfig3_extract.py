"""Digitize SI Fig. S3 of Gabričević, Lente & Fábián 2020: stoichiometry of the OsO4 + t-DCE redox reaction.

Source: word/media/image3.tiff in poc4045-sup-0001-supporting_information.docx (893 x 631 px, 220 ppi, lossless
palette TIFF). Main panel: 11 spectra, one colour each, no legend. Inset (upper right): y axis title 'A (nm)' (sic,
no wavelength given) vs [trans-DCE]/[Os(VIII)], grey diamonds with a red dotted and an orange dashed straight line.
    python3 -I sfig3_extract.py   -> sfig3main.csv, sfig3inset.csv (+ ../work/sfig3_overlay.png)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spectra_common import extract_si_spectra  # noqa: E402

TITLE = ["Gabričević, Lente & Fábián 2020, Supporting Information Fig. S3: stoichiometry of the redox reaction between OsO4",
         "  and t-DCE; all spectra measured after completion of the reaction (24 h); [Os(VIII)] = 1 mM,",
         "  [t-DCE] = 0.05-5 mmol/dm3, [NaOH] = 0.10 mol/dm3, I = 0.1 mol/dm3, T = 25 °C (caption). The figure does not",
         "  say which spectrum belongs to which [t-DCE]."]
extract_si_spectra("sfig3", dict(
    out="sfig3main",
    title=[TITLE[0] + " Main panel."] + TITLE[1:],
    frame=dict(left=134, right=803, top=63, bottom=536),
    xlabels=[300, 350, 400, 450], ylabels=[1.5, 1.0, 0.5], ybottom=0.0,
    exclude=[(380, 58, 806, 342)],   # inset frame, its tick labels and y title (the x title is black text over coloured lines)
    specs=[dict(name="royal blue", rgb=(0, 0, 165), seed=(320, 316), tol=20),
           dict(name="green", rgb=(0, 132, 0), seed=(320, 333), tol=40),
           dict(name="pink", rgb=(247, 0, 132), seed=(320, 373), tol=40),
           dict(name="wine", rgb=(132, 0, 0), seed=(320, 388), tol=40),
           dict(name="navy", rgb=(0, 0, 132), seed=(320, 399), tol=20),
           dict(name="olive", rgb=(132, 132, 0), seed=(320, 413), tol=40),
           dict(name="magenta", rgb=(247, 0, 255), seed=(320, 420)),
           dict(name="dark cyan", rgb=(0, 132, 132), seed=(320, 423), tol=40),
           dict(name="blue", rgb=(0, 0, 247), seed=(320, 428), tol=40),
           dict(name="red", rgb=(247, 0, 0), seed=(320, 431), tol=40),
           dict(name="black", rgb=(0, 0, 0), seed=(320, 434), tol=40, alpha_min=0.75, max_run=8)],
    inset=dict(out="sfig3inset", frame=dict(left=446, right=803, top=63, bottom=315),
               xlabels=[1, 2, 3, 4, 5], ylabels=[0.8, 0.6, 0.4], ybottom=None, marker_rgb=(132, 132, 132),
               xname="[trans-DCE]/[Os(VIII)] (x axis title)", yname="A (y axis title 'A (nm)', sic)", ycol="A",
               title=[TITLE[0] + " Inset: y axis 'A (nm)' (sic) vs [trans-DCE]/[Os(VIII)]."]),
))
