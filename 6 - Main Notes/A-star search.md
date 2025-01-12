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
#### A* search - Các đặc điểm:
- Nếu không gian các trạng thái là hữu hạn và có giải pháp để tránh vi tránh việc xét (l c xét (lặp) lại các tr i các trạng thái, thì giải thuật A* là hoàn chỉnh (tìm được lời giải) – nhưng không đảm bảo là tối ưu.
- Nếu không gian các trạng thái là hữu hạn và không có giải pháp để tránh việc xét (lặp) lại các trạng thái, thì giải thuật A là không hoàn chỉnh (không đảm bảo tìm được lời giải).
- Nếu không gian các trạng thái là vô hạn, thì giải thuật A* là không hoàn chỉnh.
#### Admissible heuristic:
- Một ước lượng (heuristic) h(n) được xem là chấp nhận được nếu đối với mọi nút n: 
	- 0 ≤ h(n) ≤ h* được nếu đối với mọi nút n: 0 ≤ h(n) ≤ h (n), trong đó h*(n) là chi phí thật (thực tế) để đi từ nút n đến đích
- Một ước lượng chấp nhận được không bao giờ đánh giá quá cao (overestimate) đối với chi phí để đi tới đích
-  Ví dụ:
	- **Chi phí thực tế**: Từ A đến B là 10 (tính đúng).
	- **Ước lượng**:
	    - Nếu **ước lượng là 8**, nó **không quá cao** → đây là một ước lượng chấp nhận được.
	    - Nếu **ước lượng là 12**, nó **quá cao (overestimate)** → không còn chấp nhận được.
#### Tính tối ưu của A* - chứng minh
![[Pasted image 20250113015441.png]]
![[Pasted image 20250113015929.png]]
![[Pasted image 20250113020048.png]]
#### Ước lượng ưu thế:
![[Pasted image 20250113020216.png]]
#### Ước lượng kiên định:
![[Pasted image 20250113020232.png]]
# References
