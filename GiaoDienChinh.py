import tkinter as tk
from tkinter import ttk, messagebox
import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass


class HRDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hệ thống quản lý nhân sự")
        self.geometry("1000x600")
        self.configure(bg="#f1f5f9")

        self.active_button = None  # <--- Nút đang được chọn

        # ====== Khung chính ======
        self.sidebar = tk.Frame(self, bg="#032864", width=200)
        self.sidebar.pack(side="left", fill="y")

        self.content = tk.Frame(self, bg="#f8fafc")
        self.content.pack(side="right", expand=True, fill="both")

        # ====== Sidebar ======
        self._build_sidebar()

        # ====== Nội dung mặc định ======
        self.set_active_button(self.btn_nv)
        self.show_employee_page()

    # ====== Đổi màu nút đang chọn ======
    def set_active_button(self, button):
        for btn in [self.btn_nv, self.btn_pb, self.btn_lg]:
            btn.configure(bg="#1e293b")

        button.configure(bg="#0f172a")
        self.active_button = button

    # ====== Hiệu ứng hover ======
    def add_hover_effect(self, button):

        def on_enter(e):
            if button != self.active_button:
                button.configure(bg="#334155")

        def on_leave(e):
            if button != self.active_button:
                button.configure(bg="#1e293b")

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    # ====== Sidebar ======
    def _build_sidebar(self):
        tk.Label(self.sidebar, text="HR SYSTEM", fg="white", bg="#032864",
                 font=("Arial", 16, "bold"), pady=20).pack()

        btn_style = {
            "bg": "#1e293b", "fg": "white",
            "font": ("Arial", 12),
            "bd": 0, "activebackground": "#334155",
            "activeforeground": "white",
            "anchor": "w", "padx": 20, "pady": 10,
            "relief": "flat"
        }

        # Nút nhân viên
        self.btn_nv = tk.Button(
            self.sidebar, text="👤 Quản lý nhân viên",
            command=lambda: (self.set_active_button(self.btn_nv), self.show_employee_page()),
            **btn_style
        )

        # Nút phòng ban
        self.btn_pb = tk.Button(
            self.sidebar, text="🏢 Quản lý phòng ban",
            command=lambda: (self.set_active_button(self.btn_pb), self.show_department_page()),
            **btn_style
        )

        # Nút lương
        self.btn_lg = tk.Button(
            self.sidebar, text="💰 Quản lý lương",
            command=lambda: (self.set_active_button(self.btn_lg), self.show_salary_page()),
            **btn_style
        )

        # Gắn hiệu ứng hover
        for btn in [self.btn_nv, self.btn_pb, self.btn_lg]:
            self.add_hover_effect(btn)

        self.btn_nv.pack(fill="x")
        self.btn_pb.pack(fill="x")
        self.btn_lg.pack(fill="x")

        tk.Label(self.sidebar, bg="#1e293b").pack(expand=True, fill="both")

    # ====== Các trang ======
    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_employee_page(self):
        self.clear_content()
        tk.Label(self.content, text="Quản lý nhân viên", font=("Arial", 18, "bold"),
                 bg="#f8fafc", fg="#0f172a").pack(anchor="w", padx=20, pady=10)

        frame = tk.Frame(self.content, bg="#f8fafc")
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        add_btn = tk.Button(
            frame, text="➕ Thêm mới",
            bg="#0ea5e9", fg="white",
            font=("Arial", 11, "bold"),
            relief="flat", padx=10, pady=5,
            command=lambda: messagebox.showinfo("Thêm nhân viên", "Tính năng đang phát triển")
        )
        add_btn.pack(anchor="e", pady=5)

        columns = ("Mã Nhân Viên", "Họ và Tên", "Giới tính", "SĐT", "Địa chỉ")
        table = ttk.Treeview(frame, columns=columns, show="headings", height=12)

        for col in columns:
            table.heading(col, text=col)
            table.column(col, width=150, anchor="center")

        data = [
            ("NV001", "Nguyễn Văn A", "Nam", "0123456789", "Hà Nội"),
            ("NV002", "Trần Thị B", "Nữ", "0987654321", "Đà Nẵng"),
            ("NV003", "Lê Văn C", "Nam", "0123456789", "Hồ Chí Minh"),
            ("NV004", "Phạm Thị D", "Nữ", "0123456789", "Cần Thơ"),
        ]

        for row in data:
            table.insert("", "end", values=row)

        table.pack(fill="both", expand=True, pady=10)

    def show_department_page(self):
        self.clear_content()
        tk.Label(self.content, text="Quản lý phòng ban", font=("Arial", 18, "bold"),
                 bg="#f8fafc", fg="#0f172a").pack(anchor="w", padx=20, pady=10)

        frame = tk.Frame(self.content, bg="#f8fafc")
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("Mã phòng", "Tên phòng ban")
        table = ttk.Treeview(frame, columns=columns, show="headings", height=10)

        for col in columns:
            table.heading(col, text=col)
            table.column(col, width=200, anchor="center")

        data = [
            ("PB01", "Kinh doanh"),
            ("PB02", "Kỹ thuật"),
            ("PB03", "Kế toán"),
            ("PB04", "Marketing"),
        ]

        for row in data:
            table.insert("", "end", values=row)

        table.pack(fill="both", expand=True, pady=10)

    def show_salary_page(self):
        self.clear_content()
        tk.Label(self.content, text="Quản lý lương", font=("Arial", 18, "bold"),
                 bg="#f8fafc", fg="#0f172a").pack(anchor="w", padx=20, pady=10)

        frame = tk.Frame(self.content, bg="#f8fafc")
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("ID", "Tên", "Lương cơ bản")
        table = ttk.Treeview(frame, columns=columns, show="headings", height=10)

        for col in columns:
            table.heading(col, text=col)
            table.column(col, width=200, anchor="center")

        data = [
            ("NV001", "Nguyễn Văn A", "8.000.000"),
            ("NV002", "Trần Thị B", "15.000.000"),
            ("NV003", "Lê Văn C", "12.000.000"),
            ("NV004", "Phạm Thị D", "9.000.000"),
        ]

        for row in data:
            table.insert("", "end", values=row)

        table.pack(fill="both", expand=True, pady=10)


if __name__ == "__main__":
    app = HRDashboard()
    app.mainloop()
