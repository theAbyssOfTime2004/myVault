#!/bin/bash
# Build the finalized thesis PDF using customized LaTeX files directly.
set -e
R=/mnt/c/Users/Maidanng/Repos/myVault/10_Projects/14_Thesis_SDPO/report
cd "$R/latex"
TECT=~/bin/tectonic

echo "[1] Skipping Markdown pre-processing to preserve customized .tex files..."
# Các bước gen cũ đã được loại bỏ để tránh ghi đè lên các file .tex bạn đã chỉnh sửa

echo "[2] Skipping appendix / abstract / refs generation..."
# Giữ nguyên b_abstract.tex, b_refs.tex, và b_appendix.tex bạn đã tối ưu hóa

echo "[3] compile ..."
$TECT -X compile main_bestcase.tex 2>&1 | tail -6

if ls -la main_bestcase.pdf 2>/dev/null; then
    echo "=== PDF OK ($(wc -c < main_bestcase.pdf) bytes) ==="
else
    echo "=== ERROR: Compilation failed ==="
fi