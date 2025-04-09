2025-04-09 18:21


Tags: [[data scientist]], [[review]] 

# ôn tập
### Tổng hợp các câu hỏi (có thể được hỏi khi intern) thu thập được 

1. ==explain how F1-score balances precision and recall. When is F1 - score preferred over individual metrics==
	- Precision = $\frac{TP}{TP + NP}$ : trong tổng số dự đoán đúng, có bao nhiêu thật sự đúng
	- Recall = $\frac {TP}{TP + FN}$: trong tổng số outcom thật sự đúng, ta dự đoán đúng được bao nhiêu (độ phủ)
	- F1-score = $$2 \times \frac{precision \times recall}{precision + recall}$$
	- F1-score chính là trung bình điều hòa (*mean harmonic*) của precision và recall -> nhạy cảm hơn với sự mất căng bằng
	- Nếu precision hoặc recall quá thấp thì F1-score cũng sẽ thấp, F1-score **không cho phép 1 trong 2 cái quá cao còn cái còn lại quá thấp**
	- **when to use F1-score over individual metrics** 
		- Khi ta cần cân bằng cả 2 precision và recall: ví dụ như trong bài toán phân loại thư rác và nhận diện bệnh: ta sẽ muốn precision cao (vì ta không muốn cảnh báo nhầm) và recall cao (cần độ phủ cao vì ta không muốn bỏ sót trường hợp nào)
2. ==Hạn chế của các mô hình Seq2Seq truyền thống: tại sao các mô hình này gặp khó khăn với long term dependencies và tại sao cơ chế attention giúp giải quyết được vấn đề này==
	- **Mô hình Seq2Seq**: là mô hình có thiết kế **encoder-decoder** dùng để chuyển 1 chuỗi đầu vào thành 1 chuỗi đầu ra
		- **Encoder** dùng để embedding chuỗi đầu vào thành vector
		- **Decoder** sử dụng vector đó để sinh chuỗi đầu ra
	- **Hạn chế của long-term dependencies**: khi các chuỗi đầu vào quá dài sẽ khiến mô hình "quên" đi (nghĩa là không còn thông tin về chuỗi đấy hoặc trọng số khá thấp khiến thông tin bị phai nhạt) thông tin đó theo thời gian dẫn đến đầu ra không ổn định
	- **Cơ chế attention giải quyết vấn đề này như thế nào**: attention cho phép decoder truy cập đến từng phần tử đầu vào do đó tạo ra context vector riêng cho từng bước dự đoán (với mỗi từ) -> cho phép mô hình nhìn lại toàn bộ các đầu vào xác định mối quan hệ giữa các từ, từ đó khắc phục được vấn đề trên
	- **Lưu ý:** *Word2Vec* hay *GloVe* là các mô hình word embedding, không phải Seq2Seq
3. ==Cho ví dụ về High Variance data và cho biết nó ảnh hưởng như thế nào đến model generalization, và regularization giúp xử lý High Variance Data như thế nào?==
	- **High Variance Data** (Dữ liệu có phương sai cao) là những dữ liệu có khoảng sai số rộng và sự phân tán lớn so với mean.
	- **Ví dụ về High Variance Data**: 
		-  **Dữ liệu dự báo thời tiết**: Nhiệt độ biến thiên rõ rệt (nhiệt độ âm -> nhiệt độ dương) qua các mùa 
		- **Dữ liệu giá nhà**: Nhiều nhà giá rất rẻ và nhiều nhà giá rất cao 
# References
