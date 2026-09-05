

bài hôm nay về mixed precision + gradscaler là gồm: các loại số thực floating point như FP32, FP16, BF16 và TF32, ta phân tích ưu và nhược điểm của từng loại, rút ra kết luận hiện tại tối ưu và đuược đông đảo người dùng nhất là BF16 vì nó giữ được dãy giá trị dài như FP32 và phải đánh đổi lại bằng 1 ít sự chính xác, tuy nhiên trong việc training model thì sự có mặt của giá trị sẽ có ích hơn là độ mịn chi tiết, do đó có nhiễu hay không vẫn không quan trọng bằng tín hiệu, ngoài ra ta học thêm Autoscaler cho FP16, vì FP16 sẽ bỏ bớt 1 vài bit biểu diễn exponent để đổi lại sự chính xác nên vài số quả nhỏ sẽ bị underflow thành 0.0, do đó có scaler để giúp handle việc này, tuy nhiên sau khi kiểm tra bằng code thì thấy kết quả vẫn không được bằng BF16 native

# Mixed Precision & GradScaler

|**Định dạng**|**Cấu trúc bit (Sign + Exp + Mantissa)**|**Điểm mạnh**|**Điểm yếu**|**Vị trí thực chiến hiện nay**|
|---|---|---|---|---|
|**FP32**|$1 + 8 + 23$ ($32\text{ bits}$)|Rất mịn, dải giá trị chuẩn mực, không lo underflow/overflow.|Rất nặng VRAM, tính toán chậm trên GPU.|Dùng làm **Master Weights** để tích lũy cập nhật trọng số chính xác.|
|**FP16**|$1 + \mathbf{5} + 10$ ($16\text{ bits}$)|Tiết kiệm $50\%$ VRAM, độ mịn cao ($10\text{ bits}$), được hỗ trợ rộng rãi trên GPU đời cũ/Edge device.|Dải số mũ ngắn ($\mathbf{5\text{ bits}}$) $\rightarrow$ **Dễ Underflow**, bắt buộc phải dùng kèm **`GradScaler`** để nhân phóng to gradient.|Dùng cho **Inference** hoặc huấn luyện trên GPU đời cũ ($<$ 2020 như Tesla T4, V100).|
|**BF16**|$1 + \mathbf{8} + 7$ ($16\text{ bits}$)|Giữ nguyên dải số mũ của FP32 ($\mathbf{8\text{ bits}}$) $\rightarrow$ **Không bao giờ bị Underflow**, không cần scaler, code gọn, loss giảm mượt.|Độ mịn thô hơn một chút (chấp nhận nhiễu nhẹ ở đuôi mantissa).|**Tiêu chuẩn vàng (Golden Standard)** để huấn luyện LLM và AI hiện đại trên GPU Ampere trở lên (RTX 30xx/40xx, A100, H100).|
|**TF32**|$1 + 8 + 10$ ($19\text{ bits}$)|Giữ nguyên code FP32, GPU tự động gọt bit để tăng tốc gấp $4\times$ trên Tensor Cores.|Vẫn chiếm trọn $32\text{ bits}$ trong VRAM (không tiết kiệm được byte nhớ nào).|Tính năng tự động của phần cứng NVIDIA khi chạy các phép toán `torch.float32`.|


# Quantization

- Nếu như **BF16/FP16** giúp giảm kích thước từ 32-bit xuống 16-bit, thì quantization tiếp tục ép weights xuống còn 8bit (INT8/FP8), 4bit(INT4/FP4) hay thậm chí là 2bit(INT2)

- Có bài toán VRAM thực tế:
	- thử với LLaMA - 70B 
		- với FP16/BF16 cần 70B * 2bytes = 140GB VRAM chỉ để load model, chưa tính chạy 
		- Nhưng nếu nén lại về INT4 (0.5 bytes) ~ 70B * 0.5 = 35GB VRAM, rtx3090/4090 hay macbook cũng có thể chạy được 
		- => quantization giúp local AI phổ biến và dễ tiếp cận hơn 

- Bản chất, cách hoạt động: 
	- bằng cách mapping **một dải số thực liên tục (Continuous float) thành các số nguyên rời rạc (Discrete integers)** thông qua một hệ số tỉ lệ (Scale factor)
	- $$X_{\text{quantized}} = \text{round}\left(\frac{X_{\text{float}}}{\text{Scale}}\right)$$

- 2 approach nổi bật: 
	- Cho **Post-training** (PTQ - cho inference): 
		- Mô hình đã được train xong xuôi ở BF16. Bạn dùng các thuật toán thông minh để nén nó xuống 4-bit/8-bit mà **suy giảm độ thông minh (Perplexity) gần như bằng 0%**
	- Cho training (Quantization-aware training / fine-tuning)
		- **QLoRA** (Quantized Low-Rank Adaptation): Đóng băng mô hình gốc ở dạng **4-bit (NF4)** để tiết kiệm VRAM tối đa, sau đó chỉ gắn thêm một vài tầng trọng số nhỏ bằng BF16 để train. Nhờ đó, bạn có thể fine-tune một mô hình 70B ngay trên một chiếc GPU phổ thông

- Kể từ H100 và RTX 40xx, NVDIA bổ sung nhân phần cứng xử lý FP8 giúp training trực tiếp trên FP8 khả thi, không underflow, nhanh gấp đôi BF16, giảm 1 nửa VRAM