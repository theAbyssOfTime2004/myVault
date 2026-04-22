---
type: source
created: 2026-04-22
updated: 2026-04-22
tags: [paper, self-distillation, epistemic-verbalization, critique, core-thesis]
sources: [src_kim2026_why_self_distillation_degrades]
aliases: [Kim 2026 suppression paper, Kim et al. 2026 degrade]
---

# Kim et al. 2026 — Why Does Self-Distillation (Sometimes) Degrade the Reasoning Capability of LLMs?

arXiv:2603.24472v1 (25 Mar 2026). Microsoft Research + KAIST + Seoul National University.

Authors: Jeonghye Kim (first, KAIST intern), Xufang Luo (corresponding, MSR), Minbeom Kim, Sangmook Lee, Dohyung Kim, Jiwon Jeon, Dongsheng Li, Yuqing Yang.

## TL;DR

Self-distillation (bao gồm [[ent_sdpo]]) **suppress [[con_epistemic_verbalization]]** — những token uncertainty như *wait, hmm, perhaps, maybe, actually, alternatively, seems, might, likely, check*. Ở task coverage hẹp (Chemistry, LCBv6 131 questions) → OK, thậm chí có lợi. Ở math với 14k distinct problems, OOD eval → **degrade tới 40% trên AIME24**.

Paper frame vấn đề qua 2 nhân tố: **information richness** của teacher context và **task coverage** của training distribution.

## Setup

- **Base models**: DeepSeek-R1-Distill-Qwen-7B (primary), [[ent_qwen3_8b]] (thinking ON/OFF), [[ent_olmo3_7b_instruct]] (appendix).
- **Training data**: DAPO-Math-17k (14,000 distinct math problems, Yu et al. 2025).
- **Eval**: AIME24, AIME25, AMC23, MATH500 — OOD từ training.
- **Methods compared**: [[ent_grpo]] baseline vs [[ent_sdpo]].

## Định nghĩa central

### Epistemic verbalization
10 tokens theo Kim et al. 2026 (Understanding reasoning paper, cited):
```
T = {wait, hmm, perhaps, maybe, actually, alternatively, 
     seems, might, likely, check}
```
Metric: `E(y) = Σ_{t ∈ T} count(t, y)` cho mỗi response `y`.

### Information richness
Conditional mutual information:
```
I(y; c | x) = H(y | x) − H(y | x, c)
```
"Reduction in uncertainty về `y` khi có context `c`."

Orderings tested (§3):
- (1) Unguided: `c = ∅`, `I = 0`.
- (2) Solution-guided: `c = s` (full solution + CoT). Largest `I`.
- (3) Solution without think: `c = s\think` (removed `<think>` content). Intermediate.
- (4) Regeneration-conditioned: `c = ỹ` (response generated under setting 2). Intermediate.

### Task coverage
Số lượng và diversity problems trong training set. Paper vary `|D| ∈ {1, 8, 64, 128, 512, 14000}`.

## Kết quả chính

### Table 1 (§3) — Reasoning behavior under richer information

| Setting | Avg Score | Avg Length | Epistemic Count |
|---|---|---|---|
| (1) Unguided `c=∅` | 0.30 | 13,054 | 182.5 |
| (2) Solution-guided `c=s` | 0.98 | 1,873 | 8.8 |
| (3) Solution no-think `c=s\think` | 0.78 | 12,036 | 159.8 |
| (4) Regeneration `c=ỹ` | 0.95 | 2,808 | 24.1 |

**Takeaway 1**: càng giàu info, càng ngắn, càng confident, càng ít epistemic.

### Table 2 (§4) — SFT-based self-distillation

SFT DeepSeek-R1-Distill-Qwen-7B trên 800 **correct** trajectories, 2 dataset variants:

| Model | AIME24 | AIME25 | AMC23 | MATH500 |
|---|---|---|---|---|
| Base | 54.79 | 37.92 | 89.06 | 92.19 |
| SFT on `D_ug` (unguided, 12k tokens) | 51.04 | 40.00 | 87.66 | 90.93 |
| **SFT on `D_sg` (solution-guided, 2k tokens)** | **20.21** | **12.71** | **57.03** | **65.52** |

**Cả hai dataset đều là correct answers**. Chênh nhau duy nhất ở epistemic density. `D_sg` degrade mạnh nhất.

**Takeaway 2**: suppress epistemic verbalization degrade reasoning NGAY CẢ khi train trên correct trajectories.

### §5 — On-policy (GRPO vs SDPO)

**DeepSeek-R1-Distill-Qwen-7B** (Figure 3):
- GRPO modest gain: AIME24 54.7 → 56.0, AMC23 89.3 → 91.1.
- **SDPO `c=s`**: AIME24 drop ~40%, AMC23 drop ~15%.
- SDPO `c=s\think`: drop attenuated nhưng vẫn dưới base.
- Figure 3d: SDPO suppress tokens `wait` (-60.8), `maybe` (-17.1), `perhaps` (-17.1) rất mạnh.

**Qwen3-8B Thinking ON** (Figure 4):
- Cả GRPO và SDPO đều suppress, nhưng SDPO aggressive hơn.
- OOD AIME24 SDPO `c=s\think` degrade progressive theo training.
- Base Qwen3-8B "over-express" uncertainty → GRPO có margin để trim.

**Qwen3-8B Thinking OFF** (Figure 5):
- Response length ngắn sẵn → GRPO tự **tăng** epistemic verbalization để improve score (0.25 → 0.75+).
- SDPO ngược lại: giảm length, training score improve chậm, AIME24 slight drop (0.25 → 0.23).

### §5.4 — Fixed vs Moving target teacher (**KEY HYPERPARAM FINDING**)

SDPO paper (Hübotter 2026) default EMA 0.05. Kim et al. test:

| Teacher regime | Training | AIME24 |
|---|---|---|
| SDPO EMA 0.0 (fixed to initial) | better | better |
| SDPO EMA 0.05 (slow-moving) | aggressive suppression | worse |

Interpretation: feedback loop. Student → confident → teacher (cùng model) càng confident → amplify suppression over iterations. Fixed initial teacher break loop.

> *"Even slow updates (e.g., rate 0.05) lead to a sharper reduction in response length, resulting in larger performance degradation."*

**Contradiction trực tiếp với Hübotter 2026 default.** Hübotter §4.3 nói trust-region > EMA > frozen; Kim et al. nói frozen > EMA ở math.

### §6 — Task coverage × suppression

Bảng 3 so dataset:

| Dataset | Total questions | Unique types | Train/eval overlap |
|---|---|---|---|
| Chemistry (SciKnowEval) | 2,400 | **6 types** | 90/10 same dist |
| LiveCodeBench v6 | 131 | diverse nhưng small | **train == eval** questions |
| DAPO-Math-17k | 14,000 | diverse | eval OOD |

Figure 7–8: với |D| ∈ {1, 8, 64, 128}, SDPO wins fast + efficient. Với |D| = 512+, SDPO wins training score nhưng OOD degrade. GRPO scale ngược lại — càng nhiều |D|, càng tăng epistemic verbalization.

**Takeaway 4**: epistemic verbalization **redundant khi task hẹp, crucial khi task đa dạng**.

## Conclusion (§7)

> *"post-training objectives need to account not only for answer correctness, but also for eliciting and preserving uncertainty-aware reasoning behaviors."*

Paper không đề xuất algorithm mới — diagnostic paper, frame problem.

## Thesis impact

### RQ2 (suppression ở test-time code)
- Paper này là **reference chính cho RQ2**. Nhưng đo ở **train-time math** (DAPO-Math-17k, AIME).
- Thesis gap: **test-time code** (LCBv6 hard/very-hard, 1 question/run).
- Hypothesis testable: code có ít inherent epistemic tokens hơn math (structured syntax) → suppression magnitude nhỏ hơn? Cần measure.
- Concern: Kim et al. nói LCBv6 131 questions = *narrow task coverage* → SDPO có thể suppress nhưng không hurt. Thesis test-time setting càng hẹp hơn (1 q) → có thể SDPO "vẫn work" mặc dù suppress. Hay nói cách khác: discovery@k có thể ẩn đi suppression problem.

### RQ1 (template × suppression)
- `c` trong [[con_reprompt_template]] = control knob của `I(y;c|x)`.
- Kim et al. chỉ test `c ∈ {∅, s, s\think, ỹ}` — không vary **template structure** (phrasing, ordering, framing).
- Thesis taxonomy: giữ information content roughly constant, vary macro-structure → đo second-order effect template có modulate suppression không.

### RQ3 (CTC metric)
- Suppression → response ngắn (compute nhỏ) nhưng wrong (correctness thấp).
- [[con_discovery_at_k]] raw count không catch trade-off này; [[con_ctc_metric]] catches.
- Có thể thêm **epistemic-density per token** như sub-metric → ratio suppression/compute.

### Hyperparameter implication
- **Thesis MUST test EMA 0.0 vs 0.05**, không assume Hübotter default correct.
- Qwen3-8B thinking ON vs OFF cho behavior rất khác → thesis nên fix mode rõ ràng trong proposal (hiện đang ON trong examples).
- Budget 2750 generations/question × batch 16 = ~172 SDPO steps → vào vùng `|D|=1` trong Kim et al. framework. Suppression chắc chắn xảy ra.

### Validation framing
- Paper §7 conclude: post-training objectives must preserve uncertainty → thesis RQ2 được frame như open problem official.
- Combine với Hübotter 2026 §7 ("study how template influence behavior") → thesis sitting ở intersection của 2 open problems từ 2 papers đồng thuận.

## Related papers cited

- **Kim et al. 2026** (other — *Understanding reasoning in LLMs through strategic information allocation under uncertainty*) — origin của epistemic verbalization concept. Cần ingest: [[src_kim2026_strategic_info_allocation]] (stub).
- Hübotter et al. 2026 — [[src_hubotter2026_self_distillation]]. SDPO primary.
- Zhao et al. 2026 — *Self-distilled reasoner: On-policy self-distillation for LLMs* (arXiv:2601.18734). Alternative SD method.
- Ye et al. 2026 — *On-policy context distillation* (arXiv:2602.12275).
- Shenfeld et al. 2026 — *Self-distillation enables continual learning* (arXiv:2601.19897).
- Snell et al. 2022 — original self-distillation / learning by distilling context.

## Gaps / follow-up

- Paper không test template structure variation → RQ1 scope intact.
- Paper không test test-time (1-question) → RQ2 core intact.
- Paper không propose fix → thesis có thể đề xuất template-based regularization để preserve epistemic tokens.
- Paper đo trên math/chemistry/code separately — chưa cross-domain analysis về suppression transfer.

## Links

- [[ent_sdpo]] · [[ent_grpo]] · [[con_epistemic_verbalization]] · [[con_uncertainty_suppression]] · [[con_task_coverage]]
- [[src_hubotter2026_self_distillation]] (paper này critique)
- [[ent_qwen3_8b]] · [[ent_olmo3_7b_instruct]] · [[ent_deepseek_distill_7b]]
