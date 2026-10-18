# pallotto2015: decompiled

Marta Pallotto, Paul V Watkins, Boma Fubara, Joshua H Singer, Kevin L Briggman. "Extracellular space
preservation aids the connectomic analysis of neural circuits." *eLife* **2015**;4:e08206.
DOI [10.7554/eLife.08206](https://doi.org/10.7554/eLife.08206). Research article, Neuroscience.
Received 18 April 2015; accepted 27 October 2015; published 09 December 2015. Reviewing editor: Michael Häusser.
(Pallotto and Watkins contributed equally; corresponding author Briggman.) All of this is taken from p. 1 of the
PDF and agrees with the task message.

**Licence** (p. 1): "This is an open-access article, free of all copyright, and may be freely reproduced,
distributed, transmitted, modified, built upon, or otherwise used by anyone for any lawful purpose. The work is
made available under the Creative Commons CC0 public domain dedication."

## Local and external

**In the local collection**
- Source files:
  - `papers/pallotto2015/elife-08206-v3.pdf` – the article, 20 pp., eLife version of record (v3) → `main.tex`
  - `papers/pallotto2015/elife-08206-figures-v3.pdf` – eLife "Figures and figure supplements" PDF, 13 pp. → `supplement.tex`
  - `papers/pallotto2015/elife_figure_supplements/elife-08206-fig{1-figsupp1,1-figsupp2,2-figsupp1,3-figsupp1,4-figsupp1}-v3.jpg` – the five figure supplements, full-size JPEGs (used for the data extraction)
  - `papers/pallotto2015/elife_figure_supplements/elife-08206-fig2-data{1..4}-v3.tif` – Figure 2 source data 1–4 (raw image + expert labels, 2016 × 1736 px, 2 frames each)
  - `papers/pallotto2015/elife_figure_supplements/elife-08206-fig3-data{1..4}-v3.zip` – Figure 3 source data 1–4 (Knossos NML dense skeletons of M0027_11 / M0007_33; six 128³ training cubes per volume)
  - `papers/pallotto2015/SOURCE.txt` – fetch note
- Cited works decompiled here: none of the 51 references is in the local collection.

**External pull needed** (not on this machine)
- Figure 4 source data 1–3 (example image stacks of an AII–AII tight contact, a cone bipolar–AII tight contact and a chemical-synapse cleft contact; ≈ 50 MB each) – https://cdn.elifesciences.org/articles/08206/elife-08206-fig4-data1-v3.tif , …-fig4-data2-v3.tif , …-fig4-data3-v3.tif – image stacks for Figure 4B–D, not plot data
- Dryad data set "Extracellular space preservation aids the connectomic analysis of neural circuits" – http://dx.doi.org/10.5061/dryad.36h28 (Data availability, p. 18; reference "Pallotto et al., 2015") – contents not known here; the paper cites it for the SBEM volumes. It might hold the analysis outputs behind Figs. 2B–D, 3C–E and the supplements, i.e. the missing tier-1 source for the digitized panels.
- All other cited references: 51 entries (unnumbered, alphabetical) without a [local: …] tag.
- (Not needed for the decompile: decision letter and author response, which this PDF does not mention.)

## Source files (`../../papers/pallotto2015/`)

| file | what it is |
|---|---|
| `elife-08206-v3.pdf` | the article, 20 pp. **Publisher version of record** (eLife typeset PDF v3, created 2016-02-12 by Arbortext/Ghostscript). Born-digital; all five figures are 300-ppi JPEGs with no vector plot content (`get_drawings()` finds only the figure frames). The text layer renders the Greek μ (Symbol font) as "m": "1 mm", "2 ms" in the text layer are μm, μs on the page. |
| `elife-08206-figures-v3.pdf` | eLife figures PDF, 13 pp.: cover page; Figs. 1–5 again (images pixel-identical to the article PDF; legends identical except "The following source data is available for figure N:" and no figure-supplement lines); the five figure supplements with their legends. |
| `elife_figure_supplements/*.jpg` | the five figure supplements as full-size JPEGs; same pixel size as the images in the figures PDF, mean difference 0.4–3 grey levels (JPEG re-encoding). |
| `elife_figure_supplements/elife-08206-fig2-data{1..4}-v3.tif` | Figure 2 source data 1–4: 2-page ImageJ TIFFs, frame 1 = raw EM image, frame 2 = expert labels with grey 0 (membrane), 85 (ECS), 171 (intracellular). The grey-85 area fractions are 0.59, 5.78, 11.36 and 24.1 %, matching the data sets' ECS fractions 0.6, 5.8, 11.3, 23.9 %. The whole 2016 × 1736 frame is labelled (the methods speak of a 1920 × 1728-pixel labelled portion). |
| `elife_figure_supplements/elife-08206-fig3-data{1..4}-v3.zip` | unzipped (read-only use, nothing executed) into `work/zips/d1..d4`: `M0027_11_dense_skels.186.nml` (data 1, LowECS), `M0007_33_dense_skels.152.nml` (data 2, HighECS), six `M0007_33_groundtruth_cleaned_x…_y…_z….tif` (data 3, HighECS) and six `M0027_11_groundtruth_cleaned_….tif` (data 4, LowECS): 128 × 128 × 128 uint16 label volumes, 0 = membrane, 1 = ECS, ≥ 2 = one intracellular object each. The NML files give voxel size 9.8 × 9.8 × 25 nm. |

## Contents

- `main.tex` / `main.pdf`: the whole article in reading order: article type, subject and footer citation (once),
  title, authors, affiliations, the p. 1 margin block (correspondence, equal contribution, competing interests,
  funding pointer, dates, reviewing editor, CC0 statement), abstract, eLife digest (placed after the paragraph it
  interrupts), Introduction, Results, Figures 1–5 with legends, source-data and figure-supplement lines and DOIs,
  Discussion, Materials and methods, Acknowledgements, Additional information (funding table, author
  contributions, ORCID, ethics), Additional files (datasets table), 51 references.
- `supplement.tex` / `.pdf`: the whole figures PDF: cover page, Figs. 1–5 (images reused, legends verbatim,
  descriptions pointing to `main.tex`), and Figure 1—figure supplements 1–2, Figure 2—figure supplement 1,
  Figure 3—figure supplement 1, Figure 4—figure supplement 1 with images, verbatim legends and descriptions.
  (The task asked for `figure_supplements.tex`; the coordinator renamed it to the SPEC's `supplement.tex`.)
- `figures/`: `fig1.png` … `fig5.png` (200-dpi crops of the article PDF), `sfig1-1.png`, `sfig1-2.png`, `sfig2-1.png`,
  `sfig3-1.png`, `sfig4-1.png` (200-dpi crops of the figures PDF). Naming: Figure N—figure supplement M → `sfigN-M`,
  panel x → `sfigN-Mx`. Data: one CSV per plotted panel, extraction scripts `*_extract.py`, plot scripts and
  `*_replot.png` (table below); `pal_common.py` holds the shared helpers (image loading, axis fits, template
  matching, curve tracing, colour masks, CSV reader).
- `tables/funding.csv`, `tables/datasets.csv`: the two untitled tables on p. 18 (also as `tabular` in `main.tex`).
- `work/`: scratch: page renders, unzipped Figure 3 source data (`work/zips/`, ≈ 52 MB; re-created by
  `figures/sfig3-1_extract.py` if missing), extracted embedded images, overlays, `cmp_*.png` side-by-sides,
  helper scripts used while calibrating. May be deleted.

Compile: `TEXINPUTS=../tools: lualatex -interaction=nonstopmode -halt-on-error main.tex` (and
`supplement.tex`); both compile without errors (run twice); some overfull lines (long DOIs, the tables).

Re-run the data: `python3 -I figures/<x>_extract.py` then the plot script, for x = fig1b, fig2 (B–D), fig3 (C–E),
fig4f, fig5c, sfig1-1a, sfig2-1a, sfig2-1c, sfig3-1 (A–C), sfig4-1a. Plot scripts: `fig1b.py`, `fig2.py`, `fig3.py`,
`fig4f.py`, `fig5c.py`, `sfig1-1a.py`, `sfig2-1.py` (A and C), `sfig3-1.py` (A–C), `sfig4-1a.py`. The main-figure
scripts read the embedded JPEGs straight from the PDF (PyMuPDF), the supplement scripts read the eLife JPEGs.

## The fixation / staining / embedding protocol (where to find it)

Transcribed verbatim in `main.tex`, Materials and methods, p. 12–14: "Tissue fixation protocols" (acute slices:
ACSF composition, 2 % GA in 100/150/175/200 mM sodium cacodylate at 20 °C for 8 h, 4 h rinse; perfusion: 2 % GA +
2 % PFA in 150 mM CB, 8 h postfix, 4 h rinse; isolated retina: modified Ames, 2 % GA in unbuffered sucrose or in
150 mM CB, 1 h), "EM tissue staining" (ROTO: 1 % OsO₄ + 1.5 % potassium ferrocyanide + 150 mM CB 2 h RT; 1 %
aqueous TCH 1 h at 50 °C; 2 % aqueous OsO₄ 1 h RT; 2 % aqueous uranyl acetate 12 h RT; lead aspartate 2–12 h RT;
Epon), "Antibody labeling" (2 % PFA + 0.01 % GA in 7.5 % sucrose or 150 mM CB, …), and SBEM re-embedding in Epon
Hard (p. 14). The paper uses chemical fixation only; high-pressure freezing and rapid freezing are discussed, not used.
No dehydration or resin-infiltration schedule and no lead-aspartate recipe is given (the staining is cited to
Briggman et al., 2011). Osmolarities quoted: 100 mM CB = 204 mOsm, 175 mM CB = 343 mOsm (p. 4).

## Figures

All plots are raster images: no panel is tier 2. Fig. 3—figure supplement 1A is **tier 1** (computed from the eLife
source data and checked against the print); everything else plotted is **tier 3**. Two more panels carry a companion
CSV computed from the source data that does *not* reproduce the print exactly (see below).

| panel | type | data | tier | notes |
|---|---|---|---|---|
| Fig. 1A | flow-chart schematic | – | – | steps and interventions transcribed in `\alttext` |
| Fig. 1B | scatter (3 marker types) + 2 fit lines, broken x axis | `figures/fig1b.csv` | 3 | 14 + 3 + 9 points + perfused cluster; recomputed R = 0.80 / 0.79 match the caption |
| Fig. 1C–F | EM micrographs, ECS coloured cyan | – | – | |
| Fig. 2A | 4 × 4 EM / label / network output / segmentation images | – | – | Source data 1–4 = raw images + labels (local) |
| Fig. 2B | scatter (folds) + medians | `figures/fig2b.csv` | 3 | 28 of 36 circles resolved |
| Fig. 2C | scatter + medians | `figures/fig2c.csv` | 3 | 24 of 36 |
| Fig. 2D | scatter + medians | `figures/fig2d.csv` | 3 | 24 of 36 |
| Fig. 3A, B | 3D renderings (EM cube, skeletons, segmentation) | – | – | |
| Fig. 3C | line plot, categorical thresholds, 99 % bands | `figures/fig3c.csv` | 3 | value + band at each of 18 ticks |
| Fig. 3D | parametric curves with bands + 2 solid points | `figures/fig3d.csv` | 3 | per pixel column |
| Fig. 3E | line plot, categorical thresholds, bands | `figures/fig3e.csv` | 3 | peaks 46.7 % (HighECS), 40.3 % (LowECS); text 47 % / 40 % |
| Fig. 4A, E | 3D surface renderings | – | – | |
| Fig. 4B–D | EM images + 3D renderings | – | – | source data 1–3 (image stacks) external |
| Fig. 4F | stacked bars | `figures/fig4f.csv` | 3 | 17 + 4 / 130 + 7 + 13 |
| Fig. 5A, B | confocal images | – | – | |
| Fig. 5C | means ± SEM | `figures/fig5c.csv` | 3 | means match text; two bars do not (below) |
| Fig. 5D | EM images | – | – | |
| Fig. 1—fs1 A | means ± SEM, broken x axis | `figures/sfig1-1a.csv` | 3 | 5 points |
| Fig. 1—fs1 B, Bi–Biii | schematic + 3 EM images | – | – | |
| Fig. 1—fs2 A–D | EM images | – | – | |
| Fig. 2—fs1 A | 4 curves with SEM bands + circles | `figures/sfig2-1a.csv` | 3 | bands only for 0.6 % (others overlap) |
| Fig. 2—fs1 B | label images + segmentations | – | – | |
| Fig. 2—fs1 C | 4 CDFs, log x, median crosses | `figures/sfig2-1c.csv` (+ `sfig2-1c_sourcedata.csv`) | 3 (+ source-data reconstruction) | see below |
| Fig. 3—fs1 A | 2 CDFs, log x | `figures/sfig3-1a.csv` | **1** | 182 (LowECS) / 270 (HighECS) objects from the training cubes |
| Fig. 3—fs1 B | 2 CDFs, log x | `figures/sfig3-1b.csv` (+ `sfig3-1b_sourcedata.csv`) | 3 (+ source-data reconstruction) | see below |
| Fig. 3—fs1 C | 2 CDFs | `figures/sfig3-1c.csv` (+ `sfig3-1c_sourcedata.csv`) | 3 (+ source-data reconstruction) | see below |
| Fig. 4—fs1 A | log–log scatter, 3 classes | `figures/sfig4-1a.csv` | 3 | 79/150 grey, 16/17 green, 3/4 blue resolved |

Panels per tier: tier 1: 1 (Fig. 3—fs1 A); tier 2: 0; tier 3: 15 (Figs. 1B, 2B, 2C, 2D, 3C, 3D, 3E, 4F, 5C;
Fig. 1—fs1 A; Fig. 2—fs1 A, C; Fig. 3—fs1 B, C; Fig. 4—fs1 A); tier 4: 0. Three of the tier-3 panels also have a
source-data reconstruction file.

**How the digitizing was done** (details in each script's docstring and CSV header): axis frames and tick marks
were located in the embedded image (dark-pixel runs along the axis lines) and fitted linearly (or log10); the
residuals are in each CSV header. Markers: template matching (ring template for the open circles of Fig. 2,
templates cut from clean markers for Fig. 1B, filled-disc and x templates for Fig. 4—fs1), refined from positions
picked on gridded zooms where needed; red medians and bar segments by colour components; curves by colour masks
per pixel column, following each line with a linear prediction across hidden stretches; the categorical-axis
polylines of Fig. 3C/E by fitting each straight segment and intersecting at the ticks.

**Checks:** every extraction was drawn back onto the source image (`work/*_overlay.png`; zoomed and looked at,
including the hidden/overlapping regions), and every re-plot was put next to the original panel with
`tools/compare.py` (`work/cmp_*.png`, also combined in `work/cmp_allA.png`, `cmp_allB.png`) and looked at: ranges,
scales (log axes in Fig. 2—fs1 C, 3—fs1 A/B, 4—fs1 A), series, markers and bands match. Independent checks against
numbers printed in the paper: Fig. 1B fits give R = 0.80 (olfactory bulb, n = 14) and R = 0.79 (cortex, n = 9)
(caption: 0.80, 0.79); Fig. 5C means 6.8, 28.1, 6.1, 16.9 μm (text: same); Fig. 4F heights round to 17 + 4 and
130 + 7 + 13 (text: 21 tight, 150 cleft, 4 AII, 17 cone bipolar, 13 amacrine); Fig. 3E peaks 40.3 / 46.7 % (text
40 % / 47 %); Fig. 3D solid points (41.7, 17.1) and (41.5, 10.4).

**Source data, what they reproduce:**
- *Fig. 3—fs1 A (tier 1):* object sizes (voxel counts of labels ≥ 2) of the six training cubes per volume. The step
  CDFs lie on the printed curves (`work/sfig3-1a_tier1_overlay.png`); medians 11 779 (LowECS) and 3 673 (HighECS)
  voxels sit at the printed crosses.
- *Fig. 3—fs1 B, C:* from the NML skeletons (all non-empty "things"): LowECS 241 skeletons, 5477 nodes, 3.292 mm,
  median 9.97 μm, 16 nodes; HighECS 219 skeletons, 5798 nodes, 3.397 mm, median 11.47 μm, 19 nodes. The total
  path lengths match the text (3.29 / 3.40 mm), but the paper gives 220 / 217 skeletons, 5130 / 5364 nodes and
  medians 10.2 / 10.1 μm and 16 / 17 nodes, and the printed HighECS curves lie left of the full-file HighECS CDF
  (`work/sfig3-1_srcdata_overlay.png`). Cropping z to 480 slices (12 μm) brings the node counts near the paper's
  (e.g. HighECS z 29–508: 218 skeletons, 5364 nodes, median 17 nodes, 10.55 μm), so the plotted data were
  probably restricted to the 10 × 10 × 12 μm³ analysis region, whose exact position is not given. These panels
  therefore stay tier 3, with the NML statistics as `_sourcedata.csv` companions.
- *Fig. 2—fs1 C:* 4-connected intracellular components of the expert labels, computed in the nine 640 × 576
  sub-images of the top-left 1920 × 1728 pixels. Medians 746 / 449 / 490.5 / 274 pixels (0.6 / 5.8 / 11.3 / 23.9 %)
  vs. printed crosses ≈ 746 / ≈ 475 / ≈ 468 / ≈ 277. The printed curves are 0 below ≈ 18 pixels and drawn as
  straight segments ≈ 0.25 decade apart, while the labels contain 1–17-pixel objects; variants (whole image, one
  undivided block, other crop offsets, minimum-size filters) were tried; their medians are 4–15 % higher, so none
  matches better. Tier 3 stays primary.
- Figure 2 source data are the panel A images; Figure 3 source data are inputs, not the values of Fig. 3C–E.

## Text check (`tools/check_text.py`, version 2026-10-17i)

| file | coverage of PDF tokens | without text repeated on ≥ 3 pages | running text (also without in-figure text) | tex tokens found in PDF | MISSING ≥ 6 | EXTRA ≥ 6 |
|---|---|---|---|---|---|---|
| `main.tex` | 98.8 % | **99.7 %** (119 repeated tokens) | 99.7 % | 99.6 % | 0 | 0 |
| `supplement.tex` | 90.0 % | **99.2 %** (181 repeated tokens) | 99.2 % | 99.1 % | 0 | 0 |

Everything unmatched (`--min-run 1`) is explained:
- Repeated: running header "Research article Neuroscience" + "n of 20/13" (both files) and the footer citation
  "Pallotto et al. eLife 2015;4:e08206" (figures PDF; given once in `main.tex`).
- MISSING/EXTRA singletons "mm"/"m" and "ms"/"s" (main: 36 runs, one of them "mm a e 1 mm" in the Fig. 4 legend; supplements file: 14): the Symbol-font μ, which
  the text layer reads as "m"; the page images show μm / μs, which are transcribed.
- "reembedded" (main p. 14) and "crossvalidation" (figures p. 5): real hyphens at line ends, transcribed as
  "re-embedded", "cross-validation".
- EXTRA "research article neuroscience" / "research article": the article type and subject given once.
All figures are images without text in the text layer, so the third number (in-figure text left out) equals the second.

Read-through against the page images (step 4) done for: μm/μs (every instance), ×  (SBEM section, where the text
layer has no glyph), °C, ±, superscripts (μm³, nm³, nm², μm²), subscripts in the ACSF salts (including the printed
"H₂0" with a zero), "~" (\textasciitilde), the □ marker in the Fig. 1 legend, T_min, en dashes in ranges, the eLife
digest's ’ quotes, and the order of text, figures and the "Figure N continued" blocks. Figure legends were
compared between the two PDFs (wording differs only in the source-data/supplement lines).

## Errors and inconsistencies found in the paper (kept verbatim; most flagged with `\decompnote`)

- **Temperatures:** text (p. 4) and methods (p. 12) say slices were cut at 4 °C or 20 °C and fixed at 20 °C; the
  Figure 1—figure supplement 2 legend and panel titles say 4 °C or 25 °C dissection and 25 °C fixation.
- **Fig. 5C vs text:** the error bars of VAChT ECS fix (≈ ±0.95 μm) and VGAT conv fix (≈ ±0.95 μm) do not match
  the text's SEMs (2.4 and 0.4 μm); VGAT ECS (≈ ±1.0) and VAChT conv (≤ ±0.4, bar hidden by the marker) do.
- **Fig. 3D vs text:** "the LowECS data achieved a lower node merger error rate", but the plotted minimum points
  show fewer merged nodes for HighECS (≈ 10 % vs ≈ 17 %).
- **Skeleton statistics:** text 220 / 217 skeletons and 5130 / 5364 nodes; the published NML files hold 241 / 219
  non-empty skeletons and 5477 / 5798 nodes (path lengths agree). The text's IQRs of the path length
  ([7.6–13.3] and [6.6–12.7] μm) are much narrower than those of the files (≈ 4.5–17.7 and 5.8–19.9 μm) and of the
  printed CDFs (25–75 % at ≈ 4–18 μm), so they are probably not interquartile ranges.
- Methods (3D metrics) cite "Figure 3—figure supplement 1A" for nodes per skeleton; that is panel C.
- Fig. 4F counts 7 cone-bipolar (green) contacts inside the cleft bar; the text puts all 137 non-chemical cleft
  contacts in "other". "A2" (source-data titles) = AII.
- Text cites "Strettoia et al., 1992" (reference: Strettoi), "Rash et al., 1998" (reference: "Rash J. 1998"),
  "Harreveld and Fifkova 1975" (reference: van Harreveld), "van Harreveld and Khattab 1968" (no reference entry).
- Methods: "M007_33" once for M0007_33; "NaH₂PO₄.H₂0" with a zero; "the modified ACSF solution" in the antibody
  protocol where the retina protocol defines a modified Ames solution; "84 NaHCO₃" in the ACSF (background
  knowledge, not from the paper: standard ACSF has ≈ 26 mM NaHCO₃, so 84 is probably a typo — not changed).
- Caption Fig. 4: "tight contact (C)" repeated inside panel C's description; "vACHT" vs "VAChT"; Fig. 3—fs1 C
  legend "The distributions not significantly different"; "procotol", "in vivoECS", "shrinked" (text).
- References: "Neutral Information Processing Systems" (twice); Nunez-Iglesias 2013 DOI ends ".s004"; Nunez-Iglesias
  2014 (Frontiers in Neuroinformatics) carries a 10.1109/TPAMI DOI; background knowledge, not from the paper: the
  Turaga 2010 DOI 10.1098/rstb.1986.0056 is a Phil. Trans. R. Soc. B DOI, not Neural Computation's.

## Known problems and limitations

- Overlapping markers: Fig. 2B–D (28/24/24 of 36 circles), Fig. 4—fs1 A (79 of 150 grey crosses, 3 of 4 blue dots;
  the elongated blue blob is probably two dots), Fig. 1B perfused cluster (only the x at ≈ 0.5 % and the square at
  0 % are given). Each CSV header gives the counts.
- Overlapping curves: Fig. 2—fs1 A (5.8 % traced only from splits ≈ 0.18 on; bands only for 0.6 %), Fig. 2—fs1 C,
  Fig. 3—fs1 B/C (lower curve hidden where they coincide), Fig. 3C/E (some vertices from one segment only;
  LowECS at 0.999999 hidden in C, flagged).
- The Fig. 3C/E band edges are taken in the tick column; where the band is narrower than the 5-px line they are the
  line edges (flag `band_hidden`).

## Problems and suggestions for the spec and tools

- `digitize_common.py` has no marker or curve helpers for the common cases here (open-circle scatter, x/square
  markers, overlapping coloured curves, categorical-axis polylines). `figures/pal_common.py` has
  `match_peaks`/`refine` (template matching), `ring_template`, `trace_curve`/`trace_both` (colour-run tracing with
  linear prediction across hidden stretches) and `polyline_vertices` (vertex values on a categorical axis); worth
  moving into `tools/`.
- `check_text.py`: the Symbol-font μ → "m" mismatch is systematic in eLife (and other) PDFs and produced 50 of the
  53 unmatched runs here (all but the two line-end hyphens and the header); mapping a tex "μ" to "m" (or ignoring a lone "m"/"s" after a number) would make
  the remaining runs more informative.
- SPEC: tier 1 is defined as "the authors' own data file", but here the files are *inputs* from which the plotted
  quantity must be computed, sometimes by a procedure the paper does not fully state. A labelled tier such as
  "1-derived (computed from source data, checked against the print)" plus a rule for when a reconstruction that
  does not match the print may still be shipped (as a companion file) would help.
- SPEC: the task pointed to "the SPEC's eLife notes", but the SPEC has one sentence on eLife (figure supplements
  from the API). It does not cover the eLife figures PDF (which repeats the main figures with slightly different
  legends) or the file name (the task asked for `figure_supplements.tex`; renamed to `supplement.tex` as in templier2019/stroh2022).
- SPEC: placing a full-page figure "at the end of the paragraph that spans that point" puts `\pdfpage` markers out
  of order three times in this paper (p. 3, 5, 11); it works, but a note in the SPEC that this is expected for
  eLife's full-page figures would save the per-case `\decompnote`s.
