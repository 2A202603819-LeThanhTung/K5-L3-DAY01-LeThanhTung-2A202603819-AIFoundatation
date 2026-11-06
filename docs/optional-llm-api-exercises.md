# Ngày 1 — Bài Tập & Phản Ánh (side lab TUỲ CHỌN)

> Side lab này **không** thuộc điểm chính của Day 01 (xem [RUBRIC.md](../RUBRIC.md) mục Bonus). Model: `gpt-6.1-terra` (lớn) và `gpt-6-luna` (nhỏ). `gpt-4o` / `gpt-4o-mini` bị gỡ khỏi API ngày 14/01/2027 ([nguồn](https://developers.openai.com/api/docs/deprecations)). Tên khoá `gpt4o_*` / `mini_*` trong kết quả là hợp đồng của test, giữ nguyên để tương thích: đọc là "model lớn" / "model nhỏ".
## Nền Tảng LLM API | Phiếu Thực Hành

**Thời lượng:** 1:30 giờ  
**Cấu trúc:** Lập trình cốt lõi (60 phút) → Bài tập mở rộng (30 phút)

---

## Phần 1 — Lập Trình Cốt Lõi (0:00–1:00)

Chạy các ví dụ trong Google Colab tại: https://colab.research.google.com/drive/172zCiXpLr1FEXMRCAbmZoqTrKiSkUERm?usp=sharing

Copy `src/optional_llm_api/template.py` thành `src/optional_llm_api/solution/solution.py`, triển khai mọi TODO, rồi chạy từ gốc repo: `pytest tests/test_solution.py -v`. Chưa có `solution/solution.py` thì test tự bỏ qua.

**Điểm kiểm tra:** Sau khi hoàn thành 4 nhiệm vụ, chạy:
```bash
python src/optional_llm_api/solution/solution.py
```
Bạn sẽ thấy output so sánh phản hồi của `gpt-6.1-terra` và `gpt-6-luna`.

---

## Phần 2 — Bài Tập Mở Rộng (1:00–1:30)

### Bài tập 2.1 — Độ Nhạy Của Temperature
Gọi `call_openai` với các giá trị temperature 0.0, 0.5, 1.0 và 1.5 sử dụng prompt **"Hãy kể cho tôi một sự thật thú vị về Việt Nam."** (nhớ gửi `reasoning_effort="none"`: model GPT-6 chỉ nhận `temperature` khi tắt suy luận)

**Bạn nhận thấy quy luật gì qua bốn phản hồi?** (2–3 câu)
> Khi temperature = 0.0, câu trả lời mang tính tất định, các lần chạy đều đưa ra sự thật phổ biến nhất (ví dụ: Việt Nam là nước xuất khẩu hạt điều/cà phê hàng đầu) với cấu trúc câu chuẩn mực, súc tích. Khi temperature tăng lên 0.5 - 1.0, cách hành văn trở nên phong phú hơn, giới thiệu các sự thật đa dạng về văn hoá, hang Sơn Đoòng. Khi temperature = 1.5, câu chữ mang tính ngẫu hứng cao, dùng nhiều từ ngữ hoa mỹ hoặc có thể xuất hiện câu văn thiếu tự nhiên.

**Bạn sẽ đặt temperature bao nhiêu cho chatbot hỗ trợ khách hàng, và tại sao?**
> Với chatbot hỗ trợ khách hàng, em sẽ đặt temperature thấp trong khoảng 0.0 đến 0.2. Vì trong kịch bản chăm sóc khách hàng, tính chính xác, nhất quán và đáng tin cậy về chính sách, giá cả là quan trọng nhất; cần hạn chế tối đa việc mô hình tự bịa đặt thông tin (hallucination).

---

### Bài tập 2.2 — Đánh Đổi Chi Phí
Xem xét kịch bản: 10.000 người dùng hoạt động mỗi ngày, mỗi người thực hiện 3 lần gọi API, mỗi lần trung bình ~350 token.

**Ước tính xem `gpt-6.1-terra` đắt hơn `gpt-6-luna` bao nhiêu lần cho workload này** (giá 11/2026: terra $1.00 / $5.00, luna $0.10 / $0.50 mỗi 1M token input / output):
> Tổng lượt gọi mỗi ngày: 10.000 * 3 = 30.000 lượt gọi. Tổng token mỗi ngày: 30.000 * 350 = 10.500.000 tokens (10.5M tokens). Tỷ lệ giá token giữa terra ($1.00/$5.00) và luna ($0.10/$0.50) đều chênh lệch đúng 10 lần ở cả input và output. Do đó, model `gpt-6.1-terra` sẽ đắt hơn `gpt-6-luna` đúng 10 lần cho toàn bộ workload này (chênh lệch từ khoảng vài USD lên vài chục USD mỗi ngày).

**Mô tả một trường hợp mà chi phí cao hơn của `gpt-6.1-terra` là xứng đáng, và một trường hợp `gpt-6-luna` là lựa chọn tốt hơn:**
> - Chi phí cao của `gpt-6.1-terra` xứng đáng khi dùng cho các tác vụ đòi hỏi lập luận logic phức tạp, viết code chuyên sâu, phân tích hợp đồng pháp lý hoặc tư vấn chiến lược kinh doanh đa bước.
> - `gpt-6-luna` là lựa chọn tốt hơn và tiết kiệm hơn nhiều cho các tác vụ downstream lặp đi lặp lại như: phân loại intent tin nhắn rác/chăm sóc khách hàng, trích xuất thực thể (NER), tóm tắt nhanh văn bản ngắn hoặc kiểm tra chính tả.

---

### Bài tập 2.3 — Trải Nghiệm Người Dùng với Streaming
**Streaming quan trọng nhất trong trường hợp nào, và khi nào thì non-streaming lại phù hợp hơn?** (1 đoạn văn)
> Streaming quan trọng nhất trong các ứng dụng đối thoại trực tiếp với người dùng (như giao diện chat tương tác, trợ lý ảo thời gian thực), giúp giảm thời gian chờ đợi phản hồi đầu tiên (Time to First Token - TTFT) xuống dưới 1 giây, tạo cảm giác phản hồi tức thì và nâng cao trải nghiệm người dùng. Ngược lại, non-streaming phù hợp hơn cho các tác vụ xử lý hàng loạt chạy ngầm (batch processing), các endpoint API trả về JSON có cấu trúc nghiêm ngặt để hệ thống backend khác đọc trực tiếp (như phân loại nhãn, chấm điểm, tự động hoá quy trình), nơi không có người dùng trực tiếp ngồi nhìn màn hình.

---

## Danh Sách Kiểm Tra Nộp Bài
- [x] Tất cả tests pass: `pytest tests/test_solution.py -v`
- [x] `call_openai` đã triển khai và kiểm thử
- [x] `call_openai_mini` đã triển khai và kiểm thử
- [x] `compare_models` đã triển khai và kiểm thử
- [x] `streaming_chatbot` đã triển khai và kiểm thử
- [x] `retry_with_backoff` đã triển khai và kiểm thử
