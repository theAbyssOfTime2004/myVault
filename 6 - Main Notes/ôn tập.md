2025-04-09 18:21


Tags: [[data scientist]], [[review]] 

# ôn tập
### Tổng hợp các câu hỏi (có thể được hỏi khi intern) thu thập được 

1. explain how F1-score balances precision and recall. When is F1 - score preferred over individual metrics
	- Precision = $\frac{TP}{TP + NP}$ : trong tổng số dự đoán đúng, có bao nhiêu thật sự đúng
	- Recall = $\frac {TP}{TP + FN}$: trong tổng số outcom thật sự đúng, ta dự đoán đúng được bao nhiêu (độ phủ)
	- F1-score = $$2 \times \frac{precision \times recall}{precision + recall}$$
	- F1-score chính là trung bình điều hòa (*mean harmonic*) của precision và recall -> nhạy cảm hơn với sự mất căng bằng
	- Nếu precision hoặc recall quá thấp thì F1-score cũng sẽ thấp, F1-score **không cho phép 1 trong 2 cái quá cao còn cái còn lại quá thấp**
	- **when to use F1-score over individual metrics** 
		- Khi ta cần cân bằng cả 2 precision và recall: ví dụ như trong bài toán phân loại thư rác và nhận diện bệnh: ta sẽ muốn precision cao (vì ta không muốn cảnh báo nhầm) và recall cao (cần độ phủ cao vì ta không muốn bỏ sót trường hợp nào)
2. Hạn chế của các mô hình Seq2Seq truyền thống: tại sao các mô hình này gặp khó khăn với long term dependencies và tại sao cơ chế attention giúp giải quyết được vấn đề này
	- **Mô hình Seq2Seq**: là mô hình có thiết kế **encoder-decoder** dùng để chuyển 1 chuỗi đầu vào thành 1 chuỗi đầu ra
		- **Encoder** dùng để embedding chuỗi đầu vào thành vector
		- **Decoder** sử dụng vector đó để sinh chuỗi đầu ra
	- **Hạn chế của long-term dependencies**: khi các chuỗi đầu vào quá dài sẽ khiến mô hình "quên" đi (nghĩa là không còn thông tin về chuỗi đấy hoặc trọng số khá thấp khiến thông tin bị phai nhạt) thông tin đó theo thời gian dẫn đến đầu ra không ổn định
	- **Cơ chế attention giải quyết vấn đề này như thế nào**: attention cho phép decoder truy cập đến từng phần tử đầu vào tại mỗi bước sinh đầu ra (với mỗi từ )
# References
