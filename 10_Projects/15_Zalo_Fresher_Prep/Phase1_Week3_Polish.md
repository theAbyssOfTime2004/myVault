---
tags: [zalo-prep, mlops, phase-1, week-3]
---

# Phase 1 · Tuần 3 — Tracing + Logging + IaC + NGINX + Polish

> **Option A path (Tier 1):** Ngày 19 → 20 → 21. **Skip Ngày 15-18 (Jaeger, Loki, NGINX Ingress, Terraform).** Lý do: scope tradeoff cho thesis. Có thể quay lại Phase E nếu cần upgrade CV cho công ty tiếp theo.

## Ngày 15 — Jaeger distributed tracing

- [ ] Cài Jaeger Operator bằng Helm (hoặc Tempo nếu muốn Grafana stack)
- [ ] Add OpenTelemetry vào FastAPI: `opentelemetry-instrumentation-fastapi`, config exporter → Jaeger
- [ ] Tạo custom spans: `face_detection`, `liveness_inference`, `ensemble_fusion`
- [ ] Verify trên Jaeger UI: 1 request `/predict` → trace với 3 spans + latency từng bước
- [ ] Đọc: [OpenTelemetry Python Quickstart](https://opentelemetry.io/docs/languages/python/getting-started/)

> **Output**: Jaeger UI hiển thị distributed trace cho mỗi prediction request

---

## Ngày 16 — Loki + Grafana logging

- [ ] Cài Loki stack: `helm install loki grafana/loki-stack` (Promtail tự collect logs từ tất cả pods)
- [ ] Config structured logging trong FastAPI bằng `structlog`, log JSON với fields: `request_id`, `latency_ms`, `liveness_score`, `decision`, `error_type`
- [ ] Tạo Grafana Loki datasource, viết LogQL query: filter error logs + slow requests (>500ms)
- [ ] Tạo Grafana alert: error rate >5% trong 5 phút
- [ ] Đọc: [Loki LogQL](https://grafana.com/docs/loki/latest/query/) — chỉ Basic queries

> **Output**: Grafana Explore hiển thị structured logs, alert rule configured

---

## Ngày 17 — NGINX Gateway + authentication

- [ ] Cài NGINX Ingress Controller: `helm install nginx ingress-nginx/ingress-nginx`
- [ ] Viết Ingress manifest: route `/api/v1/predict` → FastAPI, `/kserve/` → KServe
- [ ] Thêm auth: NGINX annotation `nginx.ingress.kubernetes.io/auth-type: basic` hoặc JWT middleware trong FastAPI
- [ ] Test: request không có token → 401, có token → 200
- [ ] Đọc: [NGINX Ingress annotations](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/) — phần Authentication

> **Output**: một EXTERNAL-IP duy nhất cho toàn bộ service, auth working

---

## Ngày 18 — Terraform IaC cho GKE

- [ ] Viết `terraform/main.tf`: provider google, resource `google_container_cluster` (machine type, node count, autoscaling)
- [ ] Viết `terraform/variables.tf`: `project_id`, `region`, `cluster_name`, `node_count`
- [ ] Viết `terraform/outputs.tf`: `cluster_endpoint`, `cluster_ca_certificate`
- [ ] **Không cần destroy/recreate cluster** — dùng `terraform import` để import cluster đang chạy vào state, verify bằng `terraform plan`
- [ ] Đọc: [Terraform GKE resource](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/container_cluster) — chỉ basic example

> **Output**: `terraform plan` hiển thị đúng config, `terraform.tfstate` có cluster resource

---

## Ngày 19 — HPA + load testing

- [ ] Thêm HPA manifest vào Helm chart: target CPU 70%, minReplicas: 1, maxReplicas: 5
- [ ] Chạy load test bằng `locust` hoặc `k6`: 50 concurrent users liên tục trong 2 phút
- [ ] Verify trên Grafana: CPU tăng → HPA scale up → request phân tải → CPU giảm → scale down
- [ ] Chụp screenshot Grafana scaling event để đưa vào README
- [ ] Đọc: [k6 Quickstart](https://grafana.com/docs/k6/latest/get-started/running-k6/) (~5 phút)

> **Output**: screenshot/video HPA scale từ 1 lên 3+ pods khi load test

---

## Ngày 20 — End-to-end integration + README

- [ ] Chạy full E2E một lần: train → MLflow log → DVC push → CI → build image → helm deploy → KServe update → send request → check Grafana + Jaeger + Loki
- [ ] Viết `README.md`: architecture diagram (draw.io hoặc Mermaid), hướng dẫn setup từng component, screenshot mỗi tool
- [ ] Viết `ARCHITECTURE.md`: tại sao chọn mỗi tool, trade-offs (Loki vs ELK, KServe vs custom serving...)

> **Output**: GitHub repo với README đẹp, mọi link và screenshot hoạt động

---

## Ngày 21 — CV update + nộp CV

- [ ] Update CV bullet: xem gợi ý ở [[00_Overview]]
- [ ] Check tất cả GitHub links còn active, README đẹp trên mobile
- [ ] Nộp CV lên zalo.careers/techfresher

> Nghỉ ngơi. Phase 2 bắt đầu khi nhận email thông báo Entry Test date.
