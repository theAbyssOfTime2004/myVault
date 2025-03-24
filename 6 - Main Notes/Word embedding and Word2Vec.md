2025-03-24 12:48


Tags: [[data scientist]], [[Neural Network]], [[DeepLearning]], [[NLP]]

# Word embedding and Word2Vec

### Word embedding
![[Pasted image 20250324124934.png]]
![[Pasted image 20250324125001.png]]
![[Pasted image 20250324125028.png]]
![[Pasted image 20250324125040.png]]
![[Pasted image 20250324125056.png]]
- Thay vì sử dụng cách truyền thống là assign random numbers to words, ta có thể train một mô hình neural network để assign numbers to words cho ta, lợi ích của việc sử dụng neural networks để làm việc này là vì neural network có thể dựa vào ngữ nghĩa của câu để thực hiện việc assigning và những số được assigned được gọi là weights và các weights này có thể được tối ưu = backpropagation, optimizing weights sẽ giúp ta được các từ giống nhau sẽ được embedded gần nhau (khi ta project các weight này lên 1 hệ tọa độ) do đó giúp cho việc dự đoán từ tiếp theo sẽ trở nên hiệu quả hơn 
### Word2Vec
#### Continuous Bag of Words  
![[Pasted image 20250324125948.png]]
- Ví dụ trong câu *Troll 2 is greate* continuous bag of words sẽ sử dụng từ *Troll 2* và từ *great!* để dự đoán từ is
#### Skip-gram
![[Pasted image 20250324130115.png]]
- Skip gram sẽ sử dụng từ ở giữa để dự đoán các từ xung quanh, ví dụ trong 2 câu trên thì Skip gram sẽ sử dụng từ *is* để dự đoán các từ *Troll 2, great!* và *Gymkata*
- 

# References
