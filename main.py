from tkinter import*
from tkinter import ttk
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
        self.root.title("Face Recognition Attendance System")
        
        # Thêm phím tắt để thoát khỏi chế độ fullscreen (Esc)
        self.root.bind("<Escape>", self.toggle_fullscreen)
        
        # Hiển thị thông báo đang tải
        self.loading_label = Label(self.root, text="Loading application...", font=("verdana", 16, "bold"))
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
            self.pho_img1 = None
            self.dev_img1 = None
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
            
            # Tải các hình ảnh nút
            images_data = [
                (r".\Images_GUI\std1.jpg", "std_img1"),
                (r".\Images_GUI\det1.jpg", "det_img1"),
                (r".\Images_GUI\att.jpg", "att_img1"),
                (r".\Images_GUI\hlp.jpg", "hlp_img1"),
                (r".\Images_GUI\tra1.jpg", "tra_img1"),
                (r".\Images_GUI\qr1.png", "pho_img1"),
                (r".\Images_GUI\dev.jpg", "dev_img1"),
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

        # Tiêu đề
        title_lb1 = Label(bg_img, text="Attendance Management System Using Facial Recognition", font=("verdana", 30, "bold"), bg="white", fg="navyblue")
        title_lb1.place(x=0, y=0, width=screen_width, height=45)

        # Tính toán vị trí các nút để căn giữa
        button_width = 180
        button_height = 180
        button_spacing = 50  # Khoảng cách giữa các nút
        
        total_width_top_row = 4 * button_width + 3 * button_spacing
        start_x_top = (screen_width - total_width_top_row) // 2
        
        # Tạo các nút dưới tiêu đề - Hàng 1
        # Nút Student
        std_b1 = Button(bg_img, command=self.student_pannels, image=self.std_img1, cursor="hand2")
        std_b1.place(x=start_x_top, y=100, width=button_width, height=button_height)

        std_b1_1 = Button(bg_img, command=self.student_pannels, text="Student Panel", cursor="hand2", font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        std_b1_1.place(x=start_x_top, y=280, width=button_width, height=45)

        # Nút phát hiện khuôn mặt
        x2 = start_x_top + button_width + button_spacing
        det_b1 = Button(bg_img, command=self.face_rec, image=self.det_img1, cursor="hand2")
        det_b1.place(x=x2, y=100, width=button_width, height=button_height)

        det_b1_1 = Button(bg_img, command=self.face_rec, text="Face Detector", cursor="hand2", font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        det_b1_1.place(x=x2, y=280, width=button_width, height=45)

        # Nút điểm danh
        x3 = x2 + button_width + button_spacing
        att_b1 = Button(bg_img, command=self.attendance_pannel, image=self.att_img1, cursor="hand2")
        att_b1.place(x=x3, y=100, width=button_width, height=button_height)

        att_b1_1 = Button(bg_img, command=self.attendance_pannel, text="Attendance", cursor="hand2", font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        att_b1_1.place(x=x3, y=280, width=button_width, height=45)

        # Nút hỗ trợ
        x4 = x3 + button_width + button_spacing
        hlp_b1 = Button(bg_img, command=self.helpSupport, image=self.hlp_img1, cursor="hand2")
        hlp_b1.place(x=x4, y=100, width=button_width, height=button_height)

        hlp_b1_1 = Button(bg_img, command=self.helpSupport, text="Help Support", cursor="hand2", font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        hlp_b1_1.place(x=x4, y=280, width=button_width, height=45)

        # Hàng 2
        # Nút Train
        tra_b1 = Button(bg_img, command=self.train_pannels, image=self.tra_img1, cursor="hand2")
        tra_b1.place(x=start_x_top, y=350, width=button_width, height=button_height)

        tra_b1_1 = Button(bg_img, command=self.train_pannels, text="Data Train", cursor="hand2", font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        tra_b1_1.place(x=start_x_top, y=530, width=button_width, height=45)

        # Nút QR code
        pho_b1 = Button(bg_img, command=self.open_img, image=self.pho_img1, cursor="hand2")
        pho_b1.place(x=x2, y=350, width=button_width, height=button_height)

        pho_b1_1 = Button(bg_img, command=self.open_img, text="QR-Codes", cursor="hand2", font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        pho_b1_1.place(x=x2, y=530, width=button_width, height=45)

        # Nút Developers
        dev_b1 = Button(bg_img, command=self.developr, image=self.dev_img1, cursor="hand2")
        dev_b1.place(x=x3, y=350, width=button_width, height=button_height)

        dev_b1_1 = Button(bg_img, command=self.developr, text="Developers", cursor="hand2", font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        dev_b1_1.place(x=x3, y=530, width=button_width, height=45)

        # Nút Exit
        exi_b1 = Button(bg_img, command=self.Close, image=self.exi_img1, cursor="hand2")
        exi_b1.place(x=x4, y=350, width=button_width, height=button_height)

        exi_b1_1 = Button(bg_img, command=self.Close, text="Exit", cursor="hand2", font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        exi_b1_1.place(x=x4, y=530, width=button_width, height=45)

        # Thêm hướng dẫn thoát fullscreen
        exit_label = Label(bg_img, text="Press 'Esc' to toggle fullscreen mode", font=("verdana", 10), bg="white", fg="gray")
        exit_label.place(x=screen_width-300, y=screen_height-180, width=280, height=20)

# ==================Funtion for Open Images Folder==================
    def open_img(self):
        try:
            if os.path.exists("dataset"):
                os.startfile("dataset")
            else:
                messagebox.showerror("Error", "Dataset folder not found!", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open folder: {str(e)}", parent=self.root)
            
# ==================Functions Buttons=====================
    def student_pannels(self):
        self.new_window=Toplevel(self.root)
        self.new_window.state('zoomed')  # Chế độ zoomed cho cửa sổ con
        self.app=Student(self.new_window)

    def train_pannels(self):
        self.new_window=Toplevel(self.root)
        self.new_window.state('zoomed')  # Chế độ zoomed cho cửa sổ con
        self.app=Train(self.new_window)
    
    def face_rec(self):
        self.new_window=Toplevel(self.root)
        self.new_window.state('zoomed')  # Chế độ zoomed cho cửa sổ con
        self.app=Face_Recognition(self.new_window)
    
    def attendance_pannel(self):
        self.new_window=Toplevel(self.root)
        self.new_window.state('zoomed')  # Chế độ zoomed cho cửa sổ con
        self.app=Attendance(self.new_window)
    
    def developr(self):
        self.new_window=Toplevel(self.root)
        self.new_window.state('zoomed')  # Chế độ zoomed cho cửa sổ con
        self.app=Developer(self.new_window)
    
    def helpSupport(self):
        self.new_window=Toplevel(self.root)
        self.new_window.state('zoomed')  # Chế độ zoomed cho cửa sổ con
        self.app=Helpsupport(self.new_window)

    def Close(self):
        user_response = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=self.root)
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
