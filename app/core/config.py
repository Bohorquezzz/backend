"""
Configuration settings for UpDaily API
"""

from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/UpDaily"
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "1234"
    MYSQL_DATABASE: str = "updaily"
    
    # Security
    SECRET_KEY: str = "updaily-secret-key-2024-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:8080",      # Kotlin local development
        "http://127.0.0.1:8080",      # Alternative localhost
        "http://10.0.2.2:8080",       # Android Emulator
        "http://localhost:3000",      # Para desarrollo web
        "capacitor://localhost",      # Para aplicaciones Capacitor
        "http://192.168.1.*",        # IPs locales
        "*"                          # Desarrollo (remover en producción)
    ]
    ALLOW_METHODS: List[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]
    ALLOW_HEADERS: List[str] = [
        "Content-Type",
        "Authorization",
        "Accept",
        "Origin",
        "X-Requested-With"
    ]
    
    # App settings
    APP_NAME: str = "UpDaily API"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
