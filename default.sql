	CREATE DATABASE face_recognition;
   USE face_recognition;
      CREATE TABLE student (
       Student_ID VARCHAR(20) PRIMARY KEY,
       Name VARCHAR(50) NOT NULL,
       Department VARCHAR(50) NOT NULL,
       Course VARCHAR(20) NOT NULL,
       Year VARCHAR(20) NOT NULL,
       Semester VARCHAR(20) NOT NULL,
       Division VARCHAR(20) NOT NULL,
       Gender VARCHAR(10) NOT NULL,
       DOB VARCHAR(20) NOT NULL,
       Mobile_No VARCHAR(15) NOT NULL,
       Address VARCHAR(100) NOT NULL,
       Roll_No VARCHAR(20) NOT NULL,
       Email VARCHAR(50) NOT NULL,
       Teacher_Name VARCHAR(50) NOT NULL,
       PhotoSample VARCHAR(5) NOT NULL
   );
      CREATE TABLE login (
       username VARCHAR(50) PRIMARY KEY,
       password VARCHAR(50) NOT NULL
   );
   
   -- Thêm tài khoản mặc định
   INSERT INTO login VALUES ('admin', 'admin');
   -- Sửa đổi bảng student để thêm cột lưu hình ảnh
ALTER TABLE student ADD COLUMN face_images LONGBLOB;


   -- Tạo bảng mới để lưu nhiều ảnh cho mỗi sinh viên
CREATE TABLE student_images (
  id INT AUTO_INCREMENT PRIMARY KEY,
  student_id VARCHAR(20),
  image_data LONGBLOB NOT NULL,
  image_number INT NOT NULL,
  FOREIGN KEY (student_id) REFERENCES student(Student_ID),
  INDEX (student_id, image_number)
);