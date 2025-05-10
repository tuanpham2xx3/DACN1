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
        self.root.title("Nhận Diện Khuôn Mặt")
        
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

        # Thêm nút thoát góc phải trên (nằm trên banner)
        exit_btn = Button(self.root, text="×", command=self.exit_window, 
                          font=("Arial", 16, "bold"), 
                          fg="white", bg="#E81123", 
                          cursor="hand2", 
                          bd=0,                     # Không có viền
                          relief=FLAT,              # Kiểu nút phẳng
                          width=3, height=1)
        exit_btn.place(x=screen_width-50, y=10, width=40, height=40)

        # backgorund image 
        bg1=Image.open(r".\Images_GUI\bg2.jpg")
        bg1=bg1.resize((screen_width,screen_height),Image.LANCZOS)
        self.photobg1=ImageTk.PhotoImage(bg1)

        # set image as lable
        bg_img = Label(self.root,image=self.photobg1)
        bg_img.place(x=0,y=130,width=screen_width,height=screen_height-130)


        #title section
        title_lb1 = Label(bg_img,text="Chào mừng đến với hệ thống Nhận Diện Khuôn Mặt",font=("Times New Roman",30,"bold"),bg="white",fg="#00008B")
        title_lb1.place(x=0,y=0,width=screen_width,height=50)

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

        std_b1_1 = Button(bg_img,command=self.face_recog,text="Nhận Diện Khuôn Mặt",cursor="hand2",font=("Times New Roman",13,"bold"),bg="white",fg="#00008B")
        std_b1_1.place(x=btn_x,y=350,width=button_width,height=50)
        
        # Thêm hướng dẫn thoát fullscreen
        exit_label = Label(bg_img, text="Nhấn 'Esc' để bật/tắt chế độ toàn màn hình", font=("verdana", 10), bg="white", fg="gray")
        exit_label.place(x=screen_width-350, y=screen_height-180, width=330, height=20)
    #=====================Attendance===================

    def mark_attendance(self,i,r,n):
        try:
            with open("attendance.csv","r+",newline="\n") as f:
                myDatalist = f.readlines()
                name_list = []
                id_list = []
                roll_list = []
                
                # Lấy danh sách ID, Roll và Name đã có
                for line in myDatalist:
                    entry = line.split(",")
                    if len(entry) >= 3:
                        id_list.append(entry[0].strip())
                        roll_list.append(entry[1].strip())
                        name_list.append(entry[2].strip())

                # Kiểm tra nếu ID hoặc Roll hoặc Name chưa có trong danh sách
                if((i.strip() not in id_list)) and ((r.strip() not in roll_list)) and ((n.strip() not in name_list)):
                    now = datetime.now()
                    d1 = now.strftime("%d/%m/%Y")
                    dtString = now.strftime("%H:%M:%S")
                    
                    # Thêm bản ghi mới vào CSV - KHÔNG lưu buổi
                    f.writelines(f"\n{i}, {r}, {n}, {dtString}, {d1}, Co mat")
                    print(f"[INFO] Đã ghi điểm danh vào file CSV: ID={i}, Name={n}")

                    # Ghi log kết quả điểm danh
                    print(f"[SUCCESS] Điểm danh thành công cho: {n} (ID: {i})")
                    
                    # Xác định buổi từ thời gian - CHỈ để lưu vào MySQL
                    hour = int(dtString.split(":")[0])
                    if 7 <= hour < 12:
                        session = "Sang"
                    elif 13 <= hour < 17:
                        session = "Chieu"
                    else:
                        session = "Khac"
                    
                    # Cố gắng lưu vào MySQL (không bắt buộc)
                    try:
                        conn = mysql.connector.connect(username='root', password='12345', host='localhost', database='face_recognition', port=3307)
                        mycursor = conn.cursor()
                        # Kiểm tra xem bản ghi đã tồn tại chưa
                        mycursor.execute("SELECT * FROM stdattendance WHERE std_id=%s AND std_date=%s AND std_session=%s", (i, d1, session))
                        result = mycursor.fetchone()
                        if result is None:  # Nếu chưa có bản ghi nào trong ngày hôm nay với buổi này
                            # Thêm bản ghi mới vào database
                            mycursor.execute("INSERT INTO stdattendance (std_id, std_roll_no, std_name, std_time, std_date, std_session, std_attendance) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                                            (i, r, n, dtString, d1, session, "Co mat"))
                            conn.commit()
                            print(f"[INFO] Đã lưu điểm danh vào MySQL: ID={i}, Name={n}, Buổi={session}")
                        conn.close()
                    except Exception as db_err:
                        print(f"[WARNING] Không thể lưu vào MySQL (không ảnh hưởng đến điểm danh): {str(db_err)}")
                else:
                    print(f"[INFO] {n} (ID: {i}) đã được điểm danh trước đó.")
        except Exception as e:
            print(f"[ERROR] Lỗi khi ghi điểm danh: {str(e)}")

    #================face recognition==================
    def face_recog(self):
        # Clear attendance.csv file - tạo mới với header 6 cột (không có buổi)
        try:
            # Tạo file mới với header chuẩn 6 cột
            with open("attendance.csv", "w", newline="") as f:
                # Header với 6 cột (không bao gồm buổi)
                f.write("ID,Roll_No,Name,Time,Date,Attend\n")
            
            print("[INFO] Đã tạo mới file attendance.csv với header 6 cột")
            messagebox.showinfo("Reset Attendance", "Đã xóa dữ liệu điểm danh cũ để bắt đầu phiên mới", parent=self.root)
        except Exception as csv_err:
            print(f"[ERROR] Không thể reset file attendance.csv: {str(csv_err)}")
            messagebox.showwarning("Warning", "Không thể xóa dữ liệu điểm danh cũ", parent=self.root)

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
                        cv2.putText(img, f"MSSV: {r}", (x+5, y-45), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                        cv2.putText(img, f"Tên: {n}", (x+5, y-25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                        cv2.putText(img, f"Độ tin cậy: {confidence}%", (x+5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                        
                        self.mark_attendance(i, r, n)
                    else:
                        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
                        cv2.rectangle(img, (x, y-25), (x+w, y), (0, 0, 255), -1)
                        cv2.putText(img, "Không xác định", (x+5, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                    
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
            messagebox.showerror("Lỗi", "Không tìm thấy file clf.xml! Vui lòng huấn luyện mô hình trước.", parent=self.root)
            return
        
        if not os.path.exists("haarcascade_frontalface_default.xml"):
            messagebox.showerror("Lỗi", "Không tìm thấy file phát hiện khuôn mặt!", parent=self.root)
            return
        
        try:
            # Tạo bảng stdattendance nếu chưa tồn tại
            try:
                conn = mysql.connector.connect(username='root', password='12345', host='localhost', database='face_recognition', port=3307)
                mycursor = conn.cursor()
                mycursor.execute("""
                    CREATE TABLE IF NOT EXISTS stdattendance (
                        std_id VARCHAR(20) NOT NULL,
                        std_roll_no VARCHAR(20) NOT NULL,
                        std_name VARCHAR(50) NOT NULL,
                        std_time VARCHAR(50) NOT NULL,
                        std_date VARCHAR(50) NOT NULL,
                        std_session VARCHAR(10) NOT NULL,
                        std_attendance VARCHAR(10) NOT NULL,
                        PRIMARY KEY (std_id, std_date, std_session)
                    )
                """)
                conn.commit()
                conn.close()
                print("[INFO] Đã kiểm tra/tạo bảng stdattendance")
            except Exception as table_err:
                print(f"[ERROR] Không thể tạo bảng: {str(table_err)}")
            
            # Tải classifier
            clf = cv2.face.LBPHFaceRecognizer_create()
            clf.read("clf.xml")
            
            # Tải bộ phát hiện khuôn mặt
            faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
            
            # Kiểm tra camera
            videoCap = cv2.VideoCapture(0)
            if not videoCap.isOpened():
                messagebox.showerror("Lỗi", "Không thể truy cập camera! Vui lòng kiểm tra kết nối camera của bạn.", parent=self.root)
                return
            
            # Hiển thị thông báo và hướng dẫn
            messagebox.showinfo("Bắt đầu", "Đã bắt đầu nhận diện khuôn mặt.\nNhấn 'f' để bật/tắt chế độ toàn màn hình.\nNhấn 'q' hoặc Enter để thoát.", parent=self.root)
            
            # Trạng thái fullscreen
            is_fullscreen = True  # Mặc định bắt đầu với fullscreen
            
            # Thiết lập cửa sổ mặc định với chế độ fullscreen
            cv2.namedWindow("Nhận Diện Khuôn Mặt", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Nhận Diện Khuôn Mặt", 1280, 720)
            cv2.setWindowProperty("Nhận Diện Khuôn Mặt", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            
            # Bắt đầu vòng lặp camera
            while True:
                ret, img = videoCap.read()
                if not ret:
                    messagebox.showerror("Lỗi", "Không thể lấy khung hình từ camera!", parent=self.root)
                    break
                
                # Xử lý nhận diện
                img = recognize(img, clf, faceCascade)
                
                # Hiển thị thời gian thực
                now = datetime.now()
                dt_string = now.strftime("%H:%M:%S")
                cv2.putText(img, f"Thời gian: {dt_string}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                
                # Hiển thị hướng dẫn rõ ràng hơn
                cv2.putText(img, "Nhấn 'f': Toàn màn hình | 'q' hoặc Enter: Thoát", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                # Hiển thị ảnh
                cv2.imshow("Nhận Diện Khuôn Mặt", img)
                
                # Xử lý phím nhấn
                key = cv2.waitKey(1)
                if key == 13 or key == ord('q'):  # Enter key hoặc q
                    break
                elif key == ord('f') or key == ord('F'):  # 'f' key để toggle fullscreen
                    is_fullscreen = not is_fullscreen
                    if is_fullscreen:
                        cv2.setWindowProperty("Nhận Diện Khuôn Mặt", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                        print("[INFO] Fullscreen mode ON")
                    else:
                        cv2.setWindowProperty("Nhận Diện Khuôn Mặt", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
                        cv2.resizeWindow("Nhận Diện Khuôn Mặt", 1280, 720)  # Kích thước chuẩn khi thoát fullscreen
                        print("[INFO] Fullscreen mode OFF")
            
            # Giải phóng tài nguyên
            videoCap.release()
            cv2.destroyAllWindows()
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi trong quá trình nhận diện khuôn mặt: {str(e)}", parent=self.root)
            # Đảm bảo giải phóng tài nguyên ngay cả khi có lỗi
            if 'videoCap' in locals() and videoCap.isOpened():
                videoCap.release()
            cv2.destroyAllWindows()

    def toggle_fullscreen(self, event=None):
        """Chuyển đổi giữa chế độ fullscreen và không fullscreen"""
        is_fullscreen = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not is_fullscreen)
        return "break"

    # Exit current window and return to main menu
    def exit_window(self):
        self.root.destroy()

if __name__ == "__main__":
    root=Tk()
    obj=Face_Recognition(root)
    root.mainloop()