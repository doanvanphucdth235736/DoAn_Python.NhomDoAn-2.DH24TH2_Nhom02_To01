import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from tkcalendar import DateEntry
import mysql.connector
# ====== Kết nối MySQL ======
def connect_db():
    return mysql.connector.connect(
    host="localhost",
    user="root", # thay bằng user MySQL của bạn
    password="1234", # thay bằng password MySQL của bạn
    database="qlns"
 )

root = tk.Tk()
root.title("Quản lý nhân sự")
root.geometry("700x500")

