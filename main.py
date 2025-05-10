from tkinter import*
from tkinter import ttk
from tkinter import messagebox
from train import Train
from PIL import Image,ImageTk
from student import Student
from train import Train
from face_recognition import Face_Recognition
from attendance import Attendance
from developer import Developer
import os
import threading
from helpsupport import Helpsupport
import time
import mysql.connector

class Face_Recognition_System:
    def __init__(self,root):
        self.root=root
        # Thiết lập toàn màn hình
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.state('zoomed')  # Chế độ zoomed cho Windows
        self.root.attributes('-fullscreen', True)  # Chế độ fullscreen thực sự
        self.root.title("Hệ Thống Điểm Danh Bằng Nhận Diện Khuôn Mặt")
        
        # Thêm phím tắt để thoát khỏi chế độ fullscreen (Esc)
        self.root.bind("<Escape>", self.toggle_fullscreen)
        
        # Hiển thị thông báo đang tải
        self.loading_label = Label(self.root, text="Đang tải ứng dụng...", font=("verdana", 16, "bold"))
        self.loading_label.place(x=0, y=0, width=screen_width, height=screen_height)
        self.root.update()
        
        # Tải trước hình ảnh trong một luồng riêng
        threading.Thread(target=self.load_images).start()
    
    def toggle_fullscreen(self, event=None):
        """Chuyển đổi giữa chế độ fullscreen và không fullscreen"""
        is_fullscreen = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not is_fullscreen)
        return "break"
        
    def load_images(self):
        try:
            # Tạo các thuộc tính hình ảnh
            self.photoimg = None
            self.photobg1 = None
            self.std_img1 = None
            self.det_img1 = None
            self.att_img1 = None
            self.hlp_img1 = None
            self.tra_img1 = None
            self.exi_img1 = None
            
            # Lấy kích thước màn hình
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            # Tải hình ảnh banner với kích thước màn hình thực
            img=Image.open(r".\Images_GUI\banner.jpg")
            img=img.resize((screen_width, 130), Image.LANCZOS)
            self.photoimg=ImageTk.PhotoImage(img)

            # Tải hình ảnh nền
            bg1=Image.open(r".\Images_GUI\bg3.jpg")
            bg1=bg1.resize((screen_width, screen_height), Image.LANCZOS)
            self.photobg1=ImageTk.PhotoImage(bg1)
            
            # Tải các hình ảnh nút - đã xóa QR và Developers
            images_data = [
                (r".\Images_GUI\std1.jpg", "std_img1"),
                (r".\Images_GUI\det1.jpg", "det_img1"),
                (r".\Images_GUI\att.jpg", "att_img1"),
                (r".\Images_GUI\hlp.jpg", "hlp_img1"),
                (r".\Images_GUI\tra1.jpg", "tra_img1"),
                (r".\Images_GUI\exi.jpg", "exi_img1")
            ]
            
            for img_path, attr_name in images_data:
                img = Image.open(img_path)
                img = img.resize((180, 180), Image.LANCZOS)
                setattr(self, attr_name, ImageTk.PhotoImage(img))
            
            # Hoàn thành tải hình ảnh, xây dựng giao diện
            self.root.after(0, self.build_ui)
            
        except Exception as e:
            self.loading_label.config(text=f"Error loading images: {str(e)}")
            
    def build_ui(self):
        # Lấy kích thước màn hình
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Xóa nhãn loading
        self.loading_label.destroy()
        
        # Thiết lập banner và nền
        f_lb1 = Label(self.root, image=self.photoimg)
        f_lb1.place(x=0, y=0, width=screen_width, height=130)
        
        bg_img = Label(self.root, image=self.photobg1)
        bg_img.place(x=0, y=130, width=screen_width, height=screen_height-130)

        # Tiêu đề - Việt hóa
        title_lb1 = Label(bg_img, text="Hệ Thống Điểm Danh Bằng Nhận Diện Khuôn Mặt", 
                          font=("Times New Roman", 30, "bold"), 
                          bg="white", fg="#00008B")
        title_lb1.place(x=0, y=0, width=screen_width, height=45)

        # Tính toán vị trí các nút để căn giữa
        button_width = 180
        button_height = 180
        button_text_height = 50  # Tăng chiều cao phần text lên 50px
        button_spacing = 50  # Giảm khoảng cách giữa các nút để vừa với hàng ngang
        
        # Có 5 nút trên 1 hàng ngang
        buttons_count = 5
        total_width_row = buttons_count * button_width + (buttons_count - 1) * button_spacing
        start_x = (screen_width - total_width_row) // 2
        start_y = 150  # Đặt nút cao hơn một chút

        # Style cho các nút
        button_font = ("Times New Roman", 13, "bold")
        button_bg = "white"
        button_fg = "#000080"  # Navy blue
        button_relief = RAISED
        button_border = 2

        # Nút 1: Quản lý Sinh viên
        x1 = start_x
        std_b1 = Button(bg_img, command=self.student_pannels, image=self.std_img1, cursor="hand2", 
                       relief=button_relief, bd=button_border)
        std_b1.place(x=x1, y=start_y, width=button_width, height=button_height)

        std_b1_1 = Button(bg_img, command=self.student_pannels, text="Quản Lý Sinh Viên", 
                         cursor="hand2", font=button_font, 
                         bg=button_bg, fg=button_fg, relief=button_relief)
        std_b1_1.place(x=x1, y=start_y+button_height, width=button_width, height=button_text_height)

        # Nút 2: Nhận diện khuôn mặt
        x2 = x1 + button_width + button_spacing
        det_b1 = Button(bg_img, command=self.face_rec, image=self.det_img1, cursor="hand2", 
                       relief=button_relief, bd=button_border)
        det_b1.place(x=x2, y=start_y, width=button_width, height=button_height)

        det_b1_1 = Button(bg_img, command=self.face_rec, text="Nhận Diện Khuôn Mặt", 
                         cursor="hand2", font=button_font, 
                         bg=button_bg, fg=button_fg, relief=button_relief)
        det_b1_1.place(x=x2, y=start_y+button_height, width=button_width, height=button_text_height)

        # Nút 3: Điểm danh
        x3 = x2 + button_width + button_spacing
        att_b1 = Button(bg_img, command=self.attendance_pannel, image=self.att_img1, cursor="hand2", 
                       relief=button_relief, bd=button_border)
        att_b1.place(x=x3, y=start_y, width=button_width, height=button_height)

        att_b1_1 = Button(bg_img, command=self.attendance_pannel, text="Điểm Danh", 
                         cursor="hand2", font=button_font, 
                         bg=button_bg, fg=button_fg, relief=button_relief)
        att_b1_1.place(x=x3, y=start_y+button_height, width=button_width, height=button_text_height)

        # Nút 4: Huấn luyện dữ liệu
        x4 = x3 + button_width + button_spacing
        tra_b1 = Button(bg_img, command=self.train_pannels, image=self.tra_img1, cursor="hand2", 
                       relief=button_relief, bd=button_border)
        tra_b1.place(x=x4, y=start_y, width=button_width, height=button_height)

        tra_b1_1 = Button(bg_img, command=self.train_pannels, text="Huấn Luyện Dữ Liệu", 
                         cursor="hand2", font=button_font, 
                         bg=button_bg, fg=button_fg, relief=button_relief)
        tra_b1_1.place(x=x4, y=start_y+button_height, width=button_width, height=button_text_height)

        # Nút 5: Thoát
        x5 = x4 + button_width + button_spacing
        exi_b1 = Button(bg_img, command=self.Close, image=self.exi_img1, cursor="hand2", 
                       relief=button_relief, bd=button_border)
        exi_b1.place(x=x5, y=start_y, width=button_width, height=button_height)

        exi_b1_1 = Button(bg_img, command=self.Close, text="Thoát", 
                         cursor="hand2", font=button_font, 
                         bg=button_bg, fg="#8B0000", relief=button_relief)  # Màu đỏ đậm cho nút thoát
        exi_b1_1.place(x=x5, y=start_y+button_height, width=button_width, height=button_text_height)

        # Thêm hướng dẫn thoát fullscreen
        exit_label = Label(bg_img, text="Nhấn 'Esc' để bật/tắt chế độ toàn màn hình", 
                          font=("verdana", 10), bg="white", fg="gray")
        exit_label.place(x=screen_width-350, y=screen_height-180, width=330, height=20)

# ==================Funtion for Open Images Folder==================
    def open_img(self):
        try:
            if os.path.exists("dataset"):
                os.startfile("dataset")
            else:
                messagebox.showerror("Lỗi", "Không tìm thấy thư mục dataset!", parent=self.root)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở thư mục: {str(e)}", parent=self.root)
            
# ==================Functions Buttons=====================
    def student_pannels(self):
        self.new_window=Toplevel(self.root)
        self.new_window.state('zoomed')  # Chế độ zoomed cho cửa sổ con
        self.new_window.attributes('-fullscreen', True)  # Thêm dòng này để đảm bảo fullscreen
        self.app=Student(self.new_window)

    def train_pannels(self):
        self.new_window=Toplevel(self.root)
        self.new_window.state('zoomed')  # Chế độ zoomed cho cửa sổ con
        self.new_window.attributes('-fullscreen', True)  # Thêm dòng này để đảm bảo fullscreen
        self.app=Train(self.new_window)
    
    def face_rec(self):
        self.new_window=Toplevel(self.root)
        self.new_window.state('zoomed')  # Chế độ zoomed cho cửa sổ con
        self.new_window.attributes('-fullscreen', True)  # Thêm dòng này để đảm bảo fullscreen
        self.app=Face_Recognition(self.new_window)
    
    def attendance_pannel(self):
        self.new_window=Toplevel(self.root)
        self.new_window.state('zoomed')  # Chế độ zoomed cho cửa sổ con
        self.new_window.attributes('-fullscreen', True)  # Thêm dòng này để đảm bảo fullscreen
        self.app=Attendance(self.new_window)
    
    def developr(self):
        self.new_window=Toplevel(self.root)
        self.new_window.state('zoomed')  # Chế độ zoomed cho cửa sổ con
        self.new_window.attributes('-fullscreen', True)  # Thêm dòng này để đảm bảo fullscreen
        self.app=Developer(self.new_window)
    
    def helpSupport(self):
        self.new_window=Toplevel(self.root)
        self.new_window.state('zoomed')  # Chế độ zoomed cho cửa sổ con
        self.new_window.attributes('-fullscreen', True)  # Thêm dòng này để đảm bảo fullscreen
        self.app=Helpsupport(self.new_window)

    def Close(self):
        user_response = messagebox.askyesno("Thoát", "Bạn có chắc chắn muốn thoát?", parent=self.root)
        if user_response:
            self.root.destroy()

if __name__ == "__main__":
    try:
        root=Tk()
        obj=Face_Recognition_System(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"Application error: {str(e)}")
        if 'root' in locals():
            root.destroy()
