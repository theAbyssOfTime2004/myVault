2025-07-02 15:15


Tags:

# Word embedding and Word Representation

### 1. One hot Representation là gì và những hạn chế của nó là gì?
-  One - hot representation là một phương pháp rất trực quan để encode 1 từ trong 1 từ vựng cố định. Mỗi từ được biểu diễn dưới dạng 1 vector có chiều bằng kích thước của từ vựng $|V|$. Trong vector này, chỉ có 1 chiều là 1 (tại vị trí tương ứng với từ đó), còn tất cả các chiều khác là 0. Ví dụ nếu từ vựng là (ăn, ngủ , học), thì từ *ngủ* có thể được biểu diễn là: `[0, 1, 0]`.
-  Những điểm yếu chính của one - hot representation bao gồm: 
	-  **Không thể hiện mối quan hệ ngữ nghĩa:** Vector one-hot không năm bắt được abất kỳ mối quan hệ ngữ nghĩa nào giữa các từ. Mọi từ đều cách đều nhau trong không gian vector, có nghĩa là *chó* và *mèo* không được coi là gần nhau hơn *chó* và *bàn*.
	- **Vấn đề kích thước:** kích thước của vector tăng tuyến tính với kích thước của từ vựng. Với từ vựng lớn, vector one-hot trở nên rất thưa thớt *sparse* (chứa rất nhiều số 0) và có chiều cao, dẫn đến việc xử lý không hiệu quả và tốn bộ nhớ 
### 2. Các mô hình ngôn ngữ dựa trên N-gram hoạt động như thế nào để gán xác suất cho các câu và chúng được ước tính như thế nào?
-  Các mô hình ngôn ngữ dựa trên N-gram được sử dụng để gán xác suất cho một câu. Một N-gram là 1 câu gồm N từ. Ví dụ, một **unigram** là 1 từ đơn *"I"* , một **bigram** là một chuỗi 2 từ *"I do"*, và một **trigram** là một chuỗi 3 từ *"I do my"*. Mục tiêu là tính toán xác suất của toàn bộ chuỗi từ $P(w_1, w_2, \dots, w_k)$
-  Việc ước tính xác suất của các N-grams thường được thực hiện bằng phương pháp *maximum likelihood estimation - MLE* dựa trên số lần xuất hiện của các chuỗi từ trong corpus. Các công thức phổ biến là: 
	- Xác suất của một từ đơn: $$ P(w_i) = \frac{C(w_i)}{\sum_j C(w_j)} $$
		- trong đó $C(w_i)$ là số lần xuất hiện của từ $w_i$
	- Xác suất của một từ dựa trên từ trước đó: $$ P(w_i|w_{i-1}) = \frac{C(w_{i-1}, w_i)}{\sum_k C(w_{i-1}, w_k)} $$
		- trong đó, $C(w_{i-1}, w_i)$ là số lần xuất hiện của cặp từ $w_{i-1}, w_i$
	- Xác suất của một từ dựa trên hai từ trước đó $$ P(w_i|w_{i-1}, w_{i-2}) = \frac{C(w_{i-2}, w_{i-1}, w_i)}{\sum_k C(w_{i-2}, w_{i-1}, w_k)}. $$
	- Ta có công thức tỗng quát: $$
P(w_n \mid w_{n-N+1}, ..., w_{n-1}) = \frac{C(w_{n-N+1}, ..., w_n)}{C(w_{n-N+1}, ..., w_{n-1})}
$$
		- trong đó 
			- $( P(w_n \mid w_{n-N+1}, ..., w_{n-1}))$: xác suất từ $( w_n )$ xuất hiện sau chuỗi $( N-1 )$từ liền trước
			- $( C(w_{n-N+1}, ..., w_n) )$: số lần chuỗi $( N )$ từ xuất hiện trong corpus
			- $( C(w_{n-N+1}, ..., w_{n-1}) )$: số lần chuỗi $( N-1 )$ từ xuất hiện (làm điều kiện)
		- công thức tổng quát này có nghĩa là MLE tìm xác suất xuất hiện cho từ thứ $N$ biết $N-1$ từ gần nhất.
- Các mô hình này hữu ích trongn nhiều tác vụ NLP như dịch máy (ví dụ: $$P(\text{high winds tonight}) > P(\text{large winds tonight})$$
- Sửa lỗi chính tả và nhận dạng giọng nói.
# References
