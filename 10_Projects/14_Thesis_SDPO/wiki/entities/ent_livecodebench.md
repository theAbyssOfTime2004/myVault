---
type: entity
created: 2026-04-22
updated: 2026-04-22
tags: [benchmark, code, evaluation]
sources: [src_hubotter2026_self_distillation]
aliases: [LiveCodeBench, LCB]
---

# LiveCodeBench

Competitive programming benchmark để eval code reasoning của LLM. Thiết kế để chống contamination bằng cách scrape problems sau known training cutoff. Thesis target **v6**, split hard và very-hard.

## Vì sao thesis chọn LCB

- Split **hard / very-hard** nhạy với chất lượng reasoning → phù hợp để ablation test-time SDPO.
- **Versioned** → kiểm soát contamination.
- Đo cả correctness và compute → dùng làm input cho [[con_ctc_metric]].

## Xuất hiện ở đâu

- [[src_hubotter2026_self_distillation]] — một trong các benchmark eval SDPO vs RLVR.

## Gaps

- Chưa ingest LCB origin paper. Cần clip vào [[raw/]] rồi re-ingest để populate: contamination protocol, nguồn problem, cách scoring.
