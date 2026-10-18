# nguyen2016: decompiled

Huy Bang Nguyen, Truc Quynh Thai, Sei Saitoh, Bao Wu, Yurika Saitoh, Satoshi Shimo, Hiroshi Fujitani,
Hirohide Otobe, Nobuhiko Ohno. "Conductive resins improve charging and resolution of acquired images in
electron microscopic volume imaging." *Scientific Reports* **6**, 23721 (2016).
DOI [10.1038/srep23721](https://doi.org/10.1038/srep23721).
Received 11 November 2015; accepted 14 March 2016; published 29 March 2016.

**Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0), as stated on p. 10.

## Local and external

**In the local collection**
- Source files:
  - `papers/nguyen2016/srep23721.pdf` – the article, 10 pp., publisher's version of record
  - `papers/nguyen2016/srep23721.txt`, `papers/nguyen2016/srep23721.raw.txt` – earlier text extractions (not used)
  - `papers/nguyen2016/SOURCE.txt` – fetch note
- Cited works decompiled here: hua2015 (`decompiled/hua2015/`), mikula2015 (`decompiled/mikula2015/`)

**External pull needed** (not on this machine)
- Nothing besides the references: the paper has no supplementary information and names no data set or source-data file.
- All other cited references: 32 entries in the reference list (1–34) without a [local: …] tag.

## Source files (`../../papers/nguyen2016/`)

| file | what it is |
|---|---|
| `srep23721.pdf` | the article, 10 pp. **Publisher's version of record** (Scientific Reports typesetting, masthead, running header `www.nature.com/scientificreports/`, footer `SCIENTIFIC REPORTS \| 6:23721 \| DOI: 10.1038/srep23721` + page number). `SOURCE.txt`: fetched from nature.com/articles/srep23721.pdf on 2026-10-12. |
| `srep23721.txt`, `.raw.txt` | earlier text extractions (looked at, not used). |

The paper has no supplementary information (the nature.com page lists none), and it names **no data set or
source-data file** (no data-availability statement). So no tier-1 source was missing. Table 1 (imaging
conditions) is the only tabulated data; see the Fig. 5h cross-check below.

## Contents

- `main.tex` / `main.pdf`: the whole article in reading order (journal footer once, OPEN label, title, dates,
  authors, affiliations + correspondence (a p.1 footnote, placed after the authors), abstract, introduction,
  Results, Discussion, Materials and Methods, Table 1, 34 references, Acknowledgements, Author Contributions,
  Additional Information incl. competing interests, how to cite, licence). `\pdfpage{N}` marks every page start.
- `figures/fig1.png` … `fig5.png`: each figure rendered from the PDF at 200 dpi (image bbox + 4 pt margin).
- Plotted panels: `fig1b`, `fig5h`, `fig5i`, each with `.csv`, `_extract.py`, `.py`, `_replot.png`.
  `pairs_common.py` holds the marker/line helpers used by `fig5h_extract.py` and `fig5i_extract.py`;
  `fig5i.py` is the same code as `fig5h.py` (it picks its settings from its own file name).
- `tables/table1.csv`: Table 1, cell by cell, caption in `#` lines.
- `work/`: scratch (page renders, embedded images, vector dumps, overlays `*_overlay*.png`, side-by-side
  comparisons `cmp_*.png`, `check.json`). May be deleted.

Compile: `TEXINPUTS=../tools: lualatex -interaction=nonstopmode -halt-on-error main.tex` (twice); no errors.
Re-run data: `python3 -I figures/<panel>_extract.py`, then `python3 -I figures/<panel>.py` (any working dir).

## Figures

Each figure is **one embedded JPEG** (Figs 1–5, about 220 ppi: 917×1309, 907×1808, 1210×607, 1210×1643,
1210×1229 px). `tools/vector_dump.py` (re-run after the coordinator's fix for zero-width lines) finds only the
dotted grey separator rule under each caption in the figure areas, so there are no vector plots: all
plotted panels are **tier 3 (digitized)** from the embedded image at native resolution.

- **Fig. 1b** (log scatter): 4 black discs located as connected components (centroids); x calibrated on the
  4 labelled ticks (residual 0.008 wt%), y on the 5 log ticks 10⁰–10⁴ (residual 0.009 decades).
- **Fig. 5h, 5i** (paired dot plots): semi-transparent markers ~9.5 px across, joined by thin lines of the same
  colour. Marker centres from the colour run down each category column (half-ink edges, sub-pixel); where
  markers overlap partly, centre = visible edge ± radius; in the Fig. 5h Carbon cluster (six markers between
  ~600 and 1500 nm³) the hidden centres come from least-squares fits of the connecting lines. Pairs are
  assigned by following each line (checked in code for 5i). Uncertainty is given per marker type in the CSV
  headers (5h: ±20 nm³ isolated, ±44 nm³ edge-covered, ±87 nm³ in the cluster; 5i: ±0.19 e⁻/nm²).
  Note: on isolated markers the connecting lines miss the marker centres by up to ~2–5 px on steep segments,
  so line ends are used only where nothing better is visible.

**Checks done:** every extraction draws its points onto the source image (`work/fig1b_overlay_zoom.png`,
`work/fig5h_overlay_zoom.png`, `work/fig5i_overlay_zoom.png`), and every replot was put next to the original
with `tools/compare.py` (`work/cmp_fig1b.png`, `cmp_fig5h.png`, `cmp_fig5i.png`). I looked at all six:
the points sit on the markers, and series, ranges and scales (log y in 1b) match.

**Cross-check of Fig. 5h against Table 1** (my calculation, not in the paper): Methods define voxel size
as (pixel resolution)² × slice thickness; Table 1 lists 7 Normal/Conductive pairs for Fig. 5h, giving
1299.6/640.0, 3698.0/974.7, 8487.2/2957.5, 1740.5/1440.0, 2371.6/1392.4, 2964.5/921.6, 1152.0/739.6 nm³.
The digitized pairs are 8497/3011, 3688/1126, 2929/815 (purple), 2869/983 (green), 2309/1360, 1409/677,
1128/677. Five or six of them line up with table pairs within ~1–4 px (8487/2958, 3698/975, 2372/1392,
1152/740, 1300/640, and 2965/922 with one of the two ~2900 pairs), but the table pair 1740.5/1440 has no
counterpart in the plot, while the plot has a second pair starting near 2900 nm³. So Fig. 5h and Table 1
do not agree completely (or the table rows are not all the plotted pairs). Fig. 5i can't be checked this
way: the probe current is given only for the Merlin (150 pA), and the table does not say which
microscope each row used.

| panel | type | data | tier | notes |
|---|---|---|---|---|
| Fig. 1a | TEM micrograph (Ketjen black) + inset photo of powder | – | – | |
| Fig. 1b | scatter plot, log y, + inset photo of block | `figures/fig1b.csv` | 3 digitized | 4 points |
| Fig. 1c | schematic (resin preparation, steps i–v) | – | – | transcribed in `\alttext` |
| Fig. 1d–h | light micrographs (kidney d–f, brain g, h; inset in h) | – | – | |
| Fig. 2a–h | SEM block-face images (insets in a, b) | – | – | |
| Fig. 3a, b | SBF-SEM images | – | – | |
| Fig. 3c–e | 3D renderings / reconstructions | – | – | |
| Fig. 4a–c | single-colour and merged SBF-SEM images | – | – | |
| Fig. 4d–g | merged SBF-SEM images with insets | – | – | |
| Fig. 5a–f | SBF-SEM X-Y and X-Z images | – | – | |
| Fig. 5g | 2×4 merged serial images (Success/Skipping) | – | – | |
| Fig. 5h | paired dot plot, voxel size | `figures/fig5h.csv` | 3 digitized | 7 pairs |
| Fig. 5i | paired dot plot, electron dose | `figures/fig5i.csv` | 3 digitized | 6 pairs |
| Table 1 | table | `tables/table1.csv` | (text) | |

## Text check (`tools/check_text.py`)

| file | coverage of PDF tokens | without text repeated on ≥3 pages | tex tokens found in PDF | MISSING ≥6 | EXTRA ≥6 |
|---|---|---|---|---|---|
| `main.tex` | 98.5 % | 99.2 % (45 tokens repeated) | 98.7 % | 0 | 0 |

With `--min-run 1`, everything left over is explained:
- Repeated (9 pages): the running header `www.nature.com/scientificreports/` plus the page number; on p. 1 the
  same header (4 tokens) and page number "1" are reported singly because p. 1 has no trailing slash form;
  boilerplate, left out. (The footer "Scientific Reports | 6:23721 | DOI…" is matched by the copy given once
  at the top.)
- "open": the OPEN label, transcribed but placed after the footer line, so it counts as moved.
- 34 × "40962"/"81922"/"30722" (MISSING) vs "4096 2" etc. (EXTRA): Table 1 image sizes with a superscript 2
  (4096²), glued to the number in the PDF text layer; "234" = "TrakEM2" + superscript reference 34, glued.
No transcription errors remained.

Read-through against the page images (step 4) done for: μ (1-μm-thick, 30-μm aperture, scale bars), °C,
"(<1mm in size)", OsO₄ and K₄[Fe(CN)₆] subscripts, "(=(pixel resolution)² × slice thickness)", nm²/nm³,
"*p < 0.05", "N = 7 (h) or 6 (i)", en dashes in citation ranges and panel ranges, Table 1 cells (all 35 rows
read off a 200 dpi render), bold panel letters in captions, italic *en bloc*, journal names, bold volumes.

## Errors and oddities in the paper (kept verbatim)

- Ref. 8: page range "2424–2332" (end lower than start); flagged with `\decompnote`.
- Ref. 1 is dated (2011) with volume 22 of Curr Opin Neurobiol; from my background knowledge (not from
  anything in the source folder) that volume and the article are 2012. Not flagged in main.tex.
- Fig. 5 caption: brain is "purple dot and line" (singular), but panels h and i each show three purple
  pairs; flagged with `\decompnote`.
- Fig. 5h vs Table 1: one Table 1 pair (1740.5/1440 nm³ by the Methods formula) is not in the plot, and the
  plot has an extra pair near 2900 nm³ (see cross-check above). Not flagged in main.tex (it depends on my
  calculation).
- Fig. 1b: y axis unit printed "Ω/cm", while the text calls it "surface resistance" measured by the
  4-point-probe method (usually given in Ω/sq; resistivity in Ω·cm). The x axis is "wt%" while the text gives
  the chosen concentrations as "% (w/v)".
- Fig. 2 caption: "10μm" with no space (trivial).

## Known problems

- Fig. 5h Carbon cluster: values for 3 of the 7 Carbon markers rely on connecting-line fits (±~90 nm³).
- Fig. 5i: at Cont ≈ 16 and Carbon ≈ 51 two markers coincide; both get the same value.
- Fig. 1b series name "Conductive Plain resin" is taken from the main-text sentence that cites Fig. 1b; the
  figure itself has no legend.
