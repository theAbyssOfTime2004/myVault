---
type: concept
created: 2026-04-22
updated: 2026-04-22
tags: [rl, signal, credit-assignment]
sources: [src_hubotter2026_self_distillation]
---

# Credit assignment (RL)

Bài toán xác định **token / action nào** trong một trajectory chịu trách nhiệm cho final reward. Là khó khăn cốt lõi của RL; đặc biệt khó khi reward sparse hoặc chỉ có ở outcome-level.

## Vì sao quan trọng với code / math

Một solution đúng có thể trải dài hàng chục reasoning tokens — token nào thực sự quyết định? Outcome reward không cho biết. Credit assignment kém → training sample-inefficient → học chậm, gradient noisy.

## Điểm yếu của [[ent_rlvr]]

Verifiable reward là binary ở episode level. Mọi token share cùng một scalar signal → gradient không có khả năng phân biệt theo token.

## [[ent_sdpo]] giải quyết thế nào

Chuyển [[con_rich_feedback]] thành per-token signal qua [[con_self_teacher]]. Signal dense đi kèm implicit credit assignment, không cần thay đổi verifier.

## Links

- [[src_hubotter2026_self_distillation]] — motivation và fix được đề xuất.
