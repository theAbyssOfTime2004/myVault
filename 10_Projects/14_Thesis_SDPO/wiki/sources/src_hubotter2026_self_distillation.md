---
type: source
created: 2026-04-22
updated: 2026-04-22
tags: [sdpo, rl, self-distillation, rlvr, code, origin-paper]
cite: "Hübotter et al., 2026"
arxiv: "2601.20802"
url: https://arxiv.org/abs/2601.20802
raw: raw/hubotter2026_sdpo.md
depth: abstract-only
---

# Hübotter et al. 2026 — Reinforcement Learning via Self-Distillation

**Tác giả**: J. Hübotter, F. Lübeck, L. Behric, A. Baumann, M. Bagatella, D. Marta, I. Hakimi, I. Shenfeld, T. Kleine Buening, C. Guestrin, A. Krause.

**arXiv**: [2601.20802](https://arxiv.org/abs/2601.20802) · submitted 2026-01-28 · revised 2026-02-16 · cs.LG, cs.AI.

**Status**: abstract-only ingest. Chưa đọc full PDF — cần tải về [[raw/hubotter2026_sdpo]] rồi re-ingest để deepen method/results.

## TL;DR

[[ent_rlvr]] (scalar outcome reward) có signal quá sparse → [[con_credit_assignment]] yếu. SDPO densify signal bằng cách dùng chính model conditioned on feedback làm *internal teacher*, rồi distill retrospective predictions của nó ngược về policy gốc. Không cần external teacher hay reward model. Báo cáo **3× efficiency** so với best-of-k trên hard tasks.

## Problem setting

- Baseline: [[ent_rlvr]] — tiêu chuẩn hiện tại để post-train LLM trên code/math.
- Gap: reward chỉ ở outcome-level → signal sparse → [[con_credit_assignment]] kém → sample-inefficient khi bài toán khó.

## Key contributions

1. Formalize hoá **"RL with rich feedback"** như một problem setting mới, vượt ra khỏi scalar reward — xem [[con_rich_feedback]].
2. Đề xuất phương pháp **[[ent_sdpo]]**: model conditioned on textual feedback đóng vai trò [[con_self_teacher]]; predictions của nó được distill về policy gốc.
3. Thực nghiệm vượt RLVR baselines trên: scientific reasoning, tool use, competitive programming ([[ent_livecodebench]]).
4. **3× compute efficiency** so với best-of-k sampling trên hard tasks.

## Method (high-level, chờ PDF)

SDPO coi `π(· | state, feedback)` là internal teacher. Textual feedback condition model để nó sinh ra next-token predictions tốt hơn, sau đó distill về `π(· | state)` qua self-distillation. Signal trở thành dense/per-token thay vì sparse/per-episode.

## Results (chờ PDF cho con số cụ thể)

- Scientific reasoning: ✅
- Tool use: ✅
- Competitive programming trên [[ent_livecodebench]]: ✅
- 3× compute efficiency vs best-of-k ở hard-split.

## Liên quan tới thesis

- Đây là **origin paper** của SDPO — mọi thứ thesis nghiên cứu đều dựa trên method này.
- **RQ1** của thesis xoáy vào biến thể **test-time** (reprompt template ablation), trong khi paper này chỉ cover **train-time** setup.
- **RQ2** hỏi liệu hiện tượng uncertainty-suppression mà Kim et al. 2026 phát hiện (trên math) có xuất hiện ở test-time SDPO trên code không — paper này không đề cập trực tiếp.

## Open questions

- Distillation objective chính xác là gì? KL divergence tới teacher posterior? Token-level cross-entropy? Temperature setting? — cần đọc PDF.
- Feedback format sensitivity — map trực tiếp vào [[con_reprompt_template]] taxonomy của thesis.
- SDPO có suppress [[con_epistemic_verbalization]] không? Paper không report; Kim et al. 2026 gợi ý là có (ít nhất trên math domain).

## Links

- Entities: [[ent_sdpo]] · [[ent_rlvr]] · [[ent_livecodebench]]
- Concepts: [[con_rich_feedback]] · [[con_self_teacher]] · [[con_credit_assignment]]
- Thesis proposal: [[../../SDPO 2026-04-11]]
