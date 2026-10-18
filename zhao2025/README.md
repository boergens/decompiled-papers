# zhao2025: decompiled

Donghao Zhao, Alex Cartier, Tetsuharu Narita, Frederic Lechenault, Costantino Creton, Matteo Ciccotti.
"Why cutting is easier than tearing elastomers." *Nature Communications* **2025**, 16:3203.
DOI [10.1038/s41467-025-58483-1](https://doi.org/10.1038/s41467-025-58483-1) (printed on p. 1).
Received 13 December 2024; accepted 21 March 2025; published online 03 April 2025.

**Licence:** © The Author(s) 2025; open access under the Creative Commons Attribution-NonCommercial-NoDerivatives
4.0 International License (CC BY-NC-ND 4.0), as stated on p. 8. (ND: the licence does not permit sharing adapted
material; this decompiled copy is for internal reading and re-use of the data, not for redistribution.)

DOI check: verify-sources receipts `vs-20261013-8eeb9b1cce` and `vs-20261013-93bad2ec5e` (both
`verified_with_warnings`) have a Crossref `doi_record` for this DOI with the same six authors, i.e. Crossref resolved
the DOI and matched it to this PDF.

## Source files

| file | what it is |
|---|---|
| `source/zhao2025.pdf` | main article, 8 pp. **Publisher version of record** (Springer Nature typesetting, PDF metadata "Nature Communications, doi:10.1038/s41467-025-58483-1", created 2025-04-03). Copied from `papers/zhao2025/zhao2025.pdf`. Fetch note in `papers/zhao2025/SOURCE.txt`: "zhao2025.pdf: https://www.nature.com/articles/s41467-025-58483-1.pdf (doi:10.1038/s41467-025-58483-1) curl 2026-10-13 by simulation agent". |

`papers/zhao2025/` also holds `zhao2025.txt` (an earlier text extraction; not used, not copied).

**Not available** (named by the paper, not on this machine):
- **Tier-1 data set**: the OSF deposit named in the Data availability statement, https://doi.org/10.17605/OSF.IO/RZWKE
  ("The data presented in both the main paper and supplementary information have been deposited in the OSF database").
  All plotted panels here are therefore tier 2 or 3.
- **Supplementary Information** (Supplementary Figs. 1–3, Supplementary Notes 1–2; cited for the mechanical comparison
  of labelled vs. unlabelled PDMS, the cutting fixture, the blade radius measurement, the calibration parameter α and
  the crosslink density ν_x).
- The peer review file mentioned under "Peer review information".

Cited works in our collection (from `decompile_work/manifest.json`): ref. 12 (Goda, Ma, Fregonese & Bacca, *Soft Matter*
20, 6016–6022 (2024)) is `goda2024`, whose local PDF is the arXiv author version (arXiv 2412.02021), not the
journal version. No other reference matched a collection key.

## Contents

- `main.tex` / `main.pdf`: the whole article in reading order: header line, title, dates, authors, affiliations
  (footnote moved after the author list), abstract, introduction with Eqs. (1)–(4), Results (four subsections,
  Eqs. (5)–(8)), Discussion, Methods (three subsections), Data availability, References 1–38, Acknowledgements, Author
  contributions, Competing interests, Additional information (incl. the full licence text) and the copyright line.
  `\pdfpage{N}` marks the start of each PDF page. Left out: running header/footer, page numbers, "Check for updates",
  logo/icons and the margin string "1234567890():,;" on p. 1.
- `figures/`: `fig1.png` … `fig5.png` (each whole figure rendered at 200 dpi with `crop.py`, without caption); per
  plotted panel `<panel>.csv`, `<panel>_extract.py`, `<panel>.py`, `<panel>_replot.png`.
- `tools/`: `digitize_common.py` (copied from the osmium tools), plus helpers written for this paper:
  `vecplot.py` (vector paths → data: axis fits, vertices, segments, error bars, centre lines of filled dash outlines),
  `markerpanel.py` (shared extractor for the vector scatter panels with error bars, Figs. 4a/b, 5a/b),
  `plotpanel.py` (shared re-plot for those), `rastermarkers.py` (square markers, caps and icons in the raster
  Figs. 2b/2c).
- `tables/`: not created. The paper has no tables.
- `work/`: scratch (page renders, embedded images, overlays `*_overlay.png`, side-by-side checks `cmp_*.png`, glyph
  crops, `check.json`, helper scripts `work/scripts/`). May be deleted.

Compile: `lualatex -interaction=nonstopmode -halt-on-error main.tex` from this folder (twice); compiles without
errors and without "Missing character" warnings.

Re-run the data: `python3 -I -B figures/<panel>_extract.py` then `python3 -I -B figures/<panel>.py` (any working
directory; all paths are relative to the scripts). The extract scripts read `source/zhao2025.pdf` directly.

## Figures

The PDF mixes vector and raster: Figs. 2a, 2d (right), 3e (plot), 4a, 4b, 5a and 5b are **vector paths**
(MATLAB-style export; tier 2). The plot areas of **Figs. 2b and 2c** (frame, ticks, markers, lines, error bars) are part
of one 1333 × 1018 px, 300 ppi raster image embedded on p. 3 (their tick labels, axis titles and legend text are PDF
text over it), so they are **digitized (tier 3)**. Figs. 5a/5b have their tick labels as glyph outlines (no text);
those labels were read off the page. Check `vector_dump`-style: a drawings-only render of every figure page
(`work/draw_p3.png` … `draw_p6.png`, made with `work/scripts/draw_only.py`) shows which parts are vector.

Vector details: marker squares are filled rectangles, error bars are stroked lines (Fig. 4) or thin filled rectangles
(Fig. 5); data points are taken from the error-bar lines/junctions (they agree with the square centres to < 0.1 pt);
dash-dot fit lines and the dashed curve of Fig. 3e are filled dash polygons (lines fitted through all vertices; the
Fig. 3e dashed curve's centre line computed from the two sides of each dash); Fig. 2d's circles are filled rings
(centre = bbox centre), its fit lines are single cubic Béziers (sampled).

**Checks:** every extraction draws its points back onto a render of the page (`work/*_overlay.png`) and every re-plot
was put next to the original with `compare.py` (`work/cmp_*.png`); I looked at all 18 images: series, ranges, scales
and points match.

| panel | type | data | tier | notes |
|---|---|---|---|---|
| Fig. 1a | 3D rendering of the pure-shear cutting set-up | – | – | |
| Fig. 1b | schematic, network at the crack tip | – | – | |
| Fig. 1c | schematic, post-mortem sample | – | – | |
| Fig. 2a | line plot, f vs δ, 3 curves | `figures/fig2a.csv` | 2 vector | all polyline vertices (11 200 rows); curves clipped at δ = 30 mm |
| Fig. 2b | two-axis scatter + lines, f and r_b vs λ | `figures/fig2b.csv` | 3 digitized | upper bar of the λ ≈ 1.12 force point leaves the frame; Fracture icons handled separately |
| Fig. 2c | scatter + lines, G, G1, G2 vs λ, regions I–III | `figures/fig2c.csv` | 3 digitized | total and blade values at λ ≈ 1.08 off scale (line exit point given); red λ ≈ 1.2 square partly hidden |
| Fig. 2d left | two photographs of the crack tip (λ = 1.21, 1.41) | – | – | |
| Fig. 2d right | scatter (profiles) + parabolic fits + dashed arcs | `figures/fig2d.csv` | 2 vector | refitted parabolas give apex radii 133 / 266 μm (printed 130 / 260 μm) |
| Fig. 3a | chemical scheme (mechanophore and its fragments) | – | – | SMILES in `\alttext` |
| Fig. 3b | schematic, labelled network | – | – | |
| Fig. 3c | 3D rendering of the sample | – | – | |
| Fig. 3d | confocal fluorescence image | – | – | |
| Fig. 3e i, ii | fluorescence damage maps | – | – | |
| Fig. 3e plot | line plot, φ_y vs y, 2 curves + φ_b line | `figures/fig3e.csv` | 2 vector | dashed curve = centre line of its dash outlines |
| Fig. 4a | scatter + error bars + fit line, d vs λ | `figures/fig4a.csv` | 2 vector | |
| Fig. 4b | scatter + error bars + fit line, Σ̄ vs λ | `figures/fig4b.csv` | 2 vector | |
| Fig. 5a | scatter + horizontal error bars + fit line, Γ vs Σ_exp | `figures/fig5a.csv` | 2 vector | fit line passes through the origin |
| Fig. 5b | scatter + error bars + fit line, r_b vs d | `figures/fig5b.csv` | 2 vector | see "errors" below (3rd point) |
| Fig. 5c | two photographs + two sketches of the damage mechanism | – | – | |

Counts: 9 plotted panels: 0 tier 1 (OSF set not available), 7 tier 2, 2 tier 3, 0 tier 4. 13 image/schematic panels
with descriptions only. All figures were viewed at 200–400 dpi before writing the descriptions.

### Cross-checks between panels and text (my computations from the CSVs)

- Fig. 2a plateaus (≈ 0.10, 0.045–0.05, 0.03 N for λ = 1.16, 1.28, 1.41) agree with Fig. 2b (0.103, 0.044, 0.031 N).
- Fig. 2c: blade + stretch = total within 3 J m⁻² at every λ (e.g. 1.2: 90.9 + 119.7 vs 212.7).
- Fig. 4b vs Fig. 5a: Σ_exp/Σ̄ is constant, 0.398–0.399 × 10¹⁸ m⁻² (i.e. Σ_LT as used by the authors), for all 7 points;
  the text's "2.0 to 4.3 … 8.1·10¹⁷ to 1.7·10¹⁸" matches (2.03 → 4.26; 0.81 → 1.70 × 10¹⁸).
- Fig. 4a "d changes from 20 to 40 µm": plotted 21.3 → 42.4 µm. OK.
- Fig. 5b r_b values match Fig. 2b's r_b at λ ≈ 1.16 … 1.45 to < 1 μm; its d values match Fig. 4a except one point (below).
- Fig. 3e: the φ_b line is drawn at φ_y = 0.0186 % (label 0.02 %).

## Text check (`check_text.py` 2026-10-17j, no options)

| file | coverage of PDF tokens | without text repeated on ≥ 3 pages | also without in-figure text | tex tokens found in PDF | MISSING ≥ 6 | EXTRA ≥ 6 |
|---|---|---|---|---|---|---|
| `main.tex` | 96.3 % | 96.7 % (28 repeated tokens) | **98.9 %** (157 in-figure tokens) | 99.9 % | 4 runs, 31 tokens | 0 |

All MISSING runs ≥ 6 are tick labels and axis titles inside figures (Fig. 2b right axis, Fig. 3e plot, Fig. 4a/4b
axes), described in `\alttext`. With `--min-run 1` the rest is: equation glyph fragments of the text layer ("d",
"z" = integral sign, "di d"), the page numbers and footer, "Check for updates", the margin string "1234567890" on
p. 1, and in-figure words (panel letters, "Steady-state regime", axis units). EXTRA (6 tokens): "Published online
03 April 2025" (printed as an image on p. 1, not in the text layer), "i" (I in Eq. 5) and "e" (Γ/E, whose E the text
layer stores as Greek Ε). No prose word is missing.

**Glyph audit (required):** `glyph_audit.py` lists 13 hidden glyphs; all checked against their crops
(`work/glyphs/`, montage `work/glyphs_all.png`): 3 × minus sign (AdvMacMthSyN U+0001) in Eqs. (1), (3), (5) → `-` in
math; 4 × large-parenthesis pieces (AdvP4C4E46) in Eqs. (3), (8) → `\left( \right)`; 6 × the overbar of Σ̄
(AdvP4C4E59) in the text and the Fig. 4 caption → `$\bar{\Sigma}$`. All are in main.tex.

Read-through against the page images: equations (1)–(8) (incl. the minus signs, λ², 1/λ², the double integral limits
z_s, x_s, the L limits), subscripts (U_el, G₁, G₂, h₀, φ_xyz, I_bkg, Σ_exp, Σ_LT, r_b, ν_x), superscripts (m⁻², m⁻³,
s⁻¹, R²₁), "∼" in the Discussion (written as ∼, not a bare tilde), "≈ 120 nm", "× 2", "5×", "1024 × 1024", "60 °C".

## Errors and oddities in the paper (kept verbatim; flagged with `\decompnote` where in the text)

1. **Crack extension energy values in the text vs the figures.** p. 4: "540 J·m⁻² (λ = 1.45)" and "a plateau region
   of to 260 J·m⁻² (λ = 1.2)"; p. 5: "the crack extension energy changes from 260 to 540 J·m⁻²". Fig. 2c as printed
   shows ≈ 508 J m⁻² at the λ ≈ 1.45 fracture point and ≈ 213 J m⁻² at λ ≈ 1.2 (digitized, ±3). Fig. 5a plots Γ from
   208 to 554 J m⁻², and its Γ values differ from Fig. 2c's G at the same points (e.g. 502 vs 466 at λ ≈ 1.41; 554 vs
   508 at λ ≈ 1.45), although both are called the crack extension energy.
2. **Fig. 5b, third point**: plotted at d = 24.8 μm, r_b = 161 μm. Fig. 2b gives r_b = 160 μm at λ ≈ 1.245, where
   Fig. 4a gives d = 27.7 μm (bar ±4.8 μm); the Fig. 5b point's horizontal bar (±4.75 μm) matches that λ ≈ 1.245
   bar, but its d is 2.9 μm lower. The other six Fig. 5b points match Fig. 4a's d to < 0.1 μm. Probably a plotting
   slip in Fig. 5b.
3. p. 5: "consistent with the observed increase of the cutting/fracture energy in Fig. 2d" — that energy is in Fig. 2c.
4. Methods: "A side camera captures the images of the strained sample, as shown in Fig. 3d" — the side-camera crack
   images are Fig. 2d; Fig. 3d is a confocal fluorescence image.
5. Fig. 3 caption: "pre-stretch λ of 1.2 (i) and 1.45 (ii)"; the plot legend in Fig. 3e says λ = 1.21 and 1.45.
6. Eqs. (7) and (8) print an italic *v*_x; the text defines Greek *ν*_x.
7. Typos kept: "a plateau region of to 260" (p. 4), "molecular damage undercutting and tearing conditions" (p. 6),
   "D.Z, M.C., and F.L." (author contributions), ref. 14 without "&" before the last author.
8. Fig. 4b: the PDF's text layer has the word "PDMS" hidden under the legend entry "Cutting-induced" (not visible).
9. Fig. 2c: the stretch contribution has a point at λ ≈ 1.08 but the total and blade contribution there are off scale
   (their joining lines leave the top of the frame at λ ≈ 1.11); the region-I values are not readable.

## Time

About 2 h of wall-clock: reading spec/brief/example and all pages ~15 min; vector panels (7) ~45 min; raster panels
2b/2c ~30 min; transcription and descriptions ~25 min; checks and README ~15 min.
