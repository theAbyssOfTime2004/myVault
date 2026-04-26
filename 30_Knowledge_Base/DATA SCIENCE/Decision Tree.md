2025-01-13 19:39


Tags: [[supervised learning]], [[Machine Learning]], [[regression]], [[classification]]

# Decision Tree

---

## 1. Cơ chế hoạt động

Decision Tree là một thuật toán học có giám sát (supervised learning) xây dựng một cây phân nhánh để đưa ra quyết định phân loại (classification) hoặc hồi quy (regression).

Cây được xây dựng từ trên xuống bằng cách liên tục chia nhỏ dataset tại mỗi node theo một feature và ngưỡng nhất định. Quá trình này gọi là **recursive binary splitting**.

```
                  [Age < 30?]
                 /            \
           Yes /              \ No
         [Income < 50k?]    [Credit > 700?]
          /        \           /        \
        Deny     Approve    Approve    Deny
```

---

## 2. Tiêu chí phân chia (Splitting Criteria)

Tại mỗi node, thuật toán tìm feature và ngưỡng tối ưu để chia data thành hai nhánh sao cho mỗi nhánh càng "thuần" càng tốt (homogeneous). Độ đo "thuần" phụ thuộc vào loại bài toán:

### Gini Impurity (Classification)

Đo xác suất một sample bị phân loại sai nếu label được chọn ngẫu nhiên theo phân phối của node đó:

$$Gini = 1 - \sum_{k=1}^{K} p_k^2$$

Trong đó $p_k$ là tỷ lệ của class $k$ trong node. Gini = 0 khi node chứa toàn một class (pure). Gini = 0.5 (với binary class) khi hai class bằng nhau (worst case).

### Entropy / Information Gain (Classification)

$$Entropy = -\sum_{k=1}^{K} p_k \log_2 p_k$$

**Information Gain** = Entropy của node cha − weighted average Entropy của hai node con. Thuật toán chọn split có Information Gain cao nhất.

Gini và Entropy cho kết quả tương tự trong thực tế. Gini tính nhanh hơn (không có log), Entropy nhạy hơn với class imbalance.

### MSE (Regression)

Với bài toán regression, tiêu chí là giảm thiểu Mean Squared Error:

$$MSE = \frac{1}{n}\sum_{i=1}^{n}(y_i - \bar{y})^2$$

Node prediction là mean của tất cả $y$ trong node đó.

---

## 3. Thuật toán xây dựng cây

**Greedy approach** — tại mỗi bước chọn split tốt nhất cục bộ, không đảm bảo cây tối ưu toàn cục:

```
function BuildTree(data, depth):
    if stopping_condition(data, depth):
        return LeafNode(predict(data))

    best_feature, best_threshold = find_best_split(data)
    left_data, right_data = split(data, best_feature, best_threshold)

    return Node(
        feature=best_feature,
        threshold=best_threshold,
        left=BuildTree(left_data, depth+1),
        right=BuildTree(right_data, depth+1)
    )
```

**Stopping conditions:**
- Node đạt `max_depth`
- Node có ít hơn `min_samples_split` sample
- Information Gain của split tốt nhất < threshold
- Node đã pure (Gini = 0)

---

## 4. Overfitting và Pruning

Decision Tree không bị chặn sẽ grow đến khi mỗi leaf chứa đúng 1 sample → overfit hoàn toàn vào training data. Hai hướng kiểm soát:

### Pre-pruning (Early Stopping)
Dừng sớm trong quá trình xây dựng cây bằng cách giới hạn hyperparameter:
- `max_depth`: chiều sâu tối đa của cây
- `min_samples_split`: số sample tối thiểu để split một node
- `min_samples_leaf`: số sample tối thiểu trong một leaf
- `min_impurity_decrease`: Information Gain tối thiểu để thực hiện split

### Post-pruning
Xây cây đầy đủ trước, sau đó cắt bỏ các subtree không cải thiện performance trên validation set. **Cost-Complexity Pruning** (hay Weakest Link Pruning) là phương pháp phổ biến nhất — tìm subtree tối ưu hóa:

$$R_\alpha(T) = R(T) + \alpha \cdot |T|$$

Trong đó $R(T)$ là training error, $|T|$ là số leaf, $\alpha$ là regularization parameter. Tăng $\alpha$ → cây nhỏ hơn.

---

## 5. Feature Importance

Sau khi train, mỗi feature được gán một score dựa trên tổng Information Gain mà feature đó đóng góp khi được dùng để split, có weighted theo số sample đi qua node đó:

$$Importance(f) = \sum_{\text{nodes split by } f} \frac{n_{node}}{n_{total}} \cdot \Delta impurity$$

Feature importance được normalize về [0, 1]. Đây là cách nhanh để hiểu feature nào quan trọng, nhưng có bias với feature có nhiều giá trị unique (high cardinality).

---

## 6. Ưu và nhược điểm

**Ưu điểm:**
- Không cần scale feature (invariant với monotonic transformation)
- Xử lý được cả numerical và categorical feature
- Interpretable: có thể visualize và trace từng decision
- Không cần nhiều preprocessing

**Nhược điểm:**
- Dễ overfit nếu không regularize
- Unstable: thay đổi nhỏ trong data có thể tạo ra cây hoàn toàn khác
- Không phù hợp với quan hệ tuyến tính (axis-aligned splits kém hiệu quả)
- Bias với feature có nhiều giá trị unique

---

## 7. Decision Tree làm nền tảng cho Ensemble Methods

Decision Tree đơn lẻ hiếm khi được dùng trong production vì variance cao. Thay vào đó, nó là thành phần cơ bản của:

- **Random Forest**: Train nhiều cây trên random subsample của data và feature, average kết quả → giảm variance
- **Gradient Boosting (XGBoost, LightGBM)**: Train cây tuần tự, mỗi cây fit vào residual của cây trước → giảm bias

---

# References
