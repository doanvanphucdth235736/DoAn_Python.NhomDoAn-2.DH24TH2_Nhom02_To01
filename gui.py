# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from dialogs import DepartmentDialog, EmployeeDialog
from database import connect_sql_server

class recursive_update:
    def __init__(self):
        pass


class HRDashboard(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Hệ thống quản lý nhân sự")
        self.geometry("1150x620")
        self.configure(bg="#f1f5f9")
        self.active_button = None
        self.dark_mode = False
        self.colors = {
            "light": {
                "bg": "#f1f5f9",
                "content": "#f8fafc",
                "sidebar": "#19202d",
                "text": "black"
            },
            "dark": {
                "bg": "#0f172a",
                "content": "#ffffff",
                "sidebar": "#020617",
                "text": "white"
            }
        }
        self.sidebar_buttons = []
        self.sidebar_default_bg = "#1e293b"
        self.sidebar_hover_bg = "#475569"
        self.sidebar_active_bg = "#00567D"

        self.conn, self.cursor = connect_sql_server()
        if not self.conn:
            self.destroy()
            return

        self.sidebar = tk.Frame(self, bg="#1e293b", width=200)
        self.sidebar.pack(side="left", fill="y")

        self.content = tk.Frame(self, bg="#f8fafc")
        self.content.pack(side="right", expand=True, fill="both")

        self.build_sidebar()
        self.show_employee_page()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    # ========== SIDEBAR ==========
    def set_active_button(self, btn):
        if self.active_button:
            self.active_button.configure(bg=self.sidebar_default_bg)
        btn.configure(bg=self.sidebar_active_bg)
        self.active_button = btn

    def on_enter(self, btn):
        if btn != self.active_button:
            btn.configure(bg=self.sidebar_hover_bg)

    def on_leave(self, btn):
        if btn != self.active_button:
            btn.configure(bg=self.sidebar_default_bg)

    def build_sidebar(self):
        tk.Label(self.sidebar, text="HR SYSTEM", fg="white", bg="#1e293b",
             font=("Arial", 16, "bold"), pady=20).pack()

        btn_style = {
            "bg": self.sidebar_default_bg,
            "fg": "white",
            "font": ("Arial", 12),
            "bd": 0,
            "activebackground": self.sidebar_active_bg,
            "anchor": "w",
            "padx": 20,
            "pady": 10
        }

        def create_btn(text, command):
            btn = tk.Button(self.sidebar, text=text, **btn_style,
                            command=lambda: command(btn))
            btn.pack(fill="x")

            # Hover effect
            btn.bind("<Enter>", lambda e, b=btn: self.on_enter(b))
            btn.bind("<Leave>", lambda e, b=btn: self.on_leave(b))

            self.sidebar_buttons.append(btn)
            return btn

        self.btn_emp = create_btn("👤 Quản lý nhân viên", self.show_employee_page)
        self.btn_dept = create_btn("🏢 Quản lý phòng ban", self.show_department_page)
        self.btn_salary = create_btn("💰 Quản lý lương", self.show_salary_page)

        def create_bottom_btn(text, command):
            btn = tk.Button(self.sidebar, text=text, **btn_style,
                            command=lambda: command(btn))
            btn.pack(side="bottom", fill="x", pady=10)  
            self.sidebar_buttons.append(btn)
            # Hover effect
            btn.bind("<Enter>", lambda e, b=btn: self.on_enter(b))
            btn.bind("<Leave>", lambda e, b=btn: self.on_leave(b))
            return btn

        self.btn_dark_mode = create_bottom_btn("🌙    Dark Mode", self.toggle_dark_mode)


    # ========== COMMON ==========
    def clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def create_table(self, parent, columns):
        frame = tk.Frame(parent, bg=self.colors["dark"]["content"] if self.dark_mode else self.colors["light"]["content"])
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

    # ========== NHÂN VIÊN ==========
    def show_employee_page(self, btn=None):
        if btn:
            self.set_active_button(btn)

        self.clear_content()

        tk.Label(self.content, text="Quản lý nhân viên",
            bg=self.colors["dark"]["content"] if self.dark_mode else self.colors["light"]["content"],
            fg=self.colors["dark"]["text"] if self.dark_mode else self.colors["light"]["text"],
                font=("Arial", 18, "bold")).pack(anchor="w", padx=20, pady=10)

        frame = tk.Frame(self.content, bg=self.colors["dark"]["content"] if self.dark_mode else self.colors["light"]["content"])
        search_frame = tk.Frame(frame, bg=self.colors["dark"]["content"] if self.dark_mode else self.colors["light"]["content"])

        search_frame.pack(fill="x", pady=5)

        tk.Label(search_frame, text="🔍 Tìm kiếm:", font=("Arial", 12),
            bg=self.colors["dark"]["content"] if self.dark_mode else self.colors["light"]["content"],
            fg=self.colors["dark"]["text"] if self.dark_mode else self.colors["light"]["text"])

        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var,
                width=35, font=("Arial", 12)).pack(side="left", padx=5)

        tk.Button(search_frame, text="Tìm", bg="#16a34a", fg="white",
                font=("Arial", 11, "bold"),
                command=self.search_employee).pack(side="left", padx=5)

        tk.Button(search_frame, text="Reset", bg="#dc2626", fg="white",
                font=("Arial", 11, "bold"),
                command=self.load_employees).pack(side="left", padx=5)

        frame.pack(fill="both", expand=True, padx=20)

        tk.Button(frame, text="➕ Thêm nhân viên", bg="#0ea5e9",
                fg="white", font=("Arial", 11, "bold"),
                command=self.add_employee).pack(anchor="e", pady=5)

        columns = ("Mã NV", "Họ và Tên", "Giới tính", "Ngày sinh", "SĐT",
                "Địa chỉ", "Chức vụ", "Phòng ban")
        self.emp_table = self.create_table(frame, columns)
        self.load_employees()

        self.emp_table.bind("<Button-3>", self.right_click_employee)

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


    def right_click_employee(self, event):
        sel = self.emp_table.focus()
        if not sel:
            return

        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Sửa", command=lambda: self.edit_employee(sel))
        menu.add_command(label="Xóa", command=lambda: self.delete_employee(sel))
        menu.post(event.x_root, event.y_root)

    def add_employee(self):
        EmployeeDialog(self, self.cursor, self.conn, self.load_employees).open()

    def edit_employee(self, item):
        data = self.emp_table.item(item, "values")
        EmployeeDialog(self, self.cursor, self.conn, self.load_employees,
                       emp_data=data).open()

    def delete_employee(self, item):
        emp_id = self.emp_table.item(item, "values")[0]

        if not messagebox.askyesno("Xóa", f"Xóa nhân viên {emp_id}?"):
            return

        self.cursor.execute("DELETE FROM salaries WHERE emp_id=?", emp_id)
        self.cursor.execute("DELETE FROM employees WHERE id=?", emp_id)
        self.conn.commit()
        self.load_employees()

    # ========== PHÒNG BAN ==========
    def show_department_page(self, btn=None):
        if btn:
            self.set_active_button(btn)
        self.clear_content()

        tk.Label(self.content, text="Quản lý phòng ban",
         bg=self.colors["dark"]["content"] if self.dark_mode else self.colors["light"]["content"],
         fg=self.colors["dark"]["text"] if self.dark_mode else self.colors["light"]["text"],
         font=("Arial", 18, "bold")).pack(anchor="w", padx=20, pady=10)

        columns = ("Mã PB", "Tên phòng", "Số NV", "Chi tiết")
        table = self.create_table(self.content, columns)

        self.cursor.execute("SELECT dept_id, dept_name FROM departments")

        for dept_id, name in self.cursor.fetchall():
            self.cursor.execute("SELECT COUNT(*) FROM employees WHERE dept_id=?", dept_id)
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

    def delete_department(self, dept_id):
        if not messagebox.askyesno("Xóa", f"Xóa phòng ban {dept_id}?"):
            return
        
        self.cursor.execute("DELETE FROM departments WHERE dept_id=?", dept_id)
        self.conn.commit()
        self.show_department_page(self.btn_dept)


    def show_employees_by_dept(self, dept_id):
        self.clear_content()
        tk.Label(self.content, text=f"Nhân viên phòng {dept_id}",
                 bg="#f8fafc", font=("Arial", 18, "bold")).pack(anchor="w", padx=20, pady=10)

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


    # ========== LƯƠNG ==========
    def show_salary_page(self, btn=None):
        if btn:
            self.set_active_button(btn)
        self.clear_content()

        tk.Label(self.content, text="Quản lý lương",
         bg=self.colors["dark"]["content"] if self.dark_mode else self.colors["light"]["content"],
         fg=self.colors["dark"]["text"] if self.dark_mode else self.colors["light"]["text"],
         font=("Arial", 18, "bold")).pack(anchor="w", padx=20, pady=10)

        columns = ("Mã NV", "Họ tên", "Số ngày công", "Lương chính thức")
        table = self.create_table(self.content, columns)

        self.cursor.execute("""
            SELECT e.id, e.name, s.working_days, s.official_salary
            FROM salaries s
            JOIN employees e ON s.emp_id = e.id
            ORDER BY e.id
        """)

        def right_click(event):
            sel = table.focus()
            if not sel:
                return

            values = table.item(sel, "values")

            menu = tk.Menu(self, tearoff=0)
            menu.add_command(label="Sửa lương", 
                command=lambda: self.edit_salary(values))
            menu.post(event.x_root, event.y_root)

        table.bind("<Button-3>", right_click)


        for row in self.cursor.fetchall():
            row = tuple(str(x) if x is not None else "" for x in row)
            table.insert("", "end", values=row)

    
    # ========== DARK MODE ==========
    def toggle_dark_mode(self, btn=None):
        self.dark_mode = not self.dark_mode
        mode = "dark" if self.dark_mode else "light"

        # Nút Dark Mode
        self.btn_dark_mode.configure(
            text="🌙     Dark Mode" if not self.dark_mode else "☀️ Light Mode"
        )

        # Cập nhật màu nền tổng thể
        self.configure(bg=self.colors[mode]["bg"])
        self.sidebar.configure(bg=self.colors[mode]["sidebar"])
        self.content.configure(bg=self.colors[mode]["content"])

        # Label trong sidebar
        for w in self.sidebar.winfo_children():
            if isinstance(w, tk.Label):
                w.configure(
                    bg=self.colors[mode]["sidebar"],
                    fg="white"
                )

        # Sidebar buttons
        for b in self.sidebar_buttons:
            b.configure(bg=self.sidebar_default_bg, fg="white")

        if self.active_button:
            self.active_button.configure(bg=self.sidebar_active_bg)

        # ==============================
        #   HÀM CẬP NHẬT TOÀN BỘ WIDGET
        # ==============================
        def recursive_update(widget):
            for w in widget.winfo_children():

                # Label
                if isinstance(w, tk.Label):
                    w.configure(
                        bg=self.colors[mode]["content"],
                        fg=self.colors[mode]["text"]
                    )

                # Frame
                elif isinstance(w, tk.Frame):
                    w.configure(bg=self.colors[mode]["content"])

                # Entry
                elif isinstance(w, tk.Entry):
                    w.configure(
                        bg="#334155" if mode == "dark" else "white",
                        fg="white" if mode == "dark" else "black",
                        insertbackground="white" if mode == "dark" else "black"
                    )

                # Button
                elif isinstance(w, tk.Button):
                    # Chỉ đổi màu các button không phải action button
                    if w["bg"] not in ["#0ea5e9", "#16a34a", "#dc2626"]:
                        w.configure(
                            bg="#475569" if mode == "dark" else "#e2e8f0",
                            fg="white" if mode == "dark" else "black"
                        )

                recursive_update(w)

        recursive_update(self.content)

        # ==============================
        #   TREEVIEW STYLE
        # ==============================
        style = ttk.Style()
        style.theme_use("default")

        if mode == "dark":
            style.configure(
                "Treeview",
                background="#1e293b",
                fieldbackground="#1e293b",
                foreground="white",
                rowheight=25,
                borderwidth=0
            )
            style.configure(
                "Treeview.Heading",
                background="#334155",
                foreground="white",
                font=("Arial", 11, "bold")
            )
            style.map(
                "Treeview",
                background=[("selected", "#2563eb")],
                foreground=[("selected", "white")]
            )
        else:
            style.configure(
                "Treeview",
                background="white",
                fieldbackground="white",
                foreground="black"
            )
            style.configure(
                "Treeview.Heading",
                background="#e2e8f0",
                foreground="black",
                font=("Arial", 11, "bold")
            )

    # ========== CLOSE ==========
    def on_close(self):
        if self.conn:
            self.conn.close()
        self.destroy()
