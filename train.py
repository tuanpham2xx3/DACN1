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
        self.root.geometry("1366x768+0+0")
        self.root.title("Train Pannel")

        # This part is image labels setting start 
        # first header image  
        img=Image.open(r".\Images_GUI\banner.jpg")
        img=img.resize((1366,130),Image.LANCZOS)
        self.photoimg=ImageTk.PhotoImage(img)

        # set image as lable
        f_lb1 = Label(self.root,image=self.photoimg)
        f_lb1.place(x=0,y=0,width=1366,height=130)

        # backgorund image 
        bg1=Image.open(r".\Images_GUI\t_bg1.jpg")
        bg1=bg1.resize((1366,768),Image.LANCZOS)
        self.photobg1=ImageTk.PhotoImage(bg1)

        # set image as lable
        bg_img = Label(self.root,image=self.photobg1)
        bg_img.place(x=0,y=130,width=1366,height=768)


        #title section
        title_lb1 = Label(bg_img,text="Welcome to Training Pannel",font=("verdana",30,"bold"),bg="white",fg="navyblue")
        title_lb1.place(x=0,y=0,width=1366,height=45)

        # Create buttons below the section 
        # ------------------------------------------------------------------------------------------------------------------- 
        # Training button 1
        std_img_btn=Image.open(r".\Images_GUI\t_btn1.png")
        std_img_btn=std_img_btn.resize((180,180),Image.LANCZOS)
        self.std_img1=ImageTk.PhotoImage(std_img_btn)

        std_b1 = Button(bg_img,command=self.train_classifier,image=self.std_img1,cursor="hand2")
        std_b1.place(x=600,y=170,width=180,height=180)

        std_b1_1 = Button(bg_img,command=self.train_classifier,text="Train Dataset",cursor="hand2",font=("tahoma",15,"bold"),bg="white",fg="navyblue")
        std_b1_1.place(x=600,y=350,width=180,height=45)

    # ==================Create Function of Traing===================
    def train_classifier(self):
        data_dir=("data_img")
        # Kiểm tra xem thư mục có tồn tại không
        if not os.path.exists(data_dir):
            messagebox.showerror("Error","Dataset folder not found!", parent=self.root)
            return

        # Kiểm tra xem có ảnh trong thư mục không
        path=[os.path.join(data_dir,file) for file in os.listdir(data_dir)]
        if len(path) == 0:
            messagebox.showerror("Error","No images found in dataset folder!", parent=self.root)
            return

        faces=[]
        ids=[]
        
        print("Training started...")
        print(f"Found {len(path)} images")

        for image in path:
            try:
                # Debug: In ra tên file đang xử lý
                print(f"Processing image: {image}")
                
                img=Image.open(image).convert('L')
                imageNp=np.array(img,'uint8')
                
                # Lấy ID từ tên file và kiểm tra tính hợp lệ
                id=int(os.path.split(image)[1].split('.')[1])
                print(f"Extracted ID: {id}")

                faces.append(imageNp)
                ids.append(id)

                cv2.imshow("Training",imageNp)
                cv2.waitKey(1)

            except Exception as e:
                print(f"Error processing image {image}: {str(e)}")
                continue

        ids=np.array(ids)

        print(f"Total faces: {len(faces)}")
        print(f"Unique IDs: {np.unique(ids)}")

        # Tạo và train classifier
        try:
            clf= cv2.face.LBPHFaceRecognizer_create()
            clf.train(faces,ids)
            
            # Lưu file với đường dẫn đầy đủ
            clf_path = "clf.xml"
            clf.write(clf_path)
            print(f"Training file saved to: {clf_path}")
            
            cv2.destroyAllWindows()
            messagebox.showinfo("Success","Training Dataset Completed Successfully!", parent=self.root)
            
        except Exception as e:
            cv2.destroyAllWindows()
            messagebox.showerror("Error",f"Error during training: {str(e)}", parent=self.root)




if __name__ == "__main__":
    root=Tk()
    obj=Train(root)
    root.mainloop()