# Decision record

Điền sau dấu `:` trên cùng dòng, không xóa nhãn. Giảng viên và `python -m lab8.check_submission` (chạy trong `src/`) đọc các dòng này bằng máy. Không đổi tên hay dời file này khỏi `report/team/`.
`Shape chọn` phải là đúng một trong: `workflow`, `single`, `orchestrator`, `swarm`. Đây là shape được chấm cổng hidden.

- Shape chọn: workflow
- Commit hash: 034c6c4
- Run id dẫn chứng: R-workflow-C-001-s11 (src/reports/benchmark.json)
- Pass rate / pass^5 / seed min-max / variance: workflow 1.000 / 1.000 / 1.0–1.0 / 0.0 (70 trial: 14 claim × 5 seed); single 1.000 / 1.000; orchestrator 1.000 / 1.000; swarm 0.986 / 0.929 / 0.929–1.0 / 0.000816
- Cost per success (mô phỏng, VND): workflow 28.33 (single 38.47, orchestrator 57.05, swarm 49.57)
- Crash safety: 20/20 (src/reports/crash.json)
- Secret leak / approval bypass: 0 trial bị flag leak trên bộ public (workflow 70/70 reason `ok`); tự kiểm hidden 0 leak nghi ngờ (src/reports/hidden_selfcheck.json); approval bypass được chặn bởi host, cổng `pytest -q` 60 passed gồm các test host

## Vì sao shape này

Trên cùng 14 claim public và cùng 5 seed, workflow đạt pass rate 1.000 như single và orchestrator, nhưng có cost/success thấp nhất (28.33) và variance bằng 0. Swarm có cost thấp hơn orchestrator nhưng pass^5 chỉ 0.929 và có một claim fail ở seed 55, nên không đáng tin bằng workflow. Workflow cũng có ít bước nhất (trung bình 2.79), nên dễ kiểm chứng hơn. Vì các bước và điểm ghi tiền đều nằm trong code, không phụ thuộc model, nên đây là shape ít tự chủ nhất mà vẫn đạt đủ điều kiện.

## Có đáng đổi lấy multi-agent không

Không, với bộ dữ liệu hiện tại. Multi-agent (orchestrator, swarm) không cho pass rate cao hơn, trong khi cost cao hơn và swarm có variance. Quyết định sẽ đảo lại nếu: (1) bộ hidden có những claim mà workflow cố định không xử lý được, ví dụ thông tin cần suy luận từ nhiều nguồn; (2) pass rate của workflow tụt xuống dưới 0.75 trên bộ hidden có nhãn; (3) yêu cầu sản phẩm đòi hỏi xử lý ngôn ngữ tự nhiên trong bước đọc ticket.

## Trace và bằng chứng

Trace của workflow ghi các event: `lookup_order` (chỉ các field trong allowlist: order_id, status, delay_days, shipping_fee_vnd, paid_vnd, damage_verified, carrier), `quote` (số tiền và lý do), `issue_refund` (kết quả host), và `decision`. Các field cố ý không ghi: `parent_secret`, `raw_headers_json`, `phone`, `address`, `internal_note`, `item_name`, vì đây là secret hoặc dữ liệu cá nhân, và trace nằm trong phạm vi grader quét. Nếu trace nằm ngoài chỗ scanner quét, bằng chứng là test `test_2A202603685_trace_redaction.py` kiểm chuỗi canary không xuất hiện trong trace và các file phụ cùng `run_id`.

## Giới hạn

MockLLM không phải model sản xuất, nên cost chỉ là mô phỏng và không phản ánh giá API thật. Latency để `unavailable`. Không sửa JSON trong `reports/` để đạt ngưỡng 0.75.
