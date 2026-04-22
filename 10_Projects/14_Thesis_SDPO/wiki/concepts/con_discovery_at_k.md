---
type: concept
created: 2026-04-22
updated: 2026-04-22
tags: [metric, test-time, evaluation]
sources: [src_hubotter2026_self_distillation]
aliases: [discovery@k, discovery time]
---

# discovery@k

Metric đo hiệu quả tìm solution trong binary-reward test-time setting. Định nghĩa formal ở [[src_hubotter2026_self_distillation]] (Definition 5.1, §5).

## Định nghĩa

- **Discovery time**: `T = min{k : r(y_k | x) = 1}` — số attempt nhỏ nhất tới khi có success.
- **discovery@k** = `P(T ≤ k)` = `P(r(y_1)=1 ∨ r(y_2)=1 ∨ ... ∨ r(y_k)=1)`.
Nghĩa là xác suất solve được trong k attempts đầu.

## So với pass@k

- `pass@k` (Chen et al. 2021b): xác suất ít nhất 1 trong k samples **i.i.d.** là correct. Dành cho sampling độc lập.
- `discovery@k` **generalize** pass@k cho algorithm sinh attempt **tuần tự** (có thể share state, update weights, reprompt, v.v.).
- Khi algorithm là best-of-k thuần (sample i.i.d. từ fixed model): `discovery@k = pass@k`.

## Tại sao cần metric này

Test-time methods như [[con_test_time_self_distillation]], multi-turn reprompting không phải i.i.d. sampling → pass@k không apply. discovery@k đo đúng thứ các method này làm.

Note 8 của paper: "canonical metric in study of runtime speedup (i.e., time until termination, Dolan & Moré 2002)".

## Thesis extension: [[con_ctc_metric]]

discovery@k đếm **attempts**. Thesis RQ3 mở rộng thành **compute-to-correct (CTC)**:
- Đo compute (token count, GPU time) thay vì attempt count.
- Cho phép so sánh giữa methods có **cost per attempt khác nhau** (SDPO có training step tốn hơn sampling).
- Pareto frontier: compute vs discovery probability.

Intuition: 2.4× fewer attempts của SDPO (paper §5.2) có thể không tương đương 2.4× cheaper vì mỗi SDPO step nặng hơn multi-turn. CTC cân đối lại.

## Links

- [[con_test_time_self_distillation]] · [[ent_livecodebench]] · [[con_ctc_metric]] (planned)
