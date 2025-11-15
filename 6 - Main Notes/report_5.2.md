# Báo cáo Tổng hợp: Yêu cầu quản lý và Đánh giá các Chỉ số Dự báo Cháy rừng tại Việt Nam

## Giới thiệu

Báo cáo này trình bày một phân tích toàn diện về các yêu cầu cần thiết để xây dựng và vận hành một hệ thống dự báo cháy rừng hiện đại tại Việt Nam. Nội dung được chia thành ba phần chính:

1. **Các yêu cầu tổng thể:** Phân tích các khía cạnh kỹ thuật, pháp lý, tổ chức và chia sẻ dữ liệu.
2. **Phân tích chuyên sâu các chỉ số dự báo:** Đánh giá chi tiết các chỉ số dự báo nguy cơ cháy rừng phổ biến trên thế giới như FWI, KBDI, FFDI, NDWI, và FPI.
3. **Thực trạng và định hướng cho Việt Nam:** Kết hợp bài học kinh nghiệm quốc tế, thực trạng trong nước và một nghiên cứu tình huống cụ thể tại Bình Chánh, TP.HCM để đề ra định hướng phát triển.

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

## Reference

1. **Bộ NN&PTNT (2023)** – Số liệu hiện trạng rừng Việt Nam năm 2022. _Nguồn trích dẫn:_ Tạp chí Môi trường, bài “Xây dựng hệ thống cảnh báo cháy rừng…”[tapchimoitruong.vn](https://tapchimoitruong.vn/nghien-cuu-23/xay-dung-he-thong-canh-bao-chay-rung-su-dung-cong-nghe-vien-tham-dua-tren-mo-hinh-ngon-ngu-lon-32428#:~:text=Ch%C3%A1y%20r%E1%BB%ABng%20l%C3%A0%20m%E1%BB%99t%20trong,camera%20c%E1%BB%91%20%C4%91%E1%BB%8Bnh%20kh%C3%B4ng%20bao).
    
2. **Báo Thanh Niên (2024)** – “Trong năm 2023, cả nước xảy ra 310 vụ cháy rừng…”, tác giả Đức Nhật, đăng ngày 05/05/2024. _Nguồn trích:_ Báo Thanh Niên điện tử[thanhnien.vn](https://thanhnien.vn/trong-nam-2023-ca-nuoc-xay-ra-310-vu-chay-rung-185240505190641751.htm#:~:text=Trong%20n%C4%83m%202023%2C%20c%E1%BA%A3%20n%C6%B0%E1%BB%9Bc,quy%20%C4%91%E1%BB%8Bnh%20c%E1%BB%A7a%20ph%C3%A1p%20lu%E1%BA%ADt)[thanhnien.vn](https://thanhnien.vn/trong-nam-2023-ca-nuoc-xay-ra-310-vu-chay-rung-185240505190641751.htm#:~:text=Ph%C3%B3%20th%E1%BB%A7%20t%C6%B0%E1%BB%9Bng%C2%A0Tr%E1%BA%A7n%20L%C6%B0u%20Quang,s%E1%BB%9Bm%20ch%C3%A1y%20r%E1%BB%ABng%20t%E1%BB%B1%20%C4%91%E1%BB%99ng%E2%80%A6).
    
3. **Thủ tướng Chính phủ (2024)** – Công điện 43/CĐ-TTg ngày 01/05/2024 về tăng cường PCCCR trên phạm vi cả nước. _Nguồn:_ Trích dẫn qua Báo Thanh Niên[thanhnien.vn](https://thanhnien.vn/thu-tuong-quyet-liet-phong-chay-chua-chay-rung-tren-pham-vi-ca-nuoc-185240501211303957.htm#:~:text=Chi%E1%BB%81u%201,tr%C3%AAn%20ph%E1%BA%A1m%20vi%20c%E1%BA%A3%20n%C6%B0%E1%BB%9Bc)[thanhnien.vn](https://thanhnien.vn/thu-tuong-quyet-liet-phong-chay-chua-chay-rung-tren-pham-vi-ca-nuoc-185240501211303957.htm#:~:text=%C4%90%E1%BB%83%20ti%E1%BA%BFp%20t%E1%BB%A5c%20ch%E1%BB%A7%20%C4%91%E1%BB%99ng,r%E1%BB%ABng%20t%E1%BB%AB%20s%E1%BB%9Bm%2C%20t%E1%BB%AB%20xa).
    
4. **European Environment Agency (2021)** – Định nghĩa chỉ số **FWI**. _Nguồn:_ Climate-ADAPT, mục Fire Weather Index[climate-adapt.eea.europa.eu](https://climate-adapt.eea.europa.eu/en/metadata/indicators/fire-weather-index#:~:text=Fire%20Weather%20Index%20%28Dimensionless%29,relative%20humidity%2C%20and%20wind%20speed).
    
5. **Keetch & Byram (1968)** – **Chỉ số hạn KBDI** do US Forest Service phát triển. _Nguồn:_ Earth Engine Data Catalog (ĐH Tokyo, 2015)[developers.google.com](https://developers.google.com/earth-engine/datasets/catalog/UTOKYO_WTLAB_KBDI_v1?hl=vi#:~:text=Thang%20%C4%91i%E1%BB%83m%20n%C3%A0y%20dao%20%C4%91%E1%BB%99ng,c%C3%A2y%20ph%E1%BB%A5%20thu%E1%BB%99c%20v%C3%A0o%20m%C6%B0a) và Wikipedia tiếng Việt[vi.wikipedia.org](https://vi.wikipedia.org/wiki/Ch%E1%BB%89_s%E1%BB%91_h%E1%BA%A1n_h%C3%A1n_Keetch-Byram#:~:text=KBDI%20l%C3%A0%20m%E1%BB%99t%20%C6%B0%E1%BB%9Bc%20t%C3%ADnh,k%E1%BB%83%20%C4%91%E1%BA%BFn%20t%C3%ADnh%20ch%E1%BA%A5t%20ch%C3%A1y).
    
6. **CSIRO (2018)** – **Chỉ số FFDI** (Forest Fire Danger Index) – Hướng dẫn đánh giá nguy cơ cháy rừng Úc. _Nguồn:_ CSIRO Bushfire Guide[research.csiro.au](https://research.csiro.au/bushfire/assessing-bushfire-hazards/hazard-identification/fire-danger-index/#:~:text=The%20Forest%20Fire%20Danger%20Index,uses%20FFDI%20to%20assign%20a).
    
7. **Roberts et al. (2006)** – Nghiên cứu sử dụng **NDWI** để giám sát độ ẩm nhiên liệu sống. _Nguồn:_ USFS Research (Int. J. Remote Sensing)[research.fs.usda.gov](https://research.fs.usda.gov/treesearch/41842#:~:text=33,chlorophyll%20absorption%20such%20as%20NDVI).
    
8. **USGS (2022)** – **Chỉ số FPI/WFPI** – Mô tả sản phẩm dự báo nguy cơ cháy. _Nguồn:_ USGS Fire Danger Forecast[usgs.gov](https://www.usgs.gov/fire-danger-forecast/fire-danger-data-products-and-tools#:~:text=The%20Wildland%20Fire%20Potential%20Index,burn%20more%20than%20500%20acres)[usgs.gov](https://www.usgs.gov/fire-danger-forecast/fire-danger-data-products-and-tools#:~:text=The%20WFPI%20model%20is%20primarily,windspeed%2C%20measured%20at%20flame%20height).
    
9. **Bui et al. (2019)** – Ứng dụng **AI (MARS-DFP)** dự báo nguy cơ cháy rừng tại Lào Cai, Việt Nam. _Nguồn:_ J. Environmental Management[pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/30825780/#:~:text=optimize%20the%20model,prediction%20of%20forest%20fire%20susceptibility).
    
10. **Báo Chính Phủ (2025)** – “Ngành Lâm nghiệp: Hướng tới phát triển bền vững, hiện đại…”. _Nguồn trích:_ Báo điện tử Chính phủ ngày 06/11/2025[baochinhphu.vn](https://baochinhphu.vn/nganh-lam-nghiep-huong-toi-phat-trien-ben-vung-hien-dai-va-da-gia-tri-102251106095615537.htm#:~:text=Tuy%20nhi%C3%AAn%2C%20v%E1%BB%9Bi%20n%E1%BB%81n%20t%E1%BA%A3ng,v%C3%A0%20th%C6%B0%C6%A1ng%20m%E1%BA%A1i%20b%E1%BB%81n%20v%E1%BB%AFng)[baochinhphu.vn](https://baochinhphu.vn/nganh-lam-nghiep-huong-toi-phat-trien-ben-vung-hien-dai-va-da-gia-tri-102251106095615537.htm#:~:text=ngh%E1%BB%89%20d%C6%B0%E1%BB%A1ng%20trong%20r%E1%BB%ABng%20%C4%91%C6%B0%E1%BB%A3c,500%20t%E1%BB%B7%20%C4%91%E1%BB%93ng%20n%C4%83m%202024).
    
11. **Tạp chí Môi trường (2025)** – “Xây dựng hệ thống cảnh báo cháy rừng sử dụng công nghệ viễn thám và mô hình ngôn ngữ lớn”. _Nguồn:_ Tạp chí MT số 08/2025[tapchimoitruong.vn](https://tapchimoitruong.vn/nghien-cuu-23/xay-dung-he-thong-canh-bao-chay-rung-su-dung-cong-nghe-vien-tham-dua-tren-mo-hinh-ngon-ngu-lon-32428#:~:text=v%C3%A0%20nghi%C3%AAm%20tr%E1%BB%8Dng%20h%C6%A1n%20do,cho%20ph%C3%A9p%20gi%C3%A1m%20s%C3%A1t%20hi%E1%BB%87n)[tapchimoitruong.vn](https://tapchimoitruong.vn/nghien-cuu-23/xay-dung-he-thong-canh-bao-chay-rung-su-dung-cong-nghe-vien-tham-dua-tren-mo-hinh-ngon-ngu-lon-32428#:~:text=Vehicle%20,kh%C3%B4ng%20ng%E1%BB%ABng%20c%E1%BB%A7a%20c%C3%B4ng%20ngh%E1%BB%87).

12. **FAO (2016)** – Đánh giá hiện trạng cháy rừng Việt Nam giai đoạn 1990–2015, _trích trong_: **State of the World’s Forests 2016** (báo cáo quốc gia Việt Nam)[openknowledge.fao.org](https://openknowledge.fao.org/items/594b22b1-c266-45d3-9e84-6bf2f2fc8cd7#:~:text=,2014).