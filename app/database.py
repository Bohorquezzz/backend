from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:1234@localhost/updaily"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency for database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def init_db():
    """Initialize database and create tables"""
    try:
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        if db:
            print("Database connection successful")
            db.close()
            return True
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise e
