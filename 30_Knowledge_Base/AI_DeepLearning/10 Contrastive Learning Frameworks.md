2024-11-25 21:12

Tags: [[DeepLearning]], [[Machine Learning]], [[Self-Supervised Learning]], [[supervised learning]]

# 10 [[Contrastive Learning]] Frameworks

[[Contrastive Learning]] (Học Tương phản) là một phương pháp học biểu diễn (representation learning) thuộc lĩnh vực [[Self-Supervised Learning]]. Ý tưởng cốt lõi là học một không gian nhúng (embedding space) nơi các mẫu "tương tự" (positive pairs) được kéo lại gần nhau và các mẫu "khác biệt" (negative pairs) bị đẩy ra xa nhau.

Dưới đây là 10 framework học tương phản nổi bật và có ảnh hưởng lớn trong lĩnh vực này.

1.  **[[SimCLR]] (A Simple Framework for Contrastive Learning of Visual Representations)**
    *   **Ý tưởng chính**: Sử dụng các kỹ thuật tăng cường dữ liệu (data augmentation) mạnh mẽ để tạo ra các cặp positive từ cùng một ảnh. Mô hình học cách phân biệt các phiên bản tăng cường của cùng một ảnh với các ảnh khác trong một batch lớn. SimCLR không cần memory bank.

2.  **[[MoCo]] (Momentum Contrast for Unsupervised Visual Representation Learning)**
    *   **Ý tưởng chính**: Giải quyết vấn đề cần batch size lớn của SimCLR bằng cách sử dụng một "dictionary" động dưới dạng hàng đợi (queue) để lưu trữ các negative samples. MoCo sử dụng một momentum encoder để giữ cho các biểu diễn trong dictionary nhất quán.

3.  **[[BYOL]] (Bootstrap Your Own Latent)**
    *   **Ý tưởng chính**: Một phương pháp không hoàn toàn "tương phản" vì nó chỉ học từ các cặp positive. BYOL sử dụng hai mạng nơ-ron: online và target. Mạng online học cách dự đoán biểu diễn của mạng target (một phiên bản trung bình động của mạng online). Điều này giúp tránh hiện tượng sụp đổ (collapsing) mà không cần negative samples.

4.  **[[SimSiam]] (Exploring Simple Siamese Representation Learning)**
    *   **Ý tưởng chính**: Đơn giản hóa hơn nữa các phương pháp Siamese (như BYOL) và chứng minh rằng chỉ cần một thao tác "stop-gradient" là đủ để ngăn chặn hiện tượng sụp đổ. SimSiam cho thấy các thành phần phức tạp như negative pairs, batch lớn, hay momentum encoder không phải lúc nào cũng cần thiết.

5.  **[[SwAV]] (Unsupervised Learning of Visual Features by Contrasting Cluster Assignments)**
    *   **Ý tưởng chính**: Thay vì so sánh trực tiếp các feature, SwAV so sánh các "cluster assignments" (phân cụm). Mô hình học cách gán các phiên bản tăng cường của cùng một ảnh vào cùng một cụm. Đây là một phương pháp kết hợp giữa học tương phản và học theo cụm (clustering).

6.  **[[InfoNCE Loss]] & [[CPC]] (Contrastive Predictive Coding)**
    *   **Ý tưởng chính**: InfoNCE là hàm mất mát nền tảng cho nhiều phương pháp học tương phản. CPC sử dụng InfoNCE để học các biểu diễn bằng cách dự đoán các biểu diễn trong tương lai (ví dụ: các patch tiếp theo trong một ảnh hoặc các đoạn âm thanh tiếp theo) từ một ngữ cảnh trong quá khứ.

7.  **[[PIRL]] (Pretext-Invariant Representation Learning)**
    *   **Ý tưởng chính**: Học các biểu diễn bất biến với một "pretext task" (nhiệm vụ tự tạo). Ví dụ, mô hình học một biểu diễn cho ảnh gốc sao cho nó gần với biểu diễn của phiên bản ảnh đã được giải đố Jigsaw.

8.  **[[DINO]] (Self-**DI**stillation with **NO** labels)**
    *   **Ý tưởng chính**: Một phương pháp tự chưng cất (self-distillation) không cần nhãn. DINO huấn luyện một student network để khớp với đầu ra của một teacher network (được cập nhật bằng momentum). Phương pháp này đặc biệt hiệu quả với Vision Transformers (ViT) và có thể tạo ra các segmentation map chất lượng cao.

9.  **[[CLIP]] (Contrastive Language–Image Pre-training)**
    *   **Ý tưởng chính**: Học các biểu diễn đa phương thức (multimodal) bằng cách đối chiếu các cặp (ảnh, văn bản) từ một tập dữ liệu khổng lồ trên web. CLIP học cách liên kết một mô tả văn bản với hình ảnh tương ứng, tạo ra các biểu diễn mạnh mẽ có khả năng zero-shot transfer.

10. **[[Barlow Twins]]**
    *   **Ý tưởng chính**: Một phương pháp không cần negative sampling. Thay vì kéo các cặp positive lại gần và đẩy các cặp negative ra xa, Barlow Twins tối ưu hóa ma trận tương quan chéo (cross-correlation matrix) giữa các embedding của hai phiên bản tăng cường của cùng một ảnh, buộc nó phải gần với ma trận đơn vị. Điều này giúp giảm sự dư thừa thông tin giữa các chiều của vector embedding.

# References
- Chen, T., Kornblith, S., Norouzi, M., & Hinton, G. (2020). *A Simple Framework for Contrastive Learning of Visual Representations*.
- He, K., Fan, H., Wu, Y., Xie, S., & Girshick, R. (2020). *Momentum Contrast for Unsupervised Visual Representation Learning*.
- Grill, J. B., Strub, F., Altché, F., Tallec, C., Richemond, P., Buchatskaya, E., ... & Valko, M. (2020). *Bootstrap Your Own Latent: A New Approach to Self-Supervised Learning*.
- Chen, X., & He, K. (2021). *Exploring Simple Siamese Representation Learning*.
- Caron, M., Misra, I., Mairal, J., Goyal, P., Bojanowski, P., & Joulin, A. (2020). *Unsupervised Learning of Visual Features by Contrasting Cluster Assignments*.
- Radford, A., Kim, J. W., Hallacy, C., Ramesh, A., Goh, G., Agarwal, S., ... & Sutskever, I. (2021). *Learning Transferable Visual Models From Natural Language Supervision*.
- Zbontar, J., Jing, L., Misra, I., LeCun, Y., & Deny, S. (2021). *Barlow Twins: Self-Supervised Learning via Redundancy Reduction*.
- Caron, M., Touvron, H., Misra, I., Jégou, H., Mairal, J., Bojanowski, P., & Joulin, A. (2021). *Emerging Properties in Self-Supervised Vision Transformers*.
