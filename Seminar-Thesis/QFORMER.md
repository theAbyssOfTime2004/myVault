[[seminar HCMUS]]
### 1. **Hiểu vai trò của Qformer trong DASCO paper**

- **Qformer là gì?** Đây là một transformer-based module (từ BLIP-2) sử dụng "query-based attention" để bridging (kết nối) và alignment (căn chỉnh) giữa image features (V) và text features. Thay vì chỉ concatenate hoặc average như code hiện tại, Qformer học cách "hỏi" (query) từ text để tương tác với image patches, tạo ra representations chung cho multimodal.
- **Tại sao cần?** Trong mô tả gốc, V là visual features được xử lý qua Qformer để align với text (ví dụ: aspect "camera" được align với visual patches của camera). Code hiện tại thiếu phần này, nên fusion chỉ là cơ bản (average với [CLS] token), không tối ưu cho alignment tinh tế.
- **Lợi ích**: Cải thiện multimodal understanding, giúp model hiểu mối quan hệ giữa text và image tốt hơn, đặc biệt cho ABSA (aspect-based sentiment analysis).