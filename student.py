from tkinter import* 
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
# Testing Connection 
"""
conn = mysql.connector.connect(username='root', password='12345',host='localhost',database='face_recognition',port=3307)
cursor = conn.cursor()

cursor.execute("show databases")

data = cursor.fetchall()

print(data)

conn.close()
"""
class Student:
    def __init__(self,root):
        self.root=root
        # Thiết lập toàn màn hình
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.title("Quản Lý Sinh Viên")
        
        # Thêm phím tắt để thoát khỏi chế độ fullscreen (Esc)
        self.root.bind("<Escape>", self.toggle_fullscreen)

        #-----------Variables-------------------
        self.var_dep=StringVar()
        self.var_course=StringVar()
        self.var_year=StringVar()
        self.var_semester=StringVar()
        self.var_std_id=StringVar()
        self.var_std_name=StringVar()
        self.var_div=StringVar()
        self.var_roll=StringVar()
        self.var_gender=StringVar()
        self.var_dob=StringVar()
        self.var_email=StringVar()
        self.var_mob=StringVar()
        self.var_address=StringVar()
        self.var_teacher=StringVar()

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
        bg1=Image.open(r".\Images_GUI\bg3.jpg")
        bg1=bg1.resize((screen_width,screen_height),Image.LANCZOS)
        self.photobg1=ImageTk.PhotoImage(bg1)

        # set image as lable
        bg_img = Label(self.root,image=self.photobg1)
        bg_img.place(x=0,y=130,width=screen_width,height=screen_height-130)

        #title section
        title_lb1 = Label(bg_img,text="Quản Lý Thông Tin Sinh Viên",font=("Times New Roman",32,"bold"),bg="white",fg="#00008B")
        title_lb1.place(x=0,y=0,width=screen_width,height=50)
        
        # Tính toán kích thước khung chính dựa trên kích thước màn hình
        main_frame_width = min(1355, screen_width - 10)
        main_frame_height = min(580, screen_height - 180)  # Tăng chiều cao từ 510 lên 580

        # Creating Frame 
        main_frame = Frame(bg_img,bd=2,bg="white") #bd mean border 
        main_frame.place(x=(screen_width-main_frame_width)//2,y=55,width=main_frame_width,height=main_frame_height)
        
        # Tính toán kích thước cho các frame con
        left_frame_width = main_frame_width // 2 - 15
        right_frame_width = main_frame_width // 2 - 15

        # Left Label Frame 
        left_frame = LabelFrame(main_frame,bd=2,bg="white",relief=RIDGE,text="Thông tin Sinh viên",font=("Times New Roman",12,"bold"),fg="#00008B")
        left_frame.place(x=10,y=10,width=left_frame_width,height=main_frame_height-20)

        # Current Course 
        current_course_frame = LabelFrame(left_frame,bd=2,bg="white",relief=RIDGE,text="Khoá học hiện tại",font=("Times New Roman",12,"bold"),fg="#00008B")
        current_course_frame.place(x=10,y=5,width=left_frame_width-20,height=150)

        # Tính toán khoảng cách đều nhau - điều chỉnh cho phù hợp hơn
        field_width = 25  # Tăng kích thước combobox
        label_width = 8
        field_padx = 5
        field_pady = 8
        
        #label Department
        dep_label=Label(current_course_frame,text="Khoa:",font=("Times New Roman",12,"bold"),bg="white",fg="#00008B", width=label_width, anchor=E)
        dep_label.grid(row=0,column=0,padx=field_padx,pady=field_pady)

        #combo box 
        dep_combo=ttk.Combobox(current_course_frame,textvariable=self.var_dep,width=field_width,font=("Times New Roman",12,"bold"),state="readonly")
        dep_combo["values"]=("Chọn Khoa","CNTT","Điện tử","Kinh tế","Cơ khí","KHTN")
        dep_combo.current(0)
        dep_combo.grid(row=0,column=1,padx=field_padx,pady=field_pady,sticky=W)

        # -----------------------------------------------------

        #label Course
        cou_label=Label(current_course_frame,text="Ngành:",font=("Times New Roman",12,"bold"),bg="white",fg="#00008B", width=label_width, anchor=E)
        cou_label.grid(row=0,column=2,padx=field_padx,pady=field_pady)

        #combo box 
        cou_combo=ttk.Combobox(current_course_frame,textvariable=self.var_course,width=field_width,font=("Times New Roman",12,"bold"),state="readonly")
        cou_combo["values"]=("Chọn Ngành","CNPM","KTPM","HTTT","KHMT","MMT")
        cou_combo.current(0)
        cou_combo.grid(row=0,column=3,padx=field_padx,pady=field_pady,sticky=W)

        #-------------------------------------------------------------

        #label Year
        year_label=Label(current_course_frame,text="Năm học:",font=("Times New Roman",12,"bold"),bg="white",fg="#00008B", width=label_width, anchor=E)
        year_label.grid(row=1,column=0,padx=field_padx,pady=field_pady)

        #combo box 
        year_combo=ttk.Combobox(current_course_frame,textvariable=self.var_year,width=field_width,font=("Times New Roman",12,"bold"),state="readonly")
        year_combo["values"]=("Chọn Năm","2017-21","2018-22","2019-23","2020-24","2021-25")
        year_combo.current(0)
        year_combo.grid(row=1,column=1,padx=field_padx,pady=field_pady,sticky=W)

        #-----------------------------------------------------------------

        #label Semester 
        year_label=Label(current_course_frame,text="Học kỳ:",font=("Times New Roman",12,"bold"),bg="white",fg="#00008B", width=label_width, anchor=E)
        year_label.grid(row=1,column=2,padx=field_padx,pady=field_pady)

        #combo box 
        year_combo=ttk.Combobox(current_course_frame,textvariable=self.var_semester,width=field_width,font=("Times New Roman",12,"bold"),state="readonly")
        year_combo["values"]=("Chọn Học kỳ","Học kỳ-1","Học kỳ-2","Học kỳ-3","Học kỳ-4","Học kỳ-5","Học kỳ-6","Học kỳ-7","Học kỳ-8")
        year_combo.current(0)
        year_combo.grid(row=1,column=3,padx=field_padx,pady=field_pady,sticky=W)

        #Class Student Information
        class_Student_frame = LabelFrame(left_frame,bd=2,bg="white",relief=RIDGE,text="Thông tin chi tiết",font=("Times New Roman",12,"bold"),fg="#00008B")
        class_Student_frame.place(x=10,y=160,width=left_frame_width-20,height=270)  # Tăng chiều cao từ 230 lên 270

        # Thiết lập các biến cho khoảng cách đồng nhất - giảm padding, tăng kích thước field
        detail_field_width = 25  # Tăng từ 15 lên 25
        detail_label_width = 8   # Giảm từ 10 xuống 8
        detail_padx = 5          # Giảm từ 10 xuống 5
        detail_pady = 3          # Giảm từ 5 xuống 3
        
        #Student id
        studentId_label = Label(class_Student_frame,text="Mã SV:",font=("Times New Roman",12,"bold"),fg="#00008B",bg="white", width=detail_label_width, anchor=E)
        studentId_label.grid(row=0,column=0,padx=detail_padx,pady=detail_pady,sticky=W)

        studentId_entry = ttk.Entry(class_Student_frame,textvariable=self.var_std_id,width=detail_field_width,font=("Times New Roman",12,"bold"))
        studentId_entry.grid(row=0,column=1,padx=detail_padx,pady=detail_pady,sticky=W)

        #Student name
        student_name_label = Label(class_Student_frame,text="Họ tên:",font=("Times New Roman",12,"bold"),fg="#00008B",bg="white", width=detail_label_width, anchor=E)
        student_name_label.grid(row=0,column=2,padx=detail_padx,pady=detail_pady,sticky=W)

        student_name_entry = ttk.Entry(class_Student_frame,textvariable=self.var_std_name,width=detail_field_width,font=("Times New Roman",12,"bold"))
        student_name_entry.grid(row=0,column=3,padx=detail_padx,pady=detail_pady,sticky=W)

        #Class Didvision
        student_div_label = Label(class_Student_frame,text="Lớp:",font=("Times New Roman",12,"bold"),fg="#00008B",bg="white", width=detail_label_width, anchor=E)
        student_div_label.grid(row=1,column=0,padx=detail_padx,pady=detail_pady,sticky=W)

        div_combo=ttk.Combobox(class_Student_frame,textvariable=self.var_div,width=detail_field_width-2,font=("Times New Roman",12,"bold"),state="readonly")
        div_combo["values"]=("Sáng","Chiều")
        div_combo.current(0)
        div_combo.grid(row=1,column=1,padx=detail_padx,pady=detail_pady,sticky=W)

        #Roll No
        student_roll_label = Label(class_Student_frame,text="Mã số:",font=("Times New Roman",12,"bold"),fg="#00008B",bg="white", width=detail_label_width, anchor=E)
        student_roll_label.grid(row=1,column=2,padx=detail_padx,pady=detail_pady,sticky=W)

        student_roll_entry = ttk.Entry(class_Student_frame,textvariable=self.var_roll,width=detail_field_width,font=("Times New Roman",12,"bold"))
        student_roll_entry.grid(row=1,column=3,padx=detail_padx,pady=detail_pady,sticky=W)

        #Gender
        student_gender_label = Label(class_Student_frame,text="Giới tính:",font=("Times New Roman",12,"bold"),fg="#00008B",bg="white", width=detail_label_width, anchor=E)
        student_gender_label.grid(row=2,column=0,padx=detail_padx,pady=detail_pady,sticky=W)

        #combo box 
        gender_combo=ttk.Combobox(class_Student_frame,textvariable=self.var_gender,width=detail_field_width-2,font=("Times New Roman",12,"bold"),state="readonly")
        gender_combo["values"]=("Nam","Nữ","Khác")
        gender_combo.current(0)
        gender_combo.grid(row=2,column=1,padx=detail_padx,pady=detail_pady,sticky=W)

        #Date of Birth
        student_dob_label = Label(class_Student_frame,text="Ngày sinh:",font=("Times New Roman",12,"bold"),fg="#00008B",bg="white", width=detail_label_width, anchor=E)
        student_dob_label.grid(row=2,column=2,padx=detail_padx,pady=detail_pady,sticky=W)

        student_dob_entry = ttk.Entry(class_Student_frame,textvariable=self.var_dob,width=detail_field_width,font=("Times New Roman",12,"bold"))
        student_dob_entry.grid(row=2,column=3,padx=detail_padx,pady=detail_pady,sticky=W)

        #Email
        student_email_label = Label(class_Student_frame,text="Email:",font=("Times New Roman",12,"bold"),fg="#00008B",bg="white", width=detail_label_width, anchor=E)
        student_email_label.grid(row=3,column=0,padx=detail_padx,pady=detail_pady,sticky=W)

        student_email_entry = ttk.Entry(class_Student_frame,textvariable=self.var_email,width=detail_field_width,font=("Times New Roman",12,"bold"))
        student_email_entry.grid(row=3,column=1,padx=detail_padx,pady=detail_pady,sticky=W)

        #Phone Number
        student_mob_label = Label(class_Student_frame,text="SĐT:",font=("Times New Roman",12,"bold"),fg="#00008B",bg="white", width=detail_label_width, anchor=E)
        student_mob_label.grid(row=3,column=2,padx=detail_padx,pady=detail_pady,sticky=W)

        student_mob_entry = ttk.Entry(class_Student_frame,textvariable=self.var_mob,width=detail_field_width,font=("Times New Roman",12,"bold"))
        student_mob_entry.grid(row=3,column=3,padx=detail_padx,pady=detail_pady,sticky=W)

        #Address
        student_address_label = Label(class_Student_frame,text="Địa chỉ:",font=("Times New Roman",12,"bold"),fg="#00008B",bg="white", width=detail_label_width, anchor=E)
        student_address_label.grid(row=4,column=0,padx=detail_padx,pady=detail_pady,sticky=W)

        student_address_entry = ttk.Entry(class_Student_frame,textvariable=self.var_address,width=detail_field_width,font=("Times New Roman",12,"bold"))
        student_address_entry.grid(row=4,column=1,padx=detail_padx,pady=detail_pady,sticky=W)

        #Teacher Name
        student_tutor_label = Label(class_Student_frame,text="Giảng viên:",font=("Times New Roman",12,"bold"),fg="#00008B",bg="white", width=detail_label_width, anchor=E)
        student_tutor_label.grid(row=4,column=2,padx=detail_padx,pady=detail_pady,sticky=W)

        student_tutor_entry = ttk.Entry(class_Student_frame,textvariable=self.var_teacher,width=detail_field_width,font=("Times New Roman",12,"bold"))
        student_tutor_entry.grid(row=4,column=3,padx=detail_padx,pady=detail_pady,sticky=W)

        #Radio Buttons
        radio_frame = Frame(class_Student_frame, bg="white")
        radio_frame.grid(row=5, column=0, columnspan=4, sticky=W, padx=detail_padx+5, pady=4)
        
        self.var_radio1=StringVar()
        radiobtn1=ttk.Radiobutton(radio_frame,text="Có hình ảnh",variable=self.var_radio1,value="Yes")
        radiobtn1.grid(row=0,column=0,padx=30,pady=2)

        radiobtn2=ttk.Radiobutton(radio_frame,text="Không có hình ảnh",variable=self.var_radio1,value="No")
        radiobtn2.grid(row=0,column=1,padx=30,pady=2)
        
        # Help button for explanation
        help_btn = Button(radio_frame, text="?", command=self.explain_photo_option, 
                         font=("Times New Roman", 8, "bold"), 
                         fg="white", bg="#008CBA", cursor="hand2", 
                         relief=RAISED, width=2, height=1)
        help_btn.grid(row=0, column=2, padx=20, pady=2)

        #Button Frame
        btn_frame = Frame(left_frame,bd=2,bg="white",relief=RIDGE)
        btn_frame.place(x=10,y=435,width=left_frame_width-20,height=60)  # Điều chỉnh vị trí y từ 390 lên 435

        # Tính toán kích thước nút và khoảng cách để phân bố đều
        btn_count = 6  # Số lượng nút
        total_width = left_frame_width - 40  # Trừ padding
        btn_width = total_width // btn_count
        btn_padx = 5

        #save button
        save_btn=Button(btn_frame,command=self.add_data,text="Lưu",width=7,font=("Times New Roman",12,"bold"),fg="white",bg="#00008B", relief=RAISED)
        save_btn.grid(row=0,column=0,padx=btn_padx,pady=10,sticky=W)

        #update button
        update_btn=Button(btn_frame,command=self.update_data,text="Cập nhật",width=10,font=("Times New Roman",12,"bold"),fg="white",bg="#00008B", relief=RAISED)
        update_btn.grid(row=0,column=1,padx=btn_padx,pady=8,sticky=W)

        #delete button
        del_btn=Button(btn_frame,command=self.delete_data,text="Xóa",width=7,font=("Times New Roman",12,"bold"),fg="white",bg="#00008B", relief=RAISED)
        del_btn.grid(row=0,column=2,padx=btn_padx,pady=10,sticky=W)

        #reset button
        reset_btn=Button(btn_frame,command=self.reset_data,text="Làm mới",width=10,font=("Times New Roman",12,"bold"),fg="white",bg="#00008B", relief=RAISED)
        reset_btn.grid(row=0,column=3,padx=btn_padx,pady=10,sticky=W)

        #take photo button
        take_photo_btn=Button(btn_frame,command=self.generate_dataset,text="Chụp ảnh",width=10,font=("Times New Roman",12,"bold"),fg="white",bg="#00008B", relief=RAISED)
        take_photo_btn.grid(row=0,column=4,padx=btn_padx,pady=10,sticky=W)

        #update photo button
        update_photo_btn=Button(btn_frame,text="Cập nhật ảnh",width=13,font=("Times New Roman",12,"bold"),fg="white",bg="#00008B", relief=RAISED)
        update_photo_btn.grid(row=0,column=5,padx=btn_padx,pady=10,sticky=W)

        #----------------------------------------------------------------------
        # Right Label Frame 
        right_frame = LabelFrame(main_frame,bd=2,bg="white",relief=RIDGE,text="Danh sách sinh viên",font=("Times New Roman",12,"bold"),fg="#00008B")
        right_frame.place(x=left_frame_width+10,y=10,width=right_frame_width,height=main_frame_height-20)

        #Searching System in Right Label Frame 
        search_frame = LabelFrame(right_frame,bd=2,bg="white",relief=RIDGE,text="Tìm kiếm",font=("Times New Roman",12,"bold"),fg="#00008B")
        search_frame.place(x=10,y=5,width=right_frame_width-20,height=80)

        # Tính toán khoảng cách đều và phù hợp
        search_padx = 8
        search_pady = 15
        search_field_width = 20  # Tăng chiều rộng ô tìm kiếm
        
        #Search label
        search_label = Label(search_frame,text="Tìm kiếm:",font=("Times New Roman",12,"bold"),fg="#00008B",bg="white", width=8, anchor=E)
        search_label.grid(row=0,column=0,padx=search_padx,pady=search_pady,sticky=W)
        
        self.var_searchTX=StringVar()
        
        #combo box 
        search_combo=ttk.Combobox(search_frame,textvariable=self.var_searchTX,width=15,font=("Times New Roman",12,"bold"),state="readonly")
        search_combo["values"]=("Chọn","Mã SV","Mã số","Họ tên","Lớp","Năm học","Ngành")
        search_combo.current(0)
        search_combo.grid(row=0,column=1,padx=search_padx,pady=search_pady,sticky=W)

        self.var_search=StringVar()
        search_entry = ttk.Entry(search_frame,textvariable=self.var_search,width=search_field_width,font=("Times New Roman",12,"bold"))
        search_entry.grid(row=0,column=2,padx=search_padx,pady=search_pady,sticky=W)

        search_btn=Button(search_frame,command=self.search_data,text="Tìm kiếm",width=9,font=("Times New Roman",12,"bold"),fg="white",bg="#00008B", relief=RAISED)
        search_btn.grid(row=0,column=3,padx=search_padx,pady=search_pady,sticky=W)

        showAll_btn=Button(search_frame,command=self.fetch_data,text="Xem tất cả",width=10,font=("Times New Roman",12,"bold"),fg="white",bg="#00008B", relief=RAISED)
        showAll_btn.grid(row=0,column=4,padx=search_padx,pady=search_pady,sticky=W)

        # -----------------------------Table Frame-------------------------------------------------
        # Table Frame 
        table_frame = Frame(right_frame, bd=2, bg="white", relief=RIDGE)
        table_frame.place(x=10, y=90, width=right_frame_width-20, height=main_frame_height-120)
        
        # Tạo frame con cho bảng dữ liệu (không chứa thanh cuộn ngang)
        data_frame = Frame(table_frame, bg="white")
        data_frame.pack(side=TOP, fill=BOTH, expand=True, padx=0, pady=0)
        
        # Tạo frame riêng cho thanh cuộn ngang, đặt ở vị trí cách đáy khoảng 20px
        scroll_frame = Frame(table_frame, bg="#f0f0f0", height=25)
        scroll_frame.pack(side=BOTTOM, fill=X, padx=0, pady=(0, 20))
        
        # Đặt thanh cuộn ngang vào frame riêng
        scroll_x = ttk.Scrollbar(scroll_frame, orient=HORIZONTAL)
        scroll_x.pack(side=TOP, fill=X)
        
        # Thanh cuộn dọc đặt bên phải bảng dữ liệu
        scroll_y = ttk.Scrollbar(data_frame, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        # Điều chỉnh kích thước cột để đảm bảo tổng chiều rộng lớn hơn khung hiển thị
        column_width = {
            "ID": 100,
            "Name": 200,
            "Dep": 150,
            "Course": 150,
            "Year": 120,
            "Sem": 150,
            "Div": 120,
            "Gender": 120,
            "DOB": 150,
            "Mob-No": 150,
            "Address": 200,
            "Roll-No": 120,
            "Email": 200,
            "Teacher": 180,
            "Photo": 100
        }
        
        # Tạo bảng trong frame dữ liệu
        self.student_table = ttk.Treeview(data_frame,
                columns=("ID","Name","Dep","Course","Year","Sem","Div","Gender","DOB","Mob-No","Address","Roll-No","Email","Teacher","Photo"),
                xscrollcommand=scroll_x.set,
                yscrollcommand=scroll_y.set)

        # Kết nối thanh cuộn với bảng
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)
        
        # Làm nổi bật thanh cuộn ngang
        style = ttk.Style()
        style.configure("Horizontal.TScrollbar", arrowsize=20, background="#00008B", troughcolor="#f0f0f0", borderwidth=2)
        scroll_x.configure(style="Horizontal.TScrollbar")
        
        # Điều chỉnh style của bảng
        style.configure("Treeview", rowheight=25)
        style.configure("Treeview.Heading", font=('Times New Roman', 12, 'bold'))
        
        # Đặt tiêu đề cột
        self.student_table.heading("ID",text="Mã SV")
        self.student_table.heading("Name",text="Họ tên")
        self.student_table.heading("Dep",text="Khoa")
        self.student_table.heading("Course",text="Ngành")
        self.student_table.heading("Year",text="Năm học")
        self.student_table.heading("Sem",text="Học kỳ")
        self.student_table.heading("Div",text="Lớp")
        self.student_table.heading("Gender",text="Giới tính")
        self.student_table.heading("DOB",text="Ngày sinh")
        self.student_table.heading("Mob-No",text="SĐT")
        self.student_table.heading("Address",text="Địa chỉ")
        self.student_table.heading("Roll-No",text="Mã số")
        self.student_table.heading("Email",text="Email")
        self.student_table.heading("Teacher",text="Giảng viên")
        self.student_table.heading("Photo",text="Hình ảnh")
        self.student_table["show"]="headings"

        # Đặt chiều rộng cột
        for col, width in column_width.items():
            self.student_table.column(col, width=width, minwidth=width)
            
        # Hiển thị bảng dữ liệu
        self.student_table.pack(fill=BOTH, expand=1)
        
        # Thêm tag cho hàng lẻ và hàng chẵn để tạo màu nền xen kẽ
        self.student_table.tag_configure('oddrow', background="white")
        self.student_table.tag_configure('evenrow', background="#f0f0f0")
        
        self.student_table.bind("<ButtonRelease>",self.get_cursor)
        self.fetch_data()
# ==================Function Decleration==============================
    def add_data(self):
        # Kiểm tra từng trường dữ liệu và hiển thị lỗi cụ thể
        missing_fields = []
        
        if self.var_dep.get()=="Chọn Khoa":
            missing_fields.append("Khoa")
        if self.var_course.get()=="Chọn Ngành":
            missing_fields.append("Ngành")
        if self.var_year.get()=="Chọn Năm":
            missing_fields.append("Năm học")
        if self.var_semester.get()=="Chọn Học kỳ":
            missing_fields.append("Học kỳ")
        if self.var_std_id.get()=="":
            missing_fields.append("Mã SV")
        if self.var_std_name.get()=="":
            missing_fields.append("Họ tên")
        if self.var_div.get()=="":
            missing_fields.append("Lớp")
        if self.var_roll.get()=="":
            missing_fields.append("Mã số")
        if self.var_gender.get()=="":
            missing_fields.append("Giới tính")
        if self.var_dob.get()=="":
            missing_fields.append("Ngày sinh")
        if self.var_email.get()=="":
            missing_fields.append("Email")
        if self.var_mob.get()=="":
            missing_fields.append("SĐT")
        if self.var_address.get()=="":
            missing_fields.append("Địa chỉ")
        if self.var_teacher.get()=="":
            missing_fields.append("Giảng viên")
        
        if missing_fields:
            error_msg = "Vui lòng điền các trường: " + ", ".join(missing_fields)
            messagebox.showerror("Lỗi", error_msg, parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(username='root', password='12345',host='localhost',database='face_recognition',port=3307)
                mycursor = conn.cursor()
                mycursor.execute("insert into student(Student_ID, Name, Department, Course, Year, Semester, Division, Gender, DOB, Mobile_No, Address, Roll_No, Email, Teacher_Name, PhotoSample) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(
                self.var_std_id.get(),
                self.var_std_name.get(),
                self.var_dep.get(),
                self.var_course.get(),
                self.var_year.get(),
                self.var_semester.get(),
                self.var_div.get(),
                self.var_gender.get(),
                self.var_dob.get(),
                self.var_mob.get(),
                self.var_address.get(),
                self.var_roll.get(),
                self.var_email.get(),
                self.var_teacher.get(),
                self.var_radio1.get()
                ))

                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Thành công","Đã lưu thông tin sinh viên!",parent=self.root)
            except Exception as es:
                messagebox.showerror("Lỗi",f"Lỗi cơ sở dữ liệu: {str(es)}",parent=self.root)

    # ===========================Fetch data form database to table ================================

    def fetch_data(self):
        conn = mysql.connector.connect(username='root', password='12345',host='localhost',database='face_recognition',port=3307)
        mycursor = conn.cursor()

        mycursor.execute("select * from student")
        data=mycursor.fetchall()

        if len(data)!= 0:
            self.student_table.delete(*self.student_table.get_children())
            for i, row in enumerate(data):
                # Thêm tag để tạo màu nền xen kẽ
                if i % 2 == 0:
                    self.student_table.insert("",END,values=row, tags=('evenrow',))
                else:
                    self.student_table.insert("",END,values=row, tags=('oddrow',))
            
            # Sau khi load dữ liệu, đảm bảo thanh cuộn ngang được cập nhật
            self.student_table.update_idletasks()
            
            conn.commit()
        conn.close()
        
        # Đảm bảo thanh cuộn ngang hiển thị
        if self.student_table.get_children():
            self.student_table.see(self.student_table.get_children()[0])
            # Dịch chuyển để kích hoạt thanh cuộn ngang
            self.root.after(100, lambda: self.student_table.xview_moveto(0.2))
            self.root.after(400, lambda: self.student_table.xview_moveto(0))

    #================================get cursor function=======================

    def get_cursor(self,event=""):
        cursor_focus = self.student_table.focus()
        content = self.student_table.item(cursor_focus)
        data = content["values"]

        self.var_std_id.set(data[0]),
        self.var_std_name.set(data[1]),
        self.var_dep.set(data[2]),
        self.var_course.set(data[3]),
        self.var_year.set(data[4]),
        self.var_semester.set(data[5]),
        self.var_div.set(data[6]),
        self.var_gender.set(data[7]),
        self.var_dob.set(data[8]),
        self.var_mob.set(data[9]),
        self.var_address.set(data[10]),
        self.var_roll.set(data[11]),
        self.var_email.set(data[12]),
        self.var_teacher.set(data[13]),
        self.var_radio1.set(data[14])
    # ========================================Update Function==========================
    def update_data(self):
        # Kiểm tra từng trường dữ liệu và hiển thị lỗi cụ thể
        missing_fields = []
        
        if self.var_dep.get()=="Chọn Khoa":
            missing_fields.append("Khoa")
        if self.var_course.get()=="Chọn Ngành":
            missing_fields.append("Ngành")
        if self.var_year.get()=="Chọn Năm":
            missing_fields.append("Năm học")
        if self.var_semester.get()=="Chọn Học kỳ":
            missing_fields.append("Học kỳ")
        if self.var_std_id.get()=="":
            missing_fields.append("Mã SV")
        if self.var_std_name.get()=="":
            missing_fields.append("Họ tên")
        if self.var_div.get()=="":
            missing_fields.append("Lớp")
        if self.var_roll.get()=="":
            missing_fields.append("Mã số")
        if self.var_gender.get()=="":
            missing_fields.append("Giới tính")
        if self.var_dob.get()=="":
            missing_fields.append("Ngày sinh")
        if self.var_email.get()=="":
            missing_fields.append("Email")
        if self.var_mob.get()=="":
            missing_fields.append("SĐT")
        if self.var_address.get()=="":
            missing_fields.append("Địa chỉ")
        if self.var_teacher.get()=="":
            missing_fields.append("Giảng viên")
        
        if missing_fields:
            error_msg = "Vui lòng điền các trường: " + ", ".join(missing_fields)
            messagebox.showerror("Lỗi", error_msg, parent=self.root)
        else:
            try:
                Update=messagebox.askyesno("Cập nhật","Bạn có muốn cập nhật thông tin sinh viên này?",parent=self.root)
                if Update > 0:
                    conn = None
                    try:
                        conn = mysql.connector.connect(username='root', password='12345',host='localhost',database='face_recognition',port=3307)
                        mycursor = conn.cursor()
                        mycursor.execute("update student set Name=%s,Department=%s,Course=%s,Year=%s,Semester=%s,Division=%s,Gender=%s,DOB=%s,Mobile_No=%s,Address=%s,Roll_No=%s,Email=%s,Teacher_Name=%s,PhotoSample=%s where Student_ID=%s",( 
                        self.var_std_name.get(),
                        self.var_dep.get(),
                        self.var_course.get(),
                        self.var_year.get(),
                        self.var_semester.get(),
                        self.var_div.get(),
                        self.var_gender.get(),
                        self.var_dob.get(),
                        self.var_mob.get(),
                        self.var_address.get(),
                        self.var_roll.get(),
                        self.var_email.get(),
                        self.var_teacher.get(),
                        self.var_radio1.get(),
                        self.var_std_id.get()   
                        ))
                        conn.commit()
                        self.fetch_data()
                        messagebox.showinfo("Thành công","Đã cập nhật thông tin sinh viên!",parent=self.root)
                    except Exception as es:
                        messagebox.showerror("Lỗi",f"Lỗi cơ sở dữ liệu: {str(es)}",parent=self.root)
                    finally:
                        if conn is not None:
                            conn.close()
            except Exception as e:
                messagebox.showerror("Lỗi",f"Đã xảy ra lỗi: {str(e)}",parent=self.root)
    
    #==============================Delete Function=========================================
    def delete_data(self):
        if self.var_std_id.get()=="":
            messagebox.showerror("Lỗi","Mã sinh viên không được để trống!",parent=self.root)
        else:
            try:
                delete=messagebox.askyesno("Xóa thông tin","Bạn có chắc muốn xóa thông tin này?",parent=self.root)
                if delete>0:
                    conn = mysql.connector.connect(username='root', password='12345',host='localhost',database='face_recognition',port=3307)
                    mycursor = conn.cursor() 
                    sql="delete from student where Student_ID=%s"
                    val=(self.var_std_id.get(),)
                    mycursor.execute(sql,val)
                else:
                    if not delete:
                        return

                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Xóa","Đã xóa thông tin thành công!",parent=self.root)
            except Exception as es:
                messagebox.showerror("Lỗi",f"Lỗi: {str(es)}",parent=self.root)    

    # Reset Function 
    def reset_data(self):
        self.var_std_id.set(""),
        self.var_std_name.set(""),
        self.var_dep.set("Chọn Khoa"),
        self.var_course.set("Chọn Ngành"),
        self.var_year.set("Chọn Năm"),
        self.var_semester.set("Chọn Học kỳ"),
        self.var_div.set("Sáng"),
        self.var_gender.set("Nam"),
        self.var_dob.set(""),
        self.var_mob.set(""),
        self.var_address.set(""),
        self.var_roll.set(""),
        self.var_email.set(""),
        self.var_teacher.set(""),
        self.var_radio1.set("")
    
    # ===========================Search Data===================
    def search_data(self):
        if self.var_search.get()=="" or self.var_searchTX.get()=="Chọn":
            messagebox.showerror("Lỗi","Vui lòng chọn loại tìm kiếm và nhập thông tin tìm kiếm",parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(username='root', password='12345',host='localhost',database='face_recognition',port=3307)
                my_cursor = conn.cursor()
                
                # Xác định cột tìm kiếm dựa trên lựa chọn
                search_column = ""
                if self.var_searchTX.get() == "Mã SV":
                    search_column = "Student_ID"
                elif self.var_searchTX.get() == "Mã số":
                    search_column = "Roll_No"
                elif self.var_searchTX.get() == "Họ tên":
                    search_column = "Name"
                elif self.var_searchTX.get() == "Lớp":
                    search_column = "Division"
                elif self.var_searchTX.get() == "Năm học":
                    search_column = "Year"
                elif self.var_searchTX.get() == "Ngành":
                    search_column = "Course"
                
                # Tạo câu truy vấn dựa trên loại tìm kiếm
                sql = f"SELECT Student_ID,Name,Department,Course,Year,Semester,Division,Gender,DOB,Mobile_No,Address,Roll_No,Email,Teacher_Name,PhotoSample FROM student where {search_column}='{str(self.var_search.get())}'" 
                my_cursor.execute(sql)
                rows=my_cursor.fetchall()        
                
                if len(rows)!=0:
                    self.student_table.delete(*self.student_table.get_children())
                    for i in rows:
                        self.student_table.insert("",END,values=i)
                    conn.commit()
                else:
                    messagebox.showinfo("Kết quả","Không tìm thấy dữ liệu phù hợp",parent=self.root)
                
                conn.close()
            except Exception as es:
                messagebox.showerror("Lỗi",f"Lỗi: {str(es)}",parent=self.root)


#=====================This part is related to Opencv Camera part=======================
# ==================================Generate Data set take image=========================
    def generate_dataset(self):
        # Kiểm tra các trường thông tin
        if self.var_dep.get()=="Chọn Khoa" or self.var_course.get()=="Chọn Ngành" or self.var_year.get()=="Chọn Năm" or self.var_semester.get()=="Chọn Học kỳ" or self.var_std_id.get()=="" or self.var_std_name.get()=="" or self.var_div.get()=="" or self.var_roll.get()=="" or self.var_gender.get()=="" or self.var_dob.get()=="" or self.var_email.get()=="" or self.var_mob.get()=="" or self.var_address.get()=="" or self.var_teacher.get()=="":
            messagebox.showerror("Lỗi","Vui lòng điền đầy đủ thông tin sinh viên!",parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(username='root', password='12345',host='localhost',database='face_recognition',port=3307)
                mycursor = conn.cursor()
                
                # Cập nhật thông tin sinh viên và đánh dấu đã chụp ảnh
                mycursor.execute("update student set Name=%s,Department=%s,Course=%s,Year=%s,Semester=%s,Division=%s,Gender=%s,DOB=%s,Mobile_No=%s,Address=%s,Roll_No=%s,Email=%s,Teacher_Name=%s,PhotoSample=%s where Student_ID=%s",(
                self.var_std_name.get(),
                self.var_dep.get(),
                self.var_course.get(),
                self.var_year.get(),
                self.var_semester.get(),
                self.var_div.get(),
                self.var_gender.get(),
                self.var_dob.get(),
                self.var_mob.get(),
                self.var_address.get(),
                self.var_roll.get(),
                self.var_email.get(),
                self.var_teacher.get(),
                self.var_radio1.get(),
                self.var_std_id.get()
                ))
                conn.commit()
                
                # Bắt đầu chụp ảnh
                face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
                
                def face_croped(img):
                    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                    faces = face_classifier.detectMultiScale(gray,1.3,5)
                    for (x,y,w,h) in faces:
                        face_croped=img[y:y+h,x:x+w]
                        return face_croped
                
                cap=cv2.VideoCapture(0)
                img_id=0
                
                while True:
                    ret,my_frame=cap.read()
                    if face_croped(my_frame) is not None:
                        img_id+=1
                        face=cv2.resize(face_croped(my_frame),(200,200))
                        face=cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
                        
                        # Chuyển ảnh thành dạng nhị phân để lưu vào MySQL
                        _, img_encoded = cv2.imencode('.jpg', face)
                        binary_data = img_encoded.tobytes()
                        
                        # Lưu ảnh vào database
                        sql = "INSERT INTO student_images (student_id, image_data, image_number) VALUES (%s, %s, %s)"
                        mycursor.execute(sql, (self.var_std_id.get(), binary_data, img_id))
                        conn.commit()
                        
                        # Hiển thị ảnh đã chụp
                        cv2.putText(face,str(img_id),(50,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,0),2)        
                        cv2.imshow("Chụp khuôn mặt",face)

                    if cv2.waitKey(1)==13 or int(img_id)==100:
                        break
                        
                cap.release()
                cv2.destroyAllWindows()
                messagebox.showinfo("Kết quả","Đã hoàn thành việc chụp khuôn mặt!",parent=self.root)
                
            except Exception as es:
                messagebox.showerror("Lỗi",f"Lỗi: {str(es)}",parent=self.root)
            finally:
                if conn is not None:
                    conn.close()

    # Thêm phương thức toggle_fullscreen
    def toggle_fullscreen(self, event=None):
        """Chuyển đổi giữa chế độ fullscreen và không fullscreen"""
        is_fullscreen = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not is_fullscreen)
        return "break"

    # Exit current window and return to main menu
    def exit_window(self):
        self.root.destroy()
        
    # Explain the difference between Photo options
    def explain_photo_option(self):
        explanation = """
Giải thích về lựa chọn hình ảnh:

- "Có hình ảnh": Sinh viên này sẽ được chụp ảnh khuôn mặt để sử dụng cho hệ thống điểm danh tự động bằng nhận diện khuôn mặt.

- "Không có hình ảnh": Sinh viên này sẽ không sử dụng tính năng nhận diện khuôn mặt và cần được điểm danh thủ công.

Khi chọn "Có hình ảnh" và nhấn nút "Chụp ảnh", hệ thống sẽ bật camera để chụp 100 ảnh khuôn mặt sinh viên ở các góc độ khác nhau và lưu vào cơ sở dữ liệu.
        """
        messagebox.showinfo("Giải thích lựa chọn hình ảnh", explanation, parent=self.root)

# main class object

if __name__ == "__main__":
    root=Tk()
    obj=Student(root)
    root.mainloop()
