**Họ và tên**: Mai Phong Đăng
**Mssv**: 22280008
**Lớp**: 22KDL

# Data Mining Lab2 Report

## Bài 1: Xử lý dữ liệu ionosphere 

### Data Overview

- Data có 35 cột với 34 đặc trưng với các giá trị số đại diện cho tín hiệu của radar, cột cuối cùng là nhãn ("label") với hai giá trị:
	- - `"g"` (good) - tín hiệu phản xạ có thể dùng để phân biệt đối tượng.
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
- **Số lượng thuộc tính:** Mỗi bản ghi có 41 thuộc tính, bao gồm:​[
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