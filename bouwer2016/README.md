# bouwer2016: decompiled

James C. Bouwer, Thomas J. Deerinck, Eric Bushong, Vadim Astakhov, Ranjan Ramachandra, Steven T. Peltier,
Mark H. Ellisman. "Deceleration of probe beam by stage bias potential improves resolution of serial block-face
scanning electron microscopic images." *Advanced Structural and Chemical Imaging* **2016**, 2:11.
DOI [10.1186/s40679-016-0025-y](https://doi.org/10.1186/s40679-016-0025-y) (printed on p. 1; Crossref-matched to this
PDF by verify-sources, e.g. receipt `vs-20261013-4cdf67f92e`; also listed in our whitepaper's References).
Received 20 July 2016; accepted 9 September 2016; published online 15 September 2016.

**Licence:** © 2016 The Author(s); Creative Commons Attribution 4.0 International License (CC BY 4.0), as stated
on p. 1.

## Source files

| file | what it is |
|---|---|
| `source/bouwer2016.pdf` | main article, 13 pp. **Publisher version of record** (SpringerOpen typesetting, header "Bouwer et al. Adv Struct Chem Imag (2016) 2:11", footer "Page N of 13"; PDF metadata: Creator Springer, Acrobat Distiller, 2016-09-14). Born-digital, text layer good. Copied (cp) from `papers/bouwer2016/bouwer2016.pdf`. |

Fetch note (`papers/bouwer2016/SOURCE.txt`): "Fetched 2026-10-13 by the lead session (oct-12-epoxy-cutting) from
NCBI's PMC Open Access bucket: https://pmc-oa-opendata.s3.amazonaws.com/PMC5025511.1/PMC5025511.1.pdf (%PDF checked)."
(`papers/bouwer2016/bouwer2016.txt`, an older text extraction, was not used.)

The paper has no supplement and names no data set, source-data file or video. So there is **no tier-1 source**
for any figure, and nothing is missing.

Cited works in our collection (from `decompile_work/manifest.json`): ref. 7 Denk & Horstmann 2004 = `denk2004`;
ref. 17 Titze & Denk 2013 = `titze2013`.

## Contents

- `main.tex` / `main.pdf`: the whole article in reading order: header block, title, authors, correspondence
  footnote (moved after the author list), abstract, keywords, licence footer (moved after the keywords), all
  sections, Eqs. (1)–(2), Figs. 1–12 with captions, abbreviations, authors' contributions, acknowledgements,
  competing interests, dates, references 1–27. `\pdfpage{N}` marks every page start.
- `figures/`: `fig1.png` … `fig12.png` (200 dpi crops without captions, `tools/crop.py`); per plotted panel
  `<panel>.csv`, `<panel>_extract.py`, `<panel>.py`, `<panel>_replot.png` (details below).
- `tables/`: none. The paper has no tables.
- `tools/digitize_common.py`: copy of the osmium helper module, imported by the extraction scripts.
- `decomp.sty`: copy of the osmium macro package, so `main.tex` compiles here without TEXINPUTS.
- `work/`: scratch (page renders, embedded images at native resolution, overlays `*_overlay.png`, side-by-side
  comparisons `cmp_*.png`, check output). May be deleted.

Compile: `lualatex -interaction=nonstopmode -halt-on-error main.tex` (from this folder, twice): no errors,
some overfull/underfull boxes from long lines.

Re-run the data: `python3 -I -B figures/<fig>_extract.py` then `python3 -I -B figures/<fig>.py` (any working
directory; all paths are relative to the script).

## Figures

All figures are embedded raster images (300 ppi; Fig. 8 a 600 ppi 1-bit stencil). `get_drawings()` finds only
the figure frames on every page, no plot paths, so no panel is tier 2. Image digests are all different (no
duplicated plates).

| panel | type | data | tier | notes |
|---|---|---|---|---|
| Fig. 1a–d | schematic (stage-biasing geometry, 4 configurations) | – | – | labels transcribed in `\alttext` |
| Fig. 2 | scatter plot, measured vs applied potential | `figures/fig2.csv` | 3 digitized | 17 points; circle fits; ±2 V |
| Fig. 3a | Monte Carlo trajectory plot, 1.5 keV, depth scale bar | `figures/fig3a.csv` | 3 digitized | deepest black (BSE) and deepest grey/black (all) pixel per column; no lateral scale |
| Fig. 3b | 3D wireframe plot, BSE energy spread | `figures/fig3bd_peak.csv` | 4 (peak height only) | mesh not digitizable point by point; peak 0.99 ± 0.03 |
| Fig. 3c | as 3a, 3 keV | `figures/fig3c.csv` | 3 digitized | uneven scale-bar ticks: linear and piecewise depths both given |
| Fig. 3d | as 3b, 3 keV | `figures/fig3bd_peak.csv` | 4 (peak height only) | peak 1.00 ± 0.03 |
| Fig. 4a–f | SBEM BSE micrographs (overlay test) | – | – | |
| Fig. 5 (6 panels, labelled by energy) | SBEM BSE micrographs, inverted | – | – | |
| Fig. 6 | scatter plot, 4 series | `figures/fig6.csv` | 3 digitized | 22 markers; ±0.007 keV, ±0.0015 |
| Fig. 7a, b | SBEM BSE micrographs | – | – | |
| Fig. 8 | schematic (SE1/SE2/BSE) | – | – | |
| Fig. 9a | trajectory fans (BSE blue, SE green), Height vs Distance | `figures/fig9a.csv` | 3 digitized | outer fan edges per pixel row |
| Fig. 9b | as 9a | `figures/fig9b.csv` | 3 digitized | |
| Fig. 10a, b | SBEM images (SE-dominated vs BSE) | – | – | |
| Fig. 11 | 3D volume rendering | – | – | |
| Fig. 12 | orthogonal views (XY, XZ, YZ) with 10 µm scale bar | – | – | |

Panels per tier: tier 1: 0; tier 2: 0; tier 3: 6 (Fig. 2, 3a, 3c, 6, 9a, 9b); tier 4: 2 (Fig. 3b, 3d, peak height
only). Image panels with description only: 23 (Fig. 1a–d, 4a–f, 5 ×6, 7a–b, 8, 10a–b, 11, 12).

How each was extracted (details in each CSV header and script docstring):
- **Fig. 2, Fig. 6:** axes fitted on the blue frame and grid lines (which sit at the labelled ticks; residuals
  < 1 V and < 0.003 keV / 0.0004). Open circles: least-squares circle fit to the ring; open squares: bounding-box
  centre (pieces cut by grid lines merged); filled diamonds: ink centroid; filled down-triangles: bounding-box
  centre (ink centroid given in an extra column). At 5 keV in Fig. 6 the circle and square overlap at (5, 1) on the
  frame corner (flagged).
- **Fig. 3a/3c:** per source pixel column the deepest pure-black pixel (BSE trajectories) and the deepest grey or
  black pixel (all trajectories), depth from the scale bar's labelled ticks. The panel-c scale bar is unevenly
  ticked (0–50 nm: 157 px; 50–100: 140.5 px; 100–150: 140 px), so the CSV gives both a linear and a piecewise
  depth (they differ by up to 2.3 nm). The figure has no lateral scale: x is given in source pixels and, under
  the stated assumption of an isotropic plot, in nm from the cloud centre.
- **Fig. 3b/3d:** only the height of the central spike: orthographic view assumed; z calibrated on the z-axis
  tick marks; base level at the panel centre = midpoint of the mesh's left and right corners; apex = topmost line
  pixel there. Result 0.995 (b) and 0.996 (d); against the z axis at the back corner the apex would read only
  ~0.93–0.95, which is the projection error the construction avoids.
- **Fig. 9a/9b:** per pixel row, leftmost and rightmost blue and green pixel within ±2 rows (the outer
  trajectories are dotted), axes from 9 x ticks + y-axis line and 6 y ticks + x-axis line (residuals ≤ 0.023 mm).

**Checks:** every extraction draws its points back onto the native-resolution source image
(`work/fig2_overlay.png`, `fig3_overlay.png`, `fig3a_overlay.png`, `fig3c_overlay.png`, `fig6_overlay.png`,
`fig9a_overlay.png`, `fig9b_overlay.png`) and every re-plot was put beside the original with `tools/compare.py`
(`work/cmp_fig2.png`, `cmp_fig3.png`, `cmp_fig6.png`, `cmp_fig9.png`); I looked at all of them. Markers, fan
edges and envelopes sit on the printed ink; series, ranges and scales match.

Consistency with the text (my reading of the CSVs): Fig. 6 ratios (deceleration / FEI CBS at the same landing
energy) are 16.3 and 23.3 at 1 keV and 4.5 and 6.5 at 1.5 keV, against the caption's ×16.5, ×23.6, ×4.5, ×6.5.
Fig. 3 maximum depths: all trajectories 53.6 nm (a) and ~135 nm (c), BSE 22.8 nm (a) and 56–58 nm (c), against
the text's "~50 and 130 nm" electron range and "~20 and 40 nm" BSE escape depth (the deepest single black
trajectory in c is deeper than 40 nm; the bulk of the black cloud ends around 40–45 nm).

## Text check (`check_text.py` version 2026-10-17j, no options)

`python3 -I -B .../tools/check_text.py main.tex source/bouwer2016.pdf`

| file | coverage of PDF tokens | without text repeated on ≥ 3 pages | also without in-figure text | tex tokens found in PDF | MISSING ≥ 6 | EXTRA ≥ 6 |
|---|---|---|---|---|---|---|
| `main.tex` | 99.3 % | **99.9 %** (48 repeated tokens) | 99.9 % | 99.9 % | 0 | 0 |

All unmatched runs (`--min-run 1`):
- REPEATED: the page footer "Page N of 13" (boilerplate, left out). The running header is given once at the top,
  so it matches.
- MISSING: "1" and "2" equation numbers and "N backscattered / N incident" of Eq. (2): equation math, which the
  tool strips from the .tex; transcribed in `equation` environments.
- EXTRA: "Open Access" (same text, placed after the DOI line instead of before "RESEARCH" as in the text layer);
  Eq. (2) tokens and the "1" equation tag (same math, tokens in a different order); "Published online: 15
  September 2016": printed on p. 13 as an embedded image, not in the text layer (noted in main.tex).

Read-through against the page images (step 4) done for: Eq. (1) δ\_c = C\_c(ΔE/E\_0)α and Eq. (2), italic symbols
δ, α, η, C, E, N; × in dimensions and magnifications; minus signs (−5000 V, −1.5-keV, −1 keV …); ~ and %;
µm/µs; en dashes in ranges; bold volume numbers in the references; italics in captions (*left half*, *white*,
*open circles* …). Real hyphens at line ends were kept (e.g. beam-deceleration, electron-landing-energy,
thin-surface, high-Z, TEM-like, re-acceleration, indium-tin, 8.9-mm); "multiscale", "autofocus" and
"photo-diode" (p. 9 line end, written as on pp. 7–8) are my reading of ambiguous line-end hyphens.

## Errors and inconsistencies in the paper (kept verbatim; the ones that matter are flagged with `\decompnote`)

- p. 2: "It was been pointed out"; "SBEM and FIB-SBEM use SEM backscattered electron imaging" (FIB-SEM elsewhere).
- p. 3: "Figure 3a, b shows that the escape depth of the BSE is ~20 and 40 nm" — the 1.5- and 3-keV trajectory
  plots are panels a and c.
- p. 3 vs Fig. 3 caption: lateral-energy-spread pixels "of size 1 and 2 nm for the 1.5- and 3-keV beams" vs caption
  "b and d were performed at a pixel size of 1 nm".
- Working distance on the Zeiss Sigma: 8.8 mm (Fig. 1 caption), 8.0 mm (text p. 12), 8.9 mm (Fig. 12 caption).
- Fig. 10: caption "with 1.5-keV deceleration voltage" (no minus sign; −1.5-keV in the next sentence); caption
  "a Signal from the central ring only" vs text p. 10 "Figure 10a, using all rings of the detector".
- Fig. 2 caption: "Above −500 V, the surface potential measured shows an approximately 12 % drop". From the
  digitized points the drop (1 − measured/applied) is 8 % at −1500 V, 12.5 % at −1000 V, 25 % at −600 V and
  32 % at −500 V, so 12 % holds only near −1000 V (decompiler's reading of `fig2.csv`).
- Fig. 1 caption: "no arcing occurs during cutting at voltages lower than 3.5 keV" (keV for a voltage).
- Fig. 3c: the depth scale bar's ticks are unevenly spaced (see above).
- Fig. 4 caption ends with an incomplete sentence ("Note that the decrease in signal to noise as the acceleration
  voltage is lowered"); Fig. 12 caption "4K × 4K× raster"; text p. 5 "subject increased chromatic aberration";
  p. 8 "between to the two detectors)" (unmatched parenthesis); p. 11 "an monolithic".
- Fig. 6 caption "closed triangles" = the filled down-triangles of the legend (not an error, just wording).

## Time

About 45 minutes of wall-clock: reading brief/spec/example ~5 min; page review ~5 min; digitizing Figs. 2, 6, 9,
3 with checks ~15 min; main.tex and descriptions ~15 min; checks and README ~5 min.
