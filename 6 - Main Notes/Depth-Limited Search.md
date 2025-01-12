2025-01-13 00:14


Tags: [[Basic Search Algorithms in Artificial Intelligence]], [[beginner]]

# Depth-Limited Search
#### Ý tưởng:
- DLS = DFS + giới hạn độ sâu trong quá trình tìm kiếm
	- => các nút ở độ sâu/không có nút con
#### Giải thuật:
![[Pasted image 20250113001552.png]]
- giải thích
	- Recursive - DLS(Make-Node(Initial-State[problem]), problem, limit) = khởi tạo node đầu cùng với các tham số *problem* và *limit*
	- function Recursive-DLS (node, problem, limit) returns soln/fail/cutoff = hàm recursive-DLS sẽ trả về 3 trạng thái soln/fail/cutoff, dòng này cũng thể hiện rằng hàm Recursive-DLS đang tiến hành xem xét node đầu tiên sau khi khởi tạo
	- bắt đầu hàm recursive-DLS:
		- `cutoff - occurred <- false` = tham số cutoff - occurred được khởi tạo mặc định là false 
		- `if GOAL - Test[problem](State[node]) then return SOLUTION(node)`: nếu node đầu tiên là GOAL thì trả về SOLUTION
		- nếu không phải goal thì ta sang dòng tiếp theo
		- `else if DEPTH[node] = limit then return cutoff`: kiểm tra nếu độ sâu node hiện tại = limit thì trả về cutoff
		- nếu không = limit thì ta sang dòng tiếp theo
		- `else for each successor in EXPAND(node,problem) do`: với mỗi successor của node hiện tại (có được successor bằng hàm EXPAND(node,problem)) ta thực hiện các bước sau:
			- `result <- Recursive-DLS(successor, problem, limit)`: thực thi hàm recursive-DLS trên node (sucessor) hiện tại
			- `if result = cutoff then cutoff-occurred? <- true`: khi thực thi hàm recursive-DLS trên node (successor) hiện tại thì hàm này sẽ khởi tạo tham số cutoff-occurred với giá trị mặc định là false, nếu result (hay giá trị trả về từ hàm Recursive-DLS) là cutoff thì tham số cutoff-occurred đc thay đổi thành true
			- nếu result không = cutoff thì ta sang dòng tiếp theo
			- `else if result != failure`: result khác failure nghĩa là kết quả đó = sol do đó ta trả về result
			- kết thúc vòng lặp cho từng successor <=> chỉ có 1 trong 2 output có thể trả ra là:
				- result = cutoff do đó tham số cutoff-occurred được set = true (nếu đúng không trả về kết quả và sẽ thoát ra khỏi vòng lặp và thực hiện bước cuối cùng là `if cutoff-occurred? then return cutoff else return failure` ở dưới)
				- không có cutoff nào và cũng không có failure do đó trả về kết quả
			- thoát ra khỏi vòng lặp cho các successor (nghĩa là sau khi ta hoàn thành việc đánh giá result của 1 successor)
				- `if cutoff-occurred? then return cutoff else return failure`: nếu tham số cutoff-occurred = true như ở trên đã nói thì sẽ ngay lập tức thực hiện việc trả về kết quả cutoff, không thì failure 
![[Pasted image 20250113001614.png]]


# References
