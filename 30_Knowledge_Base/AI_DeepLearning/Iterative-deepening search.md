2025-01-13 00:47


Tags: [[Basic Search Algorithms in Artificial Intelligence]], [[beginner]], [[search algorithm]], [[uninformed search]]

# Iterative-deepening search
#### Ý tưởng: 
- Vấn đề với DLS:
	- nếu tất cả các goal node đều nằm ở độ sâu > limit thì DLS thất bại
- Giải thuật IDS:
	- áp dụng dfs với các đường đi (trong cây) có độ dài <=1
	- Nếu thất bại, tiếp tục áp dụng giải thuật DFS với các đường đi có độ dài <= 2
	- Nếu thất bại, tiếp tục áp dụng giải thuật DFS với các đường đi có độ dài <= 3
	- ... tiếp tục cho đến khi
		1. tìm dc lời giải
		2. toàn bộ cây đã xét mà ko tìm dc lời giải
#### Giải thuật:
![[Pasted image 20250113005558.png]]
- Chú thích: 
	- Cho là depth I khởi tạo ban đầu là 1 thì khi ta xét đến 1 node có tham số depth = 1 cũng == depth I luôn thì fringe (danh sách các node cần xử lý) sẽ + thêm các node con của node hiện tại và thoát khỏi case đó xong quay lên lấy tiếp node con của node hiện tại từ fringe
	- còn nếu node hiện tại đang ở vị trí depth + 1 thì nghĩa là ta cần cập nhật depth, và biểu thức `if (I = 1) then fringe + gamma(n); else fringe <- gamma(n) + fringe` được thêm vào với mục đích để thêm các node con của node đầu tiên vào fringe ban đầu bởi vì I = 1 nghĩa là ta đang ở lần xem xét đầu tiên do đó trong fringe sẽ rỗng còn nếu khác thì ta chỉ việc thêm các phần tử con của node hiện tại vào fringe
![[Pasted image 20250113005308.png]]
![[Pasted image 20250113005314.png]]
![[Pasted image 20250113005529.png]]
![[Pasted image 20250113005538.png]]

#### So sánh
![[Pasted image 20250113011859.png]]
![[Pasted image 20250113011916.png]]

# References
