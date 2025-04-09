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
	- **Ảnh hưởng như thế nào đến model generalization**: 
		- Mô hình sẽ khó học được quy luật bởi vì dữ liệu quá lộn xộn làm cho mô hình khó tìm được pattern chung 
		- Dễ bị overfitting vì mô hình sẽ học cả những dữ liệu nhiễu 
		![[Pasted image 20250409204735.png]]
		- (Ví dụ giải thích nhiễu)
	- **Regularization** giúp xử lý high variance như thế nào: 
		- **Regularizatio** là kỹ thuật đưa thêm "hình phạt" (*penalty*) vào quá trình huấn luyện giúp giảm độ phức tạp mô hình, cải thiện khả năng tổng quát hóa trên dữ liệu mới.
		![[Pasted image 20250409205248.png]]

4. ==Handling imbalance data: giải thích tác dụng của cost-sensitive learning trong scenario imbalance data==
	- **Cost-sensitive learning** : là kỹ thuật gán trọng số lên các label có chi phí đặc biệt (quan trọng hơn và cần được chú ý nhiều hơn các label còn lại), ví dụ như là fraud transaction trong bài toán classify good and bad transaction với tỉ lệ imbalance data giữa good và bad transaction là 99% và 1%, vì fraud transaction ở đây quá ít nên ta cần chú ý đến label này nhiều hơn
		- Mục tiêu của *cost-sensitive* là *lỗi đối với minor class phải bị trừng phạt nhiều hơn khi sai*
	- **Cost-sensitive learning giúp gì trong imbalance data**: 
		- Mô hình sẽ tăng trọng số lỗi ở lớp thiểu số khiến cho sự trừng phạt khi sai ở lớp này nặng hơn từ đó mô hình sẽ tránh lặp lại lỗi xảy ra ở lớp này
		- Nếu precision hay độ phủ (recall) thấp ở lớp nhỏ  thì việc áp dụng cost-sensitive learning sẽ khiến mô hình đặc biệt chú ý đến các lớp quan trọng
# References
