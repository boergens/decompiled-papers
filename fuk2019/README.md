# fuk2019: decompiled

Kexin Fu, Qing Xie, Fangcheng LÜ, Qijun Duan, Xinjie Wang, Quansheng Zhu, Zhengyong Huang. "Molecular
Dynamics Simulation and Experimental Studies on the Thermomechanical Properties of Epoxy Resin with
Different Anhydride Curing Agents." *Polymers* **2019**, *11*, 975. DOI
[10.3390/polym11060975](https://doi.org/10.3390/polym11060975) (printed in the p. 1 footer).
Received 23 April 2019; accepted 27 May 2019; published 3 June 2019.

**Licence:** © 2019 by the authors, licensee MDPI, Basel; open access under CC BY 4.0
(http://creativecommons.org/licenses/by/4.0/), as stated on p. 15.

DOI check: the verify-sources receipts `vs-20261013-fe80a3eee0` (and others listed in our whitepaper's
References) carry a Crossref `doi_record` for 10.3390/polym11060975 (title, authors, *Polymers* 11(6) 975,
not retracted) for a PDF of 5 185 550 bytes with SHA-256 `50965929…93e8f8`, which is the same file as
`source/fuk2019.pdf`.

## Source files

| file | what it is |
|---|---|
| `source/fuk2019.pdf` | the article, 15 pp. **Publisher version of record** (MDPI typesetting, pdfTeX, running header "Polymers 2019, 11, 975 / n of 15"). Copied from `papers/fuk2019/fuk2019.pdf`. `papers/fuk2019/SOURCE.txt`: "Fetched 2026-10-13 by the lead session (oct-12-epoxy-cutting) from NCBI's PMC Open Access bucket: https://pmc-oa-opendata.s3.amazonaws.com/PMC6630713.1/PMC6630713.1.pdf (%PDF checked)." |

(`papers/fuk2019/fuk2019.txt`, an earlier text extraction, was not used and not copied.)

The paper names no supplementary material and no data set, so there is no tier-1 source to miss.

PDF oddities (no effect on the content):
- Every figure is placed as a clipped piece of a page of the authors' peer-review manuscript: the text layer
  holds invisible, clipped-away copies of that manuscript's header "Polymers 2019, 11, x FOR PEER REVIEW"
  (pp. 4, 6–11; check_text lists it as repeated text) and `pdftotext` also prints clipped manuscript
  paragraphs on p. 3. PyMuPDF (used by the checker and here) sees only the visible text.
- On pp. 6, 8 and 10 each figure image is drawn twice, offset by 2–10 pt (same image object); tables on
  pp. 9–12 have doubled rules. The rendered pages look normal.

## Contents

- `main.tex` / `main.pdf`: the whole article in reading order (title block, affiliations, dates, the p. 1
  footer with journal and DOI, abstract, keywords, sections 1–4, equations 1–9, tables 1–5, figures 1–12
  with captions, author contributions, funding, conflicts of interest, 40 references, licence).
  Compile: `lualatex -interaction=nonstopmode -halt-on-error main.tex` (twice) from this folder; it
  compiles without errors (some overfull lines in wide tables and long URLs).
- `figures/`: every figure rendered from the PDF at 250 dpi (`fig1.png` … `fig12.png`, crops without the
  caption); for each plotted panel `<panel>.csv`, `<panel>_extract.py`, `<panel>.py`, `<panel>_replot.png`.
  Extra files: `fig3inset.csv` (written by `fig3_extract.py`, which does both parts of the one image),
  `fig5_bondlengths.csv` (bond lengths printed in Fig. 5), `fig7a_pixels.csv.gz` / `fig7b_pixels.csv.gz`
  (one row per surface pixel) and `fig7a_key.csv` / `fig7b_key.csv` (colour keys).
- `tables/table1.csv` … `table5.csv`: the five tables, captions as `#` comments.
- `tools/`: `digitize_common.py` (copied unchanged from the osmium tools), and helpers written for this
  paper: `fukplot.py` (image loading, white-blend colour classifier, inward tick finder),
  `msdtime.py` (Fig. 9), `scatterfit.py` (Figs. 10, 11), `bondlen.py` (Figs. 3, 4), `surf3d.py` and
  `fig7common.py` (Fig. 7). Scripts import them via a path relative to the script.
- `work/`: scratch (page renders, embedded images, overlays `*_overlay.png`, side-by-side comparisons
  `cmp_*.png`, Fig. 7 camera checks `fig7?_check.png`, logs, `PROGRESS.md`). May be deleted.

Re-run the data: `python3 -I figures/<panel>_extract.py`, then `python3 -I figures/<panel>.py` (any
working directory).

## Figures

All plots are raster images (Origin exports, 220–300 ppi); `get_drawings()` finds only table rules and
equation strokes, no plot paths, so no panel is tier 2, and no source data exist (no tier 1). All 13 plotted
panels are **tier 3 (digitized)**: frame and inward tick marks found in the image, linear axis fit on the
major ticks (residuals in each CSV header, mostly < 0.1 of a pixel), series separated by colour with a
white-blend classifier.

**Checks:** every extraction draws its points back onto the source image (`work/*_overlay.png`; for
Fig. 7 the fitted camera's projected box and grids, `work/fig7?_check.png`) and every replot was put next
to the original with `compare.py` (`work/cmp_*.png`); I looked at all of them. Cross-checks between panels
that show the same data (median absolute difference, density units, 1 px ≈ 0.1–0.13):
Fig. 4b dashed DGEBA-MTHPA vs Fig. 4a red 0.06; Fig. 4b dashed DGEBA-NA vs Fig. 4a black 0.02; Fig. 4b
MTHPA vs Fig. 3 MTHPA 0.12; Fig. 4b NA vs Fig. 3 NA 0.16; Fig. 4a DGEBA vs Fig. 3 DGEBA 0.05 (90th
percentiles up to ~1, on steep peak flanks where ±1 px in x matters). Fig. 12 simulated bars and error bars
(4.136 ± 0.188, 4.873 ± 0.408 GPa) agree with Table 5 (4.14 ± 0.18, 4.87 ± 0.41). The digitized crossing
points of the fitted lines in Figs. 10 and 11 agree with the printed values to 0.2–0.4 K (398.6 vs 398.26,
419.9 vs 419.46, 399.3 vs 399.03, 421.05 vs 421.02).

**Fig. 7 (3D surfaces):** a perspective camera (3×4 matrix, DLT) was fitted on the tick marks of all three
axes (19 and 20 ticks; rms 0.06 / 0.13 px). Independent checks: the fitted box spans 465.4–576.9 (a) and
52.8–949.5 (b) kcal/mol, matching the colour keys (465.5–577.0, 54.00–950.0), and the projected top of the
back box corner lands within 1.3 px of the drawn one. Each surface pixel's energy comes from its colour
(colour key, linear between the top and bottom labels); its (φ1, φ2) from intersecting the pixel's view
ray with the plane of that energy. Limits: only the visible front of each surface is covered; where the
key repeats one colour over many rows (plain red, about 538–558 in (a), 634–797 in (b)) the energy is
uncertain (column `E_err`) and so are the angles (columns `dphi1`, `dphi2`); on flat parts of a surface a
small energy error moves the angles a lot, and the key's discrete colour steps show up as stripes in the
gridded data (gaps between 10° columns in `fig7?.csv`). Box ranges from the fits: φ1 −98.4…29.8°, φ2
−184.3…149.4° (a); φ1 −92.3…86.9°, φ2 −166.6…164.0° (b) (the outer ticks are not at the box ends).

| panel | type | data | tier | notes |
|---|---|---|---|---|
| Fig. 1a–d | reaction schemes (condensed formulas) | – | – | transcribed in `\alttext`, SMILES where possible |
| Fig. 2a | ball-and-stick renderings of 5 molecules | – | – | |
| Fig. 2b | flow diagram | – | – | transcribed |
| Fig. 2c | flow chart (crosslinking program) | – | – | transcribed with all branches |
| Fig. 2d, 2e | renderings of amorphous / crosslinked cells | – | – | |
| Fig. 2f | structural formulas | – | – | SMILES for DGEBA, MTHPA, NA |
| Fig. 3 (main) | line plot, 3 series | `figures/fig3.csv` | 3 digitized | upper/lower line edge per column; hidden parts empty |
| Fig. 3 (inset) | line plot, zoom 1.44–1.56 Å | `figures/fig3inset.csv` | 3 digitized | small (≈240 × 170 px) |
| Fig. 4a | line plot, 3 series | `figures/fig4a.csv` | 3 digitized | |
| Fig. 4b | line plot, 2 solid + 2 dashed | `figures/fig4b.csv` | 3 digitized | solid/dashed separated by component size; dashed only where a dash is clear of the solid line |
| Fig. 5a–c | molecule renderings with bond-length labels | `figures/fig5_bondlengths.csv` | (transcribed) | not a plot |
| Fig. 6a, 6b | molecule renderings, torsions φ1, φ2 | – | – | |
| Fig. 7a | 3D colour-mapped surface + key | `figures/fig7a.csv` (+ `_pixels.csv.gz`, `_key.csv`) | 3 digitized | see above |
| Fig. 7b | 3D colour-mapped surface + key | `figures/fig7b.csv` (+ `_pixels.csv.gz`, `_key.csv`) | 3 digitized | see above |
| Fig. 8a, 8b | renderings of free volume in the cell | – | – | no key |
| Fig. 9a | line plot, 7 temperatures | `figures/fig9a.csv` | 3 digitized | |
| Fig. 9b | line plot, 7 temperatures | `figures/fig9b.csv` | 3 digitized | |
| Fig. 10a | scatter + 2 fitted lines + crossing | `figures/fig10a.csv` | 3 digitized | |
| Fig. 10b | scatter + 2 fitted lines + crossing | `figures/fig10b.csv` | 3 digitized | appears to show MSD at 10 ps (below) |
| Fig. 11a | scatter with error bars + 2 lines | `figures/fig11a.csv` | 3 digitized | |
| Fig. 11b | scatter with error bars + 2 lines | `figures/fig11b.csv` | 3 digitized | |
| Fig. 12 | grouped bar chart with error bars | `figures/fig12.csv` | 3 digitized | lower error-bar halves hidden in the bars, taken as symmetric (stated) |

## Text check (`check_text.py` version 2026-10-17j, no options)

| file | coverage of PDF tokens | without text repeated on ≥ 3 pages | also without in-figure text | MISSING ≥ 6 | EXTRA ≥ 6 |
|---|---|---|---|---|---|
| `main.tex` | 96.8 % | **98.8 %** (208 repeated tokens) | 98.8 % | 7 runs (102 tokens) | 0 |

Explanation of what is not matched (`--min-run 1`):
- Repeated: running header "Polymers 2019, 11, 975 / n of 15" (left out) and the invisible "Polymers 2019,
  11, x FOR PEER REVIEW" headers inside the figure placements (see above).
- MISSING: all runs are display equations (1)–(9) and the inline math after Eq. (5), which the checker
  drops from the .tex (known limitation); the run on p. 10 also takes along the word "where", which is in
  the .tex. The single-token runs are real hyphens at line ends that the checker joins: "DGEBA-MTHPA"
  (6×) and "volume-temperature".
- EXTRA: one 2-token run "i 0" (the summation index of Eq. 5). Coverage of the text itself is ≈ 100 %.

Read-through against the page images done for: subscripts (T_g, E_coh, V_f, V_0, V_T, R_n, R_max, C_ij),
φ1/φ2, ±, Å, g/cm³, J·cm⁻³, en dashes in ranges and citations, equations 1–9 (matrix, braces, fractions),
table layouts (Table 1 two-level heads, Table 4 SV/M rows), and the reference formatting (bold years,
italic volumes and journals).

## Errors and oddities in the paper (kept verbatim; flagged with `\decompnote` where in the text)

1. p. 9: "the FFV of the DGEBA-NA system was higher than that of the DGEBA-MTHPA system" contradicts Table 3
   (14.18 % vs 16.67 %), the abstract ("lower FFV") and conclusion (2).
2. p. 11: "19.83 K higher … when the specific volume-temperature fitting was used": Table 4 / Fig. 11 give
   421.02 − 399.03 = 21.99 K. (The MSD difference 419.46 − 398.26 = 21.20 K vs printed 21.22 K.)
3. Table 5 caption "The T_g of the epoxy systems" over a table of elastic moduli and Poisson's ratio.
4. **Fig. 10b vs Fig. 9b (from the digitized data):** the caption says MSD at 15 ps, and Fig. 10a matches the
   15-ps values of Fig. 9a within 0.01 Å² at all seven temperatures. The Fig. 10b points (0.76, 0.96, 1.23,
   1.59, 2.27, 2.85, 3.09 Å²) are 0.11–0.52 Å² below the 15-ps values of Fig. 9b (0.88, 1.07, 1.40, 1.91,
   2.63, 3.32, 3.61) but within 0.06 of its 10-ps values (0.77, 0.98, 1.25, 1.62, 2.29, 2.90, 3.15). So
   Fig. 10b, and hence T_g(M) = 419.46 K for DGEBA-NA, appear to use MSD at 10 ps.
5. Fig. 5b: DGEBA-MTHPA "C-C5:1.107Å" (the monomer value is 1.485 Å). A C–C bond of 1.107 Å is far below any
   ordinary C–C length (decompiler's background knowledge, not in the paper); probably a typo.
6. p. 6: "C– bonds on benzene rings" (second atom missing).
7. p. 5: accelerator called "DMP-30" and then twice "MPD30"; "with th epoxy resin".
8. p. 3: "Though the above main reactions" (probably "Through"); "Researches have shown".
9. Eq. (9) writes Poisson's ratio as υ (upsilon), the text as ν.
10. Author contributions: "Date curation"; ref. 8 "IEEE Trns."; ref. 34 "J. Appl. Phys" (no period).
11. Ref. 36 author "Duek, K." — probably "Dušek, K." with the š lost (decompiler's background knowledge, not
    checked).
12. Table 1: the curing-agent count column is headed "MTHPA" also for the DGEBA/NA row.
13. Fig. 1a draws the product of epoxide + H₂O as CH₃–CH(OH)–R_x; Fig. 1d draws the second epoxide as
    "CH–CH–R_x". Hydrolysis of an epoxide gives a 1,2-diol (decompiler's background knowledge); transcribed
    as drawn.
14. Fig. 3 and Fig. 4b swap colours: NA is black and MTHPA red in Fig. 3, the reverse in Fig. 4b (the curves
    themselves agree, see the cross-check above).
15. The stated synergy rotational energy barriers (107.62 and 832.02 kcal/mol) are smaller than the colour-key
    spans of Fig. 7 (111.5 and 896 kcal/mol); the paper does not say how the barrier was taken from the
    surface. Not necessarily an error.

## Known problems of this decompilation

- Fig. 4b: dashed series are incomplete (gaps between dashes, dashes touching the solid line lost); around
  1.09–1.11 Å and on the zero baseline some pieces of solid lines may be listed as dashed.
- Fig. 7: only the visible part of each surface; energies in plain-red key ranges uncertain by up to ±13 (a)
  / ±107 (b) kcal/mol; angles poorly determined on flat parts (see `dphi1`, `dphi2`).
- Figs. 10, 11: a few markers are partly covered by the red line or dot; their centres were taken from the
  visible edge plus the marker size (flagged in the `note` column).
- Fig. 12: lower error-bar halves assumed equal to the upper ones.

## Time

About 3 h of wall-clock including an interruption (usage limit): reading spec/tools and pages ~15 min;
transcription ~25 min; Figs. 9–12 ~45 min; Figs. 3–4 ~30 min; Fig. 7 (camera fit and inversion) ~45 min;
checks and README ~20 min.
