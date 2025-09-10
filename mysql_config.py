"""
Configuración específica para MySQL
"""

from sqlalchemy import create_engine, text
from app.core.config import settings

def test_mysql_connection():
    """Probar conexión a MySQL"""
    try:
        engine = create_engine(settings.DATABASE_URL)
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Conexión a MySQL exitosa")
            return True
    except Exception as e:
        print(f"❌ Error conectando a MySQL: {e}")
        return False

def create_database_if_not_exists():
    """Crear base de datos si no existe"""
    try:
        # Conectar sin especificar base de datos
        temp_url = f"mysql+pymysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/"
        engine = create_engine(temp_url)
        
        with engine.connect() as connection:
            # Crear base de datos si no existe
            connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {settings.MYSQL_DATABASE}"))
            connection.commit()
            print(f"✅ Base de datos '{settings.MYSQL_DATABASE}' creada o verificada")
            return True
    except Exception as e:
        print(f"❌ Error creando base de datos: {e}")
        return False

def show_tables():
    """Mostrar tablas existentes"""
    try:
        engine = create_engine(settings.DATABASE_URL)
        with engine.connect() as connection:
            result = connection.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result]
            print(f"📋 Tablas existentes: {tables}")
            return tables
    except Exception as e:
        print(f"❌ Error mostrando tablas: {e}")
        return []

if __name__ == "__main__":
    print("🔧 Configurando MySQL para UpDaily...")
    
    # Probar conexión
    if test_mysql_connection():
        # Crear base de datos si no existe
        create_database_if_not_exists()
        # Mostrar tablas
        show_tables()
        print("\n🎉 Configuración de MySQL completada!")
    else:
        print("\n❌ No se pudo conectar a MySQL. Verifica la configuración.")
