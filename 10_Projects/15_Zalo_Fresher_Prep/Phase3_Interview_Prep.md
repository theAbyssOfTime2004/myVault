---
tags: [zalo-prep, interview, phase-3]
---

# Phase 3 — Interview Prep

**Khi nào**: Sau khi pass Entry Test (~đầu 7/2026 estimate)
**Constraint Option A**: ~1.5h/ngày, song song thesis push. Concentrated 2-3 ngày trước interview. Master timeline: [[01_Master_Timeline]].

---

## Gap Fix — Critical only (compressed)

> Defer Karpathy GPT-from-scratch + RAG deepen + paper reading lượt 1 → Phase E (sau defense 26/7).

### Training loop from scratch — TAY GÕ KHÔNG AI (3-4 ngày)

- [ ] Code MLP cho MNIST: data loader → forward → loss → `loss.backward()` → `optimizer.step()` → `optimizer.zero_grad()` → eval → save/load
- [ ] Hiểu được tại sao gọi theo thứ tự đó (zero_grad trước backward, step sau backward)
- [ ] Refactor thành `Trainer` class
- [ ] Self-test: đóng tab, code lại trong 45 phút không reference

> Lý do tay gõ: live coding interview risk. AI không cứu được.

### Sampling strategies (1-2 ngày)

- [ ] Đọc HF blog "How to generate text" — kỹ, không skim
- [ ] Code 1 sampler tay: cho 1 logit vector, implement greedy / top-k / top-p / temperature scaling
- [ ] Hiểu temperature về mặt toán: `softmax(logits / T)` — T<1 sharper, T>1 flatter
- [ ] Hiểu khi nào dùng cái nào

### GPU memory math (30 phút)

- [ ] Inference: `params × bytes_per_param + KV_cache + overhead`
- [ ] LLaMA-7B FP16: 7B × 2 = 14GB + ~2-4GB overhead → 16-18GB
- [ ] Training: ~4× inference (Adam: weights + grads + 2× moment) → 7B FP16 train ≈ 60-80GB
- [ ] Áp dụng: "deploy LLaMA-13B cho service, chọn GPU nào?" → 13B × 2 = 26GB + overhead → A100 40GB hoặc 4090 24GB không đủ → A100 40GB minimum

---

## CV Deep Dive — chuẩn bị "tại sao" cho mọi decision

### MLOps Project Tier 1 (Phase 1)

- [ ] Tại sao chọn GKE thay vì self-managed K8s / Cloud Run / EKS?
- [ ] Tại sao Helm thay vì raw kubectl manifests?
- [ ] CI/CD pipeline GitHub Actions — flow gì, secrets handling ra sao (Workload Identity Federation)?
- [ ] MLflow tracking — backend store, artifact store ở đâu, tại sao?
- [ ] Prometheus scrape interval, custom metrics nào, tại sao chọn các metrics đó?
- [ ] HPA trigger metric là gì, threshold bao nhiêu, vì sao chọn số đó?
- [ ] Load test scenario, kết quả p95 latency dưới load 50 concurrent ra sao?
- [ ] **Nếu interviewer hỏi "sao không dùng KServe?":** trả lời thẳng — scope tradeoff, FastAPI + HPA đủ cho use case này, KServe overhead Knative/Istio không cần thiết ở scale fresher project

### Solazu

- [ ] Chunk size bao nhiêu, tại sao, thử size khác kết quả thế nào?
- [ ] "30% latency reduction" — baseline ms, sau optimize ms, đo p95 hay average, bottleneck ở đâu?
- [ ] "20% retrieval improvement" — metric là gì (Recall@k? MRR?)?
- [ ] LangGraph memory — state schema, checkpointer lưu ở đâu?

### Tiger Tribe

- [ ] Tại sao 4 agents không phải 1 agent lớn?
- [ ] asyncio — tại sao phù hợp (I/O-bound)?
- [ ] Redis session — key structure, TTL, race condition?
- [ ] Brand safety — false positive rate, precision vs recall trade-off?

### AISIA Lab

- [ ] ResNet vs DenseNet vs EfficientNet — model nào tốt nhất, metric nào (mAP? FPS?)?
- [ ] ViT vs CNN — đủ data để train ViT không?
- [ ] YOLO version nào, smoke detection đặc thù gì (small object, occlusion)?

### Thesis SDPO (highlight nếu interview hỏi research)

- [ ] SDPO là gì, khác DPO ở đâu, novelty của thesis?
- [ ] Multi-turn inference loop hoạt động ra sao?
- [ ] Weight update logic (đến lúc đó implement xong rồi)
- [ ] Eval trên LCBv6 — metric, baseline, kết quả

---

## Câu hỏi mở Zalo

- [ ] Dùng thử Kiki 20 phút
- [ ] Đọc 2 bài kỹ thuật trên [ZaloPay Engineering](https://medium.com/zalopay-engineering)
- [ ] Viết câu trả lời: *"Zalo AI đang gặp vấn đề gì, em có thể giải quyết thế nào?"* — 2 ý cụ thể từ sản phẩm đã dùng thật

---

## 5 STAR Behavioral Stories

Viết ra giấy, nói to không nhìn notes:

- [ ] Project tự hào nhất (thesis SDPO + MLOps + Solazu + số liệu)
- [ ] Khi gặp deadline gấp (thesis + Zalo + finals dồn tháng 7 — câu chuyện thật)
- [ ] Conflict với teammate
- [ ] Tại sao Zalo (mention KiLM / Kiki / VMLU)
- [ ] Định hướng 3-5 năm (research lean → ML engineer hybrid)

---

## Mock Interview lần 2

- [ ] Focus vào MLOps project mới build + thesis SDPO
- [ ] Câu bắt buộc chuẩn bị: *"Nếu làm lại từ đầu, bạn sẽ đổi gì?"*
- [ ] Câu thesis: *"Thesis của em có thể commercialize không, áp dụng vào Zalo product nào?"*
- [ ] Record + review câu ấp úng

---

## Reality check — Option A constraint

Phase 3 này **chỉ ~30% so với plan gốc 6 tuần** vì priority là thesis defense 25-26/7. Accept rằng:

- Có thể không trả lời sâu được câu PyTorch/transformer internals
- Có thể stutter ở câu "implement self-attention từ scratch"
- Strategy: lead với strength (RAG/agent thực chiến + thesis research) thay vì cố deep ML fundamentals

Nếu trượt Zalo: không bi kịch. Phase E sẽ expand gap fix cho công ty khác.
