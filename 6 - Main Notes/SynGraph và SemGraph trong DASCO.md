[[seminar HCMUS]]

###  SemGraph (Semantic Graph)

- Mỗi **từ** trong câu là một **nút**.
- Trọng số cạnh được tính bằng **self-attention score** thể hiện mức tương quan ngữ nghĩa giữa các từ.
- Một **mạng GNN (SemGNN)** được huấn luyện để tổng hợp thông tin, thu được biểu diễn ngữ nghĩa giàu thông tin.
### SynGraph (Syntactic Graph)

- Dựa trên **dependency tree** sinh từ **spaCy**, trong đó các quan hệ cú pháp (chủ ngữ, bổ ngữ, động từ, …) tạo thành các cạnh vô hướng.
- **SynGNN** mã hóa cấu trúc cú pháp, giúp mô hình hiểu rõ khung cấu trúc của câu    
Hai đồ thị này cung cấp **hai góc nhìn bổ sung**: cú pháp (cấu trúc) và ngữ nghĩa (nội dung).

### Cách implement Contrastive learning trong Dasco
- **Cross-scope Contrast** 
	- Mục tiêu: **Phân biệt từ trong phạm vi (in-scope)** và **ngoài phạm vi (out-of-scope)** của từ mục tiêu.
	- Áp dụng cả trong SynGraph và SemGraph
	- Mỗi từ mục tiêu là *anchor (phần neo)* 
		- Các từ liên quan trong phạm vi → **positive pairs**.
		- Các từ không liên quan → **negative samples**.
	- Dùng **InfoNCE loss** để:
		- Kéo gần biểu diễn của các cặp dương tính.
		- Đẩy xa biểu diễn của các cặp âm tính.
-  **Cross-graph Contrast**
	- Mục tiêu: **Căn chỉnh hiểu biết ngữ cảnh giữa SynGraph và SemGraph.**    
- Ví dụ:
    - Lấy từ mục tiêu ntn_tnt​ trong SynGraph làm **anchor**.
    - Tìm từ tương ứng mtm_tmt​ và các nút thuộc phạm vi của nó trong SemGraph → **positive set**.
    - Các nút SemGraph khác → **negative samples**.
- Sử dụng **trọng số tương đồng ω** để điều chỉnh độ gần giữa hai không gian biểu diễn.
- Quá trình lặp lại theo hướng ngược lại (SemGraph → SynGraph).