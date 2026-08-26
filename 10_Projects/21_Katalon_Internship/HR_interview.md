---
tags: [job-hunt, interview, katalon, internship, hr-round, english]
status: active
created: 2026-08-21
role: AI Application Intern — RAG & memory for Katalon's AI agents
stage: passed CV + video interview; next = HR interview, then Panel
---

# Katalon — HR Interview

> **Vòng này KHÔNG kiểm kỹ thuật.** JD mô tả: *"your interests, goals, and whether we're a good fit for each other."*
> → Nặng về **động cơ, định hướng, độ hợp**. Nhẹ hơn Home Credit về câu tình huống.
>
> **Nhiều khả năng bằng tiếng Anh.**
>
> **Đọc lướt cả note. Học thuộc đúng một câu: câu mở đầu.**

---

## Ba deliverable của vị trí (thuộc để nhắc lại được)

1. **Agent quality evaluation pipeline** — đo accuracy, grounding, hallucination rate
2. **Retrieval tuning** — chunking, embedding, ranking, validate theo benchmark
3. **GraphRAG / memory prototype** — cross-session persistence

*(Cộng: viết tài liệu để core team dùng lại được.)*

---

# ① Introduce yourself

> I'm Dang. I graduated in Data Science from VNUHCM — University of Science this year, and I've done two AI engineering internships. At Solazu I worked on an agentic RAG chatbot — the ingestion pipeline, the retrieval side, and the agent's memory layer. At Tiger Tribe it was a multi-agent product, mostly orchestration and session state.
>
> So most of what I've done sits around retrieval, agents, and working out whether the output is actually any good. That's why this role stood out — it's the same three things.

**~50 giây. Đây là câu duy nhất học thuộc từng chữ** — ba mươi giây đầu là lúc căng nhất, qua được thì phần sau nói tự nhiên.

> [!important] Không nhắc khoá luận ở câu mở đầu
> Hai internship **liên quan trực tiếp hơn** tới vị trí này. Để dành khoá luận cho câu ②, đúng chỗ nó gánh nặng.

---

# ② Why this role / why Katalon

> Two reasons.
>
> The first is how closely the deliverables match what I've already worked on. The posting names three — the evaluation benchmark, retrieval tuning, and cross-session memory. At Solazu I built the ingestion pipeline and the agent's memory layer, so two of those are familiar ground; and my thesis was essentially building an evaluation loop, which covers the third.
>
> The second is the shape of the work. It's set up as: run experiments, validate them against a benchmark, and write them up so the core team can adopt them directly. That's a research-shaped role inside a product team, and there aren't many internships structured that way.
>
> One line in the posting stood out as well — that the reporting has to be honest, regressions included. Most job descriptions don't bother saying that, and it says something about how the team works.

> [!note] Vì sao bản này chắc
> Lý do hai **không dựa vào kinh nghiệm nào** — nó là quan sát về JD, nên không bị vặn được.
> Câu về *"regressions included"* chứng minh đã đọc JD tới từng dòng.

---

# ③ ⭐ Why an internship when you've already graduated?

**Câu khó nhất. TUYỆT ĐỐI không nói "vì chưa tìm được full-time".**

> Honestly, the title matters less to me than what I'd be working on. I'd rather spend six months going deeper on something I already care about, with people who know it better than I do, than take a role with a better title but further from the work.
>
> And from what I understand, this role also feeds into the AI platform team — which is where I'd want to end up anyway.

---

# ④ Tell me about your work / projects

Chuẩn bị **~2 phút mỗi cái**, sẵn sàng bị hỏi sâu.

| Dự án | Kể gì |
|---|---|
| **Solazu** | Ingestion pipeline (crawl → clean → chunk → embed) · memory đa phiên · migrate LlamaIndex → LangGraph |
| **Khoá luận** | Vòng generate → evaluate → update · và **vì sao benchmark mới là phần khó** |
| **Tiger Tribe** | Pipeline nhiều agent · session state |

> [!warning] Ranh giới
> Kể **trách nhiệm và cách tiếp cận** thì bình thường.
> **Đừng nêu chi tiết dữ liệu, khách hàng, hay code** của Solazu — người nghe sẽ tự hỏi sau này bạn kể về họ thế nào.

---

# ⑤ A time you made a mistake

> In my thesis I ran a pilot on maths problems, and I chose them using the contest difficulty labels. The pilot produced nothing — the model stayed at zero the whole way.
>
> When I went back, the mistake was in how I'd selected the problems. I picked by *contest* difficulty instead of by what the *model* could actually do, so I ended up with problems beyond its capability rather than problems it was stuck on. Wrong regime entirely.
>
> I couldn't rerun it — I was out of compute. So I wrote it up as a boundary result instead: the method works when the reference contains a method the model can reach, and fails when it only contains an answer. That became one of the more interesting parts of the thesis.

**Mạnh vì:** lỗi thật · tự phát hiện · nói rõ nguyên nhân · **biến thất bại thành kết quả** thay vì giấu.

---

# ⑥ A conflict, and how you handled it

## ⚠️ CHƯA CÓ — phải tự chọn một chuyện THẬT

Ba nguồn khả dĩ: bất đồng kỹ thuật ở Solazu / Tiger Tribe · bất đồng với thầy hướng dẫn về hướng đi · bài tập nhóm ở trường.

**Khung:**

**①** Bất đồng về **cái gì**, và vì sao mỗi bên nghĩ vậy — *trình bày phía bên kia cho công bằng*
**②** Bạn làm gì để **gỡ**: hỏi lại cho rõ · tìm dữ liệu · thử nhỏ cả hai cách · hỏi người thứ ba
**③** Kết cục — **kể cả khi bạn là người sai**

> [!warning] Tránh
> Chuyện mà bên kia hiện lên như người vô lý. Người phỏng vấn nghe ra ngay.
> **Chuyện tốt nhất là chuyện gỡ được bằng dữ kiện, không phải bằng thắng thua.**

---

# ⑦ Strengths / weakness

**Điểm mạnh — chọn MỘT, kèm bằng chứng:**

> I'm fairly self-directed — I'm a quick study—just point me in the right direction. At Solazu I migrated our memory layer from LlamaIndex onto LangGraph; I hadn't used LangGraph before and there wasn't anyone to walk me through it, so I worked it out from the docs and the existing code.

*(Lấy từ internship thay vì khoá luận — và nó khớp thẳng với dòng **"self-directed learner"** trong JD.)*

**Điểm yếu:**

> Graph databases. I've done vector retrieval and summarization-based memory, but not graph-structured memory — so GraphRAG is the part of this project I'm least prepared for. It's also the part I'm most curious about, which is partly why I applied.

*(Chuẩn bị sẵn thêm **một điểm yếu về cách làm việc** phòng khi họ hỏi "anything outside technical?")*

---

# ⑧ Goals — Katalon nhấn mạnh chỗ này

> Short term, I want to get properly good at evaluation — measuring whether an AI system is actually working, not just whether it looks like it is. That's the part I keep coming back to.
>
> Longer term I'd like to work on the model side — post-training, making models more reliable rather than just larger. But I think the evaluation work comes first, because you can't improve what you can't measure.

**Trung thực, có hướng, và nối thẳng vào deliverable số một của họ.**

---

# ⑨ Availability và trợ cấp

**Ngày bắt đầu:** có con số cụ thể, đừng nói "bất cứ lúc nào"
**Cam kết:** biết trước đi được bao lâu, nói thẳng
**Trợ cấp — hỏi ngược, đừng hét số:**

> Could you share the range you have in mind for this role? I'd rather work from what's standard here than guess.

---

# ⑩ Câu bạn hỏi lại

**Quan trọng nhất — hỏi ở vòng HR là đúng chỗ, họ chờ ứng viên nghiêm túc hỏi:**

> How does the internship usually progress? Is there a path into a full-time role on the AI platform team, and when would that be assessed?

**Thêm:**
- Team hiện đang đo chất lượng agent bằng gì?
- Quy mô team, mình sẽ làm việc với ai?
- Tháng đầu tiên trông như thế nào?

---

# Phòng hờ — câu tình huống kiểu Home Credit

*Katalon nhiều khả năng không hỏi, nhưng có sẵn thì không mất gì.*

## Ba việc gấp cùng lúc

**Sai lầm: cố giải cả ba. Đúng: phân loại rồi báo cáo.**

- **Người không liên lạc được** → thử kênh khác, **không chặn ở đó**; tạm chia lại việc; hỏi sau. Có thể là chuyện cá nhân, đừng đoán xấu
- **Team khác gặp lỗi** → hỏi họ bị chặn hoàn toàn hay chỉ chậm; giúp ở mức **có giới hạn thời gian**; lớn hơn thì **báo lên** chứ đừng âm thầm ôm
- **CEO đòi sớm một tháng** → **đừng gật hay lắc ngay**. Hỏi lại *cần chính xác cái gì* — thường chỉ là một con số chứ không phải toàn bộ. Rồi quay lại với **các phương án kèm đánh đổi**

> **"I don't think I can solve all three at once — I'd sequence them, and make sure nobody is waiting on me without knowing why."**

## Follow-up: thành viên nói không hài lòng với bạn

> I'd want to hear it properly first — not defend myself in the moment. If one person feels that way, there's a chance others do too.
>
> But I'd separate two things. Their feedback about how I lead is fair to discuss, and I'd ask what specifically they'd want me to do differently. Going unreachable, though, is a separate problem — whatever the reason, the team still needs to know when someone is blocked.
>
> **They're not a trade.**

## Kiểu đồng nghiệp bạn tránh ⚠️ *câu bẫy*

Đừng chê tính cách. Nói về **hành vi**, và nói mình sẽ **xử lý** chứ không né:

> Someone who goes quiet when they're stuck. It's completely fixable but does the most damage, because by the time anyone notices, a week is gone. Though I'd rather bring it up with them than avoid working with them.

## Mong đợi ở leader

> Clear priorities, direct feedback — including when I'm wrong — and being reachable when I'm blocked. I'd rather be told early that I'm going the wrong way than find out after two weeks.

---

# Về Playwright

**Đừng xây lý do "why Katalon" trên nó** — kinh nghiệm quá mỏng, bị hỏi thêm một câu là hụt.

**Nhưng nếu họ hỏi thẳng** *"any experience with test automation?"*:

> I wrote some Playwright tests at Solazu — fairly basic ones for our own chatbot. Not deep experience with test automation as a discipline.

Nhận là **có đụng**, không nhận là **biết**.

---

# Lưu ý khi nói

**Học thuộc đúng câu mở đầu.** Phần còn lại nói tự nhiên.
**Câu ngắn.** Đừng dựng câu nhiều mệnh đề rồi lạc giữa chừng.
**Nói chậm hơn mức thấy tự nhiên một chút.** Ngắt hơi là bình thường, đừng lấp bằng "uhm".
**Nhất quán với video interview** — họ đã xem rồi, lệch là mất điểm.
**Câu behavioral phải có kết quả.** Không kết được thì nói học được gì, đừng để lơ lửng.

---

# Thẻ ghi nhớ

| Câu | Dòng chốt |
|---|---|
| Giới thiệu | *"retrieval, agents, and working out whether the output is actually any good"* |
| Why Katalon | *"a research-shaped role inside a product team"* |
| Why intern | *"the title matters less to me than what I'd be working on"* |
| Điểm mạnh | *"I worked it out from the docs and the existing code"* |
| Điểm yếu | *"graph memory — least prepared for, most curious about"* |
| Goals | *"you can't improve what you can't measure"* |
| Đồng nghiệp | *"someone who goes quiet when they're stuck"* |

---

## Còn thiếu — làm trước khi phỏng vấn

- [ ] **Chọn chuyện cho câu ⑥ conflict** — phải là chuyện thật
- [ ] Chuẩn bị **một điểm yếu về cách làm việc** (ngoài graph databases)
- [ ] Chốt **ngày bắt đầu** và **thời hạn cam kết**
- [ ] Nói lớn câu ① và ③ vài lượt cho trôi

## Liên quan

- [[20_KE_HOACH_Job_Fundamentals]]
- Vòng sau: **Panel Interview** — kỹ thuật + hiring manager, có *"role-related assessment"*
