# -*- coding: utf-8 -*-
import re, io
base = "/mnt/c/Users/Maidanng/Repos/myVault/10_Projects/14_Thesis_SDPO/report/latex/"
new = io.open(base + "refs_manual.tex", encoding="utf-8").read()
b = "\\begin{thebibliography}"
e = "\\end{thebibliography}"
block = new[new.index(b): new.index(e) + len(e)]
ov = io.open(base + "main_bestcase_overleaf.tex", encoding="utf-8").read()
pat = re.compile(r"\\begin\{thebibliography\}.*?\\end\{thebibliography\}", re.S)
n = len(pat.findall(ov))
ov2 = pat.sub(lambda m: block, ov, count=1)
io.open(base + "main_bestcase_overleaf.tex", "w", encoding="utf-8", newline="\n").write(ov2)
# sanity: no 'et al.' left in bibliography block of overleaf
bibpart = ov2[ov2.index(b): ov2.index(e)]
print("bib blocks:", n, "| 'et al.' in bib:", bibpart.count("et al."), "| arXiv urls in bib:", bibpart.count("arxiv.org/abs"))
