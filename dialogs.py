# dialogs.py
import tkinter as tk
from tkinter import ttk, messagebox


class EmployeeDialog:
    def __init__(self, parent, cursor, conn, refresh_callback, emp_data=None):
        self.parent = parent
        self.cursor = cursor
        self.conn = conn
        self.refresh_callback = refresh_callback
        self.emp_data = emp_data
        self.original_id = emp_data[0] if emp_data else None

    # =================== OPEN DIALOG ===================
    def open(self):
        self.win = tk.Toplevel(self.parent)
        self.win.title("Sửa nhân viên" if self.emp_data else "Thêm nhân viên")

        labels = ["Mã NV", "Họ và Tên", "Giới tính", "Ngày sinh",
                  "SĐT", "Địa chỉ", "Chức vụ", "Phòng ban"]
        self.entries = {}

        for i, label in enumerate(labels):
            tk.Label(self.win, text=label).grid(row=i, column=0, padx=10, pady=5)

            # Combobox: CHỨC VỤ
            if label == "Chức vụ":
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

        # Fill old values for edit
        if self.emp_data:
            for lbl, value in zip(labels, self.emp_data):
                if isinstance(self.entries[lbl], ttk.Combobox):
                    self.entries[lbl].set(value)
                else:
                    self.entries[lbl].insert(0, value)

        tk.Button(self.win, text="Lưu", bg="#0284c7", fg="white",
                  command=self.save).grid(row=len(labels), columnspan=2, pady=10)

    # ================= SAVE DATA =================
    def save(self):
        try:
            data = {lbl: self.entries[lbl].get().strip() for lbl in self.entries}

            if not data["Mã NV"]:
                return messagebox.showerror("Lỗi", "Mã NV không được để trống")

            if not data["SĐT"].isdigit():
                return messagebox.showerror("Lỗi", "Số điện thoại phải là số")

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


class DepartmentDialog:
    def __init__(self, parent, cursor, conn, reload, dept_data=None):
        self.parent = parent
        self.cursor = cursor
        self.conn = conn
        self.reload = reload
        self.dept_data = dept_data

    def open(self):
        win = tk.Toplevel(self.parent)
        win.title("Phòng ban")
        win.geometry("350x200")

        tk.Label(win, text="Tên phòng ban:").pack()
        self.name_var = tk.StringVar()
        tk.Entry(win, textvariable=self.name_var).pack()

        if self.dept_data:
            self.name_var.set(self.dept_data[1])

        tk.Button(win, text="Lưu", command=self.save).pack(pady=10)

    def save(self):
        name = self.name_var.get().strip()

        if self.dept_data:
            self.cursor.execute(
                "UPDATE departments SET dept_name=? WHERE dept_id=?",
                (name, self.dept_data[0])
            )
        else:
            self.cursor.execute(
                "INSERT INTO departments (dept_name) VALUES (?)", (name,)
            )

        self.conn.commit()
        self.reload()

class SalaryDialog:
    def __init__(self, parent, cursor, conn, reload, data):
        self.parent = parent
        self.cursor = cursor
        self.conn = conn
        self.reload = reload
        self.data = data

    def open(self):
        win = tk.Toplevel(self.parent)
        win.title("Sửa lương")
        win.geometry("350x200")

        tk.Label(win, text="Số ngày công:").pack()
        self.days = tk.Entry(win)
        self.days.pack()
        self.days.insert(0, self.data[2])

        tk.Label(win, text="Lương:").pack()
        self.sal = tk.Entry(win)
        self.sal.pack()
        self.sal.insert(0, self.data[3])

        tk.Button(win, text="Lưu", command=self.save).pack(pady=10)

    def save(self):
        self.cursor.execute("""
            UPDATE salaries SET working_days=?, official_salary=? 
            WHERE emp_id=?
        """, (self.days.get(), self.sal.get(), self.data[0]))

        self.conn.commit()
        self.reload()

