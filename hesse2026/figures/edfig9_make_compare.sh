#!/bin/bash
# Build the QA side-by-side images: original 300-dpi crop (left) | regenerated PNG (right).
# Usage: EDFIG9_ORIG_DIR=<dir with *_orig.png from edfig9_extract.py> bash make_compare.sh
cd "$(dirname "$0")"
O=${EDFIG9_ORIG_DIR:-.}
for p in a c d e f g h_decoding_vs_cells h_modulation_index; do
  w=600; [ "$p" = a ] && w=1000; [ "$p" = h_modulation_index ] && w=800
  convert "$O/edfig9${p}_orig.png" -resize ${w}x "edfig9${p}_replot.png" -resize ${w}x -bordercolor white -border 10 +append "edfig9${p}_compare.png"
done
