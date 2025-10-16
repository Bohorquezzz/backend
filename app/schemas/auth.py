"""
Authentication schemas
"""

from pydantic import BaseModel, EmailStr
from typing import Optional

class UserLogin(BaseModel):
    correo: EmailStr
    clave: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    correo: Optional[str] = None

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    refresh: bool = False

class RefreshToken(BaseModel):
    refresh_token: str
