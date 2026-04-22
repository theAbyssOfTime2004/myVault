---
type: synthesis
created: 2026-04-22
updated: 2026-04-22
tags: [thesis-impact, rq1, rq2, rq3, synthesis]
sources: [src_kim2026_why_self_distillation_degrades, src_hubotter2026_self_distillation]
---

# Kim et al. 2026 — Thesis impact synthesis

Consolidated view: [[src_kim2026_why_self_distillation_degrades]] ảnh hưởng thesis như thế nào. Gom các inline notes rải trong entities/concepts về 1 chỗ để reference khi viết proposal/chapter.

## TL;DR cho supervisor

Paper Kim et al. 2026 critique [[ent_sdpo]] ở dimension **[[con_uncertainty_suppression]]**: self-distillation ép student imitate confident teacher → mất epistemic tokens → hurt OOD math. Thesis ba RQs **tất cả sit trong gap mà Kim et al. chưa cover**:

- Kim đo **train-time math**; thesis đo **test-time code**.
- Kim chỉ vary content `c`; thesis vary **template structure**.
- Kim dùng accuracy OOD; thesis cần **CTC metric** vì test-time có compute trade-off.

Validation: hai papers chính của thesis ([[src_hubotter2026_self_distillation]] + Kim 2026) **cùng frame RQs của thesis là open problems** trong conclusion/future work của họ.

## Impact theo RQ

### RQ1 — Template taxonomy

**Kim finding relevant**: information richness `I(y; c|x)` quyết định suppression magnitude. `c` trong teacher prompt = control knob.

**Kim test**: chỉ vary *what goes into c*:
- `c = ∅`
- `c = s\think`
- `c = ỹ` (regenerated)
- `c = s` (full solution)

**Gap cho thesis**: paper không vary **cách `c` được format/frame**:
- Phrasing: "Correctly solve" vs "Identify your mistake" vs "Rate confidence first".
- Ordering: feedback-first vs solution-first.
- Explicit uncertainty elicitation prompts.
- Negative instruction ("Do not repeat the mistake").

**Thesis contribution**: systematic template taxonomy giữ information content roughly constant, vary macro-structure → đo second-order effect. Nếu template có thể **preserve epistemic tokens** mà vẫn deliver credit signal → contribution đáng kể.

**Reference page**: [[con_reprompt_template]] (section "Template là suppression lever").

### RQ2 — Uncertainty suppression ở test-time code

**Kim finding relevant**: SDPO suppress epistemic verbalization mạnh hơn GRPO. Ở math broad coverage → AIME24 drop 40%.

**Kim scope**:
- Domain: math (DAPO-Math-17k, AIME24/25, AMC23, MATH500).
- Training regime: train-time multi-question.
- Model: DeepSeek-R1-Distill-7B (primary), Qwen3-8B, Olmo3-7B-Instruct.
- Measurement: 10 epistemic tokens *wait/hmm/perhaps/maybe/actually/alternatively/seems/might/likely/check*.

**Gap cho thesis**:
- Domain: **code** (LCBv6 hard/very-hard).
- Regime: **test-time** (1-question, weights update cho câu đó).
- Measurement cần mở rộng: code có ít "wait/hmm" tự nhiên hơn math → cần **code-specific uncertainty signals** (try/except density, assert frequency, defensive branching, "# TODO/FIXME" comments, alternative hypothesis in docstrings).

**Testable hypotheses**:
- **H1**: Suppression xảy ra monotonic qua SDPO iterations trên LCBv6 hard (analog với train-time finding).
- **H2**: Magnitude nhỏ hơn math vì code structured (syntax "ép" structure thay vì verbalize uncertainty).
- **H3**: Theo [[con_task_coverage]] Kim framework: test-time = extreme narrow (|D|=1) → suppression có thể xảy ra nhưng *không hurt discovery* trên chính câu đó. Thesis có thể thêm **leave-one-out generalization** như OOD proxy.

**Reference pages**: [[con_uncertainty_suppression]], [[con_epistemic_verbalization]], [[con_test_time_self_distillation]] (section "RQ2 gap"), [[con_code_uncertainty_signals]] (stub — cần tạo).

### RQ3 — CTC metric

**Kim finding relevant**: suppression → response ngắn nhưng wrong. Length alone không đủ để đánh giá.

**Gap cho thesis**:
- [[con_discovery_at_k]] chỉ đếm attempts, không đo compute cost.
- [[con_ctc_metric]] (planned) đo compute-to-correct.
- Có thể thêm **epistemic density per token** hoặc **epistemic-efficiency** (epistemic tokens retained / compute spent) như sub-metric.

**Thesis contribution**: CTC Pareto frontier vs template variant → trade-off giữa compute, correctness, suppression rate.

**Reference page**: [[con_discovery_at_k]] (section "Thesis extension: CTC").

## Contradiction với Hübotter 2026 — hyperparam implication

| Dimension | Hübotter 2026 default | Kim 2026 finding | Thesis obligation |
|---|---|---|---|
| Teacher regularization | Trust-region > EMA 0.05 > frozen | **Frozen (EMA 0.0) > EMA 0.05** | MUST ablate cả hai |
| Base model | Qwen3-8B ok any mode | Thinking ON/OFF behavior rất khác | Fix mode explicitly, recommend ON |
| Task coverage | SDPO win narrow (Chemistry, LCB) | SDPO lose broad (DAPO-Math) | Thesis narrow → theo Kim nên OK, nhưng verify |

**Feedback loop argument** của Kim: student confident → teacher (same model) càng confident → amplify suppression. Fixed teacher break loop vì giữ epistemic baseline của base model.

**Rủi ro**: nếu thesis follow Hübotter default (EMA 0.05) without ablation → có thể báo cáo suppression effect mà thực ra là artifact của EMA choice, không phải của SDPO mechanism.

**Reference page**: [[con_self_teacher]] (section "Teacher update regime").

## Validation framing (cho thesis intro/motivation)

Quote trực tiếp có thể cite:

**Hübotter 2026 §7 (Future Work)**:
> *"Future work should systematically study how individual aspects, such as the reprompt template, influence behavior."*

**Kim 2026 §7 (Conclusion)**:
> *"post-training objectives need to account not only for answer correctness, but also for eliciting and preserving uncertainty-aware reasoning behaviors."*

→ Thesis sit ở **intersection của hai open problems** được authoritative papers khẳng định là mở. Bản thân proposal có thể citing cả hai để frame RQs.

## Non-contradicted strengths của SDPO

Kim et al. **không reject SDPO** — họ identify conditions nó win vs lose:
- Win: narrow task coverage (Chemistry 6 types, LCB 131 q).
- Lose: broad coverage OOD (DAPO-Math 14k, AIME eval).

Thesis regime (test-time, LCBv6 hard, 1-question) = **extreme narrow** theo Kim framework → SDPO expected win *về discovery*, nhưng suppression có thể happen âm thầm mà discovery@k không catch được. Đây là value proposition của RQ2: show **hidden cost** mà metric của Hübotter không thấy.

## Risk / limitation của thesis framing

- **Code không phải math**: Kim findings có thể không transfer. Code structured syntax có thể "absorb" uncertainty vào form khác (branching, guards) thay vì tokens. Hypothesis cần empirical test trước khi assume.
- **|D|=1 regime extreme**: Kim curve `|D| ∈ {1,8,64,128,512,14000}` cho thấy `|D|=1` SDPO dominate. Thesis ở regime đó → suppression có thể không hurt anything measurable. **Backup plan**: thêm cross-question generalization test.
- **Stub dependency**: thesis reference [[src_kim2026_strategic_info_allocation]] (original epistemic verbalization paper) chưa ingest full — cần tìm và đọc để solidify definition 10 tokens.

## Action items từ synthesis này

- [ ] Tạo [[con_code_uncertainty_signals]] page với operational definition.
- [ ] Tạo [[con_ctc_metric]] page standalone (hiện chỉ mention trong discovery@k).
- [ ] Tạo [[con_teacher_regularization]] page so sánh EMA 0.0 / 0.05 / trust-region / frozen.
- [ ] Tìm và ingest [[src_kim2026_strategic_info_allocation]] full.
- [ ] Migrate `SDPO 2026-04-11.md` → `syn_thesis_proposal.md` và update theo insight từ paper Kim.

## Links

- [[src_kim2026_why_self_distillation_degrades]] (primary)
- [[src_hubotter2026_self_distillation]] (counter-paper)
- [[con_epistemic_verbalization]] · [[con_uncertainty_suppression]] · [[con_task_coverage]]
- [[con_reprompt_template]] · [[con_test_time_self_distillation]] · [[con_discovery_at_k]]
- [[ent_sdpo]] · [[ent_qwen3_8b]] · [[ent_deepseek_distill_7b]]
