"""
Pydantic schemas for User model - Conectado con MySQL
"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, date

class UserBase(BaseModel):
    nombre: Optional[str] = None
    correo: Optional[EmailStr] = None
    fecha_nacimiento: Optional[date] = None
    telefono: Optional[int] = None

class UserCreate(UserBase):
    clave: str  # Contraseña

class UserUpdate(BaseModel):
    nombre: Optional[str] = None
    correo: Optional[EmailStr] = None
    clave: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    telefono: Optional[int] = None

class UserInDB(UserBase):
    id: int
    img_foto_usuario: Optional[bytes] = None
    
    class Config:
        from_attributes = True

class User(UserInDB):
    pass

class UserLogin(BaseModel):
    correo: EmailStr
    clave: str