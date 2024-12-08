import mysql.connector as db
from mysql.connector import Error

def connect_db():
    try:
        connection = db.connect(host='localhost',
                                database='quan_ly_sinh_vien',
                                user='root',
                                password='123456')
        if connection.is_connected():
            return connection
    except Error as e:
        print("Kết nối thất bại", e)
    return connection


def loginApp(username, password):
    db = connect_db()
    query = db.cursor()
    query.execute("select * from tbl_giangvien where username = '{}' and password = '{}'".format(username, password))
    result = query.fetchall()
    db.close()
    return result

def role(username,password):
    db = connect_db()
    query = db.cursor()
    query.execute("select role from tbl_giangvien where username = %s and password = %s", (username, password))
    result = query.fetchall()
    db.close()

    if result:
        print("Role found:", result[0])  # In ra giá trị role
        return result[0]
    else:
        print("No role found for username:", username) 
        return None