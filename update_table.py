from sqlalchemy import create_engine, text

def update_table():
    try:
        # Crear conexión usando SQLAlchemy
        engine = create_engine("mysql+pymysql://root:1234@localhost/updaily")
        
        # Crear conexión
        with engine.connect() as connection:
            # Añadir columnas necesarias para el sistema de retos
            # Add categoria column
            try:
                connection.execute(text("""
                    ALTER TABLE reto 
                    ADD COLUMN categoria ENUM('SOCIAL', 'FISICA', 'INTELECTUAL') 
                    NOT NULL DEFAULT 'SOCIAL'
                """))
                print("Added categoria column")
            except Exception as e:
                if "Duplicate column name" not in str(e):
                    raise e
                print("categoria column already exists")

            # Add fecha_asignacion column
            try:
                connection.execute(text("""
                    ALTER TABLE reto 
                    ADD COLUMN fecha_asignacion DATE 
                    DEFAULT (CURRENT_DATE)
                """))
                print("Added fecha_asignacion column")
            except Exception as e:
                if "Duplicate column name" not in str(e):
                    raise e
                print("fecha_asignacion column already exists")

            # Add activo column
            try:
                connection.execute(text("""
                    ALTER TABLE reto 
                    ADD COLUMN activo BOOLEAN 
                    DEFAULT TRUE
                """))
                print("Added activo column")
            except Exception as e:
                if "Duplicate column name" not in str(e):
                    raise e
                print("activo column already exists")
            connection.commit()
            print("Columnas añadidas exitosamente")

    except Exception as error:
        print(f"Error: {error}")

if __name__ == "__main__":
    update_table()
