from sqlalchemy import create_engine, inspect, text
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
inspector = inspect(engine)

# Obtener la información de las columnas directamente de MySQL
with engine.connect() as connection:
    result = connection.execute(text("DESCRIBE reto"))
    for row in result:
        print(f"Column: {row[0]}, Type: {row[1]}")