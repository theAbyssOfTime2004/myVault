---
tags:
  - pytorch
  - autograd
  - deep-learning
  - backpropagation
  - gradient
created: 2026-05-02
---

# PyTorch Autograd & Computational Graph

## Vấn đề cần giải quyết

Training neural network yêu cầu tính gradient của loss đối với mọi tham số (`∂L/∂w`) để update weight. Với mạng hàng triệu tham số, tính tay là không thể. **Autograd** tự động hóa quá trình này.

---

## Computational Graph

Khi thực hiện các phép toán trên tensor có `requires_grad=True`, PyTorch **không tính ngay giá trị gradient** mà xây dựng một **đồ thị có hướng không chu trình (DAG)** ghi lại:
- Các tensor (node lá và node trung gian)
- Phép toán tạo ra chúng (edge)

```python
import torch

x = torch.tensor(2.0, requires_grad=True)
y = torch.tensor(3.0, requires_grad=True)

z = x ** 2 + y * x   # z = x² + yx
```

Graph tương ứng:

```
x ──┬──► (x²) ──► AddBackward ──► z
    │
y ──┴──► (y*x) ─────────────────►
```

Mỗi node trung gian lưu một **grad_fn** — hàm biết cách tính gradient ngược qua phép toán đó.

```python
print(z.grad_fn)          # <AddBackward0 object>
print(z.grad_fn.next_functions)  # ((PowBackward0, 0), (MulBackward0, 0))
```

**Quan trọng:** Graph được xây dựng **động (define-by-run)** — mỗi forward pass tạo graph mới, cho phép dùng Python control flow (if, for) thoải mái.

---

## requires_grad & leaf tensor

```python
# Leaf tensor: tạo trực tiếp, không phải kết quả của phép toán
w = torch.randn(3, 3, requires_grad=True)   # leaf, requires_grad=True
b = torch.zeros(3, requires_grad=True)       # leaf

# Non-leaf: kết quả của phép toán
h = w @ x + b    # h.grad_fn = <AddmmBackward0>
```

- **Leaf tensor** với `requires_grad=True`: gradient sẽ được tích lũy vào `.grad` sau `backward()`
- **Non-leaf tensor**: gradient chỉ tồn tại trong quá trình backward, không lưu (trừ khi gọi `.retain_grad()`)
- Tensor tạo từ data thuần (numpy, list) mặc định `requires_grad=False`

---

## loss.backward()

Gọi `.backward()` trên scalar tensor → PyTorch **duyệt ngược graph** (reverse-mode autodiff) và tính gradient theo chain rule.

```python
x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
loss = (x ** 2).sum()   # loss = x₁² + x₂² + x₃²

loss.backward()

print(x.grad)   # tensor([2., 4., 6.])  ← ∂loss/∂xᵢ = 2xᵢ
```

**Chain rule trong graph:**

```
loss = sum(z),  z = x²
∂loss/∂x = ∂loss/∂z · ∂z/∂x = 1 · 2x = 2x
```

### backward() với non-scalar

Nếu output không phải scalar, phải truyền `gradient` tensor (vector-Jacobian product):

```python
y = x * 2   # y shape: [3]
y.backward(torch.ones(3))   # gradient = dy/dx * [1,1,1] = [2,2,2]
print(x.grad)   # tensor([2., 2., 2.])
```

---

## Gradient accumulation

Mặc định `.grad` **cộng dồn** qua các lần backward, không overwrite:

```python
for step in range(3):
    loss = (x ** 2).sum()
    loss.backward()
    print(x.grad)   # tăng dần: 2x, 4x, 6x
```

Phải **zero gradient** trước mỗi backward pass:

```python
optimizer.zero_grad()   # hoặc x.grad.zero_()
loss.backward()
optimizer.step()
```

Lý do thiết kế này: cho phép **gradient accumulation** để simulate batch lớn hơn VRAM cho phép:

```python
accumulation_steps = 4
for i, (inputs, labels) in enumerate(dataloader):
    loss = model(inputs, labels) / accumulation_steps
    loss.backward()                          # tích lũy gradient

    if (i + 1) % accumulation_steps == 0:
        optimizer.step()
        optimizer.zero_grad()
```

---

## torch.no_grad() và inference mode

Trong lúc inference, không cần graph → tắt tracking để tiết kiệm memory và tăng tốc:

```python
with torch.no_grad():
    output = model(x)   # không tạo graph, không lưu grad_fn
```

`torch.inference_mode()` mạnh hơn `no_grad()`: disable thêm version tracking, nhanh hơn ~10-15%:

```python
with torch.inference_mode():
    output = model(x)
```

**Khi nào dùng cái nào:**

| | `no_grad` | `inference_mode` |
|---|---|---|
| Forward pass inference | dùng được | tốt hơn |
| Bên trong custom backward | dùng được | không dùng |
| Eval loop, metric tính | dùng được | tốt hơn |

---

## detach()

Tách tensor ra khỏi graph — kết quả không có `grad_fn`, gradient không chảy ngược qua nó:

```python
y = model_A(x)
z = model_B(y.detach())   # gradient của z không update model_A
```

Dùng khi:
- Target network trong reinforcement learning (stop-gradient)
- Chỉ train một phần của mạng
- Chuyển sang numpy: `tensor.detach().cpu().numpy()`

---

## Luồng training đầy đủ

```python
model = MyModel()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.CrossEntropyLoss()

for inputs, labels in dataloader:
    # 1. Zero gradient từ step trước
    optimizer.zero_grad()

    # 2. Forward pass → xây computational graph
    outputs = model(inputs)

    # 3. Tính loss
    loss = criterion(outputs, labels)

    # 4. Backward pass → tính gradient bằng cách duyệt ngược graph
    loss.backward()

    # 5. Gradient clipping (optional)
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

    # 6. Update weights
    optimizer.step()
```

---

## Hooks (nâng cao)

Có thể gắn hook vào tensor hoặc module để inspect/modify gradient:

```python
# Tensor hook: chạy khi gradient của tensor được tính
x.register_hook(lambda grad: print("grad of x:", grad))

# Module hook: chạy trong backward của layer
layer.register_backward_hook(lambda m, grad_in, grad_out: ...)
```

Dùng để: debug vanishing gradient, gradient visualization, custom gradient modification.

---

## Tóm tắt

```
Forward pass  →  xây computational graph (DAG)
                 mỗi op lưu grad_fn

loss.backward() →  duyệt ngược graph
                   áp dụng chain rule tại mỗi node
                   tích lũy vào .grad của leaf tensors

optimizer.step() →  w = w - lr * w.grad
```

---

## Liên kết

- [[Backpropagation]]
- [[Neural Network]]
- [[Vanishing and Exploding Gradient]]
