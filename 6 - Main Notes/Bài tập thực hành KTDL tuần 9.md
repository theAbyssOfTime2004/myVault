
## Mai Phong Đăng_22280008


### 1. Tải và khám phá dữ liệu
- Sử dụng thư viện `ucimlrepo` để tải bộ dữ liệu Banknote Authentication từ UCI Machine Learning Repository:

```python
from ucimlrepo import fetch_ucirepo

# fetch dataset

banknote_authentication = fetch_ucirepo(id=267)

# data (as pandas dataframes)

X = banknote_authentication.data.features

y = banknote_authentication.data.targets

# metadata

print(banknote_authentication.metadata)

# variable information

print(banknote_authentication.variables)
```
- kiểm tra thông tin tổng quan và mô tả thống kê của dữ liệu:
```python
x.info()
x.describe()
```

### 2. Giảm chiều và trực quan hóa dữ liệu
- Sử dụng PCA giảm chiều xuống 2D
```python
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

plt.figure(figsize=(8,6))
plt.scatter(X_pca[:,0], X_pca[:,1], c=y.values.ravel(), cmap='autumn', alpha=0.7)
plt.title('PCA - Banknote Authentication')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.show()
```
- *Nhận xét:* Quan sát scatter plot cho thấy hai lớp dữ liệu khá tách biệt trên mặt phẳng 2D.
	- ![[Pasted image 20250607135547.png]]
### 3. Kiểm tra tính phân tách tuyến tính bằng Logistic Regression
- Huấn luyện mô hình Logistic Regression trên toàn bộ dữ liệu và đánh giá độ chính xác:
```python
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

clf = LogisticRegression()
clf.fit(X, y.values.ravel())
y_pred = clf.predict(X)
acc = accuracy_score(y, y_pred)
print(f'Accuracy của Logistic Regression trên toàn bộ tập dữ liệu: {acc:.4f}')
```
- *Nhận xét:* Độ chính xác rất cao (~1.0), cho thấy dữ liệu gần như phân tách tuyến tính.
### 4. Vẽ các đường phân tách và marker minh họa 
```python
import numpy as np

plt.figure(figsize=(8,6))
plt.scatter(X_pca[y.values.ravel()==0,0], X_pca[y.values.ravel()==0,1], color='yellow', label='Class 0')
plt.scatter(X_pca[y.values.ravel()==1,0], X_pca[y.values.ravel()==1,1], color='red', label='Class 1')

x_vals = np.linspace(X_pca[:,0].min()-0.5, X_pca[:,0].max()+0.5, 100)
plt.plot(x_vals, 2.5 - 0.5*x_vals, 'k')   # Đường thẳng 1
plt.plot(x_vals, 1 + 0.5*x_vals, 'k')     # Đường thẳng 2
plt.plot(x_vals, 3 - x_vals, 'k')         # Đường thẳng 3

plt.scatter([0.7], [2], color='red', marker='x', s=150, linewidths=3)

plt.xlabel('PC1')
plt.ylabel('PC2')
plt.xlim(X_pca[:,0].min()-0.5, X_pca[:,0].max()+0.5)
plt.ylim(X_pca[:,1].min()-0.5, X_pca[:,1].max()+0.5)
plt.grid(True)
plt.show()
```
- *Nhận xét:* Các đường thẳng minh họa khả năng phân tách tuyến tính giữa hai lớp.
### 5. Trực quan hóa dữ liệu trong không gian 3 chiều
- Sử dụng PCA để giảm chiều dữ liệu xuống 3D và trực quan hóa:
```python
pca3 = PCA(n_components=3)
X_pca3 = pca3.fit_transform(X)
y_arr = y.values.ravel()

fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(X_pca3[y_arr==0,0], X_pca3[y_arr==0,1], X_pca3[y_arr==0,2], 
           color='yellow', label='Class 0', alpha=0.7)
ax.scatter(X_pca3[y_arr==1,0], X_pca3[y_arr==1,1], X_pca3[y_arr==1,2], 
           color='red', label='Class 1', alpha=0.7)

ax.set_xlabel('PC1')
ax.set_ylabel('PC2')
ax.set_zlabel('PC3')
ax.set_title('PCA 3D - Banknote Authentication')
ax.legend()
plt.show()
```
- *Nhận xét:* Hai lớp dữ liệu vẫn tách biệt rõ ràng trong không gian 3 chiều.
	- ![[Pasted image 20250607140123.png]]
### 6. Fitting SVM và vẽ decision boundary
- Huấn luyện SVM tuyến tính trên dữ liệu đã PCA và vẽ đường phân tách:
```python
from sklearn.svm import SVC

model = SVC(kernel='linear', C=1E10)
model.fit(X_pca, y_arr)

def plot_svc_decision_function(model, ax=None, plot_support=True):
    if ax is None:
        ax = plt.gca()
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    x = np.linspace(xlim[0], xlim[1], 30)
    y = np.linspace(ylim[0], ylim[1], 30)
    Y, X = np.meshgrid(y, x)
    xy = np.vstack([X.ravel(), Y.ravel()]).T
    P = model.decision_function(xy).reshape(X.shape)
    ax.contour(X, Y, P, colors='k',
               levels=[-1, 0, 1], alpha=0.5,
               linestyles=['--', '-', '--'])
    if plot_support:
        ax.scatter(model.support_vectors_[:, 0],
                   model.support_vectors_[:, 1],
                   s=300, linewidth=1, edgecolors='black',
                   facecolors='none')
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

plt.figure(figsize=(8,6))
plt.scatter(X_pca[y_arr==0,0], X_pca[y_arr==0,1], color='yellow', label='Class 0')
plt.scatter(X_pca[y_arr==1,0], X_pca[y_arr==1,1], color='red', label='Class 1')
plot_svc_decision_function(model)
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.legend()
plt.show()
```
- ![[Pasted image 20250607140156.png]]

### Kết Luận:
- Dữ liệu Banknote Authentication gần như **linearly separable**.
- Các mô hình tuyến tính như Logistic Regression và SVM đều đạt độ chính xác rất cao.
- Trực quan hóa bằng PCA 2D và 3D cho thấy hai lớp dữ liệu tách biệt rõ ràng.
# References
