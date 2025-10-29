import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

root = tk.Tk()
root.title("Quản lý nhân sự")
root.geometry("700x500")

try:
    from tkcalendar import DateEntry
except Exception:
    # Fallback simple DateEntry when tkcalendar is not installed.
    # This behaves like an Entry pre-filled with today's date in mm/dd/yy format.
    class DateEntry(tk.Entry):
        def __init__(self, master=None, date_pattern=None, **kwargs):
            super().__init__(master, **kwargs)
            # insert today's date in mm/dd/yy to match the original pattern
            self.insert(0, datetime.now().strftime("%m/%d/%y"))

        def get(self):
            return super().get()

frame_input = tk.LabelFrame(root, text="Thông tin nhân sự", padx=10, pady=10)
frame_input.pack(fill="x", padx=10, pady=10)

tk.Label(frame_input, text="Mã số nhân viên:").grid(row=0, column=0)
txt_ma = tk.Entry(frame_input)
txt_ma.grid(row=0, column=1)

tk.Label(frame_input, text="Họ và tên lót:").grid(row=0, column=2)
txt_hovatlot = tk.Entry(frame_input)
txt_hovatlot.grid(row=0, column=3)

tk.Label(frame_input, text="Tên:").grid(row=1, column=0)
txt_ten = tk.Entry(frame_input)
txt_ten.grid(row=1, column=1)

tk.Label(frame_input, text="Giới tính:").grid(row=1, column=2)
phai_var = tk.StringVar()
tk.Radiobutton(frame_input, text="Nam", variable=phai_var, value="Nam").grid(row=1, column=3, sticky="w")
tk.Radiobutton(frame_input, text="Nữ", variable=phai_var, value="Nữ").grid(row=1, column=3, sticky="e")

tk.Label(frame_input, text="Ngày sinh:").grid(row=2, column=0)
date_ngaysinh = DateEntry(frame_input, date_pattern="mm/dd/yy")
date_ngaysinh.grid(row=2, column=1)

tk.Label(frame_input, text="Chức vụ:").grid(row=2, column=2)
chucvu = ttk.Combobox(frame_input, values=["Trưởng phòng", "Nhân viên", "Phó phòng", "Kế toán"])
chucvu.grid(row=2, column=3)

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=5)

def them():
    tree.insert("", "end", values=(
        txt_ma.get(),
        txt_hovatlot.get(),
        txt_ten.get(),
        phai_var.get(),
        date_ngaysinh.get(),
        chucvu.get()
    ))
    messagebox.showinfo("Thêm", "Đã thêm nhân viên mới")

tk.Button(frame_buttons, text="Thêm", command=them, width=10).pack(side="left", padx=5)
tk.Button(frame_buttons, text="Lưu", width=10).pack(side="left", padx=5)
tk.Button(frame_buttons, text="Sửa", width=10).pack(side="left", padx=5)
tk.Button(frame_buttons, text="Xóa", width=10).pack(side="left", padx=5)
tk.Button(frame_buttons, text="Thoát", command=root.destroy, width=10).pack(side="left", padx=5)

columns = ("ma", "hovaten", "ten", "phai", "ngaysinh", "chucvu")
tree = ttk.Treeview(root, columns=columns, show="headings")

tree.heading("ma", text="Mã số")
tree.heading("hovaten", text="Họ và lót")
tree.heading("ten", text="Tên")
tree.heading("phai", text="Phái")
tree.heading("ngaysinh", text="Ngày sinh")
tree.heading("chucvu", text="Chức vụ")

tree.pack(fill="both", expand=True, padx=10, pady=10)
root.mainloop()