2025-04-06 01:53


Tags: [[data mining]], [[Data Mining Lab1 Report]]

**Họ và tên**: Mai Phong Đăng
**Mssv**: 22280008
**Lớp**: 22KDL

# Data Mining Lab2 Report

## Bài 1: Xử lý dữ liệu ionosphere 

### Data Overview

- Data có 35 cột với 34 đặc trưng với các giá trị số đại diện cho tín hiệu của radar, cột cuối cùng là nhãn ("label") với hai giá trị:
	-  `"g"` (good) - tín hiệu phản xạ có thể dùng để phân biệt đối tượng.
	- `"b"` (bad) - tín hiệu phản xạ không có giá trị phân loại.
``` python
import pandas as pd
import numpy as np
df = pd.read_csv('/content/ionosphere.data', header = None)
print(df)
```

### Data Preprocessing 

1. Bỏ cột nhãn (cột cuối) khỏi dataset để chuẩn bị cho việc tiền xử lý:
``` python
df.pop(df.columns[-1])
print(df)
```
2. Kiểm tra null, duplicate và fill null hay loại bỏ duplicate (nếu có):
``` python
df.isnull().sum()
df.duplicated().sum()
df.drop_duplicates(inplace=True)
```

### Tính khoảng cách giữa các điểm dữ liệu 

1. Khởi tạo các điểm point1, point2, point3 tương ứng là dòng 0, 1, 2 của array và tính chuẩn p
```python
array = df.values
print(array)
point1 = array[0,:]
point2 = array[1,:]
point3 = array[2,:]
```
2. Thực hiện tính chuẩn p theo công thức và in kết quả:
```python
#p=1
dist01_2 = np.linalg.norm(point1-point2, 1)
dist01_3 = np.linalg.norm(point1-point3, 1)
#p=2
dist1_2 = np.linalg.norm(point1-point2)
dist1_3 = np.linalg.norm(point1-point3)
#p=inf
dist11_2 = np.linalg.norm(point1-point2, np.inf)
dist11_3 = np.linalg.norm(point1-point3, np.inf)

#print results
print(dist1_2)
print(dist1_3)
print(dist01_2)
print(dist01_3)
print(dist11_2)
print(dist11_3)
```

3. Thực hiện tính chuẩn p = 1, 2, inf cho 50 dòng đầu tiên của array trong dataset 
```python
#Tạo hàm tính ma trận khoảng cách 
def distance_array_calc(array, n, p):
  distance_array = np.zeros([n,n]) #khởi tạo ma trận vuông cấp nxn
  for i in range(n): #duyệt qua từng hàng và cột của ma trận
    for j in range(n):
      distance_array[i, j] = np.linalg.norm(array[i, :] - array[j, :], p) #tính khoảng cách của từng hàng theo công thức 
  return distance_array
```

```python
#p=1
n = 50
p = 1
distance_array_calc(array, n, p)

#p=2
n = 50
p = 2
distance_array_calc(array, n, p)

#p=inf
n = 50
p = np.inf
distance_array_calc(array, n, p)
```

### Bài 2: Xử lý dữ liệu kddcup

### Data overview 
**Cấu trúc của tập dữ liệu KDD Cup 1999:**
- **Số lượng mẫu:** Khoảng 4.900.000 bản ghi, mỗi bản ghi đại diện cho một kết nối mạng riêng lẻ.
- **Số lượng thuộc tính:** Mỗi bản ghi có 41 đặc trưng (cột), bao gồm:​[
    1. **Thuộc tính cơ bản về kết nối:**
        - **duration:** Thời gian của kết nối (giây).
        - **protocol_type:** Loại giao thức (e.g., TCP, UDP).
        - **service:** Dịch vụ được yêu cầu (e.g., http, ftp).
        - **flag:** Trạng thái của kết nối.
    2. **Thuộc tính về nội dung:**
        - **src_bytes:** Số byte từ nguồn đến đích.
        - **dst_bytes:** Số byte từ đích đến nguồn.
    3. **Thuộc tính về lưu lượng trong khoảng thời gian:**
        - **count:** Số lượng kết nối đến cùng một đích trong khoảng thời gian nhất định.
        - **srv_count:** Số lượng kết nối đến cùng một dịch vụ trong khoảng thời gian nhất định.
- **Nhãn (label):** Mỗi bản ghi được gán nhãn là "normal" (bình thường) hoặc một trong các loại tấn công.​
### Data preprocessing
1. Lựa chọn và trích xuất dữ liệu phân loại trong dataset:
```python
categorical_columns = df2.select_dtypes(include=['object']).columns
print("Categorical attributes:", categorical_columns)
categorical_data = df2[categorical_columns]
print("Categorical Data:\n", categorical_data)
```
2. Kiểm tra giá trị trùng nhau và loại bỏ:
```python
#Kiếm tra giá trị giống nhau
print("So luong dong giong nhau: ", categorical_data.duplicated().sum())
##loại bỏ các dòng giống nhau
df2 = categorical_data.drop_duplicates()
print("Du lieu sau khi xoa nhung dong giong nhau: ", df2)
df2.shape
```
- Dữ liệu sau khi bỏ các giá trị giống nhau thì còn lại 609 dòng và 4 cột
### Tính K nearest neighbourhood sử dụng độ đo overlap và độ đo tần suất xuất hiện ngược

1. Xây dựng thuật toán tính độ tương đồng giữa các bản ghi sử dụng độ đo overlap: 
```python
n = 609 #tính độ tương đồng trên toàn bộ hàng của dataset
sim_matrix_overlap = np.zeros([n, n])
for i in range(n):
    for j in range(n):
        S = 0
        for k in range(df2.shape[1]):
            if df2.iloc[i, k] == df2.iloc[j, k]:
                S = S + 1/df2.shape[1]
        sim_matrix_overlap[i][j] = S

sim_matrix_overlap
```

- Kết quả:
![[Pasted image 20250331141811.png]]

2. Xây dựng thuật toán tính độ tương đồng giữa các bản ghi sử dụng độ đo tần suất xuất hiện ngược:
```python
from collections import Counter
n = 609
sim_matrix_inv_freq = np.zeros([n, n])

# Tính tần suất xuất hiện của từng giá trị trong mỗi cột
value_frequencies = []
for col in df2.columns:
    counts = Counter(df2[col])
    freqs = {val: count / len(df2) for val, count in counts.items()}
    value_frequencies.append(freqs)
 
# Tính ma trận độ tương đồng
for i in range(n):
    for j in range(n):
        S = 0
        for k in range(df2.shape[1]):
            x_i = df2.iloc[i, k]
            y_i = df2.iloc[j, k]
            
            if x_i == y_i:
                S += 1 / df2.shape[1]
            else:
                f_x = value_frequencies[k].get(x_i, 1e-10)  # Tránh lỗi log(0)
                f_y = value_frequencies[k].get(y_i, 1e-10)
                S += (1 / df2.shape[1]) * (1 / (1 + np.log(f_x) * np.log(f_y)))

        sim_matrix_inv_freq[i][j] = S

sim_matrix_inv_freq
```

- Kết quả:
![[Pasted image 20250331141949.png]]

3. Xây dựng hàm tìm k láng giềng gần nhất dựa trên độ tương đồng 
```python
def find_nearest_neighbors(sim_matrix, k):
    n = sim_matrix.shape[0]  # Số bản ghi
    nearest_neighbors = {}

    for i in range(n):
        # Lấy danh sách độ tương đồng và sắp xếp giảm dần
        sorted_neighbors = np.argsort(sim_matrix[i])[::-1]
        # Bỏ qua chính bản thân nó (index i)
        nearest_neighbors[i] = sorted_neighbors[1:k+1]

    return nearest_neighbors
```

4. Chạy thử với 5 láng giềng gần nhất
```python
# Sử dụng hàm
k = 5
nearest_neighbors = find_nearest_neighbors(sim_matrix_overlap, k)
  
# In danh sách k láng giềng gần nhất
print("tìm " + str(k) + " láng giềng gần nhất sử dụng độ đo overlap")
for key, value in nearest_neighbors.items():
    print(f"Hàng {key}: Láng giềng gần nhất {value}")
```

- Kết quả: 
![[Pasted image 20250331142138.png]]
