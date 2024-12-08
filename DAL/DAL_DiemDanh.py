import mysql.connector as db
from . import DAL_Connect
import numpy as np
import json

def AddSinhVienDiemDanh(ngay,lophoc,giangvien,masv,tensv,tinhtrang):
    try:
        conn = DAL_Connect.connect_db()
        cs = conn.cursor()
        new_diemDanh = (ngay,lophoc,giangvien,masv,tensv,tinhtrang)
        query = "INSERT INTO tbl_diemdanh(ngay,lophoc,giangvien,masv,tensv,tinhtrang) VALUES (%s,%s,%s,%s,%s,%s)"
        cs.execute(query,new_diemDanh)
        conn.commit()
        conn.close()
        return cs.rowcount
    except Exception as e:
        print(f"Error: {e}")

def ShowAllSinhVienDDInClass(tenlh):
    try:
        conn = DAL_Connect.connect_db()
        query = "SELECT * FROM tbl_diemdanh WHERE lophoc LIKE '%"+tenlh+"%'"
        cs = conn.cursor()
        cs.execute(query)
        result = cs.fetchall()  
        return result
    except Exception as e:
        print(f"Error: {e}")  
        return [] 
    finally:
        conn.close() 

def XacThucFaceIDSinhVien(masv):
    try:
        conn = DAL_Connect.connect_db()
        cs = conn.cursor()

        query = "SELECT masv, face FROM tbl_sinhvien WHERE masv = %s"
        cs.execute(query, (masv,))
        
        face_encodings = {}
        for row in cs.fetchall():
            if len(row) == 2:  
                masv, faceID = row
                if faceID:
                    face_encodings[masv] = np.array(json.loads(faceID))
            else:
                print(f"Dữ liệu không hợp lệ: {row}")
        
        return face_encodings

    except Exception as e:
        print(f"Lỗi khi truy vấn dữ liệu FaceCoding: {e}")
        return {}

    finally:
        if conn.is_connected():
            cs.close()
            conn.close()


def DiemDanhSinhVien(ngay, lophoc, giangvien, masv, tensv, tinhtrang):
    try:
        conn = DAL_Connect.connect_db()
        cs = conn.cursor()

        cs.execute("SELECT id FROM tbl_diemdanh WHERE masv = %s", (masv,))
        ids = cs.fetchall()

        query = """
        UPDATE tbl_diemdanh
        SET ngay = %s, lophoc = %s, giangvien = %s, masv = %s, tensv = %s, tinhtrang = %s
        WHERE id = %s;
        """
        
        for id in ids:
            cs.execute(query, (ngay, lophoc, giangvien, masv, tensv, tinhtrang, id[0]))

        conn.commit()
        conn.close()

        return cs.rowcount 
    except Exception as e:
        print(f"Error: {e}")
        return 0

def SetTextTinhTrang():
    try:
        conn = DAL_Connect.connect_db() 
        cs = conn.cursor()  
        query = "UPDATE tbl_diemdanh SET tinhtrang = ' ', ngay = ' '"  
        cs.execute(query)  
        conn.commit() 
        conn.close() 
        print("Cập nhật thành công!")  
    except Exception as e:
        print(f"Error: {e}") 

import pandas as pd

def XuatExcel(tenlh):
    try:
        conn = DAL_Connect.connect_db()
        query = "SELECT * FROM tbl_diemdanh WHERE lophoc LIKE %s"
        cs = conn.cursor()
        cs.execute(query, ('%' + tenlh + '%',))
        result = cs.fetchall()
        
        columns = [desc[0] for desc in cs.description]  # Lấy tên cột từ kết quả query
        df = pd.DataFrame(result, columns=columns)
        
        return df
    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

def DeleteSinhVienDiemDanh(masv):
    try:    
        conn = DAL_Connect.connect_db()
        cs = conn.cursor()
        query = "DELETE FROM tbl_diemdanh WHERE masv = %s"
        cs.execute(query,(masv,))
        conn.commit()
        conn.close()
        return cs.rowcount
    except Exception as e:
        print(f"Error: {e}")    