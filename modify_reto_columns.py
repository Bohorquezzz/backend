"""
Script para modificar las columnas de la tabla reto
"""
from sqlalchemy import create_engine, text
from app.core.config import settings

def modify_reto_columns():
    """Modificar las columnas nombre_reto y descripcion_reto a TEXT"""
    try:
        # Crear conexión
        engine = create_engine(settings.DATABASE_URL)
        
        # Modificar columnas
        with engine.connect() as connection:
            # Modificar nombre_reto
            connection.execute(text("ALTER TABLE reto MODIFY COLUMN nombre_reto TEXT"))
            # Modificar descripcion_reto
            connection.execute(text("ALTER TABLE reto MODIFY COLUMN descripcion_reto TEXT"))
            connection.commit()
            print("✅ Columnas modificadas exitosamente")
            return True
    except Exception as e:
        print(f"❌ Error modificando columnas: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Modificando columnas de la tabla reto...")
    modify_reto_columns()