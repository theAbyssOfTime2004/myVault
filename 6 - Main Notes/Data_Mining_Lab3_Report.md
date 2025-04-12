2025-04-12 19:36


Tags:  [[data mining]], [[Data Mining Lab2 Report]], [[Data Mining Lab1 Report]]

**Họ và Tên**: Mai Phong Đăng
**MSSV**: 22280008
**Lớp**: 22KDL

# Data Mining Lab3 Report

## Bài 1: Chương trình tìm dãy con chung lớn nhất (LCS)
### Trình bày tóm lược phần code: 

#### **Hàm** `longest_common_subsequence(X,Y):` 

**Bước 1: Khởi tạo**
```python
m = len(X)
n = len(Y)
L = [[0] * (n + 1) for _ in range(m + 1)]
```
- Tạo bảng `L` kích thước `(m+1) x (n+1)` để lưu độ dài của LCS giữa từng cặp con chuỗi `X[0..i]` và `Y[0..j]`. 

 **Bước 2: Xây dựng bảng `L` từ dưới lên:**
```python
for i in range(m + 1):
    for j in range(n + 1):
        if i == 0 or j == 0:
            L[i][j] = 0  # Nếu 1 trong 2 chuỗi rỗng → LCS = 0
        elif X[i - 1] == Y[j - 1]:
            L[i][j] = L[i - 1][j - 1] + 1  # Nếu ký tự giống → tăng độ dài LCS
        else:
            L[i][j] = max(L[i - 1][j], L[i][j - 1])  # Lấy max từ trên hoặc trái
```

**Bước 3: Lấy độ dài LCS**
```python
lcs_length = L[m][n]
```

**Bước 4: Truy vết ngược để tìm chuỗi LCS**
```python
lcs = [""] * lcs_length
i, j = m, n
index = lcs_length - 1
```
- Bắt đầu từ góc dưới phải của bảng `L[m][n]`, đi ngược để tìm các ký tự thuộc LCS.
```python
while i > 0 and j > 0:
    if X[i - 1] == Y[j - 1]:
        lcs[index] = X[i - 1]
        i -= 1
        j -= 1
        index -= 1
    elif L[i - 1][j] > L[i][j - 1]:
        i -= 1
    else:
        j -= 1
```
- Nếu ký tự trùng → đưa vào LCS.
- Nếu không trùng → đi theo hướng có giá trị lớn hơn (lên hoặc trái).

**Bước 5: Trả kết quả**
```python
return lcs_length, ''.join(lcs)
```

#### **Hàm `main()`**:

**Bước 1: Nhập chuỗi**
```python
X = input("Enter the first string: ")
Y = input("Enter the second string: ")
```

**Bước 2: Gọi hàm và in kết quả**
```python
length, sequence = longest_common_subsequence(X, Y)
```
- In ra:
	- Độ dài LCS
	- Chuỗi LCS tìm được

**Bước 3: In bảng minh họa (nếu chuỗi ngắn)**
```python
if len(X) <= 10 and len(Y) <= 10:
```
- In ra bảng `L[i][j]` giúp hình dung cách thuật toán hoạt động.
### Kết luận:
- Chương trình sử dụng thuật toán lập trình động để giải bài toán LCS một cách hiệu quả.
- Có khả năng hiển thị trực quan bảng động để kiểm tra quá trình tính toán.

## Bài 2: Chương trình tính khoảng cách biến đổi thời gian động
### Trình bày tóm lược phần code:

#### **Hàm `dtw_distance(sequence1, sequence2)`

**Bước 1: Tiền xử lý**
```python
seq1 = [int(x) for x in sequence1]
seq2 = [int(x) for x in sequence2]
```
- Chuyển từng ký tự trong chuỗi nhập vào (dạng `"1234"`) thành danh sách số nguyên `[1, 2, 3, 4]`.

**Bước 2: Tạo ma trận DTW**
```python
dtw_matrix = np.zeros((n+1, m+1))
```
- Tạo ma trận `DTW` kích thước `(n+1)x(m+1)` với (n, m là độ dài 2 chuỗi).
- Khởi tạo dòng 0 và cột 0 là `inf`, ngoại trừ gốc `(0,0)`:
```python
for i in range(1, n+1): dtw_matrix[i, 0] = inf
for j in range(1, m+1): dtw_matrix[0, j] = inf
```
- Đặt điểm bắt đầu `(1,1)` là khoảng cách giữa 2 phần tử đầu tiên:
```python
dtw_matrix[1, 1] = abs(seq1[0] - seq2[0])
```

**Bước 3: Tính toán ma trận DTW**
```python
for i in range(1, n+1):
    for j in range(1, m+1):
        if i == 1 and j == 1: continue
        cost = abs(seq1[i-1] - seq2[j-1])
        dtw_matrix[i, j] = cost + min(
            dtw_matrix[i-1, j],
            dtw_matrix[i, j-1],
            dtw_matrix[i-1, j-1]
        )
```
- Tính **khoảng cách Manhattan** giữa các phần tử. Giá trị `dtw_matrix[i,j]` là chi phí để đi đến điểm đó theo hướng tối ưu nhất.

**Bước 4: Backtracking** 
- Từ điểm cuối `(n,m)`, tìm đường đi ngược lại:
```python
# Trace the optimal path (warping path)
path = []
i, j = n, m

# Start from the end point (n,m)
current_cost = dtw_matrix[i, j]
path.append(int(current_cost))
```

```python 
while i > 1 or j > 1:
# Find the next direction (backwards from end to start)

if i == 1:
j -= 1
elif j == 1:
i -= 1

else:
min_cost = min(
dtw_matrix[i-1, j], # up
dtw_matrix[i, j-1], # left
dtw_matrix[i-1, j-1] # diagonal
)

if min_cost == dtw_matrix[i-1, j-1]:
i -= 1
j -= 1
elif min_cost == dtw_matrix[i-1, j]:
i -= 1
else:
j -= 1

# Add current cost to path
if i >= 1 and j >= 1:
current_cost = dtw_matrix[i, j]
if np.isfinite(current_cost): # Only add if value is finite
path.append(int(current_cost))
```
- Thêm `0` vào cuối (vì khởi đầu ở (0,0)), rồi **đảo ngược path**:
```python
path.append(0)
path.reverse()
```

#### **Hàm `pretty_print_matrix()`**

- In ra ma trận chi phí DTW theo **định dạng đẹp mắt**.
- Dòng đầu là các phần tử chuỗi `seq1`, cột là chuỗi `seq2`.

#### **Hàm `main()`**
- Cho người dùng nhập 2 chuỗi.
- Gọi hàm `dtw_distance` để tính toán.
- In ra kết quả: khoảng cách, ma trận, warping path.

### Kết Luận:
- Chương trình áp dụng thuật toán DTW giúp tính toán khoảng cách linh hoạt giữa hai chuỗi có độ dài khác nhau, hữu ích trong những ứng dụng như nhận diện giọng nói, so khớp chuỗi thời gian, hay xử lý tín hiệu.
# References
