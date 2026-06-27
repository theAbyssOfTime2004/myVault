#!/bin/bash
# Build the BEST-CASE / projected thesis PDF.
set -e
R=/mnt/c/Users/Maidanng/Repos/myVault/10_Projects/14_Thesis_SDPO/report
cd "$R/latex"
PY=~/tfig/bin/python
PANDOC=~/bin/pandoc
TECT=~/bin/tectonic
PFLAGS="--top-level-division=chapter --listings --wrap=preserve"

echo "[1] chapters ..."
# out=src  (bestcase overrides for 1,4,5,6,7; real reuse for 2,3)
gen () { $PY preprocess.py "$1" | $PANDOC $PFLAGS -f markdown -t latex -o "$2"; }
gen "$R/bestcase/bc_ch1.md" b_ch1.tex
gen "$R/ch2_related_work.md" b_ch2.tex
gen "$R/ch3_method.md" b_ch3.tex
gen "$R/bestcase/bc_ch4.md" b_ch4.tex
gen "$R/bestcase/bc_ch5.md" b_ch5.tex
gen "$R/bestcase/bc_ch6.md" b_ch6.tex
gen "$R/bestcase/bc_ch7.md" b_ch7.tex

echo "[2] appendix + abstract + refs ..."
$PY preprocess.py "$R/08_appendices.md" | $PANDOC $PFLAGS -f markdown -t latex -o b_appendix.tex
grep -v '^# Abstract' "$R/bestcase/bc_abstract.md" | $PANDOC --no-highlight -f markdown -t latex -o b_abstract.tex
grep -E '^\[[0-9]+\]' "$R/00_references.md" | $PANDOC --no-highlight -f markdown -t latex -o b_refs.tex

echo "[3] compile ..."
$TECT -X compile main_bestcase.tex 2>&1 | tail -6
ls -la main_bestcase.pdf 2>/dev/null && echo "=== BESTCASE PDF OK ($(wc -c < main_bestcase.pdf) bytes) ==="
