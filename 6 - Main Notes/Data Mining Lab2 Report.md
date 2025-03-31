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
