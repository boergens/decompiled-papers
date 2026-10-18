# scheffer2020: decompiled

Louis K Scheffer, C Shan Xu, Michal Januszewski, Zhiyuan Lu, Shin-ya Takemura, Kenneth J Hayworth, Gary B Huang,
Kazunori Shinomiya, … Viren Jain, Stephen M Plaza (115 authors; full list in `main.tex`).
"A connectome and analysis of the adult *Drosophila* central brain." *eLife* **2020**;9:e57443.
DOI [10.7554/eLife.57443](https://doi.org/10.7554/eLife.57443) (printed in every page footer).
Received 31 March 2020; accepted 01 September 2020; published 07 September 2020. Reviewing editor: Eve Marder.
DOI check: verify-sources receipt `vs-20261013-72c9081bdb` (Crossref record for 10.7554/eLife.57443 matched to this PDF,
10,143,607 bytes; also `-99590ff668`, `-eb58a33d55`, cited in `web/whitepaper.md`).

**Licence:** Copyright Scheffer et al.; distributed under the terms of the Creative Commons Attribution License (CC BY),
as stated in the p. 1 sidebar.

## Source files

| file | what it is |
|---|---|
| `source/elife-57443-v4.pdf` | copied from `papers/scheffer2020/elife-57443-v4.pdf`. **Publisher's version of record**, eLife typeset PDF, version 4 (Arbortext, created 16 Oct 2020), 83 pp.: article pp. 1–51, acknowledgements and additional information pp. 51–56, references pp. 56–62, Appendix 1 pp. 63–83 (with Appendix 1—tables 1–6 and Appendix 1—figures 1–3). `SOURCE.txt` fetch note: "elife-57443-v4.pdf: https://cdn.elifesciences.org/articles/57443/elife-57443-v4.pdf (curl, 2026-10-12)". |

`papers/scheffer2020/` also holds `elife-57443-v4.txt` / `.raw.txt` (older text extractions; not used). The paper has no figure
supplements (eLife figure supplements API folder not needed).

## Contents

- `main.tex` / `main.pdf`: the whole PDF in reading order: title, 115 authors with affiliations, the p. 1 sidebar (placed
  after the affiliations), abstract, eLife digest (a box at the top of p. 2, placed after the abstract), Introduction, all
  sections, Figures 1–26, Tables 1–6, Conclusions, Acknowledgements, Additional information (competing interests, funding table,
  author contributions, ORCIDs, decision letter links), Additional files, Data availability, the 132 references (`hangpars`),
  and Appendix 1 with its six tables and three figures. Running headers and footers are left out.
- `figures/`: every figure cropped at 200 dpi from the embedded image (JPEG q90 for renderings/micrographs and JPEG sources,
  PNG for plots): `fig1` … `fig26`, `afig1` … `afig3` (Appendix 1—figures 1–3). Per plotted panel `<panel>.csv`,
  `<panel>_extract.py` (some cover two panels: `fig5_extract.py`, `fig8_extract.py`, `fig20_extract.py`, `fig25_extract.py`),
  `<panel>.py` and `<panel>_replot.png`. Also `fig1_table.csv` (the table printed inside the Fig. 1 image) and `fig23_edges.csv`
  (+ `fig23_edges_extract.py`, the edge values of the Fig. 23 network diagram).
- `tables/`: `table1.csv` … `table6.csv`, `atable1.csv` … `atable6.csv` (Appendix 1—tables 1–6), `funding.csv` (the funding
  table, pp. 52–53). Written by `work/make_tables.py` from the PDF text layer (word positions, row rules), checked against the
  page images; Appendix 1—table 4 (math) transcribed by hand from the page image. The CSV headers give caption, layout notes and
  what is as printed.
- `tools/`: helper modules for the figure scripts written for this paper (`rasterfig.py`, `fc_dig.py`, `fc_pr.py`).
- `decomp.sty`: copied from the osmium tools, so `main.tex` compiles here.
- `work/`: scratch (page renders, text drafts, overlays, side-by-side comparisons `cmp_*.png`, check output, `PROGRESS.md`).
  The working source is `work/main_src.tex`; `main.tex` is generated from it by `work/assemble.py` (inlines the table bodies
  from `work/tables/*.tex` and the figure descriptions from `work/figs/*_alt.tex`). May be deleted.

Compile (from this folder): `lualatex -interaction=nonstopmode -halt-on-error main.tex` (twice). Compiles without errors and
without "Missing character" warnings (92 pages); only overfull-line warnings from long URLs and tables.
Re-run data: `python3 -I -B figures/<name>_extract.py`, then `python3 -I -B figures/<name>.py` (any working directory; all 15
extraction and 18 plotting scripts were re-run from `/tmp` at the end and reproduce their outputs).

## How the text was made

The text layer is good (born-digital, eLife/Arbortext). Each page was drafted from it with `work/draft2.py` (paragraphs,
headings from font sizes, italics/bold, sub/superscripts, line-end hyphens resolved against the rest of the PDF; 34 ambiguous
cases decided by hand, 10 kept as real hyphens), then hand-edited: page 1 layout, digest box, figure and table placement,
captions continued across pages (Figs. 7 and 8), equations (p. 49 Rent's rule; the p. 70 agglomeration criteria and
Appendix 1—table 4, whose math font has no usable text layer), the Cypher query on p. 37 (monospace font whose spaces the text
layer stores as "X"), the ORCID list, and 20 names whose accents the text layer stores as separate glyphs ("Garcı´a-Cerda´n"
→ García-Cerdán, "Bu¨ hler" → Bühler, etc.; all in the reference list).

Symbol fonts (checked on crops, `work/symfont_*.png`): AdvP4C4E74 stores − · × ∗ ≤ ≥ ∧ ∨ ⟨ ⟩ = ( ) as control characters or
Latin letters; AdvP4C4E51 (math italic) stores μ χ and "." "," "/" as other characters; AdvP697C stores μ ∼ ≈ Ω α β γ as
Latin letters; AdvPi1 "." is the list bullet. All were mapped while drafting.

**Glyph audit (`decompile_work/tools/glyph_audit.py --crops work/glyphs`): 130 hidden glyphs**, all checked: 28 × "×" (pp. 8,
9, 37, 47, 67–69), 19 × "−" (pp. 18, 33, 42, 43, 63, 64; 12 in the p. 70 table/paragraph, written as math minus), 2 × "·"
(p. 9 "3 · 10⁷", p. 48 "Ω · m"), 30 × "∗" (p. 49 equation, p. 70 subscripts f\*\*, f_A\*), 14 × "≤" and 34 × "≥" (pp. 6, 41, 42,
44, 48, 70, 79), 2 × "μ" (p. 9), 1 × "χ" (p. 33). Every one is in `main.tex` (as Unicode or as `\leq`, `\geq`, `\wedge`, `\vee`,
`*` in math).

## Text check (`check_text.py` version 2026-10-17j, no options)

`python3 -I -B /home/admin/ephemeral/sep_28__osmium_chemistry/decompiled/tools/check_text.py main.tex source/elife-57443-v4.pdf`

| file | coverage of PDF tokens | without text repeated on ≥ 3 pages | also without in-figure text | tex tokens found in PDF | MISSING ≥ 6 | EXTRA ≥ 6 |
|---|---|---|---|---|---|---|
| `main.tex` | 97.2 % | **99.7 %** (1218 repeated tokens) | 99.7 % | 99.8 % | 1 run (6 tokens) | 2 runs (13 tokens) |

All figures are raster images, so their in-figure text is not in the text layer (described in `\alttext`).
What is not matched (`--min-run 1`, `work/check_min1.txt`): 
- REPEATED: running header "Research article / Computational and Systems Biology | Neuroscience" and the footer
  "Scheffer, Xu, Januszewski, et al. eLife 2020;9:e57443. DOI: … n of 83" (boilerplate, left out; the journal block and DOI
  are given once).
- MISSING: the Table 4 column heads ⟨k⟩ ⟨str⟩ ⟨non-r⟩ ⟨r⟩ (stored as "hki", "hstri" … with ⟨ ⟩ as h/i; written as ⟨…⟩ in the tex,
  so the EXTRA run "k d str non r r" is the same text); "μm" read as "mm" by the checker (μ stored as "m", ≈ 40 single tokens);
  α/β/γ stored as "a"/"b"/"g" (p. 17); math on pp. 48–49 and 70 (Table 6 units "Ω · m", "Ω/m²"; "Pins = a ∗ (computation)^b";
  "ðdA", "maxðminðf…" with ( ) stored as ð Þ); real hyphens at line ends that the checker joins ("left-side", the URL
  "elifesciences-publications"); "Projec tion" on p. 82 (joined, see below).
- EXTRA: the Cypher query on p. 37 ("c weight order by c weight descending": the PDF has "XORDERXBYX…" with X for spaces); the
  Table 4 heads (above); the math tokens of p. 70/71 ("max", "min", "f", "d") written as LaTeX math.

Read-through against the page images (step 4) done for: p. 1–2 (authors, superscripts † ‡ § #, sidebar, digest), every
heading level, all tables (cell values come from the text layer; columns and rows checked against the page images for Tables 2–6 and Appendix 1—tables 1–4; row counts and spot checks for Table 1 and
Appendix 1—tables 5–6), the funding table, the p. 9 and p. 37 voxel sizes (×, μm³, ·10⁷), the p. 33 statistics (χ², 0.79²),
p. 42 (0.19⁶⁰⁰ ≈ 10⁻⁴³²), the p. 47–49 delay model and Rent's rule equation, the p. 70 criteria, the degree signs (˚C as printed),
the code query, figure/caption order around every figure and the continued captions.

## Figures

**All 29 figures are raster images** (embedded images, 109–392 ppi; `get_drawings()` finds only table rules and the page
frame, the vector drawings on pp. 5–6, 24, 41, 45, 48, 65–83 are table rules). No source data is in the local collection,
so every plotted panel is **tier 3 (digitized)** from the embedded image at native resolution, with axis calibration on
ticks/gridlines; every extraction was checked by drawing the result back onto the source image (`work/*overlay*.png`) and
side by side with `tools/compare.py` (`work/cmp_*.png`), and both images were looked at.

**Panels per tier:** tier 1: 0; tier 2: 0; tier 3: 18 (Figs. 5A, 5B, 8A, 8B, 11, 12, 14, 15, 16, 20a, 20b, 21, 25a, 25b, 26,
Appendix 1—figures 1, 2, 3); tier 4: 0. Transcribed from figure images: the Fig. 1 table (`fig1_table.csv`), the Fig. 23
edge values (`fig23_edges.csv`). All other panels (renderings, EM images, schematics) have descriptions only.

**Source data named by the paper and not available locally (tier-1 sources):** Figure 5—source data 1–2, Figure 8—source
data 1, Figure 11—source data 1, Figure 12—source data 1, Figure 15—source data 1, Figure 16—source data 1, Figure 20—source
data 1–6, Figure 21—source data 1, Figure 25—source data 1–4, Figure 26—source data 1, Appendix 1—figures 1–3—source data 1;
Supplementary file 1 (spreadsheet of sparse-to-many connections) and the Transparent reporting form; the data sets themselves
(neuPrint, https://neuprint.janelia.org, doi:10.25378/janelia.11676099.v2; the image volume and segmentation via the
NeuroGlancer links in the text).

| panel | type | data | tier | notes |
|---|---|---|---|---|
| Fig. 1 (top) | 3D surface rendering of the whole brain, hemibrain highlighted | – | – | |
| Fig. 1 (bottom) | table printed inside the figure image (5 rows) | `figures/fig1_table.csv` | transcribed | counts as printed |
| Fig. 2 | EM mosaic (13 slabs, vertical section) with coloured brain regions | – | – | scale bar 50 μm (caption) |
| Fig. 3a | EM micrograph (original, tab 34) | – | – | scale bar 1 μm (caption) |
| Fig. 3b | EM micrograph after CycleGAN | – | – | |
| Fig. 3c | segmentation overlay on (a) | – | – | |
| Fig. 3d | segmentation overlay on (b) | – | – | |
| Fig. 4A | EM micrograph, synapses marked (red arrows, white arrowheads) | – | – | scale bar 0.5 μm (caption) |
| Fig. 4B | synapse point-cloud image, horizontal section | – | – | |
| Fig. 5A | bubble scatter, precision vs recall per brain region (T-bars) | `figures/fig5a.csv` | 3 digitized | dot centres + radii by circle fits; dense cluster uncertain (flags) |
| Fig. 5B | bubble scatter, precision vs recall per brain region (synapses) | `figures/fig5b.csv` | 3 digitized | |
| Fig. 6A | greyscale section with synapse point cloud, glia, fiber bundles, labels | – | – | scale bar 50 μm (caption) |
| Fig. 6B | EM section with segmented neuropils, labels | – | – | scale bar 50 μm |
| Fig. 6C | 3D rendering of neuropils, frontal view | – | – | |
| Fig. 7A | 3D rendering, uniglomerular PNs, dorsal view | – | – | |
| Fig. 7B | 3D rendering, multiglomerular PNs, dorsal view | – | – | |
| Fig. 7C | 3D rendering, LC neurons, anterior view | – | – | |
| Fig. 7D | 3D rendering, LPC/LLPC/LPLC neurons, anterior view | – | – | |
| Fig. 7E | 3D rendering, FB layers, anterior-ventral view | – | – | |
| Fig. 7F | 3D rendering, FB layers, lateral view | – | – | |
| Fig. 7G | EM horizontal section + segmented EB ring-neuron zones | – | – | scale bar 20 μm (caption) |
| Fig. 8A | bubble matrix, boundary areas between 35 regions (size, log scale) | `figures/fig8a.csv` | 3 digitized | semi-quantitative: values from dot size |
| Fig. 8B | bubble matrix, excess crossings per boundary area (size) | `figures/fig8b.csv` | 3 digitized | semi-quantitative |
| Fig. 9 | 3D renderings of PEN1/PEN2 neurons and their PB inputs (two halves) | – | – | |
| Fig. 10 | flow chart (cell-typing workflow, steps 1–4) | – | – | `figures/fig10.png`; text transcribed in `\alttext` |
| Fig. 11 | bar chart, number of cell types per brain region (43 regions) | `figures/fig11.csv` | 3 digitized | y calibrated on ticks (±2 types); labels as printed (Greek lobe letters printed as Latin: gL, b'L, a'L, aL, bL); PRW has no visible bar |
| Fig. 12 | histogram, number of cell types vs number of neurons per type (1–20, >20) | `figures/fig12.csv` | 3 digitized | y calibrated on ticks (±2 types) |
| Fig. 13 | flow chart (CBLAST loop) with an example feature table | – | – | `figures/fig13.png`; the example table (3 neuron ids × type columns) is transcribed in `\alttext` |
| Fig. 14 | scatter (UMAP, 9 cell types, translucent square markers) | `figures/fig14.csv` | 3 digitized | markers overlap within clusters: one row per same-colour blob (centroid, outermost marker centres, area-based marker count as a lower bound); 12 blobs |
| Fig. 15 | grouped histogram, % valid connections, upstream/downstream | `figures/fig15.csv` | 3 digitized | counts read to ±0.4 and rounded; 21 bins of 5 %, two series |
| Fig. 16 | scatter, synapse count at 50 % vs 30 % completeness (~40,000 "+" markers) + two reference lines | `figures/fig16.csv` | 3 digitized | dense band not resolvable: 391 whole markers read individually, upper/lower ink envelope per pixel column, line fits y = x + 4.99 and y = x − 5.01 |
| Fig. 17 | data-flow diagram (data stores, applications, users) | – | – | `figures/fig17.png`; all labels transcribed in `\alttext` |
| Fig. 18 | graph-schema diagram (neo4j node types, relations and properties) | – | – | `figures/fig18.png`; every property list transcribed in `\alttext` |
| Fig. 19 (a)–(c) | greyscale sagittal-section images (EM synapse point-cloud density, confocal, template) | – | – | angles −11.5°, 7.0°, 2.5° printed in the panels |
| Fig. 20a | line plot, 5 threshold series + human designed (dotted), linear x 0–8 | `figures/fig20a.csv` | 3 digitized | per-column trace + vertices at integer x; Figure 20—source data 1–6 not available |
| Fig. 20b | same data, log x 1–~200 | `figures/fig20b.csv` | 3 digitized | dotted line one row per dot; source data not available |
| Fig. 21 | log-log scatter (observed, + markers) + fit line | `figures/fig21.csv` | 3 digitized | 1017 detected crosses (20 isolated, rest in overlapping cloud, flagged `overlap`) + fit line per column; Figure 21—source data 1 not available |
| Fig. 22 (a)–(d) | schematic (motif diagrams) | – | – | |
| Fig. 23 (a)–(c) | network diagram with numbers on arrows | `figures/fig23_edges.csv` (transcription) | – | schematic; arrow values and cell counts transcribed by eye (written by `figures/fig23_edges_extract.py`) |
| Fig. 24 (a), (b) | 3D renderings of neurons and neuropils | – | – | |
| Fig. 25a | scatter, 3 series (GA→GA, GA→EB, GA→PB) | `figures/fig25a.csv` | 3 digitized | groups of overlapping markers: cluster summaries + per-step centre lines/extents (single markers not separable); Figure 25—source data 1–3 not available |
| Fig. 25b | scatter, 9 clusters + 2 annotation arrows | `figures/fig25b.csv` | 3 digitized | one row per cluster (centroid, extent); Figure 25—source data 4 not available |
| Fig. 26 | log-log plot: compartment text labels as points, bound lines, shaded 2D/3D packing bands, annotations | `figures/fig26.csv` | 3 digitized (labels in crowded clusters partly uncertain) | 34 compartment labels located by matching rendered label text (DejaVu Sans 16 px) against the ink; bands and lines fitted as power laws; Figure 26—source data 1 not available |
| App. 1—fig. 1 | line plot, precision vs recall (initial, cascade) + manual estimated point | `figures/afig1.csv` | 3 digitized | per-column trace; Appendix 1—figure 1—source data 1 not available |
| App. 1—fig. 2 | line plot, precision vs recall (initial, cascade, hybrid, synful+) + manual estimated point | `figures/afig2.csv` | 3 digitized | per-column trace; cascade is hidden under hybrid/initial below recall ≈ 0.52 (missing columns); Appendix 1—figure 2—source data 1 not available |
| App. 1—fig. 3 | scatter/density plot with log colour bar (neuron pair frequency) | `figures/afig3.csv.gz` | 3 digitized (semi-quantitative colour map) | 25,611 coloured pixels mapped through the colour bar; markers (~3 px) exceed one count per pixel, so not a per-count histogram; Appendix 1—figure 3—source data 1 not available |

### Figure notes (cross-checks, methods, oddities; from the figure work)

**fig1.** Cross-checks: the table's 9.5M T-bars and 64M PSDs are the numbers in the Fig. 4 caption ("64 million PSDs and 9.5 million
T-bars ... (Figure 1)"; 64/9.5 = 6.7 PSDs per T-bar, as stated). 21,734 + 4,456 = 26,190 traced neurons with large arbors, vs.
the caption's "≈ 25K neurons".

**fig3.** Paper oddity: caption "at a resolution of 16 nm / resolution" (kept verbatim).

**fig4.** Oddity: the caption names synaptic vesicles 'SV'; the label in the image reads "SVs".

**fig5.** Data: the embedded image is a 1187 × 562 px JPEG (~167 ppi). Axes calibrated on the frame and the gridlines 0.6–1.0
(residual ≤ 0.0004). The gridlines are drawn over the dots and are bridged in the colour mask; each dot's visible piece gets
a RANSAC circle fit (a candidate may not cover open background); components holding several dots are fitted iteratively;
one large dot hidden under the panel-A cluster is refitted near a hand-placed guide circle (flag `partly_hidden_guided`).
Overlay `work/fig5_overlay.png`, side by side `work/cmp_fig5a.png`, `work/cmp_fig5b.png` (both looked at).
Source data not available: Figure 5—source data 1 and 2 (eLife online).

Cross-check: the purple human-proofreader reference dots come out at (0.9003, 0.8997) and (0.7998, 0.8004), the caption's
0.9/0.9 and 0.8/0.8.

Open problem: panel A's dense cluster (recall 0.91–0.99, precision 0.88–0.96) cannot be fully separated; the dot counts
(45 in A, 43 in B) differ although both panels show the same regions, so A probably holds 1–2 double fits or B hides a dot.
The tier-1 source data would settle it.

**fig6.** Oddity: the caption calls (A) "a vertical section"; the panels are labelled "coronal section".

**fig7.** Note: the caption names the LLPC cells for (D), but no LLPC label is printed in panel D (labels: LPLC1, LPLC2, LPLC4, LPC1).

**fig8.** Data: lossless 1132 × 2450 px image (~303 ppi). Dot radii measured at every gridline crossing (median edge distance over 72
rays after a centre refit; dots < 2.5 px from their weighted area). Mirror cells (the matrices are symmetric) agree to
0.03 px (A) and 0.05 px (B) rms. Size scale: the legend symbols are drawn 1.20× smaller than the data dots, so each panel is
calibrated on its largest dot (= the legend Max) with the legend's shape: (A) radius linear in log10(value) — the legend's
three symbols fit this to 0.02 px; (B) radius proportional to value (the Min 0.0 symbol is invisible). Checks: A smallest dot
→ 1.01 (legend Min 1), median → 825 (legend Med 883); B median over the 254 boundary cells (38 without a B dot = 0) → 0.80
(legend Med 0.8). The B Med legend symbol is 12 % larger than this scale implies (a straight line through the two B legend
symbols would put the median at 0.69). Overlay `work/fig8_overlay.png`, side by side `work/cmp_fig8a.png`, `cmp_fig8b.png`
(looked at). Source data not available: Figure 8—source data 1.

Cross-check with the text (p. 20): the five largest B values are CRE/SMP (2.6), AB(L)/FB (2.43), CRE/LAL (2.08), SIP/SLP
(1.97) and SIP/SMP (1.94) — exactly the boundaries the text names as worst (SMP/CRE, CRE/LAL, SMP/SIP, SIP/SLP) plus FB/AB,
which the text says "also has a high excess crossing score".

Open problem: the size-scale model (and the 1.20 legend/data factor) is inferred, not stated; values are semi-quantitative.

**fig11.** - Fig. 11 cross-check: the 43 bars add up to ≈ 17,250 types, larger than the 5609 connectivity types of Table 3, as the caption says
  (types arborizing in several regions are counted in each).
- Fig. 11 tier 1 not available: "Figure 11—source data 1" (eLife online).

**fig12.** - Fig. 12 cross-checks: bin "1" = ≈ 2048 types, consistent with "Over 2000 of these are types with only a single instance" (p. 29).
  The bars add up to ≈ 5670 types, 1.1 % more than the 5609 connectivity types of Table 3 (and 8 % more than the 5229 morphology
  types); the difference (≈ 60) is larger than the digitizing error (≈ ±10 summed), so the figure may come from a slightly different
  data version or count. Not flagged as an error.
- Fig. 12 tier 1 not available: "Figure 12—source data 1" (eLife online).

**fig14.** - Fig. 14: no source data are named. Individual cells cannot be separated (markers ~0.38 AU wide, stacked); the blob
  marker counts (area ÷ one-marker area) are lower bounds.

**fig15.** - Fig. 15 cross-checks: each series adds up to exactly **1735**, the number of traced neurons examined in the text (p. 33: "1735
  traced neurons spanning 1518 unique cell types"; source-data title "Data on 1735 neurons, one per row"). So the histogram counts
  neurons, although the y axis says "Cell Type Count" and the caption says "for ≈ 1000 cell types" (neither 1000 nor 1518) –
  listed under oddities below.
- Bins at ≥ 70 % hold 89.7 % (upstream) and 90.5 % (downstream) of the counts, matching "90% of cell types have an accuracy of at
  least 70%" (depending on where the bin edges lie). The median falls in the bin centred on 85 % for both series (cumulative
  44 % below it, 59 % through it); the text gives a median of 88 %. If the bins are 82.5–87.5 % the histogram median would be
  ≈ 84–85 %, below the printed 88 %; if the bar at "85" stands for 85–90 % the two agree. The bin edges are not printed, so this
  is left open. The single upstream count at 10 % is consistent with "the worst outlier, having an upstream connection accuracy of 12%".
- Fig. 15 tier 1 not available: "Figure 15—source data 1" (data on 1735 neurons, eLife online).

**fig16.** - Fig. 16 cross-checks: the two reference lines come out as y = x + 4.99 (orange, "Additional synapses: Five synapses") and
  y = x − 5.01 (grey, "Fewer synapses: Five synapses"). No marker lies clearly below the grey line; two sit on it at (20.75, 15.59)
  and (22.06, 17.01), i.e. decreases of ≈ 5.1–5.2, within reading accuracy of the caption's "no path decreased by more than five
  synapses". Exactly two markers lie at x ≈ 0 with y > 10, at (0.1, 19.8) and (−0.3, 11.5), matching "Only two new strong
  (count >10) paths were found that were not present in the original".
- The isolated marker centres do not fall on integer synapse counts (fractional parts spread evenly in both x and y), so the
  plotted values were probably jittered or are not raw integer counts; the CSV gives them as read.
- Fig. 16 tier 1 not available: "Figure 16—source data 1" (eLife online).

**fig20.** Calibration: (a) y on gridlines 0.1–0.9 (max residual 0.0005), x on gridlines 1–8 (max residual 0.014); (b) x on 19 major/minor tick marks 1…100 (log fit, max residual 0.0012 decades). Checked with overlays (`work/fig20a_overlay.png`, `work/fig20b_overlay.png`) and side-by-side (`work/cmp_fig20a.png`, `work/cmp_fig20b.png`).

Cross-checks with the text (p. 41): "Three quarters of all possible pairs are connected by a path with fewer than three interneurons, even when only connections with ≥5 synapses are included": the Threshold 5 curve reads 0.34 at x = 2 and 0.75 at x = 3, i.e. three quarters is reached at three interneurons, not with fewer than three (possible off-by-one between the text and the axis definition; kept verbatim, not flagged in main.tex). "A typical node pair is separated by 60 intervening nodes" (human designed benchmark): the dotted curve reaches 0.5 at about 59 and half of its final 0.79 at about 52, consistent.

Oddity: Fig. 20a prints no tick label "3" on its x axis (gridline present).

**fig21.** Calibration: white decade gridlines (x 1/10/100/1000, max residual 0.0024 decades; y 1e6…1, 0.0021 decades). Checked with `work/fig21_overlay.png` (+ zoom) and `work/cmp_fig21.png`.

Cross-check with the caption ("power law (exponent −1.67) with exponential cutoff (at N = 42)"): a free fit of log N = c + k log s − s/s0 to the digitized orange line gives k = −1.673 and s0 = 41.7, i.e. the printed parameters. The low-count rows come out at 1.00, 2.01, 3.0, 4.0, 5.0, 6.0 (integers, as counts must be), which confirms the y calibration.

Limits: above strength ~20 neighbouring integer strengths are closer than a marker width (13 px), so crosses overlap; hidden markers are not recovered and some crosses are detected twice a few pixels apart.

**fig23.** Cross-check: caption (a) "PLP008, has bidirectional connections to all 82 cells of type LC13": the bottom circle prints 82.

**fig25.** Calibration on white gridlines (a: x residual 0.0015 ms, y 0.0006 mV; b: x 0.0044 ms, y exact on 3 lines). Checked with `work/fig25a_overlay.png`, `work/fig25b_overlay.png`, `work/cmp_fig25a.png`, `work/cmp_fig25b.png`.

Cross-check: the (b) cluster at (3.59 ms, 0.108 mV) coincides with the GA→PB band of (a) (centroid 3.60 ms, 0.107 mV), as expected if (a) uses the nominal (middle) R_a and R_m values of the 3 × 3 grid in (b). The caption does not say which cluster is which R_a/R_m pair, so the CSV does not label them.

**fig26.** Calibration: decade tick marks on the frame (residuals < 0.003 decades). Checked with `work/fig26_overlay.png` (label boxes, band-edge and line traces drawn on the source) and `work/cmp_fig26.png`.

Method notes: the plot has no markers, each compartment is only its printed label; the label centre is taken as the data point (assumes the labels are centred on their points, which cannot be checked from the figure). Candidates were all Table 1 region names with "(R)", "(L)" or no suffix; 8 false matches made of letters of overlapping labels were dropped and 4 matches whose "(R)" is hidden were renamed (listed in `figures/fig26_extract.py`); two clearly printed labels (EB, AOTU(R)) needed a looser mask. Two labels are marked `uncertain` (ATL(L) and IB, partly hidden); one more label in each crowded cluster may be missing.

Cross-checks with the text (pp. 49–50): fitted green upper bound N = 0.998·T^1.000 and blue lower bound N = 3.99·T^0 match "theoretical range of 0.0 to 1.0" for the Rent exponent and "a is a scale factor (typically in the range 1–4)". The packing bands come out with exponents 0.553–0.708 (2D, olive + overlap) and 0.662–0.787 (3D, light grey + overlap), prefactor ≈ 1, consistent with "roughly 0.5–0.7". EB lies just below the bands, as the text says ("the ellipsoid body (EB) falls just outside the expected area").

Inconsistency in the paper: the caption names the microprocessor "ST7LU55"; the figure label reads "ST7LUS5".

**afig1.** Calibration on the grey gridlines (max residual 0.0006 recall, 0.0001 precision); checked with `work/afig1_overlay.png` and `work/cmp_afig1.png`. Cross-check: the purple point comes out at (0.900, 0.900), the "estimated manual agreement rate of 0.9" of the caption.

**afig2.** Calibration on the grey gridlines (max residual 0.0008 recall, 0.0004 precision); checked with `work/afig2_overlay.png` and `work/cmp_afig2.png`. Cross-check: the purple point comes out at (0.800, 0.800), the "estimated manual agreement rate of 0.8" of the caption; the hybrid curve lies above cascade and synful+ at high recall, consistent with the text ("a 'hybrid' classifier that achieved both better recall and precision than the two individual classifiers").

**afig3.** Calibration: axes on gridlines and frame (residual 0.4 counts), colour bar on its six log ticks (0.005 decades). Checked with `work/cmp_afig3.png` and `work/afig3_overlay.png` (pixels mapped above 10² frequency drawn in green: all within ~40 counts of the origin).

## Errors and oddities in the paper (kept verbatim)

- Table 1: FBl3 is named "Fan-shaped body layer 4" (FBl4 has the same name); "Medula" (medulla); "Rubu"; "prow" in lower case;
  "SMP(R)(L)" without the slash; the mushroom-body lobes are printed with Latin letters (a′L, aL, gL, b′L, bL, a1 …) where the
  text uses α, β, γ (p. 17). The same Latin letters appear in Table 2 and Table 4.
- Table 6: the unit of R_m is printed as Ω/m² (membrane resistance is usually Ω·m²).
- Appendix 1—table 4: the score of group 10 is printed "11 − J_AB" (groups 1–9 score n − J_AB; 11 and 12 score 12 − … and 13 − …).
- Appendix 1—figures 1–3: "The online version of this article includes the following source data is available for figure N:"
  (garbled sentence, as printed).
- Appendix 1—table 6, p. 82: "Projec" / "tion" is broken over a line without a hyphen; joined to "Projection" in the CSV and
  the tex.
- Fig. 15: y axis "Cell Type Count" and caption "≈ 1000 cell types", but the counts sum to 1735, the number of neurons examined
  (p. 33). Fig. 12 bars sum to ≈ 5670 types against 5609 in Table 3.
- Fig. 26: the caption names "ST7LU55"; the label in the figure reads "ST7LUS5".
- p. 41: "Three quarters of all possible pairs are connected by a path with fewer than three interneurons" (≥ 5 synapses);
  Fig. 20a reads 0.34 at two and 0.75 at three interneurons (possible off-by-one).
- Fig. 3 caption "at a resolution of 16 nm / resolution"; Fig. 4 image label "SVs" vs caption 'SV'; Fig. 6 caption "vertical
  section" vs panel labels "coronal section"; Fig. 7 caption names LLPC cells for (D), but no LLPC label is printed in (D).

## Collection cross-references

Cited works that are in the collection (`decompile_work/manifest.json`): hayworth2015 (Hayworth et al., 2015, Nature Methods),
xu2017 (Xu et al., 2017, eLife), zheng2018 (Zheng et al., 2018, Cell).

## Known limitations

- Fig. 5A dense cluster, Fig. 14 clusters, Fig. 16 point cloud, Fig. 21 crosses above strength ≈ 20, Fig. 25 point clouds:
  overlapping markers cannot all be separated; the CSVs flag partly hidden points or give cluster summaries/envelopes (see the
  figure notes). Fig. 8 bubble values depend on an inferred size scale (semi-quantitative). Fig. 26 points are text-label
  positions; ATL(L) and IB uncertain. Appendix 1—figure 3 is a colour map read through its log colour bar (semi-quantitative).
- Table 1 and Appendix 1—tables 5–6 were checked by row counts and spot checks against the page images, not cell by cell.

## Time

About 3.5 h wall clock (03:48–07:00 and 07:30–07:45 UTC, with a usage-limit stop in between), main agent plus three figure agents
working in parallel (Figs. 1–9, 10–18, 19–26 + appendix figures).
