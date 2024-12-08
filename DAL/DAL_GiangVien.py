import mysql.connector as db
from . import DAL_Connect

def ShowAllGiangVien():
    try:
        conn = DAL_Connect.connect_db()
        query = "SELECT * FROM tbl_giangvien"
        cs = conn.cursor()
        cs.execute(query)
        result = cs.fetchall()  
        return result
    except Exception as e:
        print(f"Error: {e}")  
        return [] 
    finally:
        conn.close() 
        
        
def AddGiangVien(magv,tengv,userName,password,gioiTinh,diaChi,SoDienThoai,email,role):
    try:
        conn = DAL_Connect.connect_db()
        cs = conn.cursor()
        new_giangVien = (magv,tengv,userName,password,gioiTinh,diaChi,SoDienThoai,email,role)
        query = "INSERT INTO tbl_giangvien(magv,tengv,userName,password,gioiTinh,diaChi,SoDienThoai,email,role) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cs.execute(query,new_giangVien)
        conn.commit()
        conn.close()
        return cs.rowcount
    except Exception as e:
        print(f"Error: {e}")
        
        
def UpdateGiangVien(magv,tengv,userName,password,gioiTinh,diaChi,SoDienThoai,email,role):
    try:
        conn = DAL_Connect.connect_db()
        cs = conn.cursor()
        new_giangVien = (tengv,userName,password,gioiTinh,diaChi,SoDienThoai,email,role,magv)
        query = "UPDATE tbl_giangvien SET tengv = %s, userName = %s, password = %s, gioiTinh = %s, diaChi = %s, SoDienThoai = %s, email = %s, role = %s WHERE magv = %s"
        cs.execute(query,new_giangVien)
        conn.commit()
        conn.close()
        return cs.rowcount
    except Exception as e:
        print(f"Error: {e}")
        
def DeleteGiangVien(magv):
    try:
        conn = DAL_Connect.connect_db()
        cs = conn.cursor()
        query = "DELETE FROM tbl_giangvien WHERE magv = %s"
        cs.execute(query,(magv,))
        conn.commit()
        conn.close()
        return cs.rowcount
    except Exception as e:
        print(f"Error: {e}")
        
        
def SearchGiangVien(tengv):
    conn = DAL_Connect.connect_db()
    qr = "SELECT * FROM tbl_giangvien WHERE tengv LIKE '%"+tengv+"%'"
    cs = conn.cursor()
    cs.execute(qr)
    rs = cs.fetchall()
    conn.close()
    return rs