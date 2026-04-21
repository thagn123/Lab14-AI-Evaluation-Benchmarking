# 📂 Thư mục Data: Lab 14 AI Evaluation

Thư mục này chứa bộ dữ liệu chuẩn (Golden Dataset) và các công cụ bổ trợ để xây dựng hệ thống đánh giá RAG Agent.

## 📄 Danh sách tệp tin

1.  **`golden_set.jsonl`**: Bộ dữ liệu gồm **70 test cases** chuẩn (Easy, Medium, Hard, Multi-hop, Adversarial). Đây là đầu vào chính cho pipeline đánh giá.
2.  **`vector_db.json`**: Chứa 29 text chunks được trích xuất từ các tài liệu thực tế của `day08`. Mỗi chunk có `chunk_id` duy nhất.
3.  **`review_dataset.md`**: Báo cáo định dạng Markdown để con người dễ dàng kiểm tra lại chất lượng câu hỏi/trả lời của AI.
4.  **`synthetic_gen.py`**: Script sử dụng OpenAI/Gemini để sinh dữ liệu tự động từ các tài liệu PDF/Text.
5.  **`generate_review_report.py`**: Công cụ chuyển đổi từ `.jsonl` sang `.md` để phục vụ bước **Manual Review**.
6.  **`HARD_CASES_GUIDE.md`**: Hướng dẫn thiết kế các trường hợp kiểm thử khó để thử thách Agent.

## 🛠 Cách sử dụng

### 1. Sinh dữ liệu mới (nếu cần)
Nếu bạn thay đổi tài liệu trong `day08/lab/data/docs/`, hãy chạy lại:
```bash
python data/synthetic_gen.py
```

### 2. Kiểm tra thủ công (Manual Review)
Đây là bước **bắt buộc** để đảm bảo AI sinh dữ liệu không bị lỗi:
1. Chạy `python data/generate_review_report.py`.
2. Mở `data/review_dataset.md` để xem bảng câu hỏi.
3. Nếu thấy câu nào sai, hãy sửa trực tiếp trong `golden_set.jsonl`.

### 3. Chạy đánh giá (Benchmark)
Từ thư mục gốc, chạy:
```bash
python main.py
```

## ⚠️ Lưu ý về Encoding
Tất cả các file đều được lưu ở định dạng **UTF-8 (ensure_ascii=False)** để hiển thị chính xác tiếng Việt. Tuyệt đối không lưu file bằng các trình soạn thảo làm thay đổi encoding này.
