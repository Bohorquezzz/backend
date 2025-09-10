import mysql.connector
from mysql.connector import Error
import asyncio
from contextlib import contextmanager

def get_connection():
    return mysql.connector.connect(
        host="localhost",      
        user="root",           
        password="1234",
        database="updaily"     
    )

@contextmanager
def get_db():
    """Context manager for database connections"""
    conn = get_connection()
    try:
        yield conn
    finally:
        if conn.is_connected():
            conn.close()

async def init_db():
    """Initialize database connection and verify it's working"""
    try:
        with get_db() as conn:
            if conn.is_connected():
                print("Database connection successful")
                return True
    except Error as e:
        print(f"Error connecting to database: {e}")
        raise e
