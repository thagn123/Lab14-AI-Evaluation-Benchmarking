# 🎯 Hướng dẫn thiết kế Hard Cases cho AI Evaluation (Updated)

Để hệ thống RAG đạt chuẩn production, các test cases cần được thiết kế để "phá" logic của Agent. Dưới đây là phân tích các loại Hard Cases dựa trên bộ dữ liệu 70 câu hỏi thực tế:

### 1. Multi-hop Reasoning (Suy luận đa bước)
*   **Ví dụ:** "Nếu sự cố P1 bắt đầu lúc 10:00 AM, deadline viết incident report là mấy giờ ngày hôm sau?"
*   **Tại sao khó:** Agent phải tìm SLA của P1 (4 giờ resolution) → Tính ra thời gian fix sớm nhất (14:00) → Tìm quy định viết report (trong 24h sau fix) → Kết luận (14:00 ngày hôm sau).
*   **Yêu cầu:** Phải truy xuất được 2 chunks khác nhau (`sla_p1_c2` và `sla_p1_c3`).

### 2. Adversarial & Hallucination Risk (Thông tin sai & Nguy cơ bịa đặt)
*   **Ví dụ:** "SLA của ticket P1 là 8 giờ phải không? Tôi nhớ tài liệu cũ ghi vậy."
*   **Tại sao khó:** Người dùng cố tình đưa thông tin sai (8h). Agent phải đối chiếu với tài liệu hiện tại (4h) và đính chính thay vì đồng ý với người dùng.
*   **Yêu cầu:** Agent phải ưu tiên context hơn là kiến thức cũ hoặc câu dẫn dụ của người dùng.

### 3. Edge Cases (Trường hợp biên & Mơ hồ)
*   **Ví dụ:** "Tôi là contractor mới. Vào ngày đầu tôi có quyền truy cập gì?"
*   **Tại sao khó:** Tài liệu có thể dùng từ "Nhân viên" chung chung. Agent phải suy luận xem "Contractor" có thuộc phạm vi áp dụng không (thường là có trong các SOP bảo mật).
*   **Yêu cầu:** Khả năng suy luận (Inference) từ các định nghĩa rộng.

### 4. Retrieval dễ sai (Distractor Chunks)
*   **Ví dụ:** "Quy trình hoàn tiền cho sản phẩm license key."
*   **Tại sao khó:** Một chunk nói về quy trình hoàn tiền chung, một chunk nói về các ngoại lệ (License key không được hoàn tiền). Retriever dễ chỉ lấy chunk quy trình mà bỏ qua chunk ngoại lệ.
*   **Yêu cầu:** Agent phải đọc cả 2 để trả lời chính xác là "Không được hoàn tiền".

---
*Lưu ý: Bộ dữ liệu `golden_set.jsonl` đã bao gồm đầy đủ các loại câu hỏi trên.*
