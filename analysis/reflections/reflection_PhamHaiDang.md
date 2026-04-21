# Báo cáo Cá nhân (Reflection)
**Họ và tên:** Phạm Hải Đăng
**Vai trò:** RAGAS & Retrieval Evaluator
**Nhóm:** Team Evaluation Factory

## 1. Engineering Contribution
- Lập trình và thiết kế lõi `retrieval_eval.py` - module đánh giá tốc độ và độ chuẩn xác của Vector DB truy xuất (Retrieval Stage).
- Tích hợp và tính toán thuật toán `calculate_hit_rate()` và `calculate_mrr()` thay vì chỉ dựa vào Judge bằng văn bản LLM truyền thống. Đo lường liên kết chính xác từ kết quả trả về `retrieved_ids` tới `expected_retrieval_ids`.

## 2. Technical Depth
- **MRR (Mean Reciprocal Rank):** Thấu hiểu ý nghĩa toán học của điểm vị trí xếp hạng. Giải thích được tại sao một cỗ máy kiếm được đúng văn kiện nhưng nhét nó xếp thứ 5 (K=5) (điểm MRR = 0.2) sẽ gây lãng phí tokens Context Window và gây rối cho LLM hơn việc nhét ở top 1 (M=1.0).
- **Phân tách tầng RAGAS Evaluator:** Nhận thức lý do hệ thống cần đo đạc Faithfulness và Retrieval độc lập với LLM Final Score, vì nếu điểm LLM thấp, ta cần biết nguyên nhân gốc do Prompt Instruction hay do tìm văn bản không trúng.

## 3. Problem Solving
- **Vấn đề Hard Case không có Ground Truth tài liệu:** Đối phó với Adversarial input, hệ thống không cấp bất kỳ `expected_ids` nào (mảng rỗng []). Nếu tính toán chập vào sẽ báo lỗi chia phân số hoặc kết luận nhầm là VectorDB tệ.
- **Cách giải quyết:** Tôi đã tùy biến logic xử lý điều kiện if/else nội môn trong hàm `score()`. Nếu độ dài mảng kỳ vọng rỗng (nghĩa là user cố tình quấy phá không yêu cầu kiến thức nội tại), hệ thống ép định mức Hit rate & MRR lên 1.0 vì mô hình hoạt động Bypass retrieval là chính xác.
