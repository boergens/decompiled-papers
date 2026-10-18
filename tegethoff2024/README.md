# tegethoff2024: decompiled

Lennart Tegethoff, Kevin L. Briggman. "Quantitative evaluation of embedding resins for volume electron
microscopy." *Frontiers in Neuroscience* **18**:1286991 (2024). DOI
[10.3389/fnins.2024.1286991](https://doi.org/10.3389/fnins.2024.1286991). Max Planck Institute for Neurobiology of
Behavior – caesar, Bonn. Received 01 September 2023, accepted 29 January 2024, published 09 February 2024.

**Licence:** © 2024 Tegethoff and Briggman; open access under the Creative Commons Attribution License (CC BY), as
stated on p. 1.

## Local and external

**In the local collection**
- Source files:
  - `papers/tegethoff2024/fnins-18-1286991.pdf` – the article, 13 pp., publisher's version of record
  - `papers/tegethoff2024/fnins-18-1286991.txt`, `papers/tegethoff2024/fnins-18-1286991.raw.txt` – earlier text extractions (not used)
  - `papers/tegethoff2024/SOURCE.txt` – fetch note
- Cited works decompiled here: kasthuri2015 (`decompiled/kasthuri2015/`), lu2023 (`decompiled/lu2023/`)

**External pull needed** (not on this machine)
- The raw data ("will be made available by the authors, without undue reservation", Data availability) – no link given (on request from the authors) – the only possible tier-1 source; every CSV here is digitized. The paper names no supplementary material.
- All other cited references: 38 entries in the reference list (40 unnumbered, alphabetical entries) without a [local: …] tag.

## Source files (`../../papers/tegethoff2024/`)

| file | what it is |
|---|---|
| `fnins-18-1286991.pdf` | the article, 13 pp. **Publisher's version of record** (Frontiers typesetting, journal header "TYPE Original Research / PUBLISHED / DOI", running headers and footers "Frontiers in Neuroscience … frontiersin.org", "Check for updates" button; PDF made with pdfTeX on 2024-02-06). `SOURCE.txt`: fetched from frontiersin.org/articles/10.3389/fnins.2024.1286991/pdf on 2026-10-12. |
| `fnins-18-1286991.txt`, `.raw.txt` | earlier text extractions (not used; the draft text came from the PDF's text layer with PyMuPDF, `work/gen_tex.py`). |

**Not available:** the paper names no supplementary material and no data repository. Its Data availability
statement says only "The raw data supporting the conclusions of this article will be made available by the
authors, without undue reservation." So there is no tier-1 source data; every CSV here is digitized.

## Contents

- `main.tex` / `main.pdf`: the whole article in reading order: journal block, title, authors, affiliation, the
  article-information column of p. 1 (editor, reviewers, correspondence, dates, citation, copyright; placed after the
  affiliation, noted in the file), abstract, keywords, all sections, Table 1, Figures 1–8 with captions, data
  availability, ethics, author contributions, funding, acknowledgments, conflict of interest, publisher's note and
  the 40 references. `\pdfpage{N}` marks every page start (p. 10 holds only Figure 7; its marker sits with p. 11's in
  the paragraph that runs from p. 9 to p. 11, noted in the file).
- `figures/`: `fig1.png` … `fig8.png` (whole figures, 200 dpi, `tools/crop.py` on the image bbox + 5 pt);
  per plotted panel `<panel>.csv`, `<panel>_extract.py`, `<panel>.py`, `<panel>_replot.png`. Shared code:
  `tg_common.py` (image loading, axis/tick finding, colour classification, marker detection, swarm profiles, colour-bar
  lookup; imports `../../tools/digitize_common.py`), `fig1_maps.py`/`fig8_maps.py` (+ `fig1_mapplot.py`,
  `fig8_mapplot.py`) for the hardness maps, `fig5ef_common.py`/`fig5ef_plot.py`, `fig6_common.py`, `swarm_common.py`/
  `swarm_plot.py` (beeswarms), `fig8_lines.py`/`fig8_lineplot.py`.
- `tables/table1.csv`: Table 1 (caption, footnote and column groups in `#` lines).
- `work/`: scratch: page renders, embedded images (`work/img`), overlays (`*_overlay.png`), side-by-side comparisons
  (`cmp_*.png`), the text draft and the build script (`draft.txt`, `gen_tex.py`, `main_template.tex`, `alttexts.py`,
  `build_tex.py`: `python3 -I work/build_tex.py` regenerates `main.tex` from them), check JSON, LaTeX logs. May be deleted
  (but then `main.tex` cannot be regenerated; it stands on its own).

Compile: `TEXINPUTS=../tools: lualatex -interaction=nonstopmode -halt-on-error main.tex`; compiles without errors
(run twice), with some overfull lines (long DOIs, the wide Table 1).

Re-run the data: `python3 -I figures/<panel>_extract.py` then `python3 -I figures/<panel>.py`, from any directory; the
extract scripts read the embedded images straight from the source PDF.

## Figures

All eight figures are **JPEG raster images** (304–404 ppi) embedded in the PDF. `tools/vector_dump.py` (re-run after
the zero-area-path fix) finds only the four grey frame lines of each figure box on pp. 4–11, no plot paths; so
**every plotted panel is tier 3 (digitized)**: 34 panels, 0 tier 1, 0 tier 2, 0 tier 4.

Methods (details in each CSV header):
- axes: axis lines and tick marks located in the image (`axis_line()`, `ticks()` on a grey < 205 mask: the axes are
  thin antialiased grey lines), linear fit pixel → value on the labelled ticks (residuals in the CSV headers);
- dot/strip plots (Figs 2, 3, 6): connected components of each series colour (nearest MATLAB default colour in Lab);
  merged blobs split into round(area / single-marker area) markers with k-means. Counts are lower limits where markers
  overlap completely;
- beeswarms (Figs 5A–D, 7A–H): markers (~4.5 px) are packed too densely to separate, so each swarm is given as a
  per-pixel-row profile (coloured pixel count, left/right extent, estimated number of markers = pixels / marker area),
  with group summaries (estimated n, quartiles, range) in the CSV header. The estimated n (about 90–235 per group in
  Fig. 5, lower for the flat strips) is a lower limit; the text says a 15 min session "typically yielded ∼250 cuts";
- markers with error bars (Fig. 5E, F): marker positions picked by eye on a 2× zoom, refined on the colour mask; bar ends
  traced along the marker column;
- line plots (Figs 4B–D, 8B, D, F): per pixel column, centre and edges of each coloured trace; Fig. 4D (a 900 s trace
  with ~250 cuts) as max/min per column; Fig. 8 traces as thick line, thin side lines and grey band;
- hardness maps (Figs 1D, E, G; 8A, C, E): one row per measurement dot: grid position, position in µm (scale bar),
  median colour of the dot core mapped to the nearest colour of the colour bar (sampled in the image; Lab distance).
  Panel D of Fig. 1 and panels C, E of Fig. 8 have no colour bar of their own; the neighbouring one is assumed.

**Checks:** every extraction draws its points onto the source image (`work/*_overlay.png`) and every re-plot was put next
to the original with `tools/compare.py` (`work/cmp_*.png`); I looked at both for every panel. Series, ranges and scales
match. Internal consistency checks: the hardness values read from Figs 5E, 5F and 6C agree (MH 12.3, Spurr's 12.9,
Durcupan 13.3, M 13.6, LX 112 13.8, H 14.6, VH 17.7 HV); the dot values of Figs 1D/E/G, 2A–C and 3A fall within ±0.05 HV, mostly
±0.02 HV, of a 0.1 HV grid (1D: 25/25 within 0.02; 1E 23/25, 1G 24/29, all within 0.04; 2B 49/49; 2C 48/50; 2A 95 %;
3A 96 %), so the hardness values were evidently recorded to 0.1 HV, which supports the axis and colour calibrations.

| panel | type | data | tier | notes |
|---|---|---|---|---|
| Fig. 1A | schematic (mould, block milling, smoothing) | – | – | |
| Fig. 1B | photograph (block in vise) | – | – | |
| Fig. 1C | light micrograph (indentation grid) + inset | – | – | |
| Fig. 1D | hardness map (dots on block face) | `figures/fig1d.csv` | 3 | colour bar of panel E assumed |
| Fig. 1E | hardness map + colour bar 11.0–12.6 HV | `figures/fig1e.csv` | 3 | |
| Fig. 1F | schematic (stub, cross-section) | – | – | |
| Fig. 1G | hardness map + colour bar | `figures/fig1g.csv` | 3 | 29 dots |
| Fig. 2A | strip plot, 6 resins × 3–4 blocks | `figures/fig2a.csv` | 3 | categorical x |
| Fig. 2B | strip plot vs NMA:DDSA ratio | `figures/fig2b.csv` | 3 | categorical x |
| Fig. 2C | strip plot vs BDMA % | `figures/fig2c.csv` | 3 | y labels misaligned with ticks; two calibrations given |
| Fig. 3A | strip plot vs days post cure, 3 series | `figures/fig3a.csv` | 3 | broken x axis, piecewise calibration |
| Fig. 3B | strip plot vs relative humidity | `figures/fig3b.csv` | 3 | sequence numbers kept |
| Fig. 4A | photograph + force diagram | – | – | |
| Fig. 4B | line plot, S1 and S2 | `figures/fig4b.csv` | 3 | |
| Fig. 4C | line plot, 4 force traces | `figures/fig4c.csv` | 3 | F_T traces overlap |
| Fig. 4D | dense line plot (900 s) + inset | `figures/fig4d.csv` | 3 | envelope per column; inset has no axes |
| Fig. 4E | diagram (traces, no axes) | – | – | described |
| Fig. 4F | diagram (trace with chatter, no axes) | – | – | described |
| Fig. 5A | beeswarm, 12 groups | `figures/fig5a.csv` | 3 | row profiles |
| Fig. 5B | beeswarm | `figures/fig5b.csv` | 3 | row profiles |
| Fig. 5C | beeswarm | `figures/fig5c.csv` | 3 | row profiles |
| Fig. 5D | beeswarm | `figures/fig5d.csv` | 3 | row profiles |
| Fig. 5E | scatter + error bars | `figures/fig5e.csv` | 3 | 12 markers |
| Fig. 5F | scatter + error bars | `figures/fig5f.csv` | 3 | 2 open squares nearly hidden, estimated |
| Fig. 6A | light micrographs (block face, section) | – | – | |
| Fig. 6B | light micrographs | – | – | |
| Fig. 6C | dot plot vs hardness | `figures/fig6c.csv` | 3 | ~20 per resin |
| Fig. 6D | video frames (0, 200, 400 ms) | – | – | |
| Fig. 6E | dot plot vs mean F_R | `figures/fig6e.csv` | 3 | open/filled LX 112 markers |
| Fig. 6F | dot plot vs cutting speed | `figures/fig6f.csv` | 3 | categorical x |
| Fig. 7A–H | 8 beeswarms (speed; clearance angle) | `figures/fig7a.csv` … `fig7h.csv` | 3 | row profiles, groups on x ticks (8 panels) |
| Fig. 8A | block-face image with hardness dots + colour bar 10–25 HV; section image | `figures/fig8a.csv` | 3 | dots only |
| Fig. 8B | line plot (mean, thin lines, grey traces) | `figures/fig8b.csv` | 3 | |
| Fig. 8C | block-face image with dots; section image | `figures/fig8c.csv` | 3 | colour bar of A assumed |
| Fig. 8D | line plot | `figures/fig8d.csv` | 3 | |
| Fig. 8E | block-face image with dots; section image | `figures/fig8e.csv` | 3 | colour bar of A assumed |
| Fig. 8F | line plot | `figures/fig8f.csv` | 3 | |

## Text check (`tools/check_text.py`, version 2026-10-17f)

`python3 -I ../tools/check_text.py main.tex ../../papers/tegethoff2024/fnins-18-1286991.pdf`:

- **raw coverage 98.7 %** of the PDF's 8657 tokens; 100.0 % of the 8494 tex tokens found in the PDF;
- **coverage without text repeated on ≥ 3 pages: 100.0 %** (114 tokens left out);
- MISSING runs ≥ 6: 0; EXTRA runs ≥ 6: 0.

What is not matched: the running header "Tegethoff and Briggman / 10.3389/fnins.2024.1286991" and footer "Frontiers in
Neuroscience / NN / frontiersin.org" (the repeated text, 114 tokens; the footer of p. 1 has no header, so the tool lists
it separately as a 1-page text). With `--min-run 1` one more token: "Nordrhein-Westfalen" (p. 2), a real hyphen at a
line end that the tool's dehyphenation joins. The tick labels and other words inside the figures are not in the text
layer (the figures are images), so they do not enter the check.

Read-through against the page images (step 4): degree signs (the text layer has them as superscript "◦"; written °,
with the space the page shows in "110° leading", "136° diamond", "35° diamond"), µm² and mm³, ×, ∼, the minus signs
(−70 kPa) and the range dashes (13−18 HV, 24−48 h, printed with a minus-like dash, kept), subscripts F\_R, F\_S (one "F\_s"
lowercase on p. 5, kept), F\_T and δF, italics (*Danionella cerebrum*, *n*, journal names), Table 1 cell by cell, and the
DOIs broken across lines in the reference list (re-joined).

## Errors and oddities in the paper

- **Fig. 2C: y tick labels not aligned with the ticks.** The labels 12, 11, 10, 9 are ~120 px apart in the embedded image,
  the tick marks and grid lines ~52 px; only "10" sits on a grid line. Panels A and B have their labels on the ticks.
  Reading the ticks as 0.5 HV apart (as in panel B, same plot height) with "10" on its tick puts 48 of the 50 dots
  within ±0.02 HV of a 0.1 HV grid (the other two within 0.05); a calibration on the label positions does not. Both are in `fig2c.csv`; the readings differ by up
  to ~0.3 HV.
- **Text vs Fig. 5F:** "The cutting uniformity (δF\_T) was also not obviously correlated with block hardness (Figure 5F)"
  (p. 7–8), but Figure 5F plots δF\_S (axis label and caption). Noted in `main.tex`.
- **Hardness range quoted for chatter:** "Durcupan, EMbed 812 M and MH all exhibited chatter at 35 nm despite spanning a
  range of hardness from 12.3 to 13.8 HV" (p. 8); in Figs 5E/F and 6C these resins sit at about 12.3 (MH), 13.3
  (Durcupan) and 13.6 HV (M); 13.8 HV is LX 112. Noted in `main.tex`.
- **NMA:DDSA ratios (Fig. 2B, text p. 4) are not the mass ratios of Table 1** (e.g. MH: 2.71 g NMA / 3.02 g DDSA = 0.90,
  but the text calls MH 1.34). My own calculation (not in the paper): with molar masses NMA 178.18 and DDSA 266.38 g/mol
  the Table 1 amounts give molar ratios 1.34 (MH), 1.58 (var I), 1.83 (var II), 2.14 (var III), 2.45 (H), i.e. the
  printed 1.34, 1.57, 1.83, 2.11, 2.44 except var III (2.14 vs 2.11). So the ratios are probably molar; the paper does
  not say so.
- **Table 1:** the DER 736 cell of the "EMbed 812 -var III epon" row is empty (all other empty cells have "−"); the
  components "A", "B", "C" (Durcupan) are not named anywhere; "EMbed 812 –hard (H) epon" has an en dash where the other
  rows have a hyphen. Kept as printed.
- "silicon mold(s)" (p. 4 text and Fig. 1 caption) vs "silicone embedding molds" / "flatbed silicone molds" in the Methods
  (p. 2): presumably silicone in all cases. Kept.
- Small typos, kept: "indention" (p. 4, for indentation), "we also cured … and measure hardness" (p. 4), "compressed by
  factor of" (p. 8), "compare to the samples" (p. 9), "systemically measured" (p. 11), "Fs" with lowercase s once (p. 5).
- Fig. 2A caption: "n = 8–20 points per block face"; the digitized counts are 7–11 per block (lower limits, markers
  overlap), not a contradiction.

## Known problems of this decompilation

- Marker counts in strip/dot plots and swarm sizes are lower limits (overlap); positions of markers split from merged
  blobs are approximate (about one marker diameter). Fig. 6E shows the same compression data as 6C at different x, but
  fewer markers are separable there (10–13 vs ~20 per resin).
- Beeswarm CSVs give distributions, not individual cut values.
- In Fig. 5A–D and 7, JPEG colour bleeding puts some pixels of a swarm into a neighbouring colour class (the "colour
  share" in each group summary); groups were assigned by the dominant colour and their columns, so this does not move
  pixels between groups, but touching swarms may exchange a few edge pixels.
- Fig. 8 colour bar spans 15 HV over ~450 px and its middle colours change slowly, so the map values there are good to
  about ±0.3–0.5 HV; Fig. 1 maps (1.6 HV over ~260 px) to about ±0.05 HV, worse in the flat blue and red ends of the bar.
- The replots of the hardness maps use matplotlib's "jet", not the paper's colour map; the values, not the colours, are
  the data.
