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
- Khác với K-Means, K-Medians cập nhật medoids bằng cách chọn điểm thực tế trong mỗi cụm sao cho tổng khoảng cách Manhattan trong cụm là nhỏ nhất:
```python
def update_medoids(dset, assignments, k):
    """
    Cập nhật medoids. Medoid mới của một cụm là điểm trong cụm đó
    mà tổng khoảng cách Manhattan đến tất cả các điểm khác trong cùng cụm là nhỏ nhất.
    """
    new_medoids_list = []
    feature_cols = dset.columns.tolist()
    
    for i in range(k): # Với mỗi cụm i
        # Lấy các điểm thuộc cụm i
        cluster_points_df = dset[assignments == i]

        if cluster_points_df.empty:
            print(f"Cảnh báo: Cụm {i} rỗng. Chọn medoid ngẫu nhiên.")
            random_point_for_empty_cluster = dset.sample(1)
            new_medoids_list.append(random_point_for_empty_cluster.iloc[0])
            continue

        min_sum_intra_cluster_dist = float('inf')
        current_medoid_for_cluster = None

        # Duyệt qua từng điểm 'p' trong cụm hiện tại để tìm medoid mới
        cluster_points_values = cluster_points_df.values
        
        for p_idx in range(cluster_points_values.shape[0]):
            point_p_values = cluster_points_values[p_idx, :]
            current_sum_dist = 0
            # Tính tổng khoảng cách từ point_p_values đến tất cả các điểm khác trong cùng cụm
            for other_p_idx in range(cluster_points_values.shape[0]):
                if p_idx == other_p_idx:
                    continue
                other_point_values = cluster_points_values[other_p_idx, :]
                current_sum_dist += kmed_rsserr(point_p_values, other_point_values)
            
            if current_sum_dist < min_sum_intra_cluster_dist:
                min_sum_intra_cluster_dist = current_sum_dist
                current_medoid_for_cluster = cluster_points_df.iloc[p_idx] 
        
        if current_medoid_for_cluster is not None:
            new_medoids_list.append(current_medoid_for_cluster)
        elif not cluster_points_df.empty:
             new_medoids_list.append(cluster_points_df.iloc[0])

    if not new_medoids_list:
        print("Lỗi: Không thể tạo medoid mới.")
        return pd.DataFrame(columns=feature_cols)

    new_medoids_df = pd.DataFrame(new_medoids_list)
    if not new_medoids_df.empty:
        new_medoids_df = new_medoids_df[feature_cols]
    return new_medoids_df.reset_index(drop=True)
```
# References
