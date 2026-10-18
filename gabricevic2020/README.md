# gabricevic2020: decompiled

Mario Gabričević, Gábor Lente, István Fábián. "Kinetic detection of osmium(VI) ester intermediates during the
OsO4-mediated aqueous dihydroxylation of chloroethylenes." *J Phys Org Chem* **2020**, 33, e4045.
DOI [10.1002/poc.4045](https://doi.org/10.1002/poc.4045). Received 30 May 2019; revised 27 October 2019;
accepted 17 November 2019.

**Licence:** open access under the Creative Commons Attribution License (CC BY), "© 2020 The Authors. Journal of
Physical Organic Chemistry published by John Wiley & Sons Ltd" (p. 1 footer).

## Local and external

**In the local collection**
- Source files:
  - `papers/gabricevic2020/poc.4045.pdf` – the article, 10 pp., publisher's version of record
  - `papers/gabricevic2020/poc4045-sup-0001-supporting_information.docx` – Supporting Information (Word file: Figs. S1–S3, derivation, thermodynamic analysis)
  - `papers/gabricevic2020/poc.4045.txt`, `papers/gabricevic2020/poc.4045.raw.txt` – earlier text extractions (not used)
  - `papers/gabricevic2020/SOURCE.txt` – download note
- Cited works decompiled here: riemersma1968 (`decompiled/riemersma1968/`)

**External pull needed** (not on this machine)
- Nothing besides the references: the paper and SI name no data set, repository or source-data file.
- All other cited references: 49 entries in the reference list ([1]–[50]) without a [local: …] tag. The SI has no reference list.

## Source files (`../../papers/gabricevic2020/`)

| file | what it is |
|---|---|
| `poc.4045.pdf` | the article, 10 pp. **Publisher's version of record**, not the accepted manuscript: Wiley typesetting (Arbortext/Distiller, STIX2 fonts), running headers "n of 10 / WILEY Journal of Physical Organic Chemistry / GABRIČEVIĆ ET AL.", "Check for updates" button, first-page footer "J Phys Org Chem. 2020;33:e4045". `SOURCE.txt`: fetched from the REAL repository of the Library of the Hungarian Academy of Sciences (real.mtak.hu/122004), which serves the publisher PDF (PDF metadata: created 2020-01-03, modified by iText 2021-03-06). |
| `poc4045-sup-0001-supporting_information.docx` | Supporting Information, a Word file (author: "mariog", modified 2019-10-27): title, authors, Figs. S1–S3, the derivation of Eqs. 12/13 (heading "Derivation of Eq. 14"), and a thermodynamic analysis. Equations are MathType 6 OLE objects; figures are three 893 × 631 px, 220 ppi palette TIFFs. |
| `poc.4045.txt`, `poc.4045.raw.txt` | earlier text extractions of the PDF (not used). |
| `SOURCE.txt` | download note. |

No data set, repository or source-data file is named anywhere in the paper or the SI, so there is no tier-1
source to miss. The SI named on p. 10 ("Additional supporting information may be found online") is the .docx above.

## Contents

- `main.tex` / `main.pdf`: the whole article in reading order: dates/DOI/journal block, "RESEARCH ARTICLE", title,
  authors, affiliations, correspondence and funding (margin column of p. 1), licence and copyright lines (p. 1
  footer, placed after the affiliations, noted), abstract, keywords, sections 1–5 with Equations (1)–(19) and the two
  unnumbered equations, Figures 1–7 with captions, acknowledgement, ORCID, references [1]–[50], the Supporting
  Information note and the "How to cite this article" box. `\pdfpage{N}` marks every page start.
- `supplement.tex` / `supplement.pdf`: the whole SI (title, authors, affiliations, Figs. S1–S3, the derivation with
  Eqs. (11), (12), (S1)–(S8) and one unnumbered equation, the thermodynamic section). `\sourcefile{}` names the .docx;
  there are no pages, so no `\pdfpage`.
- `figures/`: `fig1.png` … `fig7.png` (crop.py renders of the PDF at 200 dpi, figure bbox + margin);
  `sfig1.png` … `sfig3.png` (the SI TIFFs converted losslessly to PNG at their native 893 × 631 px). Per plotted panel:
  `<panel>.csv`, `<panel>.py` (re-plot, reads only the CSV) and `<panel>_replot.png`. Extraction scripts are one per
  **figure** (`fig1_extract.py` writes `fig1main.csv` and `fig1inset.csv`, `fig6_extract.py` writes `fig6top.csv` and
  `fig6bottom.csv`, `sfig2/3_extract.py` write `…main.csv` and `…inset.csv`), because both panels come from one image
  and share its calibration code. Shared helpers: `gab_common.py` (loading the source rasters straight from the PDF or
  the .docx, anti-aliasing-aware colour masks, column tracker, marker finder, re-plot helpers) and `spectra_common.py`
  (multi-line spectra and the inset lines); both import `../../tools/digitize_common.py`.
- `tables/`: not created; the paper and SI have no tables.
- `work/`: scratch (page renders, embedded images, overlays `*_overlay.png`, side-by-side checks `cmp_*.png`, the
  pandoc conversion of the SI `si_pandoc.tex` / `si_plain.txt` and media, the unzipped .docx, `mtef_dump.py`
  (MathType MTEF v5 → linear text, used to transcribe the SI equations exactly), `check_si.py` (SI text check, below),
  `alttexts_*.py` (the descriptions, inserted into the .tex), logs). May be deleted.

Compile: `TEXINPUTS=../tools: lualatex -interaction=nonstopmode -halt-on-error main.tex` (and `supplement.tex`);
both compile without errors (run twice), no missing glyphs (≅ in running text is set as `$\cong$`, DejaVu Serif has no
U+2245).

Re-run the data: `python3 -I figures/<fig>_extract.py`, then `python3 -I figures/<panel>.py` (any working directory).

## Figures

All plots are **raster images** (main PDF: embedded images ~1003 px wide, JPEG-like with compression artefacts; SI:
lossless 220 ppi palette TIFFs). `tools/vector_dump.py` on pp. 3–6 finds only the page-header logo paths and one
equation fraction bar, no plot paths, so no panel is tier 2 and **every plotted panel is tier 3 (digitized)**:
frame lines and tick marks found in the image, linear (or log10) fit on the labelled ticks (residuals and the
unlabelled-tick checks are in each CSV header), series traced with colour masks that allow for anti-aliasing,
followed column by column from a seed point (lines, marker bands) or found as connected components (markers;
overlapping markers split by a greedy fit of copies of an isolated marker; partly hidden markers centred from their
unhidden edges, flagged). Dense marker traces (Figs. 2, 3) are given per pixel column as band middle/top/bottom.
Multi-line spectra without a legend are named by the line colour.

**Checks.** Every extraction draws its points back on the source image (`work/*_overlay.png`) and every re-plot was
put beside the original with `tools/compare.py` (`work/cmp_*.png`); I looked at both for every panel (zooms of the
crowded regions too). Series, ranges and scales match. Independent numerical checks against the paper's text:
- Fig. 5 fit line vs Equation (1) with k_acid = 4.3 s⁻¹, pK = 12.0, k_base = 0, pKw = 13.58: mean +0.007, max 0.022 s⁻¹.
- Fig. 6 line slopes 0.534, 0.110 and 0.0357 dm³ mol⁻¹ s⁻¹ vs the text's k_2nd 0.53, 0.111, 0.036.
- Fig. 7 curves vs Equation (1) with the paper's three parameter sets: mean −0.5 to +1.6 %, max 2.6 %.
- Fig. 1: the inset's first six values (2.06, 1.70, 1.62, 1.55, 1.17, 0.93) equal the red, blue, teal, magenta, olive and
  navy spectra at 320 nm (2.06, 1.70, 1.62, 1.55, 1.16, 0.92), and the remaining five (0.83–0.89) the bundle; so the
  colour order is the [TCE] order (my inference from the two digitizations, not stated in the paper).

Limits: in the bundles of nearly coincident spectra (Fig. 1: six lines within ~10 px between 280 and 400 nm; S2, S3
similar) lines hide each other, so some series have gaps or only short stretches (e.g. Fig. 1 "pink" 317–348 nm,
"wine" 321–395 nm) and values flagged `overlap` may belong to a neighbour (~0.05 A). Near t = 0 in Fig. 2 the first
markers sit on the y axis and are partly missed (noted in the CSV).

| panel | type | data | tier | notes |
|---|---|---|---|---|
| Fig. 1 main | line plot, 11 UV-vis spectra, no legend | `figures/fig1main.csv` | 3 digitized | series = line colours; `overlap`/`clipped` flags |
| Fig. 1 inset | scatter (11 diamonds) + red dotted and orange dashed straight lines | `figures/fig1inset.csv` | 3 digitized | lines as end points of a least-squares line |
| Fig. 2 | kinetic traces (dense markers) + fit curves, 3 series | `figures/fig2.csv` | 3 digitized | bands per pixel column |
| Fig. 3 | kinetic traces + fit curves, broken y axis | `figures/fig3.csv` | 3 digitized | two y calibrations |
| Fig. 4 | scatter, 3 series | `figures/fig4.csv` | 3 digitized | 17 points |
| Fig. 5 | scatter, 3 series + fit curve | `figures/fig5.csv` | 3 digitized | one point almost hidden (flagged) |
| Fig. 6 top | scatter, 2 series + lines | `figures/fig6top.csv` | 3 digitized | no panel letters: "top"/"bottom" are my names |
| Fig. 6 bottom | scatter, TCE + line | `figures/fig6bottom.csv` | 3 digitized | |
| Fig. 7 | scatter + fit curves, log y | `figures/fig7.csv` | 3 digitized | log scale confirmed on 15 minor ticks |
| Fig. S1 | line plot, 2 spectra + arrow | `figures/sfig1.csv` | 3 digitized | |
| Fig. S2 main | line plot, 10 spectra | `figures/sfig2main.csv` | 3 digitized | |
| Fig. S2 inset | scatter (9) + 2 lines | `figures/sfig2inset.csv` | 3 digitized | |
| Fig. S3 main | line plot, 11 spectra | `figures/sfig3main.csv` | 3 digitized | |
| Fig. S3 inset | scatter (11) + 2 lines | `figures/sfig3inset.csv` | 3 digitized | y title "A (nm)" (sic) |

14 plotted panels, all tier 3; no micrographs, photographs or schematics.

## Text check

`tools/check_text.py` (version 2026-10-17g):

| file | coverage of source tokens | without text repeated on ≥ 3 pages | tex tokens found in source | MISSING ≥ 6 | EXTRA ≥ 6 |
|---|---|---|---|---|---|
| `main.tex` vs `poc.4045.pdf` | 95.3 % | **96.0 %** (54 repeated tokens: running headers "n of 10 GABRIČEVIĆ ET AL.") | 99.5 % | 11 runs, 93 tokens (all equations) | 0 |
| `supplement.tex` vs the .docx (own script `work/check_si.py`, see below) | **98.7 %** | – | 99.4 % | 0 | 0 |

The main text is below the 98 % aim only because of the equations: the PDF's text layer encodes the math in
MathType-style fonts whose glyphs come out as other characters (`þ` for "+", `¼` for "=", `½`/`ð`/`Þ` for brackets and
parentheses, square-root bars as "ffiffi…"), which the tokenizer turns into "th", "1 4", "1 2", "d" etc. All 93 tokens
of the MISSING runs ≥ 6 and nearly all of the 298 unmatched tokens at `--min-run 1` are of this kind (Equations (1),
(2)–(19), the two unnumbered equations on pp. 8–9). The only others: the page number "1 of 10" on p. 1 (the other pages'
numbers are in the repeated text), and "pseudo-first" (a real hyphen at a line end on p. 4, joined by the tool). The 28
short EXTRA runs (1–3 tokens) are the same equations seen from the .tex side (H, aq, l, 4 2 …). Equations, sub- and
superscripts, Greek letters, ±, ×, minus signs and units were read against 200–220 dpi page renders (step 4).

**SI check (tool gap).** `check_text.py` takes PDFs only, so `work/check_si.py` compares `supplement.tex` (through
check_text's own `tex_text()`/`tokens()`) with `pandoc -t plain --wrap=none` of the .docx, using the same
SequenceMatcher logic. Pandoc renders the 11 MathType objects as "[]", so the 11 equation environments are removed from
the .tex before comparing. Unmatched at `--min-run 1`: the 10 equation numbers ((11), (12), (S1)–(S8), which sit in
`\tag{}` inside the removed equations: 16 tokens) and six "OsO2(OH)4²⁻" where pandoc's plain output glues "₄²" into
"42" (12 tokens). The equations themselves were transcribed from the MTEF data of each OLE object
(`work/mtef_dump.py`, a small parser written for this) and compared with the WMF previews rendered by ImageMagick
(`work/eq/`); the previews lose one MT Extra glyph (≫ in Eq. S7 shows as "?"), which the MTEF data gives.

## Errors and oddities in the paper (kept verbatim; flagged with `\decompnote` where it matters)

- **SI, Henry constant conversion (my arithmetic):** 21.7 kPa m³ mol⁻¹ × 997 kg m⁻³ = 216 bar kg mol⁻¹, not the stated
  21.6; with K = 216 the aq → g step is −13.3 kJ mol⁻¹ (not −7.6) and the overall aqueous ΔG° about −23.5 kJ mol⁻¹
  (not −17.8, which the main text also quotes on p. 9). The conclusion (no highly exergonic intermediate) is not
  changed by this. Noted in supplement.tex.
- **SI heading** "Derivation of Eq. 14": the section derives Eqs. 12 and 13.
- **SI reference [37]** for the solution technique of Eq. 11: in the main list [37] is Yan & Schwartz (Environ. Sci.
  Technol.); the main text cites [45] (Lente, Deterministic Kinetics) for this. The SI has no reference list.
- **SI Eq. S4**, second line: "(B + A − 2k₊x)" where the following lines have [EO] (stray x from an earlier notation).
- **SI Fig. S3 inset**: y axis title "A (nm)" without the wavelength (S2 says "A (345 nm)", Fig. 1 "A (320 nm)").
- **p. 6:** "K_a1 = 8.69 × 10⁻¹³ M (pK_a1 = 12.2) and 7.58 × 10⁻¹⁵ M (pK_a2 = 14.4)": −log of these values is 12.06 and
  14.12 (my arithmetic).
- Typos (verbatim): "forms in a reversible way form osmium(VIII)" and "chloroethyelene" (p. 6), "can be givens as"
  (p. 7), "the formula give in Equation (1)" (Fig. 5 caption), missing full stop after "significantly higher" (p. 4),
  "glyoxilic acid" (p. 3), "Englewood Clipps" (ref. 49 and SI), "J. Org. Chem" (ref. 8), "Angew. Chem. Inter" (ref. 11),
  "J. Chem, Soc., Faraday Trans. 1" (ref. 42), "k₋ > > …" printed with a space (p. 7); SI: "All other thermodynamic data
  at were taken", "inequity" for inequality, "chloroethyelenes", an unclosed parenthesis after "(the chemical meaning of
  this inequality …", and "D. Richens, The Chemistry of Aqua Ions" vs ref. 30 "D. T. Richens, The Chemistry of the Aqua
  Ions".

## Known problems of this decompilation

- Spectra bundles (see Figures above): partial coverage and `overlap` flags; the colour names are mine.
- Fig. 2/3 data are bands, not individual points (the markers overlap completely).
- Line widths of the main-figure images are ~3 px and the images are lossy-compressed, so the 2-px uncertainties in
  the CSV headers are for isolated lines; fit lines through markers were traced only where they are visible.
