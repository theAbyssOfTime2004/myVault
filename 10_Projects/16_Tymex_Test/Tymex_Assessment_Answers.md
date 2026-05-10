---
title: Tymex Assessment — MCQ Answers
date: 2026-05-10
tags: [interview, assessment, tymex]
---

# Tymex Assessment — Phần Trắc Nghiệm Kiến Thức

> Tổng cộng **32 câu**: 22 câu trắc nghiệm (knowledge/situational) + 10 câu code (Q5, Q7, Q8, Q11, Q14, Q15, Q17, Q23, Q25, Q26).
> Note này chỉ làm **22 câu trắc nghiệm**. Phần code để sau.

## Bảng tổng hợp đáp án

| Q | Đáp án | Chủ đề chính |
|---|--------|--------------|
| 1 | A | Root-cause latency: instrument & profile từng stage |
| 2 | C | Align với dev + document cho PO, không escalate vội |
| 3 | B | Self-directed: prototype + share ngắn gọn với team |
| 4 | A | Align với teammate, đề xuất plan tích hợp |
| 6 | B | Precision-recall + cost-sensitive eval + shadow deploy |
| 9 | D | Hypothesis → controlled experiment trong staging |
| 10 | A | Prototype trên subset + share để team đánh giá |
| 12 | C | Build prototype nhỏ, test, share feedback |
| 13 | D | Controlled experiment để isolate sources of instability |
| 16 | C | Bỏ sót trade-offs về maintainability/complexity |
| 18 | A | Recall + FP trade-offs + threshold tuning trước deploy |
| 19 | A | Chọn Model Y (recall rare fraud + explainability) |
| 20 | A | Validation tốt vẫn fail nếu real-world diverges |
| 21 | A | Pilot nhỏ song song process cũ + feedback team |
| 22 | A | Đồng thuận ngầm: cautious limited rollout (experiment) |
| 24 | A | Phân tích precision/recall theo segment + threshold |
| 27 | D | Limited pilot + monitor + cross-functional feedback |
| 28 | A | Prototype AI nhỏ ngoài giờ, share để spark discussion |
| 29 | A | Prototype độc lập + chia sẻ findings với team |
| 30 | A | Inform cả dev lẫn PO + sync với data science team |
| 31 | C | Liên kết trade-offs với hệ thống hiện tại của công ty |
| 32 | A | Đánh giá phản biện + kết nối với business context |

---

## Chi tiết từng câu

### Q1 — Latency tăng sau update pipeline AI inference
**Đáp án: A** — Instrument and profile each stage with fine-grained latency/resource metrics, compare against historical baselines, identify bottlenecks before deciding optimization or architectural changes.
**Lý do:** Senior engineers đang debate; đề bài nhấn mạnh "sound technical reasoning". Phương án A là evidence-based, có hệ thống. B (scale up trước) và C (rewrite stage) là tối ưu mù; D (redesign cả pipeline) đi xa quá khi chưa biết bottleneck.

### Q2 — AI recommendation, dev không trả lời clarification
**Đáp án: C** — Initiate quick alignment với dev + document agreed approach + share với PO trong khi tiếp tục progress.
**Lý do:** Cân bằng tiến độ (sprint deadline) với technical correctness. A (escalate ngay) phá hỏng quan hệ; B (proceed mù) gây lỗi; D (pause hẳn) làm trễ sprint.

### Q3 — Startup văn hóa self-directed research
**Đáp án: B** — Independently explore, build small prototype, share concise summary.
**Lý do:** Đúng văn hóa "learning agility, self-directed, proactive exploration".

### Q4 — Teammate xây giải pháp tương tự, không tương thích
**Đáp án: A** — Initiate focused discussion, compare approaches, propose short-term integration plan.
**Lý do:** Hợp tác + cân bằng deadline, tránh duplicate work.

### Q6 — Fintech fraud detection 98% acc nhưng FP cao
**Đáp án: B** — Precision-recall + cost-sensitive eval + threshold tuning + shadow deployment.
**Lý do:** Class imbalance trong fraud → accuracy không đủ. Shadow deployment cho phép quan sát real-world trước full rollout.

### Q9 — API latency spikes, structured experimentation culture
**Đáp án: D** — Formulate hypotheses, design controlled experiments in staging, isolate variables, document findings systematically.
**Lý do:** Đề bài nhấn mạnh "structured experimentation" và staging env có sẵn.

### Q10 — Newer algorithm vs refining existing model, tight deadline
**Đáp án: A** — Quickly prototype new algorithm on subset, document, share with team.
**Lý do:** Văn hóa AI-first, openness to fail. Không bỏ qua cơ hội nhưng cũng không gambling toàn bộ project.

### Q12 — Identified potential improvement, manager bận, không deadline
**Đáp án: C** — Build simple prototype, test on small dataset, document, share.
**Lý do:** Văn hóa "perfection less valuable than iteration speed".

### Q13 — Model mới unstable trong prod, team tranh cãi nguyên nhân
**Đáp án: D** — Controlled experiments to isolate sources of instability across segmented data, instrument prediction variance/input sensitivity.
**Lý do:** Cần evidence-based root cause, không patch (A), không tune mù (B), không rollback hèn (C).

### Q16 — Documentation review về DB scaling
**Đáp án: C** — Fails to incorporate critical trade-offs related to maintainability/complexity, focusing only on performance.
**Lý do:** Senior engineer chỉ ra "summary overlooked nuances" — nuances chính là trade-offs về maintainability đã bị skip.

### Q18 — Vendor AI fraud, recall 60%, FP 8%
**Đáp án: A** — Further evaluation focusing on recall + FP trade-offs, threshold tuning, cost-sensitive metrics aligned with fraud risk.
**Lý do:** Fintech compliance + customer impact đòi hỏi metric phù hợp với chi phí thực tế.

### Q19 — Model X (98% acc, edge-case yếu) vs Model Y (92% acc, recall rare fraud, explainable)
**Đáp án: A** — Recommend Model Y vì recall rare fraud và explainability align với regulatory requirements và high cost of missed fraud.
**Lý do:** Banking regulated → audit + missed fraud cost cao → Model Y phù hợp dù accuracy thấp hơn.

### Q20 — Deployment readiness document
**Đáp án: A** — Model có thể strong validation nhưng poor deployment nếu real-world diverges from validation assumptions.
**Lý do:** Đúng tinh thần document — validation ≠ deployment readiness.

### Q21 — AI-driven startup, manual script vs experimental AI tool
**Đáp án: A** — Propose small-scale pilot using AI tool alongside existing process, outline benefits/risks, seek feedback.
**Lý do:** AI-first culture nhưng tool còn experimental → pilot là cân bằng tốt.

### Q22 — Cross-functional thread về deploy recommendation model
**Đáp án: A** — Implicitly aligning around cautious, limited rollout framed as experiment.
**Lý do:** Tất cả đều có quan điểm thận trọng (PM lo small beta group, engineer lo reliability, DS lo drift). Không ai oppose hẳn → consensus ngầm là pilot/experiment.

### Q24 — Vendor fraud API, FP cao đặc biệt với new users
**Đáp án: A** — Analyze precision/recall separately, FP rates by segment, adjust thresholds or request retraining.
**Lý do:** Segment-level analysis (new users) là đúng kỹ thuật.

### Q27 — Internal tool prototype, edge cases inconsistent
**Đáp án: D** — Limited pilot release to small informed user group + monitoring + cross-functional feedback.
**Lý do:** Cân bằng "rapid experimentation" + "responsible deployment" + "collaborative decision-making".

### Q28 — Rule-based system vs AI approach, tight deadlines
**Đáp án: A** — Quickly build small prototype using AI in own time, share results to spark discussion.
**Lý do:** Không cản trở deadline (làm own time), nhưng vẫn proactive theo culture.

### Q29 — New open-source AI framework
**Đáp án: A** — Independently explore, build small prototype, share findings + recommendations.
**Lý do:** Văn hóa "self-directed research" và leadership đã expressed interest.

### Q30 — Sprint, model output format đổi, dev chưa biết, PO không biết
**Đáp án: A** — Proactively inform both devs and PO, suggest quick sync với data science team.
**Lý do:** Communication chủ động, cross-functional alignment trước sprint review.

### Q31 — Documentation về DB scalability, team yêu cầu kết nối với hệ thống công ty
**Đáp án: C** — Incorporate specific examples showing how trade-offs apply to company's current systems.
**Lý do:** Chính xác feedback của team là "connect theoretical insights to company's existing infrastructure constraints".

### Q32 — Intern đánh giá paper về caching strategy
**Đáp án: A** — Intern critically evaluated research and communicated both benefits and limitations in practical business context.
**Lý do:** Intern highlighted assumptions, recommended limited experiment, documented risks → critical evaluation đúng nghĩa.

---

## Pattern chung của bộ đề (rút ra để dùng cho phần code và các bài tương tự)

1. **Văn hóa AI-first + experimentation:** luôn chọn phương án **prototype nhỏ + share team** thay vì (a) chờ approval, (b) bỏ qua, (c) thay thế độc lập không hỏi ai, hay (d) chờ deadline xong.
2. **Root cause / debugging:** luôn chọn **instrument → hypothesis → controlled experiment → document**, KHÔNG patch (ensemble, scale up, hyperparam tuning) trước khi hiểu nguyên nhân.
3. **Fintech / regulated domain:** luôn ưu tiên **precision-recall theo segment + cost-sensitive metric + threshold tuning + shadow deployment**, KHÔNG dựa vào accuracy tổng.
4. **Deployment readiness:** validation tốt ≠ production-ready; phải account for drift + real-world distribution.
5. **Communication / teamwork:** **proactive sync + document + cross-functional feedback** thắng mọi phương án "đợi", "escalate ngay", hoặc "tự quyết".
6. **Documentation review:** giá trị nằm ở **trade-offs cụ thể + connect to company context**, không phải tóm tắt theo một chiều.

## TODO tiếp theo
- [ ] Phần code: Q5 (select_model), Q7 (clean_predictions), Q8 (get_stable_models), Q11 (calculate_model_costs), Q14 (evaluate_model), Q15 (analyze_model_logs), Q17 (evaluate_model precision/recall/macro_f1), Q23 (evaluate_model logits→accuracy), Q25 (aggregate_tokens), Q26 (compute_avg_response_time).
