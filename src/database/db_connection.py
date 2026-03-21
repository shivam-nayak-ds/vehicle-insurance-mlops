import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",  
        password="SHIvam2005@$",
        database="insurance_db",
        port=3306
    )
    return conn


if __name__ == "__main__":
    try:
        conn = get_connection()
        print("MySQL Connected Successfully ")
        conn.close()
    except Exception as e:
        print(" Error:", e)