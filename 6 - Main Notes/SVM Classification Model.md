2024-10-25 03:21


Tags: [[Machine Learning]], [[data scientist]], [[supervised learning]], [[classification]]




# SVM Model And its variations

## Ý tưởng
- Quay lại bài toán về phân chia 2 class sử dụng PLA, giả sử rằng có hai class khác nhau được mô tả bởi các điểm trong không gian nhiều chiều, hai classes này _linearly separable_, tức tồn tại một siêu phẳng phân chia chính xác hai classes đó. Hãy tìm một siêu mặt phẳng phân chia hai classes đó, tức tất cả các điểm thuộc một class nằm về cùng một phía của siêu mặt phẳng đó và ngược phía với toàn bộ các điểm thuộc class còn lại. Chúng ta đã biết rằng, thuật toán PLA có thể làm được việc này nhưng nó có thể cho chúng ta vô số nghiệm như Hình 1 dưới đây:
	![[Pasted image 20241027225530.png]]
- Vậy thì làm sao để ta có thể biết được chọn đường nào trong hình trên làm nghiệm cuối cùng cho bài toán, SVM ở đây là để giải quyết vấn đề này với ý tưởng chính là tìm đường phân chia sao cho margin lớn nhất với margin được minh họa trong hình dưới đây:
![[Pasted image 20241027225801.png]]

- Đây cũng là lý do vì sao SVM còn được gọi là _Maximum Margin Classifier_. Nguồn gốc của tên gọi Support Vector Machine sẽ sớm được làm sáng tỏ.
- Bài toán tối ưu trong SVM là một bài toán lồi với hàm mục tiêu là _stricly convex_, nghiệm của bài toán này là duy nhất. Hơn nữa, bài toán tối ưu đó là một Quadratic Programming (QP).
- Mặc dù có thể trực tiếp giải SVM qua bài toán tối ưu gốc này, thông thường người ta thường giải bài toán đối ngẫu. Bài toán đối ngẫu cũng là một QP nhưng nghiệm là _sparse_ nên có những phương pháp giải hiệu quả hơn.
- Với các bài toán mà dữ liệu _gần linearly separable_ hoặc _nonlinear separable_, có những cải tiến khác của SVM để thích nghi với dữ liệu đó
## Soft Margin SVM
-  SVM thuần (Hard Margin SVM) hoạt động không hiệu quả khi có nhiễu ở gần biên hoặc thậm chí khi dữ liệu giữa hai lớp gần _linearly separable_. Soft Margin SVM có thể giúp khắc phục điểm này.
    
- Trong Soft Margin SVM, chúng ta chấp nhận lỗi xảy ra ở một vài điểm dữ liệu. Lỗi này được xác định bằng khoảng cách từ điểm đó tới đường biên tương ứng. Bài toán tối ưu sẽ tối thiểu lỗi này bằng cách sử dụng thêm các biến được gọi là _slack varaibles_.
    
- Để giải bài toán tối ưu, có hai cách khác nhau. Mỗi cách có những ưu, nhược điểm riêng, các bạn sẽ thấy trong các bài tới.
    
- Cách thứ nhất là giải bài toán đối ngẫu. Bài toán đối ngẫu của Soft Margin SVM rất giống với bài toán đối ngẫu của Hard Margin SVM, chỉ khác ở ràng buộc chặn trên của các nhân tử Laggrange. Ràng buộc này còn được gọi là _box costraint_.
    
- Cách thứ hai là đưa bài toán về dạng không ràng buộc dựa trên một hàm mới gọi là _hinge loss_. Với cách này, hàm mất mát thu được là một hàm lồi và có thể giải được khá dễ dàng và hiệu quả bằng các phương pháp Gradient Descent.
    
- Trong Soft Margin SVM, có một hằng số phải được chọn, đó là CC. Hướng tiếp cận này còn được gọi là C-SVM. Ngoài ra, còn có một hướng tiếp cận khác cũng hay được sử dụng, gọi là νν-SVM, bạn đọc có thể đọc thêm
# References
[sklearn.svm.svc](http://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html)
[machine learning cơ bản - bài 19]([Machine Learning cơ bản](https://machinelearningcoban.com/2017/04/09/smv/))
[machine learning cơ bản - bài 20](https://machinelearningcoban.com/2017/04/13/softmarginsmv/#-tom-tat-va-thao-luan)
