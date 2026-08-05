---
tags: [project, job-hunt, interview, data-engineer, quiz, home-credit, english]
status: active
created: 2026-08-05
event: AC 2026-08-06
---

# 100 MCQ — Home Credit AC Prep Guide (English)

> Covers exactly the four areas in the official prep guide: **data literacy**, **streaming pipeline shape**, **open-source landscape**, **latency vs throughput vs concurrency**, and **failure/recovery handling**.
> Answer key with explanations at the end. Correct answers are evenly distributed across A/B/C/D.

---

## SECTION A — Reading a small tabular dataset (Q1-18)

**1.** You are handed an unfamiliar table. What is the very first question to ask?
- A. How many rows does it have?
- B. What does exactly one row represent?
- C. Which column has the most nulls?
- D. When was it last refreshed?

**2.** A table has columns `customer_id`, `month`, `outstanding_balance`. Its grain is:
- A. One row per customer
- B. One row per transaction
- C. One row per loan product
- D. One row per customer per month

**3.** Which best describes event-level data?
- A. Each row records an action that occurred at a point in time
- B. Each row records the current status of an entity
- C. Each row is an aggregated summary
- D. Each row is a dimension attribute

**4.** You join `customers` (one row each) to `payments` (many rows each) and then compute `SUM(customers.credit_limit)`. The result is:
- A. Correct
- B. Understated, because customers without payments drop out
- C. Overstated, because credit_limit is repeated per payment row
- D. Null, because of a type mismatch

**5.** The effect described in Q4 is commonly called:
- A. Data skew
- B. Fan-out
- C. Cardinality violation
- D. Schema drift

**6.** The safest way to aggregate from the many-side without inflating totals is to:
- A. Aggregate the many-side to the correct grain first, then join
- B. Add `DISTINCT` to the select list
- C. Switch from `INNER JOIN` to `LEFT JOIN`
- D. Index the foreign key

**7.** A many-to-many join performed directly, without a bridge table, typically causes:
- A. Silent data loss
- B. Null propagation
- C. A syntax error
- D. Row explosion with uncontrolled duplication

**8.** A column is 80% null. The most reasonable first interpretation is:
- A. The pipeline is broken
- B. The column should be dropped
- C. Null may carry business meaning, such as "not applicable"
- D. Nulls should be replaced with zero

**9.** Why inspect 10-20 raw rows before running aggregate functions?
- A. Aggregates hide row-level structure, duplication, and anomalies
- B. It reduces compute cost
- C. It is required for compliance
- D. It is unnecessary if a schema exists

**10.** A "logical dependency" between columns means:
- A. One column is a foreign key to another table
- B. A business rule links them, e.g. if status is CLOSED then balance must be zero
- C. One column is physically stored next to another
- D. One column is derived by a formula

**11.** Which is a temporal pattern worth checking in raw data?
- A. Column ordering
- B. Number of distinct values
- C. Character encoding
- D. Seasonality, trend, and out-of-order arrivals

**12.** A candidate key must be:
- A. The first column in the table
- B. An integer
- C. Unique and non-null across all rows
- D. Indexed

**13.** `transaction_id` appears twice with different amounts. Most likely explanation:
- A. Normal behaviour for transactions
- B. The grain is finer than assumed, or duplicates were introduced upstream
- C. The column is a foreign key
- D. The table is sorted incorrectly

**14.** A table of loan applications where one applicant appears 12 times suggests:
- A. The grain is one row per application, not one row per applicant
- B. The data is corrupted
- C. The applicant committed fraud
- D. A join already fanned out

**15.** Which check would catch a broken upstream load fastest?
- A. Verifying column names
- B. Checking data types
- C. Comparing today's row count against the recent daily average
- D. Reading the schema documentation

**16.** Two tables both have `customer_id`, but one uses a different format. This is a problem of:
- A. Latency
- B. Concurrency
- C. Compression
- D. Key consistency across sources

**17.** When a dataset mixes two grains in one table, the main risk is:
- A. Slower queries
- B. Double counting during aggregation
- C. Higher storage cost
- D. Loss of column ordering

**18.** Before trusting a correlation you spotted in 20 rows, you should:
- A. Consider that the sample is far too small to generalise
- B. Immediately report it as a finding
- C. Compute the p-value
- D. Build a model on it

---

## SECTION B — Sanity-checking numbers and units (Q19-36)

**19.** A Unix timestamp with 13 digits is expressed in:
- A. Seconds
- B. Minutes
- C. Milliseconds
- D. Microseconds

**20.** Interpreting a millisecond timestamp as seconds will:
- A. Shift time backward to 1970
- B. Push the date thousands of years into the future
- C. Cause a small rounding error
- D. Have no effect on relative comparisons

**21.** A `latency` column contains the value 2000. Before concluding the system is slow, you must:
- A. Compute the column average
- B. Compare it to the SLA
- C. Check for nulls
- D. Establish the unit, since 2000 ms and 2000 s are very different

**22.** A financial system stores `amount = 100000`. A key risk is:
- A. It may be stored in the smallest currency unit, so it means 1000.00
- B. It is definitely in USD
- C. It must be divided by 1000
- D. There is no ambiguity

**23.** An `amount` column with no accompanying `currency_code` means:
- A. Currency can be inferred from magnitude
- B. Only reporting is affected
- C. Sums may be adding different currencies together, making them meaningless
- D. It is safe if the company is domestic

**24.** An `age` column contains 1987. The most plausible cause is:
- A. Random data entry error
- B. The column actually holds year of birth
- C. Age measured in months
- D. A sentinel value for missing data

**25.** A conversion rate computes to 137%. The most common root cause is:
- A. A duplicated numerator or an incorrect denominator
- B. Customers converting more than once
- C. Rounding error
- D. Seasonal effects

**26.** "Physical reality check" on a threshold means asking:
- A. Whether the threshold is three standard deviations out
- B. Whether the threshold matches the historical percentile
- C. Whether business approved the threshold
- D. Whether the value is plausible in the real world, e.g. human age between 0 and 120

**27.** A current account shows a negative balance. The correct first question is:
- A. Should we delete these rows?
- B. Should we take the absolute value?
- C. Does this product permit overdraft, or are these reversal entries?
- D. Is the pipeline broken?

**28.** A `distance_km` column has a maximum of 40075. This should prompt you to:
- A. Accept it, since distances can be large
- B. Note that it equals Earth's circumference, suggesting a cumulative or erroneous value
- C. Convert it to miles
- D. Drop the row

**29.** A percentage column stores values between 0 and 1 in some rows and 0 to 100 in others. This indicates:
- A. Correct behaviour for ratios
- B. A rounding artefact
- C. Nothing unusual
- D. Two different sources with different conventions merged without normalisation

**30.** Timestamps arrive without timezone information. The safest assumption is:
- A. None — you must establish the timezone before doing any date-based grouping
- B. They are UTC
- C. They are local time
- D. It does not matter for daily aggregation

**31.** A daily revenue column jumps 30x on a single day. Before reporting a record day, you should check:
- A. Whether marketing ran a campaign
- B. Whether the pipeline double-loaded that partition
- C. Whether the currency changed
- D. Whether the fiscal calendar shifted

**32.** A `temperature_c` column has values around 310. This most likely means:
- A. Sensor failure
- B. Fahrenheit
- C. Kelvin, not Celsius
- D. Data corruption

**33.** The safest way to detect unit problems systematically is to:
- A. Define expected min/max ranges per column and assert them automatically
- B. Manually inspect samples weekly
- C. Trust the source system's documentation
- D. Rely on the data type

**34.** A latency column contains -50. This indicates:
- A. Very fast processing
- B. A valid measurement below baseline
- C. A compression artefact
- D. A logic error, most likely clock skew or subtracting timestamps in the wrong order

**35.** `avg_transaction_amount` is far higher than the median. This means:
- A. The data is normally distributed
- B. The data is left-skewed
- C. The data is right-skewed, with large outliers pulling the mean up
- D. The median was computed incorrectly

**36.** For threshold-based anomaly detection on skewed financial data, prefer:
- A. Mean plus one standard deviation
- B. Percentiles or IQR-based fences
- C. The arithmetic mean
- D. The maximum value

---

## SECTION C — Stating assumptions explicitly (Q37-48)

**37.** The core value a data engineer adds when given a vague business request is:
- A. Turning an ambiguous question into logic with explicitly stated assumptions
- B. Waiting until the request is fully specified
- C. Implementing every possible interpretation
- D. Choosing the most common interpretation silently

**38.** Given statuses SUCCESS, PENDING, CANCELLED and FAILED, the correct way to compute revenue is:
- A. Sum all rows
- B. Exclude PENDING only
- C. State the rule explicitly — only SUCCESS and not refunded — then filter accordingly
- D. Ask and stop working until answered

**39.** Why is an implicit assumption more dangerous than an incorrect one?
- A. It slows down queries
- B. It violates compliance
- C. It always produces wrong numbers
- D. Nobody knows it exists, so nobody can challenge or correct it

**40.** After applying a filtering assumption, the essential final step is to:
- A. Document it in the ticket
- B. Quantify its impact — what percentage of rows it removes or retains
- C. Write a unit test
- D. Notify the data steward

**41.** Why does quantifying that impact matter?
- A. It reduces storage cost
- B. It is a regulatory requirement
- C. Removing 2% is a detail; removing 40% suggests the problem was misunderstood
- D. It improves query performance

**42.** An end-of-day accounting report should group by:
- A. `event_time`, because it reflects when the financial event actually occurred
- B. `processing_time`, because it reflects when the system recorded it
- C. Either — the difference is negligible
- D. The average of both

**43.** A well-formed explicit assumption sounds like:
- A. "The data seems fine."
- B. "I filtered out the bad rows."
- C. "This is the standard approach."
- D. "I'm assuming a daily batch is sufficient; if same-day intervention is required, the design changes."

**44.** "Churned customer" is undefined in the request. The best response is:
- A. Use the industry standard silently
- B. Propose a concrete definition, state it, and flag that it is adjustable
- C. Refuse to proceed
- D. Compute every possible definition

**45.** In an assessment centre with deliberately incomplete information, the highest-scoring behaviour is:
- A. Stating an assumption and proceeding, while noting what would change if it were wrong
- B. Waiting for more information
- C. Assuming silently and presenting a confident answer
- D. Listing every unknown without resolving any

**46.** A metric definition should always specify:
- A. The visualisation type
- B. The refresh schedule only
- C. The population included, the time window, and the exclusion rules
- D. The storage format

**47.** Two teams report different values for the same metric. The most likely cause is:
- A. Hardware differences
- B. Different implicit assumptions about filters, grain, or time window
- C. Network latency
- D. Different query engines

**48.** Documenting assumptions in SQL comments primarily helps because:
- A. It improves execution plans
- B. It is required by most linters
- C. It reduces file size
- D. The next person can see the intent and challenge it rather than reverse-engineering it

---

## SECTION D — General shape of a streaming pipeline (Q49-62)

**49.** The four core layers of a streaming pipeline, in order, are:
- A. Source, processor, broker, serving store
- B. Broker, source, processor, serving store
- C. Source, message broker, stream processor, serving store
- D. Source, serving store, processor, broker

**50.** The primary role of the message broker layer is to:
- A. Buffer events and decouple producers from consumers so they can run at different speeds
- B. Transform and enrich records
- C. Serve low-latency reads to applications
- D. Compress data for storage efficiency

**51.** Kafka stores data as:
- A. A B-tree index
- B. An append-only, immutable log
- C. A queue that deletes messages on consumption
- D. A relational table

**52.** Change Data Capture works by:
- A. Polling the source table on a schedule
- B. Installing triggers on every table
- C. Diffing daily snapshots
- D. Reading the database transaction log, such as the Postgres WAL or MySQL binlog

**53.** The main advantage of CDC over querying the operational database directly is:
- A. It avoids adding query load to a database that is serving live customers
- B. It cleans the data automatically
- C. It requires no database credentials
- D. It always has higher throughput

**54.** An online serving store is characterised by:
- A. Lowest possible storage cost
- B. Complex multi-table SQL support
- C. Very low read latency, typically single-digit milliseconds
- D. Maximum compression ratio

**55.** In Kafka, message ordering is guaranteed:
- A. Across the entire topic
- B. Within a single partition
- C. Within a consumer group
- D. Across the cluster when ordering mode is enabled

**56.** Setting a message key in Kafka primarily controls:
- A. Compression algorithm
- B. Retention period
- C. Serialisation format
- D. Which partition the message is routed to

**57.** A consumer group exists so that:
- A. Messages are duplicated to every consumer
- B. Messages are compressed before delivery
- C. Partitions are divided among consumers for parallel processing
- D. Consumers can write back to the topic

**58.** A consumer offset represents:
- A. The position a consumer has read up to within a partition
- B. The physical byte address on disk
- C. The message timestamp
- D. The partition number

**59.** Kappa architecture differs from Lambda architecture in that it:
- A. Uses two parallel code paths
- B. Requires no message broker
- C. Only supports batch processing
- D. Uses a single streaming path and replays the stream to recompute history

**60.** The main drawback of Lambda architecture is:
- A. It cannot handle real-time data
- B. The same logic must be maintained in two codebases
- C. It requires exactly-once semantics
- D. It cannot scale horizontally

**61.** A tumbling window differs from a sliding window in that tumbling windows:
- A. Do not overlap
- B. Always overlap
- C. Have variable length
- D. Close on inactivity

**62.** A session window closes when:
- A. A fixed interval elapses
- B. A record count is reached
- C. There is a gap of inactivity longer than a configured threshold
- D. The job checkpoints

---

## SECTION E — Open-source landscape (Q63-80)

**63.** The fundamental difference between Kafka and RabbitMQ is that:
- A. Kafka is always faster
- B. RabbitMQ cannot support multiple consumers
- C. Kafka runs only on the JVM
- D. Kafka retains messages and supports replay; RabbitMQ is a queue where consumed messages are gone

**64.** Apache Pulsar's distinguishing architectural feature is:
- A. It is written in C++
- B. It separates the serving layer from the storage layer
- C. It does not use partitions
- D. It only supports at-most-once delivery

**65.** Redpanda's main selling point is:
- A. Kafka API compatibility implemented in C++, avoiding JVM overhead
- B. A completely different messaging model
- C. Cloud-only deployment
- D. Built-in stream processing

**66.** Debezium belongs to which category?
- A. Stream processor
- B. Online serving store
- C. Change Data Capture connector
- D. Workflow orchestrator

**67.** Apache Flink's processing model is best described as:
- A. Micro-batching at fixed intervals
- B. Record-at-a-time, event-driven true streaming
- C. Scheduled batch execution
- D. Request-response

**68.** Spark Structured Streaming fundamentally works by:
- A. Processing each event immediately on arrival
- B. Delegating entirely to Kafka consumer groups
- C. Running only on static datasets
- D. Splitting the stream into micro-batches processed by the batch engine

**69.** Typical latency of Spark Structured Streaming compared with Flink:
- A. Higher — roughly 100 ms to 1 s, versus single-digit milliseconds
- B. Lower
- C. Identical
- D. Only differs above 1 TB of data

**70.** The biggest operational difference of Kafka Streams versus Flink and Spark is:
- A. It requires more nodes
- B. It does not support stateful operations
- C. It is a client library, deployable as an ordinary application with no dedicated processing cluster
- D. It runs only on managed cloud services

**71.** Kafka Streams scales horizontally by:
- A. Adding nodes to a dedicated cluster
- B. Increasing the driver memory
- C. Configuring a scheduler
- D. Running additional application instances sharing the same application ID, letting Kafka rebalance partitions

**72.** The most notable constraint of Kafka Streams is that it:
- A. Cannot perform windowed aggregations
- B. Reads only from Kafka and writes only to Kafka
- C. Cannot run in containers
- D. Has higher latency than Spark

**73.** Kafka Streams stores local state in:
- A. HDFS
- B. A relational database
- C. RocksDB, backed up to a Kafka changelog topic
- D. The broker's memory

**74.** Redis is chosen as an online serving store primarily because:
- A. It is in-memory, delivering millisecond reads
- B. It supports full SQL
- C. It is cheaper than object storage
- D. It stores the largest volumes

**75.** Apache Cassandra is typically selected when the workload requires:
- A. Complex multi-table joins
- B. Very high write throughput with horizontal scalability
- C. Strict multi-row ACID transactions
- D. Large binary object storage

**76.** ClickHouse and Apache Pinot are best described as:
- A. Message brokers
- B. Stream processors
- C. Object stores
- D. Real-time OLAP engines that aggregate very large row counts in milliseconds

**77.** The difference between Redis and ClickHouse as serving layers is that:
- A. Redis serves key-based lookups; ClickHouse serves fast aggregations over large scans
- B. Redis supports SQL; ClickHouse does not
- C. They are interchangeable
- D. ClickHouse is in-memory only

**78.** Apache Airflow's role in a data platform is:
- A. Stream processing
- B. Message brokering
- C. Orchestration — scheduling tasks, managing dependencies, retries and alerting
- D. Feature serving

**79.** Delta Lake, Apache Iceberg and Apache Hudi are:
- A. Query engines
- B. Table formats providing ACID transactions and versioning over files in object storage
- C. Message brokers
- D. Stream processors

**80.** Trino is best described as:
- A. A message broker
- B. A stream processor
- C. An object store
- D. A distributed SQL query engine that reads data where it lives

---

## SECTION F — Latency vs throughput vs concurrency (Q81-90)

**81.** Latency measures:
- A. The time for a single record to travel from source to destination
- B. Records processed per second
- C. Simultaneous connections supported
- D. Total daily data volume

**82.** Throughput measures:
- A. Time per single request
- B. Number of parallel workers
- C. Memory consumption
- D. Units of work completed per unit of time

**83.** Concurrency measures:
- A. Time per request
- B. Data volume per day
- C. How many units of work are in progress simultaneously
- D. Compression ratio

**84.** Batching records before processing generally:
- A. Reduces both latency and throughput
- B. Increases throughput but also increases latency
- C. Reduces latency and increases throughput
- D. Has no effect on either

**85.** A fraud detection system that must block a transaction at the point of sale should optimise for:
- A. Maximum throughput
- B. Storage efficiency
- C. Lowest infrastructure cost
- D. Low latency, since the decision must complete before the transaction does

**86.** A log ingestion pipeline feeding a data lake should optimise for:
- A. High throughput, using large batches
- B. Sub-millisecond latency
- C. Minimum concurrency
- D. Exactly-once semantics above all

**87.** Increasing concurrency will:
- A. Always reduce single-request latency proportionally
- B. Reduce latency if enough nodes are added
- C. Increase total throughput without reducing the latency of an individual request
- D. Have unpredictable effects depending on language

**88.** A single non-splittable compressed file limits a distributed job because:
- A. It consumes too much memory
- B. It cannot be divided into parallel tasks, so concurrency is capped at one
- C. It has poor compression
- D. It corrupts easily

**89.** Splitting one large input file into many smaller shards primarily improves:
- A. Single-record latency
- B. Storage cost
- C. Data accuracy
- D. Throughput, by raising the number of tasks that can run in parallel

**90.** Measuring API performance, the P99 latency is more informative than the mean because:
- A. The mean hides the tail where users experience the worst delays
- B. P99 is always lower than the mean
- C. The mean is mathematically invalid
- D. P99 is easier to compute

---

## SECTION G — Failure and recovery handling (Q91-100)

**91.** At-most-once delivery means:
- A. No loss, possible duplicates
- B. Possible loss, never duplicated
- C. Neither loss nor duplication
- D. Every message processed exactly once under all conditions

**92.** At-least-once delivery is achieved by:
- A. Committing the offset before processing
- B. Two-phase commit
- C. Deduplicating at the source
- D. Retrying when no acknowledgement is received, which risks duplicates

**93.** At-least-once is usually paired with an idempotent sink because:
- A. Records may be processed more than once, so repeated writes must yield the same result
- B. It improves compression
- C. It preserves ordering
- D. It reduces network usage

**94.** Exactly-once semantics genuinely means:
- A. Each message is physically processed only once
- B. Retries are disabled
- C. The final effect on state and output is as if each message were processed once
- D. The system never fails

**95.** Achieving exactly-once end-to-end requires:
- A. Enabling producer retries only
- B. A replayable source, consistent state checkpoints, and a transactional or idempotent sink
- C. Extending Kafka retention
- D. Manual periodic deduplication

**96.** Flink's checkpointing mechanism works by:
- A. Writing every event to a local log file
- B. Replicating the cluster to a standby region
- C. Compressing state in memory
- D. Injecting barriers into the stream so operators snapshot state consistently without halting processing

**97.** A checkpoint must record both state and consumer offsets because:
- A. Offsets compress better alongside state
- B. It is a Kafka requirement
- C. Restoring state without the matching read position would double-count or skip records
- D. Offsets are needed for monitoring only

**98.** A "poison pill" message is dangerous mainly because:
- A. It causes the consumer to crash repeatedly at the same offset, blocking every subsequent message
- B. It consumes excessive storage
- C. It corrupts the broker
- D. It slows compression

**99.** The purpose of a dead letter queue is to:
- A. Retry messages indefinitely until they succeed
- B. Isolate unprocessable messages for later investigation while the main flow continues
- C. Archive all processed messages
- D. Buffer messages during peak load

**100.** Distinguishing transient from permanent errors matters because:
- A. Permanent errors compress differently
- B. Transient errors require a dead letter queue
- C. Retrying a permanent error forever creates the blocking loop, whereas transient errors succeed on retry
- D. Only permanent errors should be retried

---
---

# ANSWER KEY

**A — Reading tabular data**
1 **B** — grain is question zero; row count tells you almost nothing.
2 **D** — the composite key `customer_id + month` defines the grain.
3 **A** — events record actions; state records status at a point in time.
4 **C** — the one-side value repeats per many-side row, inflating the sum.
5 **B** — fan-out. A Cartesian product is a missing join condition, which is different.
6 **A** — pre-aggregate to matching grain, then join one-to-one. `DISTINCT` masks the symptom.
7 **D** — both sides multiply, producing uncontrolled duplication.
8 **C** — nulls frequently mean "not applicable"; filling them invents data.
9 **A** — aggregates conceal duplication, wrong grain, sentinel values and mixed units.
10 **B** — a business rule linking columns; extremely valuable as an automated check.
11 **D** — including out-of-order arrival, which matters for windowing.
12 **C** — uniqueness plus non-null is the definition.
13 **B** — either the true grain is finer, or duplicates were introduced upstream.
14 **A** — repetition of an entity signals the grain is the event, not the entity.
15 **C** — volume comparison against a baseline catches broken loads immediately.
16 **D** — key consistency; without it joins silently under-match.
17 **B** — mixed grain is the classic cause of double counting.
18 **A** — 20 rows cannot support a generalisable correlation.

**B — Units and sanity checks**
19 **C** — 10 digits seconds, 13 milliseconds, 16 microseconds.
20 **B** — multiplying by 1000 throws the date far into the future.
21 **D** — unit first, conclusion second.
22 **A** — financial systems commonly store minor units to avoid float error.
23 **C** — summing mixed currencies produces a meaningless figure.
24 **B** — implausible as an age, entirely plausible as a birth year.
25 **A** — rates above 100% almost always indicate duplication or a wrong denominator.
26 **D** — plausibility in the real world, not just statistical fit.
27 **C** — overdraft, fees and reversals all produce legitimate negatives.
28 **B** — matching Earth's circumference is a strong hint of a cumulative or bogus value.
29 **D** — two conventions merged without normalisation; a very common silent bug.
30 **A** — never assume; timezone determines which day a record falls into.
31 **B** — a 30x jump is far more likely a double load than genuine business growth.
32 **C** — around 310 is body-temperature range in Kelvin, not Celsius.
33 **A** — automated range assertions catch unit errors systematically.
34 **D** — negative durations indicate clock skew or reversed subtraction.
35 **C** — mean far above median indicates right skew with large outliers.
36 **B** — percentile and IQR fences are robust to skew; mean-based thresholds are not.

**C — Explicit assumptions**
37 **A** — converting ambiguity into transparent, checkable logic is the core contribution.
38 **C** — state the rule, then filter. You keep moving and remain correctable.
39 **D** — an unstated assumption cannot be challenged, so it fails silently forever.
40 **B** — quantify the impact; an unquantified assumption is incomplete.
41 **C** — the magnitude tells you whether to proceed or revisit the problem statement.
42 **A** — accounting closes on when the financial event occurred, with a late-arrival window.
43 **D** — a good assumption names the assumption and its consequence.
44 **B** — propose, state, flag as adjustable. Neither silent nor blocked.
45 **A** — proceed with a stated assumption; ambiguity is deliberate in assessment centres.
46 **C** — population, time window and exclusions are what make a metric reproducible.
47 **B** — divergent metrics nearly always trace back to differing implicit definitions.
48 **D** — intent captured in place is what makes logic reviewable later.

**D — Streaming pipeline shape**
49 **C** — source, broker, processor, serving store.
50 **A** — buffering and decoupling is the defining role.
51 **B** — append-only immutable log, which is what makes replay possible.
52 **D** — reading the transaction log, which avoids loading the source database.
53 **A** — no additional query load on a live operational system.
54 **C** — single-digit millisecond reads define this layer.
55 **B** — within a partition only. There is no whole-topic ordering guarantee.
56 **D** — the key determines partition routing, hence ordering and state locality.
57 **C** — partitions are divided among group members for parallelism.
58 **A** — the read position within a partition, which enables replay.
59 **D** — one streaming path, replay to recompute history.
60 **B** — maintaining the same logic twice is Lambda's principal cost.
61 **A** — tumbling windows are contiguous and non-overlapping.
62 **C** — session windows close after a configured inactivity gap.

**E — Open-source landscape**
63 **D** — retention and replay versus consume-and-delete.
64 **B** — Pulsar separates brokers from BookKeeper storage, scaling each independently.
65 **A** — Kafka-compatible API without JVM overhead.
66 **C** — Debezium is the standard CDC connector.
67 **B** — record-at-a-time, event-driven.
68 **D** — micro-batches processed by the batch engine.
69 **A** — roughly 100 ms to 1 s versus single-digit milliseconds.
70 **C** — a library, not a framework requiring its own cluster.
71 **D** — more instances sharing an application ID; Kafka rebalances partitions.
72 **B** — Kafka in, Kafka out. Other sinks require Kafka Connect.
73 **C** — RocksDB locally, with a changelog topic for recovery.
74 **A** — in-memory, millisecond reads.
75 **B** — high write throughput and horizontal scale.
76 **D** — real-time OLAP.
77 **A** — key lookups versus large-scan aggregations; different jobs entirely.
78 **C** — orchestration.
79 **B** — table formats adding ACID and versioning over object storage files.
80 **D** — a distributed SQL engine querying data in place.

**F — Latency, throughput, concurrency**
81 **A** — time for one record end to end.
82 **D** — work completed per unit time.
83 **C** — work in progress simultaneously.
84 **B** — the classic trade-off: batching raises throughput and latency together.
85 **D** — the decision must complete inside the transaction window.
86 **A** — throughput first; nobody waits on log ingestion.
87 **C** — concurrency raises aggregate throughput, not per-request latency.
88 **B** — concurrency capped at one because the file cannot be divided.
89 **D** — more parallel tasks on the same infrastructure.
90 **A** — the mean hides the tail where real users suffer.

**G — Failure and recovery**
91 **B** — possible loss, never duplicated.
92 **D** — retry on missing acknowledgement, risking duplicates.
93 **A** — repeated processing must produce the same result.
94 **C** — the effect is as-if-once; reprocessing still physically happens.
95 **B** — all three pieces are required; checkpointing alone is insufficient.
96 **D** — barriers flow with the data, giving a consistent cut without stopping the job.
97 **C** — state and read position must be restored together or counts break.
98 **A** — it blocks the partition, halting every subsequent message.
99 **B** — isolate and preserve, so the main flow proceeds and the failure stays visible.
100 **C** — retrying permanent errors is precisely what creates the poison-pill loop.

---

## How to use this tonight

You have a few hours and an assessment centre at 9:30 tomorrow. **Do not attempt all 100 questions tonight.**

Tonight, if anything at all:
- **Section F (Q81-90)** — 10 questions, and it is a named bullet in their guide. You mislabelled latency once already, so this is the highest-value ten minutes available.
- **Section B (Q19-36)** — skim only. Units and plausibility checks are what the data-literacy exercise will test.

Everything else is reinforcement of material you already know, and is better used after tomorrow.

**The single highest-return action tonight is still sleep.** Reading, listening, synthesising and presenting in a second language under observation all degrade sharply on short sleep. Ten more questions will not change your outcome tomorrow; two more hours of sleep might.

Good luck.
