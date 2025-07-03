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
### Latent Semantic Analysis (LSA) và SVD 
- LSA  là 1 tập các chiến lược bắt nguồn từ các mô hình trong không gian vector, nhằm mục đích nắm bắt ngữ nghĩa của từ tốt hơn. LSA khám phá các yếu tố tiềm ẩn cho từ và tài liệu bằng cách phân tích ma trận để cải thiện việc ước tính độ tương đồng của từ  
- LSA hoạt động theo các bước sau: 
	1. **Vector space model:** Mỗi tài liệu và thuật ngữ được biểu diễn dưới dạng một vector trong một không gian nhiều chiều 
	2. **Term-Document Matrix:** tạo một ma trận $X$ trong đó mỗi hàng tương ứng với một term, mỗi cột tương ứng với một document, và các phần tử của ma trận biểu thị tần suất xuất hiện của 1 term trong 1 tài liệu
	3. **Singular Value Decomposition (SVD):** Áp dụng SVD để phân tách ma trận term-document $X$ thành 3 ma trận: $U : \text{không gian term}$,$\Sigma : \text{ma trận đường chéo của các gía trị số ít}$, $V^T : \text{không gian document}$, sao cho $X = U*\Sigma*V^T$
- Bằng cách sử dụng SVD và giữ lại các giá trị số lớn nhất (giảm kích thước), LSA có thể giảm chiều dữ liệu, biểu diễn các từ và tài liệu trong một không gian thấp chiều hơn, đồng thời khám phá các mối quan hệ ngữ nghĩa tiềm ẩn giữa chúng 
### Những hạn chế của LSA là gì và tại sao PMI/PPMI  được sử dụng? 
- Mặc dù LSA có khả năng nắm bắt ngữ nghĩa, nó cũng có 1 số hạn chế:
	- **Chi phí tính toán cao**: Việc tính toán SVD rất computationally expensive, với thời gian chạy thường là $O(\max(w, d) \cdot \min(w,d)^2)$, trong đó $w$ là số lượng từ và $d$ là số lượng document
	- **Non-incremental:** Phương pháp này không incremental, có nghĩa là khi có dữ liệu mới, toàn bộ quá trình phân tách (SVD) phải được tính toán lại từ đầu, làm giảm hiệu quả của các dynamic system
- Để giải quyết vấn đề tần suất thô (*raw counts*) gán quá nhiều weights cho các từ chức năng (*function words*) như "the", "she", "has" và quá ít weights cho các từ có nội dung (*content words*) như "cheese", "bread", "sheep", *Pointwise Mutual Information (PMI)* được sử dụng. PMI đo lường mức độ liên kết (associative strength) giữa một từ mục tiêu $w$ và một ngữ cảnh $c$.
- *Positive Pointwise Mutual Information (PPMI)* là 1 biến thể phổ biến của PMI. Bởi vì các hàng của ma trận đồng xuất hiện thường thưa thớt <=> nhiều giá trị PMI sẽ là $\log 0 = -\infty$. PPMI giúp giải quyết vấn đề này bằng cách thay thế tất  cả các giá trị PMI âm bằng 0, chỉ giữ lại các mối liên hệ tích cực mạnh mẽ, giúp tạo ra các biểu diễn từ có ý nghĩa hơn 
### Word2Vec là gì và sự khác biệt giữa CBOW và Skip-gram?
- Word2vec là 1 nhóm các kỹ thuật biểu diễn từ phân tán, tạo ra các "word embedding" có thể nắm bắt ngữ nghĩa của từ dựa trên ngữ cảnh của chúng. Ý tưởng cơ bản là "ý nghĩa của một từ có thể được học từ ngữ cảnh của nó".
	- **Continuous Bag-of-Words (CBOW):** mô hình CBOW dự đoán từ trung tâm (target word) dựa trên một cửa sổ các từ ngữ cảnh xung quanh nó. Về mặt hình thức, CBOW dự đoán $w_t$ dựa trên các từ ngữ cảnh $$w_{t-l}, \ldots, w_{t-1}, w_{t+1}, \ldots, w_{t+l}$$
	- Mục tiêu tối ưu hóa các embedding sao cho chúng có thể dự đoán từ mục tiêu một cách hiệu quả nhất. CBOW được tối ưu hóa các embedding sao cho chúng có thể dự đoán từ mục tiêu một cách hiệu quả nhất. CBOW được tối ưu hóa bằng cách giảm thiểu tổng log xác suất âm.
	- **Skip-gram:** Ngược lại với CBOW, Skip-gram dự đoán các từ ngữ cảnh (context words) dựa trên target word duy nhất. Cụ thể, với 1 từ $w_t$, Skip-gram dự đoán ngữ cảnh. Hàm mất mát được định nghĩa tương tự như CBOW, nhằm mục đích tối đa hóa xác suất của các cặp từ-ngữ cảnh đã quan sát. 
- Điểm khác biệt chính là hướng dự đoán: CBOW đi từ ngữ cảnh đến target word, trong khi Skip-gram đi từ target word đến ngữ cảnh. Skip-gram thường hoạt động tốt hơn với các ngữ liệu nhỏ và các từ ít xuất hiện. 
### Skip-gram with negative sampling là gì và tại sao nó được sử dụng?
- **Skip-gram with negative sampling - SGNS** là một cải tiến của mô hình Skip-gram cơ bản. Mục tiêu của SGNS là làm cho việc huấn luyện hiệu quả hơn bằng cách giảm số lượng các cặp ngữ cảnh phải cập nhật trong mỗi bước 
- Thay vì dự đoán tất cả các từ trong từ vựng làm ngữ cảnh tiềm năng (điều này rất tốn kém khi từ vựng lớn), SGNS tập trung vào:
	- Tối đa hóa xác suất của các cặp word-context đã quan sát: Tức là, tăng xác suất của các từ ngữ cảnh thực sự xuất hiện xung quanh từ trung tâm.
	- Tối thiểu hóa xác suất của các mẫu được chọn ngẫu nhiên: Đồng thời, giảm xác suất của một số lượng nhỏ các từ được chọn ngẫu nhiên từ từ vựng (gọi là negative samples) không phải là ngữ cảnh thực sự của target word.
- Bằng cách chỉ cập nhật các embedding cho các từ ngữ cảnh dương và một số lượng nhỏ các từ ngữ cảnh âm, SGNS làm giảm đáng kể chi phí tính toán cho mỗi training step, cho phép train trên các dataset lớn hơn 1 cách hiệu quả hơn
### Tái sử dụng pre-trained word embedding có ý nghĩa gì trong NLP?
- Tái sử dụng các embedding từ đã được huấn luyện trước (pre-trained  word embeddings) là một kỹ thuật phổ biến và mạnh mẽ trong NLP. Nó liên quan đến việc huấn luyện các embedding từ trên một tập dữ liệu lớn (thường là 1 corpus rất lớn) cho một tác vụ A (ví dụ: mô hình ngôn ngữ), sau đó sửu dụng các embedding này để khởi tạo các lớp embedding của mạng thần kinh cho một tác vụ A, sau đó sử dụng các embedding này để khởi tạo các lớp embedding của mạng thần kinh cho một tác vụ B khác (ví dụ: phân loại văn bản, nhận dạng thực thể). 
- Có hai cách chính để sử dụng các embedding này:
	- **Tùy chỉnh (fine-tuning):** các embedding được huấn luận trước được sử dụng làm điểm khởi đầu, và sau đó chúng được tiếp tục điều chỉnh (huấn luyện) cùng với còn lại của mạng lưới trên dữ liệu của tác vụ B. Điều này cho phép các embedding thích ứng với đặc điểm cụ thể của tác vụ mới.
		- **Đóng băng trọng số (Freezing Weights)**
# References
