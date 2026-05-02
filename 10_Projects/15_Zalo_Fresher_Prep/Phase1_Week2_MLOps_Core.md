---
tags: [zalo-prep, mlops, phase-1, week-2]
---

# Phase 1 · Tuần 2 — KServe + CI/CD + Monitoring

> **Option A path (Tier 1):** Ngày 10 → 11 → 12 → 14. **Skip Ngày 8-9 (KServe + Knative scale-to-zero) và Ngày 13 (Evidently).** Dùng raw K8s Deployment + HPA thay KServe; bỏ drift detection.

## Ngày 8 — KServe installation + InferenceService

- [ ] Cài Istio: `istioctl install --set profile=default`
- [ ] Cài KServe: `kubectl apply -f https://github.com/kserve/kserve/releases/download/v0.13.0/kserve.yaml`
- [ ] Viết `InferenceService` manifest cho ONNX model: `spec.storageUri` trỏ tới GCS bucket
- [ ] Verify: `kubectl get inferenceservice` → READY = True
- [ ] Đọc: [KServe ONNX example](https://kserve.github.io/website/latest/modelserving/v1beta1/onnx/)

> ⚠️ KServe scale-to-zero cần Knative Serving — cài thêm nếu rubric yêu cầu. Nếu timeout, tăng `initialDelaySeconds` trong probe.

> **Output**: curl KServe endpoint trả về prediction

---

## Ngày 9 — KServe scale-to-zero + MLflow → KServe pipeline

- [ ] Config Knative autoscaling: annotation `autoscaling.knative.dev/minScale: "0"` — verify pod terminate sau 60s không có traffic
- [ ] Viết `scripts/deploy_model.py`: lấy artifact từ MLflow → upload GCS → update InferenceService
- [ ] Test end-to-end: train → MLflow log → `deploy_model.py` → KServe serve → curl predict

> **Output**: `kubectl get pods` hiển thị 0 pods khi idle, scale up khi có request

---

## Ngày 10 — GitHub Actions — test stage

- [ ] Viết thêm unit tests đến coverage ≥80%: test `pipeline.py` (mock detector), `dataset.py` (mock loader), `inference.py` (mock ONNX runtime)
- [ ] Tạo `.github/workflows/ci.yml`: trigger on push/PR, job "test": setup Python → pip install → `pytest --cov=src --cov-report=xml --cov-fail-under=80` → upload coverage artifact
- [ ] Push và verify trên GitHub Actions tab
- [ ] Đọc: [GitHub Actions Quickstart](https://docs.github.com/en/actions/writing-workflows/quickstart)

> **Output**: GitHub Actions green, coverage report ≥80%

---

## Ngày 11 — GitHub Actions — build + deploy stage

- [ ] Thêm job "build" (needs: test): `docker build + push` lên Artifact Registry, dùng GitHub Secrets cho GCP credentials (Workload Identity Federation)
- [ ] Thêm job "deploy" (`workflow_dispatch` — manual): `helm upgrade --install` trên GKE
- [ ] Build auto khi push, deploy chỉ trigger manual

> ⚠️ Dùng Workload Identity Federation thay service account key — an toàn hơn, Google khuyến nghị.

> **Output**: merge PR → test pass → Docker image tự build + push lên registry

---

## Ngày 12 — Prometheus + Grafana

- [ ] Cài kube-prometheus-stack: `helm install prometheus prometheus-community/kube-prometheus-stack`
- [ ] Expose `/metrics` trong FastAPI bằng `prometheus_fastapi_instrumentator` (request count, latency histogram, error rate)
- [ ] Thêm custom metrics: `liveness_score_histogram`, `prediction_confidence_gauge`
- [ ] Tạo Grafana dashboard: import ID 17175 (FastAPI monitoring) rồi customize
- [ ] Đọc: [prometheus-fastapi-instrumentator README](https://github.com/trallnag/prometheus-fastapi-instrumentator)

> **Output**: Grafana dashboard hiển thị request rate, p95 latency, liveness score distribution

---

## Ngày 13 — Evidently data drift dashboard

- [ ] Tạo `monitoring/drift_monitor.py`: dùng Evidently so sánh reference dataset (training) với production data
- [ ] Metrics: image brightness distribution, face detection confidence, prediction score distribution
- [ ] Tạo Evidently Report + Test Suite, export HTML + JSON metrics
- [ ] Setup K8s CronJob chạy mỗi 1 giờ, lưu report lên GCS
- [ ] Đọc: [Evidently Quickstart](https://docs.evidentlyai.com/get-started/tutorial) — phần Classification

> **Output**: CronJob chạy được, HTML report có drift metrics với threshold alerts

---

## Ngày 14 — Review tuần 2 + integration test

- [ ] Checklist: KServe READY + scale-to-zero · CI green · Prometheus scraping FastAPI · Grafana dashboard · Evidently CronJob running
- [ ] Viết integration test: gửi 100 request lên `/predict`, verify Grafana metrics tăng, verify MLflow log
- [ ] Fix bugs còn tồn đọng

> **Output**: toàn bộ stack tuần 2 hoạt động end-to-end
