#!/bin/bash
# Build the thesis PDF: preprocess MD -> pandoc -> tectonic.
set -e
R=/mnt/c/Users/Maidanng/Repos/myVault/10_Projects/14_Thesis_SDPO/report
cd "$R/latex"
PY=~/tfig/bin/python
PANDOC=~/bin/pandoc
TECT=~/bin/tectonic
PFLAGS="--top-level-division=chapter --no-highlight --wrap=preserve"

echo "[1] chapters ..."
declare -A MAP=( [_ch1]=ch1_introduction [_ch2]=ch2_related_work [_ch3]=ch3_method \
                 [_ch4]=ch4_experiments [_ch5]=ch5_discussion [_ch6]=ch6_limitations_future \
                 [_ch7]=ch7_conclusion )
for out in "${!MAP[@]}"; do
  src="${MAP[$out]}"
  $PY preprocess.py "$R/$src.md" | $PANDOC $PFLAGS -f markdown -t latex -o "$out.tex"
done

echo "[2] appendix ..."
$PY preprocess.py "$R/08_appendices.md" | $PANDOC $PFLAGS -f markdown -t latex -o _appendix.tex

echo "[3] abstract ..."
grep -v '^# Abstract' "$R/00_abstract.md" | $PANDOC --no-highlight -f markdown -t latex -o _abstract.tex

echo "[4] references ..."
grep -E '^\[[0-9]+\]' "$R/00_references.md" | $PANDOC --no-highlight -f markdown -t latex -o _refs.tex

echo "[5] compile ..."
$TECT -X compile main.tex 2>&1 | tail -20
ls -la main.pdf 2>/dev/null && echo "=== PDF OK ($(wc -c < main.pdf) bytes) ==="
