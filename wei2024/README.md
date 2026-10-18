# wei2024: decompiled

Pengchang Wei, Zhen-Yu Yin, Pierre-Yves Hicher, Wangqi Xu. "Interfacial mechanical behavior of
epoxy-quartz: MD nanoindentation and nanoscratching study." *Acta Geotechnica* (2025) **20**:1599–1620.
DOI [10.1007/s11440-024-02503-9](https://doi.org/10.1007/s11440-024-02503-9) (printed on p. 1; confirmed by
Crossref through verify-sources receipts `vs-20261013-4accaa8acb` and `vs-20261013-6d98ef4185`, identity
"confirmed", Crossref issue 4).
Received 18 June 2024; accepted 5 December 2024; published online 27 December 2024.

**Licence:** © The Author(s) 2024; open access under the Creative Commons Attribution 4.0 International
License (CC BY 4.0), as stated on p. 21.

Folder key and PDF agree: first author Wei, published online 2024 (the journal issue is 2025).

## Source files

| file | what it is |
|---|---|
| `source/wei2024.pdf` | the article, 22 pp. **Publisher version of record** (Springer typesetting, running heads "Acta Geotechnica (2025) 20:1599–1620", Springer logo footers). Copied from `papers/wei2024/wei2024.pdf`. `papers/wei2024/SOURCE.txt`: "wei2024.pdf: https://ira.lib.polyu.edu.hk/bitstream/10397/112550/1/s11440-024-02503-9.pdf (doi:10.1007/s11440-024-02503-9) curl 2026-10-13 by simulation agent" (PolyU institutional repository serving the publisher PDF). |

`papers/wei2024/wei2024.txt` (an earlier text extraction) was not used.

**Not available (not in `papers/wei2024/`):** the Supplementary Information
(https://doi.org/10.1007/s11440-024-02503-9, "Supplementary materials": Tables S1–S9 with the PCFF and CVFF
potential parameters, Eqs. S3–S5 for tensile stress, strain and Poisson's ratio). The paper names no data set
("Data availability: No datasets were generated or analyzed during the current study"), so there is no tier-1
source for any figure.

References in our collection: none known (checked against `decompile_work/manifest.json`; `goel2015` there is a
different Goel paper from ref. 16).

## Contents

- `main.tex` / `main.pdf`: the whole article in reading order: title block, authors, affiliations and
  corresponding-author block (printed as a p. 1 footnote, placed after the authors), dates, abstract, keywords,
  Sections 1–4 with Eqs. (1)–(16), Tables 1–5, Figs. 1–18 with captions, descriptions and data pointers,
  Supplementary Information note, acknowledgements, author contributions, funding, data availability,
  declarations, licence, 56 references, publisher's note. Compile:
  `lualatex -interaction=nonstopmode -halt-on-error main.tex` (twice) from this folder; compiles without errors
  or missing glyphs (`decomp.sty` is copied here).
- `tables/table1.csv` … `table5.csv`: all five tables (transcribed from the page images; written by
  `tools/make_tables.py`).
- `figures/figN.png`: every figure rendered at 200 dpi (`crop.py`, image bbox + 3 pt). Per plotted panel:
  `<panel>.csv`, `<panel>.py` → `<panel>_replot.png`; extraction scripts `figN_extract.py` (one per figure;
  `fig15f_extract.py` reads the fig15a–e CSVs, run it after `fig15_extract.py`). The atom-rendering grid CSVs
  share one extract and one plot script per figure (`fig5d.py`, `fig6d.py`, `fig8.py`, `fig13.py`, `fig14.py`,
  `fig16.py`).
- `tools/`: `digitize_common.py` (copy of the osmium tool), helper modules `f1_origin.py`, `f2_common.py`,
  `f2_plot.py`, `f3_markers.py`, `f3_panels.py`, `f3_plot.py`, `f4_atommap.py`, and `make_tables.py`.
  All scripts use paths relative to themselves and run under `python3 -I -B` from any directory.
- `work/`: scratch (page renders, embedded images `work/img/`, overlays, compare images, alt-text pieces and
  `assemble.py`/`main_template.tex` used to build `main.tex`, glyph crops). May be deleted.

## Figures

All 18 figures are 300 ppi JPEGs embedded in the PDF (one image per figure; Figs. 9/10, 15/16, 17/18 share
pages). No plot is drawn as vector paths (`get_drawings()` finds only table rules), no source data exist, and no
image digest repeats. So every plotted panel is **tier 3 (digitized)**.

Methods (details and calibration residuals in each CSV header): linear axis calibration on the tick marks (Fig. 3:
on the gridlines), least-squares; markers by template matching against the legend marker (Fig. 5a, 12, 15) or by
colour classification of shaded ball markers (Figs. 6, 9, 10); lines by colour masks per pixel column (centre plus
upper/lower edge); bars by edge rows. Where the paper prints fit equations (Figs. 5a, 6b, 9b, 15f), the CSVs
also give the curve computed from the printed equation (kind `fit_equation`), and that curve was drawn over the
image: it lies on the printed dashed line in every case.

**Checks:** every extraction was drawn back onto the source image (`work/*overlay*.png`) and every replot put
next to the original with `compare.py` (`work/*cmp*.png`); both were looked at for every panel (by the four
digitizing helper agents, and spot-checked by me for Figs. 3, 6b and 6d). All plot scripts were re-run at the end
without error.

**Colour-keyed atom renderings (Figs. 5d, 6d, 8, 13, 14a/c/d, 16):** treated as colour maps with a key, per the
brief: one grid CSV per panel at native 300 ppi, one row per pixel row; each pixel's colour is scaled to brightest
channel 255 (undoing the sphere shading) and mapped to the nearest colour of the figure's own key bar if within
distance 60; other pixels are empty. These are colours of rendered atoms in image-pixel coordinates (no length
scale), not a continuous field; dense top views are 87–95 % mapped, sparse slices 32–42 %. Annotations drawn over
the renderings (yellow dashed circles and arrows in 6d, blue dashed ellipses and arrows in 14a, the fan outline
and red arrow in 14a(iii)) were masked out. Whether particle renderings should get grids at all is for the
coordinator to confirm (it adds 59 CSVs, about 13 MB).

| panel | type | data | tier | notes |
|---|---|---|---|---|
| Fig. 1a | quartz pyramid model, 3 views + 3D sketch | – | – | |
| Fig. 1b | epoxy molecules, cross-linking, network box | – | – | |
| Fig. 1c | epoxy-quartz system side view with layers and dimensions | – | – | |
| Fig. 2 | flowchart of the fitting method | – | – | transcribed in `\alttext` |
| Fig. 3a–h | line plots, 9–6 LJ vs 12–6 LJ fit, E vs r | `fig3a.csv` … `fig3h.csv` | 3 | lines skeletonized + isolated markers; points off the 0.5 top flagged `clipped_at_top`; blue curve partly hidden under orange |
| Fig. 4a, b | renderings of the simulation box | – | – | |
| Fig. 5a | scatter x/y/z + 3 exponential fits | `fig5a.csv` | 3 | 61-step strain grid (0.005) inferred; 26 markers missing, 32 uncertain (below strain 0.03 hidden under fits) |
| Fig. 5b | total energy vs strain, 3 lines | `fig5b.csv` | 3 | |
| Fig. 5c | density vs strain, 3 lines | `fig5c.csv` | 3 | |
| Fig. 5d | bulk box (element colours) + 4 displacement maps (0–20 Å key) | `fig5d_strain0`, `_strain0p1`, `_strain0p2`, `_strain0p3` | 3 (colour key) | top row and 3D box: description only |
| Fig. 6a | F_z vs h_z, 7 rates, markers + dashed curves | `fig6a.csv` | 3 | INCOMPLETE: hidden markers; dashed curves traced for h_z ≥ 32 Å only, none for 0.50 Å/ps |
| Fig. 6a inset | 0.1 Å/ps markers + dotted curve | `fig6a_inset.csv` | 3 | |
| Fig. 6b | F_z vs h_c, 7 rates + power-law fits | `fig6b.csv` | 3 | INCOMPLETE (hidden markers); fit curves from printed equations |
| Fig. 6c | 8 side-view renderings | – | – | |
| Fig. 6d | 4 displacement maps (0–5 Å key) | `fig6d_0p10`, `_0p5`, `_1p50`, `_2p0` | 3 (colour key) | |
| Fig. 7 | surface-mesh renderings, no key | – | – | |
| Fig. 8a | 3D box + top view (description only); 8 slices 0–74 Å; 3 slices 64–74 Å (0–5 Å key) | `fig8a_top_i` … `_viii`, `fig8a_slice_i` … `_iii` | 3 (colour key) | |
| Fig. 8b | 5 shear-strain slices (0–0.4) | `fig8b_i` … `_v` | 3 (colour key) | |
| Fig. 8c | 5 volumetric-strain slices (0–0.2) | `fig8c_i` … `_v` | 3 (colour key) | |
| Fig. 9a | pairwise force x/y/z/overall vs h_z; sketch | `fig9a.csv` | 3 | INCOMPLETE below h_z ≈ 18 Å (overlapping zero band) |
| Fig. 9a inset | zoom 15–25 Å | `fig9a_inset.csv` | 3 | only 21 of the ~5 px open markers found; lines complete |
| Fig. 9b | average force vs loading rate, 2 series + fits | `fig9b.csv` | 3 | 14/14 markers; fit curves from printed equations |
| Fig. 10a | total energy vs h_z, 7 rates | `fig10a.csv` | 3 | INCOMPLETE (hidden markers); dashed curves only for 0.10 and 0.25 Å/ps |
| Fig. 10b | energy increments pe/ke/total, 3 lines | `fig10b.csv` | 3 | |
| Fig. 10c | energy increments, 6 terms | `fig10c.csv` | 3 | |
| Fig. 10d | grouped bars ΔE (pe/ke/total) × 7 rates | `fig10d.csv` | 3 | category axis |
| Fig. 11 | mechanism flowchart | – | – | transcribed in `\alttext` |
| Fig. 12a–e | Fx/Fy/Fz vs sliding distance, h_c 5–25 Å | `fig12a.csv` … `fig12e.csv` | 3 | 30 points per series; 12d F_z at 29 Å not drawn |
| Fig. 12f | total energy vs sliding distance, 5 h_c | `fig12f.csv` | 3 | 9 overlapping markers flagged |
| Fig. 13 | 5 structures (element colours) + 5 shear-strain slices (0–0.4) | `fig13_shear_i` … `_v` | 3 (colour key) | top row description only |
| Fig. 14a | displacement slices (hidden / not hidden quartz) + top view | `fig14a_hidden_i` … `_iv`, `fig14a_nohidden_i`, `_ii`, `fig14a_xy_iii` | 3 (colour key) | fan-shape drawing description only |
| Fig. 14b | surface mesh, no key | – | – | |
| Fig. 14c | 4 shear-strain slices | `fig14c_i` … `_iv` | 3 (colour key) | |
| Fig. 14d | 4 volumetric-strain slices | `fig14d_i` … `_iv` | 3 (colour key) | |
| Fig. 15a–e | Fx/Fy/Fz vs sliding distance, 5 velocities | `fig15a.csv` … `fig15e.csv` | 3 | marker spacing 0.5/0.5/1/0.375/0.5 Å (found from the data) |
| Fig. 15f | F_y scatter, 5 velocities + exponential fits | `fig15f.csv`, `fig15f_fits.csv` | 3 | markers searched near the 15a–e values (guided); 70 of 290 rows flagged |
| Fig. 16a | 5 shear-strain slices (0–0.4) | `fig16a_col1` … `_col5` | 3 (colour key) | no per-panel labels; named by column |
| Fig. 16b | 5 displacement top views (0–5 Å) | `fig16b_0p1` … `_2p0` | 3 (colour key) | |
| Fig. 17a–d | grouped bars Fx/Fy/Fz × 5 velocities with error bars | `fig17.csv` | 3 | 5 error bars clipped at the frame (flagged) |
| Fig. 18 | mechanism flowchart | – | – | transcribed in `\alttext` |

Counts: 37 plotted panels/insets with conventional axes, all tier 3 (Fig. 3a–h 8, 5a–c 3, 6a + inset + 6b 3, 9a + inset + 9b 3, 10a–d 4, 12a–f 6, 15a–f 6, 17a–d 4; 35 CSVs incl. `fig15f_fits.csv`, with `fig17.csv` covering 4 panels) and 59 colour-key grid panels (tier 3); 0 tier 1, 0 tier 2, 0 tier 4.

### Cross-checks of panel values against the text and tables

- **Table 5 P_max vs Fig. 6a/6b end points:** agree within 0.02 nN (0.25: 9.757 vs 9.747; 0.5: 10.594 vs 10.605;
  0.75: 13.052 vs 13.057; 1.0: 13.115 vs 13.105; 1.5: 14.813 vs 14.833 Å/ps). The 2.0 Å/ps end point is hidden.
- **Table 5 H vs Eq. (8)–(9):** recomputing H = P_max/(4 h_c² tan φ tan θ) with h_c = 25 Å, φ = 27.87°, θ = 26.35°
  gives values 0.13 % below the printed H for every rate (e.g. 1.490 vs 1.492 GPa): consistent (rounding of the
  angles).
- **Table 3:** Ē = 2.075 is the root-mean-square of E_x, E_y, E_z ("square average", as the footnote says), and
  E_r = Ē/(1 − 0.377²) = 2.419 (Eq. 11). **Table 4:** the printed v̄ = 0.377 is the arithmetic mean of the six
  components; their geometric mean (the footnote says "geometric average") is 0.376.
- **Fig. 5c vs text:** density 1.129 at zero strain, 1.097–1.1025 at 0.30, as the text's "1.13 to around 1.10".
  **Fig. 5a vs Table 3 moduli:** inconclusive (only 6–7 noisy markers per direction in strain 0–0.04).
- **Fig. 9a vs caption:** overall = √((x²+y²+z²)/3) within 0.02 nN wherever all four markers were found.
  Fig. 9b at 1.0 Å/ps (6.04 / 2.70 nN) vs the mean of the found 9a markers (6.18 / 2.96): close, not exact.
- **Fig. 10:** 10d total ≈ pe + ke within 16–24 kcal/mol; 10b at 45 Å: 1506 + 927 vs 2435. **Mismatch:** 10d at
  1.0 Å/ps has pe 1458, ke 1008 (total 2450), 10b at h_z = 45 Å has E_pe 1506, E_ke 927 (E_total 2435): totals agree,
  pe/ke differ by +50/−80 kcal/mol. 10a end values minus ≈5500 match the 10d totals within 10–30 kcal/mol.
- **Fig. 15f equations vs Fig. 15a–e:** refitting Eq. (16) to the digitized 15a–e F_y reproduces the five printed
  equations (e.g. 1.5 Å/ps: 8.40, 9.37, −10.02, R² 0.62 vs printed 8.39, 9.34, −10.01, 0.61). Fig. 15c and 12d (same
  run, h_c 20 Å, 1.0 Å/ps) agree within 0.1 nN.
- **Fig. 17 vs Figs. 12/15:** the Fig. 17 bars equal the means of the Fig. 12a–d / 15a–e points over 15–30 Å within
  0.00–0.14 nN, and the error-bar half-lengths match the standard deviations of those points (0.5–1.8 nN), so the
  error bars are ± 1 SD over the sliding distance (my inference; the caption does not say). Exception: 12d F_z
  (5.10 vs 4.75) because the 29 Å point is missing from Fig. 12d (`work/fig17_vs_f3.txt`).

## Text check (`check_text.py` 2026-10-17j, no options)

`python3 -I -B .../tools/check_text.py main.tex source/wei2024.pdf`

| coverage of PDF tokens | without text repeated on ≥ 3 pages | also without in-figure text | tex tokens found in PDF |
|---|---|---|---|
| 95.8 % | 96.0 % (24 repeated tokens) | 96.0 % (no in-figure text: the figures are images without a text layer) | 98.8 % |

Below 98 % because the paper is math-heavy and set in Springer "Adv" symbol fonts (brief: accepted when every
unmatched run is equation or inline-math tokens). With `--min-run 1` there are 147 MISSING runs (496 tokens) and
42 EXTRA runs (147 tokens). All runs of 4 or more tokens are inside Eqs. (1)–(16) or inline math (θ → "h", φ →
"u"/"/", η → "g", ε → "e", σ → "r", χ → "v", Δ → "D", = → "¼", ( ) → "ð Þ", + → "þ", √ → "ffiffi"). The short ones are:
page numbers and the Springer "123" footer mark, the hidden "(0123456789().,-volV)" stamp on p. 1, "9" for ×,
"t" for v̄, "lm" for μm, "de" for ΔE, "a" for α/Å, and four real line-end hyphens that the checker joins
("micro- and" → "microand", "Writing-Review", "fiber-reinforced" in ref. 13, "s11440-024-02503-9"). No prose word
is among the unmatched runs.

**Glyph audit** (`decompile_work/tools/glyph_audit.py`, crops in `work/glyphs/`, contact sheets
`work/glyph_sheet_0.png`, `_1.png`): 95 hidden glyphs, all checked against their crops: minus signs in
equations (U+0003), × (U+0005), ° (pp. 3, 9, 14), © (p. 1), middle dots · (keywords, p. 1 affiliation and p. 20
acknowledgements), and bracket/radical pieces of the large equations. All are in `main.tex` (· and ° as printed;
the stray dots in "Research·Centre·for" kept verbatim with a `\decompnote`).

Read-through against the page images (step 4) done for: Eqs. (1)–(16) (zoomed at 300 dpi), all five tables, the
∼ ranges (text layer "*"), ×, μm, ∞, °C, Å, the subscripts h_c/h_z/h_o/h_0, E_r, P_max, F_z/F_y, v̄ and Ē, and the
reference list (line-end hyphens in DOIs restored from the images).

## Errors and oddities in the paper (kept verbatim)

In `main.tex` with `\decompnote`:
- Eq. (1): the three bond-stretching and three angle-bending terms all carry exponent 2 (k₂, k₃, k₄; H₂, H₃, H₄).
  *(Background knowledge, not from the paper: in PCFF these are the 2nd, 3rd and 4th powers.)*
- Eq. (4): the Morse bond term is printed without a square on the bracket; "cos" in the F_{φθθ′} term is italic.
  *(Background knowledge: the CVFF Morse term is squared.)*
- p. 9: "the epoxy-quartz structure … at different h_z are shown in Figs. 6b and 7": the structures are in Fig. 6c.
- Fig. 12 caption names a panel g (structure and shear strain) that the figure lacks; that content is Fig. 13.
- Conclusion 3: "H = 1.492 ∼ 2.174 Gpa" — Table 5's maximum is 2.266 GPa (1.5 Å/ps); 2.174 is the 2.0 Å/ps value.

In this README only:
- Density units: text and Fig. 5c say kg/m³ for values 1.10–1.13. *(Background knowledge: epoxy density is
  ≈ 1.1–1.2 g/cm³, so g/cm³ is meant.)*
- Table 4 footnote says geometric average; 0.377 is the arithmetic mean (geometric 0.376).
- Text: R² of the Eq. (16) fits "0.42 ∼ 0.63"; the Fig. 15f legend prints 0.42–0.62.
- Fig. 3 b–h: the 9–6 LJ curve (the same potential in every panel) is shifted to larger r by about (interval start
  − 1.6 Å) relative to panel a; E = 0.2 kcal/mol is reached at r ≈ 3.2 (a), 3.6 (b), 4.4–5.0 Å (d–h). Panel a matches
  Table 1's 9–6 parameters for atom type c (ε 0.054, σ 4.01: computed E(3.1 Å) = 0.336 vs 0.335 digitized), and panel
  g's orange curve matches the final 12–6 parameters (σ 3.479) only after subtracting a 1.7 Å offset. So panels b–h
  seem to plot r measured from the interval start (or shifted); the CSVs give r as plotted.
- Fig. 6a/6b: the 0.75 and 1.50 Å/ps series are sampled every 0.75 Å (others 1 Å); in 6b their last point sits at
  h_c = 25.5 Å, i.e. h_c ≠ h_z − 20 by 0.5 Å for these two rates (against Eq. 5), and Table 5's P_max for 0.75 Å/ps is
  the value at h_c = 25.5 Å. The Fig. 6a dashed curves are smoothing curves, not the 6b power-law fits shifted by 20 Å.
- Fig. 10d vs 10b pe/ke mismatch at 1.0 Å/ps (above).
- Fig. 12d: the F_z marker at 29 Å is missing (its dashed line breaks off near 7 nN); the same run in Fig. 15c has 9.1 nN there.
- Figs. 15a–e use different marker spacings (0.5/0.5/1/0.375/0.5 Å), not mentioned in the paper.
- Fig. 17: the text says forces rise with sliding velocity and depth along all three directions, but the bars are not
  monotonic (F_x changes sign; |F_y| at 2.0 < 1.5 Å/ps for h_c 15 and 20 Å; F_z in (a) 0.83 at 1.0 vs 0.99 at 0.5 Å/ps).
- Fig. 6d rate labels mix formats ("0.10", "0.5", "1.50", "2.0 Å/ps"); Figs. 13/16 captions say "with sliding distance"
  but show only the 30 Å state; Fig. 1b's last dimension "55.8246" has no unit.
- Typos kept: "cuase", "epoxy resion", "Fast paraller algorithms" (ref. 29), "Gpa"; ref. 36's DOI is printed doubled
  ("…mj20076910.2320/matertrans.mj200769").

## Known limits

- Hidden and overlapping markers make Figs. 5a, 6a, 6b, 9a (and its inset), 10a and 15f incomplete; the CSV headers
  say "INCOMPLETE" or flag the rows.
- Fig. 3: where the orange 12–6 curve covers the blue 9–6 curve, the blue curve has gaps (blue minima in e–h uncertain).
- Atom-rendering grids: anti-aliased atom edges (25–35 % of each slice box) are unmapped; values are rendered colours.

## Time

About 1 h wall-clock (03:00–04:00 UTC by the machine clock): text, tables and README by me; figure digitization in four
parallel helper agents (F1: Figs. 3, 5a–c; F2: Figs. 6a/b, 9, 10; F3: Figs. 12, 15; F4: Fig. 17 and the atom maps).
