---
tags: [zalo-prep, mlops, handoff, spec]
status: active
audience: coding-agent
repo: face-spoofing-detection (WSL)
deadline: 2026-05-22 EOD (CV submit)
---

# Handoff Spec — MLOps Week 1 (face-spoofing-detection)

> Spec cho coding agent. User làm planning + review, agent code. Mỗi ngày 1 task, end of day user verify trước khi sang ngày kế.

## Context

- **Repo**: `face-spoofing-detection` (WSL local path, đã push GitHub `theAbyssOfTime2004/face-spoofing-detection`)
- **Goal**: wrap pipeline liveness detection thành stack MLOps Tier 1 deploy được trên GKE, để screenshot vào CV Zalo Tech Fresher 2026.
- **Deadline**: 22/5/2026 EOD nộp CV. Hôm nay 14/5 → còn 8 ngày.
- **Stack Tier 1**: GKE + FastAPI + Docker + Helm + MLflow + Terraform + GitHub Actions + Prometheus + Grafana + HPA.
- **Skip**: KServe, Knative, DVC, Loki, Jaeger, NGINX Ingress, Evidently, ArcFace recognition.

## Repo state (pre-existing)

```
face-spoofing-detection/
├── config/config.yaml                # pipeline config (load nguyên block `pipeline:`)
├── models/
│   ├── global_branch.onnx            # 416K
│   └── local_branch.onnx             # 19M
├── src/
│   ├── pipeline/
│   │   ├── pipeline.py               # FaceLivenessPipeline class — entry point
│   │   ├── quality_gate.py
│   │   ├── detection.py              # SCRFD
│   │   ├── liveness_ensemble.py
│   │   └── recognition.py            # SKIP — disabled in config
│   ├── train_global.py               # MLflow tracking gắn vào đây
│   ├── train_local.py                # MLflow tracking gắn vào đây
│   └── evaluate_ensemble.py
├── tests/test_pipeline.py            # extend cho FastAPI
├── requirements.txt
└── README.md
```

**Key API**: `FaceLivenessPipeline(config_dict).process_frame(bgr_ndarray) -> dict` với keys `status`, `liveness.is_real`, `liveness.final_score`, `message`.

## Constraints

1. **Không sửa logic pipeline gốc** (`src/pipeline/`, `src/train_*.py`). Chỉ thêm hook (MLflow logging) không thay behavior.
2. **InsightFace auto-download `buffalo_l`** (~280MB) lần đầu chạy. Trong Docker phải pre-bake hoặc cache via PVC. Không để pod download mỗi lần restart.
3. **Image base**: `python:3.11-slim` (mediapipe có thể không support 3.12). Multi-stage build BẮT BUỘC — image cuối < 2GB.
4. **CPU inference only** — `onnxruntime` không `onnxruntime-gpu`. GKE node default `e2-standard-2`, không GPU.
5. **Không commit secrets**: `terraform.tfvars`, service account key, MLflow DB password → `.gitignore`.

## Day-by-day plan (14/5 → 22/5)

### N2 — 14/5 (today): FastAPI scaffold

**Tạo**:
- `app/__init__.py` (empty)
- `app/schemas.py`: Pydantic `PredictResponse` (status, is_real, liveness_score, message, latency_ms) + `HealthResponse` (status, model_loaded, version).
- `app/main.py`:
  - Load `config/config.yaml` lúc startup → instantiate `FaceLivenessPipeline`.
  - `POST /predict`: nhận `UploadFile`, decode `cv2.imdecode(np.frombuffer(...))` → ndarray BGR → `pipeline.process_frame(frame)` → map ra `PredictResponse`. Errors: 400 (empty/decode fail), 503 (pipeline not loaded), 500 (pipeline exception).
  - `GET /health`: returns 200 với `model_loaded` flag.
  - `GET /metrics`: Prometheus format. Counters: `liveness_requests_total{status}`, `liveness_errors_total{kind}`. Histogram: `liveness_latency_seconds`.
- Update `requirements.txt`: thêm `fastapi>=0.110`, `uvicorn[standard]>=0.27`, `python-multipart>=0.0.9`, `prometheus-client>=0.19`.

**Verify**:
- `uvicorn app.main:app --reload --port 8000` chạy được local.
- `curl localhost:8000/health` → `{"status":"ok","model_loaded":true,...}`.
- `curl -X POST -F "file=@<test_image>.jpg" localhost:8000/predict` → JSON có `liveness_score`.
- `curl localhost:8000/metrics` → text Prometheus format có `liveness_requests_total`.

### N3 — 15/5: Dockerfile + Artifact Registry

**Tạo**:
- `Dockerfile` multi-stage:
  - **Stage 1 (builder)**: `python:3.11-slim`, cài `build-essential`, `pip install -r requirements.txt --target=/install`.
  - **Stage 2 (runtime)**: `python:3.11-slim`, copy `/install` → `/usr/local/lib/python3.11/site-packages`, copy `app/`, `src/`, `config/`, `models/`. Pre-download `buffalo_l` model vào `/root/.insightface/` lúc build (chạy 1 dummy import) để pod startup không download lại.
  - `CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]`.
  - Expose 8000.
- `.dockerignore`: `data/`, `checkpoints/`, `documents/`, `*.ipynb`, `results/`, `__pycache__`, `.git`.
- `docker-compose.yml` local dev (optional).

**Verify**:
- `docker build -t liveness-api:dev .` → image size < 2GB.
- `docker run -p 8000:8000 liveness-api:dev` → endpoints chạy.
- `docker tag` + `docker push` lên Artifact Registry: `asia-southeast1-docker.pkg.dev/<PROJECT>/liveness-repo/liveness-api:v0.1.0`.

### N4 — 16/5: Helm chart + deploy GKE

**Tạo** `helm/liveness-chart/`:
- `Chart.yaml`
- `values.yaml`: `image.repository`, `image.tag`, `replicaCount=2`, `resources.requests` (cpu=500m, memory=1Gi), `resources.limits` (cpu=1500m, memory=2Gi), `service.type=LoadBalancer`, `service.port=80`, `config.path=/app/config/config.yaml`.
- `templates/deployment.yaml`: 1 container, expose 8000, readiness probe `GET /health` (initialDelay=30s vì model load chậm), liveness probe `GET /health` (initialDelay=60s).
- `templates/service.yaml`: LoadBalancer 80 → 8000.
- `templates/hpa.yaml` (chuẩn bị cho N7 day, có thể empty hoặc 1 replica fixed lúc này).

**Verify**:
- `helm lint helm/liveness-chart` clean.
- `helm install liveness ./helm/liveness-chart` thành công.
- `kubectl get pods` → 2 pods Running.
- `kubectl get svc` → EXTERNAL-IP có IP.
- `curl <EXTERNAL-IP>/health` → 200.

### N5 — 17/5: MLflow trên K8s

**Tạo**:
- Deploy MLflow server trên cùng GKE cluster (community Helm chart `community-charts/mlflow` hoặc tự viết Deployment + Service).
- Backend store: PostgreSQL (deploy bitnami chart) hoặc SQLite via PVC (đơn giản hơn). Artifact store: GCS bucket `gs://mlflow-artifacts-ztf-<random>`.
- Add MLflow tracking vào `src/train_global.py` + `src/train_local.py`:
  - `mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))`.
  - `mlflow.start_run()` wrap training loop.
  - Log params (epochs, lr, weight_decay, label_smoothing), metrics (loss/acc/ACER per epoch), artifacts (best checkpoint .pth).
- **KHÔNG đụng logic training** — chỉ thêm logging hooks.

**Verify**:
- `kubectl port-forward svc/mlflow 5000:5000` → MLflow UI ở `localhost:5000`.
- Chạy `python src/train_global.py --epochs 1 --data-dir <small_data>` → experiment xuất hiện trong UI với params + metrics + checkpoint artifact.

### N6 — 18/5: Terraform Path A (destroy & rebuild)

**Quy trình**:
1. Backup state hiện tại: `gcloud container clusters describe ztf-cluster --zone=asia-southeast1-a > terraform/_backup_cluster_describe.yaml` (gitignore).
2. Backup workload: `helm list`, `kubectl get all -A -o yaml > terraform/_backup_k8s_state.yaml` (gitignore).
3. `gcloud container clusters delete ztf-cluster --zone=asia-southeast1-a`.
4. Tạo GCS bucket cho remote state: `gsutil mb -l asia-southeast1 gs://tfstate-ztf-<random>` + `gsutil versioning set on gs://...`.
5. **Tạo** trong `terraform/`:
   - `backend.tf`: GCS backend trỏ tới bucket bước 4.
   - `versions.tf`: pin `google` provider version.
   - `variables.tf`: `project_id`, `region`, `zone`, `cluster_name`, `node_count`, `machine_type`.
   - `terraform.tfvars` (gitignore): values thật.
   - `terraform.tfvars.example` (commit): template.
   - `main.tf`:
     - `google_container_cluster` (no default node pool, `remove_default_node_pool=true`, `initial_node_count=1`).
     - `google_container_node_pool` separate (cho phép update không destroy cluster).
     - `google_artifact_registry_repository` cho Docker images.
6. `terraform init` → `plan` → `apply`.
7. Re-push Docker image (nếu Artifact Registry mới) + `helm install liveness ./helm/liveness-chart` + re-deploy MLflow.

**Verify**:
- `terraform plan` sau apply ra "No changes. Your infrastructure matches the configuration."
- `kubectl get nodes` ra số nodes đúng.
- Helm + MLflow chạy lại trên cluster mới.

### N7 — 19/5: pytest + helm lint

**Tạo** `tests/test_api.py`:
- `test_health()`: client GET `/health` → 200, `model_loaded` True.
- `test_predict_real_image()`: POST với ảnh face thật → 200, `is_real` true expected.
- `test_predict_spoof_image()`: POST với ảnh print attack → 200, `is_real` false expected.
- `test_predict_empty()`: POST không file → 400.
- `test_predict_invalid_image()`: POST file text → 400.
- `test_metrics_endpoint()`: GET `/metrics` → 200 với content-type Prometheus.
- Mock `FaceLivenessPipeline` cho speed (không load thật) — dùng `pytest.fixture` + monkeypatch.

**Verify**:
- `pytest tests/ --cov=app --cov-report=term-missing` → coverage > 80% trên `app/`.
- `helm lint helm/liveness-chart` clean.

### N8 — 20/5: Observability (JIT learn)

**Tạo**:
- Install `kube-prometheus-stack` Helm chart: `helm install monitoring prometheus-community/kube-prometheus-stack -n monitoring --create-namespace`.
- `monitoring/servicemonitor.yaml`: ServiceMonitor cho liveness-api scrape `/metrics` mỗi 30s.
- `monitoring/grafana-dashboard.json`: dashboard với panels — request rate (QPS), p50/p95/p99 latency, error rate, requests by status.
- `helm/liveness-chart/templates/hpa.yaml`: HPA target CPU 70%, min=2, max=5.

**Verify**:
- `kubectl port-forward svc/monitoring-grafana 3000:80 -n monitoring` → Grafana UI, login admin/<password>, dashboard import được, panels có data sau khi gửi vài request `/predict`.
- `kubectl get hpa` → HPA active.
- Load test (`hey -z 30s -c 10 http://<EXTERNAL-IP>/health`) → HPA scale up.

### N9 — 21/5: GitHub Actions CI/CD

**Tạo** `.github/workflows/ci.yml`:
- Trigger: push tới `main` + PR.
- Jobs:
  1. **test**: `pytest tests/ --cov`, fail if coverage < 80%.
  2. **lint**: `helm lint helm/liveness-chart`, `terraform fmt -check terraform/`, `ruff check app/`.
  3. **build-push** (chỉ trên `main`): build Docker, push Artifact Registry với tag `:${{ github.sha }}` + `:latest`. Auth via GCP Workload Identity Federation hoặc service account JSON từ GitHub Secret.
  4. **deploy** (chỉ trên `main`): `helm upgrade liveness ./helm/liveness-chart --set image.tag=${{ github.sha }}`.

**Verify**:
- Push commit dummy → workflow chạy xanh.
- Image mới xuất hiện trong Artifact Registry với SHA tag.
- `kubectl rollout status deployment/liveness` → rollout success.

### N10 — 22/5: README + screenshot + submit CV

**Tạo/sửa**:
- Update `README.md` root: thêm section "MLOps Deployment" với:
  - Architecture diagram (text-based hoặc Mermaid): GitHub Actions → Artifact Registry → GKE → Helm → FastAPI → Prometheus/Grafana, MLflow tracking branch, Terraform IaC.
  - Quick start: `terraform apply` → `docker build/push` → `helm install`.
  - Tech stack list với version.
  - Screenshots: Grafana dashboard, MLflow UI, `kubectl get all`, GitHub Actions green run.
- `docs/architecture.md` (optional): diagram chi tiết.

**Submit CV EOD 22/5**:
- Link repo trong CV.
- Bullet point: "Productionized face liveness detection (89% acc, F1 90%) on GKE: FastAPI serving · Docker multi-stage · Helm · Terraform IaC · MLflow tracking · Prometheus/Grafana observability · GitHub Actions CI/CD with auto-deploy."

## Cross-cutting rules cho agent

1. **Commit message convention**: `feat(app): ...`, `feat(infra): ...`, `chore(ci): ...`, `docs: ...`. Mỗi N1 day = 1 PR hoặc 1 batch commit để user review.
2. **PR description**: list file thay đổi + verify command để user copy-paste chạy.
3. **Stop & ask** nếu:
   - Image build > 2.5GB.
   - InsightFace pre-bake fail trong Docker.
   - Terraform `plan` ra unexpected destroys.
   - Test coverage không đạt 80% vì code khó test (cần discuss design).
4. **Không tự ý** add features ngoài Tier 1 scope kể trên. KServe / Knative / DVC / Loki / Jaeger = OUT.
5. **Không sửa** `src/pipeline/*.py`, `src/main.py`, `src/inference_ensemble.py`. Chỉ thêm MLflow logging vào `src/train_*.py`.

## Buffer / fallback

Nếu trễ schedule, cut theo thứ tự:
1. **N9 GitHub Actions** → giữ workflow basic test+lint, bỏ auto-deploy → manual `helm upgrade`.
2. **N8 HPA** → giữ Prometheus + Grafana, bỏ HPA.
3. **N6 Terraform** → giữ cluster manual `gcloud`, document commands trong README (mất signal CV nhưng infra vẫn chạy).
4. **N5 MLflow** → log file local thay vì server (chỉ rớt signal, training vẫn chạy).
