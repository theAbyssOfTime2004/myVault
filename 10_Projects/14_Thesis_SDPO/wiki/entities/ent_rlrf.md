---
type: entity
created: 2026-04-22
updated: 2026-04-22
tags: [rl, training-setting, paradigm]
sources: [src_hubotter2026_self_distillation]
aliases: [Reinforcement Learning with Rich Feedback, RLRF]
---

# RLRF — Reinforcement Learning with Rich Feedback

Paradigm RL training được formalize hoá trong [[src_hubotter2026_self_distillation]] như successor của [[ent_rlvr]]. Thay vì giới hạn signal ở scalar reward `r ∈ R`, RLRF cho phép environment trả về **tokenized feedback** (bất kỳ sequence tokens nào: runtime error, unit test output, LLM judge, sample solution, v.v.).

## Ý tưởng cốt lõi

Nhiều verifiable environments thực ra **đã expose** rich feedback (runtime error trace, failing test case), nhưng RLVR pipelines vứt đi bằng cách collapse về scalar reward. RLRF giữ feedback dưới dạng token và cho policy tiêu thụ.

Figure 2 của paper: RLVR có bottleneck thông tin — masking state behind scalar `r`. RLRF đi qua bottleneck đó.

## Tính chất

- Generalize RLVR (mọi RLVR env đều là RLRF với `f = tokenize(r)`).
- Cho phép environment trả về **any tokenized representation** của state.
- Credit assignment có thể denser nếu dùng feedback khéo.

## Method instantiate

[[ent_sdpo]] là algorithm đầu tiên của paradigm này theo tác giả. Dùng chính policy làm [[con_self_teacher]] để extract credit assignment từ feedback mà không cần external reward model hay teacher.

## Liên hệ thesis

Thesis nằm trong **test-time variant** của RLRF. Hard question + code env với LeetCode-style feedback = perfect RLRF testbed. Xem §5 của paper và [[con_test_time_self_distillation]].

## Không phải là

- **RLHF**: feedback đến từ human preference. RLRF cơ chế automatic, từ environment.
- **PRM (Process Reward Model)**: PRM vẫn là scalar (per-step). RLRF dùng token sequences.
- **RLAIF**: feedback từ LLM judge cũng OK trong RLRF, nhưng RLRF rộng hơn.
