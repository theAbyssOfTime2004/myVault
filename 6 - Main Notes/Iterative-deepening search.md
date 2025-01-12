2025-01-13 00:47


Tags: [[Basic Search Algorithms in Artificial Intelligence]], [[beginner]], 

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
![[Pasted image 20250113005308.png]]
![[Pasted image 20250113005314.png]]
![[Pasted image 20250113005529.png]]
![[Pasted image 20250113005538.png]]

# References
