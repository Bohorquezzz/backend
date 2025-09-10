"""
Authentication schemas
"""

from pydantic import BaseModel, EmailStr

class UserLogin(BaseModel):
    correo: EmailStr
    clave: str
