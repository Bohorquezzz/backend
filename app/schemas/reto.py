"""
Pydantic schemas for Reto model - Conectado con MySQL
"""

from pydantic import BaseModel
from typing import Optional

class RetoBase(BaseModel):
    nombre_reto: Optional[str] = None
    descripcion_reto: Optional[str] = None
    tipo: Optional[int] = None  # 1=simple, 2=progreso, 3=checklist

class RetoCreate(RetoBase):
    pass

class RetoUpdate(BaseModel):
    nombre_reto: Optional[str] = None
    descripcion_reto: Optional[str] = None
    tipo: Optional[int] = None

class RetoInDB(RetoBase):
    id: int
    
    class Config:
        from_attributes = True

class Reto(RetoInDB):
    pass

class RetoUsuarioBase(BaseModel):
    id_usuario: int
    id_reto: int
    progreso_reto: float = 0.0

class RetoUsuarioCreate(RetoUsuarioBase):
    pass

class RetoUsuarioUpdate(BaseModel):
    progreso_reto: Optional[float] = None

class RetoUsuarioInDB(RetoUsuarioBase):
    id: int
    
    class Config:
        from_attributes = True

class RetoUsuario(RetoUsuarioInDB):
    pass
