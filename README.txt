# Thông tin sinh viên:
23634031_Lê Huỳnh Tấn Đạt
23631971_Nguyễn Xuân Đỉnh
23640391_ Trần Vĩnh Cơ

# Hệ thống Quản lý Thư viện Trường Đại học (MVP)

Hệ thống phục vụ các nghiệp vụ: quản lý độc giả (thẻ thư viện), quản lý chuyên ngành, quản lý đầu sách & bản sao, quản lý mượn/trả, báo cáo thống kê, quản trị người dùng (thủ thư/admin). Backend cung cấp API; frontend là các trang HTML thao tác qua API.

---

## 1) Kết quả hoàn thành dự án so với yêu cầu đề bài (Tự đánh giá: 10 - Tự làm được )

| Nhóm yêu cầu | Mô tả theo đề bài | Trạng thái | Ghi chú/Hiện thực |
|---|---|---|---|
| Đăng nhập | Người dùng hệ thống phải đăng nhập trước khi thực hiện | Hoàn thành | `/auth/login` (JWT Bearer), frontend có `login.html` |
| Quản lý độc giả (thẻ) | Thêm/sửa/xóa thẻ: (mã, họ tên, lớp, ngày sinh, giới tính) | Hoàn thành | CRUD độc giả: `/readers` |
| Quản lý chuyên ngành | (mã, tên, mô tả) | Hoàn thành | CRUD chuyên ngành: `/majors` |
| Quản lý đầu sách | (mã đầu sách, tên, NXB, số trang, kích thước, tác giả, số lượng) | Hoàn thành | CRUD đầu sách: `/titles`; `total_quantity` tự cập nhật theo số bản sao |
| Quản lý bản sao | (mã đầu, mã sách, tình trạng, ngày nhập) | Hoàn thành | CRUD bản sao: `/copies`; tình trạng `available/borrowed` |
| Mượn sách | Mỗi độc giả 1 lần chỉ mượn 1 cuốn; phiếu mượn gồm (mã sách, mã độc giả, mã thủ thư, ngày mượn, tình trạng) | Hoàn thành | `/borrows/borrow` có ràng buộc “1 độc giả chỉ có 1 phiếu đang mượn”; lưu `librarian_id`, `borrow_date`, `status` |
| Trả sách | Ghi nhận tình trạng trả cho phiếu mượn | Hoàn thành | `/borrows/return` cập nhật phiếu mượn và trả trạng thái bản sao về `available` |
| Báo cáo | (1) đầu sách mượn nhiều nhất (2) độc giả chưa trả | Hoàn thành | `/reports/most-borrowed`, `/reports/unreturned-readers` |
| Quản trị người dùng | Admin quản lý thủ thư: tạo/sửa/xóa, cấp quyền | Hoàn thành | CRUD thủ thư: `/librarians` (yêu cầu role `admin`) |
| In thẻ thư viện | In thẻ giao cho sinh viên | Chưa có | Hiện tại chỉ quản lý thông tin độc giả trên hệ thống (chưa tích hợp in ấn) |

---

## 2) Các công nghệ sử dụng

- Backend: FastAPI, Uvicorn, SQLAlchemy ORM, Pydantic, JWT (python-jose), hash mật khẩu (passlib), SQLite.
- Frontend: HTML + Bootstrap + Bootstrap Icons + Vanilla JavaScript (ES Modules, Fetch API).
- Công cụ: Python 3.x, `pip`, chạy frontend qua `python -m http.server`.

---

## 3) Techstack

- **Backend**
  - Language: Python
  - Framework: FastAPI
  - Database: SQLite (`backend/library.db`)
  - ORM: SQLAlchemy
  - Auth: JWT Bearer + role (`admin`/`librarian`)
- **Frontend**
  - Static pages: `frontend/*.html`
  - UI: Bootstrap 5
  - API client: `frontend/assets/api.js`

---

## 4) Quy trình làm (đề xuất/đã áp dụng)

1. Phân tích yêu cầu đề bài → xác định các thực thể: Độc giả, Chuyên ngành, Đầu sách, Bản sao, Thủ thư, Phiếu mượn.
2. Thiết kế CSDL (SQLite) + quan hệ + ràng buộc (mỗi độc giả chỉ có 1 phiếu “đang mượn”).
3. Xây dựng Backend API theo module (auth/readers/majors/books/borrows/reports/librarians).
4. Xây dựng Frontend theo từng màn hình nghiệp vụ (đăng nhập, độc giả, sách, mượn-trả, báo cáo, admin).
5. Kiểm thử thủ công theo luồng: tạo dữ liệu → mượn → trả → thống kê/báo cáo.

---

## Chạy dự án (Windows / PowerShell)

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

- Swagger UI: `http://127.0.0.1:8000/docs`
- Tài khoản admin mặc định (tự tạo khi chạy lần đầu):
  - username: `admin`
  - password: `admin`

### Frontend

Khuyến nghị chạy qua web server để tránh hạn chế CORS/file:

```powershell
cd frontend
python -m http.server 5500
```

Mở: `http://127.0.0.1:5500/login.html`

Ghi chú: URL backend mặc định nằm ở `frontend/assets/api.js` (`API_BASE = http://127.0.0.1:8000`).
