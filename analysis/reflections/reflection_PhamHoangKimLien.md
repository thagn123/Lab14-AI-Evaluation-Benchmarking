# Báo cáo Cá nhân (Reflection)
**Họ và tên:** Phạm Hoàng Kim Liên
**Vai trò:** LLM Consensus & Judging System
**Nhóm:** Team Evaluation Factory

## 1. Engineering Contribution
- Xây dựng module `llm_judge.py` xử lý hai mô hình giám khảo khác nhau (GPT-4o và Claude 3.5).
- Phát triển logic tính `Agreement Rate` (Độ đồng thuận chéo) và quy tắc phạt chênh lệch điểm (nếu điểm lệch lớn hơn 1 điểm). Chuyển logic điểm số này thành API đánh giá trung bình.

## 2. Technical Depth
- **Cohen's Kappa & Consensus Rate:** Ứng dụng bản sao logic Cohen's Kappa để đánh giá tính cực đoan của một mô hình Language Model trong việc đánh giá LLM khác (LLM-as-a-judge). 
- **Cost Efficiency:** Giải thích tại sao việc dùng nhiều model giá rẻ (như GPT-4o-mini và Claude 3.5 Haiku) ở lớp filter đầu rất hiệu quả về kinh tế so với việc nhét mọi thứ qua GPT-4o mà không suy tính.

## 3. Problem Solving
- **Vấn đề mô hình giám khảo bất đồng quan điểm:** Khi một Judge khắt khe cho 3 điểm, còn người khác châm trước cho 5 điểm.
- **Cách giải quyết:** Áp dụng ràng buộc khoảng cách tin cậy `diff > 1`. Nếu sự lệch phân quá lớn tôi không dùng trung bình cộng mà sử dụng hàm `min()` để lấy điểm thấp nhất phạt con Agent, đồng thời ghi nhận Agreement Rate là `0.0`. Điều này chặn triệt để hiện tượng gian lận điểm từ một Judge ảo bảo vệ Agent V2 một cách mù quáng.
