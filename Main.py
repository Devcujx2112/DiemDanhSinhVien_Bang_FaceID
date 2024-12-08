import ip
import os
import openpyxl
from PyQt6.QtWidgets import *
from uiform import Ui_MainWindow
from login import Ui_MainLogin
import cv2
import face_recognition
import json
import numpy as np
import pandas as pd

#__________________________________________________________________________
#Login
class MainLogin(QMainWindow,Ui_MainLogin):
    def __init__(self):
        super(MainLogin,self).__init__()
        self.setupUi(self)
        self.btn_login.clicked.connect(self.loginApp)

    def loginApp(self):
        username = self.txt_userName.text()
        password = self.txt_passWord.text()

        login = ip.DAL_Connect.loginApp(username,password)

        if login:   
            role = ip.DAL_Connect.role(username,password)
            current_user = {'username': username, 'role': role}

            self.main_window = MyWindow(current_user)

            widget.removeWidget(self)

            widget.addWidget(self.main_window)
            widget.setCurrentIndex(1)   
            self.deleteLater()

            self.main_window.show()
        else:
            ip.QMessageBox.information(self,"Thông báo","Sai tài khoản hoặc mật khẩu")
        

#__________________________________________________________________________
#Trang chủ quản lý sinh viên

class MyWindow(QMainWindow,Ui_MainWindow):
    def __init__(self, current_user=None):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Quản lý sinh viên")
        self.icon_name_widget.setHidden(True)

        self.current_user = current_user if current_user is not None else {}

        print("Current user:", self.current_user)  
        role = self.current_user.get('role', ('0',))[0]  # Lấy phần tử đầu tiên của tuple

        self.stackedWidget.setCurrentIndex (0)

        if int(role) == 1:
            self.giangVien_1.setEnabled(True)
            self.giangVien_2.setEnabled(True)
            self.role_app.setText("   Admin   ")
        else:
            self.giangVien_1.setEnabled(False)
            self.giangVien_2.setEnabled(False)
            self.role_app.setText("Giang Vien")


#__________________________________________________________________________
#Button chuyen trang

        self.sinhVien_1.clicked.connect(self.switch_to_sinhVien_page)
        self.sinhVien_2.clicked.connect(self.switch_to_sinhVien_page)

        self.giangVien_1.clicked.connect(self.switch_to_giangVien_page)
        self.giangVien_2.clicked.connect(self.switch_to_giangVien_page)

        self.lopHoc_1.clicked.connect(self.switch_to_lopHoc_page)   
        self.lopHoc_2.clicked.connect(self.switch_to_lopHoc_page)

        self.quanLyLopHoc_1.clicked.connect(self.switch_to_quanLyLopHoc_page)   
        self.quanLyLopHoc_2.clicked.connect(self.switch_to_quanLyLopHoc_page)

        self.diemDanh_1.clicked.connect(self.switch_to_diemDanh_page)
        self.diemDanh_2.clicked.connect(self.switch_to_diemDanh_page)

        self.dangXuat_1.clicked.connect(self.switch_to_DangXuatPage) 
        self.dangXuat_2.clicked.connect(self.switch_to_DangXuatPage)

#__________________________________________________________________________
#Funtion sinh vien  
        self.ShowAllSinhVien()
        self.btn_addFace.clicked.connect(self.AddFaceID)
        self.tbl_sinhVien.cellClicked.connect(self.tbl_sinhVien_Clicked)
        self.btn_themSV.clicked.connect(self.AddSinhVien)
        self.btn_suaSV.clicked.connect(self.UpdateSinhVien)
        self.btn_xoaSV.clicked.connect(self.DeleteSinhVien)
        self.btn_timKiemSV.clicked.connect(self.SearchSinhVien)
        
#__________________________________________________________________________
#Funtion giang vien 
        self.ShowAllGiangVien()
        self.tbl_giangVien.cellClicked.connect(self.ClickGiangVien)
        self.btn_themGV.clicked.connect(self.AddGiangVien)
        self.btn_suaGV.clicked.connect(self.UpdateGiangVien)
        self.btn_xoaGV.clicked.connect(self.DeleteGiangVien)
        self.btn_timKiemGV.clicked.connect(self.SearchGiangVien)


#__________________________________________________________________________
#Funtion lop hoc
        self.ShowAllLopHoc()
        self.tbl_lopHoc.cellClicked.connect(self.OneClickLopHoc)
        self.btn_themLopHoc.clicked.connect(self.AddLopHoc)
        self.btn_suaLopHoc.clicked.connect(self.UpdateLopHoc)
        self.btn_xoaLopHoc.clicked.connect(self.DeleteLopHoc)
        self.btn_timKiemLH.clicked.connect(self.SearchLopHoc)


#__________________________________________________________________________
#Funtion quan ly lop hoc
        self.btn_danhSachSinhVien.clicked.connect(self.ShowAllSinhVienQL)
        self.tbl_sinhVienQL.cellClicked.connect(self.OneClickSinhVienQL)
        self.btn_addDS.clicked.connect(self.AddSinhVienInLopHoc)
        self.btn_danhSachLop.clicked.connect(self.DanhSachSinhVienInClass)
        self.btn_xoaDS.clicked.connect(self.DeleteSinhVienInClass)


#__________________________________________________________________________
#Funtion diem danh
        self.btn_danhSachDD.clicked.connect(self.ShowAllSinhVienDD)
        self.tbl_danhSachDD.cellClicked.connect(self.OneClickSinhVienDD)
        self.btn_xacThucKhuonMat.clicked.connect(self.XacThucFaceIDSinhVien)
        self.btn_diemDanh.clicked.connect(self.DiemDanhSinhVien)
        self.btn_excel.clicked.connect(self.XuatFileExcel)
#__________________________________________________________________________
#funtion chuyen trang

    def switch_to_sinhVien_page(self):
        self.stackedWidget.setCurrentIndex (0)
    def switch_to_giangVien_page(self):
        self.stackedWidget.setCurrentIndex (1)  
    def switch_to_lopHoc_page(self):
        self.stackedWidget.setCurrentIndex (2)
        self.UpdateComboBoxGiangVien()

    def switch_to_quanLyLopHoc_page(self):
        self.ShowAllLopHocInComBoBox()
        self.stackedWidget.setCurrentIndex (3)
    def switch_to_diemDanh_page(self):
        self.ShowAllLopHocInComBoBoxDD()
        self.stackedWidget.setCurrentIndex (4)
    def switch_to_DangXuatPage(self):
        reply = ip.QMessageBox.question(self, 'Xác nhận', 
                                   "Bạn có muốn đăng xuất không?", 
                                   ip.QMessageBox.StandardButton.Yes | ip.QMessageBox.StandardButton.No, 
                                   ip.QMessageBox.StandardButton.No)

        if reply == ip.QMessageBox.StandardButton.Yes:
            print("Đang xuất...")
            self.deleteLater()
            self.current_user = {}  
            widget.setCurrentIndex(0)  
            widget.setFixedHeight(5)
            widget.setFixedWidth(5)
            widget.move(250, 100)

            print("Đăng xuất thành công! Quay về trang đăng nhập.")
        else:
            print("Hủy đăng xuất")



#__________________________________________________________________________
#Quan ly sinh vien

#Show All Sinh Vien
    def ShowAllSinhVien(self):
        self.tbl_sinhVien.setRowCount(ip.DAL_SinhVien.ShowAllSinhVien().__len__())
        self.tbl_sinhVien.setColumnCount(6)
        self.tbl_sinhVien.setHorizontalHeaderLabels(["Mã sinh viên", "Họ và tên","Giới tính", "Khoa", "Địa chỉ", "FaceID"]) 
        self.tbl_sinhVien.setColumnWidth(1, 150)
        self.tbl_sinhVien.setColumnWidth(5, 150)
        table_row = 0
    
        for row in ip.DAL_SinhVien.ShowAllSinhVien():
            self.tbl_sinhVien.setItem(table_row, 0, ip.QTableWidgetItem(str(row[0])))
            self.tbl_sinhVien.setItem(table_row, 1, ip.QTableWidgetItem(str(row[1])))
            self.tbl_sinhVien.setItem(table_row, 2, ip.QTableWidgetItem(str(row[2])))
            self.tbl_sinhVien.setItem(table_row, 3, ip.QTableWidgetItem(str(row[3])))
            self.tbl_sinhVien.setItem(table_row, 4, ip.QTableWidgetItem(str(row[4])))
            self.tbl_sinhVien.setItem(table_row, 5, ip.QTableWidgetItem(str(row[5])))
            table_row += 1

#Function add FaceID
    def AddFaceID(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            QMessageBox.warning(self, "Lỗi", "Không thể mở camera!")
            return

        face_saved = False  # Biến kiểm tra khi đã lưu mã hóa khuôn mặt

        while True:
            ret, frame = cap.read()
            if not ret:
                QMessageBox.warning(self, "Lỗi", "Không thể đọc khung hình từ camera!")
                break
        
            # Chuyển đổi khung hình sang định dạng RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Nhận diện khuôn mặt
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for face_location, face_encoding in zip(face_locations, face_encodings):
                top, right, bottom, left = face_location
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                # Chuyển mã hóa khuôn mặt thành chuỗi JSON
                encoding_str = json.dumps(face_encoding.tolist())

                self.txt_faceCoding.setText(encoding_str) 

                QMessageBox.information(self, "Thông báo", "Mã hóa khuôn mặt đã được lưu!")

                face_saved = True
                break

            if face_saved:
                break

            # Hiển thị khung hình
            cv2.imshow("Face Recognition", frame)

            # Nhấn 'q' để thoát
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Đóng camera và cửa sổ hiển thị
        cap.release()
        cv2.destroyAllWindows()
        
#Function One Click
    def tbl_sinhVien_Clicked(self, row, column):
        self.txt_masvSV.setText(self.tbl_sinhVien.item(row, 0).text())
        self.txt_tensvSV.setText(self.tbl_sinhVien.item(row, 1).text())
        gender = self.tbl_sinhVien.item(row, 2).text().strip().lower()
        index = -1
        if gender == "nam":
            index = 0 
        elif gender == "nữ":
            index = 1 
        if index != -1:
            self.ccb_genderSV.setCurrentIndex(index)
        self.txt_khoaSV.setText(self.tbl_sinhVien.item(row, 3).text())
        self.txt_diaChiSV.setText(self.tbl_sinhVien.item(row, 4).text())
        self.txt_faceCoding.setText(self.tbl_sinhVien.item(row, 5).text())

#Funtion Add Sinh Vien
    def AddSinhVien(self):
        masv = self.txt_masvSV.text()
        tensv = self.txt_tensvSV.text()
        gender = self.ccb_genderSV.currentText()
        khoa = self.txt_khoaSV.text()
        diachi = self.txt_diaChiSV.text()
        facecoding = self.txt_faceCoding.text()
        kt = ip.DAL_SinhVien.AddSinhVien(masv,tensv,gender,khoa,diachi,facecoding)

        if not masv or not tensv or not gender or not khoa or not diachi or not facecoding:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        if kt == 1:
            QMessageBox.information(self, "Thông báo", "Thêm sinh viên thành công")
            self.ShowAllSinhVien()
            self.txt_masvSV.setText("")
            self.txt_tensvSV.setText("")
            self.ccb_genderSV.setCurrentText("")
            self.txt_khoaSV.setText("")
            self.txt_diaChiSV.setText("")
            self.txt_faceCoding.setText("")

        else:
            QMessageBox.information(self, "Thông báo", "Thêm sinh viên thất bại")
                   
#Funtion Update Sinh Vien
    def UpdateSinhVien(self):
        masv = self.txt_masvSV.text()
        tensv = self.txt_tensvSV.text()
        gender = self.ccb_genderSV.currentText()
        khoa = self.txt_khoaSV.text()
        diachi = self.txt_diaChiSV.text()
        facecoding = self.txt_faceCoding.text()
        kt = ip.DAL_SinhVien.UpdateSinhVien(masv,tensv,gender,khoa,diachi,facecoding)
        if kt == 1:
            QMessageBox.information(self, "Thông báo", "Cập nhật thông tin sinh viên thành công")
            self.ShowAllSinhVien()
        else:
            QMessageBox.information(self, "Thông báo", "Cập nhật thông tin sinh viên thất bại")
                        
#Funtion Delete Sinh Vien
    def DeleteSinhVien(self):
        masv = self.txt_masvSV.text()
        kt = ip.DAL_SinhVien.DeleteSinhVien(masv)
        if kt == 1:
            QMessageBox.information(self, "Thông báo", "Xóa sinh viên thành công")
            self.ShowAllSinhVien()
            self.txt_masvSV.setText("")
            self.txt_tensvSV.setText("")
            self.ccb_genderSV.setCurrentIndex(-1)
            self.txt_khoaSV.setText("")
            self.txt_diaChiSV.setText("")
            self.txt_faceCoding.setText("")
        else:
            QMessageBox.information(self, "Thông báo", "Xóa sinh viên thất bại")
                     
#Funtion Search Sinh Vien
    def SearchSinhVien(self):
        tensv = self.txt_timKiemSV.text()
        self.tbl_sinhVien.setRowCount(ip.DAL_SinhVien.SearchSinhVien(tensv).__len__())
        self.tbl_sinhVien.setColumnCount(6)
        self.tbl_sinhVien.setHorizontalHeaderLabels(["Mã sinh viên", "Họ và tên","Giới tính", "Khoa", "Địa chi", "FaceID"])
        self.tbl_sinhVien.setColumnWidth(1, 150)
        self.tbl_sinhVien.setColumnWidth(5, 150)
        table_row = 0

        for row in ip.DAL_SinhVien.SearchSinhVien(tensv):
            self.tbl_sinhVien.setItem(table_row, 0, ip.QTableWidgetItem(row[0]))
            self.tbl_sinhVien.setItem(table_row, 1, ip.QTableWidgetItem(row[1]))
            self.tbl_sinhVien.setItem(table_row, 2, ip.QTableWidgetItem(row[2]))
            self.tbl_sinhVien.setItem(table_row, 3, ip.QTableWidgetItem(row[3]))    
            self.tbl_sinhVien.setItem(table_row, 4, ip.QTableWidgetItem(row[4]))
            self.tbl_sinhVien.setItem(table_row, 5, ip.QTableWidgetItem(row[5]))
            table_row += 1

#__________________________________________________________________________
#Quan Ly Giang Vien 

#Show ALl Giang Vien
    def ShowAllGiangVien(self):
        self.tbl_giangVien.setRowCount(ip.DAL_GiangVien.ShowAllGiangVien().__len__())
        self.tbl_giangVien.setColumnCount(9)
        self.tbl_giangVien.setHorizontalHeaderLabels(["Mã giảng viên", "Tên giảng viên", "Username", "Password", "Giới tính","Địa chỉ","Số điện thoại","Email","role"]) 
        self.tbl_giangVien.setColumnWidth(1, 150)
        self.tbl_giangVien.setColumnWidth(8, 150)
        table_row = 0

        for row in ip.DAL_GiangVien.ShowAllGiangVien():
            self.tbl_giangVien.setItem(table_row, 0, ip.QTableWidgetItem(str(row[0])))
            self.tbl_giangVien.setItem(table_row, 1, ip.QTableWidgetItem(str(row[1])))
            self.tbl_giangVien.setItem(table_row, 2, ip.QTableWidgetItem(str(row[2])))
            self.tbl_giangVien.setItem(table_row, 3, ip.QTableWidgetItem(str(row[3])))
            self.tbl_giangVien.setItem(table_row, 4, ip.QTableWidgetItem(str(row[4])))
            self.tbl_giangVien.setItem(table_row, 5, ip.QTableWidgetItem(str(row[5])))
            self.tbl_giangVien.setItem(table_row, 6, ip.QTableWidgetItem(str(row[6])))
            self.tbl_giangVien.setItem(table_row, 7, ip.QTableWidgetItem(str(row[7])))
            self.tbl_giangVien.setItem(table_row, 8, ip.QTableWidgetItem(str(row[8])))
            table_row += 1

#Funtion Click Giang Vien
    def ClickGiangVien(self, row, column):
        self.txt_magv.setText(self.tbl_giangVien.item(row, 0).text())  
        self.txt_tengv.setText(self.tbl_giangVien.item(row, 1).text())     
        self.username.setText(self.tbl_giangVien.item(row, 2).text())  
        self.password.setText(self.tbl_giangVien.item(row, 3).text())   
        gender = self.tbl_giangVien.item(row, 4).text().strip().lower()  
        index = -1
        if gender == "nam":  
            index = 0
        elif gender == "nữ":
            index = 1
        elif gender == "khác":
            index = 2
        if index != -1:
            self.ccb_genderGV.setCurrentIndex(index)
        self.txt_diaChiGV.setText(self.tbl_giangVien.item(row, 5).text())  
        self.txt_sdtGV.setText(self.tbl_giangVien.item(row, 6).text())    
        self.txt_emailGV.setText(self.tbl_giangVien.item(row, 7).text())  

#Funtion Add Giang Vien
    def AddGiangVien(self):
        magv = self.txt_magv.text()
        tengv = self.txt_tengv.text()
        username = self.username.text()
        password = self.password.text()
        gender = self.ccb_genderGV.currentText()
        diachi = self.txt_diaChiGV.text()
        sdt = self.txt_sdtGV.text()
        email = self.txt_emailGV.text()
        role = "0"
        
        if not magv or not tengv or not username or not password or not gender or not diachi or not sdt or not email:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        kt = ip.DAL_GiangVien.AddGiangVien(magv, tengv, username, password, gender, diachi, sdt, email, role)
        if kt == 1:
            QMessageBox.information(self, "Thông báo", "Thêm giảng viên thành công")
            self.ShowAllGiangVien()
            self.txt_magv.setText("")
            self.txt_tengv.setText("")
            self.username.setText("")
            self.password.setText("")
            self.ccb_genderGV.setCurrentText("")
            self.txt_sdtGV.setText("")
            self.txt_emailGV.setText("")
        else:
            QMessageBox.information(self, "Thông báo", "Thêm giảng viên thất bại")

#Funtion Update Giang Vien
    def UpdateGiangVien(self):
        magv = self.txt_magv.text()
        tengv = self.txt_tengv.text()
        username = self.username.text()
        password = self.password.text()
        gender = self.ccb_genderGV.currentText()
        diachi = self.txt_diaChiGV.text()
        sdt = self.txt_sdtGV.text()
        email = self.txt_emailGV.text()
        role = "0"
        
        if not magv or not tengv or not username or not password or not gender or not diachi or not sdt or not email:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập đầy đủ thông tin!")
            return

        kt = ip.DAL_GiangVien.UpdateGiangVien(magv, tengv, username, password, gender, diachi, sdt, email, role)
        if kt == 1:
            QMessageBox.information(self, "Thông báo", "Cập nhật giảng viên thành công")
            self.ShowAllGiangVien()
        else:
            QMessageBox.information(self, "Thông báo", "Cập nhật giảng viên thất bại")

#Funtion Delete Giang Vien
    def DeleteGiangVien(self):
        magv = self.txt_magv.text()
        kt = ip.DAL_GiangVien.DeleteGiangVien(magv)
        if kt == 1:
            QMessageBox.information(self, "Thông báo", "Xoá giảng viên thành công")
            self.ShowAllGiangVien()
            self.txt_magv.setText("")
            self.txt_tengv.setText("")
            self.username.setText("")
            self.password.setText("")
            self.ccb_genderGV.setCurrentIndex(-1)
            self.txt_diaChiGV.setText("")
            self.txt_sdtGV.setText("")
            self.txt_emailGV.setText("")
        else:
            QMessageBox.information(self, "Thông báo", "Xoá giảng viên thất bại")

#Funtion Search Giang Vien
    def SearchGiangVien(self):
        tengv = self.txt_timKiemGV.text()
        self.tbl_giangVien.setRowCount(ip.DAL_GiangVien.SearchGiangVien(tengv).__len__())
        self.tbl_giangVien.setColumnCount(9)
        self.tbl_giangVien.setHorizontalHeaderLabels(["Mã giảng viên", "Ten giảng viên", "Username", "Password", "Giới tính","Địa chi","Số điện thoại","Email","role"]) 
        self.tbl_giangVien.setColumnWidth(1, 150)
        self.tbl_giangVien.setColumnWidth(8, 150)
        table_row = 0

        for row in ip.DAL_GiangVien.SearchGiangVien(tengv):
            self.tbl_giangVien.setItem(table_row, 0, ip.QTableWidgetItem(str(row[0])))
            self.tbl_giangVien.setItem(table_row, 1, ip.QTableWidgetItem(str(row[1])))
            self.tbl_giangVien.setItem(table_row, 2, ip.QTableWidgetItem(str(row[2])))
            self.tbl_giangVien.setItem(table_row, 3, ip.QTableWidgetItem(str(row[3])))
            self.tbl_giangVien.setItem(table_row, 4, ip.QTableWidgetItem(str(row[4]))) 
            self.tbl_giangVien.setItem(table_row, 5, ip.QTableWidgetItem(str(row[5])))
            self.tbl_giangVien.setItem(table_row, 6, ip.QTableWidgetItem(str(row[6])))
            self.tbl_giangVien.setItem(table_row, 7, ip.QTableWidgetItem(str(row[7])))
            self.tbl_giangVien.setItem(table_row, 8, ip.QTableWidgetItem(str(row[8])))
            table_row += 1


#__________________________________________________________________________
#Quan ly lop hoc  
#Funtion Show All lop hoc  
    def ShowAllLopHoc(self):
        self.ccb_giangVien.clear()
        for i in range(ip.DAL_GiangVien.ShowAllGiangVien().__len__()):
            self.ccb_giangVien.addItem(str(ip.DAL_GiangVien.ShowAllGiangVien()[i][1]))
        self.tbl_lopHoc.setRowCount(ip.DAL_LopHoc.ShowAllLopHoc().__len__())
        self.tbl_lopHoc.setColumnCount(4)
        self.tbl_lopHoc.setHorizontalHeaderLabels(["Mã lớp", "Giảng viên quản lý","Tên lớp học", "Số tín chỉ"]) 
        self.tbl_lopHoc.setColumnWidth(1, 200)
        self.tbl_lopHoc.setColumnWidth(2, 200)
        self.tbl_lopHoc.setColumnWidth(3, 150)
        table_row = 0

        for row in ip.DAL_LopHoc.ShowAllLopHoc():
            self.tbl_lopHoc.setItem(table_row, 0, ip.QTableWidgetItem(str(row[0])))
            self.tbl_lopHoc.setItem(table_row, 1, ip.QTableWidgetItem(str(row[1])))
            self.tbl_lopHoc.setItem(table_row, 2, ip.QTableWidgetItem(str(row[2])))
            self.tbl_lopHoc.setItem(table_row, 3, ip.QTableWidgetItem(str(row[3])))
            table_row += 1

#Funtion Update data giangVien
    def UpdateComboBoxGiangVien(self):
        self.ccb_giangVien.clear()
        for giangvien in ip.DAL_GiangVien.ShowAllGiangVien():
            self.ccb_giangVien.addItem(str(giangvien[1]))

#Funtion One Click Lop Hoc
    def OneClickLopHoc(self):
        row = self.tbl_lopHoc.currentRow()
        self.txt_maLop.setText(self.tbl_lopHoc.item(row, 0).text())
        magv = self.tbl_lopHoc.item(row, 1).text().strip()
        for i in range(self.ccb_giangVien.count()):
            if magv == self.ccb_giangVien.itemText(i).strip():
                self.ccb_giangVien.setCurrentIndex(i)
        self.txt_tenlopHoc.setText(self.tbl_lopHoc.item(row, 2).text())
        self.txt_soTin.setText(self.tbl_lopHoc.item(row, 3).text())

#Funtion Add Lop Hoc
    def AddLopHoc(self):
        malop = self.txt_maLop.text()   
        magv = self.ccb_giangVien.currentText()
        tenlop = self.txt_tenlopHoc.text()
        soTin = self.txt_soTin.text()

        if not malop or not magv or not tenlop or not soTin:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập đầy đủ thông tin!")
            return

        kt = ip.DAL_LopHoc.AddLopHoc(malop,magv,tenlop,soTin)
        if kt == 1:
            QMessageBox.information(self, "Thông báo", "Thêm lớp học thành công")
            self.ShowAllLopHoc()
            self.txt_maLop.setText("")
            self.txt_tenlopHoc.setText("")
            self.txt_soTin.setText("")
        else:
            QMessageBox.information(self, "Thông báo", "Thêm lớp học thất bại")

#Funtion Update Lop Hoc
    def UpdateLopHoc(self):
        malop = self.txt_maLop.text().strip()
        magv = self.ccb_giangVien.currentText().strip()
        tenlop = self.txt_tenlopHoc.text().strip()
        soTin = self.txt_soTin.text().strip()

        if not malop or not magv or not tenlop or not soTin:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập đầy đủ thông tin!")
            return

        try:
            soTin = int(soTin)
        except ValueError:
            QMessageBox.warning(self, "Thông báo", "Số tín chỉ phải là một số nguyên!")
            return

        kt = ip.DAL_LopHoc.UpdateLopHoc(magv,tenlop,soTin,malop)
        if kt == 1:
            QMessageBox.information(self, "Thông báo", "Cập nhật lớp học thành công")
            self.ShowAllLopHoc()
        else:
            QMessageBox.warning(self, "Thông báo", "Cập nhật lớp học thất bại")


#Funtion Delete Lop Hoc
    def DeleteLopHoc(self):
        malop = self.txt_maLop.text()

        kt = ip.DAL_LopHoc.DeleteLopHoc(malop)
        if kt == 1:
            QMessageBox.information(self, "Thông báo", "Xóa lớp học thành công")
            self.ShowAllLopHoc()
            self.txt_maLop.setText("")
            self.txt_tenlopHoc.setText("")
            self.txt_soTin.setText("")
        else:
            QMessageBox.information(self, "Thông báo", "Xóa lớp học thất bại")

#Funtion Search Lop Hoc
    def SearchLopHoc(self):
        tenLH = self.txt_timKiemLH.text()
        self.tbl_lopHoc.setRowCount(ip.DAL_LopHoc.SearchLopHoc(tenLH).__len__())
        self.tbl_lopHoc.setColumnCount(4)
        self.tbl_lopHoc.setHorizontalHeaderLabels(["Mã lớp", "Giảng viên quản lý","Tên lớp học", "Số tín chỉ"]) 
        self.tbl_lopHoc.setColumnWidth(1, 200)
        self.tbl_lopHoc.setColumnWidth(2, 200)
        self.tbl_lopHoc.setColumnWidth(3, 150)
        table_row = 0

        for row in ip.DAL_LopHoc.SearchLopHoc(tenLH):
            self.tbl_lopHoc.setItem(table_row, 0, ip.QTableWidgetItem(str(row[0])))
            self.tbl_lopHoc.setItem(table_row, 1, ip.QTableWidgetItem(str(row[1])))
            self.tbl_lopHoc.setItem(table_row, 2, ip.QTableWidgetItem(str(row[2])))
            self.tbl_lopHoc.setItem(table_row, 3, ip.QTableWidgetItem(str(row[3])))
            table_row += 1


#__________________________________________________________________________
#Quan ly lop hoc    

#Show All Combobox 
    def ShowAllLopHocInComBoBox(self):
        self.ccb_lopHocQL.clear()
        self.txt_giangVienQL.clear()

        self.lopHocData = ip.DAL_LopHoc.ShowAllLopHoc()

        for lopHoc in self.lopHocData:
            self.ccb_lopHocQL.addItem(str(lopHoc[2])) 

        self.ccb_lopHocQL.currentIndexChanged.connect(self.updateGiangVienQL)

    def updateGiangVienQL(self):
        index = self.ccb_lopHocQL.currentIndex()

        if index >= 0 and index < len(self.lopHocData):
            self.txt_giangVienQL.setText(str(self.lopHocData[index][1]))

#Click index All Sinh Vien
    def OneClickSinhVienQL(self,row,collum):
        self.txt_tenSinhVienQL.setText(self.tbl_sinhVienQL.item(row, 1).text())
        self.txt_masvQL.setText(self.tbl_sinhVienQL.item(row,0).text())

#Show All sinh vien 
    def ShowAllSinhVienQL(self):
        self.tbl_sinhVienQL.setRowCount(ip.DAL_SinhVien.ShowAllSinhVien().__len__())
        self.tbl_sinhVienQL.setColumnCount(6)
        self.tbl_sinhVienQL.setHorizontalHeaderLabels(["Mã sinh viên", "Họ và tên","Giới tính", "Khoa", "Địa chỉ", "FaceID"]) 
        self.tbl_sinhVienQL.setColumnWidth(1, 150)
        self.tbl_sinhVienQL.setColumnWidth(5, 150)
        table_row = 0
        for row in ip.DAL_SinhVien.ShowAllSinhVien():
            self.tbl_sinhVienQL.setItem(table_row, 0, ip.QTableWidgetItem(str(row[0])))
            self.tbl_sinhVienQL.setItem(table_row, 1, ip.QTableWidgetItem(str(row[1])))
            self.tbl_sinhVienQL.setItem(table_row, 2, ip.QTableWidgetItem(str(row[2])))
            self.tbl_sinhVienQL.setItem(table_row, 3, ip.QTableWidgetItem(str(row[3])))
            self.tbl_sinhVienQL.setItem(table_row, 4, ip.QTableWidgetItem(str(row[4])))
            self.tbl_sinhVienQL.setItem(table_row, 5, ip.QTableWidgetItem(str(row[5])))
            table_row += 1

#Add sinh vien vao lop hoc
    def AddSinhVienInLopHoc(self):
        tenlh = self.ccb_lopHocQL.currentText()
        gvql = self.txt_giangVienQL.text()
        tensv = self.txt_tenSinhVienQL.text()
        masv = self.txt_masvQL.text()

        if not tenlh or not gvql or not tensv or not masv:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập đầy đủ thông tin!")
            return

        kt = ip.DAL_QuanLyLopHoc.AddSinhVienInLopHoc(tenlh,gvql,tensv,masv)
        if kt == 1:
            QMessageBox.information(self, "Thông báo", "Thêm sinh viên vào lớp thành công")
            self.DanhSachSinhVienInClass()
            self.txt_tenSinhVienQL.setText("")
            self.txt_masvQL.setText("")
            ngay = "day"
            tinhtrang = "Nghỉ"
            kt = ip.DAL_DiemDanh.AddSinhVienDiemDanh(ngay,tenlh,gvql,masv,tensv,tinhtrang)

        else:
            QMessageBox.information(self, "Thông báo", "Thêm sinh viên vào lớp thất bại")  

#Danh sach lop hoc
    def DanhSachSinhVienInClass(self):
        tenlh = self.ccb_lopHocQL.currentText() 
        self.tbl_sinhVienQL.setRowCount(ip.DAL_QuanLyLopHoc.DanhSachSinhVienInLopHoc(tenlh).__len__())
        self.tbl_sinhVienQL.setColumnCount(2)
        self.tbl_sinhVienQL.setHorizontalHeaderLabels(["Mã sinh viên", "Tên sinh viên"]) 
        self.tbl_sinhVienQL.setColumnWidth(0, 200)
        self.tbl_sinhVienQL.setColumnWidth(1, 200)
     

        table_row = 0

        for row in ip.DAL_QuanLyLopHoc.DanhSachSinhVienInLopHoc(tenlh):
            self.tbl_sinhVienQL.setItem(table_row, 0, ip.QTableWidgetItem(str(row[4])))
            self.tbl_sinhVienQL.setItem(table_row, 1, ip.QTableWidgetItem(str(row[3])))
            table_row += 1

#Delete sinh vien in class
    def DeleteSinhVienInClass(self):
        masv = self.txt_masvQL.text()

        kt = ip.DAL_QuanLyLopHoc.DeleteSinhVienInClass(masv)
        if kt == 1:
            QMessageBox.information(self, "Thông báo", "Đã xóa sinh viên ra khỏi lớp học")
            self.DanhSachSinhVienInClass()
            self.txt_tenSinhVienQL.setText("")
            self.txt_masvQL.setText("")
            kt = ip.DAL_DiemDanh.DeleteSinhVienDiemDanh(masv)
        else:
            QMessageBox.information(self, "Thông báo", "Xóa sinh viên thất bại")


#__________________________________________________________________________
#Diem Danh Sinh Vien

#Update Combobox 
    def ShowAllLopHocInComBoBoxDD(self):
        self.ccb_lopHocDD.clear()
        self.txt_giangVienDD.clear()

        self.lopHocData = ip.DAL_LopHoc.ShowAllLopHoc()

        for lopHoc in self.lopHocData:
            self.ccb_lopHocDD.addItem(str(lopHoc[2])) 

        self.ccb_lopHocDD.currentIndexChanged.connect(self.updateGiangVienDD)

    def updateGiangVienDD(self):
        index = self.ccb_lopHocDD.currentIndex()

        if index >= 0 and index < len(self.lopHocData):
            self.txt_giangVienDD.setText(str(self.lopHocData[index][1]))

#Show All sinh vien diem danh
    def ShowAllSinhVienDD(self):
        tenlh = self.ccb_lopHocDD.currentText() 
        self.tbl_danhSachDD.setRowCount(ip.DAL_DiemDanh.ShowAllSinhVienDDInClass(tenlh).__len__())        
        self.tbl_danhSachDD.setColumnCount(6)
        self.tbl_danhSachDD.setHorizontalHeaderLabels(["Ngày", "Lớp học","Giảng viên", "Mã sinh viên", "Tên sinh viên", "Tình trạng"]) 
        self.tbl_danhSachDD.setColumnWidth(1, 70)
        self.tbl_danhSachDD.setColumnWidth(5, 150)
        table_row = 0
        for row in ip.DAL_DiemDanh.ShowAllSinhVienDDInClass(tenlh):
            self.tbl_danhSachDD.setItem(table_row, 0, ip.QTableWidgetItem(str(row[1])))
            self.tbl_danhSachDD.setItem(table_row, 1, ip.QTableWidgetItem(str(row[2])))
            self.tbl_danhSachDD.setItem(table_row, 2, ip.QTableWidgetItem(str(row[3])))
            self.tbl_danhSachDD.setItem(table_row, 3, ip.QTableWidgetItem(str(row[4])))
            self.tbl_danhSachDD.setItem(table_row, 4, ip.QTableWidgetItem(str(row[5])))
            self.tbl_danhSachDD.setItem(table_row, 5, ip.QTableWidgetItem(str(row[6])))
            table_row += 1

#Funtion One Click index table
    def OneClickSinhVienDD(self,row,collum):
        self.txt_ngayDD.setText(self.tbl_danhSachDD.item(row, 0).text())
        self.txt_masvDD.setText(self.tbl_danhSachDD.item(row,3).text())
        self.txt_tensvDD.setText(self.tbl_danhSachDD.item(row,4).text())
        tinhtrang = self.tbl_danhSachDD.item(row, 5).text().strip().lower()
        index = -1
        if tinhtrang == "có mặt":
            index = 0 
        elif tinhtrang == "đi muộn":
            index = 1 
        elif tinhtrang == "nghỉ":
            index = 2 
        if index != -1:
            self.ccb_tinhTrang.setCurrentIndex(index)
        

#Funtion xac thuc faceID
    def ReturnDataFaceID(self, new_face_encoding):
        try:
            masv = self.txt_masvDD.text()
            face_encodings = ip.DAL_DiemDanh.XacThucFaceIDSinhVien(masv)

            for masv, stored_encoding in face_encodings.items():
                # Kiểm tra độ chính xác với face_distance
                face_distance = face_recognition.face_distance([stored_encoding], new_face_encoding)[0]
                if face_distance < 0.3: 
                    return masv
            return None  

        except Exception as e:
            print(f"Lỗi khi so sánh khuôn mặt: {e}")
            return None


    def XacThucFaceIDSinhVien(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            QMessageBox.warning(self, "Lỗi", "Không thể mở camera!")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                QMessageBox.warning(self, "Lỗi", "Không thể đọc khung hình từ camera!")
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Nhận diện 
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for face_location, face_encoding in zip(face_locations, face_encodings):
                top, right, bottom, left = face_location
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                masv = self.ReturnDataFaceID(face_encoding)
                if masv:
                    QMessageBox.information(self, "Thông báo", f"Khuôn mặt khớp với sinh viên Mã SV: {masv}")
                    cap.release()
                    cv2.destroyAllWindows()
                    return
                else:
                    QMessageBox.warning(self, "Lỗi", "Không tìm thấy khuôn mặt khớp!")

        
            cv2.imshow("Face Authentication", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

#Funtion Diem danh sinh vien
    def DiemDanhSinhVien(self):
        day = self.txt_ngayDD.text()
        lophoc = self.ccb_lopHocDD.currentText()
        giangVien = self.txt_giangVienDD.text()
        masv = self.txt_masvDD.text()
        tensv = self.txt_tensvDD.text()
        tinhTrang = self.ccb_tinhTrang.currentText()

        if not day or not lophoc or not giangVien or not masv or not tensv or not tinhTrang:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập đầy đủ thông tin!")
            return

        kt = ip.DAL_DiemDanh.DiemDanhSinhVien(day,lophoc,giangVien,masv,tensv,tinhTrang)
        if kt == 1:
            QMessageBox.information(self, "Thông báo", "Đã lưu thông tin điểm danh")
            self.ShowAllSinhVienDD()
            self.txt_ngayDD.setText("")
            self.txt_masvDD.setText("")
            self.txt_tensvDD.setText("")
            self.ccb_tinhTrang.setCurrentText("")
        else:
            QMessageBox.warning(self, "Thông báo", "Điểm danh thất bại")


#Funtion xuat ra file Excel
    def XuatFileExcel(self):
        tenlophoc = self.ccb_lopHocDD.currentText() 
        ngay = self.txt_ngayDD.text()
        df = ip.DAL_DiemDanh.XuatExcel(tenlophoc) 
        ngay = ngay.replace('/', '_').replace('\\', '_').replace(':', '_')

        if not df.empty:
            file_path = 'DiemDanh_' + tenlophoc + ngay + '.xlsx' 
            df.to_excel(file_path, index=False)  
            QMessageBox.information(self, "Thông báo", f"File Excel đã được xuất ra: {file_path}")
        else:
            QMessageBox.warning(self, "Cảnh báo", "Không có dữ liệu để xuất.")
        ip.DAL_DiemDanh.SetTextTinhTrang()
        ip.DAL_DiemDanh.ShowAllSinhVienDDInClass(tenlophoc)
        
#__________________________________________________________________________
#Chuong trinh chay dau tien
app = ip.QApplication(ip.sys.argv)
widget = ip.QtWidgets.QStackedWidget()
login_f = MainLogin()
mainGui_f = MyWindow()
widget.addWidget(login_f)
widget.addWidget(mainGui_f)
widget.setCurrentIndex(0)
widget.setFixedHeight(800)
widget.setFixedWidth(860)
widget.show()
app.exec()
