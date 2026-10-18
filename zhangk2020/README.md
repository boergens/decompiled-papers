# zhangk2020: decompiled

Kai Zhang, Yindi Cai, Yuki Shimizu, Hiraku Matsukuma and Wei Gao. "High-Precision Cutting Edge Radius
Measurement of Single Point Diamond Tools Using an Atomic Force Microscope and a Reverse Cutting Edge Artifact."
*Appl. Sci.* **2020**, *10*, 4799. DOI [10.3390/app10144799](https://doi.org/10.3390/app10144799) (printed in the
page-1 footer; Crossref record matched to this PDF in verify-sources receipt vs-20261013-9fdbb8613f and seven
others listed in the whitepaper's References). Received 28 May 2020; accepted 6 July 2020; published 13 July 2020.

**Licence:** © 2020 by the authors, Licensee MDPI, Basel; open access under CC BY 4.0, as stated on p. 14.

## Source files

| file | what it is |
|---|---|
| `source/zhangk2020.pdf` | the article, 14 pp., **publisher version of record** (MDPI typesetting, pdfTeX, running header "Appl. Sci. 2020, 10, 4799" and "n of 14"). Copied from `papers/zhangk2020/zhangk2020.pdf`. SOURCE.txt: "Fetched 2026-10-13 via browser slot 1 (UIC access) from https://www.mdpi.com/2076-3417/10/14/4799/pdf (Download PDF link on article page); %PDF and title checked." |

`papers/zhangk2020/` also holds `zhangk2020.pdf.notpdf` (an earlier failed download, ignored) and `zhangk2020.txt`
(an earlier text extraction, not used).

**Hidden text in the PDF.** Every figure is embedded as a page of the authors' Word manuscript (with line numbers),
clipped to the figure. The clipped-away manuscript text stays in the PDF text layer, invisibly, around each figure:
pdftotext and PyMuPDF return it (line numbers such as 95–126, 152–176, 225–261, and duplicates of nearby
paragraphs, sometimes in an older wording, e.g. "Bruker, Billerica, USA" and "MicroSense, Lowell, Massachusetts,
USA" where the printed text reads "MA, USA"). It is not part of the printed article and is not transcribed. This is
why the text check stays below 98 % (below).

## Contents

- `main.tex` / `main.pdf`: the whole article in reading order: journal block, title, authors, affiliations,
  dates, abstract, keywords, Sections 1–4, Equations (1)–(6), Table 1, Figures 1–13, author contributions,
  funding, conflicts of interest, references 1–27, licence. Compile from this folder:
  `lualatex -interaction=nonstopmode -halt-on-error main.tex` (twice); compiles without errors (a few overfull lines
  from long e-mail addresses).
- `figures/`: every figure rendered at 200 dpi (`fig1.png` … `fig13.png`; Figure 3 is split over pp. 5–6 as
  `fig3a.png`, `fig3b.png`); per plotted panel `<panel>.csv`, `<panel>_extract.py`, `<panel>.py`, `<panel>_replot.png`.
- `tables/table1.csv`: Table 1.
- `tools/vec.py`: helpers for the vector extractions (frame, tick and marker finding, axis fit, overlay);
  `tools/digitize_common.py`: copy of the shared raster helpers. Scripts import them relative to themselves.
- `work/`: scratch (page renders, embedded images, overlays `*_overlay.png`, side-by-side comparisons `cmp_*.png`,
  check JSON, `figblocks.py` that inserted the figure blocks). May be deleted.

Re-run the data: `python3 -I -B figures/<panel>_extract.py`, then `python3 -I -B figures/<panel>.py` (any working
directory; all paths are relative to the scripts).

## Figures

The plots of Figs. 5, 6b, 8, 10–13 are **vector drawings** (tier 2): frame and ticks are thin filled rectangles,
tick labels are text, markers are stroked paths, so marker centres and line vertices come out exactly; the axis
fits on the labelled ticks have residuals ≤ 0.04 in axis units (in each CSV header). Figs. 4b and 7b are
**raster** (300-ppi JPEGs, tier 3). Several panels (4b, 5, 6b, 7b) have no tick numbers, only "nm/div." or
"s/div." scales; their CSVs give values from the lower left frame corner (arbitrary origin) and list the tick
positions.

Checks: every extraction draws its points back onto the source (vector: on a 300-dpi render of the PDF region,
`work/fig*_overlay.png` and `work/overlay_montage.png`; raster: on the embedded image, `work/fig4b_overlay.png`,
`work/fig7b_overlay.png`), and every replot was put next to the original with `compare.py` (`work/cmp_*.png`). I
looked at all of them: points sit on the markers and lines, ranges and scales match. Further checks against the
paper's own numbers (in the CSV headers):

- Fig. 8: R_tool_m = 40.32 nm at all depths; (R_tool_m + R_mark_m)/2 − R_tool ≤ 0.04 nm; mean R_tool 30.39 nm (text 30.38 nm).
- Fig. 11: SD of the uncertainties 0.0052 nm (text 0.005 nm).
- Fig. 12: mean radius 29.67 nm, SD 0.164 nm, SD of uncertainties 0.028 nm (text 29.67, 0.16, 0.028).
- Fig. 13: depths 35.0, 45.0, 77.0, 104.0, 127.0, 163.1 nm (text 35, 45, 77, 104, 127, 163); mean 41.29 nm, SD 0.66 nm, SD of uncertainties 0.033 nm (text 41.29, 0.66, 0.032).
- Fig. 6b: circle through the fitted-curve vertices, radius 41.1 nm (label 40.32 nm). Fig. 7b: circle through the
  digitized black arc, radius 21.2 nm (label 21.04 nm).

| panel | type | data | tier | notes |
|---|---|---|---|---|
| Fig. 1 | schematic (three steps, two insets) | – | – | raster image |
| Fig. 2 | schematic (nanoindentation system) | – | – | vector |
| Fig. 3a | schematic (tool positions, steps) | – | – | vector, p. 5 |
| Fig. 3b | schematic signal plot, no scales | – | – | vector, p. 6; no numerical axes |
| Fig. 4a | AFM 3D topography with photo inset | – | – | no colour key |
| Fig. 4b | line profile (nm/div scales) | `figures/fig4b.csv` | 3 digitized | arbitrary origin |
| Fig. 5 | two step traces, two y axes (nm/div, s/div) | `figures/fig5.csv` | 2 vector | line edges per 0.25 pt bin; arbitrary origins |
| Fig. 6a | AFM 3D topography | – | – | no colour key |
| Fig. 6b | profile: circles, line, fitted arc (nm/div) | `figures/fig6b.csv` | 2 vector | arbitrary origin |
| Fig. 7a | AFM 3D topography | – | – | no colour key |
| Fig. 7b | profile: circles, line, fitted arc (nm/div) | `figures/fig7b.csv` | 3 digitized | arbitrary origin; 14 arc columns flagged (arrowhead) |
| Fig. 8 | scatter, 3 series | `figures/fig8.csv` | 2 vector | |
| Fig. 9 | schematic (contact area) | – | – | vector |
| Fig. 10 | line with markers | `figures/fig10.csv` | 2 vector | |
| Fig. 11 | scatter | `figures/fig11.csv` | 2 vector | |
| Fig. 12 | scatter, two y axes | `figures/fig12.csv` | 2 vector | |
| Fig. 13 | scatter, two y axes | `figures/fig13.csv` | 2 vector | |

Tiers: 7 panels tier 2, 2 panels tier 3, none tier 1 (the paper names no data set or supplement).

## Text check (`check_text.py` 2026-10-17j, no options)

`python3 -I -B .../tools/check_text.py main.tex source/zhangk2020.pdf`

| coverage of PDF tokens | without text repeated on ≥ 3 pages | also without in-figure text | tex tokens found in PDF | MISSING ≥ 6 | EXTRA ≥ 1 |
|---|---|---|---|---|---|
| 93.0 % | 94.4 % (162 repeated tokens) | 95.4 % (119 in-figure tokens) | 100.0 % | 20 runs, 168 tokens | 0 |

All remaining MISSING tokens (479 at `--min-run 1`) are explained, none is article text left out:
- 222 bare numbers: line numbers of the hidden manuscript text (above);
- 28 single "r": hidden copies of R with a subscript, split differently from the visible text;
- 229 other tokens: axis titles and tick labels of the vector plots that the checker does not recognize as
  in-figure text (e.g. "Output of inside sensor 110 nm/div.", "Evaluated Radius nm 0 20 40 60", "1.90 1.95 2.00",
  Fig. 3b "Output of sensor"; all are in `\alttext`), and fragments of the hidden manuscript text (e.g.
  "3. Experiment and Discussion", "MicroSense, Lowell, Massachusetts, USA", "Then, … 4. Summary" duplicates,
  the hidden Equation (6) "d er … 4").
- REPEATED: running header "Appl. Sci. 2020, 10, 4799" / "n of 14" (boilerplate) and axis labels repeated
  across the plot pages.

EXTRA: none, at any run length. Read-through against the page images done for the equations (1)–(6), sub- and
superscripts (R_tool, R_tool_m, R_mark_m, d_depth, d_in, d_out, d_er, ×10⁻⁵, ×10⁻⁴), ξ, ν, π, ×, µm, ≤, en dashes in
ranges and citations, Table 1 cells, and the reference formatting (journal italic, year bold, volume italic).
The coordinator can exclude nothing by rectangle here: the hidden text overlaps the visible text.

## Errors and oddities in the paper (kept verbatim)

- Abstract: "reverse cutting edFigurege artifact" (the word "Figure" pasted into "edge"); flagged in main.tex.
- Equation (4) prints R_tool = (R_tool_m + R_mark_m)/(2 − ξ). Combining Equations (1)–(3) as printed gives
  R_tool = (1 − ξ)(R_tool_m + R_mark_m)/(2 − ξ) (decompiler's algebra). The two agree for ξ = 0, the only case
  the paper evaluates (30.68 nm = (40.32 + 21.04)/2). Flagged in main.tex.
- Table 1: the two combined uncertainties look swapped. Root-sum-square of the listed standard uncertainties
  (decompiler's arithmetic) gives 1.42 nm for the R_tool_m block (0.56, 1.2, 0.2, 1.9×10⁻⁵, 0.46) and 1.36 nm for the
  R_mark_m block (0.56, 1.2, 0.2, 2.8×10⁻⁵, 0.12, 0.21, 5.7×10⁻⁴); the table and the text give 1.36 and 1.42 nm.
  The final 1.97 nm (k = 2) is unaffected: 2 × ½ √(1.36² + 1.42²) = 1.97 nm.
- Fig. 4b / text: "the Root Mean Square (RMS) roughness of the section A–A’ … 2.43 nm". In the printed profile
  (5 nm/div) the RMS of the trace about its mean is 0.40 nm; the "2.43 nm" annotation spans the two short lines at
  the highest peak and a low valley, about 2.7 nm on the printed scale, i.e. it marks a peak-to-valley height, not an
  RMS (decompiler's measurement, `fig4b.csv` header).
- Fig. 5: the arrow labelled "52 nm" spans about 56 nm on the printed 110 nm/div scale, the "27 nm" dip is about
  28 nm on the 50 nm/div scale (`fig5.csv` header). Small; the scale labels are round numbers.
- Fig. 10 has a stray small mark below the x axis between 60 and 100 (a "5" in the text layer).
- Typos kept: "experiments are preformed", "steeping motor controller" (stepping), "measured revered cutting edge"
  (reversed), "researches".
- The text says the indentation depth "was set at approximately 20 nm" intervals from 20 to 180 nm; Figs. 8, 11
  and 12 show six depths at about 29, 44, 62, 84, 125 and 157 nm.

## References in our collection

From `decompile_work/manifest.json`: ref. 15 (Asai et al. 1990, CIRP Ann.) = `asai1990`. No other cited work is
among the manifest keys.

## Not available

The paper names no data set, source data or supplement. AFM raw data behind Figs. 4, 6, 7 are not published.
