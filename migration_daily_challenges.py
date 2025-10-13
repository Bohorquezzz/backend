"""
Script de migración para agregar las tablas de retos diarios
"""

from sqlalchemy import create_engine, text
from app.core.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_daily_challenge_tables():
    """Crear las tablas para retos diarios"""
    
    # Configurar conexión a la base de datos
    database_url = f"mysql+pymysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DATABASE}"
    engine = create_engine(database_url)
    
    # SQL para crear las tablas
    create_tables_sql = """
    -- Tabla para retos diarios automáticos
    CREATE TABLE IF NOT EXISTS daily_challenges (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        reto_id INT NOT NULL,
        challenge_date DATE NOT NULL,
        is_completed BOOLEAN DEFAULT FALSE,
        completed_at DATETIME NULL,
        progress_value FLOAT DEFAULT 0.0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_user_date (user_id, challenge_date),
        INDEX idx_date (challenge_date),
        FOREIGN KEY (user_id) REFERENCES usuario(id) ON DELETE CASCADE,
        FOREIGN KEY (reto_id) REFERENCES reto(id) ON DELETE CASCADE
    );
    
    -- Tabla para plantillas de retos diarios
    CREATE TABLE IF NOT EXISTS daily_challenge_templates (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        descripcion TEXT,
        tipo INT NOT NULL,
        categoria VARCHAR(50),
        dificultad INT DEFAULT 1,
        puntos_recompensa INT DEFAULT 10,
        is_active BOOLEAN DEFAULT TRUE,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_categoria (categoria),
        INDEX idx_dificultad (dificultad),
        INDEX idx_active (is_active)
    );
    """
    
    try:
        with engine.connect() as connection:
            # Ejecutar el SQL
            connection.execute(text(create_tables_sql))
            connection.commit()
            
        logger.info("✅ Tablas de retos diarios creadas exitosamente")
        
        # Verificar que las tablas se crearon
        with engine.connect() as connection:
            result = connection.execute(text("SHOW TABLES LIKE 'daily_%'"))
            tables = result.fetchall()
            
            logger.info(f"Tablas creadas: {[table[0] for table in tables]}")
            
    except Exception as e:
        logger.error(f"❌ Error creando tablas: {str(e)}")
        raise
    
    finally:
        engine.dispose()

if __name__ == "__main__":
    create_daily_challenge_tables()
