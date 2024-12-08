import mysql.connector as db
from . import DAL_Connect

def AddSinhVienInLopHoc(tenlh, gvql,tensv,masv):
    try:
        conn = DAL_Connect.connect_db()
        cs = conn.cursor()
        new_sinhVien = (tenlh,gvql,tensv,masv)
        query = "INSERT INTO tbl_qlylophoc(tenlh,gvql,tensv,masv) VALUES (%s,%s,%s,%s)"
        cs.execute(query,new_sinhVien)
        conn.commit()
        conn.close()
        return cs.rowcount
    except Exception as e:
        print(f"Error: {e}")

def DanhSachSinhVienInLopHoc(tenlophoc):
    conn = DAL_Connect.connect_db()
    qr = "SELECT * FROM tbl_qlylophoc WHERE tenlh LIKE '%"+tenlophoc+"%'"
    cs = conn.cursor()
    cs.execute(qr)
    rs = cs.fetchall()
    conn.close()
    return rs

def DeleteSinhVienInClass(masv):
    try:
        conn = DAL_Connect.connect_db()
        cs = conn.cursor()
        query = "DELETE tbl_qlylophoc FROM tbl_qlylophoc JOIN (SELECT id FROM tbl_qlylophoc WHERE masv = %s) AS temp ON tbl_qlylophoc.id = temp.id;"
        cs.execute(query, (masv,))
        conn.commit()
        conn.close()
        return cs.rowcount
    except Exception as e:
        print(f"Error: {e}")
        return 0
