"""
Pydantic schemas for Logro model - Conectado con MySQL
"""

from pydantic import BaseModel
from typing import Optional

class LogroBase(BaseModel):
    id_reto_usuario: Optional[int] = None

class LogroCreate(LogroBase):
    pass

class LogroUpdate(BaseModel):
    id_reto_usuario: Optional[int] = None

class LogroInDB(LogroBase):
    id: int
    
    class Config:
        from_attributes = True

class Logro(LogroInDB):
    pass

class LogroWithDetails(Logro):
    """Logro con información detallada del reto y usuario"""
    reto_usuario: Optional[dict] = None
    reto: Optional[dict] = None
    usuario: Optional[dict] = None
