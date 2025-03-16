2025-03-16 10:57


Tags: [[data mining]]

# Scalability Issues And The Streaming Scenario
- Với lượng dữ liệu ngày càng lớn thì chúng ta có 2 tình huống mở rộng như sau:
	- Dữ liệu được chứa trên một hoặc nhiều máy, nhưng quá nhiều để xử lý một cách hiệu quả
	- Dữ liệu được sinh ra liên tục theo thời gian và với lượng lớn, việc đã lưu trữ toàn bộ không thực tế. Đây là tình huống dòng dữ liệu. (*Data streaming scenario*)
- The streaming scenario has increasingly popular because of advances in data collection technology that can collect large amount of data over time. The major challenges that arise in the context of data stream processing are as follows:
	- **One-pass constraint**: Một số thuật toán phải xử lý toàn bộ tập dữ liệu chỉ trong **một lần quét duy nhất**. Sau khi một mục dữ liệu đã được xử lý và thông tin quan trọng đã được trích xuất, dữ liệu thô sẽ bị loại bỏ và không thể truy cập lại. Lượng dữ liệu có thể xử lý tại một thời điểm phụ thuộc vào bộ nhớ có sẵn để lưu trữ tạm thời các phần dữ liệu.
	- **Concept drift**: Trong nhiều ứng dụng, **phân bố dữ liệu có thể thay đổi theo thời gian**, làm ảnh hưởng đến độ chính xác của các mô hình khai phá dữ liệu hoặc học máy.
		- For example, the pattern of sales in a given hour of a day may not be similar to that at another hour of day
## A Troll Through Some Application Scenarios
- **Store Product Placement**
![[Pasted image 20250316111133.png]]
	-  **Vấn đề:** Làm sao sắp xếp sản phẩm trên kệ để tối ưu hóa việc mua sắm.
	- **Giải pháp:** Sử dụng khai phá mẫu thường xuyên (*frequent pattern mining*) để tìm sản phẩm hay được mua cùng nhau, sau đó áp dụng thuật toán heuristic để tối ưu bố cục kệ hàng.
	- **Thực tế:** Không có một mô hình chung cho mọi cửa hàng, việc tối ưu cần được điều chỉnh dựa trên thực nghiệm.
- **Customer Recommendations**
![[Pasted image 20250316111150.png]]
- Bài toán này là một dạng đơn giản của **Collaborative Filtering** trong hệ thống gợi ý. Có nhiều cách giải quyết, trong đó tài liệu đề xuất ba cách với độ phức tạp tăng dần:
1. **Dùng Association Rule Mining (Luật kết hợp)**
    - Áp dụng thuật toán khai phá luật kết hợp (ví dụ: Apriori, FP-Growth) để tìm các sản phẩm thường xuyên mua cùng nhau.
    - Nếu khách hàng đã mua các sản phẩm $A, B,$ ta tìm luật dạng $A,B \Rightarrow C$
    - Nếu $C$ xuất hiện nhiều trong các giao dịch có $A, B,$ thì ta đề xuất $C$ cho khách hàng.
2. **Dùng Similarity Between Customers (Tìm khách hàng tương tự)**
    - Thay vì chỉ dựa vào luật kết hợp, ta tìm những khách hàng có hành vi mua sắm **giống nhau**.
    - Với một khách hàng cần gợi ý, ta tìm những khách hàng tương tự nhất (hàng trong ma trận giống nhau nhất).
    - Sau đó, đề xuất những sản phẩm phổ biến mà nhóm khách hàng tương tự đã mua.
3. **Dùng Clustering (Phân cụm khách hàng)**
    - Chia khách hàng thành các nhóm dựa trên thói quen mua hàng bằng thuật toán phân cụm (ví dụ: K-Means, DBSCAN).
    - Trong từng cụm, áp dụng phương pháp khai phá mẫu thường xuyên để tìm sản phẩm phổ biến.
    - Đề xuất sản phẩm phổ biến nhất trong nhóm cho từng khách hàng thuộc nhóm đó
- **Medical Diagnosis*
![[Pasted image 20250316111526.png]]
- Chẩn đoán y khoa dựa trên dữ liệu ECG có thể được tiếp cận theo nhiều hướng khác nhau.
- Nếu **không có nhãn**, ta áp dụng **phát hiện bất thường** để tìm tín hiệu khác biệt.
- Nếu **có nhãn**, ta áp dụng **phân loại chuỗi thời gian** để dự đoán bệnh.
- Dữ liệu y khoa thường mất cân bằng, nên cần áp dụng kỹ thuật xử lý như **tái mẫu (resampling), trọng số (class weighting), hoặc mô hình học sâu đặc thù** để cải thiện hiệu suất.
- **Web log Anomalies**
![[Pasted image 20250316112220.png]]- Tương tự như chẩn đoán tín hiệu ECG, cách tiếp cận vấn đề sẽ khác nhau tùy theo dữ liệu đầu vào:
	1. **Phát hiện bất thường không giám sát (Unsupervised Anomaly Detection)**
	    - Nếu không có nhãn (tức là không biết trước đâu là hoạt động bình thường, đâu là bất thường), ta sử dụng các thuật toán **phát hiện bất thường không giám sát**.
	    - Các phương pháp phổ biến:
	        - **Phân cụm chuỗi sự kiện (Sequence Clustering)**: Phát hiện các chuỗi không thuộc cụm nào.
	        - **Mô hình Markov (Markovian Models)**: Phát hiện các chuỗi sự kiện bất thường dựa vào mô hình xác suất.
	2. **Phát hiện bất thường có giám sát (Rare Class Detection)**
	    - Nếu có dữ liệu nhãn (có mẫu nhật ký web bất thường), ta có thể **huấn luyện mô hình học máy để phát hiện mẫu lạ**.
	    - Đây là bài toán **phát hiện lớp hiếm** vì số lượng mẫu bất thường ít hơn nhiều so với mẫu bình thường.
# References
