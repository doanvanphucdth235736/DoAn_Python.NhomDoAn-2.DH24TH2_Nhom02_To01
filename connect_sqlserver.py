import pyodbc

# 👇 Kết nối SQL Server bằng Windows Authentication
connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"            # hoặc tên máy + instance (VD: LAPTOP\\SQLEXPRESS)
    "DATABASE=qlns;"               # tên cơ sở dữ liệu bạn đã tạo
    "Trusted_Connection=yes;"      # sử dụng Windows Authentication
)

try:
    conn = pyodbc.connect(connection_string)
    print("✅ Kết nối thành công tới SQL Server!")

    cursor = conn.cursor()

    # 🧾 Thực hiện câu lệnh SQL ví dụ: thêm phòng ban mới
    insert_query = """
        INSERT INTO phongban (Maphongban, Tenphongban, Ngaynhanchuc)
        VALUES ('HC', N'Phòng Hành Chính', GETDATE());
        VALUES ('NS', N'Phòng Nhân Sự', GETDATE());
        VALUES ('KD', N'Phòng Kinh Doanh', GETDATE());
        VALUES ('MK', N'Phòng Marketing', GETDATE());
    """
    cursor.execute(insert_query)
    conn.commit()

    print("✅ Dữ liệu đã được lưu vào bảng phongban.")
    
except Exception as e:
    print("❌ Lỗi kết nối hoặc truy vấn:", e)
finally:
    if 'conn' in locals():
        conn.close()
        print("🔒 Đã đóng kết nối.")
