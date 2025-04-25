2025-04-25 16:09


Tags:

# Data_Mining_Lab5_report

## Tóm tắt code của thuật toán Vertical Apriori

### **Mục tiêu**

- Hàm `vertical_apriori()` là một triển khai thuật toán Apriori theo hướng tiếp cận **vertical format** – tức là thay vì duyệt từng dòng giao dịch, ta theo dõi các **danh sách ID giao dịch (TID list)** tương ứng với từng item hoặc itemset. Việc xử lý và tính toán hỗ trợ thông qua phép giao tập của các TID giúp tăng hiệu quả, đặc biệt trên dữ liệu thưa (sparse).

### **Tóm tắt**

#### Bước 1: **Chuyển đổi dữ liệu đầu vào**
- Chuyển từ `DataFrame` nhị phân sang dạng từ điển `{transaction_id: set(items)}`.
```python
tid_database = {}
for tid, row in transactions.iterrows():
    items_in_transaction = set(row.index[row == 1])
    if items_in_transaction:  # Chỉ thêm nếu không rỗng
        tid_database[tid] = items_in_transaction
```

#### Bước 2: **Tìm tập mục đơn phổ biến (1-itemsets)**
- Với mỗi item, ta tạo danh sách các giao dịch mà item đó xuất hiện:
```python
item_tids = {}
for item in transactions.columns:
    item_tids[frozenset([item])] = {
        tid for tid, items in tid_database.items() if item in items
}
```
- Sau đó, lọc ra các item có độ hỗ trợ thỏa điều kiện:
```python
F1 = {itemset: tid_list for itemset, tid_list in item_tids.items()
      if len(tid_list) >= abs_min_sup}
```

#### Bước 3: **Lặp để tìm các tập mục phổ biến cấp cao hơn (k-itemsets)**

- Ta sử dụng vòng lặp chính để kết hợp các tập phổ biến hiện tại nhằm tạo các ứng viên mới:
```python
while Fk:
    ...
    for i in range(len(Fk_items)):
        for j in range(i+1, len(Fk_items)):
            itemset1 = set(Fk_items[i])
            itemset2 = set(Fk_items[j])
            if len(itemset1.union(itemset2)) == k:
                candidate = frozenset(itemset1.union(itemset2))

                # Kiểm tra downward closure - nếu bất kỳ tập con nào không phổ biến thì loại
                for subset in combinations(candidate, k-1):
                    if frozenset(subset) not in Fk:
                        should_prune = True
                        break
                        
                if not should_prune:
                    # Giao TID list để tính hỗ trợ
                    tid_list1 = Fk[frozenset(itemset1)]
                    tid_list2 = Fk[frozenset(itemset2)]
                    Ck[candidate] = tid_list1.intersection(tid_list2)

```
- Cuối mỗi vòng, ta lọc ra các ứng viên đủ điều kiện hỗ trợ:
```python
Fk = {itemset: tid_list for itemset, tid_list in Ck.items()
      if len(tid_list) >= abs_min_sup}
```

#### Bước 4: **Trả về kết quả dạng `{itemset: support}`**

- Sau khi thu được tất cả các tập phổ biến, ta tính lại độ hỗ trợ (support) tương đối:
```python
result = {}
for itemset, tid_list in all_frequent_itemsets.items():
    support = len(tid_list) / n_transactions
    item_str = ' & '.join(sorted(itemset)) if len(itemset) > 1 else next(iter(itemset))
    result[item_str] = support
```
# References
