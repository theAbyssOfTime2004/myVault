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

## [2026-04-22] ingest | Hübotter et al. 2026 — **deep re-ingest (full PDF 50 pages)**

- Source: `raw/hubotter2026_sdpo.md` upgraded — full PDF extracted từ `\\wsl.localhost\Ubuntu\home\theabyssoftime\Repos\SDPO_thesis\sdpo.pdf` (§1–§7 + appendices A–F).
- Depth upgrade: **abstract-only → full-paper**. Giờ wiki cover được formal loss, 3 evaluation regimes (§3 RLVR / §4 RLRF / §5 test-time), toàn bộ ablations (feedback content, credit granularity, template, scale), và future work.
- Pages deepened: [[src_hubotter2026_self_distillation]], [[ent_sdpo]], [[ent_rlvr]], [[ent_livecodebench]], [[con_rich_feedback]], [[con_self_teacher]], [[con_credit_assignment]]
- Pages created: [[ent_grpo]], [[ent_rlrf]], [[ent_qwen3_8b]], [[ent_olmo3_7b_instruct]], [[con_reprompt_template]], [[con_test_time_self_distillation]], [[con_discovery_at_k]]
- Updated: `wiki/index.md` (entities 3→6, concepts 3→6, planned list shrunk).
- Key numbers captured: SDPO 48.8% vs GRPO 41.2% LCBv6 (§4); Chemistry 6× sample-efficiency (Olmo3-7B); test-time TTT-SDPO 3× fewer attempts on very-hard, 2.4× on hard (§5.2, discovery@k metric); compute overhead +5.8%–+17.1%; feedback ablation Table 6 (output+own_solution = 48.3% best); credit granularity logit > token > sequence > GRPO.
- Key takeaway (validation): paper §7 Future Work **trực tiếp mention thesis topic** — *"Future work should systematically study how individual aspects, such as the reprompt template, influence behavior"*. RQ1 (template taxonomy) được authors viết thẳng ra là open direction. Kết hợp với việc §5 không đo epistemic verbalization → RQ2 (suppression ở test-time) cũng là gap thật. CTC metric (RQ3) là natural extension của [[con_discovery_at_k]] vì các method có cost/attempt khác nhau.
- Lint deferred: một số wiki entry mới reference stubs chưa tạo (`con_teacher_regularization`, `con_epistemic_verbalization`, `con_ctc_metric`, `con_code_uncertainty_signals`) — listed in index's planned section.

