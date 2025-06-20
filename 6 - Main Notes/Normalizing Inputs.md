2025-04-21 11:28


Tags: [[Model Generalization]], [[data scientist]]

# Normalizing Inputs
### Normalizing Training set
![[Pasted image 20250421113310.png]]
#### **Bên trái (Raw data - Dữ liệu gốc)**
Biểu đồ này hiển thị dữ liệu ban đầu chưa qua chuẩn hóa, với trục hoành là `x₁` và trục tung là `x₂`.
- Giá trị `x₁` dao động từ khoảng `0` đến `5`, trong khi `x₂` chỉ từ khoảng `0` đến `3`.
- Điều này khiến scale giữa các feature (đặc trưng) lệch nhau → gây khó khăn cho mô hình khi học, đặc biệt là thuật toán dựa vào khoảng cách (như KNN, gradient descent...).

#### **Giữa (Sau khi trừ mean)**

Bước đầu tiên là **trừ trung bình (subtract mean)** để đưa dữ liệu về trung tâm quanh gốc tọa độ (mean = 0).
**Công thức:**

$$μ= \frac{1}{m} \sum_{i=1}^{m} x^{(i)}, \quad x := x−μ$$
- Tính trung bình (mean) của từng feature.
- Trừ mean khỏi từng giá trị tương ứng.
- Sau bước này, các feature có trung bình bằng 0, nhưng vẫn còn scale khác nhau.

📌 Dòng dưới ghi:

> “Use same μ to normalize test set.”  
> → Nghĩa là ta cũng phải **dùng mean của tập train để chuẩn hóa tập test**.

---

#### 📏 **Bên phải (Sau khi chuẩn hóa phương sai - Normalize variance)**

Tiếp theo là chuẩn hóa phương sai để đưa scale của các feature về giống nhau (variance ≈ 1).

**Công thức:**

$$σ2= \frac{1}{m} \sum_{i=1}^{m} x^{(i)} \circ x^{(i)}, \quad x: =σx$$
- Tính độ lệch chuẩn `σ` theo từng feature (element-wise).    
- Chia dữ liệu cho `σ`.    

Kết quả: Cả `x₁` và `x₂` giờ đều có **mean = 0** và **variance ≈ 1** → giúp mô hình học nhanh và ổn định hơn.

---

### 📌 **Tóm tắt quy trình chuẩn hóa (Normalization):**

1. **Tính trung bình `μ` cho từng feature.**
2. **Trừ `μ` khỏi dữ liệu → mean = 0.**
3. **Tính độ lệch chuẩn `σ`.*    
4. **Chia dữ liệu cho `σ` → variance = 1.**    
5. **Dùng cùng `μ` và `σ` để chuẩn hóa tập test.**
### Why normalizing inputs?

![[Pasted image 20250421113836.png]]
- Việc không normalizing sẽ khiến hàm loss $J(w, b)$ có hình dạng méo mó, khiến cho quá trình hội tụ không ổn định. 
## **Bên trái: Unnormalized (Không chuẩn hóa)**

###  Hình dạng hàm mất mát (`J`)
- Hình elip dài, dẹt → các đường đồng mức (contour) bị **kéo dài** theo 1 hướng.
- Gradient descent khó tìm đường đi ngắn → phải "zigzag" rất nhiều để tới được điểm cực tiểu.    
###  Đường đi gradient
- Đường đi lắc ngoằn ngoèo.
- Mất **nhiều bước** để hội tụ.    
- Nguyên nhân: Scale của các đặc trưng không giống nhau (ví dụ `x₁ ∈ [1, 1000]`, `x₂ ∈ [0, 1]`).

##  **Bên phải: Normalized (Đã chuẩn hóa)**

###  Hình dạng hàm mất mát (`J`)

- Trông như hình bát úp tròn, đối xứng → contour là **đường tròn đồng tâm**.
- Gradient descent dễ tìm đường đi ngắn nhất đến cực tiểu.

###  Đường đi gradient
- Trực tiếp, nhanh chóng.
- Hội tụ **nhanh hơn nhiều**.

|                                | **Kết luận:**                          |
| ------------------------------ | -------------------------------------- |
| Before normalizing             | After normalizing                      |
| Hàm loss méo mó                | Hàm loss đối xứng, dễ tối ưu           |
| Gradient descent không ổn định | Gradient descent ổn định, hội tụ nhanh |


# References
