2026-01-19 23:30


Tags: [[diffusion models]]

# VAE và các Diffusion Models

Về bản chất thì VAE và các diffusion models đều có mục tiêu chung là học phân phối xác suất của dữ liệu đầu vào, cụ thể là:

- VAE và Diffusion đều học xấp xỉ phân phối xác suất của dữ liệu gốc:

$$p_{data}(x) ~ p_{\theta}(x)$$

  
- Sau khi học được phân phối, mô hình có thể:
	- Sampling từ phân phối đã học
	- Decode / sinh ra ảnh, video mới  

- Mỗi mô hình có loss function và chiến lược tối ưu khác nhau, nhưng đều nhằm cải thiện chất lượng generating  
- Một số điểm dễ nhầm lẫn giữa generative modeling và supervised learning:
	- Trong VAE / Diffusion model không có ground-truth label để đối chiếu, mục tiêu không phải là giảm khoảng cách giữa 2 điểm $y_{pred}$ và $y_{target}$,  mà thay vào đó, mục tiêu là giảm khoảng cách giữa 2 phân phối xác suất, thông qua:
		- KL-divergence (VAE)
		- Variational bound / score matching (Diffusion)

Nói một cách tổng quát thì:
- Các Variational Autoencoders (VAEs) và Diffusion models đều học cách xấp xỉ phân phối xác suất của dữ liệu huấn luyện. Sau khi phân phối này được học, mô hình có thể thực hiện sampling từ phân phối xấp xỉ đó để sinh ra các mẫu dữ liệu mới như ảnh hoặc video. Mặc dù VAEs và Diffusion models sử dụng các hàm loss và chiến lược tối ưu khác nhau, mục tiêu chung của chúng là giảm sai khác giữa phân phối sinh của mô hình và phân phối dữ liệu thực, thay vì chỉ tối ưu sai số giữa từng cặp mẫu riêng lẻ.  
- Với ảnh thì input là $H\times W \times C$ nhưng vào latent space thì sẽ bị transformed thành một đối tượng  thuộc không gian trừu tượng khác tuỳ thuộc vào tính chất của encoder

|   |   |   |
|---|---|---|
|**Loại Encoder**|**Bản chất Latent Object**|**Ý nghĩa của không gian trừu tượng**|
|**Vanilla CNN**(ResNet/VGG)|**Vector đặc trưng (Feature Vector)**|Không gian chứa các khái niệm cấp cao (mắt, mũi, lông, kim loại, gỗ...). Các vật thể giống nhau về _nội dung_ sẽ nằm gần nhau.|
|**Variational Encoder** (VAE)|**Phân phối xác suất (Gaussian)**|Không gian trơn (smooth). Đối tượng là một "đám mây" xác suất. Các vật thể giống nhau về _cấu trúc_ sẽ nằm gần nhau.|
|**Vision Transformer**(ViT)|**Chuỗi các Token (Sequence)**|Không gian ngữ cảnh (Contextual). Ảnh bị cắt nhỏ thành từng mảnh (patch) và biểu diễn giống như một câu văn gồm nhiều từ ngữ.|
|**Metric Learning**(Siamese Net)|**Embedding Vector**|Không gian khoảng cách (Distance Space). Chỉ quan tâm việc: Ảnh A cùng lớp với ảnh B thì vector phải gần nhau, khác lớp thì đẩy xa ra (dùng trong FaceID).|


# References
