2025-01-12 23:14


Tags: [[search algorithm]], [[beginner]]
# Bread-first search
#### Ý tưởng:
- Phát triển các nút chưa xét theo chiều rộng - Các nút được xét theo thứ tự độ sâu tăng dần
#### Cài đặt giải thuật:
- fringe là 1 cấu trúc kiểu `queue` (FIFO - các nút mới dc bổ sung vào cuối fringe).
#### Các ký hiệu được sử dụng
- fringe: queue lưu giữ các node (state) *sẽ* đc duyệt
- closed: queue lưu giữ các node (state) *đã* dc duyệt
- G=(N,A): cây biểu diễn không gian trạng thái của bài toán
- $n_{0}$ : state đầu của bài toán hay là nút gốc của cây
- GOAL: trạng thái đích
- $\gamma(n)$ : tập các node con của node đang xét n
![[Pasted image 20250112235959.png]]
![[Pasted image 20250113000007.png]]
![[Pasted image 20250113000013.png]]
![[Pasted image 20250113000018.png]]
![[Pasted image 20250113000028.png]]

### BFS - Các đặc điểm 
- completeness
- time complexity
- space complexity
- optimal?
=> xem cụ thể hơn ở [[Basic Search Algorithms in Artificial Intelligence]]
