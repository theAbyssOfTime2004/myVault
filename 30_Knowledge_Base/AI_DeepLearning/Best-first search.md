2025-01-13 01:33


Tags: [[informed search]], [[search algorithm]], [[Basic Search Algorithms in Artificial Intelligence]], [[beginner]]

# Best-first search
#### Ý tưởng: 
- Sử dụng hàm *đánh giá f(n)* cho mỗi node của cây tìm kiếm
	- để đánh giá mức độ "phù hợp" của node đó
	=> trong quá trình tìm kiếm, ưu tiên xét các node có mức độ phù hợp cao nhất
#### Cài đặt
- Sắp thứ tự các node trong cấu trúc fringe theo trật tự giảm dần về mức độ phù hợp
#### Các trường hợp đặc biệt của Best-first search:
- GBFS
- A* search
#### GBFS:
- hàm đánh giá *f(n)* là hàm *heuristic h(n)*
- hàm heuristic *h(n)* đánh giá cost để đi từ node hiện tại *n* đến node goal
- Ví dụ: Trong bài toán tìm đường đi từ Arad đến Bucharest, sử dụng: hSLD(n) = Ước lượng khoảng cách đường thẳng ("chim bay") từ thành phố hiện tại n đến Bucharest.
- Phương pháp tìm ki ng pháp tìm kiếm Greedy best m Greedy best-first search s first search sẽ xét (phát triển) nút “có vẻ” gần với nút đích (mục tiêu) nhất
#### GBFS ví dụ:
![[Pasted image 20250113013913.png]]
giải:
![[Pasted image 20250113013922.png]]
![[Pasted image 20250113013927.png]]
![[Pasted image 20250113013934.png]]
![[Pasted image 20250113013941.png]]

### GBFS - các đặc điểm
 - Completeness
 - Time complexity
 - Space complexity
 - Optimal?
 => có thể xem cụ thể tại [[Basic Search Algorithms in Artificial Intelligence]]
# References
