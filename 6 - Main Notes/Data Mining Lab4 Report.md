2025-04-19 21:49


Tags: [[Data_Mining_Lab3_Report]], [[Data Mining Lab2 Report]], [[Data Mining Lab1 Report]]

**Họ và Tên**: Mai Phong Đăng
**MSSV**: 22280008
**Lớp**: 22KDL

# Data Mining Lab4 Report

## Thuật toán Apriori
- Thực hiện thuật toán Apriori để tìm các **tập mục thường xuyên (frequent itemsets)** trong một tập dữ liệu giao dịch. Mục tiêu là xác định các tập hợp mặt hàng (items) xuất hiện thường xuyên cùng nhau, nhằm phục vụ cho các bài toán phân tích như phân loại, gợi ý sản phẩm, hoặc khai phá luật kết hợp.
### Các bước thực hiện:
1. **Chuẩn bị dữ liệu:** 
- Đọc dữ liệu từ một DataFrame (`df`), sau đó duyệt từng dòng (transaction).    
- Với mỗi dòng, loại bỏ các giá trị `NaN` và chuyển đổi thành tập hợp các item, rồi đưa vào danh sách `transactions`.
```python 
import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
from collections import Counter
#Load dữ liệu
df = pd.read_csv('/content/dataW4.csv', header=None)
print(df)

transactions = []
for i in range(len(df)):
transaction = df.iloc[i].dropna().tolist()
transactions.append(set(transaction))
```

2. **Cài đặt thuật toán Apriori**
- Tìm tập 1-itemset xuất hiện thường xuên
# References
