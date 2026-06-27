# Placeholder / mock data registry

This draft is for **format and framing review** (advisor-approved) while Modal/Colab
compute is unavailable. The items below are **synthetic placeholders**, not real
results. They MUST be replaced with real runs before any committee submission.
Real runs scheduled after the compute-quota reset (planned August 2026).

Every placeholder number in the report text/figures is marked with a dagger **†**.

| # | Location | What is mock | Replace with |
|---|---|---|---|
| 1 | §4.2.5 table (SF $g{=}10$ column, all †) | Compute-matched student-first at `num_generations=10` POST pass@16 means | Real SF runs at `num_generations=10` on idx39/12/64/77, 4 seeds each (script `07`, `--num_generations 10`) |
| 2 | Figure 4.8 (`figures/fig_4_8_compute_matched.py`) | The SF $g{=}10$ bars | Same real runs as #1 |
| 3 | §5.1 sentence interpreting the compute-matched result | Conclusion drawn from #1 | Re-confirm against real #1 |
| 4 | §6.1.5 / §6.2.4 wording ("compute-matched … placeholder") | Status statement | Flip to "completed" once #1 is in |
| 5 | Abstract clause on compute-matched | Status statement | Flip once #1 is in |

## How to replace
1. Run `07_discovery_curve.py --problem_index {12,39,64,77} --num_generations 10 --seed {0..3}` (W&B project `ttt-sdpo-thesis`).
2. Pull per-seed POST pass via `data/reconcile.py` (add the `g=10` filter).
3. Replace the † numbers in §4.2.5 + `fig_4_8` data, drop the daggers, remove the §4.2.5 banner, remove the title-page draft note, delete this registry's mock rows.
