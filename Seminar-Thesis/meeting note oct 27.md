- Tăng cường data 
- model architect sẽ có 2 kiến trúc 
	- 1 là review + với ảnh matching với review đó 
	- 2 là chỉ có ảnh (trong các trường hợp có 1 review + nhiều ảnh) => làm sao để gen ra được caption (trong trường hợp có ảnh mà không match với bất kỳ câu review nào) 
- trong bài toán ABSA có các khái niệm:
	- **Aspect term**: là từ hoặc đối tượng trong câu dc nhắc đến
		- => phân loại 6 nhóm aspect category
	- **Aspect category**: là 6 nhóm trên 
	- **Opinion term**: là (tính) từ thể hiện cảm xúc trong câu
		- => polarity sentiment: phân loại cảm xúc (sentiment) 

	- ví dụ: *nhân viên rất thân thiện*

- Important: xử lý dataset 
- thử nghiệm sinh 4 label (ở trên) cho sample data