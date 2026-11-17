# Báo cáo cá nhân — 2A202603685_DangVietAnh

> Bản gợi ý do AI soạn. Bạn cần đọc lại và viết bằng lời của mình, đặc biệt phần Tự đánh giá. Các chỗ trong ngoặc vuông `[...]` là thông tin bạn phải tự điền từ git và file báo cáo.

## 1. Thông tin thành viên

- Họ tên: Đặng Việt Anh
- MSSV: 2A202603685
- Email: 26ai.anhdv3@vinuni.edu.vn
- GitHub: anhdv282

## 2. Phần việc phụ trách

Nhóm 1 người nên tôi phụ trách toàn bộ phần kỹ thuật:

- Ba shape `workflow.py`, `single.py`, `orchestrator.py` (CP2, CP3).
- Chạy và đọc kết quả crash suite (CP4), benchmark và tự kiểm trên `student_drop/` (CP5).
- Viết ADR, research card, báo cáo nhóm và báo cáo cá nhân.

## 3. Đóng góp cụ thể

- Viết ba shape theo hướng dẫn trong docstring. Cả ba đều gọi `durability.issue_refund` với quote đầy đủ và truyền `crash_at` xuyên qua, không bắt `InjectedCrash`.
- Kết quả: student test từ 186 failed xuống còn 248 passed, cổng host `pytest -q` xanh (54 passed).
- Commit chính: 034c6c4
- Test đã thêm hoặc sửa: `test_2A202603685_trace_redaction.py::test_canary_secret_never_reaches_trace` (test cá nhân, không gắn marker `student`).
- Quyết định kỹ thuật: Shape mình chọn là workflow vì tỷ lệ pass cao. Số liệu benchmark gợi ý workflow có cost/success thấp nhất (28.33) và variance bằng 0. Đây là gợi ý từ số liệu, quyết định là của bạn.

## 4. Bằng chứng

- Crash suite: `src/reports/crash.json`, `crash_safety` = 20/20.
- Benchmark: `src/reports/benchmark.json`, 4 shape × 14 claim × 5 seed, run id `[lấy từ benchmark.json]`.
- Tự kiểm hidden: `src/reports/hidden_selfcheck.json`, 40 claim × 3 shape × 5 seed, không có leak nghi ngờ và không có exception. Không có pass rate vì bộ này không có nhãn.
- Link commit: 

## 5. Công cụ AI đã dùng

- Trợ lý AI (Claude Code) đã viết phần lớn code trong ba shape, đọc các file trong repo để giải thích kiến trúc, và soạn bản nháp của một số tài liệu.
- Cách tự kiểm tra: chạy lại `pytest`, `lab8.crash_test`, `lab8.benchmark`, và `lab8.check_submission` trên máy của tôi; đọc từng shape để hiểu cách hoạt động; không dùng số liệu nào mà AI soạn ra mà không kiểm tra lại từ file JSON do công cụ sinh ra.
- `[Bổ sung: bạn đã đọc và sửa đến mức nào, phần nào bạn tự viết.]`

## 6. Tự đánh giá

Gợi ý, bạn cần viết lại bằng lời của mình:

- Điều đã học: vì sao ghi tiền phải nằm ở host và không phụ thuộc shape; vì sao idempotency và ledger quan trọng hơn checkpoint đơn lẻ; cách đo kiến trúc bằng pass rate, variance và cost.
- Điều chưa làm tốt: 
- Nếu làm lại: 
