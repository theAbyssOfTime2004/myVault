---
title: Lichess Feature Store — Project Plan
type: project-plan
course: Data Engineering
status: planning
created: 2026-05-30
data_source: Lichess Open Database
---

# Lichess Feature Store — Project Plan

Data Engineering course project. Build a Feature Store on a Lakehouse / Medallion architecture with batch + streaming pipelines over 100GB+ chess game data, fully deployed on GKE. Independent from the face-spoofing MLOps project (no data integration — reuse infra/deploy skills only).

## 1. Objectives

- Đạt rubric: Storage (MinIO) + Compute (Trino) + Batch (Spark) + Messaging (Kafka) + Streaming (Flink + window) + Orchestration (Airflow) + Deploy thực tế (GKE 20%).
- Vượt brief: biến "Gold serving table" thành một Feature Store thật — offline store + online store + Feature API + một ML consumer (cheat/anomaly detection) chứng minh training/serving consistency và point-in-time correctness.
- Deliverable: GitHub repo + README chi tiết + video demo full flow.

## 2. Data source

Lichess Open Database — https://database.lichess.org

- **Batch (historical)**: file dump `.pgn.zst`, mỗi tháng ~30 triệu games (~30GB nén, >150GB bung). Tải trực tiếp qua HTTP — KHÔNG crawl, KHÔNG rate limit.
- **Stream (real-time)**: Lichess API stream các live games đang diễn ra. Volume thấp tự nhiên → không chạm rate limit.

Mỗi game (PGN) chứa metadata (players, Elo, result, ECO opening, time control, termination) + moves, một phần có annotation `%eval` (Stockfish) và `%clk` (clock).

**Caveat dữ liệu**: `%eval` chỉ có ở một subset games (games được phân tích engine). Features dựa trên accuracy (ACPL) chỉ tính được trên subset này; features dựa trên activity/timing tính được trên toàn bộ.

## 3. Architecture

```
                    BATCH PATH (historical features)
  Lichess dump ──> Bronze ──> Silver ──> Gold ──────────> Offline store
  (.pgn.zst)       (raw)     (parsed)   (features)         (Delta on MinIO)
   [Spark]        [Spark]   [Spark]    [Spark+Trino]            │
                                                                │ materialize
                                                                │ [Airflow]
                    STREAM PATH (real-time features)            v
  Lichess API ──> Kafka ──> Flink ────────────────────> Online store
  (live games)  [Strimzi] (windowed agg)                 (Redis)
                                                                │
                          Feature API (FastAPI) <───────────────┤
                                    │                           │
                          Cheat Detection Model ────────────────┘
                          (IsolationForest)

  Trino ──> query/transform/DQ trực tiếp trên Delta tables (MinIO)
  Tất cả deploy trên 1 GKE cluster. Terraform provision. Prometheus/Grafana monitor.
```

## 4. Tech stack & rubric mapping

Tables ở column 0 để Obsidian render đúng.

| Layer | Tool | Rubric % | Ghi chú |
|---|---|---|---|
| Storage (Lakehouse) | MinIO + Delta Lake | 10% | MinIO = object store; Delta = table format trên Parquet |
| Computing / Transformation | Trino + Delta connector | 10% | SQL transform Silver→Gold + ad-hoc + DQ check |
| Batch processing | Apache Spark | 10% | Parse PGN bằng UDF/mapPartitions (python-chess), distributed |
| Source + message storage | Kafka (Strimzi) | 10% | Ingest live games stream |
| Stream processing | Apache Flink | 10% | BẮT BUỘC dùng window (full 10% vs 5%) |
| Orchestration | Airflow | 10% | Schedule dump download, Spark jobs, materialize Delta→Redis |
| Distribution / Serving | Redis + FastAPI | — | Online store + Feature API |
| Deploy thực tế | GKE (all) | 20% | 4×5%: MinIO, Spark, Flink, Airflow trên GKE |
| Data >100GB | Lichess monthly dump | 10% | 1 tháng dump đã >100GB |

## 5. Feature design

### Player entity (offline, batch)

| Feature | Mô tả |
|---|---|
| elo_blitz / rapid / bullet | Rating hiện tại theo time control |
| games_played_total / last_30d | Số game tổng / 30 ngày gần nhất |
| win_rate / draw_rate / loss_rate | Tỷ lệ theo overall + theo time control |
| avg_accuracy (ACPL) | Average centipawn loss từ %eval (subset có eval) |
| accuracy_std | Độ ổn định accuracy (consistency) |
| avg_move_time / move_time_std | Time management profile |
| opening_diversity | Entropy / số ECO khác nhau đã chơi |
| rating_volatility | Std của rating theo thời gian |
| blunder_rate | % nước đi eval drop lớn |
| accuracy_vs_rating_gap | Tín hiệu cheat chính: accuracy cao bất thường so với rating |

### Opening entity (offline, batch)

| Feature | Mô tả |
|---|---|
| eco_code / opening_name | Mã ECO + tên khai cuộc |
| popularity | Số lần được chơi |
| white_win_rate / black_win_rate / draw_rate | Tỷ lệ thắng theo bên |
| avg_game_length | Số nước trung bình |
| avg_player_rating | Rating trung bình người chơi |

### Real-time (online, stream)

| Feature | Mô tả |
|---|---|
| current_game_avg_move_time | Thời gian/nước trong game đang chơi |
| move_time_consistency | Variance timing — engine-like nếu quá đều (cheat signal, KHÔNG cần engine) |
| moves_in_window | Số nước trong sliding window (windowed agg cho Flink) |

**Lưu ý stream path**: live games qua API KHÔNG có `%eval` sẵn. Để tính accuracy real-time phải tự chạy Stockfish — nặng. Phương án:
- Mặc định: stream chỉ dùng **behavioral features (timing-based)** — không cần engine, vẫn là tín hiệu cheat mạnh.
- Stretch (optional): chạy Stockfish nhẹ trong Flink để eval live → accuracy real-time.

## 6. ML consumer — Cheat / anomaly detection

Mục đích: chứng minh feature store serve được model thật, KHÔNG phải showcase ML. Giữ nhẹ.

- Model: IsolationForest (unsupervised anomaly) hoặc LightGBM nếu có nhãn ToS-violation.
- Input: player offline features (accuracy_vs_rating_gap, blunder_rate, consistency...) + online features (timing trong game hiện tại).
- Output: anomaly score → flag player nghi vấn.
- **Điểm ăn tiền — Point-in-time correctness**: khi tạo training data, features của player phải tính từ games TRƯỚC game được gán nhãn, không leak future games. Chess cho temporal ordering tự nhiên → minh hoạ PIT join chuẩn.

## 7. Phased implementation

Effort-based (không gán ngày cứng — cân với thesis defense ~25-26/7). Ưu tiên dứt điểm rủi ro kỹ thuật trước.

### Phase 0 — Spike (rủi ro cao nhất, làm trước)
- [ ] Tải 1 file dump nhỏ (1 ngày data thay vì cả tháng).
- [ ] Viết PGN parser prototype bằng python-chess → Parquet (local, chưa Spark).
- [ ] Xác nhận schema, tỷ lệ games có `%eval`, cách tính ACPL.
- [ ] Quyết định stream features (behavioral-only vs Stockfish-in-Flink).

### Phase 1 — Infra (IaC nền tảng)
- [ ] Terraform: GKE Standard cluster + node pools (1 always-on nhỏ + 1 Spot autoscale) + GCS (tfstate) + Artifact Registry.
- [ ] Deploy MinIO (Operator/Bitnami) trên GKE — tạo buckets bronze/silver/gold.
- [ ] Deploy Kafka (Strimzi), Redis (Bitnami) trên GKE.
- [ ] Smoke test: ghi/đọc MinIO, produce/consume Kafka.

### Phase 2 — Batch pipeline (Spark + Delta + Trino)
- [ ] Spark Operator trên GKE; PGN parser chuyển thành Spark UDF/mapPartitions.
- [ ] Bronze (raw PGN landed) → Silver (parsed games, 1 row/game, Delta).
- [ ] Gold: player features + opening features (Spark heavy aggregate + Trino SQL transform).
- [ ] Trino + Delta connector: ad-hoc query + DQ checks trên Gold.
- [ ] Implement point-in-time join logic cho training set.

### Phase 3 — Stream pipeline (Kafka + Flink + Redis)
- [ ] Collector: Lichess live games API → Kafka topic.
- [ ] Flink K8s Operator; Flink job đọc Kafka → **windowed aggregation** (sliding window timing features) → ghi Redis.
- [ ] Materialize job (Airflow): Gold Delta features → Redis online store (batch refresh).

### Phase 4 — Serving + ML + Orchestration + Observability
- [ ] Feature API (FastAPI): online feature lookup từ Redis (reuse face-spoofing Helm pattern).
- [ ] Cheat detection model: train offline (PIT-correct) → serve qua API consuming features.
- [ ] Airflow DAGs: download dump (monthly) → Spark Bronze→Silver→Gold → materialize Redis.
- [ ] Prometheus + Grafana: monitor Spark/Flink/API (reuse face-spoofing monitoring).
- [ ] README + video demo full flow.

## 8. Cost management (bắt buộc)

| Chiến lược | Chi tiết |
|---|---|
| GKE Standard + Spot | Spot node pool cho Spark/Flink worker (rẻ 60-90%) |
| Autoscale to 0 | Node pool scale về 0 khi không dùng |
| Tách node pool | 1 pool nhỏ always-on (MinIO/Kafka/Redis) + 1 pool spot burst (Spark/Flink) |
| Free trial $300 | GCP 90 ngày — đủ nếu quản lý tốt |
| Run-on-demand | Chỉ bật full stack lúc dev + quay demo, còn lại tear down |

Mục tiêu: tổng <$100 trong free credit.

## 9. Risks & mitigations

| Risk | Mức | Mitigation |
|---|---|---|
| PGN parse ở scale lớn | Cao | Spike Phase 0; parser trong Spark UDF; test trên file nhỏ trước |
| Stream không có %eval cho accuracy | Trung bình | Dùng behavioral/timing features (không cần engine); Stockfish-in-Flink là stretch |
| Chi phí GKE vượt budget | Trung bình | Spot + autoscale-to-0 + run-on-demand |
| Quên window trong Flink → mất 5% | Thấp | Windowed agg là requirement cứng, đưa vào Phase 3 checklist |
| Trino chỉ query không transform → lệch rubric | Thấp | Đẩy một phần Silver→Gold transform sang Trino SQL |
| Xung đột thời gian với thesis (defense ~25-26/7) | Cao | Effort-based phases; dứt điểm Phase 0-1 sớm; phần ML giữ tối giản |

## 10. Deliverables

- GitHub repo: source + Terraform + Helm/manifests + Airflow DAGs + Spark/Flink jobs + README (cách cài + cách chạy).
- Video: demo full flow (batch + stream + serving + cheat detection) + chứng minh các công nghệ.
- CV bullet: "Data Engineering — Chess Feature Store (Lichess, 100GB+): Lakehouse (MinIO + Delta + Trino), batch + streaming (Spark + Kafka + Flink) với point-in-time correct features, online serving (Redis + FastAPI) powering real-time cheat detection, orchestrated by Airflow on GKE."

## Related

- [[project_de_feature_store]] (memory)
- Face-spoofing MLOps project — parallel track, serving plane (reuse Terraform/Helm/Prometheus/CI-CD skills)
