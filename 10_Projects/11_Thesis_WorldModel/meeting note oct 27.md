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
- triplet: tạo ra relationship giữa các objects


- edit code này để thêm prompt vào khi generating caption, prompt sao cho caption được tạo ra tập trung vào ngữ cảnh, thể hiện được ý đồ review của nguời chụp ảnh, highlight yếu tố quan trọng trong ảnh,... nói chung là cần thiết cho bài toán absa, bên cạnh đó generate ra thêm 4 label bao gồm:

- Aspect term: Là từ hoặc cụm từ xuất hiện trong văn bản, biểu thị khía cạnh cụ thể của một sản phẩm, dịch vụ hoặc đối tượng mà người nói/bình luận đang nói đến.

- Aspect category: Là loại hoặc nhóm khía cạnh lớn hơn mà aspect term thuộc về, ở đây tôi muốn nó là 6 nhóm sau (Amenity, Branding, Experience, Facility, Loyalty, Service)

- Opinion term: Là từ hoặc cụm từ trong văn bản mà người nói dùng để diễn đạt cảm xúc, đánh giá, quan điểm về khía cạnh đó.

- Polarity sentiment: Là việc xác định xem người nói có cảm xúc positive, negative hay neutral đối với khía cạnh đó.