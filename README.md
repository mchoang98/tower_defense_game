# Game Thủ Thành (Tower Defense)

Đây là một game **Thủ Thành** được phát triển bằng **Python** và thư viện **Pygame**, theo mô hình hướng đối tượng. Người chơi xây dựng các tháp để tiêu diệt kẻ địch trước khi chúng đến được căn cứ.

---
![image](https://github.com/user-attachments/assets/c064d86c-5c2e-46c9-af42-1b48495d5e5e)

## Mục tiêu

- Xây tháp và nâng cấp để tiêu diệt kẻ địch.
- Bảo vệ căn cứ khỏi các đợt tấn công liên tục.
- Quản lý tài nguyên vàng một cách hợp lý.

---

## Cách chơi

- **Nhấn chuột trái**: Đặt tháp vào ô trống đã mở khóa.
- **Nhấn chuột phải vào tháp**: Nâng cấp tháp nếu đủ vàng.
- **Nhấn Space**: Bắt đầu đợt quái tiếp theo.
- **Mỗi đợt** sẽ có số lượng và độ mạnh quái tăng dần.
- Khi **quái đến được căn cứ**, bạn sẽ **mất máu**.

---

## Sơ đồ thuật toán (Luồng chính của game)

```text
+---------------------+
| Khởi tạo Game       |
| - Màn hình          |
| - Đường đi của quái |
| - Tài nguyên ban đầu|
+---------------------+
            |
            v
+------------------------+
| Vòng lặp chính của game|
+------------------------+
            |
            v
+-----------------------------+
| Xử lý sự kiện người dùng    |
| - Chuột trái: đặt tháp      |
| - Chuột phải: nâng cấp tháp |
| - Space: bắt đầu đợt mới    |
+-----------------------------+
            |
            v
+---------------------------+
| Cập nhật trạng thái game  |
| - Tháp bắn quái           |
| - Đạn di chuyển và gây sát thương |
| - Quái di chuyển, mất máu, chết   |
+---------------------------+
            |
            v
+----------------------+
| Vẽ lại màn hình      |
| - Lưới, tháp, đạn     |
| - Quái, máu, vàng     |
+----------------------+
            |
            v
+---------------------+
| Kết thúc nếu máu <= 0|
+---------------------+
