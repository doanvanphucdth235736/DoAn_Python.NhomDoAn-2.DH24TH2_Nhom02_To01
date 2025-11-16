# database.py

# =================== KẾT NỐI SQL SERVER ===================
import pyodbc
from tkinter import messagebox

def connect_sql_server():
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost;"
            "DATABASE=HR_DATABASE;"
            "Trusted_Connection=yes;"
        )
        return conn, conn.cursor()

    except Exception as e:
        messagebox.showerror("Lỗi kết nối SQL", str(e))
        return None, None
