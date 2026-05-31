---
title: Phase 0 — Cursor Prompt (PGN Parsing Spike)
type: cursor-prompt
phase: 0
created: 2026-05-30
---

# Phase 0 — Cursor Prompt (PGN Parsing Spike)

Paste phần dưới (trong khối) vào Cursor. Mục tiêu: de-risk việc parse PGN trước khi dựng infra. Local-only, KHÔNG Spark, KHÔNG cloud.

---

## CONTEXT

I'm building a Data Engineering "Feature Store" course project on Lichess chess data (Lakehouse + batch/streaming, later deployed on GKE). This is **Phase 0: a local spike to de-risk PGN parsing** before any Spark/cloud work. Do NOT add Spark, Docker, cloud, or any infra yet. Keep it a single local Python project.

## GOAL

Build a small local Python tool that downloads a Lichess PGN dump, parses games into a flat structured schema, writes Parquet, and prints a data-profile report. The point is to answer: what's in the data, what % of games have engine `%eval` and clock `%clk` annotations, and how fast can we parse (to extrapolate feasibility at 100GB).

## TASKS

1. **Project setup**
   - Python project with `uv` or `venv` + `requirements.txt`.
   - Deps: `python-chess`, `zstandard`, `pyarrow`, `pandas`, `requests`, `tqdm`.

2. **Download a SMALL dump**
   - Use an early, small month so the file is tiny (tens of MB), e.g. `https://database.lichess.org/standard/lichess_db_standard_rated_2013-01.pgn.zst`.
   - Make the URL / a local path a CLI arg. Support reading a local `.pgn.zst` too.
   - Add a `--max-games N` flag so we can cap parsing for quick iteration.

3. **Streaming parse (memory-safe)**
   - Stream-decompress the `.zst` with `zstandard` (do NOT load the whole file into memory).
   - Parse games incrementally with `python-chess` (`chess.pgn.read_game` in a loop).
   - Stop early when `--max-games` reached.

4. **Extract per-game flat schema** (one row per game):
   - `game_id` (parse from the `[Site "https://lichess.org/XXXX"]` header)
   - `white`, `black`, `white_elo` (int), `black_elo` (int)
   - `result` (`1-0` / `0-1` / `1/2-1/2`)
   - `eco`, `opening`, `time_control`, `termination`, `event` (to derive speed: bullet/blitz/rapid/classical)
   - `moves_count` (int)
   - `has_eval` (bool — does any move have a `[%eval ...]` comment?)
   - `has_clock` (bool — does any move have a `[%clk ...]` comment?)
   - For games where `has_eval` is true: also compute a simple **ACPL proxy** (average centipawn loss) per side — `white_acpl`, `black_acpl`. Mate scores: clamp to a large cp value (e.g. ±10000 → cap at e.g. 1000cp for averaging, document the choice). If too complex, leave these nullable but still implement the eval-presence detection.

5. **Write output**
   - Write parsed rows to `output/games.parquet` (pyarrow).
   - Partition not needed at this scale.

6. **Profile report** — print to stdout AND write `output/profile.md`:
   - Total games parsed, parse duration, **games/sec** (and extrapolated time for 30M games).
   - `% has_eval`, `% has_clock`.
   - Distribution of `event`/speed category counts.
   - Elo distribution (min/max/mean/percentiles) for white_elo.
   - Top 10 `eco`/`opening` by frequency.
   - Print the inferred schema + 5 sample rows.

7. **README.md** — how to install and run, with example commands.

## TECH CONSTRAINTS

- Single local Python project. No Spark, no Docker, no cloud, no orchestrator.
- Stream the compressed file — must handle a 30GB `.zst` without loading it all (even though the spike uses a small file).
- Clean, typed functions; small modules (`download.py`, `parse.py`, `profile.py`, `main.py`).
- Use `tqdm` for progress.

## ACCEPTANCE CRITERIA

- `python main.py --url <lichess-url> --max-games 50000` runs end-to-end and produces `output/games.parquet` + `output/profile.md`.
- Report clearly states the `% has_eval` and `% has_clock` numbers and the parse throughput (games/sec).
- Code does not load the whole decompressed PGN into memory.
- README documents how to point it at a recent large month later.

## OUT OF SCOPE (do NOT do)

- No Spark, no MinIO/Delta, no Kafka/Flink, no Airflow, no GKE/Terraform.
- No ML model, no feature engineering beyond the per-game fields above.
- No streaming/live-games API.

---

## Sau khi Cursor chạy xong — đem kết quả về cho strategist

Báo lại các số sau (quyết định kiến trúc các phase sau phụ thuộc vào chúng):

- `% has_eval` — quyết định accuracy/ACPL features khả thi tới đâu (batch path).
- `% has_clock` — quyết định timing features.
- games/sec — extrapolate feasibility ở 100GB, ước lượng cluster size Spark.
- Bất kỳ schema quirk nào (field thiếu, format lạ, games không parse được).
