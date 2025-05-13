2025-05-13 15:14


Tags:

# Data_Mining_Lab6_Report

**Họ và Tên**: Mai Phong Đăng
**MSSV**: 22280008
**Lớp**: 22KDL

## Thuật Toán K-means và K-meadian
### **K-means**
- Đọc và Khám phá dữ liệu: 
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
#reading the dataset
blobs = pd.read_csv('data.csv')
colnames = list(blobs.columns[1:-1])
print(blobs.head())
```
- trực quan hóa: 
```python
customcmap = ListedColormap(['crimson', 'mediumblue', 'darkmagenta'])

fig,ax = plt.subplots(figsize=(8, 6))
plt.scatter(x=blobs['x'], y=blobs['y'], s=150,
            c=blobs['cluster'].astype('category'),
            cmap=customcmap)
ax.set_xlabel(r'x', fontsize=14)
ax.set_ylabel(r'y', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.show()
```
- Bước 1: Khởi tạo tâm cụm ngẫu nhiên
```python
customcmap = ListedColormap(['crimson', 'mediumblue', 'darkmagenta'])
fig,ax = plt.subplots(figsize=(8, 6))
plt.scatter(x=blobs['x'], y=blobs['y'], s=150,
            c=blobs['cluster'].astype('category'),
            cmap=customcmap)
ax.set_xlabel(r'x', fontsize=14)
ax.set_ylabel(r'y', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.show()
```

- Bước 2: tính toán khoảng cách Euclidean
```python
def rsserr(a,b):
    '''
    Calculate the root sum squared error
    a and b are numpy arrays
    '''
    return (np.sum(np.square(a-b)))
```
- Bước 3: Gán điểm dữ liệu cho cụm gần nhất:
```python
def rsserr(a,b):
    '''
    Calculate the root sum squared error
    a and b are numpy arrays
    '''
    return (np.sum(np.square(a-b)))
```

- Bước 4: Cập nhật tâm cụm
```python
centroids = df.groupby('centroid').agg('mean').loc[:, colnames].reset_index(drop = True)
```
- Bước 5: hoàn thiện thuật toán
```python
def kmeans(dset, k=2, tol=1e-4):
    # Work in a copy 
    working_dset = dset.copy()
    # Define some variables to hold the error, the
    # stopping signal and a counter for the iterations
    err = []
    goahead = True
    j = 0

    # Step 2: Inititate clusters by defining centroids
    centroids = initiate_centroids(k, working_dset)

    while(goahead):
        # Step 3 and 4: Assign centroids and calc error
        working_dset['centroid'], j_err = centroid_assignation(working_dset, centroids)
        err.append(sum(j_err))
        # Step 5: update centoids position
        centroids = working_dset.groupby('centroid').agg('mean').reset_index(drop = True)

        # Step 6: Restart iteration
        if j > 0:
            # Is the error less than a tolerance (1e-4))
            if err[j-1]-err[j] < tol:
                goahead = False
        j+=1
    return working_dset['centroid'], j_err, centroids
```

- Tìm số cụm tối ưu bằng Elbow plot:
```python
err_total = []
n = 10
df_elbow = blobs[['x', 'y']]
for i in range(n):
    _, my_err, _ = kmeans(df_elbow, i+1)
    err_total.append(sum(my_err))
fig, ax = plt.subplots(figsize=(8, 6))
plt.plot(range(1, n+1), err_total, linewidth=3, marker = 'o')
ax.set_xlabel(r'Number of clusters', fontsize=14)
ax.set_ylabel(r'Total error', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.show()
```

### **K-Medians** 
- K-Medians là một biến thể của K-Means nhưng sử dụng khoảng cách Manhattan thay vì Euclidean và chọn medoid (điểm thực tế trong dữ liệu) thay vì centroids.
- *Bước 1: Khởi tạo Medoids*
```python
def initiate_medoids(k, dset):
    '''
    Select k data points as medoids 
    k: number of medoids
    dset: pandas dataframe
    '''
    medoids = dset.sample(k)
    return medoids
```
- *Bước 2: Tính khoảng cách Manhattan*
```python
def kmed_rsserr(point1, point2):
    """Tính khoảng cách Manhattan giữa hai điểm."""
    return np.sum(np.abs(point1 - point2))
```
- *Bước 3: Gán điểm dữ liệu cho Medoids gần nhất*
```python
def assign_to_medoids(dset, medoids_df):
    """
    Gán mỗi điểm trong dset cho medoid gần nhất dựa trên khoảng cách Manhattan.
    """
    num_obs = dset.shape[0]
    num_medoids = medoids_df.shape[0]
    
    assignments = np.zeros(num_obs, dtype=int)
    assignment_errors = np.zeros(num_obs)

    # Chuyển sang numpy arrays để tăng tốc độ
    dset_values = dset.values
    medoids_values = medoids_df.values

    for i in range(num_obs):
        current_point = dset_values[i, :]
        distances_to_medoids = np.zeros(num_medoids)
        for j in range(num_medoids):
            distances_to_medoids[j] = kmed_rsserr(current_point, medoids_values[j, :])
        
        assignments[i] = np.argmin(distances_to_medoids)
        assignment_errors[i] = np.min(distances_to_medoids)
        
    return assignments, assignment_errors
```
- *Bước 4: Cập nhật medoids*
- Cập nhật medoids bằng cách tính giá trị trung vị cho từng thành phần (chiều) riêng biệt.

```python

def update_medoids(dset, assignments, k):
    """
    dset: DataFrame chứa dữ liệu (chỉ các cột đặc trưng).
    assignments: Mảng chứa chỉ số cụm được gán cho mỗi điểm.
    k: Số lượng cụm (medoids).
    """
    new_medoids_list = []
    feature_cols = dset.columns.tolist()
    
    for i in range(k):  # Với mỗi cụm i
        # Lấy các điểm thuộc cụm i
        cluster_points_df = dset[assignments == i]
        
        if cluster_points_df.empty:
            # Nếu cụm rỗng, chọn một điểm ngẫu nhiên
            print(f"Cảnh báo: Cụm {i} rỗng. Chọn medoid ngẫu nhiên.")
            random_point = dset.sample(1)
            new_medoids_list.append(random_point.iloc[0])
            continue
            
        # Tạo một dict để lưu các giá trị trung vị cho từng thành phần
        medoid_components = {}
        
        # Tính giá trị trung vị cho từng thành phần (chiều)
        for feature in feature_cols:
            medoid_components[feature] = cluster_points_df[feature].median()
        
        # Tạo medoid mới từ các giá trị trung vị đã tính
        new_medoid = pd.Series(medoid_components)
        new_medoids_list.append(new_medoid)
    
    # Tạo DataFrame từ danh sách các medoid mới
    new_medoids_df = pd.DataFrame(new_medoids_list)
    
    # Đảm bảo các cột được giữ lại và đúng thứ tự
    if not new_medoids_df.empty:
        new_medoids_df = new_medoids_df[feature_cols]
    
    return new_medoids_df.reset_index(drop=True)
```
- Bước 5: hoàn thiện thuật toán
```python
def kmedians(dset_features, k, tol=1e-4, max_iter=100):
    """
    Thuật toán K-Medians.
    """
    # Khởi tạo medoids
    current_medoids = initiate_centroids(k, dset_features) 
    
    error_history = []
    
    for iteration in range(max_iter):
        # Gán các điểm cho medoid gần nhất
        assignments, assignment_errors = assign_to_medoids(dset_features, current_medoids)
        
        total_error = np.sum(assignment_errors)
        error_history.append(total_error)
        
        # Cập nhật medoids
        new_medoids = update_medoids(dset_features, assignments, k)

        if new_medoids.empty or new_medoids.shape[0] < k :
            print(f"Lỗi ở vòng lặp {iteration}: Không đủ medoid được tạo ra. Dừng thuật toán.")
            break
        
        # Kiểm tra sự hội tụ
        if current_medoids.equals(new_medoids):
            print(f"Hội tụ ở vòng lặp {iteration+1} do medoids không thay đổi.")
            break
        
        current_medoids = new_medoids
        
        if iteration > 0:
            if abs(error_history[iteration-1] - error_history[iteration]) < tol:
                print(f"Hội tụ ở vòng lặp {iteration+1} do thay đổi lỗi nhỏ hơn dung sai.")
                break
        
        if iteration == max_iter - 1:
            print("Đạt số vòng lặp tối đa.")
            
    final_assignments, final_errors = assign_to_medoids(dset_features, current_medoids)
    return final_assignments, final_errors, current_medoids, error_history
```

## Kết quả và so sánh

Cả K-Means và K-Medians đều có khả năng phân cụm tốt cho tập dữ liệu này, tuy nhiên có một số khác biệt cơ bản:
1. **Độ đo khoảng cách**:
    - K-Means sử dụng khoảng cách Euclidean (bình phương)
    - K-Medians sử dụng khoảng cách Manhattan (tổng giá trị tuyệt đối)
2. **Cập nhật tâm cụm**:
    - K-Means sử dụng trung bình các điểm (centroids có thể không phải là điểm thực tế trong dữ liệu)
    - K-Medians sử dụng điểm thực tế trong dữ liệu (medoid)
3. **Độ nhạy với outlier**:
    - K-Means nhạy hơn với các điểm ngoại lai do sử dụng bình phương khoảng cách
    - K-Medians ít nhạy cảm hơn với các điểm ngoại lai
Trực quan kết quả cho thấy cả hai thuật toán đều có thể phân tách 3 nhóm dữ liệu một cách hiệu quả, với vài khác biệt nhỏ về biên của các cụm.
![[Pasted image 20250513153737.png]]
![[Pasted image 20250513153755.png]]

# References
