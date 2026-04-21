# 📋 Manual Review: Golden Dataset (70 cases)

> [!IMPORTANT]
> Please review the Q/A pairs, ground truth IDs, and sources below.
> Mark incorrect cases for correction.

| # | Question | Expected Answer | Ground Truth ID | Source | Diff |
|---|---|---|---|---|---|
| 1 | Sự cố nào được xếp loại là P1? | Sự cố ảnh hưởng toàn bộ hệ thống production, không có workaround. | sla_p1_2026_c25 | support/sla-p1-2026.pdf | easy |
| 2 | Thời gian phản hồi ban đầu cho ticket P2 là bao lâu? | 2 giờ. | sla_p1_2026_c26 | support/sla-p1-2026.pdf | easy |
| 3 | Quy trình xử lý sự cố P1 bắt đầu từ bước nào? | Bước 1: Tiếp nhận. | sla_p1_2026_c27 | support/sla-p1-2026.pdf | easy |
| 4 | Thời gian tối đa để escalate ticket P1 là bao lâu? | 10 phút. | sla_p1_2026_c26 | support/sla-p1-2026.pdf | easy |
| 5 | Nếu không có phản hồi sau 90 phút cho ticket P2, điều gì sẽ xảy ra? | Tự động escalate. | sla_p1_2026_c26 | support/sla-p1-2026.pdf | medium |
| 6 | Thời gian tối đa để xử lý và khắc phục ticket P3 là gì? | 1 ngày làm việc. | sla_p1_2026_c26 | support/sla-p1-2026.pdf | medium |
| 7 | Quy trình thông báo cho ticket P1 cần làm gì? | Gửi thông báo tới Slack #incident-p1 và email incident@company.internal ngay lập tức. | sla_p1_2026_c27 | support/sla-p1-2026.pdf | medium |
| 8 | Cập nhật SLA P1 resolution từ 6 giờ xuống 4 giờ diễn ra vào ngày nào? | 2026-01-15. | sla_p1_2026_c29 | support/sla-p1-2026.pdf | medium |
| 9 | Sau khi khắc phục sự cố, engineer cần làm gì trong vòng 24 giờ? | Viết incident report. | sla_p1_2026_c27 | support/sla-p1-2026.pdf | hard |
| 10 | Mỗi khi có ticket P1 mới, ai sẽ được nhắn tin tự động? | On-call engineer. | sla_p1_2026_c28 | support/sla-p1-2026.pdf | hard |
| 11 | Các kênh Slack nào được sử dụng để thông báo sự cố? | #incident-p1 và #incident-p2. | sla_p1_2026_c28 | support/sla-p1-2026.pdf | multi_hop |
| 12 | Nếu một số tính năng không hoạt động nhưng có workaround, sự cố đó thuộc loại nào? | P2 — HIGH (Nghiêm trọng). | sla_p1_2026_c25 | support/sla-p1-2026.pdf | multi_hop |
| 13 | Nếu engineer không cập nhật tiến độ ticket P1 trong 30 phút, điều gì sẽ xảy ra? | Cần phải escalate ngay. | sla_p1_2026_c27 | support/sla-p1-2026.pdf | adversarial |
| 14 | Chính sách hoàn tiền này bắt đầu áp dụng từ ngày nào? | 01/02/2026 | policy_refund_v4_c19 | policy/refund-v4.pdf | easy |
| 15 | Khách hàng cần làm gì để yêu cầu hoàn tiền? | Gửi yêu cầu qua hệ thống ticket nội bộ với category 'Refund Request'. | policy_refund_v4_c22 | policy/refund-v4.pdf | easy |
| 16 | Có những điều kiện nào để khách hàng được yêu cầu hoàn tiền? | Sản phẩm bị lỗi do nhà sản xuất, yêu cầu gửi trong vòng 7 ngày làm việc và đơn hàng chưa được sử dụng hoặc mở seal. | policy_refund_v4_c20 | policy/refund-v4.pdf | easy |
| 17 | Sản phẩm nào không đủ điều kiện hoàn tiền? | Sản phẩm thuộc danh mục hàng kỹ thuật số, đơn hàng đã áp dụng mã giảm giá Flash Sale, sản phẩm đã được kích hoạt. | policy_refund_v4_c21 | policy/refund-v4.pdf | easy |
| 18 | Quy trình hoàn tiền mất bao lâu? | Finance Team xử lý trong 3-5 ngày làm việc. | policy_refund_v4_c22 | policy/refund-v4.pdf | medium |
| 19 | Khách hàng có thể nhận hoàn tiền qua phương thức nào? | Qua phương thức thanh toán gốc hoặc qua credit nội bộ. | policy_refund_v4_c23 | policy/refund-v4.pdf | medium |
| 20 | Nếu khách hàng chọn nhận store credit, giá trị hoàn tiền là bao nhiêu phần trăm? | 110% so với số tiền hoàn. | policy_refund_v4_c23 | policy/refund-v4.pdf | medium |
| 21 | Thời gian làm việc của bộ phận hỗ trợ hoàn tiền là gì? | Thứ 2 - Thứ 6, 8:00 - 17:30. | policy_refund_v4_c24 | policy/refund-v4.pdf | hard |
| 22 | Nếu sản phẩm bị lỗi do người dùng, khách hàng có được hoàn tiền không? | Không. | policy_refund_v4_c20 | policy/refund-v4.pdf | hard |
| 23 | Khách hàng cần gửi yêu cầu hoàn tiền trong vòng bao lâu sau khi xác nhận đơn hàng? | 7 ngày làm việc. | policy_refund_v4_c20 | policy/refund-v4.pdf | multi_hop |
| 24 | Nếu sản phẩm đã được kích hoạt, khách hàng có thể yêu cầu hoàn tiền không? | Không. | policy_refund_v4_c21 | policy/refund-v4.pdf | multi_hop |
| 25 | Địa chỉ email nào khách hàng cần liên hệ để yêu cầu hoàn tiền? | cs-refund@company.internal | policy_refund_v4_c24 | policy/refund-v4.pdf | adversarial |
| 26 | Nếu khách hàng không gửi yêu cầu trong vòng 7 ngày, họ có thể nhận hoàn tiền không? | Không. | policy_refund_v4_c20 | policy/refund-v4.pdf | adversarial |
| 27 | Tài liệu nào quy định quy trình cấp phép truy cập vào hệ thống nội bộ của công ty? | Tài liệu này quy định quy trình cấp phép truy cập vào các hệ thống nội bộ của công ty. | access_control_sop_c1 | it/access-control-sop.md | easy |
| 28 | Ai là người phê duyệt yêu cầu cấp quyền cho nhân viên mới trong 30 ngày đầu? | Line Manager. | access_control_sop_c2 | it/access-control-sop.md | easy |
| 29 | Quy trình cấp quyền cho nhân viên chính thức đã qua thử việc mất bao lâu? | 2 ngày làm việc. | access_control_sop_c2 | it/access-control-sop.md | easy |
| 30 | Bước đầu tiên trong quy trình cấp phép truy cập là gì? | Nhân viên tạo Access Request ticket trên Jira (project IT-ACCESS). | access_control_sop_c3 | it/access-control-sop.md | easy |
| 31 | Làm thế nào để cấp quyền tạm thời trong trường hợp khẩn cấp? | On-call IT Admin có thể cấp quyền tạm thời (max 24 giờ) sau khi được Tech Lead phê duyệt bằng lời. | access_control_sop_c4 | it/access-control-sop.md | medium |
| 32 | Quyền truy cập cần được thu hồi trong trường hợp nào? | Nhân viên nghỉ việc, hết hạn contract, chuyển bộ phận. | access_control_sop_c5 | it/access-control-sop.md | medium |
| 33 | Mỗi khi có bất thường trong access review, ai là người cần được báo cáo? | CISO. | access_control_sop_c6 | it/access-control-sop.md | medium |
| 34 | Quy trình nào áp dụng khi cần thay đổi quyền hệ thống ngoài quy trình thông thường? | Quy trình escalation khẩn cấp. | access_control_sop_c4 | it/access-control-sop.md | hard |
| 35 | Sau bao lâu thì quyền tạm thời sẽ bị thu hồi nếu không có ticket chính thức? | 24 giờ. | access_control_sop_c4 | it/access-control-sop.md | hard |
| 36 | Hệ thống nào được sử dụng để tạo ticket cho yêu cầu cấp quyền? | Jira (project IT-ACCESS). | access_control_sop_c7 | it/access-control-sop.md | multi_hop |
| 37 | Nếu nhân viên chuyển bộ phận, quyền truy cập cần được điều chỉnh trong bao lâu? | 3 ngày làm việc. | access_control_sop_c5 | it/access-control-sop.md | multi_hop |
| 38 | Nếu một nhân viên nghỉ việc, quyền truy cập của họ sẽ được thu hồi như thế nào? | Thu hồi ngay trong ngày cuối. | access_control_sop_c5 | it/access-control-sop.md | adversarial |
| 39 | Nhân viên có bao nhiêu ngày nghỉ phép năm nếu họ có dưới 3 năm kinh nghiệm? | 12 ngày/năm | hr_leave_policy_c8 | hr/leave-policy-2026.pdf | easy |
| 40 | Nếu nhân viên muốn nghỉ ốm trên 3 ngày liên tiếp, họ cần gì? | Cần giấy tờ y tế từ bệnh viện. | hr_leave_policy_c8 | hr/leave-policy-2026.pdf | easy |
| 41 | Nhân viên cần làm gì để yêu cầu nghỉ phép? | Gửi yêu cầu nghỉ phép qua hệ thống HR Portal ít nhất 3 ngày làm việc trước ngày nghỉ. | hr_leave_policy_c9 | hr/leave-policy-2026.pdf | easy |
| 42 | Hệ số lương làm thêm cho ngày cuối tuần là bao nhiêu? | 200% lương giờ tiêu chuẩn. | hr_leave_policy_c10 | hr/leave-policy-2026.pdf | medium |
| 43 | Điều kiện nào cần có để nhân viên làm việc từ xa? | Nhân viên sau probation period có thể làm remote tối đa 2 ngày/tuần. | hr_leave_policy_c11 | hr/leave-policy-2026.pdf | medium |
| 44 | Nhân viên phải làm gì khi nghỉ phép trong trường hợp khẩn cấp? | Gửi yêu cầu muộn hơn nhưng phải được Line Manager đồng ý qua tin nhắn trực tiếp. | hr_leave_policy_c9 | hr/leave-policy-2026.pdf | medium |
| 45 | Có bao nhiêu ngày nghỉ phép năm được chuyển sang năm tiếp theo? | Tối đa 5 ngày phép năm chưa dùng được chuyển sang năm tiếp theo. | hr_leave_policy_c8 | hr/leave-policy-2026.pdf | hard |
| 46 | Nhân viên cần bật gì trong các cuộc họp team khi làm việc từ xa? | Camera bật trong các cuộc họp team. | hr_leave_policy_c11 | hr/leave-policy-2026.pdf | hard |
| 47 | Nếu nhân viên làm thêm giờ vào ngày lễ, họ sẽ nhận được bao nhiêu phần trăm lương? | 300% lương giờ tiêu chuẩn. | hr_leave_policy_c10 | hr/leave-policy-2026.pdf | multi_hop |
| 48 | Khi nào nhân viên cần thông báo cho Line Manager trong trường hợp nghỉ ốm? | Thông báo cho Line Manager trước 9:00 sáng ngày nghỉ. | hr_leave_policy_c8 | hr/leave-policy-2026.pdf | multi_hop |
| 49 | Giờ làm việc của HR là gì? | Thứ 2 - Thứ 6, 8:30 - 17:30. | hr_leave_policy_c12 | hr/leave-policy-2026.pdf | adversarial |
| 50 | Địa chỉ email của HR là gì? | hr@company.internal | hr_leave_policy_c12 | hr/leave-policy-2026.pdf | adversarial |
| 51 | Tôi quên mật khẩu, phải làm gì? | Truy cập https://sso.company.internal/reset hoặc liên hệ Helpdesk qua ext. 9000. Mật khẩu mới sẽ được gửi qua email công ty trong vòng 5 phút. | it_helpdesk_faq_c13 | support/helpdesk-faq.md | easy |
| 52 | Tài khoản bị khóa sau bao nhiêu lần đăng nhập sai? | Tài khoản bị khóa sau 5 lần đăng nhập sai liên tiếp. Để mở khóa, liên hệ IT Helpdesk hoặc tự reset qua portal SSO. | it_helpdesk_faq_c13 | support/helpdesk-faq.md | easy |
| 53 | Công ty sử dụng phần mềm VPN nào? | Công ty sử dụng Cisco AnyConnect. Download tại https://vpn.company.internal/download. | it_helpdesk_faq_c14 | support/helpdesk-faq.md | easy |
| 54 | Tôi bị mất kết nối VPN liên tục, phải làm gì? | Kiểm tra kết nối Internet trước. Nếu vẫn lỗi, tạo ticket P3 với log file VPN đính kèm. | it_helpdesk_faq_c14 | support/helpdesk-faq.md | medium |
| 55 | Laptop mới được cấp sau bao lâu khi vào công ty? | Laptop được cấp trong ngày onboarding đầu tiên. Nếu có vấn đề, liên hệ HR hoặc IT Admin. | it_helpdesk_faq_c16 | support/helpdesk-faq.md | medium |
| 56 | Laptop bị hỏng phải báo cáo như thế nào? | Tạo ticket P2 hoặc P3 tùy mức độ nghiêm trọng. Mang thiết bị đến IT Room (tầng 3) để kiểm tra. | it_helpdesk_faq_c16 | support/helpdesk-faq.md | medium |
| 57 | Tôi cần cài phần mềm mới, phải làm gì? | Gửi yêu cầu qua Jira project IT-SOFTWARE. Line Manager phải phê duyệt trước khi IT cài đặt. | it_helpdesk_faq_c15 | support/helpdesk-faq.md | hard |
| 58 | Hộp thư đến đầy, phải làm gì? | Xóa email cũ hoặc yêu cầu tăng dung lượng qua ticket IT-ACCESS. Dung lượng tiêu chuẩn là 50GB. | it_helpdesk_faq_c17 | support/helpdesk-faq.md | hard |
| 59 | Tôi không nhận được email từ bên ngoài, phải làm gì? | Kiểm tra thư mục Spam trước. Nếu vẫn không có, tạo ticket P2 kèm địa chỉ email gửi và thời gian gửi. | it_helpdesk_faq_c17 | support/helpdesk-faq.md | multi_hop |
| 60 | Ai chịu trách nhiệm gia hạn license phần mềm? | IT Procurement team quản lý tất cả license. Nhắc nhở sẽ được gửi 30 ngày trước khi hết hạn. | it_helpdesk_faq_c15 | support/helpdesk-faq.md | multi_hop |
| 61 | Quy trình cấp phép truy cập vào hệ thống nội bộ của công ty áp dụng cho ai? | Áp dụng cho tất cả nhân viên, contractor, và third-party vendor. | access_control_sop_c1 | it/access-control-sop.md | medium |
| 62 | Mức độ truy cập nào áp dụng cho nhân viên mới trong 30 ngày đầu? | Level 1 — Read Only. | access_control_sop_c2 | it/access-control-sop.md | easy |
| 63 | Quy trình escalation khẩn cấp áp dụng khi nào? | Khi cần thay đổi quyền hệ thống ngoài quy trình thông thường. | access_control_sop_c4 | it/access-control-sop.md | hard |
| 64 | Nếu nhân viên nghỉ việc, quyền truy cập sẽ được thu hồi như thế nào? | Thu hồi ngay trong ngày cuối. | access_control_sop_c5 | it/access-control-sop.md | easy |
| 65 | Quy trình gửi yêu cầu nghỉ phép qua HR Portal như thế nào? | Nhân viên gửi yêu cầu ít nhất 3 ngày làm việc trước ngày nghỉ. | hr_leave_policy_c9 | hr/leave-policy-2026.pdf | medium |
| 66 | Điều kiện để yêu cầu hoàn tiền là gì? | Sản phẩm bị lỗi do nhà sản xuất, yêu cầu gửi trong vòng 7 ngày làm việc. | policy_refund_v4_c20 | policy/refund-v4.pdf | hard |
| 67 | Quy trình xử lý ticket P1 trong SLA là gì? | Phản hồi ban đầu trong 15 phút, xử lý trong 4 giờ. | sla_p1_2026_c26 | support/sla-p1-2026.pdf | multi_hop |
| 68 | Nếu tôi muốn cài phần mềm mới, tôi cần làm gì? | Gửi yêu cầu qua Jira project IT-SOFTWARE, phải có sự phê duyệt của Line Manager. | it_helpdesk_faq_c15 | support/helpdesk-faq.md | medium |
| 69 | Khi nào thì nhân viên có thể làm remote? | Nhân viên sau probation period có thể làm remote tối đa 2 ngày/tuần. | hr_leave_policy_c11 | hr/leave-policy-2026.pdf | multi_hop |
| 70 | Chính sách hoàn tiền mới áp dụng từ khi nào? | Từ ngày 01/02/2026. | policy_refund_v4_c19 | policy/refund-v4.pdf | adversarial |
