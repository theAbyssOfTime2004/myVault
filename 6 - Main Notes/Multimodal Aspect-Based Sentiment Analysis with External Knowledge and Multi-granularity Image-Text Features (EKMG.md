## Tóm tắt: 
TL;DR: 
- Bài toán: cho **một câu + một ảnh**, tìm **các khía cạnh (aspect terms)** trong câu và **cảm xúc** tương ứng (pos/neg/neu). Mô hình EKMG làm ba việc: 
	- (1) mã hoá văn bản & ảnh và kéo thêm **tri thức ngoài** (AMR cho văn bản, tags cho ảnh)
	- (2) **lọc/nâng cao ngữ nghĩa** bằng hai mạng “làm sạch” (cho text & image) 
	- (3) **căn chỉnh đa mức (multi-granularity)** giữa từ/cụm từ và vùng ảnh qua một **đồ thị GAT** rồi học tương phản ảnh-văn bản; cuối cùng **decoder BART** sinh ra các aspect và polarity.
- **Input** gồm cặp câu S và ảnh V đi kèm - là dữ liệu kiểu tweet có cả text và ảnh
- **Mục tiêu:** nhận diện tất cả các **aspect terms** có trong câu và **gán cảm xúc** cho từng aspect
- Output: mô hình tạo ra **chuỗi** biểu diễn các aspect và **thẻ cảm xúc** (`<POS>/<NEU>/<NEG>`) bằng **BART decoder** (kết hợp đặc trưng img-txt đã căn chỉnh)