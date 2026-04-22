---
type: source
created: 2026-04-22
updated: 2026-04-22
tags: [paper, stub, epistemic-verbalization, foundational]
sources: [src_kim2026_strategic_info_allocation]
aliases: [Kim 2026 strategic info, Kim et al. 2026 original]
---

# Kim et al. 2026 — Understanding Reasoning in LLMs through Strategic Information Allocation under Uncertainty

**STUB** — chưa ingest full PDF. Source của [[con_epistemic_verbalization]] concept.

Cited trong [[src_kim2026_why_self_distillation_degrades]] làm nền tảng:
- Định nghĩa 10 epistemic markers `T = {wait, hmm, perhaps, maybe, actually, alternatively, seems, might, likely, check}`.
- Claim: remove epistemic tokens → significant performance drop.
- Frame reasoning như **self-Bayesian process** — model iteratively update belief over intermediate hypotheses.

Authors (same first author): Jeonghye Kim, Xufang Luo, Minbeom Kim, Sangmook Lee, Dohyung Kim, Dongsheng Li, Yuqing Yang. 2026.

## Cần ingest

Để hoàn thiện RQ2 framework, cần đọc paper này cho:
- Full list epistemic markers và methodology chọn.
- Ablation experiments chứng minh "remove → drop".
- Self-Bayesian framing formal.
- Có test trên code tasks không, hay chỉ math/general?

## Status: **KHÔNG ACCESSIBLE** (search 2026-04-22)

Đã search:
- arXiv trực tiếp, Google, DuckDuckGo.
- Google Scholar (captcha block).
- dblp (connection fail).
- Personal site beanie00.com (empty).
- GitHub repo `beanie00/self-distillation-analysis` (không mention).

**Không tìm thấy**. Bibliography trong `src_kim2026_why_self_distillation_degrades` chỉ ghi bare entry *"Jeonghye Kim ... Understanding reasoning in llms through strategic information allocation under uncertainty, 2026"* — không arxiv ID, không venue, không URL.

Khả năng cao paper này là:
- Concurrent/unpublished work cùng nhóm (MSR + KAIST).
- Forthcoming submission chưa indexed.
- Internal document cited như forthcoming.

## Methodology 10 tokens — chỉ verify được 1 câu

Từ `src_kim2026_why_self_distillation_degrades` §3:
> *"Following Kim et al. (2026), we define a set of 10 epistemic markers T = {wait, hmm, perhaps, maybe, actually, alternatively, seems, might, likely, check} as **practical indicators** of regions where uncertainty externalization may occur."*

**"Practical indicators"** = heuristic/expert-chosen. Paper self-distillation không detail:
- Validation procedure (inter-rater, ablation per-token, etc.).
- Whether derived via frequency analysis of reasoning models (DeepSeek-R1 "Wait/Hmm" observation gợi ý possibly).
- Coverage completeness.

## Implication cho thesis RQ2

**Không thể cite methodology derivation**. Thesis 3 lựa chọn:

- **(a)** Cite Kim 2026 "following" như paper self-distillation đã làm — accept as heuristic, explicit flag limitation trong thesis methodology section.
- **(b)** Derive code-specific tokens empirically (frequency analysis base model trên LCBv6, expert annotation cho code uncertainty patterns).
- **(c)** **Triangulation**: dùng Kim's 10 tokens (compatibility) + code-specific empirical signals. Report both, compare. **Recommend cho thesis.**

## Follow-up actions

- Monitor arxiv/Google Scholar định kỳ cho paper này xuất hiện.
- Email direct tới Jeonghye Kim (beanie00@kaist.ac.kr or MSR contact) request preprint nếu thesis cần solid methodology.
- Nếu không accessible by proposal submission, dùng option (c) với transparent limitation note.

## Links

- [[src_kim2026_why_self_distillation_degrades]] — follow-up paper dùng framework này.
- [[con_epistemic_verbalization]] — concept derive từ paper này.
- [[con_code_uncertainty_signals]] — stub cho code adaptation (RQ2 option c).

## Links

- [[src_kim2026_why_self_distillation_degrades]] — follow-up paper dùng framework này.
- [[con_epistemic_verbalization]]
