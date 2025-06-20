2025-06-20 11:19


Tags:

# SVD for denoising
| Bước                 | Mục tiêu                             |
| -------------------- | ------------------------------------ |
| 1. Đọc file âm thanh | Lấy mảng mẫu `s`                     |
| 2. Chọn `N`, `H`     | Kích thước frame và bước trượt       |
| 3. Chia frame        | Tạo ma trận `A`                      |
| 4. Cửa sổ hóa        | Làm mượt biên frame                  |
| 5. SVD               | Phân tích thành phần tín hiệu        |
| 6. Tapering          | Giảm nhiễu bằng chỉnh `S`            |
| 7. PDE               | Làm mượt `U`, `V` (nếu cần)          |
| 8. Tái tạo           | Ghép lại ma trận âm thanh            |
| 9. Overlap-add       | Biến về tín hiệu 1D để nghe hoặc lưu |
|                      |                                      |
|                      |                                      |


# References
