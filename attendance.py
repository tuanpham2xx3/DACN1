# import re
import re
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
import csv
from tkinter import filedialog

#Global variable for importCsv Function 
mydata=[]
class Attendance:
    
    def __init__(self,root):
        self.root=root
        # Thiết lập toàn màn hình
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.title("Attendance Panel")
        
        # Thêm phím tắt để thoát khỏi chế độ fullscreen (Esc)
        self.root.bind("<Escape>", self.toggle_fullscreen)
        # Thiết lập fullscreen
        self.root.attributes('-fullscreen', True)
        
        # Tạo style cho các thành phần
        self.create_styles()

        #-----------Variables-------------------
        self.var_id=StringVar()
        self.var_roll=StringVar()
        self.var_name=StringVar()
        self.var_dep=StringVar()
        self.var_time=StringVar()
        self.var_date=StringVar()
        self.var_attend=StringVar()

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
        bg1=Image.open(r"Images_GUI\bg2.jpg")
        bg1=bg1.resize((screen_width,screen_height),Image.LANCZOS)
        self.photobg1=ImageTk.PhotoImage(bg1)

        # set image as lable
        bg_img = Label(self.root,image=self.photobg1)
        bg_img.place(x=0,y=130,width=screen_width,height=screen_height-130)


        #title section
        title_lb1 = Label(bg_img,text="Quản Lý Điểm Danh",font=("Times New Roman",30,"bold"),bg="white",fg="#00008B")
        title_lb1.place(x=0,y=0,width=screen_width,height=50)

        #========================Section Creating==================================

        # Creating Frame 
        main_frame = Frame(bg_img,bd=2,bg="white") #bd mean border 
        main_width = screen_width - 10
        main_height = screen_height - 250 
        main_frame.place(x=5,y=55,width=main_width,height=main_height)

        # Left Label Frame 
        left_frame = LabelFrame(main_frame,bd=2,bg="white",relief=RIDGE,text="Nhập/Xuất CSV",font=("verdana",12,"bold"),fg="navyblue")
        left_frame_width = (main_width // 2) - 15
        left_frame.place(x=10,y=10,width=left_frame_width,height=main_height-20)

        # Thêm nhãn cho bảng CSV
        csv_label = Label(left_frame, text="Dữ liệu từ tệp CSV", font=("verdana", 10, "bold"), bg="honeydew", fg="green", relief=RIDGE, bd=1)
        csv_label.place(x=10, y=70, width=200, height=24)

        # ==================================Text boxes and Combo Boxes====================

        # Tạo frame riêng cho phần nhập liệu
        entry_frame = Frame(left_frame, bg="alice blue", bd=2, relief=RIDGE)
        entry_frame.place(x=10, y=5, width=left_frame_width-20, height=90)  # Tăng chiều cao để chứa 2 hàng

        #Student id - Hàng 1
        studentId_label = Label(entry_frame,text="Mã SV:",font=("verdana",10,"bold"),fg="navy",bg="alice blue")
        studentId_label.grid(row=0,column=0,padx=5,pady=5,sticky=W)

        studentId_entry = ttk.Entry(entry_frame,textvariable=self.var_id,width=15,font=("verdana",10))
        studentId_entry.grid(row=0,column=1,padx=5,pady=5,sticky=W)

        #Student Roll - Hàng 1
        student_roll_label = Label(entry_frame,text="Mã số:",font=("verdana",10,"bold"),fg="navy",bg="alice blue")
        student_roll_label.grid(row=0,column=2,padx=5,pady=5,sticky=W)

        student_roll_entry = ttk.Entry(entry_frame,textvariable=self.var_roll,width=15,font=("verdana",10))
        student_roll_entry.grid(row=0,column=3,padx=5,pady=5,sticky=W)

        #Studnet Name - Hàng 1
        student_name_label = Label(entry_frame,text="Họ tên:",font=("verdana",10,"bold"),fg="navy",bg="alice blue")
        student_name_label.grid(row=0,column=4,padx=5,pady=5,sticky=W)

        student_name_entry = ttk.Entry(entry_frame,textvariable=self.var_name,width=15,font=("verdana",10))
        student_name_entry.grid(row=0,column=5,padx=5,pady=5,sticky=W)

        #time - Hàng 2
        time_label = Label(entry_frame,text="Giờ:",font=("verdana",10,"bold"),fg="navy",bg="alice blue")
        time_label.grid(row=1,column=0,padx=5,pady=5,sticky=W)

        time_entry = ttk.Entry(entry_frame,textvariable=self.var_time,width=15,font=("verdana",10))
        time_entry.grid(row=1,column=1,padx=5,pady=5,sticky=W)

        #Date - Hàng 2
        date_label = Label(entry_frame,text="Ngày:",font=("verdana",10,"bold"),fg="navy",bg="alice blue")
        date_label.grid(row=1,column=2,padx=5,pady=5,sticky=W)

        date_entry = ttk.Entry(entry_frame,textvariable=self.var_date,width=15,font=("verdana",10))
        date_entry.grid(row=1,column=3,padx=5,pady=5,sticky=W)

        #Attendance - Hàng 2
        student_attend_label = Label(entry_frame,text="Trạng thái:",font=("verdana",10,"bold"),fg="navy",bg="alice blue")
        student_attend_label.grid(row=1,column=4,padx=5,pady=5,sticky=W)

        attend_combo=ttk.Combobox(entry_frame,textvariable=self.var_attend,width=13,font=("verdana",10),state="readonly")
        attend_combo["values"]=("Chọn","Co mat","Vang mat")
        attend_combo.current(0)
        attend_combo.grid(row=1,column=5,padx=5,pady=5,sticky=W)

        # ===============================Table Sql Data View==========================
        table_frame = Frame(left_frame,bd=2,bg="white",relief=RIDGE)
        table_frame_height = main_height - 180  # Để lại khoảng trống cho các nút và trường nhập liệu
        table_frame.place(x=10,y=100,width=left_frame_width-20,height=table_frame_height)

        #scroll bar 
        scroll_x = ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame,orient=VERTICAL)

        #create table 
        self.attendanceReport_left = ttk.Treeview(table_frame,column=("ID","Roll_No","Name","Time","Date","Session","Attend"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.attendanceReport_left.xview)
        scroll_y.config(command=self.attendanceReport_left.yview)

        self.attendanceReport_left.heading("ID",text="Mã SV")
        self.attendanceReport_left.heading("Roll_No",text="Mã số")
        self.attendanceReport_left.heading("Name",text="Họ tên")
        self.attendanceReport_left.heading("Time",text="Giờ")
        self.attendanceReport_left.heading("Date",text="Ngày")
        self.attendanceReport_left.heading("Session",text="Buổi")
        self.attendanceReport_left.heading("Attend",text="Trạng thái")
        self.attendanceReport_left["show"]="headings"


        # Set Width of Colums 
        self.attendanceReport_left.column("ID",width=80)
        self.attendanceReport_left.column("Roll_No",width=80)
        self.attendanceReport_left.column("Name",width=100)
        self.attendanceReport_left.column("Time",width=80)
        self.attendanceReport_left.column("Date",width=80)
        self.attendanceReport_left.column("Session",width=80)
        self.attendanceReport_left.column("Attend",width=80)
        
        self.attendanceReport_left.pack(fill=BOTH,expand=1)
        self.attendanceReport_left.bind("<ButtonRelease>",self.get_cursor_left)
    

        # =========================button section========================

        #Button Frame
        btn_frame = Frame(left_frame,bd=2,bg="white",relief=RIDGE)
        btn_frame.place(x=10,y=main_height-80,width=left_frame_width-20,height=60)

        #Import button
        save_btn=Button(btn_frame,command=self.importCsv,text="Nhập CSV",width=12,font=("verdana",10,"bold"),fg="white",bg="navy",cursor="hand2", relief=RAISED)
        save_btn.grid(row=0,column=0,padx=6,pady=10,sticky=W)

        #Exprot button
        update_btn=Button(btn_frame,command=self.exportCsv,text="Xuất CSV",width=12,font=("verdana",10,"bold"),fg="white",bg="navy",cursor="hand2", relief=RAISED)
        update_btn.grid(row=0,column=1,padx=6,pady=8,sticky=W)

        #Update button
        del_btn=Button(btn_frame,command=self.action,text="Cập nhật MySQL",width=15,font=("verdana",10,"bold"),fg="white",bg="navy",cursor="hand2", relief=RAISED)
        del_btn.grid(row=0,column=2,padx=6,pady=10,sticky=W)

        #Delete button
        delete_btn=Button(btn_frame,command=self.delete_csv,text="Xóa",width=12,font=("verdana",10,"bold"),fg="white",bg="maroon",cursor="hand2", relief=RAISED)
        delete_btn.grid(row=0,column=3,padx=6,pady=10,sticky=W)

        # Reset button
        reset_btn = Button(btn_frame, command=self.reset_attendance_csv, text="Reset", width=12, 
                          font=("verdana",10,"bold"), fg="white", bg="red", cursor="hand2", relief=RAISED)
        reset_btn.grid(row=0, column=4, padx=6, pady=10, sticky=W)



        # Right section=======================================================

        # Right Label Frame 
        right_frame = LabelFrame(main_frame,bd=2,bg="white",relief=RIDGE,text="Dữ liệu điểm danh từ MySQL",font=("verdana",12,"bold"),fg="navyblue")
        right_frame_width = (main_width // 2) - 15
        right_frame.place(x=left_frame_width+20,y=10,width=right_frame_width,height=main_height-20)

        # Thêm nhãn cho bảng MySQL - dịch và chỉnh vị trí
        mysql_label = Label(right_frame, text="Dữ liệu từ cơ sở dữ liệu MySQL", font=("verdana", 10, "bold"), bg="lavender", fg="navy", relief=RIDGE, bd=1)
        mysql_label.place(x=10, y=135, width=250, height=24)

        # Thêm frame lọc dữ liệu - chỉnh lại design cho đẹp
        filter_frame = Frame(right_frame, bg="alice blue", bd=2, relief=RIDGE)
        filter_frame.place(x=10, y=30, width=right_frame_width-20, height=60)

        # Biến để lưu trữ lựa chọn
        self.var_filter_date = StringVar()
        self.var_filter_session = StringVar()

        # Nhãn và trường lọc theo ngày - dịch sang tiếng Việt
        date_filter_label = Label(filter_frame, text="Ngày:", font=("verdana", 10, "bold"), bg="alice blue", fg="navy")
        date_filter_label.grid(row=0, column=0, padx=5, pady=15, sticky=W)

        # Dùng DateEntry nếu có thể, hoặc Entry thông thường
        date_filter_entry = ttk.Entry(filter_frame, textvariable=self.var_filter_date, width=15, font=("verdana", 10))
        date_filter_entry.grid(row=0, column=1, padx=5, pady=15, sticky=W)
        date_filter_entry.insert(0, datetime.now().strftime("%d/%m/%Y")) # Đặt ngày hiện tại làm mặc định

        # Lọc theo buổi - điều chỉnh padx, pady để cân đối
        session_filter_label = Label(filter_frame, text="Buổi:", font=("verdana", 10, "bold"), bg="alice blue", fg="navy")
        session_filter_label.grid(row=0, column=2, padx=15, pady=15, sticky=W)

        session_combo = ttk.Combobox(filter_frame, textvariable=self.var_filter_session, width=18, font=("verdana", 10), state="readonly")
        session_combo["values"] = ("Tất cả", "Sáng (7:30-11:30)", "Chiều (13:00-17:00)")
        session_combo.current(0)  # Mặc định là "Tất cả"
        session_combo.grid(row=0, column=3, padx=5, pady=15, sticky=W)

        # Nút lọc dữ liệu - làm đẹp nút, thêm relief
        filter_btn = Button(filter_frame, command=self.filter_data, text="Lọc", width=10, font=("verdana", 10, "bold"), 
                           fg="white", bg="navy", cursor="hand2", relief=RAISED)
        filter_btn.grid(row=0, column=4, padx=15, pady=15, sticky=W)

        # Nút clear lọc
        clear_filter_btn = Button(filter_frame, command=self.clear_filter, text="Xóa lọc", width=10, font=("verdana", 10, "bold"), 
                                 fg="white", bg="maroon", cursor="hand2", relief=RAISED)
        clear_filter_btn.grid(row=0, column=5, padx=5, pady=15, sticky=W)

        # Thêm các nút vào right_frame ở đây - dịch tên nút và chỉnh lại vị trí
        #Refresh button
        refresh_btn=Button(right_frame,command=self.fetch_data,text="Làm mới",width=10,font=("verdana",10,"bold"),fg="white",
                          bg="green",cursor="hand2", relief=RAISED)
        refresh_btn.place(x=10, y=100, width=100, height=30)
        #Update button
        update_btn=Button(right_frame,command=self.update_data,text="Cập nhật",width=10,font=("verdana",10,"bold"),fg="white",
                         bg="navy",cursor="hand2", relief=RAISED)
        update_btn.place(x=120, y=100, width=100, height=30)
        #Delete button
        delete_btn=Button(right_frame,command=self.delete_data,text="Xóa",width=10,font=("verdana",10,"bold"),fg="white",
                         bg="maroon",cursor="hand2", relief=RAISED)
        delete_btn.place(x=230, y=100, width=100, height=30)

        # Điều chỉnh vị trí của table_frame
        table_frame = Frame(right_frame,bd=2,bg="white",relief=RIDGE)
        table_frame.place(x=10,y=165,width=right_frame_width-20,height=main_height-205)

        #scroll bar 
        scroll_x = ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame,orient=VERTICAL)

        #create table 
        self.attendanceReport = ttk.Treeview(table_frame,column=("ID","Roll_No","Name","Time","Date","Session","Attend"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.attendanceReport.xview)
        scroll_y.config(command=self.attendanceReport.yview)

        # Điều chỉnh tên các cột trong bảng sang tiếng Việt
        self.attendanceReport.heading("ID",text="Mã SV")
        self.attendanceReport.heading("Roll_No",text="Mã số")
        self.attendanceReport.heading("Name",text="Họ tên")
        self.attendanceReport.heading("Time",text="Giờ")
        self.attendanceReport.heading("Date",text="Ngày")
        self.attendanceReport.heading("Session",text="Buổi")
        self.attendanceReport.heading("Attend",text="Trạng thái")
        self.attendanceReport["show"]="headings"


        # Set Width of Colums 
        self.attendanceReport.column("ID",width=80)
        self.attendanceReport.column("Roll_No",width=80)
        self.attendanceReport.column("Name",width=100)
        self.attendanceReport.column("Time",width=80)
        self.attendanceReport.column("Date",width=80)
        self.attendanceReport.column("Session",width=80)
        self.attendanceReport.column("Attend",width=80)
        
        self.attendanceReport.pack(fill=BOTH,expand=1)
        self.attendanceReport.bind("<ButtonRelease>",self.get_cursor_right)
        
        # Tự động load dữ liệu từ attendance.csv vào bảng bên trái
        self.load_attendance_csv()
        
        # Load dữ liệu từ MySQL vào bảng bên phải
        self.fetch_data()
    # ===============================update function for mysql database=================
    def update_data(self):
        if self.var_id.get()=="" or self.var_roll.get=="" or self.var_name.get()=="" or self.var_time.get()=="" or self.var_date.get()=="" or self.var_attend.get()=="Chọn":
            messagebox.showerror("Lỗi","Vui lòng điền đầy đủ các trường thông tin!",parent=self.root)
        else:
            try:
                Update=messagebox.askyesno("Cập nhật","Bạn có muốn cập nhật thông tin điểm danh này?",parent=self.root)
                if Update > 0:
                    # Xác định buổi từ thời gian
                    session = self.get_session_from_time(self.var_time.get())
                    
                    conn = mysql.connector.connect(username='root', password='12345',host='localhost',database='face_recognition',port=3307)
                    mycursor = conn.cursor()
                    
                    # Kiểm tra xem đã có bản ghi với cùng ID, ngày và buổi chưa
                    mycursor.execute("SELECT * FROM stdattendance WHERE std_id=%s AND std_date=%s AND std_session=%s", 
                                    (self.var_id.get(), self.var_date.get(), session))
                    existing = mycursor.fetchone()
                    
                    if existing:
                        # Nếu đã tồn tại, thực hiện cập nhật
                        mycursor.execute("""
                            UPDATE stdattendance 
                            SET std_roll_no=%s, std_name=%s, std_time=%s, std_attendance=%s 
                            WHERE std_id=%s AND std_date=%s AND std_session=%s
                        """, (
                            self.var_roll.get(),
                            self.var_name.get(),
                            self.var_time.get(),
                            self.var_attend.get(),
                            self.var_id.get(),
                            self.var_date.get(),
                            session
                        ))
                    else:
                        # Nếu chưa tồn tại, thêm mới
                        mycursor.execute("""
                            INSERT INTO stdattendance 
                            (std_id, std_roll_no, std_name, std_time, std_date, std_session, std_attendance)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """, (
                    self.var_id.get(),
                    self.var_roll.get(),
                    self.var_name.get(),
                    self.var_time.get(),
                    self.var_date.get(),
                            session,
                            self.var_attend.get()
                    ))
                    
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Thành công","Đã cập nhật thông tin điểm danh!",parent=self.root)
                
            except Exception as es:
                messagebox.showerror("Lỗi",f"Lỗi: {str(es)}",parent=self.root)
    # =============================Delete Attendance form my sql============================
    def delete_data(self):
        if self.var_id.get()=="":
            messagebox.showerror("Lỗi","Vui lòng chọn bản ghi cần xóa!",parent=self.root)
        else:
            try:
                delete=messagebox.askyesno("Xóa","Bạn có chắc muốn xóa bản ghi này?",parent=self.root)
                if delete>0:
                    # Xác định buổi từ thời gian
                    session = self.get_session_from_time(self.var_time.get())
                    
                    conn = mysql.connector.connect(username='root', password='12345',host='localhost',database='face_recognition',port=3307)
                    mycursor = conn.cursor() 
                    
                    # Xóa bản ghi với ID, ngày và buổi xác định
                    sql="DELETE FROM stdattendance WHERE std_id=%s AND std_date=%s AND std_session=%s"
                    val=(self.var_id.get(), self.var_date.get(), session)
                    mycursor.execute(sql, val)

                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Xóa","Đã xóa bản ghi thành công!",parent=self.root)
                
            except Exception as es:
                messagebox.showerror("Lỗi",f"Lỗi: {str(es)}",parent=self.root)
    # ===========================fatch data form mysql attendance===========

    def fetch_data(self):
        # Xóa dữ liệu hiện tại trong bảng
        self.attendanceReport.delete(*self.attendanceReport.get_children())
        
        # Chỉ đọc từ MySQL
        try:
            conn = mysql.connector.connect(username='root', password='12345',host='localhost',database='face_recognition',port=3307)
            mycursor = conn.cursor()

            mycursor.execute("select * from stdattendance")
            data = mycursor.fetchall()

            if len(data) != 0:
                for i in data:
                    self.attendanceReport.insert("", END, values=i)
            
            conn.commit()
            conn.close()
            print("[INFO] Đã đọc dữ liệu từ MySQL")
        except Exception as e:
            print(f"[WARNING] MySQL fetch error: {str(e)}")
            messagebox.showerror("Database Error", f"Không thể kết nối với MySQL: {str(e)}", parent=self.root)

    #============================Reset Data======================
    def reset_data(self):
        self.var_id.set("")
        self.var_roll.set("")
        self.var_name.set("")
        self.var_time.set("")
        self.var_date.set("")
        self.var_attend.set("Status")

    # =========================Fetch Data Import data ===============

    def fetchData(self,rows):
        global mydata
        mydata = rows
        self.attendanceReport_left.delete(*self.attendanceReport_left.get_children())
        for i in rows:
            if len(i) > 0:  # Chỉ thêm dòng không trống
                self.attendanceReport_left.insert("",END,values=i)

    # Thêm hàm để đọc tự động file attendance.csv
    def load_attendance_csv(self):
        try:
            # Xóa dữ liệu cũ trong bảng trước khi tải mới
            self.attendanceReport_left.delete(*self.attendanceReport_left.get_children())
            
            # Xóa dữ liệu trong biến mydata
            global mydata
            mydata.clear()
            
            # Đọc file attendance.csv
            with open("attendance.csv") as f:
                csvread = csv.reader(f, delimiter=",")
                # Bỏ qua dòng đầu tiên (header)
                next(csvread)
                
                # Đọc và hiển thị các dòng còn lại
                for i in csvread:
                    if len(i) >= 6:  # Đảm bảo không đọc dòng trống và đủ 6 cột
                        # Xác định buổi từ thời gian trong dữ liệu
                        time_str = i[3].strip()
                        session = self.get_session_from_time(time_str)
                        
                        # Tạo giá trị hiển thị với 7 cột (thêm cột session)
                        row_values = [i[0].strip(), i[1].strip(), i[2].strip(), i[3].strip(), i[4].strip(), session, i[5].strip()]
                        mydata.append(row_values)
                        self.attendanceReport_left.insert("", END, values=row_values)
            
            print("[INFO] Đã tự động tải dữ liệu từ file attendance.csv")
        except Exception as e:
            print(f"[ERROR] Không thể tải file attendance.csv: {str(e)}")

    # Cập nhật phương thức importCsv để hỗ trợ định dạng mới
    def importCsv(self):
        try:
            global mydata
            mydata.clear()
            fln=filedialog.askopenfilename(initialdir=os.getcwd(),title="Open CSV",filetypes=(("CSV File","*.csv"),("All File","*.*")),parent=self.root)
            with open(fln) as myfile:
                csvread=csv.reader(myfile,delimiter=",")
                
                # Bỏ qua header
                header = next(csvread)
                
                # Kiểm tra số cột trong header
                has_session_column = len(header) >= 7
                
                for i in csvread:
                    if len(i) > 0:  # Đảm bảo không đọc dòng trống
                        # Nếu file không có cột session, thêm session dựa vào giờ
                        if not has_session_column and len(i) >= 6:
                            session = self.get_session_from_time(i[3])
                            # Tạo bản ghi với 7 cột
                            row = [i[0], i[1], i[2], i[3], i[4], session, i[5]]
                            mydata.append(row)
                        elif has_session_column and len(i) >= 7:
                            # File đã có cột session
                            mydata.append(i)
                        else:
                            # Trường hợp khác - bản ghi không đủ dữ liệu
                            print(f"[WARNING] Bỏ qua bản ghi không hợp lệ: {i}")
                            
            self.fetchData(mydata)
        except Exception as es:
            messagebox.showerror("Lỗi",f"Lỗi khi nhập file: {str(es)}",parent=self.root)

    #==================Experot CSV=============
    def exportCsv(self):
        try:
            # Nếu mydata trống, hiển thị thông báo
            if len(mydata) < 1:
                messagebox.showerror("Không có dữ liệu","Không có dữ liệu để xuất file",parent=self.root)
                return False

            # Mở file CSV để ghi
            with open("attendance_export.csv", "w", newline="") as myfile:
                exp_write = csv.writer(myfile, delimiter=",")
                
                # Ghi tiêu đề cột (header) với cột session mới
                exp_write.writerow(["ID", "Roll_No", "Name", "Time", "Date", "Session", "Attend"])
                
                # Ghi dữ liệu từ mydata
                for x in mydata:
                    exp_write.writerow(x)
                    
                messagebox.showinfo("Xuất dữ liệu", "Dữ liệu của bạn đã được xuất vào file attendance_export.csv", parent=self.root)
        except Exception as es:
            messagebox.showerror("Lỗi",f"Lỗi khi xuất dữ liệu: {str(es)}",parent=self.root)

    #=============Cursur Function for CSV========================

    def get_cursor_left(self,event=""):
        cursor_focus = self.attendanceReport_left.focus()
        content = self.attendanceReport_left.item(cursor_focus)
        data = content["values"]

        if data:
            self.var_id.set(data[0])
            self.var_roll.set(data[1])
            self.var_name.set(data[2])
            self.var_time.set(data[3])
            self.var_date.set(data[4])
            # data[5] là cột buổi (session) mới thêm, không cần đặt vào biến
            self.var_attend.set(data[6])

     #=============Cursur Function for mysql========================

    def get_cursor_right(self,event=""):
        cursor_focus = self.attendanceReport.focus()
        content = self.attendanceReport.item(cursor_focus)
        data = content["values"]

        if data:
            self.var_id.set(data[0])
            self.var_roll.set(data[1])
            self.var_name.set(data[2])
            self.var_time.set(data[3])
            self.var_date.set(data[4])
            # data[5] là session
            self.var_attend.set(data[6])

    #=========================================Update CSV============================

    # export update
    def action(self):
        # Hỏi người dùng muốn cập nhật một bản ghi hay tất cả
        update_choice = messagebox.askyesno("Tùy chọn cập nhật", "Bạn muốn cập nhật TẤT CẢ dữ liệu từ CSV vào MySQL?\nChọn 'Yes' để cập nhật tất cả\nChọn 'No' để chỉ cập nhật bản ghi đang chọn", parent=self.root)
        
        try:
            conn = mysql.connector.connect(username='root', password='12345', host='localhost', database='face_recognition', port=3307)
            mycursor = conn.cursor()
            
            success_count = 0
            error_count = 0
            
            if update_choice:
                # Cập nhật tất cả
                for row in mydata:
                    if len(row) >= 7:  # Đảm bảo có đủ 7 cột với session
                        # Làm sạch dữ liệu
                        clean_row = [item.strip() if isinstance(item, str) else item for item in row]
                        
                        # Lấy trực tiếp session từ dữ liệu (vị trí 5)
                        session = clean_row[5]
                        
                        try:
                            # Kiểm tra xem bản ghi đã tồn tại chưa
                            mycursor.execute("SELECT * FROM stdattendance WHERE std_id=%s AND std_date=%s AND std_session=%s", 
                                            (clean_row[0], clean_row[4], session))
                            existing = mycursor.fetchone()
                            
                            if existing:
                                # Nếu đã tồn tại với cùng ID, ngày và buổi - cập nhật
                                mycursor.execute("""
                                    UPDATE stdattendance 
                                    SET std_roll_no=%s, std_name=%s, std_time=%s, std_attendance=%s 
                                    WHERE std_id=%s AND std_date=%s AND std_session=%s
                                """, (clean_row[1], clean_row[2], clean_row[3], clean_row[6], clean_row[0], clean_row[4], session))
                            else:
                                # Nếu chưa tồn tại - thêm mới
                                mycursor.execute("""
                                    INSERT INTO stdattendance 
                                    (std_id, std_roll_no, std_name, std_time, std_date, std_session, std_attendance)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                                """, (clean_row[0], clean_row[1], clean_row[2], clean_row[3], clean_row[4], session, clean_row[6]))
                            
                            success_count += 1
                        except Exception as e:
                            print(f"Lỗi khi cập nhật bản ghi {clean_row[0]}: {str(e)}")
                            error_count += 1
                    else:
                        print(f"[WARNING] Bỏ qua bản ghi không hợp lệ: {row}")
                        error_count += 1
            else:
                # Cập nhật chỉ bản ghi hiện tại
                # Kiểm tra xem đã chọn dữ liệu chưa
                if self.var_id.get() == "" or self.var_roll.get() == "" or self.var_name.get() == "" or self.var_time.get() == "" or self.var_date.get() == "":
                    messagebox.showerror("Lỗi", "Vui lòng chọn bản ghi cần cập nhật!", parent=self.root)
                    return
                
                # Xác định buổi từ thời gian
                session = self.get_session_from_time(self.var_time.get())
                
                # Kiểm tra bản ghi đã tồn tại chưa
                mycursor.execute("SELECT * FROM stdattendance WHERE std_id=%s AND std_date=%s AND std_session=%s", 
                                (self.var_id.get(), self.var_date.get(), session))
                existing = mycursor.fetchone()
                
                if existing:
                    # Cập nhật bản ghi
                    mycursor.execute("""
                        UPDATE stdattendance 
                        SET std_roll_no=%s, std_name=%s, std_time=%s, std_attendance=%s 
                        WHERE std_id=%s AND std_date=%s AND std_session=%s
                    """, (
                        self.var_roll.get(), 
                        self.var_name.get(), 
                        self.var_time.get(),
                        self.var_attend.get(),
                        self.var_id.get(),
                        self.var_date.get(),
                        session
                    ))
                else:
                    # Thêm mới
                    mycursor.execute("""
                        INSERT INTO stdattendance 
                        (std_id, std_roll_no, std_name, std_time, std_date, std_session, std_attendance)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (
                self.var_id.get(),
                self.var_roll.get(),
                self.var_name.get(),
                self.var_time.get(),
                self.var_date.get(),
                        session,
                self.var_attend.get()
                ))
                
                success_count = 1

            conn.commit()
            conn.close()
            
            # Cập nhật bảng bên phải
            self.fetch_data()
            
            messagebox.showinfo("Kết quả", f"Đã cập nhật {success_count} bản ghi thành công!\n{error_count} bản ghi có lỗi.", parent=self.root)
        
        except Exception as es:
            messagebox.showerror("Lỗi Database", f"Lỗi khi cập nhật dữ liệu: {str(es)}", parent=self.root)

    # Thêm phương thức toggle_fullscreen
    def toggle_fullscreen(self, event=None):
        """Chuyển đổi giữa chế độ fullscreen và không fullscreen"""
        is_fullscreen = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not is_fullscreen)
        return "break"

    # Thêm hàm tạo style cho các thành phần
    def create_styles(self):
        # Tạo style cho Treeview (bảng)
        style = ttk.Style()
        style.theme_use("clam")  # Sử dụng theme "clam" cho vẻ hiện đại
        
        # Style cho bảng
        style.configure("Treeview", 
                        background="white",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="white")
        
        # Style cho header của bảng
        style.configure("Treeview.Heading", 
                        font=('verdana', 10, 'bold'),
                        background="#3b5998",
                        foreground="white")
        
        # Style khi chọn dòng trong bảng
        style.map('Treeview', 
                  background=[('selected', '#4a6fbf')],
                  foreground=[('selected', 'white')])
        
        # Style cho nút
        style.configure("TButton", 
                        font=('verdana', 10, 'bold'),
                        background="#3b5998")
                        
        # Style cho entry
        style.configure("TEntry", 
                        font=('verdana', 10))
                        
        # Style cho combobox
        style.configure("TCombobox", 
                        font=('verdana', 10),
                        background="white")

    # Thêm phương thức lọc dữ liệu
    def filter_data(self):
        try:
            # Lấy giá trị lọc
            filter_date = self.var_filter_date.get().strip()
            filter_session = self.var_filter_session.get()
            
            # Xóa dữ liệu hiện tại trong bảng
            self.attendanceReport.delete(*self.attendanceReport.get_children())
            
            # Kết nối database
            conn = mysql.connector.connect(username='root', password='12345', host='localhost', database='face_recognition', port=3307)
            mycursor = conn.cursor()
            
            # Xây dựng truy vấn SQL dựa trên bộ lọc
            query = "SELECT * FROM stdattendance WHERE 1=1"
            params = []
            
            # Lọc theo ngày nếu có
            if filter_date != "":
                query += " AND std_date=%s"
                params.append(filter_date)
            
            # Lọc theo buổi từ dropdown
            if filter_session == "Sáng (7:30-11:30)":
                query += " AND std_session=%s"
                params.append("Sáng")
            elif filter_session == "Chiều (13:00-17:00)":
                query += " AND std_session=%s"
                params.append("Chiều")
            
            # Thực hiện truy vấn
            mycursor.execute(query, params)
            data = mycursor.fetchall()
            
            # Hiển thị dữ liệu lọc
            if len(data) != 0:
                for i in data:
                    self.attendanceReport.insert("", END, values=i)
            
            messagebox.showinfo("Kết quả lọc", f"Đã tìm thấy {len(data)} bản ghi", parent=self.root)
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"[ERROR] Lỗi khi lọc dữ liệu: {str(e)}")
            messagebox.showerror("Lỗi Database", f"Lỗi khi lọc dữ liệu: {str(e)}", parent=self.root)

    # Thêm phương thức xóa lọc
    def clear_filter(self):
        self.var_filter_date.set(datetime.now().strftime("%d/%m/%Y"))
        self.var_filter_session.set("Tất cả")
        self.fetch_data()  # Tải lại toàn bộ dữ liệu

    # Thêm phương thức xóa bản ghi CSV
    def delete_csv(self):
        try:
            # Xác nhận xóa
            if self.attendanceReport_left.focus() == "":
                messagebox.showerror("Lỗi","Vui lòng chọn bản ghi cần xóa!",parent=self.root)
                return
            
            # Lấy giá trị ID từ focus
            id_value = self.var_id.get()

            # Xác nhận từ người dùng
            confirm = messagebox.askyesno("Xác nhận xóa","Bạn có chắc muốn xóa bản ghi này?",parent=self.root)
            if confirm:
                # Tìm và xóa bản ghi khỏi mydata
                for i, item in enumerate(mydata):
                    if str(item[0]) == str(id_value):
                        mydata.pop(i)
                        break
                
                # Ghi lại file CSV với header mới bao gồm cột session
                with open("attendance.csv", 'w', newline="") as csvfile:
                    writer = csv.writer(csvfile, delimiter=",")
                    # Ghi header với cột session
                    writer.writerow(["ID", "Roll_No", "Name", "Time", "Date", "Session", "Attend"])
                    # Ghi dữ liệu
                    writer.writerows(mydata)
                
                # Cập nhật lại bảng
                self.load_attendance_csv()
                # Cập nhật trường nhập để xóa dữ liệu cũ
                self.reset_data()
                messagebox.showinfo("Xóa","Đã xóa bản ghi thành công!",parent=self.root)
        except Exception as es:
            messagebox.showerror("Lỗi",f"Lỗi khi xóa bản ghi: {str(es)}",parent=self.root)

    # Thêm hàm xác định buổi từ thời gian
    def get_session_from_time(self, time_str):
        try:
            # Chuyển đổi chuỗi thời gian thành đối tượng datetime
            time_parts = time_str.split(":")
            hour = int(time_parts[0])
            
            # Xác định buổi dựa trên giờ
            if 7 <= hour < 12:
                return "Sáng"
            elif 13 <= hour < 17:
                return "Chiều"
            else:
                return "Khác"
        except Exception as e:
            print(f"[ERROR] Lỗi khi xác định buổi: {str(e)}")
            return "Khác"

    def update_csv(self):
        try:
            # Lấy row_id từ focus của bảng bên trái
            if self.attendanceReport_left.focus() == "":
                messagebox.showerror("Lỗi", "Vui lòng chọn bản ghi cần cập nhật!", parent=self.root)
                return
            
            # Lấy số hàng của mydata và đảm bảo nó có ít nhất 7 cột sau khi cập nhật
            id_value = self.var_id.get()
            for i, row in enumerate(mydata):
                if str(row[0]) == str(id_value):
                    # Xác định buổi từ thời gian
                    session = self.get_session_from_time(self.var_time.get())
                    
                    # Cập nhật dữ liệu với 7 cột (bao gồm cột session)
                    mydata[i] = [
                        self.var_id.get(), 
                        self.var_roll.get(), 
                        self.var_name.get(), 
                        self.var_time.get(), 
                        self.var_date.get(),
                        session,  # Thêm cột session
                        self.var_attend.get()
                    ]
                    break
            
            # Ghi ra file CSV với header
            with open("attendance.csv", "w", newline="") as csvfile:
                writer = csv.writer(csvfile, delimiter=",")
                # Thêm header với cột session mới
                writer.writerow(["ID", "Roll_No", "Name", "Time", "Date", "Session", "Attend"])
                # Ghi dữ liệu
                writer.writerows(mydata)
            
            # Cập nhật lại bảng bên trái
            self.load_attendance_csv()
            messagebox.showinfo("Thành công", "Đã cập nhật thông tin trong file CSV!", parent=self.root)
            
        except Exception as es:
            messagebox.showerror("Lỗi", f"Lỗi: {str(es)}", parent=self.root)

    # Thêm phương thức để tạo file CSV mới với định dạng bao gồm cột session
    def reset_attendance_csv(self):
        try:
            # Xác nhận từ người dùng
            confirm = messagebox.askyesno("Xác nhận reset", "Bạn có chắc muốn xóa toàn bộ dữ liệu điểm danh hiện tại?\nHành động này không thể hoàn tác!", parent=self.root)
            if not confirm:
                return
            
            # Tạo file attendance.csv mới với chỉ có header
            with open("attendance.csv", "w", newline="") as csvfile:
                writer = csv.writer(csvfile, delimiter=",")
                # Header mới bao gồm cột Session
                writer.writerow(["ID", "Roll_No", "Name", "Time", "Date", "Session", "Attend"])
            
            # Reset mydata và bảng hiển thị
            global mydata
            mydata.clear()
            self.attendanceReport_left.delete(*self.attendanceReport_left.get_children())
            
            # Reset các trường nhập liệu
            self.reset_data()
            
            messagebox.showinfo("Reset thành công", "Đã xóa toàn bộ dữ liệu điểm danh!", parent=self.root)
        except Exception as es:
            messagebox.showerror("Lỗi", f"Lỗi khi reset dữ liệu: {str(es)}", parent=self.root)

    # Exit current window and return to main menu
    def exit_window(self):
        self.root.destroy()

if __name__ == "__main__":
    root=Tk()
    obj=Attendance(root)
    root.mainloop()