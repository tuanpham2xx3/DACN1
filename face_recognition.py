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
        self.root.geometry("1366x768+0+0")
        self.root.title("Face Recognition Pannel")

        # This part is image labels setting start 
        # first header image  
        img=Image.open(r".\Images_GUI\banner.jpg")
        img=img.resize((1366,130),Image.LANCZOS)
        self.photoimg=ImageTk.PhotoImage(img)

        # set image as lable
        f_lb1 = Label(self.root,image=self.photoimg)
        f_lb1.place(x=0,y=0,width=1366,height=130)

        # backgorund image 
        bg1=Image.open(r".\Images_GUI\bg2.jpg")
        bg1=bg1.resize((1366,768),Image.LANCZOS)
        self.photobg1=ImageTk.PhotoImage(bg1)

        # set image as lable
        bg_img = Label(self.root,image=self.photobg1)
        bg_img.place(x=0,y=130,width=1366,height=768)


        #title section
        title_lb1 = Label(bg_img,text="Welcome to Face Recognition Pannel",font=("verdana",30,"bold"),bg="white",fg="navyblue")
        title_lb1.place(x=0,y=0,width=1366,height=45)

        # Create buttons below the section 
        # ------------------------------------------------------------------------------------------------------------------- 
        # Training button 1
        std_img_btn=Image.open(r".\Images_GUI\f_det.jpg")
        std_img_btn=std_img_btn.resize((180,180),Image.LANCZOS)
        self.std_img1=ImageTk.PhotoImage(std_img_btn)

        std_b1 = Button(bg_img,command=self.face_recog,image=self.std_img1,cursor="hand2")
        std_b1.place(x=600,y=170,width=180,height=180)

        std_b1_1 = Button(bg_img,command=self.face_recog,text="Face Detector",cursor="hand2",font=("tahoma",15,"bold"),bg="white",fg="navyblue")
        std_b1_1.place(x=600,y=350,width=180,height=45)
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
        def draw_boundray(img,classifier,scaleFactor,minNeighbors,color,text,clf):
            gray_image=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            featuers=classifier.detectMultiScale(gray_image,scaleFactor=1.3,minNeighbors=5,minSize=(30,30))

            coord=[]
            
            for (x,y,w,h) in featuers:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
                id,predict=clf.predict(gray_image[y:y+h,x:x+w])

                confidence=int((100*(1-predict/300)))

                # Debug: In ra ID và confidence để kiểm tra
                print(f"Detected ID: {id}, Confidence: {confidence}%")

                try:
                    conn = mysql.connector.connect(username='root', password='12345',host='localhost',database='face_recognition',port=3307)
                    cursor = conn.cursor()

                    # Sửa câu lệnh SQL để in ra để debug
                    query = f"SELECT Name, Roll_No, Student_ID FROM student WHERE Student_ID={str(id)}"
                    print(f"Executing query: {query}")
                    
                    # Thực hiện một truy vấn duy nhất để lấy tất cả thông tin
                    cursor.execute(query)
                    result = cursor.fetchone()
                    
                    if result:
                        n, r, i = result
                        print(f"Database result: Name={n}, Roll={r}, ID={i}")
                    else:
                        print(f"No results found for ID={id}")
                        n = r = i = "Unknown"

                except Exception as e:
                    print(f"Database error: {str(e)}")
                    n = r = i = "Unknown"
                finally:
                    cursor.close()
                    conn.close()

                if confidence > 50:
                    cv2.putText(img,f"ID:{i}",(x,y-75),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    cv2.putText(img,f"Roll:{r}",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    cv2.putText(img,f"Name:{n}",(x,y-30),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    cv2.putText(img,f"Confidence:{confidence}%",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    self.mark_attendance(i,r,n)
                else:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
                    cv2.putText(img,"Unknown Face",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,0),3)    

                coord=[x,y,w,y]
            
            return coord


        #==========
        def recognize(img,clf,faceCascade):
            coord=draw_boundray(img,faceCascade,1.1,10,(255,25,255),"Face",clf)
            return img
        
        # Kiểm tra file clf.xml
        if not os.path.exists("clf.xml"):
            messagebox.showerror("Error","Training file clf.xml not found!")
            return
        
        try:
            # Load classifier với thông tin debug
            clf=cv2.face.LBPHFaceRecognizer_create()
            print("Loading training file...")
            clf.read("clf.xml")
            print("Training file loaded successfully")
            
            faceCascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

            videoCap=cv2.VideoCapture(0)

            while True:
                ret,img=videoCap.read()
                img=recognize(img,clf,faceCascade)
                cv2.imshow("Face Detector",img)

                if cv2.waitKey(1) == 13:
                    break
            videoCap.release()
            cv2.destroyAllWindows()
        except Exception as e:
            messagebox.showerror("Error",f"Error during face recognition: {str(e)}")




if __name__ == "__main__":
    root=Tk()
    obj=Face_Recognition(root)
    root.mainloop()