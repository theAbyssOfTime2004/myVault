- Ý tưởng: thêm object detection để có thể tạo từng cặp sentiment cho object-review_text 
![[Pasted image 20251116222429.png]]
-  trong trường hợp có câu review không liên quan gì đến ảnh: 
	- cho vào bộ dataset **A** gồm: **ảnh -> review -> sentiment score** (bỏ đi phần text_review không liên quan)
	- cho vào bộ dataset **B** gồm: chỉ có **review -> sentiment score** thôi (bỏ đi ảnh) 