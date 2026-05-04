---
tags: [project, interview-prep, zalo, mlops, timeline]
status: active
strategy: option-A-thesis-priority
path: A1-negotiate-delay
---

# Master Timeline — Option A / Path A1

> **Decision lock (3/5/2026):**
> - Option A: thesis SDPO defense (~25-26/7) ưu tiên hơn Zalo
> - Path A1: apply Zalo, nếu đậu **negotiate delay start sang sau 26/7**. Fallback A3 (decline) nếu Zalo cứng.

## Official ZTF 2026 dates

| Mốc | Ngày |
|---|---|
| CV mở | 4/5/2026 |
| **CV đóng** | **22/5/2026** |
| **Entry Test** | **30/5/2026** (offline @ VNG Campus) |
| **Phỏng vấn** | **15-26/6/2026** (offline @ VNG Campus) |
| **Nhập học** | **13/7/2026** ← conflict thesis defense |
| Kết thúc program | 22/10/2026 |

## Other key dates

| Mốc | Ngày | Source |
|---|---|---|
| Midterm xong | ~10/5/2026 | school |
| Finals | ~23-25/6/2026 | 1.5 tháng sau midterm |
| Submit báo cáo thesis | ~10-15/7/2026 | HK2/2024-2025 pattern |
| **Bảo vệ KLTN (KHDL)** | **~25-26/7/2026** | HK2/2024-2025 pattern |

## Phase breakdown

### Phase 0: 3/5 → 10/5 — Midterm only

### Phase A: 11/5 → 22/5 (~12 ngày) — MLOps Tier 1 + DSA elevated

| Block | Time/day |
|---|---|
| MLOps Phase 1 **Tier 1 only** | 2.5-3h |
| Thesis SDPO (maintain) | 1h |
| **DSA refresh elevated** | **1h** (vì sprint Phase B chỉ 8 ngày) |

**Tier 1 scope:** GKE + FastAPI + Docker + Helm + MLflow + GitHub Actions + Prometheus + Grafana + HPA + README. **Skip:** KServe, Knative, Evidently, Jaeger, Loki, NGINX Ingress, Terraform.

**Checkpoint 22/5 EOD:** submit CV + bảng điểm. Hard deadline.

[[Phase1_Week1_Foundation]] · [[Phase1_Week2_MLOps_Core]] · [[Phase1_Week3_Polish]]

### Phase B: 23/5 → 30/5 (8 ngày) — DSA sprint full intensity

| Block | Time/day |
|---|---|
| DSA + CS sprint | 3-4h |
| Thesis maintain | 1h |
| Mock test 28-29/5 | included |

**Checkpoint 30/5:** Entry Test offline @ VNG Campus.

[[Phase2_Entry_Test_Sprint]]

### Phase B.5: 31/5 → 14/6 (~2 tuần) — Wait + Interview prep + Finals warmup

| Block | Time/day |
|---|---|
| Phase 3 prep (CV deep dive + behavioral + gap fix critical) | 2h |
| Thesis (start weight update) | 1.5h |
| Finals warmup | 1h |

**Sub-actions:**
- ~6-10/6: nhận kết quả entry test (estimate)
- Nếu pass → schedule interview **càng sớm trong window 15-26/6 càng tốt** (target 15-20/6 để né finals 23-25/6)
- Phase 3 gap fix: training loop tay gõ + sampling + GPU memory (xem [[Phase3_Interview_Prep]])

### Phase C: 15/6 → 25/6 — Interview + Finals push

| Block | Time/day |
|---|---|
| Zalo interview (1 ngày, offline @ VNG) | scheduled |
| Finals study | 4-5h |
| Thesis maintain | 1h |

### Phase D: 26/6 → 12/7 (~2.5 tuần) — THESIS PUSH + offer negotiation

| Block | Time/day |
|---|---|
| Thesis main push (weight update finish, experiments, viết báo cáo) | 4-5h |
| **Negotiate delay start với Zalo** (nếu nhận offer) | as needed |

**Negotiation script (template):**
> "Em nhận offer Zalo Tech Fresher rất vui. Tuy nhiên, em đang trong giai đoạn cuối luận văn tốt nghiệp với ngày bảo vệ chính thức 25-26/7/2026. Em xin phép được delay nhập học sang ~28/7 hoặc 3/8 để hoàn thành tốt nghiệp. Em sẽ giữ full commitment và bù bằng performance trong program."

**Submit báo cáo thesis: ~10-12/7**

### Phase E: 13/7 → 26/7 — Final thesis prep + Decision on ZTF

**Scenario A1.1 (negotiation success):**
- Defense 25-26/7
- Bắt đầu ZTF ~28/7-3/8

**Scenario A1.2 (negotiation fail) → Path A3:**
- Decline offer politely
- Focus thesis defense
- Apply công ty khác sau defense

| Block | Time/day |
|---|---|
| Thesis slide prep + practice defense | 4h |
| Polish báo cáo cuối | 1-2h |
| Buffer | 2h |

### Phase F: 27/7+ — Recovery + next phase

- A1.1: nghỉ vài ngày → ZTF onboarding → 12 tuần program → 22/10 evaluation
- A1.2: nghỉ → expand Phase 3 (transformer scratch, RAG deepen, paper reading) → apply tier 2/3 companies

## Tradeoffs (re-confirmed under official dates)

| Cái mất | Cái được |
|---|---|
| Phase 3 chỉ còn ~2 tuần (vs 3-4 tuần plan cũ) | CV submitted on-time, thesis defense vững |
| DSA sprint chỉ 8 ngày sau CV | Pre-loaded trong Phase A bù lại |
| Có thể không nail PyTorch deep questions | Lead với strength: thesis SDPO + RAG/agent thực chiến |
| Có thể phải decline ZTF nếu không negotiate được | Thesis chất lượng, ZTF 2027 vẫn open |

## Quy tắc bất biến

1. CV deadline 22/5 EOD — không trễ một phút
2. Schedule interview càng sớm trong 15-26/6 càng tốt
3. Thesis vibecode OK với bar hiểu rationale — không vibecode SDPO core / weight update math
4. Phase 3 gap fix training loop **tay gõ** (interview live coding risk)
5. Finals 10/10 — non-negotiable
6. Negotiate ZTF delay ngay khi nhận offer, không trì hoãn

## Verification

- [x] Verify ZTF dates → confirmed via zalo.careers/techfresher
- [ ] Verify finals exact dates từ trường
- [ ] Verify lịch defense khi khoa announce (~đầu 7)
- [ ] Reach out anh chị ZTF 2025 hỏi về flex start date precedent
