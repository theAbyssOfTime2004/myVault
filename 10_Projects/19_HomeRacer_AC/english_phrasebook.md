---
tags: [project, job-hunt, interview, data-engineer, home-credit, english]
status: active
created: 2026-08-05
event: AC 2026-08-06, 9:30
---

# English phrasebook — AC 6/8

> Dùng tối 5/8 và sáng 6/8. **Đọc to lên**, đừng đọc thầm — mục tiêu là miệng quen, không phải mắt quen.
> Nguyên tắc: câu ngắn, rõ, tự tin. Không cần văn hoa. Assessor chấm **tư duy**, tiếng Anh chỉ là phương tiện.

---

## 1. Clarifying questions — khung 5 câu, bản tiếng Anh

Nói **trong 5 phút đầu**. Đây là phần được chấm nặng nhất.

**Goal & metric**
> "Before we jump into solutions — what problem are we actually solving, and how would we measure success?"
> "What happens after the system produces an output? Who acts on it?"

**Users & decisions**
> "Who's the end user here, and what decision are they making with this?"

**Data**
> "What data do we already have, and what's the quality like?"
> "Do we have historical labels for this, or is it unsupervised?"

**Constraints**
> "Does this need to be real-time, or is a daily batch enough?"
> "What's the scale we're talking about — thousands or millions of records?"

**Assumptions**
> "Let me state an assumption: I'm assuming X. If that's wrong, the Y part of the design changes."
> "I'll assume a daily batch is sufficient here, since the follow-up action happens the next day."

---

## 2. Collaboration — cụm ghi điểm teamwork

Email của họ ghi rõ: *"build on others' ideas, ask clarifying questions, help the team move forward."* Đây là bản dịch sang hành động.

**Kéo người khác vào**
> "What do you think about this?"
> "You mentioned the business side earlier — how would that affect the design?"
> "I'd like to hear from someone on the product side about what metric matters most."

**Xây trên ý người khác** (làm cái này nhiều — chính là "build on others' ideas")
> "Building on what Linh just said, we could also..."
> "That's a good point. To add to that..."
> "I like that direction. One thing we'd need to handle is..."

**Không đồng ý một cách lịch sự**
> "That could work. My only concern is..."
> "I see it slightly differently — could we consider...?"
> "That's valid. The trade-off there would be..."

**Tổng hợp** (vai giá trị nhất trong nhóm 6 người)
> "So to summarize where we are: we've agreed on X, we're still deciding on Y."
> "Let me try to pull these ideas together..."
> "It sounds like we have two options here. Should we pick one and move on?"

---

## 3. Time-keeping — nước đi mở màn

Nhớ: **60 phút thảo luận, 10 phút present cho 6 người**. Nói câu này trong 2 phút đầu:

> "We have 60 minutes and only 10 minutes to present for six people — that's about a minute and a half each. Should we plan the time? Maybe 10 minutes to understand the problem, 10 for ideas, 25 to design, and save the last 15 to put the presentation together and decide who says what?"

Giữa buổi:
> "We're at the 30-minute mark — should we start converging?"
> "We have 15 minutes left. Should we start putting the presentation together?"

---

## 4. Presentation — cấu trúc 3 nhịp, ~90 giây

**Nhịp 1 — Problem + assumptions (20 giây)**
> "Our goal was to design a system for [X]. We assumed [Y] — that the action happens daily, so batch processing is sufficient."

**Nhịp 2 — Solution, vừa nói vừa chỉ (40 giây)**
> "The data flows like this: we capture changes from the core banking database using CDC, land them in a data lake, run a daily feature pipeline, score the model, and write the results to a serving store that the collections dashboard reads from."

**Nhịp 3 — Trade-offs + next steps (30 giây)**
> "The main trade-off is batch versus streaming. Batch is simpler and cheaper, and it's enough if the team acts the next day. If the business needs to intervene within the same day, this design can be upgraded to streaming without rebuilding it.
> Next steps would be to align on the features with the data analyst, and confirm the alert threshold with product."

---

## 5. Project pitch — bản tiếng Anh, đọc to 3 lần tối nay

Dùng khi được hỏi *"tell me about a project you've worked on."*

> "I built a feature store on public chess data from Lichess, with both a batch and a streaming path.
>
> On the **batch side**, I ingest monthly PGN dumps — about 30 gigabytes compressed — into object storage, then process them with Spark into a Delta lakehouse using a medallion architecture. The interesting problem there was that zstd-compressed files aren't splittable, so Spark could only run a single task, which took around 60 to 75 hours for one month. I added a shredding step that decompresses in one pass and cuts the file at game boundaries into shards, so the work could run in parallel. That brought it down to about four minutes — same infrastructure, I just made the data divisible.
>
> On the **streaming side**, a collector reads Lichess's live TV feed and produces each move into Kafka, keyed by game ID so all moves for a game land in the same partition and stay ordered. A Flink job keeps the previous clock values in state to derive how long each move took, then computes rolling statistics over a 30-second sliding window and writes them to Redis with a one-hour TTL. A very low standard deviation in move times means a machine-like rhythm, which is a cheating signal — without running a chess engine.
>
> Both paths meet at Redis, which is the online store, while Delta on object storage is the offline store for training. One part I'm particularly careful about is **point-in-time correctness** — when building the training set, a player's historical features for a given game only use games that happened before it, otherwise you get data leakage and the model looks great in training but fails in production."

**Nếu bị hỏi "did you run it at full scale?" — trả lời thật:**
> "The architecture and pipeline are verified on a real month with evaluation and clock annotations. The full-scale run is the last remaining step — I designed the shredding and spot autoscaling specifically to handle it."

**Nếu bị hỏi về failure handling:**
> "I deliberately simplified it for this use case: processing-time windows with no watermarks, so I avoid the event-time complexity, and I accept at-most-once because the Redis sink is an overwrite with a TTL — losing a few updates on restart doesn't affect the result. For production I'd add state TTL so the state doesn't grow unbounded, checkpointing to object storage for recovery, and consider a transactional sink if the business needs exact numbers."

---

## 6. Thuật ngữ — hầu hết vốn đã là tiếng Anh

| Tiếng Việt hay nghĩ | Nói tiếng Anh |
|---|---|
| độ trễ | latency |
| thông lượng | throughput |
| chạy song song | run in parallel / concurrency |
| chạy lại không nhân đôi | idempotent |
| ghi đè theo phân vùng | partition overwrite |
| chụp trạng thái | checkpoint / snapshot |
| tua lại | replay |
| bản ghi lỗi | malformed record → dead letter queue |
| cửa sổ trượt | sliding window |
| tính trước | precompute |
| độ tươi dữ liệu | data freshness |
| nguồn sự thật | source of truth |
| rò rỉ dữ liệu tương lai | data leakage |
| dữ liệu lệch | skewed data |
| nhân bản khi join | fan-out |
| mức hạt dữ liệu | granularity |
| đánh đổi | trade-off |

**Câu hay dùng khi phân tích bảng dữ liệu:**
> "What does one row represent here?" ← câu số 0, hỏi trước mọi thứ
> "What unit is this column in — milliseconds or seconds?"
> "That number doesn't look physically plausible — is this age or year of birth?"

---

## 7. Khi không biết — xử lý cho đẹp

**Đừng** im lặng, **đừng** bịa. Dùng:
> "I haven't worked with that specifically, but my thinking would be..."
> "I'm not sure about the exact mechanism, but conceptually I'd expect..."
> "That's a good question — I'd want to check that rather than guess."

→ Ba câu này giữ được uy tín. Bịa một câu là mất niềm tin cho **mọi** câu còn lại.

**Nếu cần thêm thời gian nghĩ:**
> "Let me think about that for a second."
> "Just to make sure I understand the question — you're asking about...?"

---

## 8. Kế hoạch vài tiếng còn lại

**Tối nay — tối đa 60 phút, rồi DỪNG:**
1. Đọc to mục 5 (project pitch) **3 lần**. Đây là việc giá trị nhất tối nay — nó biến kiến thức thành phản xạ miệng.
2. Đọc lướt mục 1 và 2, nhặt lấy 5-6 câu thấy tự nhiên nhất với mình. Không cần thuộc hết.
3. Đọc mục 3 một lần — câu mở màn về chia thời gian.
4. **Ngủ trước 12h.** Nghiêm túc: check-in 9:30 sáng, bạn quen dậy 10h. Một giờ ngủ thêm có giá trị hơn một giờ ôn thêm rất nhiều — thiếu ngủ đánh thẳng vào đúng thứ đang được chấm là phản xạ nói và sự tập trung.

**Sáng mai:**
- Dậy sớm đủ để ăn sáng và tỉnh táo trước 9:30 — Thủ Đức giờ cao điểm, đi sớm hơn dự tính.
- Trên đường: đọc lại mục 1 (5 câu hỏi) và mục 3 (câu mở màn). Chỉ hai cái đó.
- **Không** đọc thêm tài liệu kỹ thuật mới. Giờ này nạp thêm chỉ gây nhiễu.

**Mang theo:** laptop sạc đầy + sạc, smart casual, số điện thoại Mr. Khang (0938.368.316).

---

## Ba điều mang vào phòng

1. **Hỏi trước khi giải.** Câu đầu tiên bạn nói nên là một câu hỏi làm rõ, không phải một giải pháp.
2. **Kéo người khác vào rồi tổng hợp.** Bạn là người duy nhất có nền DE — dùng nó để dẫn dắt nhẹ, không phải để đè.
3. **Tiếng Anh của bạn tốt hơn mặt bằng phòng đó.** Nói chậm, rõ, tự tin. Không cần nói nhanh để chứng minh gì cả.
