# hildebrand2017: decompiled

David Grant Colburn Hildebrand, Marcelo Cicconet, Russel Miguel Torres, Woohyuk Choi, Tran Minh Quan, Jungmin Moon,
Arthur Willis Wetzel, Andrew Scott Champion, Brett Jesse Graham, Owen Randlett, George Scott Plummer, Ruben Portugues,
Isaac Henry Bianco, Stephan Saalfeld, Alex Baden, Kunal Lillaney, Randal Burns, Joshua Tzvi Vogelstein, Alexander Franz
Schier, Wei-Chung Allen Lee, Won-Ki Jeong, Jeff William Lichtman, Florian Engert. "Whole-brain serial-section electron
microscopy in larval zebrafish." **bioRxiv preprint** 134882, version posted May 7, 2017.
DOI [10.1101/134882](https://doi.org/10.1101/134882) (printed in the bioRxiv stamp on every page).

**Version:** this is the **bioRxiv preprint**, not the journal version. (From background knowledge, not from the PDF: the
paper was later published in *Nature* 545, 345–349 (2017), doi:10.1038/nature22356; that version is not in the collection.)
The collection key `hildebrand2017` fits both; the folder holds the preprint only.

**DOI check:** verify-sources receipt `vs-20261013-de73d2784b` (and -f960bd837c, -3be89511f2, -798e06dc61, cited in
`web/whitepaper.md`) resolved 10.1101/134882 at Crossref (type posted-content, publisher openRxiv, not retracted) and matched
it to this PDF: identity "confirmed", sha256 `cb1bb5dd…62519ee` = `source/hildebrand2017_biorxiv_134882.pdf`.

**Licence:** "It is made available under a CC-BY 4.0 International license" (bioRxiv stamp, every page). Copyright holder:
the author/funder.

## Source files

| file | what it is |
|---|---|
| `source/hildebrand2017_biorxiv_134882.pdf` | the preprint, 47 pp. (Word/Acrobat PDFMaker, born-digital text; all figures are 150 ppi raster images). Copied from `papers/hildebrand2017/`; `SOURCE.txt` there says: "hildebrand2017_biorxiv_134882.pdf: https://www.biorxiv.org/content/biorxiv/early/2017/05/07/134882.full.pdf (curl, 2026-10-13)". |

`papers/hildebrand2017/` also holds `.txt`/`.raw.txt` text extractions (not used).

Layout of the PDF: pp. 1 title/authors, 2–6 main text, 7–9 references 1–43, 10–19 Methods, 20–21 Methods references 44–65,
22 acknowledgements, 23 author contributions/information, 24–45 Figures 1–4 and Extended Data Figures 1–10 (each figure
image with its caption below, captions running onto the next page; Extended Data Fig. 9 fills p. 43 and its caption is on
p. 44), 46–47 legends of Supplementary Videos 1–10.

**Cited works in our collection** (from `decompile_work/manifest.json`): ref. 35, Hayworth et al. 2014 (*Front. Neural
Circuits* 8, 68) = `hayworth2014`. No other reference matches a manifest key (`wanner2015` is a different Wanner paper,
*J. Microsc.* 2015, not ref. 30; `luft1961` is not ref. 50, Luft 1973).

**Not available** (named by the paper, not on this machine):
- Supplementary Videos 1–10 (only their legends are in the PDF).
- The complete dataset and reconstructions (http://hildebrand16.neurodata.io/, CATMAID) and the custom tools
  (http://github.com/davidhildebrand/hildebrand16/); these would be the tier-1 source for the Fig. 4 and Extended Data
  Fig. 3–5, 9 data. No source-data files are named.
- The journal (Nature) version of the paper.

## Contents

- `main.tex` / `main.pdf`: the whole preprint in reading order: bioRxiv stamp (once, with a note), title, authors,
  affiliations, corresponding-author and present-address notes, the unheaded summary paragraph and main text, References
  1–43, Methods (all subsections, including the two displayed equations and the slice notation of p. 17–18, transcribed
  from the page image as LaTeX math), Methods References 44–65, Acknowledgements, Author Contributions, Author Information,
  Figures 1–4 and Extended Data Figures 1–10 with full captions, descriptions and data links, and the Supplementary Video
  legends. `\pdfpage{N}` marks every page start. Compile from this folder:
  `lualatex -interaction=nonstopmode -halt-on-error main.tex` (twice): no errors, no missing characters (main.pdf is
  39 pp., 16.8 MB because it embeds all figure PNGs).
- `figures/`: each figure rendered at 200 dpi from the PDF without its caption (`fig1–fig4.png`, `edfig1–edfig10.png`;
  Extended Data figures are named `edfigN`), and for each plotted panel `<panel>.csv`, `<panel>_extract.py`,
  `<panel>.py`, `<panel>_replot.png`.
- `tools/`: helpers imported by the figure scripts (`digitize_common.py` copied from the osmium tools; `cmap_common.py`,
  `heatmap_grid.py`, `heatmap_plot.py`, `pairs_matrix.py`, `pairs_plot.py`, `histo_common.py`, `histo_plot.py` written here).
  Scripts import them relative to themselves and read the embedded images straight from `source/…pdf`; run them with
  `python3 -I -B figures/<panel>_extract.py` then `python3 -I -B figures/<panel>.py` from any directory.
- No `tables/`: the paper has no tables.
- `work/`: scratch: `PROGRESS.md`, `draft.py`/`tidy.py` (turned the text layer into draft LaTeX with superscripts, italics and
  bold taken from the fonts; every page was then structured and checked by hand), `check.json`, side-by-side comparisons
  `cmp_*.png`, the equation crops `z17.png`/`z18.png`, glyph-audit crops `glyphs/`. May be deleted.

## Figures

All figures are raster images (150 ppi JPEG/PNG with soft masks); `get_drawings()` finds no vector paths in any figure
area, so every data panel is **tier 3 (digitized)**. Every overlay (extracted points drawn back onto the embedded image) and
every side-by-side comparison with `compare.py` (`work/cmp_*.png`) was looked at; series, ranges and scales match.

| panel | type | data | tier | notes |
|---|---|---|---|---|
| Fig. 1a | volume rendering with reslices | – | – | |
| Fig. 1b–c | contour-reslice EM images | – | – | |
| Fig. 1d | EM section with boxes | – | – | |
| Fig. 1e–k | EM micrographs at 3 resolutions | – | – | |
| Fig. 2a–f | EM reslices/micrographs with reconstructions | – | – | |
| Fig. 3a–f | renderings of reconstructions | – | – | |
| Fig. 4a | rendering with reconstructions and Z-Brain label | – | – | |
| Fig. 4b | 22×22 cost matrix, colour key 2000–6000 | `fig4b.csv` | 3 | cell colour → key; checked against printed costs (below) |
| Fig. 4c | axon traces, top/side views, printed costs | – | – | spatial traces with scale bar only |
| Fig. 4d | EM cross-section with axon dots | – | – | |
| Fig. 4e | 6×6 matrix, key 0–180° / 0–8 µm | `fig4e.csv` | 3 | |
| Fig. 4f | top view of 6 axon pairs | – | – | |
| Fig. 4g | heatmap, angle difference vs slice | `fig4g.csv` | 3 | grid, 80 × 668 px |
| Fig. 4h | heatmap, distance difference vs slice | `fig4h.csv` | 3 | grid, 80 × 668 px |
| Fig. 4i | line plot, 2 series | `fig4i.csv` | 3 | |
| Fig. 4j | 6×6 variance matrix, key 0–22.5° / 0–1 µm | `fig4j.csv` | 3 | |
| ED Fig. 1a, c, i | EM micrographs | – | – | |
| ED Fig. 1b, g | schematic / rendering | – | – | |
| ED Fig. 1d–f, h | photographs | – | – | |
| ED Fig. 2a–d | CAD renderings | – | – | |
| ED Fig. 2e | wafer photograph | – | – | |
| ED Fig. 2f | overview EM | – | – | |
| ED Fig. 3a–c | section stack, rendering, reslices | – | – | |
| ED Fig. 3d | 3 histograms + 2 insets | `edfig3d.csv` | 3 | 50-section bins not resolved (≈1.2 px/bin): per pixel column; insets per 5-section bin |
| ED Fig. 4a–c | section stack, rendering, reslices | – | – | |
| ED Fig. 4d | 3 histograms | `edfig4d.csv` | 3 | per bar run |
| ED Fig. 5a–i | overview EM sections and enlargements | – | – | |
| ED Fig. 5j | bar chart | `edfig5j.csv` | 3 | |
| ED Fig. 6a–b | software screenshots | – | – | |
| ED Fig. 7a–g | renderings, EM/fluorescence pairs | – | – | |
| ED Fig. 8a–h | renderings and reslices with atlas labels | – | – | |
| ED Fig. 9a, d | axon traces with printed costs | – | – | |
| ED Fig. 9b, c, e, g | schematics | – | – | transcribed in the description |
| ED Fig. 9f | 6×6 matrix with key | `edfig9f.csv` | 3 | identical to Fig. 4e within reading error |
| ED Fig. 9h | two heatmaps (a, d), 15 pairs | `edfig9h_a.csv`, `edfig9h_d.csv` | 3 | grids |
| ED Fig. 9i | top view of 22 axon pairs | – | – | |
| ED Fig. 9j, k | heatmaps, 231 pair rows | `edfig9j.csv`, `edfig9k.csv` | 3 | grids, 361 × 871 px; single pair rows (≈1.56 px) not resolved |
| ED Fig. 10a–o | EM sections and enlargements | – | – | |

**How the colour maps were read** (`tools/cmap_common.py`): the printed colour bar is sampled in the figure image (one RGB
per pixel row, linear from 0 at its bottom edge to the top label at its top edge) and each cell or pixel takes the value
of the nearest key colour. Heatmaps (`tools/heatmap_grid.py`): one CSV row per image pixel row, one column per pixel
column (header = slice number of the column), black = no data (empty); pixels darkened by blending with thin black
no-data stripes are matched on colour direction instead (counts in each CSV header).

**Cross-checks against numbers printed in the paper:**
- Fig. 4b vs printed costs (Fig. 4c, ED Fig. 9a, d): MiD3cm/MiD3cm read 2006 (printed 1315, below the key, so at its yellow
  end), MiD2cm 2006 (2054), MiD2i/MiD2i 2031 (2062), MiM1 #1/MiM1 #1 2354 (2321), MiD2i/MiM1 #1 2354 (2242), MiM1 #1/MiD2i
  2155 (1967), CaV row/MeMv column 5968 (printed 14608, above the key). So ±50–200 near the flat yellow end of the key;
  the asterisk pattern (20 black on the diagonal, 2 red at MiD2i/MiM1 #1) matches the caption.
- ED Fig. 9d: 2242 + 1967 = 4209 vs 2062 + 2321 = 4383, difference 174, as the caption says ("by 174").
- ED Fig. 5j: 84 + 81 + 43 = 208, the printed "208 total".
- ED Fig. 3d: bar area gives 243 lost (printed 244) and 276 partial (printed 283); 5 adjacent bars (printed 5).
  The insets (5-section bins) hold 32 lost (z 5000–5500) and 43 partial (z 1250–1750) sections, while the main histograms'
  bar area over the same z ranges gives ≈41 and ≈52: the main histograms are too coarse (≈1.2 px per bin, anti-aliased) to
  pin this down.
- ED Fig. 4d: bar runs give 6 lost (printed 6), 24 partial (25) and 5 adjacent (6); two runs near z ≈ 300 may each hide a
  second bin.
- Fig. 4i/Fig. 4g: the red slice marker sits at slice 5559 on the calibrated axis (caption: slice 5560); ED Fig. 9f equals
  Fig. 4e cell by cell within reading error.
- Main text vs captions: 17963 sections, 244 lost (1.34%), 283 partial (1.55%), 5 adjacent events (0.03%) agree with
  ED Fig. 3d; 7dpf series 6 lost, 25 partial, 6 adjacent agree with ED Fig. 4d; 80 wafers × ≈227 sections ≈ 18160 ≈ 18207.

Figure descriptions were written while looking at each figure crop (all 14 figures were viewed, the small labels of Figs.
2d, 4b–e, ED Figs. 2e, 5j, 9a–h also at 3–4× zoom).

## Text check (`check_text.py` 2026-10-17j, no options)

`python3 -I -B …/tools/check_text.py main.tex source/hildebrand2017_biorxiv_134882.pdf`

| | raw coverage | without repeated text | without in-figure text | tex tokens in PDF | MISSING ≥ 6 | EXTRA ≥ 6 |
|---|---|---|---|---|---|---|
| `main.tex` | 98.9 % | **99.9 %** (188 repeated tokens) | 99.9 % | 99.9 % | 0 | 0 |

Repeated text: the bioRxiv stamp on all 47 pages (given once in main.tex). With `--min-run 1` the remaining unmatched tokens
are explained: real hyphens at line ends that the tool joins ("light-sheet", "left-right", "domain-specific",
"co-registered" ×2, "two-dimensional"); the inline equation (i.e., Σ₁⁵ n) whose glyph order differs; and
"e\textit{lavl3}" in the Supplementary Video 5 legend (the PDF prints the "e" upright and "lavl3" italic; the checker
splits the word at the font change).

**Glyph audit** (`decompile_work/tools/glyph_audit.py --crops work/glyphs`): 18 hidden glyphs, all on p. 18 (Cambria Math
pieces of the large parentheses, norm and absolute-value bars in the two displayed equations and in "the maximum of
‖‖s_j − s_i‖ − ‖t_j^s − t_i^s‖‖"). All checked against the crops and the page image; the equations are in main.tex as
LaTeX math. The text layer's ASCII "~" (approximately) is written ∼ in main.tex.

Read-through against the page images: the equations of pp. 17–18 (compiled output compared with the page), superscript
citations, units (µm, nm³ vx⁻¹, mL⁻¹, °C/ºC as printed), –/– and +/+ genotypes, italic gene and species names, ≤, ×, the
headings and the bold/italic of figure titles.

## Errors and oddities in the paper (kept verbatim)

- Main text p. 12 (Methods, 7dpf series): "(Extended Data Fig. 5)", "Extended Data Fig. 5d top/middle/bottom": the 7dpf
  statistics are in Extended Data Fig. 4 (4d); Extended Data Fig. 5 shows partial sections of the 5.5dpf series
  (`\decompnote` added).
- Supplementary Video 6 legend: "Figure 3a−e", "Figure 3b−c" for the lateral line afferent; that neuron is shown in
  Figure 2a–e / 2b–c (`\decompnote` added).
- Extended Data Fig. 5 caption: "e–f, Expanded views…" and "g–h, Anterior examples…" for panels d–f and g–i
  (`\decompnote` added).
- Typos: "Hungrarian method" (Methods p. 17); "co-registered form a coherent" (p. 4, "to" missing); "fasiculus" (Fig. 3
  caption; `\decompnote`); "co-registrered" (ED Fig. 6 caption; `\decompnote`); "this is likely why it assignment result"
  (ED Fig. 9 caption; `\decompnote`); "this sum over for all cross-sections" (Fig. 4 caption); "Survey of traverse larval
  zebrafish" (Supplementary Video 3); "Fig 1i–k" without full stop (p. 4).
- ED Fig. 3 caption speaks of "a collection of 18207 × ∼60 nm-thick … sections"; 18207 is the number attempted, 17963
  were collected (main text p. 3).
- ED Fig. 9f is described as a "distance matrix" in the caption; it is the difference matrix of the methods.

## Time

About 30 minutes of wall-clock time by the machine clock (03:37–04:06 UTC, 2026-10-18): reading spec/brief and setting up
~3 min; text drafting, structuring and equations ~5 min; figure crops and descriptions ~7 min; digitizing the 14 data CSVs
with overlays and comparisons ~12 min; checks and README ~3 min.
