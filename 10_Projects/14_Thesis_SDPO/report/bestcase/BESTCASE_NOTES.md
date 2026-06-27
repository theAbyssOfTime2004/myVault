# Best-case projection — registry

This is the **best-case / projected** variant of the thesis, built to demonstrate
(for the advisor, and the post-graduation publication trajectory) how the work
improves once the limitations are resolved with more compute and time.

**Nothing here is a new real result.** Every result that is not in the current
real draft is a **projection**: an extrapolation of the existing real numbers
under the stated hypotheses. Projected results are marked **‡**. The current
real draft (`report/latex/main.pdf`) remains the factual baseline.

## What changes vs the current real draft

| Resolved limitation | Best-case change | Projected (‡) |
|---|---|---|
| §6.1.1 small n | medium n (≈16 problems × 6 seeds); Wilcoxon signed-rank instead of crude sign test | TF significantly ≥ SF ‡ |
| §6.1.5 compute | full compute-matched + compute-to-correct (CTC) Pareto | TF wins at matched compute ‡ |
| §6.1.6 RQ2 thin | code run with thinking ON → epistemic suppression measured at test time | suppression observed ‡ |
| §6.1.4 fallback | keep-best-correct fallback removed (never distil a copy) | cleaner leak filter |
| §6.1.2 / value-vs-procedure | MATH-500 method-reference + same reasoner (Qwen3-4B) on both domains | math escapes with method-reference ‡ |
| framing | RQ2 + RQ3 promoted from secondary to answered; claims upgraded from "directional" to "we find" | — |

## Honesty boundary

The best-case assumes the projections land in the **hypothesized direction**.
Each could go the other way (medium-n may shrink the effect; compute-matched may
erase it; epistemic suppression may not appear). The real runs decide. This draft
shows the *upside* trajectory, not a guaranteed outcome — see §5 "If the
projections do not hold".

Build: `report/latex/build_bestcase.sh` → `bestcase.pdf`. Reuses the real Ch2,
Ch3, references, and appendices; overrides abstract, Ch1, Ch4, Ch5, Ch6, Ch7.
