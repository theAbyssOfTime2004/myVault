2025-04-22 00:21


Tags: [[data scientist]], [[Machine Learning]], [[Deep Learning]]

# Regularization

---

## 1. Vấn đề cần giải quyết

Một model không bị ràng buộc sẽ tối ưu hóa hoàn toàn trên training data, học cả noise lẫn signal → overfit. Trên unseen data, performance sụt giảm.

Regularization là tập kỹ thuật thêm **penalty vào loss function** hoặc **ràng buộc vào quá trình training** để giảm model complexity, từ đó giảm variance mà không tăng bias quá nhiều.

---

## 2. L1 Regularization (Lasso)

Thêm tổng giá trị tuyệt đối của weights vào loss:

$$L_{total} = L_{original} + \lambda \sum_{j=1}^{n} |w_j|$$

**Tính chất quan trọng — sparse solution:**

L1 penalty tạo ra góc nhọn (non-differentiable) tại $w = 0$. Khi tối ưu hóa, nhiều weight bị đẩy về đúng bằng 0 → model tự động chọn feature (feature selection). Kết quả là sparse weight vector: phần lớn $w_j = 0$, chỉ một số feature có trọng số khác 0.

**Khi nào dùng:** Khi nghi ngờ chỉ một tập nhỏ feature thực sự có ý nghĩa, cần interpretability, hoặc cần giảm số feature.

---

## 3. L2 Regularization (Ridge)

Thêm tổng bình phương của weights vào loss:

$$L_{total} = L_{original} + \lambda \sum_{j=1}^{n} w_j^2$$

**Tính chất quan trọng — weight shrinkage:**

L2 penalty phạt weight lớn nặng hơn (bình phương), nhưng gradient tiến dần về 0 khi $w \to 0$ nên không đẩy weight về đúng bằng 0. Kết quả là tất cả weight đều nhỏ nhưng không ai bằng 0 — model vẫn dùng tất cả feature nhưng với magnitude thấp hơn.

Với Linear Regression, L2 có closed-form solution:

$$w = (X^TX + \lambda I)^{-1} X^T y$$

$\lambda I$ làm cho ma trận luôn invertible → giải quyết được cả trường hợp multicollinearity.

**Khi nào dùng:** Khi hầu hết feature đều có đóng góp, cần ổn định với multicollinearity.

---

## 4. Elastic Net

Kết hợp cả L1 và L2:

$$L_{total} = L_{original} + \lambda_1 \sum|w_j| + \lambda_2 \sum w_j^2$$

Giữ tính chất sparse của L1 nhưng ổn định hơn khi có nhiều feature tương quan với nhau (L1 thường chỉ chọn một trong nhóm feature tương quan, bỏ qua phần còn lại).

---

## 5. So sánh L1 và L2 — Góc nhìn hình học

Bài toán regularization tương đương với constrained optimization:

- **L1**: Tối ưu subject to $\sum|w_j| \leq t$ → feasible region là hình thoi (diamond) trong 2D. Optimal solution thường nằm tại đỉnh hình thoi → $w_j = 0$ cho một số chiều.
- **L2**: Tối ưu subject to $\sum w_j^2 \leq t$ → feasible region là hình cầu (sphere). Optimal solution nằm trên surface của cầu → weight nhỏ nhưng hiếm khi đúng bằng 0.

---

## 6. Dropout (Deep Learning)

Trong neural network, Dropout là kỹ thuật regularization khác — tại mỗi training step, randomly set một tỷ lệ $p$ neuron về 0:

$$\tilde{h}_i = h_i \cdot \text{Bernoulli}(1-p)$$

Tại inference, không drop neuron nhưng scale output: $h_i \leftarrow h_i \cdot (1-p)$ để giữ expected value nhất quán.

**Cơ chế:** Dropout ngăn model phụ thuộc quá vào một tập neuron cụ thể, buộc network học các redundant representation. Tương đương với training trên ensemble $2^n$ sub-network chia sẻ weight.

---

## 7. Early Stopping

Dừng training khi validation loss bắt đầu tăng dù training loss vẫn giảm. Đây là một dạng regularization implicit: ngăn model fit quá kỹ vào training data.

```
Training loss  ────────────────────────────► (giảm liên tục)
Validation loss ──────────\____/‾‾‾‾‾‾‾‾‾► (giảm rồi tăng)
                           ▲
                     best checkpoint
```

---

## 8. Batch Normalization

Normalize activation của mỗi layer về mean=0, std=1 trước khi đưa vào layer tiếp theo:

$$\hat{x} = \frac{x - \mu_B}{\sqrt{\sigma_B^2 + \epsilon}}, \quad y = \gamma\hat{x} + \beta$$

$\gamma$ và $\beta$ là learnable parameters. Có tác dụng regularization nhẹ do noise từ batch statistics, nhưng mục đích chính là ổn định training (giảm internal covariate shift).

---

## 9. Tóm tắt

| Kỹ thuật | Áp dụng cho | Cơ chế | Effect |
|---|---|---|---|
| L1 (Lasso) | Linear model, neural net | Penalty $\sum\|w\|$ | Sparse weights, feature selection |
| L2 (Ridge) | Linear model, neural net | Penalty $\sum w^2$ | Weight shrinkage, xử lý multicollinearity |
| Elastic Net | Linear model | L1 + L2 | Sparse + stable với correlated features |
| Dropout | Neural network | Random zero-out neuron | Ensemble effect, reduce co-adaptation |
| Early Stopping | Mọi iterative model | Dừng theo val loss | Ngăn overfit theo thời gian train |
| Batch Norm | Neural network | Normalize activation | Ổn định training, regularization nhẹ |

---

# References
