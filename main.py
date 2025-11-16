# main.py

# =================== IMPORT CHÍNH CỦA APP ===================
from gui import HRDashboard

# =================== CẢI THIỆN DPI TRÊN WINDOWS ===================
import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

# =================== CHẠY ỨNG DỤNG ===================
if __name__ == "__main__":
    app = HRDashboard()
    app.mainloop()
