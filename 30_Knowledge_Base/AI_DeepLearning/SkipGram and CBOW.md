2025-03-27 23:36


Tags: [[data scientist]], [[DeepLearning]], [[Mathematics]], [[NLP]]

# SkipGram and CBOW

## SkipGram
### Xây dựng hàm loss cho skipgram
1. **Mô hình tối ưu xác suất của từ ngữ cảnh quanh từ đích**
$$
\prod_{c \in C_t} P(w_c | w_t)
$$
- Với:
	- $w_t$ là từ đích và $C_t$ là tập hợp các từ xung quanh nó
	- Ta muốn tối đa hóa xác suất xuất hiện các từ ngữ  cảnh $w_c$ khi biết từ đích $w_t$ , <=> ta muốn tối đa hóa tích trên 
	- Tích càng lớn thì tổng thể mô hình càng có khả năng dự đoán đúng các từ ngữ cảnh.
2. **Chuyển đổi về bài toán tối ưu hàm mất mát**
	- Ta sẽ gặp 1 vấn đề: Nếu có nhiều từ ngữ cảnh, tích của nhiều xác suất $P(w_c|w_t)$ sẽ càng nhỏ và sẽ nhỏ đến mức gây ra lỗi *floating point precision*
	- Do đó thay vì tối đa hóa tích các xác suất, ta sẽ chuyển sang *tối ưu tổng log của các xác suất* (hay còn gọi là *negative log loss*):
	- $$
	 - \sum_{c \in C_t} \log P(w_c | w_t)
	 $$
	- Ở đây ta dùng log là bởi vì:
		- Logarithm giúp chuyển tích thành tổng, giúp tính toán ổn định hơn.
		- Logarithm cũng giúp tránh giá trị quá nhỏ hoặc quá lớn khi nhân nhiều xác suất với nhau.
		- Ta muốn **giá trị này càng nhỏ càng tốt** (tối thiểu hóa hàm mất mát).
3. **Công thức Softmax để tính xác suất**
- Ta có định nghĩa cho công thức xác suất có điều kiện trên là: 
- $$
 P(w_c | w_t) = \frac{\exp(\mathbf{u}_t^T \mathbf{v}_c)}{\sum_{i=1}^{N} \exp(\mathbf{u}_t^T \mathbf{v}_i)}
$$
Trong đó:
- $( \mathbf{u}_t)$ là vector từ đích $( w_t )$.
- $( \mathbf{v}_c)$ là vector từ ngữ cảnh $( w_c )$.
- $( \mathbf{u}_t^T \mathbf{v}_c )$ là tích vô hướng thể hiện mức độ liên quan giữa $( w_t )$ và $( w_c )$.
- $( \sum_{i=1}^{N} \exp(\mathbf{u}_t^T \mathbf{v}_i) )$ là tổng của tất cả các giá trị tương tự trong từ điển \( \mathcal{V} \), giúp chuẩn hóa thành xác suất.
- Để dễ hiểu thì  trên tử sẽ là mối liên hệ giữa 1 từ đích và 1 từ ngữ cảnh bất kỳ còn dưới mẫu là tổng tất cả mối liên hệ giữa từ đích và toàn bộ các từ ngữ cảnh
- Bên cạnh đó ta thấy rằng biểu thức này rất giống hàm *Softmax*, và việc định nghĩa biểu thức trên giống định nghĩa hàm *Softmax* giúp đảm bảo rằng tổng xác suất sẽ luôn bằng 1: 
- $$
\sum_{w \in \mathcal{V}} P(w | w_t) = 1
 $$
 1. Hàm mất mát tổng quát
- Khi mở rộng công thức trên cho tất cả từ đích và ngữ cảnh, ta có hàm mất mát tổng quát cho toàn bộ mô hình:
$$
\mathcal{L}(U, V; w_t) = - \sum_{c \in C_t} \log \frac{\exp(\mathbf{u}_t^T \mathbf{v}_c)}{\sum_{i=1}^{N} \exp(\mathbf{u}_t^T \mathbf{v}_i)}
$$
- Hàm mất mát này giúp tối ưu hóa mô hình sao cho:
- Xác suất của từ ngữ cảnh đúng $(w_c)$ càng cao càng tốt.
- Các vector từ học được phản ánh đúng quan hệ ngữ nghĩa giữa từ đích và từ ngữ cảnh.
### Biểu diễn dưới dạng Neural Network
![[Pasted image 20250328002314.png]]
-  Quy trình trong Skip-gram Word2Vec diễn ra như sau:
1. **Chọn từ đích** → Ban đầu, ta có từ đích là **"fox"**.
2. **Nhân với ma trận trọng số $U$** →
    - Biểu diễn "fox" dưới dạng **one-hot vector**.
    - Nhân vector này với **ma trận nhúng** $U$ để thu được **embedding** $\mathbf{u}_t$​.
3. **Nhân với ma trận trọng số $V$** →
    - $\mathbf{u}_t$​ được nhân với **ma trận trọng số đầu ra** $V$ để thu được $\mathbf{u}_t^TV$.
    - Kết quả này là một vector logit, trong đó mỗi phần tử đại diện cho mức độ liên quan giữa "fox" và một từ khác trong từ điển.
4. **Áp dụng Softmax** →
    - Chuyển $\mathbf{u}_t^TV$. thành xác suất bằng cách áp dụng **Softmax**.
    - Giá trị đầu ra thể hiện **mối liên hệ giữa "fox" và các từ ngữ cảnh**.
- **Mục tiêu cuối cùng**: Mô hình **học được embedding của từ "fox" sao cho nó có thể dự đoán đúng các từ ngữ cảnh xung quanh**.
- (Để cho dễ hiểu: ban đầu ta có từ đích là "fox" sau đấy từ fox đi qua lớp ẩn và thực hiện phép nhân với ma trận trọng số $U$ và được embedding $u_t$ sau đấy $u_t$ đến output layer và thực hiện phép nhân với ma trận trọng số $V$ và ta được  $\mathbf{u}_t^TV$ và cuối cùng kích hoạt softmax để thể hiện mối liên hệ giữa các từ trong ngữ cảnh đối với "fox")
# References
