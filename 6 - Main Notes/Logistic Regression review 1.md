2025-04-05 19:46


Tags: [[data scientist]], [[Machine Learning]], [[regression]], [[classification]], [[Logistic Regression]]

# Logistic Regression review 1

- Có các loại bài toán classification sau:
	- Binary Classification
	- Multi-class  Classification
	- Multi-class multi-label classification
- Ví dụ với bài toán theo tuổi, thông thường người ta sẽ giải quyết với bài toán regression (based on khoảng cách hay mối quan hệ giữa các datasample hoặc output expectation của người xây dựng)
- **Về Binary Classification**
- Tại sao output của các bài toán phân loại nhị phân thường không phải là pricisely $0$ hoặc $1$
	$=>$ Instead of just predicting the class, binary classifier gives the probability of the datasample being that class
- **Logistic regression** chỉ là linear regression bọc trong sigmoid 
- **Logistic regression** sử dụng cross entropy làm loss function thay vì MSE
- Ví dụ với bài toán phân loại email có threshold là 0.5, ta có câu hỏi rằng: *intuition and impact of having threshold >= 0.5 or <= 0.5*
	$=>$ Điều chỉnh threshold dựa trên kết quả, yêu cầu hay ngữ cảnh của bài toán (ví dụ như trong giai đoạn đầu covid khi tình hình còn nghiêm trọng và khó lường trước thì threshold nên rất nhỏ và loose dần về sau)
	- Việc điều chỉnh threshold được gọi là *threshold calibration*

# References
