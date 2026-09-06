# KV-cached

- Với attention mechanism, mỗi lần autoregressive model sinh ra 1 chữ mới, nó cần tính lại Q của chữ mới với K,V của toàn bộ các chữ cũ, nếu không KV-cached thì: 
	- Có 3 chữ → tính K,V cho 3 chữ
	- Thêm chữ thứ 4 → tính lại K,V cho cả 4 chữ
	- Thêm chữ thứ 5 → tính lại K,V cho cả 5 chữ
=> rất lãng phí và tốn thời gian

- Với KV-cached:
	- Có 3 chữ → tính K,V, cất vào ngăn kéo (cache)
	- Chữ thứ 4 → chỉ tính K,V của chữ 4 → bỏ thêm vào ngăn kéo
	- Chữ thứ 5 → chỉ tính K,V của chữ 5 → bỏ thêm vào ngăn kéo
	
	→ Nhanh hơn nhiều vì không làm lại việc cũ.


# PagedAttention

- Thay đổi cách lưu KV-cached trên GPU 
- các vùng nhớ sẽ được đưa vào pool chung chia thành các block cố định kích thước `block_size`, khi cần thì lôi ra, group by block table,  rồi cấp động 1 cách phù hợp, thay vì cứ auto gán max_seq_len như trước, còn khi đã lấy ra đủ rồi nhưng mà cần thêm thì append block mới vào block table