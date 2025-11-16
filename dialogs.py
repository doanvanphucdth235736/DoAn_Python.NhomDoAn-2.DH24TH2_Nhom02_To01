# dialogs.py

# =================== IMPORT MODULES ===================
import tkinter as tk
from tkinter import ttk, messagebox

# =================== DIALOG NHÂN VIÊN ===================
class EmployeeDialog:
    def __init__(self, parent, cursor, conn, refresh_callback, emp_data=None):
        self.parent = parent
        self.cursor = cursor
        self.conn = conn
        self.refresh_callback = refresh_callback
        self.emp_data = emp_data
        self.original_id = emp_data[0] if emp_data else None

    # ----------------- MỞ DIALOG NHÂN VIÊN ----------------
    def open(self):
        self.win = tk.Toplevel(self.parent)
        self.win.title("Sửa nhân viên" if self.emp_data else "Thêm nhân viên")

        labels = ["Mã NV", "Họ và Tên", "Giới tính", "Ngày sinh",
                  "SĐT", "Địa chỉ", "Chức vụ", "Phòng ban"]
        self.entries = {}

        for i, label in enumerate(labels):
            tk.Label(self.win, text=label).grid(row=i, column=0, padx=10, pady=5)

            # Combobox: GIỚI TÍNH
            if label == "Giới tính":
                combo = ttk.Combobox(self.win, width=30, state="readonly")
                combo["values"] = ["Nam", "Nữ"]    
                combo.grid(row=i, column=1)
                self.entries[label] = combo

            # Combobox: CHỨC VỤ
            elif label == "Chức vụ":
                combo = ttk.Combobox(self.win, width=30, state="readonly")
                self.cursor.execute("SELECT position_id, position_name FROM positions")
                data = self.cursor.fetchall()
                self.position_map = {name: pid for pid, name in data}
                combo["values"] = list(self.position_map.keys())
                combo.grid(row=i, column=1)
                self.entries[label] = combo

            # Combobox: PHÒNG BAN
            elif label == "Phòng ban":
                combo = ttk.Combobox(self.win, width=30, state="readonly")
                self.cursor.execute("SELECT dept_id, dept_name FROM departments")
                data = self.cursor.fetchall()
                self.dept_map = {name: did for did, name in data}
                combo["values"] = list(self.dept_map.keys())
                combo.grid(row=i, column=1)
                self.entries[label] = combo

            else:
                entry = tk.Entry(self.win, width=33)
                entry.grid(row=i, column=1)
                self.entries[label] = entry

        # Nếu sửa → điền dữ liệu cũ
        if self.emp_data:
            for lbl, value in zip(labels, self.emp_data):
                if isinstance(self.entries[lbl], ttk.Combobox):
                    self.entries[lbl].set(value)
                else:
                    self.entries[lbl].insert(0, value)

        tk.Button(
            self.win,
            text="💾  Lưu",
            bg="#0284c7",
            fg="white",
            font=("Arial", 13, "bold"),  
            width=12,                   
            height=1,                    
            cursor="hand2",
            command=self.save
        ).grid(row=len(labels), columnspan=2, pady=15)
        

    # ------------------ LƯU DỮ LIỆU NHÂN VIÊN ----------------
    def save(self):
        try:
            data = {lbl: self.entries[lbl].get().strip() for lbl in self.entries}

            if not data["Mã NV"]:
                return messagebox.showerror("Lỗi", "Mã NV không được để trống")
            if not self.emp_data:  # Chỉ kiểm tra khi thêm mới
                self.cursor.execute("SELECT id FROM employees WHERE id=?", (data["Mã NV"],))
                if self.cursor.fetchone() is not None:
                    return messagebox.showerror("Lỗi", "Mã nhân viên đã tồn tại!")

            if not data["SĐT"].isdigit():
                return messagebox.showerror("Lỗi", "Số điện thoại phải là số")
            
            import datetime
            try:
                datetime.datetime.strptime(data["Ngày sinh"], "%Y-%m-%d")
            except ValueError:
                return messagebox.showerror(
                    "Lỗi", 
                    "Ngày sinh phải đúng dạng YYYY-MM-DD (ví dụ: 2000-05-20)"
                )

            position_id = self.position_map[data["Chức vụ"]]
            dept_id = self.dept_map[data["Phòng ban"]]

            # UPDATE
            if self.emp_data:
                self.cursor.execute("""
                    UPDATE employees
                    SET name=?, gender=?, birthday=?, phone=?, address=?, 
                        position_id=?, dept_id=?
                    WHERE id=?
                """, (data["Họ và Tên"], data["Giới tính"], data["Ngày sinh"], data["SĐT"],
                      data["Địa chỉ"], position_id, dept_id, self.original_id))

            # INSERT
            else:
                self.cursor.execute("""
                    INSERT INTO employees (id,name,gender,birthday,phone,address,position_id,dept_id)
                    VALUES (?,?,?,?,?,?,?,?)
                """, (data["Mã NV"], data["Họ và Tên"], data["Giới tính"], data["Ngày sinh"],
                      data["SĐT"], data["Địa chỉ"], position_id, dept_id))

                self.cursor.execute(
                    "INSERT INTO salaries (emp_id) VALUES (?)", data["Mã NV"]
                )

            self.conn.commit()
            self.refresh_callback()
            self.win.destroy()
            messagebox.showinfo("Thành công", "Lưu dữ liệu thành công!")

        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

# =================== DIALOG PHÒNG BAN ===================
class DepartmentDialog:
    def __init__(self, parent, cursor, conn, refresh_callback, dept_data=None):
        self.parent = parent
        self.cursor = cursor
        self.conn = conn
        self.refresh_callback = refresh_callback
        self.dept_data = dept_data  # (dept_id, dept_name) nếu sửa

        self.win = tk.Toplevel()
        self.win.title("Phòng ban")
        self.win.geometry("370x220")
        self.win.resizable(False, False)
        self.win.grab_set()

        tk.Label(self.win, text="Mã phòng ban:", font=("Arial", 12)).pack(pady=5)
        self.var_id = tk.StringVar()
        tk.Entry(self.win, textvariable=self.var_id, font=("Arial", 12), width=25).pack(pady=2)

        tk.Label(self.win, text="Tên phòng ban:", font=("Arial", 12)).pack(pady=5)
        self.var_name = tk.StringVar()
        tk.Entry(self.win, textvariable=self.var_name, font=("Arial", 12), width=25).pack(pady=2)

        # Nút lưu
        tk.Button(
            self.win,
            text="💾 Lưu",
            font=("Arial", 13, "bold"),
            bg="#0ea5e9",
            fg="white",
            width=12,
            height=1,
            command=self.save
        ).pack(pady=15)

        # Nếu sửa → fill dữ liệu
        if dept_data:
            self.var_id.set(dept_data[0])
            self.original_id = dept_data[0]
            self.var_name.set(dept_data[1])
        else:
            self.original_id = None

    # ------------------ LƯU DỮ LIỆU PHÒNG BAN ----------------
    def save(self):
        dept_id = self.var_id.get().strip()
        dept_name = self.var_name.get().strip()

        if not dept_id or not dept_name:
            return messagebox.showerror("Lỗi", "Mã và tên phòng ban không được bỏ trống!")

        # KIỂM TRA TRÙNG MÃ (khi thêm mới)
        if not self.dept_data:
            self.cursor.execute("SELECT dept_id FROM departments WHERE dept_id=?", (dept_id,))
            if self.cursor.fetchone():
                return messagebox.showerror("Lỗi", "Mã phòng ban đã tồn tại!")

        # KIỂM TRA TRÙNG MÃ KHI SỬA (thay đổi sang mã khác)
        if self.dept_data and dept_id != self.original_id:
            self.cursor.execute("SELECT dept_id FROM departments WHERE dept_id=?", (dept_id,))
            if self.cursor.fetchone():
                return messagebox.showerror("Lỗi", "Mã phòng ban mới đã tồn tại!")

        try:
            if self.dept_data:  # UPDATE
                self.cursor.execute(
                    "UPDATE departments SET dept_id=?, dept_name=? WHERE dept_id=?",
                    (dept_id, dept_name, self.original_id)
                )

                # Update dept_id của employees nếu mã PB bị đổi
                if dept_id != self.original_id:
                    self.cursor.execute(
                        "UPDATE employees SET dept_id=? WHERE dept_id=?",
                        (dept_id, self.original_id)
                    )

            else:  # INSERT
                self.cursor.execute(
                    "INSERT INTO departments (dept_id, dept_name) VALUES (?, ?)",
                    (dept_id, dept_name)
                )

            self.conn.commit()
            self.refresh_callback()
            self.win.destroy()
            messagebox.showinfo("Thành công", "Lưu phòng ban thành công!")

        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    # ----------------- MỞ DIALOG PHÒNG BAN ----------------
    def open(self):
        self.win.mainloop()

# =================== DIALOG LƯƠNG NHÂN VIÊN ===================
class SalaryDialog:
    def __init__(self, parent, cursor, conn, reload, data):
        # data = (emp_id, name, working_days, salary, rating)
        self.parent = parent
        self.cursor = cursor
        self.conn = conn
        self.reload = reload
        self.data = data

    # ----------------- MỞ DIALOG LƯƠNG NHÂN VIÊN ----------------
    def open(self):
        win = tk.Toplevel(self.parent)
        win.title("Sửa lương")
        win.geometry("380x280")
        win.resizable(False, False)
        self.win = win

        # SỐ NGÀY CÔNG
        tk.Label(win, text="Số ngày công:", font=("Arial", 12)).pack(pady=5)
        self.days = tk.Entry(win, font=("Arial", 12))
        self.days.pack()
        self.days.insert(0, self.data[2])

        # ĐÁNH GIÁ (rating)
        tk.Label(win, text="Đánh giá:", font=("Arial", 12)).pack(pady=5)

        self.rating_combo = ttk.Combobox(
            win,
            state="readonly",
            width=25,
            font=("Arial", 11)
        )
        self.rating_combo["values"] = ("Xuất sắc", "Tốt", "Trung bình", "Kém")
        self.rating_combo.pack()

        # set rating cũ
        if self.data[4]:
            self.rating_combo.set(self.data[4])
        else:
            self.rating_combo.set("Tốt")

        tk.Button(
            win,
            text="💾 Lưu",
            bg="#0ea5e9",
            fg="white",
            font=("Arial", 12, "bold"),
            width=12,
            height=1,
            command=self.save
        ).pack(pady=15)
    
    # ------------------ LƯU DỮ LIỆU LƯƠNG NHÂN VIÊN ----------------
    def save(self):
        days = self.days.get().strip()
        rating = self.rating_combo.get()

        if not days.isdigit():
            return messagebox.showerror("Lỗi", "Ngày công phải là số!")

        self.cursor.execute("""
            UPDATE salaries
            SET working_days=?, rating=?
            WHERE emp_id=?
        """, (days, rating, self.data[0]))

        self.conn.commit()
        self.reload()
        self.win.destroy()
        messagebox.showinfo("Thành công", "Cập nhật lương thành công!")


