# fu2025: decompiled

Guoyu Fu, Jia Ge, Hao Li, Fengzhen Sun, Weizhou Wu. "Finite Element Analysis and Experimental Investigation on
the Machinability of PMMA/CNT Composites via Nanosectioning." *Polymers* **2025**, 17, 2441.
DOI [10.3390/polym17182441](https://doi.org/10.3390/polym17182441) (printed on p. 1).
Received 1 July 2025; revised 25 August 2025; accepted 27 August 2025; published 9 September 2025.
Academic editor: Alexander Malkin.

**Licence:** © 2025 by the authors; licensee MDPI, Basel. Open access under the Creative Commons Attribution (CC BY 4.0)
licence, as stated on p. 1.

**Version:** publisher's version of record (MDPI typeset PDF, 19 pages, "Polymers 2025, 17, 2441" running header).
The DOI is printed in the PDF; it is also confirmed by verify-sources receipt `vs-20261013-f8bbe2729c` (Crossref
record for 10.3390/polym17182441 matched to this PDF, sha256 `eb6d30d6…b6ec2`, identical to `source/fu2025.pdf`).

## Source files

| file | what it is |
|---|---|
| `source/fu2025.pdf` | the article, 19 pp., copied from `papers/fu2025/fu2025.pdf`. `papers/fu2025/SOURCE.txt`: "Fetched 2026-10-13 by the lead session (oct-12-epoxy-cutting) from NCBI's PMC Open Access bucket: https://pmc-oa-opendata.s3.amazonaws.com/PMC12473824.1/PMC12473824.1.pdf (%PDF checked)." |

`papers/fu2025/fu2025.txt` (an earlier text extraction) was not used. The paper has no supplementary material.
Its Data Availability Statement says "The original contributions presented in this study are included in the
article"; no data set is named, so there is no tier-1 source to miss.

**Cited works in our collection** (from `decompile_work/manifest.json`, matched by journal, volume and pages):
ref. 44 (Sun & Gamstedt, Int. J. Mech. Sci. 151, 13–21) = `sun2018ijms`; ref. 67 (Patel, Blackman & Williams, Eng.
Fract. Mech. 76, 2711–2730) = `patel2009`. (`atkins2005` in the collection is a different Atkins 2005 paper, in
Int. J. Mech. Sci.; ref. 66 is in Eng. Fract. Mech.)

## Contents

- `main.tex` / `main.pdf`: the whole article in reading order: journal block, title, authors, affiliations and
  footnotes, abstract, keywords, the left-margin block of p. 1 (editor, dates, citation, copyright), sections 1–6,
  Equations (1)–(39), Tables 1–2, Figures 1–12 with captions, descriptions and data links, author contributions,
  funding, IRB statement, data availability, acknowledgments, conflicts of interest, references 1–69 and MDPI's
  disclaimer. Running headers ("Polymers 2025, 17, 2441", "n of 19") left out.
  Compile from this folder: `lualatex -interaction=nonstopmode -halt-on-error main.tex` (twice); compiles without
  errors (a few overfull lines from long reference entries).
- `figures/`: every figure rendered at 200 dpi (`fig1.png` … `fig12.png`); CSVs, extraction scripts, plot scripts
  and replots for the plotted panels (below).
- `tables/table1.csv`, `tables/table2.csv`: the two tables, caption in `#` lines.
- `tools/`: helper modules imported by the figure scripts: `digitize_common.py` (copy of the osmium tool),
  `lineplot.py` (colour classification and run tracing for the multi-colour line plots, written here),
  `strips.py` (stacks figures stored as many image strips, written here), `fe_mises.py` (12-band Abaqus contour
  classifier, adapted from `oct_17_papers/sun2019/tools/fe_contour.py`).
- `work/`: scratch (page renders, embedded images, overlays, comparisons `cmp_*.png`, classified maps). May be deleted;
  the extraction scripts recreate what they need.

Re-run the data: `python3 -I figures/fig7_extract.py`, `fig8_extract.py`, `fig9_extract.py`, `fig11_extract.py`
(the last writes Figs. 10 and 11), then `python3 -I figures/fig7.py`, `python3 -I figures/fig7.py fig8a fig8b fig8c fig8d`,
`python3 -I figures/fig9.py`, `python3 -I figures/fig11.py`. All paths are relative to the scripts.

## Figures

All figures are raster images (JPEG or Flate, 300–600 ppi); the PDF holds no vector plot data (`get_drawings()`
finds only rules and equation strokes). Figure 2 (34 strips) and Figure 9 (21 strips) are stored as horizontal image
strips; `tools/strips.py` stacks them. No two embedded images are identical (digest check over all pages).

| panel | type | data | tier | notes |
|---|---|---|---|---|
| Fig. 1a–d | SEM micrographs (fracture surfaces) | – | – | |
| Fig. 2a | photograph (ultramicrotome set-up) | – | – | |
| Fig. 2b | schematic (orthogonal cutting) | – | – | |
| Fig. 3a, b | schematics (chain alignment; rheological model) | – | – | |
| Fig. 4a | SEM micrographs | – | – | taken from ref. [49] per caption |
| Fig. 4b, c | schematic; FE model screenshot | – | – | |
| Fig. 5 | flow chart | – | – | transcribed in `\alttext` |
| Fig. 6 | schematic (CNT placements, θ) | – | – | |
| Fig. 7a | line plot, 6 series (experimental force vs time) | `figures/fig7a.csv` | 3 digitized | |
| Fig. 7b | line plot, 6 series (simulated, plain PMMA) | `figures/fig7b.csv` | 3 digitized | identical to Fig. 8d, see errors |
| Fig. 8a–d | line plots, 6 series each | `figures/fig8a.csv` … `fig8d.csv` | 3 digitized | |
| Fig. 9 | line plot with markers and error bars, 5 series | `figures/fig9.csv` | 3 digitized | markers from connecting lines; caps hand-guided and snapped |
| Fig. 10 left, right | FE contour maps (S, Mises) with 12-band key | `figures/fig10left.csv`, `fig10right.csv` | 3 digitized (classified colour map) | made by `fig11_extract.py`, replotted by `fig11.py` |
| Fig. 11a–f | FE contour maps (S, Mises), each with own key | `figures/fig11a.csv` … `fig11f.csv` | 3 digitized (classified colour map) | |
| Fig. 12a–d | optical images of chips | – | – | taken from ref. [69] per caption |

Per tier: tier 1: 0; tier 2: 0; tier 3: 15 panels (Figs. 7a, 7b, 8a–d, 9, 10 ×2, 11a–f); tier 4: 0.
Image-only panels: 21 (all have `\alttext`).

**Line plots (Figs. 7, 8)**: axes calibrated on the tick marks found in the image (residuals in each CSV header,
≤ 0.9 µs and ≤ 0.05 N/m). Pixels are assigned to series by colour (a pixel = blend of a legend colour with white;
JPEG-darkened edges of the pure blue lines are split from navy at blue channel 160, and black-classified pixels
that are bluish go to navy); small specks and thin slivers (JPEG ringing between two lines) are removed by an
area and erosion test. Each series is given as *runs* per pixel column (centre, top, bottom), so a column can have
several rows; hidden parts are gaps. Checks: every replot was put beside the original with `compare.py`
(`work/cmp_fig7a.png` … `cmp_fig8d.png`) and looked at; per-series overlays (`work/fig7*_series.png`,
`work/fig8*_series.png`, `work/fig7*_overlay.png`) were also inspected. Remaining weakness: where lines of
similar dark colours (black/navy/blue) run together, a few runs may be assigned to the neighbour.

**Fig. 9**: marker centres from straight-line fits to each connecting segment, evaluated at the marker's x (left and
right segments agree within 0.05 N/m). Error-bar caps were placed by hand on 2×–4× zooms (`GUIDE` in the script) and
snapped to the nearest cap bar of the series colour; all 48 caps snapped, and every error bar is symmetric about its
marker within 0.09 N/m, which supports the assignment. Checked with `work/fig9_overlay.png` and `work/cmp_fig9.png`.

**Figs. 10, 11** (Abaqus contour maps with colour keys): one character per pixel at native resolution (band code
`0`–`9`, `a`, `b`; `.` white; `#` unclassified; `X` annotation). The model colours are the key colours × 216/255
(Abaqus shading), measured on both figures. Key values transcribed from 3× zooms of every key; each set is linear
in 12 steps, which confirms the reading. The figure gives no stress unit. Checked with `work/fig1*_classified.png`
and `work/cmp_fig10left.png`, `cmp_fig11a.png`, `cmp_fig11d.png`. The Fig. 10 image (lossless) was resampled
before embedding, so its band boundaries are blurred like the JPEG of Fig. 11.

## Text check (`check_text.py` version 2026-10-17j, no options)

`python3 -I -B …/tools/check_text.py main.tex source/fu2025.pdf`

| file | coverage of PDF tokens | without text repeated on ≥ 3 pages | also without in-figure text | tex tokens found in PDF | MISSING ≥ 6 | EXTRA ≥ 6 |
|---|---|---|---|---|---|---|
| `main.tex` | 98.4 % | **99.9 %** (126 repeated tokens) | 99.9 % | 100.0 % | 0 | 0 |

With `--min-run 1`: repeated = the running header "Polymers 2025, 17, 2441 … n of 19" (18 pages). MISSING: 9 single
tokens, all explained: equation glyph pieces in the text layer (bracket halves "h", "i", radical "r", "q", fraction
digits "2" in Eqs. (23), (26), (30)–(31), (39)) and "ob"/"served", a line-end hyphen across the page break p. 14/15
("ob-served", written as "observed"). EXTRA: only that "observed".
Real hyphens at line ends kept as hyphens: reinforcement-knife, long-range, thermal-mechanical, high-speed,
three-dimensional, short-fiber-reinforced (the checker joins them; they still match).

Read-through against the page images (step 4) done for all 39 equations (sub/superscripts, dots, primes, the
"InU" in (22)–(23), τ\_α in (33), s\_ss,a in (35)), both tables, Greek letters, °, ±, ×, μm, the √m unit, the
reference list (italic journals, bold years, italic volumes; text-layer errors corrected from the image:
Smoleń, Powęzka, Altintaş, Cieśla, Halilovič).

## Errors and oddities found in the paper

1. **Figure 7(b) and Figure 8(d) show the same curves.** Fig. 7b is captioned as the simulated force of *plain PMMA*,
   Fig. 8d as *PMMA/1.0 wt% CNTs*. The digitized series agree to a median of 0.10–0.20 N/m per 5-µs bin for all six
   thicknesses (`figures/fig7b_fig8d_compare.py`), against 1.5–7.9 N/m for Fig. 7b vs Figs. 8a–c; the saw-tooth with
   drops to 0 near 170, 360, 550, 735 µs is identical. The two images differ in resolution and legend layout, so the
   same data were plotted twice. Which caption is right cannot be told from the paper.
2. **Text vs Figure 9**: p. 13 says the simulated force at 200 nm is "about 30.4 N/m" for plain PMMA and "about
   35.7 N/m" for PMMA/1.0 wt% CNT; Fig. 9 shows about 33.0 and 48.3 N/m. The experimental 55.3 and 72.9 N/m (used for
   the "31.8%"/"32%" increase in the abstract and conclusions) appear in no figure; Fig. 7a (experiment, plain PMMA)
   stays below about 40 N/m at all thicknesses.
3. **Citation numbers that do not match the named works**: "Kumar et al. [15]" (no Kumar in the list; [15] is
   Mahmoodi), "Mahmoudi et al. [16]" ([16] is Samuel), "Samuel et al. [17]" ([17] is Gong), "Gong et al. [18]"
   ([18] is Weule); "Mulliken–Boyce model [35,36]" ([31] is Mulliken & Boyce; [35], [36] are other works);
   "Arruda–Boyce model [30]" ([30] is a CFRP machine-learning paper); "Gearing–Anand model [42]" (Gearing & Anand is
   [41]). Table 1 cites [41] (Gearing & Anand) for Mulliken–Boyce parameters.
4. Table 1 is captioned "Epoxy material parameters" in a section about PMMA; first row subscript "0,a" (Latin a);
   N (limiting chain extensibility) given the unit m^−1/2.
5. Equations: (1) printed as x/X without ∂; (22)–(23) "InU" vs "lnU" in the text; (33) uses τ\_α for the β process;
   (32)–(33) write the pressure coefficient α\_α+β, the text α\_p,i; (35) s\_ss,a vs s\_ss,β in (37).
6. "As shown in Figure 5, θ is the disorientation angle": θ is drawn in Figure 6.
7. Section 4.5 gives the CNT Poisson's ratio as −0.38 [46]; ref. [46] is a paper on random sequential adsorption.
   (Kept as printed; noted only because the value is unusual. Background knowledge, not from the paper: a negative
   Poisson's ratio is not a usual value for CNTs.)

All are kept verbatim in `main.tex`, flagged with `\decompnote` where they occur (items 1–6).

## Known problems

- Digitized line plots (Figs. 7, 8): parts of series hidden under other lines are missing; at crossings of
  black/navy/blue a few runs may be misassigned (documented in the CSV headers).
- Fig. 9: the thin grey bars inside some Plain-PMMA error bars (a second, shorter bar?) were not extracted; the figure
  does not say what the error bars are.
- Contour maps: band boundaries uncertain by 1–2 px (blurred sources); stress unit not given in the figures.
