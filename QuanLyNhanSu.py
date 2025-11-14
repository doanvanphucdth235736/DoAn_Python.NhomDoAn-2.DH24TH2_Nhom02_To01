# =================== IMPORT THƯ VIỆN ===================
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pyodbc

# =================== CẢI THIỆN DPI TRÊN WINDOWS ===================
import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

# =================== KẾT NỐI SQL SERVER ===================
def connect_sql_server():
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost;"
            "DATABASE=HR_DATABASE;"
            "Trusted_Connection=yes;"
        )
        cursor = conn.cursor()
        return conn, cursor
    except Exception as e:
        messagebox.showerror("Kết nối lỗi", str(e))
        return None, None

# =================== GIAO DIỆN HỆ THỐNG QUẢN LÝ NHÂN SỰ ===================
class HRDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hệ thống quản lý nhân sự")
        self.geometry("1100x600")
        self.configure(bg="#f1f5f9")

        self.conn, self.cursor = connect_sql_server()
        if not self.conn:
            self.destroy()
            return

        # Sidebar
        self.sidebar = tk.Frame(self, bg="#032864", width=200)
        self.sidebar.pack(side="left", fill="y")
        self.content = tk.Frame(self, bg="#f8fafc")
        self.content.pack(side="right", expand=True, fill="both")

        self._build_sidebar()
        self.show_employee_page()

    # =================== SIDEBAR ===================
    def _build_sidebar(self):
        tk.Label(self.sidebar, text="HR SYSTEM", fg="white", bg="#032864",
                 font=("Arial", 16, "bold"), pady=20).pack()
        btn_style = {
            "bg": "#1e293b",
            "fg": "white",
            "font": ("Arial", 12),
            "bd": 0,
            "activebackground": "#334155",
            "activeforeground": "white",
            "anchor": "w",
            "padx": 20,
            "pady": 10
        }

        tk.Button(self.sidebar, text="👤 Quản lý nhân viên",
                  command=self.show_employee_page, **btn_style).pack(fill="x")
        tk.Button(self.sidebar, text="🏢 Quản lý phòng ban",
                  command=self.show_department_page, **btn_style).pack(fill="x")
        tk.Button(self.sidebar, text="💰 Quản lý lương",
                  command=self.show_salary_page, **btn_style).pack(fill="x")
        tk.Label(self.sidebar, bg="#1e293b").pack(expand=True, fill="both")

    # =================== XÓA NỘI DUNG ===================
    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    # =================== QUẢN LÝ NHÂN VIÊN ===================
    def show_employee_page(self):
        self.clear_content()
        tk.Label(self.content, text="Quản lý nhân viên",
                 font=("Arial", 18, "bold"),
                 bg="#f8fafc", fg="#0f172a").pack(anchor="w", padx=20, pady=10)

        frame = tk.Frame(self.content, bg="#f8fafc")
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Button(frame, text="➕ Thêm mới", bg="#0ea5e9",
                  fg="white", font=("Arial", 11, "bold"),
                  relief="flat", padx=10, pady=5,
                  command=self.add_employee).pack(anchor="e", pady=5)

        columns = ("Mã NV", "Họ và Tên", "Giới tính", "SĐT",
                   "Địa chỉ", "Chức vụ", "Phòng ban")
        self.emp_table = ttk.Treeview(
            frame, columns=columns, show="headings", height=12)

        for col in columns:
            self.emp_table.heading(col, text=col)
            self.emp_table.column(col, width=130, anchor="center")

        self.emp_table.pack(fill="both", expand=True, pady=10)

        self.load_employees()
        self.emp_table.bind("<Button-3>", self.emp_right_click)

    def load_employees(self):
        for row in self.emp_table.get_children():
            self.emp_table.delete(row)

        self.cursor.execute("""
            -- Đảm bảo thứ tự cột TRẢ VỀ từ DB khớp với tiêu đề Treeview
            SELECT e.id, e.name, e.gender, e.phone, e.address,
            -- ^ Mã NV, ^ Họ và Tên, ^ Giới tính, ^ SĐT, ^ Địa chỉ
                   p.position_name, d.dept_name
            --     ^ Chức vụ,       ^ Phòng ban
            FROM employees e
            LEFT JOIN positions p ON e.position_id = p.position_id
            LEFT JOIN departments d ON e.dept_id = d.dept_id
        """)
        for row in self.cursor.fetchall():
            row = tuple(str(x) if x is not None else "" for x in row)
            self.emp_table.insert("", "end", values=row)

    def emp_right_click(self, event):
        selected = self.emp_table.focus()
        if not selected:
            return
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Sửa",
                         command=lambda: self.edit_employee(selected))
        menu.add_command(label="Xóa",
                         command=lambda: self.delete_employee(selected))
        menu.post(event.x_root, event.y_root)

    def add_employee(self):
        EmployeeDialog(self, self.cursor,
                       self.conn, self.load_employees).open()

    def edit_employee(self, item):
        values = self.emp_table.item(item, "values")
        EmployeeDialog(self, self.cursor, self.conn,
                       self.load_employees, emp_data=values).open()

    def delete_employee(self, item):
        emp_id = self.emp_table.item(item, "values")[0]
        if messagebox.askyesno("Xóa nhân viên",
                               f"Bạn có chắc muốn xóa {emp_id}?"):
            self.cursor.execute("DELETE FROM salaries WHERE emp_id=?", emp_id)
            self.cursor.execute("DELETE FROM employees WHERE id=?", emp_id)
            self.conn.commit()
            self.load_employees()
            messagebox.showinfo("Xóa thành công",
                                f"Nhân viên {emp_id} đã bị xóa.")

    # =================== QUẢN LÝ PHÒNG BAN ===================
    def show_department_page(self):
        self.clear_content()
        tk.Label(self.content, text="Quản lý phòng ban",
                 font=("Arial", 18, "bold"),
                 bg="#f8fafc", fg="#0f172a").pack(anchor="w", padx=20, pady=10)

        frame = tk.Frame(self.content, bg="#f8fafc")
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("Mã PB", "Tên phòng", "Số nhân viên", "Chi tiết")
        table = ttk.Treeview(frame, columns=columns,
                             show="headings", height=12)

        for col in columns:
            table.heading(col, text=col)
            table.column(col, width=200, anchor="center")

        self.cursor.execute("SELECT dept_id, dept_name FROM departments")
        for dept_id, name in self.cursor.fetchall():
            self.cursor.execute(
                "SELECT COUNT(*) FROM employees WHERE dept_id=?", dept_id)
            count = self.cursor.fetchone()[0]
            table.insert("", "end", values=(dept_id, name, count, "Xem thêm"))

        table.pack(fill="both", expand=True, pady=10)

        def on_click(event):
            selected = table.focus()
            if not selected:
                return

            col = table.identify_column(event.x)  # <-- FIX CHÍNH
            if col == "#4":  # Cột "Xem thêm"
                dept_id = table.item(selected, "values")[0]
                self.show_employees_by_dept(dept_id)

        table.bind("<Button-1>", on_click)

    def show_employees_by_dept(self, dept_id):
        self.clear_content()
        tk.Label(self.content, text=f"Nhân viên phòng {dept_id}",
                 font=("Arial", 18, "bold"),
                 bg="#f8fafc", fg="#0f172a").pack(anchor="w", padx=20, pady=10)

        frame = tk.Frame(self.content, bg="#f8fafc")
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("Mã NV", "Họ và Tên", "Chức vụ")
        table = ttk.Treeview(
            frame, columns=columns, show="headings", height=12)
        for col in columns:
            table.heading(col, text=col)
            table.column(col, width=200, anchor="center")

        self.cursor.execute("""
            SELECT e.id, e.name, p.position_name
            FROM employees e
            LEFT JOIN positions p ON e.position_id = p.position_id
            WHERE e.dept_id = ?
        """, dept_id)

        for row in self.cursor.fetchall():
            row = tuple(str(x) if x is not None else "" for x in row)
            table.insert("", "end", values=row)


        table.pack(fill="both", expand=True, pady=10)

    # =================== QUẢN LÝ LƯƠNG ===================
    def show_salary_page(self):
        self.clear_content()
        tk.Label(self.content, text="Quản lý lương",
                 font=("Arial", 18, "bold"),
                 bg="#f8fafc", fg="#0f172a").pack(anchor="w", padx=20, pady=10)

        frame = tk.Frame(self.content, bg="#f8fafc")
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("Mã NV", "Họ và Tên", "Số ngày công", "Lương chính thức")
        table = ttk.Treeview(
            frame, columns=columns, show="headings", height=12)

        for col in columns:
            table.heading(col, text=col)
            table.column(col, width=150, anchor="center")

        self.cursor.execute("""
            SELECT e.id, e.name, s.working_days, s.official_salary
            FROM salaries s
            JOIN employees e ON s.emp_id = e.id
        """)
        for row in self.cursor.fetchall():
            row = tuple(str(x) if x is not None else "" for x in row)
            table.insert("", "end", values=row)

        table.pack(fill="both", expand=True, pady=10)

# =================== DIALOG THÊM/SỬA NHÂN VIÊN ===================
class EmployeeDialog:
    def __init__(self, parent, cursor, conn, refresh_callback, emp_data=None):
        self.parent = parent
        self.cursor = cursor
        self.conn = conn
        self.refresh_callback = refresh_callback
        self.emp_data = emp_data

    def open(self):
        self.win = tk.Toplevel(self.parent)
        self.win.title(
            "Thêm nhân viên" if not self.emp_data else f"Sửa {self.emp_data[1]}")
        labels = ["Mã NV", "Họ và Tên", "Giới tính",
                  "SĐT", "Địa chỉ", "Chức vụ", "Phòng ban"]
        self.entries = {}

        for i, label in enumerate(labels):
            tk.Label(self.win, text=label).grid(
                row=i, column=0, padx=10, pady=5)

            if label == "Chức vụ":
                combo = ttk.Combobox(self.win, width=30, state="readonly")
                self.cursor.execute(
                    "SELECT position_id, position_name FROM positions")
                data = self.cursor.fetchall()
                self.position_map = {f"{name}": pid for (pid, name) in data}
                combo["values"] = list(self.position_map.keys())
                self.entries[label] = combo
                combo.grid(row=i, column=1, padx=10, pady=5)

            elif label == "Phòng ban":
                combo = ttk.Combobox(self.win, width=30, state="readonly")
                self.cursor.execute(
                    "SELECT dept_id, dept_name FROM departments")
                data = self.cursor.fetchall()
                self.dept_map = {f"{name}": did for (did, name) in data}
                combo["values"] = list(self.dept_map.keys())
                self.entries[label] = combo
                combo.grid(row=i, column=1, padx=10, pady=5)

            else:
                entry = tk.Entry(self.win, width=33)
                entry.grid(row=i, column=1, padx=10, pady=5)
                self.entries[label] = entry

        if self.emp_data:
            for i, label in enumerate(labels):
                value = self.emp_data[i]
                try:
                    self.entries[label].insert(0, value)
                except:
                    pass

        tk.Button(self.win, text="Lưu", command=self.save).grid(
            row=len(labels), column=0, columnspan=2, pady=10)

    def save(self):
        try:
            data = {lbl: self.entries[lbl].get() for lbl in self.entries}

            position_id = self.position_map.get(data["Chức vụ"], None)
            dept_id = self.dept_map.get(data["Phòng ban"], None)

            if not position_id or not dept_id:
                messagebox.showerror("Lỗi", "Chức vụ hoặc phòng ban không hợp lệ!")
                return

            if self.emp_data:  # === UPDATE ===
                self.cursor.execute("""
                    UPDATE employees
                    SET name=?, gender=?, phone=?, address=?,
                        position_id=?, dept_id=?
                    WHERE id=?
                """, data["Họ và Tên"], data["Giới tính"], data["SĐT"],
                     data["Địa chỉ"], position_id, dept_id, data["Mã NV"])
            else:  # === INSERT ===
                self.cursor.execute("""
                    INSERT INTO employees (id,name,gender,phone,address,position_id,dept_id)
                    VALUES (?,?,?,?,?,?,?)
                """, data["Mã NV"], data["Họ và Tên"], data["Giới tính"],
                     data["SĐT"], data["Địa chỉ"], position_id, dept_id)

                self.cursor.execute(
                    "INSERT INTO salaries (emp_id) VALUES (?)", data["Mã NV"])

            self.conn.commit()
            self.refresh_callback()
            self.win.destroy()
            messagebox.showinfo("Thành công", "Lưu nhân viên thành công!")

        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

# =================== CHẠY APP ===================
if __name__ == "__main__":
    app = HRDashboard()
    app.mainloop()
