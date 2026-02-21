- Ý tưởng: thêm object detection để có thể tạo từng cặp sentiment cho object-review_text 
![[Pasted image 20251116222429.png]]
-  trong trường hợp có câu review không liên quan gì đến ảnh: 
	- cho vào bộ dataset **A** gồm: **ảnh -> review -> sentiment score** (bỏ đi phần text_review không liên quan)
	- cho vào bộ dataset **B** gồm: chỉ có **review -> sentiment score** thôi (bỏ đi ảnh) 

![[Pasted image 20251116225647.png]]
![[Pasted image 20251116230708.png]]
- Tóm lại: cần detect object trong ảnh, tạo mô tả cho từng object, giả sử rằng bộ dataset hiện tại đã có các labels (aspect term, aspect category, opinion term, sentiment polarity) => matching các detected object và các labels này + câu review_text tương ứng => sentiment score tương ứng cho từng object => dataset (thứ 1)  
- Với trường hợp không có detected object liên quan đền câu review nào => cho ảnh của object đó vào 1 dataset riêng (thứ 2)  
- Với trường hợp không có câu review_text nào liên quan đến object detected được => cho vào 1 dataset riêng (thứ 3)