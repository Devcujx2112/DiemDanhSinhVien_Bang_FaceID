import mysql.connector as db
from . import DAL_Connect

def ShowAllLopHoc():
    try:
        conn = DAL_Connect.connect_db()
        query = "SELECT * FROM tbl_lophoc"
        cs = conn.cursor()
        cs.execute(query)
        result = cs.fetchall()  
        return result
    except Exception as e:
        print(f"Error: {e}")  
        return [] 
    finally:
        conn.close()

def AddLopHoc(malop,magv,tenlophoc,sotin):
    try:
        conn = DAL_Connect.connect_db()
        cs = conn.cursor()
        new_lopHoc = (malop,magv,tenlophoc,sotin)
        query = "INSERT INTO tbl_lophoc(malop,magv,tenlophoc,sotin) VALUES (%s,%s,%s,%s)"
        cs.execute(query,new_lopHoc)
        conn.commit()
        conn.close()
        return cs.rowcount
    except Exception as e:
        print(f"Error: {e}")

def DeleteLopHoc(malop):
    try:
        conn = DAL_Connect.connect_db()
        cs = conn.cursor()
        query = "DELETE FROM tbl_lophoc WHERE malop = %s"
        cs.execute(query,(malop,))
        conn.commit()
        conn.close()
        return cs.rowcount
    except Exception as e:
        print(f"Error: {e}")

def UpdateLopHoc(magv,tenlophoc,sotin,malop):
    try:
        conn = DAL_Connect.connect_db()
        cs = conn.cursor()
        new_lopHoc = (magv,tenlophoc,sotin,malop)
        query = "UPDATE tbl_lophoc SET magv = %s, tenlophoc = %s, sotin = %s WHERE malop = %s"
        cs.execute(query,new_lopHoc)
        conn.commit()
        conn.close()
        return cs.rowcount
    except Exception as e:
        print(f"Error: {e}")

def SearchLopHoc(tenlop):
    try:
        conn = DAL_Connect.connect_db()
        query = "SELECT * FROM tbl_lophoc WHERE tenlophoc LIKE %s"
        cs = conn.cursor()
        cs.execute(query,('%'+tenlop+'%',))
        result = cs.fetchall()
        return result
    except Exception as e:
        print(f"Error: {e}")
        return []