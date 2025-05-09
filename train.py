from sys import path
from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
import os
import mysql.connector
import cv2
import numpy as np
from tkinter import messagebox

class Train:

    def __init__(self,root):
        self.root=root
        # Thiết lập toàn màn hình
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.title("Train Panel")
        
        # Thêm phím tắt để thoát khỏi chế độ fullscreen (Esc)
        self.root.bind("<Escape>", self.toggle_fullscreen)

        # This part is image labels setting start 
        # first header image  
        img=Image.open(r".\Images_GUI\banner.jpg")
        img=img.resize((screen_width,130),Image.LANCZOS)
        self.photoimg=ImageTk.PhotoImage(img)

        # set image as lable
        f_lb1 = Label(self.root,image=self.photoimg)
        f_lb1.place(x=0,y=0,width=screen_width,height=130)

        # backgorund image 
        bg1=Image.open(r".\Images_GUI\t_bg1.jpg")
        bg1=bg1.resize((screen_width,screen_height),Image.LANCZOS)
        self.photobg1=ImageTk.PhotoImage(bg1)

        # set image as lable
        bg_img = Label(self.root,image=self.photobg1)
        bg_img.place(x=0,y=130,width=screen_width,height=screen_height-130)


        #title section
        title_lb1 = Label(bg_img,text="Welcome to Training Panel",font=("verdana",30,"bold"),bg="white",fg="navyblue")
        title_lb1.place(x=0,y=0,width=screen_width,height=45)

        # Căn giữa nút train
        button_width = 180
        button_height = 180
        btn_x = (screen_width - button_width) // 2
        
        # Create buttons below the section 
        # ------------------------------------------------------------------------------------------------------------------- 
        # Training button 1
        std_img_btn=Image.open(r".\Images_GUI\t_btn1.png")
        std_img_btn=std_img_btn.resize((button_width,button_height),Image.LANCZOS)
        self.std_img1=ImageTk.PhotoImage(std_img_btn)

        std_b1 = Button(bg_img,command=self.train_classifier,image=self.std_img1,cursor="hand2")
        std_b1.place(x=btn_x,y=170,width=button_width,height=button_height)

        std_b1_1 = Button(bg_img,command=self.train_classifier,text="Train Dataset",cursor="hand2",font=("tahoma",15,"bold"),bg="white",fg="navyblue")
        std_b1_1.place(x=btn_x,y=350,width=button_width,height=45)
        
        # Thêm hướng dẫn thoát fullscreen
        exit_label = Label(bg_img, text="Press 'Esc' to toggle fullscreen mode", font=("verdana", 10), bg="white", fg="gray")
        exit_label.place(x=screen_width-300, y=screen_height-180, width=280, height=20)
    
    def toggle_fullscreen(self, event=None):
        """Chuyển đổi giữa chế độ fullscreen và không fullscreen"""
        is_fullscreen = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not is_fullscreen)
        return "break"

    # ==================Create Function of Traing===================
    def train_classifier(self):
        data_dir = ("data_img")
        # Kiểm tra thư mục
        if not os.path.exists(data_dir):
            messagebox.showerror("Error", "Dataset folder not found! Please create data_img folder first.", parent=self.root)
            return

        # Hiển thị progress bar
        progress_label = Label(self.root, text="Training is in progress...", font=("verdana", 12, "bold"), bg="white", fg="navyblue")
        progress_label.place(x=500, y=120, width=300, height=30)
        
        progress_bar = ttk.Progressbar(self.root, orient=HORIZONTAL, length=250, mode='determinate')
        progress_bar.place(x=500, y=150, width=300, height=20)
        
        try:
            # Lấy danh sách ảnh
            path = [os.path.join(data_dir, file) for file in os.listdir(data_dir) if file.endswith(('.jpg', '.png', '.jpeg'))]
            
            if len(path) == 0:
                messagebox.showerror("Error", "No images found in dataset folder!", parent=self.root)
                progress_label.destroy()
                progress_bar.destroy()
                return
            
            # Hiển thị thông tin
            counts_label = Label(self.root, text=f"Found {len(path)} images to train", font=("verdana", 12), bg="white", fg="navyblue")
            counts_label.place(x=500, y=180, width=300, height=20)
            
            # Chuẩn bị dữ liệu
            faces = []
            ids = []
            total_images = len(path)
            
            # Cập nhật progress bar
            self.root.update()
            progress_bar["maximum"] = total_images
            progress_bar["value"] = 0
            
            # Xử lý từng ảnh
            for i, image_path in enumerate(path):
                try:
                    # Cập nhật progress
                    progress_bar["value"] = i + 1
                    progress_label.config(text=f"Processing image {i+1}/{total_images}")
                    self.root.update()
                    
                    # Đọc và xử lý ảnh
                    img = Image.open(image_path).convert('L')  # Chuyển sang ảnh grayscale
                    img_np = np.array(img, 'uint8')
                    
                    # Lấy ID từ tên file
                    id = int(os.path.split(image_path)[1].split('.')[1])
                    
                    faces.append(img_np)
                    ids.append(id)
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Error processing image {image_path}: {str(e)}", parent=self.root)
                    continue
            
            # Kiểm tra dữ liệu trước khi training
            if len(faces) == 0:
                messagebox.showerror("Error", "No valid faces found for training!", parent=self.root)
                progress_label.destroy()
                progress_bar.destroy()
                counts_label.destroy()
                return
                
            # Thông báo bắt đầu training
            progress_label.config(text="Training classifier...")
            self.root.update()
            
            # Chuyển đổi sang numpy array
            ids = np.array(ids)
            
            # Train classifier
            clf = cv2.face.LBPHFaceRecognizer_create()
            clf.train(faces, ids)
            
            # Lưu model
            clf_path = "clf.xml"
            clf.write(clf_path)
            
            # Hiển thị thông báo thành công
            progress_label.config(text="Training completed successfully!")
            progress_bar["value"] = total_images
            self.root.update()
            
            # Hiển thị hộp thoại thành công
            messagebox.showinfo("Success", f"Training completed with {len(faces)} images!", parent=self.root)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error during training: {str(e)}", parent=self.root)
        finally:
            # Dọn dẹp UI
            if 'progress_label' in locals():
                progress_label.destroy()
            if 'progress_bar' in locals():
                progress_bar.destroy()
            if 'counts_label' in locals():
                counts_label.destroy()




if __name__ == "__main__":
    root=Tk()
    obj=Train(root)
    root.mainloop()