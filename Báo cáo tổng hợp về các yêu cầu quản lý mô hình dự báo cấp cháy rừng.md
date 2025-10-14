# 1. Yêu cầu kỹ thuật:

- **Dữ liệu đầu vào cần thiết**
- **Thuật toán dự báo và phân tích**: 
	- Theo các chỉ số cảnh báo truyền thống dựa trên công thức khí tượng
	- Ứng dụng các mô hình AI, ML
- **Hạ tầng cảm biến và giám sát**
- **Hệ thống phân tích và cảnh báo trung tâm** 
=> yêu cầu kỹ thuật đối với mô hình dự báo cháy rừng trải dài từ việc chuẩn bị đầy đủ dữ liệu dầu vào, lựa chọn thuật toán phù hợp, cho đến xây dựng hạ tầng cảm biến – viễn thám và trung tâm phân tích hiện đại. Tất cả nhằm đảm bảo **phát hiện sớm nhất nguy cơ cháy** và **cảnh báo chính xác, kịp thời** đến người quản lý rừng.

# 2. Yêu cầu pháp lý và quy định quản lý liên quan

- **Luật lâm nghiệp 2017**
- **Luật PCCC 2001**
- **Nghị định 156/2018/NĐ-CP**
- **Thông tư 25/2019/TT-BNNPTNT**
- **Các chính sách về chuyển đổi số, ứng dụng AI, IoT**
 => Tóm lại, khuôn khổ pháp lý Việt Nam đã khá đầy đủ cho công tác phòng cháy, chữa cháy rừng và việc ứng dụng công nghệ trong dự báo cháy. Các đơn vị triển khai mô hình cần **bám sát quy định hiện hành**, đặc biệt về trách nhiệm thông tin cảnh báo kịp thời, phối hợp đa ngành và đầu tư hạ tầng PCCR đạt chuẩn. Việc tuân thủ pháp luật không chỉ đảm bảo tính hợp pháp của hệ thống mà còn giúp mô hình **phát huy hiệu quả trong thực tiễn quản lý rừng**.

# 3. Tổ chức quản lý và vận hành hệ thống

- **Vận hành và bảo trì hệ thống kỹ thuật:** Hệ thống dự báo cháy rừng (bao gồm các trạm cảm biến, camera, máy chủ, phần mềm) cần một đơn vị chuyên trách quản lý vận hành. Thông thường, Cục Kiểm lâm sẽ phân công một **Trung tâm kỹ thuật** chịu trách nhiệm giám sát hoạt động hệ thống hàng ngày. Nhân sự kỹ thuật phải theo dõi tính ổn định của các cảm biến, đường truyền, đảm bảo dữ liệu thông suốt. Cần có quy trình **bảo trì định kỳ**: kiểm tra hiệu chuẩn thiết bị đo, vệ sinh camera, nâng cấp phần mềm dự báo... Bên cạnh đó, cơ quan quản lý phải xây dựng **quy trình vận hành chuẩn (SOP)** cho hệ thống: ví dụ, khi trung tâm nhận tín hiệu cảnh báo mức nguy cơ cao, phải lập tức thông báo đến những ai, bằng phương tiện gì; hoặc khi phát hiện điểm cháy trên ảnh vệ tinh, quy định thời gian xác minh chéo hiện trường tối đa bao lâu. Việc vận hành bài bản, chuyên nghiệp và có **kiểm tra, diễn tập thường xuyên** sẽ giúp hệ thống dự báo thực sự trở thành công cụ hỗ trợ đắc lực cho quản lý và ứng phó cháy rừng.

# 4. Yêu cầu về tích hợp và chia sẻ dữ liệu 

- **Tích hợp dữ liệu đa nguồn**:
	- Cần xây dựng database tập trung nơi tích hợp tất cả nguồn dữ liệu này để phân tích tổng hợp
		- Ví dụ dữ liệu thời tiết từ Trung tâm Dự báo khí tượng thủy văn quốc gia có thể được kết nối trực tiếp vào hệ thống dự báo cháy rừng; dữ liệu ảnh vệ tinh (MODIS, NOAA, Sentinel...) được cập nhật tự động vào lớp bản đồ điểm cháy; cơ sở dữ liệu về rừng (diện tích, trạng thái rừng, vật liệu cháy) từ kiểm kê rừng được liên kết để hiệu chỉnh mô hình
		- Việc tích hợp này đòi hỏi **chuẩn hóa dữ liệu** (định dạng, đơn vị đo, hệ tham chiếu bản đồ) để các nguồn khác nhau có thể “hiểu” lẫn nhau.
- **Chia sẻ dữ liệu giữa các cấp chính quyền**:
	- Việc chia sẻ dữ liệu giữa các cấp cũng cần tính đến **phân quyền truy cập**: cấp nào được xem, chỉnh sửa loại dữ liệu gì, nhằm đảm bảo an ninh và tính xác thực của thông tin.
- **Chia sẻ dữ liệu giữa các ngành và hệ thống khác**:
	- Yêu cầu đặt ra là hệ thống phải thiết kế **API mở** hoặc cổng dữ liệu mở cho phép các hệ thống thông tin chính phủ khác khai thác dữ liệu một cách an toàn.
- **Tích hợp và chia sẽ dữ liệu quốc tế**: 
	- Cháy rừng là vấn đề mang tính toàn cầu, trong đó **các vụ cháy xuyên biên giới và khói mù khu vực** đòi hỏi **hợp tác quốc tế về chia sẻ thông tin và dữ liệu**. Hệ thống dự báo cháy rừng của Việt Nam nên **kết nối với các mạng lưới cảnh báo toàn cầu** như **Global Fire Early Warning System (Global EWS)** hoặc **RFMRC-SEA**, nhằm **nhận dữ liệu dự báo nguy cơ cháy (như chỉ số FWI 10 ngày)** và **so sánh tình hình với các nước trong khu vực** để hỗ trợ **quyết định điều phối nguồn lực chữa cháy ở tầm khu vực**.

	- Đồng thời, Việt Nam cần **chia sẻ dữ liệu cháy rừng nội địa** (báo cáo, bản đồ nguy cơ, điểm nóng) tới các **tổ chức quốc tế** như **GFMC (Global Fire Monitoring Center)** hoặc **Trung tâm Phòng cháy rừng châu Á**, theo **chuẩn định dạng quốc tế** (ví dụ: **GeoJSON**, mẫu báo cáo **FAO**). Điều này giúp **tăng tính minh bạch, tương thích và hợp tác quốc tế** trong quản lý và dự báo cháy rừng.