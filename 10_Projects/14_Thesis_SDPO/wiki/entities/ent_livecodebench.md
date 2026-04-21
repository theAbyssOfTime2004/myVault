---
type: entity
created: 2026-04-22
updated: 2026-04-22
tags: [benchmark, code, evaluation]
sources: [src_hubotter2026_self_distillation]
aliases: [LiveCodeBench, LCB, LCBv6]
---

# LiveCodeBench (LCB)

Competitive programming benchmark cho code reasoning (Jain et al. 2025, ICLR). Thiết kế để **contamination-free** bằng cách scrape problems sau known training cutoff; versioning theo thời gian cho phép tách subset "sau cutoff".

## LCBv6 (version dùng trong paper & thesis)

- **131 questions** phát hành giữa **Feb–May 2025**.
- Contest-style, range từ đơn giản đến competition-level.
- Public/private test split — public dùng khi training, private cho validation (mirror LeetCode setup).

## Feedback format (cho RLRF)

LeetCode-style runtime error trace. Ví dụ (Figure 3 của paper):
```
Runtime Error
ZeroDivisionError: division by zero
Line 73 in separateSquares (Solution.py)
Last Executed Input
[[26,30,2],[11,23,1]]
```

→ Đây là **rich feedback** mà [[ent_sdpo]] consume qua [[con_self_teacher]].

## Difficulty splits dùng trong thesis scope

Paper §5 định nghĩa:
- **Hard tasks**: pass@64 của [[ent_qwen3_8b]] < 0.5 → 19 questions (after filtering).
- **Very hard tasks**: pass@64 < 0.03 → 9 questions.

Thesis target cả hai splits cho RQ1–RQ3.

## Benchmark performance (Qwen3-8B + SDPO, paper §4)

- Base Qwen3-8B: 27.9%
- + GRPO: 41.2%
- + SDPO: **48.8%** — vượt Claude Sonnet 4 (40.5%) và Claude Opus 4 (39.7%) trên public leaderboard LCBv6.

## Thesis usage

- **Primary eval benchmark** cho Component A (template ablation).
- Hard/very-hard splits → sensitive với reasoning quality và compute → suited cho [[con_ctc_metric]] (RQ3).
- Provide both correctness và compute → input cho [[con_discovery_at_k]].

## Gaps

- LCB origin paper (Jain et al. 2025) chưa ingest vào `raw/`. Cần bổ sung để deep về: contamination protocol, nguồn problems, scoring nuances.
