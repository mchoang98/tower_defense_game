
# Game Thủ Thành (Tower Defense)

Đây là một game **Thủ Thành** được phát triển bằng **Python** và thư viện **Pygame**, theo mô hình hướng đối tượng. Người chơi xây dựng các tháp để tiêu diệt kẻ địch trước khi chúng đến được căn cứ.

---
![image](https://github.com/user-attachments/assets/55ec2c66-3a27-46c2-ae98-4cfbd8c45117)

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
+----------------------+| Vẽ lại màn hình      |
| - Lưới, tháp, đạn     |
| - Quái, máu, vàng     |
+----------------------+
            |
            v
+---------------------+
| Kết thúc nếu máu <= 0|
+---------------------+
```

---

## Yêu cầu cài đặt

- Python 3.7+
- Pygame

Cài đặt Pygame qua pip:

```bash
pip install pygame
```

---

## Cách chạy game

```bash
python main.py
```

> Hãy thay `main.py` bằng tên tệp game thực tế của bạn.

---

## Cấu trúc thư mục

```
📁 project/
 ┣ 📄 main.py
 ┣ 📁 assets/
 ┃ ┣ 🖼️ enemy.png
 ┃ ┣ 🖼️ tower.png
 ┃ ┣ 🖼️ tower_1.png đến tower_5.png
```

---

## Tài nguyên trong thư mục `assets/`

| Tên tệp             | Vai trò              |
|---------------------|----------------------|
| `enemy.png`         | Hình quái vật        |
| `tower.png`         | Hình tháp mặc định   |
| `tower_1.png` → `tower_5.png` | Ảnh tháp theo cấp độ |

Tất cả ảnh nên có kích thước khoảng **40x40 pixel**.

---

## Điều khiển

| Hành động                | Phím / Chuột         |
|--------------------------|----------------------|
| Đặt tháp                 | Chuột trái           |
| Nâng cấp tháp            | Chuột phải           |
| Bắt đầu đợt quái mới     | Phím Space           |
| Thoát game               | Đóng cửa sổ game     |

---

## Tác giả

Phát triển bởi mchoang98 
Dự án học tập dùng Python & Pygame  
