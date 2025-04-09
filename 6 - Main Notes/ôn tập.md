2025-04-09 18:21


Tags: [[data scientist]],

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

# References
