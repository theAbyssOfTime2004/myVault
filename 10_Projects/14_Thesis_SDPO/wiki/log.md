# Thesis SDPO — Log

Chronological record of ingests, queries, and lint passes. Append-only.

Tip: `grep "^## \[" log.md | tail -5` shows the five most recent entries.

---

## [2026-04-22] bootstrap | wiki scaffolding created

- Created: `CLAUDE.md`, `wiki/index.md`, `wiki/log.md`, empty dirs for `raw/`, `wiki/sources/`, `wiki/entities/`, `wiki/concepts/`, `wiki/synthesis/`
- Existing `SDPO 2026-04-11.md` left in place; referenced from index as the thesis proposal. Migration to `wiki/synthesis/syn_thesis_proposal.md` pending user decision.
- Key takeaway: architecture ready. Next step is ingesting the two core sources (Hübotter et al., Kim et al. 2026).

## [2026-04-22] ingest | Hübotter et al. 2026 — Reinforcement Learning via Self-Distillation

- Source: `raw/hubotter2026_sdpo.md` (abstract + metadata clip from arXiv; full PDF pending)
- Created: [[src_hubotter2026_self_distillation]], [[ent_sdpo]], [[ent_rlvr]], [[ent_livecodebench]], [[con_rich_feedback]], [[con_self_teacher]], [[con_credit_assignment]]
- Updated: `wiki/index.md` (3 entities, 3 concepts, 1 source added; planned list shrunk)
- Depth: **abstract-only**. Full paper methods/results sections not yet ingested — download PDF to `raw/` and re-ingest to deepen pages (especially [[src_hubotter2026_self_distillation]] method section and [[ent_sdpo]] distillation objective).
- Key takeaway: SDPO's core move is treating the model-conditioned-on-feedback as a [[con_self_teacher]] to densify the sparse scalar reward of [[ent_rlvr]]. This frames the thesis's test-time variant clearly — same mechanism, frozen weights, template ablation.
