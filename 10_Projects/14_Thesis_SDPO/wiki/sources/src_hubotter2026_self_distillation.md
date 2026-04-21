---
type: source
created: 2026-04-22
updated: 2026-04-22
tags: [sdpo, rl, self-distillation, rlrf, rlvr, code, origin-paper]
cite: "Hübotter et al., 2026"
arxiv: "2601.20802"
url: https://arxiv.org/abs/2601.20802
code: https://github.com/lasgroup/SDPO
raw: raw/hubotter2026_sdpo.md
depth: full-paper
---

# Hübotter et al. 2026 — Reinforcement Learning via Self-Distillation

**Tác giả**: J. Hübotter, F. Lübeck*, L. Behric*, A. Baumann*, M. Bagatella, D. Marta, I. Hakimi, I. Shenfeld, T. Kleine Buening, C. Guestrin, A. Krause. (*equal second)

**Affiliations**: ETH Zurich, MPI-IS, MIT, Stanford.

**arXiv**: [2601.20802v2](https://arxiv.org/abs/2601.20802) · code: [lasgroup/SDPO](https://github.com/lasgroup/SDPO) · cs.LG, cs.AI.

**Status**: full-paper ingest (main body + figures/tables). Appendix chưa read sâu.

## TL;DR

Paper đề xuất **[[ent_rlrf]]** (Reinforcement Learning with Rich Feedback) như paradigm mới, và **[[ent_sdpo]]** là algorithm instantiate RLRF. Thay vì học từ scalar reward của [[ent_rlvr]], SDPO chuyển tokenized feedback thành **logit-level credit assignment** bằng cách dùng chính policy (conditioned on feedback) làm [[con_self_teacher]]. Distill retrospective predictions của teacher về student qua KL loss.

Vượt [[ent_grpo]] trên cả 3 regime: RLVR standard (science, tool use), RLRF (code với runtime feedback), và **test-time** discovery trên hard questions (§5) — regime này chính là scope của thesis.

## Motivation (§1)

- RLVR đang là standard cho post-training LLM trên code/math, nhưng:
  - Scalar outcome reward → [[con_credit_assignment]] yếu.
  - Nếu cả group rollout cùng fail, GRPO advantage collapse về 0 → learning stall.
  - Distillation từ strong teacher giải quyết sparsity nhưng yêu cầu teacher có sẵn — không khả thi khi muốn raise capability ceiling.
- Observation: nhiều verifiable environment thực ra **expose tokenized feedback** (runtime error, unit test diff, LLM judge) — bị vứt đi khi collapse về scalar reward.
- Paradigm mới **[[ent_rlrf]]**: dùng rich feedback làm signal, không chỉ scalar.
- LLMs đã có sẵn mechanism để dùng feedback: **in-context learning**. Khi được condition trên feedback, cùng model có thể identify mistake. Đây là cơ sở của [[con_self_teacher]].

## Phương pháp SDPO (§2)

### Định nghĩa

Self-teacher `π_θ(· | x, f)`: cùng model nhưng condition thêm feedback `f` ngoài question `x`. Student `π_θ(· | x)` là policy gốc.

### Loss function

```
L_SDPO(θ) = Σ_t KL( π_θ(·|x, y<t) || stopgrad(π_θ(·|x, f, y<t)) )
```

- KL-divergence ở next-token distribution, per-position `t`.
- `stopgrad` chặn gradient flow qua teacher → không cho teacher collapse về student (ignore `f`).
- Ý nghĩa: teacher xác định ở **đâu** và **như thế nào** attempt gốc của student đã sai dựa trên `f`.

### SDPO advantage (§2.1) — khác biệt với GRPO

| | GRPO | SDPO |
|---|---|---|
| Advantage | `A_i,t = r_i − mean{r_j}` (constant across `t`) | `A_i,t(ŷ) = log(π_teacher(ŷ)/π_student(ŷ))` |
| Áp dụng ở token nào | Chỉ token được sample `y_i,t` | Trên top-K next-token candidates tại mỗi position |
| Granularity | Sequence-level | **Logit-level** |

→ SDPO là drop-in extension của RLVR pipelines: giữ code cũ, chỉ swap advantages.

### Reprompt template (Table 2 của paper)

Template self-teacher sử dụng (slot-based):
```
User: <prompt>
Correct solution:
<successful_previous_rollout>     # nếu có sample solution
The following is feedback from your unsuccessful earlier attempt:
<environment_output>               # nếu attempt fail
Correctly solve the original question.
Assistant: <original_response>     # để re-evaluate log-probs
```

Chi tiết ở [[con_reprompt_template]]. **Paper note quan trọng**: "performance is not sensitive to syntactic variations of the reprompting template" — nhưng **feedback type** (output vs own solution vs both) quan trọng.

### Compute & memory (§2.2)

- Overhead chỉ là compute log-probs của teacher — parallelizable, nhanh hơn sequential generation.
- Chi phí thực tế: +5.8% time/step không có code env, +17.1% có code env.
- Memory: naive KL cần full logits của cả 2 → dùng **top-K distillation** (K=100) approximate KL, avoid memory overhead. Xem [[con_top_k_distillation]].

### Stability (§2.3)

1. **Regularized self-teacher**: EMA của student params, hoặc interpolate với initial teacher. Không regularize → teacher collapse.
2. **Jensen-Shannon divergence** thay KL — symmetric, ổn định hơn (theo Agarwal et al. 2024).

## Kết quả

### Regime 1: RLVR setting, không có rich feedback (§3)

- **Trick**: dùng successful rollout trong batch làm "feedback" cho failed rollout cùng question. Không thay đổi environment.
- Tasks: SciKnowEval (Chemistry, Physics, Biology, Materials), ToolAlpaca.
- Models: [[ent_qwen3_8b]], [[ent_olmo3_7b_instruct]].
- Highlight: trên Chemistry với Olmo3-7B-Instruct, SDPO đạt accuracy 5h-GRPO chỉ trong **50 phút → 6× speedup**. Cuối 5h cao hơn GRPO >10 points.
- Response length **ngắn hơn 3×–11×** so với GRPO. GRPO sinh filler như "Hmm", "Wait", circular reasoning; SDPO concise.

→ **Takeaway 1**: SDPO có thể dùng ngay cả trong RLVR env thuần (không có rich feedback), vượt GRPO đáng kể.

### Regime 2: RLRF setting, có rich feedback từ code env (§4)

- Task: [[ent_livecodebench]] v6 (131 questions, Feb–May 2025), LeetCode-style public/private tests.
- Model default: Qwen3-8B.
- Headline (Figure 1): SDPO đạt **48.8% accuracy** vs GRPO **41.2%**, vượt cả Claude Sonnet 4 (40.5%) và Claude Opus 4 (39.7%) trên LCBv6 public leaderboard. Đạt final accuracy của GRPO với **4× fewer generations**.

#### Ablation (§4.2): rich feedback vs dense credit assignment

Paper tách riêng 2 đóng góp:
- **Logit-level SDPO** (full): advantage trên top-100 token tại mỗi position.
- **Token-level SDPO**: chỉ most-likely token.
- **Sequence-level SDPO**: average advantage về scalar per sequence (= dense → sparse, nhưng vẫn dùng rich feedback).

Kết quả: logit > token > sequence > GRPO. Nghĩa là **cả rich feedback và dense credit assignment đều đóng góp**, không phải chỉ một trong hai.

#### Self-teacher bootstrapping (§4.3)

- Teacher **không frozen** — update cùng student (với regularization).
- Teacher accuracy tăng theo thời gian training.
- Student cuối > **initial teacher** — true bootstrapping, không bị cap bởi initial teacher.
- Table 4: trust-region teacher 50.6% > EMA 49.3% > frozen 48.8% > unregularized (diverge).

#### Model scaling (§4.1)

Ability self-teaching là **emergent phenomenon với scale**:
- Qwen3-8B: SDPO >> GRPO.
- Qwen3-0.6B: SDPO ≈ GRPO (marginal).
- Qwen2.5-1.5B: SDPO **underperform** GRPO.
- → SDPO cần in-context learning đủ mạnh.

#### Feedback type ablation (Table 6, §4.6)

| Feedback | Training acc | Teacher acc | Diversity impact |
|---|---|---|---|
| `output` only | 39.9% | 32.5% | OK |
| `own_solution` only | 42.6% | 42.4% | OK |
| **`output + own_solution`** | **48.3%** | **42.5%** | ✅ complementary |
| `y + output + own_solution` | 44.5% | 39.3% | ❌ teacher bias về student, entropy giảm 0.23 |

→ **Include student's original attempt trong teacher template giảm diversity**. Output + sample solution bổ trợ nhau.

#### Catastrophic forgetting (§4.4, Table 5)

- SDPO giữ performance tốt hơn SFT-on-self-teacher trên holdout (IFEval, ArenaHard-v2, MMLU-Pro).
- SDPO hơi kém GRPO về preserve nhưng hơn xa SFT. On-policy > off-policy về mitigating forgetting.

#### SDPO + GRPO hybrid (§4.5)

`A = λ·A_GRPO + (1−λ)·A_SDPO`, λ=0.9. Tốt hơn SDPO trên weak model (Qwen3-0.6B), kém hơn trên strong model.

### Regime 3: Test-time self-distillation trên hard questions (§5) — ⭐ quan trọng cho thesis

- Setting: 1 câu khó, binary reward, model phải discover solution càng nhanh càng tốt.
- Metric: **[[con_discovery_at_k]]** — xác suất solve trong k attempts đầu.
- RLVR không làm gì được trên hard tasks vì cần >=1 success để có signal. SDPO nhận rich feedback mỗi attempt → improve ngay cả trước khi solve lần đầu.
- Mechanism: **compress context vào model weights**. Instead of concat history (như multi-turn), SDPO distill `π(·|x, c)` về `π'(·|x)`. Tránh context window limit.

#### Setup

- [[ent_livecodebench]] v6 hard/very-hard splits:
  - Hard: pass@64 < 0.5 → 19 questions.
  - Very hard: pass@64 < 0.03 → 9 questions.
- Base model Qwen3-8B.
- Baselines: best-of-k, multi-turn reprompting (sliding window 32k).
- SDPO batch size 16 (ablation cho thấy marginal difference).

#### Kết quả

- Very hard: SDPO discover 53.2% vs best-of-k 41.5% vs multi-turn 35.6%. **3× fewer generations** để đạt 22% discovery.
- Hard: SDPO 78% discover@2750, đạt 67% với **2.4× fewer generations** vs baselines.
- Q3 (của very hard set): **chỉ SDPO solve được**, ở attempt 321. Best-of-k và multi-turn không solve trong 2750.
- Initial self-teacher accuracy **<1%** trên almost all hard questions — không solve được ngay cả 1-shot, **nhưng credit assignment vẫn đủ để iterate và cuối cùng solve**. Đây là insight quan trọng.

→ **Takeaway 3**: RLRF via self-distillation mở đường để học ngay cả khi chưa có success nào.

## Liên hệ trực tiếp tới thesis

Trong **§7 Future Work**, paper list 4 hướng — hướng thứ 4 **chính là thesis của bạn**:

> "**Behavioral differences in reasoning.** We observed that SDPO induces qualitatively different reasoning patterns than GRPO, notably avoiding the latter's tendency toward verbosity and superficial reasoning. Future work should systematically study how individual aspects, such as **the reprompt template**, influence behavior."

- **RQ1** (template taxonomy) map vào đây gần như nguyên văn.
- **RQ2** (suppression transfer to test-time code) xây trên §5 (test-time SDPO) × Kim et al. 2026.
- **RQ3** (compute-to-correct Pareto) xây trên §5 discovery@k metric.

## Open questions (từ thesis perspective)

- Template variations paper claim "not sensitive syntactically" — nhưng chưa test systematically. [[con_reprompt_template]] taxonomy của thesis sẽ đào sâu.
- §5 test-time SDPO không measure uncertainty language explicitly → thesis RQ2 fill gap đó.
- [[con_discovery_at_k]] là compute-based; thesis mở rộng thành [[con_ctc_metric]] (compute-to-correct).
- Feedback type ablation (Table 6) dừng ở combining ON/OFF — thesis có thể deep hơn về **cấu trúc template**.
- Self-teacher regularization (trust-region vs EMA) — có tác động gì ở test-time không? Paper chỉ test train-time.

## Links

- Entities: [[ent_sdpo]] · [[ent_rlvr]] · [[ent_rlrf]] · [[ent_grpo]] · [[ent_livecodebench]] · [[ent_qwen3_8b]] · [[ent_olmo3_7b_instruct]]
- Concepts: [[con_rich_feedback]] · [[con_self_teacher]] · [[con_credit_assignment]] · [[con_reprompt_template]] · [[con_test_time_self_distillation]] · [[con_discovery_at_k]] · [[con_top_k_distillation]] · [[con_teacher_regularization]]
- Thesis proposal: [[../../SDPO 2026-04-11]]
