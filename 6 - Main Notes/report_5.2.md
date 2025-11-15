# Báo cáo Tổng hợp: Yêu cầu Xây dựng Hệ thống và Đánh giá các Chỉ số Dự báo Cháy rừng tại Việt Nam

## Giới thiệu

Báo cáo này trình bày một phân tích toàn diện về các yêu cầu cần thiết để xây dựng và vận hành một hệ thống dự báo cháy rừng hiện đại tại Việt Nam. Nội dung được chia thành ba phần chính:

1. **Các yêu cầu tổng thể:** Phân tích các khía cạnh kỹ thuật, pháp lý, tổ chức và chia sẻ dữ liệu.
2. **Phân tích chuyên sâu các chỉ số dự báo:** Đánh giá chi tiết các chỉ số dự báo nguy cơ cháy rừng phổ biến trên thế giới như FWI, KBDI, FFDI, NDWI, và FPI.
3. **Thực trạng và định hướng cho Việt Nam:** Kết hợp bài học kinh nghiệm quốc tế, thực trạng trong nước và một nghiên cứu tình huống cụ thể tại Bình Chánh, TP.HCM để đề ra định hướng phát triển.

---

## **PHẦN I: CÁC YÊU CẦU TỔNG THỂ ĐỂ XÂY DỰNG HỆ THỐNG DỰ BÁO CHÁY RỪNG**

### 1. Yêu cầu về Kỹ thuật

Một hệ thống dự báo cháy rừng hiệu quả phải dựa trên ba trụ cột kỹ thuật chính:

- **Dữ liệu đầu vào:** Cần thu thập dữ liệu đa dạng và đầy đủ, bao gồm các yếu tố khí tượng (nhiệt độ, độ ẩm, mưa, gió), độ ẩm vật liệu cháy, đặc điểm thảm thực vật, địa hình và lịch sử các vụ cháy.
- **Thuật toán phân tích:** Có hai hướng tiếp cận chính:
    - **Truyền thống:** Sử dụng các chỉ số khí tượng như **FWI (Fire Weather Index)** của Canada hay **chỉ số P (Nesterov)** mà Việt Nam đang áp dụng.
    - **Hiện đại:** Ứng dụng **Trí tuệ nhân tạo (AI) và Máy học** để phân tích dữ liệu lớn, nhận diện các mẫu hình phức tạp.  
        Cả hai hướng đều cần tích hợp **Hệ thống Thông tin Địa lý (GIS)** để trực quan hóa nguy cơ trên bản đồ. Việc lựa chọn và hiệu chỉnh các chỉ số này cho điều kiện Việt Nam sẽ được phân tích sâu ở Phần II.
- **Hạ tầng giám sát:** Cần một mạng lưới thu thập dữ liệu thời gian thực, bao gồm **trạm khí tượng chuyên dụng**, **cảm biến IoT** (đo nhiệt độ, khói), **ảnh vệ tinh** (như hệ thống FireWatch) và **camera giám sát ứng dụng AI** để tự động phát hiện khói/lửa. Toàn bộ dữ liệu cần được truyền về một **trung tâm phân tích** để xử lý và cảnh báo.

### 2. Yêu cầu về Pháp lý và Quy định

Hệ thống phải tuân thủ chặt chẽ khung pháp lý của Việt Nam, bao gồm:

- **Luật Lâm nghiệp 2017 và Luật PCCC 2001:** Đặt nền tảng về trách nhiệm của chủ rừng và các cơ quan nhà nước.
- **Thông tư 25/2019/TT-BNNPTNT:** Hướng dẫn chi tiết về việc xây dựng hệ thống dự báo, cảnh báo và nhấn mạnh việc **ứng dụng khoa học công nghệ**.
- **Chính sách chuyển đổi số:** Các chỉ thị của Chính phủ tạo điều kiện thuận lợi cho việc áp dụng công nghệ mới như AI, IoT.

### 3. Yêu cầu về Tổ chức Quản lý và Vận hành

Một hệ thống kỹ thuật tốt cần một bộ máy vận hành hiệu quả:

- **Phân cấp quản lý:** **Cục Kiểm lâm** là cơ quan đầu mối trung ương, chịu trách nhiệm ban hành cảnh báo toàn quốc. **Chi cục Kiểm lâm tỉnh** và **Hạt Kiểm lâm huyện** truyền đạt thông tin đến cơ sở.
- **Cơ chế phối hợp:** Khi có cảnh báo cấp nguy hiểm (cấp IV, V), **Ban chỉ huy PCCR các cấp** được kích hoạt để huy động lực lượng đa ngành theo phương châm "4 tại chỗ". Mô hình **Hệ thống Chỉ huy Sự cố (ICS)** của Mỹ là một kinh nghiệm tốt để học hỏi.
- **Vận hành kỹ thuật:** Cần có đội ngũ chuyên trách để bảo trì, giám sát hệ thống và xây dựng quy trình vận hành chuẩn (SOP).

### 4. Yêu cầu về Tích hợp và Chia sẻ Dữ liệu

Dữ liệu là tài sản cốt lõi, đòi hỏi khả năng tích hợp và chia sẻ thông suốt:

- **Tích hợp đa nguồn:** Xây dựng cơ sở dữ liệu tập trung, tổng hợp dữ liệu từ ngành khí tượng, viễn thám, kiểm kê rừng.
- **Chia sẻ đa chiều:** Thông tin cần lưu thông hai chiều giữa trung ương và địa phương, cũng như chia sẻ liên ngành (môi trường, nông nghiệp) và tích hợp vào các Trung tâm điều hành thông minh (IOC) của tỉnh.
- **Hợp tác quốc tế:** Kết nối với các mạng lưới toàn cầu như **Global EWS** để tham khảo dự báo và chia sẻ dữ liệu.

---

## **PHẦN II: PHÂN TÍCH CHUYÊN SÂU CÁC CHỈ SỐ DỰ BÁO NGUY CƠ CHÁY RỪNG**

### 5. Bảng so sánh chi tiết các chỉ số

Để lựa chọn thuật toán phù hợp, việc hiểu rõ các chỉ số dự báo quốc tế là rất quan trọng. Dưới đây là bảng so sánh 5 chỉ số phổ biến:

|**Chỉ số**|**Đặc điểm chính**|**Ưu điểm**|**Nhược điểm**|**Ứng dụng điển hình**|
|:--|:--|:--|:--|:--|
|**FWI**  <br>(Fire Weather Index)|Chỉ số tổng hợp **thời tiết cháy rừng** của Canada, dựa trên nhiệt độ, độ ẩm, mưa, gió.|- Phản ánh toàn diện điều kiện thời tiết.  <br>- Được dùng rộng rãi trên thế giới (Canada, Châu Âu).  <br>- Giúp dự báo khả năng bắt lửa và cường độ cháy.|- Phức tạp, cần nhiều dữ liệu.  <br>- Không xét đến nguồn gây cháy hay địa hình.  <br>- Cần hiệu chỉnh ngưỡng cho từng vùng.|- Canada, Châu Âu (EFFIS).  <br>- Hệ thống cảnh báo cháy rừng toàn cầu.|
|**KBDI**  <br>(Keetch-Byram Drought Index)|Chỉ số **hạn khô tích lũy** của Mỹ, biểu thị độ thiếu ẩm trong đất và thảm mục. Thang đo 0-800.|- Dễ tính toán.  <br>- Phản ánh hạn hán dài hạn.  <br>- Tương thích làm tham số cho các chỉ số khác.|- Không xét gió, độ ẩm không khí trực tiếp.  <br>- Biến động nhanh sau mưa lớn.  <br>- Cần hiệu chỉnh ngưỡng theo vùng.|- Đông Nam Hoa Kỳ.  <br>- Dùng gián tiếp trong FFDI của Úc.|
|**FFDI**  <br>(Forest Fire Danger Index)|Chỉ số của Úc, kết hợp nhiệt độ, độ ẩm, gió và **hệ số khô hạn (Drought Factor)**.|- Cân bằng giữa thời tiết ngắn hạn và hạn dài hạn.  <br>- Gắn liền với thang cảnh báo công cộng, dễ hiểu.|- Mang tính đặc thù của Úc, cần hiệu chỉnh khi áp dụng nơi khác.  <br>- Phụ thuộc vào cách tính Drought Factor.|- Úc (chỉ số cảnh báo chính thức).  <br>- Nghiên cứu ở các vùng khí hậu tương tự.|
|**NDWI**  <br>(Normalized Difference Water Index)|Chỉ số viễn thám, thể hiện **hàm lượng nước trong thảm thực vật** từ ảnh vệ tinh.|- Phản ánh trực tiếp độ ẩm nhiên liệu sống.  <br>- Cung cấp thông tin không gian chi tiết.  <br>- Hữu ích cho vùng thiếu trạm khí tượng.|- Bị ảnh hưởng bởi mây che.  <br>- Cần kết hợp với yếu tố thời tiết.  <br>- Chu kỳ cập nhật không liên tục.|- Giám sát hạn hán và nguy cơ cháy toàn cầu.  <br>- Tích hợp vào các mô hình dự báo.|
|**FPI**  <br>(Fire Potential Index)|Chỉ số của Mỹ, **kết hợp dữ liệu vệ tinh** (độ xanh thực vật) và **khí tượng** (độ ẩm nhiên liệu, gió, nhiệt).|- Tích hợp nhiều yếu tố, toàn diện hơn.  <br>- Cập nhật được biến động theo mùa của thảm thực vật.  <br>- Tương quan tốt với các vụ cháy lớn.|- Yêu cầu dữ liệu đa nguồn, phức tạp khi triển khai.  <br>- Có độ trễ do chu kỳ cập nhật của vệ tinh.  <br>- Chưa phổ biến cho cảnh báo đại chúng.|- Bắc Mỹ (USGS).  <br>- Nghiên cứu ứng dụng tại Châu Âu, Châu Á.|

---

## **PHẦN III: THỰC TRẠNG, KINH NGHIỆM QUỐC TẾ VÀ ĐỊNH HƯỚNG CHO VIỆT NAM**

### 6. Bài học Kinh nghiệm từ các Mô hình Quốc tế

- **Canada:** Thành công với hệ thống **FWI** nhờ tính đơn giản, nhất quán và được chuẩn hóa.
- **Hoa Kỳ:** Đi đầu trong việc tích hợp công nghệ đa nguồn (camera AI, drone, vệ tinh) và hệ thống cảnh báo nhanh như **"Cảnh báo Cờ đỏ"**.
- **Úc:** Chú trọng việc truyền thông cảnh báo (dựa trên **FFDI**) đến cộng đồng một cách dễ hiểu, gắn liền với hướng dẫn hành động cụ thể.
- **Châu Âu (hệ thống EFFIS):** Thể hiện tầm quan trọng của hợp tác khu vực và chia sẻ dữ liệu xuyên biên giới.

### 7. Thực trạng và Định hướng tại Việt Nam

- **Thực trạng:** Hệ thống hiện tại của Việt Nam dựa trên **FireWatch** (phát hiện điểm nóng qua vệ tinh) và **chỉ số P Nesterov** để đưa ra cảnh báo 5 cấp. Một số địa phương như **Đồng Nai** đã thí điểm thành công camera AI phát hiện khói sớm.
- **Thách thức:** Kinh phí đầu tư lớn, nguồn nhân lực cần đào tạo, và hạ tầng viễn thông ở vùng sâu còn hạn chế.
- **Định hướng:** Tiếp tục đầu tư vào hạ tầng cảnh báo sớm, xây dựng cơ sở dữ liệu cháy rừng quốc gia, và nhân rộng các mô hình ứng dụng công nghệ cao. Để cụ thể hóa định hướng này, việc đánh giá mức độ phù hợp của các chỉ số quốc tế tại một địa bàn cụ thể là rất cần thiết.

### 8. Nghiên cứu Tình huống: Đánh giá các Chỉ số tại Bình Chánh, TP.HCM

Với đặc thù khí hậu nhiệt đới gió mùa (nóng ẩm, hai mùa mưa-khô rõ rệt), mức độ phù hợp của các chỉ số tại Bình Chánh như sau:

- **FWI và FFDI:** Khá phù hợp để cảnh báo nguy hiểm hàng ngày trong mùa khô, nhưng cần **hiệu chỉnh lại ngưỡng cảnh báo** cho phù hợp với điều kiện độ ẩm cao của địa phương.
- **KBDI:** Hữu ích để theo dõi **tích lũy khô hạn trong mùa khô**, nhưng không đủ để cảnh báo ngắn hạn hàng ngày.
- **NDWI:** Rất hữu ích để **khoanh vùng các khu vực trọng điểm** có thảm thực vật khô kiệt vào cuối mùa khô, cung cấp thông tin không gian mà các chỉ số thời tiết không có.
- **FPI:** Rất phù hợp về mặt khoa học vì kết hợp được cả yếu tố thời tiết và tình trạng thực vật, nhưng đòi hỏi đầu tư về công nghệ và dữ liệu để triển khai.

## Kết luận và Kiến nghị

1. **Không có chỉ số nào là hoàn hảo:** Việc xây dựng một hệ thống dự báo cháy rừng hiệu quả cho Việt Nam không nên dựa vào một chỉ số duy nhất. Thay vào đó, cần một **cách tiếp cận tích hợp**.
2. **Kiến nghị mô hình kết hợp:**
    - **Cảnh báo hàng ngày:** Sử dụng một chỉ số thời tiết mạnh như **FWI** (đã được chuẩn hóa quốc tế) hoặc **FFDI** (đơn giản, dễ truyền thông) làm chỉ số chính, nhưng cần nghiên cứu để hiệu chỉnh ngưỡng cho từng vùng sinh thái ở Việt Nam.
    - **Theo dõi mùa vụ:** Sử dụng **KBDI** để đánh giá mức độ khô hạn nền, giúp xác định thời điểm bắt đầu và đỉnh điểm của mùa cháy.
    - **Giám sát không gian:** Tích hợp dữ liệu viễn thám qua **NDWI** để xác định các "điểm nóng" về độ khô của thảm thực vật, ưu tiên nguồn lực giám sát cho các khu vực này.
3. **Lộ trình phát triển:**
    - **Ngắn hạn:** Cải tiến hệ thống hiện tại bằng cách thử nghiệm và hiệu chỉnh FWI/FFDI song song với chỉ số Nesterov. Tăng cường sử dụng bản đồ NDWI để khoanh vùng nguy cơ.
    - **Dài hạn:** Hướng tới xây dựng một hệ thống tiên tiến hơn như **FPI**, kết hợp dữ liệu vệ tinh, khí tượng và AI, đồng thời nhân rộng các mô hình giám sát tự động như camera AI đã thành công tại Đồng Nai.

Việc triển khai đồng bộ các giải pháp trên, trong một khuôn khổ pháp lý và tổ chức vận hành chặt chẽ, sẽ giúp Việt Nam xây dựng được một hệ thống dự báo cháy rừng tiên tiến, hiệu quả và phù hợp với điều kiện thực tiễn.

