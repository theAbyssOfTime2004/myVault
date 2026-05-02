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

## [2026-04-22] ingest | Kim et al. 2026 — Why Does Self-Distillation (Sometimes) Degrade Reasoning

- Source: `raw/kim2026_why_self_distillation_degrades.md` (arXiv:2603.24472v1, 18-page PDF full-ingest từ `C:\Users\Maidanng\Downloads\2603.24472v1.pdf`).
- Created: [[src_kim2026_why_self_distillation_degrades]], [[src_kim2026_strategic_info_allocation]] (stub), [[con_epistemic_verbalization]], [[con_uncertainty_suppression]], [[con_task_coverage]], [[ent_deepseek_distill_7b]].
- Updated: [[ent_sdpo]] (critique section + EMA contradiction), [[ent_qwen3_8b]] (thinking ON/OFF behavior), [[ent_olmo3_7b_instruct]] (Chemistry counterpoint), [[con_self_teacher]] (fixed vs moving teacher), [[con_reprompt_template]] (template as suppression lever), [[con_test_time_self_distillation]] (RQ2 gap section), [[con_credit_assignment]] (suppression not penalized caveat).
- Updated: `wiki/index.md` (sources 1→3, entities 6→7, concepts 6→9, planned list shrunk).
- Key findings captured: suppression 10 epistemic tokens (wait/hmm/maybe/...); SFT on correct solution-guided responses drops AIME24 54.8→20.2; SDPO drops AIME24 ~40% on DeepSeek-R1-Distill-7B; EMA 0.0 > EMA 0.05 (contradicts Hübotter default); task coverage Chemistry 6 types narrow vs DAPO-Math 14k broad.
- Key takeaway cho thesis: paper fill RQ2 framework formally — suppression là phenomenon documented, nhưng **chưa ai đo ở test-time code**. RQ2 scope intact, thậm chí strengthened vì có reference quantitative. Contradiction EMA forces thesis phải ablate hyperparam. RQ1 × RQ2 intersection formalized: template là "suppression lever" qua `I(y;c|x)`.
- Note: hai papers chính của thesis (Hübotter + Kim) **agree là open problems đó chính là thesis RQs**. Hübotter §7 future work explicit về template, Kim §7 explicit về preserving uncertainty-aware reasoning.

## [2026-05-02] synthesis | template taxonomy rationale

- Created: [[syn_template_taxonomy_rationale]] — principled justification cho 7 templates qua 3 dimensions: (1) information content ← Kim et al. `I(y;c|x)`; (2) instruction framing ← Hübotter §4.6 + §7 open question; (3) memory depth ← Hübotter §5 sliding window + Kim suppression accumulation.
- Updated: `wiki/index.md` (synthesis 2→3).
- Key takeaway: taxonomy defensible mà không cần cite source mới — derive trực tiếp từ 2 papers đã có. Template T2 là anchor, 6 còn lại vary đúng 1 dimension mỗi cái → clean ablation design.

## [2026-05-02] migrate | thesis design spec → syn_thesis_proposal

- Source: `2026-04-12-sdpo-thesis-design.md` (Cursor, generated 2026-04-12) — bản đầy đủ nhất của thesis plan, chưa được ingest vào wiki.
- Created: [[syn_thesis_proposal]] — ground truth design spec với title, RQ1/2/3, 7 templates (T1–T7), 4 components, budget ~$200, timeline 12 tuần, cut-list, risks.
- Updated: `wiki/index.md` (synthesis 1→2, removed old SDPO 2026-04-11 stub link).
- Key new info so với wiki cũ: 7 templates đã define đầy đủ (T1 Minimal / T2 Standard / T3 Verbose / T4 JSON / T5 Reasoning-inducing / T6 First-person / T7 Cumulative); budget là ~$200 không phải $100; pilot model là Qwen3-1.7B; 2 waves experiment.

## [2026-04-23] experiment | multi-turn inference loop — first working end-to-end

- **Status**: Pipeline hoạt động end-to-end trên LCBv6, 1 câu/lần chạy.
- **Components confirmed working**:
  - Load 1 bài từ `train.parquet`
  - Model sinh lời giải (Qwen3-8B, vLLM)
  - Evaluator chạy test cases → trả rich feedback
  - Reprompt loop với feedback → lặp đến khi pass hoặc hết budget
  - Logging đầy đủ: reward/acc, prompt+response token length, feedback detail, total runtime
- **Observed behavior trên 3 câu**:
  - `q_2`: pass gần như ngay (easy case)
  - `q_120`: pass sau số turn trung bình
  - `q_1`: pass sau **54 turns**, nhiều lỗi trung gian (MemoryError) trước khi hội tụ — cho thấy hard-case cần nhiều iteration
- **Note**: Đây là **multi-turn inference** (không có weight update) — baseline tương đương `baseline_multiturn/multiturn.py` trong [[src_lasgroup_sdpo_repo]]. Bước tiếp theo là thêm SDPO gradient step để thành test-time SDPO thật sự.
- **Infrastructure gap đã bridge**: pipeline 1-câu hoạt động → foundation để add weight update layer lên trên.

## [2026-04-23] concept | SDPO loss mechanics derivation

- Created: [[con_sdpo_loss_mechanics]] — derivation kỹ thuật KL divergence → gradient per logit = π_S − π_T, generalized JSD (α), IS correction, EMA teacher update, top-K approximation. Includes code refs (`core_algos.py:1085`) và implications cho RQ1/RQ2/RQ3.
- Updated: `wiki/index.md` (concepts 9→10).
- Key takeaway: formal mechanism chứng minh template (c) và α là knobs trực tiếp trên gradient direction — không chỉ là hyperparam empirical. α ablation là new angle RQ2 chưa ai test.

## [2026-04-23] ingest | lasgroup/SDPO codebase (GitHub raw API)

- Source: https://github.com/lasgroup/SDPO — read via curl GitHub raw (không clone). Files covered: `README.md`, `verl/trainer/config/sdpo.yaml`, `verl/trainer/config/actor/actor.yaml` (templates + defaults), `verl/trainer/ppo/core_algos.py` (`compute_self_distillation_loss` line 1085), `verl/workers/actor/dp_actor.py` (`TrustRegionTeacher`, `_update_teacher` EMA), `experiments/{generalization,rich_feedback,ttt}/*.sh`, `baseline_multiturn/multiturn.py`, `run_local_sdpo.sh`.
- Created: [[src_lasgroup_sdpo_repo]].
- Updated: `wiki/index.md` (sources 3→4).
- Key findings: (1) **no dedicated TTT-SDPO script** — `experiments/ttt/` chỉ có multi-turn baseline, thesis phải tự wire up; (2) default `remove_thinking_from_demonstration=True` trùng Kim's `c=s\think`; (3) rich_feedback LCBv6 hyperparams khác default đáng kể — ALPHA=1.0 (reverse KL), LR=1e-6, mini_batch=1, topk=20, ema=0.01; (4) α knob (forward/JSD/reverse KL) chưa được Kim ablate — thesis RQ2 ablation mới; (5) fixed teacher bật qua `teacher_update_rate=0.0` không cần code change; (6) 19 LCB hard question IDs = {1,3,10,43,46,59,69,74,86,91,92,95,100,103,111,120,125,127,129}; (7) templates là plain strings với placeholders — trivial cho RQ1 taxonomy.
- Key takeaway: infrastructure cho RQ1 và RQ2 (ngoại trừ TTT loop) có sẵn qua config flags. Thesis implementation cost chính = TTT-SDPO loop + epistemic token logging callback. Hyperparam differentials giữa §3 và §4 cho biết code regime cần tuning riêng từ scratch.

## [2026-04-22] synthesis | Kim 2026 thesis impact consolidation

- Created: [[syn_kim2026_thesis_impact]] — first synthesis page của thesis.
- Purpose: gom thesis impact notes rải trong entities/concepts về 1 page, chuẩn bị cho proposal/chapter writing.
- Contains: RQ1/2/3 impact mapping, hyperparam contradiction table (Hübotter vs Kim), validation framing với direct quotes, testable hypotheses, action items.
- Updated: `wiki/index.md` (synthesis section giờ có 1 page + proposal stub).

