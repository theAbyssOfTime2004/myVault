---
tags: [home-credit, interview, data-engineer, mock-interview]
created: 2026-06-24
role_target: Data Engineer (Fresher/Junior) @ Home Credit
---

# Home Credit — Mock Interview Prep (Data Engineer)

## 0. Định vị bản thân trước khi vào phỏng vấn

CV hiện tại nặng về **AI Engineer (LLM/RAG/Agent)** — 2 internship thật (Tiger Tribe, Solazu) đều là GenAI, không phải DE. Nhưng có **1 project Data Engineering nghiêm túc, đúng chất**: **Lichess Feature Store** (`18_DE_FeatureStore`) — Lakehouse Medallion (MinIO+Delta), Spark batch, Kafka+Flink streaming, Airflow orchestration, Trino SQL, Redis online store, deploy GKE qua Terraform. Đây là project phải **lead với nó trong mọi câu hỏi project**.

**Chiến lược:** Nền Data Science (VNUHCM) + project DE thật + 2 internship AI Engineer là *bằng chứng làm việc với data pipeline / production system thật*, không phải chỉ học lý thuyết. Đừng cố biến mình thành "DE thuần" giả tạo — frame là: *"Em base là Data Science, đã tự build 1 data platform end-to-end theo đúng kiến trúc production (lakehouse + batch + streaming + serving), và 2 internship AI Engineer cho em kinh nghiệm thực chiến về pipeline dữ liệu cho LLM (ingestion, ETL-like chunk/embed, latency optimization)."*

**Điểm bán hàng đặc biệt ăn khớp với Home Credit:** Lichess project có khái niệm **point-in-time correctness / chống data leakage** (`rowsBetween(unboundedPreceding, -1)` — chỉ dùng dữ liệu TRƯỚC thời điểm dự đoán) để train model anomaly detection. Đây **chính xác là vấn đề lớn nhất trong credit risk scoring** (không được dùng thông tin "tương lai" như đã trả nợ hay chưa để dự đoán khả năng trả nợ). Nhắc điểm này khi nói về project — nó cho thấy hiểu đúng bài toán mà một công ty tài chính tiêu dùng quan tâm nhất.

---

## 1. "Introduce yourself"

**Khung trả lời (60-90s, theo công thức Present → Past → Future):**

> "Em là Mai Phong Đăng, sinh viên năm cuối Data Science tại Đại học Khoa học Tự nhiên TP.HCM, GPA 3.5/4.0, đang làm khoá luận về test-time learning cho code generation.
>
> Về kinh nghiệm thực chiến, em có 2 kỳ thực tập AI Engineer — ở Solazu em làm pipeline RAG cho chatbot e-commerce (ingestion crawl/chunk/embed dữ liệu vào vector DB, giảm ~30% latency), ở Tiger Tribe em build hệ thống multi-agent xử lý hội thoại real-time cho một sản phẩm của Heineken.
>
> Song song đó em tự build một project Data Engineering hoàn chỉnh: một feature store theo kiến trúc Lakehouse trên 100GB+ dữ liệu cờ vua Lichess — batch pipeline với Spark + Delta Lake, streaming với Kafka + Flink windowed aggregation, orchestrate bằng Airflow, deploy trên GKE qua Terraform, và một điểm em đầu tư kỹ là tính **point-in-time correctness** để tránh data leakage khi build feature cho model.
>
> Em ứng tuyển vị trí Data Engineer ở Home Credit vì em muốn áp dụng nền tảng đó vào một bài toán có tác động thật — dữ liệu tài chính tiêu dùng, nơi data pipeline đúng và sạch trực tiếp ảnh hưởng đến quyết định cho vay."

**Lưu ý:** Đừng đọc thuộc lòng cứng — nói tự nhiên, nhấn đúng 3 điểm: **nền tảng học thuật + 1 DE project thật + lý do chọn Home Credit**.

---

## 2. "Why this position / this company" (hỏi dạng khác đi, không hỏi thẳng)

Có thể được hỏi gián tiếp qua: *"Em hiểu Home Credit làm gì?"*, *"Điều gì khiến em apply công ty tài chính tiêu dùng thay vì công ty tech thuần?"*, *"Em thấy data ở Home Credit khác gì so với project cờ vua em làm?"*

**Trả lời mẫu:**

> "Em chọn Home Credit vì hai lý do. Một, Home Credit là công ty tài chính tiêu dùng phục vụ nhóm khách hàng 'thin-file' — chưa có lịch sử tín dụng truyền thống — nên phải dựa rất nhiều vào dữ liệu hành vi thay thế (alternative data) và mô hình rủi ro tín dụng để ra quyết định nhanh, ở quy mô nhiều thị trường. Đó là bài toán data engineering thật, có ràng buộc thật (chính xác, đúng giờ, đúng quy định), không phải bài toán demo.
>
> Hai, project em tự làm — feature store cho phát hiện gian lận trong cờ vua — về bản chất kiến trúc giống hệt bài toán credit risk: cần feature point-in-time-correct, cần serving nhanh (online store), cần pipeline batch lẫn streaming. Em muốn mang nền tảng đó vào một domain có ý nghĩa thật với hàng triệu khách hàng, thay vì tiếp tục làm trên dữ liệu public/demo."

---

## 3. "Tell about a time you made a mistake and how you resolved it" (hỏi dạng khác đi)

Có thể hỏi: *"Kể một lần em gặp vấn đề kỹ thuật và cách em xử lý"*, *"Project nào em làm sai và phải sửa lại?"*

**STAR — dùng bug thật từ Lichess Feature Store (B8 trong `end_to_end_walkthrough.md`):**

- **Situation:** Khi build bronze→silver layer của pipeline (Spark ghi dữ liệu games đã parse vào Delta Lake, partition theo tháng + loại cờ), em cần ghi đè dữ liệu của tháng đang chạy lại khi sửa logic parser.
- **Task:** Ghi đè (overwrite) đúng phần dữ liệu của tháng đó mà không ảnh hưởng dữ liệu các tháng khác đã có.
- **Action:** Em dùng `mode("overwrite")` mặc định của Spark — không để ý rằng theo mặc định, overwrite sẽ **xoá toàn bộ partition của bảng**, không chỉ phần đang ghi. Khi chạy lại job cho tháng mới, dữ liệu của các tháng cũ đã build trước đó bị xoá sạch mà em không nhận ra ngay (vì job vẫn "chạy thành công", không báo lỗi).
- **Em phát hiện ra sao:** Khi check lại Delta table để debug một việc khác, thấy chỉ còn 1 tháng dữ liệu thay vì nhiều tháng đã chạy trước.
- **Resolution:** Tìm ra nguyên nhân là Spark partition overwrite mode mặc định là `static`. Fix bằng cách set `spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")` — chỉ ghi đè đúng partition đang xử lý, giữ nguyên các partition khác. Sau đó viết lại toàn bộ dữ liệu các tháng đã mất.
- **Learning:** Từ đó em có "reflex" mới — bất kỳ write operation nào trên dữ liệu partition, luôn explicit kiểm tra/set overwrite mode, không tin vào default; và luôn có cách verify (đếm số partition/rows trước-sau) sau mỗi lần ghi dữ liệu quan trọng, không chỉ tin job "chạy xanh" là đúng.

**Tại sao chọn câu chuyện này:** nó là lỗi kỹ thuật thật, cụ thể, có root cause rõ và bài học chuyển hoá thành hành vi cụ thể (không phải bài học sáo rỗng "em học được phải cẩn thận hơn"). Đặc biệt hợp với DE interview vì đụng đúng vào silent data loss — rất liên quan đến lo ngại về data integrity trong ngành tài chính.

---

## 4. "Tell about a time you encountered a conflict and how you overcame it"

> ⚠️ **Trong vault không có ghi chép cụ thể một conflict thật đã xảy ra.** Phần dưới là khung STAR dựng từ context project thật (seminar nhóm MABSA — `11_Seminar_MABSA`, có nhiều buổi research + 2 round meeting note) — **bạn cần điền lại bằng tình huống thật của chính bạn** trước khi dùng, vì phỏng vấn viên sẽ hỏi xoáy chi tiết (ai nói gì, cảm xúc lúc đó, kết quả cụ thể) và một câu chuyện không thật sẽ lộ ngay khi bị hỏi sâu.

**Khung gợi ý (điền lại bằng trải nghiệm thật):**

- **Situation:** [Bối cảnh nhóm — VD: làm seminar nghiên cứu nhóm, hoặc trong internship khi 2 người có hướng kỹ thuật khác nhau]
- **Task:** [Vấn đề cụ thể cần thống nhất — VD: chọn kiến trúc model A vs B, hoặc chia việc không đều]
- **Action:** Em chủ động đề nghị 1-1 trước khi đưa ra group, lắng nghe lý do của người kia trước khi bảo vệ ý mình, tìm điểm chung (tiêu chí khách quan: data/deadline/effort) thay vì tranh luận quan điểm.
- **Result:** [Kết quả cụ thể — quan hệ làm việc sau đó, deliverable có đúng hạn không]
- **Learning:** Conflict về công việc (technical disagreement) nên giải quyết bằng dữ liệu/tiêu chí khách quan, conflict về cá nhân nên giải quyết riêng tư trước khi đưa ra nhóm.

**Việc cần làm trước interview:** chọn 1 tình huống thật (gợi ý: trong Tiger Tribe — quyết định 4-agent kiến trúc; hoặc trong Solazu — chọn chunk size/threshold; hoặc trong nhóm seminar MABSA) và viết lại theo khung trên bằng giấy, tập nói to.

---

## 5. Project deep dive — chuẩn bị câu hỏi follow-up

### 5.1 Lichess Feature Store (ưu tiên #1 — DE thật)

**Một câu mở đầu:** *"Em build một feature store theo kiến trúc Lakehouse Medallion trên 100GB+ dữ liệu cờ vua Lichess: batch pipeline (Spark, Delta Lake, Trino) song song với streaming pipeline (Kafka, Flink windowed aggregation), serving qua Redis + FastAPI, orchestrate bằng Airflow, hạ tầng dựng bằng Terraform trên GKE — nuôi một model phát hiện gian lận với feature point-in-time-correct."*

| Câu hỏi có thể gặp | Trả lời ngắn |
|---|---|
| Tại sao cần Lakehouse, không chỉ Data Warehouse? | Dữ liệu thô (PGN text) không có schema cố định ngay từ đầu, cần giữ raw để parse lại khi sửa logic; Lakehouse (Delta trên object storage) cho phép schema-on-read + versioning + rẻ hơn warehouse truyền thống cho dữ liệu thô lớn |
| Tại sao file `.zst` không đọc song song được? | Format nén zstd không splittable — 1 file = 1 task = 62-75h/tháng. Giải pháp: bước "shred" decompress 1 lần rồi cắt theo ranh giới ván thành N shard → 75 phút xuống 4 phút |
| Point-in-time correctness là gì, sao quan trọng? | Khi tính feature lịch sử của 1 entity tại thời điểm X, chỉ dùng dữ liệu TRƯỚC X (`rowsBetween(unboundedPreceding, -1)` trong Spark Window). Nếu lỡ dùng dữ liệu tương lai → data leakage → model train đẹp nhưng vô dụng lúc serving thật. **Đây chính là vấn đề lớn nhất trong credit scoring** (không dùng outcome tương lai để dự đoán) |
| Batch vs streaming, sao cần cả hai? | Batch (Spark) tính feature lịch sử sâu, không cần nhanh; Streaming (Flink) tính feature hành vi real-time (nhịp đánh đều/bất thường trong game đang diễn ra) cần latency thấp — 2 loại tín hiệu khác nhau, bổ sung cho nhau |
| Offline store vs online store khác gì? | Offline (Delta trên MinIO) — đầy đủ, dùng train, query chậm (giây). Online (Redis) — chỉ feature cần cho serving, tra cứu ms. Materialize job copy từ offline sang online định kỳ |
| Sao chọn GKE tự quản thay vì managed service (Dataproc, MWAA)? | Trade-off có chủ đích: tự quản trong free credit $300, vẫn đáp ứng yêu cầu "deploy thật"; đổi lại phải tự lo operator/RBAC/capacity (biết rõ các bug đã gặp — B10-B15) |
| Vấn đề khó nhất đã gặp? | Bug Flink: một `MapFunction` ghi Redis không có downstream sink → Flink optimizer **tự cắt bỏ nó khỏi execution graph** → job chạy RUNNING không lỗi nhưng không ghi gì vào Redis. Loại bug nguy hiểm nhất: "chạy không lỗi nhưng không có tác dụng". Fix: thêm sink `.print()` để giữ trong graph |
| Đã chạy full 100GB+ chưa? | **Thành thật:** kiến trúc + pipeline đã verify đúng trên 1 tháng dữ liệu thật có annotation; full-scale run (~120GB) là bước cuối, đã thiết kế sẵn shred + spot autoscale để gánh được scale đó |
| Cái gì sẽ làm khác nếu làm lại? | Thêm state TTL cho Flink (state phình vô hạn theo game_id chưa được clear), thêm checkpointing (hiện tại restart Flink mất state), cân nhắc exactly-once sink nếu nghiệp vụ cần |

### 5.2 Face Anti-Spoofing MLOps (dùng cho câu hỏi về CI/CD, infra)

- Terraform provision GKE, Helm deploy FastAPI service, HPA autoscaling, Prometheus+Grafana, GitHub Actions CI/CD với Workload Identity Federation (không lưu key tĩnh), pytest coverage-gated.
- Nếu hỏi sâu: tại sao GKE không phải Cloud Run? → cần control fine-grained autoscaling (HPA theo custom metric) + đã có sẵn pattern tái dùng cho project Feature Store.

### 5.3 Solazu (RAG ingestion — frame như ETL-like pipeline)

- Ingestion pipeline: sitemap crawl → clean → chunk → embed (`text-embedding-3-small`) → load vào Supabase pgvector — về bản chất là một **ETL pipeline cho dữ liệu unstructured**, có thể frame: extract (crawl), transform (clean/chunk), load (embed+index).
- Số liệu: giảm ~30% latency, tăng ~20% retrieval recall.

### 5.4 Tiger Tribe / Thesis SDPO

- Backup, chỉ cần biết tóm tắt 1-2 câu, không phải trọng tâm cho vai trò DE — nếu hỏi sâu thì trả lời ngắn rồi lái lại Lichess Feature Store.

---

## 6. Tình huống lãnh đạo: leader nhóm 5 người, vừa lead vừa làm data analysis, 3 vấn đề trong 1 ngày

**Vấn đề:** (1) CEO yêu cầu gửi kết quả sớm 1 tháng, (2) 1 member mất liên lạc, (3) team khác bị lỗi system cần mình hỗ trợ.

**Khung trả lời — Triage theo urgency × impact, không xử lý tuần tự mù quáng:**

> "Em sẽ không xử lý 3 việc này lần lượt theo thứ tự nghe được — em triage nhanh theo mức độ urgent/impact trước khi hành động.
>
> **Đầu tiên (trong 15-30 phút đầu, làm song song):**
> - Với member mất liên lạc: em ưu tiên *con người* trước — thử nhiều kênh (gọi, nhắn, liên hệ người thân/khẩn cấp nếu có theo quy trình công ty), vì có thể là tình huống cá nhân nghiêm trọng, không chỉ là vấn đề công việc.
> - Đồng thời, em nhanh chóng hỏi team khác: lỗi system của họ có ảnh hưởng production / khách hàng / dữ liệu tài chính không? Nếu critical, đó là ưu tiên kỹ thuật cao nhất bất kể team nào.
>
> **Sau đó, với CEO:** Em không trả lời ngay 'được' hoặc 'không được' theo cảm tính. Em xem lại scope hiện tại, xác định phần nào tạo giá trị cao nhất (Pareto — 20% công việc cho ra 80% giá trị kết quả), rồi quay lại CEO với phương án cụ thể: ví dụ 'Full scope đúng deadline gốc, hoặc 70% scope quan trọng nhất giao sớm 1 tháng, hoặc full scope sớm 1 tháng nếu có thêm 1 người support' — để CEO ra quyết định dựa trên trade-off rõ ràng, không phải một lời hứa suông.
>
> **Với việc hỗ trợ team khác:** nếu thật sự critical (ảnh hưởng khách hàng/production), em sẽ cử 1 người trong nhóm có kỹ năng phù hợp hỗ trợ trong thời gian giới hạn (timeboxed), đồng thời báo với manager của 2 team để việc phân bổ người được ghi nhận chính thức — không tự ôm hết một mình vì nhóm chỉ có 5 người và vẫn đang thiếu 1.
>
> **Với phần data analysis của riêng em (vì em vừa là leader vừa làm data):** em sẽ tạm gác việc không-urgent của mình lại để dồn thời gian cho việc điều phối trong ngày khủng hoảng này, rồi catch-up sau."

---

## 7. Follow-up: nếu member đó đưa lý do (excuse) không thỏa mãn, bạn (leader) làm gì?

> "Em tách rõ hai phần: tìm hiểu sự thật, và đánh giá/phản hồi — không làm cùng lúc để tránh phản ứng theo cảm xúc.
>
> Em sẽ nói chuyện riêng 1-1 (không trước mặt cả nhóm), hỏi mở để hiểu rõ tình huống trước khi kết luận đó là 'lý do không chính đáng'. Nhưng nếu sau khi nghe kỹ, lý do thật sự không hợp lý (ví dụ lặp lại, hoặc rõ ràng có thể tránh được), em sẽ phản hồi thẳng nhưng không công kích cá nhân — tập trung vào **impact khách quan**: 'Việc không liên lạc được trong X giờ khiến team mất Y thời gian để re-plan, ảnh hưởng đến deadline chung' — thay vì 'em sai vì lý do của em dở'.
>
> Sau đó em đặt kỳ vọng rõ cho lần sau (ví dụ: bắt buộc báo trước nếu sẽ offline quá X giờ, có kênh backup liên lạc), và hỏi thêm liệu có vấn đề gốc rễ nào (workload quá tải, vấn đề cá nhân, không phù hợp với role) cần giải quyết — vì kỷ luật mà không đi kèm hỗ trợ thường chỉ xử lý triệu chứng, không xử lý nguyên nhân. Nếu việc lặp lại nhiều lần dù đã được nói rõ, em sẽ escalate theo đúng quy trình công ty (HR/quản lý cấp trên), có ghi chép lại cuộc nói chuyện."

---

## 8. "Tưởng tượng làm ở Home Credit, thử thách lớn nhất bạn sẽ gặp là gì?"

> "Thử thách lớn nhất với em là **khoảng cách giữa quy mô project cá nhân em từng làm và quy mô dữ liệu tài chính thật ở Home Credit**. Project Lichess của em chạy trên ~100GB dữ liệu public, không có ràng buộc compliance, sai một chút thì chỉ ảnh hưởng một báo cáo demo. Ở Home Credit, dữ liệu là thông tin tín dụng của khách hàng thật, qua nhiều thị trường, với yêu cầu chính xác, đúng quy định, và sai sót có thể ảnh hưởng trực tiếp đến quyết định cho vay của một người thật.
>
> Em nghĩ thử thách cụ thể sẽ là: học cách làm việc với data lineage/governance nghiêm ngặt hơn nhiều, và tư duy lại 'point-in-time correctness' em đã làm ở mức project cá nhân thành chuẩn production thật — vì đây chính xác là nguyên tắc quan trọng nhất trong credit risk modeling. Em coi đây là khoảng cách cần học nhanh, không phải rào cản không vượt qua được, vì nền tảng (Spark/Delta/point-in-time join) em đã có sẵn, chỉ thiếu kinh nghiệm vận hành ở quy mô doanh nghiệp."

---

## 9. "Điều gì thú vị về Home Credit?"

> "Điều em thấy thú vị nhất là Home Credit phục vụ nhóm khách hàng 'thin-file' — những người chưa có lịch sử tín dụng truyền thống — nên phải dựa vào dữ liệu thay thế (alternative data) và mô hình dữ liệu để ra quyết định cho vay công bằng và nhanh, ở quy mô nhiều quốc gia. Đó là bài toán data engineering có ý nghĩa xã hội thật: pipeline dữ liệu đúng và sạch trực tiếp giúp nhiều người tiếp cận được tài chính mà ngân hàng truyền thống không phục vụ.
>
> Em cũng thấy thú vị ở góc độ kỹ thuật: vận hành data platform ở nhiều thị trường (đa hệ thống core khác nhau, đa định dạng dữ liệu) đòi hỏi engineering rigor cao hơn nhiều so với 1 hệ thống đơn lẻ — đúng loại bài toán em muốn học."

> Lưu ý: kiểm tra lại trên trang tuyển dụng/engineering blog của Home Credit (nếu có) trước ngày phỏng vấn để có 1 chi tiết cụ thể, mới (sản phẩm/sáng kiến gần đây) thay câu trả lời chung này.

---

## 10. "Mong đợi của bạn về leader?"

> "Em mong leader: (1) truyền đạt rõ priority và 'why' đằng sau quyết định, không chỉ giao việc; (2) cho autonomy để tự quyết cách làm, nhưng rõ ràng về accountability; (3) feedback hai chiều — nói thẳng khi em làm chưa tốt, và sẵn sàng nghe khi em thấy hướng khác hợp lý hơn; (4) chắn được 'noise' không cần thiết (politics, thay đổi yêu cầu liên tục) để team tập trung làm việc; (5) đầu tư vào việc em phát triển kỹ năng, không chỉ coi em là người hoàn thành task."

---

## 11. "Có kiểu nhân viên nào bạn tránh làm việc với?"

> ⚠️ Trả lời tránh chê người, tập trung vào **hành vi cụ thể**, và luôn kèm cách bạn vẫn cố gắng làm việc được với họ — câu trả lời "tôi ghét người lười" nghe thiếu chuyên nghiệp.

> "Em không nghĩ theo kiểu 'tránh làm việc với ai' vì trong môi trường công việc mình không luôn được chọn người làm cùng. Nhưng hành vi em thấy khó làm việc nhất là **không chủ động báo khi bị block hoặc gặp vấn đề** — để đến gần deadline mới lộ ra là đang trễ hoặc gặp khó, vì lúc đó team không còn đủ thời gian xử lý. Ngay cả với kiểu đồng nghiệp này, em vẫn cố gắng tạo môi trường an toàn để họ báo sớm — ví dụ check-in ngắn thường xuyên hơn thay vì chỉ hỏi khi deadline gần — vì thường nguyên nhân là sợ bị đánh giá, không phải vô trách nhiệm."

---

## 12. Câu hỏi chuẩn bị để hỏi lại HR (bắt buộc phải hỏi, đừng nói "em không có câu hỏi gì")

Chọn 1, ưu tiên theo thứ tự:

1. **(Khuyến nghị)** *"Trong vai trò Data Engineer, đâu là thử thách về dữ liệu lớn nhất mà team đang đối mặt trong 6-12 tháng tới, và một fresher như em có thể chuẩn bị gì để đóng góp sớm nhất?"* — cho thấy tư duy hướng-đóng-góp, không chỉ hỏi về quyền lợi.
2. *"Team Data Engineering ở Home Credit làm việc với data từ nhiều thị trường (Việt Nam, Indonesia, Philippines...) như thế nào — có chuẩn hoá chung hay mỗi market một stack riêng?"* — cho thấy đã suy nghĩ về đặc thù multi-country của công ty.
3. *"Lộ trình onboarding/mentorship cho fresher Data Engineer trong 3 tháng đầu thường như thế nào?"* — an toàn, luôn dùng được.

---

## Checklist trước ngày phỏng vấn

- [ ] Tập nói to phần 1 (introduce) và 3 (mistake) không nhìn note, dưới 90s mỗi câu
- [ ] **Viết lại phần 4 (conflict) bằng câu chuyện thật của chính mình** — phần này hiện chỉ là khung
- [ ] Đọc lại `18_DE_FeatureStore/end_to_end_walkthrough.md` mục 12 (cheat sheet) trước khi vào phòng
- [ ] Tìm 1 thông tin mới/cụ thể về Home Credit (sản phẩm, sáng kiến, engineering blog nếu có) để trả lời câu 9 sắc hơn
- [ ] Chốt 1 câu hỏi hỏi lại HR (mục 12) — học thuộc, đừng đọc

## Related

- [[../18_DE_FeatureStore/end_to_end_walkthrough.md]] — chi tiết kỹ thuật project chính
- [[../18_DE_FeatureStore/plan.md]] — rubric/kiến trúc gốc
- [[../15_Zalo_Fresher_Prep/Phase3_Interview_Prep]] — format CV deep dive tham khảo (đợt Zalo trước)
- CV: `cv_expanded.tex`, `cv_nttdata.tex`
