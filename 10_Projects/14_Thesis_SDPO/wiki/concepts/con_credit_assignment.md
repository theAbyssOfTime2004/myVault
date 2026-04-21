---
type: concept
created: 2026-04-22
updated: 2026-04-22
tags: [rl, signal, credit-assignment]
sources: [src_hubotter2026_self_distillation]
---

# Credit assignment (RL)

Bài toán xác định **token / action nào** trong trajectory chịu trách nhiệm cho final reward. Core difficulty của RL; đặc biệt khó khi reward sparse hoặc outcome-only.

## Vì sao quan trọng với code / math

Một solution đúng trải dài hàng chục reasoning tokens — token nào thực sự quyết định? Outcome reward không nói. Credit assignment kém → training sample-inefficient, gradient noisy, verbose reasoning (GRPO case).

## Điểm yếu của [[ent_rlvr]] & [[ent_grpo]]

- Reward binary ở episode level.
- Mọi token trong rollout share cùng scalar advantage.
- Gradient không phân biệt token nào important.
- Worst case: cả group cùng reward → advantage = 0 → learning stall.

## [[ent_sdpo]] giải pháp: dense signal ở 3 mức

Paper §4.2 tách 3 cấp độ density:

| Level | Signal per sequence | Key property |
|---|---|---|
| Sequence-level SDPO | 1 scalar (avg over tokens) | Dùng [[con_rich_feedback]] nhưng không dense |
| Token-level SDPO | 1 per sampled token | Medium |
| **Logit-level SDPO** | \|y\| × (K+1) unique advantages (K=100 top) | Full dense |

**Findings (Figure 10 left)**: logit > token > sequence > GRPO. Tức là:
- **Rich feedback** đóng góp lớn (sequence SDPO đã > GRPO).
- **Dense credit assignment** thêm gain nữa (logit > sequence).
- Hai effect là **complementary**, không overlap.

## Hệ quả dưới góc nhìn behavior

Credit assignment dày đặc → gradient chỉ "bump" đúng những token cần thiết → model không cần dài dòng để đạt accuracy. Đây lý giải hiện tượng §3.3: SDPO responses **3×–11× ngắn hơn** GRPO mà accuracy cao hơn.

→ Liên hệ RQ1 của thesis: khác biệt behavior reasoning giữa SDPO và GRPO *có thể trace* về credit assignment pattern.

## Alternative approaches

- **PRM (Process Reward Model)**: model ngoài estimate step reward. Scalar ở mức step, không logit.
  - Paper argue: "each language model is implicitly a PRM through retrospection if given rich feedback" → PRM không cần separate model.
- **GAE, TD learning, value networks**: truyền thống RL. Bottleneck memory + info.

## Links

- [[ent_sdpo]] · [[ent_grpo]] · [[src_hubotter2026_self_distillation]]
