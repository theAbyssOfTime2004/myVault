---
tags: [project, interview-prep, zalo, mlops, timeline]
status: active
strategy: option-A-thesis-priority
---

# Master Timeline — Option A: Thesis Priority

> **Decision lock (3/5/2026):** thesis SDPO defense (~25-26/7) ưu tiên hơn Zalo interview. Khi conflict trong tháng 7, thesis full intensity, Zalo "best effort".

## Concrete dates

| Mốc | Ngày | Source |
|---|---|---|
| ZTF 2026 CV mở | 5/5/2026 | confirmed |
| Midterm xong | ~10/5/2026 | school |
| Submit CV Zalo (early) | ~22/5/2026 | self-set |
| ZTF CV đóng | ~2/6/2026 (estimate) | based on ZTF 2025 4-week window |
| Entry test | mid-late 6/2026 (estimate) | based on ZTF 2025 |
| Finals | ~25/6/2026 | school |
| Kết quả entry test | đầu 7/2026 | estimate |
| Zalo interview (if pass) | giữa 7/2026 | estimate |
| Submit báo cáo thesis | ~10-15/7/2026 | based on HK2/2024-2025 pattern |
| **Bảo vệ KLTN (Khoa học Dữ liệu)** | **~25-26/7/2026** | based on HK2/2024-2025 |

## Phase breakdown

### Phase 0: 3/5 → 10/5 — Midterm only
Nothing else. Một tuần.

### Phase A: 11/5 → 22/5 (~12 ngày) — MLOps Tier 1 + apply early

| Block | Time/day |
|---|---|
| MLOps Phase 1 **Tier 1 only** | 2.5-3h |
| Thesis SDPO (maintain) | 1h |
| DSA refresh light | 30 phút |

**Tier 1 scope:** GKE + FastAPI + Docker + Helm + MLflow + GitHub Actions + Prometheus + Grafana + HPA + README. **Skip:** KServe, Knative, Evidently, Jaeger, Loki, NGINX Ingress, Terraform.

**Checkpoint 22/5:** submit CV → [[Phase1_Week1_Foundation]] · [[Phase1_Week2_MLOps_Core]] · [[Phase1_Week3_Polish]]

### Phase B: 23/5 → entry test (~3-4 tuần) — DSA sprint + thesis ramp

| Block | Time/day |
|---|---|
| DSA + CS sprint | 2.5h |
| Thesis (start weight update) | 1.5h |
| Finals warmup | 30-45 phút |

**Detail:** [[Phase2_Entry_Test_Sprint]] (~80% nội dung đã pre-load trong Phase A, focus vào security/SQL/CV deep dive/mock test)

### Phase C: 20/6 → 25/6 — Finals priority

| Block | Time/day |
|---|---|
| Finals (10/10 target) | 4-5h |
| Thesis maintain | 1h |
| Phase 3 gap-fix | **defer** |

### Phase D: 26/6 → 26/7 (~1 tháng) — THESIS PUSH + light Zalo prep

| Block | Time/day |
|---|---|
| Thesis main push (weight update finish, experiments, viết báo cáo) | 4-5h |
| Phase 3 critical only | 1.5h |
| Zalo interview prep | concentrated 2-3 ngày trước interview |

**Phase 3 compressed scope:**
- Training loop from scratch trên MNIST (3-4 ngày, **tay gõ không AI**)
- Sampling strategies — đọc HF blog "How to generate text" + code 1 sampler tay (1-2 ngày)
- GPU memory math (30 phút)
- **Skip:** Karpathy GPT-from-scratch, RAG deepen, paper reading lượt 1 — defer Phase E

**Thesis sub-milestones:**
- 10-15/7: submit báo cáo
- 20-25/7: slide prep
- 25-26/7: defense

**Detail:** [[Phase3_Interview_Prep]]

### Phase E: 27/7+ — Recovery + expand

- Nghỉ vài ngày
- Tiếp tục job hunt với full attention
- Phase 3 expanded (transformer from scratch, RAG deepen, paper reading) cho interviews tiếp theo
- Apply tier 2/3 companies song song

## Tradeoffs accepted

| Cái mất | Cái được |
|---|---|
| Zalo technical interview có thể không nail PyTorch deep questions | Thesis chất lượng cao, defense vững |
| Tier 2/3 MLOps (KServe/Jaeger/Terraform) skip | Đủ stack core fresher, không over-engineer |
| Phase 3 chỉ làm ~30% plan gốc | Buffer cho thesis emergency |
| Có thể trượt Zalo | Path research-leaning được preserve |

## Quy tắc bất biến

1. Thesis vibecode OK nhưng phải hiểu rationale trước khi commit (không vibecode novelty / SDPO core / weight update math)
2. Phase 3 chỉ trigger sau khi pass entry test — không pre-emptive
3. Finals 10/10 — non-negotiable
4. 1 ngày off/tuần
5. Interview live coding nguy cơ cao → training loop trong Phase 3 phải tay gõ, không AI

## Verification points

- [ ] Verify ZTF CV deadline khi Zalo announce (5/5)
- [ ] Verify entry test date khi nhận email
- [ ] Verify lịch defense khi khoa announce (~đầu 7)
- [ ] Verify finals exact dates từ trường
