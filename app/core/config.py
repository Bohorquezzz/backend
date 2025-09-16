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
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    # App settings
    APP_NAME: str = "UpDaily API"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
