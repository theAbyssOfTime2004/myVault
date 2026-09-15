---
tags: [job-hunt, interview, katalon, internship, panel, rag, evaluation, software-engineering]
status: active
created: 2026-09-15
updated: 2026-09-16
role: AI Application Engineering Intern — RAG & memory cho AI agents của Katalon
stage: passed HR; next = Technical Panel (90') + VP Engineering (45', optional)
---

# Katalon — Panel Interview

> **Round 1 — Technical Panel, 90 phút, với Technical Directors.** Đào sâu kinh nghiệm kỹ thuật.
> **Round 2 — VP Engineering, 45 phút** (optional, có thể xếp chung hoặc online sau).
> Địa điểm: Katalon Office, Viettel Building, Cách Mạng Tháng 8.
>
> **HR đã nhấn mạnh: đây là role *software engineering làm AI app*, không phải role thuần model.**
> JD cũng đặt "Solid Python and software engineering fundamentals" lên bullet đầu tiên.
>
> Note có hai trụ:
> - **Phần B — Eval module** (`rag-assistant-demo`) → bằng chứng cho deliverable ① eval pipeline và ② retrieval tuning. Code của mình, mở ra giải thích được.
> - **Phần C — Chatbot Solazu** → bằng chứng cho software engineering thật: kiến trúc, trạng thái, race condition, tool safety. Kể ở mức *thiết kế và quyết định*, không nêu khách hàng, không mở code.
>
> **Chuẩn đạt:** mỗi câu nói trôi 60–90 giây không nhìn note. Director sẽ chọn một dòng bất kỳ để hỏi "vì sao".

---

## Mục lục

**A.** [[#A — Định vị bản thân]]
**B.** [[#B — Eval module (rag-assistant-demo)]]
**C.** [[#C — Chatbot Solazu]]
**D.** [[#D — Câu chuyện nối hai phần]]
**E.** [[#E — Cheat sheet, câu hỏi ngược, checklist]]
**F.** [[#F — Background Katalon]]
**G.** [[#G — Ôn thêm trước giờ G]]
**H.** [[#H — Kịch bản hỏi – đáp theo JD]]

---
---

# A — Định vị bản thân

Hồ sơ đọc lên hơi nghiêng research (khoá luận SDPO). Gỡ chủ động, đừng đợi bị hỏi:

> "I want to be clear about what I'm looking for — this isn't a research role and that's fine by me. The thesis taught me how to measure things honestly, but what I've actually shipped is services. Evaluation interests me as an engineering problem, not an academic one."

**Mở đầu khi được hỏi giới thiệu kỹ thuật:**

> "At Solazu I worked on a multichannel AI assistant for e-commerce — retrieval, memory, and the logic around the LLM call. Afterwards I built an evaluation harness on my own RAG project, partly to fix what I thought the production system got wrong about measurement. So I can talk about both sides: running it, and measuring it."

---
---

# B — Eval module (rag-assistant-demo)

Repo: `\\wsl.localhost\Ubuntu\home\theabyssoftime\Repos\rag-assistant-demo`

## B.1 — Bài toán

> Chatbot RAG rất dễ *trông có vẻ chạy được*. Harness biến cảm tính thành số đo, để khi đổi chunking / top-k / ranking thì biết thay đổi có thật sự tốt lên không.

**English core:** *"A RAG demo that looks fine is easy. The harness is there so that a change to chunking or ranking produces a number, not an opinion."*

## B.2 — Kiến trúc

```text
golden_set.json ──► dataset.py (load + validate)
                        │
experiments.py ──► [RagConfig × N] ──► runner.py
	                                          │
                     ┌────────────────────┼────────────────────┐
                     ▼                    ▼                    ▼
              retrievers.py         core/chat.py           judge.py
            (top-k / MMR)       (sinh câu trả lời)   (LLM local, Ollama)
                     │                    │                    │
                     ▼                    └─────────┬──────────┘
               metrics.py                           ▼
         (retrieval, tất định)          faithfulness / correctness /
                                         relevancy / abstention
                     └──────────────► results/*_report.md, *_summary.csv, *_cases.csv
```

| File | Vai trò |
|---|---|
| `evals/golden_set.json` | 45 câu: 26 direct · 6 reasoning · 2 cross_doc · 2 conflict · 9 out_of_scope. Mỗi câu có `ground_truth` + `gold_snippets` |
| `evals/dataset.py` | Load, kiểm tra ràng buộc, `normalize()`, `validate_against_corpus()` |
| `evals/config.py` | `RagConfig` frozen dataclass — mô tả trọn một biến thể pipeline; `index_fingerprint` |
| `evals/metrics.py` | HitRate@k, Context Recall, Context Precision, MRR — **không gọi LLM** |
| `evals/judge.py` | LLM-as-judge local: faithfulness (theo claim), correctness (F1 theo ý), relevancy (0/0.5/1), abstention |
| `evals/retrievers.py` | Top-k thường hoặc lấy dư rồi rerank MMR |
| `evals/runner.py` | Chạy golden set qua một config, gom `CaseResult` → `RunResult.summary()` |
| `evals/experiments.py` | Ma trận thí nghiệm + xuất báo cáo có delta so với baseline |
| `evals/test_harness.py` | Test logic thuần: bóc JSON, normalize, retrieval metrics, generation metrics, MMR |
| `run_eval.py` | CLI: `validate` · `baseline [--no-judge]` · `sweep` |

## B.3 — Bảy quyết định thiết kế (phải nói được "vì sao")

**① Metric retrieval tất định, không dùng LLM.**
Khi tuning, thước đo phải đứng yên. Nếu judge cũng dao động thì hai lần chạy cùng config đã ra hai số khác nhau → không phân biệt được cải thiện thật với nhiễu.
> *"The instrument has to be fixed while you turn the knobs."*

**② Nhãn bằng đoạn văn nguyên văn (`gold_snippets`), không bằng chunk id.**
Chunk được coi là liên quan nếu chứa ít nhất một snippet. Gán chunk id thì đổi chunk size là nhãn hỏng hết — mà chunk size lại chính là thứ đang tuning.

**③ Recall tính theo snippet, precision tính theo thứ hạng chunk.**
Câu reasoning / cross_doc cần gộp nhiều mẩu thông tin: bắt được 1/2 mẩu chỉ đáng 0.5. Context precision thì hỏi "chunk đúng có nằm ở đầu danh sách không" — dùng average precision kiểu RAGAS (công thức ở B.3b).

**④ Câu out-of-scope trả `None` cho retrieval score.**
Không có đoạn nào "đúng" → recall/precision vô nghĩa. Những câu đó chấm bằng **abstention** (có chịu nói "không tìm thấy" không).

**⑤ Tách hai loại hallucination.**

| Chỉ số | Nghĩa | Lỗi ở đâu |
|---|---|---|
| `Hallu(claim)` = 1 − faithfulness | Có tài liệu nhưng thêm thắt ngoài context | Prompt / model |
| `Hallu(OOS)` = 1 − abstention rate | Lẽ ra nói "không tìm thấy" nhưng vẫn bịa | Prompt ràng buộc từ chối / ngưỡng |

Gộp làm một số sẽ che mất vấn đề, vì hai lỗi sửa bằng hai cách khác nhau.

**⑥ Mỗi thí nghiệm chỉ đổi một biến so với baseline.** Đổi hai thứ cùng lúc mà điểm lên thì không quy được nguyên nhân.
Kèm `index_fingerprint` = hash(chunk_size, overlap, embed_model, base_url): config chỉ khác `top_k` / reranker dùng chung collection Chroma → sweep không embed lại thừa.

**⑦ Judge chạy local (Ollama, qwen3:4b), temperature 0, có retry, có health check.**
Harness chỉ có ích khi chạy hàng chục lần lúc tuning. Judge trả phí → tốn tiền, dính rate limit → người ta chạy ít đi, đúng cái phản tác dụng. `health_check()` báo lỗi sớm thay vì chết giữa chừng.

**Bonus — `validate_against_corpus()`:** kiểm mọi snippet có thật trong tài liệu. Một snippet gõ sai làm recall câu đó luôn = 0, và mình sẽ đi tuning theo một tín hiệu hỏng.

## B.3b — Định nghĩa chỉ số (bản đã sửa, khớp code hiện tại)

### Hai loại nhãn trong golden set

| Nhãn | Là gì | Dùng cho |
|---|---|---|
| `gold_snippets` | Đoạn **nguyên văn trong tài liệu nguồn** chứa câu trả lời. Cứng, tất định. So khớp sau `normalize()` (NFC, gạch/nháy typographic, gộp khoảng trắng, chữ thường) | Metric retrieval |
| `ground_truth` | Câu trả lời đúng, diễn đạt tự do | Tham chiếu cho judge chấm correctness |

### Retrieval — tất định, không gọi LLM

| Chỉ số | Công thức | Ý nghĩa |
|---|---|---|
| **HitRate@k** | 1 nếu top-k có ít nhất một chunk chứa gold snippet, ngược lại 0 | Có bắt được đoạn đúng nào không |
| **Context Recall** | số snippet bắt được / tổng số snippet của câu | Cần 3 snippet, lấy được 2 → 0.67 |
| precision@i | số chunk liên quan trong top-i / i | **Bước tính trung gian**, không báo cáo riêng |
| **Context Precision** | Σ (precision@i × v_i) / số chunk liên quan đã lấy về — v_i = 1 nếu chunk hạng i liên quan | Average precision: chunk đúng càng ở đầu càng cao |
| **MRR** | 1 / hạng của chunk liên quan đầu tiên (không có → 0) | Hạng 1 → 1.0, hạng 2 → 0.5, hạng 4 → 0.25 |

Ví dụ Context Precision:

```text
[✓ ✗ ✓ ✗] → (1/1 + 2/3) / 2 = 0.83
[✗ ✓ ✗ ✓] → (1/2 + 2/4) / 2 = 0.50
[✗ ✗ ✗ ✓] → (1/4) / 1       = 0.25
```

> [!warning] Hay bị hỏi
> Mẫu số là số chunk liên quan **đã lấy về**, không phải tổng gold snippet.
> Một chunk đúng ở hạng 1 là đủ precision = 1.0 dù recall rất thấp → **precision phải đi cặp với recall**.

### Generation — LLM judge

| Chỉ số | Đối chiếu với | Công thức |
|---|---|---|
| **Faithfulness** | **Context đã retrieve** (không phải ground_truth) | Judge tách câu trả lời thành claim → số claim có trong context / tổng claim |
| **Correctness** | **ground_truth** | Judge liệt kê ý của đáp án mẫu và của câu trả lời, đếm số ý khớp → F1 do code tính |
| **Relevancy** | Câu hỏi | Judge cho 0 / 0.5 / 1, code snap về ba mức |
| **Abstention** | Câu out-of-scope | Câu trả lời có chịu nói "không tìm thấy" không |
| Hallu(claim) | — | 1 − faithfulness |
| Hallu(OOS) | — | 1 − abstention rate |

**Faithfulness** — ví dụ: context chỉ nói remote 2 ngày/tuần; trả lời "Remote 2 ngày/tuần và thứ Bảy được nghỉ" → 1/2 claim được chống lưng → 0.5.

**Correctness (F1 theo ý):**

```text
P = TP / (TP + FP)      ← FP = ý thừa trong câu trả lời
R = TP / (TP + FN)      ← FN = ý đáp án mẫu bị thiếu
F1 = 2PR / (P + R)
```

Ví dụ: ground truth có 3 ý (cho remote · tối đa 2 ngày · phải đăng ký với quản lý); câu trả lời có (cho remote · tối đa 2 ngày · thứ Bảy nghỉ) → TP = 2, FP = 1, FN = 1 → P = R = 2/3 → F1 = 0.67.
*P = R ở đây chỉ vì tình cờ FP = FN. Không được nói "P = R = TP/(TP+FN)".*

Trong code: TP = `n_matched`, FP = số ý của câu trả lời − TP, FN = số ý của đáp án mẫu − TP. Một ý **sai** (ví dụ "remote 3 ngày") bị tính **hai lần**: vừa FP vừa FN.

**Faithfulness vs correctness có thể lệch nhau:**
- **Faithful mà sai:** retriever lấy văn bản cũ, model trả lời đúng theo văn bản đó → loại câu `conflict` trong golden set để bắt đúng trường hợp này.
- **Đúng mà không faithful:** model đoán đúng nhờ kiến thức sẵn có, không dựa vào tài liệu.

**Abstention:** câu out-of-scope **vẫn lấy về đủ k chunk** — retriever luôn trả k đoạn gần nhất, chỉ là không đoạn nào chứa đáp án. Model dễ bịa chính vì nhận được context *trông có vẻ* liên quan.

## B.4 — Judge: cách chấm từng chỉ số

| Chỉ số       | Prompt yêu cầu                                                                                                           | Tính điểm              |
| ------------ | ------------------------------------------------------------------------------------------------------------------------ | ---------------------- |
| Faithfulness | Tách câu trả lời thành claim, mỗi claim `supported` true/false so với **context**; bỏ qua dòng trích nguồn; câu từ chối = 1 claim supported | supported / tổng claim |
| Correctness  | Tách `ground_truth` và câu trả lời thành ý nguyên tử, đếm `n_matched`. **Cấm judge tự cho điểm 0/0.5/1**                  | F1 do `correctness_from_facts()` tính |
| Relevancy    | Câu trả lời có đi đúng trọng tâm câu hỏi không                                                                            | 0 / 0.5 / 1 (`snap_ternary_score`) |
| Abstention   | Câu hỏi không trả lời được từ tài liệu — câu trả lời có từ chối không                                                    | true / false           |

**Vì sao đổi correctness từ 0/0.5/1 sang F1 theo ý?** Để judge tự cho 0.5 thì tuỳ tiện và dao động. Bắt judge chỉ *liệt kê và đếm*, phần tính điểm là code → đọc lại được judge đã đếm gì, kiểm tra được nó sai ở đâu.

**Vậy sao relevancy vẫn ba mức?** Relevancy khó tách thành ý hơn và ít quyết định hơn correctness — nhưng thật ra là **chưa kịp chuyển**. Nói thẳng đó là bước tiếp theo, không phải lựa chọn đã cân nhắc kỹ.

`_extract_json()` xử lý output lộn xộn của model nhỏ: JSON bị bọc trong khối code, lời dẫn phía trước, khối `<think>` của Qwen3, chữ thừa phía sau, JSON lồng nhau, JSON bị cắt cụt. Đây là chỗ dễ vỡ nhất nên có test riêng.

## B.5 — Kết quả sweep: chỉ nói xu hướng, không mang số

> [!warning] Không trích số
> `sweep_report.md` chạy lúc 04:50 ngày 14/9, **trước** khi `metrics.py` đổi Context Precision sang average precision (23:32 ngày 15/9).
> Cột precision trong báo cáo là công thức cũ (precision@k). **Đi phỏng vấn chỉ nói khái niệm và xu hướng.**
> Muốn có số khớp code: `python run_eval.py sweep --no-judge`.

Chế độ retrieval-only, embedding `qwen3-embedding:0.6b`, 9 tài liệu, 45 câu (36 answerable). Ma trận: baseline 400/60 k=4 · chunk 200/40 · chunk 800/120 · top_k 2 · top_k 8 · MMR (fetch 12).

**Bốn điều đọc ra — và phải tự nói giới hạn trước khi bị hỏi:**

**① Một câu hỏi ≈ 3 điểm phần trăm.** Với 36 câu answerable, mỗi câu chiếm ~0.028. Phần lớn chênh lệch giữa các config chỉ là **một câu**. Harness đã phân biệt được cấu hình, nhưng chưa đủ mẫu để kết luận chênh lệch nhỏ là thật.
> *"Most of those deltas are a single question. The harness can separate configurations, but this set isn't large enough to call a small difference real."*

**② Top-k là đánh đổi recall ↔ precision kinh điển.** k lớn thì recall lên, nhưng chunk rác nhiều hơn; k nhỏ thì gọn hơn nhưng dễ trượt đoạn cần thiết.

**③ Chunk nhỏ (200) nhỉnh hơn baseline; chunk to (800) kém hơn.** Hợp lý: chunk to pha loãng embedding, thông tin cụ thể bị chìm. Nhưng xem ① — chênh lệch chỉ cỡ một câu.

**④ MMR tệ hơn baseline ở mọi chỉ số — kết quả âm, và vẫn là phát hiện thật.** Giả thuyết:
- Phần lớn câu là direct, chỉ cần một đoạn → đa dạng hoá không có lợi, lại đẩy đoạn đúng xếp hạng 2–4 ra ngoài nếu nó gần giống đoạn hạng 1 (chunk kề nhau có overlap).
- `query_sim` (score từ Chroma) và `doc_sim` (cosine tự tính) có thể không cùng thang → `mmr_lambda=0.6` không mang nghĩa như mong đợi.
- `mmr_lambda=0.6` là giá trị mặc định chọn tay, chưa quét.

> *"MMR made everything worse, which I didn't expect. My read is that most questions need a single passage, so diversity costs more than it gives. I'd check the score scales before trusting that, and sweep lambda instead of using 0.6."*

**Chưa có:** số faithfulness / correctness / abstention (sweep chạy retrieval-only). Nếu kịp thì chạy `python run_eval.py baseline` có judge trước buổi phỏng vấn.

## B.6 — Điểm yếu tự nêu

| Điểm yếu | Cách nói |
|---|---|
| Golden set 45 câu, 36 answerable | Đủ để harness chạy đúng, chưa đủ để kết luận delta nhỏ. Cần vài trăm câu, hoặc báo khoảng tin cậy |
| Judge chưa hiệu chuẩn | qwen3:4b tách claim tiếng Việt có thể sai. Cần chấm tay ~20–30 câu, đo mức đồng thuận với judge trước khi tin số |
| Golden set tự viết, cùng người viết tài liệu | Dễ viết câu hỏi "vừa khớp" tài liệu. Câu hỏi từ người dùng thật khó hơn |
| Test tự viết bằng `check()`, chưa dùng pytest | Chuyển sang pytest + parametrize là việc 30 phút |
| Chưa theo dõi latency / cost theo config | Config nhanh hơn mà recall ngang nhau thì vẫn là config tốt hơn |
| Chưa có git history / link public | — |

## B.7 — Câu hỏi đào sâu

**Sao biết judge đáng tin?**
> Chưa biết — đó là bước còn thiếu. Cách làm: tự chấm tay một tập con, so với judge, báo tỉ lệ đồng thuận; đảo thứ tự khi so sánh cặp; cố định model và prompt judge theo phiên bản. Judge chưa hiệu chuẩn là cái thước chưa biết đơn vị.

**Sao không dùng Ragas / DeepEval?**
> Muốn hiểu từng chỉ số tính thế nào trước khi dùng thư viện, và cần metric retrieval tất định dựa trên nhãn — Ragas mặc định dùng LLM cho cả context precision/recall. Trong môi trường team thì sẽ dùng thư viện cho phần generation, giữ metric retrieval tất định, và kiểm lại xem hai bên có ra cùng xu hướng không.

**Faithfulness khác correctness thế nào?**
> Faithfulness so với context đã lấy về, correctness so với ground truth. Hai thứ lệch nhau được: retriever lấy văn bản cũ → trả lời faithful mà sai (loại câu `conflict` để bắt cái này); model đoán đúng nhờ kiến thức sẵn có → đúng mà không faithful.

**Context recall thấp vs faithfulness thấp — khác nhau thế nào?**
> Recall thấp → lỗi retrieval: chunking, embedding, top-k. Recall cao mà faithfulness thấp → retrieval ổn, model bịa: lỗi ở prompt hoặc model. Đó là lý do phải tách hai nhóm chỉ số.

**Có đưa eval vào CI không?**
> Metric retrieval tất định thì gate được — ví dụ recall không được tụt quá ngưỡng. Metric từ judge thì không nên làm cổng pass/fail: nó dao động, cổng sẽ flaky, rồi bị tắt. Chạy nightly hoặc khi đổi prompt/model, theo dõi xu hướng.

**`temperature=0` có làm judge tái lập hoàn toàn không?**
> Không. Batching, số thực trên GPU, và model được cập nhật đều làm output đổi. Nên coi model judge là một dependency có phiên bản.

**Nối với Katalon:**
> Phần lớn eval của agent phải dùng LLM-as-judge vì không có chân lý nền. Trong test automation thì có: test chạy pass hay fail là một oracle tất định — cùng ý tưởng execution-guided evaluation trong khoá luận.

---
---

# C — Chatbot Solazu

Repo local: `D:\Repos\solazu` — `aicb-ecom-backend` (Main Backend) · `aicb-ecom-backend-ai` (AI Backend) · `chatbot-ecom-web` (Frontend).

> [!warning] Ranh giới khi kể
> Kể trách nhiệm, luồng dữ liệu, quyết định thiết kế, đánh đổi.
> **Không** nêu tên khách hàng / merchant, dữ liệu, không mở code cho người phỏng vấn xem.
> Nói "một trợ lý AI đa kênh cho e-commerce ở kỳ thực tập trước" là đủ.

## Câu 1 — Tổng quan kiến trúc

**Câu hỏi:** Project giải quyết bài toán gì? Thành phần chính? Tin nhắn đi từ khách đến bot trả lời như thế nào?

**Câu trả lời mẫu**

> Project cung cấp trợ lý AI đa kênh cho doanh nghiệp e-commerce: website live chat và các nền tảng social. Hệ thống gồm Main Backend, Flowise (AI Factory), AI Backend và Frontend.
> Khi khách nhắn tin, channel handler nhận request, kiểm tra customer/conversation/quota/human mode, rồi gọi `ChatService` V2. ChatService lấy agent context, history, tạo runtime state và gọi Flowise `custom-prediction`. Flowise load graph của agent, chạy Memory → Retriever → LLM/Agent → Tools/Confidence tùy nhánh. Kết quả gồm `text` và `agentFlowExecutedData` trả về Main Backend để lưu và gửi lại đúng channel.

**English core:** *"Channel handler validates the customer and conversation, ChatService builds a runtime state and calls the workflow engine; the graph runs memory, retrieval, generation and confidence, and returns the text plus a per-node execution log that the backend stores and sends back to the right channel."*

**Nhớ rõ**
- Flowise = workflow/orchestration engine, không chỉ "LLM wrapper".
- Luồng hiện hành là **V2**: Main Backend → Flowise trực tiếp; AI Backend chỉ được gọi từ trong node.
- Phân biệt: Main Backend (business), Flowise (graph), AI Backend (RAG/summary/confidence), Model provider (sinh câu trả lời).

**Đối chiếu code:** `aicb-ecom-backend/app/services/chat_service.py` — `build_agentflow_vars` (dòng 67), `stream_chat_v2` (dòng 203); `ai_factory_client.py` gọi `/api/v1/custom-prediction/{chatflowId}`. Channel handler riêng cho Facebook, Instagram, TikTok, WhatsApp, Zalo, Zalo personal.

**Vẽ được lên bảng:**

```text
Khách ─► Channel handler (FB/IG/TikTok/WA/Zalo/web)
            │  customer · conversation · quota · human mode
            ▼
        ChatService V2 ── build_agentflow_vars ──► Flowise custom-prediction
            │                                          │
            │                           Memory → Retriever → LLM/Agent → Tools → Confidence
            │                                          │         │
            │                                          │         └─► AI Backend (/agent/retrieve,
            │                                          │               summary, confidence)
            │◄──────── text + agentFlowExecutedData ───┘
            ▼
     kiểm tra latest message → lưu → gửi đúng channel
```

---

## Câu 2 — Vì sao tách 3 phần?

**Câu hỏi:** Vì sao tách Main Backend, Flowise, AI Backend thay vì gom hết vào một Python backend?

**Câu trả lời mẫu**

> Tách theo ranh giới trách nhiệm. Main Backend điều phối business request, tích hợp channel, quản lý customer/conversation/quota/human mode và dữ liệu nghiệp vụ. Flowise điều phối AI workflow dạng graph: model, prompt, branching, tools — tùy biến mà không phải đổi code orchestration. AI Backend cung cấp năng lực AI chuyên biệt trên Python: summary, embedding, Pinecone retrieval, confidence evaluation.
> Lợi ích: chuyên biệt hóa, tùy biến agent, deploy độc lập. Nhược điểm: thêm network hops, khó trace end-to-end, dễ overlapping. Hướng tốt là làm rõ interface và observability, không nhất thiết "đưa hết logic vào Flowise".

**English core:** *"Two layers of orchestration — business in the backend, AI workflow in the graph engine — plus a Python service for the AI-specific work. You gain per-agent customization and independent deploys; you pay in network hops and harder end-to-end tracing."*

**Nhớ rõ**
- Có **hai lớp điều phối**: business (Main Backend) vs AI workflow (Flowise).
- Không nói Main Backend "handle toàn bộ DB" — mỗi service có DB/concern riêng.
- Không gọi là "Flowise SDK"; đúng hơn là Flowise fork + node components.

**Nếu bị hỏi "làm lại có tách vậy không?"** — nêu chỗ trùng lặp thật: logic `is_latest_message` xuất hiện ở cả Main Backend (`chat_service.py`, các channel handler) lẫn AI Backend (`ai_factory/pipeline.py`) — dấu vết của luồng V1 và V2 cùng tồn tại. Đó chính là "overlapping" trong câu trả lời, có ví dụ cụ thể.

---

## Câu 3 — Runtime state

**Câu hỏi:** State gửi sang Flowise chứa gì? Thay đổi qua từng node thế nào? Có tự tồn tại sang lần chat sau không?

**Câu trả lời mẫu**

> Main Backend tạo state ban đầu qua `build_agentflow_vars`: agent/customer/conversation, collection IDs, platform, `recent_messages`, `previous_summary`, các field trống như `message_response`, `retrieval_*`, `confidence_score`.
> Memory bổ sung `sum_history` + `full_question`. Retriever bổ sung retrieval context, raw result, URL map. LLM/Agent ghi `message_response`. Confidence ghi `confidence_score`.
> Runtime state **không mặc định** trở thành state của request tiếp theo. Main Backend lưu summary/history (cache/DB), lần sau gửi lại `recent_messages` và `previous_summary`. Flowise lưu execution data chủ yếu để audit/trace.

**English core:** *"The state is a per-request backpack. Nothing carries over by itself — persistence is the backend's job: it stores history and summary, and sends them back in on the next turn."*

**Tránh nhầm**
- `final_message`, `execution_id`, `confidence_result` trong `stream_chat_v2` là biến hậu xử lý Backend, không phải toàn bộ state gửi lên.
- `agentFlowExecutedData` là mảng nhật ký từng node; state thường lấy ở phần tử cuối: `executed_data[-1].data.state`.

**Góc software engineering nên nói thêm:** giữ state *ngoài* engine (backend tự lưu, tự gửi lại) → Flowise gần như stateless giữa các request → scale ngang và thay engine dễ hơn. Đánh đổi: payload mỗi request lớn hơn, và backend phải quyết định cắt history bao nhiêu.

---

## Câu 4 — RAG / Retriever

**Câu hỏi:** Retriever tìm dữ liệu thế nào từ `full_question` đến prompt LLM? Vì sao không để LLM trả lời từ kiến thức sẵn có?

**Câu trả lời mẫu**

> Memory biến câu hỏi thiếu ngữ cảnh thành `full_question`. Retriever (omnichannel) gọi AI Backend `/agent/retrieve`. AI Backend tạo embedding, hybrid search Pinecone (dense + sparse), lọc theo collection/category, trả document liên quan. Flowise ghi vào state rồi resolve biến trong system prompt (`{{ $flow.state.retrieval... }}`) trước khi gọi LLM.
> Không dùng kiến thức sẵn của model vì model không biết tồn kho, giá, chính sách mới của shop và dễ hallucinate. RAG buộc câu trả lời bám dữ liệu riêng của merchant.

**Thứ tự đúng (hay bị đảo)**

```text
Gửi state → Memory → Retriever → embedding/Pinecone
→ ghi context vào state → LLM sinh text
→ Confidence → trả text + executed_data
→ Backend kiểm tra latest message → lưu/gửi
```

Backend **không** dùng `executed_data` để "bắt đầu tạo câu trả lời". Câu trả lời đã có trong `text`.

**Chi tiết retrieval phải nói được** (`aicb-ecom-backend-ai/app/rag/pinecone_database.py`):

| Bước | Cài đặt | Vì sao |
|---|---|---|
| Hybrid search | Dense embedding + sparse `BM25Encoder`, trộn bằng `alpha` (`DENSE_WEIGHT`) | Dense bắt nghĩa; sparse bắt từ khoá chính xác — mã SKU, tên sản phẩm mà embedding hay làm mờ |
| Lấy dư | `PRE_FILTER_TOP_K` | Cho reranker có đủ ứng viên |
| Rerank | LlamaIndex `LLMRerank` | Xếp hạng lại theo mức liên quan thật tới câu hỏi |
| Lọc | `min_score` | Bỏ đoạn yếu thay vì nhét đủ k đoạn |
| Chi phí | `estimate_rerank_tokens` | Rerank bằng LLM tốn token — phải đếm |
| Chunk | 1024 / overlap 128 | — |

**Đánh đổi của LLM rerank:** chính xác hơn cosine nhưng thêm một lần gọi LLM mỗi request → latency + cost. Phương án rẻ hơn: cross-encoder nhỏ. Nối với Phần B: demo thử MMR và nó tệ hơn — nghĩa là "thêm bước rerank" không mặc nhiên tốt, phải đo.

---

## Câu 5 — Message coalescing / latest message

**Câu hỏi:** Vì sao kiểm tra latest message trước và sau khi gọi Flowise? Không có cơ chế này thì sao?

**Câu trả lời mẫu**

> Mục tiêu chính là tránh gửi **stale response** khi khách gửi thêm tin trong lúc LLM đang chạy. Kiểm tra trước: bỏ request cũ, tránh tốn token. Kiểm tra sau: race condition trong lúc request đang chạy — discard response cũ, không trả cho khách.
> Không có cơ chế này: nhiều LLM chạy song song, trả lời sai thứ tự, thiếu context, trải nghiệm rời rạc. Lưu ý: discard sau Flowise **không hoàn lại** chi phí LLM đã tiêu; muốn tiết kiệm cần cancellation (`AbortController`/abort job).

**Ví dụ hay dùng**

```text
Tin 1: "Tôi muốn mua áo"      → đang xử lý
Tin 2: "Nhưng phải màu trắng" → latest
→ Không được gửi câu trả lời của Tin 1
```

**English core:** *"It's a last-writer-wins guard against stale replies. Checking before the call saves tokens; checking after handles the race. Discarding doesn't refund the tokens — for that you need real cancellation."*

**Bổ sung từ code** (`chat_service.py` dòng 248, 303, 327, 351): trong `stream_chat_v2` việc kiểm tra diễn ra **ở nhiều điểm**, kể cả trong lúc đang stream — không chỉ "trước và sau". Cơ chế nằm ở `ChatCoalescingService` trên Redis: `set_as_latest_message_async`, `is_latest_message_async`, và một **buffer** gom các tin liên tiếp (`get_buffer_async` / `update_buffer_async`) để tin 1 + tin 2 được trả lời cùng lúc.

**Director có thể đào:**
- *Hai request cùng kiểm tra một lúc thì sao?* → check-then-act trên Redis không nguyên tử; khoảng hở nhỏ vẫn còn. Chặt hơn thì dùng so sánh message_id nguyên tử (Lua script / `SET` có điều kiện) hoặc version number.
- *Key Redis có TTL không?* → phải có, không thì rò bộ nhớ theo số conversation.

---

## Câu 6 — LLM node vs Agent node

**Câu hỏi:** Khi nào dùng LLM, khi nào dùng Agent? Lợi ích/rủi ro của tool calling?

**Câu trả lời mẫu**

> LLM node: luồng deterministic, chỉ cần prompt → text/structured output. Agent node: model tự chọn hành động, gọi một/nhiều tools, dùng kết quả để suy luận tiếp (dynamic planning).
> Lợi ích Agent: linh hoạt, giảm hardcode nhánh. Rủi ro: gọi sai tool/args, latency và token tăng, side effects (tạo đơn trùng), prompt injection, agent loop. MCP/skills mở rộng tích hợp nhưng **không tự tăng accuracy**; vẫn cần schema, validation, authorization. Hành động nguy hiểm cần confirm/human-in-the-loop.

**English core:** *"Use a plain LLM step when the path is known; use an agent when the path depends on what the tools return. The agent buys flexibility and costs predictability — so I'd default to the LLM node and earn my way up to an agent."*

**Góc eval (nối Katalon):** agent khó đánh giá hơn nhiều — không chỉ chấm câu trả lời cuối mà phải chấm **trajectory**: chọn đúng tool chưa, args đúng chưa, có vòng lặp thừa không.

---

## Câu 7 — Thiết kế tool `create_order` an toàn

**Câu hỏi:** Tránh tạo đơn trùng, đặt sai SP, prompt injection khiến Agent tự tạo đơn?

> [!important] Phân biệt hiện trạng và đề xuất
> Câu trả lời 5 lớp dưới đây là **thiết kế nên có**. Hệ thống thật có luồng xác nhận đơn
> (prompt `is_user_confirming`, `is_ai_confirming_order`, `extract_order_details` trong `fallback_prompt_manager.py`,
> `ordering_service_comfirm.py`) nhưng **không thấy idempotency key** trong code.
> Khi kể: *"Here's what we had, and here's what I'd add."* Đừng trình bày cả 5 lớp như đã làm hết.

**Câu trả lời mẫu (5 lớp)**

1. **Không tin LLM**: schema chặt; không cho LLM truyền giá/org/payment status — Backend lấy từ DB + auth context.
2. **Human confirmation**: xác nhận rõ trước khi gọi tool; dùng `requiresHumanInput` nếu có.
3. **Backend validate**: ownership, tồn kho, quantity, giá hiện tại, quyền agent/org.
4. **Idempotency**: key = `conversation_id + message_id + tool_name` + unique constraint — gọi lại trả đơn cũ.
5. **Transaction + least privilege + audit**: tạo đơn + trừ kho trong transaction; rate limit; log input/confirm/result/execution_id.

Prompt alone không đủ chống injection; retrieval chỉ là data, không phải instruction — lớp thật nằm ở Backend.

**English 1-liner**
> Treat every LLM tool call as an untrusted action request; confirm, validate, idempotentize, and authorize on the backend.

**Nối Câu 5:** coalescing + retry là đúng hai nguồn gây gọi tool trùng → idempotency không phải lý thuyết, nó cần thật trong hệ thống này.

---

## Câu 8 — Vì sao dùng `full_question`?

**Câu hỏi:** Vì sao không đưa trực tiếp message mới nhất vào Retriever?

**Câu trả lời mẫu**

> Message mới thường thiếu entity ("Còn size M không?"). `full_question` viết lại thành câu độc lập chứa đủ entity + intent ("Áo A123 màu trắng còn size M không?"), giúp embedding và vector search chính xác hơn.
> Trade-off: thêm 1 lần gọi LLM → latency/cost; rủi ro semantic drift nếu rewrite sai lịch sử.

**Nhấn mạnh khi phỏng vấn:** mục tiêu chính là **retrieval accuracy**, không chỉ "để model đọc dễ".

**English core:** *"Follow-ups don't embed well — 'still in size M?' has no entity. Rewriting into a standalone query fixes retrieval, at the cost of an extra call and the risk that the rewrite drifts."*

**Đo thế nào (nối Phần B):** thêm vào golden set các câu hội thoại nhiều lượt, so recall khi retrieve bằng message thô vs `full_question`. Đó là cách biến trade-off này thành con số.

---

## Câu 9 — Confidence score / evaluator trong production

**Câu hỏi:** Node Confidence tính điểm thế nào? Tin được không?

**Hiện trạng** (`aicb-ecom-backend-ai/app/rag/evaluator.py`, gọi qua `background_tasks_service.handle_confidence_score_task`):

| Thành phần | Trọng số | Cách tính |
|---|---|---|
| Context precision / recall (F1) | 30% | Similarity của top-k đoạn lấy về |
| Faithfulness | 40% | Tách câu trả lời thành câu → embed → cosine với các đoạn nguồn → trung bình top-3 → ngưỡng **0.65** → tỉ lệ câu được chống đỡ; trừ điểm theo keyword không có trong context |
| Answer relevancy | 20% | Similarity câu hỏi – câu trả lời |
| Answer diversity | 10% | Độ khác biệt câu trả lời so với nguồn |

Có tiền xử lý tiếng Việt: `underthesea.word_tokenize` + danh sách stopword tự xây (dạ, vâng, ạ, anh/chị…). Có đếm token.

**Câu trả lời mẫu**

> "The production confidence score was embedding-based, not an LLM judge — cheap, fast, deterministic, so it could run on every answer. The weakness is that cosine similarity measures topical support, not entailment: a sentence saying the price is five million looks very similar to a context saying fifteen million. It catches unsupported claims; it doesn't catch contradictions. And the weights and the 0.65 threshold were heuristics — never calibrated against human labels."

**Phải trả lời thật khi bị hỏi "0.65 và 30/40/20/10 ở đâu ra":** chọn theo kinh nghiệm, chưa hiệu chuẩn. Cách đúng: gán nhãn tay một tập, quét ngưỡng, chọn theo precision/recall mong muốn. → Chính là lý do làm lại ở Phần B.

**Hai lớp chống bịa song song:** `guardrail_service.py` (Guardrails SDK + `HALLUCINATION_CHECK_PROMPT`, LLM-based) vs `evaluator.py` (embedding-based). Một cái đắt mà chính xác hơn, một cái rẻ để chạy mọi câu.

---

## Câu 10 — Memory

**Câu hỏi:** Bot nhớ gì giữa các phiên? Có liên quan GraphRAG không?

### Ba module memory — phải phân biệt được

| Module | Là gì | Trạng thái |
|---|---|---|
| **Custom stack** (Main Backend) | Summary + recent messages theo `conversation_id`; Redis trước, fallback DB | **Production, luồng V2** |
| **`lg_memory.py`** (AI Backend) | LangGraph state + checkpointer Postgres + `langgraph_history_cache` | Có code; lời gọi `get_memory_manager()` trong `pipeline.py` **đã bị comment** |
| **`langmem_process.py`** (AI Backend) | `Triple` / `Episode` / `UserProfile` | Được gọi từ `handle_history_manager` của AI Backend |

### Custom memory trên production

- Mỗi `customer_id` có thể có nhiều `conversation_id`; hệ thống **ưu tiên resume** hội thoại cũ hơn là tạo mới.
- Memory lưu và lấy theo `conversation_id`. Mỗi tin nhắn: query **Redis** lấy summary + recent messages → nếu không có (TTL đã hết) thì query **DB** theo `conversation_id`, lấy summary + các tin sau `summary_update_time` → gửi vào node Memory của Flowise.
- Chỉ graph nào dùng node `COLLECTION_HISTORY` mới truy xuất QnA đã train trong collection loại **`CHAT_HISTORY`** trên Pinecone (một collection vector cho mỗi agent, tạo lúc tạo agent — không phải một bảng).
  → Vì không phải truy xuất toàn bộ hội thoại, `CHAT_HISTORY` **gần với FAQ hơn là memory**.
- `customer_profile` vẫn được cập nhật khi cần nhưng **không dùng cho memory** — chỉ dùng cho tạo đơn, CRM, nghiệp vụ khác.
- Đây là stack tự viết, không dựa trên module memory có sẵn của framework nào.

| Pros | Cons |
|---|---|
| Context rẻ | Logic trùng lặp: nạp `previous_summary` + `recent_messages` ở cả Main Backend lẫn node Memory → dễ lệch context |
| Latency thấp nhờ Redis | Không có memory cá nhân hoá: chỉ nhớ theo hội thoại, không nhớ theo khách hàng |
| | Không tận dụng `customer_profile` |
| | Summary drift: tóm tắt qua nhiều vòng làm mất chi tiết quan trọng |

### LangGraph memory (`lg_memory.py`) — bản đề xuất

- Viết trên module và class memory có sẵn của LangGraph. State gồm `messages`, `extracted_facts`, `vector_context`, `session_metadata`, `raw_query`.
- Mỗi phiên phân biệt bằng `thread_id`; mỗi lần state đổi thì snapshot vào checkpointer và persist xuống DB.
- **Graph trong `lg_memory.py`:** `init → extract_facts → retrieve_vector → vector_save → summarize → END` (chạy **tuần tự**).
  - `init`: khởi tạo các trường, thiếu thì là list rỗng.
  - `extract_facts`: prompt trích xuất + messages → LLM → fact lưu vào `extracted_facts`, **đi xuyên state** nên không phải duyệt lại snapshot cũ.
  - `retrieve_vector`: semantic retrieval tin nhắn cũ trong `langgraph_history_cache`.
  - Fact + tin nhắn cũ → ngữ cảnh cho LLM trả lời.
- **Respond node và `get_routing_result`** (gọi LLM quyết định đang ở bước nào: đang hỏi / đã chốt / đã điền địa chỉ / đã đặt đơn) **chỉ có trong script prototype `langgraph_memory_test.py`**, không nằm trong `lg_memory.py`.

| Pros | Cons |
|---|---|
| Có memory dài hạn theo từng người | `retrieve_vector_context_node` và `vector_save_node` là hàm `def` thường gọi DB/vector store trong graph async → **chặn event loop**, latency cao |
| Ownership memory rõ ràng hơn | Gọi LLM nhiều (trích fact, tóm tắt, routing) → token cost cao |
| Checkpointer của LangGraph sạch, có điểm tựa | |

### Đề xuất gộp — và ba chỗ sẽ bị vặn

**Đề xuất:** dùng LangGraph memory làm luồng chính trong node Memory của Flowise, tận dụng memory cá nhân và checkpointer; bỏ phần code dài và logic trùng lặp. Thêm: chạy song song `extract_facts` và `retrieve_vector` (ghi vào hai chỗ khác nhau: checkpointer và `langgraph_history_cache`), chỉ gọi LLM khi cần, đẩy mọi việc nền sang bất đồng bộ.

1. **Không để hai hệ thống memory ngang hàng.** Một nguồn sự thật duy nhất; stack cũ chỉ là **chế độ dự phòng xuống cấp** (chỉ dùng recent messages khi phần mới lỗi). Hai hệ thống đầy đủ chạy song song là tái tạo đúng lỗi trùng lặp vừa chê.
2. **Song song chỉ khi độc lập.** Nếu truy vấn vector dùng fact vừa trích ở chính lượt đó thì phải tuần tự. Nếu độc lập: fan-out trong LangGraph hoặc `asyncio.gather`.
3. **Đo trước khi chuyển.** Dựng tập eval nhiều phiên: fact nói ở phiên 1, hỏi lại ở phiên 3. Đo fact recall, fact cũ/mâu thuẫn, token và latency mỗi lượt.
   > *"Before switching, I'd build a memory eval set — a fact stated in session one, asked about in session three — and measure recall, staleness, and cost per turn. Then the migration is a measured decision, not a rewrite."*

**Summary drift:** sửa bằng cách **tách fact có cấu trúc khỏi bản tóm tắt** — fact không bao giờ bị tóm tắt mất. **Fact mâu thuẫn** (khách chuyển thành phố): gắn timestamp + nguồn, fact mới thay fact cũ nhưng giữ lịch sử để truy vết.

### `langmem_process.py` — schema memory

| Loại | Schema | Nghĩa |
|---|---|---|
| Semantic | `Triple(subject, predicate, object, context)` | Sự kiện dạng bộ ba |
| Episodic | `Episode(observation, thoughts, action, result, mentioned_entities)` | Chuỗi suy luận của một lượt thành công |
| Profile | `UserProfile(name, language, preferences, interests, …)` | Hồ sơ người dùng |

**Cách khai báo gap GraphRAG (đã chỉnh so với vòng HR):**

> "I've done the extraction half — the memory layer pulled subject-predicate-object triples out of conversations. What I haven't done is store them in a graph database and traverse them; they were retrieved like vectors. That's the specific gap, and it's the part of this project I'm most curious about."

---

## Câu 11 — Làm lại thì sửa gì?

Nói thẳng, cụ thể, có thứ tự ưu tiên:

1. **Test.** Cả AI Backend không có bộ test (chỉ một script `langgraph_memory_test.py`). Evaluator là hàm thuần trên embedding — dễ test nhất mà không có test, trong khi mọi thứ khác được chấm bằng nó.
2. **Hiệu chuẩn confidence** trước khi dùng nó ra quyết định (Câu 9).
3. **Idempotency cho tool có side effect** (Câu 7).
4. **Observability end-to-end:** trace id xuyên Main Backend → Flowise → AI Backend; hiện khó trace (Câu 2).
5. **Dọn code:** `print()` → logger có mức; tách file >1000 dòng (`pinecone_database.py`); xoá code chết đang comment; gỡ trùng lặp V1/V2.

> *"Tests first. The evaluation logic was pure functions over embeddings — the easiest thing in the codebase to test — and it had none, while everything else was being judged by it."*

---
---

# D — Câu chuyện nối hai phần

Đây là mạch kể mạnh nhất, dùng khi được hỏi "tell me about a project" hoặc "why this role":

```text
Solazu: chạy RAG thật
   → confidence bằng embedding, trọng số và ngưỡng chọn tay, không có test
   → tự thấy: không biết con số đó có đúng không
Demo: làm lại phần đo
   → metric retrieval tất định dựa trên nhãn
   → faithfulness theo claim bằng judge
   → tách hai loại hallucination, thí nghiệm một biến, có test
   → kết quả: MMR tệ hơn, delta nhỏ chưa đủ kết luận — báo cả hai
Katalon: deliverable ① và ② đúng là việc này, ở quy mô thật
```

> *"At my internship the confidence score was a weighted heuristic nobody had calibrated. Afterwards I rebuilt the measurement side on my own project — deterministic retrieval metrics, claim-level faithfulness, two kinds of hallucination kept separate. One result was that MMR reranking made things worse, which I reported rather than dropped. That's the loop this role describes: run the experiment, validate against a benchmark, write it up honestly."*

---
---

# E — Cheat sheet, câu hỏi ngược, checklist

## Cheat sheet 30 giây

| Chủ đề | 1 câu nhớ |
|---|---|
| Kiến trúc | Channel → ChatService V2 → Flowise graph → (AI Backend cho RAG/memory/confidence) → Backend lưu/gửi |
| 3 service | Business / AI workflow / AI specialty APIs |
| State | Runtime balô; persist do Backend gửi lại history/summary |
| RAG | `full_question` → embed → hybrid Pinecone → rerank → inject prompt → LLM |
| Coalescing | Chống stale reply, kiểm tra nhiều điểm; discard ≠ refund token |
| LLM vs Agent | Text only vs tool + planning |
| Tool safety | Confirm + validate + idempotency + transaction |
| full_question | Contextual rewrite for better retrieval |
| Confidence | Embedding-based, rẻ, chạy mọi câu; cosine ≠ entailment; chưa hiệu chuẩn |
| Memory production | Redis → DB theo conversation; rẻ, nhanh; không cá nhân hoá, summary drift |
| Memory đề xuất | LangGraph: fact xuyên state + checkpointer; một nguồn sự thật, fallback xuống cấp, đo trước khi chuyển |
| GraphRAG | Đã trích triple, chưa lưu graph DB và duyệt đồ thị |
| Eval — retrieval | Tất định, nhãn bằng snippet nguyên văn; CP = average precision, đi cặp với recall |
| Eval — generation | Faithfulness so **context** · correctness F1 theo ý so **ground truth** · relevancy 3 mức · 2 loại hallucination |
| Eval — thí nghiệm | Một biến mỗi lần; 1 câu ≈ 3% → delta nhỏ chưa kết luận; **không mang số** |
| Eval — MMR | Tệ hơn mọi chỉ số; báo cáo, không giấu |

## Câu hỏi ngược

**Ưu tiên nhất — rút thẳng từ JD:**
> "The posting attributes the quality gaps to retrieval and memory infrastructure. How was that established — is there existing measurement pointing there, or is it the leading hypothesis? It changes where I'd start."

**Thêm:**
- Trong sáu agent của True Platform, tầng memory này phục vụ agent nào trước, hay dùng chung cho cả sáu?
- Retrieval lấy từ nguồn nào: tài liệu ứng dụng, kho test, hay lịch sử chạy test?
- Hiện team đo chất lượng agent bằng gì — có golden set chưa, ai gán nhãn?
- Test do agent sinh ra được đánh giá thế nào: kết quả chạy, người review, hay LLM chấm?
- Làm sao để self-healing không vô tình che mất một lỗi thật?
- Findings của intern được core team tiếp nhận thế nào — qua doc, PR, hay demo?
- Với VP: sau kỳ thực tập, việc chuyển sang AI platform team được đánh giá dựa trên gì?

## Checklist trước buổi

- [ ] Nói trôi Câu 1 kèm vẽ sơ đồ, không nhìn note
- [ ] Nói trôi B.3 (bảy quyết định) — mỗi cái một câu "vì sao"
- [ ] Nói đúng công thức B.3b: Context Precision (average precision) · faithfulness so **context** · P = TP/(TP+FP), R = TP/(TP+FN)
- [ ] Nói xu hướng B.5 (không số), **tự nói** giới hạn 1 câu ≈ 3%
- [ ] Tự trả lời: vì sao recall theo snippet · vì sao OOS trả `None` · `mmr_lambda=0.6` ở đâu ra · vì sao relevancy còn 3 mức
- [ ] Phân biệt ba module memory (Câu 10); nói đề xuất gộp kèm ba chỗ bị vặn
- [ ] Câu 9 + Câu 11 — hai câu tự phê bình, nói bằng tiếng Anh
- [ ] G.1 async · G.2 khung system design · G.3 GraphRAG
- [ ] Đọc lại F (background Katalon) và mục VIII [[Job Fundamentals 07 - Testing]]
- [ ] (Nếu kịp) `python run_eval.py sweep --no-judge` để số khớp công thức mới
- [ ] (Nếu kịp) `git init` + push demo lên GitHub, sửa README cho khớp embedding đang dùng
- [ ] Mang nước, ăn trước — tổng có thể tới 135 phút

---
---

# F — Background Katalon

> Nguồn: blog Katalon và các trang tổng hợp (tra ngày 15/9/2026). Chi tiết 6 agent chủ yếu từ bài bên thứ ba — **xem lại trang chính thức của True Platform trước khi nhắc cụ thể.** Con số khách hàng là họ tự công bố, đừng trích như sự thật đã kiểm chứng.

## Công ty

- Thành lập **2016**, tách ra từ **KMS Technology**. Nhà sáng lập: **Vu Lam** (CEO) và **Uy Tran**.
- Trụ sở **Atlanta**, đội kỹ thuật lớn ở Việt Nam. Bắc Mỹ ~45% doanh thu.
- **Series A ~27 triệu USD năm 2021.** Tự công bố hơn 30.000 doanh nghiệp dùng, gồm cả Fortune 100.
- CTO theo trang tổng hợp: Coty Rosenblath — kiểm tra lại trên LinkedIn trước khi nhắc tên.

## Sản phẩm qua các giai đoạn

| Giai đoạn | Sản phẩm | Ý nghĩa |
|---|---|---|
| 2016 | **Katalon Studio** | Viết test low-code trên nền Selenium / Appium |
| Sau đó | **Katalon Platform** | Nền tảng quản lý chất lượng: viết, chạy, quản lý, báo cáo test |
| 2025 | **TrueTest** | Dựa vào hành vi người dùng thật trên production để sinh và bảo trì regression test |
| 4/2026 | **Katalon True Platform** | Nền tảng agentic, **6 AI agent**: design → generation → execution → maintenance → analysis → insights; dùng chung context, tự chuyển việc cho nhau |

**Tính năng AI (bản tổng hợp sản phẩm tháng 5/2026):**
- **Katalon AI Assistant** (trước là StudioAssist): viết test bằng ngôn ngữ tự nhiên, "Run with AI", Agent Mode.
- **AI Self-Healing**: tự sửa locator hỏng, nay dùng thêm ngữ cảnh hình ảnh.
- **AI Failure Analysis**: tự phân loại nguyên nhân test fail.
- **MCP**: gộp hơn 20 tool cũ trùng lặp thành một bộ; thêm **True Skill Library**.
- **Context**: orchestrator giữ context phiên, nhiều lịch sử hội thoại song song.

## Vì sao quan trọng với buổi phỏng vấn

**① Project nằm bên dưới 6 agent.** JD viết agent đang *"hallucination, inaccurate grounding, lost context across sessions"*; True Platform lại quảng bá agent *dùng chung context*. → **Tầng memory và retrieval là thứ giữ cho lời hứa đó thành sự thật.** Bản tổng hợp tháng 5 cho thấy phần giữ context vẫn đang làm dở.

**② Self-healing có thể che lỗi thật.** Locator hỏng có hai khả năng: giao diện đổi nhẹ, hoặc tính năng hỏng thật. Tự sửa cả hai thì test vẫn xanh trong khi sản phẩm lỗi → bài toán đánh giá, nối vào *"honest reporting, regressions included"*. **Nêu như câu hỏi tò mò, không như lời chê.**

**③ Oracle tất định.** Test chạy pass/fail là tín hiệu đánh giá thật mà phần lớn sản phẩm LLM không có; agent **execution** và **analysis** sinh ra đúng loại dữ liệu đó.

## Không nên

- Chê vendor lock-in (dù bài bên thứ ba có nhắc).
- Tỏ ra rành bảng giá, doanh thu.
- Nói "đã từng dùng Katalon" nếu chưa dùng.

---
---

# G — Ôn thêm trước giờ G

## G.1 — Python async (ưu tiên cao nhất)

Mình đã tự đưa ý "sync node chặn event loop" vào câu trả lời → gần như chắc chắn bị hỏi tiếp.

- **Event loop:** một luồng chạy nhiều coroutine; `await` là chỗ nhường quyền cho coroutine khác trong lúc chờ I/O.
- **Hàm `def` gọi DB bên trong code async** không nhường quyền → **cả worker đứng chờ**, mọi request khác cũng chậm theo.
- **Ba cách sửa:** dùng thư viện async · `asyncio.to_thread` / `run_in_executor` · chuyển thành việc chạy nền.
- **Chạy song song việc độc lập:** `asyncio.gather(...)`; quyết định trước khi một việc lỗi — huỷ hết hay lấy kết quả còn lại (`return_exceptions=True`).
- **I/O-bound vs CPU-bound:** async chỉ giúp khi chờ mạng / DB. Tính toán nặng vướng GIL → multiprocessing hoặc tách service.
- **Pydantic vs dataclass:** Pydantic ở biên hệ thống (request, output LLM); dataclass cho dữ liệu nội bộ đã tin cậy.

Nguồn: mục V [[Job Fundamentals 05 - Backend cho AI-DE]].

## G.2 — Khung trả lời câu system design

Đề có thể gặp: *"thiết kế eval pipeline cho agent"* · *"thiết kế memory xuyên phiên cho agent"*.

1. **Làm rõ yêu cầu** — thế nào là "tốt"? Latency, chi phí, quy mô, quyền riêng tư?
2. **Dữ liệu** — golden set lấy đâu, ai gán nhãn; memory lưu gì.
3. **Thành phần và luồng** — vẽ ra.
4. **Cách đo** — số liệu nào cho biết làm tốt hơn.
5. **Đánh đổi và chỗ dễ hỏng** — nói luôn cái mình **không** làm.

## G.3 — GraphRAG ở mức khái niệm

- **Luồng:** trích entity + relation từ văn bản → lưu graph (Neo4j…) → gom cụm cộng đồng (Leiden) → tóm tắt từng cụm.
- **Local search:** hỏi quanh một entity cụ thể. **Global search:** câu tổng quát ("các chủ đề chính là gì") — loại vector search làm kém.
- **Graph hơn vector:** câu hỏi về quan hệ, suy luận nhiều bước, câu tổng quát.
- **Graph thua vector:** dựng graph tốn (gọi LLM trên toàn bộ tài liệu), khó cập nhật khi dữ liệu đổi, câu tra một fact đơn giản. **Nói được ý này có giá trị hơn khen graph.**
- **Nối kinh nghiệm:** đã làm nửa đầu (trích triple ở Solazu), chưa lưu graph và duyệt đồ thị.

## G.4 — Không ôn

DSA · Spark · distributed systems · cài thử Ragas/DeepEval · viết note mới · chạy thêm thí nghiệm.

---
---

# H — Kịch bản hỏi – đáp theo JD

> **Cách dùng:** đừng học thuộc từng chữ — nắm **ý và thứ tự ý**. Câu chính 60–90 giây, câu vặn 20–40 giây.
> Nếu buổi phỏng vấn dùng tiếng Anh thì dịch ý, đừng dịch từng câu.

## Round 1 — Technical Panel (90')

| Phase | Thời gian | Bám JD |
|---|---|---|
| 0 — Mở đầu | 0–5' | — |
| 1 — Software engineering (Solazu) | 5–30' | Python & SE fundamentals · data engineering |
| 2 — Evaluation pipeline | 30–50' | Deliverable ① · honest reporting |
| 3 — Retrieval tuning | 50–65' | Deliverable ② · experimentation mindset |
| 4 — GraphRAG / memory | 65–80' | Deliverable ③ · comfortable with ambiguity · loop engineering |
| 5 — Tài liệu, câu bất ngờ | 80–85' | Written English for documentation |
| 6 — Câu hỏi ngược | 85–90' | — |

### Phase 0 — Mở đầu

**Q0. *"Walk us through your background — focus on the technical side."***

> Tôi tốt nghiệp ngành Khoa học Dữ liệu ở trường Khoa học Tự nhiên, và đã có hai kỳ thực tập về AI engineering.
>
> Kỳ liên quan nhất tới vị trí này là ở Solazu. Tôi làm trên một trợ lý AI đa kênh cho thương mại điện tử, gồm các phần retrieval, memory, và phần logic xoay quanh lời gọi LLM, ví dụ xử lý khi khách nhắn nhiều tin liên tiếp.
>
> Sau kỳ thực tập đó, tôi tự dựng một eval harness trên project RAG cá nhân. Lý do là tôi thấy hệ thống thật có chấm điểm câu trả lời, nhưng không ai biết con số đó có đáng tin hay không.
>
> Nên tôi nói được cả hai phía: vận hành một hệ thống RAG, và đo xem nó có thật sự chạy tốt không. Đó cũng là lý do vị trí này thu hút tôi: ba deliverable trong JD đúng là những thứ đó.

**Q0.1. *"Your thesis is quite research-heavy. Why an application engineering role?"***

> Tôi muốn nói rõ luôn: tôi không tìm một vị trí nghiên cứu. Khoá luận dạy tôi cách đo lường cho trung thực, biết một thí nghiệm chứng minh được gì và không chứng minh được gì. Nhưng những gì tôi thật sự làm ra là service: API, Docker, deploy, những thứ phải chạy ổn định. Tôi quan tâm evaluation như một bài toán kỹ thuật, không phải một đề tài học thuật.

### Phase 1 — Software engineering

**Q1. *"Pick the most complex system you've worked on. Draw the request flow."***

*(Vừa nói vừa vẽ sơ đồ Câu 1.)*

> Khách nhắn qua một kênh: Facebook, Zalo, TikTok hoặc website. Mỗi kênh có một handler riêng. Handler kiểm tra khách hàng, cuộc hội thoại, quota, và xem cuộc hội thoại có đang ở chế độ nhân viên trả lời tay không.
>
> Sau đó request đi vào ChatService. ChatService lấy thông tin agent, lịch sử chat, rồi dựng một runtime state và gọi sang Flowise, là workflow engine chạy graph của agent đó.
>
> Graph chạy lần lượt: node Memory viết lại câu hỏi cho đầy đủ ngữ cảnh, node Retriever gọi sang AI Backend để tìm tài liệu, node LLM sinh câu trả lời, và node Confidence chấm điểm.
>
> Flowise trả về câu trả lời cùng một nhật ký chạy của từng node. Backend kiểm tra xem đây có còn là tin nhắn mới nhất không, rồi mới lưu và gửi lại đúng kênh.

**Vặn — *"Why three services instead of one?"***
> Tách theo trách nhiệm. Main Backend lo nghiệp vụ và tích hợp các kênh. Flowise lo điều phối luồng AI, nên đổi prompt, đổi nhánh, đổi model cho từng agent mà không phải sửa code. AI Backend lo những phần AI chuyên biệt viết bằng Python. Cái được là deploy độc lập và tuỳ biến agent dễ. Cái mất là thêm các chặng mạng, khó trace một request từ đầu đến cuối, và có chỗ logic bị trùng lặp. Làm lại tôi vẫn giữ cách tách này, nhưng làm rõ interface và đầu tư vào observability.

**Vặn — *"How would you trace one slow request across three services?"***
> Một trace id sinh ở handler, truyền qua cả ba service, mọi log gắn id đó; đo latency riêng từng node. Hệ thống lúc đó chưa làm đầy đủ — đây là thứ tôi sẽ sửa đầu tiên.

**Vặn — *"Where is state kept? What if Flowise restarts mid-request?"***
> Runtime state chỉ sống trong một request; lưu lâu dài do Main Backend làm và gửi lại lượt sau, nên Flowise gần như stateless. Restart giữa chừng thì request đang chạy mất nhưng dữ liệu hội thoại không mất. Phía gọi cần timeout và retry — và cẩn thận khi retry với tool có tác dụng phụ như tạo đơn.

**Q2. *"A customer sends three messages in two seconds. What happens?"***

> Hệ thống có cơ chế gộp tin nhắn. Mỗi tin mới được đánh dấu là tin mới nhất trên Redis, các tin liên tiếp được gom vào một buffer.
>
> Trong lúc xử lý, hệ thống kiểm tra "đây có còn là tin mới nhất không" ở nhiều điểm: trước khi gọi Flowise, trong lúc nhận câu trả lời, và trước khi gửi. Có tin mới hơn thì bỏ câu trả lời cũ, request mới trả lời cho cả cụm tin.
>
> Không có cơ chế này thì khách nhận ba câu trả lời rời rạc, sai thứ tự, câu đầu còn thiếu thông tin ở tin thứ hai.
>
> Nói thẳng: bỏ câu trả lời cũ không lấy lại được token đã tốn. Muốn tiết kiệm thật thì phải huỷ được lời gọi đang chạy.

**Vặn — *"Two workers check 'is latest' at the same moment — safe?"***
> Không hoàn toàn. Kiểm tra rồi mới hành động trên Redis không nguyên tử, còn khoảng hở nhỏ. Chặt hơn thì gộp so sánh và ghi vào một thao tác nguyên tử bằng Lua script, hoặc gắn số phiên bản. Với chat thì hiếm gây hậu quả, nhưng phía sau là tạo đơn thì không được bỏ qua.

**Vặn — *"The stale request already called `create_order`. Now what?"***
> Hệ thống có luồng xác nhận đơn trước khi tạo, nhưng không có idempotency key — phần tôi sẽ bổ sung: key từ conversation id + message id + tên tool, unique constraint trong DB, gọi lại thì trả đơn cũ. Tạo đơn và trừ kho trong cùng transaction; giá và tồn kho lấy từ DB, không lấy từ tham số LLM truyền vào.

**Q3. Python fundamentals — hỏi nhanh**

| Câu | Trả lời |
|---|---|
| Graph async có node `def` gọi DB? | Chặn cả event loop, mọi request khác chờ theo. Sửa: thư viện async hoặc `asyncio.to_thread` |
| Khi nào async không giúp? | Việc nặng về tính toán → vướng GIL → multiprocessing / tách service |
| Chạy song song hai lời gọi độc lập? | `asyncio.gather`; quyết trước khi một cái lỗi — huỷ hết hay `return_exceptions=True` |
| Pydantic hay dataclass? | Pydantic ở biên (request, output LLM hay sai schema); dataclass cho dữ liệu nội bộ, ví dụ `RagConfig` |
| Test code gọi LLM? | Phần tất định test thường; mock LLM ở tầng HTTP trong CI; output kiểm theo tính chất; chất lượng tách thành eval suite riêng |

**Q4. *"Design a pipeline ingesting websites, PDFs and JSON exports."***

> Tách thành các bước: lấy dữ liệu, làm sạch, chia chunk, embed, ghi vào vector store. Mỗi loại nguồn có bộ đọc riêng, từ bước chunk trở đi dùng chung.
>
> Ba điểm quan trọng. Một, chunk id tất định, sinh từ hash nội dung và nguồn, để chạy lại không tạo bản trùng. Hai, crawl và embed chậm nên đưa vào hàng đợi — Solazu dùng SQS. Ba, JSON thì validate schema ngay khi đọc vì dữ liệu export thường bẩn.
>
> Mỗi chunk lưu metadata nguồn và phiên bản để trích dẫn và xoá được.

**Vặn — *"A document gets updated. How do you avoid stale chunks?"***
> Xoá toàn bộ chunk theo id của nguồn rồi nạp lại, hoặc so hash chỉ nạp phần thay đổi. Cách đầu đơn giản an toàn, cách sau rẻ hơn khi tài liệu lớn.

### Phase 2 — Evaluation pipeline

**Q5. *"How would you know whether an agent's answers are actually good?"***

> Tôi tách thành hai tầng, vì hai tầng hỏng vì những lý do khác nhau.
>
> Tầng retrieval chấm hoàn toàn tất định, không dùng LLM. Mỗi câu trong golden set được gán gold snippet, đoạn nguyên văn trong tài liệu chứa câu trả lời. Chunk nào chứa snippet thì tính là liên quan, từ đó tính hit rate, context recall, context precision và MRR. Không dùng LLM vì khi tuning thì thước đo phải đứng yên.
>
> Tầng generation dùng LLM làm judge: faithfulness, correctness, relevancy và abstention.
>
> Tôi cũng tách hallucination làm hai: có tài liệu nhưng thêm thắt ngoài tài liệu, và lẽ ra phải nói "không tìm thấy" nhưng vẫn bịa. Hai loại sửa bằng hai cách khác nhau.

**Vặn — *"Context precision vs recall."***
> Recall: lấy về được bao nhiêu phần thông tin cần thiết, tính theo snippet. Precision: chunk đúng có nằm đầu danh sách không — tôi dùng average precision: tại mỗi vị trí có chunk liên quan, tính precision tới vị trí đó rồi lấy trung bình. Hai chỉ số phải đi cặp: một chunk đúng ở hạng một là precision tối đa dù recall rất thấp.

**Vặn — *"Faithfulness vs correctness."***
> Faithfulness so với context đã lấy về; correctness so với ground truth. Retriever lấy văn bản cũ thì câu trả lời faithful mà sai — loại câu "conflict" trong golden set bắt đúng trường hợp này. Ngược lại model đoán đúng nhờ kiến thức sẵn có thì đúng mà không faithful.

**Vặn — *"Why F1 over facts instead of 0/0.5/1?"***
> Để judge tự cho 0.5 thì tuỳ tiện, chạy lại dễ ra điểm khác. Giờ judge chỉ liệt kê ý và đếm số ý khớp; phần tính điểm là code. Đọc lại được judge đếm gì, kiểm tra được nó sai ở đâu.

**Vặn — *"Then why is relevancy still ternary?"***
> Relevancy khó tách thành ý hơn và ít quyết định hơn. Nhưng thực tế là tôi chưa kịp chuyển — đó là bước tiếp theo, không phải lựa chọn đã cân nhắc kỹ.

**Q6. *"How do you know your LLM judge is trustworthy?"***

> Hiện tại tôi chưa biết chắc — đó là bước còn thiếu. Judge chạy local, temperature 0, có retry, nhưng như vậy mới là tái lập được, chưa phải chính xác.
>
> Cách làm đúng: tự chấm tay 20–30 câu, so với judge để đo mức đồng thuận. Cố định phiên bản model và prompt; khi so sánh hai câu trả lời thì đảo thứ tự để tránh thiên lệch vị trí; để ý judge hay chấm câu dài cao hơn. Judge chưa hiệu chuẩn giống một cái thước chưa biết đơn vị.

**Q7. *"We have no golden set today. Where do you start?"***

> Lấy câu hỏi từ log thật trước, vì câu tự nghĩ ra thường dễ hơn thực tế. Chia theo loại: tra một thông tin, cần suy luận, ghép nhiều tài liệu, tài liệu không có đáp án. Bắt đầu nhỏ, khoảng 50 câu, gán nhãn cẩn thận, chạy bước kiểm tra mọi snippet có thật trong tài liệu. Rồi mở rộng theo lỗi gặp thật — mỗi lỗi mới thành một câu.

**Q8. *"Your change improves recall 4% but faithfulness drops 3%. How do you write it up?"***

> Báo cả hai con số, không chọn con số đẹp. Mở từng câu để xem faithfulness giảm ở đâu và vì sao — có thể lấy nhiều chunk hơn làm lẫn thông tin nhiễu vào context. Ghi rõ cỡ mẫu: vài chục câu thì một câu đã chiếm vài phần trăm. Cuối cùng là khuyến nghị có điều kiện, còn quyết định để team vì đánh đổi phụ thuộc sản phẩm.

**Vặn — *"Should eval run in CI?"***
> Một phần. Chỉ số retrieval tất định thì làm cổng được. Chỉ số từ judge thì không — nó dao động, cổng sẽ lúc đỏ lúc xanh rồi bị tắt. Phần đó chạy định kỳ hoặc khi đổi prompt, đổi model, và theo dõi xu hướng.

### Phase 3 — Retrieval tuning

**Q9. *"Tell me about a tuning experiment that didn't go as expected."***

> Tôi thử MMR rerank, lấy dư ứng viên rồi chọn lại sao cho vừa liên quan vừa đa dạng. Tôi kỳ vọng nó cải thiện vì chunk có overlap nên top-k hay gần trùng nhau.
>
> Kết quả ngược lại: gần như mọi chỉ số retrieval đều kém đi.
>
> Giả thuyết một: phần lớn câu chỉ cần một đoạn, ép đa dạng thì đoạn đúng ở hạng hai, ba mà giống đoạn hạng một bị đẩy ra ngoài. Giả thuyết hai: điểm liên quan từ vector store và độ tương đồng tôi tự tính có thể không cùng thang, nên tham số cân bằng không đúng ý nghĩa.
>
> Tôi chưa kiểm chứng xong, nhưng vẫn ghi vào báo cáo — kết quả âm cũng là một phát hiện thật.

| Câu vặn | Trả lời ngắn |
|---|---|
| Sao chỉ đổi một biến? | Đổi hai thứ mà điểm tăng thì không biết nhờ cái nào; fingerprint giúp config chỉ khác top-k/reranker dùng chung chỉ mục |
| Đánh đổi chunk size? | Nhỏ: tìm chính xác, dễ mất ngữ cảnh. To: giữ ngữ cảnh, embedding loãng, tốn token |
| BM25 giúp khi nào? | Mã sản phẩm, SKU, tên riêng — Solazu dùng vector + BM25 với trọng số `alpha` |
| LLM rerank hay cross-encoder? | LLM chính xác hơn nhưng thêm latency, chi phí; cross-encoder rẻ. MMR đã cho thấy thêm rerank chưa chắc tốt → đo rồi mới quyết |
| Cải thiện 2% có thật không? | Vài chục câu thì 2% chỉ là một câu; cần tập lớn hơn, xem từng câu, chạy lặp nếu có judge |
| Câu nối tiếp truy xuất kém? | Viết lại thành `full_question`; giá là thêm một lời gọi LLM và rủi ro viết sai; đo bằng câu nhiều lượt trong golden set |

### Phase 4 — GraphRAG / memory

**Q10. *"Design cross-session memory. A user states a preference in session one; session three should use it."***

> Trước tiên tôi muốn hỏi lại: memory theo từng user hay từng project, có yêu cầu gì về riêng tư hay thời gian lưu không?
>
> *(Giả sử theo user.)* Về dữ liệu, tách hai loại: fact có cấu trúc và bản tóm tắt hội thoại — vì tóm tắt nhiều vòng làm rơi chi tiết, còn fact không được phép bị tóm tắt mất.
>
> Về luồng: sau mỗi lượt trích fact, lưu kèm thời điểm và nguồn; lượt mới truy xuất fact liên quan đưa vào prompt; lưu và tóm tắt chạy nền.
>
> Về đo lường: trước khi đưa vào dùng, dựng tập eval nhiều phiên — thông tin nói ở phiên một, hỏi lại ở phiên ba. Đo agent có nhớ đúng không, có dùng thông tin cũ hoặc mâu thuẫn không, tốn thêm bao nhiêu token và latency.
>
> Về đánh đổi: trích fact tốn lời gọi LLM, fact có thể lỗi thời, và phải xoá được dữ liệu theo yêu cầu.

**Vặn — *"What did you build at Solazu, and what was wrong with it?"***
> Memory production là stack tự viết: summary + tin nhắn gần nhất theo từng hội thoại, Redis trước rồi xuống DB. Rẻ và nhanh. Nhưng chỉ nhớ theo hội thoại, không theo khách hàng; hồ sơ khách hàng có mà không dùng; logic nạp lịch sử lặp ở nhiều chỗ; tóm tắt lâu dần mất chi tiết. Tôi có đề xuất hướng LangGraph có checkpointer và trích fact — đó là đề xuất, chưa chạy trên luồng chính.

**Vặn — *"Two memory systems — isn't that the same duplication?"***
> Đúng, nên không để hai hệ thống ngang hàng. Một nguồn sự thật; hệ cũ chỉ là chế độ dự phòng xuống cấp khi phần mới lỗi.

**Vặn — *"Can fact extraction and retrieval run in parallel?"***
> Được nếu truy xuất không dùng fact vừa trích ở lượt đó. Độc lập thì fan-out trong LangGraph hoặc `gather`; không thì bắt buộc tuần tự. Phải kiểm tra trước, không mặc định.

**Vặn — *"When does a graph beat vector memory — and when not?"***
> Graph hơn khi hỏi về quan hệ, suy luận nhiều bước, hoặc câu tổng quát kiểu "các vấn đề chính là gì". Graph không đáng khi chỉ tra một fact đơn giản, vì dựng graph rất tốn và khó cập nhật. Tôi đã làm nửa đầu là trích triple từ hội thoại; phần lưu graph database và duyệt đồ thị thì chưa — đó là phần tôi muốn học nhất.

**Vặn — *"Two facts contradict — the user moved city."***
> Mỗi fact có thời điểm và nguồn. Fact mới thay fact cũ khi dùng, fact cũ đánh dấu hết hiệu lực để truy vết. Không chắc cái nào đúng thì agent hỏi lại người dùng.

**Q11. *"An agent keeps calling the same tool in a loop."***

> Ba lớp. Một, giới hạn cứng: số bước, tổng token, timeout cả vòng lặp. Hai, phát hiện lặp: cùng tool, cùng tham số vài lần liên tiếp thì dừng. Ba, tool lỗi thì trả lỗi có cấu trúc để model đổi hướng — trả rỗng thường khiến model thử lại mãi.
>
> Về đánh giá: với agent không chỉ chấm câu trả lời cuối mà chấm cả trajectory — chọn tool đúng không, tham số đúng không, có bước thừa không.

### Phase 5 — Tài liệu và câu bất ngờ

**Q12. *"How would you document an experiment so the core team can adopt it without asking you?"***
> Khung cố định: mục đích, baseline, thay đổi gì, kết quả kèm cỡ mẫu, những gì chưa kết luận được, khuyến nghị, câu lệnh chạy lại. Phần "chưa kết luận được" quan trọng nhất và hay bị bỏ qua nhất. Harness của tôi xuất sẵn báo cáo có chênh lệch so với baseline và file chi tiết từng câu.

**Làm lại ở Solazu thì sửa gì?** → Câu 11: test trước tiên; hiệu chuẩn confidence; idempotency; trace xuyên ba service.

**Self-healing của Katalon có rủi ro gì?**
> Có thể che lỗi thật: locator hỏng vì giao diện đổi nhẹ hoặc vì tính năng hỏng thật. Tự sửa cả hai thì test vẫn xanh trong khi sản phẩm lỗi. Mỗi lần tự sửa nên được ghi lại cho người xem lại, và tỉ lệ tự sửa nên được theo dõi như một chỉ số. Tôi tò mò team đang xử lý thế nào.

**Gần đây tự học được gì không theo tutorial?**
> Cách tính context precision theo thứ hạng. Ban đầu tôi tính tỉ lệ chunk đúng trong top-k, rồi nhận ra nó không phân biệt được chunk đúng ở hạng một hay hạng bốn, nên chuyển sang average precision. Tương tự, tôi chuyển correctness từ để judge tự cho điểm sang đếm ý rồi tính F1.

### Phase 6 — Câu hỏi ngược

Xem mục E.

## Round 2 — VP Engineering (45')

**AI thay đổi software testing thế nào?**
> Viết test sẽ rẻ đi rất nhiều; bài toán khó chuyển sang thẩm định — test do máy sinh có đúng không, có bắt được lỗi thật không. Testing có lợi thế mà phần lớn sản phẩm AI không có: kết quả chạy test là tín hiệu thật. Ai dùng tốt tín hiệu đó để đánh giá và cải thiện agent sẽ đi xa hơn.

**Deadline gấp: tốc độ hay chất lượng?**
> Cắt phạm vi, không cắt phần đo lường. Làm ít hơn nhưng biết chắc cái đã làm đúng tới đâu, và nói rõ những gì chưa kiểm.

**Không đồng ý với thiết kế của senior?**
> Biến bất đồng thành câu hỏi kiểm chứng được. Hồi làm khoá luận, tôi và giảng viên bất đồng về việc đưa ví dụ lần thử sai vào — thầy lo kết quả đẹp giả tạo. Tôi đề xuất chạy cả hai phiên bản cùng điều kiện; kết quả gần như giống nhau, nhưng vẫn giữ phiên bản an toàn hơn làm cấu hình chính. Không kiểm chứng được thì nêu quan điểm một lần rồi làm theo người chịu trách nhiệm.

**Vị trí chi phí bằng một phần nhỏ FTE — làm sao để xứng đáng?**
> Để team dùng được kết quả mà không phải kèm tôi nhiều: tài liệu đọc là áp dụng được, báo cáo trung thực cả thứ không hiệu quả, tự tìm hiểu trước khi hỏi, và hỏi có trọng tâm kèm những gì đã thử.

**Hai năm nữa muốn ở đâu?**
> Trong AI platform team, giỏi thật sự về đánh giá và cải thiện chất lượng hệ thống AI. JD nói project này là đường vào team đó — đó là con đường tôi muốn đi.

## Khi gặp câu không biết

> Tôi chưa làm phần này. Nếu phải làm, tôi sẽ bắt đầu bằng… và thứ tôi sẽ tìm hiểu trước là…

---

## Liên quan

- [[HR_interview]] — vòng trước; câu giới thiệu, why Katalon, strengths/weakness
- [[Job Fundamentals 07 - Testing]] — test hệ thống không tất định, Ragas/DeepEval, CI
- [[Job Fundamentals 05 - Backend cho AI-DE]] — FastAPI, async, lifespan, health check
- [[Job Fundamentals 06 - Nghề dev thực chiến]] — debug, đọc codebase, PR
