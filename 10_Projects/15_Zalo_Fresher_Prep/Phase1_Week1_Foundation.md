---
tags: [zalo-prep, mlops, phase-1, week-1]
---

# Phase 1 · Tuần 1 — GKE + FastAPI + Docker + Helm

> **Option A path (Tier 1):** Ngày 1 → 2 → 3 → 4 → 5 → 7. **Skip Ngày 6 (DVC)** — MLflow đã đủ versioning signal.

## Ngày 1 — GKE cluster + project structure

- [x] Tạo GCP project, enable billing ($300 free credit), enable APIs: `container.googleapis.com`, `artifactregistry.googleapis.com`
- [x] Cài gcloud CLI + kubectl + helm local
- [x] Tạo GKE cluster: `gcloud container clusters create ztf-cluster --num-nodes=3 --machine-type=e2-standard-2 --zone=asia-southeast1-a`
- [x] Setup Artifact Registry repo để push Docker image
- [ ] Tổ chức folder: `app/`, `helm/`, `terraform/`, `ci/`, `monitoring/`
- [ ] Đọc: [GKE Quickstart](https://cloud.google.com/kubernetes-engine/docs/deploy-app-cluster) — chỉ phần "Before you begin" + "Create cluster"

> **Output**: `kubectl get nodes` trả về 3 nodes

---

## Ngày 2 — FastAPI serving endpoint

- [ ] Tạo `app/main.py`: 3 endpoints — `POST /predict` (nhận ảnh, trả liveness score), `GET /health`, `GET /metrics` (Prometheus format)
- [ ] Wrap `src/inference_ensemble.py` thành class `LivenessModel`, inject vào FastAPI
- [ ] Test local: `uvicorn app.main:app --reload`, gửi request bằng curl
- [ ] Thêm Pydantic schema cho request/response
- [ ] Đọc: [FastAPI request files](https://fastapi.tiangolo.com/tutorial/request-files/)

> **Output**: `curl localhost:8000/predict` → `{"liveness": 0.87, "decision": "real"}`

---

## Ngày 3 — Dockerfile + push Artifact Registry

- [ ] Viết `Dockerfile`: multi-stage build (builder cài deps, runtime copy artifact), base `python:3.11-slim`
- [ ] Viết `docker-compose.yml` cho local dev
- [ ] Build + test local: `docker build -t liveness-api . && docker run -p 8000:8000 liveness-api`
- [ ] Tag + push: `docker tag liveness-api asia-southeast1-docker.pkg.dev/PROJECT/repo/liveness-api:v1`
- [ ] Đọc: [Docker multi-stage](https://docs.docker.com/build/building/multi-stage/) — chỉ ví dụ đầu tiên

> **Output**: Image trên Artifact Registry, docker pull được từ máy khác

---

## Ngày 4 — K8s Deployment + Service + Helm chart

- [ ] `helm create liveness-chart`, xóa templates mặc định, viết lại `deployment.yaml` và `service.yaml`
- [ ] Viết `values.yaml`: image repo, tag, replicas, resource limits, service type LoadBalancer
- [ ] Deploy: `helm install liveness ./liveness-chart`
- [ ] Verify: `kubectl get pods`, `kubectl get svc`, curl tới EXTERNAL-IP
- [ ] Đọc: [Helm Quickstart](https://helm.sh/docs/intro/quickstart/) (~10 phút)

> **Output**: Pod running trên GKE, `curl EXTERNAL-IP/health` → 200

---

## Ngày 5 — MLflow tracking server

- [ ] Deploy MLflow server trên K8s: tìm Helm chart community hoặc tự viết Deployment + Service
- [ ] Config backend store: GCS bucket (artifact store) + SQLite/PostgreSQL (metadata)
- [ ] Add MLflow tracking vào `src/train_global.py` và `src/train_local.py`: log params, metrics (loss, accuracy, ACER), artifacts
- [ ] Verify: `kubectl port-forward svc/mlflow 5000:5000` → MLflow UI có experiment
- [ ] Đọc: [MLflow Tracking Quickstart](https://mlflow.org/docs/latest/getting-started/intro-quickstart/)

> **Output**: MLflow UI hiển thị experiment với params + metrics + model artifact

---

## Ngày 6 — DVC setup + data/model versioning

- [ ] `dvc init`, setup remote GCS: `dvc remote add -d gcs_remote gs://bucket-name/dvc`
- [ ] Track dataset: `dvc add data/`, commit `.dvc` files vào git
- [ ] Track model sau train: `dvc add models/global_model.onnx`
- [ ] Viết `dvc.yaml` pipeline: stages `train_global` → `evaluate` → `convert_onnx`
- [ ] Test: `dvc repro`
- [ ] Đọc: [DVC Get Started](https://dvc.org/doc/start) — phần Data Management + Pipelines

> **Output**: `dvc push` thành công, `dvc pull` trên máy mới reproduce được pipeline

---

## Ngày 7 — Review tuần 1 + fix bugs

- [ ] Checklist: GKE up · FastAPI /predict chạy · Docker image trên registry · Helm deploy được · MLflow có experiment · DVC pipeline reproduce được
- [ ] Fix tất cả bugs ngày 1–6
- [ ] Viết unit tests cho `app/main.py` bằng pytest: test `/health`, test `/predict` với mock model — coverage >80%
- [ ] `helm lint liveness-chart` không có error

> **Output**: pytest pass, helm lint clean, toàn bộ stack tuần 1 hoạt động
