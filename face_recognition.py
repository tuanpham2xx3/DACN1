# import re
from sys import path
from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
import os
import mysql.connector
import cv2
import numpy as np
from tkinter import messagebox
from time import strftime
from datetime import datetime
class Face_Recognition:

    def __init__(self,root):
        self.root=root
        # Thiết lập toàn màn hình
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.title("Face Recognition Panel")
        
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
        bg1=Image.open(r".\Images_GUI\bg2.jpg")
        bg1=bg1.resize((screen_width,screen_height),Image.LANCZOS)
        self.photobg1=ImageTk.PhotoImage(bg1)

        # set image as lable
        bg_img = Label(self.root,image=self.photobg1)
        bg_img.place(x=0,y=130,width=screen_width,height=screen_height-130)


        #title section
        title_lb1 = Label(bg_img,text="Welcome to Face Recognition Panel",font=("verdana",30,"bold"),bg="white",fg="navyblue")
        title_lb1.place(x=0,y=0,width=screen_width,height=45)

        # Căn giữa nút face detector
        button_width = 180
        button_height = 180
        btn_x = (screen_width - button_width) // 2
        
        # Create buttons below the section 
        # ------------------------------------------------------------------------------------------------------------------- 
        # Training button 1
        std_img_btn=Image.open(r".\Images_GUI\f_det.jpg")
        std_img_btn=std_img_btn.resize((button_width,button_height),Image.LANCZOS)
        self.std_img1=ImageTk.PhotoImage(std_img_btn)

        std_b1 = Button(bg_img,command=self.face_recog,image=self.std_img1,cursor="hand2")
        std_b1.place(x=btn_x,y=170,width=button_width,height=button_height)

        std_b1_1 = Button(bg_img,command=self.face_recog,text="Face Detector",cursor="hand2",font=("tahoma",15,"bold"),bg="white",fg="navyblue")
        std_b1_1.place(x=btn_x,y=350,width=button_width,height=45)
        
        # Thêm hướng dẫn thoát fullscreen
        exit_label = Label(bg_img, text="Press 'Esc' to toggle fullscreen mode", font=("verdana", 10), bg="white", fg="gray")
        exit_label.place(x=screen_width-300, y=screen_height-180, width=280, height=20)
    #=====================Attendance===================

    def mark_attendance(self,i,r,n):
        with open("attendance.csv","r+",newline="\n") as f:
            myDatalist=f.readlines()
            name_list=[]
            for line in myDatalist:
                entry=line.split((","))
                name_list.append(entry[0])

            if((i not in name_list)) and ((r not in name_list)) and ((n not in name_list)):
                now=datetime.now()
                d1=now.strftime("%d/%m/%Y")
                dtString=now.strftime("%H:%M:%S")
                f.writelines(f"\n{i}, {r}, {n}, {dtString}, {d1}, Present")


    #================face recognition==================
    def face_recog(self):
        def draw_boundray(img, classifier, scaleFactor, minNeighbors, color, text, clf):
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Điều chỉnh tham số để tăng cường phát hiện khuôn mặt
            features = classifier.detectMultiScale(gray_image, scaleFactor=1.05, minNeighbors=4, minSize=(30, 30))
            
            if len(features) == 0:
                return []
            
            coord = []
            
            for (x, y, w, h) in features:
                # Tăng kích thước vùng khuôn mặt để cải thiện nhận diện
                y_offset = max(0, y - int(0.1 * h))
                h_new = min(gray_image.shape[0] - y_offset, int(1.2 * h))
                x_offset = max(0, x - int(0.05 * w))
                w_new = min(gray_image.shape[1] - x_offset, int(1.1 * w))
                
                face_region = gray_image[y_offset:y_offset+h_new, x_offset:x_offset+w_new]
                
                # Cải thiện độ tương phản trước khi nhận diện
                face_region = cv2.equalizeHist(face_region)
                
                try:
                    # Áp dụng cải thiện histogram trước khi nhận diện
                    id, predict = clf.predict(face_region)
                    # Điều chỉnh công thức tính độ tin cậy để chính xác hơn
                    confidence = int((100 * (1 - predict / 300)))
                    
                    print(f"DEBUG: Face detected with ID={id}, Confidence={confidence}%")
                    
                    # Kết nối database trong khối try-except riêng
                    try:
                        conn = mysql.connector.connect(username='root', password='12345', 
                                                     host='localhost', database='face_recognition', 
                                                     port=3307, connect_timeout=3)
                        cursor = conn.cursor()
                        
                        # Sử dụng prepared statement để tránh SQL injection
                        query = "SELECT Name, Roll_No, Student_ID FROM student WHERE Student_ID=%s"
                        cursor.execute(query, (str(id),))
                        result = cursor.fetchone()
                        
                        if result:
                            n, r, i = result
                            print(f"Found in database: Name={n}, Roll={r}, ID={i}")
                        else:
                            print(f"ID {id} not found in database")
                            n = r = i = "Unknown"
                            
                    except Exception as db_error:
                        print(f"Database error: {str(db_error)}")
                        n = r = i = "Unknown"
                    finally:
                        if 'cursor' in locals() and cursor:
                            cursor.close()
                        if 'conn' in locals() and conn:
                            conn.close()
                    
                    # Giảm ngưỡng xuống 45% để dễ nhận diện hơn
                    if confidence > 45:
                        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        cv2.rectangle(img, (x, y-90), (x+w, y), (0, 255, 0), -1)
                        cv2.putText(img, f"ID: {i}", (x+5, y-65), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                        cv2.putText(img, f"Roll: {r}", (x+5, y-45), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                        cv2.putText(img, f"Name: {n}", (x+5, y-25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                        cv2.putText(img, f"Conf: {confidence}%", (x+5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                        
                        self.mark_attendance(i, r, n)
                    else:
                        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
                        cv2.rectangle(img, (x, y-25), (x+w, y), (0, 0, 255), -1)
                        cv2.putText(img, "Unknown", (x+5, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                    
                    coord = [x, y, w, h]
                    
                except Exception as e:
                    print(f"Processing error: {str(e)}")
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    cv2.putText(img, "Processing Error", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            
            return coord

        def recognize(img, clf, faceCascade):
            coord = draw_boundray(img, faceCascade, 1.1, 10, (255, 25, 255), "Face", clf)
            return img
        
        # Kiểm tra các file cần thiết
        if not os.path.exists("clf.xml"):
            messagebox.showerror("Error", "Training file clf.xml not found! Please train the model first.", parent=self.root)
            return
        
        if not os.path.exists("haarcascade_frontalface_default.xml"):
            messagebox.showerror("Error", "Face detector file not found!", parent=self.root)
            return
        
        try:
            # Tải classifier
            clf = cv2.face.LBPHFaceRecognizer_create()
            clf.read("clf.xml")
            
            # Tải bộ phát hiện khuôn mặt
            faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
            
            # Kiểm tra camera
            videoCap = cv2.VideoCapture(0)
            if not videoCap.isOpened():
                messagebox.showerror("Error", "Cannot access camera! Please check your camera connection.", parent=self.root)
                return
            
            # Hiển thị thông báo 
            messagebox.showinfo("Starting", "Face recognition started.\nPress 'f' để bật/tắt chế độ fullscreen.\nPress Enter (Return) để thoát.", parent=self.root)
            
            # Thiết lập cửa sổ mặc định
            cv2.namedWindow("Face Recognition", cv2.WINDOW_NORMAL)
            
            # Trạng thái fullscreen
            is_fullscreen = False
            
            # Bắt đầu vòng lặp camera
            while True:
                ret, img = videoCap.read()
                if not ret:
                    messagebox.showerror("Error", "Failed to grab frame from camera!", parent=self.root)
                    break
                
                # Xử lý nhận diện
                img = recognize(img, clf, faceCascade)
                
                # Hiển thị thời gian thực
                now = datetime.now()
                dt_string = now.strftime("%H:%M:%S")
                cv2.putText(img, f"Time: {dt_string}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                
                # Hiển thị hướng dẫn
                cv2.putText(img, "Press 'f' for fullscreen, Enter to exit", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                # Hiển thị ảnh
                cv2.imshow("Face Recognition", img)
                
                # Xử lý phím nhấn
                key = cv2.waitKey(1)
                if key == 13:  # Enter key
                    break
                elif key == ord('f') or key == ord('F'):  # 'f' key để toggle fullscreen
                    is_fullscreen = not is_fullscreen
                    if is_fullscreen:
                        cv2.setWindowProperty("Face Recognition", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                    else:
                        cv2.setWindowProperty("Face Recognition", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
                    
            # Giải phóng tài nguyên
            videoCap.release()
            cv2.destroyAllWindows()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error during face recognition: {str(e)}", parent=self.root)
            # Đảm bảo giải phóng tài nguyên ngay cả khi có lỗi
            if 'videoCap' in locals() and videoCap.isOpened():
                videoCap.release()
            cv2.destroyAllWindows()

    def toggle_fullscreen(self, event=None):
        """Chuyển đổi giữa chế độ fullscreen và không fullscreen"""
        is_fullscreen = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not is_fullscreen)
        return "break"

if __name__ == "__main__":
    root=Tk()
    obj=Face_Recognition(root)
    root.mainloop()