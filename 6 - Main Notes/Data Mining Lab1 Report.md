**Họ và Tên**: Mai Phong Đăng
**MSSV**: 22280008
**Lớp**: 22KDL

# Data Mining Lab1 Report

## Bài 1: Xử lý dữ liệu nhân viên

### Dataset Overview

- Dataset chứa thông tin về nhân viên bao gồm: ID, First Name, Last Name, Age, Gender, Department, Salary và Date of Joining
- Dữ liệu được đọc từ file CSV với delimiter là ';'
 ```python
df = pd.read_csv("/content/data.csv", delimiter=';')
df.head(5)
```

### Data Preprocessing

1. Xử lý missing values:

- Phát hiện và điền giá trị null trong cột Age và Salary bằng mean của mỗi cột
```python
print(df.isnull().sum())

df['Age'].fillna(df['Age'].mean(), inplace=True)
df['Salary'].fillna(df['Salary'].mean(), inplace=True)
print(df)
```
- Kiểm tra và xóa các bản ghi trùng lặp
```python
print(df.duplicated().sum())

df=df.drop_duplicates()
print(df)
```
2. Encoding categorical variables:

- Thực hiện one-hot encoding cho các biến categorical (Gender, Department)
```python
df=pd.get_dummies(df, columns=['Gender','Department'])
print(df)
```
- Chuyển đổi Date of Joining thành các features mới: month và day_of_week
```python
df['Date of Joining']=pd.to_datetime(df['Date of Joining'])
df['month']=df['Date of Joining'].dt.month
df['day_of_week']=df['Date of Joining'].dt.day_name()
df=df.drop('Date of Joining', axis=1)
print(df)
```
3. Data Normalization/Scaling:

- Áp dụng RobustScaler để xử lý outliers
```python
#Sử dụng RobustScaler() để loại bỏ những giá trị ngoại lai
scaler = preprocessing.RobustScaler()
robust_df = scaler.fit_transform(array)
robust_df = pd.DataFrame(robust_df)
```
- Chuẩn hóa dữ liệu bằng StandardScaler
```python
#Chuẩn hóa dữ liệu bằng phương pháp z-score (Standard)
scaler = preprocessing.StandardScaler()
standard = scaler.fit_transform(array)
standard_df = pd.DataFrame(robust_df)
print('Chuan hoa du lieu:\n', standard_df)
```
- Scale dữ liệu bằng MinMaxScaler
```python
#Scale dữ liệu bằng phương pháp minmax
scaler = preprocessing.MinMaxScaler()
minmax = scaler.fit_transform(array)
minmax_df = pd.DataFrame(minmax, index = df.index)
print('Scaling dữ liệu:\n', minmax_df)
```
4. Data Discretization:

- Thực hiện equal-width binning với 10 bins cho cột đầu tiên
```python
#10 equi-width ranges với cột đầu tiên của standard_df
df2=standard_df.copy()
df['equi-width_column0'] = pd.cut(x=df2[0], bins=10)
print('Roi rac hoa cot 0 bang 10 equi-width ranges:\n', df2)
```
- Thực hiện equal-depth binning với 10 bins cho cột đầu tiên
```python
#10 equi-depth ranges với cột đầu tiên của standard_df
df3=standard_df.copy()
df3['equi-depth column0'] = pd.qcut(x=df3[0], q=10)
print('Roi rac hoa cot 0 bang 10 equi-depth ranges:\n', df3)
```
## Bài 2: Xử lý dữ liệu Arrhythmia

### Dataset Overview

- Dataset về bệnh loạn nhịp tim với 279 thuộc tính

- Dữ liệu được đọc từ file arrhythmia.data
```python
df_bai2 = pd.read_csv("/content/arrhythmia.data", delimiter=',', header=None)
print(df_bai2)
```
### Data Preprocessing

1. Xử lý missing values:

- Phát hiện các giá trị "?" trong dataset
```python
# Bởi vì trong file .names có đề cặp rằng các giá trị null sẽ có value là "?"
# nên ta sẽ kiểm tra xem liệu rằng trong dataset có value nào là "?" hay không
for column in df_bai2.columns:
  if df_bai2[column].dtype == object:  
    count = df_bai2[column].str.count("\?").sum()
    if count > 0:
      print(f"Column '{column}' contains {count} '?' values.")
```

- Loại bỏ cột có quá nhiều giá trị missing (cột 13)
```python
df_bai2 = df_bai2.drop(df_bai2.columns[13], axis=1)
```
- Thay thế các giá trị "?" bằng mean của mỗi cột
```python
for column in df_bai2.columns:
    df_bai2[column] = df_bai2[column].replace('?', np.nan)
    df_bai2[column] = pd.to_numeric(df_bai2[column], errors='coerce')
    df_bai2[column].fillna(df_bai2[column].mean(), inplace=True)
```
- Kiểm tra xem trong dataset có biến categorical nào không
```python
# Kiểm tra xem trong df_bai2 có biến categorical hay không
categorical_features = df_bai2.select_dtypes(include=['object']).columns
if len(categorical_features) > 0:
  print("Các biến categorical trong df_bai2:")
  print(categorical_features)
else:
  print("Không có biến categorical trong df_bai2.")
```
2. Data Normalization/Scaling:

- Scale dữ liệu bằng MinMaxScaler
```python
#Chuản hóa dữ liệu bằng minmaxScaler
scaler = preprocessing.MinMaxScaler()
minmax = scaler.fit_transform(df_bai2)
minmax_df = pd.DataFrame(minmax, index = df_bai2.index)
print('Scaling dữ liệu:\n', minmax_df)
```
3. Data Discretization:

- Thực hiện equal-width binning với 10 bins cho tất cả các cột số hóa
```python
# Lặp qua các cột có giá trị số hóa trong DataFrame
df_b2_discretized1=df_bai2.copy()
for column in df_b2_discretized1.select_dtypes(include=np.number).columns:
  # Tạo 10 equi-width ranges cho cột hiện tại
  df_b2_discretized1[f'equi-width_{column}'] = pd.cut(x=df_b2_discretized1[column], bins=10)
print('Roi rac hoa cac cot co gia tri so hoa bang 10 equi-width range:\n',df_b2_discretized1)
```
- Thực hiện equal-depth binning với 10 bins cho tất cả các cột số hóa
```python
# Lặp qua các cột có giá trị số hóa trong DataFrame
df_b2_discretized2 = df_bai2.copy()
for column in df_b2_discretized2.select_dtypes(include=np.number).columns:
  # Tạo 10 equi-depth ranges cho cột hiện tại
  df_b2_discretized2[f'equi-depth_{column}'] = pd.qcut(x=df_b2_discretized2[column], q=10, duplicates='drop')
print('Roi rac hoa cac cot co gia tri so hoa bang 10 equi-depth range:\n', df_b2_discretized2)
```

## Bài 3: Phân tích PCA trên dữ liệu Musk

### Dataset Overview

- Dataset về phân loại mùi xạ hương
```python
muskv2_df = pd.read_csv("/content/clean2.data", delimiter=',')
```
- Loại bỏ các biến categorical và tạo biến target
```python
#tạo cột target từ dataset và drop các cột có index là 0 1 2
#bởi vì các cột này là biến categorical
muskv2_df['target'] = muskv2_df.iloc[:, 0]
muskv2_df = muskv2_df.drop(muskv2_df.columns[[0, 1, 2]], axis=1)
muskv2_df
```
### Data Preprocessing

1. Data Preparation:

- Kiểm tra và xóa duplicates trong dataset
```python 
print(muskv2_df.duplicated().sum())
muskv2_df = muskv2_df.drop_duplicates()
muskv2_df
```

- Tạo X để chuẩn bị đầu vào cho PCA
```python
# tạo biến X để chuẩn bị data processing cho quá trình pca
Y = muskv2_df['target']
X = muskv2_df.drop(columns=['target'])
X
```

- Chuyển đổi biến target thành dạng numeric (0/1)
```python
# tạo cột Y_numeric để chứa numerical value của Y
Y_numeric = np.where(Y.str.contains('NON-MUSK'), 0, 1)
Y_numeric
Y = pd.DataFrame(Y_numeric, columns=['target'])
Y
```

- Kiểm tra các giá trị null và sự tồn tại của các biến categorical trong X
```python
# Kiểm tra xem có giá trị null trong dataset hay không,
# nếu có sẽ trả về true và không có sẽ trả về false
print(X.isnull().values.any())

# Kiểm tra xem trong X có biến categorical hay không
categorical_features = X.select_dtypes(include=['object']).columns
if len(categorical_features) > 0:
  print("Các biến categorical trong X:")
  print(categorical_features)
else:
  print("Không có biến categorical trong X.")
```
- Chuẩn hóa dữ liệu bằng StandardScaler
```python 
# Chuẩn hóa dữ liệu bằng StandardScaler
scaler  = preprocessing.StandardScaler()
X = scaler.fit_transform(X)
Y = scaler.fit_transform(Y)
X = pd.DataFrame(X) #cần trả lại dữ liệu trong X về dataframe bởi vì scaler.fit_transform(X) sẽ trả về mảng numpy
Y = pd.DataFrame(Y)
print(X)
print("\n",Y)
```
### PCA Analysis

1. Thực hiện PCA:

- Tiến hành khởi tạo PCA và vẽ biểu đồ tỉ lệ phương sai tích lũy
```python
# Import thư viện và tiến hành pca
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np

pca = PCA()
pca.fit(X)

# Vẽ biểu đồ tỉ lệ phương sai tích lũy
plt.figure(figsize=(10, 6))
plt.plot(np.cumsum(pca.explained_variance_ratio_), marker='o')
plt.xlabel('Số lượng thành phần')
plt.ylabel('Phương sai tích lũy')
plt.axhline(y=0.95, color='r', linestyle='--')
plt.grid()
plt.show()

# Chọn số lượng thành phần dựa trên ngưỡng phương sai (ví dụ: 95%)
n_components = np.argmax(np.cumsum(pca.explained_variance_ratio_) >= 0.95) + 1
print(f"Số lượng thành phần cần thiết để giữ lại 95% phương sai: {n_components}")
```

- Xác định số lượng components cần thiết để giữ 95% phương sai (39 components)
![[Pasted image 20250326134856.png]]
- Trích xuất eigenvalues và eigenvectors
```python
# Lấy ra trị riêng và vector riêng
eigenvalues = pca.explained_variance_
eigenvectors = pca.components_
  
print("Eigenvalues:\n", eigenvalues)
print("\nEigenvectors:\n", eigenvectors)
```
![[Pasted image 20250326134921.png]]
1. Visualization:

- Giảm chiều dữ liệu xuống 3D sử dụng UMAP
```python
# Plotting PCA trên 3d plane
# Bước 1: PCA xuống 39 thành phần
pca = PCA(n_components=39)
X_pca = pca.fit_transform(X)

# Bước 2: Giảm tiếp xuống 3 chiều bằng UMAP
import umap
X_embedded = umap.UMAP(n_components=3).fit_transform(X_pca)
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection="3d")

# Vẽ scatter plot
scatter = ax.scatter(
    X_embedded[:, 0], X_embedded[:, 1], X_embedded[:, 2],
    c=Y, cmap='viridis', s=40
)

ax.set_title("Musk Dataset - 3D Visualization")
ax.set_xlabel("Dimension 1")
ax.set_ylabel("Dimension 2")
ax.set_zlabel("Dimension 3")

# Thêm legend
legend1 = ax.legend(
    *scatter.legend_elements(),
    loc="upper right",
    title="Classes"
)
ax.add_artist(legend1)
plt.show()
```
- Vẽ scatter plot 3D để hiển thị kết quả phân cụm
![[Pasted image 20250326135113.png]]

### Kết luận

- Các phương pháp xử lý dữ liệu đã được áp dụng thành công

- PCA giúp giảm chiều dữ liệu hiệu quả trong khi vẫn giữ được thông tin quan trọng

- Visualization 3D cho thấy sự phân tách rõ ràng giữa các classes