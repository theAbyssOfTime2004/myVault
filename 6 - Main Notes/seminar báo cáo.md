2026-01-25 00:34


Tags: [[seminar HCMUS]]

# seminar báo cáo

### 1. Nhóm câu hỏi về Phương pháp SMF

**Câu hỏi:** _"Tại sao nhóm lại chọn hướng tiếp cận Data-centric (xử lý dữ liệu bên ngoài) thay vì Model-centric (cải tiến kiến trúc bên trong)?"_

- **Trả lời:** Các phương pháp model-centric (điều chỉnh nội bộ kiến trúc) giúp mô hình nắm bắt thông tin tốt hơn nhưng làm tăng số lượng tham số và kéo dài thời gian huấn luyện. Trong thực tế, đặc biệt là lĩnh vực khách sạn, dữ liệu thường có độ nhiễu cross-modal lớn do hình ảnh và văn bản ít liên quan đến nhau. Vì vậy, nhóm chọn hướng data-centric để giảm nhiễu ngay từ đầu vào, giúp mô hình học biểu diễn chính xác hơn mà không cần thay đổi kiến trúc phức tạp.
    

**Câu hỏi:** _"Tại sao lại tách văn bản thành từng câu đơn (sentences)? Việc này có làm mất ngữ cảnh không?"_

- **Trả lời:** Nhóm thực hiện tách câu để giảm độ phức tạp của văn bản gốc, xem mỗi câu là một đơn vị ngữ nghĩa tương đối độc lập. Việc này tạo điều kiện để mô hình khai thác mối liên hệ chi tiết hơn giữa từng câu văn cụ thể và nội dung hình ảnh tương ứng, thay vì phải xử lý cả đoạn văn dài.
    

**Câu hỏi:** _"Cơ sở nào để chọn ngưỡng (threshold) lọc độ tương đồng là 0.3?"_

- **Trả lời:** Nhóm thiết lập ngưỡng threshold=0.3 nhằm đảm bảo chỉ giữ lại những cặp câu - hình ảnh có mối liên hệ ngữ nghĩa đủ mạnh. Các giá trị similarity được tính toán giữa câu và mô tả ảnh (caption), và chỉ k cặp có giá trị cao nhất và lớn hơn 0.3 mới được đưa vào tập text-image để loại bỏ các cặp có mức độ liên quan thấp.
    

**Câu hỏi:** _"Tại sao dùng BLIP để sinh caption rồi mới tính similarity thay vì tính trực tiếp?"_

- **Trả lời:** Nhóm sử dụng mô hình BLIP để tạo ra các mô tả văn bản cho ảnh (bao gồm ảnh gốc và ảnh vật thể). Các mô tả này đóng vai trò là biểu diễn trung gian, đưa thông tin thị giác về cùng không gian ngữ nghĩa với văn bản. Điều này tạo thuận lợi cho việc so sánh và đo lường mức độ tương đồng giữa hai loại dữ liệu.
    

### 2. Nhóm câu hỏi về Dữ liệu và Gán nhãn

**Câu hỏi:** _"Quy trình gán nhãn kết hợp người và máy như thế nào? Độ tin cậy ra sao?"_

- **Trả lời:** Nhóm áp dụng chiến lược Human-in-the-Loop. Đầu tiên, framework pyABSA được dùng để tạo nhãn sơ bộ cho Aspect Term, Opinion Term và Opinion Category. Sau đó, mô hình Gemma 3 được dùng để sinh Aspect Category. Cuối cùng, con người sẽ kiểm tra (recheck), chỉnh sửa nhãn sai hoặc bổ sung nhãn thiếu. Cách này giúp giảm thời gian, chi phí nhưng vẫn đảm bảo tính tin cậy và nhất quán của dữ liệu.
    

**Câu hỏi:** _"Nếu hình ảnh và văn bản mâu thuẫn cảm xúc thì xử lý thế nào?"_

- **Trả lời:** Bài toán ABSA cho phép phản ánh đồng thời nhiều quan điểm trong cùng một bài đánh giá. Nhãn cảm xúc được gán cho từng khía cạnh (aspect) cụ thể chứ không gán chung cho toàn văn bản. Do đó, nếu hình ảnh và văn bản thể hiện cảm xúc trái ngược trên các khía cạnh khác nhau, chúng sẽ được xử lý như các cặp Aspect-Sentiment riêng biệt.
    

### 3. Nhóm câu hỏi về Kết quả thực nghiệm

**Câu hỏi:** _"Tại sao VLP-MABSA lại tăng trưởng mạnh nhất (+18.4%) khi áp dụng SMF?"_

- **Trả lời:** Trong 4 mô hình, VLP-MABSA là mô hình duy nhất không sử dụng cơ chế bộ điều chỉnh nội bộ để kết hợp thông tin đa phương thức. Do đó, nó rất nhạy cảm với dữ liệu nhiễu. Khi áp dụng bộ lọc SMF (được xem là bộ điều chỉnh ngoại vi), dữ liệu đầu vào sạch hơn giúp hiệu năng mô hình tăng vọt, chứng tỏ SMF có hiệu quả tương tự các bộ điều chỉnh nội mô hình.
    

**Câu hỏi:** _"Tại sao DASCO có kiến trúc phức tạp nhưng kết quả lại thấp hơn?"_

- **Trả lời:** Mặc dù DASCO có kiến trúc hai giai đoạn và sử dụng đồ thị ngữ nghĩa/ngữ pháp để giảm nhiễu , kết quả thực nghiệm cho thấy nó đạt F1-score thấp hơn VLP-MABSA (0.7945 so với 0.8109). Điều này cho thấy mô hình này có sự nhạy cảm nhất định đối với đặc thù của dữ liệu lĩnh vực khách sạn trong nghiên cứu này.
    

**Câu hỏi:** _"Mô hình custom-DEQA có gì đặc biệt mà đạt kết quả cao nhất?"_

- **Trả lời:** Custom-DEQA (cùng với FCMF) là mô hình có tích hợp các cơ chế điều chỉnh hoặc tương tác chéo để khai thác mối quan hệ ngữ nghĩa. Kết quả F1-score 0.8523 cao nhất bảng chứng minh rằng việc thiết kế cơ chế căn chỉnh hiệu quả giữa các modality đóng vai trò quan trọng nhất trong bài toán này. Khi kết hợp thêm SMF, hiệu năng của nó tiếp tục tăng thêm 8.8%.
    

### 4. Nhóm câu hỏi mở rộng

**Câu hỏi:** _"Phương pháp SMF phụ thuộc vào yếu tố nào?"_

- **Trả lời:** Phương pháp SMF phụ thuộc vào hiệu quả của các mô hình thành phần trong pipeline xử lý. Cụ thể là mô hình YOLOv8 dùng để phát hiện và cắt ảnh vật thể , và mô hình BLIP dùng để sinh mô tả ảnh. Nếu các mô hình này hoạt động không tốt (ví dụ: cắt sai vật thể hoặc caption sai), chất lượng của bộ lọc sẽ bị ảnh hưởng.

# References
   