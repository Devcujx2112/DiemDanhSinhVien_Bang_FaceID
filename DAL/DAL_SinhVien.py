import mysql.connector as db
from . import DAL_Connect

def ShowAllSinhVien():
    try:
        conn = DAL_Connect.connect_db()
        query = "SELECT * FROM tbl_sinhvien"
        cs = conn.cursor()
        cs.execute(query)
        result = cs.fetchall()  
        return result
    except Exception as e:
        print(f"Error: {e}")  
        return [] 
    finally:
        conn.close() 

def AddSinhVien(masv,tensv,gioiTinh,khoa,diaChi,face):
    try:
        conn = DAL_Connect.connect_db()
        cs = conn.cursor()
        new_sinhVien = (masv,tensv,gioiTinh,khoa,diaChi,face)
        query = "INSERT INTO tbl_sinhvien(masv,tensv,gioiTinh,khoa,diaChi,face) VALUES (%s,%s,%s,%s,%s,%s)"
        cs.execute(query,new_sinhVien)
        conn.commit()
        conn.close()
        return cs.rowcount
    except Exception as e:
        print(f"Error: {e}")
        
def UpdateSinhVien(masv,tensv,gioiTinh,khoa,diaChi,face):
    try:
        conn = DAL_Connect.connect_db()
        cs = conn.cursor()
        new_sinhVien = (tensv,gioiTinh,khoa,diaChi,face,masv)
        query = "UPDATE tbl_sinhvien SET tensv = %s, gioiTinh = %s, khoa = %s, diaChi = %s, face = %s WHERE masv = %s"
        cs.execute(query,new_sinhVien)
        conn.commit()
        conn.close()
        return cs.rowcount
    except Exception as e:
        print(f"Error: {e}")
        
        
def DeleteSinhVien(masv):
    try:
        conn = DAL_Connect.connect_db()
        cs = conn.cursor()
        query = "DELETE FROM tbl_sinhvien WHERE masv = %s"
        cs.execute(query,(masv,))
        conn.commit()
        conn.close()
        return cs.rowcount
    except Exception as e:
        print(f"Error: {e}")
        
def SearchSinhVien(tensv):
    conn = DAL_Connect.connect_db()
    qr = "SELECT * FROM tbl_sinhvien WHERE tensv LIKE '%"+tensv+"%'"
    cs = conn.cursor()
    cs.execute(qr)
    rs = cs.fetchall()
    conn.close()
    return rs