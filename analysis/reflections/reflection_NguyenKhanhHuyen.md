# Báo cáo Cá nhân (Reflection)
**Họ và tên:** Nguyễn Khánh Huyền
**Vai trò:** Synthetic Data Gen & Vulnerability Testing
**Nhóm:** Team Evaluation Factory

## 1. Engineering Contribution
- Phụ trách chính trị liệu luồng dữ liệu đánh giá `data/synthetic_gen.py`.
- Tự thiết kế một Golden Dataset vượt xa mức bài tập cơ bản bằng cách bện hàm tự động nhồi đủ 3 chủng loại: Chủng loại tiêu chuẩn (Standard Cases 60%), Chủng loại biên tối (Edge Cases 20%) và Chủng loại đầu độc (Adversarial Prompts 20%) theo phân nhóm chỉ định. Đảm bảo Pipeline đánh giá Agent đủ sát với đời thực.

## 2. Technical Depth
- **Hallucination & Position Bias:** Lên khung định hình chiến thuật kiểm tra LLM. Hiểu vì sao có những câu hỏi Agent lại "Bịa chuyện" do System prompt yếu, tôi đã cung cấp các Edge case ("tổng thống của sao Hỏa vào năm 2050") để bắt Agent phải đầu hàng nói Không biết.
- **Data Mapping Analysis:** Nắm cấu trúc Schema JSONL nhằm nối chính xác `expected_answer` và Ground truth ID, thiết lập nền móng tiên phong giúp bạn Đăng làm Evaluator RAG rất thuận tay.

## 3. Problem Solving
- **Vấn đề Báo Cáo Không Chứa 5 Whys:** Trong quá trình chạy Test, Agent thường cho kết quả Failure ngớ ngẩn (vd: Làm thơ chính trị) và rất khó truy gốc nguyên nhân do lượng log lớn.
- **Cách giải quyết:** Chắp bút trực tiếp viết phần `Failure Clustering` và phương pháp truy tìm vết `5 Whys` cực sắc bén liệt kê vào `analysis/failure_analysis.md`. Viết kế hoạch chốt Action plan chặn Prompt Injection bằng Boundary (Threshold Vector & Guardrails).
