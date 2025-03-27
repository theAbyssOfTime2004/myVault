2025-03-27 23:36


Tags: [[data scientist]], [[DeepLearning]], [[Mathematics]], [[NLP]]

# SkipGram and CBOW

## SkipGram
### Xây dựng hàm loss cho skipgram
- 1. **Mô hình tối ưu xác suất của từ ngữ cảnh quanh từ đích**
$$
\prod_{c \in C_t} P(w_c | w_t)
$$
- Với:
	- $w_t$ là từ đích và $C_t$ là tập hợp các từ xung quanh nó
	- Ta muốn tối đa hóa xác suất xuất hiện các từ ngữ  cảnh $w_c$ khi biết từ đích $w_t$ , <=> ta muốn tối đa hóa tích trên
	- Tích càng lớn thì tổng thể mô hình càng có khả năng dự đoán đúng các từ ngữ cảnh.
- 2. **Chuyển đổi về bài toán tối ưu hàm mất mát**
	- Ta sẽ gặp 1 vấn đề: Nếu có nhiều từ ngữ cảnh, tích của nhiều xác suất $P(w_c|w_t)$ sẽ càng nhỏ và sẽ nhỏ đến mức gây ra lỗi *floating point precision*
	- Do đó thay vì tối đa hóa tích các xác suất, ta sẽ chuyển sang *tối ưu tổng log của các xác suất* (hay còn gọi là *negative log loss*):
	- $$
	 - \sum_{c \in C_t} \log P(w_c | w_t)
	 $$
	- Ở đây ta dùng log là bởi vì:
		- Logarithm giúp chuyển tích thành tổng, giúp tính toán ổn định hơn.
		- Logarithm cũng giúp tránh giá trị quá nhỏ hoặc quá lớn khi nhân nhiều xác suất với nhau.
		- Ta muốn **giá trị này càng nhỏ càng tốt** (tối thiểu hóa hàm mất mát).
# References
