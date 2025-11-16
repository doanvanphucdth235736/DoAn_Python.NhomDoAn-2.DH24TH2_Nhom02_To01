# gui.py

# 📌 PHẦN 1 — IMPORT MODULES

import tkinter as tk
from tkinter import ttk, messagebox
from dialogs import DepartmentDialog, EmployeeDialog, SalaryDialog
from database import connect_sql_server

# 📌 PHẦN 2 — CLASS HRDashboard (CỬA SỔ CHÍNH)
class HRDashboard(tk.Tk):
    def __init__(self):
        super().__init__()

        # 🖼️ CẤU HÌNH CỬA SỔ CHÍNH
        self.title("Hệ thống quản lý nhân sự")
        self.geometry("1150x620")
        self.configure(bg="#f1f5f9")

        # Lưu trạng thái nút sidebar & dark mode
        self.active_button = None
        self.dark_mode = False

        # 🎨 BẢNG MÀU GIAO DIỆN: LIGHT & DARK
        self.colors = {
            "light": {
                "bg": "#f1f5f9",
                "content": "#f8fafc",
                "sidebar": "#1e293b",
                "sidebar_button": "#1e293b",
                "sidebar_hover": "#475569",
                "sidebar_active": "#00567D",
                "text": "black",
                "entry_bg": "white",
                "entry_fg": "black"
            },
            "dark": {
                "bg": "#0f172a",
                "content": "#1e293b",
                "sidebar": "#020617",
                "sidebar_button": "#020617",
                "sidebar_hover": "#334155",
                "sidebar_active": "#0ea5e9",
                "text": "white",
                "entry_bg": "#334155",
                "entry_fg": "white"
            }
        }

        # 🗄️ KẾT NỐI DATABASE SQL SERVER
        self.conn, self.cursor = connect_sql_server()
        if not self.conn:
            self.destroy()
            return

        # 🏗️ LAYOUT CHÍNH
        # Sidebar (pack)
        self.sidebar = tk.Frame(self, bg=self.colors["light"]["sidebar"], width=200)
        self.sidebar.pack(side="left", fill="y")

        # Nội dung (pack)
        self.content = tk.Frame(self, bg=self.colors["light"]["content"])
        self.content.pack(side="right", fill="both", expand=True)

        # 🧩 KHỞI TẠO CÁC THÀNH PHẦN
        self.build_sidebar()
        self.show_employee_page()

        # Đóng chương trình
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    # 📌 PHẦN 3 — SIDE BAR (MENU TRÁI)

    # -------------------------- ACTIVE BUTTON -------------------------
    def set_active_button(self, btn):
        mode = "dark" if self.dark_mode else "light"

        if self.active_button:
            self.active_button.configure(bg=self.colors[mode]["sidebar_button"])

        btn.configure(bg=self.colors[mode]["sidebar_active"])
        self.active_button = btn

    # ---------------------- HIỆU ỨNG HOVER -----------------------
    def on_enter(self, btn):
        mode = "dark" if self.dark_mode else "light"
        if btn != self.active_button:
            btn.configure(bg=self.colors[mode]["sidebar_hover"])

    # ---------------------- HIỆU ỨNG RỜI -----------------------
    def on_leave(self, btn):
        mode = "dark" if self.dark_mode else "light"
        if btn != self.active_button:
            btn.configure(bg=self.colors[mode]["sidebar_button"])

    # -------------------------- TẠO SIDEBAR -----------------------------
    def build_sidebar(self):
        mode = "dark" if self.dark_mode else "light"

        title = tk.Label(
            self.sidebar,
            text="📊 HR SYSTEM",
            bg=self.colors[mode]["sidebar"],
            fg="white",
            font=("Arial", 17, "bold"),
            pady=20
        )
        title.pack()

        self.sidebar_buttons = []

        def create_btn(text, command):
            mode = "dark" if self.dark_mode else "light"
            btn = tk.Button(
                self.sidebar,
                text=text,
                bg=self.colors[mode]["sidebar_button"],
                fg="white",
                bd=0,
                anchor="w",
                padx=20,
                pady=10,
                font=("Arial", 13, "bold"),
                activebackground=self.colors[mode]["sidebar_active"],
                command=lambda: command(btn)
            )
            btn.pack(fill="x")

            btn.bind("<Enter>", lambda e, b=btn: self.on_enter(b))
            btn.bind("<Leave>", lambda e, b=btn: self.on_leave(b))

            self.sidebar_buttons.append(btn)
            return btn

        self.btn_emp = create_btn("👤 Quản lý nhân viên", self.show_employee_page)
        self.btn_dept = create_btn("🏢 Quản lý phòng ban", self.show_department_page)
        self.btn_salary = create_btn("💰 Quản lý lương", self.show_salary_page)

        def create_bottom_btn(text, command):
            mode = "dark" if self.dark_mode else "light"
            btn = tk.Button(
                self.sidebar,
                text=text,
                bg=self.colors[mode]["sidebar_button"],
                fg="white",
                bd=0,
                anchor="w",
                padx=20,
                pady=10,
                activebackground=self.colors[mode]["sidebar_active"],
                command=lambda: command(btn)
            )
            btn.pack(side="bottom", fill="x", pady=10)

            btn.bind("<Enter>", lambda e, b=btn: self.on_enter(b))
            btn.bind("<Leave>", lambda e, b=btn: self.on_leave(b))

            self.sidebar_buttons.append(btn)
            return btn

        self.btn_dark_mode = create_bottom_btn("🌙    Dark Mode", self.toggle_dark_mode)

    # 📌 PHẦN 4 — HÀM CHUNG

    # -------------------------- XÓA CONTENT ---------------------------
    def clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    # -------------------------- TẠO BẢNG TREEVIEW --------------------
    def create_table(self, parent, columns):
        mode = "dark" if self.dark_mode else "light"
        frame = tk.Frame(parent, bg=self.colors[mode]["content"])
        frame.pack(fill="both", expand=True)

        table = ttk.Treeview(frame, columns=columns, show="headings", height=14)
        table.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=table.yview)
        scrollbar.pack(side="right", fill="y")
        table.configure(yscrollcommand=scrollbar.set)

        for col in columns:
            table.heading(col, text=col)
            table.column(col, width=160, anchor="center")

        return table

    # 📌 PHẦN 5 — QUẢN LÝ NHÂN VIÊN

    # --------------------------- HIỂN THỊ TRANG ------------------------
    def show_employee_page(self, btn=None):
        if btn:
            self.set_active_button(btn)

        self.clear_content()

        mode = "dark" if self.dark_mode else "light"

        tk.Label(
            self.content,
            text="Quản lý nhân viên",
            bg=self.colors[mode]["content"],
            fg=self.colors[mode]["text"],
            font=("Arial", 18, "bold")
        ).pack(anchor="w", padx=20, pady=10)

        frame = tk.Frame(self.content, bg=self.colors[mode]["content"])
        frame.pack(fill="both", expand=True, padx=20)

        search_frame = tk.Frame(frame, bg=self.colors[mode]["content"])
        search_frame.pack(fill="x", pady=5)

        tk.Label(
            search_frame, text="🔍 Tìm kiếm:",
            bg=self.colors[mode]["content"],
            fg=self.colors[mode]["text"],
            font=("Arial", 12)
        ).pack(side="left")

        self.search_var = tk.StringVar()
        tk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=35,
            font=("Arial", 12),
            bg=self.colors[mode]["entry_bg"],
            fg=self.colors[mode]["entry_fg"],
            insertbackground=self.colors[mode]["entry_fg"]
        ).pack(side="left", padx=5)

        tk.Button(
            search_frame, text="Tìm",
            bg="#16a34a", fg="white",
            font=("Arial", 11, "bold"),
            command=self.search_employee
        ).pack(side="left", padx=5)

        tk.Button(
            search_frame, text="Reset",
            bg="#dc2626", fg="white",
            font=("Arial", 11, "bold"),
            command=self.load_employees
        ).pack(side="left", padx=5)

        tk.Button(
            frame, text="➕ Thêm nhân viên",
            bg="#0ea5e9", fg="white",
            font=("Arial", 11, "bold"),
            command=self.add_employee
        ).pack(anchor="e", pady=5)

        columns = ("Mã NV", "Họ và Tên", "Giới tính", "Ngày sinh", "SĐT",
                   "Địa chỉ", "Chức vụ", "Phòng ban")
        self.emp_table = self.create_table(frame, columns)
        self.load_employees()

        self.emp_table.bind("<Button-3>", self.right_click_employee)

    # --------------------------- TẢI DỮ LIỆU NHÂN VIÊN ------------------------
    def load_employees(self):
        self.emp_table.delete(*self.emp_table.get_children())

        self.cursor.execute("""
            SELECT e.id, e.name, e.gender, e.birthday, e.phone, e.address,
                   p.position_name, d.dept_name
            FROM employees e
            LEFT JOIN positions p ON e.position_id = p.position_id
            LEFT JOIN departments d ON e.dept_id = d.dept_id
            ORDER BY e.id
        """)

        for row in self.cursor.fetchall():
            row = tuple(str(x) if x is not None else "" for x in row)
            self.emp_table.insert("", "end", values=row)

    # --------------------------- TÌM KIẾM NHÂN VIÊN ------------------------
    def search_employee(self):
        keyword = self.search_var.get().strip()
        if not keyword:
            return self.load_employees()

        key = f"%{keyword}%"
        query = """
            SELECT e.id, e.name, e.gender, e.phone, e.address,
                p.position_name, d.dept_name
            FROM employees e
            LEFT JOIN positions p ON e.position_id = p.position_id
            LEFT JOIN departments d ON e.dept_id = d.dept_id
            WHERE
                e.id LIKE ? OR
                e.name LIKE ? OR
                e.phone LIKE ? OR
                p.position_name LIKE ? OR
                d.dept_name LIKE ?
        """

        self.cursor.execute(query, (key, key, key, key, key))
        rows = self.cursor.fetchall()

        self.emp_table.delete(*self.emp_table.get_children())
        for row in rows:
            row = tuple(str(x) if x is not None else "" for x in row)
            self.emp_table.insert("", "end", values=row)

    # ------------------------- CLICK CHUỘT PHẢI NHÂN VIÊN ----------------------
    def right_click_employee(self, event):
        sel = self.emp_table.focus()
        if not sel:
            return

        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Sửa", command=lambda: self.edit_employee(sel))
        menu.add_command(label="Xóa", command=lambda: self.delete_employee(sel))
        menu.post(event.x_root, event.y_root)

    # ------------------------- THÊM NHÂN VIÊN ----------------------
    def add_employee(self):
        EmployeeDialog(self, self.cursor, self.conn, self.load_employees).open()

    # ------------------------- SỬA NHÂN VIÊN ----------------------
    def edit_employee(self, item):
        data = self.emp_table.item(item, "values")
        EmployeeDialog(self, self.cursor, self.conn, self.load_employees,
                       emp_data=data).open()

    # ------------------------- XÓA NHÂN VIÊN ----------------------
    def delete_employee(self, item):
        emp_id = self.emp_table.item(item, "values")[0]

        if not messagebox.askyesno("Xóa", f"Xóa nhân viên {emp_id}?"):
            return

        self.cursor.execute("DELETE FROM salaries WHERE emp_id=?", emp_id)
        self.cursor.execute("DELETE FROM employees WHERE id=?", emp_id)
        self.conn.commit()
        self.load_employees()

    # 📌 PHẦN 6 — QUẢN LÝ PHÒNG BAN

    # --------------------------- HIỂN THỊ TRANG ------------------------
    def show_department_page(self, btn=None):
        if btn:
            self.set_active_button(btn)
        self.clear_content()

        mode = "dark" if self.dark_mode else "light"

        tk.Label(self.content, text="Quản lý phòng ban",
             bg=self.colors[mode]["content"],
             fg=self.colors[mode]["text"],
             font=("Arial", 18, "bold")).pack(anchor="w", padx=20, pady=10)

        top_frame = tk.Frame(self.content, bg=self.colors[mode]["content"])
        top_frame.pack(fill="x", padx=20)
        tk.Button(top_frame, text="➕ Thêm phòng ban", bg="#0ea5e9", fg="white",
                  font=("Arial", 11, "bold"),
                  command=lambda: DepartmentDialog(self, self.cursor, self.conn, self.show_department_page).open()
                 ).pack(anchor="e", pady=5)

        columns = ("Mã PB", "Tên phòng", "Số NV", "Chi tiết")
        table = self.create_table(self.content, columns)

        self.cursor.execute("SELECT dept_id, dept_name FROM departments")
        for dept_id, name in self.cursor.fetchall():
            # correct parameter passing as tuple
            self.cursor.execute("SELECT COUNT(*) FROM employees WHERE dept_id=?", (dept_id,))
            count = self.cursor.fetchone()[0]
            table.insert("", "end", values=(dept_id, name, count, "Xem ➜"))

        def click(event):
            sel = table.focus()
            if not sel:
                return
            col = table.identify_column(event.x)
            if col == "#4":
                dept_id = table.item(sel, "values")[0]
                self.show_employees_by_dept(dept_id)

        table.bind("<Button-1>", click)

        def click_right(event):
            sel = table.focus()
            if not sel:
                return

            data = table.item(sel, "values")

            menu = tk.Menu(self, tearoff=0)
            menu.add_command(label="Sửa phòng ban",
                command=lambda: DepartmentDialog(self, self.cursor, self.conn, 
                                                self.show_department_page, data).open())
            menu.add_command(label="Xóa phòng ban",
                command=lambda: self.delete_department(data[0]))
            menu.post(event.x_root, event.y_root)

        table.bind("<Button-3>", click_right)

    # ------------------------- XÓA PHÒNG BAN ----------------------
    def delete_department(self, dept_id):
        if not messagebox.askyesno("Xóa", f"Xóa phòng ban {dept_id}?"):
            return
        try:
            self.cursor.execute("UPDATE employees SET dept_id=NULL WHERE dept_id=?", (dept_id,))
            self.cursor.execute("DELETE FROM departments WHERE dept_id=?", (dept_id,))
            self.conn.commit()
            self.show_department_page(self.btn_dept)
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    # ------------------------- HIỂN THỊ NHÂN VIÊN THEO PHÒNG BAN ----------------------
    def show_employees_by_dept(self, dept_id):
        self.clear_content()

        self.cursor.execute("SELECT dept_name FROM departments WHERE dept_id=?", (dept_id,))
        dept_name = self.cursor.fetchone()[0]

        tk.Label(
            self.content,
            text=f"Nhân viên thuộc phòng: {dept_name} ({dept_id})",
            bg="#f8fafc",
            font=("Arial", 18, "bold")
        ).pack(anchor="w", padx=20, pady=10)

        columns = ("Mã NV", "Họ và tên", "Chức vụ")
        table = self.create_table(self.content, columns)

        self.cursor.execute("""
            SELECT e.id, e.name, p.position_name
            FROM employees e
            LEFT JOIN positions p ON e.position_id = p.position_id
            WHERE e.dept_id = ?
            ORDER BY e.id
        """, dept_id)

        for row in self.cursor.fetchall():
            row = tuple(str(x) if x is not None else "" for x in row)
            table.insert("", "end", values=row)

        tk.Button(
            self.content,
            text="⬅ Quay lại",
            bg="#0ea5e9",
            fg="white",
            font=("Arial", 12, "bold"),
            command=lambda: self.show_department_page(self.btn_dept)
        ).pack(anchor="w", padx=20, pady=10)


    # 📌 PHẦN 7 — QUẢN LÝ LƯƠNG

    # --------------------------- HIỂN THỊ TRANG ------------------------
    def show_salary_page(self, btn=None):
        if btn:
            self.set_active_button(btn)
        self.clear_content()

        tk.Label(
            self.content,
            text="Quản lý lương",
            bg=self.colors["dark"]["content"] if self.dark_mode else self.colors["light"]["content"],
            fg=self.colors["dark"]["text"] if self.dark_mode else self.colors["light"]["text"],
            font=("Arial", 18, "bold")
        ).pack(anchor="w", padx=20, pady=10)

        columns = ("Mã NV", "Họ tên", "Số ngày công", "Lương chính thức", "Đánh giá")
        table = self.create_table(self.content, columns)
        self.salary_table = table

        self.cursor.execute("""
            SELECT e.id, e.name, s.working_days, s.official_salary, s.rating
            FROM salaries s
            JOIN employees e ON s.emp_id = e.id
            ORDER BY e.id
        """)

        for row in self.cursor.fetchall():
            row = tuple("" if x is None else str(x) for x in row)
            table.insert("", "end", values=row)

        # ------------------------- CLICK CHUỘT LƯƠNG ----------------------
        def right_click(event):
            row_id = table.identify_row(event.y)
            if not row_id:
                return

            table.selection_set(row_id)
            table.focus(row_id)

            values = table.item(row_id, "values")

            menu = tk.Menu(self, tearoff=0)
            menu.add_command(
                label="Sửa",
                command=lambda: self.edit_salary(values)
            )
            menu.post(event.x_root, event.y_root)

        table.bind("<Button-3>", right_click)

    # ------------------------- SỬA LƯƠNG ----------------------
    def edit_salary(self, values):
        SalaryDialog(
            self,
            self.cursor,
            self.conn,
            lambda: self.show_salary_page(),
            values
        ).open()


    # 📌 PHẦN 8 — DARK / LIGHT MODE
    def toggle_dark_mode(self, btn=None):

        # ------------------------- ĐẢO TRẠNG THÁI DARK / LIGHT ----------------------
        self.dark_mode = not self.dark_mode
        mode = "dark" if self.dark_mode else "light"

        self.btn_dark_mode.configure(
            text="☀️ Light Mode" if self.dark_mode else "🌙    Dark Mode"
        )

        # ------------------------- ĐỔI MÀU NỀN CHUNG ----------------------
        self.configure(bg=self.colors[mode]["bg"])
        self.sidebar.configure(bg=self.colors[mode]["sidebar"])
        self.content.configure(bg=self.colors[mode]["content"])

        for w in self.sidebar.winfo_children():
            if isinstance(w, tk.Label):
                w.configure(bg=self.colors[mode]["sidebar"], fg="white")

        # ------------------------- CẬP NHẬT MÀU BUTTON TRONG SIDEBAR ----------------------
        for b in self.sidebar_buttons:
            b.configure(
                bg=self.colors[mode]["sidebar_button"],
                fg="white",
                activebackground=self.colors[mode]["sidebar_active"],
                activeforeground="white"
            )

        if self.active_button:
            self.active_button.configure(bg=self.colors[mode]["sidebar_active"])

        # ------------------------- HÀM ĐỆ QUY ĐỔI MÀU TẤT CẢ WIDGET TRONG CONTENT ----------------------
        def recursive_update(widget):
            for w in widget.winfo_children():
                if isinstance(w, tk.Frame):
                    w.configure(bg=self.colors[mode]["content"])

                elif isinstance(w, tk.Label):
                    w.configure(bg=self.colors[mode]["content"], fg=self.colors[mode]["text"])

                elif isinstance(w, tk.Entry):
                    w.configure(
                        bg=self.colors[mode]["entry_bg"],
                        fg=self.colors[mode]["entry_fg"],
                        insertbackground=self.colors[mode]["entry_fg"]
                    )

                elif isinstance(w, tk.Button):
                    if w not in self.sidebar_buttons:
                        special = ["#0ea5e9", "#16a34a", "#dc2626"]
                        if w.cget("bg") in special:
                            w.configure(fg="white")
                        else:
                            w.configure(
                                bg=self.colors[mode]["content"],
                                fg=self.colors[mode]["text"],
                                activebackground=self.colors[mode]["sidebar_hover"]
                            )

                recursive_update(w)

        recursive_update(self.content)

        # ------------------------- ĐỔI STYLE TREEVIEW (ttk) ----------------------
        style = ttk.Style()
        style.theme_use("default")

        if mode == "dark":
            style.configure("Treeview",
                            background="#1e293b",
                            fieldbackground="#1e293b",
                            foreground="white")
            style.configure("Treeview.Heading",
                            background="#334155",
                            foreground="white")
        else:
            style.configure("Treeview",
                            background="white",
                            fieldbackground="white",
                            foreground="black")
            style.configure("Treeview.Heading",
                            background="#e2e8f0",
                            foreground="black")


    # 📌 PHẦN 9 — ĐÓNG CHƯƠNG TRÌNH

    def on_close(self):
        if self.conn:
            self.conn.close()
        self.destroy()
