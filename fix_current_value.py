from sqlalchemy import create_engine, text
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)

def fix_current_value_column():
    with engine.connect() as connection:
        # Crear nueva columna con valor por defecto
        connection.execute(text("ALTER TABLE challenges ADD COLUMN current_value_new FLOAT NOT NULL DEFAULT 0.0"))
        
        # Copiar los valores existentes, usando 0.0 para los NULL
        connection.execute(text("UPDATE challenges SET current_value_new = COALESCE(current_value, 0.0)"))
        
        # Eliminar la columna antigua
        connection.execute(text("ALTER TABLE challenges DROP COLUMN current_value"))
        
        # Renombrar la nueva columna
        connection.execute(text("ALTER TABLE challenges RENAME COLUMN current_value_new TO current_value"))
        
        connection.commit()
        print("Columna current_value actualizada correctamente")

if __name__ == "__main__":
    fix_current_value_column()