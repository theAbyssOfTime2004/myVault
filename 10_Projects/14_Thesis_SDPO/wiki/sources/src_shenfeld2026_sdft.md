---
type: source
created: 2026-05-19
updated: 2026-05-19
tags: [paper, self-distillation, continual-learning, sdft, sister-paper]
sources: [src_shenfeld2026_sdft]
cite: "Shenfeld et al., 2026"
arxiv: "2601.19897"
url: https://arxiv.org/abs/2601.19897
depth: abstract+transcript-explanation
aliases: [SDFT paper, Shenfeld 2026 continual learning]
---

# Shenfeld et al. 2026 — Self-Distillation Enables Continual Learning

**Tác giả**: Idan Shenfeld, Mehul Damani, **Jonas Hübotter**, Pulkit Agrawal.

**Affiliations**: MIT (Shenfeld, Damani, Agrawal) + ETH Zurich (Hübotter).

**arXiv**: [2601.19897](https://arxiv.org/abs/2601.19897) · TRL integration merged 2026-05.

**Status**: abstract + author-narrated mechanism từ [[src_youtube_hubotter_shenfeld_discussion]] (PDF full ingest pending).

## Quan hệ với SDPO

**Cùng research line, khác mục tiêu** — Hübotter là co-author cả 2 paper:

| Paper | Algorithm | Replace | Học từ data | Regime focus |
|---|---|---|---|---|
| [[src_hubotter2026_self_distillation]] | [[ent_sdpo]] | [[ent_rlvr]] | feedback (error trace, judge) | train-time + test-time |
| **Shenfeld 2026 (paper này)** | **SDFT** | SFT | expert demonstrations | continual / multi-task |
| Shenfeld 2025 RL's Razor | — (theoretical) | — | — | on-policy forgets less |

Cùng cơ chế cốt lõi: model conditioned on extra context = self-teacher. Khác signal source.

## TL;DR

Paper đề xuất **SDFT (Self-Distillation Fine-Tuning)** thay thế SFT khi học từ demonstrations. Claim chính: SDFT preserve prior capabilities qua **implicit bias toward minimum change** của on-policy method — không cần thêm thuật toán anti-forgetting nào. Validate trên LLM (tool use → scientific QA → medical QA), robotic foundation models, và 3-layer MLP trên MNIST.

## Abstract (verbatim)

> *"Continual learning, enabling models to acquire new skills and knowledge without degrading existing capabilities, remains a fundamental challenge for foundation models. While on-policy reinforcement learning can reduce forgetting, it requires explicit reward functions that are often unavailable. Learning from expert demonstrations, the primary alternative, is dominated by supervised fine-tuning (SFT), which is inherently off-policy. We introduce Self-Distillation Fine-Tuning (SDFT), a simple method that enables on-policy learning directly from demonstrations. SDFT leverages in-context learning by using a demonstration-conditioned model as its own teacher, generating on-policy training signals that preserve prior capabilities while acquiring new skills. Across skill learning and knowledge acquisition tasks, SDFT consistently outperforms SFT, achieving higher new-task accuracy while substantially reducing catastrophic forgetting. In sequential learning experiments, SDFT enables a single model to accumulate multiple skills over time without performance regression, establishing on-policy distillation as a practical path to continual learning from demonstrations."*

## Cơ chế chính: implicit bias toward minimum change

Shenfeld giải thích trong [[src_youtube_hubotter_shenfeld_discussion]] (line 1238-1253 verbatim):

> *"in a lot of these problems, there's not only one policy that can get to, let's say, 90% success on the new task. It's a whole set of them. And which one you converge to will affect how much forgetting you'll have. And RL ... have a tendency to converge to one that are as close as possible to the original policy, **even without any explicit KL regularization**. So, this kind of implicit bias towards minimum change keep the models from forgetting more and more."*

### 2 trụ argument

**Trụ A — On-policy robustness (DAgger lineage)** [transcript line 1161-1211]
- Off-policy (SFT teacher-forcing): student không phải tạo trajectory → train-test distribution shift. Khi inference student deviate → vào region không có training coverage → fail.
- On-policy: student rollout chính mình → trajectory tự nhiên match distribution → robust.
- Ví dụ minh họa: autonomous driving — expert demo chỉ cover lane giữa đường; SFT student không biết làm gì khi lệch gần wall.

**Trụ B — Minimum-change implicit bias (RL's Razor lineage)**
- Tồn tại MANIFOLD policy đạt 90% task mới.
- SFT có thể hội tụ về điểm bất kỳ → có thể xa π_prior → forget mạnh.
- On-policy gradient bias về điểm gần π_prior nhất → forget ít.
- Quan trọng: bias này TỰ NHIÊN, không cần KL regularization explicit.

### Generality claim [transcript line 1233-1235]

> *"not only true for LLMs. We tried with **robotic foundation models** and even with **three-layer MLP on MNIST**."*

→ Họ position đây là implicit-bias của on-policy gradient, **architecture-agnostic**.

## Setup thực nghiệm

### Single-task forgetting measurement [transcript line 1216-1228]
- Train tool use, sau đó measure degradation trên 8 standard benchmark: IFEval, TruthfulQA, MMLU, ...
- SFT: degrade các benchmark cũ.
- SDFT / RL: hầu như không degrade.

### Sequential continual learning [transcript line 1308-1326]
- Sequence: tool use → scientific QA → medical QA.
- SDFT: **aggregate skill** — sau mỗi task chuyển, slight degradation nhưng giữ được.
- SFT: chỉ retain task cuối, các task trước drop mạnh.

### Quote chính cho continual claim

> *"On-policy self-distillation is actually able to do it. Every time you change from one train data set to another, you have a slight degradation of performance, but overall you are able to retain and aggregate."*

## Limitation tự thừa nhận [transcript line 1347-1353]

> *"We still need to push it to scale to see where things break. That's kind of the downside of doing academic research where at some point you're saying, 'Okay, I ran out of compute.'"*

→ Chưa test với task sequence rất dài hoặc domain shift mạnh. Robustness của implicit-bias claim trong regime dài hạn còn open.

## Connection sang [[ent_sdpo]] mechanism

Cả SDFT và SDPO dùng cùng cơ chế core: **teacher = model + extra context** (`f` hoặc demo `d`); student = model không có extra context; minimize KL distill teacher → student; update student weights only.

Khác biệt:
- SDFT: `c = demonstration` (expert sequence).
- SDPO: `c = feedback` (error trace, runtime output, judge).

→ Cùng paradigm "on-policy self-distillation"; tách ra vì application domain khác.

## Thesis impact

### Forgetting argument relevant cho TTT regime — nhưng KHÔNG trực tiếp

Forgetting setup của Shenfeld = **multi-task / cross-session**. TTT-SDPO của thesis = **single-question / within-session**. Hai chế độ khác nhau:

| Regime | Forgetting risk | Implicit-bias argument áp dụng? |
|---|---|---|
| SDFT multi-task | mất knowledge task cũ khi học task mới | ✅ paper validate trực tiếp |
| TTT-SDPO within-question (thesis) | turn n's update phá ability từ turn 1..n-1 cùng câu | gián tiếp, chưa validate |
| TTT-SDPO across-question | sau khi solve câu A, model degrade cho câu B | bypass được nếu reset weight per question |

**Recommendation cho thesis**:
1. Reset model về base weight giữa các câu (mỗi question = independent TTT session). Bypass cross-question forgetting concern.
2. Nếu không reset → thêm cross-question generalization test như experiment phụ (đo trên 1 câu holdout sau khi TTT trên 1 câu khác).

### RQ2 angle — "minimum change" như counter-argument vs Kim

Nếu implicit bias kéo update về policy gần π_prior nhất → epistemic token suppression CHỈ xảy ra mạnh khi hmm/wait tokens là **systematically off-policy** trong feedback-conditioned distribution.

→ Hypothesis testable trong thesis: measure log-prob của 10 epistemic tokens trong `π_student` vs `π_teacher` trước khi update. Nếu gap lớn → minimum-change vẫn cho phép suppression. Nếu gap nhỏ → minimum-change protect epistemic baseline.

### Limitation cho thesis cần ghi

- Shenfeld chưa scale up nhiều task → claim "no catastrophic forgetting" có giới hạn empirical.
- TTT regime của thesis = extreme narrow (|D|=1 theo [[con_task_coverage]] framework của Kim) → implicit-bias claim có thể không transfer hoàn toàn vì regime quá khác.

## TRL integration (2026-05)

Theo [[src_youtube_hubotter_shenfeld_discussion]] (line 2055-2064):

> *"both SDFT and SDPO ... are available with TRL. **In the last week, Hugging Face people merged** ... in their code base."*

→ Implication cho thesis: có thể **drop verl path**, dùng `trl + peft + LoRA` cho Qwen3-8B trên Modal A100. Phase 3 implementation đơn giản hẳn.

## Related work (paper cite)

- [[src_hubotter2026_self_distillation]] — sister paper, RLRF angle.
- Shenfeld et al. 2025 — *RL's Razor: Why online RL forgets less*. Origin của minimum-change argument.
- [[src_kim2026_why_self_distillation_degrades]] — critique paper, không cite trực tiếp trong abstract nhưng cited trong related work.
- Snell et al. 2022 — original self-distillation / learning by distilling context.

## Open questions cho thesis

- **PDF full ingest pending** — hiện chỉ ingest abstract + author transcript. Cần read §3-4 chi tiết để verify "minimum change" có formal statement không (e.g., bound, theorem).
- Paper claim "no catastrophic forgetting" trên scale có giới hạn — robustness ở task sequence > 5 chưa test.
- Cross-domain transfer (math demo → code policy) chưa được Shenfeld test → thesis component B (math-SDPO Qwen3-8B → code) là valid contribution nếu compute cho phép.

## Links

- Sister: [[src_hubotter2026_self_distillation]] · [[src_kim2026_why_self_distillation_degrades]]
- Discussion source: [[src_youtube_hubotter_shenfeld_discussion]]
- Concepts: [[con_self_teacher]] · [[con_credit_assignment]] · [[con_task_coverage]]
- Entity: [[ent_sdpo]] (sister algorithm)
