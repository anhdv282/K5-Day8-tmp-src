# Research card

File này nằm cố định ở `report/team/research_card.md`; `python -m lab8.check_submission` đọc cột "Nhóm điền" bằng máy.

Phần này nối tiếp phần mini research ở buổi lý thuyết (slide 62–63). Chọn **một** câu R1–R4, điền 6 dòng, rồi biến nó thành **một ablation** chạy được trong lab: giữ nguyên model (MockLLM), tool, seed, corpus và giá, chỉ thay đổi một biến.

| Câu | Nguồn (thư viện tham khảo, slide 68–69) | Câu hỏi gợi ý cho lab |
| --- | --- | --- |
| R1 · Scaling | Google Research 2026, *Towards a Science of Scaling Agent Systems* | Task claims chủ yếu tuần tự hay song song được? Dự đoán thêm investigator sẽ làm pass rate và cost/success thay đổi thế nào. |
| R2 · Failure taxonomy | MAST, NeurIPS 2025, *Why Do Multi-Agent LLM Systems Fail?* | Các trial fail của swarm (seed 55) thuộc nhóm nào: lỗi giao việc, lệch mục tiêu, hay lỗi kiểm chứng? |
| R3 · Architecture choices | AgentArch, AACL 2026 | Nếu đổi topology mà giữ nguyên mọi thứ khác, biến nào phải cố định để kết luận còn đúng? |
| R4 · Evaluation confounders | EMNLP 2026, *Rethinking Evaluation of MAS Efficiency* | Làm sao chứng minh chênh lệch giữa A/B/C/D là do topology, không phải do prompt, tool hay seed? |

## Phiếu của nhóm

Điền vào cột cuối. Không xóa hai cột đầu.

| Field | Hướng dẫn | Nhóm điền |
| --- | --- | --- |
| CÂU | R1 / R2 / R3 / R4 | R2 · Failure taxonomy |
| SOURCE | Paper/blog, năm, URL, loại bằng chứng (benchmark, production report, blog kinh nghiệm) | [CHƯA ĐIỀN. Tác giả cần mở slide 68–69 hoặc paper MAST để lấy tên, năm, URL và loại bằng chứng. AI không xác minh được nội dung này.] |
| CLAIM | Một kết luận gốc của nguồn. Không viết rộng hơn phạm vi paper | [CHƯA ĐIỀN. Tác giả đọc paper rồi tự viết, không dùng câu của AI.] |
| BOUNDARY | Model / dataset / setup giới hạn kết luận đó | [CHƯA ĐIỀN. Tác giả điền sau khi đọc paper.] |
| HYPOTHESIS | Nếu đổi shape A→B (hoặc bật/tắt một thành phần), metric X sẽ đổi theo hướng nào, khoảng bao nhiêu | Nếu bật bước kiểm chứng bằng code (đối chiếu `delay_days` từ ticket với DB trước khi quote) trong swarm, thì swarm sẽ pass `C-002` ở seed 55, pass^5 tăng từ 0.929 lên 1.000, và pass rate tăng từ 0.986 lên 1.000. Cost/success tăng nhẹ vì thêm một bước kiểm tra. |
| METHOD | Biến giữ cố định: model, tools, seed, corpus, giá, evaluator. Biến duy nhất được thay đổi: … | Giữ cố định: MockLLM, tool, seed 11–55, corpus public, bảng giá, evaluator. Biến duy nhất thay đổi: bật hoặc tắt bước kiểm chứng `delay_days` theo DB. Thực hiện bằng bản sao của swarm trong bonus (`swarm_verified`) hoặc chỉnh tạm trong scratch, không commit. |
| FAILURE / METRIC | Một lỗi dự kiến và cách đo nó: pass rate, pass^5, variance, cost/success, leak, bypass | Lỗi dự kiến: lỗi kiểm chứng, peer tin số ngày trong ticket thay vì DB khi `seed % 5 == 0`. Đo bằng pass rate, pass^5, variance trên 14 claim × 5 seed. |

## Kết quả ablation

- Lệnh đã chạy (copy nguyên văn):
  ```bash
  python -m lab8.benchmark --shapes workflow,single,orchestrator,swarm --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/benchmark.json
  ```
- Run id / file report: `R-swarm-C-002-s55` trong `src/reports/benchmark.json`. Tôi chưa chạy bản swarm đã sửa, nên đây là kết quả baseline, chưa phải ablation hoàn chỉnh.
- Kết quả so với hypothesis: **chưa kết luận được** đầy đủ, vì chưa có bản swarm có bước kiểm chứng để so sánh. Quan sát có sẵn: swarm chỉ có 1 trial fail trên 70 (`C-002`, seed 55, `status resolved != denied`), đúng seed `% 5 == 0` mà `docs/metrics.md` nêu. Điều này khớp với lỗi kiểm chứng, nhưng cần ablation để xác nhận nhân quả.
- Giới hạn: MockLLM không phải model sản xuất, latency là `unavailable`. Chỉ có một trial fail nên chưa đủ để nói về phân bố lỗi.

> Ghi chú cho tác giả: phần HYPOTHESIS, METHOD và FAILURE là bản nháp do AI soạn từ dữ liệu trong repo. Bạn cần đọc, hiểu, và sửa bằng lời của mình. Ba dòng SOURCE, CLAIM, BOUNDARY bạn phải tự điền từ nguồn thật. Nếu muốn hoàn chỉnh ablation, bạn có thể làm theo gợi ý bonus `swarm_verified` trong `docs/bonus_topics.md`, nhưng không commit bản sửa vào `src/lab8/shapes/swarm_reference.py`.

Muốn đi xa hơn một ablation để lấy điểm cộng thì xem [docs/bonus_topics.md](../../docs/bonus_topics.md).
