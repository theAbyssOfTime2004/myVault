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
- 
