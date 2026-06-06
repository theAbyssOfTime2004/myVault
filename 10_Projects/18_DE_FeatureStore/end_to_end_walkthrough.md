---
title: Lichess Feature Store — End-to-End Walkthrough
type: project-doc
course: Data Engineering
status: built (verified on dev month; full-scale demo pending)
created: 2026-06-05
repo: github.com/theAbyssOfTime2004/lichess-feature-store (WSL ~/Repos/lichess-feature-store)
source_of_truth: repo README.md + docs/phase*.md + source code
---

# Lichess Feature Store — End-to-End Walkthrough

Tài liệu này giải thích toàn bộ project từ đầu đến cuối: nó là gì, dữ liệu đi qua những đâu, từng component làm gì (kèm logic thật trong code), nó được dựng theo trình tự nào, và mọi bug đã gặp cùng cách xử lý. Mục đích là sau khi vibecode khá nhiều vẫn nắm lại được mạch và đủ tự tin nói khi phỏng vấn.

> Một lưu ý thẳng thắn để khỏi nói quá: pipeline mới chạy thông end-to-end trên dev month (`2013-01`) và một tháng có eval/clock thật, chứ chưa chạy full-scale. Phần demo >100GB, demo live-stream chạy chung, và CI/CD vẫn còn dang dở (xem mục 11). Khi phỏng vấn đừng nói "đã chạy 120GB" — nói "kiến trúc và pipeline đã sẵn, verify trên tháng thật có annotation, còn lần chạy full-scale là bước cuối".

---

## 1. Tóm tắt

Một data platform kiêm feature store chạy end-to-end trên dữ liệu cờ vua công khai của Lichess. Nó đọc PGN dump hàng tháng (đường batch) và live stream từ Lichess TV (đường real-time), dựng một Lakehouse theo kiến trúc Medallion (bronze → silver → gold), phục vụ feature ở cả hai dạng offline và online, rồi build một model nhẹ phát hiện gian lận (anomaly detection không giám sát). Toàn bộ chạy trên một cluster GKE: Terraform dựng hạ tầng, Airflow điều phối, Prometheus + Grafana giám sát.

Mục tiêu của project là làm một lakehouse + feature store đúng hình dạng production: parse phân tán ở scale lớn, feature engineering point-in-time-correct, kết hợp batch và streaming, và online serving có quan sát được.

---

## 2. Tổng quan — hai đường dữ liệu

**BATCH (lịch sử → offline features)**

```
Lichess dump .pgn.zst
  → [ingest]    curl | mc pipe → MinIO bronze (raw .zst, không đổi)
  → [shred]     1 pass stream-decompress, cắt theo ranh giới ván → nhiều shard .pgn.gz - vì file .zst không splittable
  → [Spark]     bronze_to_silver: parse PGN (python-chess) → Delta silver/games (partition year_month, speed)
  → [Spark]     silver_to_gold: player_features + opening_features (Delta)
  → [Spark]     build_training_set: ma trận point-in-time (không leak tương lai)
  → [sklearn]   train_cheat_model: IsolationForest → gold/cheat_scores + model artifact
  → [materialize] Gold Delta → Redis (offline:player:*, online:cheat:*)
  Trino + Hive Metastore: query/DQ/transform SQL trực tiếp trên Delta ở MinIO
```

**STREAM (live → online features)**

```
Lichess TV feed (NDJSON)
  → [collector]  → Kafka topic lichess.tv.moves
  → [Flink]      windowed (sliding 30s/10s) move-time stats per game
  → Redis online:movetime:<game_id>
```

**SERVING**: Feature API (FastAPI) đọc Redis, phơi ra `/features/player`, `/features/movetime`, `/predict/player`, `/metrics`.

Tất cả nằm trên một cluster GKE. Terraform lo phần hạ tầng; các K8s Operator (Spark, Strimzi/Kafka, Flink, Airflow) cài qua Helm lo phần platform; image thì build bằng Cloud Build.

---

## 3. Phương pháp build — "de-risk trước, logic sau"

Hiểu được phần này thì sẽ hiểu vì sao repo lại có cấu trúc như hiện tại. Quy tắc xuyên suốt: mỗi phase mở đầu bằng một spike nhỏ để chứng minh đoạn tích hợp rủi ro nhất chạy được, rồi mới viết logic nghiệp vụ. Trình tự thực tế (theo thư mục `docs/`):

| Phase | Mục tiêu | Rủi ro được khử |
|---|---|---|
| 0 | Parser PGN local (no cloud) | PGN parse được không? bao nhiêu % có `%eval`/`%clk`? tốc độ? |
| 0-followup | Stream-from-URL, đổi `plies` | Không tải hết 30GB; sửa schema |
| 1 | Terraform + GKE + MinIO/Kafka/Redis | Infra + connectivity (smoke test 3 cái) |
| 2.0 | Spark↔MinIO↔Delta **spike** | Spark trên GKE ghi/đọc Delta trên MinIO được không |
| 2.1 | Bronze ingestion in-cluster | Stream dump URL→MinIO không qua laptop |
| 2.2 | Bronze→Silver (Spark parse) | Parse phân tán, correctness trên dev month |
| 2.2-scale | Shred shard | Bottleneck 1 file = 1 task |
| 2.3 | Gold features + harden Silver | player/opening features, move-time, datetime |
| 2.3-validate | Unit test parser | ACPL/move-time math đúng (dev month không có eval!) |
| 2.4 | Trino + Hive Metastore | SQL query/transform Delta trên MinIO |
| 3.0 | Flink operator **spike** | PyFlink chạy trên GKE 1.35 |
| 3.1 | Collector TV→Kafka | Live feed vào Kafka |
| 3.2 | Flink windowed→Redis | Windowed agg (yêu cầu chấm điểm) |
| 4.0 | Airflow trên GKE **spike** | hello_dag chạy (KubernetesExecutor) |
| 4.1 | Batch orchestration DAG | DAG điều phối ingest→Spark→materialize |

Để ý các phase 2.0, 3.0, 4.0 đều là spike tích hợp ("prove the pipe first") trước khi làm thật. Chính vì cô lập và xử lý rủi ro sớm nên về sau ít gặp bug kiểu sập cả hệ thống.

---

## 4. Nguồn dữ liệu & schema

**Batch**: `https://database.lichess.org/standard/lichess_db_standard_rated_<MONTH>.pgn.zst`. Mỗi tháng gần đây ~30GB nén (>150GB bung), ~30 triệu ván. Tải trực tiếp qua HTTP, không crawl, không rate limit.

**Stream**: `GET https://lichess.org/api/tv/feed` — NDJSON của ván featured đang chạy:
- `{"t":"featured","d":{"id":"<gameId>",...}}` — ván mới bắt đầu.
- `{"t":"fen","d":{"fen":"...","lm":"e2e4","wc":180,"bc":175}}` — một nước: `lm` last move, `wc`/`bc` = clock còn lại (giây) của trắng/đen.

**Caveat dữ liệu quan trọng**: `%eval` (Stockfish) chỉ có ở subset ván được phân tích engine. → features dựa trên **accuracy (ACPL)** chỉ tính được trên subset đó; features dựa trên **timing/activity** tính được trên toàn bộ. **Tháng cũ (2013) hầu như KHÔNG có `%eval`/`%clk`** — đây là gốc rễ của vài bug (mục 10).

Schema mỗi ván (một row), trích trong `spark/jobs/pgn_parse.py`:
`game_id, white, black, white_elo, black_elo, result, eco, opening, time_control, termination, event, game_datetime, plies, has_eval, has_clock, white/black_avg_move_time, white/black_move_time_std, white/black_acpl`.

---

## 5. Batch pipeline — chi tiết từng bước

### 5.1 Bronze ingestion (`deploy/ingest/ingest-bronze-job.yaml`)

K8s Job chạy **trong cluster** stream dump thẳng URL→MinIO bằng `curl -sSL <url> | mc pipe <target>`. Lý do: dữ liệu KHÔNG đi qua laptop (dùng băng thông GCP), KHÔNG lưu full file trên disk pod. Bronze = file `.zst` thô, không đổi (chưa parse). Idempotent: `mc stat` trước, đã có thì skip. Object key partition theo tháng:
`bronze/lichess/standard/rated/year_month=<MONTH>/...pgn.zst`.

### 5.2 Shred — fix bottleneck scale (`spark/jobs/shred_bronze.py`)

**Vấn đề**: `.zst` là file không splittable → Spark đọc 1 file = **1 task duy nhất** = ~62–75h cho một tháng gần đây. Không khả thi.

**Cách giải**: thêm bước "shred" — một pass **chỉ stream-decompress (KHÔNG parse python-chess → nhanh, ~phút cho 30GB)**, cắt theo ranh giới ván (dòng bắt đầu bằng `[Event ` = ván mới), cứ ~30000 ván flush thành một shard `.pgn.gz`. Bronze→Silver sau đó đọc **N shard → N partition → parse song song**. Kết quả: parse một tháng thật **~75 phút → ~4 phút**. `parse_games` không phải sửa gì — chỉ đổi nguồn từ 1 file thành N shard.

### 5.3 Bronze→Silver (`spark/jobs/bronze_to_silver.py` + `pgn_parse.py`)

Job Spark: boto3 list shard keys → `parallelize(keys, numSlices=len(keys))` → `flatMap` mỗi task stream shard → gzip decompress → `parse_games(text_stream)` → Row dicts. **Stream, không bao giờ load full object vào RAM.** Derive `year_month` từ key, `speed` (bullet/blitz/rapid/classical) từ field `event`. Clean: drop null `game_id`, dedupe theo `game_id`. Ghi **Delta** `s3a://silver/games` partition theo `year_month, speed`.

**Logic parser quan trọng** (cùng module dùng cả ở Phase 0 local lẫn trong Spark):

- **ACPL (centipawn loss)**: eval token → centipawn (`float * 100`); mate `#n`/`#-n` clamp về `±mate_cp` (mặc định 1000). Mỗi nước: loss của bên đi = `max(0, mất điểm)`. Trắng (ply lẻ): `loss = prev_eval - cur_eval`. Đen (ply chẵn): `loss = cur_eval - prev_eval` (vì eval theo góc nhìn trắng — đen "được" khi eval giảm). ACPL = trung bình các loss, **chỉ khi `has_eval`**. `max(0, ...)` để không cộng "điểm thưởng" khi đi nước tốt.
- **Move-time**: per side, duration nước = `max(0, prev_clock - cur_clock + increment)`. Increment parse từ `TimeControl` "300+3" → 3.0. Tính `avg` + **population std** (`statistics.pstdev`).
- **Robustness**: `parse_games` bọc mỗi ván trong `try/except: continue` → một ván hỏng (vd đuôi zstd bị cắt) không làm chết cả job.

### 5.4 Silver→Gold features (`spark/jobs/silver_to_gold.py`)

Hai bảng Gold Delta:

`gold/player_features` (1 row/player, có thể theo speed): unpivot mỗi ván thành 2 row (góc nhìn trắng + đen), aggregate: `games_played, wins/draws/losses, win_rate, elo (latest theo datetime), avg_acpl, acpl_std, avg_move_time, move_time_std, opening_diversity (số ECO distinct/entropy), accuracy_vs_rating_gap, last_game_datetime`.

`gold/opening_features` (1 row/ECO): `popularity (count), white_win_rate, black_win_rate, draw_rate, avg_plies, avg_player_rating`.

### 5.5 Point-in-time training set — phần lõi (`spark/jobs/build_training_set.py`)

Đây là phần đáng giá nhất về mặt khái niệm, cũng là chỗ dễ ăn điểm nhất. Khi tạo dữ liệu train cho model phát hiện gian lận, feature lịch sử của một player ở ván X chỉ được phép tính từ các ván trước X — không được để lọt thông tin từ ván tương lai. Cờ vua có sẵn thứ tự thời gian (`game_datetime`) nên đây là ví dụ minh hoạ point-in-time join rất sạch.

Cơ chế (code thật):

```python
player_window = (
    Window.partitionBy("player", "speed")
    .orderBy(F.col("game_datetime").asc_nulls_last(), F.col("game_id").asc_nulls_last())
    .rowsBetween(Window.unboundedPreceding, -1)   # -1 = LOẠI ván hiện tại → không leak
)
```

`rowsBetween(unboundedPreceding, -1)` = tổng hợp **mọi ván trước, trừ ván hiện tại**. Từ window này tính: `games_played_so_far, win_rate_so_far, avg_acpl_so_far, acpl_std_so_far, avg_move_time_so_far, move_time_std_so_far`. Rồi so ván hiện tại với lịch sử:
- `acpl_dev = cur_acpl - avg_acpl_so_far` (ván này chính xác bất thường so với chính mình?)
- `move_time_dev = cur_avg_move_time - avg_move_time_so_far`

Hai cột này chính là tín hiệu nghi vấn: một player bỗng đánh chính xác hơn hẳn hoặc nhịp ra nước đều hơn hẳn so với quá khứ của chính họ. Kết quả ghi xuống Delta `gold/training_set` với dynamic partition overwrite và `mergeSchema=true`.

### 5.6 Cheat model (`model/train_cheat_model.py`)

Mục đích ở đây là chứng minh feature store nuôi được một model thật, chứ không phải khoe kỹ thuật ML. Nên giữ model đơn giản, không giám sát.

- Đọc `gold/training_set` bằng **delta-rs (`deltalake` Python, không phải Spark)** → PyArrow table.
- Filter: `cur_acpl` hợp lệ AND `games_played_so_far >= 5` (cần đủ lịch sử).
- 8 feature: `cur_elo, cur_acpl, acpl_dev, avg_acpl_so_far, acpl_std_so_far, cur_move_time_std, move_time_dev, win_rate_so_far`. NaN impute bằng median (lưu median vào metadata để serving nhất quán).
- `IsolationForest(n_estimators=200, contamination=0.02, random_state=42)`.
- `decision_function` → anomaly_score; `predict == -1` → is_anomaly.
- Ghi `gold/cheat_scores` (Delta) + upload `models/cheat/isoforest.joblib` + `metadata.json` lên MinIO. In top-10 anomaly.

### 5.7 Materialize offline→online (`stream/materialize/materialize_redis.py` + `materialize_cheat.py`)

Job nhẹ (no Spark): đọc Gold Delta bằng delta-rs → ghi Redis hash:
- `offline:player:<player>:<speed>` ← player features.
- `online:cheat:<player>:<speed>` ← anomaly score, is_suspicious, worst game.

### 5.8 Trino + Hive Metastore (`deploy/trino/`)

Trino's `delta_lake` connector **bắt buộc metastore** → deploy thrift Hive Metastore (`apache/hive:4.0.1`) backed by Postgres 16, cấu hình S3A→MinIO. Trino (`trino/trino` chart 1.42.2, Trino 480) 1 coordinator + 1 worker. Việc Trino làm (đúng rubric "Computing/Transformation", không chỉ query):
- `register_tables.sql`: `CALL delta.system.register_table(...)` đăng ký Delta tables sẵn có.
- `dq_checks.sql`: data-quality SQL (no null game_id, win_rate ∈ [0,1], popularity > 0...).
- `transform.sql`: CTAS tạo `gold_opening_summary` — một bảng Delta mới **do Trino ghi** (chứng minh Trino là transformation engine, không chỉ đọc).

---

## 6. Stream pipeline — chi tiết

### 6.1 Collector (`stream/collector/collect_tv.py`)

Mở NDJSON stream của Lichess TV (`requests` stream=True), theo dõi `current_game_id` từ event `featured`, mỗi event `fen` produce 1 message Kafka `lichess.tv.moves` key=game_id value=`{game_id, lm, wc, bc, event_ts}`. Reconnect khi stream đóng (feed long-lived). Heartbeat mỗi N message.

### 6.2 Flink windowed (`flink/jobs/tv_movetime.py`)

PyFlink DataStream — đây là phần "window" được chấm điểm (full 10% thay vì 5%):

1. KafkaSource (latest offsets) → `flat_map` parse → tuple `(game_id, lm, wc, bc, event_ts)`, dùng sentinel `-1` cho clock thiếu.
2. `key_by(game_id)` → `ClockDeltaToMoveTime` (KeyedProcessFunction): giữ **ValueState** `last_wc`/`last_bc`, mỗi nước emit duration = `max(dw, db, 0)` (bên nào clock tụt thì đó là người vừa đi; bỏ increment/reset).
3. `key_by(game_id)` → **`SlidingProcessingTimeWindows(30s, slide 10s)`** → `aggregate` bằng **Welford online algorithm** (`_StatsAgg`: count, mean, M2) + `ProcessWindowFunction` (`_AttachStats`) tính `stddev = sqrt(m2/(count-1))`.
4. `RedisMovetimeWriter` (MapFunction): `hset online:movetime:<game_id> {count, avg, stddev, updated_ts}` + `expire` TTL 3600s (ván cũ tự hết hạn).

Tín hiệu gian lận stream: `stddev` move-time quá thấp = nhịp đánh đều như máy (consistency bất thường) — **không cần chạy engine**.

### 6.3 Các bài toán khó của true streaming — cái nào né, cái nào còn thiếu

True streaming kéo theo một loạt bài toán khó (watermark/late-data, state, exactly-once, fault tolerance, vận hành 24/7). Job Flink này **cố tình đơn giản hoá** đúng theo use case — quan trọng là biết mình né cái nào và vì sao né được.

| Bài toán | Trong job này | Bằng chứng / lý do |
|---|---|---|
| State management | ✅ Có (mức cơ bản) | `ValueState` `last_wc`/`last_bc` keyed theo game_id để suy ra move-time |
| Watermark / late data | ⏭️ Né hẳn | `WatermarkStrategy.no_watermarks()` + `SlidingProcessingTimeWindows` (processing-time, không phải event-time) → khỏi xử lý event đến trễ |
| Exactly-once | ⏭️ Né (chấp nhận at-most-once) | `offsets.latest()`, sink Redis là Map thường (không transactional), `parallelism=1`. Ghi Redis là `hset` ghi đè + TTL nên mất vài cập nhật lúc restart không ảnh hưởng |
| Fault tolerance / recovery | ❌ Chưa làm | phase3.0 ghi rõ "NO checkpointing yet" → Flink restart là mất sạch state |
| Vận hành 24/7 | ⏭️ Chưa đối mặt thật | cụm ephemeral, demo live-stream chạy chung vẫn là TODO |

**Lỗ hổng tiềm ẩn (đề phòng bị đào sâu):**
- **Flink state phình vô hạn**: keyed theo game_id nhưng **không có state TTL/cleanup** cho ván đã kết thúc → chạy lâu thì state ván cũ không bao giờ xóa (Redis có TTL, nhưng *Flink state* thì không). Production cần state TTL hoặc timer để clear.
- **Không checkpoint = không recovery** (đã nêu ở bảng).
- **parallelism=1** → chưa kiểm chứng scale ngang.

**Câu trả lời chuẩn khi phỏng vấn:** "Dùng Flink cho true streaming move-time, nhưng cố tình đơn giản hoá theo use case: processing-time + no watermark (né event-time complexity), at-most-once + Redis overwrite có TTL (né exactly-once vì mất vài cập nhật không sao), hoãn checkpointing. Lên production sẽ thêm **state TTL** (chống state phình), **checkpoint xuống MinIO** (recovery), và cân nhắc **exactly-once sink** nếu nghiệp vụ cần." → cho thấy hiểu các bài toán tồn tại, biết đã né cái nào và vì sao, biết phải thêm gì.

---

## 7. Serving — Feature API (`service/feature_api/app.py`)

FastAPI, redis client khởi tạo trong `lifespan`. Endpoints:

| Endpoint | Nguồn | Trả về |
|---|---|---|
| `GET /health` | Redis ping | status + redis ok |
| `GET /features/player/{player}/{speed}` | `offline:player:*` | feature offline của player |
| `GET /features/movetime/{game_id}` | `online:movetime:*` | timing window live |
| `GET /predict/player/{player}/{speed}` | `online:cheat:*` | anomaly score + is_suspicious + worst game |
| `GET /metrics` | instrumentator | Prometheus RED metrics |

`/metrics` qua `prometheus_fastapi_instrumentator` → Prometheus scrape → Grafana. Ví dụ `/predict`: `{worst_anomaly_score: -0.0236, n_anomalies: 1, n_scored: 6, is_suspicious: true, worst_game_id: "m5KislpY"}`.

---

## 8. Orchestration — Airflow DAG (`dags/batch_pipeline.py`)

Airflow self-hosted trên GKE (Helm chart 1.19.0, Airflow 2.10.5, **KubernetesExecutor** — mỗi task = 1 pod, không celery). DAG `batch_pipeline` (param `months`, default `2013-01`, `schedule=None` cho dev):

```
ingest_bronze → bronze_to_silver → silver_to_gold → build_training_set → train_cheat_model → materialize_cheat
                                          └────────────────────────────→ materialize_redis
```

Operators: `KubernetesPodOperator` (ingest, materialize) + `SparkKubernetesOperator` (các job Spark — tự chờ SparkApplication xong). DAG được **bake vào Airflow image** lúc build.

---

## 9. Infra & cost (`terraform/`)

- GKE **Standard, ZONAL** (rẻ hơn regional), Workload Identity bật, release channel REGULAR, K8s 1.35.
- 2 node pool: `core-pool` (always-on, `e2-standard-4`, count=1, host MinIO/Kafka/Redis) + `spot-pool` (Spot VMs, autoscale **min 0** max 3–8, có taint `workload-tier=spot:NoSchedule` cho Spark/Flink burst).
- Artifact Registry `lichess-fs`; tfstate ở GCS backend bucket.
- **Kỷ luật chi phí**: cluster **ephemeral** — bật lúc làm/demo, `make destroy` sau mỗi session. Spot + autoscale-to-0 + `pd-standard` boot disk (tránh chạm SSD quota). Mục tiêu < $100 trong $300 free credit.

---

## 10. Bug đã gặp và cách xử lý

Phần này là chỗ học được nhiều nhất, mỗi mục là một bug có thật cùng cách sửa, đều lấy từ code và docs trong repo.

### Dữ liệu & parser

**B1. Dev month không có `%eval`/`%clk`.** Phase 0 dùng `2013-01` (nhỏ, tải nhanh) nhưng tháng đó hầu như không có annotation → **toàn bộ logic ACPL + move-time chưa từng chạy thật**. Hệ quả dây chuyền: phải (a) re-run Phase 0 trên `2024-12` để đo coverage thật, (b) viết **unit test** (`tests/test_pgn_parse.py`, phase 2.3-validate) feed PGN tự chế có clock/eval biết trước, assert ACPL/move-time **đúng từng con số** trước khi demo. Bài học: *dev data ≠ demo data; nếu dev data không kích hoạt code path quan trọng, phải test riêng code path đó.*

**B2. `download.py` tải nguyên 30GB rồi mới parse.** Lãng phí khi chỉ cần `--max-games`. Fix (phase0-followup): stream-from-URL — `requests.get(stream=True)` → `zstandard.stream_reader` → `TextIOWrapper` → `read_game` loop, dừng sớm ở max-games, KHÔNG ghi full file ra disk (`--save-download` mới tee). Refactor `parse_games` nhận *bất kỳ text stream* → cùng code cho cả local file lẫn URL stream.

**B3. `moves_count` thực ra là plies.** `game.end().ply()` trả **nửa nước** (half-moves), không phải nước đầy đủ. Đổi tên field `plies` mọi nơi + comment "full moves ≈ plies/2".

**B4. `profile.py` shadow stdlib `profile`.** Đổi tên `report.py` để không che module chuẩn của Python.

**B5. Đuôi zstd bị cắt (range-capped months).** Khi dùng `ingest-bronze-capped` (HTTP Range lấy ~150MB đầu), file `.zst` cụt đuôi → ván cuối hỏng. `parse_games` `try/except: continue` mỗi ván nên nuốt ván hỏng cuối, không chết job.

### Spark / Delta / scale

**B6. 1 file `.zst` = 1 Spark task = ~62–75h/tháng.** File không splittable. Fix: bước **shred** (mục 5.2) cắt thành shard game-aligned → N partition song song. **75 phút → 4 phút.** Shred cố tình KHÔNG parse (chỉ decompress) nên nhanh.

**B7. `spark.jars.packages` flaky (ivy/network).** Tải jar lúc runtime hay fail. Fix: **bundle jar vào image** với version compat tường minh: Spark `3.5.2` + Delta `3.2.1` (`delta-spark_2.12` + `delta-storage`) + `hadoop-aws:3.3.4` + `aws-java-sdk-bundle:1.12.262`.

**B8. Silver write XÓA các tháng khác.** `mode("overwrite")` mặc định wipe toàn bộ partition. Fix: `option("partitionOverwriteMode", "dynamic")` → chỉ ghi đè partition của tháng đang chạy. (phase 2.3)

**B9. Executor không lên spot-pool.** Spot pool có taint → executor không schedule. Fix: thêm `toleration` cho `workload-tier=spot:NoSchedule` + `nodeSelector cloud.google.com/gke-nodepool: spot-pool` trong SparkApplication → demo được autoscale 0→N + tiết kiệm chi phí.

### Kubernetes / platform

**B10. Operator crashloop trên K8s 1.35.** Phiên bản Strimzi/Spark/Flink operator cũ crashloop khi detect version. Fix: chọn bản 2.x hiện hành đã verify (Spark Operator `2.5.0`, Flink Operator `1.10.0` + cert-manager `1.20.2`), rồi mới pin `--version`. Bài học lặp lại 3 lần → thành reflex "operator mới, verify Running 1/1, rồi pin".

**B11. Orphaned GCP PD disk.** `terraform destroy` KHÔNG xóa PVC/PD provision động → đĩa 20GB mồ côi vẫn tính tiền. Fix: `kubectl -n minio delete pvc --all` (và `-n trino`) **trước** `make destroy`. Ghi vào runbook teardown.

**B12. Local docker build OOM crash máy.** Build image nặng (Spark/Flink) local làm treo WSL. Fix: build **mọi image qua Cloud Build** (`gcloud builds submit`).

**B13. Apache archive mirror timeout.** Tải Airflow Helm chart từ archive.apache.org hay timeout từ Cloud Build/WSL. Fix: tải chart `1.19.0` từ **GitHub releases** thay vì mirror.

**B14. Core node chật.** Một `e2-standard-4` gánh MinIO+Kafka+Redis+collector+Flink+operators; thêm Airflow + Spark batch là hết CPU. Fix vận hành: scale-down trước batch run — `kubectl -n trino scale deploy trino-coordinator trino-worker --replicas=0`, xóa flinkdeployment, scale collector về 0.

**B15. Airflow worker thiếu RBAC.** Task pod (KubernetesExecutor) không tạo được SparkApplication cross-namespace. Fix: `deploy/airflow/airflow-rbac.yaml` — Role/RoleBinding cho `sparkapplications.sparkoperator.k8s.io` + `pods` (+ pods/log) trong namespace `spark` và `minio`.

### Flink (subtle nhất)

**B16. Map ghi Redis bị Flink prune.** `RedisMovetimeWriter` là MapFunction không có downstream sink → optimizer của Flink **cắt bỏ** nó khỏi execution graph → **không có gì ghi vào Redis** dù job RUNNING. Fix: thêm terminal sink `.print()` sau map để giữ nó trong graph. (Comment thật trong `tv_movetime.py`.) Đây là loại bug "chạy không lỗi nhưng không có tác dụng" — khó nhất để phát hiện.

---

## 11. Còn TODO (đừng nói đã xong)

- [ ] Full-scale demo run (~120GB, 4 tháng gần đây) cho mốc ">100GB".
- [ ] Live-stream demo end-to-end (collector + Flink + online lookup chạy chung một lúc).
- [ ] CI/CD (GitHub Actions) + DAG có cron lịch thật (hiện manual trigger).
- (Stretch) Stockfish-in-Flink để có accuracy real-time (hiện stream timing-only).

---

## 12. Cách trình bày khi phỏng vấn (cheat sheet)

- **Một câu**: "Lakehouse + feature store end-to-end trên 100GB+ dữ liệu cờ Lichess: batch (Spark/Delta/Trino) + streaming (Kafka/Flink windowed), point-in-time-correct features nuôi cheat-detection, online serving qua Redis+FastAPI, điều phối Airflow, deploy GKE bằng Terraform."
- **Điểm kỹ thuật sâu nhất để khoe**: (1) point-in-time window `rowsBetween(unboundedPreceding, -1)` chống leak; (2) shred fix scale 75min→4min; (3) Welford online stddev trong Flink window; (4) bug Flink prune map — chứng tỏ hiểu execution graph.
- **Khi bị hỏi "đã chạy 100GB chưa"**: thành thật — "kiến trúc + pipeline verified trên tháng thật có eval/clock; full-scale run là bước cuối, đã thiết kế shred + spot autoscale để gánh".
- **Câu chuyện trade-off**: chọn GKE self-hosted thay Dataproc/Composer để (a) trong $300 free credit, (b) vẫn thoả rubric "deploy thật". Đổi lại: tự quản operator + RBAC + capacity (các bug B10–B15).

---

## Related

- [[plan.md]] — kế hoạch gốc (rubric mapping, feature design)
- [[project_de_feature_store]] (memory)
- Repo: `~/Repos/lichess-feature-store` (WSL) — README.md + docs/phase*.md là source of truth
- CV: project này nằm trong `cv_expanded.tex` và `cv_nttdata.tex`
