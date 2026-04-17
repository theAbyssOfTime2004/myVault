2026-04-11 18:01


Tags:

# Double descent

- Là hiện tượng khi tăng độ phức tạp model (hoặc tăng training time), test loss không đi theo hình chữ U (từ underift -> overfit), mà lại giảm thêm 1 lần sau khi overfitting
- Xuất hiện khi train 1 model rất lớn với số lượng epoch rất lớn 
![[Pasted image 20260411180330.png]]
- Điều này xảy ra, có thể lý giải 1 cách phỏng đoán như sau: khi model quá lớn, nó có rất nhiều cách để fit training data, và vấn đề giờ đây sẽ không còn là "có học hết được training data không", mà nó là "fit training data như thế nào là hợp lý", và gradient descent có xu hướng tìm ra lời giải mượt nhất, ít dao động nhất, từ đó giúp model generalize tốt hơn (implicit regularization)

# References
