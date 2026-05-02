# Bachelor Thesis Design Spec

**Title (advisor-approved):** Accelerating Test-Time Discovery in Complex Code Generation via Execution-Guided Self-Distillation

**Author:** (student) — bachelor thesis
**Created:** 2026-04-12
**Target submission:** ~2026-07-11 (12 weeks)
**Baseline paper:** Hübotter et al. 2026, *Reinforcement Learning via Self-Distillation* (arXiv 2601.20802)
**Central related work:** Kim et al. 2026, *Why Does Self-Distillation (Sometimes) Degrade the Reasoning Capability of LLMs?* (arXiv 2603.24472)

---

## 0. Tóm tắt tiếng Việt

| Mục | Nội dung |
|---|---|
| **Tên đề tài** | Accelerating Test-Time Discovery in Complex Code Generation via Execution-Guided Self-Distillation |
| **Mục tiêu** | Nghiên cứu cách thiết kế reprompt template ảnh hưởng đến hiệu quả khám phá của test-time SDPO trên code generation, kèm phân tích hiện tượng suppress uncertainty do Kim et al. nêu ra |
| **Paper nền** | Hübotter et al. 2026 (arXiv 2601.20802) — SDPO gốc, đặc biệt §5 test-time |
| **Related work trung tâm** | Kim et al. 2026 (arXiv 2603.24472) — phê bình SDPO suppress uncertainty trên math |
| **Setting** | Test-time SDPO (§5 paper) — bắt đầu từ `Qwen3-8B` instruct, update trong lúc infer từng câu, KHÔNG cần train-time SDPO checkpoint |
| **Dataset** | LiveCodeBench v6 — 19 câu hard (pass@64 < 0.5) + 9 câu very-hard (pass@64 < 0.03) |
| **RQ1** | Template formulation ảnh hưởng discovery@k và CTC thế nào? |
| **RQ2** | Trong test-time SDPO trên code, uncertainty có bị suppress qua các step như Kim et al. quan sát ở train-time math không? Template nào mitigate? |
| **RQ3** | Khi đo bằng CTC (compute-to-correct) thay vì chỉ số attempts, template nào Pareto-optimal? |
| **Component A (core)** | Main study: 7 templates × Qwen3-8B × LCBv6 hard/very-hard × 3 seeds |
| **Component B (bonus)** | Cross-domain sanity: load checkpoint `beanie00/math-SDPO-Qwen3-8B` eval trên LCBv6 — cắt đầu tiên nếu thiếu compute |
| **Component C (RQ2)** | Đo uncertainty markers (hedging comments, try/except, assertions…) qua các test-time step, phân tích theo template |
| **Component D (method-lite)** | Teacher-entropy stopping rule — dừng update khi entropy của self-teacher hội tụ |
| **Taxonomy template** | T1 Minimal / **T2 Standard (anchor)** / T3 Verbose / T4 JSON / T5 Reasoning-inducing / T6 First-person / T7 Cumulative history |
| **Metrics chính** | discovery@k (RQ1), CTC (RQ3), uncertainty marker density (RQ2), teacher entropy (Component D) |
| **Model starting point** | `Qwen3-8B` (instruct), KHÔNG fine-tune SDPO trước; pilot dùng `Qwen3-1.7B` để debug |
| **Budget** | ~$200 (Colab Pro có sẵn + $100 Modal + $100 cloud thuê) |
| **Cut-list** (nếu compute căng) | Cắt Component B → cắt T5–T7 → cắt very-hard subset → cắt seed thứ 3 |
| **Timeline** | 12 tuần (2026-04-12 → 2026-07-11); W1 đọc paper + setup, W2 reproduction, W3 pilot, W4 instrumentation, W5–7 Main Wave 1, W8 Wave 2, W9 Component B, W10 C+D, W11 draft, W12 revisions |
| **3 đóng góp** | (1) Taxonomy + ablation template cho test-time SDPO code (mở rộng §4.6 paper); (2) Lần đầu phân tích suppression trên test-time code, bắc cầu với Kim et al.; (3) Metric CTC + heuristic stopping rule |
| **Ngoài phạm vi** | Train-time SDPO on code; full LCBv6 131 câu; agentic/SWE-bench; loss variant mới; human eval; non-Python |
| **Rủi ro lớn nhất** | (a) Reproduction fail ở W2 → fallback Qwen3-1.7B; (b) compute overrun → dùng cut-list; (c) advisor muốn method-heavy thay vì empirical-primary → **cần confirm trong W1** |
| **Câu hỏi chốt với advisor (W1)** | (1) OK framing Kim-motivated? (2) empirical + method-lite đủ không? (3) LCBv6 hard subset có chấp nhận được? (4) ngôn ngữ viết thesis (Việt/Anh)? |

---

## 1. Motivation

Hübotter et al. §5 introduces **test-time Self-Distillation Policy Optimization (SDPO)**: starting from an instruct model (e.g. Qwen3-8B), the policy is updated *during inference* using execution feedback on the current problem, without any prior SDPO training. On LiveCodeBench v6 hard questions (pass@64 < 0.5) and very-hard questions (pass@64 < 0.03), test-time SDPO achieves ~3× speedup vs. best-of-k and solves problems no other method solves.

Two gaps in Hübotter §5 motivate this thesis:

1. **Reprompt template formulation is unexplored at test time.** The paper ablates broad feedback *categories* at train time (§4.6) but does not systematically study how the *textual formulation* of execution feedback influences test-time discovery efficiency. Paper §7 explicitly lists this as future work: *"future work should systematically study how individual aspects, such as the reprompt template, influence behavior."*

2. **Recent critique raises a behavioral concern.** Kim et al. 2026 show that **train-time** SDPO on **math** degrades OOD reasoning by suppressing epistemic verbalization (model stops expressing uncertainty, up to 40% drop). This phenomenon has not been studied in the test-time setting nor on the code domain. If a similar pattern manifests in test-time SDPO on code, reprompt template design may be a lever to mitigate it.

The thesis frames template study as active hypothesis-testing motivated by the Kim et al. concern, rather than a passive ablation.

---

## 2. Research Questions

- **RQ1 — Template effect on discovery efficiency.** How does the formulation of the reprompt template influence test-time SDPO discovery efficiency (discovery@k and compute-to-correct) on LiveCodeBench v6 hard and very-hard subsets?

- **RQ2 — Suppression transfer to test-time code.** Within test-time SDPO updates on code, does uncertainty expression decrease across steps in a pattern analogous to the train-time math suppression reported by Kim et al.? Which templates amplify or mitigate the pattern?

- **RQ3 — Compute-Pareto.** When discovery efficiency is measured as compute-to-correct (CTC, wall-clock or FLOPs to reach a target pass rate) rather than attempt count, which templates are Pareto-optimal?

---

## 3. Approach

All experiments use **test-time SDPO** as defined in Hübotter §5: starting point is the official instruct-tuned `Qwen3-8B` release, with **no prior SDPO fine-tuning**; per-question SDPO updates run during inference until the problem is solved or the compute budget is exhausted.

This is a deliberate choice: the thesis studies test-time dynamics, not train-time. No train-time code-SDPO checkpoint is required (none exists publicly, and training one is infeasible within the compute budget).

The thesis delivers four experimental components.

### 3.1 Component A — Main template study *(core, RQ1 + RQ3)*

Seven-template taxonomy applied to test-time SDPO on Qwen3-8B over LCBv6 hard / very-hard subsets, with 3 seeds.

**Anchor template T2** = paper's default. The other six templates each vary *one* dimension from T2 for a clean ablation.

| ID | Name | Variable | Content sketch |
|----|------|----------|----------------|
| T1 | Minimal | remove structure | "Your previous solution is incorrect. Provide a corrected version." |
| **T2** | **Standard (anchor)** | **baseline** | **failing test input / expected / actual + error_type** |
| T3 | Verbose | add stack trace | T2 + full traceback + previous code |
| T4 | Structured JSON | format only | same content as T2, JSON-encoded |
| T5 | Reasoning-inducing | add meta prompt | T2 + "First, identify the root cause, then fix it." |
| T6 | First-person | grammatical person | "I attempted this problem and got X. Let me reconsider." |
| T7 | Cumulative history | memory depth | all N previous attempts listed, not just the latest |

Wave 1 runs T1–T4 on 19 hard × 3 seeds (228 test-time SDPO trajectories). Wave 2 adds T5–T7 on 9 very-hard × 2 seeds (54 trajectories). Per-trajectory compute budgets are drawn from Hübotter §5 (batch size 16, up to ~100–1000 SDPO steps depending on difficulty).

### 3.2 Component B — Cross-domain sanity check *(bonus, cuttable)*

Load `beanie00/math-SDPO-Qwen3-8B-think-step-100` (train-time SDPO trained on MATH training set, released by Kim et al.), evaluate with standard sampling on LCBv6 hard. This answers a narrow sanity question: *"If a practitioner deploys a math-trained SDPO checkpoint on code, what does the behavior look like?"* Not core contribution; cut first if compute slips.

### 3.3 Component C — Suppression analysis on test-time code outputs *(RQ2)*

For every (question, template, seed) trajectory produced by Component A, measure **uncertainty markers** at each test-time step:

- Count of hedging comments (`# might be`, `# not sure`, `# assumption:`)
- Count of defensive constructs (`try/except`, `assert`, input validation branches, fallback cases)
- Count of `if __name__ == '__main__'` test-harness additions
- Comment-to-code ratio

Plot marker density vs. test-time step, stratified by template. Three possible outcomes (all defendable):

- **(a)** Markers decrease across steps → replicates Kim et al. pattern in test-time code setting.
- **(b)** Markers stable or increase → test-time differs from train-time; contribution is the dissociation.
- **(c)** Template-dependent → templates are a mitigation lever; strongest positive result for the thesis.

### 3.4 Component D — Method-lite: teacher-entropy stopping rule *(RQ3)*

Introduce a simple adaptive stopping heuristic: halt test-time updates when the self-teacher's per-token entropy drops below a threshold (indicating the teacher has converged and further updates waste compute). Compare against fixed-budget stopping on CTC.

This is the thesis's small method contribution; scope-controlled so it can be cut to a subsection if results are weak.

---

## 4. Metrics

- **discovery@k** = P(T ≤ k), where T is discovery time (from Hübotter §5). Primary RQ1 metric.
- **pass@k** — classical i.i.d. sampling baseline, for reference only.
- **CTC(ε)** = compute (wall-clock seconds and estimated FLOPs) required to reach pass rate ≥ ε. Primary RQ3 metric. Novel to this thesis in the test-time SDPO context.
- **Uncertainty marker density** (per category) — primary RQ2 metric. Adapted from Kim et al.'s epistemic verbalization metric; operational definitions in Component C.
- **Teacher entropy over steps** — input to Component D stopping rule, also reported as a behavioral descriptor.

---

## 5. Models and dataset

- **Starting point model:** `Qwen3-8B` (official instruct release). No prior SDPO fine-tuning. This matches Hübotter §5.
- **Pilot model:** `Qwen3-1.7B` (for pipeline debugging only; results not reported as main findings).
- **Benchmark:** LiveCodeBench v6.
  - **Hard subset:** 19 questions with pass@64 < 0.5 (per Hübotter §5).
  - **Very-hard subset:** 9 questions with pass@64 < 0.03.
  - Full 131-question set is explicitly out of scope.
- **Cross-domain checkpoint (Component B only):** `beanie00/math-SDPO-Qwen3-8B-think-step-100` + GRPO counterpart, from the Kim et al. release.

---

## 6. Compute budget

Total target: **~$200** (Colab Pro subscription + $100 Modal credit + $100 cloud rental on runpod/vast.ai).

| Phase | Hardware | Hours | Cost |
|-------|----------|-------|------|
| Dev / instrumentation | Colab Pro | — | $0 (already owned) |
| Reproduction sanity check | A100 40GB | 5 | $15 |
| Pilot (Qwen3-1.7B) | L4 24GB | 12 | $10 |
| Main Wave 1: T1–T4 × 19 hard × 3 seeds | A100 40GB | 76 | $76 |
| Main Wave 2: T5–T7 × 9 very-hard × 2 seeds | A100 40GB | 36 | $36 |
| Buffer / retries | — | — | $63 |

**Cut-list ordering** if compute slips: drop Component B → drop T5–T7 → drop very-hard subset → drop 3rd seed.

---

## 7. Timeline (12 weeks)

| Week | Milestone |
|------|-----------|
| 1 | Read Hübotter §5 + §4.6 and Kim et al. §3; set up Colab Pro + Modal; fork status check |
| 2 | Reproduction sanity check: one LCBv6 hard question with T2 template; verify discovery@k matches paper |
| 3 | Pilot on Qwen3-1.7B; debug 7-template pipeline end-to-end |
| 4 | Instrumentation: logging for discovery@k, CTC, teacher entropy, uncertainty markers |
| 5–7 | Main Wave 1 on A100 (Modal) |
| 8 | Main Wave 2 |
| 9 | Component B cross-domain eval (if on schedule) |
| 10 | Component C suppression analysis + Component D stopping-rule experiments |
| 11 | Write thesis draft, generate plots |
| 12 | Revisions, final submission |

---

## 8. Contribution claims

1. **Template taxonomy and empirical ablation for test-time SDPO on code.** Extends Hübotter §4.6 (train-time feedback categories) to the test-time inference setting with finer-grained formulation variables.
2. **First test-time code analog of the Kim et al. suppression analysis.** Reports whether the uncertainty-suppression pattern observed in train-time math transfers to test-time code, and characterizes template dependence.
3. **CTC metric and teacher-entropy stopping rule.** A compute-aware metric for test-time discovery, plus a simple adaptive-stop heuristic evaluated against fixed-budget stopping.

---

## 9. Out of scope

Explicitly **not** attempted in this thesis:

- Train-time SDPO on code (no compute).
- Full LCBv6 (131 questions) — hard/very-hard subsets only.
- Long-horizon agentic settings (SWE-bench, Aider, OpenHands).
- New SDPO loss variants or architectural changes beyond the method-lite stopping rule.
- Multilingual or non-Python code generation.
- Human evaluation of code quality.

---

## 10. Risks and mitigations

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Reproduction of paper numbers fails in Week 2 | Medium | Week 2 is explicitly a sanity-check gate. If it fails, drop to Qwen3-1.7B main study and flag as a limitation. |
| Test-time SDPO diverges on some templates | Medium | Apply Hübotter §4.3 trust-region teacher regularization; cap update steps. |
| Cloud compute overrun | Medium | Cut-list above; Wave 2 and Component B are first to go. |
| Uncertainty marker metric too noisy to show signal | Medium | Report descriptive statistics and acknowledge as a limitation; result (b) from §3.3 is still a valid contribution. |
| Component D stopping rule shows no improvement | Low-Med | Present as negative result; does not block RQ1 and RQ2. |
| Advisor expects strong method contribution rather than empirical + method-lite | Unknown | **Confirm with advisor in Week 1 before locking.** |

---

## 11. Open questions for advisor (Week 1 checkpoint)

1. Is the Kim-et-al.-motivated framing acceptable as the thesis narrative?
2. Is empirical-primary with method-lite (Component D) sufficient, or is a heavier method contribution required?
3. Is the LCBv6 hard/very-hard subset acceptable as the evaluation, rather than the full 131-question set?
4. Preferred thesis writing language (Vietnamese / English)?
