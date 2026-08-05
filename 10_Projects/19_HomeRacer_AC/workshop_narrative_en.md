---
tags: [project, job-hunt, interview, data-engineer, home-credit, english, speaking]
status: active
created: 2026-08-05
event: AC 2026-08-06
---

# "What Actually Matters in Data Engineering" — a workshop talk

> **How to use:** read it **out loud**. This is a spoken script, not a document — the sentence rhythm is built for speaking. Reading it aloud once does more for tomorrow than reading three reference notes silently.
> `[brackets]` are delivery notes, not spoken. **Bold sentences** are the ones worth remembering verbatim.

---

## Opening

Good morning, everyone. Thanks for having me.

I want to start with a confession. When I began in data engineering, I thought the job was about tools. Learn Spark, learn Kafka, learn Airflow, put them on your CV, and you're a data engineer. I spent about a year believing that.

Then I shipped a pipeline that ran perfectly, on schedule, with no errors, for three weeks — and produced numbers that were completely wrong. Nobody noticed until the finance team asked why revenue had jumped forty percent.

`[pause]`

Nothing had crashed. No alert fired. The tools all worked exactly as designed. **The failure wasn't technical — it was that I hadn't understood the data I was moving.**

So today I'm not going to teach you tools. I'm going to walk you through the five things that actually separate a data engineer who can be trusted from one who just knows the syntax. Data literacy, the shape of a streaming system, the ecosystem you'll be choosing from, the three performance numbers everybody confuses, and what happens when things break — because they will break.

Let's start with the unglamorous one.

---

## Part 1 — Data literacy

### Question zero

Here's a table. Three columns: `customer_id`, `month`, `outstanding_balance`. Two million rows.

Before you write a single line of SQL, what do you ask?

`[wait — let them answer]`

Most people say "how many rows" or "how many nulls." Those are fine questions. They're not the first question.

**The first question is: what does exactly one row represent?**

In this table, one row is not one customer. It's one customer **in one month**. The key is the combination of the two columns. And that distinction — which takes about four seconds to establish — determines whether everything you build on top of it is right or catastrophically wrong.

We call this the **grain** of the table. And I want you to develop a reflex: new table, unknown grain, ask before you touch it.

Why does it matter so much? Let me show you the single most common bug in our profession.

### The join that silently lies

You have a `customers` table — one row per customer, with their credit limit. You have a `payments` table — many rows per customer, one per payment.

You join them, because you want to analyse payments alongside customer attributes. Perfectly reasonable. Then somebody asks for total credit exposure, so you write `SUM(credit_limit)`.

`[pause]`

The number you get is wrong. Not slightly wrong — wildly wrong.

Because after the join, a customer with fifty payments appears in fifty rows. And their credit limit is now counted fifty times. This is called **fan-out**, and it is the reason so many dashboards quietly report impossible numbers.

The dangerous part is what fan-out isn't. It isn't an error. Nothing crashes. No warning appears. You get a number, it has the right shape, it looks like money, and it's inflated by a factor nobody can guess.

**A wrong number that looks reasonable is far more dangerous than a job that fails loudly.** A failed job gets fixed within the hour. A wrong number gets put in a board presentation.

The fix is simple once you see it: aggregate the many-side down to the right grain first, then join one-to-one. But you'll only think to do that if you asked question zero.

### Units, or: does this number make physical sense?

Second habit. Before you trust a number, establish what it actually is.

Let me give you three that will cost you if you miss them.

**Timestamps.** A Unix timestamp with ten digits is in seconds. Thirteen digits is milliseconds. Sixteen is microseconds. If you read a millisecond timestamp as seconds, you don't get a small error — you multiply by a thousand and your dates land somewhere in the year 57,000. That one is at least obvious. The dangerous version is the reverse, where the drift is subtle enough to look plausible.

**Money.** A column says `amount = 100000`. Is that a hundred thousand? Or is the system storing minor units — cents, xu — meaning it's actually one thousand? Financial systems very often store the smallest unit to avoid floating-point rounding, and if you assume wrong, every figure you produce is off by a factor of a hundred.

Worse: is there a `currency_code` column next to it? Because if there isn't, and the company operates in more than one country, then `SUM(amount)` is adding dong to dollars to euros. The result isn't approximately right. **It's meaningless — and it will still render beautifully in a chart.**

**Physical plausibility.** This is the habit I want you to take away most. Look at a number and ask: could this exist?

An `age` column with the value 1987. That's not a person. That's a birth year sitting in a column that someone named badly.

A conversion rate of 137 percent. Rates can't exceed one hundred. Something is duplicated in the numerator, or the denominator is wrong — and nine times out of ten, the duplication came from a join that fanned out. Notice how these problems connect.

A latency value of minus fifty. Time doesn't run backwards. Either clocks are skewed between two machines, or somebody subtracted the timestamps in the wrong order.

A temperature reading of 310. If that's meant to be Celsius, nothing survives. It's Kelvin.

None of these require statistics. They require you to look at a number and think about what it's describing in the real world. **That's what data literacy actually is — not a technique, a habit of suspicion.**

### Say your assumptions out loud

Third habit, and this is the one that changes how people perceive you.

You'll be asked for revenue. You'll open the table and find a `status` column with four values: SUCCESS, PENDING, CANCELLED, FAILED.

Nobody told you what counts as revenue. There are three ways you can respond.

You can go back and refuse to work until someone specifies it. That reads as passive, and in practice the person who asked doesn't know either.

You can pick an interpretation and quietly implement it. This is the dangerous one. Because if your interpretation is wrong, nobody finds out — the assumption is invisible, so nobody can challenge it.

Or you can say it out loud: *"I'm counting only SUCCESS transactions that haven't been refunded. That excludes about four percent of rows. If the accounting definition is different, this number changes."*

**An assumption that's stated can be corrected. An assumption that's hidden fails silently forever.**

And notice the second half of that sentence — the four percent. Always quantify the impact of your assumption. Excluding four percent of rows is a footnote. Excluding forty percent means you've probably misunderstood the question entirely. Same sentence structure, completely different conversation.

One more, because it's specific and it bites people in finance: when you build an end-of-day report, group by when the event **happened**, not when your system happened to **record** it. A transaction at 11:58 PM that your pipeline ingests at 12:03 AM belongs to yesterday. Accounting closes on economic reality, not on your ingestion schedule.

`[transition]`

Alright. That's data literacy. Now let's talk about moving data while it's still warm.

---

## Part 2 — The shape of a streaming pipeline

Every streaming system you will ever encounter has the same four layers. Different names, different logos, same shape.

```
Source  →  Message Broker  →  Stream Processor  →  Serving Store
```

Let me walk through why each one has to exist, because if you understand the *why*, you can rebuild the diagram from memory forever.

### Source

Something is generating events. A mobile app emitting user actions. A payment terminal completing transactions. A sensor reporting a reading.

There's also a source people forget: your own operational database. You often want changes from the system of record — new loans, new payments — in your analytics platform. The naive approach is to run queries against the production database on a schedule.

Please don't. **That database is serving live customers.** A heavy analytical scan across the payments history can slow it down or lock it up, and now people can't complete purchases. That's not a technical incident, that's a business incident.

The right tool is **Change Data Capture**. Instead of querying the database, you read its transaction log — the write-ahead log in Postgres, the binlog in MySQL. Every insert, update and delete becomes an event, in order, with no additional query load on the source. Debezium is the standard implementation.

### Message broker

Now, why not send events straight from the source to whatever processes them? Why put a broker in the middle?

Three reasons, and they're all about decoupling.

**Speed.** Your producer emits ten thousand events per second at peak. Your consumer handles four thousand. Without a buffer, you either drop events or you crash. With a buffer, the backlog absorbs the spike and drains afterwards.

**Independence.** The consumer can be redeployed, restarted, or broken for an hour, and the producer never knows. Events accumulate. Nothing is lost.

**Reuse.** Once events are in the broker, five different teams can consume the same stream for five different purposes, without the source knowing any of them exist.

Kafka is the default choice, and the property that matters most is this: **Kafka is an append-only log, not a queue.** Messages aren't deleted when someone reads them. They sit there for the retention period — seven days, thirty days, whatever you configure.

That single design decision gives you replay. Your processing logic had a bug for the last two days? Reset the offset, read it again, recompute. In a traditional queue, those messages are gone forever and there's nothing to recover from.

Two Kafka concepts you must be precise about.

A topic is split into **partitions** so that multiple consumers can work in parallel. And here is the detail people get wrong in interviews: **Kafka guarantees ordering within a partition. Not across a topic.**

Which is why the **message key** matters. The key decides which partition a message lands in. If you key by customer ID, every event for one customer goes to one partition and stays in order relative to each other. If you don't set a key, events scatter, and any logic that depends on sequence breaks in ways that are extremely hard to debug.

### Stream processor

This is the layer that computes. Filtering, enriching, joining streams, aggregating over time.

The important distinction is between **stateless** and **stateful** work.

Stateless is easy: drop invalid records, reshape a field, mask a phone number. Each event is independent.

Stateful is where it gets interesting: *how many transactions has this card made in the last ten minutes?* You can't answer that from the current event alone. You have to remember what came before. That memory is called **state**, and state is what makes stream processing genuinely hard — because state has to survive crashes, and we'll come back to that.

Most stateful work happens in **windows** — time buckets you aggregate over. Three kinds worth knowing.

**Tumbling** windows are contiguous and don't overlap. Midnight to one, one to two. Clean, simple, each event belongs to exactly one window.

**Sliding** windows overlap. "The last five minutes, recomputed every thirty seconds." You use these when you need a continuously updated view rather than discrete buckets.

**Session** windows have no fixed length. They group activity and close after a gap of silence. Perfect for user sessions, where you don't care about clock time — you care about a burst of activity followed by the person going away.

And one distinction that separates people who've operated streaming systems from people who've read about them: **event time versus processing time.**

Event time is when the thing actually happened. Processing time is when your system received it. They are never the same. A phone loses signal in a lift, buffers events for two minutes, and sends them when it reconnects. Those events are two minutes late.

If you aggregate by processing time, that data lands in the wrong bucket. If you aggregate by event time, you're correct — but now you face a question with no clean answer: **how long do you wait for stragglers before closing a window?** Wait forever and you never produce output. Close immediately and you drop late data.

The mechanism for making that trade-off explicit is called a **watermark** — essentially your system declaring "I believe I've now seen everything up to time T, I'm closing that window." It's a bet, and you're choosing how much correctness to trade for how much latency.

### Serving store

Finally, results have to land somewhere someone can read them — fast.

And this layer exists because of a mismatch. Your data lake holds everything, cheaply, and takes seconds to query. But if a fraud check has to complete before a card transaction times out, seconds don't exist as an option. You need single-digit milliseconds.

So you **precompute** and put the results somewhere built for fast lookups. Redis, Cassandra, DynamoDB.

Now — and this is a trade people miss — **precomputation buys latency by spending freshness.**

A value that was computed is a photograph of a moment. If you refresh it every night at 2 AM, then at 4 PM it's fourteen hours old. The lookup is still two milliseconds. The number is still stale.

So the real design question isn't "how do I make this fast." It's **"how quickly does this particular number go bad?"**

A customer's payment history over the last six months barely changes between 9 AM and 5 PM. Refresh that nightly, it's fine. But "how many times has this card been used in the last ten minutes" is worthless if it's an hour old — that one has to be updated by the stream, continuously.

Same store. Two different refresh rhythms. **That's why mature systems run batch and streaming side by side — not because streaming is more modern, but because different facts decay at different speeds.**

---

## Part 3 — The open-source landscape

Let me give you a map, because the tool list is intimidating until you realise it's three small categories.

### Message brokers

**Kafka** is the default. Distributed log, partitioned, retention and replay. If you have no specific reason to choose otherwise, choose Kafka.

**Pulsar** separates the serving layer from the storage layer, so you can scale them independently. Useful at very large scale or with many tenants.

**Redpanda** is Kafka-API compatible but written in C++, so there's no JVM to tune. Same interface, different engine, simpler operations.

**RabbitMQ** is a different animal — a traditional message queue. Messages are consumed and gone. Great for task distribution, wrong for event streaming, because there's nothing to replay.

### Stream processors

**Flink** is true streaming. Record at a time, event-driven, strong state management, latency in single-digit milliseconds. This is what you reach for when you need genuinely low latency and complex stateful logic.

**Spark Structured Streaming** is — and people find this surprising — **not true streaming.** It splits the stream into micro-batches and runs the batch engine on them. Latency lands around a hundred milliseconds to a second. That's a real cost. But you get one API for both batch and streaming, which means one codebase and one skill set for your whole team. If your platform already runs on Spark, that consistency often outweighs the latency.

**Kafka Streams** is the one that confuses people, so let me be precise. It is **not a framework — it's a library.** With Flink or Spark, you submit a job to a cluster that you have to build and operate. With Kafka Streams, you import a library, compile a JAR, and run it like any other application. Scaling means running more instances; Kafka's own consumer groups handle the coordination.

That's a serious operational saving — one less platform to run. The catch is that it reads only from Kafka and writes only to Kafka. And to be clear, since this trips people up: **you still need a Kafka cluster.** What you don't need is a *second* cluster for processing.

### Online serving stores

**Redis** is in-memory with sub-millisecond key lookups. The fastest, and the standard choice for feature serving.

**Cassandra** takes enormous write throughput and scales horizontally without drama. Choose it when writes dominate.

**ClickHouse and Pinot** are a different shape — real-time OLAP. Redis answers "give me the value for this key." ClickHouse answers "aggregate two billion rows by region, right now." Both are fast; they're fast at completely different questions.

**The skill isn't memorising this list.** It's being able to say: *here's what my workload needs, and here's why this tool fits.* That sentence is what an interviewer is listening for.

---

## Part 4 — Latency, throughput, concurrency

Three words used interchangeably by people who shouldn't. Let's fix that.

**Latency** is how long one unit takes, end to end. Milliseconds.

**Throughput** is how many units complete per unit of time. Records per second.

**Concurrency** is how many units are in flight simultaneously.

Analogy. A restaurant kitchen. Latency is how long your dish takes from order to table. Throughput is how many dishes leave the kitchen per hour. Concurrency is how many dishes are being cooked at the same moment.

Now here's why the distinction is worth money.

**They trade against each other.** Batch your work — wait to collect a hundred records before processing — and throughput goes up, because you pay the overhead once instead of a hundred times. But latency goes up too, because the first record sits waiting for ninety-nine friends.

That's the fundamental tension in every streaming system. Micro-batching in Spark is exactly this trade, made deliberately.

And this is why **you cannot optimise a system until you know which number matters.**

Fraud detection at a payment terminal: latency. The decision must land before the transaction completes. Nobody cares that you can process a million events a second if the answer arrives after the customer has left the shop.

Log ingestion into a data lake: throughput. Nobody is waiting. Batch aggressively, compress hard, move volume.

Let me give you one concrete case, because it illustrates concurrency specifically.

I once had a job processing a thirty-gigabyte compressed file. It took over sixty hours. The instinct is to blame the machines and ask for more of them.

But the actual problem was that the compression format wasn't splittable. Spark couldn't divide one file across workers. So no matter how large the cluster, **exactly one task did all the work.** Concurrency was capped at one, and every additional machine sat idle.

The fix wasn't more hardware. It was a pre-processing step that decompressed the file once and cut it into shards at record boundaries. Now there were hundreds of independent pieces, and the cluster could actually work in parallel. Sixty hours became four minutes.

**Same infrastructure. I just made the data divisible.**

And one caveat that catches people: raising concurrency raised throughput enormously, but it did **not** reduce how long a single record takes to parse. Concurrency multiplies how much work is happening at once. It doesn't make any individual piece of work faster.

Last thing here. When you measure a live system, **stop looking at averages.** An average latency of two hundred milliseconds sounds excellent. But if your ninety-ninth percentile is five seconds, then one request in a hundred waits five seconds — and at scale that's thousands of people every day having a bad experience, completely invisible in your mean. Averages hide the tail, and the tail is where users actually suffer.

---

## Part 5 — Failure and recovery

Final section, and the one that separates a prototype from a system.

Start from the correct assumption. Not *if* something fails — **when.** Networks partition. Nodes get evicted. Someone deploys a schema change at 4 PM on a Friday. Distributed systems fail continuously; the question is only whether they fail gracefully.

### What guarantee do you actually have?

Three delivery semantics. Know them precisely.

**At-most-once.** You might lose data, you'll never see duplicates. Acceptable for things like mouse-movement telemetry, where a few missing samples change nothing.

**At-least-once.** You'll never lose data, but you might process something twice. This is where most real systems live, because the failure mode is recoverable.

**Exactly-once.** Neither lost nor duplicated.

And here's the part that's genuinely misunderstood. **Exactly-once does not mean each message is physically processed once.** After a crash, messages absolutely are reprocessed. What's guaranteed is that the *effect* — on your state, on your output — is the same as if each had been processed once. The honest name is "effectively once."

### Idempotency — the master key

Which brings me to the single most valuable word in this entire talk.

**Idempotent** means: doing it again produces the same result.

Watch the difference.

```
balance = 500              →  run it ten times, still 500     ✅
balance = balance + 100    →  run it ten times, you're +1000  ❌
```

An overwrite is idempotent. An increment is not.

**And this one property determines your entire recovery strategy.** If your writes are idempotent, then at-least-once delivery is completely safe — reprocess whatever you like, the end state is correct. Retries become free. Backfills become free. You can be relaxed about failures, because failure has no lasting consequence.

If your writes are increments, you need genuine transactional guarantees, which are expensive and slow. Ledger entries, account balances, anything where each write is a delta rather than a statement of truth.

So when you design a pipeline, ask early: **can I make this idempotent?** Can I use an upsert on a business key? Can I overwrite a partition rather than appending to it? Can I deduplicate on an event ID? If the answer is yes, you've just eliminated an entire category of future pain.

### Checkpointing

For stateful streaming, you need state to survive a crash. That's what **checkpointing** does.

The elegant part is how. You can't stop a live system to take a snapshot — that would destroy throughput. So Flink injects special markers called **barriers** into the stream. They flow along with the data. When an operator has received the barrier on all its inputs, it snapshots its own state and passes the barrier downstream.

Because the barrier travels with the data, it draws a clean line between "before" and "after" across the whole distributed job — **without ever pausing processing.**

One detail people forget: the checkpoint stores **both the state and the source offsets.** Restoring state without the matching read position gives you a system that either double-counts or skips records. They have to move together.

And a boundary worth stating clearly: checkpointing protects your *internal* state. The outside world doesn't roll back. If you already wrote to a database and then replay, that write happens again — unless your sink is transactional, or, much more cheaply, **idempotent**. Which is why idempotency keeps coming up.

### The poison pill

Last one, and it's my favourite because the failure is so counter-intuitive.

A malformed message arrives. Your consumer throws an exception and dies. It restarts, reads the same offset, throws the same exception, dies again. Forever.

Now, losing one bad record — who cares. But that's not what happened. **The pipeline is stuck at that offset.** Every message behind it — potentially millions of perfectly valid records — will never be processed. One malformed record halted the entire stream.

That's why it's called a poison pill. It isn't bad data. It's lethal data.

The pattern that fixes it is the **dead letter queue**. Catch the exception, publish the failed message plus its error context to a separate topic, commit the offset, and let the main flow continue. Then alert on the depth of that queue — five messages is normal, fifty thousand means an upstream schema just changed.

Notice what a dead letter queue gives you that a simple "skip the bad record" doesn't: **visibility.** Skipping silently means you lose data and never find out. Three months later somebody notices two percent of transactions missing and nobody can explain why.

And one refinement that matters in practice: distinguish **transient** failures from **permanent** ones. A network timeout will succeed on retry — retry it, with backoff. Malformed JSON will never succeed — send it straight to the dead letter queue. **Retrying a permanent error indefinitely is precisely how you create the blocking loop in the first place.**

---

## Closing

Let me pull the thread through all of this.

Every section today came back to the same idea, and I want to name it explicitly.

Data literacy is about not trusting a number until you understand what it represents. Streaming architecture is about choosing a shape based on what the business actually needs to do. The performance trinity is about knowing which number matters before you optimise anything. And failure handling is about assuming things break and designing so that breaking is survivable.

None of that is about tools. **Tools change every three years. The judgment doesn't.**

If you take one habit from today, take this one: before you build anything, ask what decision it supports and how quickly that decision has to be made. That single question tells you batch or streaming, it tells you which performance number to chase, it tells you how fresh your data needs to be, and it tells you how much you should spend on correctness guarantees.

Everything else is implementation.

Thank you. I'm happy to take questions.

---

## Delivery notes

- **Pace.** Slower than feels natural. Nervousness speeds everyone up; slowing down reads as confidence.
- **Pauses.** The marked `[pause]` moments matter more than any sentence. Silence after a point makes it land.
- **Don't rush the numbers.** "Sixty hours became four minutes" — let that sit for a beat.
- **If you lose your place**, use a bridge: *"So — coming back to the main point..."* Nobody notices.
- **The bolded lines** are the ones to know cold. Everything else can be paraphrased freely.

**If you only read three sections aloud tonight:** Part 4 (latency/throughput/concurrency — it's a named bullet in the guide and it has your shred story in it), the idempotency block in Part 5, and the closing. That's about eight minutes of speaking and it covers the highest-value material.
