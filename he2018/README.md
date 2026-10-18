# he2018: decompiled

Q. He, M. Hsueh, G. Zhang, D. C. Joy, R. D. Leapman. "Biological serial block face scanning electron
microscopy at improved z-resolution based on Monte Carlo model." *Scientific Reports* **8**, 12985 (2018).
DOI [10.1038/s41598-018-31231-w](https://doi.org/10.1038/s41598-018-31231-w).
Received 10 January 2018; accepted 10 August 2018; published online 28 August 2018.

**Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0), "© The Author(s) 2018", as stated on p. 13.

## Local and external

**In the local collection**
- Source files:
  - `papers/he2018/he2018.pdf` – main article, 13 pp., publisher version of record
  - `papers/he2018/41598_2018_31231_MOESM1_ESM.pdf` – Supplementary Information, 14 pp.
  - `papers/he2018/he2018.txt`, `papers/he2018/he2018.raw.txt` – earlier text extractions (starting point for the transcription)
  - `papers/he2018/SOURCE.txt` – fetch note
- Cited works decompiled here: nguyen2016 (`decompiled/nguyen2016/`)

**External pull needed** (not on this machine)
- Supplementary Movie 1 (visualization of the membranes, made with Amira like Fig. 6) – no link given (a separate file on the journal site) – a movie, not plot data; the paper names no data repository or source-data file
- All other cited references: 43 entries without a [local: …] tag: 42 of the 43 in the main reference list and the 1 Supplementary Reference.

## Source files (`../../papers/he2018/`)

| file | what it is |
|---|---|
| `he2018.pdf` | main article, 13 pp. **Publisher version of record** (Springer Nature typesetting, running header "www.nature.com/scientificreports/", footer "SCIENTIFIC REPORTS \| (2018) 8:12985 \| DOI:10.1038/s41598-018-31231-w"; PDF created 22 Aug 2018). `SOURCE.txt`: fetched from nature.com. Oddity: the text layer of p. 1 says "Published: xx xx xxxx"; a small raster image placed over that line shows "Published online: 28 August 2018" (the page image is used). |
| `41598_2018_31231_MOESM1_ESM.pdf` | Supplementary Information, 14 pp.: the authors' Word document printed to PDF (title "Final_Supplementary_Information_with_changes_04-25-2018", dated "04-25-18" on p. 1). |
| `he2018.txt`, `he2018.raw.txt` | earlier text extractions of the main PDF (raw.txt = `pdftotext`; used as a starting point for the transcription, then checked against the page images). |

**Not available:** *Supplementary Movie 1* ("A visualization of the membranes is also presented in Supplementary
Movie 1"; Methods: "3D rendering model (Fig. 6) and movie (Supplementary Movie) were created using the Amira
program"). It is a separate file on the journal site and is not in the source folder. The paper names no data
repository or source-data file, so no tier-1 data exist for any panel.

## Contents

- `main.tex` / `main.pdf`: the whole article in reading order (journal line, OPEN, dates, title, authors, the
  affiliation footnote placed after the authors, abstract, introduction, Results, Discussion, Methods, 43
  references, Acknowledgements, Author Contributions, Additional Information, licence). Equations 1–8 in LaTeX.
- `supplement.tex` / `supplement.pdf`: the whole SI (title page, Supplementary Figures 1–5 with the text on p. 6,
  Supplementary Table 1, Supplementary Notes 1 and 2 — Note 2, the Digital Micrograph script, is reproduced line by
  line in a `verbatim` block — and the supplementary reference).
- `figures/`: every figure rendered at 200 dpi (`fig1.png` … `fig6.png`, `sfig1.png` … `sfig5.png`, cropped
  from the PDF without captions); per plotted panel `<panel>.csv`, `<panel>_extract.py`, `<panel>.py`,
  `<panel>_replot.png`. `sfig5_vector.py` is the shared extraction module for SI Fig. 5b–e (the four
  `sfig5?_extract.py` call it).
- `tables/stable1.csv`: Supplementary Table 1. The main article has no tables.
- `work/`: scratch (page renders, native embedded images, vector dumps, overlays `*_overlay*.png`, side-by-side
  comparisons `cmp_*.png`, LaTeX logs, check JSON). May be deleted.

Compile: `TEXINPUTS=../tools: lualatex -interaction=nonstopmode -halt-on-error main.tex` (and `supplement.tex`)
from this folder; both compile without errors (run twice), with some overfull lines from long URLs and the
verbatim script.

Re-run the data: `python3 -I figures/<panel>_extract.py`, then `python3 -I figures/<panel>.py` (any working
directory). The extract scripts read the PDFs directly with PyMuPDF.

## Figures

The main-article figures are each one embedded raster image (1650 px wide, ~300 ppi); `vector_dump.py` (re-run
after the tool fix for zero-width lines) finds only the page header/footer rules on those pages, so the plotted
panels Fig. 2c, 3d, 3e are **tier 3**. SI Fig. 4 is a low-resolution raster (549 × 344 px, ~84 ppi): **tier 3**.
SI Fig. 5b–e are spreadsheet-style charts whose frames, gridlines and polynomial trendlines are vector paths and
whose data markers are tiny raster images placed at the data points: **tier 2** (marker centres from the
placement rectangles and soft masks; trendline vertices exactly).

**Checks done for every plotted panel:** (1) the extracted points drawn back onto the source (raster panels: on
the embedded image, `work/fig2c_overlay.png`, `work/fig3d_overlay*.png`, `work/fig3e_overlay.png` with zoomed
per-sub-plot checks `work/fig3e_chk_*.png`, `work/sfig4_overlay*.png`; vector panels: on a 4× render of the panel,
`work/sfig5?_overlay.png`), and (2) original and re-plot side by side with `tools/compare.py`
(`work/cmp_fig2c.png`, `cmp_fig3d.png`, `cmp_fig3e.png`, `cmp_sfig4.png`, `cmp_sfig5?.png`, all four in
`cmp_sfig5_all.png`). I looked at all of them; series, ranges and scales match.

| panel | type | data | tier | notes |
|---|---|---|---|---|
| Fig. 1a–f | schematic (SBEM set-up, image stacks, sub-slice reconstruction) | – | – | |
| Fig. 2a | schematic (model block with 4 cuboids, 3 views) | – | – | |
| Fig. 2b | 15 simulated BSE images (0.8–2.2 keV) | – | – | |
| Fig. 2c | 15 small bar charts, 4 bars each, no axis numbers | `figures/fig2c.csv` | 3 digitized | heights in px, as fraction of each chart's gridded box and in gridline units; charts ≤1.4 keV and ≥1.5 keV have different gridline counts (possibly different y scales) |
| Fig. 3a | schematic (model block with 3 cuboids, 3 views) | – | – | |
| Fig. 3b, 3c | simulated BSE images / calculated sub-slices | – | – | |
| Fig. 3d | line plot, 2 profiles | `figures/fig3d.csv` | 3 digitized | per pixel column, top/bottom of the noisy line; gaps where one line hides the other |
| Fig. 3e | 6 histograms (dots + lines), 2 series each | `figures/fig3e.csv` | 3 digitized | 191 dots; flag `visible` / `partly hidden` / `hidden` (red dots under green ones, mainly in "cuboid 2 top sub-slice": 13 partly hidden, 3 hidden) |
| Fig. 4a–l | 12 BSE images (x-z) | – | – | |
| Fig. 5a–f | 6 BSE images (x-y, y-z) | – | – | |
| Fig. 6a–f | 6 3D surface renderings | – | – | |
| SI Fig. 1 | schematic (image stack) | – | – | |
| SI Fig. 2a–g | BSE images and difference images | – | – | |
| SI Fig. 3 | 16 BSE / sub-slice images | – | – | |
| SI Fig. 4 | EDS spectrum + 4 reference spectra | `figures/sfig4.csv` | 3 digitized | ~84 ppi source; colours hidden near the baseline; Cu standard clipped at the top left |
| SI Fig. 5a | schematic (model block with 3 cuboids, 3 views) | – | – | |
| SI Fig. 5b | scatter + 2 polynomial trendlines | `figures/sfig5b.csv` | 2 vector | 18 markers |
| SI Fig. 5c | same | `figures/sfig5c.csv` | 2 vector | 18 markers |
| SI Fig. 5d | same | `figures/sfig5d.csv` | 2 vector | 20 markers |
| SI Fig. 5e | same | `figures/sfig5e.csv` | 2 vector | 20 markers |

Fig. 3e method note: every clean series in Fig. 3e has equally spaced dots (histogram bins). Hidden red dots
were placed on that regular grid (from the series' first/last dot and the spacing of its visible dots) and their
height read from the visible red crescent with a disk template; where no red pixels remain the row has an x but
no frequency (`hidden`). Treat `partly hidden` values as ±5–10 counts; "cuboid 2 top sub-slice, red" is almost
entirely covered by the green series and is the least certain.

SI Fig. 4 note: the PDF has a few stray white vector objects on top of this figure (a white "z/x" axis icon,
white lines and a white rectangle outline near 10.5–11.5 keV and above the 10.55 keV peak). They are invisible on
the white background; the rectangle could hide at most a fraction of a point of the 10.55 keV peak top.

## Text check (`tools/check_text.py`, version 2026-10-17c)

| file | coverage (raw) | without repeated text | running text (also without in-figure text) | tex tokens found in PDF | MISSING ≥6 | EXTRA ≥6 |
|---|---|---|---|---|---|---|
| `main.tex` vs `he2018.pdf` | 98.8 % | 99.3 % (60 tokens repeated) | 99.3 % | 99.5 % | 4 runs, 24 tokens | 0 |
| `supplement.tex` vs SI PDF | 86.9 % | 90.8 % (105 tokens "repeated") | 96.4 % | 99.4 % | 1 run, 23 tokens | 0 |

Explanations:

- **main, repeated:** the running header "www.nature.com/scientificreports/" (12 pages). The footer
  "SCIENTIFIC REPORTS | (2018) 8:12985 | DOI…" is matched against the journal line given once at the top; the
  page numbers remain as single-token MISSING runs.
- **main, MISSING ≥6:** all inside Equations 1, 3, 6 and 8 (the text layer linearises the math
  differently from LaTeX). With `--min-run 1` the rest is: subscripts glued to their letter in the text layer
  ("Elow", "Ehigh", "Em", "nH", "Bm", "Sn", "Anm") against E\textsubscript{low} etc.; superscript exponents glued
  ("107 µm3" vs 10\textsuperscript{7}); "xx xx xxxx" (hidden text layer under the date image, see above) against
  "online 28 August 2018" (from the page image); "OPEN" (order). No transcription errors were found.
- **supplement:** the low raw number has three causes, none of them transcription errors:
  1. The "repeated" filter blanks digits, so every unmatched run of ≥5 *numbers* looks the same on every page and
     is counted as repeated, although the tool itself lists each with "[1 pages]". These are in-figure labels:
     the cut numbers and panel letters of SI Fig. 3, the tick labels of SI Fig. 5, and page numbers (tool bug,
     see below).
  2. The DM script (Supplementary Note 2) is in a `verbatim` block, but `check_text.py` strips LaTeX commands
     inside it, so every `\n` in the script's strings is dropped from the tex side: ~40 single "n" tokens MISSING.
  3. SI Fig. 1 is a vector drawing whose labels ("cut 1", "E low/high", …) are text; the in-figure detector does
     not catch it: the one MISSING run ≥6 (23 tokens, p. 2). Also MISSING: page numbers 2–14.
  The EXTRA tokens (12, all <6) are the two matrices of Supplementary Note 1 and "ϵ_det" in Supplementary Table 1,
  whose Cambria Math glyphs the text layer garbles ("!!", "!!"#"); transcribed from the page image.

Read-through against the page images (step 4) done for: Equations 1–8 (limits, subscripts, bold **A**, **B**,
**S**, the bracketed [J₀δz], matrix entries and exponents, minus signs in Eq. 8), γ_stain, ϵ_det, η, δz, ×, ≥,
≳ (set as `$\gtrsim$`; DejaVu Serif lacks U+2273), ±, °C, µm, \textasciitilde, superscript citation ranges with en
dashes, the reference formatting (italic journals and *et al.*, bold volumes, italic book title of ref. 12, *en
bloc* in ref. 38), the SI matrices and Supplementary Table 1. The DM script was compared line by line with the
page images of SI pp. 10–14 (it was taken from the text layer, which matches them, including the leading space
of " //set new mag").

## Errors and inconsistencies found in the paper (kept verbatim; the first two flagged with `\decompnote`)

- **Fig. 4 caption** says the 50-nm data were imaged at "1.4 keV and 2.4 keV"; the text ("E_low = 1.4 keV and
  E_high = 2.2 keV", "1.4 keV and 2.2 keV"), the Methods and Supplementary Table 1 say 1.4 and 2.2 keV.
- **Fig. 5 panel references in the text do not match the caption.** Caption: (b) enlarged x-y region,
  (c) average y-z view, (d) sub-slice y-z stack, (e)/(f) five-slice averages of (c)/(d). Text: "An orthogonal view
  in Fig. 5b shows a y-z view … obtained without sub-slice analysis", "the sub-slice image stack (Fig. 5c)",
  "Five-slice averages … of the y-z views in Fig. 5b,c are shown in Fig. 5d,e", "y-z views in Fig. 5b,c are
  presented in Fig. 6a,b" (the Fig. 6 caption says "orthoslices of Fig. 5(d,f)"). The text is shifted by one letter.
- **SI Fig. 5 caption:** "The curves in (a) and (c) … whereas the curves in (c) and (d)" — by the caption's own
  panel definitions these are (b),(c) (1–9 %) and (d),(e) (10–100 %). It calls the sum curve "blue"; the sum
  markers are blue but the "Poly. (sum)" trendline is purple.
- **Electron fluence for the 25-nm data set:** Results "total fluence of 13 electrons/nm²" (and "~13 e/nm²" for
  the simulation), Methods "15 e/nm² for 25-nm cutting increments", Supplementary Note 1 "maximum electron fluence of
  15 e/nm² for cutting at increments of 25 nm".
- Equation numbers: the text says the sub-slices are noisier "as expected from the application of the inverse
  matrix in Equation 2" and "Sub-slice analyses, based on Equation 2"; Equation 2 is the forward sum, the inverse
  is Equations 5/6.
- Methods: the first simulation has "8 lead stained (3%) cuboids" with centres 6.25–93.75 nm and energies
  "0.8 keV to 2.9 keV"; Fig. 2 shows 4 cuboids (0–50 nm) and 0.8–2.2 keV (possibly a subset; not stated).
- SI reference 1 (Ritchie, DTSA-II) gives "15, 14 (2009)"; main ref. 43 gives "15, 454–468 (2009)".
- DM script (Supplementary Note 2): comments disagree with the code, e.g. "//set beam energy value to 1.4 keV"
  before `BeamEnergy3 = 2200`, `Result( "acquire image at 1.0kev DONE \n" )` after the 1.4 keV image, the 1.4 keV
  image saved as "lowKeV", "//save image at 3.4 keV" for the 2.2 keV image, "//set beam energy value back to
  1.0 keV" before `BeamEnergy4 = 1400`.
- Typos (verbatim): "gven", "algorthim", "as indicted by the red triangle", "refined though", "fitted though",
  "electro probe x-ray microanalysis", "which we have been considered here", "microscopyand" (ref. 29), "jby"
  (ref. 36), "SEM image method. U.S. Patent US8, 232, 523 B2" (ref. 22), "10, 000" (SI Table 1).
- Fig. 2c's mini charts have no y numbers and two different gridline layouts (see `fig2c.csv`), so heights may
  not be comparable between the 0.8–1.4 keV and 1.5–2.2 keV charts; the figure does not say.

## Problems and suggestions (spec and tools)

- `vector_dump.py`: the zero-width-line bug (fixed by the coordinator during this run). I re-ran it on every
  figure page; conclusions unchanged (main figures raster; SI Fig. 5 vector).
- `check_text.py` repeated-text filter: 5-grams made only of numbers ("# # # # #") match on many pages, so
  in-figure number runs (tick labels, panel numbers) are classed as "repeated" (listed with "[1 pages]").
  Fix: require at least one non-digit token in a 5-gram before counting it across pages, or count a text as
  repeated only if the same blanked run occurs on ≥3 pages *and* those pages' runs sit at similar page positions.
- `check_text.py` and `verbatim`: command stripping runs inside `verbatim`, dropping `\n` etc. from code listings.
  Fix: cut out `verbatim`/`lstlisting` bodies before the LaTeX clean-up and tokenise them literally.
- `check_text.py` in-figure detector misses small vector schematics with text labels (SI Fig. 1, 48 paths, 13
  small images). Fix: also treat clusters of small images (Word equation/label images) as figure area, or let the
  decompiler pass figure boxes (`--figure-box page x0 y0 x1 y1`).
- `digitize_common.overlay()` draws one colour and writes the file immediately; for multi-series panels I had to
  draw into a copy myself. Suggest `overlay(a, {"series": (pts, colour)}, out)`.
- Spec: no guidance for (a) charts that mix vector lines with raster marker images (I called it tier 2 and said
  so), (b) markers hidden under other series (I added a `flag` column), (c) `\pdfpage` when a page holds only a
  figure and a sentence runs across it (I put both markers at the page break and a `\decompnote`). A sentence in
  the spec on each would make papers consistent.
