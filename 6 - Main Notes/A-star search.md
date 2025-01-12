2025-01-13 01:41


Tags: [[informed search]], [[Basic Search Algorithms in Artificial Intelligence]], [[search algorithm]], 

# A-star search
#### Ý tưởng:
- Tránh việc xét các nhánh tìm kiếm đã xác định (cho đến thời điểm hiện tại) là có chi phí cao.
- sử dụng hàm đánh giá *f(n) = g(n) + h(n)*
- g(n) = chi phí từ node gốc đến node hiện tại
- h(n) = chi phí ước lượng từ node hiện tại đến đích (có thể là đường chim bay)
- f(n) = chi phí tổng thể ước lượng của đường đi qua nút hiện tại n đến đích
#### A* Ví dụ:
![[Pasted image 20250113014346.png]]
![[Pasted image 20250113014353.png]]
![[Pasted image 20250113014359.png]]
![[Pasted image 20250113014407.png]]
![[Pasted image 20250113014421.png]]
![[Pasted image 20250113014432.png]]


# References
