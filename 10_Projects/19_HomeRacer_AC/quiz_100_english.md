---
tags: [project, job-hunt, interview, data-engineer, quiz, home-credit, english]
status: active
created: 2026-08-05
event: AC 2026-08-06
---

# 100 MCQ — Applied, Scenario-Based (English)

> Different in kind from the earlier quizzes. **Almost no definition recall here.** These are: read this table · diagnose this symptom · choose between designs · find the flaw · do the arithmetic · what do you do next.
> That is closer to how an assessment centre actually tests you.
> Answer key with reasoning at the end. Answers evenly spread across A/B/C/D.

---

## SECTION A — Read the table (Q1-12)

### Table 1 — monthly account snapshots

| customer_id | month | balance |
|---|---|---|
| C001 | 2026-01 | 1200 |
| C001 | 2026-02 | 900 |
| C002 | 2026-01 | 4500 |
| C002 | 2026-02 | 4500 |
| C002 | 2026-02 | 4500 |

**1.** What is the grain of this table?
- A. One row per customer
- ==B. One row per customer per month==
- C. One row per transaction
- D. One row per balance change

**2.** Which observation deserves investigation first?
- A. C001's balance decreased
- B. C002's balance stayed flat across months
- ==C. C002 has two identical rows for 2026-02==
- D. The table has only two customers

**3.** A colleague runs `SELECT SUM(balance)` and reports total exposure of 15,600. What is the main problem with that number?
- A. Nothing — it is a valid total
- ==B. It sums across months, so the same customer is counted repeatedly==
- C. It should be an average instead
- D. Balance cannot be summed at all

### Table 2 — transaction extract

| txn_id | amount | currency | processed_at  |
| ------ | ------ | -------- | ------------- |
| T1     | 250000 | VND      | 1712000000000 |
| T2     | 45     | USD      | 1712000001000 |
| T3     | 180000 | VND      | 1712000002000 |

**4.** A teammate proposes `SUM(amount)` to get total transaction value. The strongest objection is:
- A. The amounts are stored as integers
- B. The currency column should be dropped first
- ==C. It mixes VND and USD, producing a number with no meaning==
- D. Transaction IDs are not sequential

**5.** What unit is `processed_at` in?
- A. Seconds
- B. Milliseconds
- ==C. Microseconds==
- D. Minutes

**6.** Based on the timestamps, how far apart are T1 and T3?
- ==A. 2 milliseconds==
- B. 2 seconds
- C. 2 minutes
- D. Cannot be determined

### Table 3 — account status

| account_id | status | balance | closed_at |
|---|---|---|---|
| A1 | ACTIVE | 500 | null |
| A2 | CLOSED | 0 | 2026-03-01 |
| A3 | CLOSED | 320 | 2026-04-11 |
| A4 | ACTIVE | -50 | null |

**7.** Which row most clearly violates an expected business rule?
- A. A1
- B. A2
- ==C. A3, because a closed account still holds a balance==
- D. A4

**8.** Is row A4 necessarily an error?
- A. Yes — balances can never be negative
- ==B. No — it may be legitimate if the product allows overdraft or reversal entries==
- C. Yes — active accounts must have positive balances
- D. Cannot be assessed without more columns

**9.** The `closed_at` column is null for both ACTIVE rows. The best interpretation is:
- A. Data is missing and should be backfilled
- B. The pipeline failed to populate the column
- C. The rows should be excluded from analysis
- ==D. Null carries meaning here — the account is not closed==

### Table 4 — partner store approval rates

| store_id | applications | approved | approval_rate |
|---|---|---|---|
| S1 | 120 | 60 | 0.50 |
| S2 | 80 | 78 | 0.98 |
| S3 | 95 | 40 | 0.42 |
| S4 | 12 | 12 | 1.00 |

**10.** Which store warrants investigation most strongly?
- A. S1
- ==B. S2 — a very high rate on a substantial volume==
- C. S3
- D. S4

**11.** Why is S4 weaker evidence than S2, despite a higher rate?
- ==A. Because 12 applications is too small a sample to be conclusive==
- B. Because S4 has fewer approvals in absolute terms
- C. Because rate matters only above 0.99
- D. Because S4 may be a new store

**12.** You want to compare stores fairly. The most useful next step is:
- A. Rank purely by approval_rate
- B. Remove all stores with fewer than 100 applications
- ==C. Establish the portfolio-wide baseline rate and flag statistically significant deviations==
- D. Sort by application volume

---

## SECTION B — Units and plausibility in context (Q13-24)

**13.** A monitoring dashboard reports `avg_response_time = 0.8`. Before acting, you must establish:
- ==A. Whether the unit is seconds or milliseconds==
- B. Whether it is a mean or a median
- C. The sample size
- D. The time window

**14.** A `loan_term` column contains values 6, 12, 24, and 360. The 360 most likely means:
- A. A data entry error
- B. Days rather than months
- ==C. A 30-year term expressed in months==
- D. A sentinel value

**15.** A `credit_score` column ranges 300 to 850 for most rows, but some rows contain 0. Those zeros most likely represent:
- A. Genuinely the worst possible customers
- B. Missing data encoded as zero
- ==C. Customers with no credit history, scored correctly==
- D. A different scoring scale

**16.** Treating those zeros as real scores in an average would:
- A. Have negligible effect
- B. Improve accuracy by including more data
- C. Only affect the median
- ==D. Drag the mean down and misrepresent portfolio quality==

**17.** A field named `interest_rate` contains 0.185 in some rows and 18.5 in others. This indicates:
- ==A. Two different sources using decimal and percentage conventions==
- B. Tiered pricing
- C. Rounding differences
- D. Promotional versus standard rates

**18.** A daily active user count rises from 40,000 to 41,000 to 39,500 to 820,000. Your first hypothesis should be:
- A. A viral marketing success
- ==B. A pipeline problem such as a duplicated load==
- C. Seasonal behaviour
- D. A competitor outage

**19.** A `disbursement_date` is earlier than the `application_date` on 3% of rows. The most likely cause is:
- A. Customers applying retroactively
- B. Pre-approved offers
- ==C. A timezone or field-mapping error between two systems==
- D. Data entry by branch staff

**20.** A pipeline SLA states "data available by 07:00". You discover the source system exports at 06:55 UTC while the business operates in UTC+7. The real implication is:
- A. The SLA is comfortably met
- ==B. The export arrives at 13:55 local time, so the SLA is badly missed==
- C. Timezone is irrelevant to SLAs
- D. The SLA should be measured in UTC only

**21.** A column `duration_ms` has a minimum of -1. This most likely indicates:
- A. Extremely fast processing
- B. A valid measurement
- C. A compression artefact
- D. A sentinel for "not measured", or reversed timestamp subtraction

**22.** A file lands with 2,000,000 rows on weekdays and 4,000,000 on Mondays. The most reasonable first explanation is:
- ==A. Weekend activity is being accumulated and delivered on Monday==
- B. Monday is genuinely twice as busy
- C. The pipeline duplicates on Mondays
- D. A reporting error

**23.** Your teammate says "there are no nulls in this column, so the data is clean." The correct response is:
- A. Agreed — null-free means clean
- ==B. Nulls may be encoded as empty strings, zeros, or placeholder dates instead==
- C. Nulls only matter for numeric columns
- D. Null checks should be run weekly

**24.** The safest general practice for catching unit errors before they reach production is:
- A. Peer review of SQL
- B. Reading source documentation carefully
- C. Automated range assertions with expected min/max per column
- D. Relying on column data types

---

## SECTION C — Assumption scenarios (Q25-34)

**25.** You're asked for "the number of active customers." No definition is provided. The strongest response is:
- A. Ask and wait until someone defines it
- B. Use the most common industry definition without comment
- ==C. Propose a concrete definition, state it clearly, and note it can be adjusted==
- D. Produce several versions and let them choose

**26.** You define "active" as "transacted in the last 30 days" and it excludes 42% of the customer base. The right reaction is:
- A. Proceed — the definition is defensible
- ==B. Flag it, because excluding 42% suggests the definition may not match business intent==
- C. Change to 90 days silently
- D. Report both numbers without comment

**27.** During a group discussion, a teammate asserts a figure you cannot verify. The most constructive move is:
- A. Accept it to keep the discussion moving
- B. Challenge whether they are qualified to know
- ==C. Ask what the figure is based on, then note the design depends on it==
- D. Ignore it and design for both cases

**28.** You must design without knowing the data volume. The best approach is:
- A. Assume the largest plausible scale to be safe
- B. Refuse to design until volumes are provided
- C. Design for a small scale and revisit later
- ==D. State an assumed scale, design for it, and identify which component breaks first if it is ten times larger==

**29.** Which is the strongest formulation of an assumption?
- A. "I assumed the data was fine."
- B. "I made some standard assumptions."
- ==C. "I assumed daily batch is sufficient; if same-day intervention is needed, the ingestion layer changes to streaming."==
- D. "I assumed daily batch."

**30.** Two analysts report different churn rates. The most probable cause is:
- A. Different query engines
- ==B. Different implicit definitions of the observation window or population==
- C. Floating-point differences
- D. One of them made a typo

**31.** In a case discussion, stating assumptions early primarily helps because:
- A. It demonstrates knowledge of terminology
- ==B. It lets the group correct course before effort is spent building on a wrong premise==
- C. It fills discussion time productively
- D. It shifts responsibility to whoever does not object

**32.** You realise mid-discussion that an assumption made 20 minutes ago was wrong. The best action is:
- ==A. Say so immediately and identify what part of the design it affects==
- B. Continue, since changing course wastes time
- C. Mention it only if someone asks
- D. Note it in the final slide

**33.** A stakeholder says "just give me the number, I don't need the caveats." The professional response is:
- A. Comply — they own the decision
- ==B. Give the number with a one-line caveat, because the caveat changes how it should be used==
- C. Refuse until they accept the caveats
- D. Give a range instead

**34.** The main risk of adopting a definition from an existing dashboard without checking is:
- A. It may be slow to query
- B. It may use a deprecated table
- C. It may encode assumptions that were valid for a different question
- D. It may not be documented

---

## SECTION D — Diagnose the symptom (Q35-48)

**35.** A daily revenue figure suddenly doubles, while transaction count remains flat. The most likely cause is:
- A. A price increase
- ==B. Currency conversion applied twice, or a join duplicating amounts==
- C. Genuine growth
- D. A tax change

**36.** A dashboard shows a customer count higher than the number of rows in the customer table. Most likely:
- A. The count includes prospects
- B. Deleted customers are included
- ==C. The count runs on a joined dataset that fanned out==
- D. The dashboard caches stale results

**37.** A streaming job runs with no errors, consumes from Kafka, but the serving store never updates. The most likely cause is:
- A. The topic has no data
- B. The write step is not connected to a terminal sink, so the optimiser removed it
- C. The serving store is full
- D. The job is under-provisioned

**38.** Consumer lag grows steadily and never recovers. This indicates:
- A. The producer stopped
- ==B. The topic has too few partitions or the consumer is too slow — throughput mismatch==
- C. Messages are corrupted
- D. Retention is too short

**39.** Consumer lag spikes every day at 09:00 and drains by 09:20. This indicates:
- A. A recurring bug
- B. A broken consumer
- ==C. Normal morning traffic being absorbed by the buffer, which is the broker doing its job==
- D. Insufficient retention

**40.** A stream processing job's memory grows continuously until it is killed, restarts, and repeats. The most likely cause is:
- A. A memory leak in the framework
- ==B. Keyed state accumulating without TTL for keys that never become active again==
- C. Too many partitions
- D. Checkpoint files filling the disk

**41.** After a Flink job restarts, aggregated counts are lower than before the restart. Most likely:
- A. Data was lost in Kafka
- B. The window size changed
- ==C. Checkpointing is not enabled, so state was lost and rebuilt from empty==
- D. The sink rejected writes

**42.** A batch job that normally takes 20 minutes suddenly takes 4 hours, with one task still running while all others finished. This is:
- ==A. Data skew — one partition holds disproportionate data==
- B. Network failure
- C. Insufficient cluster memory
- D. A scheduling bug

**43.** A query over a partitioned table becomes progressively slower each month, though data volume per month is constant. Most likely:
- A. The table needs an index
- B. The query is not filtering on the partition column, so it scans everything
- C. Compression degraded
- D. The metastore is slow

**44.** Reads from a data lake become slow after a streaming job starts writing to it every few seconds. Most likely:
- A. Write locks
- ==B. The small file problem — many tiny files raise per-file overhead==
- C. Schema conflicts
- D. Network saturation

**45.** A pipeline produces correct results when run manually but duplicates rows when run by the scheduler. Most likely:
- ==A. The scheduler runs it twice, and the write is not idempotent==
- B. The scheduler uses different credentials
- C. Manual runs use a different dataset
- D. Timezone differences

**46.** Model accuracy is excellent in training and poor in production, with no code differences. The most likely cause is:
- A. Insufficient training data
- B. Wrong hyperparameters
- ==C. Data leakage — training features used information unavailable at prediction time==
- D. Production hardware differences

**47.** Feature values served by the API differ slightly from those used in training. This is:
- A. Expected behaviour
- ==B. Training-serving skew, typically from two separate implementations of the same feature==
- C. A rounding issue
- D. A caching problem

**48.** An hourly report is missing the last 15 minutes of every hour, consistently. Most likely:
- ==A. The report is scheduled before the ingestion window closes==
- B. Data is being dropped
- C. The window function is wrong
- D. Users are misreading the report

---

## SECTION E — Design choices and trade-offs (Q49-62)

**49.** A collections team calls at-risk customers each morning. The appropriate architecture is:
- A. Streaming with sub-second latency
- ==B. Daily batch scoring, since the action happens on a daily cycle==
- C. On-demand computation per request
- D. Real-time with a five-minute refresh

**50.** A system must decline fraudulent card transactions before authorisation completes. This requires:
- A. Nightly batch
- B. Hourly micro-batch
- ==C. Streaming with low-latency serving, because the decision is inside the transaction window==
- D. On-demand lake queries

**51.** A team needs both historical features (6-month payment history) and real-time features (transactions in the last 10 minutes). The right design is:
- ==A. Streaming only, replaying all history when needed==
- B. Batch only, running every 10 minutes
- C. Two paths writing to a shared serving store at different refresh rhythms
- D. Compute everything on demand at request time

**52.** Your team already runs everything on Spark and Delta, and needs near-real-time ingestion with roughly one-minute freshness. The most pragmatic choice is:
- A. Introduce Flink for lower latency
- B. Introduce Kafka Streams
- C. Build a custom consumer
- ==D. Spark Structured Streaming, since one minute is well within its range and it reuses existing skills==

**53.** You need single-digit millisecond latency and complex per-entity state. The appropriate processor is:
- ==A. Flink==
- B. Spark Structured Streaming
- C. Airflow
- D. Trino

**54.** A small team wants stream processing but has no capacity to operate another platform. Their Kafka cluster already exists. The best fit is:
- A. Flink on Kubernetes
- B. Spark on YARN
- C. A managed cloud warehouse
- ==D. Kafka Streams, deployed as an ordinary application==

**55.** A dashboard must aggregate two billion rows by region with sub-second response. The right serving layer is:
- A. Redis
- B. PostgreSQL
- C. A real-time OLAP engine such as ClickHouse
- D. Object storage queried directly

**56.** An API must return one customer's precomputed risk score in under 5 ms. The right serving layer is:
- A. A columnar warehouse
- ==B. Redis or an equivalent key-value store==
- C. A data lake with predicate pushdown
- D. A search engine

**57.** You must join a 500 GB fact table with a 2 MB lookup table in Spark. The efficient approach is:
- A. Repartition both tables on the join key
- B. Sort both before joining
- C. Increase executor memory
- D. Broadcast the small table to every executor, avoiding a shuffle

**58.** A pipeline occasionally reruns the same day's data. To keep results correct you should:
- A. Add a deduplication job afterwards
- B. Prevent reruns through scheduler configuration
- C. Alert on duplicates
- ==D. Make the write idempotent using partition overwrite or upsert on a business key==

**59.** Storage costs are rising rapidly on a table queried mostly by recent date. The most effective change is:
- A. Switch to a row-based format
- B. Reduce the replication factor
- C. Partition by date and apply retention or tiering to older partitions
- D. Compress with a stronger algorithm only

**60.** A source system will change its schema next month, adding two columns. To minimise disruption you should:
- A. Freeze the pipeline until the change is complete
- B. Use a format and table format supporting schema evolution, and validate against a data contract
- C. Rebuild the pipeline after the change
- D. Ignore the new columns permanently

**61.** Analysts keep querying the operational database directly and occasionally slow it down. The correct structural fix is:
- A. Add query timeouts
- B. Restrict analyst permissions
- ==C. Replicate changes into an analytical platform via CDC and point analysts there==
- D. Add read replicas and allow direct access

**62.** A feature must be identical during training and serving. The most reliable way to guarantee that is:
- A. Document the definition thoroughly
- B. Review both implementations carefully
- C. Test both regularly
- D. Compute it once and serve both paths from a single definition

---

## SECTION F — Find the flaw in the statement (Q63-72)

**63.** "We use exactly-once semantics, so messages are never processed more than once."
- A. Correct as stated
- ==B. Wrong — exactly-once guarantees the effect is as-if-once; reprocessing still occurs physically==
- C. Wrong — exactly-once is impossible in distributed systems
- D. Wrong — it applies only to batch

**64.** "Kafka guarantees message ordering, so our sequence-dependent logic is safe."
- A. Correct
- B. Wrong — Kafka guarantees no ordering at all
- ==C. Wrong — ordering holds only within a partition, so it depends on the message key==
- D. Wrong — ordering requires exactly-once enabled

**65.** "We enabled checkpointing, so we have end-to-end exactly-once."
- A. Correct
- ==B. Wrong — checkpointing protects internal state; the sink must also be transactional or idempotent==
- C. Wrong — checkpointing is only for batch jobs
- D. Wrong — checkpointing prevents all failures

**66.** "Our average latency is 150 ms, so users have a fast experience."
- A. Correct
- B. Wrong — latency should be measured in throughput terms
- C. Wrong — 150 ms is inherently slow
- ==D. Wrong — the mean hides the tail; P95 and P99 determine actual user experience==

**67.** "We added ten more workers, so each request will now be faster."
- A. Correct
- ==B. Wrong — more workers raise aggregate throughput, not the latency of an individual request==
- C. Wrong — adding workers always slows systems down
- D. Wrong — this only applies to batch systems

**68.** "The column has no nulls, so we can trust it."
- A. Correct
- ==B. Wrong — absence of nulls says nothing about correctness, and missing values may be encoded as zeros or placeholders==
- C. Wrong — nulls are always encoded as empty strings
- D. Wrong — null checks are unnecessary

**69.** "Redis is our online store, so our features are always current."
- A. Correct
- ==B. Wrong — Redis holds precomputed values whose freshness is bounded by the refresh cadence==
- C. Wrong — Redis cannot store features
- D. Wrong — Redis is only a cache and loses data constantly

**70.** "We skip malformed records with a try/except, so bad data can't hurt us."
- A. Correct
- ==B. Wrong — skipping silently loses data with no visibility; a dead letter queue preserves and surfaces it==
- C. Wrong — malformed records should crash the pipeline
- D. Wrong — try/except cannot catch parsing errors

**71.** "Streaming is the modern approach, so we should use it for all pipelines."
- A. Correct
- B. Wrong — streaming is only for small data
- ==C. Wrong — the choice depends on how quickly the downstream action must occur; batch is simpler and cheaper when daily is enough==
- D. Wrong — streaming cannot handle historical data

**72.** "We ran the job twice by accident but the data looks fine, so we're safe."
- A. Correct
- ==B. Wrong — it looks fine only if the write was idempotent; otherwise duplication may be invisible at a glance==
- C. Wrong — running twice always corrupts data
- D. Wrong — this can only be verified by the scheduler logs

---

## SECTION G — Do the arithmetic (Q73-82)

**73.** A consumer processes one record in 2 ms, single-threaded. Maximum throughput is approximately:
- A. 50 records/second
- B. 200 records/second
- ==C. 500 records/second==
- D. 2,000 records/second

**74.** You batch 100 records and process the batch in 50 ms. Throughput is roughly:
- A. 500 records/second
- B. 1,000 records/second
- ==C. 2,000 records/second==
- D. 5,000 records/second

**75.** In Q74, the first record in each batch waits for the batch to fill. If records arrive at 1,000/second, that added wait is about:
- A. 10 ms
- B. 50 ms
- C. 100 ms
- D. 1 second

**76.** A topic receives 10,000 messages/second. One consumer handles 3,000/second. The minimum number of consumers needed is:
- A. 2
- B. 3
- ==C. 4==
- D. 10

**77.** In Q76, the topic has only 2 partitions. Adding a fourth consumer will:
- A. Increase throughput proportionally
- B. Reduce latency
- ==C. Do nothing — parallelism is capped by partition count, so two consumers sit idle==
- D. Cause message loss

**78.** A sliding window of 60 seconds with a 15-second slide produces output:
- A. Every 60 seconds
- ==B. Every 15 seconds, each covering the previous 60 seconds==
- C. Every 15 seconds, each covering 15 seconds
- D. Continuously

**79.** A tumbling window of 5 minutes over a stream of 200 events/second aggregates approximately how many events per window?
- A. 1,000
- B. 12,000
- C. 60,000
- D. 200,000

**80.** Kafka retains 7 days at 5,000 messages/second, each 1 KB, with replication factor 3. Approximate raw storage required is:
- A. About 3 TB
- B. About 9 TB
- C. About 30 TB
- D. About 90 TB

**81.** A job scans 500 GB, but the query only needs 3 of 120 columns. Switching from CSV to a columnar format could plausibly reduce scanned volume to roughly:
- A. 12 GB
- B. 250 GB
- C. 400 GB
- D. No reduction

**82.** A batch takes 75 minutes on one task. Shredding the input into 20 parallel tasks, with perfect distribution and no overhead, gives approximately:
- A. Under 1 minute
- ==B. About 4 minutes==
- C. About 15 minutes
- D. About 40 minutes

---

## SECTION H — Failure scenarios: what do you do (Q83-94)

**83.** A consumer crashes repeatedly on the same offset. Your immediate action is:
- A. Delete the topic
- B. Increase consumer memory
- C. Skip the offset manually and move on
- ==D. Route the failing message to a dead letter queue, commit, and let the stream continue==

**84.** After doing so, the next thing you must add is:
- A. More partitions
- ==B. An alert on dead letter queue depth, so silent accumulation is visible==
- C. A larger retention window
- D. A second consumer group

**85.** A transient network timeout causes a write to fail. The correct handling is:
- A. Retry with exponential backoff
- ==B. Send to the dead letter queue immediately==
- C. Fail the entire job
- D. Ignore and continue

**86.** A malformed JSON payload causes a parse failure. The correct handling is:
- A. Retry indefinitely
- B. Retry with backoff
- ==C. Send to the dead letter queue, since retrying will never succeed==
- D. Crash the job to force attention

**87.** Your pipeline wrote partial results before crashing mid-run. To recover safely you need:
- A. Manual cleanup of the partial data every time
- ==B. An idempotent write, so rerunning produces the correct final state regardless of the partial write==
- C. To restart from a different source
- D. To disable retries

**88.** A logic bug corrupted a derived table for the last 14 days. Recovery is possible mainly because:
- A. The warehouse keeps backups
- B. The team documented the change
- ==C. Raw source data was retained unmodified, so the pipeline can be rerun over that period==
- D. The bug was small

**89.** A Flink job with 30-second checkpoints crashes 25 seconds after the last checkpoint. On restart it will:
- A. Lose all state permanently
- ==B. Restore from the last checkpoint and reprocess roughly 25 seconds of data==
- C. Start from the beginning of the topic
- D. Skip the missing 25 seconds

**90.** In Q89, reprocessing 25 seconds of data is safe provided:
- ==A. The output sink is idempotent or transactional==
- B. Kafka retention exceeds 25 seconds
- C. The window is smaller than 25 seconds
- D. Checkpoints are stored locally

**91.** A schema change upstream breaks parsing for 100% of incoming messages. The right immediate response is:
- ==A. Let every message flow to the dead letter queue and alert, then fix the parser==
- B. Silently skip all messages
- C. Delete the topic and restart
- D. Disable the consumer indefinitely

**92.** Your online store and offline store disagree on a feature value. The first thing to check is:
- A. Network latency between them
- B. Redis memory pressure
- ==C. Whether the materialisation job succeeded on its last run==
- D. Whether the model is stale

**93.** A downstream team reports missing data for one day last month. Your investigation should begin with:
- A. Rerunning the pipeline immediately
- ==B. Checking whether that day's partition exists and what the orchestrator logged for that run==
- C. Asking them to re-query
- D. Restoring from backup

**94.** The most valuable property to design in from day one, because it makes retries, backfills, and recovery all safe, is:
- A. Compression
- B. Partition pruning
- C. Idempotency
- D. Schema evolution

---

## SECTION I — What is your first move (Q95-100)

**95.** You are handed an unfamiliar dataset and asked to "find something interesting." Your first move:
- A. Run summary statistics on every column
- B. Build a visualisation
- ==C. Establish what one row represents and what the dataset is meant to describe==
- D. Check for nulls

**96.** A group case begins and a teammate immediately proposes an architecture. Your first move:
- A. Propose an alternative architecture
- ==B. Ask what problem it solves and how success is measured, before evaluating any design==
- C. Agree to maintain momentum
- D. Start drawing the data flow

**97.** You have 60 minutes to design and 10 minutes to present with six people. Your first move:
- A. Start designing immediately to maximise working time
- ==B. Propose a time allocation that reserves the final segment for assembling the presentation==
- C. Assign roles by background
- D. Ask each person to present separately

**98.** You are shown a table with an obviously implausible value. Your first move:
- A. Remove the row
- B. Report it as a data quality defect
- C. Correct it based on a reasonable guess
- ==D. Ask what the column means and what unit it uses==

**99.** You are asked a technical question you genuinely cannot answer. Your best move:
- ==A. Say you have not worked with it, then describe how you would approach finding out==
- B. Give a plausible-sounding answer
- C. Say nothing
- D. Redirect to a topic you know

**100.** Your group has 12 minutes left and no agreement on the design. Your first move:
- A. Keep debating until consensus emerges
- B. Let the most senior-sounding person decide
- ==C. Summarise the two viable options, propose picking one, and note the other as an alternative in the presentation==
- D. Split the presentation to cover both fully

---
---

# ANSWER KEY

**A — Read the table**
1 **B** — the key is `customer_id + month`; one row is a customer in a month.
2 **C** — an exact duplicate at the stated grain should not exist; investigate before anything else.
3 **B** — summing across months double-counts the same customer; you would need a single month, or an average.
4 **C** — mixed currencies make the sum meaningless regardless of magnitude.
5 **B** — 13 digits is milliseconds.
6 **B** — 1712000002000 minus 1712000000000 is 2000 ms, i.e. 2 seconds.
7 **C** — a closed account holding a non-zero balance breaks the logical dependency between the two columns.
8 **B** — negative balances are legitimate under overdraft or reversal; ask about the product rule rather than assuming error.
9 **D** — null here means "not closed"; it is information, not absence.
10 **B** — 0.98 across 80 applications is both extreme and well-supported by volume.
11 **A** — 12 applications is far too small to distinguish signal from chance.
12 **C** — compare against a baseline and account for volume; naive ranking rewards tiny samples.

**B — Units and plausibility**
13 **A** — 0.8 seconds and 0.8 milliseconds imply completely different conclusions.
14 **C** — 360 months is 30 years, consistent with a mortgage-style term.
15 **B** — 0 is outside the valid 300-850 range, so it encodes missing rather than measured.
16 **D** — including sentinel zeros drags the mean down and misstates portfolio quality.
17 **A** — one source stores a decimal fraction, the other a percentage; a classic merge defect.
18 **B** — a 20x single-day jump is far more likely duplication than genuine behaviour.
19 **C** — impossible ordering points to timezone handling or mismatched field mapping.
20 **B** — 06:55 UTC is 13:55 in UTC+7; the SLA is missed by nearly seven hours.
21 **D** — negative duration is either a sentinel or reversed subtraction; both need clarifying.
22 **A** — a regular, predictable pattern suggests batching of weekend activity, not a defect.
23 **B** — missingness is often encoded rather than null; absence of nulls proves nothing.
24 **C** — automated assertions catch these systematically; documentation and review do not scale.

**C — Assumption scenarios**
25 **C** — propose, state, remain open. Neither blocked nor silent.
26 **B** — 42% exclusion is large enough to suggest the definition misses the intent.
27 **C** — ask for the basis without attacking the person, and make the dependency explicit.
28 **D** — assume, design, and name the first bottleneck under 10x growth. That last part is what impresses.
29 **C** — it names the assumption and its consequence, which is what makes it useful.
30 **B** — divergent metrics almost always trace to differing implicit definitions.
31 **B** — early correction is cheap; late correction wastes the whole discussion.
32 **A** — surface it immediately and scope the impact; hiding it compounds the cost.
33 **B** — one line, because the caveat governs how the number may legitimately be used.
34 **C** — inherited definitions carry assumptions fitted to a different question.

**D — Diagnose the symptom**
35 **B** — flat volume with doubled value points to duplication or double conversion, not growth.
36 **C** — a count exceeding the base table is the signature of fan-out.
37 **B** — an operator with no terminal sink can be pruned from the execution graph; it runs cleanly and does nothing.
38 **B** — monotonically growing lag is a sustained throughput deficit.
39 **C** — a spike that drains is exactly what buffering exists for; this is healthy.
40 **B** — unbounded keyed state without TTL is the classic streaming memory failure.
41 **C** — without checkpointing, restart begins from empty state.
42 **A** — one straggler task alongside completed peers is textbook skew.
43 **B** — constant monthly volume but growing runtime means the scan is not being pruned.
44 **B** — frequent small writes create many small files, and per-file overhead dominates.
45 **A** — non-idempotent writes plus a duplicate scheduled run produces exactly this.
46 **C** — leakage is the standard explanation for a train-production accuracy gap with identical code.
47 **B** — two implementations of one feature is the usual source of training-serving skew.
48 **A** — a consistent, repeating gap points to scheduling, not data loss.

**E — Design choices**
49 **B** — the action cadence is daily, so batch meets the requirement at far lower cost.
50 **C** — the decision must complete inside the authorisation window.
51 **C** — one serving store, two refresh rhythms matched to how fast each feature decays.
52 **D** — one minute is comfortably within micro-batch range, and reusing the existing stack has real value.
53 **A** — Flink is the fit for low latency with rich keyed state.
54 **D** — no additional processing platform to operate, and Kafka already exists.
55 **C** — large-scan aggregation is what real-time OLAP engines are built for.
56 **B** — single-key lookup at millisecond latency is the key-value use case.
57 **D** — broadcasting a 2 MB table avoids shuffling 500 GB.
58 **D** — design the write to be safe, rather than policing the trigger.
59 **C** — partitioning plus retention or tiering addresses both cost and query efficiency.
60 **B** — schema evolution support plus a contract makes additive changes non-breaking.
61 **C** — remove the cause rather than restricting the symptom; CDC offloads the operational system.
62 **D** — a single computed definition serving both paths is the only structural guarantee.

**F — Find the flaw**
63 **B** — the guarantee is on effect, not on physical processing count.
64 **C** — ordering is per-partition, so it depends entirely on keying.
65 **B** — internal state only; the sink must cooperate for end-to-end guarantees.
66 **D** — the mean conceals the tail where users actually suffer.
67 **B** — concurrency raises throughput; it does not shorten an individual request's path.
68 **B** — no nulls says nothing about correctness or encoded missingness.
69 **B** — precomputed values are as fresh as their last refresh, no fresher.
70 **B** — silent skipping loses data invisibly; a DLQ preserves and surfaces it.
71 **C** — the downstream action cadence determines the choice, not fashion.
72 **B** — "looks fine" is not evidence; without idempotency, duplication can be subtle.

**G — Arithmetic**
73 **C** — 1000 ms ÷ 2 ms = 500 records/second.
74 **C** — 100 records ÷ 0.05 s = 2,000 records/second.
75 **C** — filling 100 records at 1,000/second takes 100 ms of waiting.
76 **C** — 10,000 ÷ 3,000 = 3.33, so 4 consumers.
77 **C** — a consumer group cannot exceed partition count in parallelism; extra consumers idle.
78 **B** — the slide sets output frequency, the size sets coverage.
79 **C** — 200 × 300 seconds = 60,000 events.
80 **B** — 5,000 × 1 KB × 604,800 s ≈ 3 TB, then × 3 replicas ≈ 9 TB.
81 **A** — reading 3 of 120 columns is roughly 2.5% of the data, plus better compression.
82 **B** — 75 ÷ 20 ≈ 3.75, so about 4 minutes under ideal conditions.

**H — Failure scenarios**
83 **D** — isolate the message, commit, keep the stream moving.
84 **B** — a DLQ without alerting just relocates the silence.
85 **A** — transient failures resolve on retry; backoff avoids amplifying the problem.
86 **C** — permanent failures never succeed on retry; retrying them is what creates the blocking loop.
87 **B** — idempotency turns partial-write recovery into a non-event.
88 **C** — retained immutable raw data is what makes any backfill possible.
89 **B** — restore from the last checkpoint and reprocess the interval since.
90 **A** — reprocessing is only safe if the sink tolerates repeated writes.
91 **A** — preserve everything, alert loudly, fix the parser, then replay from the DLQ.
92 **C** — a failed or skipped materialisation run is by far the most common cause of divergence.
93 **B** — establish whether the partition exists and what the orchestrator recorded, before acting.
94 **C** — idempotency is the property that makes retries, backfills, and recovery all safe.

**I — First move**
95 **C** — grain and purpose before any statistic.
96 **B** — problem and metric first; a design cannot be evaluated without them.
97 **B** — reserving assembly time is the single highest-value contribution in the first two minutes.
98 **D** — ask about meaning and unit before deciding it is even an error.
99 **A** — honesty plus a described approach preserves credibility; a fabricated answer destroys it.
100 **C** — converge, decide, and record the alternative. Deciding is more valuable than agreeing.

---

## What changed from the previous set

These questions test **application**, not recall. Section A gives you actual tables to read, which is literally the first bullet in their guide and was missing before. Section D asks you to reason from symptom to cause, which is what a real Q&A sounds like. Section G makes you do arithmetic under mild pressure. Section I is about behaviour in the room tomorrow, not about technology at all.

**If you only do three sections:** **A** (reading tables — the exercise they are most likely to set), **G** (arithmetic — nothing else on your desk trains this), and **I** (six questions, and they are about how you behave in the first two minutes of the case).
