import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

# ======== CỬA SỔ CHÍNH =========
root = tk.Tk()
root.title("QUẢN LÝ NHÂN SỰ")
root.geometry("1050x650")
root.resizable(False, False)

# ======== TIÊU ĐỀ =========
tk.Label(root, text="QUẢN LÝ NHÂN SỰ", font=("Arial", 20, "bold")).pack(pady=10)

# ======== KHUNG NHẬP LIỆU =========
frame_info = tk.LabelFrame(root, text="Thông tin nhân sự", padx=10, pady=10, font=("Arial", 15, "bold"))
frame_info.pack(fill="x", padx=10, pady=5)

# --- Hàng 1: Mã số NV, Họ và tên, Giới tính ---
tk.Label(frame_info, text="Mã số NV:", width=12, anchor="w").grid(row=0, column=0, pady=5, sticky="w")
entry_maso = tk.Entry(frame_info, width=25)
entry_maso.grid(row=0, column=1, padx=5, sticky="w")

tk.Label(frame_info, text="Họ và tên:", width=12, anchor="w").grid(row=0, column=2, sticky="w")
entry_hoten = tk.Entry(frame_info, width=35)
entry_hoten.grid(row=0, column=3, padx=5, sticky="w")

tk.Label(frame_info, text="Giới tính:", width=12, anchor="w").grid(row=0, column=4, sticky="w")
gender_var = tk.StringVar(value="Nam")
tk.Radiobutton(frame_info, text="Nam", variable=gender_var, value="Nam").grid(row=0, column=5, sticky="w")
tk.Radiobutton(frame_info, text="Nữ", variable=gender_var, value="Nữ").grid(row=0, column=5, sticky="e")

# --- Hàng 2: Ngày sinh, Địa chỉ, Email ---
tk.Label(frame_info, text="Ngày sinh:", width=12, anchor="w").grid(row=1, column=0, pady=5, sticky="w")
entry_ngaysinh = tk.Entry(frame_info, width=25)
entry_ngaysinh.insert(0, "dd/mm/yyyy")
entry_ngaysinh.grid(row=1, column=1, padx=5, sticky="w")

tk.Label(frame_info, text="Địa chỉ:", width=12, anchor="w").grid(row=1, column=2, sticky="w")
entry_diachi = tk.Entry(frame_info, width=35)
entry_diachi.grid(row=1, column=3, padx=5, sticky="w")

tk.Label(frame_info, text="SĐT:", width=12, anchor="w").grid(row=1, column=4, sticky="w")
entry_email = tk.Entry(frame_info, width=25)
entry_email.grid(row=1, column=5, padx=5, sticky="w")

# --- Hàng 3: Mã chức vụ, Mã phòng ban, Số ngày công ---
tk.Label(frame_info, text="Mã chức vụ:", width=12, anchor="w").grid(row=2, column=0, pady=5, sticky="w")
entry_sdt = tk.Entry(frame_info, width=25)
entry_sdt.grid(row=2, column=1, padx=5, sticky="w")

tk.Label(frame_info, text="Mã phòng ban:", width=12, anchor="w").grid(row=2, column=2, sticky="w")
entry_mapb = tk.Entry(frame_info, width=35)
entry_mapb.grid(row=2, column=3, padx=5, sticky="w")

tk.Label(frame_info, text="Số ngày công:", width=12, anchor="w").grid(row=2, column=4, sticky="w")
entry_songaycong = tk.Entry(frame_info, width=25)
entry_songaycong.grid(row=2, column=5, padx=5, sticky="w")

# ======== KHUNG NÚT CHỨC NĂNG =========
frame_buttons = tk.Frame(root, bg="#e9ecef")
frame_buttons.pack(fill="x", padx=10, pady=10)

btn_width = 18
btn_them = tk.Button(frame_buttons, text="Thêm", width=btn_width, bg="#d1ecf1", font=("Arial", 10, "bold"))
btn_luu = tk.Button(frame_buttons, text="Lưu", width=btn_width, bg="#d1ecf1", font=("Arial", 10, "bold"))
btn_sua = tk.Button(frame_buttons, text="Sửa", width=btn_width, bg="#d1ecf1", font=("Arial", 10, "bold"))
btn_xoa = tk.Button(frame_buttons, text="Xóa", width=btn_width, bg="#d1ecf1", font=("Arial", 10, "bold"))
btn_huy = tk.Button(frame_buttons, text="Hủy", width=btn_width, bg="#d1ecf1", font=("Arial", 10, "bold"))
btn_thoat = tk.Button(frame_buttons, text="Thoát", width=btn_width, bg="#f8d7da", font=("Arial", 10, "bold"))

# Căng đều 6 nút trên toàn chiều ngang
frame_buttons.grid_columnconfigure((0,1,2,3,4,5), weight=1)
btn_them.grid(row=0, column=0, padx=5, pady=8)
btn_luu.grid(row=0, column=1, padx=5, pady=8)
btn_sua.grid(row=0, column=2, padx=5, pady=8)
btn_xoa.grid(row=0, column=3, padx=5, pady=8)
btn_huy.grid(row=0, column=4, padx=5, pady=8)
btn_thoat.grid(row=0, column=5, padx=5, pady=8)

# ======== KHUNG TÌM KIẾM =========
frame_search = tk.Frame(root)
frame_search.pack(fill="x", padx=10, pady=5)

tk.Label(frame_search, text="Tìm kiếm theo mã NV:", font=("Arial", 13, "bold")).pack(side="left")
entry_search = tk.Entry(frame_search, width=25)
entry_search.pack(side="left", padx=5)
tk.Button(frame_search, text="Tìm kiếm", width=12).pack(side="left")

# ======== BẢNG DANH SÁCH NHÂN VIÊN =========
frame_table = tk.LabelFrame(root, text="Danh sách nhân viên", padx=10, pady=10, font=("Arial", 15, "bold"))
frame_table.pack(fill="both", expand=True, padx=10, pady=5)

columns = ("Mã NV", "Họ và tên", "Giới tính", "Ngày sinh", "Địa chỉ", "Email", "SĐT", "Phòng ban", "Lương")

table = ttk.Treeview(frame_table, columns=columns, show="headings", height=12)
for col in columns:
    table.heading(col, text=col)
    table.column(col, anchor="center", width=110)
table.pack(fill="both", expand=True)

# ======== CHỨC NĂNG THOÁT =========
def thoat():
    if messagebox.askyesno("Xác nhận", "Bạn có muốn thoát chương trình không?"):
        root.destroy()

btn_thoat.config(command=thoat)

root.mainloop()
