from sqlalchemy import create_engine, text

def fix_id_column():
    try:
        # Crear conexión usando SQLAlchemy
        engine = create_engine("mysql+pymysql://root:1234@localhost/updaily")
        
        # Crear conexión
        with engine.connect() as connection:
            # Modificar la columna id para que sea AUTO_INCREMENT
            sql = """
            ALTER TABLE usuario 
            MODIFY COLUMN id INT AUTO_INCREMENT;
            """
            connection.execute(text(sql))
            connection.commit()
            print("Columna id modificada exitosamente a AUTO_INCREMENT")

    except Exception as error:
        print(f"Error: {error}")

if __name__ == "__main__":
    fix_id_column()
