---
type: synthesis
created: 2026-04-12
updated: 2026-05-02
tags: [thesis-proposal, rq1, rq2, rq3, ground-truth]
sources: [src_hubotter2026_self_distillation, src_kim2026_why_self_distillation_degrades]
aliases: [thesis proposal, design spec]
---

# Thesis Design Spec — Ground Truth

Migrated từ `2026-04-12-sdpo-thesis-design.md` (Cursor). Đây là bản đầy đủ nhất của thesis plan. Supersedes `SDPO 2026-04-11.md`.

**Title (advisor-approved):** Accelerating Test-Time Discovery in Complex Code Generation via Execution-Guided Self-Distillation

**Target submission:** 2026-07-11 (12 weeks từ 2026-04-12)

---

## Tóm tắt nhanh

| Mục | Nội dung |
|---|---|
| **Setting** | Test-time SDPO (§5 Hübotter) — bắt đầu từ `Qwen3-8B` instruct, update trong lúc infer từng câu, KHÔNG cần train-time SDPO checkpoint |
| **Dataset** | LiveCodeBench v6 — 19 hard (pass@64 < 0.5) + 9 very-hard (pass@64 < 0.03) |
| **Pilot model** | `Qwen3-1.7B` (debug pipeline, kết quả không report chính thức) |
| **Budget** | ~$200 (Colab Pro + $100 Modal + $100 RunPod/Vast.ai) |
| **Submission** | 2026-07-11 |

---

## Research Questions

- **RQ1** — Template formulation ảnh hưởng discovery@k và CTC thế nào?
- **RQ2** — Test-time SDPO trên code có suppress uncertainty qua các step như Kim et al. quan sát ở train-time math không? Template nào mitigate?
- **RQ3** — Khi đo bằng CTC (compute-to-correct) thay vì chỉ số attempts, template nào Pareto-optimal?

---

## 3 Contribution claims

1. **Template taxonomy + ablation** cho test-time SDPO code — mở rộng §4.6 Hübotter (train-time) sang test-time với finer-grained formulation variables.
2. **First test-time code analog của Kim et al. suppression analysis** — liệu pattern train-time math có transfer sang test-time code không, và template dependence ra sao.
3. **CTC metric + teacher-entropy stopping rule** — compute-aware metric cho test-time discovery + adaptive-stop heuristic.

---

## 7 Templates (Component A)

T2 = anchor (paper default). 6 templates còn lại vary **1 dimension** từ T2.

| ID | Tên | Variable | Content sketch |
|---|---|---|---|
| T1 | Minimal | remove structure | "Your previous solution is incorrect. Provide a corrected version." |
| **T2** | **Standard (anchor)** | **baseline** | **failing test input / expected / actual + error_type** |
| T3 | Verbose | add stack trace | T2 + full traceback + previous code |
| T4 | Structured JSON | format only | same content as T2, JSON-encoded |
| T5 | Reasoning-inducing | add meta prompt | T2 + "First, identify the root cause, then fix it." |
| T6 | First-person | grammatical person | "I attempted this problem and got X. Let me reconsider." |
| T7 | Cumulative history | memory depth | all N previous attempts listed, not just latest |

---

## 4 Components

### Component A — Main template study (core, RQ1 + RQ3)

- **Wave 1**: T1–T4 × 19 hard × 3 seeds = **228 trajectories**
- **Wave 2**: T5–T7 × 9 very-hard × 2 seeds = **54 trajectories**
- Per-trajectory: batch size 16, up to ~100–1000 SDPO steps tùy difficulty

### Component B — Cross-domain sanity check (bonus, cắt đầu tiên)

Load `beanie00/math-SDPO-Qwen3-8B-think-step-100`, eval trên LCBv6 hard. Câu hỏi narrow: "Math-trained SDPO checkpoint behaves how on code?"

### Component C — Suppression analysis (RQ2, post-hoc free)

Với mỗi trajectory từ Component A, đo **uncertainty markers** per step:
- Hedging comments (`# might be`, `# not sure`, `# assumption:`)
- Defensive constructs (`try/except`, `assert`, input validation, fallback)
- `if __name__ == '__main__'` test-harness additions
- Comment-to-code ratio

3 possible outcomes (tất cả đều defensible):
- **(a)** Markers decrease → replicates Kim et al. pattern ở test-time code
- **(b)** Markers stable/increase → test-time differs from train-time; contribution là dissociation
- **(c)** Template-dependent → templates là mitigation lever; strongest positive result

### Component D — Teacher-entropy stopping rule (method-lite, RQ3)

Dừng test-time update khi per-token entropy của self-teacher drops below threshold. So sánh vs. fixed-budget stopping trên CTC. Có thể cut xuống thành subsection nếu results yếu.

---

## Metrics

| Metric | RQ | Mô tả |
|---|---|---|
| **discovery@k** | RQ1 | P(T ≤ k), T = discovery time. Primary RQ1 metric. |
| **CTC(ε)** | RQ3 | Wall-clock / FLOPs để reach pass rate ≥ ε. Novel với test-time SDPO. |
| **Uncertainty marker density** | RQ2 | Per-category count per step. Adapted từ Kim et al. |
| **Teacher entropy** | Component D | Per-token entropy của self-teacher over steps. |
| pass@k | reference | Classical baseline, không phải primary metric. |

---

## Compute budget

| Phase | Hardware | Hours | Cost |
|---|---|---|---|
| Dev / instrumentation | Colab Pro | — | $0 |
| Reproduction sanity | A100 40GB | 5h | $15 |
| Pilot (Qwen3-1.7B) | L4 24GB | 12h | $10 |
| Wave 1: T1–T4 × 19 hard × 3 seeds | A100 40GB | 76h | $76 |
| Wave 2: T5–T7 × 9 very-hard × 2 seeds | A100 40GB | 36h | $36 |
| Buffer / retries | — | — | $63 |

**Cut-list** (theo thứ tự): Component B → T5–T7 → very-hard subset → seed thứ 3.

---

## Timeline (12 tuần)

| Week | Milestone |
|---|---|
| 1 | Đọc Hübotter §5 + §4.6 + Kim §3; setup Colab + Modal |
| 2 | Reproduction sanity: 1 LCBv6 hard question với T2; verify discovery@k matches paper |
| 3 | Pilot Qwen3-1.7B; debug 7-template pipeline end-to-end |
| 4 | Instrumentation: logging discovery@k, CTC, teacher entropy, uncertainty markers |
| 5–7 | Main Wave 1 (Modal A100) |
| 8 | Main Wave 2 |
| 9 | Component B cross-domain eval (nếu on schedule) |
| 10 | Component C suppression analysis + Component D stopping rule |
| 11 | Viết thesis draft, generate plots |
| 12 | Revisions, final submission |

**Current status (2026-05-02, ~week 3–4)**:
- ✅ Multi-turn inference loop end-to-end (POC baseline)
- ✅ Trajectory logging hoạt động
- ⬜ TTT-SDPO gradient step (chưa có)
- ⬜ 7-template pipeline
- ⬜ Instrumentation đầy đủ (CTC, teacher entropy, uncertainty markers)

---

## Risks & mitigations

| Risk | Likelihood | Mitigation |
|---|---|---|
| Reproduction fail W2 | Medium | Fallback Qwen3-1.7B main study, flag limitation |
| Test-time SDPO diverges on some templates | Medium | Trust-region teacher regularization; cap update steps |
| Compute overrun | Medium | Cut-list theo thứ tự trên |
| Uncertainty marker metric quá noisy | Medium | Report descriptive stats; outcome (b) vẫn là valid contribution |
| Component D không improve | Low-Med | Present as negative result; không block RQ1/RQ2 |
| Advisor muốn method-heavy thay vì empirical | Unknown | **Confirm W1** |

---

## Out of scope

- Train-time SDPO on code
- Full LCBv6 131 questions
- Agentic settings (SWE-bench, OpenHands)
- New SDPO loss variants
- Multilingual / non-Python
- Human evaluation

---

## Open questions cho advisor (W1 checkpoint)

1. Kim-motivated framing có acceptable không?
2. Empirical-primary + method-lite (Component D) có đủ không?
3. LCBv6 hard/very-hard subset có chấp nhận được không?
4. Ngôn ngữ viết thesis (Việt / Anh)?

---

## Links

- [[src_hubotter2026_self_distillation]] — paper gốc SDPO, §5 test-time
- [[src_kim2026_why_self_distillation_degrades]] — motivation RQ2
- [[src_lasgroup_sdpo_repo]] — codebase implementation
- [[con_reprompt_template]] — template taxonomy detail
- [[con_test_time_self_distillation]] — TTT regime mechanics
- [[con_epistemic_verbalization]] · [[con_uncertainty_suppression]] — RQ2 concepts
- [[con_discovery_at_k]] — primary RQ1 metric
- [[syn_kim2026_thesis_impact]] — RQ1/2/3 impact mapping từ Kim 2026
