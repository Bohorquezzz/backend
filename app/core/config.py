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
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    # App settings
    APP_NAME: str = "UpDaily API"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
