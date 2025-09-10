"""
Pydantic schemas for Criterio model - Conectado con MySQL
"""

from pydantic import BaseModel
from typing import Optional
from datetime import time

class CriterioBase(BaseModel):
    id_reto: Optional[int] = None
    desc_criterio: Optional[str] = None
    tiempo_est: Optional[time] = None

class CriterioCreate(CriterioBase):
    pass

class CriterioUpdate(BaseModel):
    id_reto: Optional[int] = None
    desc_criterio: Optional[str] = None
    tiempo_est: Optional[time] = None

class CriterioInDB(CriterioBase):
    id: int
    
    class Config:
        from_attributes = True

class Criterio(CriterioInDB):
    pass

class CriterioRetoBase(BaseModel):
    id_reto_usuario: Optional[int] = None
    id_criterio: Optional[int] = None
    completado: Optional[bytes] = None
    fecha_ul_modif: Optional[str] = None  # Date as string
    fecha_prim_ra: Optional[str] = None  # Date as string

class CriterioRetoCreate(CriterioRetoBase):
    pass

class CriterioRetoUpdate(BaseModel):
    completado: Optional[bytes] = None
    fecha_ul_modif: Optional[str] = None
    fecha_prim_ra: Optional[str] = None

class CriterioRetoInDB(CriterioRetoBase):
    id: int
    
    class Config:
        from_attributes = True

class CriterioReto(CriterioRetoInDB):
    pass
