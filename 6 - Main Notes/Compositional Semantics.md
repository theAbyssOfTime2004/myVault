2025-07-05 11:38


Tags:

# Compositional Semantics
### 1. Compositionality in natural language 
- Tính cấu tạo là 1 nguyên tắc cơ bản trong NLP, nói rằng ý nghĩa của 1 chỉnh thể được xác định bởi ý nghĩa của các bộ phận cấu thành nó. Nó cho phép tạo ra các ý nghĩa phức tạp bằng cách kết hợp các yếu tố ngữ nghĩa đơn giản hơn. Tuy nhiên, việc hiểu ý nghĩa phức tạp vượt ra ngoài sự kết hợp đơn giản của các thành phần. Sự phức tạp phát sinh từ một số yếu tố:
	- **Thông tin cú pháp (R):** Các cụm từ có cùng từ vựng có thể có ý nghĩa khác nhau do cấu trúc cú pháp của chúng. Ví dụ, "machine learning" (học máy) và "learning machine" (máy học) mang ý nghĩa khác nhau mặc dù có cùng từ.
	- **Kiến thức nền (K):** Để hiểu đầy đủ các ý nghĩa phức tạp, cần có kiến thức bên ngoài hoặc kiến thức nền. Câu "Tom and Jerry is one of the most popular comedies in that style" đòi hỏi kiến thức về "Tom and Jerry" như một bộ phim hoạt hình hài và hiểu thuật ngữ "style."
- Do đó, một hàm cấu tạo hoàn chỉnh phải tính đến các thành phần ngữ nghĩa $(u, v)$, các quy tắc quan hệ cú pháp (R) và kiến thức nền (K), được thể hiện bằng công thức $p = f(u, v, R, K).$
- **Compositionality** means the meaning of a phrase or sentence can be built by combining the meanings of its parts.  
	_(Tính tổ hợp: nghĩa của cả câu/từ ghép = tổ hợp ngữ nghĩa các phần nhỏ)_
### 2. Models of Composition 
- Models of composition tìm cách biểu diễn ý nghĩa chung của 2 đơn vị ngữ nghĩa (u và v) dưới dạng một biểu diễn duy nhất (p). Các phương pháp khác nhau đã được đề xuất để đạt được điều này, mỗi phương pháp có những giả định và cách tiếp cận riêng:
	- **Additive Model:** Ý nghĩa chung có thể được biểu diễn bằng tổng trực tiếp của các vector: $p = u + v$. Ví dụ: $w(\text machine)+ w(\text learning) = [1, 7, 3, 7, 2]$.
	- **Weighted Additive**: Để khắc phục vấn đề thứ tự từ, có thể áp dụng tổng có trọng số: $p = \alpha u + \beta v$, trong đó $\alpha$ và $\beta$ là các trọng số khác nhau cho từng vector. Ví dụ, $0.3 × w(\text machine) + 0.7 × w(\text learning) = [0.7, 3.6, 1.7, 2.9, 0.6]$. Mô hình này có thể được mở rộng để kết hợp thông tin về các hàng xóm ngữ nghĩa gần nhất để tính đến kiến thức trước.
	- **Multiplicative Model:** Mô hình này nhằm mục đích tạo ra tương tác bậc cao hơn giữa các thành phần.
		- **Tích từng cặp:** Một cách tiếp cận là áp dụng tích từng cặp dưới dạng hàm cấu tạo xấp xỉ: $p_i = u_i * v_i$, có nghĩa là mỗi chiều của đầu ra chỉ phụ thuộc vào chiều tương ứng của hai vectơ đầu vào.
		- **Ma trận trọng số:** Để giảm nhẹ vấn đề thứ tự từ, các trọng số α và β trong mô hình cộng có thể được thay thế bằng hai ma trận $(W_u và W_v)$ để xác định tầm quan trọng của u và v đối với p.
		- **Tensor:** Một cách tiếp cận tổng quát hơn là sử dụng các tensor làm mô tả nhân, trong đó hàm cấu tạo có thể được xem xét dưới dạng $p = T(u, v)$, trong đó T là một tensor bậc 3. Để tính đến thứ tự từ và làm cho hàm không đối xứng, có thể sử dụng tensor bậc 4.
# References
