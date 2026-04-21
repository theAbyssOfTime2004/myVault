---
type: entity
created: 2026-04-22
updated: 2026-04-22
tags: [benchmark, code, evaluation]
sources: [src_hubotter2026_self_distillation]
aliases: [LiveCodeBench, LCB]
---

# LiveCodeBench

Competitive programming benchmark for evaluating LLM code reasoning. Released to mitigate contamination by using problems scraped after known training cutoffs. Thesis targets **v6**, hard and very-hard splits.

## Why the thesis uses it

- Hard / very-hard splits are sensitive to reasoning quality — suited to test-time SDPO ablations.
- Versioned → contamination control.
- Measures both correctness and compute (→ input to [[con_ctc_metric]]).

## Where it appears

- [[src_hubotter2026_self_distillation]] — one of the evaluation benchmarks for SDPO vs RLVR.

## Gaps

- LCB origin paper not yet ingested. Clip it into [[raw/]] and re-ingest to populate: contamination protocol, problem sourcing, scoring.
