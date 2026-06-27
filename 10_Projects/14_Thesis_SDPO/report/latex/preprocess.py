#!/usr/bin/env python3
"""Preprocess each chapter Markdown into a pandoc-friendly form:
   - replace ```mermaid blocks with raw-LaTeX TikZ (explicit coords, robust)
   - replace ![..](figures/x.png) with raw-LaTeX \includegraphics (../figures/x.pdf)
Then the caller runs: pandoc --top-level-division=chapter --no-highlight.
"""
import re
import sys
import pathlib

TIKZ = {
    "fig_2_1": r"""\begin{center}\begin{tikzpicture}[font=\footnotesize,>=Latex,every node/.style={draw,rounded corners,align=center,minimum height=0.7cm,text width=3.3cm,inner sep=2pt}]
\node(gr) at (0,3){scalar reward $r$};
\node(ga) at (0,2){one advantage / sequence};
\node(gt) at (0,1){same signal every token ($O(1)$)};
\node(sf) at (4.4,3){feedback $f$};
\node(st) at (4.4,2){teacher per-token dist.};
\node(stk) at (4.4,1){soft top-$K$ target / position ($O(T\cdot K)$)};
\draw[->](gr)--(ga);\draw[->](ga)--(gt);\draw[->](sf)--(st);\draw[->](st)--(stk);
\node[draw=none,font=\bfseries] at (0,3.8){GRPO (sparse)};
\node[draw=none,font=\bfseries] at (4.4,3.8){SDPO (dense)};
\end{tikzpicture}\end{center}""",
    "fig_3_1": r"""\begin{center}\begin{tikzpicture}[font=\footnotesize,>=Latex,every node/.style={draw,rounded corners,align=center,minimum height=0.6cm,text width=3.6cm,inner sep=2pt}]
\node(x) at (3,5){Problem $x$};
\node(s) at (0,4){Student $\pi_\theta(\cdot\,|\,x)$};
\node(t) at (6,4){Self-teacher $\pi_\theta(\cdot\,|\,x,c)$};
\node(ys) at (0,2.8){$y_{\text{student}}$ (usually wrong)};
\node(yt) at (6,2.8){$\{y_{t_i}\}\to$ verifier + judge};
\node(g) at (6,1.7){good pool $y_{\text{good}}$};
\node(kls) at (0,1.5){KL distil on $y_{\text{student}}$};
\node(klt) at (6,0.5){KL distil on $y_{\text{good}}$};
\node(u) at (3,-0.6){update $\theta$};
\draw[->](x)--(s);\draw[->](x)--(t);\draw[->](s)--(ys);\draw[->](t)--(yt);\draw[->](yt)--(g);\draw[->](ys)--(kls);\draw[->](g)--(klt);\draw[->](kls)--(u);\draw[->](klt)--(u);
\end{tikzpicture}\end{center}""",
    "fig_3_2": r"""\begin{center}\begin{tikzpicture}[font=\footnotesize,>=Latex,every node/.style={draw,rounded corners,align=center,minimum height=0.6cm,text width=3.4cm,inner sep=2pt}]
\node(c) at (0,4){privileged context $c$: feedback + few-shot};
\node(t) at (0,3){self-teacher samples $N$};
\node(v) at (0,2){verifier: correctness};
\node(j) at (0,1){judge: is\_copy / independence};
\node(gp) at (4.6,1){good pool (correct \& independent)};
\node(fs) at (4.6,2.6){few-shot good\_only / good\_bad};
\node(kl) at (4.6,-0.2){KL distil student $\to y_{\text{good}}$};
\draw[->](c)--(t);\draw[->](t)--(v);\draw[->](v)--(j);\draw[->](j)--(gp);\draw[->](gp)--(fs);\draw[->](fs.north)|-(t.east);\draw[->](gp)--(kl);
\end{tikzpicture}\end{center}""",
    "fig_3_3": r"""\begin{center}\begin{tikzpicture}[font=\footnotesize,>=Latex,every node/.style={draw,rounded corners,align=center,minimum height=0.55cm,inner sep=3pt}]
\node(a) at (0,3){T2 standard (anchor)};
\node(d1) at (-4,1.8){Dim 1: information};
\node(d2) at (0,1.8){Dim 2: framing};
\node(d3) at (4,1.8){Dim 3: memory};
\node(t1) at (-5,0.6){T1};\node(t3) at (-3,0.6){T3};
\node(t4) at (-1.4,0.6){T4};\node(t5) at (0,0.6){T5};\node(t6) at (1.4,0.6){T6};
\node(t7) at (4,0.6){T7};
\draw[->](a)--(d1);\draw[->](a)--(d2);\draw[->](a)--(d3);
\draw[->](d1)--(t1);\draw[->](d1)--(t3);\draw[->](d2)--(t4);\draw[->](d2)--(t5);\draw[->](d2)--(t6);\draw[->](d3)--(t7);
\end{tikzpicture}\end{center}""",
    "fig_5_1": r"""\begin{center}\begin{tikzpicture}[font=\footnotesize,>=Latex,every node/.style={draw,rounded corners,align=center,minimum height=0.6cm,text width=4.3cm,inner sep=3pt}]
\node(r) at (0,3){Reference in privileged context};
\node(code) at (-3.4,1.7){Code: output = program = \textbf{method}};
\node(math) at (3.4,1.7){Math (answer-only): output = \textbf{value}};
\node(ce) at (-3.4,-0.1){generalizes; distil installs procedure $\Rightarrow$ \textbf{escape}};
\node(me) at (3.4,-0.1){doesn't generalize; teacher copies; form $\neq$ substance $\Rightarrow$ \textbf{no escape}};
\draw[->](r)--(code);\draw[->](r)--(math);\draw[->](code)--(ce);\draw[->](math)--(me);
\end{tikzpicture}\end{center}""",
}

# which mermaid blocks (in order) appear in each file
ORDER = {
    "ch2_related_work": ["fig_2_1"],
    "ch3_method": ["fig_3_1", "fig_3_2", "fig_3_3"],
    "ch5_discussion": ["fig_5_1"],
}


def raw(latex):
    return "\n\n```{=latex}\n" + latex + "\n```\n\n"


def process(path):
    stem = pathlib.Path(path).stem
    text = pathlib.Path(path).read_text(encoding="utf-8")

    # mermaid -> tikz (ordered)
    keys = ORDER.get(stem, [])
    idx = [0]

    def merm(m):
        k = keys[idx[0]]
        idx[0] += 1
        return raw(TIKZ[k])
    text = re.sub(r"```mermaid.*?```", merm, text, flags=re.DOTALL)

    # images -> includegraphics (png -> pdf, prefix ../)
    def img(m):
        p = m.group(1)  # figures/xxx.png
        p = p.replace(".png", ".pdf")
        return raw(r"\begin{center}\includegraphics[width=0.85\linewidth]{../" + p + r"}\end{center}")
    text = re.sub(r"!\[[^\]]*\]\((figures/[^)]+)\)", img, text)

    sys.stdout.write(text)


if __name__ == "__main__":
    process(sys.argv[1])
