# Báo cáo Cá nhân (Reflection - Đào Quang Thắng)

**Vai trò:** Lead Data Engineer & Pipeline Optimizer

Trong giai đoạn hoàn thiện dự án, tôi đã tập trung giải quyết các bài toán về chất lượng dữ liệu và quy trình kiểm soát (Quality Control) cho hệ thống đánh giá RAG:

### 1. Xây dựng Golden Dataset 70 Cases (AI-Powered)
- **Vấn đề:** Các mẫu test case cũ (50 câu) còn đơn giản và chưa bao quát hết các kịch bản thực tế.
- **Giải quyết:** Tôi đã nâng cấp script `synthetic_gen.py` lên phiên bản V3, sử dụng GPT-4o-mini để tự động trích xuất nội dung từ các tài liệu SOP thật của `Day 08`. 
- **Kết quả:** Tạo ra bộ dữ liệu chuẩn gồm **70 câu hỏi** với đầy đủ các mức độ: Easy, Medium, Hard, Multi-hop và đặc biệt là **Adversarial Prompts** (câu hỏi đánh lừa) để kiểm tra khả năng chống Hallucination của Agent.

### 2. Xử lý triệt để lỗi Encoding Tiếng Việt
- **Vấn đề:** Dữ liệu sinh ra bị lỗi font (mojibake) khiến hệ thống đánh giá không thể đọc hiểu chính xác câu trả lời.
- **Giải quyết:** Tôi đã cấu hình lại toàn bộ pipeline lưu trữ dữ liệu, áp dụng chuẩn **UTF-8 (ensure_ascii=False)** cho mọi file JSON và JSONL. 
- **Kết quả:** Đảm bảo 100% dữ liệu tiếng Việt hiển thị hoàn hảo trên cả máy cục bộ và GitHub.

### 3. Thiết lập quy trình Manual Review (Kiểm duyệt thủ công)
- **Sáng kiến:** Vì dữ liệu do AI tạo ra có thể sai sót, tôi đã phát triển bộ công cụ hỗ trợ kiểm duyệt:
    *   `generate_review_report.py`: Tự động chuyển đổi tập dữ liệu thô sang báo cáo Markdown.
    *   `review_dataset.md`: Bảng tổng hợp câu hỏi - câu trả lời - nguồn trích dẫn để con người có thể duyệt nhanh.
- **Mục tiêu:** Đảm bảo tính "Ground Truth" tuyệt đối cho bộ dữ liệu trước khi chạy Benchmark.

### 4. Đồng bộ dữ liệu lên Repository
- **Hành động:** Trực tiếp quản lý việc staging, commit và **force push** toàn bộ thư mục `data/` và `day08/` lên repository của lớp (`mikael-0812`).
- **Kết quả:** Giúp các thành viên khác trong nhóm và giảng viên có thể truy cập ngay lập tức vào bộ dữ liệu chuẩn nhất.

---
*Báo cáo tập trung vào các công việc vừa thực hiện trong phiên làm việc cuối.*
