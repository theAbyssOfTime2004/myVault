2025-04-05 19:57


Tags: [[Logistic Regression review 1]], [[Logistic Regression]]

# Logistic Regression review 2

### Loss Function
**MSE không phù hợp**:
- Nếu dùng MSE với logistic regression, hàm loss sẽ là 1 hàm non-convex do $sigmoid^2$, làm cho quá trình tối ưu khó hội tụ về điểm cực tiểu.
![[Pasted image 20250405201601.png]]

- Giải Pháp: 
	- Sử dụng **Binary Cross Entropy** (BCE) làm hàm loss:
	$$L = -[y \log(\hat{y}) + (1 - y)\log(1 - \hat{y})]$$
	![[Pasted image 20250405201740.png]]
	- Một cách intuitive hơn để hiểu tại sao ta có thể viết hàm BCE loss thành như trên được là:
	  ![[Pasted image 20250413155445.png]]
	- **việc giảm thiểu mất mát hay minimizing cost function thực chất là ta đang thực hiện ước lượng hợp lý cực đại nhưng bỏ dấu - đi**
	=> hàm J(theta) trong hình trước đó chính là hàm loss cho 1 điểm dữ liệu và đối với toàn bộ điểm dữ liệu thì nó sẽ trở thành hàm cost và thêm 1/m để lấy trung bình, và việc có được hàm loss ban đầu (cũng như hàm cost) chính là nhờ vào MLE và nhiệm vụ của gradient descent là minimizing hàm cost (hay là minimizing negative log-loss or negative log-likelihood)
**Regularization term**:
- Được chèn vào hàm loss để giúp model khống chế độ lớn của theta 
![[Pasted image 20250405201711.png]]
- Ý nghĩa λ (lambda):
	- **λ nhỏ** → dễ **overfit**
	- **λ lớn** → dễ **underfit**
### Logistic Regression cho Multi-class Classification
- **Phương pháp One-vs-All (OvA)**:
    - Với N lớp → cần train **N mô hình**.
    - Ví dụ 3 lớp:
        - Mô hình 1: phân biệt lớp 1 và {2,3}
        - Mô hình 2: phân biệt lớp 2 và {1,3}
        - Mô hình 3: phân biệt lớp 3 và {1,2}
    - **Dự đoán**: Chọn lớp có xác suất cao nhất từ 3 mô hình.
- **Nhược điểm**:
    - Tốn **tài nguyên**, **thời gian**, **khó scale**
    -  Trong thực tế, thường **không dùng Logistic Regression** cho multi-class.
	$=>$ Thay vào đó người ta sử dụng **Softmax Regression**
### Softmax Regression
- **Thay thế cho Logistic Regression** khi phân loại nhiều lớp.

- **Flow xử lý**:
    
    1. **Feature transformation**
    2. Tính **Softmax**:$$
P(y = j \mid x) = \frac{e^{z_j}}{\sum_k e^{z_k}}
$$
    3. **Minimize cross-entropy loss**:$$
L = - \sum y_i \log(\hat{y}_i)
$$
![[Pasted image 20250405202207.png]]

### Evaluation Metrics

### **Cách nhớ nhanh**:
- *phần sau* (postive và negative): là phần mà model dự đoán
- *phần trước* (true và false): là dự đoán **đúng hay sai**

|Metric|Ý nghĩa|
|---|---|
|**Precision**|Trong số các sample mô hình dự đoán là **positive**, có bao nhiêu là **thật sự positive**.|
|**Recall**|Trong số các sample **thật sự positive**, mô hình dự đoán đúng bao nhiêu → **độ phủ**.|
|**F1 Score**|Trung hòa giữa precision và recall → nên **cao**.|
|**Accuracy**|Tỉ lệ dự đoán đúng / tổng số mẫu.|

### **Hạn chế của Accuracy**:

- **Không phù hợp với tập dữ liệu mất cân bằng** (Data Imbalance).
- Ví dụ: Fraud detection với 99 giao dịch tốt và 1 fraud → đoán đúng 99 giao dịch tốt nhưng sai 1 giao dịch fraud vẫn đạt accuracy 99% → **không phản ánh đúng chất lượng mô hình**.
# References
