---
type: source
created: 2026-05-19
updated: 2026-05-19
tags: [video, discussion, primary-source, hubotter, shenfeld, sdpo, sdft, transcript]
sources: [src_youtube_hubotter_shenfeld_discussion]
cite: "Hübotter & Shenfeld discussion, 2026 (YouTube)"
url: https://www.youtube.com/watch?v=OgEGV7apEzI
raw: "C:/Users/Maidanng/Downloads/[English (auto-generated)] Why Self-Distillation Is Taking Over LLM Post-Training (w the Researchers.txt"
depth: full-transcript-grep
aliases: [YouTube SDPO discussion, Hübotter Shenfeld panel]
---

# YouTube Discussion — *Why Self-Distillation Is Taking Over LLM Post-Training (w/ the Researchers)*

Buổi panel với **Jonas Hübotter** ([[src_hubotter2026_self_distillation]]) và **Idan Shenfeld** ([[src_shenfeld2026_sdft]]) — primary source quý vì tác giả nói thẳng motivation, mechanism, limitation mà paper không viết.

**Format**: discussion + slide presentation, ~2400 lines auto-generated transcript.

**Status**: full transcript grep'd, key quotes extracted verbatim. Source file = English auto-caption (tên riêng có thể bị mangle nhẹ).

## TL;DR — Tại sao đây là source quan trọng

1. Hübotter mô tả CHÍNH XÁC LCBv6 discovery@K experiment làm nền RQ1+RQ3 của thesis.
2. Hübotter **tự thừa nhận** SDPO dùng ít hmm/wait — frame **positive** (efficiency) thay vì negative (suppression như Kim et al.) → wedge cho RQ2.
3. Shenfeld giải thích cơ chế "minimum change" của SDFT bằng lời mình.
4. Confirm HuggingFace TRL đã merge SDFT + SDPO (2026-05) → drop verl path.
5. Confirm OpenClaw RL có collab official với group.
6. Limitation tự thừa nhận: model nhỏ → self-teacher yếu.

## Verbatim quotes theo theme

### Theme 1: Test-time framing được tác giả emphasize [line 215-256]

> *"when you learn at test time, it's very important that you are very **efficient in turning your data into gradient updates**, right? ... we are **compute bound**, we have to make the most out of the signal that we get."*
> — Hübotter

→ Direct validation cho [[con_ctc_metric]] (RQ3): efficiency turning data → gradient update.

### Theme 2: Coding origin story [line 290-300]

> *"motivation was actually yeah for me coming from pretty much that angle. Because we were working on **coding** at the time and it just seemed obvious that ... when I was trying to make ChatGPT code, it was like this back and forth — ChatGPT generating some code, I'm running it, I'm pasting back the error."*
> — Hübotter

→ Code generation là **original motivation**, không phải afterthought. Strengthen motivation paragraph của thesis.

### Theme 3: Implicit bias toward minimum change [line 1238-1253]

> *"in a lot of these problems, there's not only one policy that can get to, let's say, 90% success on the new task. It's a whole set of them. And which one you converge to will affect how much forgetting you'll have. And RL ... have a tendency to converge to one that are as close as possible to the original policy, **even without any explicit KL regularization**. So, this kind of implicit bias towards minimum change keep the models from forgetting more and more."*
> — Shenfeld

Generality claim [line 1233-1235]:
> *"not only true for LLMs. We tried with robotic foundation models and even with three-layer MLP on MNIST."*

→ Foundation cho cơ chế anti-forgetting trong [[src_shenfeld2026_sdft]]. Xem thêm thesis impact ở page đó.

### Theme 4: ⭐ Wedge cho RQ2 — Hübotter tự thừa nhận giảm hmm/wait [line 1759-1820]

> *"it uses rather less of these **typical reasoning tokens such as hmm and wait** etc. which GRPO tends to produce."*
> — Hübotter

Cơ chế ông đưa ra:
> *"hindsight policy being able in a more informed state being able to tell the policy okay, here this was like a **circular reasoning loop** that wasn't unnecessary."*

Ông frame **positive**: efficiency, shorter traces, no circular reasoning. **Kim et al. 2026 frame negative**: suppression of epistemic uncertainty, AIME24 drop 40%.

→ **Wedge hoàn hảo cho RQ2**: thesis có thể position là *"first test-time CODE evidence trên debate này"* — 2 camps disagree on whether reducing hmm/wait is good or bad. Xem [[syn_kim2026_thesis_impact]] section "Wedge angle".

### Theme 5: ⭐ Direct validation cho RQ1 + RQ3 setup [line 1941-2002]

> *"We took problems from like coding tasks from **Life Code Bench** that the model was not able to solve across a lot of attempts. And then what we were interested in is how quickly would the model **discover the solution** to that task. And how we quantified that was through this **discovery at K metric**. ... These were tasks where the **pass at 64 was less than 3%**, meaning that if you were to 100 times, each time sample 64 solutions, only in three of these 100 cases the model would actually have sampled any correct solution."*
> — Hübotter

Baseline comparison:
> *"the simplest baseline ... is what's typically called **best of K** ... And then another baseline, which is just the **multi-turn baseline**, which keeps all of the conversation history with environment in context until it runs out of context and then has a first-in-first-out queue."*

Main claim:
> *"self-distillation can really learn to **solve hard tasks even before it ever solved the task**, right? Just by the teacher providing directionally accurate feedback that points towards how to solve the task."*

→ Validation cho thesis: setup LCBv6 hard + discovery@K là correct, baseline phải gồm **cả 2** (best-of-K + multi-turn), không phải chỉ 1.

### Theme 6: ⭐ HuggingFace TRL merge (game-changer) [line 2055-2064]

> *"both **SDFT and SDPO**, the two versions of the self-distillation algorithms, are available with TRL. Um, **in the last week, Hugging Face people merged** ... in their code base. So, you know, it's make it much easier for everyone to play with these ideas."*
> — Shenfeld / Hübotter

→ Thesis có thể **drop verl entirely**, dùng `trl + peft + LoRA` cho Phase 3. Tiết kiệm 1-2 tuần implementation. Action: WebFetch TRL repo verify API.

### Theme 7: OpenClaw RL endorsement [line 2028-2044]

> *"a library called **Open Claw RL**, which is running on-policy self-distillation under the hood, but is **extending this way beyond just coding agents**, but putting this into Open Claw. So, having your agent interact with whatever tools you give it access to, and then having the agent actually learn over time and in a synchronous fashion."*
> — Hübotter

→ Confirm OpenClaw RL không phải fan-project mà có collab với Hübotter group. Repo: [Gen-Verse/OpenClaw-RL](https://github.com/Gen-Verse/OpenClaw-RL), submodule `openclaw-opd`.

### Theme 8: Self-teacher quality scales với model size [line 1827-1832]

> *"as you scale models you get better in context learners and those translate to **better self teachers**. So better teacher signals that then lead to better student models as we train them with on-policy self-distillation."*
> — Hübotter

→ **Limitation thesis cần ghi**: Qwen3-8B teacher signal có thể yếu hơn Qwen3-32B/72B. Có thể không reproduce được 2.4× speedup của paper. Plan B framing nên có sẵn.

### Theme 9: Continual code Twitter prototype [line 2003-2027]

> *"someone on Twitter had this idea of **continual code**. So, like cloud code, but running a local model, and that model is actually learning as you go. It's not just saving things in context or scaffolding. It's actually **updating the model parameters**. ... here it's it's thinking, and then he will reject the edit, and he will say that he wants the helper to be minimal, and ... the model would actually do a training step."*
> — Hübotter

→ Related work mention cho thesis intro: TTT-SDPO regime đã có prototype real-world ngoài academia.

### Theme 10: Sample efficiency future direction [line 2079-2120]

> *"on the opposite side is about **sample efficiency**, where you don't have scale. You just have one user providing a few points of feedback. And the question is how can you learn from that? ... currently we're looking into ways to make it the supervision even denser, to make the update such that that **even with a single point of environment feedback**, you can change the model quite a lot without forgetting."*
> — Shenfeld

→ Đây gần đúng TTT regime của thesis (1 question, vài turn feedback). Position thesis trong open research direction này.

## Cấu trúc thảo luận (timestamp xấp xỉ)

| Phase | Lines | Content |
|---|---|---|
| Intro | 1-100 | Host giới thiệu 2 papers (SDPO, SDFT), Jan 2026 release |
| Bio & motivation | 200-400 | Hübotter test-time efficiency lineage; Shenfeld RL's Razor |
| SDPO presentation | 700-1100 | Loss formulation, teacher-student, KL, why on-policy |
| Continual learning Q&A | 1100-1500 | Implicit bias, RL's Razor, SDFT sequential experiments |
| Trade-offs & GRPO comparison | 1700-1900 | hmm/wait suppression, circular reasoning, shorter traces |
| Test-time SDPO & roadmap | 1900-2200 | LCBv6 discovery@K, OpenClaw, TRL, future directions |

## Thesis impact mapping

| RQ | Quote tham chiếu | Action |
|---|---|---|
| RQ1 | Theme 5 (discovery@K + dual baseline setup) | Confirm thesis baseline phải gồm cả best-of-K + multi-turn |
| RQ2 | Theme 4 (Hübotter tự thừa nhận giảm hmm/wait) | Wedge angle: thesis = first test-time code evidence trên debate |
| RQ3 | Theme 1 (test-time = compute bound) | Validation cho CTC metric framing |
| Implementation | Theme 6 (TRL merge) | Drop verl, dùng TRL+PEFT |
| Limitation | Theme 8 (self-teacher scaling) | Acknowledge Qwen3-8B teacher signal có thể yếu |
| Motivation | Theme 2 (coding origin) | Strengthen intro paragraph |
| Related work | Theme 7+9 (OpenClaw, continual code) | Cite trong related work |

## Open questions sau khi xem

- TRL API cho SDPO trông thế nào? Có support test-time loop không? → action: WebFetch TRL repo.
- OpenClaw-RL `openclaw-opd` submodule có code pattern reusable cho thesis loop không? → action: explore repo nếu có thời gian.
- Paper số 3 của Hübotter ("three papers ... Edan and Thomas and I have been leading") là gì? Có thể là RL's Razor (Shenfeld 2025) — verify.

## Caveat

- Auto-caption tiếng Anh: tên riêng đôi khi sai (Idan → "Edan", "Olmo" có thể được transcribe thành "almo" v.v.).
- Vài quote là **rephrased dù dùng dấu quote** vì cắt từ transcript — line number cho phép verify nhanh trong file gốc.
- Không phải mọi điều tác giả nói = endorsed bởi paper. Cite cẩn thận trong thesis: khi cite từ video, ghi rõ "in YouTube discussion" thay vì pretend cite từ paper.

## Links

- Co-papers: [[src_hubotter2026_self_distillation]] · [[src_shenfeld2026_sdft]]
- Critique: [[src_kim2026_why_self_distillation_degrades]]
- Synthesis: [[syn_kim2026_thesis_impact]] (section "Wedge angle RQ2")
- Concepts: [[con_epistemic_verbalization]] · [[con_uncertainty_suppression]] · [[con_test_time_self_distillation]] · [[con_discovery_at_k]] · [[con_reprompt_template]]
- Entities: [[ent_sdpo]] · [[ent_livecodebench]] · [[ent_qwen3_8b]]
