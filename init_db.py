import pymysql

def init_database():
    # Primero nos conectamos sin especificar una base de datos
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='1234'
    )
    
    try:
        with connection.cursor() as cursor:
            # Crear la base de datos si no existe
            cursor.execute('CREATE DATABASE IF NOT EXISTS updaily')
            print("Base de datos 'updaily' creada o ya existente")
            
            # Usar la base de datos
            cursor.execute('USE updaily')
            print("Usando base de datos 'updaily'")
            
        connection.commit()
        print("Inicialización de la base de datos completada")
        
    except Exception as e:
        print(f"Error durante la inicialización de la base de datos: {e}")
    
    finally:
        connection.close()

if __name__ == "__main__":
    init_database()