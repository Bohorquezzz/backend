from sqlalchemy import create_engine, text

def update_table():
    try:
        # Crear conexión usando SQLAlchemy
        engine = create_engine("mysql+pymysql://root:1234@localhost/updaily")
        
        # Crear conexión
        with engine.connect() as connection:
            # Modificar la columna
            connection.execute(text("ALTER TABLE usuario MODIFY COLUMN clave VARCHAR(255);"))
            connection.commit()
            print("Columna modificada exitosamente")

    except Exception as error:
        print(f"Error: {error}")

if __name__ == "__main__":
    update_table()
