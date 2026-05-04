---
tags: [zalo-prep, interview, phase-3]
---

# Phase 3 — Interview Prep

**Date:** 31/5 → 14/6/2026 (~2 tuần, sau entry test). **Interview window 15-26/6** (offline @ VNG Campus).
**Cường độ:** 2h/ngày interview prep + 1.5h thesis + 1h finals warmup. Master timeline: [[01_Master_Timeline]].

> **Path A1 strategy:** Schedule interview càng sớm trong 15-26/6 càng tốt — target 15-20/6 để né finals 23-25/6.

---

## Gap Fix — Critical only (compressed)

> Defer Karpathy GPT-from-scratch + RAG deepen + paper reading lượt 1 → Phase F (sau defense 26/7).
> **Total time budget: ~5-6 ngày trong window 31/5 → 14/6.**

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

## Offer negotiation prep (chuẩn bị trước interview)

Nếu pass interview → likely có offer ~đầu 7. Program nhập học chính thức **13/7**, đụng thesis defense 25-26/7. Cần negotiate delay.

**Script template (gửi HR sau khi nhận offer):**

> "Em nhận offer Zalo Tech Fresher rất vui và quyết tâm tham gia. Tuy nhiên, em đang trong giai đoạn cuối luận văn tốt nghiệp với ngày bảo vệ chính thức **25-26/7/2026** (Khoa Toán Tin, ĐH KHTN-VNUHCM). Em xin phép được delay ngày nhập học sang **~28/7 hoặc 3/8** để hoàn thành tốt nghiệp đúng quy định trường. Em cam kết full commitment trong toàn bộ 12 tuần program và sẽ bù bằng performance."

**Backup plan nếu Zalo cứng:** decline politely, focus thesis, apply công ty khác sau defense (Path A3).

**Action item trước interview:** reach out anh chị ZTF 2025 hỏi về precedent — Zalo có từng flex start date cho lý do tốt nghiệp không?

---

## Reality check — Option A / Path A1

Phase 3 này **chỉ ~5-6 ngày gap fix + 1 tuần CV/behavioral** vì priority là thesis defense. Accept rằng:

- Có thể không trả lời sâu được câu PyTorch/transformer internals
- Có thể stutter ở câu "implement self-attention từ scratch"
- Strategy: lead với strength (thesis SDPO research + RAG/agent thực chiến) thay vì cố deep ML fundamentals

Nếu trượt Zalo hoặc decline offer: không bi kịch. Phase F sẽ expand gap fix cho công ty khác.
