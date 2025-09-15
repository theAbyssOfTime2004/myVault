- Hiện tại đã có baseline model với kiến trúc gồm: 
	- `bert-model`: để tokenizing và encoding (tạo embeddings)
	- `gnn layer`: gồm có *sematic graph (dựa trên attention)* và *syntactic graph (sử dụng dependency tree từ scipy*
	- `gate fusion`: để kết hợp cả 2 output từ *h_syn* và *h_sem*
	- `mate_classifier`: classifier cho nhiệm vụ MATE - Phân loại mỗi token là ASPECT hay không
	- `masc_classifier`: classifier cho nhiệm vụ MASC - Phân loại sentiment cho các aspect 
- *Contrastive_loss*: ~~tính loss tương phản giữa aspect và ảnh~~
	=> Cần sửa lại theo paper - tận dụng *syntactic graph* và *semantic graph* với 2 strategy chính là **Cross-scope Contrast** và **Cross-graph Contrast** 
- cần thay đổi encoder từ BERT sang FSUIE-base 
- thử nghiệm phần pretraining gồm:
	- tạo `SceneGraph`: trong bài báo **sử dụng GPT-4o để sinh ra các mô tả văn bản có cấu trúc, chi tiết và cụ thể hơn cho mỗi hình ảnh**
	- dùng SceneGraph làm đầu vào cho Qformer (với tham số khởi tạo lấy từ 1 bài báo khác được cited kèm theo): cho phép ánh xạ các img feature -> miền văn bản và thực hiện việc kết nối, căn chỉnh đặc trưng giữa img và text. Điều này giúp **giảm thiểu vấn đề MIM**
	- **Aspect-Oriented enhancement**:cải thiện độ nhạy trong việc bắt khía cạnh
	- **Image-Text Matching**
	- **Aspect-level Sentiment-Sensitive Cognition**: tăng khả năng nhận thức sentiment của mô hình, trực tiếp **giải quyết vấn đề SCP**
	`Loss_p = Loss_𝑄 + Loss_𝐴𝑂𝐸 + Loss_𝐼𝑇𝑀 + Loss_𝐴𝑆𝑆𝐶`
	