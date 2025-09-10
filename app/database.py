import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",      
        user="root",           
        password="1234",
        database="updaily"     
    )

@app.get("/")
def read_root():
    return {"msg": "API UpDaily funcionando"}

@app.get("/usuarios")
def get_usuarios():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios;")
        result = cursor.fetchall()
        return result
    except Error as e:
        return {"error": str(e)}
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
