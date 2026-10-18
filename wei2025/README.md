# wei2025: decompiled

Pengchang Wei, Zhen-Yu Yin, Pierre-Yves Hicher, Yuanyuan Zheng. "Molecular Dynamics Study on Quartz-Indenter
Shape and Depth Effects in Epoxy Interfacial Mechanics." *International Journal for Numerical and Analytical
Methods in Geomechanics* **2025**, 49(13): 2949–2964. DOI [10.1002/nag.4021](https://doi.org/10.1002/nag.4021)
(printed on p. 1). Received 1 April 2025; revised 12 May 2025; accepted 31 May 2025.

**Licence:** open access under the Creative Commons Attribution License (CC BY); © 2025 The Author(s),
published by John Wiley & Sons Ltd (p. 1 footer).

**DOI check:** verify-sources receipt `vs-20261013-dc634aefc8` (outcome verified_with_warnings): Crossref
resolved 10.1002/nag.4021 to this title, authors, volume 49, issue 13, pages 2949–2964, not retracted, and the
receipt's PDF SHA-256 (`8b6702e2…c449187`) is that of `source/wei2025.pdf`.

## Source files

| file | what it is |
|---|---|
| `source/wei2025.pdf` | the article, 16 pp., copied from `papers/wei2025/wei2025.pdf`. **Publisher version of record** (Wiley typesetting, journal pages 2949–2964, Wiley Online Library download stamp "on [29/09/2025]" by Hong Kong Polytechnic University in the right margin). Born-digital (embedded STIX fonts); all figures are embedded raster images (300 ppi). |

Fetch note (`papers/wei2025/SOURCE.txt`): "wei2025.pdf: https://ira.lib.polyu.edu.hk/bitstream/10397/115592/1/Wei_Molecular_Dynamics_Study.pdf (doi:10.1002/nag.4021) curl 2026-10-13 by simulation agent".
`papers/wei2025/wei2025.txt` (an earlier text extraction) was not used.

**Not available (not on this machine):**
- the Supporting Information, listed on p. 16 as eight files: `nag4021-sup-0001-SuppMat.docx` (with Equations S1–S2,
  Table S1 and Figures S1–S4, all cited in the text), six videos `nag4021-sup-0002-VidS1.mp4` … `nag4021-sup-0007-VidS6.mp4`,
  and **`nag4021-sup-0008-Data.zip`**, which the Data Availability Statement says holds "the more detailed data and
  code" — the probable **tier-1 source data** for the plotted figures. Not fetched (no network).
- the GitHub repository https://github.com/weipc3/Nanoindentation-epoxy-quartz (LAMMPS scripts for the R = 25 Å system),
  named in the Data Availability Statement.

**Cited works in the collection** (from `decompile_work/manifest.json`): ref. 30 (Wei, Yin, Hicher, Xu, "Interfacial
Mechanical Behavior of Epoxy-Quartz: MD Nanoindentation and Nanoscratching Study", Acta Geotechnica 2024) = `wei2024`
(doi 10.1007/s11440-024-02503-9).

## Contents

- `main.tex` / `main.pdf`: the whole article in reading order: journal line, title, authors, affiliations,
  correspondence, dates, funding, keywords, abstract, the p. 1 footer (licence, copyright, journal/DOI line, placed
  after the abstract), Sections 1–4 with Equations (1)–(15), Tables 1 and 2, Figures 1–17 with captions and
  descriptions, author contributions, acknowledgments, conflicts of interest, data availability statement,
  65 references, and the Supporting Information list.
- `figures/`: every figure rendered at 300 dpi (`fig1.png` … `fig17.png`, the embedded image's native resolution);
  per plotted panel `<panel>.csv`, `<panel>.py` (re-plot from the CSV only) and `<panel>_replot.png`; one
  extraction script per figure image (`fig3_extract.py`, `fig6_extract.py`, `fig7_extract.py`, `fig10_extract.py`,
  `fig11_extract.py`, `fig13_extract.py`, `fig14a_extract.py`, `fig16_extract.py`, `fig17_extract.py`,
  `fig9a_extract.py`, `fig15_extract.py`). The colour-mapped atom renderings with a colour key (Fig. 9a, Fig. 15) are
  given as gzipped per-pixel CSVs (`fig9a.csv.gz`, `fig15.csv.gz`).
- `tables/table1.csv`, `tables/table2.csv`.
- `tools/`: `digitize_common.py` (copied from the osmium tools) and helpers written for this paper
  (`hue_key.py`, plus the `figA_*`, `figB_*`, `figC_*` modules of the figure groups). Scripts import them with
  `sys.path.insert(0, <folder>/tools)`.
- `decomp.sty`: copied from the osmium tools, so `main.tex` compiles stand-alone.
- `work/`: scratch (page renders, embedded images, overlays `*_overlay.png`, side-by-side comparisons `cmp_*.png`,
  `crosscheck_fig16_fig17.py`). May be deleted; scripts recreate what they need.

Compile: `lualatex -interaction=nonstopmode -halt-on-error main.tex` (twice) from this folder.
Re-run the data: `python3 -I -B figures/<fig>_extract.py`, then `python3 -I -B figures/<panel>.py`, from this folder
or any other (all paths are relative to the scripts). The extraction scripts read the embedded images straight from
`source/wei2025.pdf` with PyMuPDF.

## Figures

All 17 figures are raster images embedded at 300 ppi (some JPEG, some lossless); `get_drawings()` finds only text
rules on every page, and no figure text is in the text layer. So no panel is tier 2, and the authors' data archive
(`nag4021-sup-0008-Data.zip`, tier 1) is not here: **every plotted panel is tier 3 (digitized)**. Each panel is
calibrated on its own tick marks, found in the image by code (residuals in each CSV header). Origin line+symbol
plots: the symbols are the data samples, so symbol centres are given wherever they can be separated (template
matching against the legend symbol, distance-transform peaks, colour masks), with the drawn line as per-column
traces where useful; hidden or merged symbols are left out or flagged, never interpolated.

**Checks:** every extraction draws its points back onto the source image (`work/*_overlay.png`), and every replot
was put next to the original panel with `tools/compare.py` (`work/cmp_*.png`); all of them were looked at, by me
or by the helper agent that made the panel (three helper agents did Figs. 3/6, 7/10/14a/17 and 11/13; I did 9a,
15, 16 and re-viewed a sample of theirs: cmp_fig3b, cmp_fig6f, cmp_fig7a, cmp_fig10d, cmp_fig13d). All figure crops
(`figures/fig1.png` … `fig17.png`) were viewed before writing the descriptions.

**Colour-keyed atom renderings** (Fig. 9a, Fig. 15: shear strain, key 0–0.4) are given per pixel, read through the
printed key by hue (`tools/hue_key.py`; the atoms are shaded spheres, so brightness is ignored). Figs. 8, 9b, 12, 14b
and 17 (snapshots) have no key of their own or are overlaid with grey mesh: description only.

| panel | type | data | tier | notes |
|---|---|---|---|---|
| Fig. 1a–c | MD snapshots/schematic of the system (side views, top view) | – | – | dimensions transcribed in `\alttext` |
| Fig. 2a, b | atom models of the six indenters | – | – | atom counts in `\alttext` |
| Fig. 3a | line+symbol plot, total energy vs time | `figures/fig3a.csv` | 3 | trace + 94 symbol centres |
| Fig. 3b | line+symbol plot, temperature vs time (2 series) | `figures/fig3b.csv` | 3 | traces + 101 Newtonian-layer symbols; thermostat symbols not separable |
| Fig. 4a–c | MD snapshot sequence (12 frames) | – | – | |
| Fig. 5a–c | indenter geometry schematics | – | – | |
| Fig. 6a–f | line+symbol plots, Fz vs hz (loading/holding/unloading loops) | `figures/fig6a.csv` … `fig6f.csv` | 3 | symbols ~1 Å apart; holding stacks at 45 Å as top/bottom rows; line runs per column |
| Fig. 7a, b | line plots, 6 series vs time | `figures/fig7a.csv`, `fig7b.csv` | 3 | hidden stretches left empty (e.g. Pyramid-0° in 7b mostly under Pyramid-45°) |
| Fig. 7c | line plot, 4 force components vs time | `figures/fig7c.csv` | 3 | |
| Fig. 7d | line+symbol plot, total energy change | `figures/fig7d.csv` | 3 | only 31 free-standing symbols listed (incomplete) |
| Fig. 8 | MD snapshots, shear strain (no key) | – | – | |
| Fig. 9a | six colour-keyed atom maps (shear strain) | `figures/fig9a.csv.gz` | 3 (colour map) | per pixel, via key hue |
| Fig. 9b | six surface-mesh views | – | – | grey mesh overlay; description only |
| Fig. 10a, b | line+symbol plots, Er / H vs hc (6 series) | `figures/fig10a.csv`, `fig10b.csv` | 3 | line traces + separable symbols + line at whole Å |
| Fig. 10c, d | bar charts | `figures/fig10c.csv`, `fig10d.csv` | 3 | bar tops ±0.01 GPa |
| Fig. 11a–f | dashed line+marker plots, Fx/Fy/Fz vs sliding distance | `figures/fig11a.csv` … `fig11f.csv` | 3 | markers at each 1 Å sample; weak/hidden rows flagged |
| Fig. 12 | MD snapshots, shear strain (no key) | – | – | |
| Fig. 13a–f | as Fig. 11, all systems at hc = 4 Å | `figures/fig13a.csv` … `fig13f.csv` | 3 | 13c is the same run as 11a (agree to 0.03 nN rms) |
| Fig. 14a | category point plot, |mean sliding force| | `figures/fig14a.csv` | 3 | |
| Fig. 14b | MD snapshots (no key) | – | – | |
| Fig. 15 | colour-keyed atom renderings of the six indenters | `figures/fig15.csv.gz` | 3 (colour map) | per pixel, via key hue |
| Fig. 16a–f | scatter + printed linear fits, Fx/Fy/Fz vs hc | `figures/fig16a.csv` … `fig16f.csv` | 3 | all 108 markers; refitted slopes match the printed ones to ≤ 0.003 |
| Fig. 17 (plot) | scatter, friction coefficient vs hc/R, broken y axis | `figures/fig17.csv` | 3 | 24 symbols; x matches hc/R to 0.002 |
| Fig. 17 (right) | two MD snapshots | – | – | |

Totals: 38 data panels, all tier 3 (36 plotted panels + 2 colour-keyed renderings); 0 tier 1, 0 tier 2, 0 tier 4.
Description-only image panels: Figs. 1, 2, 4, 5, 8, 9b, 12, 14b, 17 (right).

**Internal consistency checks (my work, not in the paper):**
- Fig. 16 vs printed fits: straight-line fits through the digitized markers reproduce all 11 printed slopes within
  0.003 and intercepts within 0.04 nN (CSV headers).
- Fig. 16 = run means of Figs. 11/13: the Fig. 16c points equal the means of the Fig. 11a–f traces over sliding
  distance > 10 Å to within 0.04 nN; Figs. 16b, d, e, f at hc = 4 Å match the Fig. 13b, d, e, f means within
  0.06 nN; Fig. 16a (Fy −1.24 nN) matches the Fig. 13a mean over the whole run (−1.25) rather than beyond 10 Å (−1.33).
- Fig. 17 = |Fy/Fz| from Fig. 16 (`work/crosscheck_fig16_fig17.py`): 23 of 24 points agree within 0.03.
- Fig. 10c/d bars agree with the means of the Fig. 10a/b traces over hc 15–25 Å to within about 0.2 GPa.
- Fig. 7c: the "overall" curve equals the root-mean-square √((Fx²+Fy²+Fz²)/3) of the three components (mean
  residual 0.05 nN), as the caption's "squared mean" suggests, not the vector magnitude.


## Text check

`check_text.py` version 2026-10-17j, no options:
`python3 -I -B …/tools/check_text.py main.tex source/wei2025.pdf`

| file | coverage of PDF tokens | without text repeated on ≥ 3 pages | running text (also without in-figure text) | tex tokens found in PDF | MISSING ≥ 6 | EXTRA ≥ 6 |
|---|---|---|---|---|---|---|
| `main.tex` | 90.1 % | **99.8 %** (933 repeated tokens) | 99.8 % (0 in-figure tokens: all figure text is raster) | 99.9 % | 0 | 0 |

Repeated text left out on purpose: page numbers "N of 2964", the running header/footer journal line, and the Wiley
download/terms stamp in the right margin of every page.
With `--min-run 1`: 12 MISSING runs (17 tokens) and 9 EXTRA runs (12 tokens), all explained: real hyphens at line
ends that the tool joins ("z-directions", "quartz-indenter", "graphite-hexagonal", "y- and"), reference 36's
"Simulations" split across pp. 15/16, and equation tokens (the superscript "loading/step" of Eq. 3, subscript "i",
"Vol", squared terms in Eqs. 12, 15) that tokenize differently in the PDF's math fonts and in LaTeX math.

`glyph_audit.py source/wei2025.pdf --crops work/glyphs`: **0 hidden glyphs** (nothing to check). The text layer
holds ∼, ×, ±, ∞, ◦ (degree), Greek and math italics as real Unicode; ∼ (5×), × (6×) and ± (2×) are in main.tex.

Read-through against the page images (spec step 4) done for: Equations (1)–(15) (fractions, the √ in Eq. 15,
subscripts c/r/i/max, superscripts T, Mises, Vol, the "loading/step" stacked index of Eq. 3), Greek (σ, ε, φ, θ, α,
η, γ, π), Å, °, ∼, ×, ±, ∞, en dashes in ranges, both tables cell by cell, italics of x/y/z-directions and
*m*-phenylenediamine, and the order of text around figures. Equation operators are written `\mathrm{tan}` so the
checker sees them.

Placement: Figures sit after the paragraph spanning their page break. Pages 7 and 12 hold only figures, so their
`\pdfpage` markers follow the markers of pp. 8 and 13 (noted in main.tex).

Compiles with lualatex without errors (run twice); only small overfull boxes (0.8 pt from the `\alttext` frames,
17 pt from the long keyword line).


## Errors and oddities in the paper

Kept verbatim in main.tex; flagged with `\decompnote` where noted.

- **Table 2 and Fig. 10 disagree** (flagged): Table 2 gives Er "1.84–6.17" GPa (MD) and H "1.90–2.04" GPa ("See
  Figure 10d"); the abstract and Conclusion 2 repeat 1.84–6.17 GPa. The Fig. 10c bars span 1.83–6.40 GPa (tallest:
  Pyramid-45°, 6.40) and the Fig. 10d bars 1.90–2.14 GPa (Sphere R = 20 Å at 2.14, clearly above the 2.0 tick);
  calibration residuals 0.01 / 0.001 GPa. E "1.58–5.29" = (1.84–6.17) × (1 − 0.377²), so it inherits the mismatch.
- **Sphere R = 10 Å at hc = 4 Å is inconsistent across figures:** Fig. 16d (Fy −2.48, Fz 1.88 nN) and the Fig. 13d
  trace (mean Fy −2.5 nN beyond 10 Å) agree with each other, but Fig. 14a gives |mean Fy| 1.81 nN and Fig. 17 gives
  a friction coefficient of 0.92 instead of 2.48/1.88 = 1.32. Both 14a and 17 fit an Fy of about −1.75 nN. The other
  23 points of Fig. 17 match |Fy/Fz| from Fig. 16 within 0.03.
- Section 2.4: "as shown in Equations (12, 13) [39]" refers to the strain equations, which are numbered (14) and (15)
  (flagged).
- Section 2.3 refers to "the section “Code availability”", which the paper does not have; the closest is the Data
  Availability Statement (flagged).
- The text after Eq. (15) defines η_i^Vol (volumetric strain), but no equation for it is given.
- Section 3.1.1: "When hz varied between 0 and 20 Å … Fz were close to 0"; in Figs. 6c–f (spheres) Fz starts to rise
  at hz ≈ 18 Å (Fig. 7a/b: interaction starts at about 15–21 ps). Minor.
- Fig. 6 caption writes F_Z (capital subscript) where the text has F_z; Fig. 17 caption also "F_Z".
- Fig. 17 y-axis title "Friciton coefficient" (typo). Keywords: "nanoscractching" (typo). Ref. 34: "Fast Paraller
  Algorithms" (typo for Parallel). Ref. 56: page range "76101–76102" (an article number, not pages). Refs. 3 and 65
  give the journal as "International Journal for Numerical and Analytical Methods" (missing "in Geomechanics").
- Author contributions spell "Yuan-Yuan Zheng"; the byline has "Yuanyuan Zheng".
- Fig. 1c labels the long side of the top view (288.559 Å) as x and the short side (144.381 Å) as y, while Fig. 9
  draws the same boxes with x horizontal (short side) and y vertical (long side); the text says the indenter slides
  along y. Possibly a mislabelled triad in Fig. 1c. (My observation.)
- Fig. 1a gives the system as 234216 atoms = 228,000 epoxy atoms (text) + 6216 atoms of the R = 25 Å indenter
  (Fig. 2b): consistent.
- Fig. 17: the red dashed 1.0 line is drawn over two symbols (R = 10 Å at 0.7, R = 25 Å at 1.0).
- Background knowledge (mine, not checked against a source and not in the .tex): Eq. (9) is the projected area of a
  spherical cap and Eq. (10) the Hertz relation; neither has an error as printed.

## Known limits of the data

- No tier-1 data: `nag4021-sup-0008-Data.zip` (Supporting File 8) and the SuppMat .docx are not on this machine.
- Fig. 7d: only symbols standing free of the line (31) are listed. Figs. 10a/b: symbols only where separable.
  Figs. 7a/b, 10a/b: stretches of lines hidden under other series have no data.
- Fig. 6: holding-stage stacks are given only as top/bottom; a few symbols under the shaded ellipses of 6a are missing.
- Fig. 3b: the Thermostat-layer trace near t = 0–12 ps overlaps the red curve and is unreliable.
- Figs. 11/13: dense panels (11a, 13a–c) have weak or missing Fx rows where open squares overlap (flagged);
  11e Fz at 1 Å and 13f Fz at 2 Å touch the top frame (flagged as possibly clipped).
- Fig. 9a / 15 colour maps: values per pixel of a rendering, not per atom; JPEG chroma blur at atom edges; the deep
  red of the strongly strained atoms reads as 0.388 (the hue of the key's last sampled columns), not exactly 0.4.


## Time

About 1 h 40 min wall time (2026-10-18), with three helper agents for Figs. 3/6, 7/10/14a/17 and 11/13 running in parallel.
