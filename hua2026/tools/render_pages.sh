#!/bin/sh
# render_pages.sh <pdf> <outdir> [dpi]   -> <outdir>/<stem>-<page>.png, one per page
set -eu
pdf=$1; out=$2; dpi=${3:-150}
mkdir -p "$out"
stem=$(basename "$pdf" .pdf)
pdftoppm -r "$dpi" -png "$pdf" "$out/$stem"
