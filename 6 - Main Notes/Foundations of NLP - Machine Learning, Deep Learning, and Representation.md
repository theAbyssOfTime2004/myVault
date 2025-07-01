2025-07-01 18:18


Tags:

# Foundations of NLP - Machine Learning, Deep Learning, and Representation
## Machine Learning là gì và nó bao gồm những thành phần nào:
- ML giải quyết vấn đề từ động học các chương trình máy tính từ dữ liệu. Một *ML system* điển hình bao gồm 3 thành phần chính: *Representation, Objecctive và Optimization*. 
	- Representation: liên quan đến cách dữ liệu được encode để thuật toán có thể xử lý
	- Objective: định nghĩa thước đo hiệu suất hoặc hàm loss mà hệ thống cố gắng minimize (or maximize)
	- Optimize: là quá trình điều chỉnh parameters của model để đạt được mục tiêu mong muốn
## Điều gì làm cho Deep Learning khác biệt so với Machine Learning nói chung
- DL là 1 phương pháp điển hình *Representation Learning*, đã đạt được thành công lớn gần đây trong các lĩnh vực như **speech recognition, computer vision và natural language processing**. Học sâu có 2 đặc điểm nổi bật chính: **Distributed Representation** và **Deep Architecture**
## Distributed Representation trong Deep Learning có nghĩa là gì? 
- Là cách mà các thuật toán Deep learning thường biểu diễn mỗi đối tượng bằng một vector mật độ giá trị thực, chiều thấp. Điều này khác biệt so với các sơ đồ biểu diễn thông thường như mô hình *(bag-of-word)* sử dụng *"one-hot representation"*, nơi mỗi từ hoặc đối tượng được biểu diễn bằng một vector thưa với **một vị trí là 1 và các vị trí khác là 0**. Distributed Representation cho phép nắm bắt các mối quan hệ ngữ nghĩa và tương tự giữa các đối tượng 1 cách hiệu quả hơn.
- Ví dụ vocabulary gồm 4 từ: 
```python
["cat", "dog", "elephant", "tiger"]
```
- Khi đó, sử dụng one-hot representation ta sẽ được:
	- **"cat"** → `[1, 0, 0, 0]`
	- **"dog"** → `[0, 1, 0, 0]`
	- **"elephant"** → `[0, 0, 1, 0]`
	- **"tiger"** → `[0, 0, 0, 1]`
- Còn với distributed reprenstation thì: 
- Giả sử ta có vector embedding với 3 chiều (thực tế là 100-300-768 chiều):
	- **"cat"** → `[0.9, 0.1, 0.4]`    
	- **"dog"** → `[0.85, 0.15, 0.35]`    
	- **"elephant"** → `[0.2, 0.9, 0.7]`
	- **"tiger"** → `[0.8, 0.2, 0.5]`
## Deep Architecture có vai trò gì trong Deep Learning
- Deep Architecture là đặc điểm quan trọng thứ 2 của Deep Learning, liên quan đến việc các thuật toán DL thường học 1 kiến trúc hierarchical và deep để biểu diễn các đối tượng, được gọi là **multilayer neural network**. DA này có khả năng extract các đặc trưng trừu tượng của đối tượng từ raw data. Khả năng này được coi là lý do quan trọng cho sự thành công lớn của DL trong Speech Recognition và Computer Vision, vì nó cho phép model học các representation ngày càng phức tạp và ý nghĩa hơn của data. 
## Vai trò của Representation Learning trong NLP là gì?
- NLP nhằm mục đích xây dựng các chương trình chuyên biệt về ngôn ngữ để máy móc có thể hiểu ngôn ngữ. Văn bản ngôn ngữ tự nhiên là *unstructured data* điển hình, với nhiều mức độ chi tiết *(granularity)*, nhiều nhiệm vụ *(tasks)* và nhiều *domains* khác nhau. Representation Learning đóng vai trò quan trọng trong việc biểu diễn ngữ nghĩa của các mục nhập ngôn ngữ ở các cấp độ khác nhau (ký tự, cụm từ, câu, đoạn văn, tài liệu) trong 1 không gian ngữ nghĩa thống nhất và xây dựng các mối quan hệ ngữ nghĩa phức tạp giữa chúng 
## Representation Learning giúp NLP giải quyết vấn đề "multiple granularities" như thế nào?
- NLP quan tâm đến nhiều cấp độ của các mục input ngôn ngữ, bao gồm nhưng không giới hạn ở ký tự, từ, cụm từ, câu. đoạn văn và tài liệu. Representation Learning giúp biểu diễn ngữ nghĩa của các mục nhập ngôn ngữ này trong một không gian ngữ nghĩa thống nhất. Điều này cho phép xây dựng các mối  quan hệ ngữ nghĩa phức tạp giữa các mục nhập ngôn ngữ ở các cấp độ khác nhau, cung cấp một khuôn khổ linh hoạt để xử lý và phân tích văn bản ngôn ngữ tự nhiên. 
- Học biểu diễn giúp NLP vượt qua ranh giới hình thức của ngôn ngữ (từ, câu, đoạn…) bằng cách **liên kết mọi cấp độ trong một không gian ngữ nghĩa chung**, hỗ trợ phân tích linh hoạt, hiệu quả và chính xác hơn.
## Làm thế nào để Representation Learning hỗ trợ các "Multiple Tasks" trong NLP?
- Có nhiều tasks NLP khác nhau dựa trên đầu vào. Ví dụ, với một câu, chúng ta có thể thực hiện nhiều nhiệm vụ như phân đoạn từ, gắn thẻ từ loại, nhận dạng thực thể có tên, trích xuất quan hệ và dịch máy. Representation Learning cung cấp một cách để tạo ra các biểu diễn ngữ nghĩa phong phú của input data, mà các biểu diễn này có thể dc sử dụng hoặc chuyển giao cho nhiều tasks khác nhau, cải thiện hiệu suất tổng thể à tính nhất quán của các mô hình NLP.
## Các phương pháp Representation trong NLP đã phát triển như thế nào? 
Sự phát triển của học biểu diễn trong NLP đã **chuyển từ kỹ thuật thủ công sang các phương pháp học sâu tự động**, đặc biệt là **học tự giám sát với mô hình lớn**, giúp **mã hóa ngữ nghĩa sâu hơn, linh hoạt hơn, và dễ chuyển giao hơn**, mở ra khả năng xử lý ngôn ngữ tự nhiên ngày càng hiệu quả và thông minh.


| **Giai đoạn**                      | **Phương pháp chính**         | **Đặc điểm nổi bật**                                 |
|-----------------------------------|-------------------------------|------------------------------------------------------|
| Biểu diễn thủ công                 | TF-IDF, BoW                   | Dựa vào đặc trưng rời rạc, không linh hoạt           |
| Học có giám sát                   | Mạng nơ-ron đơn giản          | Cần dữ liệu nhãn, không tổng quát                   |
| Biểu diễn từ không giám sát        | Word2Vec, GloVe               | Ngữ nghĩa cố định, học từ ngữ cảnh                   |
| Biểu diễn theo ngữ cảnh           | ELMo, BERT, GPT               | Ngữ nghĩa động, chuyển giao mạnh mẽ                  |
| Biểu diễn đa tầng & đa mô thức     | LLMs, Multimodal models       | Đa nhiệm, đa ngôn ngữ, đa phương tiện                |

# References
