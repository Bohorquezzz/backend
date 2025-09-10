"""
CRUD operations for Criterio model - Conectado con MySQL
"""

from sqlalchemy.orm import Session
from app.models.database import Criterio, CriterioReto
from app.schemas.criterio import CriterioCreate, CriterioUpdate, CriterioRetoCreate, CriterioRetoUpdate
from typing import List, Optional

# CRUD para Criterios
def get_criterio(db: Session, criterio_id: int) -> Optional[Criterio]:
    """Get criterio by ID"""
    return db.query(Criterio).filter(Criterio.id == criterio_id).first()

def get_criterios(db: Session, skip: int = 0, limit: int = 100) -> List[Criterio]:
    """Get all criterios"""
    return db.query(Criterio).offset(skip).limit(limit).all()

def get_criterios_by_reto(db: Session, reto_id: int) -> List[Criterio]:
    """Get criterios by reto ID"""
    return db.query(Criterio).filter(Criterio.id_reto == reto_id).all()

def create_criterio(db: Session, criterio: CriterioCreate) -> Criterio:
    """Create new criterio"""
    db_criterio = Criterio(**criterio.dict())
    db.add(db_criterio)
    db.commit()
    db.refresh(db_criterio)
    return db_criterio

def update_criterio(db: Session, criterio_id: int, criterio_update: CriterioUpdate) -> Optional[Criterio]:
    """Update criterio"""
    db_criterio = get_criterio(db, criterio_id)
    if not db_criterio:
        return None
    
    update_data = criterio_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_criterio, field, value)
    
    db.commit()
    db.refresh(db_criterio)
    return db_criterio

def delete_criterio(db: Session, criterio_id: int) -> bool:
    """Delete criterio"""
    db_criterio = get_criterio(db, criterio_id)
    if not db_criterio:
        return False
    
    db.delete(db_criterio)
    db.commit()
    return True

# CRUD para CriterioReto (progreso de criterios en retos de usuario)
def get_criterio_reto(db: Session, criterio_reto_id: int) -> Optional[CriterioReto]:
    """Get criterio_reto by ID"""
    return db.query(CriterioReto).filter(CriterioReto.id == criterio_reto_id).first()

def get_criterios_reto_by_usuario(db: Session, reto_usuario_id: int) -> List[CriterioReto]:
    """Get criterios_reto by reto_usuario ID"""
    return db.query(CriterioReto).filter(CriterioReto.id_reto_usuario == reto_usuario_id).all()

def create_criterio_reto(db: Session, criterio_reto: CriterioRetoCreate) -> CriterioReto:
    """Create new criterio_reto"""
    db_criterio_reto = CriterioReto(**criterio_reto.dict())
    db.add(db_criterio_reto)
    db.commit()
    db.refresh(db_criterio_reto)
    return db_criterio_reto

def update_criterio_reto(db: Session, criterio_reto_id: int, criterio_reto_update: CriterioRetoUpdate) -> Optional[CriterioReto]:
    """Update criterio_reto"""
    db_criterio_reto = get_criterio_reto(db, criterio_reto_id)
    if not db_criterio_reto:
        return None
    
    update_data = criterio_reto_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_criterio_reto, field, value)
    
    db.commit()
    db.refresh(db_criterio_reto)
    return db_criterio_reto

def delete_criterio_reto(db: Session, criterio_reto_id: int) -> bool:
    """Delete criterio_reto"""
    db_criterio_reto = get_criterio_reto(db, criterio_reto_id)
    if not db_criterio_reto:
        return False
    
    db.delete(db_criterio_reto)
    db.commit()
    return True

def mark_criterio_completed(db: Session, criterio_reto_id: int) -> Optional[CriterioReto]:
    """Mark criterio as completed"""
    db_criterio_reto = get_criterio_reto(db, criterio_reto_id)
    if not db_criterio_reto:
        return None
    
    # Marcar como completado (0x01 en binary)
    db_criterio_reto.completado = b'\x01'
    
    db.commit()
    db.refresh(db_criterio_reto)
    return db_criterio_reto
