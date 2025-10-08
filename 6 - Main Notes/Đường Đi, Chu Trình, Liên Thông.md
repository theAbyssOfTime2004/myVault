2025-10-08 21:36


Tags: [[Graph Theory]]

# Đường Đi, Chu Trình, Liên Thông

### Đường Đi:
- Là 1 dãy các đỉnh sao cho mỗi cặp đỉnh liên tiếp được nối với nhau bằng 1 cạnh
- **Đường đi đơn**:
	- Là 1 đường đi không lặp lại các đỉnh hoặc cạnh nào
		- Ví dụ: 
``` python
a - b - c - d: là 1 đường đi đơn 
a - b - c - b - d: không là 1 đường đi đơn
```
- **Đường đi sơ cấp**:
	- Là 1 **đường đi đơn** mà không thể tách thành 2 hay nhiều đường nhỏ hơn giữa cùng 2 đỉnh
		- Ví dụ:
```
A —— B —— C
 \         /
   \     /
      D

```
- A - B - C là đường đi sơ cấp
- A - B - D - C không là đường đi sơ cấp
### Chu Trình: 
- Là 1 đường đi bắt đầu và kết thúc tại cùng 1 đỉnh, có ít nhất 3 cạnh
- **Chu trình đơn**:
	- Không có **đỉnh hoặc cạnh nào lặp lại**, ngoại trừ đỉnh đầu = đỉnh cuối 
	- Ví dụ: `a - b - c - a` là 1 chu trình đơn
- **Chu trình sơ cấp**:
	- Là 1 chu trình đơn không chứa bất kỳ chu trình nào bên trong, là chu trình nhỏ nhất (về số cạnh) mà vẫn tạo thành 1 vòng khép kín
	- Ví dụ:
```
A —— B
|   / |
|  /  |
| /   |
D —— C

```
- A - B - C - D - A là 1 chu trình đơn nhưng không sơ cấp
- A - B - D - A hoặc B - D - C - B mới là các chu trình sơ cấp
### Liên Thông
- “Liên thông” = Có thể đi tới nhau.
- “Thành phần liên thông” = Nhóm đỉnh “đi tới nhau được”.
- “Đồ thị liên thông” = Cả đồ thị là **một nhóm duy nhất** như vậy.

# References
