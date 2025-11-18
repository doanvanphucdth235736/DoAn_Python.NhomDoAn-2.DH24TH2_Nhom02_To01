----------------------------------------------------------- TẠO DATABASE---------------------------------------------------------
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'HR_DATABASE')
BEGIN
    CREATE DATABASE HR_DATABASE;
END;
GO

USE HR_DATABASE;
GO

----------------------------------------------------------- BẢNG PHÒNG BAN---------------------------------------------------------
IF NOT EXISTS (
    SELECT * FROM sysobjects WHERE name='departments' AND xtype='U'
)
BEGIN
    CREATE TABLE departments (
        dept_id NVARCHAR(20) PRIMARY KEY,	-- mã phòng
        dept_name NVARCHAR(100) NOT NULL	-- tên phòng
    );
END;
GO

----------------------------------------------------------- BẢNG CHỨC VỤ---------------------------------------------------------
IF NOT EXISTS (
    SELECT * FROM sysobjects WHERE name='positions' AND xtype='U'
)
BEGIN
    CREATE TABLE positions (
        position_id NVARCHAR(20) PRIMARY KEY,	-- mã chức vụ
        position_name NVARCHAR(100) NOT NULL,	-- tên chức vụ
        base_salary DECIMAL(18,2) NOT NULL		-- Lương cơ bản
    );
END;
GO

----------------------------------------------------------- BẢNG NHÂN VIÊN---------------------------------------------------------
IF NOT EXISTS (
    SELECT * FROM sysobjects WHERE name='employees' AND xtype='U'
)
BEGIN
    CREATE TABLE employees (
        id NVARCHAR(20) PRIMARY KEY,	-- mã nhân viên
        name NVARCHAR(100),				-- tên nhân viên 
		birthday DATE NULL,				-- ngày sinh
        position_id NVARCHAR(20),		-- mã chức vụ 
        gender NVARCHAR(10),			-- giới tính 
        phone NVARCHAR(20),				-- số điện thoại 
        address NVARCHAR(200),			-- địa chỉ 
        dept_id NVARCHAR(20),			-- mã phòng ban 
        FOREIGN KEY (dept_id) REFERENCES departments(dept_id),
        FOREIGN KEY (position_id) REFERENCES positions(position_id)
    );
END;
GO

----------------------------------------------------------- BẢNG LƯƠNG---------------------------------------------------------
IF NOT EXISTS (
    SELECT * FROM sysobjects WHERE name='salaries' AND xtype='U'
)
BEGIN
    CREATE TABLE salaries (
        emp_id NVARCHAR(20) PRIMARY KEY,	-- mã nhân viên 
        working_days INT DEFAULT 26,		-- số ngày công 
		official_salary INT,				-- lương chính thức = lương cơ bản * số ngày công / 30 ngày 
		rating NVARCHAR(10),				-- đánh giá
        FOREIGN KEY (emp_id) REFERENCES employees(id)
    );
END;
GO

CREATE TRIGGER trg_calc_salary
ON salaries
AFTER INSERT, UPDATE
AS
BEGIN
    UPDATE s
    SET official_salary = p.base_salary * s.working_days / 30
    FROM salaries s
    JOIN employees e ON e.id = s.emp_id
    JOIN positions p ON p.position_id = e.position_id;
END;
GO


----------------------------------------------------------- DỮ LIỆU MẪU---------------------------------------------------------

-- Phòng ban
DELETE FROM departments;
GO

-- Insert dữ liệu mẫu, chỉ nếu chưa tồn tại
IF NOT EXISTS (SELECT 1 FROM departments WHERE dept_id='KD')
INSERT INTO departments (dept_id, dept_name) VALUES
('KD', N'Kinh doanh'),
('KT', N'Kỹ thuật'),
('CV', N'Công Vụ'),
('MK', N'Marketing');
GO

-- Chức vụ
DELETE FROM positions;
GO

IF NOT EXISTS (SELECT 1 FROM positions WHERE position_id='TP')
INSERT INTO positions (position_id, position_name, base_salary) VALUES
('TP', N'Trưởng Phòng', 30000000),
('PP', N'Phó Phòng', 25000000),
('KT', N'Kế Toán', 20000000),
('NV', N'Nhân Viên', 15000000),
('TT', N'Thực Tập', 5000000);
GO

-- Nhân viên
DELETE FROM employees;
GO

IF NOT EXISTS (SELECT 1 FROM employees WHERE id='NV001')
INSERT INTO employees (id, name, birthday, position_id, gender, phone, address, dept_id) VALUES
('NV001', N'Nguyễn Văn A', '01/01/2000', 'TP', N'Nam', '0123456789', N'Hà Nội', 'KD'),
('NV002', N'Trần Thị B', '01/01/2000', 'PP', N'Nữ', '0123456789', N'Đà Nẵng', 'MK'),
('NV003', N'Lê Văn C', '01/01/2000', 'NV', N'Nam', '0123456789', N'Hồ Chí Minh', 'KT'),
('NV004', N'Phạm Thị D', '01/01/2000', 'KT', N'Nữ', '0123456789', N'Cần Thơ', 'KD');

-- Lương
DELETE FROM salaries;
GO

IF NOT EXISTS (SELECT 1 FROM salaries WHERE emp_id='NV001')
INSERT INTO salaries (emp_id, working_days) VALUES
('NV001', 26),
('NV002', 24),
('NV003', 22),
('NV004', 25);
GO
---------------------------------------------------------
PRINT 'HR_DATABASE đã được tạo thành công!';
GO