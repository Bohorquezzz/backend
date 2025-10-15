import pymysql

try:
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='1234',
        database='UpDaily'
    )
    print("Conexión exitosa a la base de datos")
    connection.close()
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")