# ta2023: decompiled

Huong T. T. Ta, Nam V. Tran, M. C. Righi. "Atomistic Wear Mechanisms in Diamond: Effects of Surface
Orientation, Stress, and Interaction with Adsorbed Molecules." *Langmuir* **2023**, 39, 14396−14403.
DOI [10.1021/acs.langmuir.3c01800](https://doi.org/10.1021/acs.langmuir.3c01800) (printed in the PDF footer).
Received June 29, 2023; revised September 10, 2023; published September 27, 2023.

**Licence:** "This article is licensed under CC-BY 4.0" (p. 1, top right); "© 2023 The Authors. Published by
American Chemical Society" (p. 1 footer).

DOI check: three verify-sources receipts (vs-20261013-5606a98888, vs-20261013-5df963953b, vs-20261013-f937c7826d,
in `~/.local/share/verify-sources/receipts/`) resolved this DOI at Crossref and matched it to this PDF
(outcome verified_with_warnings); the first is also in `web/checks/receipts/`.

## Source files

| file | what it is |
|---|---|
| `source/ta2023.pdf` | copy of `papers/ta2023/ta2023.pdf` (8 pp., sha256 7f47e22d…1f1ec4). **Publisher version of record** (ACS typesetting, "Open Access" badge, download stamp "Downloaded via 188.216.158.91 on March 1, 2024" in the left margin of p. 1, "Recommended by ACS" box on p. 8). Fetch note in `papers/ta2023/SOURCE.txt`: "ta2023.pdf: https://cris.unibo.it/bitstream/11585/965046/1/ta-et-al-2023-...pdf (CC-BY published version, doi:10.1021/acs.langmuir.3c01800) curl 2026-10-13 by simulation agent". |

Born-digital PDF (embedded fonts, real text layer); every figure is a 300 ppi RGB raster image; no vector plots.

**Not available (not in `papers/ta2023/`):** the Supporting Information PDF named on p. 7 (force curves:
Figures S1–S5 — forces for clean and O-adsorbed (110), (001), (111) surfaces, O/H/OH and silicate on C(110),
and the stressed C(110) surfaces). The main text refers to Figures S1, S2, S3, S4, S5. No data set or source
data is named. The SI would be the place to get the force data behind Figs. 2 and 4–7 (only Fig. 3 and the
abstract graphic show forces).

## Contents

- `main.tex` / `main.pdf`: the whole article in reading order: licence line, journal line, title, authors,
  "Cite This" line, abstract, abstract graphic (`toc`), dates and copyright line (placed after the abstract;
  they are page-1 footers), sections 1–4, Figures 1–7 with verbatim captions, Associated Content (SI note),
  Author Information, Notes, Acknowledgments, references 1–46. `\pdfpage{}` markers for pp. 1–8.
  Left out: running header/footer (journal, page number, DOI line; the journal block is given once at the top),
  the ACS link bar ("Access / Metrics & More / Article Recommendations / Supporting Information", "Read Online"),
  the download stamp, logos, and the "Recommended by ACS" advertisement on p. 8 (all noted in a `\decompnote`).
- `figures/`: each figure cropped from the page at 300 dpi (`toc.png`, `fig1.png` … `fig7.png`); per plotted
  panel `<panel>.csv`, `<panel>_extract.py`, `<panel>.py`, `<panel>_replot.png`.
- `tools/` (shared by the figure scripts, imported relative to each script):
  `figtools.py` (image loading, axis-line and tick finding, colour masks, marker blobs, curve interpolation,
  square-edge finder), `panel.py` (per-panel driver and CSV writer), `replot.py` (re-plot from CSV),
  `asciimap.py` (prints a colour-class map of an image window: how the covered markers were read; see notes in the
  CSVs), `grid.py` (pixel grid over an image, used to choose exclusion rectangles).
- `decomp.sty`: copy of the osmium tools' style file. `tables/`: none (the paper has no tables).
- `work/`: scratch (page renders, embedded images, overlays `ov_*.png`, side-by-side comparisons `cmp_*.png`,
  glyph crops, draft text dump). May be deleted; the extract scripts recreate `work/` for their overlays.

Compile: `lualatex -interaction=nonstopmode -halt-on-error main.tex` (run twice) from this folder: compiles without
errors; 10 overfull boxes, all ≤ 0.8 pt except one of 15 pt (an unbreakable URL in Author Information).

Re-run the data: `python3 -I -B figures/<panel>_extract.py` then `python3 -I -B figures/<panel>.py` (any working
directory). The extract scripts read the embedded images straight from `source/ta2023.pdf` with PyMuPDF.

## Figures

All 10 plotted panels are **tier 3 (digitized)** from the 300 ppi raster images. Data = the DFT points, i.e.
the markers; the smooth curves through them are the plotting program's interpolation and are not digitized
(the replots draw a cubic spline only for looks). Method (`tools/panel.py`):
axis calibration on the detached axis line and its long major ticks (linear fit; residuals ≤ 0.015 eV and
≤ 0.007 Å, given in each CSV header); per series a colour mask, closed (fills holes punched by the black
dotted guide lines) and opened with an elliptic kernel (removes curves, frames, arrow shafts); each remaining
blob is a marker, centre = bbox centre plus a row offset measured on the legend (where the legend line passes
through the marker; matters for triangles, whose tips the opening blunts). Insets, legends and call-outs are
blanked with rectangles. Displacements are **measured**, not snapped to the 0.25 Å step grid (most lie
within 0.01 Å of it; the last three C(001) squares in Fig. 2a sit at about 1.80, 2.05 and 2.30 Å).
Markers in this paper overlap a lot (semi-transparent markers stacked at the same step); every covered marker
was handled individually and is flagged in the CSV `status` column (`ok`, `partly hidden`, `hidden`) with a
`note` saying how it was read: from visible edges/apex/base/rim (via `tools/asciimap.py`, with the
unobstructed marker size), from the series' curve on both sides (straight-line fit, `figtools.curve_at`), or,
at the origin cluster, from the marker on top. Uncertainty per point is in the CSV (2 px for clear markers,
3–5 px otherwise; 1 px ≈ 0.014–0.027 eV depending on the panel).

**Checks:** every extraction draws its points over the source image (`work/ov_<panel>.png`) and every replot was
put next to the original panel with `compare.py` (`work/cmp_<panel>.png`); I looked at all of them (each figure
and crop was viewed in this session); all series, ranges and scales match.
Cross-checks: the abstract graphic and Fig. 3 show the same data (agreement: energy max 0.011 eV, force max
0.028 nN); the 0 % series of Fig. 7a, Fig. 3 energy and the C(110) ketone series of Fig. 2c agree within
0.06 eV. Text values: Fig. 2a arrows read 2.93 (C(110)), 4.74 (C(001)), 8.52 eV (C(111)) vs the text's
2.95, 4.73, 8.54 eV; Fig. 2c reads 1.96 (C(110)) and 3.13 eV (C(111)) vs 1.97 and 3.13 eV — but see C(001)
under "Errors".

| panel | type | data | tier | points |
|---|---|---|---|---|
| abstract graphic | line plot, energy + force, two y axes, structure insets, gradient background | `figures/toc.csv` | 3 digitized | 22 |
| Fig. 1 | 3 × 3 ball-and-stick top views (clean/ether/ketone × C(110)/C(001)/C(111)) | – | – | – |
| Fig. 2a | line plot, energy vs displacement, clean surfaces, insets | `figures/fig2a.csv` | 3 digitized | 32 |
| Fig. 2b | line plot, ether | `figures/fig2b.csv` | 3 digitized | 27 |
| Fig. 2c | line plot, ketone | `figures/fig2c.csv` | 3 digitized | 33 |
| Fig. 3 | line plot, energy + force (two y axes), six numbered insets | `figures/fig3.csv` | 3 digitized | 22 |
| Fig. 4a | ball-and-stick top/side views (O3, O4) | – | – | – |
| Fig. 4b | line plot, O3/O4 | `figures/fig4b.csv` | 3 digitized | 22 |
| Fig. 5a | ball-and-stick top/side views (OH, OOH, H2, H2O) | – | – | – |
| Fig. 5b | line plot, OH/H2/H2O/OOH (no y-axis title) | `figures/fig5b.csv` | 3 digitized | 36 |
| Fig. 6a | ball-and-stick top/side views (silicate cases #1–#3) | – | – | – |
| Fig. 6b | line plot, Case #1–#3 | `figures/fig6b.csv` | 3 digitized | 31 |
| Fig. 7a | line plot, compression 0/3/7/10 %, insets | `figures/fig7a.csv` | 3 digitized | 44 |
| Fig. 7b | line plot, expansion 0/3/7/10 %, insets | `figures/fig7b.csv` | 3 digitized | 44 |

The structure insets inside the plots (ball-and-stick side views) are described in the `\alttext` of each figure.
The abstract graphic has no number or caption; "toc" is my name for it.

## Text check (`check_text.py` 2026-10-17j)

`python3 -I -B .../tools/check_text.py main.tex source/ta2023.pdf --exclude 8:315,405,560,745`

| options | coverage of PDF tokens | without repeated text | without in-figure text | tex tokens in PDF |
|---|---|---|---|---|
| `--exclude 8:315,405,560,745` (the "Recommended by ACS" ad box on p. 8) | **99.1 %** | 99.2 % | 99.2 % | 100.0 % |
| no options | 97.4 % | 97.5 % | 97.5 % | 100.0 % |

Every unmatched run explained (`--min-run 1`): running header word "Langmuir" (7 pages) and header
"pubs.acs.org/Langmuir Article" on p. 1; page numbers 14396–14403; the ACS link bar on p. 1 ("Read Online
Access Metrics & More Article Recommendations sı Supporting Information") and the "sı" SI icon on p. 7; the
download stamp (30 tokens); without `--exclude` also the "Recommended by ACS" box (119 tokens). Real hyphens at
line ends that the checker joins: "Pandey-reconstructed" (p. 6), "Tight-Binding" (ref. 21, p. 8). One
EXTRA/MISSING pair: ref. 19's "Ultra-/nanocrystalline" is split across the p. 7/p. 8 column break; I wrote
"Ultrananocrystalline" (as ref. 39 prints it), noted in a `\decompnote`.

**Glyph audit** (`decompile_work/tools/glyph_audit.py`): 10 hidden glyphs (U+0001 in STIXNonUnicode), all checked
against their crops (`work/glyphs/`): every one is the double-bond sign in "C═O"/"O═C"/"C═C" (pp. 2, 3, 5, 6, 7);
main.tex has "═" (U+2550) at all 10 places.

Read-through against the page images: subscripts (H₂, O₂, H₂O, H₂O₂, CO₂), superscripts (sp³, sp², 10⁻⁴, 10⁻³,
10⁻⁶, citation ranges with "−"), "4 × 4", "4 × 3", "2 × 2 × 1", "(111)-1 × 1", Å, "→" in "step 1 → 2",
"C−C(−O)", italics (z; journal names, volumes) and bold years in the references, "{100} and {111}" (ref. 25),
"H2, H₂O, and O2Molecules" (ref. 12, printed so). The run-in headings 3.1–3.3 are set as bold lead-ins.

## Errors and oddities in the paper (kept verbatim)

- Fig. 3 and the abstract graphic: right axis title printed "Forcce (nN)".
- Conclusions: "Conversly" (noted in main.tex).
- Ref. 12 title prints "H2" and "O2Molecules" without subscripts/space (H₂O is subscripted).
- **Possible mismatch, text vs Fig. 2c:** the text gives 2.51 eV for detaching the first C atom from ketone
  C(001); the green-arrowed C(001) marker (0.75 Å) reads 2.76 ± 0.05 eV. The C(001) plateau from 1.0 to 2.5 Å
  reads 2.47–2.54 eV, so 2.51 may refer to the plateau rather than the arrowed point.
- **Possible duplicated series, Fig. 7a vs 7b:** the 3 % curves of "Compression" and "Expansion" coincide at
  all 11 steps (differences −0.02…+0.05 eV, within the digitizing uncertainty), although their end-state insets
  differ (inclined chain vs vertical chain). The 0 % curves coincide too, as expected for zero stress.
- Fig. 5b: no y-axis title (the other energy panels have "Energy (eV)"); the legend shows a grey square for OH,
  the plotted OH markers are small grey diamonds.
- Fig. 2a: the C(001) markers after 1.5 Å lie at about 1.80, 2.05 and 2.30 Å, off the 0.25 Å step grid that
  the text describes ("the oxygen atom is displaced by 0.25 Å") and that all other series follow.

## Known problems

- Covered markers (flagged `partly hidden` 63 and `hidden` 28 of the 313 points; 222 are `ok`) are less certain
  (3–5 px); at each panel's origin all series overlap and the hidden ones are given the visible marker's centre.
- Insets hide parts of some axes (Fig. 2c: the 10 eV tick; Fig. 5b: the 0 Å tick and the −1/0 eV ticks);
  calibrations use the visible major ticks only (stated in the CSV headers).
- Force data for Figs. 2, 4–7 are only in the unavailable SI.
